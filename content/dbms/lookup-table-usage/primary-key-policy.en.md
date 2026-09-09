---
type: docs
title: '9.10 PRIMARY KEY Policy'
weight: 100
toc: true
---
This section covers LOOKUP primary key design principles and policies. For how SDKs identify primary
key columns in SELECT results, see
[PRIMARY KEY Metadata Support](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-primary-key-metadata).


<a id="design-primary-key"></a>

## PRIMARY KEY Design

LOOKUP tables require a `PRIMARY KEY`, which uniquely identifies rows and controls duplicates.
UPDATE and DELETE support general predicates in WHERE, but the primary key column itself cannot be
updated.

### Basic Syntax

```text
CREATE LOOKUP TABLE table_name (
    pk_col   type    PRIMARY KEY,
    col2     type,
    ...
);
```

### Single-Column PRIMARY KEY

```sql
CREATE LOOKUP TABLE ch9_pk_country_code (
    code     VARCHAR(4)  PRIMARY KEY,
    name     VARCHAR(64),
    region   VARCHAR(32)
);
```

### When a Composite Key Is Needed

```sql
CREATE LOOKUP TABLE ch9_pk_price (
    price_key  VARCHAR(64) PRIMARY KEY,
    product_id VARCHAR(32),
    region     VARCHAR(16),
    price      DOUBLE
);

-- Insert
INSERT INTO ch9_pk_price VALUES ('PROD-01:KR', 'PROD-01', 'KR', 99.0);
INSERT INTO ch9_pk_price VALUES ('PROD-01:US', 'PROD-01', 'US', 79.0);

-- Update by composite key
UPDATE ch9_pk_price SET price = 89.0
WHERE price_key = 'PROD-01:KR';
```

Only one LOOKUP column can be designated as the PRIMARY KEY. If a business key combines several
columns, store a combined string or surrogate key in a separate PRIMARY KEY column.

### Choosing a PRIMARY KEY Type

| Type | Advantages | Disadvantages |
|------|------|------|
| `VARCHAR(n)` | Readable, meaningful keys | String comparison cost |
| `INTEGER` / `LONG` | Fast comparison, efficient storage | No business meaning; separate mapping needed |

### Considerations

- PRIMARY KEY values must be unique.
- PRIMARY KEY values cannot be updated; use DELETE + INSERT to change them.
- An index is created automatically on the PRIMARY KEY column.
- Only one column can be designated as the PRIMARY KEY.

<a id="policy-lookup-primary-key"></a>

## PRIMARY KEY Policy

Consider the following policies and practices when designing primary keys.

### Natural versus Surrogate Keys

#### Natural Key

Use a value with business meaning directly as the PRIMARY KEY.

```sql
-- Country code: a standardized natural key
CREATE LOOKUP TABLE ch9_pk_country (
    iso_code VARCHAR(4) PRIMARY KEY,  -- ISO 3166-1 alpha-2
    name     VARCHAR(64)
);
```

**Advantages**: Easy to interpret; no separate lookup required.
**Disadvantages**: Changing keys creates referential-integrity concerns.

#### Surrogate Key

Use a value without business meaning, such as a SEQUENCE column or UUID, as the PRIMARY KEY.

```sql
-- Equipment master: surrogate key
CREATE LOOKUP TABLE ch9_pk_equip (
    equip_id  LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    code      VARCHAR(32),          -- Business key
    name      VARCHAR(128)
);
CREATE INDEX ch9_pk_equip_idx ON ch9_pk_equip(code);
```

**Advantages**: Immutable; efficient joins.
**Disadvantages**: Code-to-ID mapping required.

### PRIMARY KEY Immutability

PRIMARY KEY values cannot be updated. Use DELETE + INSERT when a change is required.

```sql
-- Incorrect pattern (use DELETE + INSERT for key changes)
-- UPDATE cannot change a primary key

-- Correct pattern
DELETE FROM ch9_pk_country WHERE iso_code = 'OLD';
INSERT INTO ch9_pk_country VALUES ('NEW', '새 국가명');
```

LOOKUP DML executes statement by statement. LOOKUP DML cannot be included in a TRANSACTION table
transaction enclosed by `BEGIN`/`COMMIT`.

Account for reads between the two statements and for insert failure. Retain the old values and
define the transition order for referencing keys before making changes. If the entire change must be
atomic, consider TRANSACTION tables.

Clean up the example tables as follows.

```sql
DROP INDEX ch9_pk_equip_idx;
DROP TABLE ch9_pk_equip;
DROP TABLE ch9_pk_country;
DROP TABLE ch9_pk_price;
DROP TABLE ch9_pk_country_code;
```
