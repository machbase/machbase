---
type: docs
title: 'RETENTION'
weight: 160
toc: true
---

RETENTION 정책은 TAG, KV, LOG 테이블에서 보존 기간을 지난 데이터를 주기적으로 삭제합니다.
TRANSACTION, LOOKUP, VOLATILE에는 적용할 수 없습니다.

<a id="create-retention"></a>

## RETENTION 정책 생성

```sql
create_retention_stmt ::=
    'CREATE RETENTION' policy_name
    'DURATION' positive_integer ( 'MONTH' | 'DAY' | 'HOUR' | 'MIN' | 'SEC' )
    'INTERVAL' positive_integer ( 'DAY' | 'HOUR' | 'MIN' | 'SEC' )
```

| 매개변수 | 설명 |
|----------|------|
| `policy_name` | 정책 이름 |
| `DURATION duration MONTH\|DAY\|HOUR\|MIN\|SEC` | 데이터 보존 기간 (`MONTH`는 고정 30일) |
| `INTERVAL interval DAY\|HOUR\|MIN\|SEC` | 삭제 실행 주기 |

```sql
-- 1일 보존, 1시간마다 삭제 실행
CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;

-- 30일 보존, 1일마다 삭제 실행
CREATE RETENTION policy_30d_1d DURATION 30 DAY INTERVAL 1 DAY;

-- 3개월 보존, 1일마다 삭제 실행
CREATE RETENTION policy_3m_1d DURATION 3 MONTH INTERVAL 1 DAY;
```

<a id="drop-retention"></a>

## RETENTION 정책 삭제

```sql
drop_retention_stmt ::= 'DROP RETENTION' policy_name
```

```sql
DROP RETENTION policy_1d_1h;
```

## 테이블에 RETENTION 정책 적용

