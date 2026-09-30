---
title: 자동 저장소 관리
type: docs
weight: 51
---

## 소개

여러 소스에서 고빈도 데이터를 수집하는 시계열 데이터베이스에서는 데이터가 끊임없이 쌓입니다. 초당 수백만 건의 데이터를 적재하려면 큰 저장 용량이 필요합니다. 디스크 사용량을 직접 점검하고 주기적으로 `DELETE`를 실행해 공간을 확보하는 방식은 운영이 번거롭고 오류 가능성도 높습니다. 또한 많은 시스템은 특정 기간의 데이터만 보관하며, 그보다 오래된 데이터는 더 이상 필요하지 않습니다.

Machbase는 **Retention Policy** 기능으로 이러한 문제를 해결하는 자동 저장소 관리 메커니즘을 제공합니다. 정책을 선언적으로 정의하기만 하면 정해진 보관 기간이 지난 데이터가 자동으로 삭제되므로, 저장 공간 사용량을 예측 가능하게 유지하고 장기적인 데이터 수명 주기를 간단하게 관리할 수 있습니다.

## 핵심 개념: Retention Policy

Retention Policy는 지정한 테이블의 데이터를 시간 기준으로 자동 삭제하는 규칙입니다. 다음 두 가지 파라미터로 동작합니다.

- **DURATION**: 테이블에 데이터를 보관할 최대 기간입니다. 정책을 검사하는 시점의 시스템 시각에서 DURATION을 뺀 시점보다 오래된 데이터가 삭제 대상이 됩니다. 단위는 `MONTH`, `DAY`, `HOUR`, `MIN`, `SEC` 중 하나입니다.
- **INTERVAL**: `DURATION` 기준으로 삭제 대상 데이터를 검사하는 주기입니다. 지정한 간격마다 삭제 작업이 실행되며, 단위는 `DAY`, `HOUR`, `MIN`, `SEC` 중 하나입니다.

테이블에 정책을 적용하면 백그라운드 작업이 `INTERVAL`마다 테이블을 검사합니다. 이때 `BASETIME` 컬럼의 시각이 현재 시스템 시각에서 `DURATION`을 뺀 시점보다 오래된 행을 모두 자동으로 삭제합니다.

사용 흐름은 다음과 같습니다.

1. 정책 이름과 `DURATION`, `INTERVAL`을 지정해 정책을 생성합니다(`CREATE RETENTION`).
2. 생성한 정책을 하나 이상의 대상 테이블에 적용합니다(`ALTER TABLE ... ADD RETENTION`).
3. Machbase가 정책의 주기에 따라 자동으로 데이터를 삭제합니다.
4. 자동 삭제가 더 이상 필요 없는 테이블에서는 정책 적용을 해제합니다(`ALTER TABLE ... DROP RETENTION`).
5. 어떤 테이블에도 적용되지 않은 정책이 더 이상 필요 없으면 삭제합니다(`DROP RETENTION`).

## Retention Policy 생성

Retention Policy는 `CREATE RETENTION` 문을 사용해 별도의 데이터베이스 객체로 정의합니다.

**문법:**

```sql
CREATE RETENTION policy_name
    DURATION duration_value { MONTH | DAY | HOUR | MIN | SEC }
    INTERVAL interval_value { DAY | HOUR | MIN | SEC };
```

- `policy_name`: 사용자가 지정하는 고유한 정책 이름
- `duration_value`: 보관 기간(정수)
- `MONTH | DAY | HOUR | MIN | SEC`: `duration_value`의 시간 단위
- `interval_value`: 삭제 대상 검사 주기(정수)
- `DAY | HOUR | MIN | SEC`: `interval_value`의 시간 단위

**예시:**

```sql
-- Policy to retain data for 1 day, checking every 1 hour
CREATE RETENTION policy_1d_1h
    DURATION 1 DAY
    INTERVAL 1 HOUR;

-- Policy to retain data for 1 month (approximated), checking every 3 days
CREATE RETENTION policy_1m_3d
    DURATION 1 MONTH
    INTERVAL 3 DAY;
```

## 테이블에 정책 적용

생성한 정책은 `ALTER TABLE ... ADD RETENTION` 문으로 대상 테이블에 명시적으로 연결해야 합니다. 테이블에는 한 번에 하나의 Retention Policy만 적용할 수 있습니다.

**문법:**

```sql
ALTER TABLE table_name ADD RETENTION policy_name;
```

- `table_name`: 정책을 적용할 테이블 이름
- `policy_name`: 미리 생성한 Retention Policy 이름

**예시:**

```sql
-- Assume a TAG table 'sensor_data' and policy 'policy_1d_1h' exist
CREATE TAG TABLE sensor_data ( name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED );

-- Apply the policy_1d_1h to the sensor_data table
ALTER TABLE sensor_data ADD RETENTION policy_1d_1h;
```

## 정책 모니터링

정의한 정책과 적용 상태는 시스템 카탈로그 뷰에서 조회할 수 있습니다.

