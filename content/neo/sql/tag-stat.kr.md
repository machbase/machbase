---
title: 태그 통계
type: docs
weight: 21
---

## 소개

Machbase TAG 테이블은 태그 ID별로 방대한 시계열 데이터를 저장하며, 이 데이터를 조회할 때는 특정 태그 ID의 통계를 확인하는 경우가 많습니다. `NAME`(태그 ID)과 `time` 조건으로 TAG 테이블을 직접 조회하는 것이 기본이지만, 특정 태그의 최소·최대 값, 데이터 건수, 시간 범위를 구하려면 매번 원본 테이블을 전 범위 스캔해야 하므로 계산 비용이 크고 응답도 늦어집니다.

이러한 반복적인 통계 조회를 최적화하기 위해 Machbase는 전용 시스템 뷰를 중심으로 통계를 자동 집계하는 기능을 제공합니다. 이 기능은 태그 ID별 주요 통계를 미리 계산해 유지하므로, 원본 TAG 테이블 데이터에서 직접 계산할 때보다 훨씬 빠르게 조회할 수 있습니다. Rollup 테이블과 비슷한 성능 이점이 있지만, 시간 구간이 아니라 태그 단위의 통계를 제공합니다.

## `v$tag_table_name_stat` 뷰

TAG 테이블을 생성하면 Machbase가 이에 대응하는 `v$tag_table_name_stat` 시스템 뷰를 자동으로 생성합니다. `tag_table_name`은 원본 TAG 테이블의 이름입니다. 이 뷰는 태그 ID별로 집계한 통계를 저장하며, 사용자는 이 뷰를 통해 통계를 빠르게 조회할 수 있습니다.

뷰의 내용은 Machbase 엔진이 내부에서 미리 계산해 저장하고 관리합니다. 따라서 사용자가 이러한 일반적인 통계를 얻기 위해 복잡한 집계 작업을 직접 구성하거나 관리할 필요가 없습니다.

## 통계 수집 조건

`v$tag_table_name_stat` 뷰에 통계가 저장되는지 여부는 TAG 테이블을 정의할 때 지정하는 다음 설정에 따라 달라집니다.

1. **`TAG_STAT_ENABLE` 속성**: 태그별 통계 수집 기능 전체의 활성화 여부를 제어하는 테이블 속성입니다. 기본값은 `1`(활성화)입니다. 테이블을 생성할 때 `CREATE TAG TABLE ... TAG_STAT_ENABLE=0`으로 지정하면 `v$tag_table_name_stat` 뷰에 통계가 저장되지 않으며, 태그별 통계도 유지되지 않습니다.
2. **`SUMMARIZED` 키워드**: 값 기반 통계(최소 값, 최대 값과 각각이 기록된 시각)를 수집하려면 TAG 테이블 스키마의 값 컬럼(일반적으로 센서 측정값이나 지표를 저장하는 세 번째 컬럼)을 **반드시** `SUMMARIZED` 키워드로 선언해야 합니다. 값 컬럼에 `SUMMARIZED`를 선언하지 않으면 값과 무관한 통계(건수, 시간 범위, 최근 입력 시각)만 수집되어 뷰에 저장되고, 값 관련 컬럼은 `NULL`로 남습니다.

**구문 예시(전체 통계 활성화):**

```sql
CREATE TAG TABLE device_metrics (
    name VARCHAR(80) PRIMARY KEY, -- Tag ID column
    time DATETIME BASETIME,        -- Timestamp column
    value DOUBLE SUMMARIZED        -- Value column with SUMMARIZED
)
TAG_STAT_ENABLE=1; -- Property (default, can be omitted)
```

## 제공되는 통계 컬럼

`v$tag_table_name_stat` 뷰는 원본 TAG 테이블에 있는 태그 ID마다 미리 계산된 다음 통계 컬럼을 제공합니다.

| 컬럼명            | 데이터 타입        | 설명                                               | `SUMMARIZED` 필요 |
|:------------------|:-------------------|:---------------------------------------------------|:------------------|
| `NAME`            | VARCHAR            | 고유한 태그 식별자(태그 ID)                        | 아니요            |
| `ROW_COUNT`       | ULONG              | 해당 태그 ID로 기록된 데이터(행)의 전체 건수        | 아니요            |
| `MIN_TIME`        | DATETIME           | 해당 태그 ID의 전체 데이터 중 가장 이른 시각        | 아니요            |
| `MAX_TIME`        | DATETIME           | 해당 태그 ID의 전체 데이터 중 가장 늦은 시각        | 아니요            |
| `MIN_VALUE`       | DOUBLE             | 해당 태그 ID의 `SUMMARIZED` 컬럼에 기록된 최소 값   | **예**            |
| `MIN_VALUE_TIME`  | DATETIME           | `MIN_VALUE`가 처음 기록된 데이터의 시각             | **예**            |
| `MAX_VALUE`       | DOUBLE             | 해당 태그 ID의 `SUMMARIZED` 컬럼에 기록된 최대 값   | **예**            |
| `MAX_VALUE_TIME`  | DATETIME           | `MAX_VALUE`가 처음 기록된 데이터의 시각             | **예**            |
| `RECENT_ROW_TIME` | DATETIME           | 해당 태그 ID에 가장 최근에 입력된 데이터의 시각     | 아니요            |

