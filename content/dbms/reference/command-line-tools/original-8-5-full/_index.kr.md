---
type: docs
title: '17.4.10 전체 명령행 도구 레퍼런스'
weight: 95
tocSort: true
---


## machadmin


machadmin은 Machbase 서버를 시작하거나 종료하고, 데이터베이스의 생성, 삭제 및 실행 상태를 확인하는 데 사용됩니다.

## 옵션 및 기능

machadmin의 옵션은 다음과 같습니다. 이전 설치 섹션에서 설명한 기능은 생략되었습니다.

```bash
mach@localhost:~$ machadmin -h
```

| 옵션 | 설명 |
|--|--|
|-u, --startup|Machbase 서버 시작 |
|--recovery[=simple,complex,reset]|시작 시 사용하는 복구 모드 (기본값: simple) |
|-s, --shutdown |Machbase 서버 정상 종료 |
|-c, --createdb |Machbase 데이터베이스 생성 |
| -d, --destroydb| Machbase 데이터베이스 삭제 |
| -k, --kill| Machbase 서버 강제 종료 |
| -i, --silent| 출력을 줄여 실행 |
| -r, --restore |백업으로부터 데이터베이스 복구 |
| -x, --extract| 백업 파일을 백업 디렉토리로 변환 |
| -w, --viewimage| 백업 이미지 파일 정보 출력 |
|-e, --check| Machbase 서버 실행 상태 확인 |
|-t, --licinstall| 라이선스 파일 설치 |
|-f, --licinfo| 설치된 라이선스 정보 출력|
|--home-path=path|Machbase 홈 경로 지정 |

## 복구 모드

구문

```
machadmin -u --recovery=[simple | complex | reset]
```

복구 모드는 다음과 같습니다:

* simple: 서버 실행 중 전원 손실이 없었다면 기본적으로 simple 복구 모드가 실행됩니다.
* complex: complex 복구 모드는 simple 모드보다 실행 시간이 더 오래 걸립니다. 전원이 꺼진 후 재시작할 때 기본적으로 실행됩니다.
* reset: simple 또는 complex 모드에서 복구가 수행되지 않을 때, 모든 테이블의 모든 데이터를 검사하여 데이터베이스를 복구합니다. 이 경우 일부 데이터 손실이 발생할 수 있습니다.

## 서버 정상 종료

예제:

```
mach@localhost:~$ machadmin -s

-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for the server shut down...
Server shut down successfully.
```

## 데이터베이스 생성

예제:

```
mach@localhost:~$ machadmin -c
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Database created successfully.
```

## 데이터베이스 삭제

예제:

```
mach@localhost:~$ machadmin -d
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Destroy Machbase database- Are you sure?(y/N) y
Database destroyed successfully.
```

## 서버 강제 종료

구문:

```
machadmin -k
```

예제:

```
mach@localhost:~$ machadmin -k
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for Machbase terminated...
Server terminated successfully.
```

## 무음 모드 실행

'machadmin' 실행 시 출력되는 메시지를 제거합니다.

구문:

```
machadmin -i
```

## 데이터베이스 복구

구문:

```
machadmin -r backup_database_path
```

예제:

```
mach@localhost:~$ machadmin -r 'backup'
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Backed up database restored successfully.
```

## 서버 실행 여부 확인

구문:

```
machadmin -e
```


서버가 실행 중이 아닐 때의 예제:

```
mach@localhost:~$ machadmin -e
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
[ERR] Server is not running.
```


서버가 실행 중일 때의 예제:

```
mach@localhost:~$ machadmin -e
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Machbase server is already running with PID (14098).
```

## 라이선스 파일 설치

구문:

```
machadmin -t license_file
```


예제:

```
mach@localhost:~$ machadmin -t license.dat
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
License installed successfully.
```

## 라이선스 확인

예제:

```
mach@localhost:~$ machadmin -f
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
	                   INFORMATION
ID                                : 00000001
Issue Date                        : 2099-12-31
License Type(Version 3)           : FOGUNLIMITED
Company                           : MACHBASE
Project(Product)                  : NONE
Country Code                      : KR
Install Date                      : 2026-06-13 15:08:00
-----------------------------------------------------------------
License information displayed successfully.
-----------------------------------------------------------------
License information displayed successfully.
```

## machsql


MACHSQL은 터미널 화면을 통해 SQL질의를 수행하는 대화형 도구입니다.

## 구동 옵션 설명

```bash
[mach@localhost]$ machsql -h
```

| 짧은 옵션 | 긴 옵션           |                       설명                      |
|-----------|-------------------|:-----------------------------------------------:|
| -s        | --server          | 접속할 서버의 IP 주소 (default : 127.0.0.1)     |
| -u        | --user            | 사용자명 (default : SYS)                        |
| -p        | --password        | 사용자 패스워드 (default : MANAGER)             |
| -K        | --auth-key-file   | 인증용 개인키 파일 경로 (Machbase 8.5 이상 지원) |
| -P        | --port            | 서버의 포트 번호 (default : 5656)               |
| -n        | --nls             | NLS 설정                                        |
| -f        | --script          | 실행할 SQL 스크립트 파일                        |
| -z        | --timezone=+-HHMM | Timezone 설정 ex) +0900   -1230                 |
| -o        | --output          | 질의 결과를 저장할 파일명                       |
| -i        | --silent          | 저작권 출력 없이 실행                           |
| -v        | --verbose         | 상세 출력                                       |
| -x        | --testing         | 테스트 모드로 실행                              |
| -r        | --format          | 출력 파일 포맷 지정 (default: csv)              |
|           | --auth-sig-scheme | 인증 서명 스킴 (`ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`; Machbase 8.5 이상 지원) |
| -h        | --help            | 옵션 출력                                       |
| -c        | --connstr         | Connection 매개변수 추가(6.1 이후 버전부터 지원) |

**Example:**

```bash
machsql -s localhost -u sys -p manager
machsql --server=localhost --user=sys --password=manager
machsql -s localhost -u sys -p manager -f script.sql
machsql -s localhost -u app_user -K /opt/machbase/keys/app_user_ecdsa.pem --auth-sig-scheme=ECDSA -f script.sql
## 6.1 이후버전부터 지원
machsql -s 127.0.0.1 -u sys -p manager -P 8888 -c ALTERNATIVE_SERVERS=192.168.0.147:9209;CONNECTION_TIMEOUT=10
```

