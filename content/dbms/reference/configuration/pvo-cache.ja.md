---
type: docs
title: '16.2.3 PVO Cacheプロパティ辞典'
weight: 40
toc: true
---

PVO Statement Cacheは、SQLの解析・検証・最適化の結果と実行計画を再利用し、繰り返し実行するSQLの
処理コストを削減します。公開の根拠がない略語の正式名称は定義しません。Standard Editionでのみ動作します。

## プロパティ一覧

| プロパティ | デフォルト値 | 範囲 | 動的変更 | 説明 |
|----------|--------|------|----------|------|
| `PVO_CACHE_ENABLE` | 1 | 0~1 | 可 | PVO Cacheの有効化。0=無効、1=有効 |
| `PVO_CACHE_MAX_MEMORY_SIZE` | 268435456 | 32768~2^64-1 | 可 | PVO Cache全体の最大メモリ（バイト）。デフォルトは256MB |
| `PVO_CACHE_SHARD_COUNT` | 16 | 1~256 | 不可 | キャッシュのシャード数。変更にはサーバーの再起動が必要 |
| `PVO_CACHE_MAX_SQL_ENTRIES` | 0 | 0~2^64-1 | 可 | キャッシュに保持するSQLエントリーの最大数。0=無制限 |
| `PVO_CACHE_MAX_PLANS_PER_SQL` | 512 | 1~512 | 可 | SQL文1つ当たりの最大計画（ハンドル）数 |

## プロパティの詳細

### PVO_CACHE_ENABLE

PVO Statement Cacheを有効にするかどうかを設定します。

```
PVO_CACHE_ENABLE = 1
```

### PVO_CACHE_MAX_MEMORY_SIZE

PVO Cache全体が使用できる最大メモリサイズ（バイト）です。設定値は`PVO_CACHE_SHARD_COUNT`に従って均等に分配されます。

```
PVO_CACHE_MAX_MEMORY_SIZE = 536870912   # 512MB
```

### PVO_CACHE_SHARD_COUNT

キャッシュ内部のシャード数です。初期化時のみ適用されるため、変更にはサーバーの再起動が必要です。
同時接続数が多い環境では、シャード数を増やすとロック競合を軽減できます。

```
PVO_CACHE_SHARD_COUNT = 32
```

### PVO_CACHE_MAX_SQL_ENTRIES

PVO Cacheに保持できるSQLエントリーの最大数です。0は無制限です。値を設定するとシャード数に応じて分配されます。

```
PVO_CACHE_MAX_SQL_ENTRIES = 10000
```

### PVO_CACHE_MAX_PLANS_PER_SQL

1つのSQL文に対して保持できる実行計画の最大数です。同じSQLでも、バインドパラメーターの型により異なる計画が生成されることがあります。

```
PVO_CACHE_MAX_PLANS_PER_SQL = 256
```

## 動的変更

サーバーを再起動せずに変更できるプロパティは、`ALTER SYSTEM SET`で適用します。

```sql
-- PVO Cacheを有効化
ALTER SYSTEM SET PVO_CACHE_ENABLE = 1;

-- 最大メモリを512MBに変更
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 536870912;

-- SQLエントリー数を制限
ALTER SYSTEM SET PVO_CACHE_MAX_SQL_ENTRIES = 5000;
```

## キャッシュの初期化

PVO Cacheを強制的に初期化するには、次のコマンドを使用します。

```sql
ALTER SYSTEM FLUSH PVO_CACHE;
```

## キャッシュの状態確認

```sql
SELECT name, value
  FROM v$property
 WHERE name LIKE 'PVO_CACHE%'
 ORDER BY name;
```
