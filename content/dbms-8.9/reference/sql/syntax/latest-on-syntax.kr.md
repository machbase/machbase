---
type: docs
title: 'LATEST ON'
weight: 82
toc: true
---

Standard Edition에서 사용합니다. BNF의 ε는 생략입니다. expression·column·alias·source는
각각 SELECT의 식·컬럼·별칭·테이블 또는 파생 조회를 뜻합니다. 타입·범위와 조합 제한은
BNF 아래의 규칙을 함께 적용합니다.

## BNF

```bnf
<latest_opt> ::= ε | "LATEST" "ON" <column> "PARTITION" "BY"
                    <column_list> <tie_opt>
<column_list> ::= <column> | <column_list> "," <column>
<tie_opt> ::= ε | "TIE" "ERROR"
            | "TIE" "FIRST" "BY" <tie_keys>
            | "TIE" "LAST" "BY" <tie_keys>
<tie_keys> ::= <column> | "(" <column_list> ")"
```

WHERE 뒤, SAMPLE BY·GROUP BY 앞에 둡니다. LATEST 컬럼은 지정 DATETIME 시간축과
같아야 합니다. WHERE를 통과한 입력의 키별 최신 한 행을 반환합니다. 입력이 없는 키는
출력하지 않습니다. 동률 기본은 ERROR이며 비NULL·고유 BY 키로 FIRST/LAST를 지정합니다.
최종 ORDER BY는 출력 순서입니다.

복합 키에서 VARCHAR가 마지막이 아닌 구성은 같은 그룹을 최신 한 행으로 줄이지 못할 수
있습니다. 검증된 수치 키와 마지막 VARCHAR 순서 및 경계 사례는
[13.2 LATEST ON](../../../../time-series-sql/latest/)을 참고합니다.

## 실행 예제

[공통 실습 준비](../../../../time-series-sql/#실습-준비) 후 실행합니다.

```sql
SELECT NAME,VALUE FROM TS13_STATUS  LATEST ON TIME PARTITION BY NAME ORDER BY NAME;
```
