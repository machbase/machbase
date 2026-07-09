---
type: docs
title: '17.5.2 Collector source type 사전'
weight: 20
---

Collector의 입력 소스는 템플릿(`.tpl`) 파일의 `COLLECT_TYPE`으로 지정합니다.
현재 배포 소스에서 확인되는 수집 타입은 `FILE`과 `SFTP`입니다.

## 지원 소스 타입 목록

| `COLLECT_TYPE` | 설명 | 주요 관련 키 |
|----------------|------|--------------|
| `FILE` | 로컬 파일을 읽어 Machbase로 전송합니다. | `LOG_SOURCE`, `SLEEP_TIME`, `FILE_BACKUP_PATH` |
| `SFTP` | SFTP로 접근 가능한 파일을 읽어 Machbase로 전송합니다. | `LOG_SOURCE`, `SLEEP_TIME`, `FILE_BACKUP_PATH` |

> 근거: `ad/src/include/admiDef.h`의 `ADMI_COLLECT_TYPE_FILE_NAME`,
> `ADMI_COLLECT_TYPE_SFTP_NAME` 및 `ad/src/adc/adcTemplate.c`의 collect type 검증 로직.

## FILE

`FILE`은 로컬 파일 경로를 `LOG_SOURCE`에 지정하는 방식입니다. CSV, JSON, REGEX
파싱은 `PARSE_TYPE`과 `REGEX_PATH`/`RULE_FILE` 등 템플릿 키로 결정합니다.

```ini
COLLECT_TYPE=FILE
LOG_SOURCE=/var/log/sensor/sensor.log
REGEX_PATH=/opt/machbase/collector/regex/sensor.rgx
PARSE_TYPE=CSV

DB_TABLE_NAME = "sensor_log"
DB_ADDR       = "127.0.0.1"
DB_PORT       = 5656
DB_USER       = "SYS"
DB_PASS       = "MANAGER"

CREATE_TABLE_MODE=2
```

## SFTP

`SFTP`는 원격 파일을 수집할 때 사용합니다. SFTP 접속 정보와 파일 경로는 템플릿의
관련 키로 지정합니다. 실제 키 집합은 배포 샘플 템플릿을 기준으로 확인해야 합니다.

```ini
COLLECT_TYPE=SFTP
LOG_SOURCE=/remote/path/sensor.log
PARSE_TYPE=CSV

DB_TABLE_NAME = "sensor_log"
DB_ADDR       = "127.0.0.1"
DB_PORT       = 5656
DB_USER       = "SYS"
DB_PASS       = "MANAGER"
```

## 파싱 타입과의 관계

수집 타입은 파일을 어디서 가져올지를 정하고, `PARSE_TYPE`은 읽은 내용을 어떻게
해석할지를 정합니다.

| `PARSE_TYPE` | 설명 |
|--------------|------|
| `CSV` | 구분자 기반 CSV 파싱 |
| `REGEX` | `.rgx` 파일의 정규식 규칙으로 파싱 |
| `JSON` | JSON 필드 파싱 |
| `JSON_PIVOT` | JSON 데이터를 pivot 형태로 전개 |

`TCP`, `UDP`, `SERIAL`, `HTTP`, `MQTT`는 현재 확인된 `COLLECT_TYPE` 값이 아니므로
이 장에서는 지원 소스 타입으로 문서화하지 않습니다.
