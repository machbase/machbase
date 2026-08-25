---
type: docs
title: '11.11.1 Fluentd Input Pipeline'
weight: 10
toc: true
aliases:
  - /dbms/log-table-usage/fluentd-pipeline/
---

Use a verified Machbase output plugin to buffer and deliver Fluentd records to a TAG or LOG table.
Validate plugin compatibility and options against the installed plugin version.

## Pipeline ownership

- This page owns the Fluentd-to-Machbase workflow and delivery checks.
- [LOG table usage](/dbms/log-table-usage/) owns LOG schema, search, and lifecycle behavior.
- [SDK feature support](../../sdk-support-scope/) owns Append capability comparisons.
- The installed plugin documentation owns version-specific Fluentd options.

## Deployment sequence

1. Define the source record, target table, column order, timestamp meaning, and encoding.
2. Verify the plugin with the deployed Ruby and Fluentd versions.
3. Test connectivity to the Machbase native port with a minimum-privilege account.
4. Configure buffer, flush, retry, overflow, and dead-letter behavior.
5. Send a small sample and verify row count, time range, and representative values.
6. Restart Fluentd and confirm duplicate and loss handling.

## LOG table example

`_ARRIVAL_TIME` is supplied automatically and must not be declared as a user column.

```sql
CREATE LOG TABLE fluentd_event (
    source_time DATETIME,
    host_name   VARCHAR(64),
    level       VARCHAR(16),
    message     VARCHAR(1024)
);
```

Map the record fields to this exact order or use the plugin's documented named mapping. Do not put
passwords in source-controlled Fluentd configuration.

## Verification

```sql
SELECT COUNT(*) AS row_count,
       MIN(source_time) AS min_source_time,
       MAX(source_time) AS max_source_time
  FROM fluentd_event;
```

Compare the Fluentd output count, retry and dead-letter records, and the table count before moving
the pipeline to production.
