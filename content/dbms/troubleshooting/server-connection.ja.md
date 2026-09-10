---
type: docs
title: '15.2 サーバーと接続の問題'
weight: 20
toc: true
---

接続問題は、サーバー起動、TCP 接続、ユーザー認証の順に切り分けます。

<a id="start-server"></a>

## サーバーが起動しない場合

```bash
machadmin -e
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
```

次を順に確認します。

1. 設定ポートを別プロセスが使っていないか。
2. サーバーの OS アカウントがインストール・データ・ログのパスを読み書きできるか。
3. ファイルシステムの容量と inode が十分か。
4. ライセンスがインストールされ、有効か（`machadmin -f`）。
5. 前のプロセスや lock ファイルが残る原因は何か。

原因未確認の強制停止や lock ファイル削除は避けます。正常停止できない場合はログとプロセス状態を
保存し、承認済み復旧手順を使用します。

<a id="connection"></a>

## 接続できない場合

サーバーホストで、まずローカル接続を試します。

```bash
machadmin -e
machsql -s 127.0.0.1 -P 5656 -u app_user
```

ローカルは成功し、リモートだけ失敗する場合は次を確認します。

- クライアントが使うアドレスとポート
- `GRANT_REMOTE_ACCESS`、`BIND_IP_ADDRESS` の現在値
- OS・クラウドのファイアウォールと中間ネットワーク経路
- `MAX_SESSION_COUNT` 到達と未クローズセッション

```sql
SELECT NAME, VALUE
  FROM V$PROPERTY
 WHERE NAME IN ('GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS', 'MAX_SESSION_COUNT');

SELECT ID, USER_NAME, CLOSED
  FROM V$SESSION
 ORDER BY ID;
```

リスナー設定は起動時に適用されるため、設定ファイルの変更後にメンテナンス再起動を行い、
リモート・ローカル接続を検証します。ファイアウォール操作は対象 OS の公式文書に従います。

<a id="failure-authentication"></a>

## 認証が失敗する場合

まず接続で選択した認証方式を確認します。`AUTH_MODE` はサーバーの `V$PROPERTY` ではなく、
クライアントの接続オプションです。

パスワード認証ではユーザー名、パスワードポリシー、有効期限を確認します。

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 WHERE NAME = 'APP_USER';
```

AUTH KEY 認証では登録鍵とクライアントオプションを確認します。

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

秘密鍵ファイルが存在してクライアントプロセスが読めるか、公開鍵と対になっているか、鍵が有効で
期限内かを確認します。アカウントロック解除や `CREATE AUTH KEY` など、現行構文にない操作は使わないでください。
登録と交換は [AUTH KEY 認証](/dbms/security-access-control/authentication-auth-key/)に従います。
