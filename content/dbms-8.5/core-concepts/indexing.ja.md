---
type: docs
title: 'インデックスと性能'
weight: 30
toc: true
---

インデックスの仕組み、自動管理、クエリー最適化、性能調整を説明します。

## 概要 {#indexing-overview}

時系列の負荷に合わせ、テーブル型ごとに方式を使い分けます。

| 型 | インデックス | 管理 | 用途 |
|-----------|-----------|------------|---------|
| Tag | 3 階層パーティション | 自動 | sensor_id と時刻 |
| Log | LSM（任意） | 手動 | 列の高速検索 |
| Volatile | RED-BLACK ツリー | 主キーに自動 | 主キー検索 |
| Lookup | RED-BLACK（追加は任意） | 主キーに自動、追加は手動 | 列の高速検索 |

多くの場合、自動作成される構造を利用でき、手動追加は不要です。

## Tag のインデックス {#tag-table-indexing}

### 自動の 3 階層構造 {#automatic-3-level-partitioned-index}

次の構造を自動作成します。

**第 1 層：タグ名**
- 特定センサーを高速特定
- sensor_id を O(log n) で検索

**第 2 層：時刻による分割**
- 時刻範囲で分割
- 無関係な期間を読み飛ばす

**第 3 層：値（SUMMARIZED 列）**
- パーティション単位の値インデックス
- 高速な範囲検索

### 動作 {#how-it-works}

```sql
CREATE TAG TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
) WITH ROLLUP;

-- 内部で作成される構造：
-- 1．sensor_id（タグ名）のインデックス
-- 2．時刻によるパーティション
-- 3．SUMMARIZED 列の集計とインデックス
```

### クエリー最適化 {#query-optimization}

**最適な検索（3 層を使用）：**
```sql
-- 高速：sensor_id、時刻パーティション、値インデックスを使用
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN '2025-10-10 00:00:00' AND '2025-10-10 23:59:59'
  AND temperature > 25.0;
```

**良い検索（2 層を使用）：**
```sql
-- sensor_id と時刻パーティションを使用
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

**遅い検索（全表スキャン）：**
```sql
-- 全センサーを検索（sensor_id 条件なし）
SELECT * FROM sensors
WHERE temperature > 30.0;
```

### ロールアップのインデックス {#rollup-table-indexes}

ロールアップを作成すると、インデックスも利用できます。

```sql
-- ロールアップを検索（事前集計済みで高速）
SELECT rollup('hour', 1, time) AS hour_time, AVG(temperature), COUNT(temperature)
FROM sensors
WHERE sensor_id = 'sensor01'
GROUP BY hour_time;

-- 主な集計単位：秒、分、時間
```

### 推奨事項 {#best-practices}

**推奨：**
- WHERE に sensor_id を含める
- Log には `DURATION`、Tag には BASETIME 範囲を指定
- 統計にはロールアップを使用
- 基本インデックスの管理はサーバーに任せる

**避ける操作：**
- 自動管理される基本インデックスを手動で作成しようとする
- sensor_id なしで全体をスキャン
- ロールアップで十分なのに元データを集計

## Log のインデックス {#log-table-indexing}

### 任意の LSM {#lsm-index-optional}

必要に応じて LSM（Log-Structured Merge）を作成できます。

```sql
-- Log テーブルを作成
CREATE TABLE app_logs (
    level VARCHAR(10),
    component VARCHAR(50),
    message VARCHAR(2000)
);

-- 頻用する検索列に LSM を作成
CREATE INDEX idx_level ON app_logs(level);
CREATE INDEX idx_component ON app_logs(component);
```

### 作成する場合 {#when-to-create-indexes}

**追加を検討する条件：**
- WHERE に頻繁に使う列
- 検索が遅い
- カーディナリティーが中程度

**省略を検討する条件：**
- 時刻だけの検索
- カーディナリティーが非常に高い
- 書き込み性能を最優先

### LSM の特性 {#lsm-index-characteristics}

**利点：**
- 書き込み中心の負荷に最適化
- 書き込みをブロックしない
- 自動的に保守

**動作：**
1. メモリバッファーに入力
2. ディスクセグメントへ定期フラッシュ
3. バックグラウンドでマージ
4. 複数セグメントを横断して検索

### インデックスの構築 {#index-building}

```sql
-- インデックスの状態を確認
SHOW INDEXES;

