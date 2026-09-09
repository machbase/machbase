---
type: docs
title: '8.6 Indexes and Performance'
weight: 60
toc: true
---

Indexes can enforce uniqueness as well as speed queries. Distinguish indexes protecting business
keys from those reducing reads so performance cleanup does not accidentally remove required
constraints.

<a id="index-tuning-rdb"></a>
<a id="index-strategy-rdb-primary-key-unique-normal"></a>

<a id="primary-key-unique-일반-인덱스를-구분합니다"></a>

## Index Types

| Type | Purpose | Composite columns | NULL |
|---|---|---|---|
| PRIMARY KEY | Row identification; one per table | Unsupported | Not allowed |
| UNIQUE INDEX | Business-key uniqueness | Supported | NULL-containing keys are not duplicates of each other |
| Ordinary index | Predicate-query access path | Supported | No uniqueness check |

TRANSACTION indexes are displayed as BTREE. Use a column PRIMARY KEY or add CREATE PRIMARY KEY INDEX
afterward. Do not apply LOG LSM/KEYWORD index syntax directly to TRANSACTION.

<a id="unique-index-rdb"></a>

<a id="null과-중복을-함께-확인합니다"></a>

## UNIQUE INDEX and NULL

```sql
CREATE TRANSACTION TABLE ch8_index_account (
    id      LONG PRIMARY KEY,
    email   VARCHAR(120),
    tenant  INTEGER NOT NULL,
    login   VARCHAR(64)
);
INSERT INTO ch8_index_account VALUES (1, 'a@example.com', 1, 'alpha');
INSERT INTO ch8_index_account VALUES (2, 'b@example.com', 1, 'beta');
INSERT INTO ch8_index_account VALUES (3, NULL, 2, NULL);
INSERT INTO ch8_index_account VALUES (4, NULL, 2, NULL);

CREATE UNIQUE INDEX ch8_index_email ON ch8_index_account(email);
CREATE UNIQUE INDEX ch8_index_login ON ch8_index_account(tenant, login);

SELECT id FROM ch8_index_account WHERE email IS NULL ORDER BY id;
SHOW INDEX ch8_index_email;
```

Rows 3 and 4 both exist, and the index is created. If a business key must have values, every key
column needs NOT NULL as well as UNIQUE. Use separate CREATE UNIQUE INDEX instead of UNIQUE inside
CREATE TABLE.

The following two optional statements each test a uniqueness violation.

```sql
-- Expected failure: duplicate email
INSERT INTO ch8_index_account VALUES (5, 'a@example.com', 1, 'gamma');
UPDATE ch8_index_account SET email = 'a@example.com' WHERE id = 2;
```

After failure, four rows and row 2's b@example.com should remain. Ordinary UNIQUE violations
currently report ERR-01418. Check indexes and input values together rather than inferring the
duplicated business key from the error text alone.

<a id="unique-삭제는-제약-제거입니다"></a>

## Dropping a UNIQUE INDEX

```sql
DROP INDEX ch8_index_email;
INSERT INTO ch8_index_account VALUES (5, 'a@example.com', 1, 'gamma');
SELECT id, email FROM ch8_index_account WHERE email = 'a@example.com' ORDER BY id;
```

Rows 1 and 5 are now both stored. Recreating the index while duplicates remain fails.

```sql
-- Expected failure: existing data contains duplicates.
CREATE UNIQUE INDEX ch8_index_email ON ch8_index_account(email);
```

Remove row 5 added during the exercise, then recreate the index.

```sql
DELETE FROM ch8_index_account WHERE id = 5;
CREATE UNIQUE INDEX ch8_index_email ON ch8_index_account(email);
SELECT COUNT(*) AS remaining_rows FROM ch8_index_account;
```

The count is 4. In production, determine whether an index provides performance or uniqueness before
removing it.

<a id="일반복합-인덱스는-실제-조건으로-비교합니다"></a>

## Ordinary and Composite Indexes

```sql
CREATE TRANSACTION TABLE ch8_index_event (
    id      LONG PRIMARY KEY,
    status  VARCHAR(16),
    created DATETIME,
    state   JSON
);
INSERT INTO ch8_index_event VALUES (
    1, 'OPEN', TO_DATE('2026-01-01', 'YYYY-MM-DD'), '{"status":"ALARM","code":500}');
INSERT INTO ch8_index_event VALUES (
    2, 'CLOSED', TO_DATE('2026-01-02', 'YYYY-MM-DD'), '{"status":"NORMAL","code":200}');
INSERT INTO ch8_index_event VALUES (
    3, 'OPEN', TO_DATE('2026-01-03', 'YYYY-MM-DD'), '{"code":500}');

EXPLAIN SELECT id FROM ch8_index_event
 WHERE status = 'OPEN' AND created >= TO_DATE('2026-01-01', 'YYYY-MM-DD');

CREATE INDEX ch8_index_status_time ON ch8_index_event(status, created);

EXPLAIN SELECT id FROM ch8_index_event
 WHERE status = 'OPEN' AND created >= TO_DATE('2026-01-01', 'YYYY-MM-DD');

SELECT id FROM ch8_index_event
 WHERE status = 'OPEN' AND created >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
 ORDER BY id;
```

Results must have the same semantics before and after index creation; the final query returns rows 1
and 3. Align the leading column with predicates, but do not assume every compound predicate uses the
index. Verify Machbase plan selection and supported predicate shapes with EXPLAIN. Timings for three
rows are not a benchmark.

<a id="index-strategy-rdb-json-path"></a>

<a id="json-path도-같은-데이터에서-확인합니다"></a>

## JSON Path Indexes

```sql
CREATE INDEX ch8_index_json_status ON ch8_index_event(state->'$.status');
CREATE INDEX ch8_index_json_code ON ch8_index_event(state->'$.code');

EXPLAIN SELECT id FROM ch8_index_event WHERE state->'$.status' = 'ALARM';
SELECT id FROM ch8_index_event WHERE state->'$.status' = 'ALARM' ORDER BY id;
SELECT id FROM ch8_index_event WHERE state->'$.code' = '500' ORDER BY id;
```

The status query returns row 1; the code query returns 1 and 3. An index does not mean every JSON
function expression uses that path. Distinguish result types and comparison semantics of arrow paths
and numeric extraction functions. For frequently repeated complex predicates, also compare a design
using ordinary extracted columns.

Even when a JSON path UNIQUE INDEX can be created, it is not a conflict-selection key for
TRANSACTION UPSERT. Check [UPSERT Constraints](../insert-on-duplicate-key-update/).

<a id="읽기와-쓰기-비용을-함께-기록합니다"></a>

## Read and Write Costs

Compare with the same data volume, predicate values, and concurrent input rate before and after
index creation. Measure INSERT/UPDATE/DELETE throughput and index space as well as query time. LIMIT
reduces result volume, but ORDER BY is required to fix which rows are returned.

```sql
DROP TABLE ch8_index_event;
DROP TABLE ch8_index_account;
```

Replacing a UNIQUE INDEX with an ordinary index for performance removes uniqueness guarantees. First
verify that results and constraints remain equivalent across tuning changes.
