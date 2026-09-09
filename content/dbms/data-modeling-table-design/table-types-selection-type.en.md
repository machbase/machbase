---
type: docs
title: '4.1 Choose a Table Type'
weight: 10
toc: true
---
Choose a table type that matches the data early in design. An unsuitable type can reduce
performance and limit required functionality.

- **[Selection Guide](/dbms/data-modeling-table-design/table-types-selection-type/#selection-decision)**
- **[Type Comparison](/dbms/data-modeling-table-design/table-types-selection-type/#comparison-tag-log-rdb-volatile-lookup)**
- **[TRANSACTION vs LOOKUP](/dbms/data-modeling-table-design/table-types-selection-type/#comparison-rdb-vs-lookup)**


<a id="table-types-type"></a>

For table roles and storage concepts, see [Data Model Concepts](../../core-concepts/concepts/#time-series).
The same data can need different types depending on whether you accumulate history or update
current state. Review mutation, query, and persistence requirements together.

### Describe the data before selecting a type

Before naming a table, describe the fact represented by one row in a sentence. Even for the
same equipment, one temperature reading, one current operating state, and one maintenance
job have different row semantics, keys, and update patterns.

| Design question | Equipment monitoring decision |
|---|---|
| What does one row represent? | One sensor reading or an equipment's current state |
| How is it found? | Sensor name and event time, equipment ID, or maintenance job number |
| How do values change? | Append history, correct errors, or overwrite current rows |
| Must changes commit together? | Whether job registration and part quantity changes share a transaction |
| How long is it retained? | Raw and aggregate retention periods; whether state is rebuildable after restart |
| What is the scale? | Tag count, rows/s, row size, memory used by reference data and indexes |

For example, consider TAG for temperature history, LOG for alarms, and LOOKUP for equipment
code tables. If inventory changes and job registration must commit together, consider
TRANSACTION in Standard Edition. A current-state cache can use VOLATILE if it is rebuildable
from source data. Align row semantics and failure recovery before combining these records
in one table.

<a id="selection-decision"></a>

## Selection guide

Use the following flow to narrow candidates, then verify DML, transactions, memory usage,
and edition support in the comparison tables. Even reference data may need TRANSACTION
instead of LOOKUP when multiple changes must share one transaction.

### Decision flow

```text
Is the data sensor/device measurements?
  ├── YES → Time axis?     YES → TAG TABLE (BASETIME)
  │         Distance axis? YES → TAG TABLE (BASEDISTANCE)
  └── NO  ↓

Is the data events/logs/packets? (append-only)
  ├── YES → LOG TABLE
  └── NO  ↓

Is the data a code table/reference data? (repeated reads and updates)
  ├── YES → LOOKUP TABLE
  └── NO  ↓

Is the data in-memory state/cache that can be discarded on server restart?
  ├── YES → VOLATILE TABLE
  └── NO  ↓

General relational business data (UPDATE/DELETE/SELECT/INSERT all required)
  └── TRANSACTION TABLE
```

### Key criteria

| Question | Type |
|------|------|
| Time- or distance-based measurements? | TAG |
| Append raw events and remove only older ranges? | LOG |
| Reference data requiring a PRIMARY KEY and repeated reads/updates? | LOOKUP |
| Can the data be lost on server restart? | VOLATILE |
| General relational work (INSERT/UPDATE/DELETE/SELECT)? | TRANSACTION |

### Considerations

- Using a unique tag name for every event causes continuing growth in tags and metadata.
  Consider LOG for events without recurring measurement targets.
- LOG cannot UPDATE or DELETE with general predicates, so it is unsuitable for mutable data.
  Use retention-oriented `BEFORE`, `OLDEST`, or `EXCEPT` DELETE.
- TRANSACTION is Standard Edition only. In Cluster Edition, consider LOOKUP for small datasets
  or an external RDBMS.
- VOLATILE data is lost on server restart.

<a id="comparison-tag-log-rdb-volatile-lookup"></a>

## Type comparison

### Feature comparison

| Item | TAG | LOG | TRANSACTION | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| DDL | `CREATE TAG TABLE` | `CREATE LOG TABLE` | `CREATE TABLE` / `CREATE TRANSACTION TABLE` / `CREATE TXN TABLE` | `CREATE VOLATILE TABLE` | `CREATE LOOKUP TABLE` |
| Main use | Sensors and measurements | Events and logs | Relational business data | Temporary aggregates | Codes and reference data |
| INSERT | Yes | Yes | Yes | Yes | Yes |
| UPDATE | Yes (Standard, tag/BASETIME predicates) | No | Yes | Yes | Yes |
| DELETE | Yes (BEFORE/predicates/all) | Yes (BEFORE/OLDEST/EXCEPT/all) | Yes | Yes (PK equality/all) | Yes (general predicates/all) |
| PRIMARY KEY | Required | No | Optional | Optional | Required |
| BASETIME | Required (time axis) | No | No | No | No |
| _arrival_time | No | Added automatically | No | No | No |
| Indexes | Tag/axis access, supported secondary indexes | BITMAP/KEYWORD/LSM | BTREE PK + secondary indexes | Key and secondary indexes | Key and secondary indexes |
| Persistence | Yes | Yes | Yes | No (memory) | Yes |
| Cluster Edition | Yes | Yes | No | Yes | Yes |

Append API support depends on the SDK and ingestion path as well as the table type. Check
your driver/table combination in the
[SDK Append Matrix](../../development-tools-integration/sdk-support-scope/#append-table-type-matrix).

### Storage characteristics

| Item | TAG | LOG | TRANSACTION | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| Storage | Columnar | Columnar | Row-oriented (relational) | In memory | Persistent storage + all rows resident in memory |
| Capacity criteria | Tags, raw data, ROLLUP, retention | Raw data, search indexes, retention | Rows, indexes, transaction load | Memory for all rows and indexes | Memory for all rows and indexes; reload time after restart |

Small in-memory tables do not have a fixed row-count definition. Measure actual memory
including row width, variable-length values, and secondary indexes. Compression ratios and
server specifications alone cannot guarantee disk-table throughput either; run representative
ingestion and queries together.

### TRANSACTION table restrictions

TRANSACTION tables have these restrictions:

- **No Cluster Edition support:** Standard Edition only.
- **Minimum columns:** At least one.

<a id="comparison-rdb-vs-lookup"></a>

## TRANSACTION vs LOOKUP

TRANSACTION and LOOKUP both store relational data, but differ in target scale and features.

### Comparison

| Item | TRANSACTION | LOOKUP |
|------|-----------|--------------|
| DDL | `CREATE TRANSACTION TABLE` | `CREATE LOOKUP TABLE` |
| PRIMARY KEY | Optional | Required |
| INSERT | Yes | Yes |
| UPDATE (with WHERE) | Yes | Yes |
| UPDATE (without WHERE) | Yes (all rows) | No |
| DELETE | Yes | Yes |
| Explicit transactions | Control multiple statements with COMMIT/ROLLBACK | Does not participate; changes are per statement |
| Indexes | BTREE PK + secondary indexes | In-memory key and secondary indexes |
| Data scale | Validate disk capacity and transaction load | Validate reference-data read/update load |
| JOIN target | Yes | Yes |
| Cluster Edition | No | Yes |

### Selection criteria

**Choose TRANSACTION for:**

- Data requiring explicit transactions and relational DML
- General relational workloads requiring UPDATE, DELETE, INSERT, and SELECT
- Queries on varied column combinations without a PRIMARY KEY
- Standard Edition environments

**Choose LOOKUP for:**

- Code tables and reference data
- PRIMARY KEY lookups and single-row UPDATE/DELETE
- Use in Cluster Edition
- Real-time reference-data updates

### Example

```sql
-- LOOKUP: country codes (PK lookup and predicate-based UPDATE)
CREATE LOOKUP TABLE country_code (
    code   VARCHAR(4)   PRIMARY KEY,
    name   VARCHAR(64)
);
INSERT INTO country_code VALUES ('KR', 'Republic of Korea');
UPDATE country_code SET name = 'Korea' WHERE code = 'KR';
SELECT code, name FROM country_code WHERE code = 'KR';

-- TRANSACTION: order history (large scale, general UPDATE/DELETE)
CREATE TRANSACTION TABLE order_history (
    order_id  LONG PRIMARY KEY,
    item_id   INTEGER,
    qty       INTEGER,
    amount    DECIMAL(18,2)
);
INSERT INTO order_history VALUES (12345, 501, 1, 12000.00);
UPDATE order_history SET qty = 10 WHERE order_id = 12345;
SELECT order_id, qty, amount FROM order_history WHERE order_id = 12345;
DELETE FROM order_history WHERE order_id = 12345;
SELECT COUNT(*) FROM order_history WHERE order_id = 12345;
```

The first SELECT returns the updated country name; the order SELECT returns quantity `10`.
The final COUNT is `0`. Here, `amount` is an illustrative value maintained separately from
quantity and is not recalculated automatically. In an actual order model, define the
relationship among unit price, quantity, and total, and which columns change together.
When finished, use `DROP TABLE` to remove only the tables created in this example.
