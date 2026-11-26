---
type: docs
title: 'window function / OVER'
weight: 80
toc: true
---

Machbase의 `LAG()`와 `LEAD()`는 조회 결과의 각 행에서 이전 또는 다음 행의 값을 참조합니다.
예를 들어 센서별 측정값을 시간순으로 비교해 직전 측정값과의 차이를 구할 수 있습니다.
`GROUP BY` 집계와 달리 여러 행을 하나로 줄이지 않습니다.

## 문법

```sql
LAG(value_expression, offset) OVER (
    [PARTITION BY partition_expression]
    [ORDER BY order_expression]
)

LEAD(value_expression, offset) OVER (
    [PARTITION BY partition_expression]
    [ORDER BY order_expression]
)
```

| 요소 | 설명 |
|------|------|
| `value_expression` | 이전 또는 다음 행에서 가져올 값 |
| `offset` | 현재 행에서 떨어진 행 수. 1 이상의 정수를 지정 |
| `PARTITION BY` | 비교할 행을 그룹으로 나누는 식 목록. 생략하면 전체 결과를 한 그룹으로 처리 |
| `ORDER BY` | 그룹 안에서 비교 순서를 정하는 식 목록 |

`OVER`는 필수이며, 괄호 안의 `PARTITION BY`와 `ORDER BY`는 생략할 수 있습니다.
시간순 비교에는 `ORDER BY time`처럼 기준을 명시하십시오. 정렬 기준 값이 같은 행 사이의
순서는 이 식만으로 구분할 수 없습니다. 최종 결과의 출력 순서가 필요하면 SELECT 문 끝에도
`ORDER BY`를 지정합니다.

## 지원 윈도우 함수

<a id="이동-참조-함수"></a>

| 함수 | 설명 |
|------|------|
| `LAG(value, n)` | 같은 그룹에서 현재 행보다 n행 앞의 값 |
| `LEAD(value, n)` | 같은 그룹에서 현재 행보다 n행 뒤의 값 |

참조할 행이 없으면 NULL을 반환합니다. `offset`은 시간 간격이 아니라 행 수입니다.
측정 간격이 불규칙하면 직전 행이 반드시 1초 전이나 1분 전 측정값인 것은 아닙니다.

<a id="순위-함수"></a>
<a id="집계-윈도우-함수"></a>

### OVER와 ROWS 전체 BNF {#rows-bnf}

Standard Edition에서 지원 집계 함수의 호출 뒤에 OVER를 붙입니다. 아래 ε는 생략입니다.
expression과 aggregate_call은 기존 식과 지원 집계 호출이며 COUNT(*)도 포함합니다.

```bnf
<window_aggregate> ::= <aggregate_call> "OVER" "("
                       <partition_opt> <order_opt> <rows_opt> ")"
<partition_opt> ::= ε | "PARTITION" "BY" <expression_list>
<order_opt> ::= ε | "ORDER" "BY" <sort_list>
<expression_list> ::= <expression> | <expression_list> "," <expression>
<sort_list> ::= <sort_item> | <sort_list> "," <sort_item>
<sort_item> ::= <expression> <direction_opt>
<direction_opt> ::= ε | "ASC" | "DESC"
<rows_opt> ::= ε | "ROWS" <frame_bound>
             | "ROWS" "BETWEEN" <frame_bound> "AND" <frame_bound>
<frame_bound> ::= "UNBOUNDED" "PRECEDING"
                | <row_count> "PRECEDING"
                | "CURRENT" "ROW"
                | <row_count> "FOLLOWING"
                | "UNBOUNDED" "FOLLOWING"
<row_count> ::= <nonnegative_integer_constant_expression> | <integer_bind>
```

- 양끝을 포함합니다. 폭은 0 이상의 정수 문장 상수·정수 bind입니다. NULL·음수·비정수·
  행 의존 폭은 오류입니다. 파티션 경계에서 잘리며 다른 장치의 행을 포함하지 않습니다.
- 시작에 UNBOUNDED FOLLOWING, 끝에 UNBOUNDED PRECEDING을 사용할 수 없으며 역순도 오류입니다.
- ROWS 2 PRECEDING은 ROWS BETWEEN 2 PRECEDING AND CURRENT ROW와 같습니다.
- OVER 안의 정렬 키 조합은 파티션 내에서 유일해야 합니다. 최종 SELECT의 정렬은 내부
  동률을 해결하지 않으며 내부 동률은 E_TIE_CONFLICT입니다.
- ROWS 생략 시 ORDER BY가 있으면 처음부터 현재까지 누적하고 없으면 전체 파티션입니다.
  ORDER BY 없이 명시한 프레임은 전체 파티션 또는 CURRENT ROW 단독만 허용합니다.
