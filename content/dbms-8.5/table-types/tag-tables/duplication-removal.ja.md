---
title: '重複データの自動除去'
type: docs
weight: 90
toc: true
---

## 概要 {#overview}

Machbase は、指定した期間内でセンサー値の重複を自動検出して除去できます。手動操作なしでデータ品質を維持できます。

## 重複除去の設定 {#configuring-duplicate-removal}

TAG テーブルの作成時に、重複を確認する期間をテーブルプロパティで指定します。設定できる最大期間は 43200 分（30 日）です。

```sql
-- システム時刻から 1440 分（1 日）以内の既存データと重複する入力を除去する。

CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_DUPLICATE_CHECK_DURATION=1440;
```

設定値は m$sys_table_property テーブルで確認できます。
```sql
SELECT * FROM m$sys_table_property WHERE id={table_id} AND name = 'TAG_DUPLICATE_CHECK_DURATION';
```

データの挿入と検索の例：重複を確認する期間は 1440 分（1 日）です。
```sql
-- サーバー時刻を基準とした重複確認期間内のタイムスタンプを使用する。
-- DATE_TRUNC('day', NOW) は同じ日には同じタイムスタンプを返す。

INSERT INTO tag VALUES('tag1', DATE_TRUNC('day', NOW), 0);
INSERT INTO tag VALUES('tag1', DATE_TRUNC('day', NOW), 0);

EXEC TABLE_FLUSH(tag);

SELECT * FROM tag WHERE name = 'tag1';
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
tag1                  <current day> 00:00:00 000:000:000 0
  
```
## 設定の変更 {#changing-configuration}
TAG_DUPLICATE_CHECK_DURATION は次のように変更できます。

```sql
ALTER TABLE {table_name} set TAG_DUPLICATE_CHECK_DURATION={duration in minutes};
```

## 重複除去の制約 {#constraints-of-duplication-removal}

* 確認期間は分単位で指定でき、上限は 43200 分（30 日）です。
* 既存データを削除した後に同じデータを入力しても、重複とは判定されません。

## TRACE ログによる重複の確認 {#checking-duplicates-via-trace-log}
TRACE_LOG_LEVEL の 32（SM_2）ビットを有効にすると、重複除去のログを出力します。
以下の加算は、そのビットがまだ設定されていない場合だけ行います。すでに有効なら再加算しません。
```sql
-- 現在の設定を確認する
select name, value from v$property where name = 'TRACE_LOG_LEVEL';

-- 設定を変更する
alter system set TRACE_LOG_LEVEL={current_value + 32};
```

**設定例**
```sql
-- 現在の値を確認する
Mach> select name, value from v$property where name = 'TRACE_LOG_LEVEL';
name                                                          value
---------------------------------------------------------------------------------------------------------------------------------------------------
TRACE_LOG_LEVEL                                               277
[1] row(s) selected.

-- 32 を加える（277 + 32 = 309）
Mach> alter system set TRACE_LOG_LEVEL=309;
Altered successfully.
```

- ログファイル：`$MACHBASE_HOME/trc/machbase.trc`
- 絞り込みの例：
  ```bash
  tail -n 50 $MACHBASE_HOME/trc/machbase.trc | grep DUP_DROP
  ```
- ログ形式：`DUP_DROP Table=<table> TAG=<tag id> TIME=<timestamp> COL<n>=<value> ...`
- 実際の例（TAG=1 で TIME が同じ、COL3 の値が異なる場合）：
  ```
  [2025-11-29 13:50:27 P-151395 T-126344581076672][SM-INFO] DUP_DROP Table=TAG TAG=1 TIME=1998-12-24 09:00:00 000:000:012  COL3=12.000000
  ...
  [2025-11-29 13:50:27 P-151395 T-126344581076672][SM-INFO] DUP_DROP Table=TAG TAG=1 TIME=1998-12-24 09:00:00 000:000:048  COL3=48.000000
  ```
- 活用方法
  - TIME フィールドで、同じタイムスタンプのどの重複データが除去されたか確認します。
  - `grep "Table=TAG"` や `grep "TAG=1"` を追加すると、特定のテーブルやタグに絞り込めます。
- 注意：1 行の上限は約 4 KB です。列数が多い場合は末尾が切り詰められることがありますが、クラッシュは発生しません。
