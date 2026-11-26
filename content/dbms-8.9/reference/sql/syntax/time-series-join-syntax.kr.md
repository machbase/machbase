---
type: docs
title: '시계열 JOIN / TIMESTAMP / TIE'
weight: 81
toc: true
---

Standard Edition에서 사용합니다. BNF의 ε는 생략입니다. expression·column·alias·source는
각각 SELECT의 식·컬럼·별칭·테이블 또는 파생 조회를 뜻합니다. 타입·범위와 조합 제한은
BNF 아래의 규칙을 함께 적용합니다.

## 입력 시간축과 키

```bnf
<time_source> ::= <source> <alias_opt> <timestamp_opt>
<alias_opt> ::= ε | <alias> | "AS" <alias>
<timestamp_opt> ::= ε | "TIMESTAMP" "(" <column> ")"
<key_condition> ::= <left_key> "=" <right_key>
                  | <key_condition> "AND" <left_key> "=" <right_key>
<column_list> ::= <column> | <column_list> "," <column>
```

TAG는 생략 시 BASETIME입니다. 자동 시간축이 없는 입력에는 DATETIME을 명시합니다.
계산 시각은 파생 SELECT에 컬럼으로 공개한 뒤 지정합니다. ON에는 양측 동등 비교를
AND로 연결합니다. NULL 키는 동등 매칭되지 않습니다. 입력 WHERE는 후보를 제한하고
최종 WHERE는 선택 결과를 거릅니다. 최종 WHERE가 행을 제거해도 다음 후보를 다시 찾지 않습니다.
WITH SOURCE는 시간축 뒤에 둡니다. [출처 선언](../source-provenance-syntax/)을 참고합니다.

## ASOF / LT / NEAREST

```bnf
<single_time_join> ::= <time_source> <selection> "JOIN" <time_source>
                      "ON" <key_condition> <tolerance_opt> <tie_opt>
<selection> ::= "ASOF" | "LT" | "NEAREST"
<tolerance_opt> ::= ε | "TOLERANCE" <duration_value>
<duration_value> ::= <fixed_duration_literal> | "(" <integer_ns_expression> ")"
<tie_opt> ::= ε | "TIE" "ERROR"
            | "TIE" "FIRST" "BY" <tie_keys>
            | "TIE" "LAST" "BY" <tie_keys>
<tie_keys> ::= <column> | "(" <column_list> ")"
```

| 방식 | 선택할 오른쪽 관측 |
|---|---|
| ASOF | 왼쪽 시각 이하의 최신 행 |
| LT | 왼쪽 시각보다 엄격히 이전인 최신 행 |
| NEAREST | 전후 절대 시간차가 최소인 행. 등거리면 과거 |

왼쪽을 유지하며 미매칭은 오른쪽 NULL입니다. TOLERANCE 경계를 포함하며 생략하면 제한이
없습니다. 리터럴은 5s·200ms·1h30m 같은 고정 기간, 괄호 식은 정수 나노초입니다.
0은 정확 일치만 허용하므로 LT의 0은 미매칭입니다. 기본 TIE는 ERROR이며 FIRST/LAST는
동일 시각 후보를 비NULL·고유하게 구분하는 BY 키를 요구합니다.
연속 시간 JOIN의 기준은 최초 왼쪽 시각입니다.

## INTERPOLATE

```bnf
<interpolate_join> ::= <time_source> "INTERPOLATE" "JOIN" <time_source>
                      "ON" <key_condition>
                      "COLUMNS" "(" <column_list> ")"
                      "MAX" "GAP" <duration_value> <tie_opt>
```

COLUMNS는 오른쪽 수치 scalar·수치 ARRAY 컬럼입니다. 임의 식은 먼저 파생 입력의
컬럼으로 공개합니다. 목록 밖의 오른쪽 출력은 지원하는 직접 동등 키만 조회합니다.
MAX GAP은 양수이며 두 원본 endpoint의 전체 간격에 적용합니다. 정확 일치는 실측,
나머지는 두 endpoint가 있고 간격이 한계 이내인 경우에만 선형 보간합니다. 한쪽이
없거나 NULL이면 NULL이며 외삽하지 않습니다. 부분 NULL은 해당 원소에 유지합니다.
정수·부동소수점은 DOUBLE, 수치 ARRAY는 같은 길이의 DOUBLE ARRAY로 승격합니다.
DECIMAL은 정수 자리수를 보존해 정밀도를 확장합니다. 실제 배열 길이가 다르면 오류입니다.