## AUTH KEY challenge 인증

> **참고**: 이 기능은 Machbase 8.5 이상에서 지원됩니다.

`machsql`은 비밀번호 인증 외에 공개키 기반 challenge 인증도 지원합니다.

### 전용 옵션 사용

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_ecdsa.pem \
    --auth-sig-scheme=ECDSA \
    -f script.sql
```

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_rsa.pem \
    --auth-sig-scheme=RSA_PSS \
    -f script.sql
```

설명:

- `-K`, `--auth-key-file`을 지정하면 내부적으로 `AUTH_MODE=CHALLENGE`가 적용됩니다.
- `--auth-sig-scheme`를 생략하면 키 알고리즘 기준 기본 스킴을 사용합니다.
  - ECDSA 키: `ECDSA`
  - RSA 키: `RSA_PKCS1_V15`
- 지원 키 파라미터는 ECDSA `P-256`, `P-384`, `P-521` 및 RSA `2048`, `3072`, `4096` bits입니다.
- RSA-PSS 인증을 사용하려면 `--auth-sig-scheme=RSA_PSS`를 명시합니다.
- `AUTH_MODE=CHALLENGE`에서는 `-p`를 인증에 사용하지 않습니다.
- POSIX 환경에서는 개인키 파일 권한을 `600`으로 제한하는 것을 권장합니다.

### connection string 사용

```bash
machsql -c "SERVER=127.0.0.1;PORT_NO=5656;UID=APP_USER;AUTH_MODE=CHALLENGE;AUTH_SIG_SCHEME=ECDSA;AUTH_KEY_FILE=/opt/machbase/keys/app_user_ecdsa.pem;" -f script.sql
```

connection string 형태는 프로세스 인자나 로그에 키 파일 경로가 노출될 수 있으므로, 가능하면 `-K` 옵션 사용을 권장합니다.

### 실패 예시

- 키 파일이 없으면 인증이 실패합니다.
- 키 타입과 `AUTH_SIG_SCHEME`가 맞지 않으면 인증이 실패합니다.
- 만료(`VALID_BEFORE`)되었거나 비활성화된 AUTH KEY로는 인증할 수 없습니다.

## 환경변수 MACHBASE_CONNECTION_STRING

기본 접속  매개변수를 지정합니다. 예를 들어 CONNECTION_TIMEOUT 값 설정 및 ALTERNATIVE_SERVERS 설정을 추가하기 위해 다음의 환경변수를 설정할 수 있습니다.

```bash
export MACHBASE_CONNECTION_STRING=ALTERNATIVE_SERVERS=192.168.0.148:8888;CONNECTION_TIMEOUT=3
```
-c 옵션으로 접속 매개변수를 지정하면 환경변수보다 우선하여 수행됩니다. 이 기능은 6.1 이후 버전부터 지원합니다.

## SHOW 명령어

테이블, 테이블스페이스, 인덱스 등의 정보를 출력합니다.

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

인덱스 정보를 출력합니다.

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
Mach> CREATE INDEX t1_idx2 ON t1(c2) INDEX_TYPE BITMAP;
Created successfully.
Mach> CREATE INDEX t2_idx1 ON t2(c1) INDEX_TYPE REDBLACK;
Created successfully.
Mach> CREATE INDEX t2_idx2 ON t2(c2) INDEX_TYPE REDBLACK;
Created successfully.

Mach> SHOW INDEX t1_idx2;
TABLE_NAME                                          COLUMN_NAME                                         INDEX_NAME                                          INDEX_TYPE   KEY_COMPRESS  MAX_LEVEL
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PART_VALUE_COUNT BITMAP_ENCODE
-----------------------------------
T1                                                  C2                                                  T1_IDX2                                             LSM          COMPRESSED    2
100000           EQUAL
[1] row(s) selected.
```

### SHOW INDEXES

인덱스 전체 리스트를 출력합니다.

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
Mach> CREATE INDEX t1_idx2 ON t1(c2) INDEX_TYPE BITMAP;
Created successfully.
Mach> CREATE INDEX t2_idx1 ON t2(c1) INDEX_TYPE REDBLACK;
Created successfully.
Mach> CREATE INDEX t2_idx2 ON t2(c2) INDEX_TYPE REDBLACK;
Created successfully.

Mach> SHOW INDEXES;
USER_NAME             TABLE_NAME                                          COLUMN_NAME                                         INDEX_NAME                                          INDEX_TYPE
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
SYS                   T1                                                  C1                                                  T1_IDX1                                             LSM
SYS                   T1                                                  C2                                                  T1_IDX2                                             LSM
SYS                   T2                                                  C2                                                  T2_IDX2                                             REDBLACK
SYS                   T2                                                  C1                                                  T2_IDX1                                             REDBLACK
[4] row(s) selected.
```

### SHOW INDEXGAP

인덱스 생성 GAP 정보를 출력합니다.

**Example:**

```sql
Mach> SHOW INDEXGAP
TABLE_NAME                                INDEX_NAME                                GAP
-------------------------------------------------------------------------------------------------------------
INDEX_TABLE                               T1_IDX1                                   0
INDEX_TABLE                               T1_IDX2                                   0
```

### SHOW LSM

LSM 인덱스 생성 정보를 출력합니다.

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

라이선스 정보를 출력합니다.

**Example:**

```sql
Mach> SHOW LICENSE
INSTALL_DATE          ISSUE_DATE            EXPIRY_DATE  TYPE        POLICY
---------------------------------------------------------------------------------------
2016-07-01 10:24:37   20160325              20170325    2           0
[1] row(s) selected.
```

### SHOW STATEMENTS

서버에 등록(Prepare, Execute, Fetch)된 모든 질의문을 출력합니다.

**Example:**

```sql
Mach> SHOW STATEMENTS
USER_ID     SESSION_ID  QUERY
--------------------------------------------------------------------------------------------------------------
0           2           SELECT ID USER_ID, SESS_ID SESSION_ID, QUERY FROM V$STMT
[1] row(s) selected.
```

