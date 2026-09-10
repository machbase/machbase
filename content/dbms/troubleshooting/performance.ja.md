---
type: docs
title: '15.4 クエリと性能の問題'
weight: 40
toc: true
---

<a id="slow"></a>

## クエリが遅い場合

対象 SQL、バインド値の範囲、開始・終了時刻、期待行数と実際の行数を記録します。

```sql
SELECT ID, SESS_ID, STATE, QUERY
  FROM V$STMT
 ORDER BY ID;

EXPLAIN SELECT ...;
```

実行計画で次を確認します。

- 時間・タグ条件が十分早い段階で適用されるか。
- 大きなテーブルを不必要に繰り返しスキャンしていないか。
- 結合キーの型と値の形式が一致するか。
- 必要なインデックスや ROLLUP が実際に使われているか。
- 不要な列や行を読んでいないか。

MINMAX キャッシュの現在のプロパティ名は `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE` です。
変更前に現在値と実行計画を記録し、隔離環境で比較してください。詳細は
[性能チューニング](/dbms/performance-tuning/)に従います。

<a id="search-results"></a>

## 検索結果が期待と異なる場合

```sql
SELECT COUNT(*), MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME)
  FROM target_log;
```

1. 対象データベース、所有者、テーブル名を確認します。
2. フィルターなしで少量を読み、データの存在と実際の時刻を確認します。
3. 接続タイムゾーンと入力文字列の時刻解釈を確認します。
4. タグ名、大文字・小文字、境界演算子（`>`、`>=`、`<`、`<=`）を確認します。
5. ROLLUP なら gap と更新状態を確認します。

サーバープロパティ `DEFAULT_TIMEZONE` を探さないでください。タイムゾーンはクライアント接続と
セッションで明示し、元データの基準タイムゾーンも記録します。

```sql
SHOW ROLLUPGAP;
SELECT * FROM V$ROLLUP;
```

<a id="memory-out-of"></a>

## メモリ不足

```sql
SELECT * FROM V$SYSMEM;
SELECT ID, SESS_ID, STATE, QUERY FROM V$STMT ORDER BY ID;
```

OS メモリ、スワップ、OOM 記録と、同時刻の Machbase ログを併せて確認します。大量結果の一括取得、
大きな結合・ソート、過剰な同時実行、大きなクライアント fetch・Append バッファを個別に再現します。

現在値は `V$PROPERTY` で確認します。許容範囲と変更方法は
[設定リファレンス](/dbms/reference/configuration/configuration/)で調べ、1項目ずつ負荷試験して適用します。
