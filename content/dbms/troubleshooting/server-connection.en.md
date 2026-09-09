---
type: docs
title: '15.2 Server and Connection Problems'
weight: 20
toc: true
---

Isolate connection problems in this order: server startup, TCP connection, then user authentication.

<a id="start-server"></a>

## The server does not start

```bash
machadmin -e
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
```

Check these items in order:

1. Whether another process uses the configured port.
2. Whether the Machbase server's OS account can read and write installation, data, and log paths.
3. Whether the file system has sufficient space and inodes.
4. Whether a valid license is installed (`machadmin -f`).
5. Why an earlier process or lock file remains.

Avoid forced termination or lock-file deletion without understanding the cause. If normal
shutdown is impossible, preserve logs and process state, then follow an approved recovery procedure.

<a id="connection"></a>

## A connection cannot be established

First test a local connection on the server host.

```bash
machadmin -e
machsql -s 127.0.0.1 -P 5656 -u app_user
```

If local access succeeds but remote access fails, check:

- The address and port used by the client
- Current `GRANT_REMOTE_ACCESS` and `BIND_IP_ADDRESS` values
- OS and cloud firewalls and the intermediate network path
- Whether `MAX_SESSION_COUNT` has been reached and sessions remain unclosed

```sql
SELECT NAME, VALUE
  FROM V$PROPERTY
 WHERE NAME IN ('GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS', 'MAX_SESSION_COUNT');

SELECT ID, USER_NAME, CLOSED
  FROM V$SESSION
 ORDER BY ID;
```

Listener settings apply at server startup. After changing the configuration file, perform
a maintenance restart and verify both local and remote access. Follow the deployed OS's
official documentation for firewall commands.

<a id="failure-authentication"></a>

## Authentication fails

First check the authentication mode selected for the connection. `AUTH_MODE` is a client
connection option, not a server `V$PROPERTY` setting.

For password authentication, check the username, password policy, and expiration date.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 WHERE NAME = 'APP_USER';
```

For AUTH KEY authentication, inspect registered keys and client options.

```sql
SELECT KEY_ID, USER_NAME, KEY_ALGO, KEY_PARAM, ACTIVATED, VALID_BEFORE
  FROM V$USER_AUTH_KEYS
 WHERE USER_NAME = 'APP_USER'
 ORDER BY KEY_ID;
```

```bash
machsql -s 127.0.0.1 -P 5656 -u app_user \
  -c "AUTH_MODE=CHALLENGE" \
  -K /secure/path/app_user.key
```

Verify that the private-key file exists, is readable by the client process, matches the
server's public key, and is active and valid. Do not use unsupported syntax such as account
unlocking or `CREATE AUTH KEY`. Follow
[AUTH KEY Authentication](/dbms/security-access-control/authentication-auth-key/) for registration
and rotation.
