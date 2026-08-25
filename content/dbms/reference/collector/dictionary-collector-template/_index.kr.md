---
type: docs
title: '18.5.1 Collector template 사전'
weight: 10
toc: true
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

## 전체 템플릿 키

`ad/src/adc/adcTemplate.c`에서 확인되는 `.tpl` 템플릿 키는 다음과 같습니다.

| 키 그룹 | 키 |
|---------|----|
| 수집/파싱 | `COLLECT_TYPE`, `PARSE_TYPE`, `PIVOT_JSON_KEY`, `SEND_TYPE`, `LOG_SOURCE`, `DEFAULT_ADDR`, `LIB_NAME`, `REGEX_PATH`, `LANG` |
| 입력 방식 | `APPEND_MODE`, `CREATE_TABLE_MODE`, `SLEEP_TIME`, `AUTO_ADD_COLUMN`, `REGEX_SORT`, `ROTATE_FILE_COUNT`, `ROTATE_REGEX_SORT`, `REGEX_FILE_COUNT`, `CHECK_BAD_DATA` |
| DB 접속 | `DB_TABLE_NAME`, `DB_ADDR`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_ALTERNATIVE_SERVERS`, `DB_LIST` |
| Alternative DB | `ALSDB_TABLE_NAME`, `ALSDB_ADDR`, `ALSDB_PORT`, `ALSDB_USER`, `ALSDB_PASS` |
| 연결 호환 키 | `SOCKET_PORT`, `SOCKET_PROTOCOL`, `SFTP_HOST`, `SFTP_PORT`, `SFTP_USER`, `SFTP_PASS`, `SFTP_TIMEOUT` |
| 외부 DB 호환 키 | `ODBC_DSN`, `ODBC_QUERY`, `ODBC_SEQ_COLUMN`, `ODBC_USE_ORDER_BY`, `ODBC_DATETIME_FORMAT` |
| 파일 처리 | `FILE_BACKUP_PATH`, `FILE_BACKUP_MODE`, `RULE_FILE`, `PER_FILE_QUERY_IF`, `PER_FILE_QUERY_TRUE`, `PER_FILE_QUERY_FALSE` |

## `.rgx` 규칙 파일 키

위 전체 키 목록에 socket 또는 ODBC 이름이 남아 있어도 해당 이름이 현재 지원되는
`COLLECT_TYPE`임을 뜻하지 않습니다. 지원 입력 소스는
[Collector source type 사전](../dictionary-collector-source-type/)의 `FILE`, `SFTP`를
기준으로 판단하십시오.

`REGEX_PATH`가 가리키는 `.rgx` 규칙 파일은 레코드 파싱과 컬럼 매핑을 정의합니다.

| 키 | 설명 |
|----|------|
| `REGEX` | 레코드를 파싱할 정규식입니다. |
| `FIELD_TERM` | CSV/필드 구분자입니다. 기본값은 `,`입니다. |
| `RECORD_TERM` | 레코드 구분자입니다. 기본값은 줄바꿈입니다. |
| `COL_LIST` | 컬럼 정의 컨테이너입니다. |

`COL_LIST` 내부 컬럼 키:

| 키 | 설명 |
|----|------|
| `NAME` | 컬럼 이름 |
| `TYPE` | 컬럼 타입 |
| `SIZE` | 컬럼 크기 |
| `DATE_FORMAT` | DATETIME 파싱 포맷 |
| `USE_INDEX` | 컬럼 인덱스 사용 여부 |
| `REGEX_NO` | 컬럼에 매핑할 정규식 캡처 번호 |
| `JSON_KEY` | JSON 파싱 시 매핑할 JSON 키 |
| `REGEX` | 컬럼 단위 정규식 |
| `TIMEZONE_OFFSET` | 컬럼 단위 타임존 오프셋 |
| `FORMAT_STRING` | 값 변환 포맷 문자열 |
| `COLUMN_TYPE` | 컬럼 처리 유형 |
| `REPLACE_KEY_LENGTH`, `REPLACE_SPLIT`, `REPLACE` | 치환 규칙 |
| `COMPARE_TARGET`, `DECODE_KEY` | 비교/디코딩 규칙 |

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
