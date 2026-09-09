---
type: docs
title: 'USER/AUTH'
weight: 200
toc: true
---

Syntax for creating/dropping users, changing passwords, granting/revoking
privileges, and managing public-key AUTH KEY authentication.

---

## CREATE USER {#create-drop-alter-user}

```sql
create_user_stmt ::=
    'CREATE USER' user_name 'IDENTIFIED BY' password
    [ 'PASSWORD POLICY' ( 'NONE' | 'LOW' | 'HIGH' ) ]
    [ 'WITH AUTH KEY' '(' auth_key_spec ')' ]

auth_key_spec ::=
    "key='" pem_public_key "',"
    "valid_before='" YYYY-MM-DD "',"
    "comment='" text "'"
```

User names are converted to uppercase when stored.

```sql
-- Create a basic user
CREATE USER app_user IDENTIFIED BY 'App#1234';

-- Specify password policy
CREATE USER ops_user IDENTIFIED BY 'Ops@Strong1' PASSWORD POLICY HIGH;

-- Create with AUTH KEY (public-key authentication)
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkw...(omitted)...==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial key'
);
```

### Password Policies

| Policy | Description |
|------|------|
| `NONE` | No strength restrictions or expiration |
| `LOW` | At least 10 characters, uppercase/lowercase/special characters; no consecutive-number or keyboard patterns |
| `HIGH` | LOW rules + no reuse of the last 24 passwords + automatic expiration after 90 days |

---

## DROP USER

```sql
drop_user_stmt ::= 'DROP USER' user_name
```

The `SYS` user cannot be dropped. Dropping a user that still owns tables raises an error.

