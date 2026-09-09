---
type: docs
title: '7.4 Data Input'
weight: 40
toc: true
---

Successfully inserting one or two rows does not complete ingestion preparation. Continuous
collection must account for send buffers, partial row failures, and retransmission after
disconnection. First verify columns and timestamps with SQL, then choose an ingestion path suited to
the required throughput.

<a id="original-85-inserting-data"></a>

<a id="작은-insert로-입력-계약을-확인합니다"></a>

## SQL INSERT

```sql
CREATE LOG TABLE ch7_input (
    event_time DATETIME,
    event_id   VARCHAR(32),
    device     VARCHAR(32),
    message    VARCHAR(128)
);

INSERT INTO ch7_input(event_time, event_id, device, message)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        'evt-001', 'DEV-01', 'connection timeout');

SELECT _arrival_time, event_time, event_id, device, message
  FROM ch7_input;
```

The query returns one row, with `event_time` set to the fixed event timestamp. Because
`_arrival_time` is omitted, the ingestion path uses server time. Under the default setting,
out-of-order timestamps may be adjusted, so do not assume this value always exactly matches
reception time. For details, see [Time Model](../arrival-time-model/).

Next, check what happens when the same event is inserted again.

```sql
INSERT INTO ch7_input(event_time, event_id, device, message)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        'evt-001', 'DEV-01', 'connection timeout');

SELECT event_id, COUNT(*) AS received_rows
  FROM ch7_input
 GROUP BY event_id;

DROP TABLE ch7_input;
```

The count for `evt-001` is 2. LOG does not deduplicate events with the same name. Successful
transmission by the collector and exactly-once storage of a source event are separate concerns.

<a id="입력-경로는-데이터-위치와-발생-방식으로-고릅니다"></a>

## Choosing an Ingestion Path

| Situation | Initial choice | Also check |
|---|---|---|
| Small inserts or functional checks | SQL INSERT | Column list, types, and date format |
| Continuous bulk ingestion from applications | SDK Append | Buffer transmission, row-level failures, and reconnection policy |
| CSV read by a client | csvimport or machloader | Column mapping and rejected-row files |
| Load files accessible to the server | LOAD DATA INFILE | Server path and file access permissions |

SQL INSERT incurs processing overhead for each statement. For continuous bulk ingestion, consider
the Append API, which sends rows in batches. For runnable code in your language, see
[Development and Application Integration](/dbms/development-tools-integration/).

<a id="append에서는-전송과-결과-확인을-분리해-생각하세요"></a>

## Append Transmission and Error Handling

After a row is passed to an Appender, it may still be in a client buffer. Check the SDK's flush and
close behavior, and handle remaining buffers and connections on exception paths as well as normal
shutdown.

A successful call does not necessarily mean every row was stored. SDKs expose results differently,
through return values, error callbacks, or success/failure counts at close. First test a small batch
deliberately containing oversized values, NULL values, and date-conversion errors.

A common problem is disconnection before a response arrives. A retry may resend a batch already
stored, so record source event IDs and processing positions. LOG INSERT and Append operations are
also outside the scope of ROLLBACK in TRANSACTION table transactions.

<a id="파일-적재는-성공-건수보다-매핑을-먼저-봅니다"></a>

## File Loading and Mapping

Prepare samples containing Korean text, empty strings, NULL values, long messages, and different
time zones. Check the source field count and target column order before processing the full file.
Retain rejected-row files and logs so the same errors can be investigated later.

For complete commands, see
[Data Ingestion, Loading, and Export](/dbms/development-tools-integration/data-input-load-export/).
To preserve `_arrival_time` during historical migration, check both sort order and existing target
data. For ordinary collection, it is safer to store historical event timestamps in a separate
`event_time` column.

If ingestion fails, start with one failing source row rather than the full batch. Compare its field
values, target types, and ingestion API to identify the cause.
