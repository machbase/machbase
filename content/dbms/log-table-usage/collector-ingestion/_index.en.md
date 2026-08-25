---
type: docs
title: '7.13 Collector Ingestion'
weight: 130
toc: true
---

This page owns LOG-table schema and record-mapping guidance for FILE and SFTP Collector sources.
Use the operations and reference chapters for lifecycle commands and exact configuration keys.

## Choose a path

| Requirement | Start with |
|---|---|
| Repeated local-file ingestion | FILE source |
| Repeated remote-file ingestion | SFTP source |
| Live application rows | SDK Append |
| An undocumented socket or ODBC source | An application or verified external tool |

Confirm the current source list in the
[Collector source-type reference](/dbms/reference/collector/dictionary-collector-source-type/).

## LOG schema and mapping

`_ARRIVAL_TIME` is automatic and must not be declared as a user column.

```sql
CREATE LOG TABLE collector_event (
    source_time DATETIME,
    host_name   VARCHAR(64),
    level       VARCHAR(16),
    message     VARCHAR(1024)
);
```

Validate encoding, line endings, delimiters, DATETIME format and timezone, NULL handling, and the
target column order with a small sample.

## Canonical documentation

| Subject | Canonical page |
|---|---|
| Input-path selection | [Data input and export](/dbms/development-tools-integration/data-input-load-export/) |
| Create, start, stop, and recovery | [Collector operations](/dbms/operations-configuration-recovery/collector/) |
| End-to-end file scenario | [Collector file ingestion](/dbms/scenario-guides/file-ingestion-collector/) |
| Template, regex, and source options | [Collector reference](/dbms/reference/collector/) |
