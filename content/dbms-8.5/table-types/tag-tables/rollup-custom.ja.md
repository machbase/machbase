---
title: 'カスタムロールアップ：ユーザー定義集計'
type: docs
weight: 62
toc: true
---

## 概要 {#overview}

ユーザー定義の `SELECT` 集計を定期実行し、結果を対象の TAG テーブルへ追記します。

複数列、条件付き集計、階層的な集計処理に適しています。

## 標準ロールアップとの違い {#differences-from-standard-rollup}

| 項目 | 標準 | カスタム |
|---|---|---|
| 作成構文 | `CREATE ROLLUP ... ON table(column)` | `CREATE ROLLUP ... INTO (...) AS (SELECT ...)` |
| 集計ロジック | エンジンが定義 | ユーザー定義 `SELECT` |
| 保存先 | 内部テーブル | ユーザー作成 TAG テーブル |
| `WHERE` の位置 | 外側の `INTERVAL ... WHERE ...` | 内側の `SELECT ... WHERE ...` |
| 検索方法 | `rollup()` ヒント | 保存先を再集計 |
| メタデータの型 | `v$rollup.ext_type = 0/1` | `v$rollup.ext_type = 2` |

## 実行モデルと再集計 {#execution-model-and-re-aggregation}

増分の `INSERT INTO <dest> SELECT ...` の結果を保存します。

同じ時間バケットに複数の部分集計行があるため、最終的な検索ではバケットキーごとに再集計してください。

```sql
SELECT code,
       time,
       SUM(sum_price) / SUM(cnt) AS avg_price
  FROM stock_rollup_1m
 GROUP BY code, time
 ORDER BY time;
```

## 構文 {#syntax}

### カスタムロールアップの作成 {#create-custom-rollup}

```sql
CREATE ROLLUP [IF NOT EXISTS] <rollup_name>
INTO (<dest_tag_table>)
AS (
  SELECT ...
  FROM <source_tag_table>
  [WHERE ...]
  GROUP BY ...
)
INTERVAL <n> (SEC | MIN | HOUR)
[WAKEUP INTERVAL <m> (SEC | MIN | HOUR)];
```

### 制御コマンド {#control-commands}

```sql
ALTER ROLLUP <rollup_name> START;
ALTER ROLLUP <rollup_name> STOP;
ALTER ROLLUP <rollup_name> WAKEUP;
ALTER ROLLUP <rollup_name> FORCE;
DROP ROLLUP <rollup_name>;
```

注意：作成後にワーカーが自動開始されます。直後に `START` すると、開始済みエラーになる場合があります。

## 検証規則と制約 {#validation-rules-and-constraints}

### 入力元と保存先 {#source-and-destination-tables}

- 入力元は TAG テーブル 1 つだけです。
- 保存先は事前に作成した TAG テーブルである必要があります。
- ロールアップが存在する間、保存先の `DROP TABLE` は拒否されます。

### `SELECT` の制約 {#select-constraints}

- `AS (...)` の中には有効な `SELECT` を指定します。
- `FROM` に指定できるテーブルは 1 つです。
- `JOIN`、`FROM` サブクエリー、`ON/USING` は使用できません。
- `SELECT` テキストは内部上限の 1024 バイト未満である必要があります。入力元テーブル名の正規化後も、この上限を満たす必要があります。
- 結果の列数と型は、保存先と互換性が必要です。

### `WHERE` の制約 {#where-constraints}

- `SELECT` 内部の `WHERE` は使用できます。
- 入力元の BASETIME 列を `WHERE` で直接絞り込むことはできません。
- 外側の `INTERVAL ... WHERE ...` は使用できません。

### 間隔の制約 {#interval-constraints}

- `INTERVAL` は正の値です。
- `WAKEUP INTERVAL` を省略すると、`INTERVAL` と同じになります。
- `WAKEUP INTERVAL` は `INTERVAL` 以下で、`INTERVAL` を割り切れる値にします。

### `DATE_BIN` の基準時刻 {#date_bin-origin-guidance}

`DATE_BIN` の origin には有効な DATETIME を指定します。境界付近の時刻は環境やタイムゾーンによって失敗する場合があるため、余裕のある基準値を使用してください。

## 基本例 {#basic-example}

### 1）入力元と保存先 {#1-source-and-destination-tables}

