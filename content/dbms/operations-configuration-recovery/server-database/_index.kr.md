---
type: docs
title: '13.1 서버와 데이터베이스 운영'
weight: 10
---
이 섹션에서는 Machbase 서버 프로세스와 데이터베이스를 관리하는 기본 운영 작업을 설명합니다.

`machadmin`은 Machbase의 핵심 관리 도구입니다. 서버 시작·종료, 데이터베이스 생성·삭제, 라이선스 설치, 실행 상태 확인 등 대부분의 운영 작업을 이 명령어 하나로 수행합니다. `machadmin`은 `$MACHBASE_HOME/bin/` 디렉터리에 위치합니다.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [서버 시작과 종료](/dbms/operations-configuration-recovery/server-database/#start-server) | `machadmin -u`, `-s`, `-k`, `-e` 명령어 사용법과 시작 실패 대처 |
| [데이터베이스 생성과 삭제](/dbms/operations-configuration-recovery/server-database/#create-delete-database) | DB 초기화, 디렉터리 구조, 안전한 삭제 절차 |
| [라이선스 설치와 확인](/dbms/operations-configuration-recovery/server-database/#license) | 라이선스 파일 위치, 온라인 설치, 만료 시 동작 |

## machadmin 주요 옵션 요약

| 옵션 | 기능 |
|------|------|
| `-u` / `--startup` | 서버 시작 |
| `-s` / `--shutdown` | 서버 정상 종료 |
| `-k` / `--kill` | 서버 강제 종료 |
| `-e` / `--check` | 서버 실행 상태 확인 |
| `-c` / `--createdb` | 데이터베이스 생성 |
| `-d` / `--destroydb` | 데이터베이스 삭제 |
| `-t` / `--licinstall` | 라이선스 파일 설치 |
| `-f` / `--licinfo` | 설치된 라이선스 정보 확인 |
| `-r` / `--restore` | 백업으로부터 데이터베이스 복구 |


<a id="start-server"></a>

## 서버 시작과 종료

Machbase 서버는 `$MACHBASE_HOME/bin/machadmin` 명령어로 시작하고 종료합니다. 각 명령어는 서버 프로세스(`machbased`)에 신호를 보내거나 직접 프로세스를 기동합니다.

### 서버 시작

```bash
machadmin -u
```

서버를 시작합니다. 데이터베이스가 정상적으로 종료된 경우 simple 복구 모드로 시작하고, 비정상 종료(전원 차단 등) 이후에는 자동으로 complex 복구 모드를 적용합니다.

```
mach@localhost:~$ machadmin -u
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.6.0
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Machbase server started successfully.
```

#### 복구 모드를 지정하여 시작

비정상 종료 이후 복구 방식을 직접 지정할 수 있습니다.

```bash
machadmin -u --recovery=simple    # 기본값: 정상 종료 후 재시작 시 사용
machadmin -u --recovery=complex   # 비정상 종료 후 재시작 시 사용 (시간이 더 소요됨)
machadmin -u --recovery=reset     # simple·complex로 복구 불가 시 사용 (일부 데이터 손실 가능)
```

| 모드 | 설명 |
|------|------|
| `simple` | 정상 종료 후 재시작 시 적용되는 기본 모드 |
| `complex` | 전원 차단 등 비정상 종료 후 재시작 시 적용. simple보다 시간이 더 소요됨 |
| `reset` | simple·complex 모드로 복구되지 않을 때 사용. 모든 테이블 데이터를 검사하며 일부 데이터 손실 가능 |

### 서버 정상 종료

```bash
machadmin -s
```

현재 처리 중인 트랜잭션을 완료한 뒤 서버를 종료합니다(graceful shutdown). 데이터 일관성이 보장되므로 가능한 한 이 방법을 사용합니다.

```
mach@localhost:~$ machadmin -s
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.6.0
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for the server shut down...
Server shut down successfully.
```

### 서버 강제 종료

```bash
machadmin -k
```

서버 프로세스를 즉시 종료합니다. 진행 중인 트랜잭션이 중단되므로, 다음 시작 시 complex 복구 모드가 적용될 수 있습니다. 정상 종료(`-s`)가 응답하지 않을 때만 사용합니다.

```
mach@localhost:~$ machadmin -k
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.6.0
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for Machbase terminated...
Server terminated successfully.
```

### 서버 실행 상태 확인

```bash
machadmin -e
```

서버가 현재 실행 중인지 확인합니다.

서버가 실행 중이 아닌 경우:

```
mach@localhost:~$ machadmin -e
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.6.0
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
[Error] Machbase server is not running.
```

서버가 실행 중인 경우:

```
mach@localhost:~$ machadmin -e
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.6.0
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Machbase server is running with PID(14098).
```

### 시작 실패 시 확인 사항

서버가 시작되지 않을 때는 다음 항목을 순서대로 점검합니다.

#### 1. 포트 충돌 확인

기본 포트(5656)가 이미 사용 중인지 확인합니다.

```bash
ss -tlnp | grep 5656
```

포트가 점유되어 있다면 해당 프로세스를 종료하거나 `machbase.conf`에서 `PORT_NO` 값을 변경합니다.

#### 2. 라이선스 확인

라이선스 파일이 없거나 만료된 경우 서버가 시작되지 않을 수 있습니다.

```bash
ls -l $MACHBASE_HOME/conf/license.dat
machadmin -f
```

#### 3. 데이터베이스 존재 여부 확인

데이터베이스가 생성되지 않은 경우 서버를 시작할 수 없습니다. 먼저 `machadmin -c`로 데이터베이스를 생성합니다.

```bash
ls $MACHBASE_HOME/dbs/
```

#### 4. 트레이스 로그 확인

서버 로그에서 오류 원인을 확인합니다.

```bash
tail -100 $MACHBASE_HOME/trc/machbase.trc
```

로그 파일에서 `[ERR]` 또는 `FATAL` 키워드를 찾아 원인을 파악합니다.

<a id="create-delete-database"></a>

## 데이터베이스 생성과 삭제

Machbase에서 "데이터베이스"란 테이블, 인덱스, 내부 메타데이터를 담는 파일 집합을 의미합니다. 서버를 처음 설치한 뒤에는 반드시 데이터베이스를 생성해야 서버를 시작할 수 있습니다.

### 데이터베이스 생성

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

### 데이터 디렉터리 구조

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

### 데이터베이스 삭제

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

### 데이터베이스 초기화 절차

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

<a id="license"></a>

## 라이선스 설치와 확인

Machbase를 운영하려면 유효한 라이선스가 필요합니다. 라이선스는 파일 형태로 제공되며, 오프라인(서버 시작 전) 또는 온라인(서버 실행 중) 방식으로 설치할 수 있습니다.

### 라이선스 파일 위치

라이선스 파일은 다음 경로에 위치해야 합니다.

```
$MACHBASE_HOME/conf/license.dat
```

서버 시작 시 이 파일을 자동으로 읽습니다. 파일이 없거나 유효하지 않으면 서버가 시작되지 않거나 제한된 모드로 동작합니다.

### 오프라인 라이선스 설치 (machadmin)

서버가 실행 중이지 않은 상태에서 `machadmin -t` 옵션으로 라이선스를 설치합니다.

```bash
machadmin -t /path/to/license.dat
```

```
mach@localhost:~$ machadmin -t license.dat
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.6.0
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
License installed successfully.
```

설치가 완료되면 라이선스 파일이 `$MACHBASE_HOME/conf/license.dat`로 복사됩니다.

### 온라인 라이선스 설치 (ALTER SYSTEM)

서버가 실행 중인 상태에서도 SQL 명령어로 라이선스를 갱신할 수 있습니다.

```sql
ALTER SYSTEM INSTALL LICENSE = '/path/to/new_license.dat';
```

서버 재시작 없이 즉시 적용됩니다. 새 라이선스 파일은 서버가 접근 가능한 경로에 있어야 합니다.

### 라이선스 정보 확인

#### machadmin으로 확인

```bash
machadmin -f
```

```
mach@localhost:~$ machadmin -f
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.6.0
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
```

#### SQL로 확인

서버 실행 중에는 시스템 뷰로 라이선스 정보를 조회할 수 있습니다.

```sql
SELECT * FROM v$license_info;
```

### 라이선스 만료 시 동작

라이선스가 만료되면 다음과 같이 동작합니다.

- 이미 연결된 세션은 유지되지만 새 연결이 제한될 수 있습니다.
- 데이터 쓰기(Append/Insert)가 거부되고 읽기 전용 모드로 전환될 수 있습니다.
- 트레이스 로그(`$MACHBASE_HOME/trc/machbase.trc`)에 라이선스 만료 경고가 기록됩니다.

라이선스 만료 전에 새 라이선스를 발급받아 `ALTER SYSTEM INSTALL LICENSE` 명령어로 무중단 갱신하는 것을 권장합니다.
