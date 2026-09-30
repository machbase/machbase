---
title: 중복 데이터 제거
type: docs
weight: 31
---

## 소개

분산 환경에서 센서 데이터를 수집·전송할 때 일시적인 네트워크 장애나 장비 설정 때문에 동일한 데이터가 재전송되는 일이 잦습니다. 데이터 손실을 막기 위한 재전송이지만 결과적으로 데이터베이스에는 중복 레코드가 쌓이게 됩니다. 애플리케이션 측에서 중복을 식별·제거하려면 복잡한 로직이 필요하고, 데이터 양이 많으면 성능 저하가 큰 문제가 됩니다.

Machbase는 데이터베이스 수준에서 중복 전송을 자동으로 제거하는 기능을 제공합니다. 설정한 시간 창을 기준으로 중복 입력을 자동으로 감지해 걸러내므로, 애플리케이션에 복잡한 로직을 두지 않고도 데이터 일관성을 유지할 수 있습니다. 이 기능은 TAG 테이블에서만 동작합니다.

## 핵심 개념

중복 제거 기능은 TAG 테이블 생성 시 설정한 조회 기간을 기준으로 동작합니다. 조회 기간은 데이터를 삽입하는 시점의 시스템 시각에서 과거 방향으로 잡는 시간 창입니다. TAG 테이블에 새 행이 삽입될 때 Machbase는 다음을 확인합니다.

1. **식별**: 입력 행의 `PRIMARY KEY` 컬럼 값(보통 Tag ID 또는 `name`)과 `BASETIME` 컬럼 값(타임스탬프)을 테이블의 기존 행과 비교합니다.
2. **탐색**: `PRIMARY KEY`와 `BASETIME` 값이 입력 행과 정확히 같은 행이 이미 존재하는지 확인합니다.
3. **시간 조건**: 같은 행이 존재하고 그 `BASETIME`이 설정한 조회 기간(현재 삽입 시점의 **시스템 시각** 기준 과거 방향) 안에 포함되면 입력 행을 중복으로 판단합니다.
4. **처리**: 중복으로 판정된 입력 행은 자동으로 폐기되어 TAG 테이블에 저장되지 않습니다.

즉, 지정한 시간 창 안에서는 먼저 기록된 데이터를 유지하는 first-write-wins 방식으로 동작합니다. Tag ID와 타임스탬프 조합으로 식별되는 데이터는 처음 입력된 것만 저장됩니다. 원본 레코드의 타임스탬프가 현재 시스템 시각 기준 조회 기간 안에 있는 동안에는 같은 Tag ID와 타임스탬프로 들어오는 이후 입력이 모두 별도 알림 없이 무시됩니다. 비교 대상은 `PRIMARY KEY`와 `BASETIME` 컬럼뿐이므로, 센서 값 같은 다른 컬럼 값이 달라도 키와 시간이 같으면 중복으로 처리됩니다.

## 설정 방법

TAG 테이블 생성 시 다음 테이블 속성을 지정합니다.

*   **`TAG_DUPLICATE_CHECK_DURATION`**: 중복 검사에 사용할 조회 기간을 분 단위로 지정합니다.

**구문:**

```sql
CREATE TAG TABLE table_name (
    name_column datatype PRIMARY KEY,
    time_column DATETIME BASETIME,
    value_column datatype [SUMMARIZED]
    [, additional_columns...]
)
TAG_DUPLICATE_CHECK_DURATION = duration_in_minutes;
```

*   `duration_in_minutes`: 조회 기간을 분 단위로 지정하는 정수입니다.
    *   최솟값: `1`(분)
    *   최댓값: `43200`(분, 30일)
    *   기본값: `0`(비활성화)

**설정 확인:**

시스템 카탈로그 뷰를 조회해 TAG 테이블에 설정된 기간을 확인할 수 있습니다.

1.  **테이블 ID 조회:** 테이블명은 대문자로 입력합니다.

    ```sql
    SELECT id
    FROM m$sys_tables
    WHERE name = 'YOUR_TABLE_NAME'; -- Note: Table name must be in uppercase
    ```

2.  **속성값 조회:** `{table_id_from_step_1}` 자리에 1단계에서 조회한 ID를 넣습니다.

    ```sql
    SELECT value
    FROM m$sys_table_property
    WHERE id = {table_id_from_step_1}
      AND name = 'TAG_DUPLICATE_CHECK_DURATION';
    ```

**설정 변경:**

`TAG_DUPLICATE_CHECK_DURATION` 설정은 다음과 같이 변경할 수 있습니다.

```sql
ALTER TABLE {table_name} set TAG_DUPLICATE_CHECK_DURATION={duration in minutes};
```

## 동작 및 제약 사항

이 기능을 효과적으로 사용하려면 다음 동작과 제약 사항을 이해해야 합니다.