```sql
CREATE TAG TABLE stock_tick (
  code      VARCHAR(20) PRIMARY KEY,
  time      DATETIME BASETIME,
  price     DOUBLE,
  volume    DOUBLE,
  bid_price DOUBLE,
  ask_price DOUBLE
);

CREATE TAG TABLE stock_rollup_1m (
  code       VARCHAR(20) PRIMARY KEY,
  time       DATETIME BASETIME,
  sum_price  DOUBLE,
  sum_volume DOUBLE,
  sum_bid    DOUBLE,
  sum_ask    DOUBLE,
  cnt        INTEGER
);
```

### 2）カスタムロールアップの作成 {#2-create-custom-rollup}

```sql
CREATE ROLLUP rollup_stock_1m
INTO (stock_rollup_1m)
AS (
  SELECT code,
         DATE_TRUNC('minute', time) AS time,
         SUM(price)                 AS sum_price,
         SUM(volume)                AS sum_volume,
         SUM(bid_price)             AS sum_bid,
         SUM(ask_price)             AS sum_ask,
         COUNT(*)                   AS cnt
    FROM stock_tick
   GROUP BY code, time
)
INTERVAL 1 MIN;
```

### 3）再集計クエリー {#3-re-aggregation-query}

```sql
SELECT code,
       time,
       SUM(sum_price)  / SUM(cnt) AS avg_price,
       SUM(sum_volume)            AS total_volume,
       SUM(sum_bid)    / SUM(cnt) AS avg_bid,
       SUM(sum_ask)    / SUM(cnt) AS avg_ask
  FROM stock_rollup_1m
 GROUP BY code, time
 ORDER BY time;
```

## OHLCV パターン（`FIRST/LAST`） {#ohlcv-pattern-firstlast}

`FIRST/LAST` では、`firsttime`、`lasttime` の補助時刻列を保持すると、再集計の正確性を確保できます。

```sql
SELECT code,
       time,
       FIRST(firsttime, open) AS open,
       MAX(high)              AS high,
       MIN(low)               AS low,
       LAST(lasttime, close)  AS close,
       SUM(volume)            AS volume,
       SUM(cnt)               AS cnt
  FROM stock_candle_1m
 GROUP BY code, time
 ORDER BY code, time;
```

## 階層化の例（1 分 → 10 分） {#hierarchical-pipeline-example-1m---10m}

保存先テーブルを、次段のロールアップの入力元にできます。

```sql
CREATE ROLLUP rollup_stock_candle_10m
INTO (stock_candle_10m)
AS (
  SELECT code,
         DATE_BIN('min', 10, time, TO_DATE('2000-01-01 00:00:00')) AS time,
         MIN(firsttime)         AS firsttime,
         MAX(lasttime)          AS lasttime,
         FIRST(firsttime, open) AS open,
         MAX(high)              AS high,
         MIN(low)               AS low,
         LAST(lasttime, close)  AS close,
         SUM(volume)            AS volume,
         SUM(cnt)               AS cnt
    FROM stock_candle_1m
   GROUP BY code, time
)
INTERVAL 10 MIN;
```

## メタデータの確認 {#metadata-check}

```sql
SELECT rollup_name,
       rollup_table,
       source_table,
       ext_type,
       enabled,
       interval_time,
       wakeup_interval,
       predicate
  FROM v$rollup
 WHERE rollup_name = 'ROLLUP_STOCK_1M';
```

- `ext_type = 2`：カスタムロールアップ
- `rollup_table`：保存先 TAG テーブル
- `interval_time`、`wakeup_interval`：間隔（ミリ秒）
- `predicate`：カスタム `SELECT` テキスト

## 運用上の注意 {#operational-notes}

- ロールアップがある間、保存先の `DROP TABLE` は拒否されます。
- 元データの修正後に再構築する場合は、[ロールアップの再構築](../rollup-rebuild/)を参照してください。
- 推奨する削除順：

```sql
ALTER ROLLUP <name> STOP;
DROP ROLLUP <name>;
DROP TABLE <dest_table>;
DROP TABLE <source_table>;
```

- `DROP TABLE ... CASCADE` は、依存するロールアップを削除します。
- カスタムロールアップの保存先テーブルは自動削除されません。必要なら別に削除します。

## 推奨事項 {#best-practices}

- 結果を取得するクエリーは再集計する形に統一します。
- `FIRST/LAST` には `firsttime`/`lasttime` の補助列を残します。
- 保存先スキーマを変更する場合は、ロールアップを停止、削除、再作成します。
- 異常値を修正したら、対象バケットを削除してから再挿入します。階層構成では必ず下位から再構築します。
- 遅延と負荷を調整するため、`WAKEUP INTERVAL` を明示します。
