---
type: docs
title: 'SAMPLE BY / FILL / ALIGN TO / EXPECT KEYS'
weight: 83
toc: true
---

Standard Edition에서 사용합니다. BNF의 ε는 생략입니다. expression·column·alias·source는
각각 SELECT의 식·컬럼·별칭·테이블 또는 파생 조회를 뜻합니다. 타입·범위와 조합 제한은
BNF 아래의 규칙을 함께 적용합니다.

## BNF

```bnf
<sample_opt> ::= ε | "SAMPLE" "BY" <interval> <bounds_opt> <fill_opt>
                    <align_opt> <expected_opt>
<bounds_opt> ::= ε | "FROM" <datetime_expression> "TO" <datetime_expression>
<fill_opt> ::= ε | "FILL" "(" <fill_list> ")"
<fill_list> ::= <fill_policy> | <fill_list> "," <fill_policy>
<fill_policy> ::= "NONE" | "NULL" | <typed_constant>
                | "PREV" "MAX" "AGE" <positive_fixed_duration>
                | "PREV" "(" <aggregate_alias> ")" "MAX" "AGE" <positive_fixed_duration>
                | "LINEAR" "MAX" "GAP" <positive_fixed_duration>
<align_opt> ::= ε
              | "ALIGN" "TO" "CALENDAR" <timezone_opt> <offset_opt>
              | "ALIGN" "TO" "FIRST" "OBSERVATION"
<timezone_opt> ::= ε | "TIME" "ZONE" <zone_name_expression>
<offset_opt> ::= ε | "WITH" "OFFSET" <offset_expression>
<expected_opt> ::= ε | "EXPECT" "KEYS" "(" <key_list> ")"
<key_list> ::= <key_value> | <key_list> "," <key_value>
<interval> ::= <positive_count_with_unit> | <unit>
<unit> ::= "ns" | "us" | "ms" | "s" | "m" | "h" | "d" | "w" | "mo" | "y"
```

SAMPLE 절은 WHERE·LATEST 뒤, GROUP BY 앞에 작성합니다.

## 간격·범위·정렬

- 간격은 1s·15m·1mo처럼 숫자와 단위를 붙이며 단일 단위입니다. 비집계 키로 시리즈를
  나누고 지정 시각은 버킷 시작으로 출력합니다.
- WHERE는 입력, FROM/TO는 출력 [FROM,TO)입니다. 입력에서 제거하지 않은 바깥 실측은
  FILL 근거로 사용할 수 있습니다. FROM=TO이면 0행, 역순이면 오류입니다.
- 기본 CALENDAR는 세션 UTC 오프셋입니다. TIME ZONE에 제품이 지원하는 IANA 이름을
  지정합니다. 결과 표시·입력 문자열 해석은 세션을 따릅니다. WITH OFFSET '00:30'은
  경계를 이동합니다. 지역 달력의 하루는 DST에서 23·25시간일 수 있습니다.
- FIRST OBSERVATION은 시리즈별 최소 실측이 원점이며 FROM/TO와 함께 사용하지 않습니다.
  CALENDAR의 명시 FROM은 출력 원점입니다.
- EXPECT KEYS는 관측 키에 기대 키를 추가합니다. 하나의 시리즈 키와 명시 FROM/TO가
  필요하며 NULL 기대 키는 거부합니다. FILL(NONE)은 기대 키라도 빈 행을 만들지 않습니다.

## 채움과 타입

| 정책 | 빈 버킷의 값 |
|---|---|
| 생략·NONE | 행 생략 |
| NULL·상수 | NULL 또는 출력 타입으로 검사한 상수 |
| PREV | 원래 관측 버킷에서 MAX AGE 이내의 이전값 |
| PREV(alias) | 같은 SELECT의 다른 집계 별칭의 이전값 |
| LINEAR | 두 실측 버킷 간격이 MAX GAP 이내일 때 보간 |

기간은 양수 고정 기간으로 ns/us/ms/s/m/h/d/w 또는 1h30m 같은 복합 기간을 사용합니다.
월·년은 고정 기간에 사용할 수 없습니다. 경계는 포함합니다. PREV는 채운 값으로 나이를
갱신하지 않고 LINEAR는 외삽하지 않으며 실측 NULL을 덮어쓰지 않습니다.
한 정책은 전체 집계에 적용합니다. 복수 정책은 공개 집계 순서에 하나씩 대응하며 시각·
시리즈 키·출처 열은 개수에서 제외합니다. NONE은 다른 정책과 섞지 않습니다.
교차 PREV는 원본·대상 집계 타입이 맞아야 하며 문자열 계열은 지원하지 않습니다.
LINEAR는 수치를 DOUBLE 계열로 승격하고 DECIMAL은 정수 자릿수를 보존해 확장합니다.
LINEAR 시리즈 키는 숨은 GROUP 키를 포함해 최대 하나입니다.

기간 누락은 ERR-02369, 잘못된 기간은 ERR-02370, 정책 수 불일치는 ERR-02373입니다.
FROM/TO와 FIRST OBSERVATION 충돌은 ERR-02384입니다.

## 실행 예제

[공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(LINEAR MAX GAP 4s)
) s ORDER BY NAME,B;
```

[13.3 범위·채움·시간대](../../../../time-series-sql/sample/)와
[13.5 기대 키·교차 PREV](../../../../time-series-sql/sampling-advanced/)를 참고합니다.
