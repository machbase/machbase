---
type: docs
title: '14. Accounts, Privileges, and Access Control'
weight: 140
toc: true
---

Protecting production data requires systematic account, privilege, and access control
configuration. This chapter explains the security model and practical configuration procedures.

## Chapter contents

| Order | Section | Description |
|-----:|------|------|
| 14.1 | [Security Model Overview](./security-model/) | Security architecture, default account, privilege types, AUTH KEY authentication |
| 14.2 | [Account Management](./account/) | Create and drop users, change passwords, password policies (NONE/LOW/HIGH) |
| 14.3 | [Privilege Management](./privileges/) | GRANT/REVOKE, table privileges, database privileges |
| 14.4 | [AUTH KEY Authentication](./authentication-auth-key/) | Public-key challenge authentication, key generation, registration, and management |
| 14.5 | [Access Control](./access-control/) | Remote access and bind IP settings |
| 14.6 | [Security Configuration Checklist](./checklist-configuration/) | Pre-deployment checks for production |

## Four areas of security

**1. Security model** — Understand how accounts, privileges, and authentication work together.
Reserve SYS for administration and give each user only the required privileges.

**2. Account management** — Manage identities that access the database. Create and drop users,
and apply password policies (NONE/LOW/HIGH) and public-key AUTH KEY authentication.

**3. Privilege management** — Restrict the operations an account can perform. Apply least
privilege using table-level DML privileges (SELECT, INSERT, DELETE, UPDATE) and database-level
DDL and operational privileges (CREATE, DROP, ALTER, BACKUP, MOUNT).

**4. Access control** — Control which network paths permit connections. `GRANT_REMOTE_ACCESS`
controls remote access, while `BIND_IP_ADDRESS` selects the listener's network interface.
