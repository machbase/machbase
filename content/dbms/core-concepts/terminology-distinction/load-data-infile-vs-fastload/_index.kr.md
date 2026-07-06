---
type: docs
title: 'LOAD DATA INFILE vs fastload'
weight: 50
---

파일에서 직접 데이터를 적재하는 방법 중 `LOAD DATA INFILE`과 `fastload`는 모두 CSV 파일을 처리하지만, 실행 주체와 사용 목적이 다릅니다.

## 비교 표

| 항목 | LOAD DATA INFILE | fastload |
| --- | --- | --- |
| 실행 방식 | SQL 문장 | machsql 클라이언트 옵션 (`-f`) |
| 파일 위치 | 서버 측 파일 경로 | 클라이언트 측 파일 경로 |
| 대상 테이블 | LOG, LOOKUP | LOG, TAG |
| 적합한 데이터 규모 | 소~중규모 | 대용량 |
| 속도 | 보통 | 고속 (APPEND 프로토콜 사용) |
| 설정 복잡도 | 낮음 (SQL 한 줄) | 낮음 (명령행 옵션) |

## LOAD DATA INFILE

`LOAD DATA INFILE`은 SQL 문장 형태로, 서버가 직접 지정된 파일 경로를 읽어 테이블에 적재합니다. 파일은 서버가 접근할 수 있는 경로에 있어야 합니다.

```sql
LOAD DATA INFILE '/data/device_events.csv'
INTO TABLE device_log
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```

machsql이나 ODBC/JDBC 클라이언트에서 일반 SQL처럼 실행할 수 있어 사용이 단순합니다. 서버 로컬 경로에 파일이 있어야 하므로, 클라이언트와 서버가 분리된 환경에서는 파일을 먼저 서버로 전송해야 합니다.

## fastload

fastload는 `machsql` 클라이언트에서 `-f` 옵션으로 실행하는 대용량 CSV 고속 적재 기능입니다. 클라이언트 측 파일을 읽어 Machbase의 APPEND 프로토콜로 서버에 전송합니다. APPEND 프로토콜은 SQL INSERT보다 파싱 오버헤드가 훨씬 적어, 같은 데이터 양을 훨씬 빠르게 처리합니다.

```bash
# machsql fastload 예시
machsql -u sys -p manager -s localhost \
        -f /data/sensor_data.csv \
        -t sensor_values
```

클라이언트 측 파일을 그대로 사용하므로, 파일을 서버로 먼저 복사할 필요가 없습니다. 수억 건 이상의 대용량 데이터를 일괄 적재할 때 권장합니다.

## 선택 기준

**LOAD DATA INFILE이 적합한 경우**

- 서버 로컬에 파일이 있고, 수백만 건 이하의 소~중규모 데이터를 적재하는 경우
- SQL 스크립트 형태로 적재 작업을 자동화하고 싶은 경우
- ODBC/JDBC 클라이언트에서 SQL로 처리해야 하는 경우

**fastload가 적합한 경우**

- 클라이언트에 파일이 있고, 수억 건 이상의 대용량 데이터를 가능한 빠르게 적재해야 하는 경우
- 초기 데이터 마이그레이션이나 대규모 히스토리 데이터 일괄 적재

## 다음 읽을 내용

- [machloader vs csvimport / csvexport vs tagmetaimport](../machloader-vs-csvimport-csvexport-tagmetaimport/) — 파일 기반 입출력 도구 전체 비교
- [SDK append vs SQL APPEND vs Collector 수집](../ingestion-sdk-append-vs-sql-collector/) — 실시간 수집 경로 비교
