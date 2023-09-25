---
title : 'machdeployeradmin'
type : docs
weight: 60
---

Deployer의 상태를 확인하거나, Deployer의 구동/종료/중단 명령을 직접 내릴 수 있다.

보통은 machcoordinatoradmin 을 통해서 내리는 편이 가장 빠르지만, 불가능한 경우에는 아래와 같이 수행해야 한다.

Cluster Edition 패키지에만 존재한다.

## 옵션 및 기능
machdeployeradmin의 옵션은 아래와 같다.  앞의 설치 절에서 설명한 기능은 생략한다.

```
mach@localhost:~$ machdeployeradmin -h
```

| 옵션               | 설명                      |
| ---------------- | ----------------------- |
| \-u, --startup   | Deployer 프로세스 구동        |
| \-s, --shutdown  | Deployer 프로세스 종료        |
| \-k, --kill      | Deployer 프로세스 중단        |
| \-c, --createdb  | Deployer 메타 생성          |
| \-d, --destroydb | Deployer 메타 삭제          |
| \-i, --silence   | 출력 없이 실행                |
| \-e, --check     | Deployer 프로세스가 작동중인지 확인 |

## 동작 여부 확인

**Example:**

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