- 빈 프레임 COUNT는 0이며 SUM·AVG 등은 각 집계의 빈 입력 규칙을 따릅니다.
  SAMPLE 결과에서는 FILL 버킷도 프레임의 논리 행입니다.
- SUM·AVG·MIN·MAX·COUNT 및 지원 선택 집계에 사용합니다. LAG·LEAD와 SUBSAMPLE KEEP의
  함수별 인자·프레임 제약은 각각의 계약을 따릅니다.

### 집계 윈도 함수와 ROWS 프레임

Standard Edition에서는 SUM·AVG·MIN·MAX·COUNT 등의 집계에 OVER와 ROWS 프레임을
사용할 수 있습니다. PARTITION BY·ORDER BY에 복수 키와 정렬 방향을 지정할 수 있습니다.
윈도 내부 ORDER BY 조합은 행을 유일하게 구분해야 하며 같은 시각에는 보조 키를 추가합니다.

```sql
SUM(value) OVER (
    PARTITION BY name ORDER BY time, id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

이 식은 같은 name에서 현재 행과 앞 두 행을 더합니다. 프레임은 파티션 경계에서 잘립니다.
UNBOUNDED PRECEDING·CURRENT ROW·N PRECEDING/FOLLOWING·UNBOUNDED FOLLOWING을
프레임 위치에 맞게 사용합니다. N은 0 이상의 정수입니다.
전체 데이터와 이동·누적 집계 결과는 [13.6 ROWS 윈도 프레임](../../../../time-series-sql/rows/)을 참고합니다.
시간 범위의 집계는 [WINDOW JOIN](../../../../time-series-sql/joins/window/)에서 설명합니다.

결과 행에 번호를 붙이는 `ROWNUM()`과 연속 구간 번호를 구하는 `SERIESNUM()`은
[윈도우/시리즈 함수](../../functions/series/)에서 설명합니다.

## 예시

### LAG / LEAD: 이전/이후 값 비교

다음 예제는 `name`, `time`, `value` 컬럼이 있는 `sensor_tag` 테이블을 사용합니다.

```sql
SELECT name, time, value,
       LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS prev_value,
       LEAD(value, 1) OVER (PARTITION BY name ORDER BY time) AS next_value,
       value - LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS delta
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2024-01-01', 'YYYY-MM-DD')
 ORDER BY name, time;
```

`prev_value`와 `next_value`는 조회 범위 안의 이전·다음 값을 나타냅니다. 첫 행의
`prev_value`와 마지막 행의 `next_value`는 NULL입니다. `WHERE`로 제외한 과거 행은
비교 대상에 포함되지 않으므로 첫 행의 차이까지 필요하면 조회 범위를 앞쪽으로 넓힙니다.

<a id="순위-함수-1"></a>
<a id="이동-평균"></a>
<a id="누적-합계"></a>

### 집계 결과의 이전 값 비교

태그별 시간 구간을 먼저 집계한 뒤 집계값 사이의 변화를 비교할 수 있습니다. 다음 예제는
시간 단위 ROLLUP을 조회할 수 있는 `sensor_tag` 테이블을 전제로 합니다.

```sql
SELECT name, bucket, avg_val,
       LAG(avg_val, 1) OVER (PARTITION BY name ORDER BY bucket) AS prev_avg
  FROM (
      SELECT name,
             rollup('hour', 1, time) AS bucket,
             AVG(value)              AS avg_val
        FROM sensor_tag
       WHERE time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
                      AND TO_DATE('2024-07-01', 'YYYY-MM-DD')
       GROUP BY name, bucket
  ) t
 ORDER BY name, bucket;
```

이 쿼리는 구간별 평균과 직전 구간의 평균을 비교합니다. 이동 평균이나 누적 합계를
계산하는 쿼리는 아닙니다. 데이터가 없는 구간은 자동으로 채워지지 않습니다.

## 성능 주의사항

윈도우 계산에는 그룹 구분, 정렬과 이전·다음 행의 값을 유지하는 작업이 필요합니다.
시간 범위와 태그 조건으로 대상 행을 줄이고, 장기 추세 비교는 집계 결과에 적용하면
처리해야 할 행 수를 줄일 수 있습니다.

`LAG`/`LEAD`는 SELECT 결과 식에서 사용합니다. `WHERE`, `HAVING`, `GROUP BY`,
`ORDER BY`, JOIN의 `ON` 조건에 직접 호출하지 마십시오. 계산한 값으로 필터링하려면
인라인 뷰의 결과 컬럼을 바깥 SELECT에서 참조합니다.

## 관련 문서

- [윈도우/시리즈 함수](../../functions/series/) — `ROWNUM()`과 `SERIESNUM()`
- [PIVOT syntax](../pivot-syntax/) — 행을 열로 변환
- [SERIES BY syntax](../series-syntax/) — 연속 구간 추출
