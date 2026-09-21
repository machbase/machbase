---
title: '集計用のロールアップテーブル'
type: docs
weight: 60
description: 'ロールアップの作成と検索、JSON SUMMARIZED、FIRST/LAST、時間間隔によるグループ化を説明します。'
toc: true
---

## 概要 {#overview}

ロールアップテーブルは、Tag データを時間単位で自動集計し、分析やレポートのクエリー性能を大幅に向上させます。数百万件の元レコードをスキャンする代わりに、さまざまな時間間隔の統計を事前に計算しておきます。

## 時間軸専用の機能 {#time-axis-feature-only}

ROLLUP は、時間軸（`BASETIME`、`BASE TIME`）の Tag テーブルでのみ使用できます。距離軸（`BASE DISTANCE`、`BASEDISTANCE`）の Tag テーブルでは、次の機能は使用できません。

- `WITH ROLLUP(...)`
- `CREATE ROLLUP ... ON <distance_tag> ...`
- `CREATE ROLLUP ... INTO (...) AS (...)`

たとえば、次の文は失敗します。

```sql
CREATE TAG TABLE trip_rollup_test (
    name        VARCHAR(20) PRIMARY KEY,
    distance_m  DOUBLE BASE DISTANCE,
    value       DOUBLE SUMMARIZED
) WITH ROLLUP(SEC);

[ERR-04999: ROLLUP is not supported on DISTANCE axis TAG table.]
```

距離軸のテーブルでは、代わりに次の方法を使用します。

- `BETWEEN a AND b` による直接の範囲検索
- `TRUNC(distance / bucket, 0) * bucket` によるバケット集計
- `EXPLAIN` で、距離条件がキー範囲として使用されているかを確認

## ロールアップの作成 {#creating-rollup-tables}

Tag テーブルを作成しても、ロールアップは既定では作成されません。次の構文で直接作成してください。

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

* rollup name：作成するロールアップテーブルの名前（最大 40 文字の文字列で自由に指定可能）
* source table name：ロールアップが集計する集計元テーブルの名前
* src_table_column：集計対象の列の名前
    * 既定では数値型の列だけを指定できます。
    * `JSON SUMMARIZED` は、`value` の JSON 文書全体を集計する特別なモードとしてサポートされます。
    * 集計元がロールアップテーブルの場合は省略し、集計元のロールアップ対象列が自動的に使用されます。
* number sec/min/hour：集計する時間の長さと時間単位 <br>
   例）1 秒単位の集計：1 sec <br>
   例）30 秒単位の集計：30 sec <br>
   例）1 分単位の集計：1 min <br>
   例）1 時間単位の集計：1 hour <br>
* 制約
    * 集計元には Tag テーブルまたはロールアップテーブルだけを指定できます。
    * 集計元がロールアップテーブルの場合、作成するロールアップの間隔は集計元の間隔より大きく、その整数倍である必要があります。

ロールアップテーブルの作成例

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
 
-- Error when creating rollup for non-numeric type columns
Mach> CREATE ROLLUP _tag_rollup_sec ON tag(strvalue) INTERVAL 1 SEC;
[ERR-02671: Invalid type for ROLLUP column (STRVALUE).]
```

### ROLLUP テーブルの自動作成 {#automatically-create-a-rollup-table}

`WITH ROLLUP (time_unit)` キーワードで、ロールアップテーブルを自動作成できます。

```sql
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP (time_unit)
 
