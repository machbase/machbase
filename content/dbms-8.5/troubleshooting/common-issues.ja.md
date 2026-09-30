---
title: 'よくある問題と対処'
type: docs
weight: 10
toc: true
---

## クイックガイド {#quick-troubleshooting-guide}

Machbase の利用時によくある問題と、その対処方法を説明します。

## 接続の問題 {#connection-issues}

### サーバーに接続できない {#cannot-connect-to-server}

**症状**：クライアントツールから Machbase サーバーに接続できない

**主な原因：**

1. サーバーが停止している
2. ポート番号が違う
3. ファイアウォールが接続を遮断している
4. ネットワーク設定の問題

**対処：**

```bash
# 稼働を確認
ps -ef | grep machbase

# 状態を確認
machadmin -e

# 停止中なら起動
machadmin -u

# machbase.conf のポートを確認
grep PORT_NO $MACHBASE_HOME/conf/machbase.conf
```

### 接続タイムアウト {#connection-timeout}

**症状**：接続の試行がタイムアウトする

**対処：**

- ネットワーク接続を確認
- `machbase.conf` の `PORT_NO` を確認
- ファイアウォールでポートが遮断されていないか確認
- 最大接続数に達していないか確認

```sql
-- 現在の接続を確認
SELECT * FROM v$session;
```

## 性能の問題 {#performance-issues}

### INSERT が遅い {#slow-insert-performance}

**症状**：データの挿入が想定より遅い

**主な原因：**

1. APPEND ではなく INSERT を使用している
2. バッチ操作を使用していない
3. メモリの割り当てが不足している
4. インデックスが多すぎる

**対処：**

大量入力には APPEND API または APPEND モードの CSV ツールを使用します。SQL の `INSERT /*+ APPEND */` コメントで INSERT を APPEND プロトコルへ切り替えることはできません。

```bash
# Tag の一括入力（既定の append モード）
csvimport -t TAG_TABLE -d data.csv
```

```properties
# machbase.conf：TAG キャッシュプールごとの上限を 2 GiB にする例
TAG_CACHE_MAX_MEMORY_SIZE = 2147483648
```

総キャッシュ容量はこの値と `TAG_CACHE_POOL_COUNT` の積です。物理メモリと他のプロセスのメモリ使用量に合わせて調整してください。

### SELECT が遅い {#slow-select-performance}

**症状**：クエリーに時間がかかりすぎる

**対処：**

```sql
-- EXPLAIN で実行計画を分析
EXPLAIN SELECT * FROM tag WHERE name = 'TAG_001';

-- Tag には時刻範囲を指定
SELECT * FROM tag
WHERE name = 'TAG_001'
  AND time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD') AND TO_DATE('2024-01-31', 'YYYY-MM-DD');

-- 集計にロールアップを使用
SELECT rollup('hour', 1, time), AVG(value)
FROM tag
GROUP BY rollup('hour', 1, time);

-- 頻用する検索列にインデックスを作成
CREATE INDEX idx_column ON table_name (column_name);
```

## テーブル作成の問題 {#table-creation-issues}

### PRIMARY KEY / BASETIME がない {#primary-key--basetime-missing-error}

**症状**：`ERR-02253: Mandatory column definition (PRIMARY KEY / BASETIME) is missing`

**対処：**

```sql
-- Tag には PRIMARY KEY と BASETIME が必要
CREATE TAG TABLE tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

### 可変長列のエラー {#variable-length-columns-error}

**症状**：`ERR-01851: Variable length columns are not allowed in tag table`

**対処**：このエラーは 5.6 より前のバージョンで発生します。5.6 以降へ更新するか、固定長列を使用してください。

## データ入力の問題 {#data-insertion-issues}

### SUMMARIZED が範囲外 {#summarized-value-out-of-range}

**症状：**

- `ERR-02341: SUMMARIZED value is greater than UPPER LIMIT`
- `ERR-02342: SUMMARIZED value is less than LOWER LIMIT`

**対処**：値が LSL/USL の範囲外です。上下限か入力データを修正してください。以下は、`table_name` に `LOWER LIMIT`/`UPPER LIMIT` 属性のメタデータ列 `lsl`/`usl` を定義した場合の例です。この機能は Standard Edition で使用できます。詳細は[LSL/USL](../../table-types/tag-tables/lsl-usl-limits/)を参照してください。

```sql
-- 現在の上下限を確認
SELECT * FROM _table_name_meta;

-- 上下限を変更
UPDATE table_name METADATA SET lsl = 0, usl = 1000 WHERE name = 'TAG_001';

-- または上下限を無効化
UPDATE table_name METADATA SET lsl = NULL, usl = NULL WHERE name = 'TAG_001';
```

### タグメタデータがない {#tag-metadata-not-found}

**症状**：タグ名が見つからず、データを入力できない

**対処**：メタデータにタグ名を先に登録します。

```sql
-- タグメタデータを挿入
INSERT INTO tag_table METADATA VALUES ('TAG_001');

-- 続いてデータを挿入
INSERT INTO tag_table VALUES ('TAG_001', NOW, 100);
```

## メモリの問題 {#memory-issues}

### メモリ不足 {#out-of-memory-errors}

**症状**：サーバーがクラッシュする、またはメモリエラーを返す

**対処：**

1. **現在のメモリ使用量を確認**

```sql
SELECT * FROM V$SESMEM;
```

2. **`machbase.conf` のメモリ設定を調整**

   設定項目と単位は[プロパティ](../../configuration/property/)を確認してください。TAG キャッシュの総容量は、プールごとの値とプール数の積です。

```conf
# TAG キャッシュプールごとの上限を 4 GiB にする例
TAG_CACHE_MAX_MEMORY_SIZE = 4294967296