*참고: 원본 TAG 테이블의 `SUMMARIZED` 컬럼이 정수형이어도 `MIN_VALUE`와 `MAX_VALUE`는 DOUBLE입니다.*

## 통계 조회

`v$tag_table_name_stat` 뷰를 사용하면 방대한 원본 TAG 테이블 데이터를 스캔하지 않고도 주요 통계를 빠르게 조회할 수 있습니다. 실제 데이터를 확인할 때는 통계 뷰에서 시각을 가져와 원본 테이블 조회와 조합할 수 있습니다.

**기본 조회 패턴:**

```sql
-- Retrieve min/max time boundaries for a specific tag
SELECT min_time, max_time
FROM v$your_tag_table_stat -- Replace 'your_tag_table' with the actual table name
WHERE name = 'specific_tag_id';

-- Retrieve min/max time boundaries for multiple tags
SELECT name, min_time, max_time
FROM v$your_tag_table_stat
WHERE name IN ('tag_id_1', 'tag_id_2', 'tag_id_3');

-- Retrieve row count and min/max values for a specific tag (requires SUMMARIZED)
SELECT row_count, min_value, max_value
FROM v$your_tag_table_stat
WHERE name = 'specific_tag_id';

-- Retrieve all statistics for all tags
SELECT *
FROM v$your_tag_table_stat;

-- Retrieve the actual data record corresponding to the most recent entry for a tag
SELECT *
FROM your_tag_table
WHERE name = 'specific_tag_id'
  AND time = (SELECT recent_row_time
              FROM v$your_tag_table_stat
              WHERE name = 'specific_tag_id');

-- Retrieve the actual data record corresponding to the minimum value occurrence for a tag
SELECT *
FROM your_tag_table
WHERE name = 'specific_tag_id'
  AND time = (SELECT min_value_time
              FROM v$your_tag_table_stat
              WHERE name = 'specific_tag_id');
```

## 제한 사항

태그별 통계 기능은 성능 면에서 이점이 크지만 다음과 같은 제한이 있습니다.

- **고정된 통계 항목**: 태그 ID 외에 미리 정해진 8가지 통계만 제공합니다. 표준편차, 백분위수처럼 다르거나 더 복잡한 통계가 필요하면 원본 TAG 테이블에서 직접 계산하거나 Rollup 테이블 등 다른 기능을 사용해야 합니다.
- **원본 데이터 품질에 의존**: `v$tag_table_name_stat` 뷰에 저장되는 통계의 정확도는 원본 TAG 테이블에 입력된 데이터의 품질에 그대로 의존합니다. 이상값이나 노이즈가 저장되면 `MIN_VALUE`, `MAX_VALUE` 등의 집계 값에도 반영되므로 입력 데이터를 검증하고 정제하는 것이 좋습니다.
- **설정 요구 사항**: 앞에서 설명한 것처럼 모든 통계를 수집하려면 `TAG_STAT_ENABLE=1` 속성과 대상 값 컬럼의 `SUMMARIZED` 키워드가 필요합니다. 설정이 올바르지 않으면 뷰의 통계 일부가 비어 있거나 통계가 전혀 저장되지 않습니다.
- **반영 시점**: 통계는 입력 즉시가 아니라 잠시 뒤에 뷰에 반영됩니다. 입력 직후에 조회하면 방금 넣은 데이터가 아직 통계에 없을 수 있습니다.

## 사용 예시

태그별 통계 기능을 설정하고 사용하는 예시를 소개합니다.

### 사전 준비: 스키마 생성 및 데이터 적재

다음 예시는 `tag`라는 TAG 테이블을 생성하고 데이터를 적재했다고 가정합니다.

**1. 스키마 정의(통계 활성화 확인):**

```sql
-- Drop existing table if necessary
-- DROP TABLE tag;

-- Create the TAG table, enabling statistics and marking 'value' for summary
CREATE TAG TABLE tag (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED -- Ensure SUMMARIZED is present for value stats
)
tag_partition_count=1, -- Example property
TAG_STAT_ENABLE=1;    -- Explicitly set (though default=1)
```

**2. 데이터 적재(`machbase-neo` import 사용 예시):**

`tag_name,unix_timestamp,value` 형식의 데이터가 담긴 CSV 파일 `homes.csv`가 있다고 가정합니다. `machbase-neo shell`은 현재 디렉토리를 `/work`에 마운트하므로 `homes.csv`가 있는 디렉토리에서 명령을 실행합니다.

```bash
# Example import command (adjust path and options as needed)
machbase-neo shell import --input /work/homes.csv --timeformat s TAG
```

### 통계 확인 및 기본 조회

**1. 통계 뷰 구조 확인:**

```sql
-- Display the columns and types of the auto-generated statistics view
DESC v$tag_stat;
```

**2. 태그별 건수 확인:**

