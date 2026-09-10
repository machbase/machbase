---
type: docs
title: 'テーブルの種類：詳細ガイド'
weight: 20
toc: true
---

4 種類のテーブルを、選択基準、性能、実例で比較します。

## 4 種類のテーブル {#the-four-table-types}

それぞれ異なる負荷に最適化されています。

1. **Tag**：時刻または距離を軸とするセンサーデータ
2. **Log**：イベントとログ
3. **Volatile**：インメモリのリアルタイムデータ
4. **Lookup**：参照データとマスター

## 選択の早見ガイド {#quick-decision-guide}

### 選択の開始 {#start-here}

次の条件から選択します。

```
┌─────────────────────────────────────────────────┐
│ どの種類のデータですか？                        │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
    永続保存？                 一時保存？
        │                           │
        ▼                           ▼
    ┌───────┐                 ┌──────────┐
    │ はい  │                 │ Volatile │
    └───┬───┘                 │  テーブル│
        │                     └──────────┘
        ▼
    センサー/測定データ
    （ID、軸、値）？
        │
    ┌───┴────┐
    │        │
   はい      いいえ
    │        │
    ▼        ▼
  Tag     ログ/イベント
  テーブル    データ？
            │
        ┌───┴────┐
        │        │
       はい      いいえ
        │        │
        ▼        ▼
      Log     Lookup
      テーブル    テーブル
```

### 選択表 {#decision-table}

| データ | 推奨 | 理由 |
|-----------|------------------|-----|
| 1000 台の温度センサー | Tag | 複数センサーの時系列値 |
| アプリケーションのエラーログ | Log | イベントと柔軟なスキーマ |
| 現在のユーザーセッション | Volatile | 更新が必要な一時データ |
| デバイス情報、台帳 | Lookup | 更新の少ない参照データ |
| 株式ティック | Tag | 銘柄がタグ、価格が値 |
| 位置ごとのコンベヤー振動 | Tag | 距離軸の測定 |
| HTTP アクセスログ | Log | 多数の列を持つイベント |
| ショッピングカート | Volatile | セッション単位の頻繁な更新 |
| 商品カタログ | Lookup | 変更の少ないマスター |

## Tag テーブル {#tag-table-deep-dive}

### 適した用途 {#when-to-use}

主な用途：
- 温度、湿度、圧力などの IoT
- 産業機器のテレメトリー
- スマートメーター
- GPS 追跡
- 走行距離、コンベヤー長、レール位置などの距離軸データ
- `(sensor_id, time|distance, value)` 形式のデータ

### 構造 {#structure}

```sql
-- 時間軸
CREATE TAG TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,    -- タグ名（センサー識別子）
    time DATETIME BASETIME,               -- タイムスタンプ
    value DOUBLE SUMMARIZED,              -- ロールアップ対象値
    other_value DOUBLE                    -- 追加の測定値
) WITH ROLLUP;

-- 距離軸
CREATE TAG TABLE conveyor_profile (
    line_id VARCHAR(20) PRIMARY KEY,
    distance_m DOUBLE BASE DISTANCE,
    vibration DOUBLE,
    temperature DOUBLE
);
```

### 主な機能 {#key-features}

**ロールアップ統計（時間軸のみ）：**
```sql
-- 元データ
INSERT INTO sensors (sensor_id, time, value) VALUES ('sensor01', NOW, 25.3);

-- ロールアップ式による時間単位の統計
SELECT rollup('hour', 1, time) AS hour_time, AVG(value), COUNT(value)
FROM sensors
GROUP BY hour_time;
```

`WITH ROLLUP` または `CREATE ROLLUP` で定義してから、
ロールアップ式を使用します。距離軸では、範囲検索とバケット集計を
使用します。

**メタデータ層：**
```sql
-- センサーメタデータ用の別テーブル
SELECT * FROM sensors METADATA;

-- 独自のメタデータ列を追加
ALTER TABLE sensors METADATA ADD COLUMN (location VARCHAR(100));
UPDATE sensors METADATA SET location = 'Building A' WHERE name = 'sensor01';
```

**性能：**
- 毎秒数百万件の挿入
- タグと軸の範囲による高速検索
- 自動の 3 階層パーティションインデックス

### 推奨事項 {#best-practices}

**推奨する使い方：**
- 数千のセンサーを 1 つのテーブルに保存
- 集計対象に SUMMARIZED を指定
- 時間軸の統計にはロールアップを検索
- センサー情報をメタデータに保存

**避ける使い方：**
- センサーごとにテーブルを分割
- データ値の UPDATE（メタデータの更新は可能）
- センサー以外の形式に無理に適用

### 使用例 {#example-use-cases}

