---
type: docs
title: '8.13 TRANSACTION INSERT ON DUPLICATE KEY UPDATE'
weight: 130
toc: true
---

Inserting when absent and updating when present seems simple, but the definition of a duplicate
determines which row changes. Retransmitting counter increments can apply one event twice. Check
keys, update targets, and retry policy together.

TRANSACTION `INSERT ... ON DUPLICATE KEY UPDATE` updates an existing row on a PRIMARY KEY or
ordinary UNIQUE INDEX conflict. Exercises create their own objects. Keep error-checking SQL separate
from normal flow and complete cleanup before rerunning.

## Supported Syntax

TRANSACTION supports the `INSERT ... VALUES ...` UPSERT form.

```text
INSERT INTO table_name VALUES (...)
    ON DUPLICATE KEY UPDATE;

INSERT INTO table_name VALUES (...)
    ON DUPLICATE KEY UPDATE SET column_name = expression [, ...];

INSERT INTO table_name(column_name, ...)
VALUES (...)
    ON DUPLICATE KEY UPDATE;

INSERT INTO table_name(column_name, ...)
VALUES (...)
    ON DUPLICATE KEY UPDATE SET column_name = expression [, ...];
```

The following keys qualify for conflict detection.

- TRANSACTION PRIMARY KEY
- TRANSACTION UNIQUE INDEX
- TRANSACTION composite UNIQUE INDEX

## Basic Behavior

Without a duplicate, a new row is added as in ordinary INSERT.

```sql
CREATE TRANSACTION TABLE ch8_up_device_state (
    device_id INTEGER PRIMARY KEY,
    status VARCHAR(16),
    alarm_count INTEGER,
    updated_at DATETIME
);

INSERT INTO ch8_up_device_state
VALUES (1, 'NORMAL', 0, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        status = 'NORMAL',
        updated_at = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

A duplicate PRIMARY KEY updates the existing row.

```sql
INSERT INTO ch8_up_device_state
VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        status = 'ALARM',
        alarm_count = alarm_count + 1,
        updated_at = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS');
```

The `SET` clause cannot change the PRIMARY KEY. Right-hand expressions are evaluated against the
conflicting existing row. Thus `alarm_count = alarm_count + 1` adds 1 to the existing alarm_count,
not the attempted insert value.

```sql
SELECT device_id, status, alarm_count, updated_at
FROM ch8_up_device_state
WHERE device_id = 1;
```

The expected result has the following form.

```text
DEVICE_ID  STATUS  ALARM_COUNT  UPDATED_AT
---------  ------  -----------  -----------------------------
1          ALARM   1            2026-07-10 09:05:00 000:000:000
```

The `SET` clause after `ON DUPLICATE KEY UPDATE` is optional.

```sql
CREATE TRANSACTION TABLE ch8_up_asset_cache (
    asset_id INTEGER PRIMARY KEY,
    asset_name VARCHAR(80),
    location VARCHAR(80),
    keep_value INTEGER
);

INSERT INTO ch8_up_asset_cache VALUES (1, 'compressor-a', 'plant-1', 100);

INSERT INTO ch8_up_asset_cache(asset_id, asset_name, location)
VALUES (1, 'compressor-a-renamed', 'plant-2')
    ON DUPLICATE KEY UPDATE;
```

Without SET, only non-PRIMARY KEY columns included in the INSERT target list are applied to the
existing row. Here, asset_name and location change; keep_value, omitted from the list, retains its
previous value.

```sql
SELECT asset_id, asset_name, location, keep_value
FROM ch8_up_asset_cache
ORDER BY asset_id;
```

The expected result has the following form.

```text
ASSET_ID  ASSET_NAME            LOCATION  KEEP_VALUE
--------  --------------------  --------  ----------
1         compressor-a-renamed  plant-2   100
```

For a table containing only a PRIMARY KEY column, a duplicate UPSERT without SET has no columns to
update, so the row remains unchanged.

## UNIQUE INDEX Duplicate Handling

UNIQUE INDEX conflicts also take the update path, not only PRIMARY KEY conflicts.

```sql
CREATE TRANSACTION TABLE ch8_up_account_profile (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120),
    display_name VARCHAR(80),
    login_count INTEGER
);

