---
type: docs
title: '2.2 저장 및 실행 구조'
weight: 20
toc: true
---
Machbase DBMS 내부에서 데이터가 어떻게 저장되고 SQL이 어떻게 실행되는지를 개념 수준에서 다룹니다. 성능 튜닝과 시스템 운영에서 올바른 판단을 내리기 위한 배경지식입니다.

- **[Machbase 아키텍처 개요](/dbms/core-concepts/storage-execution-architecture/#architecture-machbase)** -- SQL 엔진, 저장 관리자, 프로세스 관리자의 역할과 Standard/Cluster Edition의 구조적 차이
- **[컬럼형 저장과 압축](/dbms/core-concepts/storage-execution-architecture/#storage-columnar-compression-column)** -- 행 지향 저장과의 차이, 시계열 데이터에서 컬럼 압축이 효과적인 이유, 파티션 구조
- **[인덱싱 기본 원리](/dbms/core-concepts/storage-execution-architecture/#indexing-basics)** -- 테이블 유형별 인덱스 특성(TAG 파티션 인덱스, LOG LSM 인덱스, VOLATILE Red-Black 트리)
- **[Cache와 실행 계획 개념](/dbms/core-concepts/storage-execution-architecture/#execution-concepts-plan-cache)** -- SQL 실행 과정과 Plan Cache, PVO Cache의 역할


<a id="architecture-machbase"></a>

## Machbase 아키텍처 개요

내부 구조를 이해하면 테이블 설계, 쿼리 작성, 성능 튜닝에서 더 나은 판단을 내릴 수 있습니다.

### 주요 구성 요소

Machbase는 세 가지 핵심 구성 요소로 이루어져 있습니다.

**쿼리 프로세서 (QP, Query Processor)**

클라이언트로부터 SQL 문장을 수신해 파싱하고, 실행 계획을 생성한 뒤 저장 관리자에 요청을 전달합니다. Plan Cache를 통해 반복 쿼리의 파싱 오버헤드를 줄입니다.

**저장 관리자 (SM, Storage Manager)**

실제 데이터의 읽기와 쓰기를 담당합니다. 컬럼 단위로 데이터를 파티션에 저장하고, 인덱스를 관리하며, 압축을 수행합니다. 시계열 데이터의 핵심 성능은 SM의 컬럼형 파티션 구조에서 나옵니다.

TRANSACTION 테이블은 관계형 row 데이터를 다루기 위해 별도 TRANSACTION 저장 경로를 사용합니다. 사용자는 같은
Machbase SQL로 접근하지만, LOG/TAG의 컬럼형 시계열 저장 구조와 TRANSACTION 테이블의 row/index 저장
구조는 구분해서 이해해야 합니다.

**프로세스 관리자 (PM, Process Manager)**

서버의 생명주기(기동, 종료)와 내부 배경 작업(ROLLUP 집계, Retention 삭제, 인덱스 병합 등)을 관리합니다.

### Standard Edition 구조

Standard Edition은 QP, SM, PM을 모두 포함하는 단일 `machbase` 프로세스로 동작합니다.

```
클라이언트 (machsql, SDK, ODBC/JDBC)
        │
        ▼
   [machbase 프로세스]
   ┌──────────────────────────────┐
   │  Query Processor (QP)       │
   │  · SQL 파싱 / 최적화         │
   │  · Plan Cache                │
   │                              │
   │  Storage Manager (SM)        │
   │  · 컬럼형 파티션 저장         │
   │  · 인덱스 관리               │
   │  · 압축                      │
   │                              │
   │  Process Manager (PM)        │
   │  · ROLLUP / Retention / 병합 │
   └──────────────────────────────┘
        │
        ▼
   [디스크: 컬럼 파티션 파일]
```

### Cluster Edition 구조

Cluster Edition은 여러 노드 유형이 역할을 분담합니다.

```
클라이언트
    │
    ▼
[Broker 노드]  ←── [Coordinator 노드]
    │                (메타데이터, 노드 감시)
    ├──────────────────────────────┐
    ▼                              ▼
[Warehouse 노드 1]      [Warehouse 노드 2]
(데이터 샤드 A)          (데이터 샤드 B)
```

클라이언트는 항상 Broker에 접속합니다. Broker는 Coordinator로부터 클러스터 메타데이터를 받아 쿼리를 해당 데이터를 보유한 Warehouse 노드로 라우팅합니다. Deployer 노드는 소프트웨어 배포와 노드 초기화에 사용하며, 일상 운영에서는 직접 접촉하지 않습니다.

LOOKUP 테이블 처리를 위한 Lookup 노드도 Cluster Edition 구성에 포함됩니다. Warehouse가 대용량 시계열 데이터를 나누어 처리하고, Lookup 노드는 클러스터 전역에서 참조되는 기준 정보 처리를 담당합니다.

### 데이터 흐름: 쓰기

1. 클라이언트가 SQL INSERT 또는 Append API로 데이터를 전송
2. QP가 대상 테이블과 컬럼을 파악해 SM에 전달
3. LOG/TAG 테이블이면 SM이 해당 시간 파티션의 컬럼 파일에 데이터를 append
4. 충분한 데이터가 쌓이면 배경 스레드가 압축 및 인덱스 병합 수행

TRANSACTION 테이블의 `INSERT`/`UPDATE`/`DELETE`는 append-only 시계열 경로가 아니라 TRANSACTION 저장 경로에서
행 단위 DML로 처리됩니다.

### 데이터 흐름: 읽기

1. 클라이언트가 SELECT 쿼리 전송
2. QP가 파싱 후 실행 계획 수립 (Plan Cache 활용)
3. LOG/TAG 테이블이면 SM이 시간 범위에 해당하는 파티션만 선택 (파티션 pruning)
4. 필요한 컬럼 파일만 읽어 집계 또는 필터 적용
5. QP가 결과를 클라이언트에 반환

### 다음 읽을 내용

- [컬럼형 저장과 압축](/dbms/core-concepts/storage-execution-architecture/#storage-columnar-compression-column) -- SM의 저장 구조 상세
- [인덱싱 기본 원리](/dbms/core-concepts/storage-execution-architecture/#indexing-basics) -- 테이블 유형별 인덱스 구조
- [Cache와 실행 계획 개념](/dbms/core-concepts/storage-execution-architecture/#execution-concepts-plan-cache) -- QP의 캐시와 실행 계획 관리
- [Standard Edition과 Cluster Edition 차이](/dbms/core-concepts/concepts-edition/#differences-standard-edition-cluster) -- 두 Edition의 선택 기준

<a id="storage-columnar-compression-column"></a>

## 컬럼형 저장과 압축

LOG/TAG 테이블의 저장 성능과 압축 효율은 컬럼 지향(columnar) 저장 구조에서 비롯됩니다. 시계열 데이터의 특성이 컬럼형 저장과 만날 때 왜 뛰어난 성능이 나오는지를 이해하면, 테이블 설계와 쿼리 최적화 방향을 더 명확하게 잡을 수 있습니다. TRANSACTION 테이블은 별도 row/index 저장 구조를 사용하므로 여기서 설명하는 컬럼형 저장을 그대로 적용하지 않습니다.

### 행 지향 vs 컬럼 지향

전통적인 RDBMS는 행 지향(row-oriented) 저장을 사용합니다. 한 행의 모든 컬럼 값이 디스크에 연속으로 기록됩니다.

```
행 지향 저장:
[time1, sensor_A, 23.1] [time2, sensor_A, 23.5] [time3, sensor_B, 18.0] ...
```

컬럼 지향 저장에서는 같은 컬럼의 값들이 연속으로 기록됩니다.

```
컬럼 지향 저장:
[time1, time2, time3, ...] | [sensor_A, sensor_A, sensor_B, ...] | [23.1, 23.5, 18.0, ...]
```

이 차이는 시계열 집계 쿼리에서 결정적입니다. "모든 센서의 온도 평균"을 계산할 때, 행 지향은 각 행 전체를 읽어야 하지만 컬럼 지향은 온도 컬럼 파일만 읽으면 됩니다.

### 시계열 데이터에서 압축이 효과적인 이유

컬럼형 저장이 시계열 데이터에서 특히 높은 압축률을 달성하는 이유는 두 가지입니다.

**값의 유사성**

같은 센서가 짧은 간격으로 측정한 온도값은 서로 비슷합니다(예: 23.1, 23.2, 23.1, 23.0). 이런 값들이 연속 저장되면 델타 인코딩이나 런-렝스 인코딩 같은 압축 알고리즘이 높은 비율로 압축합니다.

**타임스탬프의 순차성**

시계열 타임스탬프는 단조 증가합니다. 연속된 타임스탬프 간의 차이(델타)가 일정한 경우가
많아 델타 기반 압축을 적용하기에 적합합니다.

실제 압축률은 데이터 타입, 값의 반복성, 입력 순서와 분포에 따라 달라집니다.

### 시간 기반 파티셔닝

데이터를 시간 기준으로 파티션에 나누어 저장합니다. 파티션은 일정 시간 범위의 데이터를 담는 독립적인 컬럼 파일 집합입니다.

시간 범위 조건(`WHERE time BETWEEN ... AND ...`)이 포함된 쿼리는 해당 범위에 속하는 파티션만 읽습니다. 이를 파티션 pruning이라 하며, 전체 데이터의 일부만 I/O하므로 조회 성능이 크게 향상됩니다.

```
[파티션 1: 2026-07-01]  [파티션 2: 2026-07-02]  [파티션 3: 2026-07-03]
       ▲ 이 파티션만 읽음
WHERE time >= '2026-07-01' AND time < '2026-07-02'
```

### 읽기 성능 이점 요약

| 항목 | 행 지향 (RDBMS) | 컬럼 지향 (Machbase) |
| --- | --- | --- |
| 집계 쿼리 I/O | 전체 행 스캔 | 필요 컬럼만 읽음 |
| 압축 | 행 단위 데이터 특성에 따라 결정 | 컬럼별 반복 패턴을 활용 |
| 시간 범위 조회 | 전체 스캔 | 파티션 pruning |
| 단건 키 조회 | 빠름 | 상대적으로 느림 |

컬럼 지향 저장은 특정 키의 단건 조회보다 시간 범위 집계와 필요한 컬럼만 읽는 분석 쿼리에
적합합니다.

### 다음 읽을 내용

- [인덱싱 기본 원리](/dbms/core-concepts/storage-execution-architecture/#indexing-basics) -- 컬럼 저장 위에서 동작하는 인덱스 구조
- [Machbase 아키텍처 개요](/dbms/core-concepts/storage-execution-architecture/#architecture-machbase) -- 저장 관리자(SM)와 데이터 흐름
- [기존 RDBMS와의 차이](/dbms/core-concepts/concepts-edition/#differences-rdbms) -- 저장 방식 차이의 전체 맥락

<a id="indexing-basics"></a>

## 인덱싱 기본 원리

테이블 타입은 저장 역할에 맞는 서로 다른 접근 구조를 사용합니다.

| 범주 | 개념 |
|---|---|
| TAG | 태그와 축 범위를 이용해 시계열 partition을 제한 |
| LOG | 수신 시간 경로와 필요 시 생성한 검색 index를 사용 |
| TRANSACTION | primary·unique·일반 index로 관계형 key를 조회 |
| LOOKUP·VOLATILE | memory-resident key와 보조 index를 사용 |

이 장은 저장 구조의 차이만 설명합니다. 컬럼·key·index 설계는 [스키마 객체 정의](../../data-modeling-table-design/schema-objects-definition/)를, 실제 생성과 측정은 [인덱스 튜닝](../../performance-tuning/index-tuning/)을 참고하십시오. Min-Max·PVO Cache의 설정과 기본값은 [캐시와 메모리 튜닝](../../performance-tuning/cache-tuning-memory/)을 정본으로 사용합니다.

<a id="execution-concepts-plan-cache"></a>

## Cache와 실행 계획 개념

반복적인 SQL 처리 비용을 줄이기 위해 여러 레벨의 캐시를 운용합니다. 각 캐시의 역할을 이해하면 시스템 설정 조정과 성능 문제 진단에 도움이 됩니다.

### SQL 실행 과정

SQL 문장이 Machbase에 도달해 결과가 반환되기까지 다음 단계를 거칩니다.

```
클라이언트 SQL
      │
      ▼
  1. 파싱 (Parsing)
     SQL 문장을 파스 트리로 변환
      │
      ▼
  2. 최적화 (Optimization)
     파스 트리를 분석해 최적 실행 경로 결정
     (인덱스 사용 여부, 파티션 pruning 범위 등)
      │
      ▼
  3. 실행 계획 생성 (Plan Generation)
     최적화 결과를 실행 가능한 계획으로 변환
      │
      ▼
  4. 실행 (Execution)
     저장 관리자(SM)에 데이터 읽기/쓰기 요청
      │
      ▼
  결과 반환
```

파싱과 최적화는 동일한 SQL이 반복 실행될 때마다 중복 수행될 수 있으며, 캐시는 이 중복 비용을 제거합니다.

### Plan Cache

SQL 문장의 실행 계획을 메모리에 저장해 두고, 같은 SQL이 다시 들어오면 파싱과 최적화 단계를 생략하고 저장된 계획을 재사용합니다.

실시간 수집 환경에서는 동일한 INSERT나 SELECT 패턴이 반복되므로, Plan Cache가 파싱 CPU 비용을 크게 줄입니다. 서버 기동 후 자동으로 운용되며 별도 설정이 필요 없습니다.

### PVO Cache

동일한 SQL의 파싱과 최적화 결과를 재사용할 수 있도록 실행 계획을 메모리에 저장합니다.
Standard Edition에서 지원하며, SELECT 결과 row를 저장하는 캐시는 아닙니다. 설정과 상태 확인은
[PVO Cache와 메모리 튜닝](/dbms/performance-tuning/cache-tuning-memory/#pvo-cache)을
참고하십시오.

### EXPLAIN으로 실행 계획 확인

`EXPLAIN` 문으로 쿼리가 실제로 어떤 실행 계획을 사용하는지 확인합니다.

```sql
EXPLAIN SELECT AVG(value)
FROM sensor_values
WHERE name = 'temp_sensor_01'
  AND time BETWEEN TO_DATE('2026-07-01', 'YYYY-MM-DD')
               AND TO_DATE('2026-07-03', 'YYYY-MM-DD');
```

실행 계획 출력에서 파티션 pruning 적용 여부, 인덱스 사용 여부, RS Cache 히트 여부를 확인합니다. 성능이 기대에 못 미칠 때 `EXPLAIN`을 먼저 실행해 실행 경로를 검토하십시오.

### 다음 읽을 내용

- [인덱싱 기본 원리](/dbms/core-concepts/storage-execution-architecture/#indexing-basics) -- 실행 계획에서 인덱스가 사용되는 원리
- [Machbase 아키텍처 개요](/dbms/core-concepts/storage-execution-architecture/#architecture-machbase) -- 쿼리 프로세서(QP)의 역할
- [컬럼형 저장과 압축](/dbms/core-concepts/storage-execution-architecture/#storage-columnar-compression-column) -- 실행 계획이 읽는 저장 구조
