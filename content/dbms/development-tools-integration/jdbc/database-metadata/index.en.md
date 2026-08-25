---
type: docs
title: '11.5.4 DatabaseMetaData'
weight: 40
toc: true
---

Use JDBC metadata for driver capabilities and table-schema facts.

```java
DatabaseMetaData meta = connection.getMetaData();
boolean generatedKeys = meta.supportsGetGeneratedKeys();

try (ResultSet keys = meta.getPrimaryKeys(null, "SYS", "ORDERS")) {
    while (keys.next()) {
        String column = keys.getString("COLUMN_NAME");
        short sequence = keys.getShort("KEY_SEQ");
    }
}
```

Result-column nullability and key flags can be unknown for expressions, joins, views, and aggregate
results. Use catalog metadata when the application needs the declared table schema. See
[SDK feature support](../../sdk-support-scope/) for cross-SDK differences.
