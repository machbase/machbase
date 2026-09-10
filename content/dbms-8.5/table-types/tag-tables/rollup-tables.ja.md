---
title: '集計用のロールアップテーブル'
type: docs
weight: 60
description: 'ロールアップの作成と検索、JSON SUMMARIZED、FIRST/LAST、時間間隔によるグループ化を説明します。'
toc: true
---

## 概要 {#overview}

Tag データを時間単位で自動集計し、分析やレポートを高速化します。多数の元レコードを毎回読む代わりに、各間隔の統計を事前に計算します。

## 時間軸専用の機能 {#time-axis-feature-only}

`BASETIME` / `BASE TIME` の Tag でのみ利用できます。距離軸（`BASE DISTANCE` / `BASEDISTANCE`）では、次の機能は使用できません。

- `WITH ROLLUP(...)`
- `CREATE ROLLUP ... ON <distance_tag> ...`
- `CREATE ROLLUP ... INTO (...) AS (...)`

次の例は失敗します。

```sql
CREATE TAG TABLE trip_rollup_test (
    name        VARCHAR(20) PRIMARY KEY,
    distance_m  DOUBLE BASE DISTANCE,
    value       DOUBLE SUMMARIZED
) WITH ROLLUP(SEC);

[ERR-04999: ROLLUP is not supported on DISTANCE axis TAG table.]
```

距離軸には次を使用します。

- `BETWEEN a AND b` による範囲検索
- `TRUNC(distance / bucket, 0) * bucket` によるバケット集計
- `EXPLAIN` による距離条件のキー範囲確認

## ロールアップの作成 {#creating-rollup-tables}

Tag の作成時に、既定ではロールアップは作成されません。次の構文で定義してください。

![create-rollup](/dbms-8.5/table-types/tag-tables/create-rollup.png)

公開構文：

```sql
CREATE ROLLUP [IF NOT EXISTS] rollup_name
  ON source_table(column_name)
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)]
  [EXTENSION]
  [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] rollup_name
  ON source_table(json_column->'$.path')
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)]
  [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] rollup_name
  FROM source_rollup_table
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)]
  [EXTENSION]
  [WHERE predicate];
```

* rollup name：名前。最大 40 文字で指定可能。
* source table name：集計元のテーブル名。
* src_table_column：集計する値列。
    * 基本は数値列。
    * `JSON SUMMARIZED` は、`value` の JSON 文書全体を集計する特別なモード。
    * 入力元がロールアップの場合は省略し、元の対象列を自動的に使用。
* number sec/min/hour：集計の長さと単位。<br>
   1 秒：1 sec<br>
   30 秒：30 sec<br>
   1 分：1 min<br>
   1 時間：1 hour<br>
* 制約
    * 入力元は Tag またはロールアップだけ。
    * 入力元がロールアップなら、元より大きく、元の間隔の整数倍であること。


作成例

```bash
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE, strvalue VARCHAR(20));
Executed successfully.
 
-- Tag に 1 秒ロールアップを作成
Mach> CREATE ROLLUP _tag_rollup_sec ON tag(value) INTERVAL 1 SEC;
  
-- Tag に 1 分ロールアップを作成
Mach> CREATE ROLLUP _tag_rollup_min ON tag(value) INTERVAL 1 MIN;
  
-- Tag に 1 時間ロールアップを作成
Mach> CREATE ROLLUP _tag_rollup_hour ON tag(value) INTERVAL 1 HOUR;
  
-- Tag に 30 秒ロールアップを作成
Mach> CREATE ROLLUP _tag_rollup_30sec ON tag(value) INTERVAL 30 SEC;
  
-- 上記ロールアップに 10 分ロールアップを作成
Mach> CREATE ROLLUP _tag_rollup_10min ON _tag_rollup_30sec INTERVAL 10 MIN;
 
-- 非数値列のロールアップはエラー
Mach> CREATE ROLLUP _tag_rollup_invalid ON tag(strvalue) INTERVAL 1 SEC;
[ERR-02671: Invalid type for ROLLUP column (STRVALUE).]
```

### 自動作成 {#automatically-create-a-rollup-table}

WITH ROLLUP(time_unit) で自動作成できます。

```sql
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP (time_unit)
 
time_unit := {SEC|MIN|HOUR}
```

time_unit を省略すると SEC を使用します。

```sql
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP
```

自動生成名は次の形式です。`tagtbl` は元テーブル名です。
* _`tagtbl`_ROLLUP_SEC
* _`tagtbl`_ROLLUP_MIN
* _`tagtbl`_ROLLUP_HOUR

