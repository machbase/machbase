---
type: docs
title: 'Collector template 사전'
weight: 10
---

Collector template은 JSON이 아니라 키-값 형식의 `.tpl` 파일입니다. 수집 대상 파일,
파싱 방식, Machbase 접속 정보, 테이블 생성 동작을 이 파일에 정의합니다.

## 템플릿 기본 구조

```ini
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

## 주요 템플릿 키

| 키 | 설명 |
|----|------|
| `COLLECT_TYPE` | 수집 타입. 현재 확인되는 값은 `FILE`, `SFTP`입니다. 생략 시 샘플에 따라 파일 수집으로 사용합니다. |
| `LOG_SOURCE` | 수집할 원본 파일 경로입니다. |
| `PARSE_TYPE` | 파싱 타입. `CSV`, `REGEX`, `JSON`, `JSON_PIVOT`을 사용합니다. |
| `REGEX_PATH` | `REGEX` 또는 `CSV` 파싱에 사용하는 `.rgx` 규칙 파일 경로입니다. |
| `PIVOT_JSON_KEY` | `JSON_PIVOT` 파싱에서 pivot 기준으로 사용할 JSON 키입니다. |
| `DB_TABLE_NAME` | 데이터를 입력할 Machbase 테이블 이름입니다. |
| `DB_ADDR` | Machbase 서버 주소입니다. |
| `DB_PORT` | Machbase 서버 포트입니다. |
| `DB_USER` | 접속 사용자입니다. |
| `DB_PASS` | 접속 비밀번호입니다. |
| `CREATE_TABLE_MODE` | 테이블 생성 동작입니다. `0`=생성 안 함, `1`=truncate, `2`=없으면 생성, `3`=drop 후 생성. |
| `SLEEP_TIME` | 파일 변경 확인 또는 반복 수집 대기 시간입니다. |
| `AUTO_ADD_COLUMN` | 입력 데이터에 맞춰 컬럼 자동 추가를 허용할지 여부입니다. |
| `FILE_BACKUP_PATH` | 수집 완료 파일을 이동할 백업 경로입니다. |
| `RULE_FILE` | 추가 파싱/처리 규칙 파일 경로입니다. |
| `PER_FILE_QUERY_IF` | 파일 단위 조건 쿼리입니다. |
| `PER_FILE_QUERY_TRUE` | `PER_FILE_QUERY_IF`가 참일 때 실행할 쿼리입니다. |
| `PER_FILE_QUERY_FALSE` | `PER_FILE_QUERY_IF`가 거짓일 때 실행할 쿼리입니다. |

## 파싱 타입

| `PARSE_TYPE` | 설명 | 관련 파일/키 |
|--------------|------|--------------|
| `CSV` | 구분자 기반 텍스트 파싱 | `REGEX_PATH`의 CSV 규칙 |
| `REGEX` | 정규식 캡처 기반 파싱 | `REGEX_PATH`의 `.rgx` 규칙 |
| `JSON` | JSON 필드 파싱 | JSON 규칙 파일 또는 템플릿 키 |
| `JSON_PIVOT` | JSON 배열/객체를 pivot 형태로 전개 | `PIVOT_JSON_KEY` |

## CSV 예시

템플릿 파일:

```ini
LOG_SOURCE=/opt/machbase/collector/log/simple.log
REGEX_PATH=/opt/machbase/collector/regex/simple.rgx
PARSE_TYPE=CSV

DB_TABLE_NAME = "csv_simple"
DB_ADDR       = "127.0.0.1"
DB_PORT       = 5656
DB_USER       = "SYS"
DB_PASS       = "MANAGER"

CREATE_TABLE_MODE=2
```

정규식/CSV 규칙 파일(`.rgx`)은 입력 필드를 테이블 컬럼으로 매핑합니다. 실제 문법은
배포 샘플의 `.rgx` 파일과 함께 확인합니다.

## JSON_PIVOT 예시

```ini
COLLECT_TYPE=FILE
LOG_SOURCE=/opt/machbase/collector/log/pivot.json
PARSE_TYPE=JSON_PIVOT
PIVOT_JSON_KEY=data

DB_TABLE_NAME = "sensor_pivot"
DB_ADDR       = "127.0.0.1"
DB_PORT       = 5656
DB_USER       = "SYS"
DB_PASS       = "MANAGER"
CREATE_TABLE_MODE=2
```

## 주의 사항

- 이 파일은 JSON 문서가 아니므로 중괄호 기반 `source.type` 또는 `template.columns`
  형식으로 작성하지 않습니다.
- 지원 수집 타입과 파싱 타입은 `ad/src/include/admiDef.h` 및
  `ad/src/adc/adcTemplate.c`의 정의와 배포 샘플 템플릿을 기준으로 확인합니다.
- 운영 환경에 배포하기 전 `machcollectoradmin --create-collector`로 템플릿을 등록하고
  `--status-collector` 또는 `--status`로 상태를 확인합니다.
