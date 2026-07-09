---
type: docs
title: '7.13.1.2 파일 Collector'
weight: 20
---

파일 Collector는 로컬 파일 시스템의 파일을 읽어 Machbase 테이블에 적재합니다. 설정은
JSON이 아니라 `COLLECT_TYPE=FILE`을 포함한 `.tpl` 파일로 작성하고, 파싱과 컬럼 매핑은
별도의 `.rgx` 파일에서 정의합니다.

## 동작 원리

```
[로컬 파일] ──읽기──→ [CSV/JSON/REGEX 파싱] ──→ [Machbase DB]
                         │
                   [처리 완료 파일 보관]
```

## 대상 테이블 예시

```sql
CREATE TABLE file_sensor_log (
    name    VARCHAR(64),
    time    DATETIME,
    value   DOUBLE,
    quality INTEGER
);
```

## `.tpl` 설정 예시

```text
COLLECT_TYPE=FILE
LOG_SOURCE=/data/sensors/sensor.csv
REGEX_PATH=/opt/machbase/collector/file_sensor.rgx
PARSE_TYPE=CSV

DB_TABLE_NAME=file_sensor_log
DB_ADDR=127.0.0.1
DB_PORT=5656
DB_USER=SYS
DB_PASS=MANAGER

FILE_BACKUP_PATH=/data/sensors/done
SLEEP_TIME=1
```

## `.rgx` 컬럼 매핑 예시

```text
COL_LIST=NAME,TIME,VALUE,QUALITY
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

NAME=QUALITY
TYPE=INTEGER
SIZE=4
```

수집 대상 CSV 파일은 `.rgx`의 컬럼 순서와 맞아야 합니다.

```csv
DEVICE_A,2024-01-01 10:00:00,72.3,100
DEVICE_A,2024-01-01 10:00:01,72.5,100
DEVICE_B,2024-01-01 10:00:00,68.5,100
```

## 주요 템플릿 키

| 키 | 설명 |
|----|------|
| `COLLECT_TYPE` | `FILE` |
| `LOG_SOURCE` | 수집할 로컬 파일 경로 |
| `REGEX_PATH` | 컬럼 매핑 `.rgx` 파일 경로 |
| `PARSE_TYPE` | `CSV`, `JSON`, `REGEX`, `JSON_PIVOT` |
| `DB_TABLE_NAME` | 적재 대상 테이블 |
| `DB_ADDR`, `DB_PORT` | Machbase 서버 주소와 포트 |
| `DB_USER`, `DB_PASS` | 접속 계정 |
| `FILE_BACKUP_PATH` | 처리 완료 파일 보관 경로 |
| `SLEEP_TIME` | 수집 루프 대기 시간 |

## Collector 등록 및 시작

```bash
machcollectoradmin --startup
```

```sql
CREATE COLLECTOR localhost.file_sensor
FROM "/opt/machbase/collector/file_sensor.tpl";

ALTER COLLECTOR localhost.file_sensor START;
ALTER COLLECTOR localhost.file_sensor STOP;
```

## 참고

- 템플릿 설정 상세: [../template-regex-collector](../template-regex-collector)
- 오류 처리: [../error-handling-collector](../error-handling-collector)
