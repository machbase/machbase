---
title: '7.13 Collector 기반 수집'
weight: 130
toc: true
---

Machbase Collector를 사용하여 외부 파일을 주기적으로 읽어 테이블에 적재하는 방법을 다룹니다.


<a id="ingestion-collector"></a>

## Collector 기반 수집

Machbase Collector는 외부 파일 소스를 주기적으로 읽어 Machbase 테이블에 적재하는
컴포넌트입니다. Collector 설정은 JSON이 아니라 `KEY=VALUE` 형식의
`.tpl` 템플릿 파일과 컬럼 매핑을 정의하는 `.rgx` 파일을 사용합니다.

### 수집 파이프라인 구조

```
[로컬 파일] ──┐
              ├─→ [Machbase Collector] ──→ [Machbase DB]
[SFTP 파일] ──┘        (.tpl + .rgx)
```

현재 코드에서 확인되는 `COLLECT_TYPE`은 `FILE`과 `SFTP`입니다. TCP/UDP socket 또는
ODBC Collector 설정은 이 장에서 예제로 제공하지 않습니다.

### 주요 특징

- **파일 기반 수집:** 로컬 파일 또는 SFTP 원격 파일을 읽어 적재합니다.
- **템플릿 기반 설정:** 수집 소스와 DB 접속 정보는 `.tpl` 파일에 작성합니다.
- **컬럼 매핑 분리:** CSV, JSON, REGEX, JSON_PIVOT 파싱 정보는 `.rgx` 파일에 작성합니다.
- **처리 파일 관리:** `FILE_BACKUP_PATH`로 수집 완료 파일을 보관할 위치를 지정합니다.

### 설정 파일 기본 구조

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

### Collector 기동 및 관리

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

### 하위 섹션

