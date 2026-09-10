---
type: docs
title: '時系列データの理解'
weight: 10
toc: true
---

時系列データの特徴と、Machbase が効率よく処理する仕組みを説明します。

## 時系列データとは {#what-is-time-series-data}

時刻を軸として並ぶデータです。各レコードは、タイムスタンプと 1 つ以上の値を持ちます。

```
(timestamp, value1, value2, ...)
```

### 一般的な例 {#common-examples}

**IoT とセンサー：**
- 毎秒の温度測定
- 車両の GPS 座標
- スマートメーターの電力使用量
- 製造装置のテレメトリー

**アプリケーション監視：**
- サーバーの CPU とメモリの指標
- アプリケーションログ
- HTTP リクエストログ
- DB クエリーの性能

**業務データ：**
- 株式のティックデータ
- 販売取引
- Web のクリックストリーム
- モバイルアプリのイベント

## ワークロードの特徴 {#characteristics-of-time-series-workloads}

### 1．書き込み中心 {#1-write-heavy}

書き込みが大部分を占めます。
- センサー、ログ、イベントを毎秒数百万件入力
- 過去のデータはほとんど変わらず、更新や削除が少ない
- 常に新しいデータを追加する追記パターン

従来型 DB での課題：
- 行ロックで書き込みが遅くなる
- 複雑な UPDATE 処理が不要な用途でも存在する
- トランザクションのオーバーヘッド

**Machbase の対応**：行ロックのない追記専用設計。

### 2．時刻による検索 {#2-time-based-queries}

多くのクエリーが時刻範囲を指定します。

```sql
-- 直近 1 時間
SELECT * FROM logs DURATION 1 HOUR;

-- 指定した日時範囲の統計
SELECT AVG(temperature) FROM sensors
WHERE time BETWEEN '2025-10-09 00:00:00' AND '2025-10-10 00:00:00';
```

従来型 DB での課題：
- 汎用インデックスは時刻に特化していない
- 期間検索が全表スキャンになる場合がある
- 時刻を考慮した分割がない

**Machbase の対応**：時刻ベースの分割とインデックスを組み込み。

### 3．最近のデータを重視 {#3-recent-data-focus}

最近の情報がよく利用されます。
- 監視：直近 24 時間
- 傾向分析：直近 1 週間
- 過去データ：監査やアーカイブ

従来型 DB での課題：
- 新旧のデータを同じように扱う
- 自動的な保存期間管理がない
- アーカイブが手作業

**Machbase の対応**：DURATION、自動分割、効率的な時刻ベースの削除。

### 4．高い圧縮効果 {#4-high-compression-potential}

時系列データは圧縮に適しています。
- 連続するタイムスタンプ
- 繰り返しパターン
- 似た値

従来型 DB での課題：
- 行指向の保存
- 汎用的な圧縮
- 一般的な圧縮率は 2 ～ 5 倍

**Machbase の対応**：列指向の専用圧縮（10 ～ 100 倍）。

### 5．大量データの集計 {#5-bulk-aggregations}

主な分析処理：
- 時間ウィンドウごとの MIN、MAX、AVG
- 時間間隔ごとのグループ化
- 統計集計

従来型 DB での課題：
- 検索のたびに集計
- 事前計算の統計がない
- 大量データでは低速

**Machbase の対応**：ロールアップを定義すると、
事前計算した統計を利用可能。

## 従来型データベースの課題 {#why-traditional-databases-fail}

### 1．行指向ストレージ {#problem-1-row-oriented-storage}

従来型は、行全体をまとめて保存します。

```
行 1： [timestamp1, sensor_id, temp, humidity]
行 2： [timestamp2, sensor_id, temp, humidity]
行 3： [timestamp3, sensor_id, temp, humidity]
```

**課題**：AVG(temperature) でも、温度以外を含む全列を読み取ります。

**Machbase**：列指向で必要な列だけを読み取ります。

### 2．B ツリーインデックス {#problem-2-b-tree-indexes}

従来型の B ツリーには次の特性があります。
- ランダムアクセスに適する
- 順次書き込みのコストが高い
- 時刻順のデータに特化していない

**Machbase**：LSM と時刻による分割を使用します。

### 3．ACID のオーバーヘッド {#problem-3-acid-overhead}

