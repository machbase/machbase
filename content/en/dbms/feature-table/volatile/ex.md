---
title : Volatile Table Utilization Example
type : docs
weight: 60
---

##  Save Sensor Data Current Value

The data of the volatile table exist only in the memory, and the update operation by the primary key is very fast. Using this feature, it creates a table that stores the current values ​​of the sensors that change very quickly. An example of a table creation script is shown below.

```sql
create volatile table sensor_current (sensor_id varchar(40) primary key, value double);
```


##  Input and Update Volatile Data

Since the table has been created, the current value of the sensor can be reflected through data input and update operations. The input sensor value is determined based on the primary key sensor_id column as to whether to perform input or update. Input or update can be performed with the following query.

```sql
insert into sensor_current values('SENSOR_001',100.0) on duplicate key update set value=100.0;
```

The data input in the above query statement updates the value column value of the record with the sensor_id value 'SENSOR_001', which is the column corresponding to the primary key, to 100.0. If there is no data, insert a new record according to the syntax of the insert statement.

##  Volatile Data Search

To find the current value of specific sensor data, search using the following query. You can perform searches using the same syntax as a regular SQL query.

```sql
SELECT value FROM sensor_current WHERE sensor_id = 'SENSOR_001'
```