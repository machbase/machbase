---
type: docs
title: '14.6 セキュリティ設定チェックリスト'
weight: 60
toc: true
---

運用デプロイ前と定期監査時に、次を点検します。

## アカウントと認証

- インストール直後に、組織のシークレット管理手順で `SYS` の初期パスワードを変更します。
- アプリケーション専用アカウントを作り、通常接続に `SYS` を使わないでください。
- パスワードをソースコード、文書、コマンド履歴に保存しないでください。
- 未使用アカウントと有効期限が近いアカウントを確認します。
- AUTH KEY を使う場合、秘密鍵の保管・交換・廃棄の担当者を決めます。

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 ORDER BY USER_ID;

SELECT USER_NAME, KEY_ID, KEY_ALGO, KEY_PARAM, ACTIVATED, VALID_BEFORE
  FROM V$USER_AUTH_KEYS
 ORDER BY USER_NAME, KEY_ID;
```

## 権限

- 各論理データベースに必要な `CONNECT` だけを付与します。
- 読み取り用アカウントに書き込み・DDL・バックアップ権限がないことを確認します。
- 一時権限の期限と取り消し責任者を記録します。
- ユーザーやテーブルを再作成した後は権限を再検証します。

```sql
SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 ORDER BY USER_NAME, DB_NAME, OWNER_NAME, TABLE_NAME;
```

`PRIV` はビットマスクです。数値を権限名へ変換する独自ツールは、稼働中バージョンの定義と
照合して検証してください。付与・取り消しは[権限管理](../privileges/)を参照します。

## ネットワーク接続

- リモート接続が必要かを先に決めます。
- `BIND_IP_ADDRESS` を必要な IPv4 インターフェースに限定します。
- ファイアウォールまたはセキュリティグループの接続元許可リストを確認します。
- 設定変更は、再起動と接続検証を含むメンテナンス手順で実施します。

```sql
SELECT NAME, VALUE
  FROM V$PROPERTY
 WHERE NAME IN ('GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS');
```

## 変更後の証跡

セキュリティ変更後、次の結果を変更記録に残します。

1. ユーザーと有効期限の検索結果
2. 対象ユーザーとデータベース・テーブル権限の検索結果
3. 許可したアドレスからの接続成功と、許可していないアドレスからの遮断結果
4. AUTH KEY を変更した場合、新しい鍵での接続成功と古い鍵での遮断結果

共有の運用サーバーで `SYS` パスワード、リスナー、ファイアウォールを試験目的で変更しないでください。
別の検証環境で復旧経路まで確認してから、運用変更を承認します。
