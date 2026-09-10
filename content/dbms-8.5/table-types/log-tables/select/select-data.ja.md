---
title : データの取得
type: docs
weight: 10
toc: true
---

ANSI 標準 SQL でデータを検索できます。

次の例は、インデックスを作成せずに検索します。

最後に入力したデータから順に表示されます。

詳細は、SQL リファレンスの [SELECT](../../../../sql-reference/select/) を参照してください。


## 基本的な検索 {#basic-access}

```sql
SELECT * FROM table_name;
```

```sql
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


## 条件を指定した検索 {#view-conditional-clause}

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

## ヒントによる検索方向の指定 {#specifying-search-direction-using-hints}

### 逆方向 {#backward-direction}

既定の検索方向です。`/*+ SCAN_BACKWARD(table_name) */` ヒントでも指定できます。

```sql
Mach> SELECT * FROM LOG;
TIME    
----------------------------------
2021-01-04 00:00:00 000:000:000
2021-01-03 00:00:00 000:000:000
2021-01-02 00:00:00 000:000:000
2021-01-01 00:00:00 000:000:000
[4] row(s) selected.
Elapsed time: 0.001
 
Mach> SELECT /*+ SCAN_BACKWARD(LOG) */ * FROM LOG;
TIME    
----------------------------------
2021-01-04 00:00:00 000:000:000
2021-01-03 00:00:00 000:000:000
2021-01-02 00:00:00 000:000:000
2021-01-01 00:00:00 000:000:000
[4] row(s) selected.
Elapsed time: 0.001
```

### 順方向 {#forward-direction}

`/*+ SCAN_FORWARD(table_name) */` ヒントで順方向に検索します。

```sql
Mach> SELECT /*+ SCAN_FORWARD(LOG) */ * FROM LOG;
TIME
----------------------------------
2021-01-01 00:00:00 000:000:000
2021-01-02 00:00:00 000:000:000
2021-01-03 00:00:00 000:000:000
2021-01-04 00:00:00 000:000:000
[4] row(s) selected.
Elapsed time: 0.001
```

### 既定のスキャン方向を設定するプロパティ {#property-to-set-default-scan-direction}

[TABLE_SCAN_DIRECTION](../../../../configuration/property/#table_scan_direction) で、SELECT にヒントがない場合の Log テーブルのスキャン方向を指定できます。
