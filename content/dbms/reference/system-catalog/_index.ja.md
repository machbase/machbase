---
type: docs
title: '16.3 システムカタログリファレンス'
weight: 30
toc: true
---

システムカタログは、Machbaseサーバーの内部メタデータと現在の運用状態をSQLで参照できる読み取り専用テーブル群です。次の2種類で構成されます。

| 種類 | 接頭辞 | 説明 |
|------|--------|------|
| メタデータテーブル | `M$` | テーブル定義、列、インデックス、ユーザーなどのスキーマ情報 |
| 仮想テーブル（動的ビュー） | `V$` | セッション、実行クエリ、メモリ、ストレージなどの現在の運用状態 |

## 共通事項

- すべてのシステムカタログテーブルは**読み取り専用**です。`INSERT`、`UPDATE`、`DELETE`はエラーを返します。
- `M$`テーブルはDDLコマンド（`CREATE`、`ALTER`、`DROP`）の実行結果を自動反映します。
- `V$`テーブルはサーバー状態をリアルタイムに反映し、クエリのたびに最新の値を返します。
- 全一覧は次のクエリで確認します。

```sql
-- 全メタデータテーブル一覧
SELECT name FROM m$tables ORDER BY name;

-- 全仮想テーブル一覧
SELECT name FROM v$tables WHERE name LIKE 'V$%' ORDER BY name;
```

## 下位セクション

| セクション | 説明 |
|------|------|
| [メタデータテーブル辞典](./meta/) | M$SYS_TABLES、M$SYS_COLUMNSなどのスキーマメタデータテーブルの詳細 |
| [仮想テーブル辞典](./virtual/) | V$SESSION、V$STMT、V$PROPERTYなどの動的ビューの詳細 |
| [TAG別統計ビュー](/dbms/tag-table-usage/query-analysis/#tag-stat-axis-schema) | `V$<TABLE>_STAT`の時間・距離軸別のスキーマと参照方法 |
| [V$ROLLUP辞典](./vrollup/) | Rollupジョブ状態ビューの列の詳細 |
| [V$STORAGE_MOUNT_*辞典](./vstorage-mount/) | マウント済みバックアップデータベースのビューの列の詳細 |
| [仮想テーブルの完全リファレンス](./virtual-table-full/) | 8.5の元の仮想テーブルリファレンスの全項目 |
