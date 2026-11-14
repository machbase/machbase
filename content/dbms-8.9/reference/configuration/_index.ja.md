---
type: docs
title: '16.2 設定リファレンス'
weight: 20
toc: true
---

Machbaseサーバーは、`$MACHBASE_HOME/conf/machbase.conf`に定義されたプロパティで動作を制御します。
このセクションでは、各プロパティの許容範囲とデフォルト値を確認できます。

## 下位セクション

| セクション | 説明 |
|------|------|
| [設定プロパティ辞典](./configuration/) | サーバーの基本設定、性能、セキュリティ、ログなど、Standard Editionの全プロパティ一覧 |
| [クラスター設定プロパティ辞典](./configuration-2/) | Cluster Edition専用のCoordinator、Broker、Warehouse設定 |
| [PVO Cacheプロパティ辞典](./pvo-cache/) | SQL実行計画キャッシュ（PVO Statement Cache）のプロパティ |
| [タイムゾーン設定辞典](./configuration-timezone/) | タイムゾーンのプロパティとクライアント別の設定方法 |

## プロパティの確認方法

サーバー実行中のプロパティ値は、`v$property`システムビューで確認します。

```sql
-- すべてのプロパティを参照
SELECT name, value, type FROM v$property ORDER BY name;

-- 特定のプロパティを参照
SELECT name, value, min, max
  FROM v$property
 WHERE name = 'PORT_NO';
```

## 動的に変更できるプロパティ

一部のプロパティは、サーバーを再起動せずに`ALTER SYSTEM SET`で変更できます。

```sql
ALTER SYSTEM SET TRACE_LOG_LEVEL = 3;
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 536870912;
```

変更後に`v$property`を参照して適用を確認します。再起動が必要なプロパティを動的に変更すると、エラーが返されます。
