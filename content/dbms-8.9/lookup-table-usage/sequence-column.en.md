---
type: docs
title: '9.11 SEQUENCE Columns'
weight: 110
toc: true
---
This section covers configuring and using LOOKUP SEQUENCE columns.


<a id="design-column-lookup-sequence"></a>


## Defining a LOOKUP SEQUENCE Column

A SEQUENCE column generates insertion identifiers through `NEXTVAL`. Because LOOKUP
[requires a PRIMARY KEY](../primary-key-policy/), decide whether the SEQUENCE column or another
column is the primary key. Do not interpret sequence order as event-time order.

## Why Use a SEQUENCE Column?

Use it to distinguish alarms or administrative history rows that share a timestamp. Because LOOKUP
keeps all rows in memory, this example is intended for small administrative histories. Consider LOG
for large event volumes accumulated over long periods.

## Declaring a SEQUENCE Column

SEQUENCE can be specified on `LONG` or `INT64` columns. Set the starting value with the `SEQUENCE`
parameter in PROPERTY. This property is available only for LOOKUP tables.

```sql
CREATE LOOKUP TABLE ch9_sequence (
    seq       LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    sensor_id VARCHAR(40),
    alarm_type VARCHAR(20),
    occurred_at DATETIME,
    message   VARCHAR(200)
);
```

- `SEQUENCE=1`: automatic numbering for seq starts at 1.
- The starting value must be an integer at least 1 and less than 4,294,967,295.
- Declaring the SEQUENCE column as PRIMARY KEY, as above, also guarantees uniqueness.

## Inserting SEQUENCE Values: NEXTVAL()

The server maintains the next number as a counter for each SEQUENCE column. `NEXTVAL()` obtains that
value for insertion; it does not recalculate the table maximum each time.

```sql
-- Insert an automatically incremented value with NEXTVAL()
INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'TEMP-01', 'HIGH', NOW, '온도 초과');

INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'PRESS-02', 'LOW', NOW, '압력 저하');

-- Query
SELECT * FROM ch9_sequence ORDER BY seq;
-- Sorted as seq=1, then seq=2
```

## Specifying Values Directly

Direct input is also allowed for SEQUENCE columns. If the value exceeds the current counter, the
counter advances to `input value + 1`. A value below the current counter does not move it backward.

```sql
-- Specify a value directly; NEXTVAL is optional
INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (100, 'FLOW-03', 'NORMAL', NOW, '정상 복구');

-- The next NEXTVAL() call returns 101
INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'TEMP-01', 'NORMAL', NOW, '온도 정상');
-- seq = 101
```

## Usage Patterns

```sql
-- Query the latest N alarms
SELECT * FROM ch9_sequence ORDER BY seq DESC LIMIT 10;

-- Query alarms after a specified seq
SELECT * FROM ch9_sequence WHERE seq > 500 ORDER BY seq;

-- Acknowledge an alarm with a primary key UPDATE
UPDATE ch9_sequence SET alarm_type = 'ACKNOWLEDGED'
WHERE seq = 101;
```

Clean up the example table as follows.

```sql
DROP TABLE ch9_sequence;
```

## Considerations

- SEQUENCE columns support `LONG` and `INT64`.
- The starting value must be positive (`SEQUENCE=1` or higher) and less than 4,294,967,295.
- The server stores a counter that only increases. Deleting the row with the largest seq does not reuse its number, so gaps can occur.
- Without PRIMARY KEY on the SEQUENCE column, duplicate values can be inserted directly without `NEXTVAL()`. Make it the PRIMARY KEY if uniqueness is required.