| 섹션 | 설명 |
|------|------|
| [Collector를 사용해야 하는 경우](/dbms/log-table-usage/collector-ingestion/#use-cases-collector) | Collector 도입 판단 기준 |
| [파일 Collector](/dbms/log-table-usage/collector-ingestion/#file-collector) | 로컬 파일 수집 |
| [SFTP Collector](/dbms/log-table-usage/collector-ingestion/#sftp-collector) | 원격 SFTP 파일 수집 |
| [Collector 템플릿과 정규식](/dbms/log-table-usage/collector-ingestion/#template-regex-collector) | `.tpl`, `.rgx` 설정 |
| [Collector 오류 처리](/dbms/log-table-usage/collector-ingestion/#error-handling-collector) | 오류 유형별 원인 분석과 복구 절차 |

### 참고

- Collector 수집 성능 튜닝: [../../performance-tuning/performance-tuning/ingestion-performance-tuning-collector](/dbms/performance-tuning/performance-tuning/#ingestion-performance-tuning-collector)
- Collector 레퍼런스: [../../reference/collector](../../reference/collector)

<a id="use-cases-collector"></a>
<a id="ingestion-collector-use-cases-collector"></a>

### Collector를 사용해야 하는 경우

Machbase에 데이터를 입력하는 방법은 여러 가지입니다. Collector를 쓸지, 애플리케이션에서 API를 직접 호출할지는 데이터 소스의 성격과 운영 환경에 따라 결정합니다.

#### Collector vs 직접 API 선택 기준

| 상황 | 권장 방법 |
|------|-----------|
| 애플리케이션이 직접 Machbase에 쓸 수 있음 | Append API (JDBC/Python/Go 등) |
| 외부 장치나 파일에서 자동 수집이 필요함 | Collector |
| 로컬 파일 또는 SFTP 파일을 자동 수집해야 함 | Collector |
| 수신 데이터의 형식 변환이나 파싱이 필요함 | Collector (템플릿 활용) |
| 네트워크 중단 시 데이터 손실 없이 버퍼링이 필요함 | Collector |
| 원격 서버의 파일을 주기적으로 가져와야 함 | Collector (SFTP 소스) |
| 단일 애플리케이션에서 실시간으로 대량 적재 | Append API (직접 연결이 더 효율적) |

#### Collector가 적합한 구체적 사용 사례

##### 1. 로그 파일 모니터링

애플리케이션이나 시스템이 생성하는 로그 파일을 실시간으로 감시하고 분석 가능한 형태로 적재합니다. 파일 회전(rotation)이 발생해도 새 파일을 자동으로 감지합니다.

```
[App Log File] ──파일 감시──→ [Collector (파일 소스)] ──→ [Machbase]
```

##### 2. 원격 서버 파일 수집

원격 장비나 서버에서 주기적으로 생성되는 CSV 파일을 SFTP로 수집합니다. 파일 다운로드, 파싱, 적재, 처리 완료 후 파일 관리까지 자동화됩니다.

```
[원격 서버 /data/*.csv] ──SFTP──→ [Collector (SFTP 소스)] ──→ [Machbase]
```

##### 3. 기존 시스템의 DB 데이터 마이그레이션

Oracle, MySQL, MSSQL 등의 기존 RDBMS에 축적된 센서/로그 데이터를 Machbase로 이전할 때는 외부 DB에서 CSV로 반출한 뒤 `machloader` 또는 `LOAD DATA INFILE`로 적재합니다. 애플리케이션 레벨에서 주기적으로 조회한 뒤 SDK나 SQL INSERT로 입력하는 방식도 가능합니다.

#### Collector가 적합하지 않은 경우

- **애플리케이션이 Machbase에 직접 연결 가능한 경우:** JDBC, Python, Go 등의 드라이버로 Append API를 직접 호출하면 중간 컴포넌트 없이 더 낮은 지연시간으로 적재할 수 있습니다.
- **단발성 대량 데이터 로드:** CSV 파일을 한 번에 대량으로 적재하려면 `machloader`나 `LOAD DATA` 구문이 더 적합합니다.
- **실시간 스트리밍(Kafka, MQTT):** Machbase Neo의 내장 스트리밍 파이프라인이나 Flink/Kafka Connect 커넥터가 더 효율적입니다.

#### Collector 선택 시 확인 사항

Collector 도입을 결정하기 전에 다음 항목을 확인합니다.

1. **데이터 소스 프로토콜:** 소스가 FILE 또는 SFTP 파일로 제공되는가?
2. **데이터 형식:** 원시 데이터가 CSV, JSON, 고정 너비, 로그 텍스트 등 어떤 형식인가?
3. **수집 주기:** 실시간 연속 수집인가, 아니면 주기적인 배치 수집인가?
4. **네트워크 안정성:** 소스와 Machbase 사이의 연결이 불안정할 수 있는가?
5. **처리 후 파일 관리:** 수집 완료 파일을 이동하거나 삭제하는 정책이 필요한가?

#### 참고

- 파일 수집 설정: [../file-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-file-collector)
- SFTP 수집 설정: [../sftp-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-sftp-collector)

<a id="file-collector"></a>
<a id="ingestion-collector-file-collector"></a>

### 파일 Collector

파일 Collector는 로컬 파일 시스템의 파일을 읽어 Machbase 테이블에 적재합니다. 설정은
`COLLECT_TYPE=FILE`을 포함한 `.tpl` 파일로 작성하고, 파싱과 컬럼 매핑은
별도의 `.rgx` 파일에서 정의합니다.

#### 동작 원리

```
[로컬 파일] ──읽기──→ [CSV/JSON/REGEX 파싱] ──→ [Machbase DB]
                         │
                   [처리 완료 파일 보관]
```

#### 대상 테이블 예시

```sql
CREATE LOG TABLE file_sensor_log (
    name    VARCHAR(64),
    time    DATETIME,
    value   DOUBLE,
    quality INTEGER
);
```

#### `.tpl` 설정 예시

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

#### `.rgx` 컬럼 매핑 예시

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

#### 주요 템플릿 키

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

#### Collector 등록 및 시작

```bash
machcollectoradmin --startup
```

```sql
CREATE COLLECTOR localhost.file_sensor
FROM "/opt/machbase/collector/file_sensor.tpl";

ALTER COLLECTOR localhost.file_sensor START;
ALTER COLLECTOR localhost.file_sensor STOP;
```

#### 참고

- 템플릿 설정 상세: [../template-regex-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-template-regex-collector)
- 오류 처리: [../error-handling-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-error-handling-collector)

<a id="ingestion-collector-socket-collector"></a>

### socket Collector

Collector `COLLECT_TYPE`은 `FILE`과 `SFTP`를 지원합니다. TCP/UDP socket 수집 타입은
지원하지 않으므로 socket Collector 설정 예제를 제공하지 않습니다.

네트워크를 통해 실시간 데이터를 입력해야 하는 경우에는 애플리케이션에서 SDK Append API를
호출하는 방식을 우선 검토합니다.

#### 대안

| 요구 사항 | 권장 경로 |
|-----------|-----------|
| 장비/게이트웨이 실시간 연동 | SDK Append API를 사용하는 수집 애플리케이션 |
| 애플리케이션 직접 연동 | SDK Append API |
| 파일로 저장된 로그 수집 | [파일 Collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-file-collector) |
| 원격 서버 파일 수집 | [SFTP Collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-sftp-collector) |

<a id="ingestion-collector-sftp-collector"></a>

### SFTP Collector

SFTP Collector는 원격 SFTP 서버의 파일을 내려받아 Machbase 테이블에 적재합니다.
`COLLECT_TYPE=SFTP`를 포함한 `.tpl` 파일로 설정합니다.

#### 동작 원리

```
[SFTP 서버 파일] ──다운로드──→ [Collector] ──파싱/적재──→ [Machbase DB]
```

#### 대상 테이블 예시

```sql
CREATE LOG TABLE sftp_sensor_log (
    name  VARCHAR(64),
    time  DATETIME,
    value DOUBLE
);
```

#### `.tpl` 설정 예시

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

#### `.rgx` 컬럼 매핑 예시

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

#### 주요 SFTP 키

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

#### Collector 등록 및 시작

```sql
CREATE COLLECTOR localhost.sftp_sensor
FROM "/opt/machbase/collector/sftp_sensor.tpl";

ALTER COLLECTOR localhost.sftp_sensor START;
```

#### 참고

- 템플릿 설정 상세: [../template-regex-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-template-regex-collector)
- 파일 Collector: [../file-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-file-collector)
- 오류 처리: [../error-handling-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-error-handling-collector)

<a id="ingestion-collector-odbc-collector"></a>

### ODBC Collector

Collector `COLLECT_TYPE`은 `FILE`과 `SFTP`를 지원합니다. ODBC 수집 타입은 지원하지 않으므로
ODBC Collector 설정 예제를 제공하지 않습니다.

외부 RDBMS 데이터를 Machbase로 이전하거나 주기적으로 적재해야 하는 경우에는 다음 경로를
검토합니다.

#### 대안

| 요구 사항 | 권장 경로 |
|-----------|-----------|
| 일회성 대량 이전 | 외부 DB에서 CSV 반출 후 `machloader` 또는 `LOAD DATA INFILE` |
| 애플리케이션 레벨 동기화 | JDBC/ODBC 클라이언트에서 조회 후 Machbase SDK 또는 SQL INSERT |
| 원격 서버에 생성된 CSV 수집 | [SFTP Collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-sftp-collector) |

<a id="template-regex-collector"></a>
<a id="ingestion-collector-template-regex-collector"></a>

### Collector 템플릿과 정규식

Collector 설정은 수집 소스와 DB 접속 정보를 담은 `.tpl` 파일, 컬럼 매핑을 담은
`.rgx` 파일로 나뉩니다. `.tpl` 파일의 `REGEX_PATH`가 사용할 `.rgx` 파일을 지정합니다.

#### 지원 파싱 타입

| `PARSE_TYPE` | 설명 |
|--------------|------|
| `CSV` | 구분자 기반 텍스트 파싱 |
| `JSON` | JSON 형식 파싱 |
| `REGEX` | 정규식 기반 파싱 |
| `JSON_PIVOT` | JSON 데이터를 pivot 형태로 파싱 |

#### `.tpl` 기본 예시

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

#### `.rgx` 컬럼 매핑

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

#### CSV 구분자 설정

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

#### 컬럼 데이터 타입

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

#### 작성 시 주의사항

- JSON 형식의 `template.columns[]` 설정은 Collector 템플릿 형식이 아닙니다.
- `.tpl` 파일에서 `PARSE_TYPE`을 지정하고, `.rgx` 파일에서 `COL_LIST`와 컬럼 속성을 맞춥니다.
- 수집 파일의 필드 순서와 `.rgx`의 컬럼 순서가 일치해야 합니다.

#### 참고

- 파일 Collector 설정: [../file-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-file-collector)
- SFTP Collector 설정: [../sftp-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-sftp-collector)

<a id="error-handling-collector"></a>
<a id="ingestion-collector-error-handling-collector"></a>

### Collector 오류 처리

Collector 운영 중 발생할 수 있는 오류 유형과 점검 절차를 정리합니다.

#### 오류 유형 분류

| 유형 | 원인 | 처리 방식 |
|------|------|-----------|
| 파일 접근 실패 | `LOG_SOURCE`, `FILE_BACKUP_PATH` 경로 오류 또는 권한 부족 | 경로와 실행 계정 권한 확인 |
| SFTP 연결 실패 | `SFTP_HOST`, `SFTP_PORT`, `SFTP_USER`, `SFTP_PASS` 오류 | 접속 정보와 네트워크 확인 |
| 파싱 오류 | `PARSE_TYPE`, `.rgx` 컬럼 매핑, 실제 데이터 형식 불일치 | `.tpl`/`.rgx`와 원본 파일 비교 |
| 대상 연결 실패 | `DB_ADDR`, `DB_PORT`, `DB_USER`, `DB_PASS` 오류 또는 Machbase 중지 | DB 접속 확인 |
| 적재 오류 | 대상 테이블명, 컬럼 타입, 컬럼 순서 불일치 | `DB_TABLE_NAME`과 `.rgx` 컬럼 정의 확인 |

#### 오류 로그 확인

Collector 이벤트와 오류는 트레이스 로그에서 확인합니다.

```bash
# 전체 로그 마지막 100줄 확인
tail -100 $MACHBASE_HOME/trc/machcollector.trc

# 오류, 실패, 건너뜀 관련 메시지만 필터링
grep -i "error\|fail\|skip\|warn" $MACHBASE_HOME/trc/machcollector.trc

# 실시간 로그 모니터링
tail -f $MACHBASE_HOME/trc/machcollector.trc
```

#### 파일 소스 점검

```bash
# LOG_SOURCE 파일 존재 여부 확인
ls -l /data/sensors/sensor.csv

# Collector 실행 계정의 읽기 권한 확인
sudo -u machbase test -r /data/sensors/sensor.csv && echo readable

# 처리 완료 파일 보관 경로 쓰기 권한 확인
sudo -u machbase test -w /data/sensors/done && echo writable
```

확인할 `.tpl` 키:

```text
COLLECT_TYPE=FILE
LOG_SOURCE=/data/sensors/sensor.csv
FILE_BACKUP_PATH=/data/sensors/done
```

#### SFTP 소스 점검

```bash
# SFTP 서버 연결 확인
sftp -P 22 collector@sftp.example.com
```

확인할 `.tpl` 키:

```text
COLLECT_TYPE=SFTP
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USER=collector
SFTP_PASS=secret
SFTP_TIMEOUT=30
LOG_SOURCE=/data/sensor/sensor.csv
```

#### Machbase 대상 연결 점검

```bash
# Machbase 서버 상태 확인
machbase status

# Collector 설정과 같은 접속 정보로 연결 테스트
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

확인할 `.tpl` 키:

```text
DB_TABLE_NAME=sensor_log
DB_ADDR=127.0.0.1
DB_PORT=5656
DB_USER=SYS
DB_PASS=MANAGER
```

#### 파싱 오류 점검

파싱 오류가 발생하면 `PARSE_TYPE`, `REGEX_PATH`, `.rgx` 컬럼 정의를 원본 데이터와
비교합니다.

```text
PARSE_TYPE=CSV
REGEX_PATH=/opt/machbase/collector/sensor.rgx
```

`.rgx` 예시:

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

원본 CSV 예시:

```csv
TEMP-01,2024-01-01 10:00:00,25.3
TEMP-02,2024-01-01 10:00:01,25.7
```

#### 일반적인 복구 절차

1. 로그에서 오류 원인을 확인합니다.

   ```bash
   grep -i "error\|fail\|warn" $MACHBASE_HOME/trc/machcollector.trc | tail -30
   ```

2. `.tpl` 파일의 `COLLECT_TYPE`, `LOG_SOURCE`, `REGEX_PATH`, DB 접속 정보를 확인합니다.
3. `.rgx` 파일의 `COL_LIST`, 각 컬럼의 `NAME`, `TYPE`, `SIZE`가 대상 테이블과 맞는지 확인합니다.
4. 설정을 수정한 후 Collector를 재시작합니다.

   ```bash
   machcollectoradmin --stop-collector=localhost.my_collector
   machcollectoradmin --start-collector=localhost.my_collector
   ```

#### 참고

- 파일 Collector: [../file-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-file-collector)
- SFTP Collector: [../sftp-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-sftp-collector)
- 템플릿과 정규식: [../template-regex-collector](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-template-regex-collector)
