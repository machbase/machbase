---
title: 태그 통계
type: docs
weight: 21
---

## 소개

Machbase TAG 테이블은 태그 ID별로 방대한 시계열 데이터를 저장합니다. 특정 태그의 최소·최대 값, 데이터 건수, 시간 범위를 빠르게 확인하려면 매번 원본 테이블을 전 범위 스캔해야 하므로 비용이 큽니다. 이러한 반복적인 통계 조회를 최적화하기 위해 Machbase는 태그별 통계를 미리 계산해 두는 시스템 뷰를 제공합니다.

## `v$tag_table_name_stat` 뷰

TAG 테이블을 생성하면 자동으로 `v$<테이블명>_stat` 뷰가 생성됩니다. Machbase 엔진이 태그 ID별 통계를 미리 계산해 저장하며 사용자는 이 뷰를 통해 빠르게 통계를 조회할 수 있습니다.

## 통계 수집 조건

1. **`TAG_STAT_ENABLE` 속성**: 기본값은 `1`(활성화)입니다. `CREATE TAG TABLE ... TAG_STAT_ENABLE = 0`으로 지정하면 통계가 수집되지 않습니다.
2. **`SUMMARIZED` 키워드**: 값 컬럼에 `SUMMARIZED`가 선언되어 있어야 최소·최대 값과 해당 시각이 기록됩니다. 선언하지 않으면 값 관련 컬럼은 `NULL`로 남고 건수, 시간 범위만 저장됩니다.

```sql
CREATE TAG TABLE device_metrics (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
TAG_STAT_ENABLE = 1;
```

## 제공되는 통계 컬럼

| 컬럼명            | 설명                               | `SUMMARIZED` 필요 |
|:------------------|:-----------------------------------|:------------------|
| `NAME`            | 태그 ID                            | -                 |
| `ROW_COUNT`       | 해당 태그의 데이터 건수             | -                 |
| `MIN_TIME`        | 가장 이른 시각                     | -                 |
| `MAX_TIME`        | 가장 늦은 시각                     | -                 |
| `MIN_VALUE`       | 최소 값                            | 필요              |
| `MIN_VALUE_TIME`  | 최소 값이 기록된 시각              | 필요              |
| `MAX_VALUE`       | 최대 값                            | 필요              |
| `MAX_VALUE_TIME`  | 최대 값이 기록된 시각              | 필요              |
| `RECENT_ROW_TIME` | 가장 최근에 입력된 데이터의 시각   | -                 |

## 통계 조회 예시

```sql
SELECT min_time, max_time
FROM v$tag_stat
WHERE name = 'use';

SELECT name, min_time, max_time
FROM v$tag_stat
WHERE name IN ('use', 'gen', 'temperature');

SELECT row_count, min_value, max_value
FROM v$tag_stat
WHERE name = 'use';

SELECT *
FROM v$tag_stat;
```

실제 데이터를 확인할 때는 통계 뷰에서 시각을 가져와 원본 테이블과 조합할 수 있습니다.

```sql
SELECT *
FROM tag
WHERE name = 'use'
  AND time = (SELECT recent_row_time FROM v$tag_stat WHERE name = 'use');

SELECT *
FROM tag
WHERE name = 'temperature'
  AND time = (SELECT min_value_time FROM v$tag_stat WHERE name = 'temperature');
```

## 제한 사항

- 제공되는 통계 항목은 고정되어 있습니다. 표준편차 등 추가 통계가 필요하면 직접 계산하거나 Rollup 기능 등을 사용해야 합니다.
- 원본 데이터 품질에 그대로 의존합니다. 이상값이 저장되면 통계에도 반영됩니다.
- `TAG_STAT_ENABLE`과 `SUMMARIZED` 설정이 올바르지 않으면 일부 통계가 비어 있을 수 있습니다.

## 사용 예시

### 1. 테이블 생성 및 데이터 적재

```sql
CREATE TAG TABLE tag (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

데이터는 CSV 등으로 적재할 수 있습니다. (예: `machbase-neo>> import --input homes.csv --timeformat s --table tag --method append TAG;`)

### 2. 통계 확인

```sql
DESC v$tag_stat;

SELECT name, row_count FROM v$tag_stat;

SELECT name, COUNT(*) FROM tag GROUP BY name;
```

### 3. 통계 기반 조회

```sql
SELECT name, min_time, max_time
FROM v$tag_stat
WHERE name IN ('use', 'gen');

SELECT *
FROM tag
WHERE name = 'use'
  AND time = (SELECT recent_row_time FROM v$tag_stat WHERE name = 'use');

SELECT *
FROM tag
WHERE name = 'temperature'
  AND time = (SELECT min_value_time FROM v$tag_stat WHERE name = 'temperature');
```

### 4. 설정 차이에 따른 통계 비교

```sql
CREATE TAG TABLE stat1 (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) TAG_STAT_ENABLE = 1;

CREATE TAG TABLE stat2 (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
) TAG_STAT_ENABLE = 1;

CREATE TAG TABLE stat3 (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) TAG_STAT_ENABLE = 0;
```

각 테이블에 동일한 데이터를 입력한 후 통계 뷰를 조회하면 설정에 따라 수집되는 항목이 달라짐을 확인할 수 있습니다.\n*** End Patch