### SHOW STORAGE

사용자가 생성한 테이블 별 디스크 사용량을 출력합니다.
**Syntax:**

```
SHOW STORAGE
```

**Example:**

```sql
Mach> CREATE TAG TABLE TAG (name varchar(20) primary key, time datetime basetime, value double summarized);
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

사용자가 생성한 테이블의 정보를 출력합니다.

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

사용자가 생성한 테이블 전체 목록을 출력합니다.

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

테이블 스페이스 정보를 출력합니다.

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

테이블스페이스 전체 목록을 출력합니다.

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

사용자 목록을 출력합니다.

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

## machloader


machloader는 텍스트 파일 데이터를 Machbase 서버로 가져오거나 내보내는 데 사용됩니다. 기본적으로 CSV 파일과 함께 작동하지만 다른 형식도 지원합니다.

machloader의 기능은 다음과 같습니다.

* machloader는 스키마 파일에서 datetime 타입을 지정할 수 있습니다. 지정된 datetime 타입은 Machbase 서버에서 지원하는 타입이어야 합니다. 하나의 datetime 타입을 모든 필드에 적용할 수 있으며, 각 필드는 다른 형식을 가질 수 있습니다.
* 입력 대상 테이블 데이터를 삭제하고 입력하려면 "-m replace" 옵션을 사용합니다.
* machloader는 스키마와 데이터 파일의 일관성을 확인하지 않습니다. 사용자는 스키마, 테이블 및 데이터 파일이 일관성을 충족하는지 확인해야 합니다.
* machloader는 기본적으로 APPEND 모드를 지원합니다.
* machloader는 기본적으로 `_ARRIVAL_TIME` 컬럼을 사용하지 않습니다. 해당 컬럼 데이터를 가져오거나 내보내려면 "-a" 옵션을 사용해야 합니다.

지원하는 날짜/시간 포맷 토큰은 [TO_CHAR](/dbms/reference/sql/dictionary/functions-full/#to_char)을 참고하세요.

machloader의 옵션은 다음 명령으로 확인할 수 있습니다:

```bash
[mach@localhost]$ machloader -h
```

|옵션| 설명|
|--|--|
|-s, --server=SERVER|Machbase 서버 IP 주소 입력 (기본값: 127.0.0.1)|
|-u, --user=USER|연결 사용자 이름 입력 (기본값: SYS)|
|-p, --password=PASSWORD|연결 사용자 비밀번호 (기본값: MANAGER)|
|-P, --port=PORT|Machbase 서버 포트 번호 (기본값: 5656)|
|-i, --import|데이터 가져오기 명령 옵션|
|-o, --export|데이터 내보내기 명령 옵션|
|-c, --schema|데이터베이스 테이블 정보를 사용하여 스키마 파일을 생성하는 명령 옵션|
|-t, --table=TABLE_NAME|스키마 파일을 생성할 테이블 이름 설정|
|-f, --form=SCHEMA_FORM_FILE|스키마 파일 이름 지정|
|-d, --data=DATA_FILE|데이터 파일 이름 지정|
|-l, --log=LOG_FILE|machloader 실행 로그 파일 지정|
|-b, --bad=BAD_FILE|-i 옵션 실행 시 입력 오류가 발생한 데이터를 기록하고 오류 설명을 기록하는 파일 이름 지정|
|-m, --mode=MODE|-i 옵션 실행 시 가져오기 방법 표시. append 또는 replace 옵션을 사용할 수 있습니다. Append는 기존 데이터 뒤에 데이터를 입력하고, replace는 기존 데이터를 삭제한 후 데이터를 입력합니다.|
|-D, --delimiter=DELIMITER|각 필드 구분자 설정. 기본값은 ','입니다.|
|-n, --newline=NEWLINE|각 레코드 구분자 설정. 기본값은 '\n'입니다.|
|-e, --enclosure=ENCLOSURE|각 필드의 둘러싸는 구분자 설정|
|-r, --format=FORMAT|파일 입출력 형식 지정 (기본값: csv)|
|--first=FIRST_ROW|처리할 첫 번째 행 번호 설정|
|-a, --atime|내장 컬럼 `_ARRIVAL_TIME` 사용 여부 결정. 기본값은 컬럼을 사용하지 않습니다|
|-z, --timezone|타임존 설정 예) +0900 -1230|
|-I, --silent| 저작권 관련 출력 및 가져오기/내보내기 상태 정보를 표시하지 않습니다|
|-h, --help	| 옵션 목록 표시|
|-F, --dateformat=DATEFORMAT| 컬럼 날짜 형식 설정 (`_arrival_time YYYY-MM-DD HH24:MI:SS`)<br> dateformat 대신 'unixtimestamp'를 설정하면 입력 값이 unix 타임스탬프 값으로 간주됩니다. ("time_column unixtimestamp")<br> dateformat 대신 'nanotimestamp'를 설정하면 입력 값이 나노초 단위의 타임스탬프 값으로 간주됩니다. ("time_column nanotimestamp")|
|-E, --encoding=CHARACTER_SET| 입출력 파일의 인코딩 설정. 지원되는 인코딩은 UTF8(기본값), ASCII, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280, UTF16입니다.|
|-C, --create| 가져오기 시 테이블이 없으면 테이블을 생성합니다.|
|-H, --header|가져오기/내보내기 시 헤더 정보 존재 여부 설정. 기본값은 설정되지 않습니다|
|--summary|선택된 옵션 값을 출력하고, 데이터를 가져오거나 내보내지 않고 종료합니다.|
|-S, --slash|백슬래시 구분자 지정|

자세한 사용법은 다음과 같습니다.

## CSV 파일 가져오기

CSV 파일을 Machbase 서버로 가져옵니다.

옵션:

```
-i: 가져오기 지정 옵션
-d: 데이터 파일 이름 지정 옵션
-t: 테이블 이름 지정 옵션
```

예제:

```
machloader -i -d data.csv -t table_name
```

## CSV 파일 내보내기

데이터를 CSV 파일에 씁니다.

옵션:

```
-o: 내보내기 지정 옵션
-d: 데이터 파일 이름 지정 옵션
-t: 테이블 이름 지정 옵션
```

예제:

```
machloader -o -d data.csv -t table_name
```

## CSV 파일 헤더 사용

CSV 파일의 헤더 관련 설정입니다.

옵션:

```
-i -H: 가져오기 시 CSV 파일의 첫 줄을 헤더로 인식하여 입력에서 제외합니다.
-o -H: 내보내기 시 테이블 컬럼명을 CSV 헤더로 생성합니다.
```

예제:

```
machloader -i -d data.csv -t table_name -H
machloader -o -d data.csv -t table_name -H
```


## 자동 테이블 생성

자동 테이블 생성 관련 옵션입니다.

옵션:

```
-C: 가져오기 시 테이블을 자동 생성합니다. 컬럼명은 c0, c1, ... 순서로 생성되며 타입은 varchar(32767)입니다.
-H: 가져오기 시 CSV 헤더명을 컬럼명으로 사용합니다.
```

예제:

```
machloader -i -d data.csv -t table_name -C
machloader -i -d data.csv -t table_name -C -H
```


## CSV가 아닌 파일 형식

CSV 형식이 아닌 파일에 사용할 구분자를 설정합니다.

옵션:

```
-D: 각 필드 구분자 지정
-n: 각 레코드 구분자 지정
-e: 각 필드의 enclosing 문자 지정
```

예제:

```
machloader -i -d data.txt -t table_name -D '^' -n '\n' -e '"'
machloader -o -d data.txt -t table_name -D '^' -n '\n' -e '"'
```

## 입력 모드 지정

가져오기(`-i`) 시 `replace`와 `append` 두 모드를 사용할 수 있습니다. 기본값은
`append`입니다. `replace` 모드는 기존 데이터를 삭제하므로 주의해서 사용해야 합니다.

옵션:

```
-m: 가져오기 모드 지정
```

예제:

```
machloader -i -d data.csv -t table_name -m replace
```

## 접속 정보 지정

서버 IP, 사용자, 비밀번호를 별도로 지정합니다.

옵션:

```
-s: 서버 IP 주소 지정 (기본값: 127.0.0.1)
-P: 서버 포트 번호 지정 (기본값: 5656)
-u: 접속 사용자 이름 지정 (기본값: SYS)
-p: 접속 사용자 비밀번호 지정 (기본값: MANAGER)
```

예제:

```
machloader -i -s 192.168.0.10 -P 5656 -u mach -p machbase -d data.csv -t table_name
```

## 로그 파일 생성

machloader 실행 로그와 bad-data 파일을 생성합니다.

옵션:

```
-b: 가져오기 실패 행을 기록할 bad-data 파일 이름 지정
-l: 가져오기 실패 행과 오류 메시지를 기록할 실행 로그 파일 이름 지정
```

예제:

```
machloader -i -d data.csv -t table_name -b table_name.bad -l table_name.log
```

## 스키마 파일 생성

machloader 스키마 파일을 생성할 수 있습니다. 스키마 파일을 사용하면 데이터 타입
형식을 변경하거나 테이블과 데이터 파일의 컬럼 수가 다른 경우에도 가져오기/내보내기를
수행할 수 있습니다.

옵션:

```
-c: 스키마 파일 생성 옵션
-t: 테이블 이름 지정 옵션
-f: 생성할 스키마 파일 이름 지정 옵션
```

예제:

```
machloader -c -t table_name -f table_name.fmt
machloader -c -t table_name -f table_name.fmt -a
```

## 스키마 파일에서 datetime 형식 설정

`DATEFORMAT` 옵션으로 날짜 형식을 지정할 수 있습니다.

구문:

```
## 모든 datetime 컬럼에 설정
DATEFORMAT <dateformat>
```
## 개별 datetime 컬럼에 설정

```
DATEFORMAT <column_name> <format>
```

예제:

```
-- 스키마 파일(datetest.fmt)에서 datetest.csv 각 필드의 dateformat을 설정합니다.
datetest.fmt
table datetest
{
INS_DT datetime;
UPT_DT datetime;
}
DATEFORMAT ins_dt "YYYY/MM/DD HH12:MI:SS"
DATEFORMAT upt_dt "YYYY DD MM HH12:MI:SS"

