---
type: docs
title: '13.4.1.2 서버 로그'
weight: 20
---

Machbase 서버의 메인 로그 파일은 `$MACHBASE_HOME/trc/machbase.trc`입니다. 서버 시작/종료, 오류, 경고, 백업/복구 등 서버 동작 전반이 기록됩니다.

## 로그 파일 위치

```
$MACHBASE_HOME/trc/machbase.trc
```

날짜가 바뀌면 이전 로그 파일은 날짜가 포함된 이름으로 보존됩니다.

```
$MACHBASE_HOME/trc/machbase.trc           # 현재 로그
$MACHBASE_HOME/trc/machbase.trc.20240115  # 롤오버된 이전 로그
```

## 로그 형식

각 로그 라인은 다음 형식을 따릅니다.

```
[YYYY-MM-DD HH:MM:SS.mmm] [레벨] [모듈] 메시지
```

예시:

```
[2024-01-15 09:00:01.123] [INFO] [SERVER] Machbase server started. Version=8.6.0
[2024-01-15 09:00:01.450] [INFO] [STORAGE] Checkpoint completed. elapsed=1230ms
[2024-01-15 10:45:22.001] [ERROR] [NETWORK] Connection refused. client=192.168.1.100
[2024-01-15 11:30:55.321] [WARN] [STORAGE] Disk usage reached 85%. used_ratio=85, ratio_cap=95
```

## 로그 레벨 설정

로그 상세 수준은 `TRACE_LOG_LEVEL`로 조정합니다. 자세한 내용은 [Trace Log 설정](../configuration-trace-log/)을 참조하십시오.

## 주요 오류 패턴과 분석

### 연결 오류 패턴

클라이언트가 연결하지 못하거나 갑자기 연결이 끊어지는 경우 아래 패턴을 확인합니다.

```
[ERROR] [NETWORK] Connection refused. client=<IP>
[ERROR] [NETWORK] Session disconnected unexpectedly. session_id=<ID>
[ERROR] [NETWORK] Max session count reached. max=<N>
```

**조치**: `MAX_SESSION_COUNT` 파라미터 확인, 비정상 세션 정리(`ALTER SYSTEM KILL SESSION`), 네트워크 방화벽 규칙 점검.

### 디스크 풀 패턴

디스크 여유 공간이 부족하면 다음 패턴이 나타납니다.

```
[WARN]  [STORAGE] Disk usage reached 85%. used_ratio=85, ratio_cap=95
[ERROR] [STORAGE] Disk full. Data append suspended. path=/machbase/dbs
[ERROR] [STORAGE] Failed to write data file. errno=28 (No space left on device)
```

**조치**: 불필요한 파일 제거, 오래된 데이터 Retention Policy 적용, 디스크 확장.

### 메모리 부족 (OOM) 패턴

```
[ERROR] [MEMORY] Memory allocation failed. requested=<SIZE>bytes
[ERROR] [QUERY]  Query aborted due to memory limit. sess_id=<ID>
```

**조치**: `MAX_QPX_MEM` 파라미터 확인, 불필요한 세션 종료, 시스템 메모리 여유 확보.

### 체크포인트 및 백업 로그

```
[INFO] [STORAGE] Checkpoint started.
[INFO] [STORAGE] Checkpoint completed. elapsed=2340ms
[INFO] [BACKUP]  Backup started. path=/backup/20240115
[INFO] [BACKUP]  Backup completed. elapsed=125s, size=2.3GB
```

체크포인트가 과도하게 오래 걸리면 (`elapsed` 값이 수십 초 이상) 디스크 I/O 부하를 점검합니다.

### 서버 시작/종료 로그

```
[INFO] [SERVER] Machbase server starting. version=8.6.0, pid=12345
[INFO] [SERVER] Storage recovery started.
[INFO] [SERVER] Storage recovery completed.
[INFO] [SERVER] Machbase server started. port=5656
[INFO] [SERVER] Machbase server shutting down. reason=SIGTERM
[INFO] [SERVER] Machbase server stopped.
```

비정상 종료 시에는 `SIGKILL` 또는 `Killed`가 함께 기록됩니다. `/var/log/syslog`에서 OOM Killer 동작 여부도 함께 확인합니다.

## 로그 파일 검색

```bash
# 오늘 발생한 ERROR 로그 확인
grep '\[ERROR\]' $MACHBASE_HOME/trc/machbase.trc

# 특정 날짜 범위에서 스토리지 관련 경고 확인
grep '2024-01-15.*STORAGE' $MACHBASE_HOME/trc/machbase.trc

# 최근 100줄 실시간 모니터링
tail -f -n 100 $MACHBASE_HOME/trc/machbase.trc
```

## 로그 파일 관리

로그 파일이 누적되면 디스크 공간을 소비합니다. 오래된 로그 파일은 주기적으로 압축하거나 삭제하십시오.

```bash
# 30일 이상 된 로그 파일 목록 확인
find $MACHBASE_HOME/trc/ -name "machbase.trc.*" -mtime +30

# 30일 이상 된 로그 파일 삭제
find $MACHBASE_HOME/trc/ -name "machbase.trc.*" -mtime +30 -delete
```
