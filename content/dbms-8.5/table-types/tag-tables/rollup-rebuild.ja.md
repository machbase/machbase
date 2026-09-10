---
title: 'ロールアップの再構築'
type: docs
weight: 63
toc: true
---

## 概要 {#overview}

異常値を収集した場合、元データを削除して修正値を挿入できます。
ただし、作成済みのロールアップ統計は自動的には巻き戻りません。
影響を受けたバケットの再構築が必要です。

組み込みプロシージャ `EXEC ROLLUP_REBUILD(...)` を使用します。

- 標準、EXTENSION、カスタムロールアップに対応
- SQL から直接実行可能
- カスタムロールアップの依存関係に沿って停止、再構築、開始

## 制限 {#limitations}

次の制限があります。

1. Standard Edition で対応し、**Cluster Edition では未サポート**です。
2. `table_name`、`tag_name`、`begin_time`、`end_time` による単一タグの再構築だけをサポートします。
3. 部分的な時刻範囲ではなく、影響を受けるバケット全体を削除してから再挿入します。

## 再構築プロシージャ {#rollup-rebuild-procedure}

### 構文 {#syntax}

```sql
EXEC ROLLUP_REBUILD(table_name, tag_name, begin_time, end_time);
```

例：

```sql
EXEC ROLLUP_REBUILD(tag,
                    'tag-00045',
                    TO_DATE('2025-09-02 01:00:00'),
                    TO_DATE('2025-09-02 01:00:00'));

EXEC ROLLUP_REBUILD(sys.tag,
                    'tag-00045',
                    TO_DATE('2025-09-02 01:00:00'),
                    TO_DATE('2025-09-02 01:00:00'));
```

### パラメーター {#parameters}

1. `table_name`
   - 入力元 TAG テーブル名
   - 必要に応じて `schema.table` を指定
2. `tag_name`
   - 再構築するタグのキー値
3. `begin_time`
   - 修正範囲の開始時刻
4. `end_time`
   - 修正範囲の終了時刻

### 対象範囲 {#coverage}

- 標準ロールアップ
- EXTENSION ロールアップ
- カスタムロールアップ
- ロールアップに依存する階層構成

## カスタムロールアップの再構築動作 {#how-custom-rollup-rebuild-works}

### 固定 SQL では不十分な理由 {#why-fixed-built-in-sql-is-not-enough}

次の要素はすべてユーザー定義です。

- 保存先のテーブル名
- 保存先の列数と型
- 集計関数
- 入力元が元テーブルか、他のロールアップの保存先か

そのため、固定スキーマを前提とした再挿入処理では対応できません。
影響するタグと時間バケットに限定して、元のカスタム `SELECT` を再実行する必要があります。

### バケット単位への拡張 {#bucket-expansion}

1 分単位のカスタムロールアップで、次の範囲に異常があるとします。

- 元データの異常範囲：`2026-01-27 09:30:12` ～ `2026-01-27 09:31:07`

実際の再構築範囲は、バケット全体に広げます。

- 開始：`2026-01-27 09:30:00`
- 終了：`2026-01-27 09:31:59.999999999`

保存先には部分集計行が存在する場合があります。
削除せずに再挿入すると、集計が重複します。
必ず対象バケットを削除してから再挿入してください。

### 手動の再構築手順 {#manual-rebuild-procedure}

プロシージャを使わずに行う場合は、次の順に実行します。

1. 影響するカスタムロールアップをすべて停止
2. 異常のある元データを修正、または再読み込み
3. バケット境界を計算
4. 保存先の対象データを削除
5. `CREATE ROLLUP ... AS (SELECT ...)` の元の集計ロジックで再挿入
6. 保存先をフラッシュ
7. 上位のロールアップがある場合、下位から順に同じ処理を実行
8. ロールアップを開始

## 手動再構築の例 {#manual-custom-rollup-rebuild-examples}

### 1 分のカスタムロールアップ {#1-minute-custom-rollup}

`stock_tick` → `stock_rollup_1m` の `09:30` ～ `09:31` のバケットを再構築します。

```sql
STOP ROLLUP rollup_stock_1m;

DELETE FROM stock_rollup_1m
WHERE time >= TO_DATE('2026-01-27 09:30:00')
  AND time < TO_DATE('2026-01-27 09:32:00');

INSERT INTO stock_rollup_1m
SELECT code,
       DATE_TRUNC('minute', time) AS time,
       SUM(price)                 AS sum_price,
       SUM(volume)                AS sum_volume,
       COUNT(*)                   AS cnt
FROM stock_tick
WHERE time >= TO_DATE('2026-01-27 09:30:00')
  AND time < TO_DATE('2026-01-27 09:32:00')
GROUP BY code, time;

EXEC TABLE_FLUSH('stock_rollup_1m');
START ROLLUP rollup_stock_1m;
```

