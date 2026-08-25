---
type: docs
title: '11.5.3 Transactions and Connection Pools'
weight: 30
toc: true
---

Use JDBC transactions for relational DML on TRANSACTION tables in Standard Edition.

```java
connection.setAutoCommit(false);
try {
    // TRANSACTION-table DML
    connection.commit();
} catch (SQLException e) {
    connection.rollback();
    throw e;
} finally {
    connection.setAutoCommit(true);
}
```

Do not assume TAG or LOG Append belongs to the same rollback unit. Before returning a pooled
connection, close results and statements, finish the transaction, and restore the configured current
database and session state. Validate a failed connection before reuse.
