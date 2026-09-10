---
type: docs
title: 'SELECTヒント'
weight: 40
toc: true
aliases:
  - /dbms/reference/sql/hint-dictionary-select/
---

SELECTヒントは`/*+ ... */`形式のコメントブロックで、オプティマイザーの動作を制御したり、サンプリングなどのデータ処理を指定したりします。

## ヒント構文

```sql
SELECT /*+ hint_clause */ ...
SELECT /*+ hint1 hint2 */ ...
```

ヒントは`SELECT`キーワードの直後の`/*+ ... */`ブロックに記述します。

## 主なヒント一覧

### 実行計画を制御するヒント

| ヒント | 構文 | 説明 |
|------|------|------|
| `PARALLEL` | `/*+ PARALLEL(table, n) */` | 並列処理係数を指定 |
| `NOPARALLEL` | `/*+ NOPARALLEL(table) */` | 並列処理を無効化 |
| `FULL` | `/*+ FULL(table) */` | インデックススキャンの代わりにフルスキャンを強制 |
| `NO_INDEX` | `/*+ NO_INDEX(table, index) */` | 特定インデックスの使用を無効化 |
| `ROLLUP_TABLE` | `/*+ ROLLUP_TABLE(rollup_table) */` | 特定ROLLUPテーブルを強制選択 |
| `RID_RANGE` | `/*+ RID_RANGE(table, start, end) */` | RID範囲を指定 |
| `SCAN_FORWARD` | `/*+ SCAN_FORWARD(table) */` | 古いレコードからスキャン（LOGテーブル） |
| `SCAN_BACKWARD` | `/*+ SCAN_BACKWARD(table) */` | 新しいレコードからスキャン（LOGテーブル） |

### データ処理ヒント

| ヒント | 構文 | 説明 |
|------|------|------|
| `SAMPLING` | `/*+ SAMPLING(SamplingRate) */` | 実数値で指定した割合に従ってデータを抽出 |

## 例

```sql
-- 8スレッドで並列処理
SELECT /*+ PARALLEL(sensor_log, 8) */ sensor, AVG(value)
  FROM sensor_log
 WHERE ts BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
               AND TO_DATE('2024-01-31', 'YYYY-MM-DD')
 GROUP BY sensor;

-- 特定インデックスを使用しない
SELECT /*+ NO_INDEX(sensor_log, idx_ts) */ *
  FROM sensor_log
 WHERE ts > TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- ROLLUPテーブルを強制選択
SELECT /*+ ROLLUP_TABLE(_rollup_tag_value_min) */
       name, rollup('min', 5, time) AS t, AVG(value)
  FROM tag
 WHERE name = 'TEMP-01'
 GROUP BY name, t;

-- 条件に一致する行を最大100,000行に制限した範囲から1%を抽出
SELECT /*+ SAMPLING(0.01) */ t_name, time, value
  FROM tag
 WHERE t_name = 'TAG_99'
 LIMIT 100000;
```

## 下位項目

- [SAMPLING hint](./sampling-hint/) — 割合を指定するサンプリングヒントの詳細

## 関連ドキュメント

- [クエリのパフォーマンスチューニング](/dbms/performance-tuning/performance-query-tuning/) — 実行計画とヒントの適用基準
