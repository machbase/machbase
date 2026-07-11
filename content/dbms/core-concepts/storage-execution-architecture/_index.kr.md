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
- **[Cache와 실행 계획 개념](/dbms/core-concepts/storage-execution-architecture/#execution-concepts-plan-cache)** -- SQL 실행 과정과 Plan Cache, Result Cache, PVO Cache의 역할


<a id="architecture-machbase"></a>

## Machbase 아키텍처 개요

내부 구조를 이해하면 테이블 설계, 쿼리 작성, 성능 튜닝에서 더 나은 판단을 내릴 수 있습니다.

### 주요 구성 요소

Machbase는 세 가지 핵심 구성 요소로 이루어져 있습니다.

**쿼리 프로세서 (QP, Query Processor)**

클라이언트로부터 SQL 문장을 수신해 파싱하고, 실행 계획을 생성한 뒤 저장 관리자에 요청을 전달합니다. Plan Cache를 통해 반복 쿼리의 파싱 오버헤드를 줄입니다.

**저장 관리자 (SM, Storage Manager)**

실제 데이터의 읽기와 쓰기를 담당합니다. 컬럼 단위로 데이터를 파티션에 저장하고, 인덱스를 관리하며, 압축을 수행합니다. 시계열 데이터의 핵심 성능은 SM의 컬럼형 파티션 구조에서 나옵니다.

RDB 테이블은 관계형 row 데이터를 다루기 위해 별도 RDB 저장 경로를 사용합니다. 사용자는 같은
Machbase SQL로 접근하지만, LOG/TAG의 컬럼형 시계열 저장 구조와 RDB 테이블의 row/index 저장
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

1. 클라이언트가 SQL INSERT 또는 APPEND 프로토콜로 데이터를 전송
2. QP가 대상 테이블과 컬럼을 파악해 SM에 전달
3. LOG/TAG 테이블이면 SM이 해당 시간 파티션의 컬럼 파일에 데이터를 append
4. 충분한 데이터가 쌓이면 배경 스레드가 압축 및 인덱스 병합 수행

RDB 테이블의 `INSERT`/`UPDATE`/`DELETE`는 append-only 시계열 경로가 아니라 RDB 저장 경로에서
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

LOG/TAG 테이블의 저장 성능과 압축 효율은 컬럼 지향(columnar) 저장 구조에서 비롯됩니다. 시계열 데이터의 특성이 컬럼형 저장과 만날 때 왜 뛰어난 성능이 나오는지를 이해하면, 테이블 설계와 쿼리 최적화 방향을 더 명확하게 잡을 수 있습니다. RDB 테이블은 별도 row/index 저장 구조를 사용하므로 여기서 설명하는 컬럼형 저장을 그대로 적용하지 않습니다.

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

테이블 유형에 따라 서로 다른 인덱스 구조를 사용합니다. 어떤 인덱스가 어떤 조회 패턴에 적합한지 파악하면, 불필요한 인덱스 생성을 피하고 최적의 조회 성능을 달성할 수 있습니다.

### TAG 테이블: 자동 3단계 파티션 인덱스

TAG 테이블은 별도의 `CREATE INDEX` 없이도 자동으로 3단계 인덱스를 구성합니다.

```
태그명 (PRIMARY KEY)
  └──► 시간 파티션 범위
          └──► 파티션 내 컬럼 값
```

"sensor_A의 2026-07-03 데이터"를 조회하면 태그명으로 해당 태그의 파티션 목록을 찾고, 시간 범위로 대상 파티션을 좁힌 뒤, 그 파티션에서 컬럼 값을 읽습니다. 대규모 TAG 테이블에서 태그명과 시간 범위가 명시된 조회는 항상 최소한의 I/O로 처리됩니다.

### LOG 테이블: LSM 인덱스 (선택적 생성)

LOG 테이블은 기본적으로 `_arrival_time` 기준의 순차 저장 구조를 사용합니다. `_arrival_time`을 조건으로 사용하면 파티션 pruning으로 해당 시간 범위만 스캔합니다.

특정 컬럼에 빠른 조회가 필요하면 LSM(Log-Structured Merge-tree) 인덱스를 명시적으로 생성합니다.

```sql
-- LOG 테이블의 device_id 컬럼에 인덱스 생성
CREATE INDEX idx_device ON device_log (device_id);
```

LSM 인덱스는 삽입 시 메모리 내 구조에 먼저 기록되고, 배경 스레드가 주기적으로 디스크의 정렬된 파일로 병합합니다. 순차 삽입이 많은 환경에서 B-Tree보다 삽입 성능이 우수하지만, 데이터 병합 중 I/O 부하가 일시 증가할 수 있습니다.

**KEYWORD 인덱스**: 긴 텍스트 컬럼에서 단어 검색이 필요한 경우 사용합니다.

```sql
CREATE INDEX idx_msg ON device_log (message) INDEX_TYPE KEYWORD;
```

### LOOKUP 테이블: 영속 저장 + 메모리 Red-Black 인덱스

LOOKUP 테이블의 데이터는 영속 저장되지만, 서버 기동 시 모든 행을 메모리 row 테이블로
복원하고 PRIMARY KEY 컬럼의 Red-Black 트리 인덱스를 구성합니다. Primary key를 key, 나머지
행 값을 value로 보는 조회 특화 구조이며, SQL 조회는 메모리 행과 인덱스를 사용합니다.

따라서 LOOKUP은 재시작 후에도 데이터를 유지하면서 빠른 key 조회를 제공하지만, 전체 행과
보조 인덱스가 서버 메모리를 사용합니다. 메모리에 상주시킬 수 있는 기준 정보에 사용하고,
대규모 관계형 데이터에는 RDB 테이블을 검토합니다.

### VOLATILE 테이블: Red-Black 트리 인덱스

VOLATILE 테이블은 메모리 기반이며, PRIMARY KEY 컬럼에 자동으로 Red-Black 트리 인덱스가 생성됩니다. 메모리에서 동작하므로 삽입과 조회 모두 빠르지만, 서버 재시작 시 데이터가 사라집니다.

### RDB 테이블: 일반/Unique/Primary Key 인덱스

RDB 테이블은 관계형 row 데이터를 위한 테이블입니다. `CREATE RDB TABLE`로 생성하며, 일반 인덱스,
Unique 인덱스, Primary Key 인덱스를 사용합니다. Primary key 없이 테이블을 만든 뒤
`CREATE PRIMARY KEY INDEX`로 사후 추가할 수도 있습니다.

RDB 인덱스는 LOG/TAG의 시간 파티션이나 append-only 입력 경로와 별개로 동작합니다. 단건 키
조회, 업무 기준 정보 조회, 관계형 조인에 필요한 컬럼에 인덱스를 생성합니다.

### 인덱스를 만들어야 할 때와 만들지 말아야 할 때

**인덱스가 유용한 경우**

- LOG 테이블에서 `_arrival_time` 이외의 컬럼(예: 장치 ID, 이벤트 유형)으로 자주 필터링하는 경우
- 텍스트 컬럼에서 특정 단어를 포함하는 행을 검색하는 경우 (KEYWORD 인덱스)

**인덱스 생성을 피해야 하는 경우**

- 입력 속도가 최우선이고 조회 빈도가 낮은 경우 (인덱스 유지 오버헤드 발생)
- 카디널리티가 낮은 컬럼 (예: TRUE/FALSE 구분값) -- 인덱스 효과 없음
- TAG 테이블 -- 이미 자동 파티션 인덱스가 있으므로 추가 인덱스 불필요

### Min-Max Cache

#### 개념

Machbase는 시계열 데이터를 시간순으로 파티션된 구조로 저장합니다. 특정 값을 인덱스로 검색할 때, 이 파티션 파일들을 순차적으로 열어 검색해야 합니다. 파티션이 1,000개라면 최악의 경우 1,000번의 파일 I/O가 발생합니다.

**Min-Max Cache**는 각 파티션의 특정 컬럼에 대해 최솟값·최댓값을 메모리에 유지하여, 검색 대상 값이 해당 파티션의 범위를 벗어나면 파티션 자체를 건너뛰는 메모리 구조입니다.

```
[파티션 1] MIN=10, MAX=50  →  검색값 85 → 건너뜀
[파티션 2] MIN=60, MAX=80  →  검색값 85 → 건너뜀
[파티션 3] MIN=80, MAX=95  →  검색값 85 → 스캔 ✓
[파티션 4] MIN=20, MAX=40  →  검색값 85 → 건너뜀
[파티션 5] MIN=75, MAX=90  →  검색값 85 → 스캔 ✓
```

#### 설정

컬럼별 Min-Max Cache 크기는 `PROPERTY(MINMAX_CACHE_SIZE = n)` 옵션으로 지정합니다.

```sql
-- id 컬럼에 Min-Max Cache 적용 (20KB)
CREATE TABLE ctest (
    id   INTEGER PROPERTY(MINMAX_CACHE_SIZE = 20480),
    name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE = 0)  -- VARCHAR는 0만 허용
);
```

#### 기본값과 규칙

| 항목 | 기본값 |
|------|--------|
| 일반 컬럼 MINMAX_CACHE_SIZE | 10KB (10240 bytes) |
| `_ARRIVAL_TIME` (숨김 컬럼) | 100MB (자동 적용) |
| VARCHAR 컬럼 | 0 고정 (캐시 미지원) |

- Min-Max Cache는 명시적으로 인덱스를 생성하지 않아도 동작합니다.
- `ALTER TABLE ... MODIFY COLUMN ... SET MINMAX_CACHE_SIZE = n`으로 생성 후 변경 가능합니다.
- 레코드가 없는 테이블은 Min-Max Cache 메모리를 할당하지 않습니다.
- 파티션 수가 증가할수록 설정된 크기만큼 메모리가 점진적으로 증가합니다.
- VARCHAR 타입에 MINMAX_CACHE_SIZE를 0 이외의 값으로 설정하면 오류가 발생합니다.

```sql
-- 생성 후 캐시 크기 변경
ALTER TABLE ctest MODIFY COLUMN id SET MINMAX_CACHE_SIZE = 20480;
```

### 다음 읽을 내용

- [컬럼형 저장과 압축](/dbms/core-concepts/storage-execution-architecture/#storage-columnar-compression-column) -- 인덱스가 동작하는 저장 구조
- [Cache와 실행 계획 개념](/dbms/core-concepts/storage-execution-architecture/#execution-concepts-plan-cache) -- 인덱스를 활용하는 실행 계획 최적화
- [Machbase 아키텍처 개요](/dbms/core-concepts/storage-execution-architecture/#architecture-machbase) -- 인덱스와 저장 관리자의 관계

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

### Result Cache (RS Cache)

SELECT 쿼리의 결과 자체를 캐시합니다. 동일한 쿼리가 짧은 시간 내에 반복 실행될 때, 저장소에서 데이터를 다시 읽지 않고 캐시된 결과를 즉시 반환합니다.

RS Cache는 기본적으로 비활성화되어 있으며, 설정 파일 또는 SQL로 활성화합니다.

```sql
-- RS Cache 활성화 여부 확인
SELECT * FROM M$SYS_CACHE;

-- 세션 수준에서 RS Cache 활성화
SET RS_CACHE_ENABLE = 1;
```

대시보드처럼 동일 쿼리를 짧은 주기로 반복하는 환경에서 유용합니다. 단, 데이터가 자주 변하는 테이블에 적용하면 오래된 결과가 반환될 수 있으므로, 정책적으로 허용 가능한 경우에만 활성화하십시오.

### PVO Cache (파티션 메타데이터 캐시)

TAG 테이블의 파티션 메타데이터를 메모리에 보관합니다. TAG 테이블 조회 시 어떤 파티션을 읽어야 하는지 결정하는 데 필요한 메타데이터를 매번 디스크에서 읽지 않고 메모리에서 즉시 참조합니다.

서버 기동 시 자동으로 로드되며, TAG 테이블 조회가 많은 환경에서 특히 효과적입니다.

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
