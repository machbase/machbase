---
type: docs
title: '16.5 Collector로 파일 수집하기'
weight: 70
toc: true
---

이 시나리오는 로컬 CSV 파일을 Collector로 읽어 LOG 테이블에 적재하는 최소 절차를
설명합니다. Collector는 `KEY=VALUE` 형식의 `.tpl` 파일과 컬럼 매핑용 `.rgx` 파일을
사용합니다.

현재 확인된 `COLLECT_TYPE`은 `FILE`과 `SFTP`입니다. TCP/UDP 소켓에서 직접 수집해야
한다면 [SDK 선택 가이드](/dbms/application-integration/guide-drivers/)에서 Append API를
지원하는 드라이버를 선택하십시오.

## 1. 대상 테이블 생성

```sql
CREATE LOG TABLE file_sensor_log (
    name    VARCHAR(64),
    time    DATETIME,
    value   DOUBLE,
    quality INTEGER
);
```

## 2. 입력 파일 준비

`/data/sensors/sensor.csv`를 다음과 같이 준비합니다. 헤더 없이 `.rgx`의 컬럼 순서에
맞춥니다.

```csv
DEVICE_A,2024-01-01 10:00:00,72.3,100
DEVICE_A,2024-01-01 10:00:01,72.5,100
DEVICE_B,2024-01-01 10:00:00,68.5,100
```

## 3. Collector 템플릿 작성

`/opt/machbase/collector/file_sensor.tpl`을 작성합니다.

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

운영 환경에서는 템플릿에 평문 비밀번호를 그대로 배포하지 말고 파일 소유권과 읽기 권한을
제한하십시오.

## 4. 컬럼 매핑 작성

`/opt/machbase/collector/file_sensor.rgx`를 작성합니다.

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

배포 버전의 `.rgx` 샘플과 입력 데이터의 날짜 형식, 구분자, 컬럼 순서가 일치하는지
확인하십시오. 설정 키 전체 목록은
[Collector template 사전](/dbms/reference/collector/dictionary-collector-template/)을
참고하십시오.

## 5. Collector 등록 및 시작

먼저 Collector manager를 기동합니다.

```bash
machcollectoradmin --startup
```

Collector를 생성하고 시작합니다.

```sql
CREATE COLLECTOR localhost.file_sensor
FROM "/opt/machbase/collector/file_sensor.tpl";

ALTER COLLECTOR localhost.file_sensor START;
```

수집을 중지할 때는 다음 명령을 실행합니다.

```sql
ALTER COLLECTOR localhost.file_sensor STOP;
```

## 6. 적재 결과 확인

```sql
SELECT name, time, value, quality
  FROM file_sensor_log
 ORDER BY time, name;
```

파일이 처리되지 않으면 다음 순서로 확인합니다.

1. `LOG_SOURCE` 파일의 존재 여부와 Collector 실행 계정의 읽기 권한을 확인합니다.
2. CSV 컬럼 수·순서가 `.rgx` 정의와 일치하는지 확인합니다.
3. `DB_ADDR`, `DB_PORT`, `DB_USER`, `DB_PASS` 접속 정보를 확인합니다.
4. `FILE_BACKUP_PATH` 디렉터리의 쓰기 권한을 확인합니다.
5. Collector 상태와 trace 로그에서 최초 오류를 확인합니다.

## 다음 단계

- SFTP 파일 수집: [Collector 기반 수집의 SFTP 절](/dbms/log-table-usage/collector-ingestion/#ingestion-collector-sftp-collector)
- 설정 키: [Collector 레퍼런스](/dbms/reference/collector/)
- Manager 운영과 복구: [Collector 운영](/dbms/operations-configuration-recovery/collector/)
- 일회성 대량 파일 적재: [대량 적재 파이프라인](/dbms/scenario-guides/bulk-pipeline/)
