---
type: docs
title: '基本概念'
weight: 40
toc: true
---

Machbase を効果的に使うために、主要な概念を説明します。

## Machbase の特徴 {#what-makes-machbase-different}

タイムスタンプ付きで継続的に入力される時系列データに最適化されています。

- IoT センサーの測定値
- アプリケーションログ
- 製造装置のデータ
- ネットワークトラフィック
- 金融ティックデータ

特に次の用途を想定しています。
- **書き込み中心**：毎秒数百万件の挿入
- **時刻による検索**：最新データや指定期間
- **追記中心**：更新や削除が少ないデータ

## 4 種類のテーブル {#the-four-table-types}

用途に合うテーブル型を選ぶことが重要です。

### 選択の早見図 {#quick-decision-guide}

**どのテーブルを使用するか**

```
センサーデータ（ID、時刻、値）ですか？
    はい → TAG TABLE

ログ、または型の混在するデータですか？
    はい → LOG TABLE

キーを指定した UPDATE/DELETE が必要ですか？
    はい → VOLATILE TABLE（メモリ内）

変更の少ない参照データやマスターですか？
    はい → LOOKUP TABLE
```

### 1．Tag：センサーデータ {#1-tag-table---for-sensor-data}

**用途**：センサーやデバイスの時系列データ

**適したデータ：**
- 温度、圧力、振動などの IoT 測定値
- スマートメーター
- 環境監視
- 機器のテレメトリー

**構造：**
```
(sensor_name, timestamp, value, [追加列])
```

**主な機能：**
- 毎秒数百万レコード
- ロールアップ有効時の自動集計
- センサー ID と時刻範囲による高速検索
- 重複除去

**例：**
```sql
CREATE TAG TABLE sensors (
    sensor_name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED,
    humidity DOUBLE
);
```

### 2．Log：一般的な時系列データ {#2-log-table---for-general-time-series-data}

**用途**：ログファイル、イベント、タイムスタンプ付きデータ

**適したデータ：**
- アプリケーションログ
- イベントストリーム
- アクセスログ
- トランザクションログ
- 複数列の PLC データ

**構造**：任意のスキーマ

**主な機能：**
- 毎秒数百万レコード
- ナノ秒精度の `_arrival_time` を自動追加
- 最新のデータから取得
- KEYWORD インデックス作成後に `SEARCH` で全文検索
- 柔軟なスキーマ

**例：**
```sql
CREATE TABLE app_logs (
    level VARCHAR(10),
    user_id INTEGER,
    message VARCHAR(1000),
    ip_addr IPV4
);
```

### 3．Volatile：インメモリデータ {#3-volatile-table---for-in-memory-data}

**用途**：メモリ上で高速な INSERT/UPDATE/DELETE が必要な場合

**適した用途：**
- リアルタイムダッシュボード
- セッションデータ
- 一時的な計算
- キーと値のキャッシュ
- リアルタイム監視画面

**構造**：任意のスキーマ、`PRIMARY KEY` に対応

**主な機能：**
- 毎秒数万回の操作
- 主キーによる UPDATE と DELETE
- 全データをメモリに保存して高速処理
- **停止時にデータが失われる**

**例：**
```sql
CREATE VOLATILE TABLE live_status (
    device_id INTEGER PRIMARY KEY,
    status VARCHAR(20),
    last_updated DATETIME
);
```

### 4．Lookup：参照データ {#4-lookup-table---for-reference-data}

**用途**：変更頻度の低い参照データやマスターデータ

**適したデータ：**
- デバイス台帳
- 設定テーブル
- カテゴリーとディメンション
- マスターデータ

**構造**：`PRIMARY KEY` を持つ任意のスキーマ

**主な機能：**
- 高速な SELECT
- 永続保存
- INSERT/UPDATE は低速（ディスクベース）
- 標準的な DB 操作

**例：**
```sql
CREATE LOOKUP TABLE devices (
    device_id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    location VARCHAR(100),
    type VARCHAR(20)
);
```

## 比較 {#comparison-table}