CREATE UNIQUE INDEX ch8_up_uidx_account_profile_email
ON ch8_up_account_profile(email);

INSERT INTO ch8_up_account_profile
VALUES (1, 'ops@example.com', 'ops-user', 1);

INSERT INTO ch8_up_account_profile
VALUES (2, 'ops@example.com', 'ops-renamed', 1)
    ON DUPLICATE KEY UPDATE SET
        display_name = 'ops-renamed',
        login_count = login_count + 1;

SELECT id, email, display_name, login_count
FROM ch8_up_account_profile
ORDER BY id;
```

The email UNIQUE INDEX conflicts, so the row with id=1 is updated. The attempted id=2 row is not inserted.

A composite UNIQUE INDEX treats the entire matching key combination as a duplicate.

```sql
CREATE TRANSACTION TABLE ch8_up_daily_device_summary (
    id INTEGER PRIMARY KEY,
    device_id INTEGER,
    summary_day VARCHAR(10),
    event_count INTEGER,
    last_status VARCHAR(16)
);

CREATE UNIQUE INDEX ch8_up_uidx_daily_device_summary
ON ch8_up_daily_device_summary(device_id, summary_day);

INSERT INTO ch8_up_daily_device_summary
VALUES (1, 101, '2026-07-10', 3, 'NORMAL');

INSERT INTO ch8_up_daily_device_summary
VALUES (2, 101, '2026-07-10', 1, 'ALARM')
    ON DUPLICATE KEY UPDATE SET
        event_count = event_count + 1,
        last_status = 'ALARM';

INSERT INTO ch8_up_daily_device_summary
VALUES (3, 101, '2026-07-11', 1, 'NORMAL')
    ON DUPLICATE KEY UPDATE SET
        event_count = event_count + 1;
```

The first UPSERT updates `(device_id, summary_day) = (101, '2026-07-10')`. The second inserts a new
row because the date differs.

UNIQUE keys containing NULL are not treated as duplicates of each other. These two inserts create
separate rows instead of overwriting each other.

```sql
INSERT INTO ch8_up_daily_device_summary VALUES (4, NULL, '2026-07-10', 1, 'NORMAL')
    ON DUPLICATE KEY UPDATE;
INSERT INTO ch8_up_daily_device_summary VALUES (5, NULL, '2026-07-10', 2, 'ALARM')
    ON DUPLICATE KEY UPDATE;
SELECT id, device_id, summary_day, event_count
  FROM ch8_up_daily_device_summary ORDER BY id;
```

Result IDs are 1, 3, 4, and 5, with event_count values 4, 1, 1, and 2, respectively. Required
business keys need NOT NULL on their component columns as well as a UNIQUE INDEX.

## Usage Examples

TAG can continuously store time-ordered measurements while TRANSACTION maintains only the latest
state per device.

```sql
CREATE TRANSACTION TABLE ch8_up_latest_device_status (
    device_name VARCHAR(80) PRIMARY KEY,
    last_value DOUBLE,
    last_state VARCHAR(16),
    event_count LONG,
    updated_at DATETIME
);

