---
type: docs
title: '11.10 데이터 입력과 반출'
weight: 100
toc: true
aliases:
  - /dbms/application-integration/data-input-load-export/
---

SQL, Append API, 파일 도구 중 데이터 양과 운영 방식에 맞는 경로를 선택합니다. 이 페이지는
선택과 검증 흐름을 설명하며, 전체 옵션은 각 도구·SQL 레퍼런스를 정본으로 사용합니다.

<a id="selection-input-method"></a>

## 입력 방식 선택

<a id="selection-input-method-table-types-type"></a>

| 방식 | 적합한 경우 | 주요 확인값 |
|------|-------------|-------------|
| 단건 INSERT | 소량 입력, 즉시 오류 확인 | 영향 행 수, generated ID |
| prepared batch | 같은 SQL의 반복 실행 | 항목별 결과와 실패 위치 |
| Append API | 지속적인 TAG·LOG 대량 수집 | ack, 성공·실패 건수 |
| `LOAD DATA INFILE` | 서버가 읽을 수 있는 파일 적재 | 서버 파일 권한, 입력 건수 |
| `machloader`·`csvimport` | 클라이언트 파일 적재 | log·bad file, 입력·실패 건수 |

<a id="machloader-vs-csvimport-csvexport-tagmetaimport"></a>
<a id="load-data-infile-vs-machloader"></a>
<a id="ingestion-sdk-append-vs-sql-collector"></a>

### 경로와 도구 비교

| 경로·도구 | 실행 위치와 용도 |
|---|---|
| SDK Append | 애플리케이션이 지속적으로 여러 TAG·LOG row 전송 |
| SQL INSERT | 소량 입력과 일반 SQL 연동 |
| `LOAD DATA INFILE` | 서버가 읽을 수 있는 파일을 SQL로 적재 |
| `machloader` | 클라이언트 파일의 mapping·log·bad file을 세밀하게 제어 |
| `csvimport`·`csvexport` | 단순 CSV 입출력 wrapper |
| `tagmetaimport` | TAG metadata를 일괄 등록·변경 |
| Collector | FILE·SFTP source를 반복 수집 |

`tagmetaimport`는 TAG 측정값 입력 도구가 아닙니다. 지원 Collector source와 정확한 option은
[명령행 도구](/dbms/reference/command-line-tools/)와
[Collector 레퍼런스](/dbms/reference/collector/)를 확인하십시오.

<a id="selection-input-method-selection-input-method-guide"></a>

원본 보존이 필요한 시계열·이벤트는 TAG 또는 LOG에 넣습니다. 관계형 변경은 TRANSACTION,
작은 참조 데이터는 LOOKUP, 재생성 가능한 메모리 캐시는 VOLATILE을 사용합니다. 테이블
선택이 끝난 뒤 예상 건수, 지연 허용치, 재시도 단위, 중복 정책을 기준으로 입력 방식을
결정합니다.

<a id="sql"></a>
<a id="insert"></a>
<a id="sql-insert"></a>

## SQL INSERT

다음 예제는 생성부터 정리까지 순서대로 실행할 수 있습니다.

```sql
CREATE LOG TABLE integration_insert_demo (
    event_time DATETIME,
    sensor_id  VARCHAR(32),
    value      DOUBLE
);

INSERT INTO integration_insert_demo
VALUES (TO_DATE('2026-01-01 00:00:00'), 'TEMP-01', 25.3);

SELECT sensor_id, value
FROM integration_insert_demo;

DROP TABLE integration_insert_demo;
```

애플리케이션에서는 값을 prepared parameter로 바인딩하고 반환된 영향 행 수를 확인합니다.

<a id="append"></a>
<a id="sql-append"></a>

## Append API

Append는 각 SDK의 전용 API로 table을 열고 여러 row를 보낸 뒤 flush·close하는 흐름입니다.
컬럼 순서와 타입을 대상 스키마에 맞추고, 일반 query와 connection을 분리합니다. 언어별
완전한 코드는 이 장의 SDK별 페이지를 참고합니다.

<a id="load-data-infile"></a>
<a id="sql-load-data-infile"></a>

## LOAD DATA INFILE

`LOAD DATA INFILE`은 서버가 접근할 수 있는 파일을 SQL로 적재합니다. 파일 경로는 서버
프로세스 관점에서 해석되므로 다음을 확인합니다.

- 서버 호스트에 파일이 존재하는지
- 서버 프로세스 계정이 파일을 읽을 수 있는지
- delimiter, enclosure, encoding, 날짜 format이 원본과 일치하는지
- 실패 row를 식별할 log·bad file을 어디에 남길지

구문과 지원 옵션은
[LOAD DATA INFILE](/dbms/reference/sql/syntax-dictionary-sql/load-data-infile-syntax/)을
참고합니다.

