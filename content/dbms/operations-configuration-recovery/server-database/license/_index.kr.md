---
type: docs
title: '13.1.3 라이선스 설치와 확인'
weight: 30
---

Machbase를 운영하려면 유효한 라이선스가 필요합니다. 라이선스는 파일 형태로 제공되며, 오프라인(서버 시작 전) 또는 온라인(서버 실행 중) 방식으로 설치할 수 있습니다.

## 라이선스 파일 위치

라이선스 파일은 다음 경로에 위치해야 합니다.

```
$MACHBASE_HOME/conf/license.dat
```

서버 시작 시 이 파일을 자동으로 읽습니다. 파일이 없거나 유효하지 않으면 서버가 시작되지 않거나 제한된 모드로 동작합니다.

## 오프라인 라이선스 설치 (machadmin)

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

## 온라인 라이선스 설치 (ALTER SYSTEM)

서버가 실행 중인 상태에서도 SQL 명령어로 라이선스를 갱신할 수 있습니다.

```sql
ALTER SYSTEM INSTALL LICENSE = '/path/to/new_license.dat';
```

서버 재시작 없이 즉시 적용됩니다. 새 라이선스 파일은 서버가 접근 가능한 경로에 있어야 합니다.

## 라이선스 정보 확인

### machadmin으로 확인

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

### SQL로 확인

서버 실행 중에는 시스템 뷰로 라이선스 정보를 조회할 수 있습니다.

```sql
SELECT * FROM v$license_info;
```

## 라이선스 만료 시 동작

라이선스가 만료되면 다음과 같이 동작합니다.

- 이미 연결된 세션은 유지되지만 새 연결이 제한될 수 있습니다.
- 데이터 쓰기(Append/Insert)가 거부되고 읽기 전용 모드로 전환될 수 있습니다.
- 트레이스 로그(`$MACHBASE_HOME/trc/machbase.trc`)에 라이선스 만료 경고가 기록됩니다.

라이선스 만료 전에 새 라이선스를 발급받아 `ALTER SYSTEM INSTALL LICENSE` 명령어로 무중단 갱신하는 것을 권장합니다.
