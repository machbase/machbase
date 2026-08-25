---
type: docs
title: '11.5.2 ResultSet, Statement, and LOB'
weight: 20
toc: true
---

Consume each `ResultSet` before closing its statement or returning the connection.

```java
try (Statement st = connection.createStatement();
     ResultSet rs = st.executeQuery(
         "SELECT event_time, message FROM app_log LIMIT 100")) {
    while (rs.next()) {
        Timestamp time = rs.getTimestamp(1);
        String message = rs.getString(2);
    }
}
```

Check `wasNull()` when a primitive getter can represent both SQL NULL and a zero value. Bound fetch
size and result range for large queries. Read large text or binary values with the JDBC accessor
documented by the driver and close streams before advancing or closing the result.