datetest.csv
2017/02/20 11:05:23,2017 20 02 11:05:23
2017/02/20 11:06:34,2017 20 02 11:06:34

-- datetest.csv 파일을 가져오고 입력 데이터를 확인합니다.
machloader -i -f datetest.fmt -d datetest.csv
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 8.5.4.develop
Copyright 2014, MACHBASE Corporation or its subsidiaries.
All Rights Reserved.
-----------------------------------------------------------------
Import time : 0 hour 0 min 0.39 sec
Load success count : 2
Load fail count : 0

mach> SELECT * FROM datetest;
INS_DT UPT_DT
-------------------------------------------------------------------
2017-02-20 11:06:34 000:000:000 2017-02-20 11:06:34 000:000:000
2017-02-20 11:05:23 000:000:000 2017-02-20 11:05:23 000:000:000
[2] row(s) selected.
Elapsed time: 0.000
```

## IGNORE

CSV 파일의 특정 필드를 입력하지 않으려면 fmt 파일에서 `IGNORE` 옵션을 설정할 수
있습니다. `ignoretest.csv` 파일에는 필드가 3개 있지만 마지막 필드가 필요 없다면,
fmt 파일에서 해당 컬럼에 `IGNORE`를 지정합니다.

예제:

```
-- ignoretest.fmt 파일의 마지막 필드에 IGNORE 옵션을 설정합니다.
ignoretest.fmt
table ignoretest
{
ID integer;
MSG varchar(40);
SUB_ID integer IGNORE;
}

ignoretest.csv
1, "msg1", 3
2, "msg2", 4


