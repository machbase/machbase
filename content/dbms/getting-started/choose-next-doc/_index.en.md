---
type: docs
title: 'Choose the Next Document'
weight: 40
toc: true
---

After finishing the quick start, you are at the first fork in the road. Users storing
industrial IoT sensor values, users ingesting financial tick data, users analyzing
logs, and users connecting applications all need different next documents. The
Machbase DBMS manual is easiest to read by design question, not by feature name.

Before choosing the next document, ask four questions: how frequently data arrives,
how often it is queried by time range, how long raw data must be retained, and whether
rollup or aggregation is needed. These answers usually reveal which table type and
feature area to study first.

## Next Paths

| What you need to do | Next document |
| --- | --- |
| Store industrial IoT sensor, equipment, or measurement values | [TAG table design](/dbms/data-modeling-table-design/table-types-design-type/design-tag/) |
| Store logs, events, or financial tick receive histories | [LOG table design](/dbms/data-modeling-table-design/table-types-design-type/design-log/) |
| Manage equipment names, codes, or mapping data | [LOOKUP design](/dbms/data-modeling-table-design/table-types-design-type/design-lookup/), [RDB design](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/), [LOOKUP vs RDB](/dbms/data-modeling-table-design/table-types-selection-type/comparison-rdb-vs-lookup/) |
| Check SQL syntax | [SQL reference](/dbms/reference/sql/), [SQL ingestion](/dbms/data-input-load-export/sql/) |
| Connect applications | [Application integration](/dbms/application-integration/), [Driver guide](/dbms/application-integration/guide-drivers/) |
| Change operational settings | [Operations, configuration, and recovery](/dbms/operations-configuration-recovery/) |

## TAG Table Preview Sample

For a TAG table, run `TABLE_FLUSH` when you want to query newly inserted data
immediately. Checking this behavior early prevents confusion when reading the TAG
chapters.

```sql
CREATE TAG TABLE DBMS_GS_TAG (
  NAME VARCHAR(128) PRIMARY KEY,
  TIME DATETIME BASETIME,
  VALUE DOUBLE
);

INSERT INTO DBMS_GS_TAG
VALUES ('sensor01', TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 21.5);

EXEC TABLE_FLUSH(DBMS_GS_TAG);

SELECT NAME, TIME, VALUE
FROM DBMS_GS_TAG
WHERE NAME = 'sensor01';

DROP TABLE DBMS_GS_TAG;
```

Assuming the SQL above is saved as `/tmp/dbms_gs_tag_preview.sql`, run the following command.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_tag_preview.sql
```

If `sensor01` is printed, basic TAG table insert and query worked.
If a rerun fails because `DBMS_GS_TAG` already exists, run
`DROP TABLE DBMS_GS_TAG;` and start again.
