---
type: docs
title: '6.3 Create and Delete ROLLUP'
weight: 30
toc: true
---

<a id="create-delete-rollup"></a>

## Creation Syntax

```text
CREATE ROLLUP [IF NOT EXISTS] name
  ON source_tag [(column_or_json_path)]
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)]
  [EXTENSION]
  [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] name
  FROM source_rollup
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)]
  [EXTENSION]
  [WHERE predicate];
```

Do not specify a separate extension name after EXTENSION. CREATE accepts SEC/MIN/HOUR, unlike
query-function units such as DAY/MONTH. The interval must be positive; the current validation
maximum is equivalent to 365 days. Source, hierarchy, and aggregation-mode requirements must also be
met.

| Target | Requirement |
|---|---|
| Ordinary numeric column | Specify a supported numeric type; SUMMARIZED is not required |
| JSON path | Specify the JSON column and a valid path |
| Entire JSON document | Requires a JSON SUMMARIZED column |
| WITH ROLLUP automatic creation | Requires the third column to be SUMMARIZED |
| METADATA, distance-axis, or non-TAG | Not a general ROLLUP target |

## Creation, Duplicate-Name Checks, and Queries

```sql
CREATE TAG TABLE ch6_create (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP IF NOT EXISTS ch6_create_ru ON ch6_create(value) INTERVAL 1 MIN;
CREATE ROLLUP IF NOT EXISTS ch6_create_ru ON ch6_create(value) INTERVAL 1 MIN;
INSERT INTO ch6_create VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_create VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_create VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_create VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_create);
ALTER ROLLUP ch6_create_ru FORCE;
SELECT DISTINCT ROLLUP_NAME, COLUMN_NAME, INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CREATE_RU';
SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_create WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

Recreating an existing name retains its definition. IF NOT EXISTS neither changes nor verifies the
definition, and does not bypass all invalid-SQL or source validation. Both interval columns are
60000 ms. The query averages are 15 at 00:00 and 30 at 00:01.

Creating the same name without IF NOT EXISTS causes an error. Check it separately from the
successful exercise.

```sql
CREATE ROLLUP ch6_create_ru ON ch6_create(value) INTERVAL 1 MIN;
```

## Automatic Creation with WITH ROLLUP

The following separate table automatically creates the default SEC→MIN→HOUR hierarchy.

```sql
CREATE TAG TABLE ch6_auto (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);
SELECT DISTINCT ROLLUP_NAME, ROOT_TABLE, INTERVAL_TIME, EXT_TYPE
  FROM V$ROLLUP WHERE ROOT_TABLE = 'CH6_AUTO'
 ORDER BY INTERVAL_TIME;
```

The query returns three rows with INTERVAL_TIME values 1000, 60000, and 3600000.

Automatic EXTENSION creation uses `WITH ROLLUP (SEC) EXTENSION`. Check actual generated names in
V$ROLLUP; do not assume name conflicts are resolved automatically.

The argument determines the hierarchy: `(SEC)` creates SEC, MIN, and HOUR; `(MIN)` creates MIN and
HOUR; `(HOUR)` creates only HOUR. Omitting the argument is equivalent to `(SEC)`. Only the first
stage reads the source TAG; each later stage reads the preceding ROLLUP. Only SEC/MIN/HOUR are
accepted. Query-function units such as DAY cause an error.

## Deleting and Changing Definitions

Remove upper-level dependents before a source referenced by another ROLLUP. A Custom target TAG
cannot be dropped before its job. To change a definition, account for readers and reaggregation
time, then switch to a new object or remove and recreate the existing definition.

```sql
DROP ROLLUP ch6_create_ru;
DROP TABLE ch6_create;
DROP TABLE ch6_auto CASCADE;
```

The final CASCADE also removes this exercise's automatic ROLLUPs. Do not use it as the default for
ordinary production cleanup. CASCADE on a Custom source can remove associated jobs, but does not
automatically delete user target TAG tables.

Conditional, extension, JSON, and Custom exercises are provided independently in their sections. For
full syntax, see the [SQL Reference](../../reference/sql/syntax/rollup-syntax/).
