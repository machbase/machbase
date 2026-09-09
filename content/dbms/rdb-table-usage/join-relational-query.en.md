---
type: docs
title: '8.11 JOIN and Relational Query Design'
weight: 110
toc: true
---

If adding JOIN changes order counts, first check relationship cardinality. INNER JOIN excludes
unmatched rows, while multiple matches multiply results. Error-free SQL does not guarantee correct
business counts.

<a id="join-design-rdb"></a>

<a id="transaction과-lookup을-연결합니다"></a>

## TRANSACTION–LOOKUP Joins

```sql
CREATE TRANSACTION TABLE ch8_join_order (
    order_id LONG PRIMARY KEY,
    item_id  LONG,
    qty      INTEGER
);
CREATE LOOKUP TABLE ch8_join_product (id LONG PRIMARY KEY, name VARCHAR(64));
CREATE TRANSACTION TABLE ch8_join_payment (order_id LONG PRIMARY KEY, status VARCHAR(16));

INSERT INTO ch8_join_order VALUES (1, 42, 2);
INSERT INTO ch8_join_order VALUES (2, 99, 1);
INSERT INTO ch8_join_product VALUES (42, 'Pump');
INSERT INTO ch8_join_payment VALUES (1, 'PAID');

SELECT o.order_id, p.name, o.qty
  FROM ch8_join_order o JOIN ch8_join_product p ON o.item_id = p.id
 ORDER BY o.order_id;

SELECT o.order_id, p.name, o.qty
  FROM ch8_join_order o LEFT JOIN ch8_join_product p ON o.item_id = p.id
 ORDER BY o.order_id;
```

INNER JOIN returns only order 1; LEFT JOIN returns orders 1 and 2. Order 2's product name is NULL. A
foreign key does not block inserting an order for missing product 99, so design required reference
validation separately.

A common mistake is putting a right-side predicate in WHERE after LEFT JOIN. Adding
`WHERE p.name = 'Pump'`, for example, excludes NULL rows. Distinguish predicates for finding matches
from predicates filtering final results.

<a id="transaction끼리도-키의-고유성을-확인합니다"></a>

## Joins Between TRANSACTION Tables

```sql
SELECT o.order_id, o.qty, p.status
  FROM ch8_join_order o
  JOIN ch8_join_payment p ON o.order_id = p.order_id
 ORDER BY o.order_id;
```

The query returns one row, (1, 2, PAID). Multiple payment-history rows per order would produce
multiple results. Check relationships and aggregation granularity to avoid duplicate totals when
summing order amounts after a join.

<a id="tag의-근접-시간-조인은-한-행을-고르는-기능이-아닙니다"></a>

## TAG Joins by Nearby Time

This example joins every measurement within 5 seconds before or after an alarm.

```sql
CREATE TRANSACTION TABLE ch8_join_alarm (
    alarm_id LONG PRIMARY KEY,
    sensor   VARCHAR(32),
    occurred DATETIME
);
CREATE TAG TABLE ch8_join_sensor (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

INSERT INTO ch8_join_alarm VALUES (
    1, 'TEMP-01', TO_DATE('2026-01-01 10:00:05', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO ch8_join_sensor VALUES (
    'TEMP-01', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10);
INSERT INTO ch8_join_sensor VALUES (
    'TEMP-01', TO_DATE('2026-01-01 10:00:10', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch8_join_sensor VALUES (
    'TEMP-01', TO_DATE('2026-01-01 10:00:11', 'YYYY-MM-DD HH24:MI:SS'), 30);

SELECT a.alarm_id, s.time, s.value
  FROM ch8_join_alarm a JOIN ch8_join_sensor s ON a.sensor = s.name
 WHERE s.time >= a.occurred - 5s
   AND s.time <= a.occurred + 5s
 ORDER BY a.alarm_id, s.time;
```

Alarm 1 joins to two rows with values 10 and 20. Both endpoints are included; value 30 is excluded.
This query does not select only the nearest measurement or an exact timestamp match. If one value is
required, separately define criteria such as latest preceding value or shortest distance, plus
tie-breaking rules.

<a id="타입과-읽기-범위를-먼저-맞춥니다"></a>

## Join Design Criteria

Match join-key types and formats, restrict time ranges, then inspect the execution plan. Return only
required columns. Compare access paths before adding functions or conversions to join keys. Do not
assume join order or algorithms match another RDBMS.

Permitted mixed joins do not mean other table types share the same transaction snapshot as
TRANSACTION. Joining current LOOKUP descriptions also does not reproduce historical descriptions.

```sql
DROP TABLE ch8_join_sensor;
DROP TABLE ch8_join_alarm;
DROP TABLE ch8_join_payment;
DROP TABLE ch8_join_product;
DROP TABLE ch8_join_order;
```

If result counts differ, first compare counts before the join and matching-row counts per key. These
two checks clarify how the query needs to change.
