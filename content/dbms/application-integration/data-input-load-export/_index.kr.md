---
type: docs
title: '11.7 데이터 입력과 반출'
weight: 960
---
SQL INSERT, Append API, 파일 적재(machloader, csvimport), SQL 기반 파일 직접 로드 등 상황에 맞는 입력 방법을 선택할 수 있습니다. 반출도 동일한 도구를 내보내기 방향으로 사용합니다.


<a id="selection-input-method"></a>

## 입력 방식 선택

사용 목적과 데이터 볼륨에 따라 입력 방법을 선택합니다.

### 입력 방법 개요

| 입력 방법 | 특징 | 주요 사용 사례 |
|----------|------|--------------|
| SQL INSERT | 단건·소량. 트랜잭션 지원 | 설정값 등록, 테스트 |
| Append API | SDK 기반 대량 입력. TAG/LOG는 비트랜잭션 버퍼 경로 | TAG/LOG 시계열 대량 수집, client API 기반 RDB batch 입력 |
| LOAD DATA INFILE | SQL로 서버 측 파일 직접 로드 | 서버에 위치한 대용량 파일 일괄 적재 |
| machloader | CLI 도구. 유연한 스키마 매핑 | 정기 배치, 마이그레이션 |
| csvimport | machloader 래퍼. 간편 CSV 입력 | 빠른 파일 적재 |
| tagmetaimport | TAG 메타데이터 전용 | TAG 메타데이터 초기 로드·업데이트 |
| REST API | HTTP 기반. 범용 연동 | 외부 시스템, IoT 디바이스 |
| SDK (Go/Python/C) | 내장 Append/INSERT | 애플리케이션 직접 연동 |

상세 선택 가이드는 하위 페이지를 참고하세요.

<a id="selection-input-method-table-types-type"></a>

### 테이블 타입별 입력 방식

테이블 타입에 따라 사용 가능한 입력 방식이 다릅니다.

#### 테이블 타입별 지원 입력 방식

| 입력 방식 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|----------|-----|-----|-----|---------|--------|
| SQL INSERT | O | O | O | O | O |
| INSERT SELECT | O | O | O | O | O |
| INSERT ON DUPLICATE KEY UPDATE | X | X | X | O (PK 필요) | O (PK 필요) |
| Append API | O | O | O (client API) | O | O |
| LOAD DATA INFILE | O | O | O | O | O |
| machloader | O | O | O | O | O |
| csvimport | O | O | O | O | O |
| tagmetaimport | O (메타데이터만) | X | X | X | X |

#### 테이블 타입별 권장 입력 방식

##### TAG 테이블

- **대량 시계열 수집**: Append API (SDK 경유) 또는 REST API
- **메타데이터 초기 로드**: tagmetaimport 또는 SQL INSERT METADATA
- **소량 데이터**: SQL INSERT

##### LOG 테이블

- **대량 로그 수집**: Append API 또는 machloader
- **파일 배치 적재**: machloader, csvimport, LOAD DATA INFILE
- **스트리밍 수집**: REST API 또는 SDK

##### RDB 테이블

- **초기 데이터 로드**: machloader 또는 SQL INSERT
- **애플리케이션 연동**: SQL INSERT/UPDATE/DELETE (JDBC, ODBC, SDK)
- **대량 입력**: 지원되는 client API의 appendBatch 또는 append stream
- **파일 적재**: csvimport

##### VOLATILE / LOOKUP 테이블

- **참조 데이터 초기 로드**: SQL INSERT 또는 machloader
- **UPSERT**: INSERT ON DUPLICATE KEY UPDATE (PK 있는 VOLATILE/LOOKUP)
- **설정 업데이트**: SQL UPDATE (PK 기준)

<a id="selection-input-method-selection-input-method-guide"></a>

### 입력 방식 선택 가이드

상황별 최적 입력 방법 선택 기준입니다.

#### 선택 플로우

```
데이터를 어디서 생성하는가?
├── 파일(CSV 등)
│   ├── 서버에서 직접 읽을 수 있다 → LOAD DATA INFILE
│   ├── 빠른 적재가 필요, 유연한 매핑 필요 → machloader
│   └── 단순 CSV → csvimport
│
├── 애플리케이션/SDK
│   ├── 대량 시계열 (수만 건/초 이상) → Append API
│   ├── RDB 대량 batch 입력 → client appendBatch/append stream
│   └── 소량 또는 일반 트랜잭션 처리 → SQL INSERT
│
├── HTTP/REST
│   └── 외부 시스템, IoT → REST API (8장 참고)
│
└── TAG 메타데이터
    └── 초기 로드 또는 일괄 업데이트 → tagmetaimport
```

#### 성능 기준 선택

| 처리량 목표 | 권장 방법 |
|-----------|---------|
| 수백만 건/초 (TAG/LOG) | Append API (SDK) |
| 수십만 건/초 | Append API, client appendBatch 또는 machloader 병렬 |
| 수천~수만 건/초 | LOAD DATA INFILE 또는 machloader |
| 수백 건/초 이하 | SQL INSERT |

#### 실시간 vs 배치

| 구분 | 권장 방법 |
|------|---------|
| 실시간 스트리밍 | REST API, SDK Append API |
| 정기 배치 | machloader, csvimport, LOAD DATA INFILE |
| 이벤트 기반 | SDK INSERT 또는 REST API |

#### 연동 경로 요약

- **REST API 상세**: [8장 애플리케이션 연동](/dbms/application-integration/) 참고
- **SDK (Go/Python/C) 상세**: [8장 애플리케이션 연동](/dbms/application-integration/) 참고

<a id="sql"></a>

## SQL 입력

표준 SQL INSERT와 함께 대량 입력을 위한 Append API, 파일 직접 로드를 위한 LOAD DATA INFILE을 제공합니다.

### 이 절에서 다루는 내용

