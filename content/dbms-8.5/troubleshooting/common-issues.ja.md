---
title: 'よくある問題と対処'
type: docs
weight: 10
toc: true
---

## クイックガイド {#quick-troubleshooting-guide}

利用時によくある問題と、その対処方法を説明します。

## 接続の問題 {#connection-issues}

### サーバーに接続できない {#cannot-connect-to-server}

**症状**：クライアントから接続できない

**主な原因：**
1. サーバーが停止している
2. ポートが違う
3. ファイアウォールが遮断
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

**症状**：接続の試行がタイムアウト

**対処：**
- ネットワークを確認
- `machbase.conf` の `PORT_NO` を確認
- ファイアウォールで許可されているか確認
- 最大接続数に達していないか確認

```sql
-- 現在の接続を確認
SELECT * FROM v$session;
```

## 性能の問題 {#performance-issues}

### INSERT が遅い {#slow-insert-performance}

**症状**：想定より挿入が遅い

**主な原因：**
1. APPEND でなく INSERT を使用
2. バッチ操作を使用していない
3. メモリ不足
4. インデックスが多すぎる

**対処：**

大量入力には APPEND API または APPEND モードの CSV ツールを使用します。SQL の `INSERT /*+ APPEND */` コメントで APPEND プロトコルへ切り替えることはできません。

```bash
# Tag の一括入力（既定の append モード）
csvimport -t TAG_TABLE -d data.csv
```

```properties
# machbase.conf：TAG キャッシュプールごとの上限を 2 GiB にする例
TAG_CACHE_MAX_MEMORY_SIZE = 2147483648
```

総キャッシュ容量はこの値と `TAG_CACHE_POOL_COUNT` の積です。物理メモリと他の処理の使用量に合わせて調整してください。

### SELECT が遅い {#slow-select-performance}

**症状**：検索に時間がかかる

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

**対処**：5.6 より前の制限です。5.6 以降へ更新するか、固定長列を使用してください。

## データ入力の問題 {#data-insertion-issues}

### SUMMARIZED が範囲外 {#summarized-value-out-of-range}

**症状：**
- `ERR-02341: SUMMARIZED value is greater than UPPER LIMIT`
- `ERR-02342: SUMMARIZED value is less than LOWER LIMIT`

**対処**：LSL/USL の範囲外です。上下限か入力値を修正します。以下は、`table_name` に `LOWER LIMIT`/`UPPER LIMIT` 属性のメタデータ列 `lsl`/`usl` を定義した場合の例です。この機能は Standard Edition が対象です。詳細は[LSL/USL](../../table-types/tag-tables/lsl-usl-limits/)を参照してください。

```sql
-- 現在の上下限を確認
SELECT * FROM _table_name_meta;

-- 上下限を変更
UPDATE table_name METADATA SET lsl = 0, usl = 1000 WHERE name = 'TAG_001';

-- または上下限を無効化
UPDATE table_name METADATA SET lsl = NULL, usl = NULL WHERE name = 'TAG_001';
```

### タグメタデータがない {#tag-metadata-not-found}

**症状**：タグ名が見つからず入力できない

**対処**：メタデータにタグ名を先に登録します。

```sql
-- タグメタデータを挿入
INSERT INTO tag_table METADATA VALUES ('TAG_001');

-- 続いてデータを挿入
INSERT INTO tag_table VALUES ('TAG_001', NOW, 100);
```

## メモリの問題 {#memory-issues}

### メモリ不足 {#out-of-memory-errors}

**症状**：クラッシュ、またはメモリエラー

**対処：**

1. **現在の使用量を確認**
```sql
SELECT * FROM V$SESMEM;
```

2. **`machbase.conf` の設定を調整**

   設定項目と単位は[サーバープロパティ](../../configuration/property/)を確認してください。TAG キャッシュはプール数との積が総容量になります。
```conf
# TAG キャッシュプールごとの上限を 4 GiB にする例
TAG_CACHE_MAX_MEMORY_SIZE = 4294967296

# 1 クエリーが使用する最大メモリを 64 MiB にする例
MAX_QPX_MEM = 67108864
```

3. **設定変更後に再起動**
```bash
machadmin -s  # サーバーを正常停止
machadmin -u  # サーバーを起動
```

詳細は[メモリ不足](../memory-error)を参照してください。

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

**症状**：集計データが古い

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

### 削除できない {#cannot-drop-index}

**症状**：DROP INDEX が失敗

**対処**：テーブルを使用する実行中のセッションがないか確認します。

```sql
-- 実行中セッションを確認
SELECT * FROM v$session;

-- SYS として、対象の session_id を確認して終了
ALTER SYSTEM KILL SESSION session_id;

-- その後にインデックスを削除
DROP INDEX index_name;
```

## ライセンスの問題 {#license-issues}

### 期限切れ {#license-expired}

**症状**：起動できない、ライセンスエラー

**対処：**

```bash
# ライセンス状態を確認
machadmin -f

# 新しいライセンスを導入
machadmin -t new_license_file.dat
```

## バックアップと復元の問題 {#backup-and-recovery-issues}

### マウントできない {#cannot-mount-database}

**症状**：マウントが失敗

**主な原因：**
1. DB ファイルの破損
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

**症状**：ノードが通信できない

**対処：**

1. ノード間のネットワークを確認
2. Coordinator の稼働を確認
3. ファイアウォールを確認
4. クラスタ設定を確認

```bash
# クラスタ状態を確認
machcoordinatoradmin --cluster-status

# 必要なら Coordinator を再起動
machcoordinatoradmin -s
machcoordinatoradmin -u
```

## 予防策 {#best-practices-for-avoiding-issues}

1. **定期的な監視**
   - サーバーログを確認
   - V$ テーブルで性能指標を確認
   - 重大なエラーの通知を設定

2. **適切な設定**
   - 十分なメモリを確保
   - パーティション数を調整
   - キャッシュサイズを適切に設定

3. **データ管理**
   - 保持ポリシーでライフサイクルを管理
   - 重要データを定期バックアップ
   - ディスク使用量を監視

4. **クエリー最適化**
   - Tag の検索に時刻範囲を指定
   - インデックスを適切に使用
   - 集計にロールアップを使用

5. **容量計画**
   - データ増加を予測
   - ピーク負荷を想定
   - 必要になる前に基盤を拡張

## その他のサポート {#getting-more-help}

- [エラーコード](../error-code)でメッセージを確認
- [メモリ不足](../memory-error)を確認
- `$MACHBASE_HOME/trc/` のログを確認
- ログとエラー詳細を添えて Machbase サポートへ連絡

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

## ログの場所 {#log-files-location}

調査で確認する主なログ：

```text
$MACHBASE_HOME/trc/machbase.trc
```

サーバーのエラー、バックアップ、ロールアップの動作は、このトレースログで確認します。ログレベルは[TRACE_LOG_LEVEL](../trace-log/)で調整できます。ログの分割名や別ファイルへの出力は運用設定に依存するため、固定の `backup.trc`、`rollup.trc`、`error.trc` が常に生成されるとは限りません。

管理操作の詳細は、[machadmin](../../tools-reference/machadmin/)、[システムとセッション管理](../../sql-reference/sys-session-manage/)、[データベースのマウント](../../advanced-features/database-mount/)を参照してください。