-- インデックス構築の進捗を確認
SHOW INDEXGAP;

-- バックグラウンドで構築（ブロックしない）
```

### 検索の最適化 {#query-optimization-1}

**インデックスを使用：**
```sql
-- 高速：idx_level を使用
SELECT * FROM app_logs
WHERE level = 'ERROR'
DURATION 1 HOUR;
```

**キーワードインデックスが必要：**
```sql
-- SEARCH には KEYWORD インデックスが必要
CREATE INDEX idx_message ON app_logs(message) INDEX_TYPE KEYWORD;

SELECT * FROM app_logs
WHERE message SEARCH 'timeout'
DURATION 1 HOUR;
```

## Volatile のインデックス {#volatile-table-indexing}

### 自動の RED-BLACK ツリー {#automatic-red-black-tree}

PRIMARY KEY にメモリ内インデックスを自動作成します。

```sql
CREATE VOLATILE TABLE device_status (
    device_id INTEGER PRIMARY KEY,  -- 自動的にインデックスを作成
    status VARCHAR(20),
    last_updated DATETIME
);
```

### 性能特性 {#performance-characteristics}

- **検索**：主キーで O(log n)
- **挿入**：O(log n)
- **更新**：O(log n)
- **削除**：O(log n)

すべてメモリ内で処理します。

### 検索の最適化 {#query-optimization-2}

**高速：**
```sql
-- PRIMARY KEY インデックスを使用
SELECT * FROM device_status WHERE device_id = 101;
UPDATE device_status SET status = 'RUNNING' WHERE device_id = 101;
DELETE FROM device_status WHERE device_id = 101;
```

**比較的低速：**
```sql
-- 全表スキャン（status にインデックスなし）
SELECT * FROM device_status WHERE status = 'ERROR';
```

## Lookup のインデックス {#lookup-table-indexing}

### RED-BLACK インデックス {#lsm-index-same-as-log-table}

```sql
CREATE LOOKUP TABLE devices (
    device_id INTEGER PRIMARY KEY,
    device_name VARCHAR(100),
    location VARCHAR(200)
);