| 機能 | Tag | Log | Volatile | Lookup |
|---------|-----------|-----------|----------------|--------------|
| 用途 | センサー | ログ、イベント | メモリキャッシュ | マスター |
| 挿入速度 | 毎秒数百万 | 毎秒数百万 | 毎秒数万 | 毎秒数百 |
| UPDATE | 不可* | 不可 | 可 | 可 |
| DELETE | 時刻条件 | 時刻条件 | キー指定 | キー指定 |
| 保存先 | ディスク | ディスク | メモリ | ディスク |
| スキーマ | 固定パターン | 柔軟 | 柔軟 | 柔軟 |
| 得意な検索 | ID と時刻 | 時刻 | キー | 任意 |
| 永続性 | あり | あり | **なし** | あり |

*Tag のメタデータ列は更新できます。

## 自動タイムスタンプ：`_arrival_time` {#automatic-timestamp-_arrival_time}

Log の各レコードに自動的に時刻を付加します。

```sql
-- 入力する内容
INSERT INTO app_logs VALUES ('ERROR', 1001, 'Connection failed', '192.168.1.10');

-- 保存される内容
-- _arrival_time: 2025-10-10 14:23:45 123:456:789
-- level: ERROR
-- user_id: 1001
-- message: Connection failed
-- ip_addr: 192.168.1.10
```

取得方法：
```sql
SELECT _arrival_time, * FROM app_logs;
```

ナノ秒精度で、高頻度データに適しています。

## データの順序：最新から {#data-order-newest-first}

Log テーブルは、既定で最新のデータから返します。

```sql
SELECT * FROM app_logs;
-- 最新ログから表示
-- ORDER BY _arrival_time DESC は不要
```

最近の情報が重要な時系列分析に最適化しています。

## 時刻による検索：`DURATION` {#time-based-queries-duration}

`DURATION` で時刻条件を簡潔に書けます。

```sql
-- 直近 10 分
SELECT * FROM app_logs DURATION 10 MINUTE;

-- 次の手動条件の代わりに使用
-- SELECT * FROM app_logs
-- WHERE _arrival_time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
--                         AND TO_DATE('2025-10-10 14:10:00', 'YYYY-MM-DD HH24:MI:SS');
```

その他の例：
```sql
-- 直近 1 時間
DURATION 1 HOUR

-- 直近 1 日
DURATION 1 DAY

-- 2 時間前を終点とする、その直前の 30 分間
DURATION 30 MINUTE BEFORE 2 HOUR
```

## 追記中心のアーキテクチャー {#write-once-architecture}

Tag/Log は追記中心に設計されています。

- データ行の UPDATE は不可
- 任意の行のランダム削除は不可
- 制約に従う時刻ベースの削除

**設計の利点：**
- 行ロックのない高速書き込み
- データの整合性（ログの上書きを防止）
- 単純なアーキテクチャー

**更新と削除が必要な場合：**
- インメモリには Volatile
- 永続的な参照データには Lookup

## 時刻に基づく削除 {#time-based-deletion}

古いデータを効率よく削除できます。

```sql
-- 最も古い 1000 行を削除
DELETE FROM app_logs OLDEST 1000 ROWS;

-- 最新 10000 行だけを残す
DELETE FROM app_logs EXCEPT 10000 ROWS;

-- 直近 7 日だけを残す
DELETE FROM app_logs EXCEPT 7 DAY;

-- 指定日より前を削除
DELETE FROM app_logs
BEFORE TO_DATE('2025-01-01', 'YYYY-MM-DD');
```

## インデックス {#indexes}

テーブル型に応じたインデックスを使用します。

- **Tag**：3 階層のパーティションインデックス（自動）
- **Log**：LSM（任意、CREATE INDEX で作成）
- **Volatile**：`PRIMARY KEY` に RED-BLACK ツリー
- **Lookup**：RED-BLACK ツリー（追加インデックスは任意）

多くの場合、自動作成されたインデックスを利用できます。

## ロールアップ（Tag 専用） {#rollup-tables-tag-tables-only}

`WITH ROLLUP` で作成するか、`CREATE ROLLUP` で定義すると、
統計を生成します。

```sql
-- SUMMARIZED 列のある Tag を作成
CREATE TAG TABLE sensors (
    sensor_name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
) WITH ROLLUP;

-- 時間単位のロールアップ統計を検索
SELECT rollup('hour', 1, time) AS hour_time, AVG(temperature), COUNT(temperature)
FROM sensors
GROUP BY hour_time;
```

