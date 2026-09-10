---
type: docs
title: '14.2 アカウント管理'
weight: 20
toc: true
---

アプリケーションと運用作業には別々のアカウントを使います。`SYS` はユーザーと権限の管理に限定し、
日常のクエリ・ロードには必要最小限の権限を持つアカウントを使用してください。

<a id="create-delete-user"></a>

## ユーザーの作成と削除

```sql
CREATE USER app_user IDENTIFIED BY 'App#Strong123' PASSWORD POLICY HIGH;

SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 WHERE NAME = 'APP_USER';
```

ユーザー名は大文字で保存されます。論理データベースへ接続するには、アカウント作成後に
対象データベースの `CONNECT` を別途付与します。

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;
```

パスワード変更時は、新しいパスワードとポリシーを同時に指定できます。

```sql
ALTER USER app_user IDENTIFIED BY 'App#Changed456' PASSWORD POLICY HIGH;
```

ユーザー削除前に、実行中のセッション、付与した権限、所有オブジェクトを確認します。
オブジェクトを所有しているユーザーは削除できません。

```sql
DROP USER app_user;
```

`SYS` と現在接続中の自分のアカウントは削除できません。`machsql` で別のアカウントに切り替えるには、
`CONNECT user/password;` で新しいセッションを認証するか、クライアントを再接続します。

<a id="drop-user-active-session"></a>

### アクティブセッションを持つユーザーの削除

他の管理セッションからユーザーを削除しても、そのユーザーで認証済みのセッションは直ちに終了しません。
既存セッションはログイン時のユーザー名と内部 ID を保持しますが、削除されたユーザーは新規接続できず、
`M$SYS_USERS` にも表示されません。削除前にアクティブセッションを確認し、アプリケーション接続を先に終了します。

Machbase 8.7.0 以降では、既存セッションのユーザーコンテキストを
[CURRENT_USER と SESSION_USER](../../reference/sql/functions/functions-full/#current-session-user)で確認できます。

<a id="policy-password"></a>

## パスワードポリシー

| ポリシー | 主な動作 |
|---|---|
| `NONE` | 互換性のためのデフォルト。強度・有効期限の制約なし |
| `LOW` | 長さと文字の組み合わせを検査 |
| `HIGH` | LOW の検査、最近のパスワードの再利用制限、有効期間 |

LOW と HIGH は10文字以上を要求します。大文字・小文字の検査は `ENABLE_CASE_SENSITIVE_PASSWORD` の
影響を受けます。HIGH は設定時点から90日後を `VALID_BEFORE` に記録します。

```sql
CREATE USER reader_user
  IDENTIFIED BY 'Reader#Strong123'
  PASSWORD POLICY HIGH;

ALTER USER reader_user
  IDENTIFIED BY 'Reader#Changed456'
  PASSWORD POLICY LOW;
```

ポリシーだけを変更せず、新しいパスワードも指定します。現在のポリシーと有効期限は次で確認します。

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 ORDER BY USER_ID;
```

`PWD_POLICY_LEVEL` は `0=NONE`、`1=LOW`、`2=HIGH` です。パスワードをアプリケーションに直接
記述せず、運用環境のシークレット管理手段を使ってください。全構文は
[USER/AUTH 構文](/dbms/reference/sql/syntax/user-auth-syntax/#create-drop-alter-user)を参照してください。
