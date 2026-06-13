---
title : Index of Log Table
type: docs
weight: 50
---

Three index type keywords can be used in the Machbase log table.

For more information, refer to the DDL page CREATE INDEX section of the SQL Reference  .

* LSM Index: used for range and equality predicates.
* BITMAP Index: can be created on LOG table columns and is displayed as `LSM` by `DESC`.
* KEYWORD Index: used to search strings; it can be created only for Varchar and Text columns.


##  Create Index

Create an index on a specific column using the CREATE INDEX statement.

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


##  Index Properties

Index properties are specified when the index is created.

```sql
CREATE BITMAP INDEX value_bitmap_idx ON log_data(value) KEY_COMPRESS=1;
```

```sql
Mach> CREATE BITMAP INDEX value_bitmap_idx ON log_data(value) KEY_COMPRESS=1;
Created successfully.
```


##  Delete Index

Delete the specified index using the DROP INDEX statement. However, if there is another session in which the table is being searched, it will fail with an error.

```sql
DROP INDEX index_name;
```

```sql
Mach> DROP INDEX id_index;
Dropped successfully.
```