*   **단위와 범위**: 분 단위로만 지정할 수 있으며 최대 43200분(30일)까지 가능합니다.
*   **데이터 삭제와의 관계**: 중복 검사는 조회 기간 안에 원본 데이터가 존재한다는 전제로 동작합니다. 동일한 데이터가 도착하기 *전에* 원본 레코드(최초 입력)를 TAG 테이블에서 삭제하면, 새로 도착한 레코드는 중복으로 판단되지 **않습니다**. 비교할 대상이 더 이상 데이터베이스에 없으므로 새로운 최초 입력으로 저장됩니다.
*   **동작 방식**: 같은 (Primary Key, Basetime) 조합에 대해 설정한 기간 안에서 *가장 먼저* 들어온 레코드를 유지하고, 이후 들어온 동일 입력은 폐기합니다. 마지막 입력을 유지하는 last-write-wins 방식이 필요한 경우에는 적합하지 않습니다.
*   **일관성 모델**: 대량 실시간 적재 환경에서는 데이터 삽입 후 중복 검사가 모든 내부 구조의 최신 상태를 반영하기까지 약간의 지연이 발생할 수 있습니다. 이는 분산 데이터 시스템에서 흔히 볼 수 있는 최종 일관성(eventual consistency) 동작입니다.
*   **타깃 기반 중복 제거**: Machbase 데이터베이스 내부에서 중복을 걸러내는 타깃 기반 방식이며, 소스 시스템에서 중복 데이터가 전송되는 것을 막지는 않습니다.
*   **리소스 사용**: 애플리케이션이 전송 전에 중복을 걸러내는 소스 기반 방식과 비교하면, 타깃 기반 중복 제거는 적재 과정에서 검사를 수행하므로 데이터베이스의 CPU와 I/O를 추가로 사용합니다.

## 예시

중복 제거를 활성화한 TAG 테이블을 생성하고 동작을 확인하는 예시입니다.

**1. 테이블 생성:**

```sql
-- Drop the table if it exists from previous runs
DROP TABLE IF EXISTS dup_tag;

-- Create a TAG table named 'dup_tag'
-- Configure it to check for duplicates within a 1440 minutes (1-day) window
CREATE TAG TABLE dup_tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED -- Value column (summarized is optional for dedupe itself)
)
TAG_DUPLICATE_CHECK_DURATION=1440; -- Enable deduplication with a 1440 minutes (1-day) lookback
```

**2. 데이터 삽입 테스트:**

다음 INSERT 문으로 중복이 어떻게 처리되는지 확인합니다. 각 INSERT 문은 순서대로 실행하며, `2024-01-02` 데이터끼리, `2024-01-04` 데이터끼리 비교할 때 해당 타임스탬프가 1일 조회 기간 안에 들도록 각 삽입 시점의 시스템 시각이 진행된다고 가정합니다. 과거의 고정된 타임스탬프를 현재 시각에 그대로 실행하면 이 전제가 성립하지 않습니다.

```sql
-- Insert initial records
INSERT INTO dup_tag VALUES('tag1', '2024-01-01 09:00:00 000:000:001', 0); -- Kept (First instance)
INSERT INTO dup_tag VALUES('tag1', '2024-01-02 09:00:00 000:000:001', 0); -- Kept (Different day/time from first)
INSERT INTO dup_tag VALUES('tag1', '2024-01-02 09:00:00 000:000:002', 0); -- Kept (First instance for this specific time)

-- Attempt to insert a duplicate (same name, same time as previous row)
-- This row has a different 'value' (1 vs 0), but will still be treated as a duplicate
-- because the (name, time) pair matches an existing record within the duration.
INSERT INTO dup_tag VALUES('tag1', '2024-01-02 09:00:00 000:000:002', 1); -- Discarded (Duplicate based on name & time)

-- Insert record for a subsequent day
INSERT INTO dup_tag VALUES('tag1', '2024-01-03 09:00:00 000:000:003', 0); -- Kept (New timestamp)

-- Insert records for a different tag ('tag2'), demonstrating multiple duplicates at the same timestamp
INSERT INTO dup_tag VALUES('tag2', '2024-01-04 09:00:00 000:000:001', 0); -- Kept (First instance for tag2 at this time)
INSERT INTO dup_tag VALUES('tag2', '2024-01-04 09:00:00 000:000:001', 1); -- Discarded (Duplicate based on name & time)
INSERT INTO dup_tag VALUES('tag2', '2024-01-04 09:00:00 000:000:001', 2); -- Discarded (Duplicate based on name & time)

-- Insert records for 'tag2' at different timestamps
INSERT INTO dup_tag VALUES('tag2', '2024-01-04 09:00:00 000:000:002', 1); -- Kept (First instance for this specific time)
INSERT INTO dup_tag VALUES('tag2', '2024-01-04 09:00:00 000:000:003', 2); -- Kept (First instance for this specific time)
```

**3. 결과 확인:**

테이블을 조회하면 각 `name`과 `time` 조합별로 유효한 기간 안에서 최초 입력된 레코드만 남아 있는 것을 확인할 수 있습니다. 이후 동일 조합으로 들어온 데이터는 폐기되었습니다.

```sql
-- Query data for 'tag1'
SELECT * FROM dup_tag WHERE name = 'tag1';

/* Expected Output for tag1:
ROWNUM | NAME | TIME                              | VALUE
------ | ---- | --------------------------------- | -----
1      | tag1 | 2024-01-01 09:00:00 000:000:001 | 0.0
2      | tag1 | 2024-01-02 09:00:00 000:000:001 | 0.0
3      | tag1 | 2024-01-02 09:00:00 000:000:002 | 0.0  -- Note: The row with value 1 was discarded
4      | tag1 | 2024-01-03 09:00:00 000:000:003 | 0.0
*/

-- Query data for 'tag2'
SELECT * FROM dup_tag WHERE name = 'tag2';

/* Expected Output for tag2:
ROWNUM | NAME | TIME                              | VALUE
------ | ---- | --------------------------------- | -----
1      | tag2 | 2024-01-04 09:00:00 000:000:001 | 0.0  -- Note: Rows with values 1 and 2 at this time were discarded
2      | tag2 | 2024-01-04 09:00:00 000:000:002 | 1.0
3      | tag2 | 2024-01-04 09:00:00 000:000:003 | 2.0
*/
```
