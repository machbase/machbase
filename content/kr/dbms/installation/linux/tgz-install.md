---
type: docs
title : 'Tarball 설치'
type : docs
weight: 20
---

## 사용자 생성

Machbase를 설치하고 사용하기 위해 리눅스 사용자 `machbase`를 생성합니다.

```bash
sudo useradd machbase
```

비밀번호를 설정한 뒤 `machbase` 계정으로 로그인합니다.

## 패키지 설치

`machbase_home` 디렉터리를 만든 후 Machbase 다운로드 사이트에서 패키지를 내려받아 설치합니다.

```bash
[machbase@localhost ~]$ wget http://machbase.com/dist/machbase-fog-x.x.x.official-LINUX-X86-64-release.tgz
[machbase@localhost ~]$ mkdir machbase_home
[machbase@localhost ~]$ mv machbase-fog-x.x.x.official-LINUX-X86-64-release.tgz machbase_home/
[machbase@localhost ~]$ cd machbase_home/
[machbase@localhost machbase_home]$ tar zxf machbase-fog-x.x.x.official-LINUX-X86-64-release.tgz

[machbase@loclahost machbase_home]$ ls -l
drwxrwxr-x  5 machbase machbase        64 Oct 30 16:10 3rd-party
drwxrwxr-x  2 machbase machbase      4096 Oct 30 16:10 bin
drwxrwxr-x  2 machbase machbase       306 Jan  2 11:36 conf
drwxrwxr-x  2 machbase machbase       136 Jan  2 11:37 dbs
drwxrwxr-x  3 machbase machbase        22 Oct 30 16:10 doc
drwxrwxr-x  2 machbase machbase        96 Oct 30 16:10 include
drwxrwxr-x  2 machbase machbase        29 Oct 30 16:10 install
drwxrwxr-x  2 machbase machbase       283 Oct 30 16:10 lib
-rw-rw-r--  1 machbase machbase 139888377 Dec 20 11:33 machbase-fog-x.x.x.official-LINUX-X86-64-release.tgz
drwxrwxr-x  2 machbase machbase        22 Dec 21 15:43 msg

drwxrwxr-x  2 machbase machbase         6 Oct 30 16:10 package
drwxrwxr-x 12 machbase machbase       140 Oct 30 16:10 sample
drwxrwxr-x  2 machbase machbase      4096 Jan  2 09:37 trc
drwxrwxr-x 10 machbase machbase       160 Oct 30 16:10 tutorials
drwxrwxr-x  3 machbase machbase        19 Oct 30 16:10 webadmin

[machbase@loclahost machbase_home]$
```

설치된 디렉터리의 용도는 다음과 같습니다.

|디렉터리|설명|
|--|--|
|bin|실행 파일|
|conf|설정 파일|
|dbs|데이터 저장 공간|
|doc|라이선스 파일|
|include|CLI 프로그램용 헤더 파일|
|install|Makefile 용 mk 파일|
|lib|각종 라이브러리|
|msg|Machbase 서버 오류 메시지|
|package|추가 패키지 저장 경로(클러스터 에디션)|
|sample|다양한 예제 파일|
|trc|Machbase 서버 로그와 추적 정보|
|webadmin|MWA 웹 서버 파일|
|3rd-party|Grafana 플러그인 파일|

## 환경 변수 설정

`.bashrc`에 Machbase 관련 환경 변수를 추가합니다.

```bash

export MACHBASE_HOME=/home/machbase/machbase_home
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH

# 아래 명령으로 변경 사항을 적용합니다.
source .bashrc
```

## Machbase 속성 설정

`$MACHBASE_HOME/conf` 디렉터리에는 `machbase.conf.sample` 파일이 포함되어 있습니다.

```bash

[machbase@localhost ~]$ cd $MACHBASE_HOME/conf
[machbase@localhost conf]$ ls -l
-rw-rw-r-- 1 machbase machbase   106 Oct 30 16:10 machtag.sql.sample
-rw-rw-r-- 1 machbase machbase 17556 Oct 30 16:10 machbase.conf.sample

[machbase@localhost conf]$
```

Machbase 접속 포트 번호는 리눅스 환경 변수를 통해 변경할 수도 있습니다. 아래는 기본값(5656) 대신 7878 포트를 사용하도록 변경하는 예시입니다.

```bash
export MACHBASE_PORT_NO=7878
```

## Machbase 간단 사용법

### 데이터베이스 생성

데이터베이스 생성에는 `machadmin` 유틸리티를 사용합니다. `--help` 옵션으로 지원 명령을 확인할 수 있습니다.

