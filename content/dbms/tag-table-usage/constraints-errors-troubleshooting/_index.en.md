---
title: '5.8 Constraints, Errors, and Troubleshooting'
weight: 80
toc: true
aliases:
  - /dbms/troubleshooting/update-delete/
---
English structure placeholder. Korean content is authoritative for this restructuring pass.


<a id="rejected-condition-tag-data-update-where"></a>

## TAG data UPDATE WHERE-condition errors

TAG data UPDATE requires both a tag selector and a BASETIME condition. Starting with
Machbase 8.7.0, Standard Edition accepts positional and named bind parameters for NAME
and BASETIME condition values.

```sql
UPDATE sensor_tag
   SET value = ?
 WHERE name = ?
   AND time = ?;
```

If this statement has both required conditions but fails with `ERR-2190: Invalid
UPDATE/DELETE condition`, check the server version. Older servers do not support
NAME/TIME binds in TAG data UPDATE. Upgrade the server to 8.7.0 or later and use an
8.7.0 SDK when calling a named-marker API.

When reusing a prepared statement, bind new SET, NAME, and TIME values before each
execution. See
[TAG data UPDATE binds](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind).

<a id="column-error-tag-data-update-set"></a>

## TAG data UPDATE SET 대상 컬럼 오류

<a id="limitations-tag"></a>

## TAG 제한사항
