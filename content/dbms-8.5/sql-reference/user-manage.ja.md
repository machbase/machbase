---
title : 'ユーザー管理'
type: docs
weight: 60
toc: true
---

# 目次 {#index}

* [CREATE USER](#create-user)
* [DROP USER](#drop-user)
* [ALTER USER](#alter-user)
* [PASSWORD POLICY](#password-policy)
* [AUTH KEY ファイルの生成](#generate-auth-key-files)
* [AUTH KEY 付きユーザーの作成](#create-a-user-with-auth-key)
* [AUTH KEY の管理](#manage-auth-key)
* [AUTH KEY メタデータの検索](#query-auth-key-metadata)
* [CONNECT](#connect)
* [GRANT/REVOKE](#grantrevoke)
* [ユーザー管理の例](#managing-user-example)


## CREATE USER {#create-user}

**create_user_stmt:**

![create_user_stmt](/images/sql/user/create_user_stmt.png)

```sql
create_user_stmt ::= 'CREATE USER' user_name 'IDENTIFIED BY' password
```

ユーザーを作成する構文は次のとおりです。

```sql
-- Example
CREATE USER new_user IDENTIFIED BY password
```

パスワードポリシーも同時に指定する場合は、次の拡張構文を使用します。

```sql
CREATE USER user_name IDENTIFIED BY password PASSWORD POLICY { NONE | LOW | HIGH }
```

例：

```sql
CREATE USER app_user IDENTIFIED BY "Aa!StrongPwd1" PASSWORD POLICY LOW;
CREATE USER ops_user IDENTIFIED BY "Bb@StrongPwd2" PASSWORD POLICY HIGH;
```

ユーザー名は作成時に大文字へ変換されます。例えば `CREATE USER app_user ...` は、メタテーブルと `V$` ビューで `APP_USER` として保存、表示されます。その後の接続や権限の文でも、同じユーザー名を参照します。


## DROP USER {#drop-user}

**drop_user_stmt:**

![drop_user_stmt](/images/sql/user/drop_user_stmt.png)

```sql
drop_user_stmt ::= 'DROP USER' user_name
```

ユーザーを削除する構文は次のとおりです。SYS ユーザーは削除できません。また、削除するユーザーが作成したテーブルが残っている場合はエラーになります。

```sql
-- Example
DROP USER old_user
```


## ALTER USER {#alter-user}

**alter_user_pwd_stmt:**

![alter_user_pwd_stmt](/images/sql/user/alter_user_pwd_stmt.png)

```sql
alter_user_pwd_stmt ::= 'ALTER USER' user_name 'IDENTIFIED BY' password
```

次の構文でパスワードを変更できます。

```sql
-- Example
ALTER USER user1 IDENTIFIED BY password
```

パスワードの変更と同時に、パスワードポリシーも変更できます。

```sql
ALTER USER user_name IDENTIFIED BY password PASSWORD POLICY { NONE | LOW | HIGH }
```

ポリシーを変更するときは、新しいパスワードを一緒に指定します。`ALTER USER user_name PASSWORD POLICY HIGH` のように、ポリシーだけを変更する文は使用できません。


## PASSWORD POLICY {#password-policy}

パスワードポリシーは、`CREATE USER` と `ALTER USER ... IDENTIFIED BY ...` でパスワードの強度を検証する機能です。ポリシーを指定しない場合は、互換性のため `NONE` が適用されます。

ポリシーレベル：

- `NONE`
  - パスワード強度の制限はありません。
  - パスワードの有効期限（`VALID_BEFORE`）は `NULL` です。
- `LOW`
  - パスワードは 10 文字以上である必要があります。
  - パスワードに大文字、小文字、特殊文字を含める必要があります。
  - 5 桁以上連続する数字、増加または減少する数字列、キーボード配列順の文字列は使用できません。
  - パスワードの有効期限（`VALID_BEFORE`）は `NULL` です。
- `HIGH`
  - `LOW` のすべての規則を適用します。
  - 現在のパスワードと直近 24 個の過去のパスワードは再利用できません。
  - パスワードを設定した時点から 90 日後が、有効期限（`VALID_BEFORE`）として自動的に設定されます。

ポリシーの例：

```sql
CREATE USER user1 IDENTIFIED BY "Aa!StrongPwd1";
CREATE USER user2 IDENTIFIED BY "Bb@StrongPwd2" PASSWORD POLICY LOW;
CREATE USER user3 IDENTIFIED BY "Cc#StrongPwd3" PASSWORD POLICY HIGH;

ALTER USER user2 IDENTIFIED BY "Dd$NewPwd44";
ALTER USER user2 IDENTIFIED BY "Ee%NewPwd55" PASSWORD POLICY LOW;
ALTER USER user3 IDENTIFIED BY "Ff#NewPwd66" PASSWORD POLICY NONE;
```

注意事項：

- `ALTER USER ... IDENTIFIED BY ...` は、そのユーザーに保存されているポリシーで新しいパスワードを検証します。
- `ALTER USER ... IDENTIFIED BY ... PASSWORD POLICY ...` は、新しいポリシーで新しいパスワードを検証します。
- `HIGH` に変更した場合、または `HIGH` のユーザーがパスワードを変更した場合、`VALID_BEFORE` は現在時刻から 90 日後に更新されます。
- `LOW` または `NONE` に変更すると、`VALID_BEFORE` は `NULL` に更新されます。
- 期限切れのアカウントはログインできないため、そのアカウントではパスワードを変更できません。管理者アカウントから新しいパスワードに再設定してください。

`M$SYS_USERS` でポリシーと期限を確認できます。

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
FROM M$SYS_USERS;
```

`PWD_POLICY_LEVEL` は `0 = NONE`、`1 = LOW`、`2 = HIGH` を表します。`VALID_BEFORE` は、値がある場合に `YYYY-MM-DD` 形式で表示されます。

## AUTH KEY ファイルの生成 {#generate-auth-key-files}

> **注意**：以下の動作は Machbase 8.5 以降でサポートされます。

AUTH KEY 認証は、クライアント側の秘密鍵ファイルと、Machbase ユーザーに登録した公開鍵を使用します。通常は `openssl` で鍵ペアを生成し、秘密鍵をクライアントに保管して、公開鍵だけを Machbase に登録します。

対応するアルゴリズムと鍵サイズは次のとおりです。

| 公開鍵アルゴリズム | 対応する鍵パラメーター | 対応する署名方式 | ハッシュ |
| --- | --- | --- | --- |
| ECDSA | P-256, P-384, P-521 | `ECDSA` | SHA-256 |
| RSA | 2048, 3072, 4096 ビット | `RSA_PKCS1_V15` | SHA-256 |
| RSA | 2048, 3072, 4096 ビット | `RSA_PSS` | SHA-256 |

`AUTH_SIG_SCHEME` を省略すると、Machbase は鍵アルゴリズムに応じた既定の方式を使用します。

- ECDSA 鍵：`ECDSA`
- RSA 鍵：`RSA_PKCS1_V15`

RSA-PSS を使用するには、クライアントの接続オプションに `AUTH_SIG_SCHEME=RSA_PSS` を指定します。登録済み公開鍵の型と、クライアントが要求する署名方式が一致しない場合は、認証に失敗します。

ECDSA P-256 鍵の生成例：

```bash
openssl ecparam -name prime256v1 -genkey -noout -out app_user_ecdsa.key
openssl ec -in app_user_ecdsa.key -pubout -out app_user_ecdsa.pub
chmod 600 app_user_ecdsa.key
```

ECDSA P-384 と P-521 鍵の生成例：

```bash
openssl ecparam -name secp384r1 -genkey -noout -out app_user_ecdsa_p384.key
openssl ec -in app_user_ecdsa_p384.key -pubout -out app_user_ecdsa_p384.pub

openssl ecparam -name secp521r1 -genkey -noout -out app_user_ecdsa_p521.key
openssl ec -in app_user_ecdsa_p521.key -pubout -out app_user_ecdsa_p521.pub
```

RSA 2048 ビット鍵の生成例：

```bash
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -pubout -out app_user_rsa.pub
chmod 600 app_user_rsa.key
```

上の例の `app_user_rsa.pub` は、`-----BEGIN PUBLIC KEY-----` 形式で生成されます。PKCS#1 RSA 公開鍵の `-----BEGIN RSA PUBLIC KEY-----` 形式で生成するには、`-RSAPublicKey_out` オプションを使用します。

```bash
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -RSAPublicKey_out -out app_user_rsa_pkcs1.pub
chmod 600 app_user_rsa.key
```

3072 ビットまたは 4096 ビットの RSA 鍵を使用するには、`openssl genrsa` の最後の引数に `3072` または `4096` を指定します。

公開鍵を SQL に埋め込む場合は、PEM の改行をエスケープして 1 つの SQL 文字列にします。

```bash
awk '{printf "%s\\n", $0}' app_user_ecdsa.pub
```

コマンドの出力を、`CREATE USER ... WITH AUTH KEY` または `ALTER USER ... ADD AUTH KEY` の `PUBKEY` の値として使用します。

生成した公開鍵から登録 SQL ファイルを作成する例です。

```bash
KEY_ESCAPED=$(awk '{printf "%s\\n", $0}' app_user_ecdsa.pub)

cat > add_app_user_key.sql <<EOF
ALTER USER app_user ADD AUTH KEY (
    PUBKEY = '${KEY_ESCAPED}',
    VALID_BEFORE = '2047-12-31',
    COMMENT = 'openssl generated ecdsa key'
);
EOF
```

X.509 証明書を登録する場合は、同じ秘密鍵で自己署名証明書を作成し、証明書の PEM を `PUBKEY` の値として使用します。認証時のクライアントは、証明書ファイルではなく、対応する秘密鍵ファイルを使用します。

```bash
openssl req -new -x509 \
    -key app_user_ecdsa.key \
    -out app_user_ecdsa.crt \
    -days 3650 \
    -subj "/CN=app_user"
```

証明書の PEM を SQL に埋め込む場合も、改行を `\n` でエスケープします。

```bash
CERT_ESCAPED=$(awk '{printf "%s\\n", $0}' app_user_ecdsa.crt)
```

生成した証明書から登録 SQL ファイルを作る例です。

```bash
cat > create_app_x509.sql <<EOF
CREATE USER app_x509 IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    PUBKEY = '${CERT_ESCAPED}',
    VALID_BEFORE = '2036-07-12',
    COMMENT = 'x509 certificate key'
);
EOF
```

## AUTH KEY 付きユーザーの作成 {#create-a-user-with-auth-key}

> **注意**：以下の動作は Machbase 8.5 以降でサポートされます。

Machbase では、パスワード認証に加えて、公開鍵チャレンジ認証用の AUTH KEY をユーザーに登録できます。

```sql
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    PUBKEY = '-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n',
    VALID_BEFORE = '2047-12-31',
    COMMENT = 'initial key'
);
```

注意事項：

- `PUBKEY` には PEM 公開鍵または X.509 証明書を指定します。
- `PUBKEY` に指定できる形式は、次の 3 種類の PEM ブロックです。
  - `-----BEGIN PUBLIC KEY-----`：SubjectPublicKeyInfo（SPKI）形式の ECDSA または RSA 公開鍵
  - `-----BEGIN RSA PUBLIC KEY-----`：PKCS#1 形式の RSA 公開鍵
  - `-----BEGIN CERTIFICATE-----`：X.509 証明書
- SQL 内では PEM の改行を `\n` と書けます。
- `VALID_BEFORE` は `YYYY-MM-DD` 形式です。
- `VALID_BEFORE` には、`YYYY-MM-DD HH24:MI:SS` のように時刻を含む日時の値は指定できません。
- 現在の AUTH KEY 構文では `COMMENT` は必須です。
- `CREATE USER ... WITH AUTH KEY` で作成した最初の鍵は、有効な状態（`ACTIVATED=1`）で登録されます。
- 1 人のユーザーが、パスワードと 1 つ以上の AUTH KEY を同時に持てます。実際の認証方式はクライアントの `AUTH_MODE` で決まり、失敗時に別の方式へ自動で切り替わることはありません。
- `ssh-rsa ...` や `ecdsa-sha2-nistp256 ...` などの生の OpenSSH 公開鍵は、`PUBKEY` に直接登録できません。先に `ssh-keygen -e -m PKCS8` などで PEM 公開鍵に変換してください。

X.509 証明書の PEM を直接入力する例です。下の証明書は、PEM の入力形式を示すための固定の例です。実際の認証では、上記 `CERT_ESCAPED` の例と同様に、登録する証明書とクライアントの秘密鍵が同じ鍵ペアである必要があります。

```sql
CREATE USER app_x509 IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    PUBKEY = '-----BEGIN CERTIFICATE-----\nMIIBmDCCAT+gAwIBAgIUAOBEtntR9La6sDNPUeW6o4m+oBcwCgYIKoZIzj0EAwIw\nIjEgMB4GA1UEAwwXbWFjaGJhc2UtMzgwNS14NTA5LWF1dGgwHhcNMjYwNzE1MDEw\nMzAxWhcNMzYwNzEyMDEwMzAxWjAiMSAwHgYDVQQDDBdtYWNoYmFzZS0zODA1LXg1\nMDktYXV0aDBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABLIcXK0praLGqlo4UZDq\nAMOL90Fqi7NzhTdo2ya7rLRHNdrgJ/yHbUxveCiuvW2Ow1pfNKc0OPHTS/hDV3vD\n096jUzBRMB0GA1UdDgQWBBQZ2DHpG/e/fq7RI3Cm1Z78N7l4LDAfBgNVHSMEGDAW\ngBQZ2DHpG/e/fq7RI3Cm1Z78N7l4LDAPBgNVHRMBAf8EBTADAQH/MAoGCCqGSM49\nBAMCA0cAMEQCIGSsnhbOFiJkhCCrKsut+cg5O2TVDfHUBgGXFeg7nS/7AiA9wVgn\no1LE0HTkPLZYt99uOXHZ7D3Ygbvo+VwJK1SoRg==\n-----END CERTIFICATE-----\n',
    VALID_BEFORE = '2036-07-12',
    COMMENT = 'x509 certificate key'
);
```

X.509 証明書を登録すると、Machbase は証明書から公開鍵を抽出して保存します。証明書チェーンや CA の信頼性は検証しません。証明書は、公開鍵と有効期限を持つ入力形式として扱います。PEM ブロックは必ず 1 つだけにしてください。チェーン PEM、秘密鍵 PEM、生の OpenSSH 鍵、未対応ヘッダー、有効な PEM の後に空白以外のテキストが続く入力は拒否されます。

X.509 証明書には `notAfter` の有効期限があります。`VALID_BEFORE` は、証明書の `notAfter` より後には設定できません。この条件を満たさない場合、登録または変更は失敗します。

## AUTH KEY の管理 {#manage-auth-key}

### AUTH KEY の追加 {#add-auth-key}

```sql
ALTER USER app_user ADD AUTH KEY (
    PUBKEY = '-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAqO+tddiAQzsT8iajPy5QJPamIlyq2zB01wgHSTs3OOrvw0uKoFQD\ncqKaDzRya73LETXIEev3nwhGCnG4SjedMHj3EH9/rRJphFtv/dzw0OHum/UhVulR\nIXUYzrTbKPTQ+qyjS8UXTteMncf9OOh4AQyS4+iJW+U344fxymR8USRgZ25N9jhf\n2gkKnn5YSPZHf8ZHQGeA7OXANBwPmH5dQwfqghXRa7Nk1hmkIAnQQXCBJW/Lin+x\nwQfqv8DVwNaiziz77voPwaeD5akq1JYWvcPlOnh+NN3tpu5gudke/t/In4NFJ3W9\n4unVcYIfxcdDSoht3AMObGmuDazOjQJFGQIDAQAB\n-----END RSA PUBLIC KEY-----\n',
    VALID_BEFORE = '2048-01-31',
    COMMENT = 'rollover candidate'
);
```

追加した鍵は直ちに有効な状態（`ACTIVATED=1`）で作成されます。鍵のロールオーバー中は、1 人のユーザーが複数の有効な AUTH KEY を持てます。

### AUTH KEY の有効化と無効化 {#activate--deactivate-auth-key}

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

- 無効化した鍵はチャレンジ認証に使用できません。
- 1 人のユーザーが複数の AUTH KEY を持てます。

### AUTH KEY の有効期限の変更 {#change-auth-key-expiration}

```sql
ALTER USER app_user ALTER AUTH KEY ID 3 VALID_BEFORE = '2048-06-30';
```

- `VALID_BEFORE` を過ぎた鍵は認証に使用できません。
- `YYYY-MM-DD` 形式で指定します。時刻を含む値は指定できません。
- X.509 証明書から登録した鍵の `VALID_BEFORE` は、証明書の `notAfter` より後の日付には変更できません。

### AUTH KEY の削除 {#drop-auth-key}

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

- 削除した鍵は、直ちに認証に使用できなくなります。
- ユーザーを削除すると、その AUTH KEY メタデータも削除されます。

## AUTH KEY メタデータの検索 {#query-auth-key-metadata}

登録した AUTH KEY のメタデータは、`V$USER_AUTH_KEYS` で確認できます。

主な列：

- `KEY_ID`：AUTH KEY の識別子
- `USER_NAME`：AUTH KEY の所有者
- `KEY_ALGO`：鍵のアルゴリズム（`RSA`、`ECDSA`）
- `KEY_PARAM`：鍵のパラメーター
  - RSA 鍵：`2048` などのビット長
  - EC 鍵：`P-256`、`P-384`、`P-521` などの曲線名
- `ACTIVATED`：有効かどうか
- `VALID_AFTER`、`VALID_BEFORE`：有効期間
- `ADDITIONAL_INFO`：サーバーが生成した AUTH KEY のメタデータ
  - 公開鍵入力：`type=PUBLIC_KEY`
  - X.509 証明書入力：`type=CERTIFICATE; cert_not_after=YYYY-MM-DD`
- `COMMENT`：ユーザーの注記
- `PUBKEY`：PEM 公開鍵の本体。X.509 証明書から登録した場合は、抽出した公開鍵が保存されます。

```sql
SELECT key_id, user_name, key_algo, key_param, activated,
       valid_before, additional_info, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name='APP_USER'
 ORDER BY key_id;
```

公開鍵の本体を確認するには、`PUBKEY` 列を検索します。

```sql
SELECT key_id, user_name, pubkey
  FROM V$USER_AUTH_KEYS
 WHERE user_name='APP_USER'
 ORDER BY key_id;
```


## CONNECT {#connect}

**user_connect_stmt:**

![user_connect_stmt](/images/sql/user/user_connect_stmt.png)

```sql
user_connect_stmt: 'CONNECT' user_name '/' password
```

アプリケーションを終了せず、次の構文で別のユーザーとして再接続できます。

```sql
-- Example
CONNECT user1/password;
```


## GRANT/REVOKE {#grantrevoke}

![grant_stmt](/images/sql/user/grant_stmt.png)

![revoke_stmt](/images/sql/user/revoke_stmt.png)

![priv_value](/images/sql/user/priv_value.png)

`GRANT` でユーザーに権限を付与し、`REVOKE` で付与済みの権限を取り消します。

基本例：

```sql
-- user1 に mytable の SELECT を付与
GRANT SELECT ON mytable TO user1;

-- user1 に mytable の全権限を付与
GRANT ALL ON mytable TO user1;
```

```sql
-- user1 の mytable に対する UPDATE を取り消す
REVOKE UPDATE ON mytable FROM user1;

-- user1 の mytable に対する全権限を取り消す
REVOKE ALL ON mytable FROM user1;
```

### テーブル権限 {#table-privileges}

テーブルの権限を付与するときは、対象を次の形式で指定します。

- `table`
- `user.table`
- `db.user.table`

利用できるテーブル権限：

- `SELECT`
- `INSERT`
- `DELETE`
- `UPDATE`
- `ALL`

例：

```sql
GRANT SELECT ON sensor_log TO reader;
GRANT SELECT, INSERT ON sys.sensor_log TO writer;
REVOKE INSERT ON sys.sensor_log FROM writer;
GRANT ALL ON machbasedb.sys.sensor_log TO app_user;
```

### Machbase 8.5 以降のデータベース権限 {#machbase-85-database-privileges}

> **注意**：以下の動作は Machbase 8.5 以降でサポートされます。

Machbase 8.5 以降では、`MACHBASEDB` を対象に、データベース範囲の権限を付与できます。

```sql
GRANT CREATE ON machbasedb TO ddl_user;
GRANT DROP ON machbasedb TO ddl_user;
GRANT ALTER ON machbasedb TO ops_user;
GRANT BACKUP ON machbasedb TO backup_user;
GRANT MOUNT ON machbasedb TO mount_user;
GRANT DDL ON machbasedb TO deploy_user;
GRANT ALL ON machbasedb TO admin_user;
```

利用できるデータベース範囲の権限：

- `CREATE`
- `DROP`
- `ALTER`
- `MOUNT`
- `BACKUP`
- `DDL`
- `ALL`

ここで `DDL` は、`CREATE + DROP` を組み合わせた権限です。

### `ALL` の意味 {#meaning-of-all}

> **注意**：以下の動作は Machbase 8.5 以降でサポートされます。

`ALL` は常に同じ意味ではありません。対象によって意味が異なります。

- `GRANT ALL ON machbasedb TO user1`
  - データベース範囲のすべての権限を付与します。
- `GRANT ALL ON sys.table1 TO user1`
  - 指定したテーブルのすべての DML 権限を付与します。

つまり、`MACHBASEDB` に対する `ALL` とテーブルに対する `ALL` は同じキーワードですが、用途が異なります。

### `MACHBASEDB` に DML 権限は直接付与できない {#dml-privileges-cannot-be-granted-directly-on-machbasedb}

> **注意**：以下の動作は Machbase 8.5 以降でサポートされます。

データベース名 `MACHBASEDB` に `SELECT`、`INSERT`、`DELETE`、`UPDATE` を直接付与することはできません。

```sql
GRANT SELECT ON machbasedb TO user1;
GRANT INSERT ON machbasedb TO user1;
REVOKE DELETE ON machbasedb FROM user1;
REVOKE UPDATE ON machbasedb FROM user1;
```

これらの文は、次のエラーで失敗します。

```sql
[ERR-02186: Invalid database name.]
```

読み取りや書き込みの権限を付与するには、テーブルを指定してください。

```sql
GRANT SELECT ON sys.sensor_log TO user1;
GRANT INSERT ON sys.sensor_log TO user1;
```

### データベース対象には `MACHBASEDB` を使用 {#use-machbasedb-as-the-database-target}

> **注意**：以下の動作は Machbase 8.5 以降でサポートされます。

データベース範囲の権限を付与するときは、`MACHBASEDB` を使用します。

```sql
GRANT BACKUP ON machbasedb TO backup_user;
REVOKE BACKUP ON machbasedb FROM backup_user;
```

無効なデータベース名を指定すると、文は失敗します。

```sql
GRANT BACKUP ON typo TO backup_user;
```

```sql
[ERR-02186: Invalid database name.]
```

### データベース権限が必要な操作 {#operations-that-require-database-privileges}

> **注意**：以下の動作は Machbase 8.5 以降でサポートされます。

次の操作には、テーブル権限ではなく、`MACHBASEDB` に対するデータベース範囲の権限が必要です。

- `CREATE TABLE`, `DROP TABLE`
- `CREATE VIEW`, `DROP VIEW`
- `CREATE INDEX`, `DROP INDEX`
- `CREATE ROLLUP`, `DROP ROLLUP`
- `CREATE TABLESPACE`, `DROP TABLESPACE`
- `CREATE RETENTION`, `DROP RETENTION`
- `ALTER SYSTEM`
- `BACKUP DATABASE`
- `MOUNT DATABASE`, `UNMOUNT DATABASE`

例えば一般ユーザーが `CREATE VIEW` を実行するには、`MACHBASEDB` に対する `CREATE` を付与します。

```sql
GRANT CREATE ON machbasedb TO user1;
```

### 新規ユーザーの既定権限 {#default-privileges-for-a-new-user}

ユーザーを作成すると、次の権限が既定で付与されます。

- `SELECT`
- `INSERT`
- `DELETE`
- `UPDATE`
- `CREATE`
- `DROP`

次の権限は既定では含まれないため、必要に応じて明示的に付与します。

- `ALTER`
- `MOUNT`
- `BACKUP`

### 権限でテーブル型の制限は解除されない {#privileges-do-not-override-table-type-restrictions}

権限があっても、各テーブル型の制限はそのまま適用されます。

- `LOG` テーブルと `TAG` テーブルは、仕様上 `UPDATE` をサポートしません。
- `VOLATILE` テーブルと `LOOKUP` テーブルはすべての DML をサポートしますが、検索、更新、削除の `WHERE` は主キーに基づく必要があります。

つまり、権限を付与しても、サポートされていない DML が使用できるようになるわけではありません。

### 主な権限付与の例 {#common-grant-examples}

```sql
-- 指定テーブルへの読み取りだけを許可
GRANT SELECT ON sys.sensor_log TO reader;

-- 指定テーブルへの読み取りと挿入を許可
GRANT SELECT, INSERT ON sys.sensor_log TO writer;

-- 一般ユーザーに DDL だけを許可
GRANT DDL ON machbasedb TO deploy_user;

-- ALTER SYSTEM を許可
GRANT ALTER ON machbasedb TO ops_user;

-- バックアップを許可
GRANT BACKUP ON machbasedb TO backup_user;

-- マウントとアンマウントを許可
GRANT MOUNT ON machbasedb TO mount_user;
```


## ユーザー管理の例 {#managing-user-example}

上記の構文の実行例と結果です。

```
############################################
#SYS アカウントで接続
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

#エラー：接続中のユーザーは削除できない
Mach> drop user SYS;
[ERR-02083 : Drop user error. You cannot drop yourself(SYS).]

############################################
#DEMO1 で接続
############################################
Mach> connect demo1/demo1;
Connected successfully.

#エラー：他のアカウントのパスワードは変更できない
Mach> alter user demo2 identified by 'demo22';
[ERR-02085 : ALTER user error. The user(DEMO2) does not have ALTER privileges.]

Mach> alter user demo1 identified by demo11;
Altered successfully.

#エラー：パスワードが不正
Mach> connect demo1/demo11234;
[ERR-02081 : User authentication error. Invalid password (DEMO11234).]

#正しいパスワード
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
#SYS で再接続
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
