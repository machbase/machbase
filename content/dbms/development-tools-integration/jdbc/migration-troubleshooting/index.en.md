---
type: docs
title: '11.5.6 Migration and Troubleshooting'
weight: 60
toc: true
---

When migrating a JDBC application, record the server build, driver version, URL, current database,
table type, SQL, bound Java types, and complete exception chain.

| Symptom | First check |
|---|---|
| Connection rejected | Host, port, authentication mode, and account state |
| Object not found | `CURRENT_DATABASE()`, owner, and table name |
| Bind conversion error | Java type, SQL type, NULL handling, and DATETIME unit |
| Unexpected commit | Table type, auto-commit, and Append path |
| Empty generated keys | Single INSERT support and `RETURN_GENERATED_KEYS` |
| Pool-only failure | Session reset, current database, and unfinished statements |

Reduce failures to one connection and one statement before changing pool or retry settings. Do not
retry syntax, privilege, or type errors automatically.
