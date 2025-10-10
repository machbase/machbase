---
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

시스템 전역 자원을 관리하거나 설정을 변경할 때 사용하는 구문입니다.

### KILL SESSION

**alter_system_kill_session_stmt:**

![alter_system_kill_session_stmt](/images/sql/sys/alter_system_kill_session_stmt.png)

```sql
alter_system_kill_session_stmt: 'ALTER SYSTEM KILL SESSION' number
```

세션 ID를 지정해 해당 세션을 강제로 종료합니다.

SYS 사용자만 실행할 수 있으며, 자신의 세션은 종료할 수 없습니다.

### CANCEL SESSION

**alter_system_cancel_session_stmt:**

![alter_system_cancel_session_stmt](/images/sql/sys/alter_system_cancel_session_stmt.png)

```sql
alter_system_cancel_session_stmt ::= 'ALTER SYSTEM CANCEL SESSION' number
```

세션 ID를 지정해 해당 세션에서 수행 중인 작업을 취소합니다.

연결을 끊는 대신, 현재 수행 중인 작업을 중단하고 작업이 취소되었다는 오류 코드를 사용자에게 반환합니다. 마찬가지로 자신의 세션은 취소할 수 없습니다.

### CHECK DISK_USAGE

**alter_system_check_disk_stmt:**

![alter_system_check_disk_stmt](/images/sql/sys/alter_system_check_disk_stmt.png)

```sql
alter_system_check_disk_stmt ::= 'ALTER SYSTEM CHECK DISK_USAGE'
```

V$STORAGE에서 로그 테이블의 디스크 사용량을 나타내는 `DC_TABLE_FILE_SIZE` 값을 재계산합니다.

프로세스 장애나 정전이 발생하면 디스크 사용량이 부정확해질 수 있습니다. 이 명령은 파일 시스템에서 값을 다시 읽어 정확한 사용량을 반영하지만, 파일 시스템에 부담을 줄 수 있으므로 필요할 때만 사용해야 합니다.

### INSTALL LICENSE

**alter_system_install_license_stmt:**

![alter_system_install_license_stmt](/images/sql/sys/alter_system_install_license_stmt.png)

```sql
alter_system_install_license_stmt ::= 'ALTER SYSTEM INSTALL LICENSE'
```

라이선스 파일을 기본 경로(`$MACHBASE_HOME/conf/license.dat`)에 설치합니다.

설치 전 라이선스 적합성을 검증하며, 검증에 성공하면 설치가 완료됩니다.

### INSTALL LICENSE (PATH)

**alter_system_install_license_path_stmt:**

![alter_system_install_license_path_stmt](/images/sql/sys/alter_system_install_license_path_stmt.png)

```sql
alter_system_install_license_path_stmt: ::= 'ALTER SYSTEM INSTALL LICENSE' '=' "'" path "'"
```

지정한 경로에 라이선스 파일을 설치합니다.

경로에 파일이 없거나 손상된 라이선스 파일을 지정하면 오류가 발생합니다. 경로는 절대 경로여야 하며, 설치 전 라이선스 적합성을 검증합니다.

### SET

**alter_system_set_stmt:**

![alter_system_set_stmt](/images/sql/sys/alter_system_set_stmt.png)

```sql
alter_system_set_stmt ::= 'ALTER SYSTEM SET' prop_name '=' value
```

변경 가능한 속성 목록은 다음과 같습니다.
* QUERY_PARALLEL_FACTOR
* DEFAULT_DATE_FORMAT
* TRACE_LOG_LEVEL
* DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE
* MAX_SESSION_COUNT
* SESSION_IDLE_TIMEOUT_SEC
* PROCESS_MAX_SIZE
* TAG_CACHE_MAX_MEMORY_SIZE


## ALTER SESSION

개별 세션 단위로 자원을 관리하거나 설정을 변경할 때 사용하는 구문입니다.

### SET SQL_LOGGING

**alter_session_sql_logging_stmt:**

![alter_session_sql_logging_stmt](/images/sql/sys/alter_session_sql_logging_stmt.png)

```sql
alter_session_sql_logging_stmt ::= 'ALTER SESSION SET SQL_LOGGING' '=' flag
```

세션의 트레이스 로그에 메시지를 남길지 여부를 지정합니다.

다음과 같은 비트 플래그 값을 사용할 수 있습니다.
* 0x1: 파싱·검증·최적화 단계 로그
* 0x2: DDL 수행 결과 로그

따라서 값이 2이면 DDL 로그만 기록되고, 값이 3이면 오류와 DDL 로그가 함께 기록됩니다.
아래는 세션의 로깅 플래그를 변경해 오류 로그를 남기는 예시입니다.

```sql
Mach> alter session set SQL_LOGGING=1;
Altered successfully.
Mach> exit
```

### SET DEFAULT_DATE_FORMAT

**alter_session_set_defalut_dateformat_stmt:**

![alter_session_set_defalut_dateformat_stmt](/images/sql/sys/alter_session_set_defalut_dateformat_stmt.png)