-- ignoretest.csv 파일을 가져오고 입력 데이터를 확인합니다.
machloader -i -f ignoretest.fmt -d ignoretest.csv
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 8.5.4.develop
Copyright 2014, MACHBASE Corporation or its subsidiaries.
All Rights Reserved.
-----------------------------------------------------------------
NLS : US7ASCII EXECUTE MODE : IMPORT
SCHEMA FILE : ignoretest.fmt DATA FILE : ignoretest.csv
IMPORT_MODE : APPEND FIELD TERM : ,
ROW TERM : \n ENCLOSURE : "
ARRIVAL_TIME : FALSE ENCODING : NONE
HEADER : FALSE CREATE TABLE : FALSE

Progress bar Imported records Error records
2 0

Import time : 0 hour 0 min 0.39 sec
Load success count : 2
Load fail count : 0


mach> SELECT * FROM ignoretest;
ID MSG
---------------------------------------------------------
2 msg2
1 msg1
[2] row(s) selected.
Elapsed time: 0.000
```

## 컬럼 수가 필드 수보다 많은 경우

테이블의 컬럼 수가 데이터 파일의 필드 수보다 많으면, 스키마 파일에 지정한 컬럼만
입력되고 나머지 컬럼은 `NULL`로 입력됩니다.

## 컬럼 수가 필드 수보다 적은 경우

테이블의 컬럼 수가 데이터 파일의 필드 수보다 적으면, 테이블에 없는 필드는 `IGNORE`
옵션으로 제외해야 합니다.

예제:

```
-- 마지막 필드에 IGNORE 옵션을 설정하여 해당 입력 데이터를 제외합니다.
loader_test.fmt
table loader_test
{
ID integer;
MSG varchar (40);
SUB_ID integer IGNORE;
}
```

## csv


'csvimport'와 'csvexport'는 Machbase 서버로 CSV 파일을 가져오거나 내보내기 위해 사용되는 도구입니다.

machloader를 사용한 CSV 파일의 간편한 사용을 위해 옵션이 단순화되었습니다.

아래 설명된 옵션 외에도 machloader에서 사용 가능한 모든 옵션을 사용할 수 있습니다.

지원하는 날짜/시간 포맷 토큰은 [TO_CHAR](/dbms/reference/sql/dictionary/functions-full/#to_char)을 참고하세요.

## 공통 래퍼 옵션

CSV 래퍼는 다음과 같은 자주 쓰는 machloader 옵션을 제공합니다:

|옵션|적용 대상|설명|
|--|--|--|
|-P, --port=PORT|csvimport, csvexport|서버 포트 번호 (기본값: 5656)|
|-l, --log=LOG_FILE|csvimport, csvexport|실행 로그 파일|
|-b, --bad=BAD_FILE|csvimport|가져오기 중 실패한 행을 기록하는 bad 파일|
|-m, --mode=MODE|csvimport|가져오기 모드 (`append` 또는 `replace`, 기본값: `append`)|
|-a, --atime|csvimport, csvexport|`_ARRIVAL_TIME` 컬럼 포함|
|-I, --silent|csvimport, csvexport|출력을 줄여 실행|
|-F, --dateformat=DATEFORMAT|csvimport, csvexport|`_arrival_time YYYY-MM-DD HH24:MI:SS` 같은 컬럼 날짜 형식|

## csvimport

csvimport를 사용하여 CSV 파일을 서버에 쉽게 입력할 수 있습니다.

### 기본 사용법

다음 옵션에 따라 테이블 이름과 데이터 파일 이름을 입력합니다.

옵션:

```
-t: 테이블 이름 지정 옵션
-d: 데이터 파일 이름 지정 옵션
* 옵션을 지정하지 않고 테이블 이름과 데이터 파일 이름만으로 실행할 수 있습니다.
```

예제:

```
csvimport -t table_name -d table_name.csv
csvimport table_name file_path
csvimport file_path table_name
```

### CSV 헤더 제외

입력 시 헤더를 제외하고 CSV 파일을 입력하려면 다음 옵션을 사용합니다.

옵션:

```
-H: CSV 파일의 첫 번째 라인을 헤더로 인식하고 가져오기 데이터에서는 제외합니다.
```

예제:

```
csvimport -t table_name -d table_name.csv -H
```

### 자동 테이블 생성

입력 시 테이블이 생성되지 않은 경우, 다음 옵션을 통해 테이블을 동시에 생성할 수 있습니다.

옵션

```
-C: 가져오기 중 자동으로 테이블을 생성합니다. 컬럼 이름은 c0, c1, .... 으로 자동 생성됩니다. 생성된 컬럼은 varchar(32767) 타입입니다.
-H: 가져오기 중 csv 헤더 이름으로 컬럼 이름을 생성합니다.
```

예제:

```
csvimport -t table_name -d table_name.csv -C
csvimport -t table_name -d table_name.csv -C -H
```


## csvexport

'csvexport'를 사용하여 데이터베이스 테이블 데이터를 CSV 파일로 쉽게 내보낼 수 있습니다.

### 기본 사용법

옵션:

```
-t: 테이블 이름 지정 옵션
-d: 데이터 파일 이름 지정 옵션
* 옵션을 지정하지 않고 테이블 이름과 데이터 파일 이름만으로 실행할 수 있습니다.
```

예제:

```
csvexport -t table_name -d table_name.csv
csvexport table_name file_path
csvexport file_path table_name
```

### CSV 헤더 사용

다음 옵션을 사용하면 내보낼 CSV 파일에 컬럼 이름으로 헤더를 추가할 수 있습니다.

옵션:

```
-H: 테이블 컬럼 이름으로 csv 파일의 헤더를 생성합니다.
```

예제:

```
csvexport -t table_name -d table_name.csv -H
```

## machcoordinatoradmin


Coordinator는 클러스터 전체 관리 도구입니다.

클러스터 에디션 패키지에만 존재합니다.

## 옵션 및 기능

machcoordinatoradmin의 옵션은 다음과 같습니다. 이전 섹션에서 설명한 기능은 생략되었습니다.

```
mach@localhost:~$ machcoordinatoradmin -h
```


|옵션| 설명|
|--|--|
|-u, --startup | Coordinator 프로세스 실행|
|-s, --shutdown | Coordinator 프로세스 종료|
|-k, --kill| Coordinator 프로세스 중지|
|-c, --createdb | Coordinator 메타 생성|
|-d, --destroydb| Coordinator 메타 제거, $MACHBASE_COORDINATOR_HOME/package의 패키지 파일 삭제|
|-e, --check | Coordinator 프로세스 실행 여부 확인|
|-i, --silent | 배너 출력 없이 실행|
|--configuration[=name] | 설정의 키와 값 출력 (특정 키만 출력 가능)|
|--configure | 시스템 속성 목록 출력 |
|--activate | 클러스터 상태를 Service로 전환|
|--deactivate | 클러스터 상태를 Deactivate로 전환|
|--list-package[=package] | 등록된 패키지 정보 목록 출력 (특정 패키지만 출력 가능)|
|--add-package=package | 패키지 추가|
|--remove-package=package | 패키지 삭제|
|--list-node[=node] | 노드 정보 목록 출력 (특정 노드만 출력 가능)|
|--add-node=node | 노드 추가|
|--remove-node=node | 노드 삭제|
|--attach-node=node | 기존 노드를 클러스터 메타에 연결|
|--detach-node=node | 노드를 클러스터 메타에서 분리|
|--upgrade-node=node | 노드 업그레이드|
|--startup-node=node | 노드 실행|
|--shutdown-node=node | 노드 종료|
|--kill-node=node | 노드 중지|
|--startup-lookup | Lookup 노드 실행|
|--shutdown-lookup | Lookup 노드 종료|
|--set-lookup-master=node | Lookup master 노드 지정|
|--cluster-status | 클러스터의 각 노드 상태 출력|
|--cluster-status-full | 클러스터의 각 노드 상태를 상세히 출력|
|--verbose | 클러스터 상태 출력 시 Deployer 상태를 함께 출력|
|--cluster-node | 클러스터 정보 출력|
|--set-group-state=`[normal | readonly]` | 특정 웨어하우스 그룹의 상태 변경|
|--set-warehouse-state=`[normal | scrapped]` | `--node`로 지정한 Warehouse 노드 상태 변경|
|--force-restore-warehouse=node | scrapped Warehouse 노드 강제 복구|
|--get-host-resource | 각 노드가 위치한 호스트 리소스 정보 출력|
|--host-resource-enable | 각 노드의 호스트 리소스 정보 수집 시작|
|--host-resource-disable | 각 노드의 호스트 리소스 정보 수집 중지|
|--deactivate-broker=node | 지정 노드를 inactive 상태로 전환|
|--activate-broker=node | 지정 노드를 normal 상태로 전환|
|--snapshot-interval=sec | Snapshot 실행 주기 설정|
|--exec-snapshot | Snapshot 실행 (`--group` 필요)|
|--snapshot-recover=node | 지정 노드 Snapshot 복구|
|--exec-sync=node | 지정 노드 Sync 실행|
|--snapshot-clean | Snapshot 정리|

|추가 옵션|설명|필수 옵션|
|--|--|--|
|--file-name=filename | 파일 이름| --add-package|
|--port-no=portno | 서비스 포트 번호| --add-node, --attach-node|
|--http-port-no=portno | HTTP 관리 포트 번호| --add-node, --attach-node|
|--deployer=node | Deployer 노드 이름| --add-node|
|--package-name=packagename | 설치 소스가 될 패키지 이름| --add-node, --upgrade-node|
|--home-path=path | Deployer 서버 기준, 현재 노드의 설치 경로| --add-node, --attach-node|
|--node-type=`[broker | warehouse | lookup]` | 노드 유형| --add-node, --attach-node |
|--lookup-type=`[master | slave | monitor]` | Lookup 노드 유형| --add-node, --attach-node |
|--node=node | 상태 변경 대상 노드 이름 또는 alias| --set-warehouse-state|
|--alias=alias | 추가 또는 연결할 노드의 alias| --add-node, --attach-node|
|--dbs-path=path | Broker/Warehouse 데이터베이스 파일 경로| --add-node|
|--group=groupname | 설치할 노드의 그룹 이름| --add-node, --attach-node, --set-group-state, --exec-snapshot |
|--replication=host:port | 복제를 교환할 host:port| --add-node, --attach-node |
|--no-replicate |설치할 노드에서 복제를 사용하지 않음 |--add-node, --attach-node|
|--primary=host:port | Secondary Coordinator 설치 시 Primary Coordinator의 노드 이름 지정 |-u, --startup|
|--host=host | 호스트 리소스 정보를 출력할 특정 호스트 지정| --get-host-resource|
|--metric=`[cpu|memory|disk|network]` | 호스트 리소스 정보를 출력할 특정 메트릭 지정| --get-host-resource|

## 실행 상태 확인

예제:

```
mach@localhost:~$ machcoordinatoradmin -e
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Machbase Coordinator is running with pid(29245)!
```

## 메타 생성 / 삭제

예제:

```
mach@localhost:~$ machcoordinatoradmin -c
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Coordinator metadata created successfully.

