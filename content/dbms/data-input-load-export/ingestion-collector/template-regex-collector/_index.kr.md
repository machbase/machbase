---
type: docs
title: 'Collector 템플릿과 정규식'
weight: 60
---

Collector 설정은 수집 소스와 DB 접속 정보를 담은 `.tpl` 파일, 컬럼 매핑을 담은
`.rgx` 파일로 나뉩니다. `.tpl` 파일의 `REGEX_PATH`가 사용할 `.rgx` 파일을 지정합니다.

## 지원 파싱 타입

| `PARSE_TYPE` | 설명 |
|--------------|------|
| `CSV` | 구분자 기반 텍스트 파싱 |
| `JSON` | JSON 형식 파싱 |
| `REGEX` | 정규식 기반 파싱 |
| `JSON_PIVOT` | JSON 데이터를 pivot 형태로 파싱 |

## `.tpl` 기본 예시

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
```

## `.rgx` 컬럼 매핑

`.rgx` 파일에는 대상 컬럼 목록과 각 컬럼의 타입, 크기를 작성합니다.

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

## CSV 구분자 설정

CSV 파싱에서는 `FIELD_TERM`과 `RECORD_TERM`으로 필드/레코드 구분자를 지정할 수 있습니다.

```text
COL_LIST=NAME,TIME,VALUE
FIELD_TERM=,
RECORD_TERM=\n
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

## 컬럼 데이터 타입

| 타입 값 | Machbase 타입 | 설명 |
|---------|--------------|------|
| `VARCHAR` | VARCHAR | 문자열 |
| `INTEGER` | INTEGER | 32비트 정수 |
| `LONG` | BIGINT | 64비트 정수 |
| `DOUBLE` | DOUBLE | 배정밀도 실수 |
| `FLOAT` | FLOAT | 단정밀도 실수 |
| `DATETIME` | DATETIME | 날짜/시각 |
| `IPV4` | IPV4 | IPv4 주소 |
| `IPV6` | IPV6 | IPv6 주소 |
| `TEXT` | TEXT | 긴 문자열 |

## 작성 시 주의사항

- JSON 형식의 `template.columns[]` 설정은 Collector 템플릿 형식이 아닙니다.
- `.tpl` 파일에서 `PARSE_TYPE`을 지정하고, `.rgx` 파일에서 `COL_LIST`와 컬럼 속성을 맞춥니다.
- 수집 파일의 필드 순서와 `.rgx`의 컬럼 순서가 일치해야 합니다.

## 참고

- 파일 Collector 설정: [../file-collector](../file-collector)
- SFTP Collector 설정: [../sftp-collector](../sftp-collector)
