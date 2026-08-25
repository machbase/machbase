---
type: docs
title: '13.10 쿼리 분석 경로'
weight: 100
toc: true
---

이 페이지는 느린 쿼리를 분석할 때 사용할 성능 문서와 SQL 레퍼런스를 연결합니다. SQL
문법을 이 장에서 다시 설명하지 않으며, 구문별 상세 페이지를 정본으로 사용합니다.

<a id="selection-query-method"></a>
<a id="selection-query-method-selection-guide-query-method"></a>
<a id="selection-query-method-table-types-type-query"></a>

## 분석 순서

1. 같은 SQL, bind 값, 세션 설정과 대표 데이터로 기준 시간을 측정합니다.
2. `EXPLAIN`으로 스캔 순서, 인덱스와 `KEY RANGE`를 확인합니다.
3. TAG/LOG 쿼리에 태그·시간 범위가 명확한지 확인합니다.
4. 불필요한 컬럼, 정렬, 광범위한 정규식과 큰 중간 집합을 줄입니다.
5. 인덱스, ROLLUP 또는 힌트 변경은 한 번에 하나씩 적용합니다.
6. 변경 전후 실행 시간과 계획을 같은 조건에서 비교합니다.

실행 계획 해석과 테이블 타입별 점검 절차는
[쿼리 성능 튜닝](/dbms/performance-tuning/performance-query-tuning/)과
[성능 진단 체크리스트](/dbms/performance-tuning/checklist-performance-diagnosis/)를
참고하십시오.

<a id="query-select"></a>
<a id="query-select-query-select"></a>
<a id="where-order-limit"></a>
<a id="query-select-where-order-limit"></a>
<a id="condition-time-duration"></a>
<a id="query-select-condition-time-duration"></a>
<a id="relative-time"></a>
<a id="query-select-relative-time"></a>

## 기본 조회와 시간 조건

| 주제 | 정본 |
|------|------|
| `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT`, `DURATION` | [SELECT syntax](/dbms/reference/sql/syntax-dictionary-sql/select-syntax/) |
| 상대 시간과 날짜 표현 | [상대 시간 사전](/dbms/reference/sql/relative-time-dictionary/) |
| 텍스트 조건 | [SEARCH / ESEARCH / REGEXP](/dbms/reference/sql/syntax-dictionary-sql/search-esearch-regexp-syntax/) |

<a id="query-view"></a>
<a id="query-select-query-view"></a>
<a id="query-cte"></a>
<a id="query-select-query-cte"></a>
<a id="set-operators-union-intersect-except"></a>
<a id="query-select-set-operators-union-intersect-except"></a>

## 쿼리 구성

| 주제 | 정본 |
|------|------|
| VIEW | [VIEW syntax](/dbms/reference/sql/syntax-dictionary-sql/view-syntax/) |
| WITH / CTE | [CTE syntax](/dbms/reference/sql/syntax-dictionary-sql/cte-syntax/) |
| 집합 연산 | [Set operator syntax](/dbms/reference/sql/syntax-dictionary-sql/set-operator-syntax/) |

<a id="hint-select"></a>
<a id="query-select-hint-select"></a>
<a id="hint-sampling"></a>
<a id="query-select-hint-select-hint-sampling"></a>
<a id="hint-interpolation"></a>
<a id="query-select-hint-select-hint-interpolation"></a>
<a id="execution-plan-explain"></a>
<a id="query-select-execution-plan-explain"></a>

## 힌트와 실행 계획

힌트의 문법과 지원 범위는 [SELECT hint syntax](/dbms/reference/sql/syntax-dictionary-sql/select-hint-syntax/)를
참고하십시오. 힌트는 실행 계획을 먼저 확인한 뒤 필요한 경우에만 적용합니다. `EXPLAIN`,
`EXPLAIN FULL`과 실제 계획 판독은
[쿼리 성능 튜닝](/dbms/performance-tuning/performance-query-tuning/#explain과-explain-full-읽기)을
참고하십시오.

<a id="item"></a>
<a id="aggregation-group"></a>
<a id="item-aggregation-group"></a>
<a id="aggregation-group-concat"></a>
<a id="item-aggregation-group-concat"></a>
<a id="item-join"></a>
<a id="item-pivot"></a>
<a id="window-functions-over"></a>
<a id="item-window-functions-over"></a>
<a id="lag-lead"></a>
<a id="item-window-functions-over-lag-lead"></a>
<a id="item-window-functions-over-ntile"></a>
<a id="partition-order"></a>
<a id="item-window-functions-over-partition-order"></a>
<a id="query-interpolation-series"></a>
<a id="item-query-interpolation-series"></a>

## 집계와 고급 조회

| 주제 | 정본 |
|------|------|
| 집계, `GROUP BY`, JOIN | [SELECT syntax](/dbms/reference/sql/syntax-dictionary-sql/select-syntax/) |
| PIVOT | [PIVOT syntax](/dbms/reference/sql/syntax-dictionary-sql/pivot-syntax/) |
| 윈도우 함수 | [Window function / OVER](/dbms/reference/sql/syntax-dictionary-sql/window-function-over-syntax/) |
| 시계열 생성과 보간 | [SERIES syntax](/dbms/reference/sql/syntax-dictionary-sql/series-syntax/) |
| 함수와 `GROUP_CONCAT` | [SQL 함수 사전](/dbms/reference/sql/dictionary/) |

<a id="condition-conditional-search"></a>
<a id="query-json-path"></a>
<a id="condition-conditional-search-query-json-path"></a>

## 텍스트와 JSON 조건

전문 검색 연산자는
[SEARCH / ESEARCH / REGEXP](/dbms/reference/sql/syntax-dictionary-sql/search-esearch-regexp-syntax/)를,
JSON 연산자와 함수는 [SQL 함수·연산자 사전](/dbms/reference/sql/dictionary/)을
참고하십시오. 텍스트 검색 성능이 중요하면 지원되는 인덱스와 실행 계획을 함께
확인하십시오.
