---
title: '5.7 운영과 데이터 생명주기'
weight: 70
toc: true
---
TAG 데이터의 수명 주기는 수동 삭제, Retention Policy와 중복 입력 방지로 관리합니다. 이
페이지는 운영 선택 기준을 설명하며 전체 SQL 문법은 관련 레퍼런스로 연결합니다.

<a id="original-85-deleting-data"></a>

## TAG 데이터 삭제

TAG 데이터는 태그 식별자와 축 조건을 사용해 삭제 범위를 제한합니다. 시간축 TAG의 대표적인
선택은 다음과 같습니다.

| 목적 | 조건 |
| --- | --- |
| 한 태그의 전체 데이터 삭제 | 태그 `PRIMARY KEY` 일치 |
| 한 태그의 시간 범위 삭제 | 태그 일치 + BASETIME 범위 |
| 모든 태그의 과거 데이터 삭제 | BASETIME 조건 또는 `BEFORE` |
| 테이블의 전체 데이터 삭제 | 조건 없는 TAG `DELETE` |

다음 예제는 별도 검증 테이블을 만들고 삭제 범위를 확인한 뒤 정리합니다.

```sql
CREATE TAG TABLE lifecycle_tag (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);

INSERT INTO lifecycle_tag VALUES
    ('TAG_0001', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1.0);
INSERT INTO lifecycle_tag VALUES
    ('TAG_0001', TO_DATE('2026-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2.0);
INSERT INTO lifecycle_tag VALUES
    ('TAG_0002', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3.0);

DELETE FROM lifecycle_tag
 WHERE name = 'TAG_0001'
   AND time < TO_DATE('2026-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');

SELECT name, time, value
  FROM lifecycle_tag
 ORDER BY name, time;

DELETE FROM lifecycle_tag;
DROP TABLE lifecycle_tag;
```

삭제 조건의 연산자와 Edition별 지원 범위는
[TAG DELETE 구문](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/)을
참고하십시오. 수동 삭제를 주기적으로 반복해야 한다면
[Retention Policy](/dbms/operations-configuration-recovery/policy-data-retention/)를
사용하십시오.

### ROLLUP 데이터 처리

원시 TAG 데이터의 삭제와 이미 계산된 ROLLUP의 처리는 별개입니다. 원시 데이터를 정정하거나
삭제한 뒤 집계도 바뀌어야 한다면 대상 범위의 ROLLUP을 재구성합니다. ROLLUP 삭제 구문을
보관 정책처럼 반복 실행하지 마십시오.

- [ROLLUP 부분 삭제와 재구성](/dbms/tag-rollup-usage/rollup-rebuild/)
- [TAG 데이터 정정 후 ROLLUP 재구성](../tag-data-update-correction/)

<a id="original-85-duplication-removal"></a>

## 자동 중복 제거

`TAG_DUPLICATE_CHECK_DURATION`은 서버 현재 시각을 기준으로 지정 기간 안에 들어오는 입력에서
태그명, 축 값과 데이터 값이 같은 행을 중복으로 처리합니다. 재전송 가능성이 있는 수집
파이프라인에서 사용하고, 입력 지연이 설정 기간을 넘을 수 있는지 함께 검토하십시오.

```sql
CREATE TAG TABLE dedup_tag (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
) TAG_DUPLICATE_CHECK_DURATION = 1440;

INSERT INTO dedup_tag VALUES ('TAG_0001', DATE_TRUNC('day', NOW), 1.0);
INSERT INTO dedup_tag VALUES ('TAG_0001', DATE_TRUNC('day', NOW), 1.0);

EXEC TABLE_FLUSH(dedup_tag);

SELECT name, time, value
  FROM dedup_tag
 WHERE name = 'TAG_0001';

ALTER TABLE dedup_tag SET TAG_DUPLICATE_CHECK_DURATION = 60;
DROP TABLE dedup_tag;
```

설정 단위는 분이며 허용 범위는 현재 버전의
[CREATE TAG TABLE 구문](/dbms/reference/sql/syntax-dictionary-sql/ddl-syntax/)을 기준으로
확인하십시오. 이미 보관 정책으로 삭제된 데이터는 중복 판정 대상에 남아 있지 않습니다.

## 운영 점검 순서

1. 원시 데이터와 ROLLUP의 보관 기간을 각각 정합니다.
2. 늦게 도착하는 데이터의 최대 지연을 측정해 중복 검사 기간을 정합니다.
3. 삭제·정정 전에 대상 태그와 시간 범위를 `SELECT`로 확인합니다.
4. 대량 변경 후 ROLLUP과 대표 조회 결과를 검증합니다.
5. 입력량, 디스크 사용량과 Retention 실행 상태를 함께 모니터링합니다.
