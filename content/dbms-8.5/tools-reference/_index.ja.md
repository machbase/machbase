---
type: docs
title: 'ツールリファレンス'
weight: 90
toc: true
---

データベース管理、データのインポートとエクスポート、システム管理に使用するコマンドラインツールを説明します。

## コマンドラインツール {#command-line-tools}

### machadmin {#machadmin}

データベースサーバーの管理：
- サーバーの起動と停止
- データベースの作成と削除
- バックアップイメージの復元と展開
- 稼働状態の確認

```bash
machadmin -u          # サーバーを起動
machadmin -s          # サーバーを停止
machadmin -c          # DB を作成
machadmin -r path     # 復元
machadmin -w path     # バックアップ情報を表示
```

[詳細](./machadmin/)

### machsql {#machsql}

対話型 SQL クライアント：
- クエリーの実行
- SQL スクリプトの実行
- 結果のエクスポート
- データベース管理

```bash
machsql                           # 対話モード
machsql -f script.sql            # スクリプトを実行
machsql -o output.csv -r csv     # CSV に出力
```

[詳細](./machsql/)

### machloader {#machloader}

データの一括インポート：
- CSV のインポート
- 高速な一括読み込み
- エラー処理

```bash
machloader -i -t table -d data.csv
```

[詳細](./machloader/)

### machcoordinatoradmin {#machcoordinatoradmin}

クラスタ Coordinator の管理（Cluster Edition）：
- Coordinator の管理
- クラスタ設定
- ノード管理

[詳細](./machcoordinatoradmin/)

### machdeployeradmin {#machdeployeradmin}

クラスタ Deployer の管理（Cluster Edition）：
- Deployer の管理
- Warehouse の管理
- クラスタの配置

[詳細](./machdeployeradmin/)

## ツールの一覧 {#tool-quick-reference}

| ツール | 用途 | 主な操作 |
|------|---------|------------|
| machadmin | サーバー管理 | 起動、停止、復元 |
| machsql | SQL クライアント | クエリー、スクリプト |
| machloader | データのインポート | CSV の読み込み |
| csvimport/csvexport | CSV ラッパー | 簡単なインポートとエクスポート |
| machcoordinatoradmin | Coordinator | クラスタ管理 |
| machdeployeradmin | Deployer | クラスタの配置 |

## 主な操作 {#common-operations}

### サーバー管理 {#server-management}

```bash
# サーバーを起動
machadmin -u

# サーバーを停止
machadmin -s

# 状態を確認
machadmin -e

# データベースを作成
machadmin -c

# DB を削除
machadmin -d
```

### データ操作 {#data-operations}

```bash
# 対話型 SQL
machsql

# スクリプトを実行
machsql -f setup.sql

# CSV を読み込み
machloader -i -t sensors -d data.csv

# 検索結果を出力
machsql -f query.sql -o results.csv -r csv
```

### バックアップイメージ操作 {#backup-image-operations}

```bash
# 復元
machadmin -r /backup/machbase_backup

# バックアップファイルをディレクトリに展開
machadmin -x /backup/machbase_backup

# バックアップイメージ情報を表示
machadmin -w /backup/machbase_backup
```

## 環境変数 {#environment-variables}

```bash
# 必要な環境変数
export MACHBASE_HOME=/path/to/machbase
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

## 設定ファイル {#configuration-files}

### machbase.conf {#machbaseconf}

主要なサーバー設定ファイルの場所：
```
$MACHBASE_HOME/conf/machbase.conf
```

主なパラメーター：
- `PORT_NO`：サーバーポート（既定値 5656）
- `PROCESS_MAX_SIZE`：サーバープロセスの最大メモリサイズ
- `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC`：テーブルのチェックポイント間隔
- `DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC`：インデックスのチェックポイント間隔

[設定リファレンス](../configuration/)

## ログファイル {#log-files}

```bash
# サーバーログ
$MACHBASE_HOME/trc/machbase.trc

# SQL クライアントのログ
$MACHBASE_HOME/trc/machsql.trc

# ローダーのログ
$MACHBASE_HOME/trc/machloader.trc
```

## トラブルシューティング {#troubleshooting}

### サーバーが起動しない {#server-wont-start}

```bash
# ポートが空いているか確認
netstat -an | grep 5656

# ログを確認
tail -50 $MACHBASE_HOME/trc/machbase.trc

# DB が作成済みか確認
ls -la $MACHBASE_HOME/dbs/
```

### 接続の問題 {#connection-issues}

```bash
# 稼働を確認
machadmin -e

# 接続テスト
machsql -s localhost -u SYS -p MANAGER
```

### インポートエラー {#import-errors}

```bash
# CSV 形式を確認
head -10 data.csv

# ローダーのログを表示
cat $MACHBASE_HOME/trc/machloader.trc
```

## 推奨事項 {#best-practices}

1. **環境変数を設定する**：MACHBASE_HOME を正しく設定します。
2. **稼働状態を確認する**：操作前に `machadmin -e` を実行します。
3. **ログを確認する**：エラーと警告を確認します。
4. **保守操作の入力を確認する**：復元や展開の前に、バックアップイメージのパスを確認します。
5. **スクリプトをテストする**：本番で使う前に SQL スクリプトを検証します。

## 関連ドキュメント {#related-documentation}

- [最初の操作](../getting-started/first-steps/)：実践的な手順
- [設定](../configuration/)：サーバー設定
- [トラブルシューティング](../troubleshooting/)：問題の解決

## クイックスタート {#quick-start}

```bash
# 1．環境を設定
export MACHBASE_HOME=/opt/machbase
export PATH=$MACHBASE_HOME/bin:$PATH

# 2．DB を作成
machadmin -c

# 3．サーバーを起動
machadmin -u

# 4．接続
machsql

# 5．データを入力
machloader -i -t mytable -d data.csv
```

各ツールの詳細は、本セクションの個別ページを参照してください。