```sql
-- 製造業：機器センサー
CREATE TAG TABLE equipment_telemetry (
    equipment_id VARCHAR(50) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED,
    vibration DOUBLE,
    rpm DOUBLE,
    power_consumption DOUBLE
);

-- スマートシティ：環境監視
CREATE TAG TABLE air_quality (
    station_id VARCHAR(30) PRIMARY KEY,
    time DATETIME BASETIME,
    pm25 DOUBLE SUMMARIZED,
    pm10 DOUBLE,
    co2 DOUBLE,
    temperature DOUBLE
);

-- 距離軸：コンベヤーや経路のプロファイル
CREATE TAG TABLE route_profile (
    route_id VARCHAR(30) PRIMARY KEY,
    distance_m DOUBLE BASE DISTANCE,
    vibration DOUBLE,
    temperature DOUBLE
);
```

## Log テーブル {#log-table-deep-dive}

### 適した用途 {#when-to-use-1}

主な用途：
- アプリケーションログ
- イベントストリーム
- アクセスログ
- トランザクションログ
- 可変スキーマのタイムスタンプ付きイベント

### 構造 {#structure-1}

```sql
CREATE TABLE app_logs (
    level VARCHAR(10),
    component VARCHAR(50),
    message VARCHAR(2000),
    user_id INTEGER,
    ip_addr IPV4
    -- _arrival_time は自動追加
);
```

### 主な機能 {#key-features-1}

**自動タイムスタンプ：**
```sql
-- 入力する内容
INSERT INTO app_logs VALUES ('ERROR', 'DB', 'Connection timeout', 123, '192.168.1.1');

-- ナノ秒タイムスタンプ付きで保存
-- _arrival_time: 2025-10-10 14:23:45.123456789
```

**全文検索：**
```sql
-- SEARCH の前にキーワードインデックスを作成
CREATE INDEX idx_app_logs_message ON app_logs(message) INDEX_TYPE KEYWORD;

-- 高速なテキスト検索
SELECT * FROM app_logs
WHERE message SEARCH 'timeout'
  AND level = 'ERROR';
```

**柔軟なスキーマ：**
- 必要に応じた列構成
- 対応する各データ型
- 固定パターンが不要

**性能：**
- 毎秒数百万件の挿入
- 最新から取得（自動的な順序）
- 必要に応じて LSM を作成

### 推奨事項 {#best-practices-1}

**推奨する使い方：**
- 可変形式のイベント
- SEARCH によるテキスト検索
- DURATION による時刻検索
- 保持ポリシーを設定

**避ける使い方：**
- センサーデータ（Tag を使用）
- 参照データ（Lookup を使用）
- キーによる UPDATE/DELETE を想定

### 使用例 {#example-use-cases-1}

```sql
-- アプリケーション監視
CREATE TABLE application_events (
    app_name VARCHAR(50),
    event_type VARCHAR(50),
    severity VARCHAR(20),
    message VARCHAR(2000),
    user_id INTEGER,
    session_id VARCHAR(100),
    stack_trace VARCHAR(4000)
);

-- Web サーバーのアクセスログ
CREATE TABLE http_access (
    method VARCHAR(10),
    uri VARCHAR(1000),
    status_code INTEGER,
    response_time INTEGER,
    client_ip IPV4,
    user_agent VARCHAR(500),
    referer VARCHAR(500)
);

-- 金融取引
CREATE TABLE transactions (
    transaction_id VARCHAR(50),
    account_id INTEGER,
    transaction_type VARCHAR(30),
    amount DOUBLE,
    currency VARCHAR(3),
    status VARCHAR(20),
    description VARCHAR(500)
);
```

## Volatile テーブル {#volatile-table-deep-dive}

### 適した用途 {#when-to-use-2}

主な用途：
- リアルタイムダッシュボード
- セッション管理
- 状態表示
- キャッシュ層
- UPDATE/DELETE が必要なデータ

### 構造 {#structure-2}

```sql
CREATE VOLATILE TABLE live_status (
    device_id INTEGER PRIMARY KEY,    -- 更新には PRIMARY KEY が必要
    status VARCHAR(20),
    last_value DOUBLE,
    last_updated DATETIME
);
```

### 主な機能 {#key-features-2}

**キーによる UPDATE と DELETE：**
```sql
-- 既存レコードを更新
UPDATE live_status
SET status = 'RUNNING', last_value = 25.3, last_updated = NOW
WHERE device_id = 101;

-- 指定レコードを削除
DELETE FROM live_status WHERE device_id = 101;
```

**インメモリ：**
- 全データを RAM に保存
- 高速な読み書き
- 毎秒数万回の操作

**警告：永続保存されない**
- 再起動時にデータを喪失
- 停止前に重要なデータを退避

### 推奨事項 {#best-practices-2}

**推奨する使い方：**
- PRIMARY KEY で高速検索
- RAM に収まる小さなデータ量
- Log/Tag へ定期退避
- 現在の状態の管理

