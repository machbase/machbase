---
type: docs
title: '16.6.7 Feature Support by Privilege'
weight: 70
toc: true
---

Machbase privileges are divided into **database privileges** and **table privileges** by scope.

## Database Privileges

Database privileges apply to the specified active database. Grant `MOUNT` on
`MACHBASEDB`. Grant `USAGE` and table `SELECT` separately for access to mounted
 databases.

| Privilege | Allowed Operations | Granted by Default |
|------|-------------|:--------:|
| `CONNECT` | Connect to an active database, `USE`, and discover objects | O (MACHBASEDB compatibility) |
| `CREATE` | Create tables, views, indexes, rollups, tablespaces, and retention policies | O |
| `DROP` | Drop tables, views, indexes, rollups, tablespaces, and retention policies | O |
| `ALTER` | Change table structure and execute `ALTER SYSTEM` | X |
| `BACKUP` | Execute `BACKUP DATABASE` | X |
| `MOUNT` | Execute `MOUNT DATABASE` / `UMOUNT DATABASE` | X |
| `USAGE` | Discover objects in mounted databases | X |
| `DDL` | CREATE + DROP (composite privilege) | — |
| `ALL` | Grant CONNECT, CREATE, DROP, ALTER, and BACKUP together | — |

> “Granted by default: O” means compatibility defaults on `MACHBASEDB` for users created with `CREATE USER`.
> Grant privileges on other logical databases separately.

## Table Privileges

Table privileges control DML on a specific table.

| Privilege | Allowed Operations |
|------|-------------|
| `SELECT` | SELECT from the table |
| `INSERT` | INSERT into the table |
| `DELETE` | DELETE from the table |
| `UPDATE` | UPDATE the table |

## GRANT / REVOKE Syntax

```sql
-- Grant database privileges
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT CREATE ON DATABASE factory_a TO app_user;
GRANT BACKUP ON DATABASE factory_a TO backup_user;
GRANT ALL ON DATABASE factory_a TO admin_user;

-- Grant table privileges
GRANT SELECT ON sys.sensor_data TO reader_user;
GRANT INSERT ON sys.sensor_data TO writer_user;

-- Revoke privileges
REVOKE SELECT ON sys.sensor_data FROM reader_user;
REVOKE BACKUP ON DATABASE factory_a FROM backup_user;
```

## Privileges for Common Operations

| Operation | Privilege Scope | Required Privilege |
|------|-------------|---------|
| `CREATE TABLE` | Database | CREATE |
| `DROP TABLE` | Database | DROP |
| `ALTER TABLE` | Database | ALTER |
| `BACKUP DATABASE` | Database | BACKUP |
| `MOUNT DATABASE` | Database | MOUNT |
| Table SELECT | Table | SELECT |
| Table INSERT | Table | INSERT |
| Table UPDATE | Table | UPDATE |
| Table DELETE | Table | DELETE |

## Checking Privileges

```sql
-- List users
SELECT user_name, user_id FROM m$sys_users;

-- Query database privileges
SELECT * FROM m$sys_grant_databases WHERE grantee = 'APP_USER';

-- Query table privileges
SELECT * FROM m$sys_grant_tables WHERE grantee = 'APP_USER';
```

## Detailed Reference

For the complete privilege model and examples, see
[Privilege Management](/dbms/security-access-control/privileges/).
