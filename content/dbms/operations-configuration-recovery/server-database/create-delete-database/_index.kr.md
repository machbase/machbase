---
type: docs
title: '데이터베이스 생성과 삭제'
weight: 20
---

Machbase에서 "데이터베이스"란 테이블, 인덱스, 내부 메타데이터를 담는 파일 집합을 의미합니다. 서버를 처음 설치한 뒤에는 반드시 데이터베이스를 생성해야 서버를 시작할 수 있습니다.

## 데이터베이스 생성

```bash
machadmin -c
```

`$MACHBASE_HOME/dbs/` 디렉터리 아래에 초기 데이터베이스 파일을 생성합니다. 이미 데이터베이스가 존재하면 오류가 발생합니다.

```
mach@localhost:~$ machadmin -c
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.6.0
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Database created successfully.
```

데이터베이스 생성이 완료되면 `machadmin -u`로 서버를 시작할 수 있습니다.

## 데이터 디렉터리 구조

데이터베이스 생성 후 `$MACHBASE_HOME` 아래에 다음과 같은 디렉터리가 구성됩니다.

```
$MACHBASE_HOME/
├── bin/          # machadmin, machsql 등 실행 파일
├── conf/         # machbase.conf, license.dat 등 설정 파일
├── dbs/          # 데이터베이스 파일 (테이블, 인덱스, 메타데이터)
├── trc/          # 트레이스 로그 (machbase.trc 등)
└── lib/          # 공유 라이브러리
```

`DBS_PATH` 프로퍼티(기본값: `?/dbs`)를 변경하면 데이터 저장 경로를 별도 디스크나 볼륨으로 지정할 수 있습니다. 변경 후에는 서버 재시작이 필요합니다.

## 데이터베이스 삭제

```bash
machadmin -d
```

데이터베이스를 영구적으로 삭제합니다. 삭제 전에 확인 메시지가 표시되며, `y`를 입력해야 실행됩니다.

```
mach@localhost:~$ machadmin -d
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.6.0
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Destroy Machbase database- Are you sure?(y/N) y
Database destroyed successfully.
```

> **주의**: 데이터베이스 삭제는 되돌릴 수 없습니다. `dbs/` 디렉터리 내의 모든 데이터가 영구적으로 삭제됩니다. 삭제 전에 반드시 백업을 수행하거나, 데이터 보존이 필요 없는 환경인지 확인하십시오.

삭제 작업은 서버가 실행 중이지 않은 상태에서 수행해야 합니다. 서버가 실행 중이라면 먼저 `machadmin -s`로 종료한 뒤 삭제합니다.

## 데이터베이스 초기화 절차

기존 데이터를 모두 제거하고 새로 시작하려면 다음 순서로 진행합니다.

```bash
# 1. 서버 종료
machadmin -s

# 2. 데이터베이스 삭제
machadmin -d

# 3. 데이터베이스 재생성
machadmin -c

# 4. 서버 시작
machadmin -u
```