自動ロールアップは 3 階層です。
- 秒単位
- 分単位
- 時間単位

## 圧縮 {#compression}

データを自動圧縮します。

- **論理圧縮**：列ベース（最大 100 倍）
- **物理圧縮**：ブロックレベル（特許技術）

追加設定なしで利用できます。

## 主な用語 {#key-terminology}

| 用語 | 意味 |
|------|---------|
| Tag | センサーやデータソースの識別子 |
| BASETIME | Tag の時刻列 |
| SUMMARIZED | 自動集計の対象列を指定 |
| `_arrival_time` | 自動生成のナノ秒タイムスタンプ |
| `DURATION` | 時刻範囲検索のキーワード |
| ロールアップ | 自動的に生成する統計集計 |
| LSM インデックス | 高速書き込み用の Log-Structured Merge インデックス |

## 推奨事項 {#best-practices}

### 1．適切なテーブル型を選ぶ {#1-choose-the-right-table-type}

- 多数のセンサー ID の大量データ → Tag
- アプリケーションログやイベント → Log
- リアルタイムの更新 → Volatile
- 設定や参照データ → Lookup

### 2．時刻検索に `DURATION` を使用 {#2-use-duration-for-time-queries}

```sql
-- 推奨（最適化した構文）
SELECT * FROM logs DURATION 1 HOUR;

-- 比較的効率が低い例
SELECT * FROM logs
WHERE _arrival_time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
                        AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 3．保持期間を実装 {#3-implement-data-retention}

自動削除を設定します。

```sql
-- 直近 30 日だけを残す
DELETE FROM app_logs EXCEPT 30 DAY;
```

cron ジョブの利用も検討してください。

### 4．複数センサーを Tag にまとめる {#4-use-tag-tables-for-multi-sensor-data}

センサーが 1000 個あっても、1000 テーブルを作る必要はありません。

```sql
-- 推奨：すべてのセンサーを 1 Tag テーブルに保存
CREATE TAG TABLE all_sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 指定センサーを検索
SELECT * FROM all_sensors
WHERE sensor_id = 'sensor123'
AND time BETWEEN ... AND ...;
```

## よくある構成 {#common-patterns}

### パターン 1：IoT データ収集 {#pattern-1-iot-sensor-collection}

```sql
-- センサーデータ用 Tag
CREATE TAG TABLE sensors (...);

-- センサーメタデータ用 Lookup
CREATE LOOKUP TABLE sensor_info (
    sensor_id VARCHAR(20) PRIMARY KEY,
    location VARCHAR(100),
    type VARCHAR(50)
);
```

### パターン 2：アプリケーション監視 {#pattern-2-application-monitoring}

```sql
-- アプリケーションログ用 Log
CREATE TABLE app_logs (...);

-- アクセスログ用 Log
CREATE TABLE access_logs (...);

-- ユーザーセッション用 Volatile
CREATE VOLATILE TABLE active_sessions (...);
```

### パターン 3：製造業 {#pattern-3-manufacturing}

```sql
-- 機器センサー用 Tag
CREATE TAG TABLE equipment_sensors (...);

-- 生産イベント用 Log
CREATE TABLE production_events (...);

-- 機器台帳用 Lookup
CREATE LOOKUP TABLE equipment_list (...);
```

## 次のステップ {#whats-next}

基本概念の後は、次を参照してください。

1. [**最初の操作**](../first-steps/)：日常的な machsql 操作
2. [**SQL リファレンス**](../../sql-reference/)：検索と DDL
3. [**テーブルの種類**](../../table-types/)：詳しい説明

## クイックリファレンス {#quick-reference}

```sql
-- TAG TABLE（センサーデータ）
CREATE TAG TABLE t (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- LOG TABLE（柔軟な時系列）
CREATE TABLE t (
    col1 TYPE,
    col2 TYPE
);
-- _arrival_time を自動追加

-- VOLATILE TABLE（メモリ内）
CREATE VOLATILE TABLE t (
    id INTEGER PRIMARY KEY,
    value TYPE
);

-- LOOKUP TABLE（参照データ）
CREATE LOOKUP TABLE t (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);
```
