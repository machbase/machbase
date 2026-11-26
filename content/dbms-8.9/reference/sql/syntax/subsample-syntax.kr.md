---
type: docs
title: 'SUBSAMPLE'
weight: 84
toc: true
---

Standard Edition에서 사용합니다. BNF의 ε는 생략입니다. expression·column·alias·source는
각각 SELECT의 식·컬럼·별칭·테이블 또는 파생 조회를 뜻합니다. 타입·범위와 조합 제한은
BNF 아래의 규칙을 함께 적용합니다.
## BNF

```bnf
<subsample_opt> ::= ε | "SUBSAMPLE" <method> <null_mode_opt>
<method> ::= "lttb" "(" <value> "," <target> <gap_opt> ")"
            | "minmax" "(" <value> "," <target> ")"
            | "m4" "(" <value> "," <target> ")"
            | "uniform" "(" <target> ")"
            | "cadence" "(" <stride> <seed_opt> ")"
            | "sdt" "(" <value> "," <compdev> ")"
<gap_opt> ::= ε | "," <gap_string>
<seed_opt> ::= ε | "," <integer_seed> | "," "NULL"
<null_mode_opt> ::= ε | "RESPECT" "NULLS" | "IGNORE" "NULLS"
```

WHERE·GROUP/SAMPLE/FILL·윈도 계산 뒤, 최종 ORDER BY/LIMIT 전에 작성합니다.

절 형태는 기준 시각 컬럼을 SELECT에 직접 포함해야 합니다. SAMPLE 뒤에서는 버킷 시각이
기준입니다. 선택된 원본의 값과 NULL을 유지하며 보간값을 새로 만들지 않습니다.

| 인자 | 범위·의미 |
|---|---|
| value | 정수·FLOAT·DOUBLE 수치 식. value 기반 알고리즘은 DECIMAL 인자를 지원하지 않음 |
| target | 2~2147483647의 정수 문장 상수 또는 지원 정수 bind |
| stride | 1~2147483647의 정수 문장 상수 또는 지원 정수 bind |
| gap_string | 양수 정수와 s/m/h/d 한 글자 단위의 문자열. 예를 들어 '2s'. ms/us/ns는 거부 |
| compdev | 유한한 0 이상의 수치 상수. bind는 거부 |
| seed | 재현 가능한 정수 seed. 생략 시 offset 0, 리터럴 NULL은 실행별 선택. bind NULL은 오류 |

RESPECT/IGNORE NULLS와 PARTITION BY는 SDT에 적용합니다. 기본은 RESPECT NULLS입니다.
SDT는 같은 수준의 JOIN·GROUP BY·SAMPLE BY·DISTINCT와 결합할 수 없으므로 파생 입력을
먼저 구성합니다. LTTB gap이 구간을 나누거나 MINMAX/M4에서 선택 행이 겹치면 반환 개수가
target과 다를 수 있습니다. LTTB·MINMAX·M4는 NULL 시각과 NULL·NaN·Inf 값을 제외합니다.
UNIFORM·CADENCE는 값과 무관하게 행을 셉니다. 선택 행의 별도 DECIMAL·ARRAY payload는 보존합니다.

## 윈도 함수 형태

```bnf
<keep_expression> ::= <window_method> <null_mode_opt> "OVER" "("
                      <partition_opt> "ORDER" "BY" <sort_list> ")"
<window_method> ::= "lttb" "(" <timestamp> "," <value> "," <target> <gap_opt> ")"
                   | "minmax" "(" <timestamp> "," <value> "," <target> ")"
                   | "m4" "(" <timestamp> "," <value> "," <target> ")"
                   | "uniform" "(" <target> ")"
                   | "cadence" "(" <stride> <seed_opt> ")"
                   | "sdt" "(" <timestamp> "," <value> "," <compdev> ")"
<partition_opt> ::= ε | "PARTITION" "BY" <expression_list>
```

원래 행마다 선택 여부 BOOL을 반환합니다. ORDER BY는 필수이며 lttb/minmax/m4/sdt의
정렬 키는 모두 ASC여야 합니다. ROWS/RANGE 프레임을 함께 지정하지 않습니다.
윈도 결과의 필터는 바깥 SELECT에서 적용합니다. partition·정렬 목록의 표기는
[OVER 문법](../window-function-over-syntax/#rows-bnf)을 따릅니다.

## 실행 예제

[공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE lttb(V,4) ORDER BY TIME;
```
```sql
SELECT ID,V FROM (SELECT ID,TIME,V,lttb(TIME,V,4) OVER(ORDER BY TIME) AS KEEP FROM TS13_SUB) s WHERE KEEP ORDER BY TIME;
```

[13.4 알고리즘별 그림과 전체 결과](../../../../time-series-sql/subsample/) 및
[윈도 형태의 추가 활용](../../../../time-series-sql/sampling-advanced/)을 참고합니다.
