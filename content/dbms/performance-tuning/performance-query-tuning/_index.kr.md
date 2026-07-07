---
type: docs
title: '조회와 분석 성능 튜닝'
weight: 50
---

이 섹션에서는 Machbase에서 SELECT 쿼리와 집계 분석의 응답 시간을 단축하기 위한 실무 튜닝 기법을 설명합니다.

## 핵심 원칙

Machbase는 시계열 데이터를 대량으로 처리하는 컬럼 기반 DBMS입니다. 조회 성능을 결정하는 핵심 요소는 다음 네 가지입니다.

### 1. 인덱스 활용

Machbase는 LOG 테이블에 BITMAP 인덱스, TAG 테이블에 인메모리 해시 인덱스를 제공합니다. WHERE 절에 인덱스가 정의된 컬럼을 우선 배치하면 스캔 범위를 크게 줄일 수 있습니다. `EXPLAIN` 명령으로 실행 계획을 확인해 INDEX SCAN이 적용되는지 반드시 검증하세요.

### 2. 파티션 Pruning

LOG 테이블은 `_arrival_time`, TAG 테이블은 `time` 컬럼을 기준으로 데이터를 파티션에 분산 저장합니다. WHERE 절에 이 컬럼의 범위 조건을 명시하면 불필요한 파티션을 건너뜁니다(Partition Pruning). 시간 범위 없이 전체 데이터를 스캔하면 수십~수백 배의 응답 시간 차이가 날 수 있습니다.

### 3. ROLLUP 사전 집계

수백만~수억 건의 원시 데이터를 매번 집계하는 대신, ROLLUP으로 미리 계산된 통계(MIN, MAX, AVG, COUNT 등)를 활용하면 집계 쿼리의 응답 시간을 수십 배 이상 단축할 수 있습니다. 분·시간·일 단위 추세 분석에 특히 효과적입니다.

### 4. 힌트 사용

옵티마이저 판단이 최적이 아닌 경우, `/*+ 힌트 */` 구문으로 병렬 처리 계수, 인덱스 사용 여부, ROLLUP 테이블 선택 등을 직접 제어할 수 있습니다. 힌트는 실행 계획을 확인한 뒤 필요한 경우에만 사용합니다.

## 이 섹션의 구성

| 주제 | 설명 |
|------|------|
| [SELECT 성능 튜닝](./performance-tuning-select/) | WHERE 절 설계, 시간 범위 조건, EXPLAIN 해석 |
| [검색 연산자 성능 튜닝](./performance-operators-tuning/) | 인덱스 활용 가능·불가 연산자, BITMAP vs LSM 선택 |
| [윈도우 함수와 PIVOT 성능 고려사항](./performance-window-functions-considerations-pivot/) | 메모리 주의사항, 서브쿼리 선처리 패턴 |
| [ROLLUP 활용 튜닝](./tuning-rollup/) | ROLLUP 조회 패턴, 계층 설계, WAKEUP INTERVAL |
| [TAG 데이터 대량 정정 성능 고려사항](./correction-performance-bulk-considerations-tag-data-update/) | DELETE + INSERT 패턴, 임시 대안 |
| [LOOKUP 일반 predicate DML 성능 고려사항](./performance-considerations-lookup-predicate-dml/) | non-PK DELETE 제약, PK 기준 분할 삭제 |
