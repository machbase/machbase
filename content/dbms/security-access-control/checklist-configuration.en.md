---
type: docs
title: '14.6 Security Configuration Checklist'
weight: 60
toc: true
---

Check the following before production deployment and during periodic audits.

## Accounts and authentication

- Change the initial `SYS` password immediately after installation using your organization's secret management procedure.
- Create dedicated accounts for each application; do not use `SYS` for routine connections.
- Do not store passwords in source code, documentation, or command history.
- Review unused accounts and accounts nearing expiration.
- For AUTH KEY, assign responsibility for private-key storage, rotation, and revocation.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 ORDER BY USER_ID;

SELECT USER_NAME, KEY_ID, KEY_ALGO, KEY_PARAM, ACTIVATED, VALID_BEFORE
  FROM V$USER_AUTH_KEYS
 ORDER BY USER_NAME, KEY_ID;
```

## Privileges

- Grant only the required `CONNECT` privileges on each logical database.
- Verify that read-only accounts have no write, DDL, or backup privileges.
- Record expiration dates and owners responsible for revoking temporary privileges.
- Recheck privileges after recreating a user or table.

```sql
SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 ORDER BY USER_NAME, DB_NAME, OWNER_NAME, TABLE_NAME;
```

`PRIV` is a bitmask. Validate custom tools that display numeric values as privilege names
against the definitions for the deployed version. For grant and revoke procedures, see
[Privilege Management](../privileges/).

## Network access

- First determine whether remote access is required.
- Restrict `BIND_IP_ADDRESS` to the required IPv4 interface.
- Review source address allowlists in firewalls or security groups.
- Apply configuration changes through maintenance procedures that include restart and connection validation.

```sql
SELECT NAME, VALUE
  FROM V$PROPERTY
 WHERE NAME IN ('GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS');
```

## Post-change evidence

After a security change, record these results:

1. User and expiration date query results.
2. Target user and database/table privilege query results.
3. Successful access from allowed addresses and blocked access from disallowed addresses.
4. For AUTH KEY changes, successful access with the new key and rejected access with the old key.

Do not change the `SYS` password, listener, or firewall on a shared production server for
testing. Verify the recovery path in a separate test environment before approving production changes.
