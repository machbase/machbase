---
type: docs
title : 'Duplication removal'
weight: 70
---

## Configuration of duplication removal

When creating the TAG table, the duration for duplicate removal is passed as a table property. The maximum configurable duration for duplicate removal is 30 days.
  
```sql
-- If the newly inserted data duplicates existing data within a day from system time those data will be deleted.
  
CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_DUPLICATE_CHECK_DURATION=1;
```
  
The property of the duplication removal is shown in the table m$sys_table_property.
```sql
SELECT * FROM m$sys_table_property WHERE id={table_id} AND name = 'TAG_DUPLICATE_CHECK_DURATION';
```
  
Data insert/select example (duplication removal duration is one day)
```sql
-- Total inserted data are 6 and 4 of them are duplicates but 1 duplicated record was inserted one day before 
-- system time(1970-01-03 09:00:00 000:000:003). 
-- Newly inserted duplicated data within the configured duration (1 day) are not displayed.

INSERT INTO tag VALUES('tag1', '1970-01-01 09:00:00 000:000:001', 0);
INSERT INTO tag VALUES('tag1', '1970-01-02 09:00:00 000:000:001', 0);    
INSERT INTO tag VALUES('tag1', '1970-01-02 09:00:00 000:000:002', 0);
INSERT INTO tag VALUES('tag1', '1970-01-02 09:00:00 000:000:002', 1);
INSERT INTO tag VALUES('tag1', '1970-01-03 09:00:00 000:000:003', 0);
INSERT INTO tag VALUES('tag1', '1970-01-01 09:00:00 000:000:001', 0);
    
SELECT * FROM tag WHERE name = 'tag1';
NAME                  TIME                            VALUE                       
--------------------------------------------------------------------------------------
tag1                  1970-01-01 09:00:00 000:000:001 0
tag1                  1970-01-02 09:00:00 000:000:001 0                           
tag1                  1970-01-02 09:00:00 000:000:002 0
tag1                  1970-01-03 09:00:00 000:000:003 0      
tag1                  1970-01-01 09:00:00 000:000:001 0
  
```
  
## Constraints of duplication removal

* Once the duplication removal policy is set during table creation, it cannot be modified thereafter.
* The duplication removal setting can be configured on a daily basis, with a maximum limit of 30 days.
* If the existing input data has already been deleted, any subsequent occurrence of the same data will not be considered as a duplicate for the purpose of duplication removal.
