---
type: docs
title : machadmin
type : docs
weight: 20
---

machadmin은 Machbase 서버를 시작하거나 종료하고, 데이터베이스의 생성, 삭제 및 실행 상태를 확인하는 데 사용됩니다.

## 옵션 및 기능

machadmin의 옵션은 다음과 같습니다. 이전 설치 섹션에서 설명한 기능은 생략되었습니다.

```bash
mach@localhost:~$ machadmin -h
```

| 옵션 | 설명 |
|--|--|
|-u, --startup/ --recovery[=simple,complex,reset]|Machbase 서버 시작/복구 모드 (기본값: simple)
|-s, --shutdown | |Machbase 서버 정상 종료 |
|-c, --createdb |Machbase 데이터베이스 생성 |
| -d, --destroydb| Machbase 데이터베이스 삭제 |
| -k, --kill| Machbase 서버 강제 종료 |
| -i, --silence| 출력 없이 실행 |
| -r, --restore |백업으로부터 데이터베이스 복구
| -x, --extract| 백업 파일을 백업 디렉토리로 변환 |
|-e, --check| Machbase 서버 실행 상태 확인 |
|-t, --licinstall| 라이선스 파일 설치 |
|-f, --licinfo| 설치된 라이선스 정보 출력|

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
     Release Version - 5.1.9.community
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
     Release Version - 5.1.9.community
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
     Release Version - 5.1.9.community
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
     Release Version - 5.1.9.community
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
     Release Version - 5.1.9.community
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
     Release Version - 5.1.9.community
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
     Release Version - 5.1.9.community
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
     Release Version - 5.1.9.community
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
     Release Version - 5.1.9.community
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
                   INFORMATION
Install Date                      : 2018-12-20 11:34:43
Company#ID-ProjectName            : machbase
License Policy                    : CORE
License Type(Version 2)           : OFFICIAL
Host ID                           : FFFFFFFFFFFFFFF
Issue Date                        : 2013-03-25
Expiry Date                       : 2037-03-18
Max Data Size For a Day(GB)       : 0
Percentage Of Data Addendum(%)    : 0
Overflow Action                   : 0
Overflow Count to Stop Per Month  : 0
Stop Action                       : 0
Reset Flag                        : 0
-----------------------------------------------------------------
                   STATUS
Usage Of Data(GB)                 : 0.000000
Previous Checked Date             : 2018-12-22
Violation Count                   : 0
Stop Enabled                      : 0
-----------------------------------------------------------------
License information displayed successfully.
```
