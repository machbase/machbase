---
type: docs
title: '18.8.2 Feature Support by Table Type'
weight: 20
toc: true
---

## Fixed-Point Type Support

| Feature | TAG | LOG | LOOKUP | VOLATILE | RDB |
|---------|:---:|:---:|:------:|:--------:|:---:|
| DECIMAL / NUMERIC column | O | O | O | O | O |

`DECIMAL` is the common exact fixed-point type for all public table types.
`NUMERIC`, `DEC`, `FIXED`, and `NUMBER` are aliases. Precision is limited to 65
digits and scale to 30 digits. See [DECIMAL and NUMERIC Fixed-Point
Types](../../sql/type-data-types-dictionary/decimal-numeric-fixed-point/).
