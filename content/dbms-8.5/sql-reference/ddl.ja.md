---
title : 'DDL'
type: docs
weight: 20
toc: true
---

> **注意**：Machbase 8.5 以降で一般ユーザーが `CREATE`/`DROP` を実行するには、`MACHBASEDB` のデータベース権限が必要な場合があります。詳細は[ユーザー管理](../user-manage/#grantrevoke)を参照してください。

## `CREATE` TABLE {#create-table}

### 構文 {#syntax}

**create_table_stmt:**

![create_table_stmt](/images/sql/ddl/create_table_stmt.png)

**column_list:**

![column_list](/images/sql/ddl/column_list.png)

**column_property_list:**

![column_property_list](/images/sql/ddl/column_property_list.png)


**table_property_list:**

![table_property_list](/images/sql/ddl/table_property_list.png)


**column_type:**

![column_type](/images/sql/ddl/column_type.png)


**with_rollup:**

![with_rollup](/images/sql/ddl/with_rollup_opt.png)

#### LOG テーブルの作成 {#create-log-table}

```sql
-- 5 列の LOG テーブル ctest を作成
CREATE TABLE ctest (id INTEGER, name VARCHAR(20), sipv4 IPV4, dipv6 IPV6, comment TEXT);
```

#### TAG テーブルの作成 {#create-tag-table}

TAG には `PRIMARY KEY` と軸列が必要です。時間軸は `DATETIME BASETIME` または `DATETIME BASE TIME`、距離軸は `DOUBLE`/`LONG`/`ULONG` に `BASE DISTANCE` または `BASEDISTANCE` を指定します。`SUMMARIZED` は任意で、ロールアップや統計が必要な値列に使用します。

```sql
-- TAG テーブルを作成
CREATE TAG TABLE tag_time (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
CREATE TAG TABLE tag_time_ext (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED, value2 FLOAT, int_column INT);
CREATE TAG TABLE tag_distance (name VARCHAR(20) PRIMARY KEY, distance_m DOUBLE BASE DISTANCE, value DOUBLE, quality INT);
CREATE TAG TABLE tag_distance_meta (name VARCHAR(20) PRIMARY KEY, distance_m LONG BASEDISTANCE, value DOUBLE) METADATA (route_id VARCHAR(20));
```

距離軸の型は `DOUBLE`、`LONG`、`ULONG` だけです。`WITH ROLLUP` は時間軸の Tag でのみ使用できます。
`JSON` メタデータ列と `JSON INDEX(...)` は、[Tag メタデータ](../../table-types/tag-tables/tag-metadata)を参照してください。

#### テーブル名と列名の規則 {#rules-for-naming-tables-or-columns}

名前には英数字を使用します。特殊文字を使用する場合は二重引用符で囲みます。

```sql
CREATE TABLE special_tbl ( "with.dot" INTEGER );
```

#### IF NOT EXISTS {#if-not-exists}

既存テーブルがある場合のエラーを抑止します。ただし、既存の構造と `CREATE` TABLE の構造が同じかは検証しません。

同じテーブル型の場合だけ有効です。

### テーブルの種類 {#table-type}

| 型 | 説明 |
|--|--|
|LOG|`CREATE` と TABLE の間に型を指定しない場合に作成。|
|VOLATILE|データを一時メモリに保持し、Log との結合などに使用する一時テーブル。サーバー停止時にデータが失われる。|
|LOOKUP|Volatile と同様、データをメモリに保持して高速検索するテーブル。|


### テーブルプロパティ {#table-property}

テーブルの属性を指定します。

| プロパティ | 対応テーブル |
|--|--|
|TAG_PARTITION_COUNT|TAG|
|TAG_DATA_PART_SIZE|TAG|
|TAG_STAT_ENABLE|TAG|
|TAG_DUPLICATE_CHECK_DURATION|TAG|
|VARCHAR_FIXED_LENGTH_MAX|TAG|

#### TAG_PARTITION_COUNT（既定値：4） {#tag_partition_countdefault4}
内部のパーティション数を指定します。タグ数やサーバー性能に合わせて設定します。

#### TAG_DATA_PART_SIZE（既定値：16MB） {#tag_data_part_sizedefault16mb}
TAG の各パーティションのデータサイズを指定します。

#### TAG_STAT_ENABLE（既定値：1） {#tag_stat_enabledefault1}
タグ ID ごとの統計情報を保存するかを指定します。

#### TAG_DUPLICATE_CHECK_DURATION（既定値：0、最大：43200） {#tag_duplicate_check_durationdefault0-max43200}
現在のシステム時刻を基準として、重複を除去する期間を分単位で指定します。指定期間内のデータだけを確認します。0 は重複除去を行いません。

#### VARCHAR_FIXED_LENGTH_MAX（既定値：15、最大：127） {#varchar_fixed_length_max-default-15-max-127}

内部の固定長領域へ保存する VARCHAR の最大長を指定します。

### 列プロパティ {#column-property}

列の属性を指定します。

| プロパティ | 対応テーブル |
|--|--|
|PART_PAGE_COUNT|LOG|
|PAGE_VALUE_COUNT|LOG|
|MAX_CACHE_PART_COUNT|LOG|
|MINMAX_CACHE_SIZE|LOG|

**PART_PAGE_COUNT**
パーティションのページ数です。格納する値の数は PART_PAGE_COUNT × PAGE_VALUE_COUNT です。

**PAGE_VALUE_COUNT**
1 ページに格納する値の数です。

**MAX_CACHE_PART_COUNT（既定値：0）**
性能向上のためのキャッシュ領域を設定します。
パーティションにアクセスする際、メモリ内のメタ情報を先に確認します。この設定は、保持するパーティション情報の数です。大きいほど性能向上が期待できますが、メモリも増えます。最小値は 1、最大値は 65535 です。

**MINMAX_CACHE_SIZE（既定値：10240）**
列の MINMAX キャッシュに使うメモリです。0 番目の隠し列 _ARRIVAL_TIME は既定で 100MB、他の列は 10KB です。作成後は ALTER TABLE MODIFY で変更できます。

**NOT NULL 制約**
NULL を許可しない列には NOT NULL を指定します。省略時は許可します。
作成後も ALTER TABLE MODIFY COLUMN で追加、解除できます。

```sql
-- c1 に NOT NULL を指定し、c2 には指定しない
CREATE TABLE t1(c1 INTEGER NOT NULL, c2 VARCHAR(200));
```

**システム定義列**
`CREATE` TABLE では _ARRIVAL_TIME と _RID の 2 つのシステム列を追加します。

_ARRIVAL_TIME は、INSERT や AppendData の入力時刻を DATETIME として保存します。古い時刻から新しい時刻への順序を守れば、machloader や INSERT で値を明示できます。DURATION はこの列を基準に検索します。
_RID は、各レコードに自動生成される一意の 64 ビット整数です。ユーザーは値を指定できず、インデックスも作成できません。_RID によるレコード検索は可能です。

```sql
create volatile table t1111 (i1 integer);
Created successfully.
Mach> desc t1111;
 
----------------------------------------------------------------
NAME                          TYPE                LENGTH       
----------------------------------------------------------------
_ARRIVAL_TIME                 datetime            8              
I1                            integer             4              
 
Mach>insert into t1111 values (1);
1 row(s) inserted.
Mach>select _rid from t1111;
_rid                
-----------------------
0                   
[1] row(s) inserted.
 
Mach>select i1 from t1111 where _rid = 0;
i1         
--------------
1          
[1] row(s) selected.
```

### Min-Max キャッシュ {#min-max-cache}

#### 概念 {#the-concept-of-min-max-cache}

一般的なディスク DBMS のインデックス検索では、インデックス領域にアクセスしてから、対象の値があるデータページを読み取ります。

Machbase は時系列順にパーティションを分割するため、インデックスも時刻順のファイルに分割されます。検索時には各ファイルを順に調べます。
対象が 1000 パーティションに分かれると、毎回 1000 ファイルを開く必要があります。列指向で効率化しても I/O はパーティション数に比例するため、MINMAX_CACHE で改善します。
パーティションごとの列の最小値と最大値を、連続したメモリ領域に保持します。検索値がその範囲外ならパーティション全体を読み飛ばし、高速に分析できます。

![When you find a value "85"](/images/sql/ddl/whenyoufindavalue85.png)

図の 85 を検索する例では、5 つのうち範囲に含む 1 と 5 だけを検索し、2、3、4 を読み飛ばします。

#### 列の設定 {#min-max-cache-column}

テーブル作成時に、列ごとにキャッシュの使用を指定できます。

MINMAX_CACHE_SIZE が 0 以外なら有効、0 なら無効です。
注意事項：

1. 列にインデックスを明示的に作成する必要はありません。
2. 通常の列は既定で 10KB です。ALTER TABLE で適切な値に変更できます。
3. _arrival_time は既定で 100MB を使用します。
4. VARCHAR は対象外です。明示的に指定するとエラーになります。
5. パーティション数に応じて段階的に増え、設定した最大メモリ量まで使用します。
6. レコードがない場合は、メモリを確保しません。

作成例を示します。

```sql

-- VARCHAR に MINMAX_CACHE_SIZE=0 を指定することは可能
CREATE TABLE ctest (id INTEGER, name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE = 0));
Created successfully.
Mach>
 
-- id 列にキャッシュを適用
CREATE TABLE ctest2 (id INTEGER PROPERTY(MINMAX_CACHE_SIZE = 10240), name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE = 0));
Created successfully.
Mach>
 
-- id1、id2、id3 に適用
CREATE TABLE ctest3 (id1 INTEGER PROPERTY(MINMAX_CACHE_SIZE = 10240), name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE = 0), id2 LONG PROPERTY(MINMAX_CACHE_SIZE = 1024), id3 IPV4 PROPERTY(MINMAX_CACHE_SIZE = 1024), id4 SHORT);
Created successfully.
Mach>
 
-- 列単位で MINMAX_CACHE_SIZE を指定、または 0 で無効化
CREATE TABLE ctest4 (id1 INTEGER PROPERTY(MINMAX_CACHE_SIZE=10240), name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE=0), id2 LONG PROPERTY(MINMAX_CACHE_SIZE=10240), id3 IPV4 PROPERTY(MINMAX_CACHE_SIZE=0), id4 SHORT);
Created successfully.
Mach>
```

### 主キー {#primary-key}

Volatile/Lookup の列に設定できる制約で、列値の重複を防ぎます。
Lookup には必須です。Volatile は省略できますが、
`INSERT ... ON DUPLICATE KEY UPDATE` を使用するには、
主キーが必要です。

主キーに対応する RED-BLACK ツリーインデックスが作成されます。

### シーケンス列 {#sequence-column}

#### Lookup の SEQUENCE {#sequence-for-lookup-table}

Lookup のレコード識別と入力順序の管理に、シーケンスを使用できます。

日時が重複して順序を区別できない問題や、データ重複によるアプリケーションエラーを防ぐための機能です。

#### 作成時の設定 {#configuring-sequence-when-creating-lookup-tables}

シーケンスにする列へ PROPERTY 句を追加します。

シーケンス列は `LONG` 型（64 ビット）だけをサポートします。

開始値を指定できます。1 なら 1 から開始します。0 と負数は指定できません。

```sql
CREATE LOOKUP TABLE table_name (v1 LONG PROPERTY(SEQUENCE=1) PRIMARY KEY, v2 VARCHAR(10));
```

#### シーケンス列の使用 {#use-of-sequence-column}

通常の `LONG` 列として使用するだけでは、自動的には増加しません。

値を直接入力でき、重複値も入力できます。

自動採番には、専用関数 nextval を使用します。

内部で最大値を保持し、nextval は最大値 + 1 を格納します。

**シーケンス列の例**
```sql
-- シーケンス列に nextval で次の値を挿入
INSERT INTO table_name (v1, v2) values (nextval(v1), 'aaaa');
   
-- シーケンス列に直接値を挿入
INSERT INTO table_name (v1, v2) values (100, 'aaaa');
   
-- シーケンス列に計算値を挿入
INSERT INTO table_name (v1, v2) values (100 + 1, 'aaaa');
   
-- シーケンス列を持つ Lookup の正常な検索
SELECT v1, v2 FROM table_name;
  
-- 不正な検索：nextval は INSERT 専用
SELECT nextval(v1), v2 FROM table_name;
```

## `CREATE` VIEW / `DROP` VIEW {#create-view--drop-view}

ビューは `SELECT` の定義を名前付きの論理オブジェクトとして保存します。
データは別に保存せず、検索時に定義 SQL を
展開して実行します。

```sql
CREATE VIEW v_example AS
SELECT id, name
FROM t1;

DROP VIEW v_example;
```

`CREATE OR REPLACE VIEW`、`DROP VIEW IF EXISTS`、`SHOW VIEWS`、
`M$SYS_VIEWS`、性能と制限、Tag/`BINARY` の例は、
[VIEW](../view) を参照してください。

## `DROP` TABLE {#drop-table}

**drop_table_stmt:**

![drop_table_stmt](/images/sql/ddl/drop_table_stmt.png)

```sql
drop_table_stmt ::= 'DROP TABLE' table_name
```

指定したテーブルを削除します。他のセッションが検索中の場合はエラーになります。

```sql
-- 例
DROP TABLE TableName;
```

## `CREATE` TABLESPACE {#create-tablespace}

**create_tablespace_stmt:**

![create_tablespace_stmt](/images/sql/ddl/create_tablespace_stmt.png)

**datadisk_list:**

![datadisk_list](/images/sql/ddl/datadisk_list.png)

**data_disk:**

![data_disk](/images/sql/ddl/data_disk.png)

**data_disk_property:**

![data_disk_property](/images/sql/ddl/data_disk_property.png)

```sql
create_tablespace_stmt ::= 'CREATE TABLESPACE' tablespace_name 'DATADISK' datadisk_list
datadisk_list ::= data_disk ( ',' data_disk )*
data_disk ::= disk_name data_disk_property
data_disk_property ::= '(' 'DISK_PATH' '=' '"' path '"' ( ',' 'PARALLEL_IO' '=' number )? ')'
```

```sql
-- 例
create tablespace tbs1 datadisk disk1 (disk_path=""); -- $MACHBASE_HOME/dbs/（この場所に作成）
create tablespace tbs1 datadisk disk1 (disk_path="tbs1_disk1"); -- $MACHBASE_HOME/dbs/tbs1_disk1（この場所に作成。tbs1_disk1 は事前作成が必要）
create tablespace tbs2 datadisk disk1 (disk_path="tbs2_disk1", parallel_io = 5);
create tablespace tbs1 datadisk disk1 (disk_path="tbs1_disk1", parallel_io = 10), disk2 (disk_path="tbs1_disk2"), disk3 (disk_path="tbs1_disk3");
```

$MACHBASE_HOME/dbs/ に、Log テーブルやそのインデックスの保存先となるテーブルスペースを作成します。

複数ディスクを指定でき、テーブルとインデックスの各パーティションファイルを分散して保存します。
2 台以上のディスクでは、各装置で並列 I/O を実行します。台数を増やすと I/O スループットが向上し、大量データを高速保存できます。
テーブルとインデックスに別のテーブルスペースとディスクを割り当てると、物理ディスクの再構成なしで I/O を論理的に分離できます。

### DATA DISK {#data-disk}

テーブルスペース内のディスクを定義します。

| プロパティ | 説明 |
|--|--|
|data_disk_property|ディスクの属性。|
|disk_name|ディスクオブジェクト名。後で ALTER TABLESPACE による属性変更に使用。|
|disk_path|作成済みのディレクトリを指定。相対パスは $MACHBASE_HOME/dbs が基準。例：disk1 は $MACHBASE_HOME/dbs/disk1。|
|parallel_io|並列 I/O 要求数。既定値 3、最小 1、最大 128。|


## `DROP` TABLESPACE {#drop-tablespace}

**drop_tablespace_stmt:**

![drop_tablespace_stmt](/images/sql/ddl/drop_tablespace_stmt.png)

```sql
drop_table_stmt ::= 'DROP TABLESPACE' tablespace_name
```

指定したテーブルスペースを削除します。オブジェクトが残っている場合は失敗します。

```sql
-- 例
DROP TABLESPACE TablespaceName;
```


## `CREATE` INDEX {#create-index}

**create_index_stmt:**

![create_index_stmt](/images/sql/ddl/create_index_stmt.png)

**index_type:**

![index_type](/images/sql/ddl/index_type.png)

**table_space:**

![table_space](/images/sql/ddl/table_space.png)

**index_property_list:**

![index_property_list](/images/sql/ddl/index_property_list.png)

```sql
create_index_stmt ::= 'CREATE' 'INDEX' index_name 'ON' table_name '(' column_name ')' index_type? table_space? index_property_list?
index_type ::= 'INDEX_TYPE' ( 'LSM' | 'KEYWORD' | 'BITMAP' | 'REDBLACK' )
table_space ::= 'TABLESPACE' table_space_name
index_property_list ::= ( 'MAX_LEVEL' | 'PAGE_SIZE' | 'BITMAP_ENCODE' | 'PART_VALUE_COUNT' ) '=' value
```

### インデックスの種類 {#index-type}

作成する種類を指定します。キーワードインデックス以外で省略すると、テーブル型に応じた既定の種類を使用します。

| テーブル型 | 既定のインデックス |
|--|--|
|Volatile|REDBLACK|
|Lookup|REDBLACK|
|Log|LSM|

### KEYWORD インデックス {#keyword-index}

Log の VARCHAR または TEXT の単一列にだけ作成できます。

### LSM インデックス {#lsm-index}

LSM（Log-Structured Merge）は、大量データの保存と検索に最適化したインデックスです。レベルごとのパーティションを管理し、下位をマージして上位へ移します。マージ済みの下位パーティションは削除します。

バックグラウンドスレッドがマージを行います。複数のパーティションを 1 つにまとめることで、次の利点があります。

1. 重複するキーを 1 度だけ保存し、ディスク領域を節約。

2. ファイルの開閉と、アクセスするインデックスページ数を削減。

### LSM のプロパティ {#lsm-index-property}

| 項目 | 説明 |
|--|--|
|MAX_LEVEL<br>（既定値 3、最小 0、最大 3）|最大レベル。1 パーティションは 2 億レコード以下。各レベルは前のレベルの 10 倍。例：PART_VALUE_COUNT=100,000 なら、Level 0=100,000、1=1,000,000、2=10,000,000、3=100,000,000。最終レベルが 2 億を超えると作成失敗。|
|PAGE_SIZE<br>（既定値 512 * 1024、最小 32 * 1024、最大 1 * 1024 * 1024）|キーとビットマップを保存するページのサイズ。既定値は 512K。|
|BITMAP_ENCODE<br>（既定値 EQUAL、選択肢 RANGE）|EQUAL はキーと同値のビットマップ、RANGE は範囲用のビットマップを作成。等価条件には EQUAL、範囲条件には RANGE を推奨。RANGE の作成コストはやや高い。|

### BITMAP インデックス {#bitmap-index}

分析用で、Log テーブルだけに作成できます。VARCHAR、TEXT、`BINARY` 以外の単一列に作成できます。

### RED-BLACK インデックス {#red-black-index}

リアルタイム検索用のメモリインデックスです。Volatile/Lookup の任意の単一列に作成できます。

### インデックスプロパティ {#index-property}

LSM には次のプロパティを指定できます。

##### PART_VALUE_COUNT {#part_value_count}
インデックスの 1 パーティションに保存する行数です。

```sql
-- 例
-- c1 にインデックスを適用
CREATE INDEX index1 on table1 ( c1 );
-- LSM を明示的に適用
CREATE INDEX index_lsm on table1 ( c1 ) INDEX_TYPE LSM;
-- VARCHAR の var_column に KEYWORD を作成。page_size は 100000
CREATE INDEX index2 on table1 (var_column) INDEX_TYPE KEYWORD PAGE_SIZE=100000;
```

##### `JSON` パスインデックス {#json-path-indexes}

`JSON` メンバーのインデックスには、従来の矢印演算子と `JSON` ドット省略記法の両方を使用できます。

```sql
CREATE TAG TABLE tag_log (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON
);

-- JSON のドット省略記法
CREATE INDEX tag_log_sensor_idx ON tag_log (value.sensor.name);

-- 従来の JSONPath 矢印構文
CREATE INDEX tag_log_metric_idx ON tag_log (value->'$.metric');

-- 配列添字と二重引用符のキー
CREATE INDEX tag_log_item_idx ON tag_log (value.items[0]."product-id");
```

引用符付きの列名やキーワードの列名でも、従来の矢印構文を使用できます。

```sql
CREATE TAG TABLE tag_log_q (
    name    VARCHAR(40) PRIMARY KEY,
    time    DATETIME BASETIME,
    "value" JSON
);

CREATE INDEX tag_log_q_idx ON tag_log_q ("value"->'$.sensor.name');

CREATE TAG TABLE tag_log_kw (
    name   VARCHAR(40) PRIMARY KEY,
    time   DATETIME BASETIME,
    "LEFT" JSON
);

CREATE INDEX tag_log_kw_idx ON tag_log_kw (left->'$.sensor.name');
```

文字列比較はパスインデックスを利用できます。数値や真偽値の比較は、文字列順と数値順が異なるため、インデックス範囲条件には使用しません。

TAG メタデータのパスインデックスは、[メタデータ](../../table-types/tag-tables/tag-metadata)と[インデックス](../../table-types/tag-tables/tag-indexes)を参照してください。

## `DROP` INDEX {#drop-index}

**drop_index_stmt:**

![drop_index_stmt](/images/sql/ddl/drop_index_stmt.png)

```sql
drop_index_stmt ::= 'DROP INDEX' index_name
```

指定したインデックスを削除します。他のセッションがテーブルを検索中ならエラーになります。

```sql
-- 例
DROP INDEX IndexName;
```

## ALTER TABLE {#alter-table}

指定テーブルのスキーマを変更します。

- 多くの操作は Log テーブルだけに対応
- RENAME COLUMN は Log と Tag の両方に対応

### ALTER TABLE SET {#alter-table-set}

テーブルのプロパティを変更する構文です。現在、動的に変更できるプロパティはありません。

### ALTER TABLE ADD COLUMN {#alter-table-add-column}

**alter_table_add_stmt:**

![alter_table_add_stmt](/images/sql/ddl/alter_table_add_stmt.png)

```sql
alter_table_add_stmt ::= 'ALTER TABLE' table_name 'ADD COLUMN' '(' column_name column_type ( 'DEFAULT' value )? ')'
```

列を動的に追加します。名前と型を指定し、DEFAULT で既定値を設定できます。

```sql
-- 例 1
alter table atest2 add column (id4 float);
 
-- 例 2
alter table atest2 add column (id6 double  default 5);
alter table atest2 add column (id7 ipv4  default '192.168.0.1');
alter table atest2 add column (id8 varchar(4) default 'hello');
```

### ALTER TABLE `DROP` COLUMN {#alter-table-drop-column}

**alter_table_drop_stmt:**

![alter_table_drop_stmt](/images/sql/ddl/alter_table_drop_stmt.png)

```sql
alter_table_drop_stmt ::= 'ALTER TABLE' table_name 'DROP COLUMN' '(' column_name ')'
```

列を動的に削除します。

```
-- 例
alter table atest2 drop column (id4);
alter table atest2 drop column (id8);
```

### ALTER TABLE METADATA ADD COLUMN {#alter-table-metadata-add-column}

**alter_table_metadata_add_stmt:**

```sql
alter_table_metadata_add_stmt ::= 'ALTER TABLE' table_name 'METADATA ADD COLUMN' '(' column_name column_type ( 'DEFAULT' value )? ')'
```

TAG にメタデータ列を追加します。測定値ごとには変わらない、タグ固有の情報を保存します。

> **注意**：TAG テーブル専用です。

```sql
-- 例：TAG にメタデータ列を追加
ALTER TABLE altertbl METADATA ADD COLUMN (m1 DOUBLE);
ALTER TABLE altertbl METADATA ADD COLUMN (m2 VARCHAR(100));
ALTER TABLE altertbl METADATA ADD COLUMN (m3 INTEGER DEFAULT 0);
```

### ALTER TABLE METADATA `DROP` COLUMN {#alter-table-metadata-drop-column}

**alter_table_metadata_drop_stmt:**

```sql
alter_table_metadata_drop_stmt ::= 'ALTER TABLE' table_name 'METADATA DROP COLUMN' '(' column_name ')'
```

TAG のメタデータ列を削除します。

> **注意**：TAG テーブル専用です。

```sql
-- 例：TAG のメタデータ列を削除
ALTER TABLE altertbl METADATA DROP COLUMN (m1);
ALTER TABLE altertbl METADATA DROP COLUMN (m2);
```

### ALTER TABLE RENAME COLUMN {#alter-table-rename-column}

**alter_table_column_rename_stmt:**

![alter_table_column_rename_stmt](/images/sql/ddl/alter_table_column_rename_stmt.png)

```sql
alter_table_column_rename_stmt ::= 'ALTER TABLE' table_name 'RENAME COLUMN' old_column_name 'TO' new_column_name
```

列名を変更します。Log と Tag に対応します。

```sql
-- Log の例
alter table atest2 rename column id7 to id7_rename;

-- Tag の例
alter table tag rename column v0001 to vmax;
```

> **注意**：Tag では追加値列、`PRIMARY KEY`、BASETIME、METADATA の列名も変更できます。ただし、ROLLUP がある場合は制限されることがあります。

> **注意**：Tag の列名変更は Machbase 8.0.50 以降で対応します。

### ALTER TABLE MODIFY COLUMN {#alter-table-modify-column}

**alter_table_modify_stmt:**

![alter_table_modify_stmt](/images/sql/ddl/alter_table_modify_stmt.png)

```sql
alter_table_modify_stmt ::= 'ALTER TABLE' table_name 'MODIFY COLUMN' ( '(' column_name 'VARCHAR' '(' new_size ')' ')' | column_name ( 'NOT'? 'NULL' | 'SET' 'MINMAX_CACHE_SIZE' '=' value ) )
```

列の属性を変更します。VARCHAR の長さ、他の型の MINMAX キャッシュ設定、NOT NULL 制約を変更できます。

**VARCHAR のサイズ**

VARCHAR の長さだけを変更します。既存データを保護するため、短縮はできず、拡張のみ可能です。

```sql
ALTER TABLE table_name MODIFY COLUMN (column_name VARCHAR(new_size));
```

```sql
-- 例：次のテーブルがある場合
-- create table atest5 (id integer, name varchar(5), id3 double, id4 float);
 
-- エラー：別の型へ変更できない
alter table atest5 modify column (id varchar(10));
 
-- エラー：VARCHAR の長さは短縮できない
alter table atest5 modify column (name varchar(3));
 
-- エラー：VARCHAR の最大サイズは 32767 を超えられない
alter table atest5 modify column (name varchar(32768));
 
-- 成功
alter table atest5 modify column (name varchar(128));
```

**MINMAX_CACHE_SIZE**

列の MINMAX_CACHE_SIZE を変更します。

```sql
ALTER TABLE table_name MODIFY COLUMN column_name SET MINMAX_CACHE_SIZE=value;
```

```sql
-- 例：次のテーブルがある場合
create table atest9 (id integer, name varchar(100));
 
-- エラー：VARCHAR には適用できない
alter table atest9 modify column name set minmax_cache_size=0;
[ERR-02139 : MINMAX CACHE is not allowed for VARCHAR column(NAME).]
 
-- 変更成功
alter table atest9 modify column id set minmax_cache_size=10240;
```

**NOT NULL**

NOT NULL を追加します。既存の NULL 値がある列では失敗します。
NULL を許可するには、次の MODIFY COLUMN NULL を使用します。

```sql
ALTER TABLE table_name MODIFY COLUMN column_name NOT NULL;
```

```sql
-- t1.c1 に NOT NULL を追加
alter table t1 modify column c1 not null;
```

**NULL**

NOT NULL を解除し、NULL の入力を許可します。LSM の Min-Max キャッシュによる性能改善は得られません。

```sql
ALTER TABLE table_name MODIFY COLUMN column_name NULL;
```

```sql
-- t1.c1 の NOT NULL を解除
alter table t1 modify column c1 null;
```


### ALTER TABLE RENAME TO {#alter-table-rename-to}

**alter_table_rename_stmt:**

![alter_table_rename_stmt](/images/sql/ddl/alter_table_rename_stmt.png)

```sql
alter_table_rename_stmt ::= 'ALTER TABLE' table_name 'RENAME TO' new_name
```

テーブル名を変更します。

メタテーブルは変更できず、新しい名前に $ は使用できません。変更できるのは Log テーブルだけです。

```sql
-- worker を employee に変更
ALTER TABLE worker RENAME TO employee;
```

### ALTER TABLE ADD RETENTION {#alter-table-add-retention}

**alter_table_add_retention_stmt:**

```sql
alter_table_add_retention_stmt ::=  'ALTER TABLE' table_name 'ADD RETENTION' policy_name
```

![alter_table_add_retention_stmt](/images/sql/ddl/alter_table_add_retention_stmt.png)

```sql
ALTER TABLE tag ADD RETENTION policy_1d_1h;
```


### ALTER TABLE `DROP` RETENTION {#alter-table-drop-retention}

**alter_table_drop_retention_stmt:**

```sql
alter_table_drop_retention_stmt ::=  'ALTER TABLE' table_name 'DROP RETENTION'
```

![alter_table_drop_retention_stmt](/images/sql/ddl/alter_table_drop_retention_stmt.png)

```sql
ALTER TABLE tag DROP RETENTION;
```


## ALTER TABLESPACE {#alter-tablespace}

指定したテーブルスペースの情報を変更します。

### ALTER TABLESPACE MODIFY DATADISK {#alter-tablespace-modify-datadisk}

テーブルスペースの DATADISK の属性を変更します。

**alter_tablespace_stmt:**

![alter_tablespace_stmt](/images/sql/ddl/alter_tablespace_stmt.png)

```sql
alter_tablespace_stmt ::= 'ALTER TABLESPACE' table_name 'MODIFY DATADISK' disk_name 'SET' 'PARALLEL_IO' '=' value
```

```sql
-- 例
ALTER TABLESPACE tbs1 MODIFY DATADISK disk1 SET PARALLEL_IO = 10;
```

## TRUNCATE TABLE {#truncate-table}

**truncate_table_stmt:**

![truncate_table_stmt](/images/sql/ddl/truncate_table_stmt.png)

```sql
truncate_table_stmt ::= 'TRUNCATE TABLE' table_name
```

```sql
-- ctest の全データを削除
Mach> truncate table ctest;
Truncated successfully.
```

全データを削除します。他のセッションが検索中の場合はエラーになります。



## `CREATE` ROLLUP {#create-rollup}

**create_rollup_stmt:**

![create_rollup_stmt](/images/sql/ddl/create_rollup_stmt.png)

```sql
create_rollup_stmt ::= 'CREATE ROLLUP' rollup_name 'ON' src_table_name '('src_table_column')' 'INTERVAL' number ('SEC' | 'MIN' | 'HOUR')
```

```sql
-- Tag の value 列を対象とするロールアップを作成
Mach> CREATE ROLLUP _rollup_tag_value_sec ON tag(value) INTERVAL 1 SEC;
Executed successfully
```

`JSON` メンバーを集計対象にする場合、従来の矢印構文とドット省略記法を使用できます。

```sql
CREATE TAG TABLE tag_json (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON
);

-- JSON のドット省略記法
CREATE ROLLUP tag_json_metric_ru
ON tag_json (value.metric)
INTERVAL 1 SEC;

-- 従来の JSONPath 矢印構文
CREATE ROLLUP tag_json_metric_arrow_ru
ON tag_json (value->'$.metric')
INTERVAL 1 SEC;

-- 配列添字と二重引用符のキー
CREATE ROLLUP tag_json_item_ru
ON tag_json (value.items[0]."metric-id")
INTERVAL 1 SEC;
```

引用名やキーワードの列名にも、従来の矢印構文を使用できます。

```sql
CREATE TAG TABLE tag_json_q (
    name    VARCHAR(40) PRIMARY KEY,
    time    DATETIME BASETIME,
    "value" JSON
);

CREATE ROLLUP tag_json_q_ru
ON tag_json_q ("value"->'$.metric')
INTERVAL 1 SEC;

CREATE TAG TABLE tag_json_kw (
    name   VARCHAR(40) PRIMARY KEY,
    time   DATETIME BASETIME,
    "LEFT" JSON
);

CREATE ROLLUP tag_json_kw_ru
ON tag_json_kw (left->'$.metric')
INTERVAL 1 SEC;
```

> 元データの修正後に再集計する場合は、[ロールアップの再構築](../../table-types/tag-tables/rollup-rebuild/)を参照してください。

```sql
create_conditional_rollup_stmt ::= 'CREATE ROLLUP' rollup_name
                                   ( 'ON' src_table_name '('src_table_column')'
                                   | 'FROM' src_rollup_table_name )
                                   'INTERVAL' number ('SEC' | 'MIN' | 'HOUR')
                                   'WHERE' predicate
```

```sql
-- 条件付き：value2=0 の行だけを集計
Mach> CREATE ROLLUP _rollup_tag_value_min_ok
      ON tag(value)
      INTERVAL 1 MIN
      WHERE value2 = 0;
Executed successfully
```

```sql
create_custom_rollup_stmt ::= 'CREATE ROLLUP' rollup_name
                              'INTO' '(' dest_table_name ')'
                              'AS' '(' select_stmt ')'
                              'INTERVAL' number ('SEC' | 'MIN' | 'HOUR')
                              [ 'WAKEUP INTERVAL' number ('SEC' | 'MIN' | 'HOUR') ]
```

```sql
-- ユーザー定義集計を TAG に保存するカスタムロールアップ
Mach> CREATE ROLLUP rollup_stock_1m
      INTO (stock_rollup_1m)
      AS (
        SELECT code,
               DATE_TRUNC('minute', time) AS time,
               SUM(price)                 AS sum_price,
               COUNT(*)                   AS cnt
          FROM stock_tick
         GROUP BY code, time
      )
      INTERVAL 1 MIN;
Executed successfully
```

注意事項
- 条件付き `WHERE` は `ON/FROM` 形式のロールアップに使用します。
- カスタムロールアップでは、`SELECT` 内の `WHERE` だけを使用します。
- 外側の `INTERVAL ... WHERE ...` はカスタムでは未サポートです。
- 詳細は[カスタムロールアップ](../../table-types/tag-tables/rollup-custom/)を参照してください。


## `DROP` ROLLUP {#drop-rollup}

**drop_rollup_stmt:**

![drop_rollup_stmt](/images/sql/ddl/drop_rollup_stmt.png)

```sql
drop_rollup_stmt ::= 'DROP ROLLUP' rollup_name
```

```
-- ロールアップを削除
Mach> DROP ROLLUP _rollup_tag_value_sec;
Executed successfully
```

## ALTER ROLLUP {#alter-rollup}

ワーカーと起動間隔を制御します。

```sql
alter_rollup_start_stop_stmt ::= 'ALTER ROLLUP' rollup_name ( 'START' | 'STOP' )
alter_rollup_force_stmt      ::= 'ALTER ROLLUP' rollup_name 'FORCE'
alter_rollup_wakeup_stmt     ::= 'ALTER ROLLUP' rollup_name 'WAKEUP'
alter_rollup_wakeup_int_stmt ::= 'ALTER ROLLUP' rollup_name 'SET WAKEUP INTERVAL' number ( 'SEC' | 'MIN' | 'HOUR' )
```

例
```sql
-- ワーカーを開始、停止
ALTER ROLLUP _rollup_tag_value_sec START;
ALTER ROLLUP _rollup_tag_value_sec STOP;

-- 直ちに起動通知（待機しない）
ALTER ROLLUP _rollup_tag_value_sec WAKEUP;

-- 直ちに実行し、完了を待つ
ALTER ROLLUP _rollup_tag_value_sec FORCE;

-- 起動間隔を短縮（集計間隔を割り切る必要あり）
ALTER ROLLUP _rollup_tag_value_sec SET WAKEUP INTERVAL 1 SEC;
```

規則
- 起動間隔は 0 より大きく、集計間隔以下で、集計間隔を割り切れる必要があります。満たさない場合はエラーになります。
- `WAKEUP` はスレッドへ通知して直ちに戻ります。追いつくまで待つ場合は `FORCE` を使用します。

## `CREATE` RETENTION {#create-retention}

**create_retention_stmt:**

![create_retention_stmt](/images/sql/ddl/create_retention_stmt.png)

```sql
create_retention_stmt ::= 'CREATE RETENTION' policy_name 'DURATION' duration ( 'MONTH' | 'DAY' ) 'INTERVAL' interval ( 'DAY' | 'HOUR' )
```

```sql
Mach> CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;
Executed successfully
```

## `DROP` RETENTION {#drop-retention}

**drop_retention_stmt:**

![drop_retention_stmt](/images/sql/ddl/drop_retention_stmt.png)

```sql
drop_retention_stmt ::= 'DROP RETENTION' policy_name
```

```sql
Mach> DROP RETENTION policy_1d_1h;
Executed successfully
```
