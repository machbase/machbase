---
type: docs
title: '17.1.1.23 AUTO_INCREMENT'
weight: 230
toc: true
aliases:
  - /dbms/rdb-table-usage/auto-increment/
---

`AUTO_INCREMENT` makes the server generate a single 64-bit integer primary-key value.

<span class="badge-since">LOOKUP and VOLATILE support is available since Machbase 8.7.0</span>

## Support

| Item | Support |
|---|---|
| Edition | Standard Edition |
| Tables | TRANSACTION, LOOKUP, VOLATILE |
| Column type | `LONG`, `INT64` |
| Key | A single column-level `PRIMARY KEY` |

Do not use it with a table-level or composite primary key. Do not combine it with
`PROPERTY(SEQUENCE)` or `NEXTVAL()` on the same LOOKUP column.

```sql
CREATE TRANSACTION TABLE device_master (
    id          LONG PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(80),
    site_code   VARCHAR(32)
);

CREATE LOOKUP TABLE lookup_order (
    id   INT64 PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);

CREATE VOLATILE TABLE volatile_order (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);
```

## Generated values

Omit the automatic column or supply `NULL` to generate a value.

```sql
INSERT INTO device_master(device_name, site_code)
VALUES ('compressor-01', 'SEOUL-A');

INSERT INTO device_master(id, device_name, site_code)
VALUES (NULL, 'pump-02', 'SEOUL-A');
```

An explicit non-NULL value at or above the next value advances the sequence. A lower value does not
rewind it. Zero is valid. After `INT64_MAX`, another generated INSERT fails. Treat this as a row
identifier, not a gap-free business sequence.

## Differences by table

| Behavior | TRANSACTION | LOOKUP | VOLATILE |
|---|:---:|:---:|:---:|
| Rows and next value survive restart | Yes | Yes | No |
| Explicit transactions | Yes | No | No |
| Generated value in `INSERT ... SELECT` | Yes | No | No |
| ROWID from a single INSERT | Yes | Yes | Yes |

See [ROWID](../../rowid/) for INSERT-result conditions and
[SDK feature support](/dbms/development-tools-integration/sdk-support-scope/) for client APIs.

## Related documentation

- [TRANSACTION table structure](/dbms/rdb-table-usage/table-structure-schema/)
- [LOOKUP table structure](/dbms/lookup-table-usage/table-structure-schema/)
- [VOLATILE table structure](/dbms/volatile-table-usage/table-structure-schema/)
