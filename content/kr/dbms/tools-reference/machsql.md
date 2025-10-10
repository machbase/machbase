---
type: docs
title : machsql
type : docs
weight: 40
---

MACHSQL은 터미널 화면을 통해 SQL질의를 수행하는 대화형 도구이다.

## 구동 옵션 설명

```bash
[mach@localhost]$ machsql -h
```

| 짧은 옵션 | 긴 옵션           |                       설명                      |
|-----------|-------------------|:-----------------------------------------------:|
| -s        | --server          | 접속할 서버의 IP 주소 (default : 127.0.0.1)     |
| -u        | --user            | 사용자명 (default : SYS)                        |
| -p        | --password        | 사용자 패스워드 (default : MANAGER)             |
| -P        | --port            | 서버의 포트 번호 (default : 5656)               |
| -n        | --nls             | NLS 설정                                        |
| -f        | --script          | 실행할 SQL 스크립트 파일                        |
| -z        | --timezone=+-HHMM | Timezone 설정 ex) +0900   -1230                 |
| -o        | --output          | 질의 결과를 저장할 파일명                       |
| -i        | --silent          | 저작권 출력 없이 실행                           |
| -v        | --verbose         | 상세 출력                                       |
| -r        | --format          | 출력 파일 포맷 지정 (default: csv)              |
| -h        | --help            | 옵션 출력                                       |
| -c        | N/A               | Connection 매개변수 추가(6.1이후 버전부터 지원) |

**Example:**

```bash
machsql -s localhost -u sys -p manager
machsql --server=localhost --user=sys --password=manager
machsql -s localhost -u sys -p manager -f script.sql
## 6.1 이후버전부터 지원
machsql -s 127.0.0.1 -u sys -p manager -P 8888 -c ALTERNATIVE_SERVERS=192.168.0.147:9209;CONNECTION_TIMEOUT=10
```

## 환경변수 MACHBASE_CONNECTION_STRING

기본 접속  매개변수를 지정한다. 예를 들어 CONNECTION_TIMEOUT 값 설정 및 ALTERNATIVE_SERVERS 설정을 추가하기 위해 다음의 환경변수를 설정할 수 있다.

```bash
export MACHBASE_CONNECTION_STRING=ALTERNATIVE_SERVERS=192.168.0.148:8888;CONNECTION_TIMEOUT=3
```
-c 옵션으로 접속 매개변수를 지정하면 환경변수보다 우선하여 수행된다. 이 기능은 6.1 이후 버전부터 지원한다.

## SHOW 명령어

테이블, 테이블스페이스, 인덱스 등의 정보를 출력한다.

SHOW 명령어 목록

* SHOW INDEX
* SHOW INDEXES
* SHOW INDEXGAP
* SHOW LSM
* SHOW LICENSE
* SHOW STATEMENTS
* SHOW STORAGE
* SHOW TABLE
* SHOW TABLES
* SHOW TABLESPACE
* SHOW TABLESPACES
* SHOW USERS

### SHOW INDEX

인덱스 정보를 출력한다.

**Syntax:**

```
SHOW INDEX index_name
```

**Example:**

```sql
Mach> CREATE TABLE t1 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE VOLATILE TABLE t2 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE INDEX t1_idx1 ON t1(c1) INDEX_TYPE LSM;
Created successfully.
Mach> CREATE INDEX t1_idx2 ON t1(c1) INDEX_TYPE BITMAP;
Created successfully.
Mach> CREATE INDEX t2_idx1 ON t2(c1) INDEX_TYPE REDBLACK;
Created successfully.
Mach> CREATE INDEX t2_idx2 ON t2(c2) INDEX_TYPE REDBLACK;
Created successfully.
 
Mach> SHOW INDEX t1_idx2;
TABLE_NAME                                COLUMN_NAME                               INDEX_NAME                      
----------------------------------------------------------------------------------------------------------------------------------
INDEX_TYPE   BLOOM_FILTER  KEY_COMPRESS  MAX_LEVEL   PART_VALUE_COUNT BITMAP_ENCODE
--------------------------------------------------------------------------------------------
T1                                        C1                                        T1_IDX2                         
LSM          ENABLE   COMPRESSED    2           100000      EQUAL
[1] row(s) selected.
```

### SHOW INDEXES

인덱스 전체 리스트를 출력한다.

**Syntax:**

```
SHOW INDEXES
```

**Example:**

```sql
Mach> CREATE TABLE t1 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE VOLATILE TABLE t2 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE INDEX t1_idx1 ON t1(c1) INDEX_TYPE LSM;
Created successfully.
Mach> CREATE INDEX t1_idx2 ON t1(c1) INDEX_TYPE BITMAP;
Created successfully.
Mach> CREATE INDEX t2_idx1 ON t2(c1) INDEX_TYPE REDBLACK;
Created successfully.
Mach> CREATE INDEX t2_idx2 ON t2(c2) INDEX_TYPE REDBLACK;
Created successfully.
 
Mach> SHOW INDEXES;
TABLE_NAME                                COLUMN_NAME                               INDEX_NAME                      
----------------------------------------------------------------------------------------------------------------------------------
INDEX_TYPE
---------------
T1                                        C1                                        T1_IDX1                         
LSM
T1                                        C1                                        T1_IDX2                         
LSM
T2                                        C2                                        T2_IDX2                         
REDBLACK
T2                                        C1                                        T2_IDX1                         
REDBLACK
[4] row(s) selected.
```