mach@localhost:~$ machcoordinatoradmin -d
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Coordinator metadata destroyed successfully.
```

## 설정 출력

구문:

```
machcoordinatoradmin --configuration[=name]
```

예제:

```
mach@localhost:~$ machcoordinatoradmin --configuration
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Name  : CLUSTER
Value : 3

Name  : DECISION
Value : ON

Name  : HOST-RESOURCE
Value : OFF

mach@localhost:~$ machcoordinatoradmin --configuration=decision
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : DECISION
             Value : ON
            Format : text/plain
```

## 시스템 속성 목록 출력

구문

```
machcoordinatoradmin --configure
```

예제

```
mach@localhost:~$ machcoordinatoradmin --configure

CLUSTER_LINK_HOST=192.168.0.30
CLUSTER_LINK_PORT_NO=36110
CLUSTER_LINK_THREAD_COUNT=16
CLUSTER_LINK_MAX_LISTEN=512
CLUSTER_LINK_MAX_POLL=4096
CLUSTER_LINK_ACCEPT_TIMEOUT=5000000
CLUSTER_LINK_CHECK_INTERVAL=1000000
CLUSTER_LINK_CONNECT_RETRY_TIMEOUT=60000000
CLUSTER_LINK_CONNECT_TIMEOUT=5000000
CLUSTER_LINK_HANDSHAKE_TIMEOUT=5000000
CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL=1000000
CLUSTER_LINK_LONG_WAIT_INTERVAL=1000000
CLUSTER_LINK_RECEIVE_TIMEOUT=5000000
CLUSTER_LINK_REQUEST_TIMEOUT=60000000
CLUSTER_LINK_SEND_TIMEOUT=5000000
CLUSTER_LINK_SESSION_TIMEOUT=3600000000
CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST=0
CLUSTER_LINK_BUFFER_SIZE=33554432
..
..
```


## 클러스터 상태 변경

예제:

```
mach@localhost:~$ machcoordinatoradmin --activate
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : CLUSTER
             Value : 3
            Format : text/plain


