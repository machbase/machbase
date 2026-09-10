---
type: docs
title: '10.3 作成、変更、削除'
weight: 30
toc: true
---

VOLATILEテーブルの作成・削除と、他のテーブルタイプとの永続性の違いを説明します。

<a id="original-85-creating-volatile-tables"></a>

## VOLATILEテーブルの作成と管理

VOLATILEテーブルの作成・削除方法は次のとおりです。

### 作成

```sql
create volatile table vtable (id1 integer, name varchar(20));
```

### 削除

```sql
drop table vtable;
```

<a id="differences-persistence-ddl"></a>

## 永続性の違いとDDL

VOLATILEテーブルは、他のテーブルタイプと異なりメモリにのみ存在します。

### 永続性の比較

| 項目 | VOLATILE | LOOKUP | TRANSACTION | TAG | LOG |
|------|----------|--------|-----|-----|-----|
| 保存場所 | メモリ | ディスク | ディスク | ディスク | ディスク |
| サーバー再起動後のデータ保持 | X | O | O | O | O |
| テーブル構造（DDL）の保持 | O | O | O | O | O |

### DDLの特性

VOLATILEで消失するのはデータであり、テーブル定義は他のテーブルタイプと同様に永続保存されます。
再起動後に必要なのは、再作成ではなく初期ロードです。

```sql
-- テーブル定義は一度だけ作成します。
CREATE VOLATILE TABLE ch10_ddl (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);
```

### 作成構文

基本構文は`CREATE VOLATILE TABLE テーブル名 (列定義, ...)`です。
キーによる更新や削除が必要な場合は、1つの列に`PRIMARY KEY`を指定します。

- `PRIMARY KEY`は任意です。
- PRIMARY KEY列は1つだけ指定します。

### AUTO_INCREMENT PRIMARY KEY

サーバーが数値のPRIMARY KEYを生成する場合は、単一の`LONG`または`INT64`列に`AUTO_INCREMENT`を指定します。

```sql
CREATE VOLATILE TABLE ch10_ddl_seq (
    request_id LONG PRIMARY KEY AUTO_INCREMENT,
    payload    VARCHAR(256)
);

INSERT INTO ch10_ddl_seq(payload) VALUES('refresh');
```

PK列を省略するかNULLを指定すると、サーバーが値を生成します。
単一の`INSERT ... VALUES`では、`0..INT64_MAX`範囲のPK値を直接指定することもできます。
指定値が現在の次の自動値以上なら、次の自動値は`指定値 + 1`に進みます。小さい値を指定しても戻りません。
AUTO_INCREMENTを使用するVOLATILEテーブルでは、`INSERT ... SELECT`と`ON DUPLICATE KEY UPDATE`は使用できません。

VOLATILEテーブルはサーバー再起動時にデータが消えるため、次の自動値も1から再開します。
テーブル定義は保持されるため、再作成は不要です。
SDKでINSERT結果のIDを取得する方法は、[ROWIDとINSERT結果ID](/dbms/reference/sql/rowid/)を参照してください。

### 列の追加と削除

Standard Editionでは、VOLATILEテーブルに固定長の数値ARRAY列を追加・削除できます。

```sql
ALTER TABLE ch10_ddl
    ADD COLUMN (thresholds DOUBLE[2] DEFAULT [10.0, 20.0]);

ALTER TABLE ch10_ddl
    DROP COLUMN (thresholds);
```

VOLATILEは既存のスカラー`ADD COLUMN`と同様に、ALTER前から存在する行をDEFAULTで書き直しません。
ARRAY DEFAULTを指定しても、既存行の新しい列は列全体がNULLになります。
この動作は、LOG、LOOKUP、TRANSACTION、TAG METADATAのバックフィル規則とは異なります。

ARRAYのサポート要素型、要素数、DEFAULT規則は、[数値ARRAY型](/dbms/reference/sql/types/array/)を参照してください。

### 削除

```sql
DROP TABLE ch10_ddl;
DROP TABLE ch10_ddl_seq;
```

### 注意事項

- VOLATILEテーブルのDDL（構造定義）はデータベースに保存され、サーバー再起動後も残ります。
- データは再起動後に自動復元されないため、初期ロードスクリプト（起動時のmachsql実行など）を構成する必要があります。