一般的な ACID の実装には、次が含まれます。
- 行ロック
- トランザクションログ
- ロールバック

**追記中心の時系列では不要な処理：**
- 過去データの更新
- 同じ行への同時更新
- そのためのオーバーヘッド

**Machbase**：追記専用の用途に向けて設計を単純化します。

### 4．時刻への特化がない {#problem-4-no-time-awareness}

汎用 DB では、次が標準で備わらない場合があります。
- 時刻ベースの自動分割
- 組み込みの保持ポリシー
- 時刻検索の最適化

**Machbase**：時刻を中心に設計しています。

## Machbase の設計原則 {#machbase-design-principles}

### 1．追記専用アーキテクチャー {#1-append-only-architecture}

データを追加し、既存の行は更新しません。

```sql
-- 許可：新しいデータの追加
INSERT INTO sensors VALUES ('sensor01', NOW, 25.3);

-- Tag/Log では不可：既存データの更新
UPDATE sensors SET temperature = 26.0 WHERE id = 123;  -- ✗
```

**利点：**
- 行ロックなし
- 毎秒数百万件の高速書き込み
- 履歴の上書きを防ぐ

### 2．時刻による分割 {#2-time-based-partitioning}

時刻に基づいて自動分割します。

```
分割 1： 2025-10-01 ～ 2025-10-07
分割 2： 2025-10-08 ～ 2025-10-14
分割 3： 2025-10-15 ～ 2025-10-21
```

**利点：**
- 関連するパーティションだけを検索
- 古いパーティションを削除し、保持期間を管理
- パーティションごとの圧縮を最適化

### 3．列指向の圧縮 {#3-columnar-compression}

列ごとに分けて保存します。

```
タイムスタンプ：    [100, 101, 102, 103, 104, ...]
センサー ID：    [s01, s01, s01, s02, s02, ...]
温度：  [22.5, 22.7, 22.6, 21.3, 21.5, ...]
```

**利点：**
- 似た値による高圧縮
- 必要な列だけを読み取り
- 高速な分析

### 4．書き込みに適したインデックス {#4-write-optimized-indexes}

LSM（Log-Structured Merge）：
- 順次書き込みに最適化
- メモリへまとめて書き込み
- 定期的にディスクへマージ

**利点：**
- 毎秒数百万件の書き込み
- 書き込み処理の効率化
- 安定した性能

### 5．自動統計（ロールアップ） {#5-automatic-statistics-rollup}

Tag で有効にすると、統計を生成します。

```sql
-- 元データ：数百万行
INSERT INTO sensors VALUES ('sensor01', NOW, 25.3);

-- ロールアップ式：秒、分、時間のバケット
SELECT rollup('hour', 1, time) AS hour_time, AVG(value), COUNT(value)
FROM sensors
GROUP BY hour_time;
```

**利点：**
- 即座の分析
- 手動集計が不要
- 検索時間の削減

## 従来型との比較 {#time-series-vs-traditional-databases}

| 機能 | 従来型 DB | Machbase |
|---------|---------------|----------|
| 主な用途 | トランザクション | 分析 |
| 書き込み | ランダム | 順次 |
| UPDATE | 全面対応 | 制限あり |
| インデックス | B ツリー | LSM とパーティション |
| 保存形式 | 行指向 | 列指向 |
| 圧縮率 | 2～5 倍 | 10～100 倍 |
| 書き込み速度 | 毎秒数千 | 毎秒数百万 |
| 時刻検索 | 汎用 | 最適化済み |
| 保持期間 | 手動 | 自動 |

## データのパターン {#time-series-data-patterns}

### 1．高頻度センサー {#pattern-1-high-frequency-sensors}

```
センサー ID： sensor01
頻度：毎秒 10 回
データ量：1 日 864,000 件
```

**適した型**：SUMMARIZED 列を 1 つ持つ Tag

```sql
CREATE TAG TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP;
```

### 2．イベントストリーム {#pattern-2-event-streams}

```
種類：アプリケーションログ
頻度：変動あり（突発的）
データ量：1 日数百万件
スキーマ：柔軟（多数の列）
```

**適した型**：Log

```sql
CREATE TABLE app_logs (
    level VARCHAR(10),
    message VARCHAR(2000),
    user_id INTEGER
);
```

### 3．リアルタイムの状態 {#pattern-3-real-time-state}

