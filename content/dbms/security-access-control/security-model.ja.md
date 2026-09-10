---
type: docs
title: '14.1 セキュリティモデルの概要'
weight: 10
toc: true
---

Machbase のセキュリティモデルは、**ユーザーアカウント**、**権限（GRANT/REVOKE）**、
**アクセス制御（IP/認証）**を階層的に組み合わせた構造です。

## Machbase のセキュリティ構造

```
クライアントの接続要求
        │
        ▼
┌────────────────────────────┐
│ アクセス制御               │  BIND_IP_ADDRESS, GRANT_REMOTE_ACCESS
│ （ネットワーク層）         │
└────────┬───────────────────┘
         │ 許可
         ▼
┌────────────────────────────┐
│ 認証                       │  パスワード認証または AUTH KEY（公開鍵）認証
│ （ユーザー識別）           │
└────────┬───────────────────┘
         │ 認証成功
         ▼
┌────────────────────────────┐
│ 権限確認                   │  GRANT/REVOKE で付与した権限を確認
│ （操作許可の判定）         │  テーブル権限 + データベース権限
└────────────────────────────┘
```

接続要求はまずネットワークアクセス制御を通過し、次にユーザー認証を行い、最後に操作に必要な
権限が付与されているかを確認します。

## 初期アカウント: SYS

インストール時に `SYS` アカウントが自動作成されます。SYS はスーパーユーザーとしてすべての
データベース操作を実行でき、他のユーザーの作成と権限付与を行います。

| 項目 | 内容 |
|------|------|
| アカウント名 | `SYS` |
| 初期パスワード | `MANAGER` |
| 権限 | 全権限（スーパーユーザー） |
| 削除 | 不可 |

> **運用環境で必須の対応**: インストール直後に SYS の初期パスワード（`MANAGER`）を変更してください。
>
> ```sql
> ALTER USER SYS IDENTIFIED BY '新しい_パスワード';
> ```

<a id="상세-정본"></a>

## 関連文書

- ユーザーのライフサイクルとパスワードポリシー: [アカウント管理](../account/)
- データベース・テーブル権限と GRANT/REVOKE: [権限管理](../privileges/)
- 公開鍵の登録・ローテーション: [AUTH KEY 認証](../authentication-auth-key/)
- リモート接続とリスナー: [アクセス制御](../access-control/)

アカウント作成、権限付与、認証設定は別々の作業です。以下のアカウントとテーブルを用意し、
各アカウントで接続し直して、許可した操作と制限した操作を確認してください。

## 最小権限の原則

運用環境では次の原則を適用します。

- **SYS は管理専用**: 日常のデータ検索や入力に SYS を使わないでください。
- **用途別アカウント**: 読み取り、入力、デプロイ（DDL）、バックアップのアカウントを分けます。
- **テーブル単位の制限**: 必要なテーブルに必要な DML 権限だけを付与します。
- **定期点検**: 不要アカウントを削除し、過剰権限のアカウントを確認します。

```sql
-- 読み取り専用アカウント
CREATE USER reader IDENTIFIED BY 'Reader#Strong123';
GRANT SELECT ON sys.sensor_log TO reader;

-- 入力専用アカウント
CREATE USER writer IDENTIFIED BY 'Writer#Strong123';
GRANT SELECT, INSERT ON sys.sensor_log TO writer;

-- DDL 専用アカウント（テーブルの作成・削除）
CREATE USER deploy IDENTIFIED BY 'Deploy#Strong123';
GRANT CONNECT ON DATABASE factory_a TO deploy;
GRANT DDL ON DATABASE factory_a TO deploy;
```
