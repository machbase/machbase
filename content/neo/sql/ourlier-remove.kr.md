---
title: 자동 이상값 제거
type: docs
weight: 41
---

## 소개

산업·환경 센서에서 수집하는 시계열 데이터에는 노이즈, 순간 스파이크, 진동 간섭 등으로 예상 범위를 벗어나는 이상값이 자주 섞입니다. 이러한 이상값은 분석을 크게 방해하고, 저장 공간과 처리 시간을 불필요하게 늘립니다.

이상값을 수동으로 걸러 내거나 애플리케이션에서 필터링 로직을 직접 구현하면 복잡하고 계산 비용도 큽니다. Machbase는 TAG 테이블의 태그 메타데이터에 정의한 사양 한계(Specification Limit)를 이용해 데이터 적재 단계에서 이상값을 자동으로 제거하는 기능을 제공합니다. 센서별 허용 범위를 선언적으로 정의해 두면 그 범위 안에 있는 데이터만 저장됩니다.

## 핵심 개념: 사양 한계(LSL/USL)

자동 이상값 제거 기능은 태그 식별자(Tag ID)별로 허용되는 값의 범위를 정의해 동작합니다. 이 범위는 태그 메타데이터 테이블의 다음 두 속성으로 설정합니다.

- **LSL (Lower Specification Limit)**: 해당 Tag ID 측정값의 최소 허용값입니다.
- **USL (Upper Specification Limit)**: 해당 Tag ID 측정값의 최대 허용값입니다.

TAG 테이블에 새 행을 삽입할 때 Machbase는 해당 Tag ID의 메타데이터에 정의된 LSL, USL 값으로 다음과 같이 유효성을 검사합니다.

1. **메타데이터 조회**: 입력되는 행의 `name`(Tag ID)에 해당하는 LSL, USL 값을 종속 태그 메타데이터 테이블(`_TableName_meta`)에서 읽습니다.
2. **값 비교**: `SUMMARIZED` 속성이 선언된 `value` 컬럼의 입력값을 LSL, USL과 비교합니다.
3. **검증 규칙**: 입력값이 `LSL <= incoming_value <= USL` 조건을 충족할 때만 삽입이 허용됩니다.
   - LSL이 `NULL`이면 하한 검사를 생략합니다(`incoming_value <= USL`).
   - USL이 `NULL`이면 상한 검사를 생략합니다(`LSL <= incoming_value`).
   - LSL과 USL이 모두 `NULL`이면 검사 없이 값을 받아들입니다.
4. **처리 결과**: 검사를 통과하면 행이 TAG 테이블에 삽입됩니다. 값이 LSL/USL 범위를 벗어나면 해당 행의 삽입이 거부되고 오류가 반환됩니다. 예를 들어 값이 LSL보다 작으면 `ERR-02342`, USL보다 크면 `ERR-02341`이 반환됩니다.

이 방식을 사용하면 태그마다 미리 정의한 허용 범위에 따라 입력 데이터를 적재 시점에 바로 걸러 낼 수 있습니다.

## 설정 방법

사양 한계(LSL/USL)는 `CREATE TAG TABLE` 문의 `METADATA` 절에서 특수 키워드를 붙인 컬럼을 정의하거나, 나중에 `ALTER TABLE`로 이런 컬럼을 추가해 설정합니다.

### 테이블 생성 시 한계 정의

LSL과 USL 값을 저장할 컬럼은 `METADATA` 절에 정의하며, 각각 `LOWER LIMIT`, `UPPER LIMIT` 키워드를 붙입니다.

**구문:**

```sql
CREATE TAG TABLE table_name (
    name_column VARCHAR(...) PRIMARY KEY,
    time_column DATETIME BASETIME,
    value_column numeric_datatype SUMMARIZED, -- Crucial: SUMMARIZED is required
    ...
)
METADATA (
    lsl_column_name numeric_datatype LOWER LIMIT, -- Column for LSL
    usl_column_name numeric_datatype UPPER LIMIT, -- Column for USL
    ... -- Other metadata columns
);
```

- `value_column`: 숫자 타입이어야 하며 `SUMMARIZED` 키워드를 **반드시** 포함해야 합니다. 이상값 검사는 이 컬럼에 입력되는 값에만 적용됩니다.
- `lsl_column_name`, `usl_column_name`: 한계 값을 저장할 메타데이터 컬럼의 이름으로, 사용자가 정합니다.
- `numeric_datatype`: LSL/USL 컬럼의 데이터 타입은 `value_column`의 데이터 타입과 호환되어야 합니다.

**예시 (LSL과 USL 모두 정의):**

```sql
CREATE TAG TABLE sensor_readings (
    tag_id VARCHAR(50) PRIMARY KEY,
    ts DATETIME BASETIME,
    reading DOUBLE SUMMARIZED
)
METADATA (
    min_acceptable DOUBLE LOWER LIMIT,
    max_acceptable DOUBLE UPPER LIMIT,
    location VARCHAR(100) -- Regular metadata column
);
```