```
種類：リアルタイムダッシュボード
頻度：継続的な更新
データ量：少量（数百行）
永続性：不要
```

**適した型**：Volatile

```sql
CREATE VOLATILE TABLE live_status (
    device_id INTEGER PRIMARY KEY,
    status VARCHAR(20),
    last_updated DATETIME
);
```

### 4．ディメンションデータ {#pattern-4-dimension-data}

```
種類：デバイスメタデータ
頻度：まれに更新
データ量：少量（数千行）
永続性：必要
```

**適した型**：Lookup

```sql
CREATE LOOKUP TABLE devices (
    device_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(200)
);
```

## よくある課題 {#common-time-series-challenges}

### 1．データ量 {#challenge-1-data-volume}

**課題**：センサーが 1 日に数百万件を生成

**Machbase の対応：**
- APPEND による高速取り込み
- 自動圧縮（10～100 倍）
- 時刻に基づく保持期間

```sql
-- 1 タグの古いデータを削除
DELETE FROM sensors
WHERE sensor_id = 'sensor01'
  AND time < TO_DATE('2025-01-01', 'YYYY-MM-DD');
```

### 2．検索性能 {#challenge-2-query-performance}

**課題**：数百万行の分析に時間がかかる

**Machbase の対応：**
- ロールアップ設定時の統計
- 時刻による分割
- 列指向の保存

```sql
-- 高速：時間バケットの検索
SELECT rollup('hour', 1, time) AS hour_time, AVG(value)
FROM sensors
GROUP BY hour_time;
```

### 3．遅れて到着するデータ {#challenge-3-late-arriving-data}

**課題**：入力順が時刻順と異なる

**Machbase の対応：**
- LSM による順序外の書き込み処理
- バックグラウンドのマージ
- 一貫した検索結果

### 4．複数のタイムゾーン {#challenge-4-multiple-time-zones}

**課題**：各地でタイムゾーンが異なる

**Machbase の対応：**
- UTC で保存し、ローカル時刻で表示
- タイムゾーン変換関数
- クライアント単位のタイムゾーン設定

```bash
machsql -z +0900  # 韓国のタイムゾーン
```

## 推奨事項 {#best-practices}

### 1．適切なテーブル型 {#1-use-appropriate-table-types}

データの特性に合わせます。
- 定期的なセンサー測定 → Tag
- 可変のイベント → Log
- リアルタイム更新 → Volatile
- 参照データ → Lookup

### 2．保持期間の設定 {#2-implement-data-retention}

必要な期間に応じてデータを削除します。

```sql
-- 日次の削除ジョブ
DELETE FROM logs EXCEPT 90 DAY;
```

### 3．DURATION の使用 {#3-use-duration-for-time-queries}

期間指定に最適化した構文を使用します。

```sql
-- 推奨
SELECT * FROM logs DURATION 1 HOUR;

-- 比較的効率が低い例
SELECT * FROM logs
WHERE _arrival_time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
                        AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 4．書き込みの一括化 {#4-batch-writes-when-possible}

一括入力に APPEND を使用します。
- 高スループット
- 圧縮の改善
- オーバーヘッドの削減

### 5．分析にはロールアップを使用 {#5-query-rollup-not-raw-data}

事前集計したデータを検索します。

```sql
-- ロールアップによる時間単位の集計
SELECT rollup('hour', 1, time) AS hour_time, AVG(temperature)
FROM sensors
GROUP BY hour_time;

-- 元データの全期間の平均（上の例とは集計単位が異なる）
SELECT AVG(temperature) FROM sensors;
```

## 次のステップ {#next-steps}

続けて、次を確認してください。

1. [テーブルの種類](../table-types-overview/)：適切な選択
2. [インデックスと性能](../indexing/)：検索の最適化
3. [Tag テーブル](../../table-types/tag-tables/)：実践

## 要点 {#key-takeaways}

1. 時系列は書き込みが多く、時刻を重視する
2. 汎用 DB は時系列専用に最適化されていない
3. Machbase は追記中心の設計
4. 列指向で高い圧縮率を実現
5. 時刻による分割で検索を最適化
6. ロールアップを設定すると高速な分析が可能
7. データのパターンに合うテーブルを選ぶ

---

基礎を理解すると、用途に適した構成を設計できます。