**避ける使い方：**
- 永続保存が必要なデータ
- 大量のストリーミングデータ
- 再起動後もデータが残る想定

### 使用例 {#example-use-cases-2}

```sql
-- 機器のリアルタイム状態
CREATE VOLATILE TABLE equipment_status (
    equipment_id INTEGER PRIMARY KEY,
    online CHAR(1),
    current_temp DOUBLE,
    current_pressure DOUBLE,
    last_heartbeat DATETIME
);

-- 有効なユーザーセッション
CREATE VOLATILE TABLE user_sessions (
    session_token VARCHAR(100) PRIMARY KEY,
    user_id INTEGER,
    ip_address IPV4,
    login_time DATETIME,
    last_activity DATETIME,
    expires_at DATETIME
);

-- リアルタイム監視のキャッシュ
CREATE VOLATILE TABLE monitoring_cache (
    metric_key VARCHAR(100) PRIMARY KEY,
    metric_value VARCHAR(500),
    updated_at DATETIME
);
```

## Lookup テーブル {#lookup-table-deep-dive}

### 適した用途 {#when-to-use-3}

主な用途：
- デバイス台帳
- 設定テーブル
- カテゴリーとディメンション
- マスターデータ
- 変更頻度の低い参照データ

### 構造 {#structure-3}

```sql
CREATE LOOKUP TABLE devices (
    device_id VARCHAR(20) PRIMARY KEY,
    device_name VARCHAR(100),
    location VARCHAR(200),
    device_type VARCHAR(50),
    owner VARCHAR(100)
);
```

### 主な機能 {#key-features-3}

**すべての CRUD：**
```sql
-- 挿入
INSERT INTO devices VALUES ('sensor01', 'Sensor A', 'Building 1', 'Temperature', 'Facilities');

-- 更新
UPDATE devices SET location = 'Building 2' WHERE device_id = 'sensor01';

-- 削除
DELETE FROM devices WHERE device_id = 'sensor01';

-- 検索
SELECT * FROM devices WHERE device_type = 'Temperature';
```

**時系列との JOIN：**
```sql
-- センサーデータにデバイス情報を付加
SELECT s.*, d.device_name, d.location
FROM sensors s
JOIN devices d ON s.sensor_id = d.device_id
WHERE s.time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
                 AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

**性能：**
- 高速な読み取り
- 低速な書き込み（毎秒数百件）
- ディスクへの永続保存

### 推奨事項 {#best-practices-3}

**推奨する使い方：**
- 参照データとマスター
- Tag/Log との結合
- 頻用する検索列のインデックス
- 適切なデータ量（100 万行未満が目安）

**避ける使い方：**
- 高頻度の挿入
- 時系列データの保存
- 毎秒数百万件の書き込みを想定

### 使用例 {#example-use-cases-3}

```sql
-- デバイス台帳
CREATE LOOKUP TABLE device_registry (
    device_id VARCHAR(50) PRIMARY KEY,
    device_name VARCHAR(100),
    device_type VARCHAR(50),
    location VARCHAR(200),
    installation_date DATETIME,
    status VARCHAR(20)
);

-- 設定管理
CREATE LOOKUP TABLE system_config (
    config_key VARCHAR(100) PRIMARY KEY,
    config_value VARCHAR(500),
    config_category VARCHAR(50),
    description VARCHAR(500)
);

-- ユーザー管理
CREATE LOOKUP TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(200),
    role VARCHAR(50),
    created_at DATETIME
);
```

## 性能比較 {#performance-comparison}

### 書き込み性能 {#write-performance}

| 型 | 毎秒の挿入 | UPDATE | DELETE |
|-----------|-------------|----------------|----------------|
| Tag | 数百万 | メタデータのみ | 時刻条件 |
| Log | 数百万 | 不可 | 時刻条件 |
| Volatile | 数万 | 主キー | 主キー |
| Lookup | 数百 | 可 | 可 |

### 読み取り性能 {#read-performance}

| 型 | 速度 | 得意な条件 | インデックス |
|-----------|-----------|----------|------------|
| Tag | 非常に高速 | sensor_id と時刻 | 3 階層パーティション |
| Log | 高速 | 時刻範囲 | LSM（任意） |
| Volatile | 非常に高速 | 主キー | RED-BLACK ツリー |
| Lookup | 高速 | 任意の列 | RED-BLACK（追加は任意） |

### ストレージ {#storage}

| 型 | 保存先 | 圧縮率 | 永続性 |
|-----------|---------|-------------|-------------|
| Tag | ディスク | 10～100 倍 | あり |
| Log | ディスク | 10～100 倍 | あり |
| Volatile | メモリ | なし | なし |
| Lookup | ディスク | 中程度 | あり |

## 型の組み合わせ {#combining-table-types}

### IoT プラットフォーム {#pattern-iot-platform}

```sql
-- Tag：センサー測定値
CREATE TAG TABLE sensor_data (...);

