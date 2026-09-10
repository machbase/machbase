---
type: docs
title: 'クイックスタート'
weight: 10
toc: true
---

約 5 分で、インストール、テーブルの作成、最初の検索を実行します。

## 前提条件 {#prerequisites}

- Linux または Windows
- 100MB の空きディスク容量
- 端末へのアクセス

## 手順 1：Machbase のインストール {#step-1-install-machbase}

### Linux {#linux}

ダウンロードして展開します。

```bash
# パッケージを取得（x.x.x は実際の版に置換）
wget http://machbase.com/dist/machbase-standard-x.x.x.official-LINUX-X86-64-release.tgz

# ディレクトリを作成して展開
mkdir machbase_home
tar zxf machbase-standard-x.x.x.official-LINUX-X86-64-release.tgz -C machbase_home

# 環境変数を設定
export MACHBASE_HOME=$(pwd)/machbase_home
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

### Windows {#windows}

1. Windows インストーラー（.msi）を取得します。
2. 実行し、ウィザードに従います。
3. 環境変数は自動設定されます。

## 手順 2：データベースの作成と起動 {#step-2-create-and-start-database}

```bash
# データベースを作成
machadmin -c

# サーバーを起動
machadmin -u
```

次の出力を確認します。
```
Database created successfully.
Machbase server started successfully.
```

## 手順 3：接続 {#step-3-connect-to-machbase}

対話型 SQL クライアントを起動します。

```bash
machsql
```

入力を求められたら：
- **サーバーアドレス**：Enter（既定値 127.0.0.1）
- **ユーザー ID**：Enter（既定値 `SYS`）
- **パスワード**：`MANAGER` を入力して Enter

`Mach>` が表示されたら、コマンドを入力できます。

## 手順 4：最初のテーブルの作成 {#step-4-create-your-first-table}

センサーの温度データ用テーブルを作成します。

```sql
CREATE TABLE sensor_data (
    sensor_id VARCHAR(20),
    temperature DOUBLE,
    humidity DOUBLE
);
```

## 手順 5：データの挿入 {#step-5-insert-data}

サンプルの測定値を追加します。

```sql
INSERT INTO sensor_data VALUES ('sensor01', 25.3, 65.2);
INSERT INTO sensor_data VALUES ('sensor01', 25.5, 64.8);
INSERT INTO sensor_data VALUES ('sensor02', 22.1, 70.5);
```

## 手順 6：検索 {#step-6-query-data}

データを取得します。

```sql
-- 全レコードを取得
SELECT * FROM sensor_data;

-- タイムスタンプとともに取得
SELECT _arrival_time, * FROM sensor_data;

-- 平均温度を取得
SELECT AVG(temperature) FROM sensor_data;

-- 直近 10 分を取得
SELECT * FROM sensor_data DURATION 10 MINUTE;
```

**注意**：各レコードに、ナノ秒精度の `_arrival_time` が自動追加されます。

## 結果の確認 {#understanding-the-results}

`SELECT * FROM sensor_data` では、次を確認できます。

1. **最新から表示**：最近の入力を先に返します。
2. **自動時刻**：各レコードに `_arrival_time` があります。
3. **高精度**：タイムスタンプはナノ秒精度です。

出力例：
```
SENSOR_ID            TEMPERATURE  HUMIDITY
------------------------------------------------
sensor02             22.1         70.5
sensor01             25.5         64.8
sensor01             25.3         65.2
[3] row(s) selected.
```

## ここまでの操作 {#what-just-happened}

次の操作が完了しました。

✓ Machbase のインストール
✓ データベースの作成と起動
✓ machsql で接続
✓ テーブルの作成
✓ 時系列データの挿入
✓ 自動タイムスタンプ付きデータの検索

## 次のステップ {#next-steps}

続けて次のガイドを参照してください。

1. [**最初の操作**](../first-steps/)：machsql のコマンド
2. [**基本概念**](../concepts/)：テーブル型と用途
3. [**テーブルの種類**](../../table-types/)：実際の用途に合うテーブルの選択

## 主なコマンド {#common-commands}

よく使うコマンドを示します。

```bash
# Machbase を起動
machadmin -u

# Machbase を停止
machadmin -s

# 稼働を確認
machadmin -e

# データベースに接続
machsql
```

## トラブルシューティング {#troubleshooting}

**サーバーが起動しない場合**
- ポート 5656 を確認：`netstat -an | grep 5656`
- `$MACHBASE_HOME/trc/` のログを確認

**接続できない場合**
- 稼働状態を確認：`machadmin -e`
- 既定の認証情報を確認：`SYS` / `MANAGER`

**詳しい対処**
- [トラブルシューティング](../../troubleshooting/)
- [エラーコード](../../troubleshooting/error-code/)

---

[最初の操作](../first-steps/)で machsql の使い方を確認してください。
