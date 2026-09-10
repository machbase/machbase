---
title : Log テーブルのインデックス
type: docs
weight: 50
toc: true
---

Machbase の Log テーブルでは、3 種類のインデックスタイプキーワードを使用できます。

詳細は、SQL リファレンスの DDL ページにある CREATE INDEX を参照してください。

* `LSM` インデックス：範囲条件と等価条件に使用します。
* BITMAP インデックス：LOG テーブルの列に作成でき、`DESC` では `LSM` と表示されます。
* KEYWORD インデックス：文字列検索に使用します。Varchar 列と Text 列にのみ作成できます。


##  インデックスの作成 {#create-index}

CREATE INDEX 文で指定した列にインデックスを作成します。

```sql
CREATE INDEX index_name ON table_name (column_name) [index_type] [tablespace] [index_prop_list]
    index_type ::= INDEX_TYPE { LSM | BITMAP | KEYWORD }
    tablespace ::= TABLESPACE tablespace_name
    index_prop_list ::= value_pair, value_pair, ...
    value_pair ::= property_name = property_value
```

```sql
Mach> CREATE INDEX id_index ON log_data(id) INDEX_TYPE LSM MAX_LEVEL=3;
Created successfully.
```


##  インデックスのプロパティ {#index-properties}

インデックスの作成時にプロパティを指定します。

```sql
CREATE BITMAP INDEX value_bitmap_idx ON log_data(value) KEY_COMPRESS=1;
```

```sql
Mach> CREATE BITMAP INDEX value_bitmap_idx ON log_data(value) KEY_COMPRESS=1;
Created successfully.
```


##  インデックスの削除 {#delete-index}

DROP INDEX 文で指定したインデックスを削除します。ただし、他のセッションがそのテーブルを検索している場合はエラーになります。

```sql
DROP INDEX index_name;
```

```sql
Mach> DROP INDEX id_index;
Dropped successfully.
```
