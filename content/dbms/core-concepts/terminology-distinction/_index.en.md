---
type: docs
title: '2.5 Operational Concept Distinctions'
weight: 50
toc: true
aliases:
  - /dbms/reference/ai-agent-reference/terminology-disambiguation/
---

This page distinguishes operations that have similar names but different outcomes. Exact syntax and
procedures belong to their feature chapters.

<a id="retention-vs-delete-truncate"></a>

## Retention versus DELETE and TRUNCATE

Retention is a recurring age-based policy. DELETE is one explicit removal operation with
table-specific predicates. TRUNCATE removes all data only for supported table types. Check the table
type before choosing a path.

<a id="backup-vs-restore-mount"></a>

## Backup versus restore and mount

Backup creates recovery material, restore replaces an offline instance from backup, and mount opens
a supported backup read-only under another name. A successful backup must still be tested through a
mount or isolated restore workflow.

<a id="machloader-vs-csvimport-csvexport-tagmetaimport"></a>
<a id="load-data-infile-vs-machloader"></a>
<a id="ingestion-sdk-append-vs-sql-collector"></a>

## Input-path comparison

The SDK, loader, and Collector comparison belongs to
[Data input and export](/dbms/development-tools-integration/data-input-load-export/#machloader-vs-csvimport-csvexport-tagmetaimport).
