---
title : 'SELECT 힌트'
type: docs
weight: 50
---

# Index

* [소개](#introduction)
* [PARALLEL](#parallel)
* [NOPARALLEL](#noparallel)
* [FULL](#full)
* [NO_INDEX](#no_index)
* [RID_RANGE](#rid_range)
* [SCAN_FORWARD, SCAN_BACKWARD](#scan_forward-scan_backward)


## 소개

SELECT 문에서 활용 가능한 힌트들을 정리했습니다.

##  PARALLEL

병렬 쿼리 실행 시 사용할 병렬 처리 계수를 지정합니다.

```sql
SELECT /*+ PARALLEL(table_name, parallel_factor) */ ...
```

```sql
Mach> CREATE TABLE log_parallel_test (sensor VARCHAR(32), frequency DOUBLE, value DOUBLE, ts DATETIME);
Mach> CREATE INDEX idx_ts ON log_parallel_test (ts);
 
Mach> EXPLAIN SELECT /*+ PARALLEL(log_parallel_test, 8) */ sensor, frequency, avg(value)
      FROM log_parallel_test
      WHERE ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD') and ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')
      GROUP BY sensor, frequency;
 
PLAN                                                                             
------------------------------------------------------------------------------------
 PROJECT                                                                         
  GROUP AGGREGATE                                                                
   PARALLEL INDEX SCAN                                                           
    *BITMAP RANGE (table id:3, column id:4, index id:4)                          
    [KEY RANGE]                                                                 
     * ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD')                                
     * ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')                                
[7] row(s) selected.
```


##  NOPARALLEL

병렬 처리를 사용하지 않도록 강제합니다.

```sql
SELECT /*+ NOPARALLEL(table_name) */ ...
```

```sql
Mach> CREATE TABLE log_parallel_test (sensor VARCHAR(32), frequency DOUBLE, value DOUBLE, ts DATETIME);
Mach> CREATE INDEX idx_ts ON log_parallel_test (ts);
 
Mach> EXPLAIN SELECT /*+ NOPARALLEL(log_parallel_test) */ sensor, frequency, avg(value)
      FROM log_parallel_test
      WHERE ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD') and ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')
      GROUP BY sensor, frequency;
  
PLAN                                                                             
------------------------------------------------------------------------------------
 PROJECT                                                                         
  GROUP AGGREGATE                                                                
   INDEX SCAN                                                                    
    *BITMAP RANGE (table id:5, column id:4, index id:6)                          
    [KEY RANGE]                                                                  
     * ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD')                                 
     * ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')                                 
[7] row(s) selected.
```


##  FULL

INDEX SCAN을 사용하지 않도록 지정합니다.

```sql
SELECT /*+ FULL(table_name) */ ...
```

```sql
Mach> CREATE TABLE log_full_test (sensor VARCHAR(32), I1 INTEGER);
Mach> CREATE INDEX idx_I1 ON log_full_test (I1);
 
Mach> EXPLAIN SELECT * FROM log_full_test WHERE I1 = 1;
PLAN                                                                             
------------------------------------------------------------------------------------
 PROJECT                                                                         
  INDEX SCAN                                                                     
   *BITMAP RANGE (table id:14, column id:2, index id:15)                         
   [KEY RANGE]                                                                   
    * I1 = 1                                                                     
[5] row(s) selected.
 
Mach> EXPLAIN SELECT /*+ FULL(log_full_test) */ * FROM log_full_test WHERE I1 = 1;
PLAN                                                                             
------------------------------------------------------------------------------------
 PROJECT                                                                         
  FULL SCAN                                                                      
[2] row(s) selected.
```


##  NO_INDEX

지정한 인덱스를 사용하지 않도록 합니다.

```sql
SELECT /*+ NO_INDEX(table_name,index_name) */ ...
```

```sql
Mach> CREATE TABLE log_no_index_test (sensor VARCHAR(32), I1 INTEGER, I2 INTEGER);
Mach> CREATE INDEX idx_I1 ON log_no_index_test (I1);
Mach> CREATE INDEX idx_I2 ON log_no_index_test (I2);
 
Mach> EXPLAIN SELECT * FROM TEST WHERE I1 = 1;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (t:7, c:1, i:8) with BLOOMFILTER
   [KEY RANGE]                                                                  
    * I1 = 1                                                                    
[5] row(s) selected.
 
Mach> EXPLAIN SELECT /*+ NO_INDEX(TEST,TEST_IDX) */ * FROM TEST WHERE I1 = 1;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  FULL SCAN
[2] row(s) selected.
 
Mach> EXPLAIN SELECT * FROM log_no_index_test WHERE I1 = 1 or I2 = 2;
PLAN                                                                             
------------------------------------------------------------------------------------
 PROJECT                                                                         
  INDEX SCAN                                                                     
   INDEX (OR)                                                                    
    *BITMAP RANGE (table id:21, column id:2, index id:22)                        
    *BITMAP RANGE (table id:21, column id:3, index id:23)                        
   [KEY RANGE]                                                                   
    * I1 = 1 or I2 = 2                                                           
[7] row(s) selected.
 
Mach> EXPLAIN SELECT /*+ NO_INDEX(log_no_index_test, idx_I1) */ * FROM log_no_index_test WHERE I1 = 1 or I2 = 2;
PLAN                                                                             
------------------------------------------------------------------------------------
 PROJECT                                                                         
  FULL SCAN                                                                      
[2] row(s) selected.
 
Mach> EXPLAIN SELECT * FROM log_no_index_test WHERE I1 = 1 and I2 = 2;
PLAN                                                                             
------------------------------------------------------------------------------------
 PROJECT                                                                         
  INDEX SCAN                                                                     
   *BITMAP RANGE (table id:21, column id:2, index id:22)                         
   *BITMAP RANGE (table id:21, column id:3, index id:23)                         
   [KEY RANGE]                                                                   
    * I1 = 1                                                                     
    * I2 = 2                                                                     
[7] row(s) selected.
 
Mach> EXPLAIN SELECT /*+ NO_INDEX(log_no_index_test, idx_I1) */ * FROM log_no_index_test WHERE I1 = 1 and I2 = 2;
 
PLAN                                                                             
------------------------------------------------------------------------------------
 PROJECT                                                                         
  INDEX SCAN                                                                     
   *BITMAP RANGE (table id:21, column id:3, index id:23)                         
   [KEY RANGE]                                                                   
    * I2 = 2                                                                     
   [FILTER]                                                                      
    * I1 = 1                                                                     
[7] row(s) selected.
Elapsed time: 0.001
Mach>
Mach>
Mach> EXPLAIN SELECT /*+ NO_INDEX(log_no_index_test, idx_I2) */ * FROM log_no_index_test WHERE I1 = 1 and I2 = 2;
 
PLAN                                                                             
------------------------------------------------------------------------------------
 PROJECT                                                                         
  INDEX SCAN                                                                     
   *BITMAP RANGE (table id:21, column id:2, index id:22)                         
   [KEY RANGE]                                                                   
    * I1 = 1                                                                     
   [FILTER]                                                                      
    * I2 = 2                                                                     
[7] row(s) selected.
```


##  RID_RANGE

RID 범위를 지정하여 해당 범위 내에서만 연산하도록 합니다.

```sql
SELECT /*+ RID_RANGE(table_name,number,number) */ ...
```

```sql
Mach> SELECT /*+ RID_RANGE(TEST,45,50) */ _RID, * FROM TEST;
_RID                 I1
------------------------------------
49                   1
48                   1
47                   1
46                   1
45                   1
[5] row(s) selected.
```


##  SCAN_FORWARD, SCAN_BACKWARD

LOG 테이블의 스캔 방향을 지정합니다. `SCAN_FORWARD`는 가장 오래된 입력 레코드부터, `SCAN_BACKWARD`는 가장 최근 입력 레코드부터 조회합니다.

표준 에디션의 LOG 테이블에만 적용됩니다.

```sql
SELECT /*+ SCAN_FORWARD(table_name) */ ...
SELECT /*+ SCAN_BACKWARD(table_name) */ ...
```

```sql
Mach> SELECT /*+ SCAN_FORWARD(mytbl) */  _ARRIVAL_TIME, VALUE FROM mytbl LIMIT 10;
_ARRIVAL_TIME                   VALUE                   
----------------------------------------------------------------
2017-01-01 00:00:49 500:000:000 0                         
2017-01-01 00:01:39 500:000:000 1                         
2017-01-01 00:02:29 500:000:000 2                         
2017-01-01 00:03:19 500:000:000 3                         
2017-01-01 00:04:09 500:000:000 4                         
2017-01-01 00:04:59 500:000:000 5                         
2017-01-01 00:05:49 500:000:000 6                         
2017-01-01 00:06:39 500:000:000 7                         
2017-01-01 00:07:29 500:000:000 8                         
2017-01-01 00:08:19 500:000:000 9                         
[10] row(s) selected.
 
Mach> SELECT /*+ SCAN_BACKWARD(mytbl) */ _ARRIVAL_TIME, VALUE FROM mytbl LIMIT 10;
_ARRIVAL_TIME                   VALUE                   
----------------------------------------------------------------
2017-02-27 20:53:19 500:000:000 9                         
2017-02-27 20:52:29 500:000:000 8                         
2017-02-27 20:51:39 500:000:000 7                         
2017-02-27 20:50:49 500:000:000 6                         
2017-02-27 20:49:59 500:000:000 5                         
2017-02-27 20:49:09 500:000:000 4                         
2017-02-27 20:48:19 500:000:000 3                         
2017-02-27 20:47:29 500:000:000 2                         
2017-02-27 20:46:39 500:000:000 1                         
2017-02-27 20:45:49 500:000:000 0                         
[10] row(s) selected.
```