mach@localhost:~$ machcoordinatoradmin --deactivate
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : CLUSTER
             Value : 0
            Format : text/plain
```

## 패키지 정보 목록 출력

구문:

```
machcoordinatoradmin --list-package[=package]
```

예제:

```
mach@localhost:~$ machcoordinatoradmin --list-package
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Package Name : machbase
File Name    : machbase-cluster-6bab497c9.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64630670 bytes

Package Name : machbase2
File Name    : machbase-cluster-e3c0717.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64677030 bytes


mach@localhost:~$ machcoordinatoradmin --list-package=machbase
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Package Name : machbase
File Name    : machbase-cluster-6bab497c9.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64630670 bytes
```

## 노드 추가, Alias, DBS_PATH

Broker 또는 Warehouse 노드를 추가할 때는 `--node-type`, `--deployer`, `--package-name`, `--home-path`, `--port-no`를 함께 지정합니다. HTTP 관리 포트가 필요한 경우 `--http-port-no`를 지정합니다.

예제:

```
machcoordinatoradmin \
  --add-node=192.168.0.32:5401 \
  --node-type=warehouse \
  --deployer=192.168.0.32:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/warehouse_a1 \
  --port-no=5400 \
  --http-port-no=5402 \
  --group=Group1 \
  --alias=warehouse-a1 \
  --dbs-path=/data/machbase/warehouse_a1_dbs
```

Lookup 노드를 추가하거나 연결할 때는 `--node-type=lookup`과 `--lookup-type`을 함께 지정합니다.

예제:

```
machcoordinatoradmin \
  --add-node=192.168.0.32:5601 \
  --node-type=lookup \
  --lookup-type=master \
  --deployer=192.168.0.32:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/lookup1 \
  --alias=lookup-master-1
```

기존 노드를 클러스터 메타에 연결할 때는 `--attach-node`를 사용합니다. `--attach-node`도 `--alias`를 사용할 수 있지만 `--dbs-path`는 사용할 수 없습니다.

```
machcoordinatoradmin \
  --attach-node=192.168.0.32:5401 \
  --node-type=warehouse \
  --home-path=/home/machbase/warehouse_a1 \
  --port-no=5400 \
  --http-port-no=5402 \
  --group=Group1 \
  --alias=warehouse-a1
```

`--alias`는 `--add-node`와 `--attach-node`에서 지정할 수 있습니다. 지정하지 않으면 노드 유형에 따라 `coordinator-N`, `deployer-N`, `broker-N`, `warehouse-N`, `lookup-N` 형식으로 자동 생성됩니다.

Alias 이름은 1자 이상이어야 하며 영문자, 숫자, `-`, `_`, `.`만 사용할 수 있습니다. Alias는 클러스터 전체에서 유일해야 하고 실제 노드 이름과도 충돌하면 안 됩니다.

등록 후 alias만 변경하는 별도 명령은 없습니다.

명령 대상 노드는 실제 노드 이름을 먼저 찾고, 없으면 alias를 찾습니다. 따라서 `--startup-node`, `--shutdown-node`, `--kill-node`, `--remove-node`, `--detach-node`, `--upgrade-node`, `--set-lookup-master`, `--set-warehouse-state`, `--force-restore-warehouse`, `--snapshot-recover`, `--exec-sync`에서 alias를 사용할 수 있습니다. 상태 출력에서는 alias가 있으면 `alias(real-node-name)` 형식으로 표시될 수 있습니다.

`--dbs-path`는 `--add-node`로 Broker 또는 Warehouse를 추가할 때만 사용할 수 있습니다. Lookup, Coordinator, Deployer 노드에는 사용할 수 없고 `--attach-node`, `--upgrade-node` 같은 다른 명령과 함께 사용할 수도 없습니다.

`--dbs-path` 값은 `/` 또는 `?`로 시작해야 합니다. 줄바꿈, 탭, 끝 공백은 허용되지 않습니다. `/`, `/etc`, `/usr`, `/home`, `/bin`처럼 시스템 경로 자체를 직접 지정하는 값은 거부됩니다. `/home/machbase/warehouse_a1_dbs`처럼 시스템 경로 아래의 실제 데이터 디렉터리는 별도 디렉터리로 지정할 수 있습니다.

절대 경로를 custom `DBS_PATH`로 지정하면 노드 추가 시점에 해당 디렉터리가 존재하지 않아야 합니다. Deployer가 `machadmin -c` 실행 전에 디렉터리를 생성합니다. 이미 존재하면 `DBS_PATH already exists` 오류로 노드 추가가 실패합니다. `--dbs-path`를 생략하면 Broker/Warehouse 설정에는 기본값 `DBS_PATH = ?/dbs`가 기록됩니다. Broker/Warehouse를 `--remove-node`로 삭제할 때 명시적인 절대 경로 `DBS_PATH`는 노드 home 경로와 별도로 정리됩니다.


## 노드 정보 목록 출력

구문:

```
machcoordinatoradmin --list-node[=node]
```

예제:

```
mach@localhost:~$  machcoordinatoradmin --list-node
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node Name             : 192.168.0.32:5101
Node Type             : coordinator
HTTP Admin Port       : 5102
Group Name            : Coordinator
Desired State         : primary
Actual State          : primary
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497590
Last Modify Time      : 421020408
Last Response Elapsed : 1006148

Node Name             : 192.168.0.32:5201
Node Type             : deployer
Group Name            : Deployer
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497594
Last Modify Time      : 404915419
Last Response Elapsed : 1006128

