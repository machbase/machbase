---
layout : post
title : '시스템/세션 관리'
type: docs
weight: 80
---

# 목차

* [ALTER SYSTEM](#alter-system)
  * [KILL SESSION](#kill-session)
  * [CANCEL SESSION](#cancel-session)
  * [CHECK DISK_USAGE](#check-disk_usage)
  * [INSTALL LICENSE](#install-license)
  * [INSTALL LICENSE (PATH)](#install-license-path)
  * [SET](#set)
* [ALTER SESSION](#alter-session)
  * [SET SQL_LOGGING](#set-sql_logging)
  * [SET DEFAULT_DATE_FORMAT](#set-default_date_format)
  * [SET SHOW_HIDDEN_COLS](#set-show_hidden_cols)
  * [SET FEEDBACK_APPEND_ERROR](#set-feedback_append_error)
  * [SET MAX_QPX_MEM](#set-max_qpx_mem)
  * [SET SESSION_IDLE_TIMEOUT_SEC](#set-session_idle_timeout_sec)
  * [SET QUERY_TIMEOUT](#set-query_timeout)


## ALTER SYSTEM

시스템 단위의 자원을 관리하거나 설정을 변경하는 구문이다.

### KILL SESSION

**alter_system_kill_session_stmt:**

![alter_system_kill_session_stmt](../sys_image/alter_system_kill_session_stmt.png)

```sql
alter_system_kill_session_stmt: 'ALTER SYSTEM KILL SESSION' number
```

SessionID를 가진 특정 세션을 종료시킨다.

단, SYS 유저만이 구문을 수행할 수 있으며 자기 자신의 세션에 대해서는 KILL할 수 없다.

### CANCEL SESSION

**alter_system_cancel_session_stmt:**

![alter_system_cancel_session_stmt](../sys_image/alter_system_cancel_session_stmt.png)

```sql
alter_system_cancel_session_stmt ::= 'ALTER SYSTEM CANCEL SESSION' number
```

SessionID를 가진 특정 세션을 취소시킨다.

접속이 끊어지는 대신 수행중인 동작을 취소하고, 사용자에게 해당 수행이 취소되었다는 에러 코드를 되돌린다. 단, KILL과 마찬가지로 자기 자신이 연결된 세션에 대해서는 취소를 할 수 없다.

### CHECK DISK_USAGE

**alter_system_check_disk_stmt:**

![alter_system_check_disk_stmt](../sys_image/alter_system_check_disk_stmt.png)

```sql
alter_system_check_disk_stmt ::= 'ALTER SYSTEM CHECK DISK_USAGE'
```

V$STORAGE에서 Log Table의 디스크 사용량을 나타내는 __DC_TABLE_FILE_SIZE__ 의 값을 보정한다.

Process Failure나 Power Failure 발생시 디스크 사용량이 부정확할 수 있다. 이 명령어를 통해서 파일 시스템으로부터 정확한 값을 읽어온다. 하지만 파일 시스템에 상당한 부하를 줄 수 있기 때문에 지양해야 한다.

### INSTALL LICENSE

**alter_system_install_license_stmt:**

![alter_system_install_license_stmt](../sys_image/alter_system_install_license_stmt.png)

```sql
alter_system_install_license_stmt ::= 'ALTER SYSTEM INSTALL LICENSE'
```

라이선스 파일의 기본위치($MACHBASE_HOME/conf/license.dat)에 라이선스 파일을 설치한다.

해당 라이선스가 설치에 적합한지 판별 후 설치된다.

### INSTALL LICENSE (PATH)

**alter_system_install_license_path_stmt:**

![alter_system_install_license_path_stmt](../sys_image/alter_system_install_license_path_stmt.png)

```sql
alter_system_install_license_path_stmt: ::= 'ALTER SYSTEM INSTALL LICENSE' '=' "'" path "'"
```

특정 위치에 있는 라이선스 파일을 설치한다.

해당 위치에 존재하지 않거나 올바르지 않은 라이선스 파일을 입력했을 시에는 에러가 발생한다. 경로는 반드시 절대경로로 입력해야 한다. 해당 라이선스가 설치에 적합한지 판별 후 설치된다.

## SET

* 5.6 이후 버전 부터 지원되는 기능입니다.

**alter_system_set_stmt:**

![alter_system_set_stmt](../sys_image/alter_system_set_stmt.png)

```sql
alter_system_set_stmt ::= 'ALTER SYSTEM SET' prop_name '=' value
```

System 의 Property 를 수정할 수 있다. 수정 가능한 Property 는 다음과 같다.
* QUERY_PARALLEL_FACTOR
* DEFAULT_DATE_FORMAT
* TRACE_LOG_LEVEL
* DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE
* MAX_SESSION_COUNT
* SESSION_IDLE_TIMEOUT_SEC
* PROCESS_MAX_SIZE
* TAG_CACHE_MAX_MEMORY_SIZE


## ALTER SESSION

세션 단위의 자원을 관리하거나 설정을 변경하는 구문이다.

### SET SQL_LOGGING

**alter_session_sql_logging_stmt:**

![alter_session_sql_logging_stmt](../sys_image/alter_session_sql_logging_stmt.png)

```sql
alter_session_sql_logging_stmt ::= 'ALTER SESSION SET SQL_LOGGING' '=' flag
```

해당 세션의 Trace Log에 메시지를 남길지 여부를 결정한다.

이 메시지를 Bit Flag 로서 다음의 값을 사용하면 된다.

* 0x1 : Parsing, Validation, Optimization 단계에서 발생하는 에러를 남긴다.
* 0x2 : DDL을 수행한 결과를 남긴다.

즉, 해당 플래그의 값이 2일 경우에는 DDL만 로깅하고, 3일 경우에는 에러 및 DDL을 함께 로깅하는 것이다.

아래는 해당 세션의 로깅 플래그를 변경하고, 에러 로깅을 남기는 예제이다.

```sql
Mach> alter session set SQL_LOGGING=1;
Altered successfully.
Mach> exit
```

### SET DEFAULT_DATE_FORMAT

**alter_session_set_defalut_dateformat_stmt:**

![alter_session_set_defalut_dateformat_stmt](../sys_image/alter_session_set_defalut_dateformat_stmt.png)

```sql
alter_session_set_defalut_dateformat_stmt ::= 'ALTER SESSION SET DEFAULT_DATE_FORMAT' '=' date_format
```

해당 세션의 Datetime 자료형의 기본 포맷을 설정한다.

서버가 구동되면, Property 인 __DEFAULT_DATE_FORMAT__ 의 값이 세션 속성으로 설정이 된다.
Property 의 속성이 바뀌지 않았다면, 세션의 값 또한 "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"이 될 것이다.
시스템과 무관하게, 특정 사용자에 한해 Datetime 자료형의 기본 포맷을 수정할 경우에 이 명령어를 사용한다.

v$session 에 해당 세션마다 설정된 Default Date Format 이 있고 확인도 할 수 있다. 아래는 해당 세션의 값을 확인 및 변경하는 예제이다.

```sql
Mach> CREATE TABLE time_table (time datetime);
Created successfully.
 
Mach> SELECT DEFAULT_DATE_FORMAT from v$session;
default_date_format                                                              
-----------------------------------------------
YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                
[1] row(s) selected.
 
Mach> INSERT INTO time_table VALUES(TO_DATE('2016/11/12'));
[ERR-00300: Invalid date value.(2016/11/12)]
 
Mach> ALTER SESSION SET DEFAULT_DATE_FORMAT='YYYY/MM/DD';
Altered successfully.
 
Mach> SELECT DEFAULT_DATE_FORMAT from v$session;
 
default_date_format                                                              
----------------------------------------------
YYYY/MM/DD                                                                       
[1] row(s) selected.
 
Mach> INSERT INTO time_table VALUES(TO_DATE('2016/11/12'));
1 row(s) inserted.
 
Mach> SELECT * FROM time_table;
 
TIME                              
----------------------------------
2016/11/12
 
[1] row(s) selected.
```

### SET SHOW_HIDDEN_COLS

**alter_session_set_hidden_column_stmt:**

![alter_session_set_hidden_column_stmt](../sys_image/alter_session_set_hidden_column_stmt.png)

```sql
alter_session_set_hidden_column_stmt ::= 'ALTER SESSION SET SHOW_HIDDEN_COLS' '=' ( '0' | '1' )
```

해당 세션의 select 수행시 *로 표현된 컬럼에서 숨은 컬럼 (_arrival_time)을 출력할 것인지를 결정한다.

서버가 구동되면, 전역 프로퍼티인 SHOW_HIDDEN_COLS의 값이 세션 속성으로 0이 설정된다.
만일 사용자가 자기 세션의 기본 동작을 변경하고자 할 경우에는 이 값을 1로 설정하면 된다.

v$session에 해당 세션마다 설정된 SHOW_HIDDEN_COLS 값이 있으며, 확인할 수 있다.

```sql
Mach> SELECT * FROM  v$session;
ID                   CLOSED      USER_ID     LOGIN_TIME                      SQL_LOGGING SHOW_HIDDEN_COLS
-----------------------------------------------------------------------------------------------------------------
DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE
------------------------------------------------------------------------------------------------------
1                    0           1           2015-04-29 17:23:56 248:263:000 3           0
YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011
[1] row(s) selected.                            
Mach> ALTER SESSION SET SHOW_HIDDEN_COLS=1;
Altered successfully.
Mach> SELECT * FROM v$session;
_ARRIVAL_TIME                   ID                   CLOSED      USER_ID     LOGIN_TIME                      SQL_LOGGING
--------------------------------------------------------------------------------------------------------------------------------
SHOW_HIDDEN_COLS DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE
------------------------------------------------------------------------------------------------------------------------
1970-01-01 09:00:00 000:000:000 1                    0           1           2015-04-29 17:23:56 248:263:000 3
1           YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011
[1] row(s) selected.
```

### SET FEEDBACK_APPEND_ERROR

**alter_session_set_feedback_append_err_stmt:**

![alter_session_set_feedback_append_err_stmt](../sys_image/alter_session_set_feedback_append_err_stmt.png)

```sql
alter_session_set_feedback_append_err_stmt ::= 'ALTER SESSION SET FEEDBACK_APPEND_ERROR' '=' ( '0' | '1' )
```

해당 세션의 Append 에러 메시지를 Client program으로 보낼 것인지를 설정한다.

에러 메시지는 다음의 값을 사용하면 된다.

* 0 = 에러 메시지를 보내지 않는다.
* 1 = 에러 메시지를 보낸다.

아래는 사용 예제이다.

```sql
mach> ALTER SESSION SET FEEDBACK_APPEND_ERROR=0;
Altered successfully.
```

### SET MAX_QPX_MEM

**alter_session_set_max_qpx_mem_stmt:**

![alter_session_set_max_qpx_mem_stmt](../sys_image/alter_session_set_max_qpx_mem_stmt.png)

```sql
alter_session_set_max_qpx_mem_stmt ::= 'ALTER SESSION SET MAX_QPX_MEM' '=' value
```

해당 세션의 하나의 SQL Statement가 GROUP BY, DISTINCT, ORDER BY 연산을 수행할때 사용하는 최대 메모리의 크기를 지정한다.

만약 최대 메모리 이상의 메모리 할당을 시도하면, 시스템은 그 SQL문의 수행을 취소하고 오류로 처리한다.
오류 발생 시 machbase.trc에 해당 질의문을 포함한 에러 코드 및 에러 메시지를 기록한다.

```sql
Mach> ALTER SESSION SET MAX_QPX_MEM=1073741824;
Altered successfully.
 
Mach> SELECT * FROM v$session;
ID                   CLOSED      USER_ID     LOGIN_TIME                      CLIENT_TYPE                                                                      
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
USER_NAME                                                                         USER_IP                                                                           SQL_LOGGING SHOW_HIDDEN_COLS
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FEEDBACK_APPEND_ERROR DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE MAX_QPX_MEM          RS_CACHE_ENABLE      RS_CACHE_TIME_BOUND_MSEC
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
RS_CACHE_MAX_MEMORY_PER_QUERY RS_CACHE_MAX_RECORD_PER_QUERY RS_CACHE_APPROXIMATE_RESULT_ENABLE IDLE_TIMEOUT         QUERY_TIMEOUT       
-----------------------------------------------------------------------------------------------------------------------------------------------
14                   0           1           2021-03-08 16:33:01 503:181:809 CLI                                                                              
NULL                                                                              192.168.0.194                                                                     11          0               
1                     YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011            1073741824           1                    1000                    
16777216                      50000                         0                                  0                    0                   
[1] row(s) selected.
Elapsed time: 0.001
```

- 최대 메모리 크기 이상을 SQL문에서 사용했을 때, trc 에러

```sql
[2021-03-08 16:36:32 P-69000 T-140515328653056][INFO] DML FAILURE (2E10000084:Memory allocation error (alloc'd: 1048595, max: 1048576).)
```

- 최대 메모리 크기 이상을 SQL문에서 사용했을 때, machsql 에러 메세지

```sql
Mach> select * from tag order by value DESC, time ASC;
NAME                  TIME                            VALUE                      
--------------------------------------------------------------------------------------
[ERR-00132: Memory allocation error (alloc'd: 1048595, max: 1048576).]
[0] row(s) selected.
Elapsed time: 0.447
```

### SET SESSION_IDLE_TIMEOUT_SEC

**alter_session_set_session_idle_timeout_sec_stmt:**

![alter_session_set_session_idle_timeout_sec_stmt](../sys_image/alter_session_set_session_idle_timeout_sec_stmt.png)

```sql
alter_session_set_session_idle_timeout_sec_stmt ::= 'ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC' '=' value
```

해당 세션이 유휴 상태일 때의 연결 유지 시간을 지정한다.

초단위로 지정하며 유휴 상태로 설정된 시간이 지나게 되면 세션이 종료된다.

v$session 에서 세션에 설정된 idle timeout 시간을 조회할 수 있다.


```sql
Mach> ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC=200;
Altered successfully.
 
 
Mach> SELECT IDLE_TIMEOUT FROM V$SESSION;
IDLE_TIMEOUT        
-----------------------
200                                     
[1] row(s) selected.
```

## SET QUERY_TIMEOUT

**alter_session_set_query_timeout_stmt:**

![alter_session_set_query_timeout_stmt](../sys_image/alter_session_set_query_timeout_stmt.png)

```sql
alter_session_set_query_timeout_stmt ::= 'ALTER SESSION SET QUERY_TIMEOUT' '=' value
```

세션에서 Query를 수행 시 서버의 응답을 대기하는 시간이다.

초단위로 지정하며 Query 수행 후 서버에서의 응답이 지정된 시간을 초과하면 Query가 종료된다.

v$session에서 세션에 설정된 Query timeout 시간을 조회할 수 있다.

```sql
Mach> ALTER SESSION SET QUERY_TIMEOUT=200;
Altered successfully.
 
Mach> SELECT QUERY_TIMEOUT FROM V$SESSION;
QUERY_TIMEOUT        
-----------------------
200                                     
[1] row(s) selected.
```
