---
type: docs
title : 'machdeployeradmin'
type : docs
weight: 60
---

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
|-i, --silence | 출력 없이 실행|
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
