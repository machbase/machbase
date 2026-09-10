---
type: docs
title: '14.4 AUTH KEY 認証'
weight: 40
toc: true
---

AUTH KEY 認証は、サーバーに公開鍵を登録し、クライアントの秘密鍵でサーバーの challenge に署名する方式です。
パスワードの代わりに秘密鍵を使えますが、秘密鍵の保護と交換は別途管理します。接続ごとに
`AUTH_MODE=PASSWORD` または `AUTH_MODE=CHALLENGE` を選択します。

## 準備

1. アプリケーション専用ユーザーを作成します。
2. クライアントホストで鍵ペアを生成します。
3. 公開鍵だけをサーバーに登録します。
4. 秘密鍵ファイルをクライアントのシークレットストアに保管します。
5. CHALLENGE 接続を確認し、鍵の有効期限と交換予定を記録します。

対応する鍵と AUTH KEY SQL の全構文は
[USER/AUTH 構文](/dbms/reference/sql/syntax/user-auth-syntax/#auth-key)を参照してください。

<a id="user-auth-key"></a>

## ユーザーの AUTH KEY 管理

登録状態は `V$USER_AUTH_KEYS` で確認します。

```sql
SELECT KEY_ID, USER_NAME, KEY_ALGO, KEY_PARAM,
       ACTIVATED, VALID_AFTER, VALID_BEFORE, COMMENT
  FROM V$USER_AUTH_KEYS
 WHERE USER_NAME = 'APP_USER'
 ORDER BY KEY_ID;
```

`PUBKEY` には公開鍵本文があるため、通常の運用レポートには含めないことを推奨します。

<a id="create-user-auth-key"></a>
<a id="user-auth-key-create-user-auth-key"></a>

### CREATE USER ... WITH AUTH KEY

ユーザー作成と同時に公開鍵を登録できます。以下の文字列を、実際の PEM の改行を `\n` で表した値に
置き換えてください。

```sql
CREATE USER app_user IDENTIFIED BY 'App#Strong123'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial application key'
);
```

パスワードを緊急復旧経路として使う場合もあるため、別の強力な値とポリシーで管理します。

<a id="alter-user-add-auth-key"></a>
<a id="user-auth-key-alter-user-add-auth-key"></a>

### ALTER USER ... ADD AUTH KEY

既存ユーザーには次のように新しい公開鍵を追加します。

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='replacement key'
);
```

登録後、新しい `KEY_ID`、アルゴリズム、アクティブ状態、有効期限を確認します。

<a id="enable-disable-auth-key"></a>
<a id="user-auth-key-enable-disable-auth-key"></a>

### AUTH KEY の有効化と無効化

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

無効化は鍵メタデータを保持したまま認証を遮断します。運用中の鍵を無効化する前に、
別の認証経路が実際に機能することを確認してください。

<a id="alter-expiration-auth-key"></a>
<a id="user-auth-key-alter-expiration-auth-key"></a>

### AUTH KEY の有効期限変更

```sql
ALTER USER app_user
  ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';
```

期限を延長する前に、利用主体と保管状態を再確認します。有効期間を延ばしても鍵自体は変わらないため、
ローテーション周期は別途管理します。

<a id="delete-auth-key"></a>
<a id="user-auth-key-delete-auth-key"></a>

### AUTH KEY の削除

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

削除は取り消せません。新しい鍵での接続成功と、古い鍵が無効であることを確認してから削除します。
ユーザーを削除すると、そのユーザーの AUTH KEY も削除されます。

## 鍵のローテーション

1. 新しい鍵ペアを生成します。
2. 新しい公開鍵を `ADD AUTH KEY` で登録します。
3. 新しい秘密鍵で CHALLENGE 接続を検証します。
4. 古い鍵を無効化し、その鍵での接続失敗を確認します。
5. 観察期間が終わったら古い鍵を削除します。

古い鍵を一度に上書きしないことで、サービスを停止せずに交換結果を検証できます。

<a id="authentication-auth-key-challenge"></a>

## AUTH KEY challenge 認証

クライアントは、登録済み公開鍵と対になる秘密鍵ファイルを読める必要があります。秘密鍵自体は
サーバーに登録しません。ファイルがない、秘密鍵が登録鍵と一致しない、登録鍵が無効または期限切れなら
CHALLENGE 認証は失敗します。PASSWORD へ自動切り替えしないため、必要なら別の PASSWORD 接続を明示します。

<a id="authentication-sys-user"></a>

## SYS AS USER 認証の制約

`SYS` で CHALLENGE 認証を使う場合も、`SYS` に AUTH KEY の登録が必要です。ただしアプリケーションの
接続に `SYS` を使わず、専用アカウントへ最小権限と鍵を付与してください。`SYS` の鍵は、
別の管理経路を検証済みのメンテナンス時間に変更します。

<a id="auth-mode-challenge"></a>

## AUTH_MODE=CHALLENGE

`machsql` では接続文字列と秘密鍵オプションを併せて指定します。

```bash
machsql -s 127.0.0.1 -P 5656 -u app_user \
  -c "AUTH_MODE=CHALLENGE" \
  -K /secure/path/app_user.key
```

JDBC 接続プロパティの例は次のとおりです。

```text
jdbc:machbase://127.0.0.1:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_KEY_FILE=/secure/path/app_user.key
```

秘密鍵ファイルの内容、パスワード、接続文字列のシークレットをログやエラーレポートに残さないでください。

<a id="auth-key-file"></a>

## AUTH_KEY_FILE

秘密鍵はクライアントホストで生成し、SQL 登録には公開鍵だけを使います。ECDSA P-256 鍵ペアは
例えば次のように生成できます。

```bash
openssl ecparam -name prime256v1 -genkey -noout -out app_user.key
openssl ec -in app_user.key -pubout -out app_user.pub
chmod 600 app_user.key
```

`chmod 600` は秘密鍵の露出を減らすための運用上の推奨です。実行プロセスのアカウントがファイルと
親ディレクトリへアクセスできることも確認します。公開鍵を SQL のインライン文字列にする場合、
次のように改行を `\n` で表します。

```bash
awk '{printf "%s\\n", $0}' app_user.pub
```

PKCS#8 を含む実際の秘密鍵形式のサポートは、使用するクライアントと配布バージョンで検証してください。

<a id="auth-sig-scheme"></a>

## AUTH_SIG_SCHEME

| 公開鍵 | 利用できる署名方式 |
|---|---|
| ECDSA P-256, P-384, P-521 | `ECDSA` |
| RSA 2048, 3072, 4096 | `RSA_PKCS1_V15`, `RSA_PSS` |

鍵に適したデフォルト方式を使用できます。RSA-PSS を明示する場合は、クライアントオプションも指定します。

```bash
machsql -s 127.0.0.1 -P 5656 -u app_user \
  -c "AUTH_MODE=CHALLENGE" \
  -K /secure/path/app_user_rsa.key \
  --auth-sig-scheme=RSA_PSS
```

公開鍵タイプと署名方式が一致しない場合、認証に失敗します。

<a id="support-scope-rsa-ecdsa-rsa-pss"></a>

## RSA / ECDSA / RSA_PSS のサポート範囲

アルゴリズムはセキュリティポリシー、クライアントのサポート、鍵管理システムとの互換性で選びます。
速度や安全性がどの環境でも同じと決めつけないでください。登録前に、実際のクライアントで
生成・接続・ローテーション・廃棄の全手順を検証します。
