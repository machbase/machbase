---
type: docs
title: '6.12 ROLLUP Scenarios'
weight: 120
toc: true
---

<a id="storage-sensor-data-rollup"></a>

## Source Data and Interval Statistics by Sensor

Do not combine averages for sensors with different units, even if they measure at the same time.
This standalone exercise manages current units as metadata and queries aggregates by tag.

### 1. Create and Insert

```sql
CREATE TAG TABLE ch6_scenario (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
) METADATA (unit VARCHAR(16));
INSERT INTO ch6_scenario METADATA VALUES ('TEMP_01', 'celsius');
INSERT INTO ch6_scenario METADATA VALUES ('PRESS_01', 'bar');
INSERT INTO ch6_scenario VALUES ('TEMP_01', TO_DATE('2026-01-01 10:00:00'), 20);
INSERT INTO ch6_scenario VALUES ('TEMP_01', TO_DATE('2026-01-01 10:00:30'), 22);
INSERT INTO ch6_scenario VALUES ('PRESS_01', TO_DATE('2026-01-01 10:00:00'), 1.02);
CREATE ROLLUP ch6_scenario_ru ON ch6_scenario(value) INTERVAL 1 MIN;
EXEC TABLE_FLUSH(ch6_scenario);
ALTER ROLLUP ch6_scenario_ru FORCE;
```

A ROLLUP created after source ingestion still initially aggregates remaining data. Creation
completion alone does not mean initial aggregation is finished.

### 2. Check Results

```sql
SELECT name, unit FROM ch6_scenario METADATA ORDER BY name;
SELECT name, DATE_TRUNC('minute', time) AS bucket, COUNT(value), AVG(value)
  FROM ch6_scenario GROUP BY name, bucket ORDER BY name, bucket;
SELECT name, rollup('min', 1, time) AS bucket, COUNT(value), AVG(value)
  FROM ch6_scenario GROUP BY name, bucket ORDER BY name, bucket;
SHOW ROLLUPGAP;
```

TEMP_01 has 2 samples averaging 21°C; PRESS_01 has 1 sample averaging 1.02 bar. Metadata queries
return current units and do not automatically preserve historical unit changes.

### 3. Inspect Individual Observations

The data uses fixed timestamps, so query the same fixed range. Applying a current-time “last 5
minutes” predicate can return no rows depending on the execution date.

```sql
SELECT name, time, value FROM ch6_scenario
 WHERE name = 'TEMP_01'
   AND time >= TO_DATE('2026-01-01 10:00:00')
   AND time < TO_DATE('2026-01-01 10:01:00')
 ORDER BY time;
```

The two source values are 20 and 22. Their individual values or occurrence order cannot be
reconstructed from the aggregate average 21.

### 4. Clean Up

```sql
DROP ROLLUP ch6_scenario_ru;
DROP TABLE ch6_scenario;
```

<a id="use-cases-rollup"></a>

## Applying ROLLUP to Workloads

| Requirement | Design to check |
|---|---|
| Valid-quality statistics | Fix filters and candidate hints; compare with source data |
| OHLC | Extension FIRST/LAST or Custom reaggregation with auxiliary timestamps |
| Multiple-sensor comparison | Tag-specific units and matching buckets/query ranges |
| Consumption from cumulative meters | Boundary differences and reset/replacement/missing-data rules; distinguish from sample averages |
| Availability | Distinguish sample ratios from time ratios; define missing-interval policy |
| Combining recent source data with long-term aggregates | Separate nonoverlapping ranges at a verified aggregation-completion point |

When combining source and ROLLUP results with UNION ALL, check boundary duplicates, omissions, and
differing sample counts. Do not assume a fixed lag such as the latest two minutes always being
unaggregated. Pass sums and valid counts when recombining partial results into averages.

Complete feature exercises are available for [Conditional](../conditional-rollup/),
[Extension](../extension-rollup/), [JSON](../json-summarized-rollup/), and
[Custom](../custom-rollup/) ROLLUP. If problems arise, first check state and semantics using the
[Diagnostic Sequence](../../troubleshooting/rollup/).
