---
type: docs
title: 'machsql の最初の操作'
weight: 30
toc: true
---

対話型 SQL コマンドラインツール `machsql` の、日常的に使用するコマンドと操作を説明します。

## `machsql` とは {#what-is-machsql}

Machbase の対話型 SQL クライアントで、次の操作ができます。
- SQL クエリーの実行
- テーブルとユーザーの管理
- システム情報の確認
- データのインポートとエクスポート

## 接続 {#connecting-to-machbase}

### 基本の接続 {#basic-connection}

```bash
machsql
```

次の入力を求められます。
- サーバーアドレス（既定値：127.0.0.1）
- ユーザー ID（既定値：SYS）
- パスワード（既定値：MANAGER）

### パラメーターを指定した接続 {#connection-with-parameters}

接続情報を引数で指定すると、対話入力を省略できます。

```bash
machsql -s localhost -u SYS -p MANAGER
```

主なオプション：

```bash
machsql -s 192.168.1.100     # リモートサーバーへ接続
machsql -u myuser -p mypass  # 認証情報を指定
machsql -P 7878              # 別のポートを使用
machsql -f script.sql        # SQL スクリプトを実行
```

## 基本コマンド {#essential-commands}

### SHOW コマンド {#show-commands}

システム情報を表示します。

```sql
-- 全テーブルを一覧
SHOW TABLES;

-- テーブル構造を表示
SHOW TABLE sensor_data;

-- インデックス一覧
SHOW INDEXES;

-- ユーザー一覧
SHOW USERS;

-- ライセンス情報
SHOW LICENSE;

-- ディスク使用量を確認
SHOW STORAGE;

-- テーブルスペース一覧
SHOW TABLESPACES;

-- 実行中のクエリーを確認
SHOW STATEMENTS;
```

### テーブルの作成 {#creating-tables}

```sql
-- 単純な Log テーブル
CREATE TABLE app_logs (
    level VARCHAR(10),
    message VARCHAR(1000)
);

-- センサーデータのテーブル
CREATE TABLE temperatures (
    sensor_id VARCHAR(20),
    value DOUBLE
);

-- 複数列のテーブル
CREATE TABLE device_data (
    device_id INTEGER,
    location VARCHAR(50),
    temperature DOUBLE,
    humidity DOUBLE,
    pressure DOUBLE
);
```

### データの挿入 {#inserting-data}

```sql
-- 1 行を挿入
INSERT INTO temperatures VALUES ('sensor01', 25.3);

-- 複数行を挿入
INSERT INTO app_logs VALUES ('INFO', 'Application started');
INSERT INTO app_logs VALUES ('WARN', 'High memory usage detected');
INSERT INTO app_logs VALUES ('ERROR', 'Connection timeout');
```

### データの検索 {#querying-data}

```sql
-- 全レコードを取得
SELECT * FROM temperatures;

-- タイムスタンプを指定
SELECT _arrival_time, * FROM temperatures;

-- 条件を指定
SELECT * FROM app_logs WHERE level = 'ERROR';

-- 最近のデータ（直近 10 分）
SELECT * FROM temperatures DURATION 10 MINUTE;

-- 指定時刻範囲のデータ
SELECT * FROM temperatures
DURATION 30 MINUTE BEFORE 1 HOUR;

-- 集計
SELECT sensor_id, AVG(value), MAX(value), MIN(value)
FROM temperatures
GROUP BY sensor_id;

-- レコードを数える
SELECT COUNT(*) FROM app_logs;
```

### データの削除 {#deleting-data}

```sql
-- 最も古い 100 行を削除
DELETE FROM app_logs OLDEST 100 ROWS;

-- 最新 1000 行を残す
DELETE FROM app_logs EXCEPT 1000 ROWS;

-- 7 日より古いデータを削除
DELETE FROM app_logs EXCEPT 7 DAY;

-- 指定日より前を削除
DELETE FROM app_logs
BEFORE TO_DATE('2025-01-01', 'YYYY-MM-DD');
```

### テーブルの管理 {#managing-tables}

```sql
-- インデックスを作成
CREATE INDEX idx_sensor ON temperatures(sensor_id);

-- TRUNCATE で全データを削除
TRUNCATE TABLE app_logs;

-- テーブルを削除
DROP TABLE temperatures;
```

## _arrival_time {#understanding-_arrival_time}

Log テーブルの各レコードには、自動的に時刻が付加されます。

```sql
SELECT _arrival_time, * FROM temperatures;
```

出力：
```
_arrival_time                   SENSOR_ID    VALUE
--------------------------------------------------------
2025-10-10 14:23:45 123:456:789 sensor01     25.3
2025-10-10 14:23:40 987:654:321 sensor01     24.8
```

タイムスタンプはナノ秒精度です。

## 時刻範囲の操作 {#working-with-time-ranges}

### `DURATION` キーワード {#duration-keyword}

`DURATION` で時刻条件を簡単に記述できます。

```sql
-- 直近 5 分
SELECT * FROM temperatures DURATION 5 MINUTE;

-- 直近 1 時間
SELECT * FROM temperatures DURATION 1 HOUR;

-- 直近 1 日
SELECT * FROM temperatures DURATION 1 DAY;

-- 2 時間前を終点とする、その直前の 30 分間
SELECT * FROM temperatures
DURATION 30 MINUTE BEFORE 2 HOUR;
```

## テキスト検索 {#text-search}

列内のテキストを検索します。