```sql
Mach> CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP (SEC)
 
Mach> SHOW TABLES;
USER_NAME             DB_NAME                                             TABLE_NAME                                          TABLE_TYPE 
-----------------------------------------------------------------------------------------------------------------------------------------------
SYS                   MACHBASEDB                                          TAGTBL                                              TAGDATA    
SYS                   MACHBASEDB                                          _TAGTBL_DATA_0                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_1                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_2                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_3                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_META                                        LOOKUP     
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_HOUR                                 KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_MIN                                  KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_SEC                                  KEYVALUE   
[9] row(s) selected.
Elapsed time: 0.001
Mach>
```

指定単位を最小として、それより上位の時間単位も自動作成します。

> 名前が衝突した場合、すべてのロールアップ作成に失敗し、Tag テーブルだけが作成されます。

自動作成時に DATA_PART_SIZE をバイト単位で指定できます。
```sql
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP ROLLUP_DATA_PART_SIZE=(data_part_size)
```

### `EXTENSION` ロールアップ {#extended-rollup}

作成構文の末尾に `EXTENSION` を追加すると、間隔内の先頭値と末尾値を含む拡張ロールアップになります。

```sql
-- EXTENSION を手動作成
CREATE ROLLUP _tag_rollup_sec ON tag(value) INTERVAL 1 SEC EXTENSION;

-- EXTENSION を自動作成
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP EXTENSION;
```

## 条件付きロールアップとヒント {#conditional-rollups-filters-and-hints}

### 解決する課題 {#what-this-feature-solves}
間隔、値列、JSON パスが同じ候補で、フィルターなしとフィルター付きのロールアップを区別します。自動選択はフィルターなしを優先し、ヒントで特定の候補を強制できます。フィルターは作成時に検証します。

### フィルター付きの作成 {#how-to-create-a-filtered-rollup}
```sql
CREATE ROLLUP <rollup_name>
  ( ON <table_name>(<value_col>)
  | FROM <src_rollup_table_name> )
  INTERVAL <n> <SEC|MIN|HOUR>
  WHERE <predicate>;
```
- 集計前の元行に条件を適用します。条件列は集計先に保存しません。
- 使用可能：既存列を参照する AND/OR/NOT、比較、BETWEEN、IN、LIKE、CASE、非集計関数。`value2` や `status` のような非 SUMMARIZED 列も利用できます。
- 使用不可：サブクエリー、集計関数、存在しない列、タグ名（PK）列。タグ名は内部で数値のため、文字列比較は意味を持ちません。
- `CREATE ROLLUP` 時に検証し、不正な条件はエラーになります。

