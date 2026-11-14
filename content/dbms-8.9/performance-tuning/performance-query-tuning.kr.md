---
type: docs
title: '14.5 조회와 분석 성능 튜닝'
weight: 140
toc: true
aliases:
  - /dbms-8.9/performance-tuning/query-analysis/
---

조회 성능은 결과 정확성을 유지하면서 읽는 행과 파티션, 정렬·집계 작업량을 줄이는
방향으로 개선합니다. 변경 전후에는 같은 데이터·조건·동시성에서 실행 시간과 결과 건수를
비교합니다.

## 핵심 원칙

1. TAG·LOG 조회는 필요한 시간 범위를 먼저 제한합니다.
2. 반환할 컬럼만 선택하고 무제한 `SELECT *`를 피합니다.
3. 자주 사용하는 동등·범위 조건과 JOIN 키에 적합한 인덱스를 검토합니다.
4. 반복되는 장기 TAG 집계에는 ROLLUP을 사용합니다.
5. 힌트나 설정 속성 변경 전에 `EXPLAIN`으로 실행 계획을 확인합니다.
6. 평균값뿐 아니라 지연 분포, 읽은 행, CPU·I/O, 동시 쿼리 영향을 기록합니다.

## 검증 가능한 예제

다음 예제는 LOG 테이블과 인덱스를 만들고 실행 계획·결과를 확인한 뒤 정리합니다.

```sql
CREATE LOG TABLE perf_event_demo (
    device_id VARCHAR(32),
    level     VARCHAR(16),
    code      INTEGER,
    message   VARCHAR(100)
);

CREATE INDEX idx_perf_event_code
ON perf_event_demo(code) INDEX_TYPE LSM;

INSERT INTO perf_event_demo VALUES ('DEV-01', 'WARN', 1001, 'temperature high');
INSERT INTO perf_event_demo VALUES ('DEV-02', 'INFO', 1000, 'started');
EXEC TABLE_FLUSH(perf_event_demo);

EXPLAIN
SELECT device_id, level, message
FROM perf_event_demo
WHERE code = 1001
  AND _ARRIVAL_TIME >= NOW - 60000000000;

SELECT device_id, level, message
FROM perf_event_demo
WHERE code = 1001
  AND _ARRIVAL_TIME >= NOW - 60000000000;

DROP TABLE perf_event_demo;
```

작은 표본에서 인덱스 스캔이 항상 더 빠르다고 결론 내리지 않습니다. 운영과 유사한 데이터
분포와 조건 선택도로 인덱스 생성 전후를 비교합니다.

<a id="performance-tuning-select"></a>
<a id="select-join-optimizer"></a>

## SELECT와 JOIN

- 큰 원본 테이블은 시간·키 조건으로 먼저 범위를 줄입니다.
- JOIN 조건의 양쪽 데이터 타입과 길이를 맞춥니다.
- WHERE 조건을 함수로 감싸 인덱스 범위를 사용할 수 없게 만드는지 확인합니다.
- outer JOIN을 inner JOIN으로 바꾸기 전에 NULL 공급 행이 사라지지 않는지 비교합니다.
- 결과 순서가 필요하면 `ORDER BY`를 명시합니다.
- 페이지 나누기는 큰 OFFSET보다 업무 키·시간을 이용한 이어 읽기를 검토합니다.

옵티마이저가 SQL에 적힌 테이블 순서를 그대로 따른다고 가정하지 않습니다. 조인 순서를
강제하는 힌트는 통계와 데이터 분포가 달라졌을 때 역효과가 날 수 있으므로 실행 계획과 결과를
함께 검증합니다.

## EXPLAIN 사용

`EXPLAIN`은 쿼리를 실행하지 않고 실행 계획을 확인합니다. `EXPLAIN FULL`은 실제 실행을 포함할
수 있으므로 운영 부하가 없는 제한된 환경에서 사용합니다.

실행 계획에서는 다음을 확인합니다.

| 항목 | 질문 |
|------|------|
| 대상 테이블 | 의도한 테이블과 view가 선택됐는가 |
| 스캔 종류 | 조건과 인덱스에 맞는 접근 경로인가 |
| 시간 범위 | TAG·LOG 파티션 범위가 제한되는가 |
| JOIN | 입력 행이 큰 상태에서 불필요한 조인이 수행되는가 |
| 정렬·집계 | 큰 중간 결과를 정렬하거나 materialize하는가 |

버전마다 달라질 수 있는 내부 객체 ID나 실행 계획 전체 문자열을 자동 검사의 고정값으로
사용하지 않습니다. 테이블 이름, 스캔 종류, 주요 조건식처럼 의미가 안정적인 항목을
검사합니다.

