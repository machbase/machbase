---
title : Data Retrieval
type: docs
weight: 10
---

You can retrieve data in ANSI standard SQL.

The following example shows a search without creating an index.

In other words, the last input data is outputed first.

For more information, see the [SELECT](/dbms/sql-ref/select) section of the SQL Reference.


## Basic access

```sql
SELECT * FROM table_name;
```

```sql
Index
Basic access
View Conditional Clause
Mach> SELECT * FROM mach_log;
DEVICE          TM                              TEMP       
----------------------------------------------------------------
MSG                                                                              
------------------------------------------------------------------------------------
192.168.0.1     NULL                            NULL       
NULL                                                                             
192.168.0.2     2014-06-15 19:50:03 484:382:010 82         
error code = 20, critical warning                                                
192.168.0.2     2014-06-15 19:50:03 484:382:008 57         
error code = 20                                                                  
192.168.0.1     2014-06-15 19:50:03 484:382:006 99         
error code = 10, critical bug                                                    
192.168.0.1     2014-06-15 19:50:03 484:382:004 55         
error code = 10                                                                  
192.168.0.2     2014-06-15 19:50:03 484:382:002 31       
normal state                                                                     
192.168.0.1     2014-06-15 19:50:03 484:382:000 32         
normal state                                                                     
[7] row(s) selected.
Mach>
```


## View Conditional Clause

```sql
SELECT column_name,column_name
FROM table_name
WHERE column_name operator value;
```

```sql
Mach> SELECT * FROM mach_log WHERE device = '192.168.0.1';
DEVICE          TM                              TEMP       
----------------------------------------------------------------
MSG                                                                              
------------------------------------------------------------------------------------
192.168.0.1     NULL                            NULL       
NULL                                                                             
192.168.0.1     2014-06-15 19:50:36 488:663:006 99         
error code = 10, critical bug                                                    
192.168.0.1     2014-06-15 19:50:36 488:663:004 55         
error code = 10                                                                  
192.168.0.1     2014-06-15 19:50:36 488:663:000 32         
normal state                                                                     
[4] row(s) selected.
 
Mach> SELECT * FROM mach_log WHERE device = '192.168.0.1' AND temp > 30 AND temp < 50;
DEVICE          TM                              TEMP       
----------------------------------------------------------------
MSG                                                                              
------------------------------------------------------------------------------------
192.168.0.1     2014-06-15 19:50:36 488:663:000 32         
normal state                                                                     
[1] row(s) selected.
 
Mach> SELECT * FROM mach_log where device > '192.168.0.1';
DEVICE          TM                              TEMP       
----------------------------------------------------------------
MSG                                                                              
------------------------------------------------------------------------------------
192.168.0.2     2014-06-15 19:50:36 488:663:010 82         
error code = 20, critical warning                                                
192.168.0.2     2014-06-15 19:50:36 488:663:008 57         
error code = 20                                                                  
192.168.0.2     2014-06-15 19:50:36 488:663:002 31         
normal state                                                                     
[3] row(s) selected.
 
Mach> SELECT * FROM mach_log WHERE msg LIKE '%error%';
DEVICE          TM                              TEMP       
----------------------------------------------------------------
MSG                                                                              
------------------------------------------------------------------------------------
192.168.0.2     2014-06-15 19:50:36 488:663:010 82         
error code = 20, critical warning                                                
192.168.0.2     2014-06-15 19:50:36 488:663:008 57         
error code = 20                                                                  
192.168.0.1     2014-06-15 19:50:36 488:663:006 99         
error code = 10, critical bug                                                    
192.168.0.1     2014-06-15 19:50:36 488:663:004 55         
error code = 10                                                                  
[4] row(s) selected.
```