### 条件付きとカスタムの `WHERE` {#where-in-conditional-rollup-vs-custom-rollup}
- 条件付きは `ON/FROM` 形式の外側の `WHERE` を使用します。
- カスタム（`INTO ... AS (SELECT ...)`）は `SELECT` 内の `WHERE` だけを使用します。
- `CREATE ROLLUP ... INTO (...) AS (...) INTERVAL ... WHERE ...` は無効です。
- 詳細は[カスタムロールアップ](../rollup-custom/)と [CREATE ROLLUP](../../../sql-reference/ddl/#create-rollup) を参照してください。

### 自動選択の順序 {#automatic-selection-order-no-hint}
1. `ROLLUP_TABLE(<rollup_table_name>)` ヒントがあれば最優先。
2. なければ、間隔、値列、JSON パスが一致する候補のうち条件なしを優先。
3. 条件なしがなければ条件付き。
4. 複数残る場合は、要求間隔を割り切る最大の集計間隔を選択。同じなら最初に登録されたもの。

### 回帰テストに沿った手順 {#quick-recipe-mirrors-the-regression-scenario}
1）SUMMARIZED の `value` に加え、フィルター用の `value2 DOUBLE`、`status INTEGER` などを定義します。
2）通常と条件付きの両方を作成します。
```sql
CREATE ROLLUP _tag_rollup_plain_1s      ON tag_bulk(value) INTERVAL 1 SEC;
CREATE ROLLUP _tag_rollup_plain_1m      FROM _tag_rollup_plain_1s INTERVAL 1 MIN;
CREATE ROLLUP _tag_rollup_cond_1s       ON tag_bulk(value) INTERVAL 1 SEC
  WHERE value2 >= 50 AND status >= 2;
CREATE ROLLUP _tag_rollup_cond_1m       FROM _tag_rollup_cond_1s INTERVAL 1 MIN;

-- FIRST()/LAST() 用の EXTENSION
CREATE ROLLUP _tag_rollup_plain_1s_ext  ON tag_bulk(value) INTERVAL 1 SEC EXTENSION;
CREATE ROLLUP _tag_rollup_cond_1s_ext   ON tag_bulk(value) INTERVAL 1 SEC EXTENSION
  WHERE value2 >= 50 AND status >= 2;
```
3）ローダーまたは INSERT で入力し、強制実行して集計を反映します。`_TAG_BULK_ROLLUP_SEC` の呼び出しは、入力元を `WITH ROLLUP` で作成した場合だけ実行します。
```sql
EXEC ROLLUP_FORCE(_TAG_BULK_ROLLUP_SEC);   -- WITH ROLLUP による自動作成
EXEC ROLLUP_FORCE(_tag_rollup_plain_1s);
EXEC ROLLUP_FORCE(_tag_rollup_cond_1s);
```
4）ヒントなしで検索すると通常のロールアップを使用します。
```sql
SELECT rollup('sec', 30, time) AS rt, AVG(value), COUNT(value)
FROM   tag_bulk
WHERE  name = 'dev9' AND time BETWEEN '2020-01-02 00:00:00' AND '2020-01-02 00:10:00'
GROUP BY rt
ORDER BY rt;
```
5）条件を必ず適用する場合は、ヒントで条件付きを指定します。
```sql
SELECT /*+ ROLLUP_TABLE(_tag_rollup_cond_1s) */
       rollup('sec', 30, time) AS rt, AVG(value), COUNT(value)
FROM   tag_bulk
WHERE  name = 'dev9' AND time BETWEEN '2020-01-02 00:00:00' AND '2020-01-02 00:10:00'
GROUP BY rt
ORDER BY rt;
```
6）FIRST()/LAST() には `EXTENSION` を指定します。通常のロールアップでは使用できません。

### メタデータと更新時の注意 {#metadata-and-upgrade-notes}
- `V$ROLLUP` の `PREDICATE` で、作成時の条件を確認できます。
- この列の追加でメタバージョンは 10.0 になります。更新後の初回起動時に自動変更します。非常に古い、または破損したメタデータなどで更新に失敗した場合は、サーバーを停止して元の DB を保全したうえで、新しい DB への復旧・移行とロールアップの再作成を行います。
- 間隔と値型の既存の制約は変わりません。

## ロールアップの開始と停止 {#startstop-rollup-table}

作成時にワーカーが自動開始されます。その後はストアドプロシージャまたは SQL で制御できます。

```sql
-- ロールアップの開始と停止
ALTER ROLLUP <rollup_name> START;
ALTER ROLLUP <rollup_name> STOP;

-- 同等のプロシージャ
EXEC ROLLUP_START(<rollup_name>);
EXEC ROLLUP_STOP(<rollup_name>);
```

### 起動間隔とスケジュール {#wakeup-interval-and-scheduling}
- 各ワーカーは個別の予定で起動します。既定は集計間隔と同じですが、境界に合わせたまま頻度を上げられます。
- 変更構文：
```sql
ALTER ROLLUP <rollup_name> SET WAKEUP INTERVAL <N> (SEC|MIN|HOUR);
```
  - `N` は 0 より大きい値。
  - 秒換算で、集計間隔以下。
  - 集計間隔を割り切れる値でなければエラー。
  - 変更すると直ちに起動し、次回予定を再計算。
- `V$ROLLUP` の `WAKEUP_INTERVAL`、`LAST_WAKEUP_TIME`、`NEXT_WAKEUP_TIME`、`RUN_STATE`（INIT/SLEEPING/RUNNING）で確認できます。`show rollupgap` にも前回、次回、状態を表示します。


## 即時集計 {#collect-rollup-instantly}

通常は設定した間隔で集計します。

* 1 時間ロールアップは、1 時間ごとに集計してそれ以外は待機します。
必要に応じて強制実行できます。

```sql
-- 待機なし：ワーカーに通知して戻る
ALTER ROLLUP <rollup_name> WAKEUP;

-- 待機あり：直ちに実行して完了を待つ
ALTER ROLLUP <rollup_name> FORCE;
-- 同等のプロシージャ
EXEC ROLLUP_FORCE(<rollup_name>);
```

### 再構築について {#rollup-rebuild-reference}

元の TAG データを削除したり、修正値を再入力しても、既存の集計結果は自動的には戻りません。
期間指定の復旧、`EXEC ROLLUP_REBUILD(...)`、手動でのカスタム再構築は、[再構築ガイド](../rollup-rebuild/)を参照してください。


## ロールアップの削除 {#drop-rollup}

指定したロールアップを削除します。

```sql
DROP ROLLUP rollup_name
```

* rollup_name：対象の名前。
* 他のロールアップが入力元として依存しているとエラーになります。依存関係の逆順に削除してください。

```bash
mach> create tag table tag (name varchar(20) primary key, time datetime basetime, value double summarized);
mach> create rollup _tag_rollup_1 on tag(value) interval 1 sec;
mach> create rollup _tag_rollup_2 on _tag_rollup_1 interval 1 min;
mach> create rollup _tag_rollup_3 on _tag_rollup_2 interval 1 hour;
  
上の例では、依存関係は次の順序になる。
  
tag -> _tag_rollup_1 -> _tag_rollup_2 -> _tag_rollup_3
  
入力元の Tag や中間のロールアップを先に削除すると、エラーになる。
  
mach> drop table tag
> [ERR-02651: Dependent ROLLUP table exists.]
mach> drop rollup _tag_rollup_1
> [ERR-02651: Dependent ROLLUP table exists.]
  
依存先から順に、次の順序で削除する。
  
mach> drop rollup _tag_rollup_3;
mach> drop rollup _tag_rollup_2;
mach> drop rollup _tag_rollup_1;
mach> drop table tag;
```
### TAG と一緒に削除 {#when-deleting-the-tag-table-delete-the-rollup-table-together}
`CASCADE` を指定して Tag を削除すると、依存するロールアップも削除します。
```sql
DROP TABLE TAG CASCADE;
```
```sql
Mach> SHOW TABLES;
USER_NAME             DB_NAME                                             TABLE_NAME                                          TABLE_TYPE 
-----------------------------------------------------------------------------------------------------------------------------------------------
SYS                   MACHBASEDB                                          TAGTBL                                              TAGDATA    
SYS                   MACHBASEDB                                          _TAGTBL_DATA_0                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_1                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_2                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_3                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_META                                        LOOKUP     
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_HOUR                                 KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_MIN                                  KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_SEC                                  KEYVALUE   
[9] row(s) selected.
Elapsed time: 0.001
Mach>

Mach> DROP TABLE tagtbl CASCADE;
Dropped successfully.
 
Mach> show tables;
USER_NAME             DB_NAME                                             TABLE_NAME                                          TABLE_TYPE 
-----------------------------------------------------------------------------------------------------------------------------------------------
[0] row(s) selected.
```

## 検索構文 {#syntax}

```sql
rollup_expr := ROLLUP(time_unit, period, basetime_column [, origin])

--例
SELECT ROLLUP('MIN', 30, time, '1970-01-01'), MIN(value), MAX(value), AVG(value) FROM tag ..
```

ROLLUP を使用すると、適したロールアップテーブルから取得します。

* time_unit：DATE_BIN() が対応する時間単位。
* period：その単位での間隔。
* basetime_column：`BASETIME` 属性の DATETIME 列。
* origin：バケットの基準時刻。省略時は 1970-01-01。

> **非推奨（8.0.19 以前）**<br>
> 8.0.19 以前は、次の式を使用します。
>```sql
>rollup_expr := basetime_column ROLLUP n time_unit
>
>-- 例
>SELECT time ROLLUP 30 MIN, MIN(value), MAX(value), AVG(value) FROM tag ..
>```

`BASETIME` の DATETIME 列の後に ROLLUP を付けると、集計テーブルを選択します。

TIME_UNIT によって、参照するテーブルが変わります。

| 時間単位（略記） | ロールアップテーブル |
|--|--|
| ナノ秒（nsec） | SECOND |
| マイクロ秒（usec） | SECOND |
| ミリ秒（msec） | SECOND |
| 秒（sec） | SECOND |
| 分（min） | MINUTE |
| 時間（hour） | HOUR |
| 日（day） | HOUR |
| 週（week） | HOUR |
| 月（month） | HOUR |
| 年（year） | HOUR |

ROLLUP は集計テーブルを直接参照するため、集計関数には次の特性があります。

* 集計関数は数値列に適用し、対応するのは SUM、COUNT、MIN、MAX、AVG、SUMSQ の 6 種類です。
    * `EXTENSION` では FIRST、LAST も使用できます。
* GROUP BY は、ROLLUP 対象の `BASETIME` に対して直接指定します。
    * 同じ ROLLUP 式をそのまま使用できます。
    * ROLLUP 式に別名を付け、GROUP BY に指定しても構いません。

```sql
SELECT   rollup('sec', 3, time) mtime, avg(value)
FROM     TAG
GROUP BY mtime;

-- 非推奨
SELECT   time rollup 3 sec mtime, avg(value)
FROM     TAG
GROUP BY time rollup 3 sec mtime;
 
-- または
SELECT   time rollup 3 sec mtime, avg(value)
FROM     TAG
GROUP BY mtime;

```


## サンプルデータ {#data-sample}

テスト用データを示します。

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized) with rollup extension;
 
