---
type: docs
title: 'DDL'
weight: 110
toc: true
---

DDL（Data Definition Language）は、テーブル、インデックス、ビュー、ROLLUPなどのデータベースオブジェクトを作成・変更・削除する構文です。

> **権限**: 一般ユーザーがアクティブなデータベースでDDLを実行するには、`GRANT DDL ON DATABASE database_name TO user_name;`または`GRANT CREATE ON DATABASE database_name TO user_name;`が必要です。詳細は[GRANT/REVOKE](../user-auth-syntax/#grant-revoke)を参照してください。

## CREATE TABLE

```sql
create_table_stmt ::=
    'CREATE' table_type? 'TABLE' ['IF NOT EXISTS'] table_name
    '(' column_def ( ',' column_def )* ')'
    [ 'METADATA' '(' column_def ( ',' column_def )* ')' ]
    [ table_property_list ]
    [ 'TABLESPACE' tablespace_name ]
    [ 'WITH ROLLUP' rollup_interval_spec ]

table_type ::= 'LOG' | 'TAG' | 'VOLATILE' | 'LOOKUP' | 'TRANSACTION' | 'TXN'
-- table_typeを省略するとTRANSACTIONテーブルが作成されます。

column_def ::= column_name column_type
               [ 'PRIMARY KEY' ]
               [ 'NOT NULL' ]
               [ column_axis ]
               [ 'SUMMARIZED' ]
               [ 'DEFAULT' value ]
               [ 'PROPERTY' '(' column_property_list ')' ]

decimal_type ::= ( 'DECIMAL' | 'NUMERIC' | 'DEC' | 'FIXED' | 'NUMBER' )
                 [ '(' precision [ ',' scale ] ')' ]

array_type ::= ( 'SHORT' | 'INT16' | 'USHORT' | 'UINT16'
               | 'INTEGER' | 'INT' | 'INT32' | 'UINTEGER' | 'UINT32'
               | 'LONG' | 'INT64' | 'ULONG' | 'UINT64'
               | 'FLOAT' | 'DOUBLE' | decimal_type )
             '[' cardinality ']'

column_axis ::= 'BASETIME' | 'BASE TIME' | 'BASE DISTANCE' | 'BASEDISTANCE'

column_property_list ::=
    ( 'MINMAX_CACHE_SIZE' '=' number
    | 'PART_PAGE_COUNT'   '=' number
    | 'PAGE_VALUE_COUNT'  '=' number
    | 'MAX_CACHE_PART_COUNT' '=' number
    | 'SEQUENCE' '=' number )
    ( ',' column_property_list )*

table_property_list ::=
    ( 'TAG_PARTITION_COUNT'           '=' number
    | 'TAG_DATA_PART_SIZE'            '=' number
    | 'TAG_STAT_ENABLE'               '=' ( '0' | '1' )
    | 'TAG_DUPLICATE_CHECK_DURATION'  '=' number
    | 'VARCHAR_FIXED_LENGTH_MAX'      '=' number )
    ( ',' table_property_list )*
```

### テーブルタイプ

| キーワード | 説明 |
|--------|------|
| （なし） | **TRANSACTIONテーブル** - リレーショナルデータとトランザクションに対応 |
| `LOG` | **LOGテーブル** - 時系列ログデータ。追加（INSERT）中心で、一般的なUPDATEは不可 |
| `TAG` | **TAGテーブル** - タグ名・時刻・値の構造の時系列データ。BASETIME列が必須 |
| `LOOKUP` | **LOOKUPテーブル** - メモリ常駐。PRIMARY KEYが必須。DML全体に対応 |
| `VOLATILE` | **VOLATILEテーブル** - メモリ常駐。サーバー再起動時にデータが消失。PRIMARY KEYは任意 |
| `TRANSACTION`, `TXN` | **TRANSACTIONテーブル** - 正式名と短縮形は同じテーブルを作成 |

タイプ指定のない`CREATE TABLE`、`CREATE TRANSACTION TABLE`、`CREATE TXN TABLE`は、すべてTRANSACTIONテーブルを作成します。
LOGテーブルの作成には`CREATE LOG TABLE`を使用します。
以前の公開名称`RDB`と`TRX`は、テーブルタイプの別名としてサポートしていません。
TRANSACTIONはStandard Edition専用のため、Cluster Editionでは3つの作成構文がすべて拒否されます。

`DECIMAL`はすべてのテーブルタイプで使用できます。精度は`1～65`、小数桁数は`0～30`で、小数桁数は精度を超えられません。
詳細は[DECIMALとNUMERIC固定小数点型](/dbms/reference/sql/types/decimal-numeric-fixed-point/)を参照してください。

Machbase DBMS 8.7.0の`ARRAY`は、数値要素型の後に`1..1024`範囲の要素数を指定します。
サポート型とテーブル別の制約は、[数値ARRAY型](/dbms/reference/sql/types/array/)を参照してください。

### 例

```sql
-- LOGテーブルの作成: LOGキーワードを明示します。
CREATE LOG TABLE sensor_log (
    id      INTEGER,
    name    VARCHAR(64),
    value   DOUBLE,
    status  VARCHAR(20)
);

-- TAGテーブルの作成（BASETIME必須。SUMMARIZEDはROLLUP対象列に指定）
CREATE TAG TABLE tag (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- TAGテーブル + メタデータ + プロパティ
CREATE TAG TABLE sensors (
    name     VARCHAR(40) PRIMARY KEY,
    time     DATETIME BASETIME,
    value    DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(100),
    unit     VARCHAR(20)
) TAG_PARTITION_COUNT = 4;

-- LOOKUPテーブル（PRIMARY KEY必須）
CREATE LOOKUP TABLE devices (
    device_id  VARCHAR(40) PRIMARY KEY,
    ip         IPV4,
    status     VARCHAR(20)
);

-- VOLATILEテーブル
CREATE VOLATILE TABLE cache_data (
    id    INTEGER PRIMARY KEY,
    value DOUBLE
);

-- TRANSACTIONテーブルの正確な固定小数点列
CREATE TRANSACTION TABLE invoice (
    id      LONG PRIMARY KEY,
    amount  DECIMAL(18,2),
    tax     NUMERIC(18,4)
);

-- IF NOT EXISTSの使用
CREATE TAG TABLE IF NOT EXISTS tag (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- NOT NULL制約
CREATE TABLE t1 (
    c1 INTEGER NOT NULL,
    c2 VARCHAR(200)
);
```

### 定義済みシステム列

次のシステム列が提供されます。

| 列 | 型 | 説明 |
|------|------|------|
| `_ARRIVAL_TIME` | DATETIME | LOGテーブルだけで提供。レコードの挿入時刻で、`DURATION`クエリの基準 |
| `_RID` | LONG | LOGテーブルとTAGテーブルの内部データテーブルで提供。レコードの一意識別子で、ユーザーによる直接指定は不可 |

---

## DROP TABLE

```sql
drop_table_stmt ::= 'DROP TABLE' table_name
```

指定テーブルと、そのすべてのデータ・インデックスを削除します。
他のセッションがそのテーブルを検索中の場合はエラーになります。

```sql
DROP TABLE sensor_log;
```

---

## ALTER TABLE

`ALTER TABLE`はテーブルのスキーマを変更します。使用可能なサブ構文はテーブルタイプによって異なります。
TRANSACTIONは`ADD COLUMN`、`DROP COLUMN`、`RENAME COLUMN`、`RENAME TO`に対応します。
TAGのメタデータ列には、`METADATA ADD COLUMN`と`METADATA DROP COLUMN`を使用します。

### ADD COLUMN

```sql
alter_table_add_stmt ::=
    'ALTER TABLE' table_name [ 'METADATA' ] 'ADD COLUMN'
    '(' column_name column_type [ 'DEFAULT' value ] ')'
```

```sql
-- 列の追加
ALTER TABLE sensor_log ADD COLUMN (quality FLOAT);

-- TRANSACTION列の追加
ALTER TABLE product_master ADD COLUMN (stock_qty INTEGER DEFAULT 0);

-- デフォルト値とともに追加
ALTER TABLE sensor_log ADD COLUMN (flag INTEGER DEFAULT 0);
ALTER TABLE sensor_log ADD COLUMN (tag_ip IPV4 DEFAULT '192.168.0.1');

-- ARRAY列とDEFAULTの追加
ALTER TABLE sensor_log
    ADD COLUMN (channels INT32[3] DEFAULT [1, NULL, 3]);

-- TAG METADATA ARRAY列の追加
ALTER TABLE sensor_tag METADATA
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);
```

`DECIMAL(p)[n]`のARRAYで小数桁数を省略すると、0として処理します。
ARRAY DEFAULTの要素数は、宣言した要素数と正確に一致する必要があります。
不正な要素型、要素数、精度、小数桁数、ネスト・多次元宣言、長さの異なるDEFAULTでは、列を部分的に作成せず文全体が失敗します。

#### ARRAY ADD COLUMNのサポート範囲

| Edition | テーブルまたは列領域 | 対応 | 既存行の明示的DEFAULT |
|---|---|:---:|---|
| Standard | LOG | O | 適用 |
| Standard | VOLATILE | O | 適用せず、列全体のNULLを保持 |
| Standard | LOOKUP | O | 適用 |
| Standard | TRANSACTION | O | 適用 |
| Standard | TAG METADATA | O | 適用 |
| Standard | TAG DATAの一般列 | X | - |
| Cluster | LOG | O | 適用 |
| Cluster | その他のテーブルまたはTAG METADATA | X | - |

DEFAULTがなければ、対応するすべてのテーブルで、ALTER前から存在する行の新しいARRAY列は列全体がNULLになります。
TAG DATAの一般ARRAY列は`CREATE TABLE`で宣言できますが、ALTERで追加できません。
型とNULLの仕様は、[数値ARRAY型](/dbms/reference/sql/types/array/)を参照してください。

### DROP COLUMN

```sql
alter_table_drop_stmt ::=
    'ALTER TABLE' table_name [ 'METADATA' ]
    'DROP COLUMN' '(' column_name ')'
```

```sql
ALTER TABLE sensor_log DROP COLUMN (quality);
ALTER TABLE product_master DROP COLUMN (stock_qty);
ALTER TABLE sensor_log DROP COLUMN (channels);
ALTER TABLE sensor_tag METADATA DROP COLUMN (limits);
```

### RENAME COLUMN

```sql
alter_table_column_rename_stmt ::=
    'ALTER TABLE' table_name 'RENAME COLUMN' old_column_name 'TO' new_column_name
```

```sql
ALTER TABLE sensor_log RENAME COLUMN status TO device_status;
ALTER TABLE product_master RENAME COLUMN name TO product_name;
```

### MODIFY COLUMN

```sql
alter_table_modify_stmt ::=
    'ALTER TABLE' table_name 'MODIFY COLUMN'
    ( '(' column_name 'VARCHAR' '(' new_size ')' ')'
    | column_name ( 'NOT NULL' [ 'NOCHECK' ] | 'NULL'
                  | 'SET' 'MINMAX_CACHE_SIZE' '=' value ) )
```

次の長さ拡張とMINMAXの例は、LOGテーブルを対象にします。
既存VARCHARの長さは拡張できますが、縮小や他の型からVARCHARへの変換はできません。
LOGの新しい長さは最大32,767バイトです。
MINMAX_CACHE_SIZEは、LOGのサポートされる固定長列に適用し、VARCHAR・TEXTなどの可変長列には適用できません。

LOGでオプションなしのNOT NULLは既存行も検査します。
NOCHECKはその検査を省略するだけで、既存NULLを埋めるオプションではありません。
NULLはその制約を解除します。
TAGにはこの範囲を一括で適用せず、[TAG列の変更](/dbms/tag-table-usage/create-alter-drop/)の別の制約を確認してください。
TRANSACTIONテーブルは`MODIFY COLUMN`をサポートしていません。

```sql
-- VARCHARの長さ拡張（縮小は不可）
ALTER TABLE sensor_log MODIFY COLUMN (name VARCHAR(128));

-- NOT NULLの追加
ALTER TABLE sensor_log MODIFY COLUMN id NOT NULL;

-- NOT NULLの解除
ALTER TABLE sensor_log MODIFY COLUMN id NULL;

-- MINMAX_CACHE_SIZEの変更
ALTER TABLE sensor_log MODIFY COLUMN id SET MINMAX_CACHE_SIZE = 10240;
```

### RENAME TO

```sql
alter_table_rename_stmt ::=
    'ALTER TABLE' table_name 'RENAME TO' new_name
```

```sql
-- TRANSACTIONテーブルでサポート
ALTER TABLE product_master RENAME TO product_catalog;
```

### ADD / DROP RETENTION

Retentionの適用・解除構文は、[RETENTION構文](../retention-syntax/)を参照してください。

---

## TRUNCATE TABLE

```sql
truncate_table_stmt ::= 'TRUNCATE TABLE' table_name
```

テーブルの全データを削除します。他のセッションがそのテーブルを検索中の場合はエラーになります。

```sql
TRUNCATE TABLE sensor_log;
```

---

## CREATE INDEX

インデックスタイプ、テーブル別のサポート範囲、JSONパス、属性は、[INDEX構文](../index-syntax/)を参照してください。

---

## DROP INDEX

削除構文と制約は、[INDEX構文](../index-syntax/#drop-index)を参照してください。

---

## CREATE TABLESPACE

```sql
create_tablespace_stmt ::=
    'CREATE TABLESPACE' tablespace_name 'DATADISK' datadisk_list

datadisk_list ::= data_disk ( ',' data_disk )*

data_disk ::= disk_name
    '(' 'DISK_PATH' '=' '"' path '"'
        [ ',' 'PARALLEL_IO' '=' number ]
    ')'
```

```sql
-- 単一ディスクのテーブルスペース
CREATE TABLESPACE tbs1 DATADISK disk1 (DISK_PATH="tbs1_disk1");

-- 並列I/O設定
CREATE TABLESPACE tbs2 DATADISK disk1 (DISK_PATH="tbs2_disk1", PARALLEL_IO = 5);

-- 複数ディスク
CREATE TABLESPACE tbs3
  DATADISK disk1 (DISK_PATH="tbs3_d1", PARALLEL_IO = 10),
           disk2 (DISK_PATH="tbs3_d2"),
           disk3 (DISK_PATH="tbs3_d3");
```

---

## DROP TABLESPACE

```sql
drop_tablespace_stmt ::= 'DROP TABLESPACE' tablespace_name
```

```sql
DROP TABLESPACE tbs1;
```

テーブルスペースに作成されたオブジェクトがある場合は、削除できません。

---

## CREATE ROLLUP

基本・条件付き・Custom ROLLUPの構文は、[ROLLUP構文](../rollup-syntax/)を参照してください。

---

## DROP ROLLUP

削除構文は、[ROLLUP構文](../rollup-syntax/#drop-rollup)を参照してください。

---

## ALTER ROLLUP

開始・停止・強制実行・周期変更は、[ROLLUP構文](../rollup-syntax/#alter-rollup)を参照してください。

---

## CREATE RETENTION

作成構文とテーブルへの適用は、[RETENTION構文](../retention-syntax/)を参照してください。

---

## DROP RETENTION

削除構文と解除順序は、[RETENTION構文](../retention-syntax/#drop-retention)を参照してください。

---

## DDLの同時実行性とロック {#ddl-concurrency}

Machbase 8.7.0 Standard Editionは、独立したオブジェクトのDDLをオブジェクト単位で調整します。
したがって、同じデータベースで異なる名前のLOG、TAG、VOLATILE、LOOKUP、TRANSACTIONテーブルを作成・変更するDDLは、同時に進行できます。

| Edition | 独立オブジェクトのDDL | 競合範囲 | 競合時の待機設定 |
|---------|-----------------|-----------|-------------------|
| Standard | 同時に進行可能 | 同じオブジェクトと直接関連するオブジェクト | `DDL_LOCK_TIMEOUT` |
| Cluster | 既存ポリシーに従って直列化 | カタログ範囲 | `DDL_LOCK_TIMEOUT`は提供しない |

独立したオブジェクトのDDLが同時に開始しても、メタデータ処理やストレージI/Oなどの共通処理を共有する場合があります。
そのため、クライアント数に比例したスループット向上や、すべてのDDLの同時完了は保証しません。

### 競合するオブジェクト

| 同時実行の状況 | 動作 |
|----------------|------|
| 名前が異なる独立テーブル | テーブルタイプに関係なく同時に進行可能 |
| 同じオブジェクト、または同名オブジェクト | 1つのDDLだけが進み、他は待機またはエラー |
| テーブルの変更・削除DDLと、そのテーブルのインデックスDDL | 関連するオブジェクトとして処理 |
| ビューDDLと、ビューが参照するテーブルの変更・削除DDL | 関連するオブジェクトとして処理 |
| TAGテーブルの変更・削除DDLと、そのROLLUPまたはRetentionのDDL | 関連するオブジェクトとして処理 |
| `DROP VIEW`、`CREATE OR REPLACE VIEW`、システム範囲のDDL | より広い範囲で直列化される場合がある |

テーブルタイプが異なっても、同じテーブル名は1つの名前空間を使用します。
例えば、同名のLOGとTAGテーブルを同時に作成すると、どちらか1つだけが作成されます。

### DDLロックの待機時間

Standard Editionでは、`DDL_LOCK_TIMEOUT`で競合するDDLロックの待機時間を秒単位で設定します。

| 値 | 動作 |
|---:|------|
| `0` | 待機せず直ちに`ERR-02031: Resource busy (<object>)`を返す |
| 正数 | 指定時間まで待機し、ロックを取得できなければ`ERR-02031`を返す |

エラーメッセージの括弧内には、代表的な競合オブジェクトが表示されます。
広い範囲で競合したDDLは、オブジェクト名の代わりに`DDL`と表示される場合があります。

デフォルトは`0`、設定範囲は`0`～`1000000`です。
現在のセッションの値を変更するには、次の文を実行します。

```sql
ALTER SESSION SET DDL_LOCK_TIMEOUT = 10;
```

1つのDDLが複数のロック段階を経ても、待機時間は段階ごとに再開始されません。
ロック取得後にオブジェクトと依存関係を再確認するため、先行DDLの結果に応じて、
`already exists`、`table not found`などの一般的なSQLエラーが返される場合があります。

`DDL_LOCK_TIMEOUT`はDDLロックの待機時間だけを制限し、SQL全体の実行時間は制限しません。
実行中のDDLは開始時点の値を継続して使用し、`ALTER SESSION`で変更した値は次のDDLから適用されます。
DDLのコミットと復旧動作は以前のバージョンと同じで、新たな暗黙的コミットは行いません。

| 設定 | 単位 | 制限対象 |
|------|------|-----------|
| `DDL_LOCK_TIMEOUT` | 秒 | Standard EditionのDDLロック待機 |
| `SESSION_QUERY_TIMEOUT_SEC` / `QUERY_TIMEOUT` | 秒 | クエリ実行と応答待機 |
| `TRANSACTION_BUSY_TIMEOUT_MS` | ミリ秒 | TRANSACTIONテーブルの同時書き込み競合待機 |

---

## 関連文書

- [テーブルタイプ](/dbms/data-modeling-table-design/) - LOG、TAG、LOOKUP、VOLATILE、TRANSACTIONの特性と使用ガイド
- [TAGテーブルのROLLUP](/dbms/tag-table-usage/create-alter-drop/#original-85-creating-tag-tables) - ROLLUPの作成と運用ガイド
- [GRANT/REVOKE](../user-auth-syntax/#grant-revoke) - DDL実行に必要な権限の付与
- [ALTER SESSION](../system-session-alter-syntax/#alter-session) - 現在のセッションのDDLロック待機時間の設定
- [スキーマ変更チェックリスト](/dbms/operations-configuration-recovery/checklist-schema-alter/) - 運用中のDDL実行と競合対応
