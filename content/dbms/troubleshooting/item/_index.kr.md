---
type: docs
title: '16.4 입력과 적재 문제'
weight: 30
---
데이터가 Machbase에 정상적으로 들어오지 않을 때, 원인은 크게 세 가지 경로로 나뉩니다. Append API를 통한 직접 입력 실패, machloader를 이용한 CSV 파일 가져오기 실패, 그리고 Machbase Collector를 통한 수집 파이프라인 오류입니다.

각 경우는 오류가 발생하는 위치와 증상이 다르므로 해당하는 섹션에서 진단을 시작하십시오.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [입력이 실패할 때](/dbms/troubleshooting/item/#failure) | Append API 오류 원인 분석 및 해결 방법 |
| [CSV import가 실패할 때](/dbms/troubleshooting/item/#failure-csv-import) | machloader 오류 진단 및 옵션 설정 |
| [Collector 수집이 실패할 때](/dbms/troubleshooting/item/#failure-ingestion-collector) | Collector 트레이스 로그 분석 및 복구 절차 |


<a id="failure"></a>

## 입력이 실패할 때

Append API를 통한 데이터 입력이 실패하는 경우 원인은 대부분 연결 상태, 테이블 정의, 데이터 형식, 디스크 상태 중 하나입니다. 오류 메시지를 단서로 삼아 해당 원인을 빠르게 좁혀 나가십시오.

### 주요 실패 원인

| 원인 | 증상 | 해당 항목 |
|------|------|-----------|
| 연결 끊김 | Connection reset 오류 반환 | [연결 끊김](#연결-끊김-connection-reset) |
| 대상 테이블 없음 | Table not found 오류 반환 | [테이블 없음](#대상-테이블이-없을-때) |
| 컬럼 타입 불일치 | Type mismatch 오류 반환 | [타입 불일치](#컬럼-타입-불일치) |
| 디스크 공간 부족 | 쓰기 실패, 서버 응답 없음 | [디스크 부족](#디스크-공간-부족) |
| 시간 역순 입력 | 입력은 되나 성능 급격히 저하 | [시간 역순 입력](#시간-역순-입력-log-테이블) |

### 진단 방법

Append 세션이 현재 어떤 상태인지 먼저 확인합니다.

```sql
-- Append 세션 확인
SELECT sess_id, id, state, record_size, query
  FROM v$stmt
 WHERE query LIKE '%APPEND%';
```

`state`가 `APPEND` 또는 `FETCH`로 고정되어 있다면 해당 세션이 중단된 것입니다. `sess_id`를 기억해 두고 아래 해결 방법을 적용하십시오.

### 오류별 해결 방법

| 오류 | 원인 | 해결 |
|------|------|------|
| `ERR-02097: Table not found` | 테이블명 오류 또는 테이블 미생성 | 테이블 이름 철자 확인, 없으면 `CREATE TABLE` 실행 |
| `ERR-02041: Type mismatch` | 컬럼 타입 불일치 | 데이터 형식과 테이블 스키마 비교 확인 |
| `Connection reset by peer` | 네트워크 단절 또는 서버 과부하 | 재연결 로직 추가, 서버 상태 확인 |
| `ERR-02268: Disk is full` | 디스크 공간 소진 | 불필요한 데이터 삭제 또는 디스크 확장 |

---

### 연결 끊김 (Connection reset)

Append 도중 네트워크가 단절되거나 서버가 과부하 상태에 빠지면 `Connection reset by peer` 오류가 발생합니다.

**확인 방법**

```bash
# 서버 상태 확인
machadmin -e

# 트레이스 로그에서 연결 관련 오류 확인
grep -i "reset\|disconnect\|abort" $MACHBASE_HOME/trc/machbase.trc | tail -20
```

**해결 방법**

- Append 클라이언트에 자동 재연결 로직(retry)을 구현합니다.
- 서버 과부하가 원인이라면 [쿼리가 느릴 때](/dbms/troubleshooting/performance/#slow)를 참고하십시오.
- 방화벽의 TCP 유휴 타임아웃 설정이 너무 짧지 않은지 확인합니다.

---

### 대상 테이블이 없을 때

`ERR-02097: Table not found` 오류는 테이블명이 틀렸거나 아직 테이블을 생성하지 않았을 때 발생합니다.

**확인 방법**

```sql
-- 테이블 존재 여부 확인
SELECT name, type FROM m$sys_tables WHERE name = 'SENSOR_LOG';
```

결과가 없으면 테이블이 존재하지 않는 것입니다.

**해결 방법**

- 테이블명의 대소문자와 철자를 확인합니다. Machbase의 테이블명은 기본적으로 대문자로 저장됩니다.
- 테이블이 없다면 적절한 `CREATE TABLE` 구문으로 먼저 생성합니다.

---

### 컬럼 타입 불일치

`ERR-02041: Type mismatch` 오류는 입력 데이터의 값 형식이 테이블 컬럼 타입과 맞지 않을 때 발생합니다.

**확인 방법**

```sql
-- 테이블 컬럼 정의 확인
DESC sensor_log;
```

반환된 컬럼 타입과 실제 입력 중인 데이터의 형식을 비교합니다.

**해결 방법**

- 입력 데이터에서 해당 컬럼의 값 형식(정수/실수/문자열/시간)을 확인합니다.
- 타임스탬프 컬럼의 경우 나노초 단위 정수값이어야 합니다. 밀리초나 초 단위로 잘못 입력하지 않았는지 확인합니다.

---

### 디스크 공간 부족

디스크가 가득 찬 경우 Append 쓰기가 실패하고 서버가 응답하지 않을 수 있습니다.

**확인 방법**

```bash
# 데이터 디렉토리의 디스크 사용량 확인
df -h $MACHBASE_HOME/dbs

# 트레이스 로그에서 디스크 관련 오류 확인
grep -i "disk\|space\|full\|write" $MACHBASE_HOME/trc/machbase.trc | tail -20
```

**해결 방법**

- 오래된 데이터를 삭제하거나 별도 파티션으로 데이터 경로를 이동합니다.
- `machbase.conf`에서 `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SECS` 설정을 확인해 체크포인트 주기를 조정합니다.
- 근본적인 해결이 어렵다면 데이터 보존 정책을 검토하십시오.

---

### 시간 역순 입력 (LOG 테이블)

LOG 테이블은 `_ARRIVAL_TIME` 컬럼이 단조 증가(monotonically increasing)하도록 설계되어 있습니다. 시간이 역순으로 입력되면 입력 자체는 성공하지만 다음과 같은 문제가 발생합니다.

- 내부 인덱스 재정렬로 인한 입력 성능 저하
- 파티션 경계가 불규칙해져 쿼리 성능 저하

**확인 방법**

```sql
-- 가장 최근 데이터와 가장 오래된 데이터의 시간 확인
SELECT MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME) FROM sensor_log;
```

입력 중인 데이터의 타임스탬프가 현재 테이블에 저장된 최댓값보다 과거 시간이라면 역순 입력이 발생하고 있는 것입니다.

**해결 방법**

- 소스에서 데이터를 수집하는 순서를 시간 순으로 정렬합니다.
- 과거 데이터를 일괄 재적재해야 한다면 별도 테이블에 넣은 뒤 시간 순으로 정렬하여 INSERT SELECT로 이관합니다.
- Collector를 사용한다면 소스 쿼리에 `ORDER BY timestamp ASC`를 명시합니다.

<a id="failure-csv-import"></a>

## CSV import가 실패할 때

machloader를 사용한 CSV 파일 가져오기가 실패하는 경우 대부분 파일 경로, 컬럼 수, 인코딩, 구분자, 날짜 형식 중 하나가 원인입니다. 오류 로그 파일을 먼저 확인한 뒤 해당 옵션을 조정하면 대부분의 문제를 해결할 수 있습니다.

### 오류 로그 확인

오류 레코드를 파일로 남기려면 `-b` 옵션으로 bad file 경로를 지정합니다. 처리 로그는
`-l` 옵션으로 남깁니다.

```bash
machloader -i -t sensor_log -d data.csv \
           -b sensor_log.bad \
           -l sensor_log.log

# 실패 레코드 확인
cat sensor_log.bad
```

오류 메시지에 행 번호와 오류 원인이 기록되어 있습니다. 이 정보를 단서로 삼아 아래 항목 중 해당하는 원인을 찾으십시오.

### 원인별 진단 및 해결

#### 1. 파일 경로 오류

```
ERR: cannot open file '/path/to/data.csv'
```

상대 경로를 사용하면 machloader를 실행하는 디렉토리에 따라 경로가 달라질 수 있습니다. 절대 경로를 사용하십시오.

```bash
# 잘못된 예 (상대 경로)
machloader -i -t sensor_log -d data.csv

# 올바른 예 (절대 경로)
machloader -i -t sensor_log -d /data/import/sensor_log_20240101.csv
```

#### 2. 컬럼 수 불일치

```
ERR: column count mismatch at line 5
```

CSV 파일의 컬럼 수가 테이블의 컬럼 수와 맞지 않을 때 발생합니다.

```bash
# CSV 첫 번째 행(헤더) 확인
head -1 /data/import/sensor_log.csv

# 테이블 컬럼 확인
echo "DESC sensor_log;" > desc_sensor_log.sql
machsql -s 127.0.0.1 -u SYS -p MANAGER -f desc_sensor_log.sql
```

CSV에 헤더 행이 포함되어 있다면 `-H` 옵션을 추가합니다.

```bash
machloader -i -t sensor_log -d data.csv -H
```

#### 3. 인코딩 문제

```
ERR: invalid character sequence at line 12
```

한글 등 멀티바이트 문자가 포함된 CSV 파일에서 인코딩이 맞지 않으면 오류가 발생합니다. `-E` 옵션으로 인코딩을 명시합니다.

```bash
# UTF-8 인코딩 명시
machloader -i -t sensor_log -d data.csv -E UTF-8

# EUC-KR 인코딩 명시
machloader -i -t sensor_log -d data.csv -E EUC-KR
```

파일의 실제 인코딩 확인 방법입니다.

```bash
file -i /data/import/sensor_log.csv
```

#### 4. 구분자 오류

기본 구분자는 쉼표(`,`)입니다. 세미콜론, 탭, 파이프 등 다른 구분자를 사용하는 파일이라면 `-D` 옵션으로 지정합니다.

```bash
# 파이프(|) 구분자
machloader -i -t sensor_log -d data.csv -D '|'

# 탭 구분자
machloader -i -t sensor_log -d data.csv -D '\t'

# 세미콜론 구분자
machloader -i -t sensor_log -d data.csv -D ';'
```

#### 5. 날짜 형식 오류

```
ERR: invalid datetime format at line 3
```

타임스탬프 컬럼의 값 형식이 machloader가 기대하는 형식과 다를 때 발생합니다. `-F` 옵션으로 시간 포맷을 직접 지정합니다.

```bash
# ISO 8601 형식 (예: 2024-01-15 09:30:00)
machloader -i -t sensor_log -d data.csv -F "YYYY-MM-DD HH24:MI:SS"

# 밀리초 포함 형식 (예: 2024-01-15 09:30:00.123)
machloader -i -t sensor_log -d data.csv -F "YYYY-MM-DD HH24:MI:SS.mmm"
```

### 자주 쓰는 옵션 조합

#### 헤더 있는 CSV

```bash
machloader -i -t sensor_log -d data.csv -H
```

#### 인코딩과 구분자 명시

```bash
machloader -i -t sensor_log -d data.csv -E UTF-8 -D '|'
```

#### 날짜 형식과 헤더 함께 지정

```bash
machloader -i -t sensor_log -d data.csv -H -F "YYYY-MM-DD HH24:MI:SS"
```

### 부분 적재 후 재시작

대용량 파일 가져오기 도중 중단된 경우 처음부터 다시 시작하면 중복 데이터가 입력됩니다. `--first` 옵션으로 시작 행을 지정해 이미 입력된 행을 건너뜁니다.

```bash
# 1001번째 행부터 재시작 (헤더 제외 1000행 완료 가정)
machloader -i -t sensor_log -d data.csv -H --first=1001
```

로그 파일에 기록된 마지막 성공 행 번호를 `--first` 값으로 사용하십시오.

### machloader 주요 옵션 요약

| 옵션 | 설명 | 예시 |
|------|------|------|
| `-i` | import 모드 | `-i` |
| `-t` | 대상 테이블명 | `-t sensor_log` |
| `-d` | CSV 파일 경로 | `-d /data/file.csv` |
| `-H` | 첫 번째 행을 헤더로 처리 | `-H` |
| `-E` | 파일 인코딩 | `-E UTF-8` |
| `-D` | 구분자 | `-D '|'` |
| `-F` | 날짜 포맷 | `-F "YYYY-MM-DD HH24:MI:SS"` |
| `--first` | 시작 행 번호 | `--first=1001` |
| `-b` | 실패 레코드 저장 파일 | `-b sensor_log.bad` |
| `-l` | 처리 로그 파일 | `-l sensor_log.log` |

<a id="failure-ingestion-collector"></a>

## Collector 수집이 실패할 때

Machbase Collector를 통한 데이터 수집이 멈추거나 지연되는 경우 트레이스 로그가 첫 번째 단서입니다. 소스 연결 실패, 큐 오버플로우, Machbase 연결 실패, 데이터 형식 오류 중 어느 쪽인지 로그를 보고 판단합니다.

### 트레이스 로그 확인

Collector 기본 로그는 `$MACHBASE_COLLECTOR_HOME/trc/machcollector.trc`에 기록됩니다.
Collector별 trace 설정을 별도로 사용한 경우에는 해당 collector 이름의 로그를 함께 확인합니다.

```bash
# 최근 100줄 확인
tail -100 $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc

# 오류/경고 메시지만 필터링
grep -i "error\|fail\|queue\|overflow" \
  $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc | tail -50
```

`MACHBASE_COLLECTOR_HOME`을 별도로 지정하지 않았다면 Collector 실행 환경의 trace 경로를
확인하십시오.

### 원인별 진단

#### 1. 소스 연결 실패

소스 장치나 서버에 연결할 수 없을 때 발생합니다.

**로그 예시**

```
[ERROR] failed to connect to source: connection refused (192.168.1.100:1234)
[ERROR] source timeout after 30s
```

**진단 및 해결**

```bash
# 소스 서버/장치 네트워크 연결 확인
ping 192.168.1.100

# 포트 연결 가능 여부 확인
telnet 192.168.1.100 1234
```

- 소스 서버가 정상 실행 중인지 확인합니다.
- 방화벽 규칙에서 해당 포트가 허용되어 있는지 확인합니다.
- Collector 설정 파일에서 소스 접속 정보(호스트, 포트, 계정)를 재확인합니다.

#### 2. 큐 오버플로우

소스에서 데이터가 들어오는 속도보다 Machbase에 저장하는 속도가 느릴 때 발생합니다. 큐가 가득 차면 데이터 유실이 생길 수 있습니다.

**로그 예시**

```
[WARN] queue overflow: dropping 500 records
[WARN] queue delay: 15000ms behind
[INFO] queue size: 10000/10000 (full)
```

**큐 상태 모니터링**

```bash
grep -i "queue\|delay\|overflow\|slow" \
  $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc | tail -50
```

**해결 방법**

- Collector 설정에서 배치 크기(`batch_size`)를 늘려 한 번에 더 많은 데이터를 저장합니다.
- 병렬 처리 스레드 수(`worker_threads`)를 늘립니다.
- Machbase 서버의 Append 성능을 점검합니다([쿼리가 느릴 때](/dbms/troubleshooting/performance/#slow) 참고).

#### 3. Machbase 연결 실패

Collector가 Machbase에 연결하지 못하는 경우입니다.

**로그 예시**

```
[ERROR] failed to connect to Machbase: connection refused (localhost:5656)
[ERROR] Machbase broker is not responding
```

**진단 및 해결**

```bash
# Machbase 서버 상태 확인
machadmin -e

# 서버가 중지된 경우 시작
machadmin -u
```

- Machbase가 정상 실행 중이라면 Collector 설정 파일의 접속 정보(호스트, 포트, 사용자, 비밀번호)를 확인합니다.
- 포트 번호가 `machbase.conf`의 `PORT_NO` 설정과 일치하는지 확인합니다.

#### 4. 데이터 형식 오류

소스 데이터의 형식이 Machbase 테이블의 스키마와 맞지 않는 경우입니다.

**로그 예시**

```
[ERROR] type mismatch at column 'temperature': expected DOUBLE, got STRING
[ERROR] invalid datetime format: '2024/01/15 09:30:00'
```

**해결 방법**

- Collector 설정 파일에서 컬럼 매핑과 타입 변환 설정을 확인합니다.
- 날짜 형식이 맞지 않는다면 Collector의 날짜 파싱 포맷을 수정합니다.
- 소스 데이터에 NULL 또는 빈 값이 섞여 있다면 NULL 처리 방식을 설정합니다.

### 수집 복구 절차

수집이 완전히 중단된 경우 다음 순서로 복구합니다.

**1단계: 로그 확인 및 원인 파악**

```bash
grep -i "error\|fail" $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc | tail -30
```

**2단계: Collector 재시작**

```bash
# Collector 중지
machcollectoradmin --stop-collector=<collector-name>

# 잠시 대기 후 시작
machcollectoradmin --start-collector=<collector-name>
```

**3단계: 수집 재개 확인**

```bash
# 로그에서 정상 수집 여부 확인
tail -f $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc
```

`[INFO] collected N records` 메시지가 주기적으로 출력되면 정상입니다.

**4단계: 배치 크기 조정 (큐 오버플로우인 경우)**

Collector 설정 파일을 열어 배치 크기를 기존 값의 2배로 늘린 뒤 재시작합니다. 변경 후 큐 딜레이 로그가 줄어드는지 확인합니다.