# 1 クエリーが使用する最大メモリを 64 MiB にする例
MAX_QPX_MEM = 67108864
```

3. **設定変更後にサーバーを再起動**

```bash
machadmin -s  # サーバーを正常停止
machadmin -u  # サーバーを起動
```

メモリエラーの詳しい対処は[メモリ不足](../memory-error)を参照してください。

## ロールアップの問題 {#rollup-issues}

### 依存する ROLLUP がある {#dependent-rollup-table-exists}

**症状**：`ERR-02651: Dependent ROLLUP table exists`

**対処**：依存関係の逆順にロールアップを削除します。

```sql
-- ロールアップ依存関係を確認
SELECT * FROM V$ROLLUP;

-- 逆順に削除
DROP ROLLUP rollup_hour;
DROP ROLLUP rollup_min;
DROP ROLLUP rollup_sec;
DROP TABLE tag_table;
```

### ロールアップが更新されない {#rollup-not-updating}

**症状**：ロールアップのデータが古い

**対処：**

```sql
-- 集計を強制実行
ALTER ROLLUP rollup_name FORCE;

-- ロールアップ状態を確認
SELECT * FROM v$rollup;

-- ロールアップを再起動
ALTER ROLLUP rollup_name STOP;
ALTER ROLLUP rollup_name START;
```

## インデックスの問題 {#index-issues}

### インデックスを削除できない {#cannot-drop-index}

**症状**：インデックスの削除が失敗する

**対処**：テーブルを使用している実行中のセッションがないか確認します。

```sql
-- 実行中セッションを確認
SELECT * FROM v$session;

-- SYS として、対象の session_id を確認して終了
ALTER SYSTEM KILL SESSION session_id;

-- その後にインデックスを削除
DROP INDEX index_name;
```

## ライセンスの問題 {#license-issues}

### ライセンスの期限切れ {#license-expired}

**症状**：サーバーが起動しない、ライセンスエラー

**対処：**

```bash
# ライセンス状態を確認
machadmin -f

# 新しいライセンスを導入
machadmin -t new_license_file.dat
```

## バックアップと復元の問題 {#backup-and-recovery-issues}

### データベースをマウントできない {#cannot-mount-database}

**症状**：マウントが失敗する

**主な原因：**

1. データベースファイルの破損
2. バージョンの非互換
3. ファイルが使用中

**対処：**

```sql
-- DB の状態を確認
SELECT * FROM V$STORAGE_MOUNT_DATABASES;

-- 再マウント前に解除
UNMOUNT DATABASE database_name;

-- DB をマウント
MOUNT DATABASE 'path/to/database' TO database_name;
```

## クラスタ固有の問題 {#cluster-specific-issues}

### ノード間の通信失敗 {#node-communication-failure}

**症状**：ノード間で通信できない

**対処：**

1. ノード間のネットワーク接続を確認
2. Coordinator が稼働しているか確認
3. ファイアウォールのルールを確認
4. クラスタ設定を確認

```bash
# クラスタ状態を確認
machcoordinatoradmin --cluster-status

# 必要なら Coordinator を再起動
machcoordinatoradmin -s
machcoordinatoradmin -u
```

## 問題を防ぐための推奨事項 {#best-practices-for-avoiding-issues}

1. **定期的な監視**：
   - サーバーログを定期的に確認
   - V$ テーブルで性能指標を確認
   - 重大なエラーの通知を設定

2. **適切な設定**：
   - 十分なメモリを割り当てる
   - パーティション数を適切に設定
   - キャッシュサイズを適切に設定

3. **データ管理**：
   - 保持ポリシーでデータのライフサイクルを管理
   - 重要なデータを定期的にバックアップ
   - ディスク使用量を監視

4. **クエリーの最適化**：
   - Tag の検索には常に時刻範囲を指定
   - インデックスを適切に使用
   - 集計にはロールアップテーブルを活用

5. **容量計画**：
   - データの増加を予測
   - ピーク負荷を想定
   - 必要になる前に基盤を拡張

## その他のサポート {#getting-more-help}

- 個々のエラーメッセージは[エラーコード](../error-code)で確認してください。
- メモリ関連の問題は[メモリ不足](../memory-error)を確認してください。
- `$MACHBASE_HOME/trc/` のサーバーログを確認してください。
- ログファイルとエラーの詳細を添えて Machbase サポートへ連絡してください。

## 診断コマンド {#diagnostic-commands}

問題調査に役立つコマンド：

```sql
-- 状態を確認
SELECT * FROM v$version;
SELECT * FROM V$SYSSTAT;

-- 性能を監視
SELECT * FROM V$SESMEM;
SELECT * FROM v$session;
SELECT * FROM V$STMT;

-- テーブル情報を確認
SELECT * FROM m$sys_tables;
SELECT * FROM m$sys_users;
SELECT * FROM m$sys_table_property;
```

## ログファイルの場所 {#log-files-location}

調査で確認する主なログ：

```text
$MACHBASE_HOME/trc/machbase.trc
```

サーバーのエラー、バックアップ、ロールアップの動作は、このトレースログで確認します。ログレベルは[TRACE_LOG_LEVEL](../trace-log/)で調整できます。ログの分割や別ファイルへの出力は運用設定に依存するため、固定の `backup.trc`、`rollup.trc`、`error.trc` が常に生成されるとは限りません。

管理操作の詳細は、[machadmin](../../tools-reference/machadmin/)、[システムとセッションの管理](../../sql-reference/sys-session-manage/)、[データベースのマウント](../../advanced-features/database-mount/)を参照してください。
