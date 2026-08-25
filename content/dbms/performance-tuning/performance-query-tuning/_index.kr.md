---
type: docs
title: '12.5 조회와 분석 성능 튜닝'
weight: 50
toc: true
---

조회 성능은 결과 정확성을 유지하면서 읽는 row와 partition, 정렬·집계 작업량을 줄이는
방향으로 개선합니다. 변경 전후에는 같은 데이터·조건·동시성에서 실행 시간과 결과 건수를
비교합니다.

## 핵심 원칙

1. TAG·LOG 조회는 필요한 시간 범위를 먼저 제한합니다.
2. 반환할 컬럼만 선택하고 무제한 `SELECT *`를 피합니다.
3. 자주 사용하는 동등·범위 조건과 JOIN key에 적합한 인덱스를 검토합니다.
4. 반복되는 장기 TAG 집계에는 ROLLUP을 사용합니다.
5. hint나 property 변경 전에 `EXPLAIN`으로 plan을 확인합니다.
6. 평균값뿐 아니라 지연 분포, 읽은 row, CPU·I/O, 동시 query 영향을 기록합니다.

## 검증 가능한 예제

다음 예제는 LOG 테이블과 인덱스를 만들고 plan·결과를 확인한 뒤 정리합니다.

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

작은 표본에서 인덱스 scan이 항상 더 빠르다고 결론 내리지 않습니다. 운영과 유사한 데이터
분포와 조건 선택도로 인덱스 생성 전후를 비교합니다.

<a id="performance-tuning-select"></a>
<a id="select-join-optimizer"></a>

## SELECT와 JOIN

- 큰 원본 테이블은 시간·key 조건으로 먼저 범위를 줄입니다.
- JOIN 조건의 양쪽 데이터 타입과 길이를 맞춥니다.
- WHERE 조건을 함수로 감싸 index range를 사용할 수 없게 만드는지 확인합니다.
- outer JOIN을 inner JOIN으로 바꾸기 전에 NULL 공급 행이 사라지지 않는지 비교합니다.
- 결과 순서가 필요하면 `ORDER BY`를 명시합니다.
- pagination은 큰 OFFSET보다 업무 key·시간을 이용한 이어 읽기를 검토합니다.

optimizer가 SQL에 적힌 table 순서를 그대로 따른다고 가정하지 않습니다. join order를
강제하는 hint는 통계와 데이터 분포가 달라졌을 때 역효과가 날 수 있으므로 plan과 결과를
함께 검증합니다.

## EXPLAIN 사용

`EXPLAIN`은 query를 실행하지 않고 plan을 확인합니다. `EXPLAIN FULL`은 실제 실행을 포함할
수 있으므로 운영 부하가 없는 제한된 환경에서 사용합니다.

plan에서는 다음을 확인합니다.

| 항목 | 질문 |
|------|------|
| 대상 table | 의도한 table과 view가 선택됐는가 |
| scan 종류 | 조건과 index에 맞는 접근 경로인가 |
| 시간 범위 | TAG·LOG partition 범위가 제한되는가 |
| JOIN | 입력 row가 큰 상태에서 불필요한 join이 수행되는가 |
| 정렬·집계 | 큰 중간 결과를 정렬하거나 materialize하는가 |

버전마다 달라질 수 있는 내부 object ID나 plan 전체 문자열을 자동 검사의 고정값으로
사용하지 않습니다. table 이름, scan 종류, 주요 predicate처럼 의미가 안정적인 항목을
검사합니다.

<a id="performance-cte"></a>

## CTE

CTE는 복잡한 query를 읽기 쉽게 만들지만 자동으로 성능을 개선하지는 않습니다. 같은 CTE가
반복 평가되는지, filter가 CTE 안쪽까지 적용되는지, 큰 중간 결과가 만들어지는지 plan으로
확인합니다. 재귀 CTE에는 종료 조건과 최대 결과 범위를 둡니다.

구문과 예제는 [CTE](/dbms/reference/sql/syntax-dictionary-sql/cte-syntax/)를 참고합니다.

<a id="performance-operators-tuning"></a>

## 검색 연산자

| 조건 | 점검 |
|------|------|
| 동등·범위 비교 | 컬럼 타입과 index 종류가 맞는지 |
| `LIKE 'prefix%'` | prefix search 지원과 문자열 index를 사용하는지 |
| leading wildcard | 전체 scan 비용을 허용할 수 있는지 |
| `SEARCH`·`ESEARCH` | KEYWORD index와 문법이 맞는지 |
| `REGEXP` | 시간·다른 index 조건으로 후보 row를 먼저 줄였는지 |
| JSON path | 지원 table type과 JSON index를 확인했는지 |
| IP 범위 | IPV4·IPV6 타입과 index 지원을 확인했는지 |

검색 문법을 이 페이지에 반복하지 않습니다.
[SEARCH·ESEARCH·REGEXP](/dbms/reference/sql/syntax-dictionary-sql/search-esearch-regexp-syntax/)와
[JSON 연산자](/dbms/reference/sql/dictionary/operators-json/)를 정본으로 사용합니다.

<a id="performance-window-functions-considerations-pivot"></a>

## Window function과 PIVOT

window partition과 order key가 넓으면 정렬·메모리 비용이 커질 수 있습니다. 먼저 시간과
업무 key로 입력 범위를 줄이고, 같은 window를 중복 계산하지 않는지 확인합니다. PIVOT은
출력 category 수를 제한하고 예상 밖 category의 처리 방식을 정합니다.

구문은
[window function](/dbms/reference/sql/syntax-dictionary-sql/window-function-over-syntax/)과
[PIVOT](/dbms/reference/sql/syntax-dictionary-sql/pivot-syntax/)을 참고합니다.

## 변경 전후 체크리스트

- 같은 결과 row 수와 NULL 분포를 반환하는가
- 같은 시간 범위와 timezone을 사용하는가
- cold·warm cache를 구분했는가
- 단일 실행뿐 아니라 동시 query에서 비교했는가
- 입력 처리량과 메모리 사용량에 부작용이 없는가
- 변경을 되돌릴 DDL·property 값과 기준 측정값을 기록했는가