```sql
alter_session_set_defalut_dateformat_stmt ::= 'ALTER SESSION SET DEFAULT_DATE_FORMAT' '=' date_format
```
Sets the default format for Datetime data types for this session.

서버가 시작되면 시스템 속성 **DEFAULT_DATE_FORMAT** 값이 각 세션에도 설정됩니다. 
속성을 변경하지 않았다면 세션 기본값은 `"YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"`입니다. 
이 구문을 사용하면 시스템 전체 설정과 무관하게 특정 세션의 날짜 형식을 변경할 수 있습니다.
각 세션에 설정된 기본 날짜 형식은 V$SESSION에서 확인 가능합니다. 아래는 값을 조회하고 변경하는 예시입니다.

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

![alter_session_set_hidden_column_stmt](/images/sql/sys/alter_session_set_hidden_column_stmt.png)

```sql
alter_session_set_hidden_column_stmt ::= 'ALTER SESSION SET SHOW_HIDDEN_COLS' '=' ( '0' | '1' )
```

세션에서 `SELECT *`를 실행할 때 숨김 컬럼(`_arrival_time`)을 함께 출력할지 결정합니다.

서버가 시작되면 전역 속성 SHOW_HIDDEN_COLS 값이 각 세션에 0으로 설정됩니다. 
세션 기본 동작을 바꾸고 싶다면 이 값을 1로 변경하면 됩니다.
각 세션의 SHOW_HIDDEN_COLS 값은 V$SESSION에서 확인할 수 있습니다.


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

![alter_session_set_feedback_append_err_stmt](/images/sql/sys/alter_session_set_feedback_append_err_stmt.png)

```sql
alter_session_set_feedback_append_err_stmt ::= 'ALTER SESSION SET FEEDBACK_APPEND_ERROR' '=' ( '0' | '1' )
```

세션에서 발생한 Append 에러 메시지를 클라이언트 프로그램으로 전달할지 여부를 설정합니다.

값은 다음과 같습니다.
* 0 = 에러 메시지를 보내지 않음
* 1 = 에러 메시지를 전송

아래는 사용 예시입니다.

```sql
mach> ALTER SESSION SET FEEDBACK_APPEND_ERROR=0;
Altered successfully.
```

### SET MAX_QPX_MEM

**alter_session_set_max_qpx_mem_stmt:**

![alter_session_set_max_qpx_mem_stmt](/images/sql/sys/alter_session_set_max_qpx_mem_stmt.png)

```sql
alter_session_set_max_qpx_mem_stmt ::= 'ALTER SESSION SET MAX_QPX_MEM' '=' value
```

세션에서 실행되는 단일 SQL이 GROUP BY, DISTINCT, ORDER BY 연산을 수행할 때 사용할 수 있는 최대 메모리를 지정합니다.

설정한 한도를 초과해 메모리를 할당하려고 하면 SQL 실행이 중단되고 오류로 처리됩니다. 
오류 발생 시 쿼리를 포함한 오류 코드와 메시지가 `machbase.trc`에 기록됩니다.

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

- SQL 문이 최대 메모리를 초과했을 때의 trc 로그 예시

```sql
[2021-03-08 16:36:32 P-69000 T-140515328653056][INFO] DML FAILURE (2E10000084:Memory allocation error (alloc'd: 1048595, max: 1048576).)
```

- SQL 문이 최대 메모리를 초과했을 때 machsql 에러 메시지 예시

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

![alter_session_set_session_idle_timeout_sec_stmt](/images/sql/sys/alter_session_set_session_idle_timeout_sec_stmt.png)

```sql
alter_session_set_session_idle_timeout_sec_stmt ::= 'ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC' '=' value
```

세션이 유휴 상태일 때 연결을 유지할 최대 시간을 지정합니다.
초 단위로 설정하며, 지정한 시간이 지나면 해당 세션이 종료됩니다.
설정된 유휴 제한 시간은 V$SESSION에서 확인할 수 있습니다.

```sql
Mach> ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC=200;
Altered successfully.
 
 
Mach> SELECT IDLE_TIMEOUT FROM V$SESSION;
IDLE_TIMEOUT        
-----------------------
200                                     
[1] row(s) selected.
```

### SET QUERY_TIMEOUT

**alter_session_set_query_timeout_stmt:**

![alter_session_set_query_timeout_stmt](/images/sql/sys/alter_session_set_query_timeout_stmt.png)

```sql
alter_session_set_query_timeout_stmt ::= 'ALTER SESSION SET QUERY_TIMEOUT' '=' value
```

세션에서 쿼리를 실행할 때 서버 응답을 기다리는 최대 시간을 지정합니다.
초 단위로 설정하며, 지정한 시간을 초과하면 쿼리가 자동으로 중단됩니다.
세션에 설정된 QUERY_TIMEOUT 값은 V$SESSION에서 확인할 수 있습니다.

```sql
Mach> ALTER SESSION SET QUERY_TIMEOUT=200;
Altered successfully.
 
Mach> SELECT QUERY_TIMEOUT FROM V$SESSION;
QUERY_TIMEOUT        
-----------------------
200                                     
[1] row(s) selected.
```
