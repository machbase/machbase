---
type: docs
title: '16.3.3 V$ROLLUP辞典'
weight: 30
toc: true
---

`V$ROLLUP`は、TagデータのRollupジョブの状態をリアルタイムに表示する仮想テーブルです。Rollupの正常動作の確認や実行間隔と所要時間の監視に使用します。

## 列の詳細

| 列名 | 型 | 説明 |
|----------|------|------|
| `ID` | INTEGER | RollupジョブID |
| `ROLLUP_NAME` | VARCHAR | Rollupジョブ名 |
| `ROLLUP_TABLE` | VARCHAR | Rollup結果の保存先テーブル名 |
| `SOURCE_TABLE` | VARCHAR | 集計元のTAGテーブル名 |
| `COLUMN_NAME` | VARCHAR | 集計対象の列名 |
| `INTERVAL_TIME` | ULONG | データの集計間隔（ミリ秒） |
| `WAKEUP_INTERVAL` | ULONG | Rollupジョブの実行間隔（ミリ秒） |
| `LAST_WAKEUP_TIME` | DATETIME | 直近の実行時刻 |
| `ENABLED` | INTEGER | 有効かどうか（1: 有効、0: 無効） |
| `LAST_ELAPSED_MSEC` | DOUBLE | 直前の実行の所要時間（ミリ秒） |
| `RUN_STATE` | VARCHAR | スレッド状態（I: 初期化、S: 待機、R: 実行中） |

## RUN_STATEの値

| 値 | 説明 |
|----|------|
| `I` | 初期化中（Initializing） |
| `S` | 次回の実行を待機中（Sleeping） |
| `R` | 実行中（Running） |

## SQL例

```sql
-- 全Rollupジョブの状態確認
SELECT rollup_name, rollup_table, source_table, column_name,
       interval_time, wakeup_interval, enabled, last_elapsed_msec, run_state
  FROM v$rollup
 ORDER BY rollup_table;

-- 最後の実行時刻の確認
SELECT rollup_name, rollup_table, last_wakeup_time, last_elapsed_msec, run_state
  FROM v$rollup;

-- 無効になっているRollupの確認
SELECT rollup_name, rollup_table, source_table, enabled
  FROM v$rollup
 WHERE enabled = 0;

-- 実行に時間がかかるRollupの確認
SELECT rollup_name, rollup_table, wakeup_interval, last_elapsed_msec,
       last_elapsed_msec * 100.0 / wakeup_interval AS usage_ratio
  FROM v$rollup
 WHERE last_elapsed_msec > 0
   AND wakeup_interval > 0
 ORDER BY last_elapsed_msec DESC;
```

## 注意事項

- `INTERVAL_TIME`はデータの集計間隔、`WAKEUP_INTERVAL`はRollupジョブの実行間隔です。
- `LAST_ELAPSED_MSEC`が`WAKEUP_INTERVAL`を超えていれば、直前の実行時間が設定された実行間隔を超えています。集計対象のデータ量と実行間隔を確認してください。例の`usage_ratio`は実行間隔に対する直前の実行時間の割合（%）です。
- `ENABLED = 0`はRollupが無効であることを示します。`ALTER ROLLUP rollup_name START`で再び有効にします。`rollup_name`には参照した`ROLLUP_NAME`の値を指定します。
- Rollupの作成と管理は[TAGテーブルとRollup](/dbms/tag-rollup-usage/overview-use-criteria/#rollup)を参照してください。