time_unit := {SEC|MIN|HOUR}
```

次のように `time_unit` を省略すると、SEC を基準に作成します。

```sql
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP
```

自動作成されるロールアップの名前は、次の形式です（`tagtbl` には Tag テーブル名が入ります）。

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

`time_unit` に指定した単位を最小単位とし、それより大きい時間単位のロールアップも自動作成します。

> ロールアップテーブルの名前が衝突した場合、ロールアップテーブルの作成はすべて失敗し、Tag テーブルだけが作成されます。

ロールアップを自動作成するときに、ロールアップの DATA_PART_SIZE をバイト単位で指定できます。

```sql
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP ROLLUP_DATA_PART_SIZE=(data_part_size)
```

### 拡張ロールアップ {#extended-rollup}

ロールアップの作成構文の末尾に `EXTENSION` キーワードを追加すると、拡張ロールアップを作成できます。
拡張ロールアップは、各間隔の先頭値と末尾値も保持します。

```sql
-- EXTENSION を手動作成
CREATE ROLLUP _tag_rollup_sec ON tag(value) INTERVAL 1 SEC EXTENSION;

-- EXTENSION を自動作成
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP EXTENSION;
```

## 条件付きロールアップ・フィルター・ヒント {#conditional-rollups-filters-and-hints}

### この機能が解決する課題 {#what-this-feature-solves}
間隔、値列、JSON パスが同じロールアップが複数ある場合、エンジンは「フィルターなし」と「フィルター付き」のロールアップを区別し、フィルターなしのロールアップを自動的に優先します。ヒントを使用すると、特定のロールアップを強制的に使用できます。フィルターは作成時に検証されるため、紛らわしい定義や安全でない定義はすぐに拒否されます。

### フィルター付きロールアップの作成方法 {#how-to-create-a-filtered-rollup}

```sql
CREATE ROLLUP <rollup_name>
  ( ON <table_name>(<value_col>)
  | FROM <src_rollup_table_name> )
  INTERVAL <n> <SEC|MIN|HOUR>
  WHERE <predicate>;
```

- 条件は集計の**前に**元の行に適用されます。条件に使用した列は、ロールアップテーブルに保存されません。
- 使用可能：既存の列を参照する一般的なスカラー式（AND/OR/NOT、比較、BETWEEN、IN、LIKE、CASE、非集計関数）。`value2` や `status` のような非 SUMMARIZED 列も条件に使用できます。
- 使用不可：サブクエリー、集計関数、存在しない列、Tag テーブルのタグ名（PK）列（タグ名は内部では数値のため、文字列比較は意味を持ちません）。
- 条件は `CREATE ROLLUP` の実行時に検証され、不正な条件はすぐにエラーになります。

### 条件付きロールアップとカスタムロールアップの `WHERE` {#where-in-conditional-rollup-vs-custom-rollup}
- 条件付きロールアップは、`ON/FROM` 構文の外側の `WHERE` を使用します。
- カスタムロールアップ（`INTO ... AS (SELECT ...)`）は、`SELECT` 内の `WHERE` だけをサポートします。
- したがって、`CREATE ROLLUP ... INTO (...) AS (...) INTERVAL ... WHERE ...` の形式は無効です。
- 構文の詳細は、[カスタムロールアップ：ユーザー定義集計](../rollup-custom/)と [DDL：CREATE ROLLUP](../../../sql-reference/ddl/#create-rollup) を参照してください。

### 自動選択の順序（ヒントなし） {#automatic-selection-order-no-hint}
1. `ROLLUP_TABLE(<rollup_table_name>)` ヒントがあれば、常にそのロールアップを使用します。
2. ヒントがなければ、間隔、値列、JSON パスが一致する候補のうち、**条件なし**のロールアップを優先します。
3. 条件なしのロールアップがなければ、条件付きのロールアップを使用します。
4. 候補が複数残る場合は、既存の規則に従います。要求された間隔を割り切れる最大の間隔を選び、間隔が同じなら最初に登録されたロールアップを使用します。

### 簡単な手順（回帰テストのシナリオに基づく） {#quick-recipe-mirrors-the-regression-scenario}
1) SUMMARIZED の `value` に加えて、`value2 DOUBLE`、`status INTEGER` など、フィルターに使用する列を持つ Tag テーブルを作成します。  
2) 条件なしと条件付きの両方のロールアップを作成します。

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

3) バルクローダーまたは INSERT でデータを入力し、強制実行（フラッシュ）して集計結果を使えるようにします。`_TAG_BULK_ROLLUP_SEC` に対する `ROLLUP_FORCE` は、集計元を `WITH ROLLUP` で作成した場合だけ実行します。

```sql
EXEC ROLLUP_FORCE(_TAG_BULK_ROLLUP_SEC);   -- WITH ROLLUP による自動作成
EXEC ROLLUP_FORCE(_tag_rollup_plain_1s);
EXEC ROLLUP_FORCE(_tag_rollup_cond_1s);
```

4) ヒントなしで検索すると、条件なしのロールアップが自動的に使用されます。

```sql
SELECT rollup('sec', 30, time) AS rt, AVG(value), COUNT(value)
FROM   tag_bulk
WHERE  name = 'dev9' AND time BETWEEN '2020-01-02 00:00:00' AND '2020-01-02 00:10:00'
GROUP BY rt
ORDER BY rt;
```

5) 条件を必ず適用する必要がある場合は、ヒントで条件付きロールアップを指定します。

```sql
SELECT /*+ ROLLUP_TABLE(_tag_rollup_cond_1s) */
       rollup('sec', 30, time) AS rt, AVG(value), COUNT(value)
