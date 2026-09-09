---
type: docs
title: '14.2 Account Management'
weight: 20
toc: true
---

Use separate accounts for applications and operations. Reserve `SYS` for user and privilege
administration. For routine queries and loading, use accounts with only the required privileges.

<a id="create-delete-user"></a>

## Create and drop users

```sql
CREATE USER app_user IDENTIFIED BY 'App#Strong123' PASSWORD POLICY HIGH;

SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 WHERE NAME = 'APP_USER';
```

Usernames are stored in uppercase. After creating an account, separately grant `CONNECT`
on the target logical database.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;
```

When changing a password, you can specify the new password and its policy together.

```sql
ALTER USER app_user IDENTIFIED BY 'App#Changed456' PASSWORD POLICY HIGH;
```

Before dropping a user, check active sessions, granted privileges, and owned objects.
A user that owns objects cannot be dropped.

```sql
DROP USER app_user;
```

You cannot drop `SYS` or the account used by your current connection. To continue as another
account in `machsql`, authenticate a new session with `CONNECT user/password;` or reconnect
the client.

<a id="drop-user-active-session"></a>

### Drop a user with active sessions

Dropping a user from another administrative session does not immediately terminate sessions
already authenticated as that user. Existing sessions retain the username and internal ID
saved at login, but the deleted user cannot establish new connections and no longer appears
in `M$SYS_USERS`. Check active sessions and close application connections before dropping the user.

From Machbase 8.7.0, use
[CURRENT_USER and SESSION_USER](../../reference/sql/functions/functions-full/#current-session-user)
to inspect the user context of existing sessions.

<a id="policy-password"></a>

## Password policies

| Policy | Main behavior |
|---|---|
| `NONE` | Default compatibility policy; no strength or expiration restrictions |
| `LOW` | Checks length and character composition |
| `HIGH` | LOW checks plus restrictions on recent password reuse and an expiration period |

LOW and HIGH require at least 10 characters. `ENABLE_CASE_SENSITIVE_PASSWORD` affects case
validation. HIGH sets `VALID_BEFORE` to 90 days after the password is set.

```sql
CREATE USER reader_user
  IDENTIFIED BY 'Reader#Strong123'
  PASSWORD POLICY HIGH;

ALTER USER reader_user
  IDENTIFIED BY 'Reader#Changed456'
  PASSWORD POLICY LOW;
```

Specify a new password together with the policy rather than changing the policy alone.
Check the current policy and expiration date as follows.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 ORDER BY USER_ID;
```

`PWD_POLICY_LEVEL` is `0=NONE`, `1=LOW`, or `2=HIGH`. Use your production secret management
mechanism instead of embedding passwords in applications. For full syntax, see
[USER/AUTH Syntax](/dbms/reference/sql/syntax/user-auth-syntax/#create-drop-alter-user).
