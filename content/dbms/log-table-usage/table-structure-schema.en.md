---
type: docs
title: '7.2 Table Structure and Schema'
weight: 20
toc: true
---

Putting an entire message in one column makes it quick to start collection. However, repeatedly
parsing raw messages to count errors by device makes queries complex. Retain the raw message and
extract values used repeatedly for queries and aggregates into separate columns.

<a id="log-table-design"></a>
<a id="log-table-design-design-schema-log"></a>

<a id="발생-시각-검색-필드-원문을-나눕니다"></a>

## Column Layout

The following standalone example stores and checks one security event.

```sql
CREATE LOG TABLE ch7_schema (
    event_time DATETIME,
    event_id   VARCHAR(64),
    device     VARCHAR(32),
    severity   SHORT,
    src_ip     IPV4,
    dst_port   INTEGER,
    message    TEXT
);

INSERT INTO ch7_schema VALUES (
    TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    'evt-0001', 'FW-01', 3, '192.0.2.10', 65535,
    'connection blocked by policy'
);

SELECT event_id, device, severity, src_ip, dst_port, message
  FROM ch7_schema;
```

The query returns the row `evt-0001` with port `65535`. Here, `event_id` is a tracking value, not a
key constraint that prevents duplicate ingestion.

Store the event timestamp recorded by the source in `event_time`. Do not redeclare the automatic
`_arrival_time` column in DDL. Network delays and batch migration can naturally cause the two
timestamps to differ.

<a id="문자열은-길이와-사용-목적을-함께-봅니다"></a>

## Choosing Data Types

| Value | Type | What to check |
|---|---|---|
| Device name, short code, or event ID | `VARCHAR(n)` | LOG permits 1–32,767 bytes, not characters |
| Long raw message | `TEXT` | Maximum 64 MiB; sorting and grouping the raw value are unsupported |
| Severity or small code | `SHORT` or `INTEGER` | Use consistent code meanings in collectors and queries |
| Port | `INTEGER` | `USHORT` reserves 65535 for NULL and cannot represent the full port range |
| Cumulative byte count | `LONG` | Check the expected maximum and reserved NULL value |
| Address | `IPV4` or `IPV6` | Distinguish address format from the need to retain the source string |

In LOG tables, both VARCHAR and TEXT support word search through KEYWORD indexes. Full-text search
alone is no reason to use TEXT for short codes.

String length is a common source of mistakes. `VARCHAR(100)` does not mean 100 Korean characters.
Check the byte length of UTF-8 samples and send oversized values through the actual ingestion path.
Verify whether excess length causes truncation or an error with the SDK or loading tool you will
use.

<a id="정렬집계할-값은-별도로-둡니다"></a>

## Columns for Sorting and Aggregation

In this schema, `device` and `severity` are query predicates and aggregation keys; `message` is used
to read raw text or search for words. Applying `ORDER BY message` or `GROUP BY message` directly to
TEXT causes an error. Choose the device, error code, or event timestamp you actually need instead of
sorting entire messages.

A KEYWORD index is not a morphological analyzer or a relevance-ranked search engine. For the
difference between word search and raw substring search, see
[Text Search](../text-search-keyword-index/).

<a id="스키마가-바뀌면-입력-쪽도-함께-확인하세요"></a>

## Schema Changes and Ingestion Mappings

LOG supports adding, dropping, and renaming columns, and limited attribute changes. This does not
mean that stored row values can be changed with UPDATE. DDL changes particularly affect Appenders
that send values by column position and CSV mappings. Coordinate schema changes with ingestion
program deployment.

Clean up the example table, then continue to [Column Changes](../create-alter-drop/).

```sql
DROP TABLE ch7_schema;
```

If you are unsure which values to extract into columns, list the questions your queries must answer.
Expressing those questions in SQL makes the required columns clearer.