FROM   tag_bulk
WHERE  name = 'dev9' AND time BETWEEN '2020-01-02 00:00:00' AND '2020-01-02 00:10:00'
GROUP BY rt
ORDER BY rt;
```

6) `FIRST()`/`LAST()` を使用する場合は、ヒントの対象を `EXTENSION` ロールアップにします。拡張でないロールアップでは、これらの関数を使用できません。

### メタデータと更新時の注意 {#metadata-and-upgrade-notes}
- `V$ROLLUP` の `PREDICATE` 列で、ロールアップの作成時に指定したフィルターを確認できます。
- この列を追加するため、メタバージョンは 10.0 に上がります。アップグレード後にサーバーを初めて起動すると、カタログが自動的に変更されます。非常に古い、または破損したメタデータなどでアップグレードに失敗した場合は、サーバーを停止し、元の DB を保全したうえで、新しい DB へデータを復旧または移行し、ロールアップを再作成してください。
- ロールアップの作成時には、間隔（倍数）と値の型（数値）に関する既存の制約がそのまま適用されます。フィルターによってこれらの制約は変わりません。

## ロールアップの開始と停止 {#startstop-rollup-table}

ロールアップを作成すると、ワーカースレッドが自動的に開始されます。その後は、ストアドプロシージャまたは SQL 構文で開始と停止を制御できます。

```sql
-- ロールアップの開始と停止
ALTER ROLLUP <rollup_name> START;
ALTER ROLLUP <rollup_name> STOP;

-- 同等のプロシージャ
EXEC ROLLUP_START(<rollup_name>);
EXEC ROLLUP_STOP(<rollup_name>);
```

### 起動間隔とスケジュール {#wakeup-interval-and-scheduling}
- 各ロールアップは、個別のスケジュールで起動します。既定の起動間隔はロールアップの間隔と同じですが、（ロールアップの境界に合うよう、間隔の約数で）短くして、より頻繁に起動できます。
- 起動間隔の変更構文：

```sql
ALTER ROLLUP <rollup_name> SET WAKEUP INTERVAL <N> (SEC|MIN|HOUR);
```

  - `N` は 0 より大きくなければなりません。
  - `N` を秒に換算した値は、ロールアップの間隔**以下**でなければなりません。
  - ロールアップの間隔が起動間隔の整数倍でない場合は、エラーになります。
  - 変更すると、スレッドが直ちに起動し、次回の起動予定を再計算します。
- 監視：`V$ROLLUP` の `WAKEUP_INTERVAL`、`LAST_WAKEUP_TIME`、`NEXT_WAKEUP_TIME`、`RUN_STATE`（INIT/SLEEPING/RUNNING）で確認できます。`show rollupgap` でも、前回と次回の起動時刻、実行状態を確認できます。


## ロールアップの即時集計 {#collect-rollup-instantly}

ロールアップは、既定では設定した時間間隔ごとにデータを集計します。

* 例）1 時間単位のロールアップは、1 時間に 1 回データを集計し、それ以外の時間は待機します。

待機時間を待たずに、手動で集計を強制実行できます。

```sql
-- 待機なし：ワーカーに通知して戻る
ALTER ROLLUP <rollup_name> WAKEUP;

