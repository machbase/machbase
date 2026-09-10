---
type: docs
title: 'トラブルシューティング'
weight: 110
toc: true
---

よくある問題の対処、エラーコード、性能改善の方法を説明します。

## よくある問題 {#common-issues}

### サーバーの問題 {#server-issues}

#### 起動しない {#server-wont-start}

**症状：**
- `machadmin -u` が失敗
- Address already in use エラー
- サーバープロセスがない

**対処：**
```bash
# ポートの使用を確認
netstat -an | grep 5656
lsof -i :5656

# lsof の PID とプロセス名を確認し、該当サービスの管理コマンドで停止
# Machbase の既存プロセスを停止する場合
machadmin -s

# DB ディレクトリを確認
ls -la $MACHBASE_HOME/dbs/

# ログを確認
tail -50 $MACHBASE_HOME/trc/machbase.trc

# 起動を再試行
machadmin -u
```

#### クラッシュする {#server-crashes}

**症状：**
- 予期しない停止
- コアダンプが生成
- Segmentation fault エラー

**対処：**
```bash
# ログを確認
tail -100 $MACHBASE_HOME/trc/machbase.trc

# システムリソースを確認
free -h
df -h

# メモリ使用量を削減（machbase.conf）
# PROCESS_MAX_SIZE = 1073741824 # 1GB

# ディスク空きを確認
du -sh $MACHBASE_HOME/dbs/
```

### 接続の問題 {#connection-issues}

#### 接続できない {#cannot-connect}

**症状：**
- Connection refused
- Connection timeout
- machsql で接続失敗

**対処：**
```bash
# 稼働を確認
machadmin -e

# ネットワーク接続を確認
ping server-address
telnet server-address 5656

# ファイアウォールを確認
sudo iptables -L | grep 5656

# 認証情報を確認
machsql -s localhost -u SYS -p MANAGER
```

#### 接続数が多すぎる {#too-many-connections}

**症状：**
- Max connections exceeded
- 新規接続が拒否される

**対処：**
```sql
-- 接続数を確認
SELECT COUNT(*) FROM V$SESSION;

-- machbase.conf の MAX_SESSION_COUNT を増やす
-- MAX_SESSION_COUNT = 200

-- 必要ならアイドル接続を終了
```

### クエリーの問題 {#query-issues}

#### 検索が遅い {#slow-queries}

**症状：**
- 実行に時間がかかる
- タイムアウト
- CPU 使用率が高い

**対処：**
```sql
-- 時刻条件を追加
SELECT * FROM table DURATION 1 HOUR;  -- この条件を追加

-- LIMIT を使用
SELECT * FROM table LIMIT 1000;

-- 元データの代わりにロールアップを検索
SELECT ROLLUP('hour', 1, time) AS rtime, AVG(value)
FROM sensors
WHERE name = 'sensor-1'
GROUP BY rtime;

-- インデックスを作成
CREATE INDEX idx_column ON table(column);

-- 実行計画を確認
EXPLAIN SELECT ...;
```

#### メモリ不足 {#out-of-memory}

**症状：**
- Out of memory
- クエリーが途中で失敗
- サーバーが応答しない

**対処：**
```sql
-- 結果を減らす
SELECT * FROM table DURATION 1 HOUR LIMIT 1000;

-- 取得する列を減らす
SELECT col1, col2 FROM table;  -- SELECT * を避ける

-- machbase.conf の MAX_QPX_MEM を増やす
-- MAX_QPX_MEM = 1G
```

### データの問題 {#data-issues}

#### インポートが失敗 {#import-fails}

**症状：**
- machloader のエラー
- CSV の読み込みが失敗
- データ型の不一致

**対処：**
```bash
# CSV 形式を確認
head -10 data.csv

# テーブルスキーマを確認
machsql -f - <<EOF
SHOW TABLE tablename;
EOF

# エラーログを確認
# machloader の -l で指定した実行ログを確認
cat /tmp/machloader.log

# データ型を検証
# CSV の列をスキーマに合わせる

# 少量のバッチで先に試す
head -100 data.csv > test.csv
machloader -i -t table -d test.csv -l /tmp/machloader.log
```

#### データが見つからない {#missing-data}

**症状：**
- 想定したデータがない
- 件数が一致しない
- 時刻に欠落がある

**対処：**
```sql
-- 時刻範囲を確認
SELECT MIN(_arrival_time), MAX(_arrival_time) FROM table;

-- 合計件数を確認
SELECT COUNT(*) FROM table;

-- NULL を確認
SELECT COUNT(*) FROM table WHERE column IS NULL;

-- インポート完了を確認
-- machloader のログを確認
```

## エラーコード {#error-codes}

### よくあるエラー {#common-error-messages}

以下は症状を分類するためのメッセージ例です。実際のエラー番号と意味は、サーバーが返した番号を[エラーコード](./error-code/)で確認してください。

