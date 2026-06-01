---
title : 'User Management'
type: docs
weight: 60
---

# Index

* [CREATE USER](#create-user)
* [DROP USER](#drop-user)
* [ALTER USER](#alter-user)
* [Generate AUTH KEY Files](#generate-auth-key-files)
* [Create a User with AUTH KEY](#create-a-user-with-auth-key)
* [Manage AUTH KEY](#manage-auth-key)
* [Query AUTH KEY Metadata](#query-auth-key-metadata)
* [CONNECT](#connect)
* [GRANT/REVOKE](#grantrevoke)
* [Managing User Example](#managing-user-example)


## CREATE USER

**create_user_stmt:**

![create_user_stmt](/images/sql/user/create_user_stmt.png)

```sql
create_user_stmt ::= 'CREATE USER' user_name 'IDENTIFIED BY' password
```

The syntax for creating a user is:

```sql
-- Example
CREATE USER new_user IDENTIFIED BY password
```

User names are converted to uppercase when they are created. For example,
`CREATE USER app_user ...` is stored and displayed as `APP_USER` in metadata tables and
`V$` views. Later connection and privilege statements refer to the same user name.


## DROP USER

**drop_user_stmt:**

![drop_user_stmt](/images/sql/user/drop_user_stmt.png)

```sql
drop_user_stmt ::= 'DROP USER' user_name
```

The syntax for deleting a user is as follows. The SYS user can not be deleted, and if there is a table already created by the user to be deleted, an error is displayed.

```sql
-- Example
DROP USER old_user
```


## ALTER USER

**alter_user_pwd_stmt:**

![alter_user_pwd_stmt](/images/sql/user/alter_user_pwd_stmt.png)

```sql
alter_user_pwd_stmt ::= 'ALTER USER' user_name 'IDENTIFIED BY' password
```

The user can change the password through the following syntax.

```sql
-- Example
ALTER USER user1 IDENTIFIED BY password
```

## Generate AUTH KEY Files

> **Note**: The following behavior is supported from Machbase 8.5 or later.

AUTH KEY authentication uses a client-side private key file and a public key registered
to the Machbase user. In normal operation, generate the key pair with `openssl`, keep the
private key on the client host, and register only the public key in Machbase.

Supported algorithms and key sizes are as follows.

| Public key algorithm | Supported key parameters | Supported signature scheme | Hash |
| --- | --- | --- | --- |
| ECDSA | P-256, P-384, P-521 | `ECDSA` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PKCS1_V15` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PSS` | SHA-256 |

If `AUTH_SIG_SCHEME` is omitted, Machbase uses the default scheme for the key algorithm.

- ECDSA key: `ECDSA`
- RSA key: `RSA_PKCS1_V15`

To use RSA-PSS, specify `AUTH_SIG_SCHEME=RSA_PSS` in the client connection options.
Authentication fails if the registered public key type does not match the requested
signature scheme.

ECDSA P-256 key example:

```bash
openssl ecparam -name prime256v1 -genkey -noout -out app_user_ecdsa.key
openssl ec -in app_user_ecdsa.key -pubout -out app_user_ecdsa.pub
chmod 600 app_user_ecdsa.key
```

ECDSA P-384 and P-521 key examples:

```bash
openssl ecparam -name secp384r1 -genkey -noout -out app_user_ecdsa_p384.key
openssl ec -in app_user_ecdsa_p384.key -pubout -out app_user_ecdsa_p384.pub

openssl ecparam -name secp521r1 -genkey -noout -out app_user_ecdsa_p521.key
openssl ec -in app_user_ecdsa_p521.key -pubout -out app_user_ecdsa_p521.pub
```

RSA 2048-bit key example:

```bash
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -pubout -out app_user_rsa.pub
chmod 600 app_user_rsa.key
```

To use a 3072-bit or 4096-bit RSA key, pass `3072` or `4096` as the last argument of
`openssl genrsa`.

To embed the public key in SQL, convert the PEM file into a single SQL string with
escaped line breaks.

```bash
awk '{printf "%s\\n", $0}' app_user_ecdsa.pub
```

Use the command output as the `key` value in `CREATE USER ... WITH AUTH KEY` or
`ALTER USER ... ADD AUTH KEY`.

The following example creates a registration SQL file from the generated public key.

```bash
KEY_ESCAPED=$(awk '{printf "%s\\n", $0}' app_user_ecdsa.pub)

cat > add_app_user_key.sql <<EOF
ALTER USER app_user ADD AUTH KEY (
    key='${KEY_ESCAPED}',
    valid_before='2047-12-31',
    comment='openssl generated ecdsa key'
);
EOF
```

## Create a User with AUTH KEY

> **Note**: The following behavior is supported from Machbase 8.5 or later.

Machbase can register an AUTH KEY for public-key challenge authentication together with password
authentication.

```sql
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial key'
);
```

Notes:

- `key` must contain a PEM public key.
- In SQL text, PEM line breaks can be written as `\n`.
- `valid_before` uses the `YYYY-MM-DD` format.
- `valid_before` does not accept a datetime value with a time portion such as
  `YYYY-MM-DD HH24:MI:SS`.
- `comment` is optional.
- The first key created by `CREATE USER ... WITH AUTH KEY` is registered as active
  (`ACTIVATED=1`).
- A user may own both a password and one or more AUTH KEY entries. The actual
  authentication method is chosen by the client's `AUTH_MODE`, and there is no automatic
  fallback from one method to the other on failure.

## Manage AUTH KEY

### Add AUTH KEY

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAqO+tddiAQzsT8iajPy5QJPamIlyq2zB01wgHSTs3OOrvw0uKoFQD\ncqKaDzRya73LETXIEev3nwhGCnG4SjedMHj3EH9/rRJphFtv/dzw0OHum/UhVulR\nIXUYzrTbKPTQ+qyjS8UXTteMncf9OOh4AQyS4+iJW+U344fxymR8USRgZ25N9jhf\n2gkKnn5YSPZHf8ZHQGeA7OXANBwPmH5dQwfqghXRa7Nk1hmkIAnQQXCBJW/Lin+x\nwQfqv8DVwNaiziz77voPwaeD5akq1JYWvcPlOnh+NN3tpu5gudke/t/In4NFJ3W9\n4unVcYIfxcdDSoht3AMObGmuDazOjQJFGQIDAQAB\n-----END RSA PUBLIC KEY-----\n',
    valid_before='2048-01-31',
    comment='rollover candidate'
);
```

An added key is created as active immediately (`ACTIVATED=1`). During key rollover, a user
can have multiple active AUTH KEY entries.

### Activate / Deactivate AUTH KEY

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

- A deactivated key cannot be used for challenge authentication.
- A user can own multiple AUTH KEY entries.

### Change AUTH KEY Expiration

```sql
ALTER USER app_user ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';
```

- A key past `VALID_BEFORE` cannot be used for authentication.
- The input format is `YYYY-MM-DD`, and a datetime value with a time portion is not
  accepted.

### Drop AUTH KEY

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

- A dropped key cannot be used for authentication immediately.
- When a user is dropped, the user's AUTH KEY metadata is also removed.

## Query AUTH KEY Metadata

Registered AUTH KEY metadata can be queried from `V$USER_AUTH_KEYS`.

Major columns:

- `KEY_ID`: AUTH KEY identifier
- `USER_NAME`: owner of the AUTH KEY
- `KEY_ALGO`: key algorithm (`RSA`, `ECDSA`)
- `KEY_PARAM`: key parameter
  - RSA key: bit length such as `2048`
  - EC key: curve name such as `P-256`, `P-384`, `P-521`
- `ACTIVATED`: whether the key is active
- `VALID_AFTER`, `VALID_BEFORE`: validity period
- `COMMENT`: user note
- `PUBKEY`: PEM public key body

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name='APP_USER'
 ORDER BY key_id;
```

To inspect the public key body, query the `PUBKEY` column.

```sql
SELECT key_id, user_name, pubkey
  FROM V$USER_AUTH_KEYS
 WHERE user_name='APP_USER'
 ORDER BY key_id;
```


## CONNECT

**user_connect_stmt:**

![user_connect_stmt](/images/sql/user/user_connect_stmt.png)

```sql
user_connect_stmt: 'CONNECT' user_name '/' password
```

The user can reconnect to another user via the following syntax without terminating the application.

```sql
-- Example
CONNECT user1/password;
```


## GRANT/REVOKE

![grant_stmt](/images/sql/user/grant_stmt.png)

![revoke_stmt](/images/sql/user/revoke_stmt.png)

![priv_value](/images/sql/user/priv_value.png)

Use `GRANT` to give privileges to a user and `REVOKE` to remove previously granted privileges.

Basic examples:

```sql
-- Grant user1 SELECT privileges on mytable
GRANT SELECT ON mytable TO user1;
 
-- Grant user1 all privileges on mytable
GRANT ALL ON mytable TO user1;
```

```sql
-- Revoke UPDATE privilege on mytable granted to user1
REVOKE UPDATE ON mytable FROM user1;
 
-- Revoke all privileges on mytable granted to user1
REVOKE ALL ON mytable FROM user1;
```

### Table Privileges

Use the following target formats when you grant privileges on a table:

- `table`
- `user.table`
- `db.user.table`

Available table privileges:

- `SELECT`
- `INSERT`
- `DELETE`
- `UPDATE`
- `ALL`

Examples:

```sql
GRANT SELECT ON sensor_log TO reader;
GRANT SELECT, INSERT ON sys.sensor_log TO writer;
REVOKE INSERT ON sys.sensor_log FROM writer;
GRANT ALL ON machbasedb.sys.sensor_log TO app_user;
```

### Machbase 8.5+: Database Privileges

> **Note**: The following behavior is supported from Machbase 8.5 or later.

From Machbase 8.5, you can grant database-scoped privileges by using `MACHBASEDB` as the target.

```sql
GRANT CREATE ON machbasedb TO ddl_user;
GRANT DROP ON machbasedb TO ddl_user;
GRANT ALTER ON machbasedb TO ops_user;
GRANT BACKUP ON machbasedb TO backup_user;
GRANT MOUNT ON machbasedb TO mount_user;
GRANT DDL ON machbasedb TO deploy_user;
GRANT ALL ON machbasedb TO admin_user;
```

Available database-scoped privileges:

- `CREATE`
- `DROP`
- `ALTER`
- `MOUNT`
- `BACKUP`
- `DDL`
- `ALL`

Here, `DDL` means the combined `CREATE + DROP` privilege.

### Meaning of `ALL`

> **Note**: The following behavior is supported from Machbase 8.5 or later.

`ALL` does not always mean the same thing. Its meaning depends on the target.

- `GRANT ALL ON machbasedb TO user1`
  - Grants the full set of database-scoped privileges.
- `GRANT ALL ON sys.table1 TO user1`
  - Grants the full set of DML privileges on that table.

In other words, `ALL` on `MACHBASEDB` and `ALL` on a table use the same keyword, but they serve different purposes.

### DML Privileges Cannot Be Granted Directly on `MACHBASEDB`

> **Note**: The following behavior is supported from Machbase 8.5 or later.

You cannot directly grant `SELECT`, `INSERT`, `DELETE`, or `UPDATE` on the database name `MACHBASEDB`.

```sql
GRANT SELECT ON machbasedb TO user1;
GRANT INSERT ON machbasedb TO user1;
REVOKE DELETE ON machbasedb FROM user1;
REVOKE UPDATE ON machbasedb FROM user1;
```

These statements fail with:

```sql
[ERR-02186: Invalid database name.]
```

To grant read or write access, specify a table instead.

```sql
GRANT SELECT ON sys.sensor_log TO user1;
GRANT INSERT ON sys.sensor_log TO user1;
```

### Use `MACHBASEDB` as the Database Target

> **Note**: The following behavior is supported from Machbase 8.5 or later.

Use `MACHBASEDB` when you grant database-scoped privileges.

```sql
GRANT BACKUP ON machbasedb TO backup_user;
REVOKE BACKUP ON machbasedb FROM backup_user;
```

If you use an invalid database name, the statement fails.

```sql
GRANT BACKUP ON typo TO backup_user;
```

```sql
[ERR-02186: Invalid database name.]
```

### Operations That Require Database Privileges

> **Note**: The following behavior is supported from Machbase 8.5 or later.

The following operations require database-scoped privileges on `MACHBASEDB`, not table-level privileges.

- `CREATE TABLE`, `DROP TABLE`
- `CREATE VIEW`, `DROP VIEW`
- `CREATE INDEX`, `DROP INDEX`
- `CREATE ROLLUP`, `DROP ROLLUP`
- `CREATE TABLESPACE`, `DROP TABLESPACE`
- `CREATE RETENTION`, `DROP RETENTION`
- `ALTER SYSTEM`
- `BACKUP DATABASE`
- `MOUNT DATABASE`, `UNMOUNT DATABASE`

For example, if a normal user needs to run `CREATE VIEW`, grant `CREATE` on `MACHBASEDB`.

```sql
GRANT CREATE ON machbasedb TO user1;
```

### Default Privileges for a New User

When a new user is created, the following privileges are granted by default.

- `SELECT`
- `INSERT`
- `DELETE`
- `UPDATE`
- `CREATE`
- `DROP`

The following privileges are not included by default and must be granted explicitly when needed.

- `ALTER`
- `MOUNT`
- `BACKUP`

### Privileges Do Not Override Table-Type Restrictions

Even with privileges, the built-in restrictions of each table type still apply.

- `LOG` and `TAG` tables do not support `UPDATE`.
- `VOLATILE` and `LOOKUP` tables support all DML operations, but `WHERE` clauses for query, update, and delete operations must be based on the primary key.

In other words, granting privileges does not enable unsupported DML behavior.

### Common Grant Examples

```sql
-- Allow read-only access to a specific table
GRANT SELECT ON sys.sensor_log TO reader;

-- Allow read and insert on a specific table
GRANT SELECT, INSERT ON sys.sensor_log TO writer;

-- Allow only DDL operations for a normal user
GRANT DDL ON machbasedb TO deploy_user;

-- Allow ALTER SYSTEM
GRANT ALTER ON machbasedb TO ops_user;

-- Allow backup
GRANT BACKUP ON machbasedb TO backup_user;

-- Allow mount and unmount
GRANT MOUNT ON machbasedb TO mount_user;
```


## Managing User Example

Here is an example of the above query and its results.

```
############################################
## Connect with SYS account
############################################
Mach> create user demo identified by 'demo';
Created successfully.
 
Mach> drop user demo;
Dropped successfully.
 
Mach> create user demo1 identified by 'demo1';
Created successfully.
 
Mach> create user demo2 identified by 'demo2';
Created successfully.
 
Mach> alter user demo2 identified by 'demo22';
Altered successfully.
 
Mach> create table demo1_table (id integer);
Created successfully.
 
Mach> create bitmap index demo1_table_index1 on demo1_table(id);
Created successfully.
 
Mach> insert into demo1_table values(99991);
1 row(s) inserted.
 
Mach> insert into demo1_table values(99992);
1 row(s) inserted.
 
Mach> insert into demo1_table values(99993);
1 row(s) inserted.
 
Mach> select * from demo1_table;
ID
--------------
99993
99992
99991
[3] row(s) selected.
 
#Error: Can't drop the user connected.
Mach> drop user SYS;
[ERR-02083 : Drop user error. You cannot drop yourself(SYS).]
 
############################################
## Connect DEMO1
############################################
Mach> connect demo1/demo1;
Connected successfully.
 
#Error: can't alter other's account password
Mach> alter user demo2 identified by 'demo22';
[ERR-02085 : ALTER user error. The user(DEMO2) does not have ALTER privileges.]
 
Mach> alter user demo1 identified by demo11;
Altered successfully.
 
#Error: wrong password
Mach> connect demo1/demo11234;
[ERR-02081 : User authentication error. Invalid password (DEMO11234).]
 
## Correct password
Mach> connect demo1/demo11;
Connected successfully.
 
Mach> create table demo1_table (id integer);
Created successfully.
 
Mach> create bitmap index demo1_table_index1 on demo1_table(id);
Created successfully.
 
Mach> insert into demo1_table values(1);
1 row(s) inserted.
 
Mach> insert into demo1_table values(2);
1 row(s) inserted.
 
Mach> insert into demo1_table values(3);
1 row(s) inserted.
 
Mach> select * from demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.
 
Mach> select * from demo1.demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.
 
############################################
## Connect SYS again
############################################
Mach> connect SYS/MANAGER;
Connected successfully.
 
Mach> select * from demo1_table;
ID
--------------
99993
99992
99991
[3] row(s) selected.
 
Mach> select * from demo1.demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.
 
Mach> drop user demo1;
[ERR-02084 : DROP user error. The user's tables still exist. Drop those tables first.]
 
Mach> connect demo1/demo11;
Connected successfully.
 
Mach> drop table demo1_table;
Dropped successfully.
 
Mach> connect SYS/MANAGER;
Connected successfully.
 
Mach> drop user demo1;
Dropped successfully.
```