<a id="performance-cte"></a>

## CTE

CTE는 복잡한 쿼리를 읽기 쉽게 만들지만 자동으로 성능을 개선하지는 않습니다. 같은 CTE가
반복 평가되는지, 필터가 CTE 안쪽까지 적용되는지, 큰 중간 결과가 만들어지는지 실행 계획으로
확인합니다. Machbase 8.7.0은 Standard Edition에서 비재귀 SELECT CTE를 지원하며,
재귀 CTE는 지원하지 않습니다.

구문과 예제는 [CTE](/dbms-8.9/reference/sql/syntax/cte-syntax/)를 참고합니다.

<a id="performance-operators-tuning"></a>

## 검색 연산자

| 조건 | 점검 |
|------|------|
| 동등·범위 비교 | 컬럼 타입과 인덱스 종류가 맞는지 |
| `LIKE 'prefix%'` | prefix search 지원과 문자열 인덱스를 사용하는지 |
| leading wildcard | 전체 스캔 비용을 허용할 수 있는지 |
| `SEARCH`·`ESEARCH` | KEYWORD 인덱스와 문법이 맞는지 |
| `REGEXP` | 시간·다른 인덱스 조건으로 후보 행을 먼저 줄였는지 |
| JSON 경로 | 지원 테이블 타입과 JSON 인덱스를 확인했는지 |
| IP 범위 | IPV4·IPV6 타입과 인덱스 지원을 확인했는지 |

조건식의 정확한 의미와 인덱스 사용 조건은
[SEARCH·ESEARCH·REGEXP](/dbms-8.9/reference/sql/syntax/search-esearch-regexp-syntax/)와
[JSON 연산자](/dbms-8.9/reference/sql/functions/operators-json/)를 참고합니다.

<a id="performance-window-functions-considerations-pivot"></a>

<a id="window-function과-pivot"></a>

## 윈도우 함수와 PIVOT

윈도우 파티션과 순서 키가 넓으면 정렬·메모리 비용이 커질 수 있습니다. 먼저 시간과
업무 키로 입력 범위를 줄이고, 같은 윈도우를 중복 계산하지 않는지 확인합니다. PIVOT은
출력 범주 수를 제한하고 예상 밖 범주의 처리 방식을 정합니다.

구문은
[윈도우 함수](/dbms-8.9/reference/sql/syntax/window-function-over-syntax/)과
[PIVOT](/dbms-8.9/reference/sql/syntax/pivot-syntax/)을 참고합니다.

## 변경 전후 체크리스트

- 같은 결과 행 수와 NULL 분포를 반환하는가
- 같은 시간 범위와 시간대를 사용하는가
- cold·warm 캐시를 구분했는가
- 단일 실행뿐 아니라 동시 쿼리에서 비교했는가
- 입력 처리량과 메모리 사용량에 부작용이 없는가
- 변경을 되돌릴 DDL·설정 속성 값과 기준 측정값을 기록했는가

<a id="관련-sql-정본"></a>

## 관련 SQL 문서

| 주제 | 상세 문서 |
|---|---|
| SELECT·시간 조건 | [SELECT 문법](/dbms-8.9/reference/sql/syntax/select-syntax/) |
| VIEW·CTE·집합 연산 | [SQL 문법 사전](/dbms-8.9/reference/sql/syntax/) |
| 힌트 | [SELECT 힌트](/dbms-8.9/reference/sql/syntax/select-hint-syntax/) |
| 함수·집계 | [함수 사전](/dbms-8.9/reference/sql/functions/) |

## TRANSACTION 인덱스 순서와 LIMIT

Linux Standard Edition에서 단일 TRANSACTION 테이블의 동등 조건과 정렬 키가 복합
B-tree 인덱스의 순서에 맞으면 인덱스 순서대로 읽을 수 있습니다. 최종 조건을 통과한
행이 LIMIT에 도달하면 읽기를 종료해 전체 정렬과 불필요한 후보 읽기를 줄입니다.

다음 예제는 전용 실습 DB에서 실행합니다. 같은 이름의 객체가 있으면 먼저 이름을 바꿉니다.

