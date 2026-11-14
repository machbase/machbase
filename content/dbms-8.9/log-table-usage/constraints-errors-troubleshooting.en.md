---
type: docs
title: '7.8 Constraints, Errors, and Troubleshooting'
weight: 80
toc: true
---

Repeating the same failed SQL can leave the cause unchanged while making the state harder to
understand. First distinguish unsupported operations from invalid input or object-state issues. This
section narrows down checks by symptom.

<a id="limitations-log"></a>
<a id="지원하지-않는-기능"></a>

<a id="모델의-제약인지-먼저-확인합니다"></a>

## Feature Support

| Request | LOG support | Alternative |
|---|---|---|
| General UPDATE | Unsupported | Design correction events or choose a mutable table |
| DELETE WHERE with arbitrary predicates | Unsupported | BEFORE, OLDEST, EXCEPT, or a different model |
| PRIMARY KEY/UNIQUE constraints | Unsupported | Handle duplicates during collection or choose another table |
| Value/range indexes | LSM supported | Choose according to type and predicate |
| Word search | KEYWORD supported | Create on VARCHAR/TEXT, then use SEARCH/ESEARCH |
| BITMAP analytical indexes | Subject to supported conditions | Check type, encoding, and value distribution |
| ORDER BY/GROUP BY on TEXT itself | Unsupported | Use separate code, severity, or time columns |

<a id="증상에서-확인-지점을-찾습니다"></a>

## Diagnosis by Symptom

| Symptom | First check | Action |
|---|---|---|
| Stored arrival time differs from the explicit value | Previous timestamp and TIME_INVERSION_MODE | Check adjustment; retain event time separately |
| SEARCH reports an index error | KEYWORD index on the column | Check type, table, and index name |
| A word exists but is not found | SEARCH tokens versus LIKE substrings | Compare both results on one raw row |
| Query remains slow after index creation | Plan, build state, and time range | Check indexing progress, then measure representative load |
| Column length change fails | Existing type and new length | Use VARCHAR expansion only; check the maximum |
| MINMAX change fails | Whether the type is variable-length | Target only supported fixed-length LOG columns |
| NOT NULL change fails | Existing NULL rows | Distinguish existing-data checks from NOCHECK semantics |
| An event appears multiple times | Source ID, retries, and file reprocessing | Review retransmission policy; arbitrary row deletion is unavailable |
| DDL reports a resource-in-use error | Conflicts with ingestion or queries | Reschedule operations and check again |

Check server settings and the index list as follows.

```sql
SELECT NAME, VALUE FROM V$PROPERTY
 WHERE NAME IN ('DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE', 'TABLE_SCAN_DIRECTION');
SHOW INDEXES;
```

Checking a setting and changing it are separate operations. Do not change production-wide settings
before identifying the cause.

<a id="작은-테이블에서-오류와-정상-경로를-비교합니다"></a>

## Reproducing and Resolving Errors

```sql
CREATE LOG TABLE ch7_error (event_id INTEGER, message TEXT);
INSERT INTO ch7_error VALUES (1, 'connection timeout');
SELECT event_id, message FROM ch7_error;
```

The query returns one row. Each statement below intentionally fails. Run only the statement you want
to verify, separately from the normal exercise.

```sql
-- No KEYWORD index exists.
SELECT event_id FROM ch7_error WHERE message SEARCH 'timeout';

-- Sorting and grouping TEXT itself are unsupported.
SELECT message FROM ch7_error ORDER BY message;
SELECT message, COUNT(*) FROM ch7_error GROUP BY message;

-- LOG does not support general UPDATE or predicate-based DELETE.
UPDATE ch7_error SET message = 'fixed' WHERE event_id = 1;
DELETE FROM ch7_error WHERE event_id = 1;

-- This statement does not convert TEXT to VARCHAR.
ALTER TABLE ch7_error MODIFY COLUMN (message VARCHAR(4096));
```

Now create the index and check the supported search path.

```sql
CREATE INDEX ch7_error_msg ON ch7_error(message) INDEX_TYPE KEYWORD;
EXEC TABLE_FLUSH(ch7_error);
EXEC INDEX_FLUSH(ch7_error);

SELECT event_id, message FROM ch7_error
 WHERE message SEARCH 'timeout'
 ORDER BY event_id;

DROP TABLE ch7_error;
```

Row 1 should be returned. Adding an index does not enable TEXT sorting or LOG UPDATE.

<a id="보존-문제는-삭제-경계부터-확인하세요"></a>

## Diagnosing Retention Policies

If expired rows remain, check the assigned policy, execution interval, LAST_DELETED_TIME, and actual
`_arrival_time` together. Do not conclude deletion failed based only on `event_time`. For exercises,
see [Operations and Data Lifecycle](../operations-lifecycle/).

If the issue persists, collect the server version and Edition, table DDL, failing SQL, complete
error message, and representative input values. Redact passwords and sensitive logs before sharing.
A small reproducer is more useful for diagnosis than sending the entire dataset.
