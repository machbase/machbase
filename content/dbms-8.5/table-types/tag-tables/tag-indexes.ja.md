---
title: 'Tag テーブルのインデックス'
type: docs
weight: 70
toc: true
---

## 概要 {#overview}

Tag テーブルの追加列や JSON パスを検索する場合、インデックスで検索性能を改善できます。TAG インデックスの作成と管理を説明します。

## TAG インデックスとは {#what-are-tag-indexes}

Machbase の TAG テーブルには、TAG 型のインデックスを作成できます。

詳細は、SQL リファレンスの DDL を参照してください。

* TAG インデックス：TAG テーブルの追加列に作成できます。


## インデックスの作成 {#create-index}

CREATE INDEX 文で指定した列にインデックスを作成します。

```sql
CREATE INDEX index_name ON table_name (column_name) [index_type]
    index_type ::= INDEX_TYPE { TAG }
```

```bash
Mach> CREATE INDEX id_index ON tag (id) INDEX_TYPE TAG;
Created successfully.
```

バージョン 7.5 以降では、Tag テーブルの JSON 列に限り、JSON パスごとにインデックスを作成できます。

通常のインデックス作成構文の列に、演算子で JSON パスを連結します。

JSON 演算子の戻り値は VARCHAR なので、VARCHAR 同士の比較でのみインデックスが使用されます。

```bash
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, jval JSON);
Executed successfully.
  
Mach> CREATE INDEX idx_jval_value1 ON tag (jval->'$.value1');
Created successfully.
  
Mach> CREATE INDEX idx_jval_value2 ON tag (jval->'$.value2');
Created successfully.
  
Mach> EXPLAIN SELECT * FROM tag WHERE jval->'$.value1' = '10';
PLAN                                                                            
------------------------------------------------------------------------------------
 PROJECT                                                                        
  TAG READ (RAW)                                                                
   KEYVALUE INDEX SCAN (_TAG_DATA_0)                                            
    [KEY RANGE]                                                                 
     * jval->'$.value1' = '10'                                                  
   VOLATILE FULL SCAN (_TAG_META)                                               
[6] row(s) selected.
```

## TAG メタデータの JSON パスインデックス {#tag-metadata-json-path-indexes}

`TAG METADATA` の JSON 列にもパスインデックスを作成できます。

```sql
CREATE TAG TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON
);

CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');
```

テーブルの作成時に、よく使用するパスを宣言することもできます。

```sql
CREATE TAG TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    info JSON INDEX('name', 'ship.status')
);
```

注意事項：

- メタデータの JSON パスインデックスには `CREATE INDEX ... ON TAG METADATA (...)` を使用します。
- 作成時にパスを宣言する場合は、`INFO JSON INDEX(...)` を使用します。
- 現在の JSON パスインデックスは、主に文字列リテラルとの比較で機能します。
- 数値リテラルとの比較では、全表スキャンになる場合があります。

## インデックスの削除 {#delete-index}

DROP INDEX 文で指定したインデックスを削除します。他のセッションがテーブルを検索している場合は、エラーになります。

```sql
DROP INDEX index_name;
```

```bash
Mach> DROP INDEX id_index;
Dropped successfully.
```

メタデータの JSON パスインデックスも、インデックス名だけで削除できます。

```sql
DROP INDEX idx_ship_owner;
```