- `SUMMARIZED` 속성이 지정된 `reading` 컬럼에 대해 이상값 검사가 수행됩니다.
- `min_acceptable`, `max_acceptable`는 LSL, USL을 저장할 컬럼입니다.

**예시 (LSL만 정의):**

최소값이나 최대값 중 한쪽만 검사하면 되는 경우에는 한계를 하나만 정의해도 됩니다.

```sql
CREATE TAG TABLE pressure_monitor (
    tag_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    pressure_kpa INTEGER SUMMARIZED
)
METADATA (
    min_pressure INTEGER LOWER LIMIT -- Only validate against a minimum pressure
);
```

### 기존 테이블에 한계 추가

기존 TAG 테이블에 LSL/USL 컬럼을 추가하려면 종속 메타데이터 테이블(`_TableName_meta`)에 `ALTER TABLE`을 실행합니다. LSL/USL 컬럼은 같은 메타데이터 테이블에 `DROP COLUMN`을 실행해(또는 `ALTER TABLE table_name METADATA DROP COLUMN (column_name)`) 지울 수도 있으며, 지운 한계는 더 이상 검사하지 않습니다.

**구문:**

```sql
-- Adding an LSL column
ALTER TABLE _table_name_meta ADD COLUMN ( lsl_column_name numeric_datatype LOWER LIMIT );

-- Adding a USL column
ALTER TABLE _table_name_meta ADD COLUMN ( usl_column_name numeric_datatype UPPER LIMIT );
```

**예시:**

```sql
-- Assume 'sensor_readings' table exists without LSL/USL initially
ALTER TABLE _sensor_readings_meta ADD COLUMN ( min_acceptable DOUBLE LOWER LIMIT );
ALTER TABLE _sensor_readings_meta ADD COLUMN ( max_acceptable DOUBLE UPPER LIMIT );
```

`ALTER TABLE`로 추가한 컬럼은 기존의 모든 메타데이터 행에서 처음에는 `NULL` 값을 가집니다.

### 한계 값 설정

LSL/USL 컬럼을 정의한 뒤에는 종속 태그 메타데이터 테이블(`_TableName_meta`)에 행을 삽입하거나 수정해 Tag ID별 한계 값을 설정합니다.

```sql
-- Set limits when inserting a new tag's metadata
INSERT INTO sensor_readings metadata (tag_id, min_acceptable, max_acceptable, location)
VALUES ('TEMP_SENSOR_01', 10.0, 90.0, 'Boiler Room');

-- Update limits for an existing tag
UPDATE sensor_readings metadata
SET min_acceptable = 15.0, max_acceptable = 85.0
WHERE tag_id = 'TEMP_SENSOR_01';
```

## 동작 및 제약 사항

- **`SUMMARIZED` 필수**: 자동 이상값 제거 기능을 사용하려면 TAG 테이블 정의에서 대상 `value` 컬럼에 `SUMMARIZED` 키워드가 **반드시** 있어야 합니다. 검사는 이 컬럼에 입력되는 값에만 수행됩니다.
- **데이터 타입 호환성**: `LOWER LIMIT`, `UPPER LIMIT`으로 지정한 메타데이터 컬럼의 데이터 타입은 TAG 테이블의 `SUMMARIZED` 값 컬럼의 데이터 타입과 숫자로서 호환되어야 합니다.
- **LSL <= USL**: 한 Tag ID에 LSL과 USL이 모두 `NULL`이 아닌 값으로 정의되어 있으면 LSL 값은 USL 값보다 작거나 같아야 합니다(`LSL <= USL`).
- **검사 시점**: 검사는 TAG 테이블에 `INSERT`할 때만 수행됩니다. LSL/USL을 정의하거나 변경하기 전에 이미 저장된 데이터에는 소급 적용되지 않습니다.
- **메타데이터 변경**: 메타데이터 테이블의 LSL/USL 값을 변경하면 *이후*에 삽입되는 데이터의 검사 규칙이 바뀝니다. 새 한계를 벗어나게 된 기존 데이터를 다시 검사하거나 삭제하지는 **않습니다**.
- **NULL 처리**: 어떤 Tag ID의 LSL이 `NULL`이면 그 태그에 입력되는 데이터의 하한 검사를 생략합니다. 마찬가지로 USL이 `NULL`이면 상한 검사를 생략합니다. 둘 다 `NULL`이면 해당 Tag ID에는 이상값 검사를 하지 않습니다.
- **한쪽 한계만 정의**: LSL 컬럼만 정의하면 최소값 검사(`value >= LSL`)만, USL 컬럼만 정의하면 최대값 검사(`value <= USL`)만 수행합니다.
- **메타데이터 테이블 의존성**: 이 기능은 종속 태그 메타데이터 테이블(`_TableName_meta`)의 구조와 값에 전적으로 의존합니다.

## 예시

이 절에서는 자동 이상값 제거 기능을 설정하고 사용하는 실제 예시를 보여 줍니다.

