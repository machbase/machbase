---
type: docs
title: 'VIEW'
weight: 140
toc: true
---

A VIEW stores a SELECT definition as a named logical object for reuse. It
does not store data separately; queries expand and execute its stored SQL.

## CREATE VIEW

```sql
CREATE VIEW view_name AS
SELECT ...
FROM ...;
```

```sql
CREATE VIEW view_name (col1, col2, ...) AS
SELECT ...
FROM ...;
```

```sql
CREATE OR REPLACE VIEW view_name AS
SELECT ...
FROM ...;
```

Standard Edition allows a nonrecursive CTE before the SELECT in a VIEW definition.

```sql
CREATE VIEW view_name AS
WITH cte_name AS (
    SELECT ...
    FROM ...
)
SELECT ...
FROM cte_name;
```

- `CREATE OR REPLACE VIEW` replaces an existing VIEW definition. If the target
  is another object type, it raises an error.
- An explicit column list defines the official VIEW column names; otherwise,
  aliases or source column names apply.
- `view_name` can be schema-qualified as `db.user.view_name`.

### Basic Example

```sql
CREATE LOOKUP TABLE customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR(20),
    city VARCHAR(20),
    amount INTEGER
);

CREATE VIEW v_customer AS
SELECT id, name, city, amount
FROM customer;

SELECT name, city
FROM v_customer
WHERE id = 100;
```

### Explicit Column Names

```sql
CREATE VIEW v_customer_short (cust_id, cust_name) AS
SELECT id, name
FROM customer;
```

### Replace a VIEW Definition

```sql
CREATE OR REPLACE VIEW v_customer_amount AS
SELECT id, amount * 10 AS amount
FROM customer
WHERE id <= 10;
```

### VIEW with a CTE

```sql
CREATE VIEW v_customer_city_summary AS
WITH city_summary AS (
    SELECT city, COUNT(*) AS customer_count, SUM(amount) AS total_amount
    FROM customer
    GROUP BY city
)
SELECT city, customer_count, total_amount
FROM city_summary;
```

VIEW definitions cannot contain bind parameters (`?`). Put conditions that
vary per execution in the SELECT querying the VIEW.

<a id="view-user-context"></a>

## VIEW User Context

Since Machbase 8.7.0, `CURRENT_*` and `SESSION_*` functions inside VIEWs
distinguish definers from callers. Here, `VIEW_OWNER` creates the VIEW
and `VIEW_CALLER` queries it with granted privileges.

```sql
CONNECT sys/manager;
CREATE USER view_owner IDENTIFIED BY 'VIEW_OWNER';
CREATE USER view_caller IDENTIFIED BY 'VIEW_CALLER';

CONNECT view_owner/VIEW_OWNER;
CREATE LOOKUP TABLE user_context_source (id INTEGER PRIMARY KEY);
INSERT INTO user_context_source VALUES (1);

CREATE VIEW v_user_context AS
SELECT CURRENT_USER() AS current_name,
       SESSION_USER() AS session_name,
       CURRENT_USER_ID() AS current_id,
       SESSION_USER_ID() AS session_id
  FROM user_context_source;

CONNECT sys/manager;
GRANT SELECT ON view_owner.v_user_context TO view_caller;

CONNECT view_caller/VIEW_CALLER;
SELECT current_name,
       session_name,
       CASE WHEN current_id <> session_id THEN 'DIFF' ELSE 'SAME' END AS id_context
  FROM view_owner.v_user_context;
```

```text
CURRENT_NAME  SESSION_NAME  ID_CONTEXT
VIEW_OWNER    VIEW_CALLER   DIFF
```

Inside a VIEW, `CURRENT_*` returns the VIEW owner and `SESSION_*` returns
the connected caller. In ordinary SQL, both return the same user. See
[User Context Functions](../../functions/functions-full/#current-session-user) for details.

```sql
CONNECT view_owner/VIEW_OWNER;
DROP VIEW v_user_context;
DROP TABLE user_context_source;

CONNECT sys/manager;
DROP USER view_caller;
DROP USER view_owner;
```

## DROP VIEW

```sql
DROP VIEW view_name;
DROP VIEW IF EXISTS view_name;
```

- `DROP VIEW IF EXISTS` succeeds without error when the target does not exist.
- Deletion is blocked if another VIEW references the target.
- `DROP TABLE view_name` cannot delete a VIEW.

## Inspect Metadata

```sql
SHOW VIEWS;
DESC view_name;

SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS
WHERE VIEW_NAME = 'V_CUSTOMER';
```

- VIEWs have `TYPE = 7` in `M$SYS_TABLES`.

## Supported VIEW Forms

| Form | Supported |
|------|-----------|
| Simple projection and predicates | O |
| Expressions, functions, constants, CASE | O |
| JOIN | O |
| Subqueries | O |
| Nested VIEWs | O |
| GROUP BY, HAVING | O |
| DISTINCT | O |
| UNION ALL | O |

## TAG / BINARY Column Example

Use `extract_*()` functions to interpret TAG BINARY columns and expose
logical columns.

```sql
CREATE TAG TABLE dam (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    frame BINARY(16)
);

CREATE VIEW damdata AS
SELECT name,
       time,
       extract_bit(frame, 0)                         AS bit0,
       extract_ulong(frame, 0, 16)                   AS u16,
       extract_float(frame, 0)                       AS f32,
       extract_scaled_double(frame, 0, 12, 0, 0.5, 0.5) AS sd12
FROM dam;

SELECT name, time, bit0, u16, f32, sd12
FROM damdata
WHERE name = 'main'
  AND time >= TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND time <  TO_DATE('2024-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time;
```

## Limitations

- VIEW definition SQL (the SELECT body) supports up to 256KB.
- VIEWs do not store data; performance depends on source queries and optimizer decisions.
- DISTINCT and predicates on computed columns may require full scans; check EXPLAIN.
- Recursive VIEWs that reference themselves are unsupported.

## Related Documentation

- [SELECT Syntax](../select-syntax/) — Use VIEWs in FROM
- [WITH / CTE Syntax](../cte-syntax/) — Define VIEWs containing CTEs
