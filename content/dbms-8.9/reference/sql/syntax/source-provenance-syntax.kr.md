---
type: docs
title: 'TIMESTAMP / WITH SOURCE / WITH PROVENANCE'
weight: 85
toc: true
---

Standard Edition에서 사용합니다. BNF의 ε는 생략입니다. expression·column·alias·source는
각각 SELECT의 식·컬럼·별칭·테이블 또는 파생 조회를 뜻합니다. 타입·범위와 조합 제한은
BNF 아래의 규칙을 함께 적용합니다.

## BNF

```bnf
<annotated_source> ::= <source> <alias_opt> <timestamp_opt> <source_opt>
<alias_opt> ::= ε | <alias> | "AS" <alias>
<timestamp_opt> ::= ε | "TIMESTAMP" "(" <column> ")"
<source_opt> ::= ε | "WITH" "SOURCE" "(" <source_items> ")"
<source_items> ::= <source_item> | <source_items> "," <source_item>
<source_item> ::= "ID" "(" <expression_list> ")"
                | "CLOCK_DOMAIN" "(" <expression> ")"
                | "CLOCK_SESSION" "(" <expression> ")"
                | "ORIGINAL_TIME" "(" <expression> ")"
                | "RECEIVED_TIME" "(" <expression> ")"
                | "CLOCK_VERSION" "(" <expression> ")"
                | "CLOCK_ERROR" "(" <expression> ")"
<expression_list> ::= <expression> | <expression_list> "," <expression>
<provenance_opt> ::= ε | "WITH" "PROVENANCE" <alias_clause_opt>
<alias_clause_opt> ::= ε | "AS" <alias>
```

## 선언 항목

| 항목 | 타입·규칙 |
|---|---|
| TIMESTAMP | 비교 DATETIME 컬럼. TAG는 생략 시 BASETIME |
| ID | 원본 행을 식별하는 안정적인 비NULL scalar tuple |
| CLOCK_DOMAIN | 문자열 clock 이름. 새 원본 입력 기본 utc |
| CLOCK_SESSION | 비UTC 실행 세션. 비UTC에서는 필수·비NULL |
| ORIGINAL_TIME·RECEIVED_TIME | 원본·수신 DATETIME. 미제공 시 NULL |
| CLOCK_VERSION | 외부 보정 버전 scalar |
| CLOCK_ERROR | 비음수 정수 나노초. 생략·NULL은 unknown |

SOURCE는 해당 입력의 공개 컬럼과 허용 scalar 식을 사용합니다. ID에는 집계·윈도·
서브쿼리·ARRAY·JSON·VECTOR를 사용하지 않습니다. 서로 다른 원본 행에 같은 ID를 주지
않습니다. domain/session이 다르면 결합 오류이며 CLOCK_ERROR는 허용차에 자동 가산하지
않습니다. domain 지정만으로 시각을 변환하지 않습니다. 파생 SAMPLE의 clock은 상속하며
실측이 없는 버킷은 unknown으로 남을 수 있습니다.

WITH PROVENANCE는 SUBSAMPLE 뒤, 최종 ORDER BY/LIMIT 앞에 작성합니다. JSON 열의 기본
이름은 _provenance이며 기존 열 이름과 충돌하면 오류입니다. 데이터 행 수·값을 유지합니다.
sources·columns의 ordinal은 1부터, JSON 배열 위치는 0부터입니다. 시각·기간·delta는
정확한 10진 나노초 문자열입니다. delta_ns는 선택 시각−기준 시각입니다. selected·left·right,
status·observed·reason으로 실제 NULL, 미매칭, 보간 양끝과 채움을 구분합니다.

## 실행 예제

[공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e WITH SOURCE(ID(ID),CLOCK_DOMAIN('utc'))
ASOF JOIN TS13_MOTOR m WITH SOURCE(ID(ID),CLOCK_DOMAIN('utc'))
ON e.NAME=m.NAME TOLERANCE 5s WHERE e.ID=2
WITH PROVENANCE AS P;
```

[13.9 전체 JSON 해석과 READ 원본 출처](../../../../time-series-sql/provenance/)를 참고합니다.