```sql
alter_table_add_retention_stmt ::=
    'ALTER TABLE' table_name 'ADD RETENTION' policy_name
    [ 'START AT' start_time ]

start_time ::= 'HH:MI'
             | TO_DATE('datetime_string')
             | TO_DATE('datetime_string', 'format_string')
```

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h;
```

<a id="retention-start-at-syntax"></a>

### START AT 입력 계약

START AT은 DBMS 8.9의 테이블별 Retention 작업에 최초 실행 기준을 지정합니다.
CREATE RETENTION에는 지정하지 않습니다. 생략하면 기존 실행·오류 재시도 방식을 유지합니다.

| 형식 | 의미와 검증 |
|---|---|
| 'HH:MI' | 정확히 5글자, 00:00~23:59. 실행 시 서버의 오늘 날짜와 결합. 현재 이하이면 다음 날 |
| TO_DATE('문자열') | 실행 시점보다 미래인 날짜·시각. 형식 생략 시 세션 DEFAULT_DATE_FORMAT 사용 |
| TO_DATE('문자열','형식') | 문자열 상수 2개로 명시적으로 해석한 미래 날짜·시각 |

모든 시작 시각은 서버 시간대로 해석합니다. 클라이언트·세션 시간대로 해석하지 않습니다.
PREPARE는 구문 형태·문자열 상수 타입·인자 개수를 확인하고, EXECUTE는 값 형식·범위·날짜와
미래 여부를 검사합니다. 재실행 때는 실행 시점에서 다시 판정합니다.

다음 두 명령은 각각 독립적인 적용 방법입니다. 이미 연결된 테이블에 다시 ADD하면 오류입니다.

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h START AT '02:00';
```

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h
    START AT TO_DATE('2099-01-02 02:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

2099년 날짜는 예시입니다. 실제 사용할 미래 날짜로 바꿉니다.

### 거부되는 입력

기존 sensor_tag와 아직 적용하지 않은 정책을 가정하며, 아래는 정상 실습과 분리하는 오류 SQL입니다.

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h START AT '24:00';
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h START AT '2:00';
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h START AT '02:00:00';
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h START AT NULL;
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h START AT NOW;
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h START AT ?;
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h
    START AT TO_DATE('2000-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

형식·범위 위반, NULL·일반 계산식·서브쿼리·bind, 상수가 아닌 TO_DATE 인자는 지원하지 않습니다.
날짜 지정은 현재와 같거나 과거여도 오류입니다. 날짜·간격의 표현 범위 초과도 오류로 거부합니다.
HH:MI의 실행 시각 동일 조건은 오류 대신 다음 날로 넘어가므로 날짜 지정과 구분합니다.

### 일정과 상태

START AT으로 정한 T0를 기준으로 T0+n×INTERVAL을 유지합니다. 성공 후 다음 예정은 완료
시각보다 뒤인 원래 슬롯입니다. 재시작 때 지난 회차는 한 번 실행하고 원래 주기로 복귀합니다.
DURATION의 삭제 cutoff는 실제 실행 시각 기준이며, 예정 시각으로 바꾸지 않습니다.

[운영 예제](/kr/dbms-8.9/operations-configuration-recovery/policy-data-retention/#retention-start-at)에서
시간대·DST·재시작·변경 절차를 확인합니다.

## 테이블에서 RETENTION 정책 해제

```sql
alter_table_drop_retention_stmt ::=
    'ALTER TABLE' table_name 'DROP RETENTION'
```

```sql
ALTER TABLE sensor_tag DROP RETENTION;
```

## RETENTION 정책 목록 조회

시스템 테이블에서 등록된 RETENTION 정책과 적용 현황을 조회합니다.

```sql
-- 모든 RETENTION 정책 조회
SELECT * FROM M$RETENTION;

-- 테이블별 적용 작업과 마지막 삭제 기준 확인
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE,
       LAST_DELETED_TIME, START_TIME, NEXT_RUN_TIME
  FROM V$RETENTION_JOB
 ORDER BY USER_NAME, TABLE_NAME;
```

## 전체 예시

새 전용 실습 DB에서 같은 이름의 정책·테이블이 없을 때 한 번 실행합니다.
이미 객체가 있으면 중단하고 다른 이름을 사용합니다.

```sql
-- 1. RETENTION 정책 생성 (1일 보존, 1시간마다 삭제)
CREATE RETENTION ret_1d DURATION 1 DAY INTERVAL 1 HOUR;

-- 2. TAG 테이블 생성
CREATE TAG TABLE sensor_tag (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 3. 야간 시각부터 시작하는 테이블별 작업 연결
ALTER TABLE sensor_tag ADD RETENTION ret_1d START AT '02:00';

-- 4. 최초 기준과 현재 미완료 회차 확인
SELECT TABLE_NAME, START_TIME, NEXT_RUN_TIME
  FROM V$RETENTION_JOB WHERE TABLE_NAME = 'SENSOR_TAG';

-- 5. 정책 해제
ALTER TABLE sensor_tag DROP RETENTION;

-- 6. 정책 삭제
DROP RETENTION ret_1d;

-- 7. 직접 만든 실습 테이블 정리
DROP TABLE sensor_tag;
```

## 주의사항

- RETENTION 정책은 LOG 테이블과 TAG 테이블에 적용할 수 있습니다.
- KV 테이블에도 적용할 수 있습니다.
- 한 테이블에는 하나의 RETENTION 정책만 적용할 수 있습니다.
- `MONTH`는 달력 월이 아니라 고정 30일로 계산됩니다. 달력 경계가 중요한 정책은 `DAY` 단위로
  환산하고 실제 삭제 기준을 검증합니다.
- RETENTION 작업이 삭제한 row는 되돌릴 수 없으므로 보존 기간과 실행 주기를 신중하게
  설정합니다. `DROP RETENTION`은 table에서 정책을 모두 해제한 뒤 정책 객체만 삭제합니다.
- `INTERVAL`은 삭제 작업 실행 주기이며, 실제 시작은 부하·재시도에 따라 지연될 수 있습니다.
- 시작 시각 변경은 DROP RETENTION 후 새 START AT으로 재ADD합니다. 두 명령 사이에는 연결이 없습니다.
- NEXT_RUN_TIME은 현재 미완료 회차, LAST_DELETED_TIME은 마지막 성공한 DELETE cutoff입니다.
  START AT 생략 시 START_TIME·NEXT_RUN_TIME은 NULL입니다.
- 존재하지 않는 정책, 지원하지 않는 테이블 타입, 한 테이블의 중복 정책 적용은 오류입니다.
- 적용 중인 정책 객체는 모든 테이블에서 해제한 뒤 삭제합니다.

## 관련 문서

- [Retention Policy 역할](/dbms-8.9/core-concepts/features-concepts/#role-retention-policy) — 자동 데이터 삭제 정책 개념

- [V$RETENTION_JOB](/kr/dbms-8.9/reference/system-catalog/virtual-table-full/#vretention_job) — 상태 컬럼 정의