```sql
CREATE TRANSACTION TABLE SORT_SAMPLE(
 ID VARCHAR(40) PRIMARY KEY,KIND VARCHAR(16),WS VARCHAR(40),BODY TEXT
);
CREATE INDEX I_SORT_SAMPLE ON SORT_SAMPLE(KIND,WS,ID) INDEX_TYPE BTREE;
INSERT INTO SORT_SAMPLE VALUES('0003','job','w1','세 번째');
INSERT INTO SORT_SAMPLE VALUES('0001','job','w1','첫 번째');
INSERT INTO SORT_SAMPLE VALUES('0002','job','w1','두 번째');
EXPLAIN SELECT ID,LENGTH(BODY) FROM SORT_SAMPLE
 WHERE KIND='job' AND WS='w1' ORDER BY ID LIMIT 2;
SELECT ID,BODY FROM SORT_SAMPLE
 WHERE KIND='job' AND WS='w1' ORDER BY ID LIMIT 2;
SELECT ID,BODY FROM SORT_SAMPLE
 WHERE KIND='job' AND WS='w1' AND ID>'0002' ORDER BY ID LIMIT 2;
```

첫 조회는 0001·0002, 마지막 키 이후의 조회는 0003을 반환합니다. 동등 조건인 KIND·WS를
앞에 놓고 정렬 키 ID를 그 뒤에 배치한 인덱스입니다. 최종 결과를 확인한 뒤 직접 만든
테이블만 `DROP TABLE SORT_SAMPLE`로 정리합니다.

### 적용 조건과 실행 계획

- 단일 테이블의 직접 signed 정수·VARCHAR 정렬 키와 같은 방향의 ASC 또는 DESC가 대상입니다.
- JOIN·집계·윈도우·ROWNUM/SERIESNUM·서브쿼리·정렬 표현식·혼합 정렬 방향은 기존 경로를 사용합니다.
- SELECT 목록의 LENGTH·CAST·상수와 정렬 키 자체에 적용하는 표현식은 구분합니다.
- 실행 계획의 `ORDERED INDEX`, 방향과 키, `FILTER=QP_FINAL`, `EARLY_STOP=QP_LIMIT`를
  확인합니다. 잔여 조건으로 탈락하는 행이 있으면 반환 행보다 많은 후보를 읽습니다.

깊은 OFFSET은 앞의 행을 계속 통과해야 합니다. 예를 들어 OFFSET 4000과 LIMIT 200은
4200행을 통과해야 하므로 연속 목록 조회에서는 마지막 키 이후 조건이 유리할 수 있습니다.
예제는 유일한 ID를 사용합니다. 중복 정렬 키로 페이지를 나누면 유일 키를 함께 정렬하고
이전 페이지의 마지막 키 조합에 맞는 조건을 작성해 누락과 중복을 방지합니다.

VARCHAR 정렬 보조 정보는 인덱스 공간과 쓰기·구축 비용을 늘립니다. 실제 쿼리의 결과와
계획, 전체 fetch까지의 시간을 함께 비교합니다. 이 최적화를 벡터 ANN 검색으로 해석하지 않습니다.

## 재귀 CTE의 실행 계획

`EXPLAIN`은 실행 전 계획이며 `EXPLAIN FULL`은 실제로 질의를 실행합니다.
큰 관계망에서는 FULL에도 쿼리와 같은 자원이 필요합니다.

| 표시 | 의미 |
|---|---|
| RECURSIVE CTE WORK | 재귀 term이 읽는 직전 작업 집합 |
| RECURSIVE CTE RESULT | consumer가 읽는 누적 결과 |
| ITERATIONS / ROWS / DUPLICATES | 실행 후 반복·행·중복 통계 |

실행 전 계획의 0을 예상 행 수로 해석하지 않습니다. UNION ALL의 DUPLICATES=0은 중복이
없다는 뜻이 아니라 누적 중복 제거를 집계하지 않는다는 뜻입니다. 같은 재귀 producer는
누적 결과를 공유하지만 일반 비재귀 CTE까지 한 번만 계산된다고 보장하지 않습니다.

[재귀 쿼리 운영과 실행 계획](/kr/dbms-8.9/ai-search-graphrag/operations/)에서 깊이·경로 폭·
읽기 일관성과 메모리 제약을 함께 확인합니다.

## DFQ 파일 조회의 비용

READ는 prepare의 추론, source open·decode, SQL 분석과 전체 fetch의 비용을 구분해 측정합니다.
LIMIT이 작아도 전체 스키마 추론이나 TEXT 정렬 비용이 남을 수 있습니다. 메모리 예산에 따라
지원되는 정렬·집계는 임시 디스크를 사용하며 모든 decoder가 같은 spill 정책을 갖지는 않습니다.
EXPLAIN FULL은 실제 질의를 실행합니다. [DFQ 운영](/kr/dbms-8.9/dfq/operations/)을 참고합니다.
