---
type: docs
title: 'Machbase 아키텍처 개요'
weight: 10
---

Machbase DBMS의 내부 구조를 이해하면 테이블 설계, 쿼리 작성, 성능 튜닝에서 더 나은 판단을 내릴 수 있습니다. 이 문서는 Standard Edition과 Cluster Edition의 아키텍처를 개념 수준에서 설명합니다.

## 주요 구성 요소

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

## Standard Edition 구조

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

## Cluster Edition 구조

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

LOOKUP 테이블 처리를 위한 Lookup 노드도 Cluster Edition 구성에 포함됩니다. 개념적으로는
Warehouse가 대용량 시계열 데이터를 나누어 처리하고, Lookup 노드는 클러스터 전역에서 참조되는
기준 정보 처리를 담당합니다.

## 데이터 흐름: 쓰기

1. 클라이언트가 SQL INSERT 또는 APPEND 프로토콜로 데이터를 전송
2. QP가 대상 테이블과 컬럼을 파악해 SM에 전달
3. LOG/TAG 테이블이면 SM이 해당 시간 파티션의 컬럼 파일에 데이터를 append
4. 충분한 데이터가 쌓이면 배경 스레드가 압축 및 인덱스 병합 수행

RDB 테이블의 `INSERT`/`UPDATE`/`DELETE`는 append-only 시계열 경로가 아니라 RDB 저장 경로에서
행 단위 DML로 처리됩니다.

## 데이터 흐름: 읽기

1. 클라이언트가 SELECT 쿼리 전송
2. QP가 파싱 후 실행 계획 수립 (Plan Cache 활용)
3. LOG/TAG 테이블이면 SM이 시간 범위에 해당하는 파티션만 선택 (파티션 pruning)
4. 필요한 컬럼 파일만 읽어 집계 또는 필터 적용
5. QP가 결과를 클라이언트에 반환

## 다음 읽을 내용

- [컬럼형 저장과 압축](../storage-columnar-compression-column/) — SM의 저장 구조 상세
- [인덱싱 기본 원리](../indexing-basics/) — 테이블 유형별 인덱스 구조
- [Cache와 실행 계획 개념](../execution-concepts-plan-cache/) — QP의 캐시와 실행 계획 관리
- [Standard Edition과 Cluster Edition 차이](/dbms/core-concepts/concepts-edition/differences-standard-edition-cluster/) — 두 Edition의 선택 기준