- **[INSERT 구문](/dbms/application-integration/data-input-load-export/#insert)**: 단건·다건·INSERT SELECT 패턴
- **[Append API](/dbms/application-integration/data-input-load-export/#append)**: SDK 기반 초고속 대량 입력
- **[LOAD DATA INFILE / FAST LOAD](/dbms/application-integration/data-input-load-export/#load-data-infile-fastload)**: SQL로 서버 측 파일 직접 로드

<a id="sql-insert"></a>

### INSERT 구문

SQL INSERT는 Machbase의 모든 테이블 타입에서 사용할 수 있는 기본 입력 방법입니다.

#### 기본 INSERT

```sql
INSERT INTO table_name VALUES (val1, val2, ...);
INSERT INTO table_name (col1, col2) VALUES (val1, val2);
```

지정하지 않은 컬럼은 NULL로 채워집니다.

```sql
-- LOG 테이블 단건 삽입
INSERT INTO sensor_log (sensor_id, ts, value) VALUES ('TEMP-01', NOW, 25.3);

-- TAG 테이블 데이터 삽입
INSERT INTO tag VALUES ('TEMP-01', NOW, 25.3);

-- TAG 메타데이터 삽입
INSERT INTO tag METADATA VALUES ('TEMP-01', 'zone-1', 'R&D');

-- RDB 테이블 삽입
INSERT INTO orders (product, qty, status) VALUES ('Widget', 10, 'PENDING');

-- VOLATILE 테이블 삽입
INSERT INTO device_status VALUES ('DEV-01', 'NORMAL', 23.5, NOW);

-- LOOKUP 테이블 삽입
INSERT INTO alarm_threshold VALUES ('TEMP-01', 85.0, 5.0);
```

#### NOW 키워드

`NOW`는 현재 서버 시각을 나타냅니다. DATETIME 타입 컬럼에 사용합니다.

```sql
INSERT INTO sensor_log VALUES ('TEMP-01', NOW, 25.3);
```

#### INSERT SELECT

다른 테이블이나 쿼리 결과를 삽입합니다.

```sql
-- 테이블 간 데이터 복사
INSERT INTO archive_log SELECT * FROM sensor_log;

-- 조건부 복사
INSERT INTO error_log
SELECT sensor_id, ts, value FROM sensor_log WHERE value > 100.0;

-- _ARRIVAL_TIME을 보존하여 복사
INSERT INTO archive_log (_arrival_time, sensor_id, ts, value)
SELECT _arrival_time, sensor_id, ts, value FROM sensor_log;
```

##### INSERT SELECT 주의사항

- `_ARRIVAL_TIME` 컬럼을 명시하지 않으면 INSERT 실행 시점의 시각이 자동 부여됩니다.
- `_ARRIVAL_TIME`을 명시한 경우, 지정값이 테이블에 이미 존재하는 가장 최신 `_ARRIVAL_TIME`보다 이전이면 해당 행은 입력되지 않습니다.
- 수행 중 오류가 발생해도 ROLLBACK되지 않습니다 (부분 성공 가능).
- VARCHAR 컬럼의 최대 길이를 초과하는 값은 자동으로 잘립니다.
- 형 변환이 필요한 경우 묵시적 변환이 적용됩니다. 변환 불가 시 해당 행은 건너뜁니다.

#### INSERT ON DUPLICATE KEY UPDATE (UPSERT)

PRIMARY KEY가 지정된 VOLATILE 또는 LOOKUP 테이블에서 PK 중복 시 자동 UPDATE되는 구문입니다.

```sql
-- PK 중복 없으면 INSERT, 있으면 UPDATE
INSERT INTO device_status VALUES ('DEV-01', 'ALARM', 95.3, NOW)
ON DUPLICATE KEY UPDATE SET status = 'ALARM', value = 95.3, updated_at = NOW;

-- SET 절로 삽입값과 다른 값 업데이트
INSERT INTO device_status VALUES ('DEV-02', 'NORMAL', 23.5, NOW)
ON DUPLICATE KEY UPDATE SET status = 'NORMAL', value = 24.0, updated_at = NOW;

-- LOOKUP 테이블에서도 PK 기준으로 UPSERT 가능
INSERT INTO alarm_threshold VALUES ('TEMP-01', 85.0, 5.0)
ON DUPLICATE KEY UPDATE SET high_limit = 85.0, low_limit = 5.0;
```

`SET` 절에는 갱신할 값을 명시합니다. 현재 빌드에서는 `value = value + 1`처럼 기존 값을
참조해 계산하는 UPSERT 표현식을 사용할 수 없습니다.

#### 다건 입력

```sql
-- SQL INSERT는 행 단위로 실행합니다.
INSERT INTO sensor_log VALUES ('TEMP-01', NOW, 25.3);
INSERT INTO sensor_log VALUES ('TEMP-02', NOW, 27.1);
INSERT INTO sensor_log VALUES ('TEMP-03', NOW, 22.8);
```

대량 입력에는 Append API, machloader, `LOAD DATA INFILE`을 사용합니다.

#### machsql에서 사용

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
Mach> INSERT INTO sensor_log VALUES ('TEMP-01', NOW, 25.3);
1 row(s) inserted.
```

<a id="sql-append"></a>

### Append API

Machbase SDK가 제공하는 대량 입력 인터페이스입니다. SQL INSERT와 달리 내부 버퍼에 데이터를 모아 배치 전송하므로, TAG/LOG 테이블에서 높은 처리량을 달성합니다.

#### Append API 특징

- **고속 입력 경로**: TAG/LOG 테이블에서 비트랜잭션 버퍼 기반으로 동작
- **버퍼 기반**: 내부 버퍼에 데이터를 누적하다가 `Close()` 또는 버퍼 플러시 시 서버로 전송
- **테이블 타입**: TAG, LOG, VOLATILE, LOOKUP에서 사용 가능. RDB는 지원되는 client API의 appendBatch 또는 append stream 경로로 사용
- **열 순서 고정**: 테이블 컬럼 순서대로 값을 전달

#### Go SDK 예시

```go
package main

import (
    "context"
    "database/sql"
    _ "github.com/machbase/neo-client/driver"
)

func main() {
    db, _ := sql.Open("machbase", "server=127.0.0.1;port=5656;user=SYS;password=MANAGER")
    conn, _ := db.Conn(context.Background())
    defer conn.Close()

    // Appender 생성
    appender, err := conn.AppendContext(context.Background(), "sensor_log")
    if err != nil {
        panic(err)
    }

    // 대량 데이터 입력
    for i := 0; i < 1_000_000; i++ {
        appender.Append("TEMP-01", time.Now(), float64(i)*0.01)
    }

    // 버퍼 플러시 및 완료
    successCount, failCount, err := appender.Close()
    // successCount: 성공 건수, failCount: 실패 건수
}
```

#### Python SDK 예시

```python
import machbasedb

conn = machbasedb.connect(host="127.0.0.1", port=5656, user="SYS", password="MANAGER")

with conn.appender("sensor_log") as app:
    for i in range(1_000_000):
        app.append("TEMP-01", time.time_ns(), i * 0.01)
# with 블록 종료 시 자동 Close (플러시)
```

#### C SDK 예시 (개념)

```c
// Appender 열기
MCH_APPENDER *appender;
MCHOpenAppender(hEnv, hConn, "sensor_log", &appender);

// 데이터 추가
MCHAppendData(appender, "TEMP-01", timestamp_ns, 25.3);

// 완료
MCHCloseAppender(appender, &successCnt, &failCnt);
```

#### Append API vs SQL INSERT 비교

| 항목 | Append API | SQL INSERT |
|------|-----------|-----------|
| 처리량 | TAG/LOG에서 수백만 건/초 수준 | 수천~수만 건/초 |
| 트랜잭션 | TAG/LOG는 비트랜잭션, RDB는 batch 실행 구간에서 트랜잭션 처리 | O |
| 오류 처리 | 실패 행 건너뜀 | 행별 오류 반환 |
| 사용 테이블 | TAG, LOG, VOLATILE, LOOKUP, RDB(client append API) | 모든 테이블 |
| 사용 방법 | SDK 필요 | SQL 클라이언트 |

#### REST API Append

REST API를 통한 Append도 동일한 고속 경로를 사용합니다. 상세는 [8장 애플리케이션 연동](/dbms/application-integration/)을 참고하세요.

#### 주의사항

- `Close()` 를 반드시 호출해야 내부 버퍼가 플러시됩니다. 호출하지 않으면 데이터 유실이 발생합니다.
- 대량 Append 중 서버 재시작 등의 이유로 연결이 끊기면 버퍼에 남은 데이터는 손실될 수 있습니다.
- RDB 테이블에는 일반 SQL `APPEND INTO` 문법을 사용하지 않습니다. RDB 대량 입력은 지원되는 client API의 appendBatch 또는 append stream 경로를 사용합니다.

<a id="sql-load-data-infile-fastload"></a>

### LOAD DATA INFILE

**서버에 위치한** CSV 파일을 SQL 한 줄로 직접 적재하는 구문입니다. machloader와 달리 서버 프로세스가 직접 파일을 읽습니다.

#### 기본 구문

```sql
LOAD DATA INFILE 'file_path'
INTO TABLE table_name
[AUTO {BULKLOAD | HEADUSE | HEADUSE_ESCAPE}]
[(FIELDS | COLUMNS) [TERMINATED BY 'char'] [ENCLOSED BY 'char']]
[LINES TERMINATED BY 'char']
[TRIM {ON | OFF}]
[IGNORE number LINES]
[MAX_LINE_LENGTH number]
[ENCODED BY coding_name]
[ON ERROR {STOP | IGNORE}];
```

#### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `AUTO BULKLOAD` | 한 행 전체를 하나의 컬럼으로 입력 (컬럼 구분 없는 원시 데이터) |
| `AUTO HEADUSE` | CSV 첫 줄을 컬럼명으로 사용하여 자동 테이블 생성 |
| `AUTO HEADUSE_ESCAPE` | HEADUSE와 동일하나, 예약어·특수문자 컬럼명에 `_` 처리 |
| `FIELDS TERMINATED BY` | 필드 구분자 (기본값: `,`) |
| `ENCLOSED BY` | 필드 감싸는 문자 (기본값: `"`) |
| `LINES TERMINATED BY` | 줄 구분자 |
| `TRIM ON/OFF` | 공백 제거 여부 (기본값: ON) |
| `IGNORE N LINES` | 첫 N줄 무시 (헤더 건너뛰기) |
| `MAX_LINE_LENGTH` | 한 줄 최대 길이 (기본값: 512KB) |
| `ENCODED BY` | 파일 인코딩 (기본값: UTF8) |
| `ON ERROR STOP/IGNORE` | 오류 시 중단 또는 건너뜀 (기본값: STOP) |

#### 예시

```sql
-- 기본: 기본 구분자(,)로 sensor_log 테이블에 입력
LOAD DATA INFILE '/data/sensor_2024.csv' INTO TABLE sensor_log;

-- 헤더 1줄 건너뛰기
LOAD DATA INFILE '/data/sensor_2024.csv' INTO TABLE sensor_log
IGNORE 1 LINES;

-- 탭 구분자
LOAD DATA INFILE '/data/sensor_2024.tsv' INTO TABLE sensor_log
FIELDS TERMINATED BY '\t';

-- 오류 발생 시 중단
LOAD DATA INFILE '/data/critical.csv' INTO TABLE orders
ON ERROR STOP;

-- 자동 테이블 생성 (첫 줄을 컬럼명으로)
LOAD DATA INFILE '/data/new_data.csv' INTO TABLE auto_table
AUTO HEADUSE;

-- 인코딩 지정
LOAD DATA INFILE '/data/korean.csv' INTO TABLE sensor_log
ENCODED BY MS949;
```

#### machsql에서 실행

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
Mach> LOAD DATA INFILE '/data/sensor_2024.csv' INTO TABLE sensor_log;
Load success count : 1000000
Load fail count    : 0
```

#### 클라이언트 적재 도구와 비교

| 항목 | LOAD DATA INFILE | machloader |
|------|-----------------|-----------|
| 파일 위치 | 서버 파일시스템 | 클라이언트 파일시스템 |
| 실행 방법 | SQL 구문 | CLI 명령 |
| 스키마 파일 | 불필요 | 필요 시 사용 |
| 자동 테이블 생성 | O (AUTO 옵션) | O (-C 옵션) |

#### 주의사항

- 파일 경로는 **Machbase 서버 프로세스**가 접근 가능한 경로여야 합니다.
- 원격 클라이언트에서 실행할 경우, 서버 로컬 경로를 기준으로 파일을 미리 복사해 두어야 합니다.
- 파일이 매우 클 경우 `MAX_LINE_LENGTH`를 적절히 늘려야 합니다.

<a id="file"></a>

## 파일 적재

CSV 파일을 클라이언트에서 서버로 전송하여 적재하는 CLI 도구입니다.

### 파일 적재 도구

| 도구 | 특징 | 주요 사용처 |
|------|------|-----------|
| `machloader` | 범용 적재/반출 도구. 스키마 파일로 유연한 매핑 | 배치 적재, 마이그레이션, 반출 |
| `csvimport` | machloader의 CSV 전용 래퍼. 옵션 단순화 | 빠른 CSV 적재 |
| `csvexport` | CSV 반출 전용 래퍼 | 빠른 CSV 반출 |
| `tagmetaimport` | TAG 메타데이터 전용 적재 | TAG 메타데이터 초기 로드·업데이트 |

### 이 절에서 다루는 내용

- **[CSV 파일 형식](/dbms/application-integration/data-input-load-export/#file-csv)**: Machbase가 인식하는 CSV 규격
- **[machloader로 가져오기](/dbms/application-integration/data-input-load-export/#import-machloader)**: 스키마 파일과 다양한 옵션 활용
- **[csvimport로 가져오기](/dbms/application-integration/data-input-load-export/#import-csvimport)**: 간편한 CSV 적재
- **[tagmetaimport](/dbms/application-integration/data-input-load-export/#metadata-import-tagmetaimport-tag)**: TAG 메타데이터 전용 임포트

<a id="file-file-csv"></a>

### CSV 파일 형식

machloader, csvimport, LOAD DATA INFILE이 인식하는 CSV 파일 형식입니다.

#### 기본 형식

- **구분자**: 콤마(`,`) — 기본값
- **필드 감싸기**: 쌍따옴표(`"`) — 선택사항
- **레코드 구분자**: 개행(`\n`)
- **인코딩**: UTF-8 — 기본값

```csv
TEMP-01,2024-01-15 10:00:00,25.3
TEMP-01,2024-01-15 10:01:00,25.7
TEMP-02,2024-01-15 10:00:00,22.1
```

#### 헤더 행

첫 줄을 컬럼명 헤더로 사용할 수 있습니다. 도구에서 `-H` 옵션으로 지정합니다.

```csv
sensor_id,ts,value
TEMP-01,2024-01-15 10:00:00,25.3
TEMP-02,2024-01-15 10:00:00,22.1
```

#### DATETIME 형식

DATETIME 컬럼의 값 형식은 machloader의 `-F` 옵션 또는 스키마 파일의 `DATEFORMAT`으로 지정합니다.

| 형식 | 설명 | 예시 |
|------|------|------|
| `YYYY-MM-DD HH24:MI:SS` | 표준 날짜시간 | `2024-01-15 10:00:00` |
| `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn` | 나노초 포함 | `2024-01-15 10:00:00 000:000:000` |
| `unixtimestamp` | Unix 타임스탬프 (초 단위) | `1705312800` |
| `nanotimestamp` | 나노초 단위 Unix 타임스탬프 | `1705312800000000000` |

#### NULL 표현

- 빈 필드는 NULL로 처리됩니다.
- `,,` 사이 빈 값은 NULL

```csv
TEMP-01,2024-01-15 10:00:00,
TEMP-02,,22.1
```

#### 특수 구분자

탭, 파이프(`|`), 캐럿(`^`) 등 다른 구분자를 사용할 경우 machloader에서 `-D` 옵션으로 지정합니다.

```bash
# 탭 구분 파일
machloader -i -d data.tsv -t sensor_log -D '\t'

# 파이프 구분 파일
machloader -i -d data.pipe -t sensor_log -D '|'
```

#### 지원 인코딩

`machloader`와 `csvimport`/`csvexport` 래퍼는 다음 인코딩을 사용할 수 있습니다.

| 코드 | 설명 |
|------|------|
| `UTF8` | UTF-8 (기본값) |
| `ASCII` | ASCII |
| `MS949` | Windows 한국어 |
| `KSC5601` | KS C 5601 |
| `EUCJP` | EUC-JP (일본어) |
| `SHIFTJIS` | Shift-JIS (일본어) |
| `BIG5` | Big5 (중국어 번체) |
| `GB231280` | GB2312 (중국어 간체) |
| `UTF16` | UTF-16 |

SQL `LOAD DATA INFILE`과 `SAVE DATA INTO`의 `ENCODED BY`는 `UTF8`, `MS949`, `KSC5601`,
`EUCJP`, `SHIFTJIS`, `BIG5`, `GB231280`을 지원합니다. SQL 구문에서는 `UTF16`을 지정하지 않습니다.

<a id="file-import-machloader"></a>

### machloader로 가져오기

CSV 파일을 Machbase 서버로 가져오거나 내보내는 범용 CLI 도구입니다. 스키마 파일로 컬럼 매핑, 날짜 형식, 특정 컬럼 무시 등을 세밀하게 제어할 수 있습니다.

#### 기본 가져오기

```bash
machloader -i -d data.csv -t sensor_log
```

| 옵션 | 설명 |
|------|------|
| `-i` | 가져오기 (import) 모드 |
| `-d data.csv` | 데이터 파일 지정 |
| `-t sensor_log` | 대상 테이블 이름 |

#### 자주 쓰는 옵션

```bash
# 접속 정보 지정
machloader -i -d data.csv -t sensor_log \
    -s 192.168.1.10 -P 5656 -u SYS -p MANAGER

# 헤더 행 건너뛰기
machloader -i -d data.csv -t sensor_log -H

# 로그/bad 파일 생성
machloader -i -d data.csv -t sensor_log \
    -l sensor_log.log -b sensor_log.bad

# 기존 데이터 삭제 후 입력 (replace 모드)
machloader -i -d data.csv -t sensor_log -m replace

# 탭 구분자
machloader -i -d data.tsv -t sensor_log -D '\t'

# 인코딩 지정
machloader -i -d data.csv -t sensor_log -E MS949

# _ARRIVAL_TIME 컬럼 포함
machloader -i -d data.csv -t sensor_log -a
```

#### DATETIME 형식 지정

`-F` 옵션으로 날짜 형식을 지정합니다.

```bash
# 컬럼명과 날짜 형식 지정
machloader -i -d data.csv -t sensor_log \
    -F "ts YYYY-MM-DD HH24:MI:SS"

# Unix 타임스탬프
machloader -i -d data.csv -t sensor_log \
    -F "ts unixtimestamp"

# 나노초 타임스탬프
machloader -i -d data.csv -t sensor_log \
    -F "ts nanotimestamp"
```

#### 스키마 파일 사용

스키마 파일로 컬럼 타입, 날짜 형식, 특정 컬럼 무시를 세밀하게 제어합니다.

##### 스키마 파일 자동 생성

```bash
machloader -c -t sensor_log -f sensor_log.fmt
```

##### 스키마 파일 형식

```text
table sensor_log
{
    sensor_id varchar(40);
    ts        datetime;
    value     double;
    status    varchar(20) IGNORE;  -- 이 컬럼은 CSV에 있지만 무시
}
DATEFORMAT ts "YYYY-MM-DD HH24:MI:SS"
```

##### 스키마 파일로 가져오기

```bash
machloader -i -f sensor_log.fmt -d data.csv
```

#### 자동 테이블 생성

테이블이 없을 때 자동 생성합니다. 컬럼 타입은 `varchar(32767)`로 생성됩니다.

```bash
# 컬럼명 c0, c1, ... 자동 생성
machloader -i -d data.csv -t auto_table -C

# CSV 헤더를 컬럼명으로 사용
machloader -i -d data.csv -t auto_table -C -H
```

#### 옵션 전체 목록

```bash
machloader -h
```

| 주요 옵션 | 설명 |
|----------|------|
| `-s SERVER` | 서버 IP (기본: 127.0.0.1) |
| `-u USER` | 사용자 (기본: SYS) |
| `-p PASSWORD` | 비밀번호 (기본: MANAGER) |
| `-P PORT` | 포트 (기본: 5656) |
| `-i` | 가져오기 모드 |
| `-o` | 내보내기 모드 |
| `-d FILE` | 데이터 파일 |
| `-f FILE` | 스키마 파일 |
| `-t TABLE` | 테이블 이름 |
| `-l FILE` | 로그 파일 |
| `-b FILE` | 실패 행 기록 파일 |
| `-m MODE` | append(기본)/replace |
| `-D CHAR` | 필드 구분자 |
| `-e CHAR` | 필드 감싸기 문자 |
| `-H` | 헤더 행 처리 |
| `-C` | 자동 테이블 생성 |
| `-a` | `_ARRIVAL_TIME` 포함 |
| `-E ENCODING` | 파일 인코딩 |
| `-F DATEFORMAT` | 날짜 형식 지정 |
| `-z TIMEZONE` | 타임존 (예: +0900) |

#### LOAD DATA INFILE (SQL 구문)

machsql이나 JDBC/ODBC에서 직접 SQL로 CSV 파일을 가져올 수 있습니다.

##### 문법

```sql
LOAD DATA INFILE 'file_name'
INTO TABLE table_name
[TABLESPACE tbs_name]
[AUTO (BULKLOAD | HEADUSE | HEADUSE_ESCAPE)]
[(FIELDS | COLUMNS) [TERMINATED BY 'char'] [ENCLOSED BY 'char']]
[LINES TERMINATED BY 'char']
[TRIM (ON | OFF)]
[IGNORE number LINES]
[MAX_LINE_LENGTH number]
[ENCODED BY coding_name]
[ON ERROR (STOP | IGNORE)];
```

##### 옵션 설명

| 옵션 | 설명 |
|------|------|
| `AUTO BULKLOAD` | 한 행을 하나의 컬럼으로 입력. 컬럼 구분이 불필요한 원시 데이터에 사용 |
| `AUTO HEADUSE` | 파일의 첫 번째 줄을 컬럼명으로 사용하여 테이블 자동 생성 |
| `AUTO HEADUSE_ESCAPE` | HEADUSE와 동일하나 예약어 충돌을 피하기 위해 컬럼명 앞뒤에 `_` 추가, 특수문자는 `_`로 치환 |
| `FIELDS TERMINATED BY 'char'` | 필드 구분자 지정 (기본값: `,`) |
| `ENCLOSED BY 'char'` | 필드 감싸기 문자 지정 (기본값: `"`) |
| `LINES TERMINATED BY 'char'` | 줄 구분자 지정 |
| `TRIM (ON\|OFF)` | 공백 제거 여부. 기본값 ON |
| `IGNORE n LINES` | 처음 n줄 무시 (헤더 건너뛰기에 사용) |
| `MAX_LINE_LENGTH n` | 한 줄의 최대 길이 지정. 기본값 512K |
| `ENCODED BY` | 파일 인코딩 지정: UTF8(기본), MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280 |
| `ON ERROR STOP\|IGNORE` | 오류 발생 시 중단(STOP) 또는 해당 줄 건너뛰기(IGNORE). 기본값 STOP |

##### 예시

```sql
-- 기본 CSV 입력 (쉼표 구분자, 큰따옴표 감싸기)
LOAD DATA INFILE '/tmp/aaa.csv' INTO TABLE sample_data;

-- 한 줄을 하나의 컬럼으로 입력
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE newtable AUTO BULKLOAD;

-- 첫 번째 줄을 컬럼명으로 사용하여 테이블 자동 생성
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE newtable AUTO HEADUSE;

-- 첫 번째 줄 무시, 세미콜론 구분자, 작은따옴표 감싸기, 오류 무시
LOAD DATA INFILE '/tmp/ccc.csv' INTO TABLE sample_data
FIELDS TERMINATED BY ';' ENCLOSED BY '\''
IGNORE 1 LINES ON ERROR IGNORE;

-- EUC-KR 인코딩 파일 입력
LOAD DATA INFILE '/tmp/data_kr.csv' INTO TABLE sample_data
ENCODED BY MS949;
```

> AUTO 옵션을 사용하지 않는 경우, 대상 테이블의 모든 컬럼은 VARCHAR 또는 TEXT 타입으로 생성되어 있어야 합니다.

<a id="file-import-csvimport"></a>

### csvimport로 가져오기

machloader를 CSV에 특화하여 래핑한 도구로, 옵션을 간소화하여 빠르게 적재할 수 있습니다.

#### 기본 사용법

```bash
# 기본 형식
csvimport -t table_name -d data.csv

# 테이블명과 파일명을 위치 인자로 지정
csvimport table_name data.csv
csvimport data.csv table_name
```

#### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-t TABLE` | 대상 테이블 이름 |
| `-d FILE` | CSV 데이터 파일 |
| `-H` | 첫 줄을 헤더로 인식하여 입력 제외 |
| `-C` | 테이블 없으면 자동 생성 (컬럼명: c0, c1, ...) |
| `-m MODE` | append(기본)/replace |
| `-b FILE` | 실패 행 기록 파일 |
| `-l FILE` | 실행 로그 파일 |
| `-a` | `_ARRIVAL_TIME` 컬럼 포함 |
| `-P PORT` | 서버 포트 (기본: 5656) |
| `-F DATEFORMAT` | 날짜 형식 |
| `-I` | 상태 출력 최소화 |

#### 예시

```bash
# 기본 적재
csvimport -t sensor_log -d sensor_data.csv

# 헤더 행 제외
csvimport -t sensor_log -d sensor_data.csv -H

# 오류 로그 저장
csvimport -t sensor_log -d sensor_data.csv \
    -l import.log -b import.bad

# 테이블 자동 생성 (헤더를 컬럼명으로)
csvimport -t new_table -d data.csv -C -H

# replace 모드 (기존 데이터 삭제 후 삽입)
csvimport -t sensor_log -d data.csv -m replace

# 날짜 형식 지정
csvimport -t sensor_log -d data.csv \
    -F "ts YYYY-MM-DD HH24:MI:SS"
```

#### machloader와의 차이

`csvimport`는 `machloader -i`의 간편 래퍼입니다. machloader의 모든 옵션(`-D`, `-e`, `-f`, `-E` 등)을 그대로 사용할 수 있습니다.

```bash
# csvimport에서 machloader 확장 옵션 사용
csvimport -t sensor_log -d data.tsv -D '\t'
csvimport -t sensor_log -d data.csv -E MS949
```

<a id="export"></a>

## 데이터 반출

테이블 데이터를 파일로 내보내는 방법입니다.

### 반출 방법 개요

| 방법 | 특징 |
|------|------|
| `SAVE DATA INTO` | SQL 구문으로 SELECT 결과를 서버 측 파일로 직접 저장 |
| `machloader -o` | CLI 도구. 스키마 파일 지원. 클라이언트 파일시스템에 저장 |
| `csvexport` | machloader 내보내기 래퍼. 간편 CSV 반출 |

### 이 절에서 다루는 내용

- **[반출 작업 소유권](/dbms/application-integration/data-input-load-export/#export-ownership)**: 반출 파일 권한 관리
- **[SAVE DATA INTO](/dbms/application-integration/data-input-load-export/#export-sql-save-data-into)**: SQL 기반 서버 측 파일 저장
- **[machloader로 내보내기](/dbms/application-integration/data-input-load-export/#export-machloader)**: CLI 기반 반출
- **[csvexport로 내보내기](/dbms/application-integration/data-input-load-export/#export-csvexport)**: 간편 CSV 반출

<a id="export-export-ownership"></a>

### 데이터 반출 작업 소유권

반출 시 생성되는 파일의 소유권(ownership)에 관한 내용입니다.

#### SAVE DATA INTO 파일 소유권

`SAVE DATA INTO` 구문으로 생성되는 파일은 **Machbase 서버 프로세스 계정**이 소유합니다. 일반적으로 `mach` 또는 Machbase를 실행한 시스템 사용자 계정입니다.

```sql
SAVE DATA INTO '/data/export/result.csv' AS SELECT * FROM sensor_log;
-- 파일 소유자: machbase 서버 프로세스 계정
```

파일을 다른 사용자가 읽어야 하는 경우, 서버 관리자가 적절한 파일 퍼미션을 설정해야 합니다.

#### machloader / csvexport 파일 소유권

`machloader -o` 또는 `csvexport`는 클라이언트 프로세스가 파일을 생성합니다. 따라서 **클라이언트를 실행한 사용자**가 파일 소유권을 갖습니다.

```bash
# machloader를 실행한 OS 사용자가 파일 소유자
machloader -o -d /home/user/export.csv -t sensor_log
```

#### 반출 디렉터리 권한 확인

`SAVE DATA INTO` 사용 시 대상 디렉터리에 Machbase 서버 프로세스가 쓰기 권한을 가져야 합니다.

```bash
# 반출 디렉터리 권한 확인
ls -la /data/export/

# 서버 프로세스 계정(예: mach)에 쓰기 권한 부여
chown mach:mach /data/export/
chmod 755 /data/export/
```

#### 접근 권한 모범 사례

- 반출 디렉터리를 Machbase 서버 계정이 쓸 수 있는 전용 경로로 지정
- 민감한 데이터 반출 시 파일 퍼미션(600 또는 640)을 엄격하게 관리
- 정기 반출 작업의 경우 전용 서비스 계정을 사용하여 실행

<a id="export-export-sql-save-data-into"></a>

### SQL 기반 반출: SAVE DATA INTO

SELECT 결과를 **서버 측 파일**로 직접 저장하는 SQL 구문입니다. machsql에서 실행하며 서버 프로세스가 파일을 생성합니다.

#### 구문

```text
SAVE DATA INTO 'file_path'
[HEADER ON|OFF]
[(FIELDS | COLUMNS) [TERMINATED BY 'char'] [ENCLOSED BY 'char']]
[ENCODED BY coding_name]
AS select_query;
```

#### 주요 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `HEADER ON/OFF` | OFF | 컬럼명 헤더 포함 여부 |
| `FIELDS TERMINATED BY` | `,` | 필드 구분자 |
| `ENCLOSED BY` | `"` | 필드 감싸기 문자 |
| `ENCODED BY` | UTF8 | 파일 인코딩 |

#### 예시

```sql
-- 기본: SELECT 결과를 CSV로 저장
SAVE DATA INTO '/data/export/sensor_2024.csv'
AS SELECT * FROM sensor_log;

-- 헤더 포함
SAVE DATA INTO '/data/export/sensor_2024.csv'
HEADER ON
AS SELECT sensor_id, ts, value FROM sensor_log;

-- 조건부 반출
SAVE DATA INTO '/data/export/high_temp.csv'
HEADER ON
AS SELECT name, time, value FROM tag
WHERE name = 'TEMP-01'
  AND time BETWEEN '2024-01-01' AND '2024-01-31';

-- 구분자 변경
SAVE DATA INTO '/data/export/data.tsv'
FIELDS TERMINATED BY '\t'
AS SELECT * FROM sensor_log;

-- 인코딩 및 구분자 지정
SAVE DATA INTO '/data/export/result.csv'
HEADER ON
FIELDS TERMINATED BY ';' ENCLOSED BY '\''
ENCODED BY MS949
AS SELECT * FROM sensor_log WHERE value > 100;
```

#### machsql에서 실행

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
Mach> SAVE DATA INTO '/data/export/result.csv' HEADER ON
   2> AS SELECT sensor_id, ts, value FROM sensor_log LIMIT 10000;
10000 row(s) saved.
```

#### 주의사항

- 파일 경로는 **서버 파일시스템** 기준입니다. 클라이언트 로컬 경로가 아닙니다.
- 기존 파일이 있으면 오류가 발생합니다. 새 파일 경로를 지정하거나 기존 파일을 먼저 삭제하세요.
- 서버 프로세스 계정에 해당 디렉터리 쓰기 권한이 필요합니다.
- 대용량 반출 시 디스크 여유 공간을 미리 확인하세요.

<a id="export-export-machloader"></a>

### machloader로 내보내기

`machloader -o` 옵션으로 테이블 데이터를 클라이언트 파일시스템의 CSV 파일로 내보냅니다.

#### 기본 내보내기

```bash
machloader -o -d export.csv -t sensor_log
```

| 옵션 | 설명 |
|------|------|
| `-o` | 내보내기 (export) 모드 |
| `-d export.csv` | 저장할 파일 이름 |
| `-t sensor_log` | 대상 테이블 이름 |

#### 주요 옵션

```bash
# 접속 정보 지정
machloader -o -d export.csv -t sensor_log \
    -s 192.168.1.10 -P 5656 -u SYS -p MANAGER

# 헤더 포함
machloader -o -d export.csv -t sensor_log -H

# _ARRIVAL_TIME 컬럼 포함
machloader -o -d export.csv -t sensor_log -a

# 탭 구분자
machloader -o -d export.tsv -t sensor_log -D '\t'

# 인코딩 지정
machloader -o -d export.csv -t sensor_log -E MS949

# 실행 로그
machloader -o -d export.csv -t sensor_log -l export.log
```

#### 스키마 파일과 함께 내보내기

컬럼 순서 변경이나 특정 컬럼만 내보낼 때 스키마 파일을 사용합니다.

```bash
# 스키마 파일 자동 생성
machloader -c -t sensor_log -f sensor_log.fmt

# 스키마 파일로 내보내기
machloader -o -f sensor_log.fmt -d export.csv
```

스키마 파일에서 `IGNORE` 키워드를 사용하여 특정 컬럼 제외:

```text
table sensor_log
{
    sensor_id varchar(40);
    ts        datetime;
    value     double;
    status    varchar(20) IGNORE;  -- 내보내기에서 제외
}
```

#### 결과 확인

```
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 8.6.0
Copyright 2014, MACHBASE Corporation or its subsidiaries.
All Rights Reserved.
-----------------------------------------------------------------
Export time : 0 hour 0 min 2.35 sec
Export success count : 1000000
```

#### 주의사항

- 파일은 클라이언트 실행 경로 또는 지정한 경로에 생성됩니다.
- 기존 파일이 있으면 덮어씁니다.
- 대용량 테이블을 내보낼 때는 `-I` 옵션(silent)으로 진행 출력을 줄일 수 있습니다.

<a id="export-export-csvexport"></a>

### csvexport로 내보내기

machloader의 CSV 반출 전용 래퍼입니다. 옵션을 간소화하여 빠르게 CSV로 내보냅니다.

#### 기본 사용법

```bash
# 기본 형식
csvexport -t table_name -d output.csv

# 위치 인자로 지정
csvexport table_name output.csv
csvexport output.csv table_name
```

#### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-t TABLE` | 내보낼 테이블 이름 |
| `-d FILE` | 저장할 CSV 파일 이름 |
| `-H` | 컬럼명을 CSV 헤더로 포함 |
| `-a` | `_ARRIVAL_TIME` 컬럼 포함 |
| `-l FILE` | 실행 로그 파일 |
| `-P PORT` | 서버 포트 (기본: 5656) |
| `-F DATEFORMAT` | 날짜 형식 |
| `-I` | 상태 출력 최소화 |

#### 예시

```bash
# 기본 반출
csvexport -t sensor_log -d sensor_log.csv

# 헤더 포함
csvexport -t sensor_log -d sensor_log.csv -H

# _ARRIVAL_TIME 포함
csvexport -t sensor_log -d sensor_log.csv -a

# 로그 파일 생성
csvexport -t sensor_log -d sensor_log.csv -l export.log

# 조용히 실행 (배치 스크립트 사용 시)
csvexport -t sensor_log -d sensor_log.csv -I
```

#### machloader와의 차이

`csvexport`는 `machloader -o`의 간편 래퍼입니다. machloader의 모든 옵션(`-D`, `-E`, `-f` 등)을 그대로 사용할 수 있습니다.

```bash
# csvexport에서 탭 구분자 사용
csvexport -t sensor_log -d export.tsv -D '\t'

# 특정 인코딩으로 내보내기
csvexport -t sensor_log -d export.csv -E MS949
```

<a id="error-handling"></a>

## 배치와 오류 처리

대량 데이터 입력의 배치 전략과 오류 처리 방법입니다.

### 이 절에서 다루는 내용

- **[Batch 입력](/dbms/application-integration/data-input-load-export/#batch)**: 대량 입력 시 배치 크기와 전략
- **[대량 입력 오류 처리](/dbms/application-integration/data-input-load-export/#error-handling-bulk)**: bad 파일, 오류 로그, 재시도 패턴

<a id="error-handling-batch"></a>

### Batch 입력

대량 데이터를 효율적으로 입력하기 위한 배치 전략입니다.

#### 배치 크기 선택

| 방법 | 권장 배치 크기 | 설명 |
|------|--------------|------|
| SQL INSERT (개별) | N/A | 건별 처리 |
| Append API | 10,000~100,000건 버퍼 | 내부 버퍼 자동 관리 |
| LOAD DATA INFILE | 제한 없음 | 파일 단위 처리 |
| machloader | 제한 없음 | 파일 단위 처리 |

#### Append API 배치 전략

Append API는 내부 버퍼에 데이터를 누적하다가 `Close()` 시 일괄 전송합니다.

```go
// Go SDK: 100만 건 배치 입력
appender, _ := conn.AppendContext(ctx, "sensor_log")
for i := 0; i < 1_000_000; i++ {
    appender.Append("TEMP-01", time.Now(), float64(i)*0.01)
}
// Close()에서 서버로 일괄 전송
success, fail, _ := appender.Close()
```

##### 멀티 Appender 병렬 입력

여러 goroutine/thread에서 각각 별도의 Appender를 사용하여 병렬 입력합니다.

```go
var wg sync.WaitGroup
for workerID := 0; workerID < 4; workerID++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        appender, _ := conn.AppendContext(ctx, "sensor_log")
        for i := 0; i < 250_000; i++ {
            appender.Append(fmt.Sprintf("TEMP-%02d", id), time.Now(), float64(i))
        }
        appender.Close()
    }(workerID)
}
wg.Wait()
```

#### SQL INSERT 배치 전략

SQL INSERT는 행 단위로 실행합니다. 대량 입력에는 Append API나 파일 적재 방식을 사용합니다.

```sql
CREATE VOLATILE TABLE batch_orders (
    order_id INTEGER PRIMARY KEY,
    product  VARCHAR(64),
    qty      INTEGER
);

INSERT INTO batch_orders VALUES (1, 'Widget', 10);
INSERT INTO batch_orders VALUES (2, 'Gadget', 5);
INSERT INTO batch_orders VALUES (3, 'Doohickey', 20);
```

#### machloader 배치 파일 분할

매우 큰 CSV 파일은 여러 파일로 분할하여 병렬 실행합니다.

```bash
# 파일 분할 (Linux)
split -l 1000000 large_data.csv chunk_

# 병렬 machloader 실행
for f in chunk_*; do
    machloader -i -d "$f" -t sensor_log -I &
done
wait
```

#### 시간대별 분할 로드

시계열 데이터는 시간 범위별로 분할하여 순서대로 적재하면 효율적입니다.

```bash
# 월별 파일 순서대로 적재
for month in 2024-01 2024-02 2024-03; do
    machloader -i -d "sensor_${month}.csv" -t sensor_log
done
```

<a id="error-handling-error-handling-bulk"></a>

### 대량 입력 오류 처리

대량 입력 중 발생할 수 있는 오류 유형과 처리 방법입니다.

#### 오류 유형

| 오류 유형 | 원인 | 처리 방법 |
|----------|------|---------|
| 타입 불일치 | CSV 값이 컬럼 타입과 맞지 않음 | bad 파일로 분리, 전처리 후 재시도 |
| VARCHAR 초과 | 값이 컬럼 최대 길이 초과 | 자동 잘림 또는 오류 기록 |
| NULL 제약 위반 | NOT NULL 컬럼에 NULL 값 | bad 파일로 분리 |
| 중복 PK | LOOKUP/VOLATILE에서 PK 중복 | UPSERT 또는 사전 정리 |
| 날짜 형식 오류 | DATETIME 파싱 실패 | `-F` 옵션으로 형식 명시 |

#### machloader: bad 파일과 로그 파일

```bash
machloader -i -d data.csv -t sensor_log \
    -b sensor_log.bad \
    -l sensor_log.log
```

- **bad 파일 (`-b`)**: 실패 행과 진단 정보를 기록
- **로그 파일 (`-l`)**: 실패 행의 오류 메시지를 기록

```bash
# 실행 후 결과 확인
# sensor_log.log 예시:
# Row 15: Type mismatch on column 'value'
# Row 42: NULL value in NOT NULL column 'sensor_id'

# bad 파일에서 실패 원인과 원본 행을 확인한 뒤 데이터만 추출/수정해 재시도
vi sensor_log.bad
machloader -i -d sensor_log_fixed.csv -t sensor_log
```

#### LOAD DATA INFILE: ON ERROR 옵션

```sql
-- 오류 발생 시 중단 (기본값)
LOAD DATA INFILE '/data/sensor.csv' INTO TABLE sensor_log
ON ERROR STOP;

-- 오류 발생 시 해당 행 건너뛰고 계속 진행
LOAD DATA INFILE '/data/sensor.csv' INTO TABLE sensor_log
ON ERROR IGNORE;
```

#### Append API: 실패 건수 확인

```go
success, fail, err := appender.Close()
if fail > 0 {
    log.Printf("Input failed: %d rows", fail)
    // 실패 행 재처리 로직
}
```

Append API는 실패한 개별 행에 대한 상세 오류 정보를 반환하지 않습니다. 실패 건수가 많을 경우 배치 크기를 줄이거나 SQL INSERT로 전환하여 오류를 추적하세요.

#### INSERT SELECT 오류 처리

INSERT SELECT는 중간에 오류가 발생해도 ROLLBACK되지 않습니다.

```sql
-- 오류가 있어도 성공한 행은 유지됨
INSERT INTO archive_log
SELECT * FROM sensor_log WHERE ts < '2024-01-01';

-- 오류 확인
SELECT COUNT(*) FROM archive_log;
```

#### 재시도 패턴

```bash
# bad 파일 오류 수정 후 재시도
# 1. bad 파일 검토
head -20 sensor_log.bad

# 2. 진단 텍스트를 제외하고 원본 데이터 행만 추출한 뒤 수정
awk '/^[^:]+,[^:]+/ { print }' sensor_log.bad > sensor_log_retry.csv
sed 's/incorrect_value/correct_value/' sensor_log_retry.csv > sensor_log_fixed.csv

# 3. 수정된 파일 재시도
machloader -i -d sensor_log_fixed.csv -t sensor_log \
    -b sensor_log_fixed.bad -l sensor_log_fixed.log
```

#### 입력 검증 권장 사항

- 대량 입력 전에 소량 샘플로 테스트 입력을 수행하세요.
- DATETIME 형식은 `-F` 옵션 또는 스키마 파일로 명시적으로 지정하세요.
- VARCHAR 컬럼 길이를 사전에 확인하고 데이터를 전처리하세요.
- bad 파일을 반드시 지정하여 실패 데이터를 보존하세요.