### `FIRST/LAST` を使用する場合 {#custom-rollup-with-firstlast}

`FIRST/LAST` の補助時刻列も再計算する必要があります。

```sql
STOP ROLLUP rollup_stock_candle_1m;

DELETE FROM stock_candle_1m
WHERE time = TO_DATE('2026-01-27 09:30:00');

INSERT INTO stock_candle_1m
SELECT code,
       DATE_TRUNC('minute', time) AS time,
       MIN(time)                  AS firsttime,
       MAX(time)                  AS lasttime,
       FIRST(time, price)         AS open,
       MAX(price)                 AS high,
       MIN(price)                 AS low,
       LAST(time, price)          AS close,
       SUM(volume)                AS volume,
       COUNT(*)                   AS cnt
FROM stock_tick
WHERE time >= TO_DATE('2026-01-27 09:30:00')
  AND time < TO_DATE('2026-01-27 09:31:00')
GROUP BY code, time;

EXEC TABLE_FLUSH('stock_candle_1m');
START ROLLUP rollup_stock_candle_1m;
```

最終取得時は引き続き `FIRST(firsttime, open)` と `LAST(lasttime, close)` で統合します。

### 階層ロールアップの順序 {#rollup-on-rollup-order}

例：

- 第 1 段：`stock_tick` → `stock_rollup_1m`
- 第 2 段：`stock_rollup_1m` → `stock_rollup_1h`

必ず下位段から再構築します。

1. `stock_rollup_1h` を停止
2. `stock_rollup_1m` を停止
3. `stock_rollup_1m` を再構築
4. `stock_rollup_1h` の対象データを削除して再構築
5. `stock_rollup_1m` を開始
6. `stock_rollup_1h` を開始

上位から再構築すると、未修復の下位結果を読み取り、不正な集計を再び保存してしまいます。

## 運用上の推奨事項 {#operational-recommendations}

1. 再構築前に、影響するバケット範囲を確認します。
2. 変更の前後で `v$rollup` の依存関係を確認します。
3. 異常範囲が複数バケットにまたがる場合、`EXEC ROLLUP_REBUILD(...)` に全範囲を渡します。
4. カスタムの保存先は追記結果を蓄積するため、必ず削除してから挿入します。
5. 階層構成は下位から上位の順に再構築します。

## 最近のデータを含めた効率的な検索 {#efficient-rollup-queries-including-recent-data}

以下の境界は例です。ロールアップが境界より前まで処理済みであることを確認し、実際の処理遅延に合わせて境界を設定してください。

標準とカスタムのどちらにも、同じ取得方式を適用できます。

基本パターン：

1. 確定した過去の範囲にはロールアップテーブルを使用
2. 最近の範囲は入力元を直接集計
3. `UNION ALL` で結合
4. 必要なら外側で再集計

### 標準の 1 分ロールアップの例 {#standard-1-minute-rollup-example}

```sql
SELECT ROLLUP('minute', 1, time) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time < DATE_TRUNC('minute', SYSDATE) - 2m
GROUP BY mtime

UNION ALL

SELECT DATE_TRUNC('minute', time) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time >= DATE_TRUNC('minute', SYSDATE) - 2m
GROUP BY mtime;
```

### 標準の 20 分集計の例 {#standard-20-minute-aggregation-example}

```sql
SELECT ROLLUP('minute', 20, time) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time < DATE_BIN('minute', 20, SYSDATE, 0) - 20m
GROUP BY mtime

UNION ALL

SELECT DATE_BIN('minute', 20, time, 0) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time >= DATE_BIN('minute', 20, SYSDATE, 0) - 20m
GROUP BY mtime;
```

### カスタムロールアップの例 {#custom-rollup-example}

同様に、確定したデータは保存先から、最近の範囲は入力元の集計から取得します。

```sql
SELECT code, time,
       SUM(sum_price) / SUM(cnt) AS avg_price
FROM (
      SELECT code, time,
             SUM(sum_price) AS sum_price,
             SUM(cnt)       AS cnt
      FROM stock_rollup_1m
      WHERE time < DATE_TRUNC('minute', SYSDATE) - 2m
      GROUP BY code, time

      UNION ALL

      SELECT code,
             DATE_TRUNC('minute', time) AS time,
             SUM(price)                 AS sum_price,
             COUNT(*)                   AS cnt
      FROM stock_tick
      WHERE time >= DATE_TRUNC('minute', SYSDATE) - 2m
      GROUP BY code, time
     )
GROUP BY code, time
ORDER BY code, time;
```
