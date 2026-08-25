---
type: docs
title: '6.1 ROLLUP 개요와 사용 기준'
weight: 10
toc: true
---
ROLLUP은 TAG 테이블의 숫자형 `SUMMARIZED` 컬럼을 지정한 시간 구간으로 미리 집계해 반복
조회 비용을 줄입니다. 원시 데이터 보관이나 임의의 쿼리 결과 캐시를 대신하는 기능은
아닙니다.

<a id="original-85-rollup-tables"></a>

## 사용 기준

| 요구사항 | 선택 |
| --- | --- |
| 초·분·시간 단위 통계를 반복 조회 | 기본 ROLLUP |
| 다른 구간 또는 조건 집계 | 사용자 정의 ROLLUP |
| 구간의 첫 값·마지막 값 필요 | 확장 ROLLUP |
| WEEK·MONTH·YEAR 달력 구간 | 해당 시간 단위와 기준 시각 검토 |
| 원시 값 조회가 대부분 | ROLLUP 없이 시작하고 측정 |
| 거리축 TAG | ROLLUP 미지원, 쿼리 집계 사용 |

ROLLUP을 추가하면 집계 저장 공간과 입력 후 집계 작업이 필요합니다. 대표 쿼리의 조회 빈도,
원시 데이터량과 허용 지연을 측정한 뒤 적용하십시오.

## 기본 동작

시간축 TAG의 집계 대상 숫자 컬럼에 `SUMMARIZED`를 지정하고 `WITH ROLLUP`으로 기본 계층을
만들 수 있습니다. 애플리케이션은 생성되는 시스템 객체 이름을 직접 사용하지 않고 원본 TAG
테이블과 공개 ROLLUP SQL을 사용합니다.

```sql
CREATE TAG TABLE rollup_overview_demo (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);

INSERT INTO rollup_overview_demo
VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0);
INSERT INTO rollup_overview_demo
VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0);

EXEC TABLE_FLUSH(rollup_overview_demo);

SELECT rollup('min', 1, time) AS minute,
       AVG(value) AS avg_value
  FROM rollup_overview_demo
 WHERE name = 'TEMP_01'
 GROUP BY minute
 ORDER BY minute;

DROP TABLE rollup_overview_demo CASCADE;
```

ROLLUP 집계는 원시 데이터 입력과 비동기로 진행될 수 있습니다. 입력 직후 결과가 필요하면
[ROLLUP 상태와 지연 확인](../state-check-rollup/)에서 처리 상태를 확인하십시오.

## 설계 순서

1. 반복되는 조회의 시간 단위와 집계 함수를 정합니다.
2. 집계 대상 숫자 컬럼에 `SUMMARIZED`가 필요한지 확인합니다.
3. 기본 계층으로 충분한지, 사용자 정의·조건·확장 ROLLUP이 필요한지 선택합니다.
4. 원시 데이터와 ROLLUP의 보관·재구성 정책을 각각 정합니다.
5. 운영 데이터량으로 입력 부하, 집계 지연, 조회 시간을 측정합니다.

## 상세 문서

| 작업 | 문서 |
| --- | --- |
| 생성·삭제 | [ROLLUP 생성과 삭제](../create-delete-rollup/) |
| 조회 문법 | [ROLLUP 조회](../query-syntax-rollup/) |
| 사용자 정의 집계 | [Custom ROLLUP](../custom-rollup/) |
| 조건 집계 | [Conditional ROLLUP](../conditional-rollup/) |
| FIRST·LAST | [확장 ROLLUP](../extension-rollup/) |
| 달력 단위와 시간대 | [WEEK·MONTH·YEAR와 시간대](../week-month-year-timezone-rollup/) |
| JSON 집계 | [JSON SUMMARIZED ROLLUP](../json-summarized-rollup/) |
| 수정·삭제 후 재구성 | [ROLLUP 재구성](../rollup-rebuild/) |
| 장애 진단 | [ROLLUP 문제 해결](/dbms/troubleshooting/rollup/) |

전체 SQL 형식은 [ROLLUP 구문 사전](/dbms/reference/sql/syntax-dictionary-sql/rollup-syntax/)을
기준으로 확인하십시오.