Node Name             : 192.168.0.32:5301
Node Type             : broker
Port Number           : 5757
Http Port             : 5302
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/machbase/broker1
Group Name            : Broker
Desired State         : leader
Actual State          : leader
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497544
Last Modify Time      : 353606480
Last Response Elapsed : 1006157

Node Name             : 192.168.0.32:5401
Node Type             : warehouse
Port Number           : 5400
Http Port             : 5402
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/machbase/warehouse_a1
Group Name            : Group1
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497556
Last Modify Time      : 332480933
Last Response Elapsed : 1006160

mach@localhost:~$  machcoordinatoradmin --list-node=192.168.0.32:5401
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node Name             : 192.168.0.32:5401
Node Type             : warehouse
Port Number           : 5400
Http Port             : 5402
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/cumulus/warehouse_a1
Group Name            : Group1
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 648879
Last Modify Time      : 419153148
Last Response Elapsed : 1005962
```


## 클러스터 노드 상태 출력

예제:

```
mach@localhost:~$ machcoordinatoradmin --cluster-status
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary      |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal       |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader       |
| warehouse   | 192.168.0.32:5401 | Group1            | normal            | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+

mach@localhost:~$ machcoordinatoradmin --cluster-status-full
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+-------------------------------+-------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |    Desired & Actual State     |  RP State   |
+-------------+-------------------+-------------------+-------------------+-------------------------------+-------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary       | primary       | ----------- |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal        | normal        | ----------- |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader        | leader        | ----------- |
| warehouse   | 192.168.0.32:5401 | Group1            | normal            | normal        | normal        | ----------- |
+-------------+-------------------+-------------------+-------------------+-------------------------------
```


## 클러스터 정보 출력

예제:

```
mach@localhost:~$ machcoordinatoradmin --cluster-node
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Token Pid      : 29245
Token Time     : 1553153902646178
Modify Time    : 1553154010296715
Modify Count   : 8
Cluster Status : Service
Broker         : 192.168.0.32:5301
Warehouse      : 192.168.0.32:5401
```


## 그룹 상태 변경

구문:

```
machcoordinatoradmin --set-group-state=[ normal | readonly ] --group=group
```

예제:

```
mach@localhost:~$ machcoordinatoradmin --set-group-state=readonly --group=Group1
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Group Name: Group1
Flag      : 1

mach@localhost:~$ machcoordinatoradmin --cluster-status
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary      |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal       |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader       |
| warehouse   | 192.168.0.32:5401 | Group1            | readonly          | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+
```

## 호스트 리소스 출력

구문:

```
machcoordinatoradmin --host-resource-enable [--metric=metric] [host=host]
```

예제:

```
mach@localhost:~$ machcoordinatoradmin --host-resource-enable
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : HOST-RESOURCE
             Value : ON
            Format : text/plain

mach@localhost:~$ machcoordinatoradmin --get-host-resource
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.32
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 14.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 99.1%
      Virtual Memory Utilization  : 98.6%
   Network Info :
      Receive Bytes(per second)    : 42809
      Receive Packets(per second)  : 337
      Transmit Bytes(per second)   : 42885
      Transmit Packets(per second) : 332
   Disk Info :
      /dev/sda1 : 87.4%
         |-> 192.168.0.32:5101   /home/cumulus/coordinator1
         |-> 192.168.0.32:5301   /home/cumulus/broker1
         |-> 192.168.0.32:5401   /home/cumulus/warehouse_a1
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 2.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 46.9%
      Virtual Memory Utilization  : 22.8%
   Network Info :
      Receive Bytes(per second)    : 12336
      Receive Packets(per second)  : 103
      Transmit Bytes(per second)   : 13500
      Transmit Packets(per second) : 103
   Disk Info :
      /dev/sda1 : 64.2%
         |-> 192.168.0.33:5101   /home/cumulus/coordinator2
         |-> 192.168.0.33:5401   /home/cumulus/warehouse_a2

mach@localhost:~$ machcoordinatoradmin --get-host-resource --metric=cpu
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.32
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 13.9%
      CPU IOWait Ratio    : 0.0%
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 1.9%
      CPU IOWait Ratio    : 0.0%

mach@localhost:~$ machcoordinatoradmin --get-host-resource --host=192.168.0.33
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 2.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 46.9%
      Virtual Memory Utilization  : 22.8%
   Network Info :
      Receive Bytes(per second)    : 12588
      Receive Packets(per second)  : 106
      Transmit Bytes(per second)   : 13330
      Transmit Packets(per second) : 100
   Disk Info :
      /dev/sda1 : 64.2%
         |-> 192.168.0.33:5101   /home/cumulus/coordinator2
         |-> 192.168.0.33:5401   /home/cumulus/warehouse_a2

mach@localhost:~$ machcoordinatoradmin --host-resource-disable
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : HOST-RESOURCE
             Value : OFF
            Format : text/plain
```

## machdeployeradmin


Deployer의 상태를 확인하거나 Deployer의 시작/종료/중지 명령을 직접 실행할 수 있습니다.

일반적으로 명령을 실행하는 가장 빠른 방법은 machcoordinatoradmin을 통하는 것이지만, 불가능한 경우 다음을 수행해야 합니다.

클러스터 에디션 패키지에만 존재합니다.

## 옵션 및 기능

machdeployeradmin의 옵션은 다음과 같습니다. 이전 섹션에서 설명한 기능은 생략되었습니다.

```
mach@localhost:~$ machdeployeradmin -h
```


|옵션|설명|
|--|--|
|-u, --startup | Deployer 프로세스 실행|
|-s, --shutdown | Deployer 프로세스 종료|
|-k, --kill | Deployer 프로세스 중지|
|-c, --createdb | Deployer 메타 생성|
|-d, --destroydb | Deployer 메타 삭제|
|-i, --silent | 배너 출력 없이 실행|
|-e, --check | Deployer 프로세스 실행 여부 확인|


## 실행 상태 확인

예제:

```
mach@localhost:~$ machdeployeradmin -e
-------------------------------------------------------------------------
     Machbase Deployer Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Machbase Deployer is running with pid(29373)!
```