### SHOW INDEXGAP

인덱스 생성 GAP 정보를 출력한다. 

**Example:**

```sql
Mach> SHOW INDEXGAP
TABLE_NAME                                INDEX_NAME                                GAP
-------------------------------------------------------------------------------------------------------------
INDEX_TABLE                               T1_IDX1                                   0
INDEX_TABLE                               T1_IDX2                                   0
```

### SHOW LSM

LSM 인덱스 생성 정보를 출력한다.

**Example:**

```sql
Mach> SHOW LSM;
TABLE_NAME                                INDEX_NAME                                LEVEL       COUNT
--------------------------------------------------------------------------------------------------------------------------
T1                                        IDX1                                      0           0
T1                                        IDX1                                      1           100000
T1                                        IDX1                                      2           0
T1                                        IDX1                                      3           0
T1                                        IDX2                                      0           100000
T1                                        IDX2                                      1           0
[6] row(s) selected.
```

### SHOW LICENSE

라이선스 정보를 출력한다.

**Example:**

```sql
Mach> SHOW LICENSE
INSTALL_DATE          ISSUE_DATE            EXPIRY_DATE  TYPE        POLICY    
---------------------------------------------------------------------------------------
2016-07-01 10:24:37   20160325              20170325    2           0         
[1] row(s) selected.
```

### SHOW STATEMENTS

서버에 등록(Prepare, Execute, Fetch)된 모든 질의문을 출력한다.

**Example:**

```sql
Mach> SHOW STATEMENTS
USER_ID     SESSION_ID  QUERY                                                                           
--------------------------------------------------------------------------------------------------------------
0           2           SELECT ID USER_ID, SESS_ID SESSION_ID, QUERY FROM V$STMT                        
[1] row(s) selected.
```

### SHOW STORAGE

사용자가 생성한 테이블 별 디스크 사용량을 출력한다.
**Syntax:**

```
SHOW STORAGE
```

**Example:**

```sql
Mach> CREATE TAGDATA TABLE TAG (name varchar(20) primary key, time datetime basetime, value double summarized);
Created successfully.
 
Mach> SHOW STORAGE
TABLE_NAME                                          DATA_SIZE            INDEX_SIZE           TOTAL_SIZE          
------------------------------------------------------------------------------------------------------------------------  
_TAG_DATA_0                                         50335744             0                    50335744            
_TAG_DATA_1                                         50335744             0                    50335744            
_TAG_DATA_2                                         50335744             0                    50335744            
_TAG_DATA_3                                         50335744             0                    50335744            
_TAG_META                                           0                    0                    0
```

### SHOW TABLE

사용자가 생성한 테이블의 정보를 출력한다.

**Syntax:**

```
SHOW TABLE table_name
```

**Example:**

```sql
Mach> CREATE TABLE t1 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE INDEX t1_idx1 ON t1(c1) INDEX_TYPE LSM;
Created successfully.
Mach> CREATE INDEX t1_idx2 ON t1(c1) INDEX_TYPE BITMAP;
Created successfully.
 
Mach> SHOW TABLE T1
[ COLUMN ]
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
C1                            integer             11
C2                            varchar             10
 
[ INDEX ]
----------------------------------------------------------------
NAME                          TYPE                COLUMN
----------------------------------------------------------------
T1_IDX1                       LSM                 C1
T1_IDX2                       LSM                 C1
```

### SHOW TABLES

사용자가 생성한 테이블 전체 목록을 출력한다.

**Example:**

```sql
Mach> SHOW TABLES
NAME                                    
--------------------------------------------
BONUS                                   
DEPT                                    
EMP                                     
SALGRADE                                
[4] row(s) selected.
```

### SHOW TABLESPACE

테이블 스페이스 정보를 출력한다.

**Example:**

```sql
Mach> CREATE TABLE t1 (id integer);
Created successfully.
Mach> CREATE INDEX t1_idx_id ON t1(id);
Created successfully.
 
Mach> SHOW TABLESPACE SYSTEM_TABLESPACE;
[TABLE]
NAME                                      TYPE
-------------------------------------------------------
T1                                        LOG
[1] row(s) selected.
 
[INDEX]
TABLE_NAME                                COLUMN_NAME                               INDEX_NAME                      
----------------------------------------------------------------------------------------------------------------------------------
T1                                        ID                                        T1_IDX_ID                   
[1] row(s) selected.
```

### SHOW TABLESPACES

테이블스페이스 전체 목록을 출력한다.

**Example:**

```sql
Mach> CREATE TABLESPACE tbs1 DATADISK disk1 (DISK_PATH="tbs1_disk1"), disk2 (DISK_PATH="tbs1_disk2"), disk3 (DISK_PATH="tbs1_disk3");
Created successfully.
 
-- 데이터를 입력한다
...
...
 
 
Mach> SHOW TABLESPACES;
NAME                                                                              DISK_COUNT  USAGE
-----------------------------------------------------------------------------------------------------------------------
SYSTEM_TABLESPACE                                                                 1           0
TBS1                                                                              3           25824256
[2] row(s) selected.
```

### SHOW USERS

사용자 목록을 출력한다.

**Example:**

```sql
Mach> CREATE USER testuser IDENTIFIED BY 'test1234';
Created successfully.
 
Mach> SHOW USERS;
USER_NAME                               
--------------------------------------------
SYS                                     
TESTUSER
[2] row(s) selected.
```