**1. LSL/USL을 포함한 스키마 정의:**

```sql
-- Drop if exists from previous runs
DROP TABLE IF EXISTS out_tag CASCADE;

-- Create TAG table with metadata for LSL and USL
CREATE TAG TABLE out_tag (
    tag_id VARCHAR(50) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED -- Value column where filtering applies
)
METADATA (
    lsl DOUBLE LOWER LIMIT, -- Lower Specification Limit column
    usl DOUBLE UPPER LIMIT  -- Upper Specification Limit column
) TAG_PARTITION_COUNT=1;
```

**2. 메타데이터에 한계 값 설정:**

```sql
-- Set the operational range for TAG_01: 100.0 <= value <= 200.0
INSERT INTO out_tag metadata (tag_id, lsl, usl) VALUES ('TAG_01', 100.0, 200.0);

-- Verify metadata entry
SELECT * FROM _out_tag_meta WHERE tag_id = 'TAG_01';
/* Expected Output:
_ID | TAG_ID | LSL   | USL
--- | ------ | ----- | -----
1   | TAG_01 | 100.0 | 200.0
*/
```

**3. 데이터 삽입과 필터링 확인:**

```sql
-- Attempt to insert data points for TAG_01

-- Value below LSL (Rejected)
INSERT INTO out_tag VALUES ('TAG_01', NOW, 95.2);
-- Expected Error: [ERR-02342: SUMMARIZED value is less than LOWER LIMIT.]

-- Value equal to LSL (Accepted)
INSERT INTO out_tag VALUES ('TAG_01', NOW, 100.0);
-- Expected Output: 1 row(s) inserted.

-- Value within range (Accepted)
INSERT INTO out_tag VALUES ('TAG_01', NOW, 150.5);
-- Expected Output: 1 row(s) inserted.

-- Value equal to USL (Accepted)
INSERT INTO out_tag VALUES ('TAG_01', NOW, 200.0);
-- Expected Output: 1 row(s) inserted.

-- Value above USL (Rejected)
INSERT INTO out_tag VALUES ('TAG_01', NOW, 205.5);
-- Expected Error: [ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]

-- Verify accepted data
SELECT * FROM out_tag WHERE tag_id = 'TAG_01';
/* Expected Output: (Timestamps will vary)
TAG_ID | TIME                              | VALUE | LSL   | USL
------ | --------------------------------- | ----- | ----- | -----
TAG_01 | 2024-XX-XX XX:XX:XX XXX:XXX:XXX | 100.0 | 100.0 | 200.0
TAG_01 | 2024-XX-XX XX:XX:XX XXX:XXX:XXX | 150.5 | 100.0 | 200.0
TAG_01 | 2024-XX-XX XX:XX:XX XXX:XXX:XXX | 200.0 | 100.0 | 200.0
*/
```

오류 메시지를 보면 어느 한계를 위반했는지 확인할 수 있습니다.

**4. 메타데이터의 한계 값 변경:**

```sql
-- Change the limits for TAG_01 to 10.0 <= value <= 100.0
UPDATE out_tag metadata SET lsl = 10.0, usl = 100.0 WHERE tag_id = 'TAG_01';

-- Verify the change in metadata
SELECT * FROM _out_tag_meta WHERE tag_id = 'TAG_01';
/* Expected Output:
_ID | TAG_ID | LSL  | USL
--- | ------ | ---- | -----
1   | TAG_01 | 10.0 | 100.0
*/

-- Attempt new insertions based on updated limits

-- Value 150.5 (Accepted previously) is now above the new USL (Rejected)
INSERT INTO out_tag VALUES ('TAG_01', NOW, 150.5);
-- Expected Error: [ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]

-- Value 95.2 (Rejected previously) is now within the new range (Accepted)
INSERT INTO out_tag VALUES ('TAG_01', NOW, 95.2);
-- Expected Output: 1 row(s) inserted.

-- Note: The previously inserted values (100.0, 150.5, 200.0) remain in the 'out_tag' table.
-- The update to metadata limits does not affect existing data.
```

**5. NULL로 필터링 해제:**

```sql
-- Disable outlier filtering for TAG_01 by setting limits to NULL
UPDATE out_tag metadata SET lsl = NULL, usl = NULL WHERE tag_id = 'TAG_01';

-- Verify metadata
SELECT * FROM _out_tag_meta WHERE tag_id = 'TAG_01';
/* Expected Output:
_ID | TAG_ID | LSL  | USL
--- | ------ | ---- | ----
1   | TAG_01 | NULL | NULL
*/

-- Insert values previously rejected (These should now succeed)
INSERT INTO out_tag VALUES ('TAG_01', NOW, 9.0);   -- Below previous LSL
-- Expected Output: 1 row(s) inserted.
INSERT INTO out_tag VALUES ('TAG_01', NOW, 250.0); -- Above previous USL
-- Expected Output: 1 row(s) inserted.
```
