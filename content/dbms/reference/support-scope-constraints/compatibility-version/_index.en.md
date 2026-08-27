---
type: docs
title: '17.6.10 버전 및 호환성'
weight: 100
toc: true
---

## Features added in Machbase 8.7.0

- `CREATE INDEX IF NOT EXISTS` succeeds without changing an existing index with the same name in the
  same database and owner namespace. Older servers do not support this syntax. See
  [INDEX syntax](/dbms/reference/sql/syntax-dictionary-sql/index-syntax/#create-index-if-not-exists).
- Standard Edition accepts positional and named bind parameters for NAME and BASETIME
  values in TAG data UPDATE predicates. Older servers can reject the same prepared
  UPDATE with `ERR-2190`. See
  [TAG data UPDATE binds](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind).

<a id="removed-features-870"></a>

## Features removed in Machbase 8.7.0

HTTP/REST, WebAdmin, STREAM, Result Cache, and the legacy MachCLI API are not available in
Machbase 8.7.0. Remove their configuration and migrate dependent applications before upgrading.