```sql
-- Efficiently get row counts using the statistics view
SELECT name, row_count
FROM v$tag_stat
ORDER BY name;

-- Compare with direct count on the base table (will be slower for large tables)
SELECT name, COUNT(*) AS direct_count
FROM tag
GROUP BY name
ORDER BY name;
```

**3. 시간 범위 조회:**

```sql
-- Get the earliest and latest timestamps for specific tags
SELECT name, min_time, max_time
FROM v$tag_stat
WHERE name IN ('use', 'gen', 'temperature');
```

**4. 통계가 가리키는 시점의 실제 데이터 조회:**

```sql
-- Get the full data record for the most recently added 'use' tag data
SELECT *
FROM tag
WHERE name = 'use'
  AND time = (SELECT recent_row_time FROM v$tag_stat WHERE name = 'use');

-- Get the full data record when the minimum 'temperature' was recorded
SELECT *
FROM tag
WHERE name = 'temperature'
  AND time = (SELECT min_value_time FROM v$tag_stat WHERE name = 'temperature');

-- Get the recorded value at the maximum time for the 'gen' tag
SELECT value
FROM tag
WHERE name = 'gen'
  AND time = (SELECT max_time FROM v$tag_stat WHERE name = 'gen');
```

### 설정 차이에 따른 통계 비교(제한 사항)

다음 예시는 설정에 따라 통계 수집 결과가 어떻게 달라지는지 보여 줍니다.

**시나리오 준비:** 설정이 서로 다른 세 테이블을 만들고 *동일한* 샘플 데이터를 입력합니다.

```sql
-- Table 1: Full Statistics Enabled (Standard Case)
DROP TABLE IF EXISTS stat1;
CREATE TAG TABLE stat1 (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_STAT_ENABLE=1;

-- Table 2: SUMMARIZED Keyword Omitted
DROP TABLE IF EXISTS stat2;
CREATE TAG TABLE stat2 (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE) TAG_STAT_ENABLE=1; -- No SUMMARIZED

-- Table 3: Statistics Disabled via Property
DROP TABLE IF EXISTS stat3;
CREATE TAG TABLE stat3 (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_STAT_ENABLE=0; -- Stats explicitly disabled

-- Insert Identical Sample Data into all three tables
INSERT INTO stat1 VALUES('tag-0', TO_DATE('2022-08-11'), 10);
INSERT INTO stat1 VALUES('tag-0', TO_DATE('2022-08-13'), 20);
INSERT INTO stat1 VALUES('tag-0', TO_DATE('2022-08-14'), 5);
INSERT INTO stat1 VALUES('tag-1', TO_DATE('2023-08-12'), 200);
INSERT INTO stat1 VALUES('tag-1', TO_DATE('2023-08-13'), 50);
INSERT INTO stat1 VALUES('tag-1', TO_DATE('2023-08-15'), 120);

INSERT INTO stat2 VALUES('tag-0', TO_DATE('2022-08-11'), 10);
INSERT INTO stat2 VALUES('tag-0', TO_DATE('2022-08-13'), 20);
INSERT INTO stat2 VALUES('tag-0', TO_DATE('2022-08-14'), 5);
INSERT INTO stat2 VALUES('tag-1', TO_DATE('2023-08-12'), 200);
INSERT INTO stat2 VALUES('tag-1', TO_DATE('2023-08-13'), 50);
INSERT INTO stat2 VALUES('tag-1', TO_DATE('2023-08-15'), 120);

INSERT INTO stat3 VALUES('tag-0', TO_DATE('2022-08-11'), 10);
INSERT INTO stat3 VALUES('tag-0', TO_DATE('2022-08-13'), 20);
INSERT INTO stat3 VALUES('tag-0', TO_DATE('2022-08-14'), 5);
INSERT INTO stat3 VALUES('tag-1', TO_DATE('2023-08-12'), 200);
INSERT INTO stat3 VALUES('tag-1', TO_DATE('2023-08-13'), 50);
INSERT INTO stat3 VALUES('tag-1', TO_DATE('2023-08-15'), 120);

```

**결과 확인:**

각 테이블에 동일한 데이터를 입력한 후 통계 뷰를 조회하면 설정에 따라 수집되는 항목이 달라지는 것을 확인할 수 있습니다.

```sql
-- Query Statistics for Table 1 (Full Stats)
SELECT * FROM v$stat1_stat;
-- Expected: All columns populated, including MIN/MAX_VALUE and their times.

-- Query Statistics for Table 2 (No SUMMARIZED)
SELECT * FROM v$stat2_stat;
-- Expected: MIN_VALUE, MIN_VALUE_TIME, MAX_VALUE, MAX_VALUE_TIME columns will be NULL.
--          ROW_COUNT, MIN_TIME, MAX_TIME, RECENT_ROW_TIME will be populated.

-- Query Statistics for Table 3 (TAG_STAT_ENABLE=0)
SELECT * FROM v$stat3_stat;
-- Expected: No rows returned (the view exists but holds no statistics).
--          Statistics collection is entirely disabled for this table.
```

태그별 통계 기능을 온전히 활용하려면 테이블 정의(특히 `SUMMARIZED` 키워드)와 `TAG_STAT_ENABLE` 속성을 올바르게 지정해야 합니다.