-- 待機あり：直ちに実行して完了を待つ
ALTER ROLLUP <rollup_name> FORCE;
-- 同等のプロシージャ
EXEC ROLLUP_FORCE(<rollup_name>);
```

### ロールアップ再構築の参考情報 {#rollup-rebuild-reference}

元の TAG データを削除したり、修正したデータを再入力したりしても、既存のロールアップ結果は自動的には巻き戻りません。
組み込みロールアップの期間指定による復旧、`EXEC ROLLUP_REBUILD(...)` の使い方、カスタムロールアップの手動復旧手順は、[ロールアップ再構築ガイド](../rollup-rebuild/)を参照してください。


## ロールアップの削除 {#drop-rollup}

指定したロールアップを削除します。

```sql
DROP ROLLUP rollup_name
```

* rollup_name：削除するロールアップの名前
* 制約：削除するロールアップを集計元として参照しているロールアップがあると、エラーになります。ロールアップ間に依存関係がある場合は、作成した順序の逆順に削除してください。

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

### TAG テーブルと一緒にロールアップテーブルを削除 {#when-deleting-the-tag-table-delete-the-rollup-table-together}
`CASCADE` キーワードを指定して Tag テーブルを削除すると、その Tag テーブルに依存するロールアップテーブルも一緒に削除されます。

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

--ex)
SELECT ROLLUP('MIN', 30, time, '1970-01-01'), MIN(value), MAX(value), AVG(value) FROM tag ..
```

上のように ROLLUP キーワードを使用すると、該当するロールアップテーブルからデータを取得します。

* time_unit：`DATE_BIN()` 関数で使用できる時間単位
* period：`time_unit` 単位での区間の長さ。単位ごとに指定できる範囲は `DATE_BIN()` 関数と同じです。
* basetime_column：`BASETIME` 属性で指定した Tag テーブルの DATETIME 型の列
* origin：ROLLUP の時間区間を区切る基準時刻。省略すると、既定値の `1970-01-01 00:00:00` を使用します。

> **非推奨（8.0.19 以前）**<br>
> 8.0.19 以前のバージョンでは、次の ROLLUP 式を使用します。
> ```sql
> rollup_expr := basetime_column ROLLUP n time_unit
>
> -- ex)
> SELECT time ROLLUP 30 MIN, MIN(value), MAX(value), AVG(value) FROM tag ..
> ```

上のように、`BASETIME` 属性で指定した DATETIME 型の列の後に ROLLUP 句を付けると、ロールアップテーブルを検索します。

TIME_UNIT によって、検索するロールアップテーブルが変わります。

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

ROLLUP 句はロールアップテーブルを直接検索するため、集計関数の使用には次の特性があります。

* **集計関数は数値型の列に対して呼び出す必要があります。** ただし、使用できるのはロールアップテーブルが対応する 6 種類の集計関数（SUM、COUNT、MIN、MAX、AVG、SUMSQ）だけです。
    * 拡張ロールアップでは、FIRST と LAST も使用できます。
* **GROUP BY は、ROLLUP 対象の `BASETIME` 列で直接指定する必要があります。**
    * 同じ ROLLUP 句を GROUP BY にそのまま記述できます。
    * または、ROLLUP 句に別名を付け、その別名を GROUP BY に記述しても構いません。

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

ロールアップの例で使用するサンプルデータです。

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