INSERT INTO ch8_up_latest_device_status
VALUES ('compressor-a', 72.5, 'NORMAL', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        last_value = 72.5,
        last_state = 'NORMAL',
        event_count = event_count + 1,
        updated_at = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS');

INSERT INTO ch8_up_latest_device_status
VALUES ('compressor-a', 91.2, 'ALARM', 1, TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        last_value = 91.2,
        last_state = 'ALARM',
        event_count = event_count + 1,
        updated_at = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS');
```

Use this pattern when dashboards need fast access only to current state.

When an external system repeatedly sends reference data with the same business key, UPSERT can use
its UNIQUE INDEX.

```sql
CREATE TRANSACTION TABLE ch8_up_customer_device (
    id LONG PRIMARY KEY AUTO_INCREMENT,
    external_device_id VARCHAR(64),
    device_name VARCHAR(80),
    owner_name VARCHAR(80),
    enabled INTEGER
);

CREATE UNIQUE INDEX ch8_up_uidx_customer_device_external_id
ON ch8_up_customer_device(external_device_id);

INSERT INTO ch8_up_customer_device(external_device_id, device_name, owner_name, enabled)
VALUES ('ERP-DEV-10001', 'compressor-a', 'line-1', 1)
    ON DUPLICATE KEY UPDATE SET
        device_name = 'compressor-a',
        owner_name = 'line-1',
        enabled = 1;

INSERT INTO ch8_up_customer_device(external_device_id, device_name, owner_name, enabled)
VALUES ('ERP-DEV-10001', 'compressor-a-renamed', 'line-2', 1)
    ON DUPLICATE KEY UPDATE SET
        device_name = 'compressor-a-renamed',
        owner_name = 'line-2',
        enabled = 1;
```

The first INSERT creates a row; the second updates it through an external_device_id UNIQUE INDEX
conflict. The internal id remains unchanged.

Use UPSERT without SET to apply source column values directly to a current-state cache.

```sql
CREATE TRANSACTION TABLE ch8_up_tag_alias_cache (
    alias_name VARCHAR(80) PRIMARY KEY,
    tag_name VARCHAR(80),
    unit VARCHAR(16),
    description VARCHAR(160),
    manually_checked INTEGER
);

INSERT INTO ch8_up_tag_alias_cache
VALUES ('compressor-a-temp', 'comp_a.temp', 'celsius', 'main compressor temp', 1);

INSERT INTO ch8_up_tag_alias_cache(alias_name, tag_name, unit, description)
VALUES ('compressor-a-temp', 'comp_a.temperature', 'celsius', 'renamed tag')
    ON DUPLICATE KEY UPDATE;
```

This statement updates only tag_name, unit, and description. manually_checked is absent from the
column list and retains its value.

An aggregate table can accumulate occurrence counts by key.

```sql
CREATE TRANSACTION TABLE ch8_up_alarm_counter (
    alarm_code VARCHAR(32) PRIMARY KEY,
    first_seen DATETIME,
    last_seen DATETIME,
    hit_count LONG
);

INSERT INTO ch8_up_alarm_counter
VALUES (
    'OVER_TEMP',
    TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    1
)
ON DUPLICATE KEY UPDATE SET
    last_seen = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    hit_count = hit_count + 1;

INSERT INTO ch8_up_alarm_counter
VALUES (
    'OVER_TEMP',
    TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'),
    1
)
ON DUPLICATE KEY UPDATE SET
    last_seen = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'),
    hit_count = hit_count + 1;
```

`hit_count = hit_count + 1` is evaluated against the existing row, making it suitable for cumulative
counters.

JSON columns can also be update targets.

```sql
CREATE TRANSACTION TABLE ch8_up_device_json_state (
    device_id INTEGER PRIMARY KEY,
    state JSON,
    updated_at DATETIME
);

INSERT INTO ch8_up_device_json_state
VALUES (
    1,
    '{"status":"NORMAL","score":10}',
    TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS')
)
ON DUPLICATE KEY UPDATE SET
    state = '{"status":"NORMAL","score":10}',
    updated_at = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS');

INSERT INTO ch8_up_device_json_state
VALUES (
    1,
    '{"status":"ALARM","score":90}',
    TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS')
)
ON DUPLICATE KEY UPDATE SET
    state = '{"status":"ALARM","score":90}',
    updated_at = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS');

SELECT JSON_EXTRACT_STRING(state, '$.status') AS status,
       JSON_EXTRACT_INTEGER(state, '$.score') AS score
FROM ch8_up_device_json_state
WHERE device_id = 1;
```

Limitation: JSON path UNIQUE INDEX is excluded from conflict-key candidates. Its conflicts produce
uniqueness errors instead of taking the UPSERT update path.

## Transactions and Privileges

TRANSACTION UPSERT is committed or rolled back inside a transaction like ordinary INSERT/UPDATE.

```sql
CREATE TRANSACTION TABLE ch8_up_tx_device_state (
    id INTEGER PRIMARY KEY,
    status VARCHAR(16),
    count_value INTEGER
);

INSERT INTO ch8_up_tx_device_state VALUES (1, 'NORMAL', 10);

BEGIN;

INSERT INTO ch8_up_tx_device_state VALUES (2, 'NORMAL', 1)
    ON DUPLICATE KEY UPDATE SET count_value = count_value + 1;

INSERT INTO ch8_up_tx_device_state VALUES (1, 'ALARM', 1)
    ON DUPLICATE KEY UPDATE SET
        status = 'ALARM',
        count_value = count_value + 1;

ROLLBACK;

SELECT id, status, count_value
FROM ch8_up_tx_device_state
ORDER BY id;
```

Both insert and update paths are rolled back in this example.

If a duplicate-update statement fails with an ordinary constraint violation, earlier successful
changes can remain in the explicit transaction. After checking the error, the application must
decide whether to continue or cancel business changes with ROLLBACK.

TRANSACTION UPSERT requires both INSERT and UPDATE privileges. Grant both even when execution takes
the insert path, because the statement includes an update path.

The following shows only the privilege syntax. Apply it as a separate administrative operation using
the actual owner, table, and existing application account.

```text
GRANT INSERT ON owner.table_name TO app_user;
GRANT UPDATE ON owner.table_name TO app_user;
```

SELECT privilege is not required to execute TRANSACTION UPSERT itself. It is required separately if
the application executes SELECT to verify results.

<a id="타입과-지원하지-않는-구문"></a>

## Supported Types and Constraints

Columns updated in SET follow the same public type support as ordinary TRANSACTION UPDATE.

| Category | Types |
| --- | --- |
| Integer | `SHORT`, `INT16`, `USHORT`, `UINT16`, `INT`, `INTEGER`, `INT32`, `UINTEGER`, `UINT32`, `LONG`, `INT64`, `ULONG`, `UINT64` |
| Floating point | `FLOAT`, `DOUBLE` |
| Fixed point | `DECIMAL`, `NUMERIC`, `DEC`, `FIXED`, `NUMBER` |
| String/LOB | `VARCHAR`, `TEXT`, `CLOB`, `BINARY`, `BLOB` |
| Other | `DATETIME`, `IPV4`, `IPV6`, `JSON` |

This table lists scalar types used by TRANSACTION. For numeric ARRAY support, see the
[Data Type Dictionary](/dbms/reference/sql/types/).

Conflict keys and index types follow TRANSACTION PRIMARY KEY and UNIQUE INDEX type policies. UPSERT
does not expand supported key types.

The following syntax is unsupported.

```text
-- Illustrative examples of unsupported syntax.
-- Combining INSERT SELECT with ON DUPLICATE KEY UPDATE is unsupported.
INSERT INTO ch8_up_device_state(device_id, status, alarm_count, updated_at)
SELECT device_id, status, alarm_count, updated_at
FROM staging_device_state
ON DUPLICATE KEY UPDATE SET status = 'UPDATED';

-- The MySQL VALUES(col) function is unsupported.
INSERT INTO ch8_up_device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
ON DUPLICATE KEY UPDATE SET status = VALUES(status);

-- The EXCLUDED alias is unsupported.
INSERT INTO ch8_up_device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
ON DUPLICATE KEY UPDATE SET status = EXCLUDED.status;

-- Conflict-target syntax is unsupported.
INSERT INTO ch8_up_device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
ON CONFLICT (device_id) DO UPDATE SET status = 'ALARM';
```

Target-table restrictions are as follows.

- This page covers only TRANSACTION PRIMARY KEY/UNIQUE conflict behavior. The same SQL form also supports PRIMARY KEY conflicts in LOOKUP and VOLATILE. Use the [DML Dictionary](/dbms/reference/sql/syntax/dml-syntax/#on-duplicate-key-update) as the authoritative common syntax reference.
- LOG and TAG DATA rows are unsupported. For TAG METADATA tag-name conflicts, see the [DML Dictionary](/dbms/reference/sql/syntax/dml-syntax/#on-duplicate-key-update).
- Even a TRANSACTION table requires a PRIMARY KEY or UNIQUE INDEX for UPSERT.
- JSON path UNIQUE INDEX is not used as a conflict key.

## Conflicts and Error Handling

If multiple UNIQUE indexes identify the same existing row, it is updated once. If they conflict with
different existing rows, the statement fails because it cannot determine which row to update.

The following sample conflicts with two business keys on different rows.

```sql
CREATE TRANSACTION TABLE ch8_up_user_contact (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120),
    phone VARCHAR(40),
    note VARCHAR(80)
);

CREATE UNIQUE INDEX ch8_up_uidx_user_contact_email ON ch8_up_user_contact(email);
CREATE UNIQUE INDEX ch8_up_uidx_user_contact_phone ON ch8_up_user_contact(phone);

INSERT INTO ch8_up_user_contact VALUES (1, 'a@example.com', '010-0000-0001', 'user-a');
INSERT INTO ch8_up_user_contact VALUES (2, 'b@example.com', '010-0000-0002', 'user-b');

```

Only the following INSERT intentionally fails in this optional exercise.

```sql
-- email conflicts with id=1; phone conflicts with id=2.
-- Different conflicting rows cause failure instead of selecting an update path.
INSERT INTO ch8_up_user_contact VALUES (3, 'a@example.com', '010-0000-0002', 'ambiguous')
ON DUPLICATE KEY UPDATE SET note = 'updated';
```

If SET results violate another UNIQUE constraint or NOT NULL, the statement fails and preserves the
existing row.

<a id="재전송과-최신-상태의-의미를-확인하세요"></a>

## Retransmission and Current State

Counter-increment UPSERT is not automatic deduplication. Repeating the same event increments the
counter again. If a COMMIT response is lost, first verify the result using business keys and
event-processing records.

Simple overwrites maintain the latest state only when ingestion order matches event order. Define
source-time comparison and collection policies so late historical events do not overwrite newer
values. For changes spanning tables, also check [Commit Scope During Failures](../transaction/).

## Operational Recommendations

- Define PRIMARY KEY or UNIQUE INDEX first when the business key is clear.
- Use `SET count_col = count_col + 1` for cumulative counters.
- Use UPSERT without SET to apply source row values directly. Columns omitted from the list retain their values.
- With multiple UNIQUE indexes, handle inputs that could conflict with different existing rows before execution.
- When migrating MySQL-compatible SQL, replace VALUES(col), EXCLUDED, and ON CONFLICT with supported Machbase syntax.
- Avoid JSON path UNIQUE INDEX as an UPSERT key. If needed, extract the key into an ordinary column and create a UNIQUE INDEX there.


<a id="실습-결과-확인과-정리"></a>

## Verify Results and Clean Up

After completing the successful exercise, recheck representative values and counts. The expectations
below assume every normal statement ran once, excluding intentional errors.

```sql
SELECT id, email, display_name, login_count
  FROM ch8_up_account_profile ORDER BY id;
SELECT device_name, last_state, event_count
  FROM ch8_up_latest_device_status;
SELECT external_device_id, device_name, owner_name
  FROM ch8_up_customer_device;
SELECT alias_name, tag_name, manually_checked FROM ch8_up_tag_alias_cache;
SELECT alarm_code, hit_count FROM ch8_up_alarm_counter;
SELECT id, status, count_value FROM ch8_up_tx_device_state ORDER BY id;
SELECT id, note FROM ch8_up_user_contact ORDER BY id;
```

| Sample | Expected result |
|---|---|
| account_profile | id=1 retained, display_name=ops-renamed, login_count=2 |
| latest_device_status | ALARM, event_count=2 |
| customer_device | One external-key row; name compressor-a-renamed, owner line-2 |
| tag_alias_cache | tag_name=comp_a.temperature; manually_checked=1 retained |
| alarm_counter | OVER_TEMP hit_count=2 |
| tx_device_state | After ROLLBACK, only existing id=1, NORMAL, count_value=10 |
| user_contact | user-a and user-b at id=1 and id=2 remain unchanged |

```sql
DROP TABLE ch8_up_user_contact;
DROP TABLE ch8_up_tx_device_state;
DROP TABLE ch8_up_device_json_state;
DROP TABLE ch8_up_alarm_counter;
DROP TABLE ch8_up_tag_alias_cache;
DROP TABLE ch8_up_customer_device;
DROP TABLE ch8_up_latest_device_status;
DROP TABLE ch8_up_daily_device_summary;
DROP TABLE ch8_up_account_profile;
DROP TABLE ch8_up_asset_cache;
DROP TABLE ch8_up_device_state;
```

DROP targets only this page's example objects. For complex keys, compare attempted input with
existing conflicting rows side by side. Clarifying which row was intended for update helps identify
the cause.