<a id="file"></a>
<a id="file-csv"></a>
<a id="file-file-csv"></a>

## CSV 파일 준비

첫 행을 header로 사용할지 결정하고, 모든 row에서 컬럼 수와 순서를 일정하게 유지합니다.
NULL, 빈 문자열, delimiter가 포함된 문자열, 줄바꿈, DATETIME format을 표본 파일로 먼저
검증합니다. 대량 파일은 전체 실행 전에 작은 표본으로 table schema와 변환 규칙을 확인합니다.

<a id="import-machloader"></a>
<a id="file-import-machloader"></a>

## machloader로 가져오기

기본 구문은 다음과 같습니다.

```bash
"$MACHBASE_HOME/bin/machloader"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -i -t SENSOR_LOG -d /data/sensor.csv   -l /data/sensor.log -b /data/sensor.bad
```

header가 있으면 `-H`, delimiter가 쉼표가 아니면 `-D`, 날짜 format이 다르면 `-F`를
명시합니다. 전체 옵션은
[machloader](/dbms/reference/command-line-tools/dictionary-machloader/)를 참고합니다.

<a id="import-csvimport"></a>
<a id="file-import-csvimport"></a>

## csvimport로 가져오기

`csvimport`는 machloader의 자주 쓰는 CSV 옵션을 간소화한 도구입니다.

```bash
"$MACHBASE_HOME/bin/csvimport"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -t SENSOR_LOG -d /data/sensor.csv -H   -l /data/sensor.log -b /data/sensor.bad
```

`-C` 자동 생성은 모든 컬럼을 의도한 업무 타입으로 만들지 않을 수 있습니다. 운영 적재는
table을 명시적으로 생성하고 schema를 확인한 뒤 실행합니다.

<a id="export"></a>

## 반출 방식 선택

| 방식 | 적합한 경우 |
|------|-------------|
| `SAVE DATA INTO` | SQL 조건과 projection으로 서버 파일 생성 |
| `machloader -o` | table 단위 반출과 상세 옵션 사용 |
| `csvexport` | 단순 CSV 반출 |
| SDK SELECT | 애플리케이션이 row를 변환·전송해야 하는 경우 |

<a id="export-ownership"></a>
<a id="export-export-ownership"></a>

## 파일 소유권과 경로

`SAVE DATA INTO`의 경로와 파일 권한은 서버 프로세스 기준입니다. machloader와 csvexport가
만드는 파일은 도구를 실행한 OS 사용자 기준입니다. 상대 경로를 피하고, 기존 파일 덮어쓰기
정책과 사용 가능한 디스크 공간을 먼저 확인합니다.

<a id="export-sql-save-data-into"></a>
<a id="export-export-sql-save-data-into"></a>

## SAVE DATA INTO

SQL 조건으로 결과를 반출할 때 사용합니다. 운영 경로에서 실행하기 전에 작은 결과와 별도
검증 경로로 파일 생성·encoding·header를 확인합니다. 전체 구문은
[SAVE DATA INTO](/dbms/reference/sql/syntax-dictionary-sql/save-data-into-syntax/)를
참고합니다.

<a id="export-machloader"></a>
<a id="export-export-machloader"></a>

## machloader로 내보내기

```bash
"$MACHBASE_HOME/bin/machloader"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -o -t SENSOR_LOG -d /data/sensor-export.csv -H   -l /data/sensor-export.log
```

<a id="export-csvexport"></a>
<a id="export-export-csvexport"></a>

## csvexport로 내보내기

```bash
"$MACHBASE_HOME/bin/csvexport"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -t SENSOR_LOG -d /data/sensor-export.csv -H   -l /data/sensor-export.log
```

<a id="error-handling"></a>
<a id="batch"></a>
<a id="error-handling-batch"></a>

## Batch 처리

- batch 크기는 row 크기와 지연 요구사항을 기준으로 부하 테스트합니다.
- 각 batch의 source offset과 대상 성공 건수를 기록합니다.
- 부분 실패 시 전체 재실행보다 실패 row만 분리해 재처리합니다.
- 같은 row를 재전송해도 안전하도록 업무 키와 중복 정책을 정의합니다.

<a id="error-handling-bulk"></a>
<a id="error-handling-error-handling-bulk"></a>

## 대량 입력 오류 처리

1. 도구 exit code와 요약 건수를 확인합니다.
2. log에서 서버 오류 코드와 최초 실패 원인을 확인합니다.
3. bad file의 컬럼 수, 타입, NULL, 날짜 format, encoding을 원본과 비교합니다.
4. 수정한 소량 파일로 재검증한 뒤 실패 row만 다시 입력합니다.
5. 대상 table의 최종 건수와 시간 범위, 표본 row를 확인합니다.

자격 증명과 원문 민감 데이터가 log·bad file에 남을 수 있으므로 접근 권한과 보존 기간을
설정합니다.
