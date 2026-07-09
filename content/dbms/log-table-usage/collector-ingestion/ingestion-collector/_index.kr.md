---
type: docs
title: '7.13.1 Collector 기반 수집'
weight: 40
---

Machbase Collector는 외부 파일 소스를 주기적으로 읽어 Machbase 테이블에 적재하는
컴포넌트입니다. 현재 확인된 Collector 설정은 JSON이 아니라 `KEY=VALUE` 형식의
`.tpl` 템플릿 파일과 컬럼 매핑을 정의하는 `.rgx` 파일을 사용합니다.

## 수집 파이프라인 구조

```
[로컬 파일] ──┐
              ├─→ [Machbase Collector] ──→ [Machbase DB]
[SFTP 파일] ──┘        (.tpl + .rgx)
```

현재 코드에서 확인되는 `COLLECT_TYPE`은 `FILE`과 `SFTP`입니다. TCP/UDP socket 또는
ODBC Collector 설정은 이 장에서 예제로 제공하지 않습니다.

## 주요 특징

- **파일 기반 수집:** 로컬 파일 또는 SFTP 원격 파일을 읽어 적재합니다.
- **템플릿 기반 설정:** 수집 소스와 DB 접속 정보는 `.tpl` 파일에 작성합니다.
- **컬럼 매핑 분리:** CSV, JSON, REGEX, JSON_PIVOT 파싱 정보는 `.rgx` 파일에 작성합니다.
- **처리 파일 관리:** `FILE_BACKUP_PATH`로 수집 완료 파일을 보관할 위치를 지정합니다.

## 설정 파일 기본 구조

Collector 템플릿은 다음과 같은 형식으로 작성합니다.

```text
COLLECT_TYPE=FILE
LOG_SOURCE=/data/sensors/sensor.csv
REGEX_PATH=/opt/machbase/collector/sensor.rgx
PARSE_TYPE=CSV

DB_TABLE_NAME=sensor_log
DB_ADDR=127.0.0.1
DB_PORT=5656
DB_USER=SYS
DB_PASS=MANAGER

FILE_BACKUP_PATH=/data/sensors/done
SLEEP_TIME=1
```

컬럼 매핑은 `.rgx` 파일에서 정의합니다.

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

## Collector 기동 및 관리

```bash
# Collector manager 기동
machcollectoradmin --startup
```

```sql
-- Collector 생성
CREATE COLLECTOR localhost.file_sensor
FROM "/path/to/file_sensor.tpl";

-- Collector 시작
ALTER COLLECTOR localhost.file_sensor START;

-- Collector 중지
ALTER COLLECTOR localhost.file_sensor STOP;
```

## 하위 섹션

| 섹션 | 설명 |
|------|------|
| [Collector를 사용해야 하는 경우](./use-cases-collector/) | Collector 도입 판단 기준 |
| [파일 Collector](./file-collector/) | 로컬 파일 수집 |
| [SFTP Collector](./sftp-collector/) | 원격 SFTP 파일 수집 |
| [Collector 템플릿과 정규식](./template-regex-collector/) | `.tpl`, `.rgx` 설정 |
| [Collector 오류 처리](./error-handling-collector/) | 오류 유형별 원인 분석과 복구 절차 |

## 참고

- Collector 수집 성능 튜닝: [../../performance-tuning/performance-tuning/ingestion-performance-tuning-collector](../../performance-tuning/performance-tuning/ingestion-performance-tuning-collector)
- Collector 레퍼런스: [../../reference/collector](../../reference/collector)
