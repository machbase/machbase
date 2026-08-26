---
type: docs
title: '17.1.1.14 VIEW syntax'
weight: 140
toc: true
---

<a id="view-user-context"></a>

## VIEW user context

Starting with Machbase 8.7.0, a VIEW can distinguish its definer from its connected caller with the
`CURRENT_*` and `SESSION_*` functions.

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

Inside the VIEW, `CURRENT_*` returns the VIEW owner and `SESSION_*` returns the connected caller.
For ordinary SQL, both families return the same user. See
[User context functions](../../dictionary/functions-full/#current-session-user).

```sql
CONNECT view_owner/VIEW_OWNER;
DROP VIEW v_user_context;
DROP TABLE user_context_source;

CONNECT sys/manager;
DROP USER view_caller;
DROP USER view_owner;
```
