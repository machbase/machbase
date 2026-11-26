---
type: docs
title: '선택 윈도 함수 / SUBSAMPLE'
weight: 25
toc: true
---

선택 여부 BOOL을 각 원본 행에 반환하는 윈도 함수입니다. 절 형태의 SUBSAMPLE은
시각 인자를 생략하며 선택된 행만 반환합니다. 아래 문법은 윈도 함수 호출 형식입니다.

## LTTB {#lttb}

```bnf
<lttb_call> ::= "LTTB" "(" <timestamp> "," <value> "," <target> ")"
                | "LTTB" "(" <timestamp> "," <value> "," <target> "," <gap> ")"
```

삼각형 면적으로 굴곡을 선택합니다. gap으로 나눈 구간의 양끝을 보존하면 target을 넘을 수 있습니다.
호출 뒤에 OVER (ORDER BY ...)를 지정합니다. 반환형은 BOOL입니다. 인자 범위와
NULL·정렬 제약은 [공통 규칙](#subsample-function-rules)을 따릅니다.

[공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT ID FROM (
    SELECT ID,LTTB(TIME,V,4) OVER(ORDER BY TIME) AS KEEP FROM TS13_SUB
) Q WHERE KEEP ORDER BY ID;
```

선택 ID는 0·3·4·7입니다.

## MINMAX {#minmax}

```bnf
<minmax_call> ::= "MINMAX" "(" <timestamp> "," <value> "," <target> ")"
```

시간 구간별 최소·최대 원본 행을 선택합니다. 끝 관측을 반드시 보존하지 않습니다.
호출 뒤에 OVER (ORDER BY ...)를 지정합니다. 반환형은 BOOL입니다. 인자 범위와
NULL·정렬 제약은 [공통 규칙](#subsample-function-rules)을 따릅니다.

[공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT ID FROM (
    SELECT ID,MINMAX(TIME,V,4) OVER(ORDER BY TIME) AS KEEP FROM TS13_SUB
) Q WHERE KEEP ORDER BY ID;
```

선택 ID는 0·3·4·5입니다.

## M4 {#m4}

```bnf
<m4_call> ::= "M4" "(" <timestamp> "," <value> "," <target> ")"
```

구간별 시작·종료·최소·최대 행을 선택하고 같은 행은 한 번만 남깁니다.
호출 뒤에 OVER (ORDER BY ...)를 지정합니다. 반환형은 BOOL입니다. 인자 범위와
NULL·정렬 제약은 [공통 규칙](#subsample-function-rules)을 따릅니다.

[공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT ID FROM (
    SELECT ID,M4(TIME,V,4) OVER(ORDER BY TIME) AS KEEP FROM TS13_SUB
) Q WHERE KEEP ORDER BY ID;
```

선택 ID는 0·3·4·7입니다.

## UNIFORM {#uniform}

```bnf
<uniform_call> ::= "UNIFORM" "(" <target> ")"
```

값과 관계없이 행 위치를 고르게 선택합니다. target 이하 입력은 모두 보존하며 양끝을 포함합니다.
호출 뒤에 OVER (ORDER BY ...)를 지정합니다. 반환형은 BOOL입니다. 인자 범위와
NULL·정렬 제약은 [공통 규칙](#subsample-function-rules)을 따릅니다.

[공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT ID FROM (
    SELECT ID,UNIFORM(4) OVER(ORDER BY TIME) AS KEEP FROM TS13_SUB
) Q WHERE KEEP ORDER BY ID;
```

선택 ID는 0·2·5·7입니다.

## CADENCE {#cadence}

```bnf
<cadence_call> ::= "CADENCE" "(" <stride> ")"
                | "CADENCE" "(" <stride> "," <seed> ")"
```

행 간격으로 선택합니다. 생략 seed의 offset은 0이며 마지막 행도 보존합니다. stride가 입력 수보다 크면 첫 행만 선택합니다.
호출 뒤에 OVER (ORDER BY ...)를 지정합니다. 반환형은 BOOL입니다. 인자 범위와
NULL·정렬 제약은 [공통 규칙](#subsample-function-rules)을 따릅니다.

[공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT ID FROM (
    SELECT ID,CADENCE(3) OVER(ORDER BY TIME) AS KEEP FROM TS13_SUB
) Q WHERE KEEP ORDER BY ID;
```

선택 ID는 0·3·6·7입니다.

## SDT {#sdt}

```bnf
<sdt_call> ::= "SDT" "(" <timestamp> "," <value> "," <compdev> ")"
```

값 단위의 허용 편차로 직선 구간의 관측을 줄입니다. 기본 RESPECT NULLS이며 IGNORE NULLS도 지정할 수 있습니다.
호출 뒤에 OVER (ORDER BY ...)를 지정합니다. 반환형은 BOOL입니다. 인자 범위와
NULL·정렬 제약은 [공통 규칙](#subsample-function-rules)을 따릅니다.

[공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT ID FROM (
    SELECT ID,SDT(TIME,V,0) OVER(ORDER BY TIME) AS KEEP FROM TS13_SUB
) Q WHERE KEEP ORDER BY ID;
```

선택 ID는 0~7 전체입니다.

## 공통 규칙 {#subsample-function-rules}

target은 2~2147483647, stride는 1~2147483647의 정수 문장 상수 또는 지원 bind입니다.
gap은 '2s'처럼 양수 정수와 s/m/h/d 단위 문자열입니다. compdev는 유한한 0 이상 상수이며
bind는 거부합니다. seed는 정수이고 NULL 리터럴은 실행별 선택, NULL bind는 오류입니다.
LTTB·MINMAX·M4·SDT의 timestamp는 명시 시각 인자이며 정렬은 모두 ASC입니다.
PARTITION BY와 RESPECT/IGNORE NULLS는 SDT에 사용합니다. 별도 ROWS/RANGE 프레임은
지원하지 않습니다. value 기반 알고리즘은 DECIMAL 입력을 지원하지 않으며 LTTB·MINMAX·
M4는 NULL 시각·NULL·NaN·Inf 값을 후보에서 제외합니다. UNIFORM·CADENCE는 값과 관계없이
행을 셉니다. 선택 결과를 거르는 WHERE는 바깥 SELECT에 작성합니다.

[SUBSAMPLE 절과 윈도 형태의 전체 BNF](../../syntax/subsample-syntax/)를 참고합니다.

## 실행 예제

[공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT ID,V FROM (SELECT ID,TIME,V,lttb(TIME,V,4) OVER(ORDER BY TIME) AS KEEP FROM TS13_SUB) s WHERE KEEP ORDER BY TIME;
```
