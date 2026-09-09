---
type: docs
title: '8.3 Create, Alter, and Drop'
weight: 30
toc: true
---

Schema changes require checking existing data and ingestion programs as well as command success. Old
SQL after a rename or dropping an indexed column before its index can cause errors. This section
checks before/after behavior with sample data present.

<a id="create-rdb-table"></a>

<a id="테이블을-만들고-한-행을-준비합니다"></a>

## Creating a Table

```sql
CREATE TRANSACTION TABLE ch8_ddl (
    id   LONG,
    code VARCHAR(32),
    qty  INTEGER
);
INSERT INTO ch8_ddl VALUES (1, 'P-01', 10);
```

<a id="create-rdb-primary-key-index"></a>

<a id="기존-데이터에-키와-인덱스를-추가합니다"></a>

## Creating Keys and Indexes

```sql
CREATE PRIMARY KEY INDEX ch8_ddl_pk ON ch8_ddl(id);
CREATE UNIQUE INDEX ch8_ddl_code ON ch8_ddl(code);
CREATE INDEX ch8_ddl_qty ON ch8_ddl(qty);
SHOW INDEX ch8_ddl_code;
```

id is the single PRIMARY KEY; code is a separate business key. Creation can fail if existing data
contains duplicates or NULL in the primary key column. Define composite uniqueness with CREATE
UNIQUE INDEX. UNIQUE constraint syntax inside CREATE TABLE is unsupported.

<a id="create-rdb-auto-increment"></a>

For automatic numbering, specify `LONG PRIMARY KEY AUTO_INCREMENT` at creation. This section's id
values are explicit, not automatic. Do not apply both creation patterns to the same object. See the
separate [AUTO_INCREMENT](/dbms/reference/sql/syntax/auto-increment-syntax/) exercise.

<a id="alter-rdb-table"></a>

<a id="새-컬럼이-기존-행에-어떻게-보이는지-확인합니다"></a>

## Adding Columns and Defaults

```sql
ALTER TABLE ch8_ddl ADD COLUMN (label VARCHAR(64));
ALTER TABLE ch8_ddl ADD COLUMN (status VARCHAR(16) DEFAULT 'NEW');
ALTER TABLE ch8_ddl ADD COLUMN (limits DECIMAL(12)[2] DEFAULT [10, 20]);

SELECT id, label, status, limits FROM ch8_ddl ORDER BY id;
```

In row 1, label is NULL, status is NEW, and limits is [10, 20]. Adding an ARRAY column without
DEFAULT gives existing rows a whole-array NULL.

DEFAULT support differs between ADD COLUMN and CREATE TABLE. ADD COLUMN accepts a value compatible
with the type, as above. In CREATE TABLE column definitions, only `DEFAULT SYSDATE` on DATETIME is
supported. Other types and values are rejected with `ERR-02346` and `ERR-02347`, respectively. If an
initial default is needed, first create the table and add the column with ADD COLUMN, or specify the
value in INSERT. Distinguish a whole-array NULL from NULL in individual array elements.

Enclose column definitions in parentheses; this syntax differs from other DBMS ALTER TABLE forms.
TRANSACTION does not support changing length or type with MODIFY COLUMN. Prepare a separate
migration to a new schema when needed.

<a id="인덱스와-의존-객체를-먼저-정리합니다"></a>

## Column Changes and Dependent Objects

```sql
DROP INDEX ch8_ddl_qty;
ALTER TABLE ch8_ddl DROP COLUMN (qty);
ALTER TABLE ch8_ddl DROP COLUMN (label);
ALTER TABLE ch8_ddl DROP COLUMN (limits);
ALTER TABLE ch8_ddl RENAME COLUMN code TO product_code;

SELECT id, product_code, status FROM ch8_ddl;
SHOW INDEX ch8_ddl_code;
```

Existing row 1 retains P-01 and NEW, and the business-key index remains. Check PRIMARY KEY, UNIQUE,
ordinary, and JSON path indexes before changing referenced columns. The last user column cannot be
dropped.

Renaming or dropping a table/column can be rejected if a VIEW references it. Application SQL and
prepared statements are also affected. After DDL, check whether existing prepared statements must be
prepared again rather than blindly reusing them.

```sql
ALTER TABLE ch8_ddl RENAME TO ch8_product;
SELECT id, product_code, status FROM ch8_product;
```

After renaming the table, query ch8_product.

<a id="drop-rdb-table"></a>

<a id="전체-삭제와-정의-삭제를-구분합니다"></a>

## Deleting All Rows and Dropping Tables

```sql
BEGIN;
TRUNCATE TABLE ch8_product;
SELECT COUNT(*) AS during_delete FROM ch8_product;
ROLLBACK;
SELECT COUNT(*) AS after_rollback FROM ch8_product;
DROP TABLE ch8_product;
```

The counts are 0 and 1, respectively. Current TRANSACTION TRUNCATE is implemented as deletion of all
rows and can be rolled back inside an explicit transaction. Do not generalize this to LOG/TAG
TRUNCATE. The final DROP removes data, definition, and related indexes.

<a id="rdb-ddl-operation-notes"></a>

<a id="ddl은-업무-트랜잭션-밖에서-수행하세요"></a>

## Operational DDL Considerations

Distinguish this TRUNCATE behavior from schema operations such as CREATE, ALTER, and DROP. Do not
assume schema changes inside BEGIN can later be rolled back. Active transactions or open cursors on
the same table can block DDL; close result sets and finish business transactions first.

ADD/DROP COLUMN modify both the catalog and separate storage files. If the server stops during the
operation, do not repeat the DDL before restart recovery finishes. After recovery, check DESC,
representative SELECT/INSERT operations, indexes, views, and server logs. Do not recover by moving,
editing, or deleting internal storage files directly.

If the schema differs from expectations, review the original DDL, execution sequence, and first
error together. This is more useful than examining only the last error.
