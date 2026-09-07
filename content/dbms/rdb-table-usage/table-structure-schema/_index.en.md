---
title: '8.2 Table Structure and Schema'
weight: 20
toc: true
---
English structure placeholder. Korean content is authoritative for this restructuring pass.


<a id="rdb-table-design"></a>

## RDB 테이블 설계 (TODO(verify): dbms-nfx#3880 기반 신규 문서화 필요)

<a id="rdb-table-design-design-schema-type-rdb"></a>

### RDB 스키마와 타입 설계

TRANSACTION tables support `DECIMAL(M,D)` exact fixed-point columns. `NUMERIC`, `DEC`,
`FIXED`, and `NUMBER` are aliases for `DECIMAL`.

```sql
CREATE TRANSACTION TABLE invoice (
    invoice_id LONG PRIMARY KEY,
    amount     DECIMAL(18,2),
    tax_rate   NUMERIC(7,4)
);
```

See [DECIMAL and NUMERIC Fixed-Point
Types](/dbms/reference/sql/type-data-types-dictionary/decimal-numeric-fixed-point/)
for precision, scale, rounding, and client mappings.