- **`M$RETENTION`**: 데이터베이스에 정의된 모든 정책의 이름과 설정한 `DURATION`, `INTERVAL` 값(내부적으로 초 단위로 저장)을 보여 줍니다.

    ```sql
    -- View all defined retention policies
    SELECT * FROM M$RETENTION;
    ```

- **`V$RETENTION_JOB`**: 각 테이블에 적용된 정책, 작업 상태(예: `WAITING`), 마지막 삭제 작업에서 사용한 기준 시각(`LAST_DELETED_TIME`)을 보여 줍니다.

    ```sql
    -- View retention policies currently applied to tables
    SELECT * FROM V$RETENTION_JOB;
    ```

## 정책 해제 및 삭제

테이블에서 정책을 해제하면 해당 테이블의 자동 삭제가 중단됩니다. 정책이 더 이상 필요 없고 다른 테이블에도 적용되어 있지 않으면 정책 객체를 삭제할 수 있습니다.

### 테이블에서 해제

`ALTER TABLE ... DROP RETENTION` 문으로 테이블과 정책의 연결을 해제합니다.

**문법:**

```sql
ALTER TABLE table_name DROP RETENTION;
```

- `table_name`: 현재 적용된 정책을 해제할 테이블 이름

### 정책 객체 삭제

`DROP RETENTION` 문으로 정책 정의 자체를 삭제합니다. 정책이 테이블에 적용 중이면 삭제할 수 없으므로, 먼저 해당 테이블에서 정책을 해제해야 합니다.

**문법:**

```sql
DROP RETENTION policy_name;
```

- `policy_name`: 삭제할 Retention Policy 이름

**의존 관계 예시:**

```sql
-- Assume 'policy_1d_1h' is applied to 'sensor_data'

-- Attempting to drop the policy while it's in use will fail
DROP RETENTION policy_1d_1h;
-- Expected Error: [ERR-02702: Policy (POLICY_1D_1H) is in use.]

-- First, detach the policy from the table
ALTER TABLE sensor_data DROP RETENTION;

-- Now, dropping the policy object will succeed
DROP RETENTION policy_1d_1h;
```

## 사용 예제

Retention Policy 기능을 사용하는 과정을 단계별로 설명합니다.

**1. 스키마 준비:**

```sql
-- Ensure a clean state (drop table and potentially dependent rollup tables)
DROP TABLE IF EXISTS ret_tag CASCADE;

-- Create a sample TAG table (with Rollup for context, though not required for Retention)
CREATE TAG TABLE ret_tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP(MIN) TAG_PARTITION_COUNT=1;
```

**2. Retention Policy 생성:**

```sql
-- Define a policy to keep data for 1 day, checking hourly
CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;

-- Verify policy creation
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'POLICY_1D_1H';
```

**3. 테이블에 정책 적용:**

```sql
-- Apply the created policy to the 'ret_tag' table
ALTER TABLE ret_tag ADD RETENTION policy_1d_1h;

-- Verify policy application
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'RET_TAG';
-- Expected: A row showing RET_TAG, POLICY_1D_1H, state (likely WAITING), and NULL last_deleted_time initially.
```

**4. 오래된 데이터를 포함한 데이터 적재:**

```tql
// Generate 150,000 records at 1-second intervals (about 41.7 hours up to now).
// Some of the records are older than 1 day.
FAKE(arrange(1, 150000, 1))
MAPVALUE(1, sin((2*PI*value(0)/100)))
MAPVALUE(0, timeAdd("now", strSprintf("-%.fs", 150000-value(0))))
PUSHVALUE(0, "sensor-a")
APPEND(table("ret_tag"))
```

**5. 초기 적재 건수 확인:**

```sql
-- Check the total number of records inserted
SELECT COUNT(*) FROM ret_tag;
-- Expected: 150000, if the retention job has not run yet
```

**6. 정책 실행 대기:**

정책의 `INTERVAL`(이 예제에서는 1시간)보다 오래 기다립니다. 백그라운드 작업이 자동으로 실행되어 1일보다 오래된 데이터가 삭제됩니다.

**7. 데이터 삭제 확인:**

```sql
-- Check the retention job status again; LAST_DELETED_TIME might be updated
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'RET_TAG';

-- Check the record count again. It should be lower than the initial count,
-- as records older than 1 day (relative to when the job ran) should have been deleted.
SELECT COUNT(*) FROM ret_tag;
-- Expected: A number less than 150000.
```

**8. 정책 해제 및 삭제:**

```sql
-- Stop automatic deletion for 'ret_tag'
ALTER TABLE ret_tag DROP RETENTION;

-- Verify detachment (the row for ret_tag should disappear)
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'RET_TAG';

-- Remove the policy definition itself
DROP RETENTION policy_1d_1h;

-- Verify removal
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'POLICY_1D_1H';
-- Expected: No rows returned.
```

자동 저장소 관리를 활용하면 일정 기간의 데이터만 유지하고 오래된 데이터는 자동으로 정리할 수 있어 운영 부담과 오류 가능성을 크게 줄일 수 있습니다.