| メッセージ例 | 対処 |
|---------|----------|
| Connection failed | サーバーとネットワークを確認 |
| Authentication failed | 認証情報を確認 |
| Table not found | 名前を確認し、SHOW TABLES を実行 |
| Column not found | 列名を確認し、SHOW TABLE を実行 |
| Duplicate key | PRIMARY KEY の制約を確認 |
| Data type mismatch | 型を検証 |
| Out of memory | 検索対象を減らす、メモリを増やす |
| Timeout | 時刻条件を追加、タイムアウトを調整 |

全一覧は[エラーコード](./error-code/)を参照してください。

## 性能の改善 {#performance-optimization}

### クエリーの最適化 {#query-optimization}

1. **時刻条件を指定**
```sql
-- 避ける例
SELECT * FROM sensors WHERE sensor_id = 'sensor01';

-- 推奨
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
DURATION 1 HOUR;
```

2. **分析にロールアップを使用**
```sql
-- 低速
SELECT AVG(value) FROM sensors
WHERE name = 'sensor-1'
  AND time BETWEEN now - 7d AND now;

-- 高速
-- sensors は WITH ROLLUP で作成した TAG であること
SELECT ROLLUP('hour', 1, time) AS rtime, AVG(value)
FROM sensors
WHERE name = 'sensor-1'
  AND time BETWEEN now - 7d AND now
GROUP BY rtime;
```

3. **必要なインデックスを作成**
```sql
CREATE INDEX idx_level ON logs(level);
```

4. **結果件数を制限**
```sql
SELECT * FROM logs DURATION 1 DAY LIMIT 1000;
```

### サーバーの調整 {#server-tuning}

```properties
# メモリ最適化
PROCESS_MAX_SIZE = 4294967296 # 4GB
MAX_QPX_MEM = 1073741824      # クエリーごとのメモリ

# 性能調整
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 900
DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC = 900
QUERY_PARALLEL_FACTOR = 8
```

### データ管理 {#data-management}

1. **保持期間を設定**
```sql
DELETE FROM logs EXCEPT 30 DAYS;
```

2. **書き込みを一括化**
```python
# 一括挿入に APPEND API を使用
# machbaseAPI.connect() の接続 conn と、行のリスト data を使用
conn.append('table', data)
```

3. **ストレージを監視**
```sql
SHOW STORAGE;
```

## 診断コマンド {#diagnostic-commands}

### 稼働状態 {#check-server-status}

```bash
# サーバーの稼働確認
machadmin -e

# 実行中のクエリーを表示
machsql -f - <<EOF
SHOW STATEMENTS;
EOF

# ストレージを確認
machsql -f - <<EOF
SHOW STORAGE;
EOF
```

### ログの確認 {#check-logs}

```bash
# サーバーログ
tail -50 $MACHBASE_HOME/trc/machbase.trc

# エラーログ
grep -i error $MACHBASE_HOME/trc/machbase.trc

# 最近の動作
tail -100 $MACHBASE_HOME/trc/machbase.trc
```

### システム情報 {#system-information}

```sql
-- テーブル
SHOW TABLES;

-- テーブル詳細
SHOW TABLE tablename;

-- ユーザー
SHOW USERS;

-- インデックス
SHOW INDEXES;

-- ライセンス
SHOW LICENSE;
```

## サポートを受ける {#getting-help}

### 収集する情報 {#information-to-gather}

問題の報告には、次を用意します。

1. **正確なエラーメッセージ**
2. **サーバーログ**（$MACHBASE_HOME/trc/machbase.trc）
3. **Machbase のバージョン**（`machadmin -v`）
4. **OS 情報**（`uname -a`）
5. **再現手順**

### 参照資料 {#support-resources}

- 本ガイドと[よくある問題](./common-issues/)
- [エラーコード](./error-code/)
- [メモリ不足](./memory-error/)

## 問題を防ぐための推奨事項 {#best-practices-to-avoid-issues}

1. クエリーに時刻条件を指定
2. 保持ポリシーを設定
3. サーバーリソースを定期監視
4. 定期バックアップ（毎日）
5. 小さなデータで先にテスト
6. 適切なテーブル型を選択
7. Machbase を適切な最新版へ更新

## 簡単な対処 {#quick-fixes}

```bash
# サーバーを再起動
machadmin -s && sleep 5 && machadmin -u

# ディスク空きを確認
df -h

# メモリを確認
free -h

# 最近のエラーを表示
grep -i error $MACHBASE_HOME/trc/machbase.trc | tail -20

# 接続テスト
machsql -s localhost -u SYS -p MANAGER -f - <<EOF
SELECT SYSDATE;
EOF
```

## 関連ドキュメント {#related-documentation}

- [設定](../configuration/)：サーバー設定
- [ツール](../tools-reference/)：コマンドライン
- [よくある問題](./common-issues/)：FAQ