-- Lookup：デバイス台帳
CREATE LOOKUP TABLE devices (...);

-- Volatile：現在の状態
CREATE VOLATILE TABLE device_status (...);

-- Log：イベントとアラート
CREATE TABLE device_events (...);
```

### Web アプリケーション {#pattern-web-application}

```sql
-- Log：アクセスログ
CREATE TABLE http_access (...);

-- Log：アプリケーションログ
CREATE TABLE app_logs (...);

-- Volatile：有効なセッション
CREATE VOLATILE TABLE sessions (...);

-- Lookup：ユーザーアカウント
CREATE LOOKUP TABLE users (...);
```

### 製造業 {#pattern-manufacturing}

```sql
-- Tag：機器センサー
CREATE TAG TABLE equipment_telemetry (...);

-- Log：生産イベント
CREATE TABLE production_log (...);

-- Volatile：生産ラインの状態
CREATE VOLATILE TABLE line_status (...);

-- Lookup：機器カタログ
CREATE LOOKUP TABLE equipment_catalog (...);
```

## 避けるべきパターン {#anti-patterns-to-avoid}

### 1．用途に合わない型 {#anti-pattern-1-wrong-table-for-use-case}

**避ける例**：センサーに Log を使用
```sql
-- この設計は避ける
CREATE TABLE sensors (sensor_id VARCHAR(20), value DOUBLE);
```

**推奨**：Tag を使用
```sql
CREATE TAG TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

### 2．センサーごとのテーブル {#anti-pattern-2-one-table-per-sensor}

**避ける例**：1000 センサーに 1000 テーブル
```sql
CREATE TAG TABLE sensor001 (...);
CREATE TAG TABLE sensor002 (...);
-- ほかに 998 テーブル
```

**推奨**：1 テーブルにまとめる
```sql
CREATE TAG TABLE all_sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    ...
);
```

### 3．Volatile に履歴を保存 {#anti-pattern-3-storing-history-in-volatile}

**避ける例**：永続データを Volatile に保存
```sql
-- 再起動するとデータは失われる
CREATE VOLATILE TABLE important_transactions (...);
```

**推奨**：Log または Tag
```sql
CREATE TABLE important_transactions (...);
```

### 4．Lookup への高頻度書き込み {#anti-pattern-4-high-frequency-writes-to-lookup}

**避ける例**：毎秒数百万件を Lookup へ入力
```sql
-- 入力が遅くなる
CREATE LOOKUP TABLE sensor_readings (...);
```

**推奨**：Tag または Log
```sql
CREATE TAG TABLE sensor_readings (...);
```

## 移行ガイド {#migration-guide}

### 他のデータベースからの移行 {#from-other-databases}

**PostgreSQL/MySQL：**
- 通常のテーブル → Log
- 時系列テーブル → Tag
- 一時テーブル → Volatile
- ディメンション → Lookup

**InfluxDB：**
- Measurement → Tag テーブル
- Tag → タグの主キーとメタデータ
- Field → SUMMARIZED の値列と通常の追加値列

**MongoDB：**
- 時系列コレクション → Tag/Log
- 参照コレクション → Lookup
- Capped collection → 保持期間を設定した Log

## 一覧 {#summary-matrix}

| 機能 | Tag | Log | Volatile | Lookup |
|---------|-----|-----|----------|--------|
| 主用途 | センサー | イベント | キャッシュ | 参照 |
| スキーマ | 固定パターン | 柔軟 | 柔軟 | 柔軟 |
| 毎秒の書き込み | 数百万 | 数百万 | 数万 | 数百 |
| UPDATE | メタデータ | 不可 | 可 | 可 |
| DELETE | 時刻条件 | 時刻条件 | キー | キー |
| 保存先 | ディスク | ディスク | メモリ | ディスク |
| 永続性 | あり | あり | なし | あり |
| ロールアップ | 設定時に利用 | なし | なし | なし |
| 得意な検索 | ID と時刻 | 時刻 | キー | 任意 |
| 圧縮 | 非常に高い | 高い | なし | 中程度 |

## 次のステップ {#next-steps}

- [インデックスと性能](../indexing/)：最適化
- [テーブルの種類](../../table-types/)：詳細リファレンス
- [テーブルの種類](../../table-types/)：実例で練習

## 要点 {#key-takeaways}

1. センサーにはロールアップを持つ Tag
2. 柔軟なイベントとログには Log
3. メモリ内で更新するデータには Volatile
4. 参照データとマスターには Lookup
5. 複数の型を組み合わせて構成
6. 型の選択が性能を左右する

---

適切なテーブルを選び、効率のよいアプリケーションを設計してください。
