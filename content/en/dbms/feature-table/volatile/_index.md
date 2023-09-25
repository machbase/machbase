---
title : Volatile Table
type : docs
weight: 30
---

##  Concept

The volatile table is a temporary table in which all the data resides in the temporary memory space and enriches the data through joining with the log table.

The volatile table is a supplementary information table that stores various information of a specific device or equipment represented by a simple symbol or a number in a log table. It can be input and updated at high speed, and is used in a case where the present state of the data (which does not match the time series data) needs to be maintained in real time.

The characteristics of this table are as follows


##  Preserving Schema
The structure (schema) information of the volatile table is maintained even if the Machbase server is shut down and then restarted. To drop the table, you need to explicitly execute the DROP table.


##  Data Volatility

The data in the volatile table disappears as soon as the server is shut down. Therefore, when the server is started, the contents of the volatile table must be INSERTed again.


##  Index Providing and Join Function

It provides a RED-BLACK index, which is a real-time optimized index for fast data access of volatile tables. Therefore, it can be efficiently used in Join and searching process with log tables.

* You can specify a primary key in the table column.
* When inserting data having a duplicate primary key value, it is possible to UPDATE the value of existing data.
* The condition clause ( WHERE clause) can be used to delete data that matches the primary key value condition.
* The _ARRIVAL_TIME column does not exist.


##  Primary Key

The primary key can be created to form a unique constraint on a table column value and to specify a key column to distinguish table data.

When inserting data into a volatile table with a primary key specified, the primary key column value of the insert data must be different from the other primary key column values ​​in the table. This constraint is called a unique constraint.

The creation constraints of the primary key are as follows.

Primary keys can only be created in volatile tables.

You can specify only one primary key column, and you can not specify more than one column as primary keys.


##  Update Function

Unlike other table types, volatile tables provide a limited update function.

If the primary key value of the data to be inserted overlaps with one of the primary key values of the other data, the mode is changed to the 'update' mode instead of 'insertion', and another column value of the existing data having the duplicated key value is inserted, it is changed to the column value of the data to be processed. The update function can be used only in the volatile table with the primary key specified. If the primary key value is not specified during the insertion, the update function can not be used.


##  Delete Function

Volatile tables provide the ability to delete specific data using primary key values.

If you add a condition clause (WHERE clause) in the DELETE clause to specify a primary key value, you can delete it only if there is data corresponding to that primary key value. The delete function can be used only on the volatile table with the primary key specified, and the condition (Primary Key Column) = (Value) that can be entered in the condition clause is limited.
