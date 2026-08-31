---
type: docs
title: '17.8.8 sql-generation-rules'
weight: 80
toc: true
---

Apply this verification sequence before generating SQL. The
[SQL reference](/dbms/reference/sql/) owns the actual grammar.

1. Identify server version and Edition.
2. Confirm database, owner, table type, and `DESC` output.
3. Verify the statement in the [SQL syntax dictionary](/dbms/reference/sql/syntax-dictionary-sql/).
4. Verify arguments and return types in the [Function dictionary](/dbms/reference/sql/dictionary/).
5. Check [Support scope](/dbms/reference/support-scope-constraints/).

Do not borrow unverified keywords, functions, hints, or transaction behavior from
another DBMS. Parameters replace values, not identifiers. Preview the target of range,
DELETE, and UPDATE statements, use `ORDER BY` when order matters, and include result
verification and cleanup in mutation examples.