insert into tag metadata values ('TAG_0001');
 
insert into tag values('TAG_0001', '2018-01-01 01:00:01 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-01 01:00:02 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-01 01:01:01 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-01 01:01:02 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-01 01:02:01 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-01 01:02:02 000:000:000', 6);
 
insert into tag values('TAG_0001', '2018-01-01 02:00:01 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-01 02:00:02 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-01 02:01:01 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-01 02:01:02 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-01 02:02:01 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-01 02:02:02 000:000:000', 6);
 
insert into tag values('TAG_0001', '2018-01-01 03:00:01 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-01 03:00:02 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-01 03:01:01 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-01 03:01:02 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-01 03:02:01 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-01 03:02:02 000:000:000', 6);
```

1 タグに、3 つの時間バケットにまたがる 18 行を入力します。直後に結果を確認する場合は、`EXEC ROLLUP_FORCE(_TAG_ROLLUP_SEC)`、`EXEC ROLLUP_FORCE(_TAG_ROLLUP_MIN)`、`EXEC ROLLUP_FORCE(_TAG_ROLLUP_HOUR)` を順に実行します。



## AVG の取得 {#get-rollup-avg}

秒、分、時間単位の平均値を取得する例です。

```sql
Mach> SELECT rollup('sec', 1, time) as mtime, avg(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           avg(value)                  
---------------------------------------------------------------
2018-01-01 01:00:01 000:000:000 1                           
2018-01-01 01:00:02 000:000:000 2                           
2018-01-01 01:01:01 000:000:000 3                           
2018-01-01 01:01:02 000:000:000 4                           
2018-01-01 01:02:01 000:000:000 5                           
2018-01-01 01:02:02 000:000:000 6                           
2018-01-01 02:00:01 000:000:000 1                           
2018-01-01 02:00:02 000:000:000 2                           
2018-01-01 02:01:01 000:000:000 3                           
2018-01-01 02:01:02 000:000:000 4                           
2018-01-01 02:02:01 000:000:000 5                           
2018-01-01 02:02:02 000:000:000 6                           
2018-01-01 03:00:01 000:000:000 1                           
2018-01-01 03:00:02 000:000:000 2                           
2018-01-01 03:01:01 000:000:000 3                           
2018-01-01 03:01:02 000:000:000 4                           
2018-01-01 03:02:01 000:000:000 5                           
2018-01-01 03:02:02 000:000:000 6                           
[18] row(s) selected.

Mach> SELECT rollup('min', 1, time) as mtime, avg(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           avg(value)                  
---------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1.5                         
2018-01-01 01:01:00 000:000:000 3.5                         
2018-01-01 01:02:00 000:000:000 5.5                         
2018-01-01 02:00:00 000:000:000 1.5                         
2018-01-01 02:01:00 000:000:000 3.5                         
2018-01-01 02:02:00 000:000:000 5.5                         
2018-01-01 03:00:00 000:000:000 1.5                         
2018-01-01 03:01:00 000:000:000 3.5                         
2018-01-01 03:02:00 000:000:000 5.5                         
[9] row(s) selected.

Mach> SELECT rollup('hour', 1, time) as mtime, avg(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           avg(value)                  
---------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 3.5                         
2018-01-01 02:00:00 000:000:000 3.5                         
2018-01-01 03:00:00 000:000:000 3.5                         
[3] row(s) selected.
```


## MIN/MAX の取得 {#get-rollup-minmax-value}

秒、分、時間単位の最小値と最大値を、1 クエリーで同時取得できます。

```sql
Mach> SELECT rollup('hour', 1, time) as mtime, min(value), max(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           min(value)                  max(value)
--------------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1                           6
2018-01-01 02:00:00 000:000:000 1                           6
2018-01-01 03:00:00 000:000:000 1                           6
[3] row(s) selected.
 
Mach> SELECT rollup('min', 1, time) as mtime, min(value), max(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           min(value)                  max(value)
--------------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1                           2
2018-01-01 01:01:00 000:000:000 3                           4
2018-01-01 01:02:00 000:000:000 5                           6
2018-01-01 02:00:00 000:000:000 1                           2
2018-01-01 02:01:00 000:000:000 3                           4
2018-01-01 02:02:00 000:000:000 5                           6
2018-01-01 03:00:00 000:000:000 1                           2
2018-01-01 03:01:00 000:000:000 3                           4
2018-01-01 03:02:00 000:000:000 5                           6
[9] row(s) selected.
```


## SUM/COUNT の取得 {#get-rollup-sumcount}

合計と件数も、1 クエリーで同時取得できます。

```sql
Mach> SELECT rollup('min', 1, time) as mtime, sum(value), count(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           sum(value)                  count(value)
-------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 3                           2
2018-01-01 01:01:00 000:000:000 7                           2
2018-01-01 01:02:00 000:000:000 11                          2
2018-01-01 02:00:00 000:000:000 3                           2
2018-01-01 02:01:00 000:000:000 7                           2
2018-01-01 02:02:00 000:000:000 11                          2
2018-01-01 03:00:00 000:000:000 3                           2
2018-01-01 03:01:00 000:000:000 7                           2
2018-01-01 03:02:00 000:000:000 11                          2
[9] row(s) selected.
```


## 二乗和の取得 {#get-rollup-sum-of-squares}

ロールアップの二乗和を取得する例です。

```sql
Mach> SELECT rollup('sec', 1, time) as mtime, SUMSQ(value) FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           SUMSQ(value)               
---------------------------------------------------------------
2018-01-01 01:00:01 000:000:000 1                          
2018-01-01 01:00:02 000:000:000 4                          
2018-01-01 01:01:01 000:000:000 9                          
2018-01-01 01:01:02 000:000:000 16                         
2018-01-01 01:02:01 000:000:000 25                         
2018-01-01 01:02:02 000:000:000 36                         
2018-01-01 02:00:01 000:000:000 1                          
2018-01-01 02:00:02 000:000:000 4                          
2018-01-01 02:01:01 000:000:000 9                          
2018-01-01 02:01:02 000:000:000 16                         
2018-01-01 02:02:01 000:000:000 25                         
2018-01-01 02:02:02 000:000:000 36                         
2018-01-01 03:00:01 000:000:000 1                          
2018-01-01 03:00:02 000:000:000 4                          
2018-01-01 03:01:01 000:000:000 9                          
2018-01-01 03:01:02 000:000:000 16                         
2018-01-01 03:02:01 000:000:000 25                         
2018-01-01 03:02:02 000:000:000 36                         
[18] row(s) selected.
 
Mach> SELECT rollup('min', 1, time) as mtime, SUMSQ(value) FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           SUMSQ(value)               
---------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 5                          
2018-01-01 01:01:00 000:000:000 25                         
2018-01-01 01:02:00 000:000:000 61                         
2018-01-01 02:00:00 000:000:000 5                          
2018-01-01 02:01:00 000:000:000 25                         
2018-01-01 02:02:00 000:000:000 61                         
2018-01-01 03:00:00 000:000:000 5                          
2018-01-01 03:01:00 000:000:000 25                         
2018-01-01 03:02:00 000:000:000 61                         
[9] row(s) selected.
```

## `JSON SUMMARIZED` のロールアップ {#rollup-for-json-summarized}

`value JSON SUMMARIZED` では、パスを個別定義せず、`value` 文書全体を集計できます。

複数の数値リーフを持つ指標、座標、カウンターなどに適します。オブジェクト構造を維持し、数値だけを集計します。

### 対応範囲 {#supported-scope}

- DDL：`value JSON SUMMARIZED`
- 集計：`AVG(value)`、`MIN(value)`、`MAX(value)`、`SUM(value)`、`SUMSQ(value)`
- 件数：`COUNT(value)`、`COUNT(*)`
- `FIRST(time, value)` と `LAST(time, value)` は `EXTENSION` のみ。

### 主な例 {#representative-examples}

```sql
-- 既定のロールアップで JSON 文書全体を集計
CREATE TAG TABLE tag_json_rollup (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON SUMMARIZED
) WITH ROLLUP;

INSERT INTO tag_json_rollup VALUES ('HVAC_A', '2026-04-07 12:00:00', '{"metrics":{"temp":20,"pressure":1000},"location":{"x":6},"status":"ok"}');
INSERT INTO tag_json_rollup VALUES ('HVAC_A', '2026-04-07 12:00:01', '{"metrics":{"temp":22,"pressure":1002},"location":{"x":8},"status":true}');
INSERT INTO tag_json_rollup VALUES ('HVAC_A', '2026-04-07 12:00:02', '{"metrics":{"temp":24,"pressure":1004},"location":{"x":10},"status":null}');
-- 必要なら ROLLUP_FORCE または WAKEUP で即時集計

SELECT rollup('hour', 1, time) AS mtime,
       COUNT(value), MIN(value), MAX(value), AVG(value), SUM(value), SUMSQ(value)
  FROM tag_json_rollup
 WHERE name = 'HVAC_A'
 GROUP BY mtime
 ORDER BY mtime;
```

```sql
-- 文字列、真偽値、null が混在しても数値リーフだけを集計
CREATE TAG TABLE tag_json_mix (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON SUMMARIZED
) WITH ROLLUP TAG_PARTITION_COUNT=1;

INSERT INTO tag_json_mix VALUES ('HVAC_B', '2026-04-07 13:00:00', '{"metrics":{"temp":10,"pressure":100},"location":{"x":1},"mode":"AUTO","enabled":false}');
INSERT INTO tag_json_mix VALUES ('HVAC_B', '2026-04-07 13:00:01', '{"metrics":{"temp":20,"pressure":200},"location":{"x":2},"mode":"MANUAL","enabled":true}');
INSERT INTO tag_json_mix VALUES ('HVAC_B', '2026-04-07 13:00:02', '{"metrics":{"temp":30,"pressure":300},"location":{"x":3},"mode":null,"enabled":null}');
-- 必要なら ROLLUP_FORCE または WAKEUP で即時集計

SELECT rollup('hour', 1, time) AS mtime, COUNT(value), COUNT(*), AVG(value), MIN(value), MAX(value), SUM(value)
  FROM tag_json_mix
 GROUP BY mtime
 ORDER BY mtime;
```

```sql
-- 配列は平坦化しない。FIRST/LAST には EXTENSION が必要
CREATE TAG TABLE tag_json_mix2 (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON SUMMARIZED
) WITH ROLLUP EXTENSION TAG_PARTITION_COUNT=1;

INSERT INTO tag_json_mix2 VALUES ('HVAC_C', '2026-04-07 14:00:00', '{"metrics":{"temp":1,"pressure":10}, "location":{"x":1}, "history":[1,2,3]}');
INSERT INTO tag_json_mix2 VALUES ('HVAC_C', '2026-04-07 14:00:01', '{"metrics":{"temp":3,"pressure":30}, "location":{"x":2}, "history":[4,5]}');
INSERT INTO tag_json_mix2 VALUES ('HVAC_C', '2026-04-07 14:00:02', '{"metrics":{"temp":5,"pressure":50}, "location":{"x":3}, "history":[6]}');
-- 必要なら ROLLUP_FORCE または WAKEUP で即時集計

SELECT rollup('hour', 1, time) AS mtime,
       COUNT(value),
       AVG(value),
       SUM(value),
       FIRST(time, value),
       LAST(time, value)
  FROM tag_json_mix2
 GROUP BY mtime
 ORDER BY mtime;
```

```sql
-- RAW → SEC → MIN → HOUR の連鎖を作成
CREATE TAG TABLE tag_json_chain (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON SUMMARIZED
);
CREATE ROLLUP _tag_json_chain_sec  ON tag_json_chain(value) INTERVAL 1 SEC;
CREATE ROLLUP _tag_json_chain_min  ON _tag_json_chain_sec INTERVAL 1 MIN;
CREATE ROLLUP _tag_json_chain_hour ON _tag_json_chain_min INTERVAL 1 HOUR;
```

```sql
SELECT rollup('hour', 1, time) AS mtime, COUNT(value), AVG(value), SUMSQ(value)
  FROM tag_json_chain
 GROUP BY mtime
 ORDER BY mtime;
```

不正な JSON は入力時に拒否され、集計対象にはなりません。

```sql
-- 不正な JSON は入力されず、集計にも含まれない
CREATE TAG TABLE tag_json_bad (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON SUMMARIZED
) WITH ROLLUP;

INSERT INTO tag_json_bad VALUES ('HVAC_D', '2026-04-07 15:00:00', '{"metrics":{"temp":1,"pressure":2},"location":{"x":1}}');
INSERT INTO tag_json_bad VALUES ('HVAC_D', '2026-04-07 15:00:01', '{"metrics":{"temp":1,"pressure":2},"location":{"x":1}');
-- 入力時に拒否された行は集計から除外

SELECT rollup('hour', 1, time) AS mtime, COUNT(value), SUMSQ(value)
  FROM tag_json_bad
 GROUP BY mtime
 ORDER BY mtime;
```

### 動作規則 {#behavior-rules}

- パスの和集合を維持し、オブジェクトを再帰的にマージ。
- 数値リーフだけを集計。
- 文字列、真偽値、null、配列は数値集計から除外。配列は平坦化しない。
- 存在しないパスは出力に作成しない。
- 同じパスで重複したキーは、パーサーの正規化後の最後の値を使用。
- `COUNT(value)` は NULL でない行、`COUNT(*)` は全行を数える。

### 確認事項 {#what-to-check}

- `rollup('sec'|'min'|'hour', ...)` で構造の保持と数値リーフ集計を確認。
- `COUNT(value)` と `COUNT(*)` を個別に確認。
- `FIRST/LAST` は `EXTENSION` に限定。
- `FIRST/LAST` は元の JSON 文書全体を返すため、文書サイズによる通信量とストレージへの影響も確認。

## `FIRST/LAST` の取得 {#get-rollup-firstlast}

`EXTENSION` が提供する先頭値と末尾値の取得例です。

```sql
Mach> SELECT rollup('min', 1, time) as mtime, FIRST(time, value), LAST(time, value) FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           FIRST(time, value)          LAST(time, value)           
--------------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1                           2                           
2018-01-01 01:01:00 000:000:000 3                           4                           
2018-01-01 01:02:00 000:000:000 5                           6                           
2018-01-01 02:00:00 000:000:000 1                           2                           
2018-01-01 02:01:00 000:000:000 3                           4                           
2018-01-01 02:02:00 000:000:000 5                           6                           
2018-01-01 03:00:00 000:000:000 1                           2                           
2018-01-01 03:01:00 000:000:000 3                           4                           
2018-01-01 03:02:00 000:000:000 5                           6                           
[9] row(s) selected.

Mach> SELECT rollup('hour', 1, time) as mtime, FIRST(time, value), LAST(time, value) FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           FIRST(time, value)          LAST(time, value)           
--------------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1                           6                           
2018-01-01 02:00:00 000:000:000 1                           6                           
2018-01-01 03:00:00 000:000:000 1                           6                           
[3] row(s) selected.
```

## 任意の時間間隔でグループ化 {#grouping-at-various-time-intervals}

ROLLUP では、間隔を変えるために別途 DATE_BIN() を記述する必要がありません。

3 秒単位の合計と件数は、次のように取得できます。
例のデータは各分の 1 秒と 2 秒だけなので、すべて 0 秒のバケットにまとまります。そのため、分単位の集計結果と一致します。

```sql
Mach> SELECT rollup('sec', 3, time) as mtime, sum(value), count(value) FROM TAG WHERE name = 'TAG_0001' GROUP BY mtime ORDER BY mtime;
mtime                           sum(value)                  count(value)
-------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 3                           2
2018-01-01 01:01:00 000:000:000 7                           2
2018-01-01 01:02:00 000:000:000 11                          2
2018-01-01 02:00:00 000:000:000 3                           2
2018-01-01 02:01:00 000:000:000 7                           2
2018-01-01 02:02:00 000:000:000 11                          2
2018-01-01 03:00:00 000:000:000 3                           2
2018-01-01 03:01:00 000:000:000 7                           2
2018-01-01 03:02:00 000:000:000 11                          2
```

## 1 日以上のロールアップ {#rollup-of-more-than-1-day}

以下は先の 2018 年のサンプルとは別に、各対象期間の毎日 00:00:00 に 1 行のデータがある場合の出力例です。

### 日単位 {#day-rollup}

```sql
Mach> SELECT ROLLUP('day', 10, time, '2023-01-01') AS mtime, COUNT(value) FROM tag WHERE time BETWEEN TO_DATE('2023-05-01') AND TO_DATE('2023-05-31') GROUP BY mtime ORDER BY mtime;
mtime                           COUNT(value)         
--------------------------------------------------------
2023-05-01 00:00:00 000:000:000 10                   
2023-05-11 00:00:00 000:000:000 10                   
2023-05-21 00:00:00 000:000:000 10                   
2023-05-31 00:00:00 000:000:000 1                    
[4] row(s) selected.
```

### 週単位 {#week-rollup}

origin を省略すると木曜～水曜の範囲です。日曜～土曜にするには、origin に日曜日の日時を指定します。

```sql
Mach> SELECT ROLLUP('week', 2, time, '2024-05-05') AS mtime, COUNT(value) FROM tag WHERE time BETWEEN TO_DATE('2024-05-01') AND TO_DATE('2024-05-31') GROUP BY mtime ORDER BY mtime;
mtime                           COUNT(value)         
--------------------------------------------------------
2024-04-21 00:00:00 000:000:000 4                    
2024-05-05 00:00:00 000:000:000 14                   
2024-05-19 00:00:00 000:000:000 13    
```

### 月単位 {#month-rollup}

origin は必ず月の 1 日にします。

```
Mach> SELECT ROLLUP('month', 2, time) AS mtime, COUNT(value) FROM tag WHERE time BETWEEN to_date('2024-05-01') AND to_date('2024-07-31') GROUP BY mtime ORDER BY mtime;
mtime                           COUNT(value)         
--------------------------------------------------------
2024-05-01 00:00:00 000:000:000 61                   
2024-07-01 00:00:00 000:000:000 31                   
[2] row(s) selected.
Mach> SELECT ROLLUP('month', 1, time, '2024-05-05') AS mtime, COUNT(value) FROM tag WHERE time BETWEEN to_date('2024-05-01') AND to_date('2024-07-31') GROUP BY mtime ORDER BY mtime;
mtime                           COUNT(value)         
--------------------------------------------------------
[ERR-02356: Origin must be the first day of the month.]
```

### 年単位 {#year-rollup}

```
Mach> SELECT ROLLUP('year', 1, time, '2022-01-01') AS mtime, COUNT(value) FROM tag WHERE time BETWEEN TO_DATE('2022-01-01') AND TO_DATE('2023-12-31') GROUP BY mtime ORDER BY mtime;
mtime                           COUNT(value)         
--------------------------------------------------------
2022-01-01 00:00:00 000:000:000 365                  
2023-01-01 00:00:00 000:000:000 365                  
[2] row(s) selected.
```
