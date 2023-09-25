---
title : machadmin
type : docs
weight: 20
---

마크베이스 서버를 시작, 종료하거나 생성, 삭제 및 실행 상태를 체크하기 위해서는 machadmin을 사용한다.

## 옵션 및 기능

machadmin의 옵션은 아래와 같다.  앞의 설치 절에서 설명한 기능은 생략한다.

```bash
mach@localhost:~$ machadmin -h
```

| 옵션                                             | 설명                                           |
|--------------------------------------------------|------------------------------------------------|
| -u, --startup/ --recovery[=simple,complex,reset] | 마크베이스 서버 시작/ 복구 mode (기본: simple) |
| -s, --shutdown                                   | 마크베이스 서버 정상 종료                      |
| -c, --createdb                                   | 마크베이스 데이터베이스 생성                   |
| -d, --destroydb                                  | 마크베이스 데이터베이스 삭제                   |
| -k, --kill                                       | 마크베이스 서버 강제 종료                      |
| -i, --silence                                    | 출력 없이 실행                                 |
| -r, --restore                                    | 백업에서 데이터베이스 복구                     |
| -x, --extract                                    | 백업 파일을 백업 디렉터리로 변환               |
| -e, --check                                      | 마크베이스 서버 실행 체크                      |
| -t, --licinstall                                 | 라이선스 파일 설치                             |
| -f, --licinfo                                    | 설치된 라이선스 정보 출력                      |

## 복구 모드

**Syntax:**

```bash
machadmin -u --recovery=[simple | complex | reset]
```

복구 모드는 다음과 같다.

* simple: 서버가 동작중일때 전원이 끊어지는 문제가 발생하지 않았다면, simple recovery 모드가 기본 실행된다. 
* complex: complex recovery 모드는 simple 모드에 비해서 실행시간이 더 오래 걸린다. 전원이 끊어진 이후 재시작시에 기본으로 실행된다.
* reset: simple 혹은 complex 모드로 복구가 수행되지 않을 때, 모든 테이블의 모든 데이터를 검사하여 데이터베이스를 복구한다. 이 경우, 데이터의 일부 유실이 발생할 수 있다.

## 서버 정상 종료

**Example:**

```bash
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

**Example:**

```bash
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

**Syntax:**

```bash
machadmin -k
```

**Example:**

```bash
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

## 침묵 모드 실행

machadmin 실행시 출력되는 메시지를 없앤다.

**Syntax:**

```bash
machadmin -i
```

## 데이터베이스 복구

**Syntax:**

```bash
machadmin -r backup_database_path
```

**Example:**

```bash
mach@localhost:~$ machadmin -r 'backup'
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 5.1.9.community
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Backed up database restored successfully.
```

## 서버 실행 유무 확인

**Syntax:**

```bash
machadmin -e
```

서버가 실행중이지 않을 때의 출력 예

```bash
mach@localhost:~$ machadmin -e
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 5.1.9.community
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
[ERR] Server is not running.
```

서버가 실행중일 때의 출력 예

```bash
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

**Syntax:**

```bash
machadmin -t license_file
```

**Example:**

```bash
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

**Example:**

```bash
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
