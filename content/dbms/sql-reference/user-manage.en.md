---
title : 'User Management'
type: docs
weight: 60
---

# Index

* [CREATE USER](#create-user)
* [DROP USER](#drop-user)
* [ALTER USER](#alter-user)
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