```sql
-- SEARCH の前にキーワードインデックスを作成
CREATE INDEX idx_message ON app_logs(message) INDEX_TYPE KEYWORD;

-- error を含むログを検索
SELECT * FROM app_logs
WHERE message SEARCH 'error';

-- timeout または connection を含むログ
SELECT * FROM app_logs
WHERE message SEARCH 'timeout'
   OR message SEARCH 'connection';

-- high と memory の両方を含むログ
SELECT * FROM app_logs
WHERE message SEARCH 'high memory';
```

## SQL スクリプトの実行 {#running-sql-scripts}

SQL を記述したファイルを実行します。

```bash
machsql -f setup.sql
```

`machsql` 内から実行する場合：

```sql
@/path/to/script.sql
```

## 結果のエクスポート {#exporting-query-results}

結果をファイルに保存します。

```bash
# CSV に出力
machsql -s localhost -u SYS -p MANAGER \
  -f query.sql -o output.csv -r csv

# JSON に出力
machsql -s localhost -u SYS -p MANAGER \
  -f query.sql -o output.json -r json
```

## 便利な操作 {#tips-and-tricks}

### 1．コマンド履歴 {#1-command-history}

矢印キーで履歴を移動します。
- **`↑`**：前のコマンド
- **`↓`**：次のコマンド

### 2．自動補完 {#2-auto-completion}

`Tab` で次を補完できます。
- テーブル名
- 列名
- SQL キーワード

### 3．複数行クエリー {#3-multi-line-queries}

SQL は複数行に分けて入力できます。

```sql
SELECT
    sensor_id,
    AVG(value) as avg_temp,
    MAX(value) as max_temp
FROM
    temperatures
WHERE
    _arrival_time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
                      AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS')
GROUP BY
    sensor_id;
```

### 4．出力の抑制 {#4-quiet-output}

スクリプトではバナーを省略できます。

```bash
machsql -i  # または --silent
```

### 5．タイムゾーンの設定 {#5-set-timezone}

```bash
machsql -z +0900  # 韓国のタイムゾーン
machsql -z -0500  # 米国東部
```

## 主な操作手順 {#common-workflows}

### 日常の監視 {#daily-monitoring}

```sql
-- 最近のエラーを確認
SELECT * FROM app_logs
WHERE level = 'ERROR'
DURATION 1 DAY;

-- センサーの状態を監視
SELECT sensor_id, COUNT(*), AVG(value)
FROM temperatures
DURATION 1 HOUR
GROUP BY sensor_id;

-- DB サイズを確認
SHOW STORAGE;
```

### データの整理 {#data-cleanup}

```sql
-- 直近 30 日だけを残す
DELETE FROM app_logs EXCEPT 30 DAY;

-- 古いセンサーデータを削除
DELETE FROM temperatures EXCEPT 7 DAY;
```

### 性能の確認 {#performance-check}

```sql
-- 実行中のクエリーを表示
SHOW STATEMENTS;

-- インデックスの状態を確認
SHOW INDEXES;

-- インデックス構築の進捗を確認
SHOW INDEXGAP;
```

## ユーザー管理 {#user-management}

```sql
-- ユーザーを作成
CREATE USER datauser IDENTIFIED BY 'password123';

-- 権限を付与
GRANT SELECT ON temperatures TO datauser;
GRANT INSERT ON temperatures TO datauser;

-- パスワードを変更
ALTER USER datauser IDENTIFIED BY 'newpassword';

-- ユーザーを削除
DROP USER datauser;
```

## キーボードショートカット {#keyboard-shortcuts}

| キー | 操作 |
|----------|--------|
| `Ctrl+C` | 現在のクエリーを取り消す |
| `Ctrl+D` | `machsql` を終了 |
| `Ctrl+L` | 画面を消去 |
| `↑` / `↓` | コマンド履歴を移動 |
| `Tab` | 自動補完 |

## ヘルプ {#getting-help}

`machsql` 内で実行します。

```sql
-- ヘルプを表示
help

-- コマンド構文を表示
help CREATE TABLE
help SELECT
help DELETE
```

## トラブルシューティング {#troubleshooting}

### 接続の失敗 {#connection-failed}

```bash
# サーバーの稼働を確認
machadmin -e

# ポートが開いているか確認
netstat -an | grep 5656
```

### クエリータイムアウト {#query-timeout}

```properties
# machbase.conf に設定し、サーバーを再起動
SESSION_QUERY_TIMEOUT_SEC = 300
```

### メモリ不足 {#out-of-memory}

```sql
-- 結果件数を制限
SELECT * FROM large_table LIMIT 1000;

-- 元データの代わりに集計を使用
SELECT COUNT(*), AVG(value) FROM large_table;
```

## 次のステップ {#next-steps}

基本操作の後は、次を参照してください。

1. [**基本概念**](../concepts/)：テーブル型と構成
2. [**テーブルの種類**](../../table-types/)：データに合う型の選択
3. [**SQL リファレンス**](../../sql-reference/)：構文の詳細

## クイックリファレンス {#quick-reference-card}

```sql
-- テーブル操作
SHOW TABLES;
SHOW TABLE tablename;
CREATE TABLE t (col TYPE);
DROP TABLE t;

-- データ操作
INSERT INTO t VALUES (...);
SELECT * FROM t;
SELECT * FROM t DURATION 10 MINUTE;
DELETE FROM t EXCEPT 7 DAY;

-- システム情報
SHOW LICENSE;
SHOW STORAGE;
SHOW USERS;

-- 時刻検索
DURATION 5 MINUTE
DURATION 1 HOUR
DURATION 1 DAY
DURATION 30 MINUTE BEFORE 2 HOUR

-- テキスト検索
CREATE INDEX idx_col ON t(column) INDEX_TYPE KEYWORD;
WHERE column SEARCH 'text'
```

---

手元のデータでも操作を試し、`machsql` に慣れてください。
