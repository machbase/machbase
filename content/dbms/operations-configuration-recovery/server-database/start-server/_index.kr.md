---
type: docs
title: '서버 시작과 종료'
weight: 10
---

Machbase 서버는 `$MACHBASE_HOME/bin/machadmin` 명령어로 시작하고 종료합니다. 각 명령어는 서버 프로세스(`machbased`)에 신호를 보내거나 직접 프로세스를 기동합니다.

## 서버 시작

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

### 복구 모드를 지정하여 시작

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

## 서버 정상 종료

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

## 서버 강제 종료

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

## 서버 실행 상태 확인

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

## 시작 실패 시 확인 사항

서버가 시작되지 않을 때는 다음 항목을 순서대로 점검합니다.

### 1. 포트 충돌 확인

기본 포트(5656)가 이미 사용 중인지 확인합니다.

```bash
ss -tlnp | grep 5656
```

포트가 점유되어 있다면 해당 프로세스를 종료하거나 `machbase.conf`에서 `PORT_NO` 값을 변경합니다.

### 2. 라이선스 확인

라이선스 파일이 없거나 만료된 경우 서버가 시작되지 않을 수 있습니다.

```bash
ls -l $MACHBASE_HOME/conf/license.dat
machadmin -f
```

### 3. 데이터베이스 존재 여부 확인

데이터베이스가 생성되지 않은 경우 서버를 시작할 수 없습니다. 먼저 `machadmin -c`로 데이터베이스를 생성합니다.

```bash
ls $MACHBASE_HOME/dbs/
```

### 4. 트레이스 로그 확인

서버 로그에서 오류 원인을 확인합니다.

```bash
tail -100 $MACHBASE_HOME/trc/machbase.trc
```

로그 파일에서 `[ERR]` 또는 `FATAL` 키워드를 찾아 원인을 파악합니다.
