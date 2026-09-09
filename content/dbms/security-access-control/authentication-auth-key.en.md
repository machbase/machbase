---
type: docs
title: '14.4 AUTH KEY Authentication'
weight: 40
toc: true
---

AUTH KEY authentication registers a public key on the server and uses the client's private
key to sign a server challenge. It can replace password authentication, but private-key
protection and rotation require separate procedures. Select `AUTH_MODE=PASSWORD` or
`AUTH_MODE=CHALLENGE` for each connection.

## Preparation

1. Create a dedicated application user.
2. Generate a key pair on the client host.
3. Register only the public key on the server.
4. Store the private-key file in the client's secret store.
5. Verify a CHALLENGE connection, then record key expiration and rotation dates.

For supported keys and complete AUTH KEY SQL syntax, see
[USER/AUTH Syntax](/dbms/reference/sql/syntax/user-auth-syntax/#auth-key).

<a id="user-auth-key"></a>

## Manage user AUTH KEYs

Check registration state in `V$USER_AUTH_KEYS`.

```sql
SELECT KEY_ID, USER_NAME, KEY_ALGO, KEY_PARAM,
       ACTIVATED, VALID_AFTER, VALID_BEFORE, COMMENT
  FROM V$USER_AUTH_KEYS
 WHERE USER_NAME = 'APP_USER'
 ORDER BY KEY_ID;
```

`PUBKEY` contains the public-key body; preferably omit it from routine operational reports.

<a id="create-user-auth-key"></a>
<a id="user-auth-key-create-user-auth-key"></a>

### CREATE USER ... WITH AUTH KEY

You can register a public key while creating a user. Replace the sample public-key string
with the actual PEM contents, representing line breaks as `\n`.

```sql
CREATE USER app_user IDENTIFIED BY 'App#Strong123'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial application key'
);
```

A password may remain an emergency recovery path. Use a separate strong password and policy.

<a id="alter-user-add-auth-key"></a>
<a id="user-auth-key-alter-user-add-auth-key"></a>

### ALTER USER ... ADD AUTH KEY

Add a new public key to an existing user as follows.

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='replacement key'
);
```

After registration, query the new `KEY_ID`, algorithm, active state, and expiration date.

<a id="enable-disable-auth-key"></a>
<a id="user-auth-key-enable-disable-auth-key"></a>

### Enable and disable AUTH KEYs

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

Disabling a key blocks authentication while preserving its metadata. Before disabling a
production key, verify that another authentication path actually works.

<a id="alter-expiration-auth-key"></a>
<a id="user-auth-key-alter-expiration-auth-key"></a>

### Change AUTH KEY expiration

```sql
ALTER USER app_user
  ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';
```

Before extending expiration, recheck who uses the key and how it is stored. Extending validity
does not change the key itself, so manage rotation intervals separately.

<a id="delete-auth-key"></a>
<a id="user-auth-key-delete-auth-key"></a>

### Drop an AUTH KEY

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

Deletion cannot be undone. Verify successful access with the new key and disabled status for
the old key before deleting it. Dropping a user also removes that user's AUTH KEYs.

## Key rotation

1. Generate a new key pair.
2. Register the new public key with `ADD AUTH KEY`.
3. Verify a CHALLENGE connection using the new private key.
4. Disable the old key and verify that connections using it fail.
5. Delete the old key after the observation period.

Keeping the old key during the transition lets you validate rotation without interrupting service.

<a id="authentication-auth-key-challenge"></a>

## AUTH KEY challenge authentication

The client must be able to read the private-key file paired with the registered public key.
Do not register the private key on the server. CHALLENGE authentication fails if the file is
missing, the private key does not match the registered public key, or the registered key is
disabled or expired. It does not automatically fall back to PASSWORD; explicitly establish
a separate PASSWORD connection if needed.

<a id="authentication-sys-user"></a>

## SYS AS USER authentication restrictions

To use CHALLENGE authentication as `SYS`, register an AUTH KEY for `SYS`. For application
connections, avoid `SYS` and use a dedicated account with minimum privileges and its own key instead. Change
`SYS` keys during a maintenance window with another verified administrative access path.

<a id="auth-mode-challenge"></a>

## AUTH_MODE=CHALLENGE

In `machsql`, specify both the connection string and private-key option.

```bash
machsql -s 127.0.0.1 -P 5656 -u app_user \
  -c "AUTH_MODE=CHALLENGE" \
  -K /secure/path/app_user.key
```

The following example uses JDBC connection properties.

```text
jdbc:machbase://127.0.0.1:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_KEY_FILE=/secure/path/app_user.key
```

Do not log private-key file contents, passwords, or secrets from connection strings in logs
or error reports.

<a id="auth-key-file"></a>

## AUTH_KEY_FILE

Generate the private key on the client host and use only the public key for SQL registration.
For example, generate an ECDSA P-256 key pair as follows.

```bash
openssl ecparam -name prime256v1 -genkey -noout -out app_user.key
openssl ec -in app_user.key -pubout -out app_user.pub
chmod 600 app_user.key
```

`chmod 600` is an operational recommendation to reduce private-key exposure. Also verify
that the actual process account can read the file and access its parent directories. When
converting a public key to an inline SQL string, represent line breaks as `\n` as follows.

```bash
awk '{printf "%s\\n", $0}' app_user.pub
```

Validate the private-key formats actually supported, including PKCS#8, with your client
and deployed version.

<a id="auth-sig-scheme"></a>

## AUTH_SIG_SCHEME

| Public key | Available signature schemes |
|---|---|
| ECDSA P-256, P-384, P-521 | `ECDSA` |
| RSA 2048, 3072, 4096 | `RSA_PKCS1_V15`, `RSA_PSS` |

You can use the key's default scheme. To explicitly select RSA-PSS, also set the client option.

```bash
machsql -s 127.0.0.1 -P 5656 -u app_user \
  -c "AUTH_MODE=CHALLENGE" \
  -K /secure/path/app_user_rsa.key \
  --auth-sig-scheme=RSA_PSS
```

Authentication fails if the registered public-key type does not match the signature scheme.

<a id="support-scope-rsa-ecdsa-rsa-pss"></a>

## RSA / ECDSA / RSA_PSS support

Choose algorithms based on security policy, client support, and compatibility with the key
management system. Do not make universal claims about an algorithm's speed or security.
Before registration, verify the full generation, connection, rotation, and revocation lifecycle
with the actual client.
