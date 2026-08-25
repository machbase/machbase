---
type: docs
title: '11.5.1 PreparedStatement and Types'
weight: 10
toc: true
---

Use `PreparedStatement` to keep SQL structure separate from values and reuse a verified statement.

```java
try (PreparedStatement ps = connection.prepareStatement(
        "INSERT INTO sensor_log VALUES (?, ?, ?)") ) {
    ps.setString(1, "sensor-01");
    ps.setTimestamp(2, Timestamp.from(instant));
    ps.setDouble(3, 25.3);
    ps.executeUpdate();
}
```

- Match Java numeric ranges to SQL types.
- Use `setNull(index, sqlType)` when the target type cannot be inferred.
- Verify DATETIME timezone and precision through a round trip.
- Use `BigDecimal` for exact DECIMAL and NUMERIC values.
- Use one marker style per statement. See [Named bind parameters](/dbms/reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/).

Close statements before returning a connection to a pool.
