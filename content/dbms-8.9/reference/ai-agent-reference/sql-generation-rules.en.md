---
type: docs
title: '16.8.8 sql-generation-rules'
weight: 80
toc: true
---

Apply the following verification sequence when generating SQL. The
[SQL Reference](/dbms-8.9/reference/sql/) defines the actual syntax.

## Before Generation

1. Check the server version and edition.
2. Check the target database, owner, table type, and `DESC` output.
3. Verify the statement form in the [SQL Syntax Dictionary](/dbms-8.9/reference/sql/syntax/).
4. Verify arguments and return types in the [Function Dictionary](/dbms-8.9/reference/sql/functions/).
5. Check edition and table constraints in [Support Scope](/dbms-8.9/reference/support-scope-constraints/).

## Generation Rules

- Do not assume keywords, functions, hints, or transaction behavior from other DBMSs apply.
- Do not replace identifiers with parameter markers.
- For time/distance ranges, DELETE, and UPDATE, provide a query to inspect expected target rows first.
- Specify `ORDER BY` when result order matters.
- Include result checks and cleanup in modification examples.

If an error occurs, use the complete error and schema with the
[Troubleshooting](/dbms-8.9/troubleshooting/) procedure rather than arbitrarily changing syntax.