```bash
[machbase@localhost machbase_home]$ machadmin --help
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.official
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
<< available option lists >>
  -u, --startup                         Startup Machbase server.
      --recovery[=simple,complex,reset] Recovery mode. (default: simple)
  -s, --shutdown                        Shutdown Machbase server.
  -c, --createdb                        Create Machbase database.
  -d, --destroydb                       Destroy Machbase database.
  -k, --kill                            Terminate Machbase server.
  -i, --silence                         Produce less output.
  -r, --restore                         Restore Machbase database.
  -x, --extract                         Extract BackupFile to BackupDirectory.
  -w, --viewimage                       Display information of BackupImageFile.
  -e, --check                           Check whether Machbase Server is running.
  -t, --licinstall                      Install the license file.
  -f, --licinfo                         Display information of installed license file.

[machbase@localhost machbase_home]$
```

`-c` 옵션으로 데이터베이스를 생성합니다.

```bash

[machbase@localhost machbase_home]$ machadmin -c
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.official
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Database created successfully.
[machbase@localhost machbase_home]$
```

### Machbase 서버 구동

`-u` 옵션으로 Machbase 서버를 구동합니다.

```bash

[machbase@localhost machbase_home]$ machadmin -u
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.official
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for Machbase server start.
Machbase server started successfully.
[machbase@localhost machbase_home]$
```

아래와 같이 `ps` 명령을 사용하면 서버 데몬 `machbased` 가 실행 중임을 확인할 수 있습니다.

```bash
[machbase@localhost machbase_home]$  ps -ef |grep machbased
machbase 11178     1  2 11:25 ?        00:00:01 /home/machbase/machbase_home/bin/machbased -s --recovery=simple
machbase 11276  9867  0 11:26 pts/1    00:00:00 grep --color=auto machbased
[machbase@localhost machbase_home]$
```

### Machbase 서버 접속

`machsql` 이라는 접속 유틸리티로 Machbase 서버에 연결합니다.

관리자 계정 `SYS` 가 기본 제공되며 비밀번호는 `MANAGER` 로 설정되어 있습니다.

```bash
[machbase@localhost machbase_home]$  machsql
=================================================================
     Machbase Client Query Utility
     Release Version x.x.x.official
     Copyright 2014 MACHBASE Corporation or its subsidiaries.
     All Rights Reserved.
=================================================================
Machbase server address (Default:127.0.0.1) :
Machbase user ID  (Default:SYS)
Machbase User Password :
MACHBASE_CONNECT_MODE=INET, PORT=5656
Type 'help' to display a list of available commands.
Mach>
```

간단한 테이블을 만들고 데이터를 입력·조회해 보겠습니다.

```sql
create table hello( id integer );
insert into hello values( 1 );
insert into hello values( 2 );
select * from hello;
select _arrival_time, * from hello;
```

```sql
Mach> create table hello( id integer );
Created successfully.
Elapsed time: 0.054
Mach> insert into hello values( 1 );
1 row(s) inserted.
Elapsed time: 0.000
Mach> insert into hello values( 2 );
1 row(s) inserted.
Elapsed time: 0.000
Mach> select * from hello;
ID
--------------
2
1
[2] row(s) selected.
Elapsed time: 0.000
Mach> select _arrival_time, * from hello;
_arrival_time                   ID
-----------------------------------------------
2019-01-02 11:33:00 122:806:804 2
2019-01-02 11:32:57 383:848:361 1
[2] row(s) selected.
Elapsed time: 0.000
Mach>
```

SELECT 결과에서 가장 최근에 입력된 데이터가 먼저 출력되는 것을 확인할 수 있습니다. 또한 `_arrival_time` 컬럼을 통해 각 행의 입력 시간이 나노초 단위로 기록됨을 알 수 있습니다.

### Machbase 서버 중지

`-s` 옵션으로 Machbase 서버를 종료합니다.

```bash
[machbase@localhost machbase_home]$ machadmin -s
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.official
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for Machbase server shut down...
Machbase server shut down successfully.
[machbase@localhost machbase_home]$
```

### 데이터베이스 삭제

`-d` 옵션으로 데이터베이스를 삭제합니다.  
**모든 데이터가 삭제되므로 각별히 주의하십시오.**

```bash
[machbase@localhost machbase_home]$ machadmin -d
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.official
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Destroy Machbase database. Are you sure?(y/N) y
Database destoryed successfully.
[machbase@localhost machbase_home]$
```
