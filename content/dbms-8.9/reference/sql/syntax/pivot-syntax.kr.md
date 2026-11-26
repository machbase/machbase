---
type: docs
title: 'PIVOT'
weight: 70
toc: true
---

`PIVOT`은 행(row) 방향 데이터를 열(column) 방향으로 변환하는 구문입니다. GROUP BY 집계 결과를 컬럼으로 재배열해 가독성 높은 리포트 형태로 표현할 때 사용합니다.

> PIVOT 구문은 Machbase 5.6 버전부터 지원됩니다.

## 문법

```sql
SELECT *
  FROM (inline_view)
 PIVOT (aggregate_expr [AS agg_alias] [, ...]
        FOR category_col IN ('val1' AS col1, 'val2' AS col2, ...)
        [GROUP BY group_expr, ...])
[WHERE ...]
```

- 명시 GROUP BY를 생략하면 입력에서 집계 인자와 FOR 키를 제외한 컬럼으로 그룹을 만듭니다.
- `FOR category_col IN (...)`: 피벗 기준 컬럼과 열로 변환할 값 목록을 지정합니다.
- 복수 집계는 IN 키 순서와 집계식 순서로 열을 만들며 `IN별칭_집계별칭` 이름을 사용합니다.
- 명시 GROUP BY가 있으면 해당 식만 그룹 키로 사용합니다.
- IN에는 한 열을 반환하는 SELECT도 사용할 수 있으며 prepare 시 결과 스키마가 고정됩니다.
  새 키를 결과 열로 추가하려면 다시 prepare합니다.
- 존재하는 그룹의 빈 COUNT 셀은 0입니다. 중복 IN 키는 ERR-02385입니다.

복수 집계·집계 결과 식·동적 열·그룹 구성의 전체 실행 예제는
[13.8 PIVOT으로 시계열 비교하기](../../../../time-series-sql/pivot/)를 참고합니다.

### PIVOT 전체 BNF {#pivot-bnf}

아래 ε는 생략이며 expression_list는 하나 이상의 쉼표로 구분한 SQL 식입니다.

```bnf
<pivot_clause> ::= "PIVOT" "(" <cell_list> "FOR" <column>
                   "IN" "(" <palette> ")" <group_opt> ")"
<cell_list> ::= <cell> | <cell_list> "," <cell>
<cell> ::= <aggregate_expression> <alias_opt>
<alias_opt> ::= ε | "AS" <alias>
<palette> ::= <pivot_values> | <single_column_select>
<pivot_values> ::= <pivot_value> | <pivot_values> "," <pivot_value>
<pivot_value> ::= <constant_expression> <alias_opt>
<group_opt> ::= ε | "GROUP" "BY" <expression_list>
```

집계식이나 집계 결과를 사용하는 scalar 식을 셀로 지정합니다. 셀 안에는 OVER·SUBSAMPLE을
넣지 않습니다. IN 키 순서 안에서 집계식 순서로 열을 만듭니다. 명시 GROUP BY는 해당
키만 사용하며 생략 시 FOR 키와 집계 인자를 제외한 입력 열이 암묵적 그룹 키입니다.
동적 IN SELECT는 한 열을 반환하고 스키마를 prepare에서 확정하므로 바인드를 받지 않습니다.
같은 준비문 재실행은 열 구성을 유지합니다. 새 열은 재prepare하고 저장 VIEW는 재정의합니다.
빈 IN, 중복 키·열 이름은 오류입니다. SQL NULL과 문자열 'NULL'은 서로 다른 키입니다.
동적 IN이 JSON·ARRAY·VECTOR를 반환하면 거부하며 지원 scalar로 먼저 추출합니다.
존재하는 그룹의 COUNT 빈 셀은 0입니다. OUTER JOIN에서 PIVOT 행 전체가 미매칭이면 NULL입니다.

## 예시

### 센서별 집계를 열로 변환

```sql
-- 인라인 뷰를 사용한 PIVOT
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
     WHERE regtime BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                       AND TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
) PIVOT (
    SUM(dvalue) FOR tagid IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE')
)
WHERE FRONT_AXIS_TORQUE >= 40 AND REAR_AXIS_TORQUE >= 20;
```

### CASE 문 대비 간결한 표현

```sql
-- PIVOT 없이 CASE 사용
SELECT regtime,
       SUM(CASE WHEN tagid = 'SENSOR_A' THEN dvalue ELSE 0 END) AS sensor_a,
       SUM(CASE WHEN tagid = 'SENSOR_B' THEN dvalue ELSE 0 END) AS sensor_b
  FROM result_d
 GROUP BY regtime;

-- PIVOT으로 간결하게 표현
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
) PIVOT (SUM(dvalue) FOR tagid IN ('SENSOR_A', 'SENSOR_B'));
```

### TAG 테이블과 PIVOT 조합

```sql
SELECT * FROM (
    SELECT name, time, value
      FROM sensor_tag
     WHERE time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                    AND TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS')
) PIVOT (
    AVG(value) FOR name IN ('sensor-01', 'sensor-02', 'sensor-03')
);
```

## 제약사항

- PIVOT은 반드시 인라인 뷰(서브쿼리)와 함께 사용해야 합니다.
- 인라인 뷰에서 PIVOT 집계 컬럼(`value_col`)과 기준 컬럼(`category_col`) 외의 모든 컬럼이 자동 GROUP BY 대상이 됩니다.
- IN 절에 나열하는 값은 컴파일 시점에 확정된 리터럴이어야 합니다 (동적 컬럼 목록 불가).

## 관련 문서

- [SELECT hint syntax](../select-hint-syntax/) — SELECT 힌트 문법과 사용 예제
