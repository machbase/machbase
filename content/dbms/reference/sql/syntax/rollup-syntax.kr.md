---
type: docs
title: 'ROLLUP'
weight: 180
toc: true
---

ROLLUP은 시간축 TAG의 반복 집계를 위한 저장·조회 기능입니다. 일반·조건·확장 ROLLUP은
공개 `rollup()` 조회로, Custom은 사용자 대상 TAG의 재집계로 읽습니다.

<a id="create-rollup"></a>

## 생성

다음은 문법 형식이며 대괄호·중괄호를 그대로 실행하지 않습니다.

```text
CREATE ROLLUP [IF NOT EXISTS] name
    ON source_tag [(column_name | json_path_expression)]
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }]
    [EXTENSION [ORDER BY basetime_column [ASC | DESC], data_column [ASC | DESC] [, ...]]]
    [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] name
    FROM source_rollup
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }]
    [EXTENSION [ORDER BY basetime_column [ASC | DESC], data_column [ASC | DESC] [, ...]]]
    [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] name
    INTO (destination_tag)
    AS (SELECT ...)
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }];
```

- EXTENSION에는 선택적으로 ORDER BY 정렬 키를 지정합니다. 별도의 extension_name은 붙이지 않습니다.
- CREATE의 시간 단위는 SEC/MIN/HOUR입니다. DAY 등은 조회 단위와 구분합니다.
- 일반 숫자 컬럼은 SUMMARIZED 없이 명시할 수 있습니다. JSON 경로 집계와 JSON
  문서 전체 집계를 구분하며, 문서 전체와 WITH ROLLUP 자동 생성에는 SUMMARIZED 조건이 있습니다.
- FROM 간격은 소스보다 큰 정수배이며 확장 속성·집계 모드가 맞아야 합니다.
- WAKEUP은 양수, 집계 간격 이하이며 그 간격을 나누어떨어지게 해야 합니다.
- Custom은 Standard 전용이고 소스 TAG 하나와 미리 만든 대상 TAG가 필요합니다.
  WHERE는 SELECT 내부에 쓰고 BASETIME 직접 조건·JOIN·FROM 서브쿼리는 허용하지 않습니다.
- IF NOT EXISTS는 기존 이름에 대해 생성하지 않는 동작이지 정의를 수정하거나 비교해
  일치시키는 기능이 아닙니다. 문법과 소스 검증을 모두 무시하는 옵션도 아닙니다.

<a id="drop-rollup"></a>

## 삭제

```sql
DROP ROLLUP rollup_name;
```

참조하는 상위 ROLLUP부터 삭제합니다. Custom 대상 TAG는 관련 작업이 남아 있으면 DROP이
거부됩니다. 원본 TAG의 CASCADE는 관련 ROLLUP 제거 범위까지 확인한 뒤 사용하며,
사용자 Custom 대상 테이블은 별도 수명주기로 관리합니다.

<a id="alter-rollup"></a>

## 제어

```sql
ALTER ROLLUP rollup_name STOP;
ALTER ROLLUP rollup_name START;
ALTER ROLLUP rollup_name WAKEUP;
ALTER ROLLUP rollup_name FORCE;
ALTER ROLLUP rollup_name SET WAKEUP INTERVAL 10 SEC;
```

이 명령은 이미 존재하는 작업과 간격 조건을 전제로 합니다.
생성 시 자동 시작되며 이미 시작·중지된 상태를 반복 지정하면 오류가 날 수 있습니다.
WAKEUP은 완료를 기다리지 않고 FORCE는 대상의 소스 처리 범위를 따라잡도록 기다립니다.
과거 원본 보정에는 [REBUILD의 별도 지원 범위](../rollup-rebuild-syntax/)를 확인합니다.

## 조회와 후보 선택

```text
rollup(time_unit, period, basetime_column [, origin])
```

반환 타입은 DATETIME입니다. period는 양의 정수 리터럴입니다. 일반 DATE_TRUNC +
GROUP BY 쿼리가 ROLLUP의 존재만으로 자동 전환된다고 안내하지 않습니다. ROLLUP 조회에는
`rollup()`을 명시하고, 적용 가능한 후보가 없으면 별도의 원본 쿼리를 사용합니다.

자동 선택은 컬럼·경로·모드와 FIRST/LAST의 정렬 키·방향에 맞는 후보 중 조건 없는 후보를 먼저 찾습니다.
두 종류를 사용할 수 있는 일반 집계는 같은 조건 범주에서 값 컬럼이 NULL을 허용하면
정렬 정의 없는 후보를 우선하며, NOT NULL이 확인되면 동등하게 취급합니다.
`COUNT(*)`는 값 컬럼의 NOT NULL을 추정하지 않습니다.
그 뒤 조회 주기를 나누어떨어지게 하는 가장 큰 유효 간격을 선택하며, 같은 간격은 등록 순서를 따릅니다.
특정 데이터 집합을 고정하려면 ROLLUP_TABLE 힌트를 사용합니다.
[상세 선택 규칙](../../../../tag-rollup-usage/extension-rollup/#ordered-rollup-selection)을 확인하십시오.

SEC/MIN의 후보 간격은 period초/분을 기준으로 하며 HOUR·DAY·WEEK·MONTH·YEAR는
후보 선택 단계에서 period시간을 기준으로 검사합니다. 결과 버킷의 달력 계산과 별개의
규칙입니다. 월·년 origin은 월의 1일 조건을 확인합니다.

SELECT에 name을 반환하는 태그별 집계는 GROUP BY에도 name을 포함합니다.
시간 범위·origin·NULL 처리와 후보 조건을 맞춘 뒤 원본 결과와 비교합니다.
일반 숫자 ROLLUP은 MIN/MAX/SUM/COUNT/AVG/SUMSQ, 확장은 FIRST/LAST를 추가로 지원합니다.
원본 FIRST/LAST 사용과 저장 ROLLUP의 확장 필요조건을 구분합니다.
JSON의 문서 전체 COUNT와 경로별 건수는 별도 계약입니다.

실행 가능한 생성·조회·오류 예제는 [6장 ROLLUP 활용](/dbms/tag-rollup-usage/)과
[조회 문법](/dbms/tag-rollup-usage/query-syntax-rollup/)을 참고하십시오.

## 정렬 EXTENSION 정의

> 복합 키 FIRST/LAST와 정렬 EXTENSION ROLLUP은 Machbase 8.7.3부터 지원합니다. 에디션별 제약은 아래 설명을 확인하십시오.

```text
CREATE ROLLUP [IF NOT EXISTS] name
    ON source_tag (numeric_column)
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }]
    EXTENSION ORDER BY basetime_column [ASC | DESC],
                       data_column [ASC | DESC] [, ...]
    [WHERE predicate];
```

ON 정의의 EXTENSION 뒤에 ORDER BY를 지정합니다. 기존 EXTENSION만 사용하는 문법도 유지합니다.
FROM 계층은 ORDER BY를 생략하면 하위의 키와 방향을 상속합니다.
명시한다면 하위와 같은 키·방향이어야 합니다.
Custom INTO...AS에서는 이 절을 사용하지 않고 SELECT 내부에 복합 키 FIRST/LAST를 지정합니다.

[전체 데이터와 정렬 ROLLUP 예제](../../../../tag-rollup-usage/extension-rollup/#composite-first-last).