1 つのタグに、異なる値の 18 行を秒単位で入力しています。データは 3 つの 1 時間バケットにまたがります。入力直後に結果を確認する場合は、`EXEC ROLLUP_FORCE(_TAG_ROLLUP_SEC)`、`EXEC ROLLUP_FORCE(_TAG_ROLLUP_MIN)`、`EXEC ROLLUP_FORCE(_TAG_ROLLUP_HOUR)` を順に実行します。


## AVG の取得 {#get-rollup-avg}

このタグの秒、分、時間単位の平均値を取得する例です。

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

このタグの時間区間ごとの最小値と最大値を取得する例です。前の例と異なり、1 回のクエリーで最小値と最大値を同時に取得できます。

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

合計と件数を取得する例です。この場合も、1 回のクエリーで合計と件数を同時に取得できます。

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

`value JSON SUMMARIZED` を使用すると、JSON のパスを個別に指定しなくても、`value` 文書全体を対象に ROLLUP 集計を実行できます。

1 つの JSON 文書に、指標、座標、カウンターなど複数の数値リーフが含まれる場合に便利です。集計結果はオブジェクト構造を維持し、数値リーフだけを集計します。

### 対応範囲 {#supported-scope}

- DDL：`value JSON SUMMARIZED`
- 集計関数：`AVG(value)`、`MIN(value)`、`MAX(value)`、`SUM(value)`、`SUMSQ(value)`
- 件数：`COUNT(value)`、`COUNT(*)`
- `FIRST(time, value)` と `LAST(time, value)` は、`EXTENSION` ロールアップでのみ使用できます。

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

不正な JSON は入力時に拒否されるため、ロールアップの集計には含まれません。

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

- オブジェクトは、パスの和集合を維持したまま再帰的にマージされます。
- 集計されるのは数値リーフだけです。
- 文字列、真偽値、null、配列は数値集計から除外されます。配列は平坦化されません。
- 存在しないパスは、出力オブジェクトに作成されません。
- 同じパスでキーが重複した場合は、パーサーによる正規化後の最後の値が使用されます。
- `COUNT(value)` は `value` が NULL でない行数を、`COUNT(*)` は全行数を数えます。

### 確認事項 {#what-to-check}

- `rollup('sec'|'min'|'hour', ...)` の結果で、構造の保持と数値リーフの集計を確認します。
- `COUNT(value)` と `COUNT(*)` を個別に確認します。
- `FIRST/LAST` を `EXTENSION` ロールアップでのみ使用していることを確認します。
- `FIRST/LAST` は元の JSON 文書全体を返すため、文書サイズによる通信量とストレージへの影響を考慮します。

## `FIRST/LAST` の取得 {#get-rollup-firstlast}

拡張ロールアップが提供する先頭値と末尾値を取得する例です。

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

ROLLUP 句を使用すると、時間間隔を変えるために `DATE_BIN()` を別途使用する必要がありません。

3 秒単位の合計と件数は、次のように取得できます。
サンプルデータには各分の 1 秒と 2 秒にしか値がないため、すべて 0 秒のバケットにまとまります。そのため、結果は分単位のロールアップの検索結果と一致します。

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

以下の例は、先の 2018 年のサンプルとは別に、検索期間の毎日 00:00:00 に 1 行ずつデータがあると仮定した出力例です。

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

origin を省略すると、（木曜日～水曜日）の範囲で集計されます。（日曜日～土曜日）の範囲で集計するには、origin に日曜日に当たる日時を指定する必要があります。

```sql
Mach> SELECT ROLLUP('week', 2, time, '2024-05-05') AS mtime, COUNT(value) FROM tag WHERE time BETWEEN TO_DATE('2024-05-01') AND TO_DATE('2024-05-31') GROUP BY mtime ORDER BY mtime;
mtime                           COUNT(value)         
--------------------------------------------------------
2024-04-21 00:00:00 000:000:000 4                    
2024-05-05 00:00:00 000:000:000 14                   
2024-05-19 00:00:00 000:000:000 13    
```

### 月単位 {#month-rollup}

origin には、常に月の初日（1 日）を指定する必要があります。

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
