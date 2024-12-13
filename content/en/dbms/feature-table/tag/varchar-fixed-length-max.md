---
type: docs
title : 'Tag table VARCHAR storage option'
weight: 80
---

## VARCHAR storage option
An option to store VARCHAR in a fixed area if its size is less than or equal to the configured value.
The configuration value is passed as a table property and can be set between a minimum of 15 and a maximum of 127 bytes, with a default value of 15.

```sql
-- If the size of the input VARCHAR data is 15 or less, it is stored in the fixed data file instead of the extended file.
  
CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED, strval VARCHAR(100)) VARCHAR_FIXED_LENGTH_MAX = 15;
```
  
The property of the VARCHAR storage option value is shown in the table m$sys_table_property.
```sql
SELECT * FROM m$sys_table_property WHERE id={table_id} AND name = 'VARCHAR_FIXED_LENGTH_MAX';
```
