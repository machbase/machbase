---
type: docs
title : Creating and Managing Log Table
weight: 10
---

The log table can be simply generated as follows. Let's create a table called sensor_data and delete it.

Data types compatible with Machbase can be found in the SQL Reference Types.


## Creating Log Table

Create a log table with the 'CREATE TABLE' syntax.

```sql
Mach> CREATE TABLE sensor_data
      (
          id VARCHAR(32),
          val DOUBLE
       );
Created successfully.
 
Mach> DROP TABLE sensor_data;
Dropped successfully.
```


## Deleting Log Table

Delete log table with 'DROP TABLE' statement.

```sql
Mach> DROP TABLE sensor_data;
Dropped successfully.
 
-- TRUNCATE deletes only data and keeps table.
Mach> TRUNCATE TABLE sensor_data;
Truncated successfully.
```