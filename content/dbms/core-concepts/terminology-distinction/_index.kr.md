---
type: docs
title: '2.5 용어 구분'
weight: 50
toc: true
---
운영에서 자주 혼동되는 개념 쌍들을 비교 표와 함께 구분합니다. 각 항목은 "어떤 상황에 무엇을 선택하는가"에 초점을 맞추었습니다.

- **[ROLLUP vs STREAM](/dbms/core-concepts/terminology-distinction/#rollup-vs-stream)** -- 자동 집계와 SQL 기반 변환 처리의 차이
- **[Retention vs DELETE / TRUNCATE](/dbms/core-concepts/terminology-distinction/#retention-vs-delete-truncate)** -- 자동 정책과 수동 삭제 명령의 차이
- **[Backup vs Restore vs Mount](/dbms/core-concepts/terminology-distinction/#backup-vs-restore-mount)** -- 데이터 복사, 복원, 읽기 전용 연결의 차이
- **[machloader vs csvimport / csvexport vs tagmetaimport](/dbms/core-concepts/terminology-distinction/#machloader-vs-csvimport-csvexport-tagmetaimport)** -- 파일 기반 입출력 도구들의 차이
- **[LOAD DATA INFILE vs machloader](/dbms/core-concepts/terminology-distinction/#load-data-infile-vs-machloader)** -- 서버 파일 SQL 적재와 클라이언트 파일 도구의 차이
- **[SDK append vs SQL APPEND vs Collector 수집](/dbms/core-concepts/terminology-distinction/#ingestion-sdk-append-vs-sql-collector)** -- 실시간 데이터 수집 경로별 특성과 선택 기준


<a id="rollup-vs-stream"></a>

## ROLLUP vs STREAM

ROLLUP과 STREAM은 모두 데이터를 자동으로 변환한다는 점에서 비슷해 보이지만, 적용 대상·동작 방식·유연성이 근본적으로 다릅니다.

### 비교 표

| 항목 | ROLLUP | STREAM |
| --- | --- | --- |
| 적용 대상 | TAG 테이블 전용 | 임의 테이블 (LOG, TAG, LOOKUP 등) |
| 집계 단위 | SEC / MIN / HOUR 고정 | 사용자가 SQL로 자유롭게 정의 |
| 변환 로직 | 고정 (SUM, COUNT, MIN, MAX, FIRST, LAST) | 임의 SQL (조인, 조건 필터, 문자열 변환 등) |
| 결과 저장 위치 | `_TAG_ROLLUP_SEC`, `_TAG_ROLLUP_MIN`, `_TAG_ROLLUP_HOUR` | 사용자가 지정한 대상 테이블 |
| 설정 방법 | `WITH ROLLUP` 절로 테이블 생성 시 지정 | `EXEC STREAM_CREATE`로 별도 생성 |
| 트리거 방식 | 데이터 입력 시 자동 | 스트림 시작 후 입력 흐름에 따라 자동 실행 |
| Cluster Edition 지원 | 지원 | 제한적 지원 |
| 조회 방법 | `rollup()` 함수 사용 | 대상 테이블에 직접 SELECT |

### ROLLUP을 선택하는 경우

- 장기간의 TAG 계측값에서 SEC/MIN/HOUR 단위 집계를 반복 조회하는 경우
- 대시보드나 모니터링 화면에서 최솟값/최댓값/평균/합계를 실시간 표시해야 하는 경우
- 설정이 단순하고 추가 관리 부담 없이 자동 집계를 원하는 경우

```sql
-- ROLLUP 활성화
CREATE TAG TABLE rollup_sensor_values_cmp (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);

-- 분 단위 평균 조회
SELECT rollup('min', 1, time) AS mtime, AVG(value) AS avg_value
FROM rollup_sensor_values_cmp
WHERE name = 'temp_01'
GROUP BY mtime;
```

### STREAM을 선택하는 경우

- LOG 테이블의 이벤트를 특정 조건으로 필터링해 TAG 테이블에 계측값 형태로 변환해야 하는 경우
- SEC/MIN/HOUR가 아닌 사용자 정의 시간 구간(예: 15분, 30분)으로 집계해야 하는 경우
- 조인이나 복잡한 변환 로직이 필요한 경우
- 특정 임계값 초과 시 알림용 파생 테이블을 자동 업데이트해야 하는 경우

```sql
-- LOG -> TAG 변환 STREAM 예시
EXEC STREAM_CREATE(error_count_stream,
    'INSERT INTO error_stats SELECT ''ERROR_EVENT'', _arrival_time, value FROM device_log WHERE severity = ''ERROR''');

EXEC STREAM_START(error_count_stream);
```

### 두 기능을 함께 사용하는 패턴

STREAM으로 LOG 테이블의 이벤트를 TAG 테이블로 변환한 뒤, 해당 TAG 테이블에 ROLLUP을 활성화하는 것도 일반적인 패턴입니다. STREAM이 정제된 데이터를 TAG 테이블에 적재하고, ROLLUP이 시간 단위로 자동 집계합니다.

### 다음 읽을 내용

- [ROLLUP 통계의 역할](/dbms/core-concepts/features-concepts/#role-statistics-rollup) -- ROLLUP 상세 개념
- [STREAM 처리 모델](/dbms/core-concepts/features-concepts/#processing-model-stream) -- STREAM 상세 개념

<a id="retention-vs-delete-truncate"></a>

## Retention vs DELETE / TRUNCATE

데이터를 삭제하는 방법은 세 가지이며, 각각 목적과 동작 방식이 다릅니다.

### 비교 표

| 항목 | Retention Policy | DELETE | TRUNCATE |
| --- | --- | --- | --- |
| 실행 방식 | 자동 (배경 스레드) | 수동 (SQL 실행 시) | 수동 (SQL 실행 시) |
| 삭제 범위 | 보관 기간 초과 데이터 자동 판단 | 테이블 타입별 DELETE 조건 기반 | 테이블 전체 데이터 |
| 지속성 | 지속적 (설정 후 계속 자동 실행) | 일회성 | 일회성 |
| 대상 테이블 | LOG, TAG | LOG, TAG, LOOKUP, VOLATILE, RDB | LOG, RDB |
| 운영 중 실행 | 가능 (무중단) | 가능 | 가능 |
| 설정 방법 | `CREATE RETENTION` + `ALTER TABLE` | `DELETE FROM ...` | `TRUNCATE TABLE` |

### Retention Policy: 자동 기간 기반 삭제

보관 기간을 정책으로 설정하면 이후 자동으로 기간이 지난 데이터를 삭제합니다. 운영 중에도 중단 없이 배경에서 실행됩니다.

```sql
-- 60일 보관 정책 생성 및 적용
CREATE RETENTION keep_60days DURATION 60 DAY INTERVAL 1 DAY;
ALTER TABLE device_log ADD RETENTION keep_60days;

-- 정책 해제
ALTER TABLE device_log DROP RETENTION;

-- 정책 삭제
DROP RETENTION keep_60days;
```

데이터가 계속 쌓이는 운영 시스템에서 저장 공간을 자동 관리할 때 사용합니다.

### DELETE: 조건 기반 수동 삭제

SQL 문장을 직접 실행해 특정 조건에 맞는 데이터를 즉시 삭제합니다. LOG 테이블은 `BEFORE`,
`OLDEST`, `EXCEPT` 같은 로그 보존형 DELETE를, TAG 테이블은 태그 이름과 축 조건 또는 `BEFORE`
조건을 사용합니다. LOOKUP과 VOLATILE 테이블은 Primary key equality 조건을, RDB 테이블은
일반 `WHERE` 조건을 사용합니다. LOOKUP의 조건 없는 DELETE는 모든 행을 삭제합니다.

```sql
-- LOG 테이블에서 특정 시각 이전 삭제
DELETE FROM device_log BEFORE TO_DATE('2026-01-01', 'YYYY-MM-DD');

-- TAG 테이블에서 특정 태그의 특정 시간 범위 삭제
DELETE FROM sensor_values
WHERE name = 'temp_sensor_01'
  AND time >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
  AND time <  TO_DATE('2026-02-01', 'YYYY-MM-DD');
```

잘못 입력된 데이터 구간 제거나 오래된 데이터의 일부를 즉시 제거할 때 사용합니다.

### TRUNCATE: 테이블 전체 즉시 삭제

지원 대상 테이블의 모든 데이터를 즉시 삭제합니다. WHERE 조건 없이 한 줄로 전체 데이터가 제거됩니다. LOG 테이블과 RDB 테이블에 사용합니다.

```sql
TRUNCATE TABLE device_log;
```

개발·테스트 환경에서 테이블을 초기 상태로 되돌리거나, 운영 데이터를 전량 폐기할 때 사용합니다. 운영 테이블에서는 실수로 실행하지 않도록 주의하십시오.

### 선택 기준 요약

| 상황 | 권장 방법 |
| --- | --- |
| 장기 보관 정책 자동화 (30일, 90일 등) | Retention Policy |
| 특정 시간 구간 데이터 즉시 제거 | DELETE |
| 잘못 입력된 데이터 구간 재입력을 위한 삭제 | DELETE |
| LOG/RDB 테이블 전체 초기화 (개발/테스트) | TRUNCATE |
| LOG/RDB 테이블 전체 즉시 폐기 | TRUNCATE |

### 다음 읽을 내용

- [Retention Policy의 역할](/dbms/core-concepts/features-concepts/#role-retention-policy) -- Retention Policy 상세 개념
- [Backup vs Restore vs Mount](/dbms/core-concepts/terminology-distinction/#backup-vs-restore-mount) -- 데이터 보호 수단 비교

<a id="backup-vs-restore-mount"></a>

## Backup vs Restore vs Mount

Backup은 "복사본 만들기", Restore는 "복사본으로 되돌리기", Mount는 "복사본을 읽기 전용으로 들여다보기"입니다.

### 비교 표

| 항목 | Backup | Restore | Mount |
| --- | --- | --- | --- |
| 목적 | 데이터 복사본 생성 | 복사본으로 데이터베이스 복원 | 복사본을 읽기 전용으로 연결 |
| 서버 상태 | 운영 중 실행 가능 | 서버 중지 필요 | 운영 중 실행 가능 |
| 실행 방법 | SQL (`BACKUP DATABASE`) | `machadmin -r` 명령 | SQL (`MOUNT DATABASE`) |
| 결과 | 별도 디렉터리에 복사본 저장 | 원래 데이터 위치에 복원 | 현재 서버에 read-only 마운트 |
| 데이터 쓰기 | 불가 (Backup 대상은 운영 DB) | 복원 후 운영 DB로 재사용 | 불가 (read-only) |
| 주요 사용 목적 | 정기 백업, 마이그레이션 준비 | 장애 복구 | 과거 시점 데이터 조회/검증 |

### Backup

운영 중인 서버에서 SQL로 실행합니다.

```sql
-- 전체 백업
BACKUP DATABASE INTO DISK = '/data/backup/full_20260703';

-- 특정 테이블만 백업
BACKUP TABLE sensor_values INTO DISK = '/data/backup/sensor_20260703';
```

`LAUNCHED` -> `PROGRESS` -> `FINISHED` (실패 시 `ERROR`) 순서로 진행됩니다. `V$BACKUP_JOB` 뷰에서 진행 상황을 확인합니다.

### Restore

서버를 중지한 후 `machadmin` 명령으로 실행합니다. 복원 완료 후 서버를 재시작합니다.

```bash
# 서버 중지
machadmin -s stop

# 백업본으로 복원
machadmin -r /data/backup/full_20260703

# 서버 재시작
machadmin -s start
```

데이터 손상이나 장애 발생 후 마지막 백업 시점으로 되돌릴 때 사용합니다.

### Mount

운영 중인 서버에서 SQL로 실행합니다. 백업 디렉터리를 read-only로 연결해 SELECT 쿼리를 실행합니다.

```sql
-- 마운트
MOUNT DATABASE '/data/backup/full_20260703' TO BACKUP_VIEW;

-- 마운트된 데이터 조회
SELECT * FROM BACKUP_VIEW.sensor_values
WHERE time BETWEEN TO_DATE('2026-07-01', 'YYYY-MM-DD')
                AND TO_DATE('2026-07-02', 'YYYY-MM-DD');

-- 마운트 해제
UMOUNT DATABASE BACKUP_VIEW;
```

Restore와 달리 데이터를 원래 위치에 복원하지 않습니다. 백업 디렉터리를 그대로 참조하므로 디스크 공간을 추가로 사용하지 않고 과거 시점 데이터를 확인합니다.

### 사용 시나리오별 선택 기준

| 시나리오 | 권장 수단 |
| --- | --- |
| 정기적인 데이터 보호 | Backup (전체/증분) |
| 서버 장애, 데이터 손상 복구 | Restore |
| 과거 특정 시점 데이터 조회 및 검증 | Mount |
| 운영 서버 마이그레이션 | Backup -> 신규 서버에서 Restore |
| 특정 테이블만 과거 상태 확인 | Backup (테이블) -> Mount |
| 데이터 감사나 포렌식 조회 | Mount (운영 서버 영향 없음) |

### 다음 읽을 내용

- [Backup / Restore / Mount 개념](/dbms/core-concepts/features-concepts/#concepts-backup-restore-mount) -- 세 개념의 상세 설명
- [Retention vs DELETE / TRUNCATE](/dbms/core-concepts/terminology-distinction/#retention-vs-delete-truncate) -- 데이터 삭제 수단 비교

<a id="machloader-vs-csvimport-csvexport-tagmetaimport"></a>

## machloader vs csvimport / csvexport vs tagmetaimport

파일로 데이터를 적재하거나 내보내는 여러 도구가 있습니다. 이름이 비슷하지만 각 도구가 다루는 대상과 용도가 다릅니다.

### 비교 표

| 항목 | machloader | csvimport | csvexport | tagmetaimport |
| --- | --- | --- | --- | --- |
| 방향 | 입력 또는 반출 | 입력 전용 | 반출 전용 | 입력 전용 |
| 대상 테이블 | LOG, LOOKUP | LOG | 모든 테이블 | TAG (메타데이터) |
| 파일 형식 | CSV, 바이너리 등 | CSV | CSV | CSV |
| 적재 내용 | 행 데이터 | 행 데이터 | 행 데이터 | 태그 이름 및 속성 |
| 실행 위치 | 클라이언트 | 클라이언트 | 클라이언트 | 클라이언트 |
| 주요 특징 | 범용, 설정 파일 기반, 다양한 포맷 지원 | 단순 CSV 입력 | 단순 CSV 반출 | TAG 테이블 태그 목록 일괄 등록 |

### machloader

테이블 데이터를 파일에서 적재하거나 반출하는 범용 도구입니다. CSV뿐 아니라 다양한 구분자
형식을 지원하며, 스키마 파일로 컬럼 매핑, 구분자와 날짜 형식을 제어합니다. RDB 테이블은
사용자 컬럼을 명시한 스키마 파일을 사용합니다.

```bash
# 적재 예시
machloader -i -t device_log -d /data/device_events.csv -f /conf/device_log.mach

# 반출 예시
machloader -o -t device_log -d /data/export.csv -f /conf/device_log.mach
```

데이터 양이 많거나 파일 포맷이 복잡할 때, 또는 컬럼 매핑이 필요한 경우에 사용합니다.

### csvimport / csvexport

단순한 CSV 파일 입출력 도구입니다. machloader보다 옵션이 적고 사용법이 간단합니다.

```bash
# CSV 파일 적재
csvimport -t device_log -d /data/device_events.csv

# CSV 파일 반출
csvexport -t device_log -d /data/export.csv
```

소량 CSV를 빠르게 적재하거나 확인 목적으로 데이터를 내보낼 때 적합합니다. 복잡한 컬럼 매핑이나 변환이 필요하면 machloader를 사용하십시오.

### tagmetaimport

TAG 테이블의 태그 메타데이터(태그 이름과 사용자 정의 속성 컬럼 값)를 CSV 파일로 일괄 등록하는 도구입니다. 계측값 데이터(타임스탬프와 측정값)가 아니라 태그 목록과 그 속성을 등록합니다.

```bash
# TAG 테이블에 태그 메타데이터 일괄 등록
tagmetaimport -t sensor_values -d /data/tag_list.csv
```

수천 개의 센서를 처음 등록하거나, 공정 라인 추가로 새 태그를 대량 등록할 때 사용합니다. 개별 태그는 `INSERT INTO sensor_values (name) VALUES ('tag_name')`으로도 등록 가능하지만, 대량 등록에는 tagmetaimport가 효율적입니다.

### 선택 기준 요약

| 상황 | 권장 도구 |
| --- | --- |
| LOG 테이블에 CSV 대량 적재, 컬럼 매핑 필요 | machloader |
| LOG 테이블에 단순 CSV 소량 적재 | csvimport |
| 테이블 데이터 CSV 반출 | csvexport |
| TAG 테이블에 태그 이름/속성 일괄 등록 | tagmetaimport |
| 바이너리나 비CSV 포맷 파일 적재 | machloader |

### 다음 읽을 내용

- [LOAD DATA INFILE vs machloader](/dbms/core-concepts/terminology-distinction/#load-data-infile-vs-machloader) -- 파일 위치와 실행 주체에 따른 적재 방법 비교
- [SDK append vs SQL APPEND vs Collector 수집](/dbms/core-concepts/terminology-distinction/#ingestion-sdk-append-vs-sql-collector) -- 실시간 수집 경로 비교

<a id="load-data-infile-vs-machloader"></a>

## LOAD DATA INFILE vs machloader

`LOAD DATA INFILE`과 `machloader`는 모두 CSV 형식의 데이터를 입력하지만 파일을 읽는 위치와
실행 인터페이스가 다릅니다.

### 비교 표

| 항목 | LOAD DATA INFILE | machloader |
| --- | --- | --- |
| 실행 방식 | SQL 문장 | `machloader` 명령행 도구 |
| 파일 위치 | Machbase 서버가 접근할 수 있는 경로 | `machloader`를 실행하는 클라이언트 경로 |
| 연결 방식 | 서버가 파일을 직접 읽음 | 클라이언트가 서버에 접속해 데이터를 전송 |
| 형식 설정 | SQL 절로 구분자, 인코딩, 오류 정책 지정 | `-f`, `-D`, `-F`, `-E` 등의 옵션 사용 |
| 오류 확인 | SQL 오류와 `ON ERROR` 정책 | `-b` bad 파일과 `-l` 로그 파일 |
| 주요 용도 | 서버에 배치된 파일을 SQL 작업으로 적재 | 클라이언트 파일 가져오기와 내보내기 |

### LOAD DATA INFILE

서버가 지정된 파일 경로를 직접 읽어 테이블에 적재합니다. 파일은 Machbase 서버가 접근할 수
있는 경로에 있어야 합니다.

```sql
LOAD DATA INFILE '/data/device_events.csv'
INTO TABLE device_log
FIELDS TERMINATED BY ','
IGNORE 1 LINES
ON ERROR STOP;
```

SQL 클라이언트에서 일반 SQL처럼 실행할 수 있습니다. 클라이언트에만 있는 파일은 먼저 서버로
전송하거나 `machloader`를 사용합니다.

### machloader

`machloader`는 클라이언트의 텍스트 파일을 Machbase 테이블로 가져오거나 테이블 데이터를
파일로 내보내는 명령행 도구입니다.

```bash
machloader -i -s 127.0.0.1 -P 5656 \
  -u SYS -p MANAGER \
  -t sensor_values \
  -d /data/sensor_data.csv \
  -b /data/sensor_data.bad \
  -l /data/sensor_data.log
```

가져오기 전 소량의 샘플로 컬럼 순서, 데이터 타입과 날짜 형식을 확인합니다.

### 선택 기준

**LOAD DATA INFILE이 적합한 경우**

- 서버가 접근할 수 있는 경로에 입력 파일이 있는 경우
- 파일 적재를 SQL 작업으로 실행해야 하는 경우
- SQL의 형식·인코딩·오류 처리 절을 사용하려는 경우

**machloader가 적합한 경우**

- 클라이언트 파일을 서버 파일 시스템으로 복사하지 않고 적재하는 경우
- bad 파일과 실행 로그를 남겨 실패 행을 분리해야 하는 경우
- 가져오기와 내보내기를 같은 도구로 자동화하는 경우

### 다음 읽을 내용

- [machloader vs csvimport / csvexport vs tagmetaimport](/dbms/core-concepts/terminology-distinction/#machloader-vs-csvimport-csvexport-tagmetaimport) -- 파일 기반 입출력 도구 전체 비교
- [SDK append vs SQL APPEND vs Collector 수집](/dbms/core-concepts/terminology-distinction/#ingestion-sdk-append-vs-sql-collector) -- 실시간 수집 경로 비교

<a id="ingestion-sdk-append-vs-sql-collector"></a>

## SDK append vs SQL APPEND vs Collector 수집

실시간 데이터 수집 경로는 크게 세 가지입니다. 성능 요구사항, 데이터 소스 유형, 개발 비용에 따라 적합한 방법이 달라집니다.

### 비교 표

| 항목 | SDK APPEND | SQL INSERT | Collector |
| --- | --- | --- | --- |
| 수집 방식 | 언어별 SDK로 APPEND 프로토콜 직접 사용 | 표준 SQL INSERT 문장 | Machbase 내장 수집기, 별도 설정 파일 |
| 입력 특성 | 배치 전송, SQL 파싱 없음 | 행 단위 SQL 실행 | 설정 기반 버퍼링 |
| 지원 언어/환경 | Go, Python, .NET, C 등 | ODBC, JDBC, machsql 등 모든 SQL 클라이언트 | 파일, 소켓, ODBC, SFTP 등 소스 기반 |
| 개발 필요성 | 높음 (SDK API 구현 필요) | 낮음 (SQL 지식만으로 구현 가능) | 낮음 (설정 파일 작성) |
| 배치 처리 | 가능 (여러 행을 한 번에 전송) | 가능하나 비효율적 | 가능 (내부 버퍼링) |
| 소스 다양성 | 코드에서 직접 생성하는 데이터 | 코드에서 직접 생성하는 데이터 | 파일, 소켓, DB, SFTP 등 외부 소스 |
| 주요 사용 사례 | 고성능 수집기, 실시간 파이프라인 직접 구현 | 간단한 애플리케이션, 테스트, 저빈도 입력 | 외부 시스템 데이터 자동 수집 |

### SDK APPEND

Go, Python, .NET 등 언어별 SDK를 사용해 APPEND 프로토콜로 데이터를 전송합니다. 여러 행을
배치로 전달하므로 반복 SQL INSERT보다 네트워크 왕복과 파싱 횟수를 줄일 수 있습니다.

```go
// Go SDK APPEND 예시 (개념)
appender, _ := conn.Appender(ctx, "sensor_values")
defer appender.Close()

appender.Append("temp_sensor_01", time.Now(), 23.5)
appender.Append("temp_sensor_02", time.Now(), 21.0)
// Flush 시 배치로 전송
```

지속적인 대량 수집 파이프라인에 적합하며 SDK를 사용하는 코드를 직접 작성해야 합니다.

### SQL INSERT

표준 SQL `INSERT` 문장으로 데이터를 입력합니다. 모든 SQL 클라이언트에서 사용 가능해 범용성이 가장 높습니다.

```sql
INSERT INTO sensor_values (name, time, value)
VALUES ('temp_sensor_01', NOW, 23.5);
```

입력 빈도가 낮거나 별도 SDK 통합 없이 기존 애플리케이션에서 데이터를 입력할 때 적합합니다.
테스트나 운영 중 소량 데이터를 수동으로 넣을 때도 사용합니다.

### Collector

Machbase 내장 수집기입니다. 설정 파일을 작성하면 파일, 소켓, ODBC 소스, SFTP 등 외부 시스템에서 데이터를 자동으로 읽어 테이블에 적재합니다.

```ini
# Collector 설정 파일 예시 (개념)
[SOURCE]
type = file
path = /var/log/sensor/*.log

[DESTINATION]
table = device_log
```

외부 파일 시스템에서 로그를 주기적으로 읽거나 소켓으로 데이터를 수신하는 등 사전 정의된 소스 유형을 처리할 때 유용합니다. 소스 형식이 Collector 지원 유형이라면 개발 비용 없이 수집 파이프라인을 구성합니다.

### 선택 기준

| 상황 | 권장 방법 |
| --- | --- |
| 지속적인 대량 시계열 수집 | SDK APPEND |
| 기존 애플리케이션에서 소량 입력 | SQL INSERT |
| SDK 통합 없이 범용 SQL 클라이언트 사용 | SQL INSERT |
| 파일, 소켓 등 외부 소스에서 자동 수집 | Collector |
| 설정 파일만으로 수집 파이프라인 구성 | Collector |

### 다음 읽을 내용

- [LOAD DATA INFILE vs machloader](/dbms/core-concepts/terminology-distinction/#load-data-infile-vs-machloader) -- 파일 기반 일괄 적재 방법 비교
- [machloader vs csvimport / csvexport vs tagmetaimport](/dbms/core-concepts/terminology-distinction/#machloader-vs-csvimport-csvexport-tagmetaimport) -- 파일 기반 입출력 도구 비교
- [쓰기 중심 워크로드와 append-only 모델](/dbms/core-concepts/concepts/#write-oriented-append-only) -- APPEND 모델의 설계 원칙
