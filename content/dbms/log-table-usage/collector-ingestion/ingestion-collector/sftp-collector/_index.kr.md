---
type: docs
title: '7.13.1.4 SFTP Collector'
weight: 40
---

SFTP Collector는 원격 SFTP 서버의 파일을 내려받아 Machbase 테이블에 적재합니다.
설정은 `COLLECT_TYPE=SFTP`를 포함한 `.tpl` 파일로 작성합니다.

## 동작 원리

```
[SFTP 서버 파일] ──다운로드──→ [Collector] ──파싱/적재──→ [Machbase DB]
```

## 대상 테이블 예시

```sql
CREATE TABLE sftp_sensor_log (
    name  VARCHAR(64),
    time  DATETIME,
    value DOUBLE
);
```

## `.tpl` 설정 예시

```text
COLLECT_TYPE=SFTP
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USER=collector
SFTP_PASS=secret
SFTP_TIMEOUT=30

LOG_SOURCE=/data/sensor/sensor.csv
REGEX_PATH=/opt/machbase/collector/sftp_sensor.rgx
PARSE_TYPE=CSV

DB_TABLE_NAME=sftp_sensor_log
DB_ADDR=127.0.0.1
DB_PORT=5656
DB_USER=SYS
DB_PASS=MANAGER

FILE_BACKUP_PATH=/data/sensor/done
SLEEP_TIME=10
```

## `.rgx` 컬럼 매핑 예시

```text
COL_LIST=NAME,TIME,VALUE
REGEX_NO=1

NAME=NAME
TYPE=VARCHAR
SIZE=64

NAME=TIME
TYPE=DATETIME
SIZE=8

NAME=VALUE
TYPE=DOUBLE
SIZE=8
```

## 주요 SFTP 키

| 키 | 설명 |
|----|------|
| `COLLECT_TYPE` | `SFTP` |
| `SFTP_HOST` | SFTP 서버 호스트명 또는 IP 주소 |
| `SFTP_PORT` | SFTP 서버 포트 |
| `SFTP_USER` | SFTP 접속 사용자명 |
| `SFTP_PASS` | SFTP 접속 비밀번호 |
| `SFTP_TIMEOUT` | SFTP 연결 타임아웃 |
| `LOG_SOURCE` | 수집할 원격 파일 경로 |
| `REGEX_PATH` | 컬럼 매핑 `.rgx` 파일 경로 |
| `PARSE_TYPE` | `CSV`, `JSON`, `REGEX`, `JSON_PIVOT` |
| `FILE_BACKUP_PATH` | 처리 완료 파일 보관 경로 |
| `SLEEP_TIME` | 수집 루프 대기 시간 |

## Collector 등록 및 시작

```sql
CREATE COLLECTOR localhost.sftp_sensor
FROM "/opt/machbase/collector/sftp_sensor.tpl";

ALTER COLLECTOR localhost.sftp_sensor START;
```

## 참고

- 템플릿 설정 상세: [../template-regex-collector](../template-regex-collector)
- 파일 Collector: [../file-collector](../file-collector)
- 오류 처리: [../error-handling-collector](../error-handling-collector)
