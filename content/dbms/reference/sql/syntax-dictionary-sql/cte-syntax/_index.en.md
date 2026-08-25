---
type: docs
title: '17.1.1.2 WITH / CTE'
weight: 20
toc: true
---

Standard Edition supports non-recursive common table expressions for structuring a query.

```text
WITH cte_name [(column_name [, ...])] AS (select_statement)
   [, cte_name AS (select_statement) ...]
select_statement
```

```sql
WITH recent_event AS (
    SELECT device_id, event_time, value
      FROM event_log
     WHERE event_time >= :from_time
)
SELECT device_id, AVG(value)
  FROM recent_event
 GROUP BY device_id;
```

CTE names are visible to the following query and later CTEs in the same `WITH` clause. Recursive CTE
syntax is not supported. A CTE improves structure but does not guarantee materialization or faster
execution; check filter pushdown and intermediate result size with `EXPLAIN`.