## WINDOW

```bnf
<window_join> ::= <time_source> "WINDOW" "JOIN" <time_source>
                 "ON" <key_condition>
                 "RANGE" "BETWEEN" <window_bound> "AND" <window_bound>
                 <prevailing_opt> <tie_opt>
<window_bound> ::= "CURRENT" "ROW"
                 | <integer_expression> <window_unit> <direction>
                 | <fixed_duration_literal> <direction>
<direction> ::= "PRECEDING" | "FOLLOWING"
<window_unit> ::= "nanoseconds" | "microseconds" | "milliseconds"
                | "seconds" | "minutes" | "hours" | "days"
<prevailing_opt> ::= ε | "INCLUDE" "PREVAILING" | "EXCLUDE" "PREVAILING"
```

단위는 단수 표기도 허용합니다. 창은 양끝을 포함하고 왼쪽의 정수식으로 폭을 지정할 수
있습니다. 음수 폭은 0으로, NULL 경계는 빈 창으로 처리합니다. 역순 창과 UNBOUNDED는
오류입니다. 오른쪽은 집계로 반환하며 빈 창의 COUNT(*)·COUNT(expr)는 0입니다.
기본 EXCLUDE PREVAILING입니다. INCLUDE는 하한에 적격 관측이 없을 때 하한 직전
상태 한 행을 추가합니다. TIE는 이 추가 대표의 중복을 처리합니다. 창 안의 행은
동일 시각도 모두 집계합니다.

## HORIZON

```bnf
<horizon_chain> ::= <time_source> <horizon_joins> <horizon_offsets>
<horizon_joins> ::= <horizon_join> | <horizon_joins> <horizon_join>
<horizon_join> ::= "HORIZON" "JOIN" <time_source>
                  "ON" <key_condition> <tolerance_opt> <tie_opt>
<horizon_offsets> ::= "LIST" "(" <offset_list> ")" "AS" <alias>
                    | "RANGE" "FROM" <offset> "TO" <offset>
                      "STEP" <offset> "AS" <alias>
<offset_list> ::= <offset> | <offset_list> "," <offset>
<offset> ::= "0" | <signed_integer_with_horizon_unit>
```

offset 단위는 ns/us/ms/s/m/h/d입니다. 단위 없는 값은 0만 허용하며 계산식·bind·NULL과
복합 기간은 거부합니다. LIST는 중복 없이 증가해야 합니다. RANGE의 STEP은 양수이며
FROM은 TO 이하입니다. TO 이하까지 생성합니다. 각 기준 시각에 offset을 더해 ASOF로
선택하고 미매칭도 행을 유지합니다. alias.offset은 LONG 나노초, alias.timestamp는
조회 DATETIME입니다. 여러 HORIZON 뒤에 LIST/RANGE를 한 번 두면 같은 offset을 공유합니다.

## SPLICE

```bnf
<splice_join> ::= <time_source> "SPLICE" "JOIN" <time_source>
                 "ON" <key_condition> <splice_ties_opt>
<splice_ties_opt> ::= ε | <splice_tie> | <splice_tie> <splice_tie>
<splice_tie> ::= "TIE" <side> "ERROR"
               | "TIE" <side> "FIRST" "BY" <tie_keys>
               | "TIE" <side> "LAST" "BY" <tie_keys>
<side> ::= "LEFT" | "RIGHT"
```

각 측의 TIE는 한 번씩 지정합니다. 양쪽 사건 시각에서 최신 상태를 결합하고 원본 시각은
유지합니다. 같은 시각의 peer는 논리 순서로 짝지으며 이어갈 대표는 측별 FIRST/LAST로
선택합니다. 기본 ERROR는 대표가 실제 모호할 때 진단합니다. NULL 키·시각의 원본 행은
반대쪽 NULL과 함께 보존합니다.

## 실행 예제

[13장 공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT e.ID AS EVENT_ID,CAST((TO_TIMESTAMP(e.TIME)-1798729200000000000)/1000000000 AS LONG) AS EVENT_S,
 m.ID AS MOTOR_ID,CAST((TO_TIMESTAMP(m.TIME)-1798729200000000000)/1000000000 AS LONG) AS MOTOR_S,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e ASOF JOIN TS13_MOTOR m ON e.NAME=m.NAME
TOLERANCE 5s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

[13.1의 JOIN별 전체 결과와 경계 예제](../../../../time-series-sql/joins/)를 참고합니다.
