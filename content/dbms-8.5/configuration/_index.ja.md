---
type: docs
title: '設定'
weight: 100
toc: true
---

サーバープロパティはキーと値の組で、起動時に `machbase.conf` から読み込まれます。
ここでは、よく変更する項目を示します。正確な制限は、
詳細なプロパティリファレンスを参照してください。

## 設定ファイル {#configuration-file}

### 保存場所 {#location}

```bash
$MACHBASE_HOME/conf/machbase.conf
```

### 設定の編集 {#editing-configuration}

```bash
# 編集前にサーバーを停止
machadmin -s

# 設定ファイルを編集
vi $MACHBASE_HOME/conf/machbase.conf

# 新しい設定でサーバーを起動
machadmin -u
```

多くのプロパティは起動時設定です。リファレンスで動的変更が明示されていない限り、
サーバーを停止してから変更してください。

## 主な設定パラメーター {#key-configuration-parameters}

### ネットワークとセッション {#network-and-sessions}

```properties
# サーバーポート
PORT_NO = 5656

# バインド IP。0.0.0.0 は全インターフェース
BIND_IP_ADDRESS = 0.0.0.0

# 最大同時セッション数
MAX_SESSION_COUNT = 4096

# アイドルとクエリーのタイムアウト（秒）。0 は無効
SESSION_IDLE_TIMEOUT_SEC = 0
SESSION_QUERY_TIMEOUT_SEC = 0
```

### メモリ {#memory}

```properties
# machbased の最大メモリ量
PROCESS_MAX_SIZE = 8589934592 # 8GB

# ディスク列指向テーブルスペースのメモリ上限
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE = 8589934592 # 8GB

# Volatile テーブルスペースのメモリ上限
VOLATILE_TABLESPACE_MEMORY_MAX_SIZE = 2147483648 # 2GB

# クエリーごとのメモリ上限
MAX_QPX_MEM = 1073741824 # 1GB
```

### ストレージとチェックポイント {#storage-and-checkpoint}

```properties
# DB ディレクトリ。? は $MACHBASE_HOME に展開
DBS_PATH = ?/dbs

# テーブルとインデックスのチェックポイント間隔（秒）
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 120
DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC = 120
```

### クエリー処理 {#query-processing}

```properties
# 並列度。Standard の既定値は 0、Cluster は 4
QUERY_PARALLEL_FACTOR = 0

# Tag の検索方向：-1 逆、0 エンジン判断、1 順
TABLE_SCAN_DIRECTION = 0
```

### トレースログ {#trace-logging}

```properties
# トレース保存先。? は $MACHBASE_HOME に展開
TRACE_LOGFILE_PATH = ?/trc

# トレースのサイズと保持ファイル数
TRACE_LOGFILE_SIZE = 10485760 # 10MB
TRACE_LOGFILE_COUNT = 1000

# トレースレベル
TRACE_LOG_LEVEL = 277
```

## 調整例 {#tuning-examples}

### メモリ上限の拡大 {#larger-memory-budget}

```properties
PROCESS_MAX_SIZE = 17179869184 # 16GB
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE = 12884901888 # 12GB
MAX_QPX_MEM = 2147483648 # 2GB
```

### 同時接続クライアント数の増加 {#more-concurrent-clients}

```properties
MAX_SESSION_COUNT = 8192
MAX_STMT_COUNT_PER_SESSION = 2048
```

### 長時間クエリーの許可 {#longer-running-queries}

```properties
# クエリータイムアウトを無効化
SESSION_QUERY_TIMEOUT_SEC = 0

# または 2 分に設定
SESSION_QUERY_TIMEOUT_SEC = 120
```

## 設定の監視 {#monitoring-configuration}

```sql
-- 現在のプロパティ値を表示
SELECT * FROM V$PROPERTY;

-- ストレージ使用量を確認
SELECT * FROM V$STORAGE;
```

## セキュリティ設定 {#security-configuration}

```properties
# 特定のインターフェースでのみ待ち受ける
BIND_IP_ADDRESS = 192.168.1.100

# ネイティブのリモート接続を拒否。HTTP もローカルに限定するには
# BIND_IP_ADDRESS=127.0.0.1 を設定する
GRANT_REMOTE_ACCESS = 0
```

## クラスタ設定 {#cluster-configuration}

Cluster Edition には追加のプロパティがあります。主な例を示します。

```properties
# クラスタリンクの接続先
CLUSTER_LINK_HOST = localhost
CLUSTER_LINK_PORT_NO = 3868

# Coordinator の保存先
COORDINATOR_DBS_PATH = ?/dbs

# Coordinator の HTTP 管理ポート
HTTP_ADMIN_PORT = 5779
```

構築手順は[クラスタのインストール](../installation/cluster/)を参照してください。

## 設定時の推奨事項 {#configuration-best-practices}

1. 変更前に `machbase.conf` をバックアップします。
2. 調整する領域を 1 つずつ変更します。
3. 本番適用前にリファレンスで値を確認します。
4. 起動時プロパティを変更したらサーバーを再起動します。
5. 変更後は `V$PROPERTY`、トレースログ、実際の負荷での動作を確認します。

## 詳細な設定リファレンス {#complete-configuration-reference}

- [設定プロパティ](./property/)：Standard のプロパティ
- [クラスタ設定プロパティ](./property-cl/)：Cluster Edition のプロパティ
- [メタテーブル](./meta-table/)：システムメタデータ
- [仮想テーブル](./virtual-table/)：実行時の監視
