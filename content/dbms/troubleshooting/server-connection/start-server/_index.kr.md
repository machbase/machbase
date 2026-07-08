---
type: docs
title: '서버가 시작되지 않을 때'
weight: 10
---

`machadmin -s` 실행 후 서버가 정상적으로 시작되지 않는 경우, 아래 체크리스트를 순서대로 확인합니다.

## 로그에서 원인 먼저 확인

서버 시작 실패의 원인은 항상 로그 파일에 기록됩니다. 다른 항목을 확인하기 전에 로그 맨 끝을 먼저 확인합니다.

```bash
tail -50 $MACHBASE_HOME/trc/machbase.trc
```

## 원인별 체크리스트

### 1. 포트 충돌

다른 프로세스가 동일한 포트(기본값: 5656)를 사용 중이면 서버가 시작되지 않습니다.

```bash
# 5656 포트 사용 중인 프로세스 확인
netstat -tlnp | grep 5656

# 사용 중인 프로세스 PID 조회
lsof -i :5656
```

포트 충돌이 확인되면 충돌하는 프로세스를 종료하거나, `machbase.conf`의 `PORT_NO`를 다른 값으로 변경합니다.

### 2. 데이터 디렉터리 권한 문제

Machbase 프로세스가 데이터 디렉터리에 접근할 권한이 없으면 시작할 수 없습니다.

```bash
# 데이터 디렉터리 권한 확인
ls -la $MACHBASE_HOME/dbs/

# Machbase 실행 사용자 확인
whoami
```

디렉터리 소유자와 Machbase를 실행하는 사용자가 일치하는지 확인합니다. 불일치하면 소유권을 변경합니다.

```bash
chown -R machbase:machbase $MACHBASE_HOME/dbs/
```

### 3. 라이선스 만료 또는 파일 없음

라이선스가 만료되었거나 라이선스 파일이 없으면 서버가 시작되지 않습니다.

```bash
# 라이선스 파일 존재 여부 확인
ls -la $MACHBASE_HOME/conf/license.dat

# 라이선스 정보 확인 (서버 실행 중이면)
machadmin -L
```

라이선스 파일이 없거나 만료된 경우 Machbase 영업팀에 새 라이선스를 요청합니다.

### 4. 디스크 공간 부족

데이터 디렉터리가 있는 파티션의 디스크 공간이 부족하면 서버가 시작되지 않을 수 있습니다.

```bash
# 전체 디스크 사용량 확인
df -h

# Machbase 데이터 디렉터리 크기 확인
du -sh $MACHBASE_HOME/dbs/
```

디스크 공간이 부족하면 불필요한 데이터나 오래된 로그 파일을 삭제합니다.

### 5. 이전 프로세스 잔존

비정상 종료 후 이전 프로세스가 남아있으면 새 프로세스가 시작되지 않을 수 있습니다.

```bash
# Machbase 관련 프로세스 확인
ps aux | grep machbase
```

잔존 프로세스가 있으면 강제 종료합니다.

```bash
machadmin -k
```

강제 종료 후에도 프로세스가 남아있으면 직접 종료합니다.

```bash
kill -9 <PID>
```

## 강제 정리 후 재시작

위 확인을 마친 후 아래 순서로 재시작합니다.

```bash
# 1. 기존 프로세스 강제 종료
machadmin -k

# 2. 잠깐 대기 후 재시작
machadmin -s

# 3. 시작 확인
machadmin -c
```

{{< callout type="warning" >}}
`machadmin -k`는 강제 종료입니다. 재시작 시 서버가 이전 비정상 종료로부터 복구 절차를 실행합니다. 복구 중에는 시작 시간이 평소보다 길어질 수 있습니다.
{{< /callout >}}

## 관련 섹션

- [로그 확인](../../troubleshooting/log-logs/) — 로그 파일 분석 방법
- [연결할 수 없을 때](../connection/) — 서버는 시작됐으나 접속이 안 될 때