Dropping a user from another administrator session does not immediately
terminate existing sessions. New connections fail; existing sessions retain
the user name and ID from login. See
[Account Management](../../../../security-access-control/account/#drop-user-active-session)
for procedures and [User Context Functions](../../functions/functions-full/#current-session-user)
for verification functions.

```sql
DROP USER old_user;
```

---

## ALTER USER

```sql
-- Change password
alter_user_pwd_stmt ::=
    'ALTER USER' user_name 'IDENTIFIED BY' new_password
    [ 'PASSWORD POLICY' ( 'NONE' | 'LOW' | 'HIGH' ) ]
```

Policy-only changes are not allowed. Always specify a new password when
changing the policy.

```sql
-- Change password
ALTER USER app_user IDENTIFIED BY 'NewPass#456';

-- Change password and policy together
ALTER USER app_user IDENTIFIED BY 'NewPass#456' PASSWORD POLICY HIGH;
```

---

## CONNECT

```sql
user_connect_stmt ::= 'CONNECT' user_name '/' password
```

Reconnects as another user without exiting the application.

```sql
CONNECT app_user/App#1234;
```

---

## GRANT / REVOKE {#grant-revoke}

```sql
grant_stmt  ::= 'GRANT'  priv_list 'ON' object_ref 'TO'   user_name
revoke_stmt ::= 'REVOKE' priv_list 'ON' object_ref 'FROM' user_name

priv_list  ::= priv_value ( ',' priv_value )*
object_ref ::= 'DATABASE' database_name
             | 'TABLE' ['database_name.'] owner_name '.' table_name
             | ['database_name.'] owner_name '.' table_name
```

### Table Privileges

```sql
-- Table DML privileges
GRANT SELECT ON sensor_log TO reader;
GRANT SELECT, INSERT ON sys.sensor_log TO writer;
GRANT ALL ON sys.sensor_log TO app_user;

-- Revoke privileges
REVOKE INSERT ON sys.sensor_log FROM writer;
REVOKE ALL ON sys.sensor_log FROM app_user;
```

Table privileges: `SELECT`, `INSERT`, `DELETE`, `UPDATE`, `ALL`

### Database Privileges (Machbase 8.5 and Later)

```sql
-- DDL privileges (CREATE + DROP)
GRANT DDL ON DATABASE factory_a TO deploy_user;

-- Individual DDL privileges
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT CREATE ON DATABASE factory_a TO create_user;
GRANT DROP   ON DATABASE factory_a TO drop_user;
GRANT ALTER  ON DATABASE factory_a TO ops_user;

-- Operational privileges
GRANT BACKUP ON DATABASE factory_a TO backup_user;
GRANT MOUNT  ON DATABASE MACHBASEDB TO mount_user;
GRANT USAGE  ON DATABASE factory_a_backup TO report_user;

-- All database privileges
GRANT ALL ON DATABASE factory_a TO admin_user;

-- Revoke privileges
REVOKE BACKUP ON DATABASE factory_a FROM backup_user;
```

Database privileges: `CONNECT`, `CREATE`, `DROP`, `ALTER`, `BACKUP`, `MOUNT`,
`USAGE`, `DDL` (`CREATE+DROP`), `ALL` (`CONNECT+CREATE+DROP+ALTER+BACKUP`)

### Operations Requiring Database Privileges

| Operation | Required privilege |
|------|------------|
| CREATE/DROP TABLE, VIEW, INDEX, ROLLUP, TABLESPACE, RETENTION | `CREATE`, `DROP`, or `DDL` |
| ALTER SYSTEM | `ALTER` |
| BACKUP DATABASE | `BACKUP` |
| MOUNT/UMOUNT DATABASE | `MOUNT` |

### Default Privileges for New Users

New users have `SELECT`, `INSERT`, `DELETE`, `UPDATE`, `CREATE`, and `DROP`
by default. Grant `ALTER`, `MOUNT`, and `BACKUP` explicitly.

---

## AUTH KEY Management {#auth-key}

An AUTH KEY is a public key registered in Machbase for challenge authentication
instead of password authentication.

### Supported Algorithms

| Algorithm | Supported parameters | Signature schemes |
|---------|-------------|----------|
| ECDSA | P-256, P-384, P-521 | ECDSA |
| RSA | 2048, 3072, 4096 bits | RSA_PKCS1_V15, RSA_PSS |

### Generate Key Files (openssl)

```bash
# Generate an ECDSA P-256 key
openssl ecparam -name prime256v1 -genkey -noout -out app_user.key
openssl ec -in app_user.key -pubout -out app_user.pub
chmod 600 app_user.key

# Generate an RSA 2048-bit key
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -pubout -out app_user_rsa.pub
chmod 600 app_user_rsa.key

# Convert PEM to inline SQL (newlines to \n)
awk '{printf "%s\\n", $0}' app_user.pub
```

### Add an AUTH KEY

```sql
alter_user_add_auth_key_stmt ::=
    'ALTER USER' user_name 'ADD AUTH KEY' '(' auth_key_spec ')'

auth_key_spec ::=
    "key='" pem_public_key "',"
    "valid_before='" YYYY-MM-DD "',"
    "comment='" text "'"
```

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkw...(omitted)...==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='primary key'
);
```

Added keys are immediately registered as active (`ACTIVATED=1`).

### Activate / Deactivate an AUTH KEY

```sql
alter_user_activate_key_stmt   ::= 'ALTER USER' user_name 'ACTIVATE AUTH KEY ID'   key_id
alter_user_deactivate_key_stmt ::= 'ALTER USER' user_name 'DEACTIVATE AUTH KEY ID' key_id
```

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

### Change AUTH KEY Validity

```sql
alter_user_alter_key_stmt ::=
    'ALTER USER' user_name 'ALTER AUTH KEY ID' key_id
    "VALID_BEFORE='" YYYY-MM-DD "'"
```

```sql
ALTER USER app_user ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';
```

### Delete an AUTH KEY

```sql
alter_user_drop_key_stmt ::=
    'ALTER USER' user_name 'DROP AUTH KEY ID' key_id
```

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

### Query AUTH KEYs

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

Main `V$USER_AUTH_KEYS` columns: `KEY_ID`, `USER_NAME`, `KEY_ALGO`, `KEY_PARAM`,
`ACTIVATED`, `VALID_AFTER`, `VALID_BEFORE`, `COMMENT`, `PUBKEY`

---

## Related Documentation

- [User Management Guide](../../../../operations-configuration-recovery/) – Operational procedures and examples
- [System/Session Management Syntax](../system-session-alter-syntax/) – ALTER SYSTEM and ALTER SESSION
