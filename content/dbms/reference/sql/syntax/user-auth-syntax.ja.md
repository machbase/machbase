---
type: docs
title: 'USER/AUTH'
weight: 200
toc: true
---

ユーザーの作成・削除・パスワード変更、権限の付与・取り消し、公開鍵を使用するAUTH KEYの管理構文です。

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

ユーザー名は保存時に大文字へ変換します。

```sql
-- 基本的なユーザー作成
CREATE USER app_user IDENTIFIED BY 'App#1234';

-- パスワードポリシーの指定
CREATE USER ops_user IDENTIFIED BY 'Ops@Strong1' PASSWORD POLICY HIGH;

-- AUTH KEYとともに作成（公開鍵認証）
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkw...(省略)...==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial key'
);
```

### パスワードポリシー

| ポリシー | 説明 |
|------|------|
| `NONE` | 強度の制約なし。有効期限なし |
| `LOW` | 10文字以上、大文字・小文字・特殊文字を含む。連続する数字・キーボード配列のパターンは禁止 |
| `HIGH` | LOWの規則 + 直近24個のパスワードの再利用禁止 + 90日で自動失効 |

---

## DROP USER

```sql
drop_user_stmt ::= 'DROP USER' user_name
```

`SYS`ユーザーは削除できません。対象ユーザーが作成したテーブルが残っている場合はエラーになります。

別の管理者セッションがユーザーを削除しても、既存のアクティブセッションは即座には終了しません。新規接続は
失敗し、既存セッションはログイン時のユーザー名とIDを保持します。運用手順は[アカウント管理](../../../../security-access-control/account/#drop-user-active-session)を、
確認関数は[ユーザーコンテキスト関数](../../functions/functions-full/#current-session-user)を参照してください。

```sql
DROP USER old_user;
```

---

## ALTER USER

```sql
-- パスワードの変更
alter_user_pwd_stmt ::=
    'ALTER USER' user_name 'IDENTIFIED BY' new_password
    [ 'PASSWORD POLICY' ( 'NONE' | 'LOW' | 'HIGH' ) ]
```

ポリシーのみを変更する構文は許可しません。ポリシーを変更する場合は、必ず新しいパスワードも指定してください。

```sql
-- パスワードの変更
ALTER USER app_user IDENTIFIED BY 'NewPass#456';

-- パスワードとポリシーを同時変更
ALTER USER app_user IDENTIFIED BY 'NewPass#456' PASSWORD POLICY HIGH;
```

---

## CONNECT

```sql
user_connect_stmt ::= 'CONNECT' user_name '/' password
```

アプリケーションを終了せず、別のユーザーで再接続します。

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

### テーブル権限

```sql
-- テーブルのDML権限
GRANT SELECT ON sensor_log TO reader;
GRANT SELECT, INSERT ON sys.sensor_log TO writer;
GRANT ALL ON sys.sensor_log TO app_user;

-- 権限の取り消し
REVOKE INSERT ON sys.sensor_log FROM writer;
REVOKE ALL ON sys.sensor_log FROM app_user;
```

テーブル権限の種類: `SELECT`, `INSERT`, `DELETE`, `UPDATE`, `ALL`

### データベース権限（Machbase 8.5以降）

```sql
-- DDL権限（CREATE + DROP）
GRANT DDL ON DATABASE factory_a TO deploy_user;

-- 個別のDDL権限
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT CREATE ON DATABASE factory_a TO create_user;
GRANT DROP   ON DATABASE factory_a TO drop_user;
GRANT ALTER  ON DATABASE factory_a TO ops_user;

-- 運用権限
GRANT BACKUP ON DATABASE factory_a TO backup_user;
GRANT MOUNT  ON DATABASE MACHBASEDB TO mount_user;
GRANT USAGE  ON DATABASE factory_a_backup TO report_user;

-- すべてのデータベース権限
GRANT ALL ON DATABASE factory_a TO admin_user;

-- 権限の取り消し
REVOKE BACKUP ON DATABASE factory_a FROM backup_user;
```

データベース権限の種類: `CONNECT`, `CREATE`, `DROP`, `ALTER`, `BACKUP`, `MOUNT`, `USAGE`,
`DDL`(`CREATE+DROP`), `ALL`(`CONNECT+CREATE+DROP+ALTER+BACKUP`)

### データベース権限が必要な操作

| 操作 | 必要な権限 |
|------|------------|
| CREATE/DROP TABLE, VIEW, INDEX, ROLLUP, TABLESPACE, RETENTION | `CREATE`、`DROP`、または`DDL` |
| ALTER SYSTEM | `ALTER` |
| BACKUP DATABASE | `BACKUP` |
| MOUNT/UMOUNT DATABASE | `MOUNT` |

### ユーザー作成時のデフォルト権限

新規ユーザーはデフォルトで`SELECT`、`INSERT`、`DELETE`、`UPDATE`、`CREATE`、`DROP`権限を持ちます。
`ALTER`、`MOUNT`、`BACKUP`は明示的に付与してください。

---

## AUTH KEY管理 {#auth-key}

AUTH KEYは、パスワードの代わりに公開鍵によるチャレンジ認証を使用するため、Machbaseに登録する公開鍵です。

### 対応するアルゴリズム

| アルゴリズム | 対応するパラメーター | 署名方式 |
|---------|-------------|----------|
| ECDSA | P-256, P-384, P-521 | ECDSA |
| RSA | 2048, 3072, 4096 bits | RSA_PKCS1_V15, RSA_PSS |

### 鍵ファイルの生成（openssl）

```bash
# ECDSA P-256鍵の生成
openssl ecparam -name prime256v1 -genkey -noout -out app_user.key
openssl ec -in app_user.key -pubout -out app_user.pub
chmod 600 app_user.key

# RSA 2048-bit鍵の生成
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -pubout -out app_user_rsa.pub
chmod 600 app_user_rsa.key

# PEMをSQLインライン形式へ変換（改行を\nにする）
awk '{printf "%s\\n", $0}' app_user.pub
```

### AUTH KEYの追加

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
    key='-----BEGIN PUBLIC KEY-----\nMFkw...(省略)...==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='primary key'
);
```

追加した鍵は直ちに有効な状態（`ACTIVATED=1`）で登録されます。

### AUTH KEYの有効化 / 無効化

```sql
alter_user_activate_key_stmt   ::= 'ALTER USER' user_name 'ACTIVATE AUTH KEY ID'   key_id
alter_user_deactivate_key_stmt ::= 'ALTER USER' user_name 'DEACTIVATE AUTH KEY ID' key_id
```

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

### AUTH KEYの有効期間変更

```sql
alter_user_alter_key_stmt ::=
    'ALTER USER' user_name 'ALTER AUTH KEY ID' key_id
    "VALID_BEFORE='" YYYY-MM-DD "'"
```

```sql
ALTER USER app_user ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';
```

### AUTH KEYの削除

```sql
alter_user_drop_key_stmt ::=
    'ALTER USER' user_name 'DROP AUTH KEY ID' key_id
```

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

### AUTH KEYの参照

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

`V$USER_AUTH_KEYS`の主な列: `KEY_ID`, `USER_NAME`, `KEY_ALGO`, `KEY_PARAM`, `ACTIVATED`, `VALID_AFTER`, `VALID_BEFORE`, `COMMENT`, `PUBKEY`

---

## 関連ドキュメント

- [ユーザー管理ガイド](../../../../operations-configuration-recovery/) - ユーザー運用の手順と例
- [システム/セッション管理構文](../system-session-alter-syntax/) - ALTER SYSTEM, ALTER SESSION
