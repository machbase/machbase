---
type: docs
title: '16.6.7 権限別機能サポート表'
weight: 70
toc: true
---

Machbaseの権限は、適用範囲に応じて**データベース権限**と**テーブル権限**に分かれます。

## データベース権限

データベース権限は、指定したアクティブデータベースの範囲に適用します。`MOUNT`は
`MACHBASEDB`に付与します。マウント済みデータベースへのアクセスには、`USAGE`と
テーブルの`SELECT`権限を個別に付与します。

| 権限 | 許可する操作 | デフォルトで保有 |
|------|-------------|:--------:|
| `CONNECT` | アクティブデータベースへの接続、`USE`、オブジェクトの探索 | O（MACHBASEDB互換） |
| `CREATE` | テーブル、ビュー、インデックス、ロールアップ、テーブルスペース、保持ポリシーの作成 | O |
| `DROP` | テーブル、ビュー、インデックス、ロールアップ、テーブルスペース、保持ポリシーの削除 | O |
| `ALTER` | テーブル構造の変更、`ALTER SYSTEM`の実行 | X |
| `BACKUP` | `BACKUP DATABASE`の実行 | X |
| `MOUNT` | `MOUNT DATABASE` / `UMOUNT DATABASE`の実行 | X |
| `USAGE` | マウント済みデータベースの探索 | X |
| `DDL` | CREATE + DROPの組み合わせ（複合権限） | — |
| `ALL` | CONNECT、CREATE、DROP、ALTER、BACKUPを一括付与 | — |

> 「デフォルトで保有 O」は、`CREATE USER`で作成したユーザーの`MACHBASEDB`に対する互換性維持用のデフォルト権限です。
> 他の論理データベースの権限は個別に付与します。

## テーブル権限

テーブル権限は、特定テーブルに対するDML操作を制御します。

| 権限 | 許可する操作 |
|------|-------------|
| `SELECT` | 特定テーブルのSELECTによる参照 |
| `INSERT` | 特定テーブルへのINSERT |
| `DELETE` | 特定テーブルのDELETE |
| `UPDATE` | 特定テーブルのUPDATE |

## GRANT / REVOKE構文

```sql
-- データベース権限を付与
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT CREATE ON DATABASE factory_a TO app_user;
GRANT BACKUP ON DATABASE factory_a TO backup_user;
GRANT ALL ON DATABASE factory_a TO admin_user;

-- テーブル権限を付与
GRANT SELECT ON sys.sensor_data TO reader_user;
GRANT INSERT ON sys.sensor_data TO writer_user;

-- 権限を取り消す
REVOKE SELECT ON sys.sensor_data FROM reader_user;
REVOKE BACKUP ON DATABASE factory_a FROM backup_user;
```

## 権限が必要な主な操作

| 操作 | 必要な権限の種類 | 必要な権限 |
|------|-------------|---------|
| `CREATE TABLE` | データベース | CREATE |
| `DROP TABLE` | データベース | DROP |
| `ALTER TABLE` | データベース | ALTER |
| `BACKUP DATABASE` | データベース | BACKUP |
| `MOUNT DATABASE` | データベース | MOUNT |
| テーブルのSELECT | テーブル | SELECT |
| テーブルのINSERT | テーブル | INSERT |
| テーブルのUPDATE | テーブル | UPDATE |
| テーブルのDELETE | テーブル | DELETE |

## 権限の状態確認

```sql
-- ユーザー一覧
SELECT user_name, user_id FROM m$sys_users;

-- データベース権限を参照
SELECT * FROM m$sys_grant_databases WHERE grantee = 'APP_USER';

-- テーブル権限を参照
SELECT * FROM m$sys_grant_tables WHERE grantee = 'APP_USER';
```

## 詳細リファレンス

権限モデル全体の説明と例は、[権限管理](/dbms/security-access-control/privileges/)を参照してください。
