---
title : Lookup Table
type : docs
weight: 40
---

##  Concept

Like the volatile table, the lookup table resides in the memory, so that it can perform fast query processing.

In addition, data input and change are reflected on disk to ensure data permanence. Compared with the volatile table, the query processing performance is the same, but the data input and change performance is somewhat lower.

The characteristics of this table are as follows.


##  Low Input / Update Performance

Unlike volatile tables, the performance of input and update due to the maintenance of disk data images is low, making them unsuitable for tables for real-time data representation such as dashboards.


##  Schema Preservation

Again, unlike volatile tables, the structure (schema) information in the lookup table is retained even after the server is restarted. You must explicitly use DROP TABLE  to drop the table .


##  Data Preservation

Unlike the volatile table, the lookup table is restored to its original state when the server is restarted.Providing Index


##  Index

Like the volatile table, it provides a RED-BLACK index. Therefore, it can be efficiently used in the search process or the join process with the log table.
