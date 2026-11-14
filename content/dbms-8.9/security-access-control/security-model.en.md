---
type: docs
title: '14.1 Security Model Overview'
weight: 10
toc: true
---

Machbase's security model combines three layers: **user accounts**, **privileges (GRANT/REVOKE)**,
and **access control (IP/authentication)**.

## Machbase security architecture

```text
Client connection request
        │
        ▼
┌──────────────────────────┐
│ Access control           │  BIND_IP_ADDRESS, GRANT_REMOTE_ACCESS
│ (network layer)          │
└────────┬─────────────────┘
         │ Allowed
         ▼
┌──────────────────────────┐
│ Authentication           │  Password or AUTH KEY (public-key) authentication
│ (user identification)    │
└────────┬─────────────────┘
         │ Authenticated
         ▼
┌──────────────────────────┐
│ Privilege check          │  Check privileges assigned by GRANT/REVOKE
│ (operation authorization)│  Table privileges + database privileges
└──────────────────────────┘
```

A connection request first passes network access control, then user authentication. Finally,
the system checks that the user has the privileges required for the operation.

## Default account: SYS

Machbase automatically creates the `SYS` account during installation. SYS is a superuser that
can perform all database operations, create other users, and grant privileges.

| Item | Value |
|------|------|
| Account name | `SYS` |
| Default password | `MANAGER` |
| Privileges | All privileges (superuser) |
| Can be dropped | No |

> **Required for production:** Change the SYS account's default password (`MANAGER`) immediately
> after installation.
>
> ```sql
> ALTER USER SYS IDENTIFIED BY 'new_password';
> ```

<a id="상세-정본"></a>

## Related documentation

- User lifecycle and password policies: [Account Management](../account/)
- Database/table privileges and GRANT/REVOKE: [Privilege Management](../privileges/)
- Public-key registration and rotation: [AUTH KEY Authentication](../authentication-auth-key/)
- Remote access and listeners: [Access Control](../access-control/)

Account creation, privilege grants, and authentication configuration are separate tasks.
Prepare the accounts and tables in the following example, then reconnect as each account
to verify both allowed and restricted operations.

## Principle of least privilege

Apply these principles in production:

- **Reserve SYS for administration:** Do not use SYS for routine reads or ingestion.
- **Separate accounts by purpose:** Use separate read-only, ingestion, deployment (DDL), and backup accounts.
- **Restrict privileges by table:** Grant only the required DML privileges on tables the account must access.
- **Review regularly:** Remove unnecessary accounts and identify accounts with excessive privileges.

```sql
-- Read-only account
CREATE USER reader IDENTIFIED BY 'Reader#Strong123';
GRANT SELECT ON sys.sensor_log TO reader;

-- Dedicated ingestion account
CREATE USER writer IDENTIFIED BY 'Writer#Strong123';
GRANT SELECT, INSERT ON sys.sensor_log TO writer;

-- Dedicated DDL account (table creation and deletion)
CREATE USER deploy IDENTIFIED BY 'Deploy#Strong123';
GRANT CONNECT ON DATABASE factory_a TO deploy;
GRANT DDL ON DATABASE factory_a TO deploy;
```
