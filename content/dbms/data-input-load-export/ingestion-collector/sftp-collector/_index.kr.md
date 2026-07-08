---
type: docs
title: 'SFTP Collector'
weight: 40
---

SFTP Collector는 원격 SFTP 서버에 접속하여 지정한 경로의 파일을 주기적으로 내려받아 Machbase 테이블에 적재합니다. 원격 장비나 서버에서 생성되는 CSV 파일을 중앙 Machbase 인스턴스에 자동으로 수집하는 용도로 적합합니다.

## 동작 원리

```
[원격 SFTP 서버]
  /data/sensor/*.csv ──SFTP 다운로드──→ [Collector 로컬 임시 저장]
                                               │
                                        [파싱 + Append]
                                               │
                                        [Machbase DB]
                                               │
                                  [처리 완료 파일 원격 이동/삭제]
```

Collector는 설정된 `interval` 주기마다 원격 서버에 접속하여 패턴에 매칭되는 파일 목록을 조회합니다. 이전에 처리한 파일은 내부 상태 DB에 기록되어 있으므로 중복 수집이 발생하지 않습니다.

## 기본 설정

### 대상 테이블 생성

```sql
CREATE TABLE sftp_sensor_log (
    name   VARCHAR(64),
    time   DATETIME,
    value  DOUBLE
);
```

### Collector 설정 파일 (JSON)

`$MACHBASE_HOME/conf/collector/sftp_collector.json`:

```json
{
  "name": "sftp_sensor",
  "source": {
    "type": "SFTP",
    "host": "sftp.example.com",
    "port": 22,
    "user": "collector",
    "keyfile": "/home/machbase/.ssh/id_rsa",
    "remote_path": "/data/sensor/",
    "pattern": "*.csv",
    "interval": 60,
    "delete_after_collect": false,
    "done_remote_path": "/data/sensor/done/"
  },
  "template": {
    "type": "CSV",
    "separator": ",",
    "skip_header": 1,
    "columns": [
      {"name": "name",  "type": "VARCHAR",  "index": 0},
      {"name": "time",  "type": "DATETIME", "index": 1, "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value", "type": "DOUBLE",   "index": 2}
    ]
  },
  "target": {
    "table": "sftp_sensor_log",
    "server": {
      "host": "127.0.0.1",
      "port": 5656,
      "user": "SYS",
      "password": "MANAGER"
    }
  }
}
```

## 소스 파라미터 상세

| 파라미터 | 필수 | 기본값 | 설명 |
|---------|------|--------|------|
| `type` | 필수 | - | `"SFTP"` |
| `host` | 필수 | - | SFTP 서버 호스트명 또는 IP 주소 |
| `port` | 선택 | `22` | SFTP 서버 포트 번호 |
| `user` | 필수 | - | SFTP 접속 사용자명 |
| `password` | 선택 | - | SFTP 접속 비밀번호 (keyfile과 택일) |
| `keyfile` | 선택 | - | SSH 개인 키 파일 경로 (password와 택일) |
| `remote_path` | 필수 | - | 파일을 탐색할 원격 디렉터리 경로 |
| `pattern` | 선택 | `"*"` | 수집할 파일 이름 패턴 (glob) |
| `interval` | 선택 | `60` | 파일 탐색 주기 (초) |
| `delete_after_collect` | 선택 | `false` | 수집 완료 후 원격 파일 삭제 여부 |
| `done_remote_path` | 선택 | - | 수집 완료 파일을 이동할 원격 디렉터리 |

## SSH 키 인증 설정

비밀번호 인증 대신 SSH 키 인증을 사용하는 것을 권장합니다. 키 파일 권한이 올바르지 않으면 연결이 거부됩니다.

```bash
# SSH 키 생성 (machbase 서버에서)
ssh-keygen -t rsa -b 4096 -f /home/machbase/.ssh/id_rsa -N ""

# 원격 SFTP 서버에 공개 키 등록
ssh-copy-id -i /home/machbase/.ssh/id_rsa.pub collector@sftp.example.com

# 개인 키 파일 권한 설정 (600 이어야 함)
chmod 600 /home/machbase/.ssh/id_rsa

# 연결 테스트
sftp -i /home/machbase/.ssh/id_rsa collector@sftp.example.com
```

설정 파일에서 키 파일 경로를 지정합니다.

```json
{
  "source": {
    "type": "SFTP",
    "user": "collector",
    "keyfile": "/home/machbase/.ssh/id_rsa"
  }
}
```

## 중복 수집 방지

Collector는 수집한 파일의 이름과 처리 시간을 로컬 상태 DB에 기록합니다. 다음 탐색 주기에 동일한 파일이 목록에 나타나더라도 이미 처리된 파일로 인식하여 건너뜁니다.

처리 완료 파일을 원격 서버에서 관리하는 방법은 두 가지입니다.

```json
// 방법 1: 수집 후 원격 파일 삭제
{
  "source": {
    "delete_after_collect": true
  }
}

// 방법 2: 수집 후 원격 done 디렉터리로 이동
{
  "source": {
    "delete_after_collect": false,
    "done_remote_path": "/data/sensor/done/"
  }
}
```

## Collector 등록 및 시작

```bash
machcollectoradmin --startup
```

```sql
CREATE COLLECTOR localhost.sftp_sensor
FROM "$MACHBASE_HOME/conf/collector/sftp_collector.json";

ALTER COLLECTOR localhost.sftp_sensor START;
```

## SFTP 연결 상태 확인

```bash
# 트레이스 로그에서 SFTP 연결 이벤트 확인
grep -i "sftp\|connect\|download\|error" $MACHBASE_HOME/trc/machcollector.trc | tail -50

# 실시간 로그 모니터링
tail -f $MACHBASE_HOME/trc/machcollector.trc | grep -i "sftp\|file\|error"
```

## SFTP 연결 오류 처리 및 재시도

SFTP 서버가 일시적으로 오프라인이거나 네트워크 연결이 불안정한 경우, Collector는 설정된 간격으로 재연결을 시도합니다.

```json
{
  "source": {
    "type": "SFTP",
    "interval": 60,
    "connect_timeout": 30,
    "retry_count": 3,
    "retry_interval": 10
  }
}
```

| 파라미터 | 설명 |
|---------|------|
| `connect_timeout` | SFTP 연결 시도 타임아웃 (초) |
| `retry_count` | 연결 실패 시 재시도 횟수 |
| `retry_interval` | 재시도 대기 시간 (초) |

재시도가 모두 실패하면, 다음 탐색 주기(`interval`)가 될 때 다시 연결을 시도합니다.

## 참고

- 템플릿 설정 상세: [../template-regex-collector](../template-regex-collector)
- 오류 처리: [../error-handling-collector](../error-handling-collector)
- 파일 Collector (로컬): [../file-collector](../file-collector)