-- 頻用する検索列にインデックスを作成
CREATE INDEX idx_location ON devices(location);
```

主キーには自動で作成されます。検索列への追加インデックスは、Log と同様に検索頻度を基に検討します。

## 時刻による分割 {#time-based-partitioning}

### 自動分割 {#automatic-partitioning}

Tag と Log は時刻を考慮した保存方式で範囲検索を効率化します。Lookup は
永続的な参照テーブルで、主キーと任意の追加インデックスで最適化します。

```
パーティション構成の模式図：
┌──────────────────────────────────────┐
│ 分割 1：第 1 週（10 月 1～7 日）    │
│   - この週のデータ                   │
│   - 個別のインデックス               │
│   - 最適化した圧縮                   │
├──────────────────────────────────────┤
│ 分割 2：第 2 週（10 月 8～14 日）   │
│   - この週のデータ                   │
│   - 個別のインデックス               │
│   - 最適化した圧縮                   │
├──────────────────────────────────────┤
│ 分割 3：第 3 週（10 月 15～21 日）  │
│   - 入力中の分割                     │
│   - 入力用に圧縮を抑制               │
└──────────────────────────────────────┘
```

### 利点 {#benefits}

**検索性能：**
- 関連するパーティションだけをスキャン
- 範囲外の過去や未来の分割を除外
- 並列スキャン

**データ管理：**
- 古いパーティションの削除で保持期間を管理
- 分割ごとの圧縮
- 効率的なバックアップと復元

### 検索の最適化 {#query-optimization-3}

**良い例（1 パーティション）：**
```sql
SELECT * FROM logs DURATION 1 DAY;
```

**比較的遅い例（複数パーティション）：**
```sql
SELECT * FROM logs DURATION 30 DAY;
```

**非常に遅い例（全パーティション）：**
```sql
SELECT * FROM logs;  -- 時刻条件なし
```

## 最適化の方針 {#query-optimization-strategies}

### 1．時刻条件を使用 {#1-always-use-time-filters}

**避ける例：**
```sql
SELECT * FROM sensors WHERE sensor_id = 'sensor01';
```

**推奨：**
```sql
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 2．`DURATION` を使用 {#2-use-duration-keyword}

**推奨（専用構文）：**
```sql
SELECT * FROM logs DURATION 1 HOUR;
```

**比較的効率が低い例（手動条件）：**
```sql
SELECT * FROM logs
WHERE _arrival_time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
                        AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 3．分析にはロールアップを使用 {#3-query-rollup-not-raw-data}

以下の例は時間条件と集計単位が異なります。性能を比較する場合は、同じ条件・同じ集計単位にそろえてください。

**推奨（一致するロールアップがある場合）：**
```sql
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN TO_DATE('2025-10-01', 'YYYY-MM-DD')
               AND TO_DATE('2025-10-08', 'YYYY-MM-DD');

SELECT rollup('hour', 1, time) AS hour_time, AVG(temperature)
FROM sensors
WHERE sensor_id = 'sensor01'
GROUP BY hour_time;
```

**遅い例（数百万行）：**
```sql
SELECT sensor_id, AVG(temperature)
FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN TO_DATE('2025-10-01', 'YYYY-MM-DD')
               AND TO_DATE('2025-10-08', 'YYYY-MM-DD')
GROUP BY sensor_id;
```

### 4．結果セットを制限 {#4-limit-result-sets}

**推奨：**
```sql
SELECT * FROM logs DURATION 1 HOUR LIMIT 1000;
```

**避ける例：**
```sql
SELECT * FROM logs;  -- 数百万行を返してしまう
```

### 5．絞り込みに有効な列にインデックス {#5-use-indexes-on-high-selectivity-columns}

**良い例（中程度のカーディナリティー）：**
```sql
-- level：ERROR、WARN、INFO（低カーディナリティーで適する）
CREATE INDEX idx_level ON logs(level);
```

**避ける例（非常に高いカーディナリティー）：**
```sql
-- message：数百万の異なる値（インデックスを避ける）
CREATE INDEX idx_message ON logs(message);  -- この使い方は避ける
```

## 圧縮 {#compression}

### 自動圧縮 {#automatic-compression}

次の圧縮を自動適用します。

**論理圧縮（列指向）：**
- 列ごとに圧縮
- パターンに基づく圧縮
- 10～100 倍の圧縮率

**物理圧縮（ブロック）：**
- ディスクブロックを圧縮
- ユーザーからは透過的
- 追加で 2～5 倍の圧縮

### 圧縮特性 {#compression-characteristics}

| 型 | 方法 | 一般的な圧縮率 |
|-----------|-------------------|---------------|
| Tag | 列とブロック | 50～100 倍 |
| Log | 列とブロック | 10～50 倍 |
| Volatile | なし（メモリ内） | 1 倍 |
| Lookup | ブロック | 2～5 倍 |

### 性能への影響 {#impact-on-performance}

**読み取り：**
- I/O が減り、高速化
- 展開の負荷は小さい
- 大規模スキャンで効果

**書き込み：**
- 先にメモリに蓄積
- フラッシュ時に圧縮
- 入力時の圧縮待ちを回避

## 性能の監視 {#performance-monitoring}

### テーブル統計の確認 {#check-table-statistics}

```sql
-- テーブル情報を表示
SHOW TABLE sensors;

-- ストレージ使用量を表示
SHOW STORAGE;

-- テーブルスペース情報を表示
SHOW TABLESPACES;
```

### クエリーの監視 {#monitor-queries}

```sql
-- 実行中のクエリーを表示
SHOW STATEMENTS;

-- 遅いクエリーを確認
-- 長時間実行中のクエリーを確認できる
```

### インデックスの状態 {#index-health}

```sql
-- インデックスを確認
SHOW INDEXES;

-- インデックス構築の進捗を確認
SHOW INDEXGAP;
```

## 性能調整 {#performance-tuning}

### サーバー設定 {#server-configuration}

machbase.conf の主なパラメーター：

```properties
# メモリ設定
PROCESS_MAX_SIZE = 8G                         # プロセスのメモリ上限
VOLATILE_TABLESPACE_MEMORY_MAX_SIZE = 1G      # Volatile のメモリ
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE = 2G # ディスクテーブルのメモリ

# 書き込み性能
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 600
DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC = 600

# 検索性能
MAX_QPX_MEM = 512M             # クエリーごとのメモリ上限
SESSION_QUERY_TIMEOUT_SEC = 60 # クエリータイムアウト。0 は無効
```

### アプリケーションの最適化 {#application-optimization}

**一括書き込みの概略（引数を省略した疑似コード）：**
```c
// 一括入力には APPEND を使用
SQLAppendOpen(stmt, "sensors");
for (int i = 0; i < 10000; i++) {
    SQLAppendDataV(stmt, sensor_id, time, value);
}
SQLAppendClose(stmt);  // バッチを反映
```

**コネクションプール：**
- 接続を再利用
- 接続のオーバーヘッドを削減
- 一般的には 10～20 接続

**結果件数の制限：**
```sql
-- UI の検索では結果件数を制限
SELECT * FROM logs DURATION 1 HOUR LIMIT 100;
```

## よくある性能問題 {#common-performance-issues}

### 1．時刻条件がなく遅い {#issue-1-slow-queries-without-time-filter}

**問題：**
```sql
SELECT * FROM sensors WHERE sensor_id = 'sensor01';
-- 低速：全パーティションを検索
```

**対処：**
```sql
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 2．分析で元データを集計 {#issue-2-querying-raw-data-for-analytics}

元データの例は期間全体の平均、ロールアップの例は時間単位の平均です。必要な集計単位に合わせて使用してください。

**問題：**
```sql
SELECT AVG(temperature)
FROM sensors
WHERE time BETWEEN TO_DATE('2025-10-01', 'YYYY-MM-DD')
               AND TO_DATE('2025-10-08', 'YYYY-MM-DD');
-- 低速：数百万行を集計
```

**対処：**
```sql
SELECT rollup('hour', 1, time) AS hour_time, AVG(temperature)
FROM sensors
WHERE time BETWEEN TO_DATE('2025-10-01', 'YYYY-MM-DD')
               AND TO_DATE('2025-10-08', 'YYYY-MM-DD')
GROUP BY hour_time;  -- 一致するロールアップがあれば高速
```

### 3．Log のインデックス不足 {#issue-3-missing-indexes-on-log-tables}

**問題：**
```sql
-- インデックスなしでは低速
SELECT * FROM logs WHERE level = 'ERROR' DURATION 1 DAY;
```

**対処：**
```sql
CREATE INDEX idx_level ON logs(level);
-- インデックスにより高速化
```

### 4．大きな結果セット {#issue-4-large-result-sets}

**問題：**
```sql
SELECT * FROM logs DURATION 30 DAY;
-- 数百万行を返してしまう
```

**対処：**
```sql
-- 代わりに集計する
SELECT level, COUNT(*) FROM logs
DURATION 30 DAY
GROUP BY level;

-- または結果件数を制限
SELECT * FROM logs DURATION 30 DAY LIMIT 1000;
```

## 推奨事項の一覧 {#best-practices-summary}

1. `DURATION` または時刻範囲を指定
2. Tag の分析にはロールアップを使用
3. Log/Lookup の頻用する検索列にインデックスを作成
4. LIMIT で結果を制限
5. APPEND で一括入力
6. Tag/Volatile の基本インデックスはサーバー管理に任せる
7. SHOW STATEMENTS で検索性能を監視
8. 古いデータを削除し、保持期間を管理

## 次のステップ {#next-steps}

- [SELECT](../../sql-reference/select/)：最適化の適用
- [テーブルの種類](../../table-types/)：詳細
- [トラブルシューティング](../../troubleshooting/)：性能問題

## 要点 {#key-takeaways}

1. Tag は 3 階層の自動パーティションインデックス
2. Log には LSM、Lookup には RED-BLACK の追加インデックス
3. Volatile は自動のメモリ内インデックス
4. 時刻による分割は自動で行われる
5. 時刻条件を指定して性能を改善
6. 分析には事前集計を使用
7. 多くの基本インデックスは自動管理

---

仕組みを理解し、実際の検索性能を確認しながら調整してください。
