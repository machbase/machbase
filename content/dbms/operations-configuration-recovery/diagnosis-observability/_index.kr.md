---
type: docs
title: '13.6 관측과 진단'
weight: 60
toc: true
---
서버 상태 파악과 문제 진단에는 두 가지 도구를 사용합니다. `M$` 메타 테이블로 스키마 정의 정보를 조회하고, `V$` 가상 테이블(Virtual Table)로 실시간 운영 상태를 확인합니다. 여기에 서버 **로그 파일** 분석을 더하면 대부분의 운영 상황에 대응할 수 있습니다.

## 주요 V$ 가상 테이블

| 카테고리 | 테이블 이름 | 주요 용도 |
|---------|-----------|---------|
| 세션/시스템 | V$SESSION | 현재 접속 세션 목록과 상태 |
| 세션/시스템 | V$STMT | 실행 중인 SQL 문과 상태 |
| 세션/시스템 | V$PROPERTY | 현재 서버 설정값 조회 |
| 세션/시스템 | V$SYSMEM | 시스템 메모리 사용량 |
| 세션/시스템 | V$SYSSTAT | 시스템 통계 정보 |
| Result Cache | V$RS_CACHE_LIST | 결과 캐시 목록 |
| Result Cache | V$RS_CACHE_STAT | 결과 캐시 통계 |
| 스토리지 | V$STORAGE_USAGE | 디스크 사용량 및 한계 비율 |
| 스토리지 | V$STORAGE_TABLES | 테이블별 스토리지 사용량 |
| 태그 Rollup | V$ROLLUP | Rollup 작업 상태 |
| 스트림 | V$STREAMS | Stream 쿼리 실행 상태 |
| 라이선스 | V$LICENSE_INFO | 라이선스 정보와 위반 상태 |

## 로그 파일 위치 요약

| 로그 파일 | 위치 | 용도 |
|---------|------|------|
| 서버 메인 로그 | `$MACHBASE_HOME/trc/machbase.trc` | 서버 동작 전반, 오류 기록 |
| machsql 이력 | `$MACHBASE_HOME/trc/machsql.history` | 대화형 SQL 실행 이력 |
| machloader 오류 | 실행 디렉터리 `machloader.err` | 적재 실패 레코드 |
| machloader 통계 | 실행 디렉터리 `machloader.log` | 처리 건수, 오류 건수 |
| Collector 로그 | `$MACHBASE_COLLECTOR_HOME/trc/` | Collector 수집 상태 |

모든 로그 파일은 기본적으로 `$MACHBASE_HOME/trc/` 디렉터리에 위치합니다. Trace Log 레벨은 `machbase.conf`의 `TRACE_LOG_LEVEL` 파라미터로 조정합니다.

## 이 섹션의 구성

- [진단과 로그](/dbms/operations-configuration-recovery/diagnosis-observability/#log-diagnosis-logs) — 서버 로그 파일의 종류와 분석 방법, Trace Log 설정, 각 도구별 로그
- [메타 테이블 활용](/dbms/operations-configuration-recovery/diagnosis-observability/#item) — M$ 메타 테이블을 이용한 스키마 정보 조회
- [가상 테이블 활용](/dbms/operations-configuration-recovery/diagnosis-observability/#item-2) — V$ 가상 테이블을 이용한 실시간 서버 상태 조회
- [모니터링과 용량 관리](/dbms/operations-configuration-recovery/diagnosis-observability/#monitoring-capacity) — 정기 점검 절차, 디스크·메모리 용량 관리, 장애 징후 확인


<a id="log-diagnosis-logs"></a>

## 진단과 로그

Machbase는 서버 동작 전반과 각 도구의 실행 이력을 로그 파일에 기록합니다. 문제가 발생했을 때 가장 먼저 확인해야 할 정보의 출처입니다.

### 로그 파일 종류

| 로그 파일 | 기본 위치 | 생성 주체 |
|---------|---------|---------|
| `machbase.trc` | `$MACHBASE_HOME/trc/` | Machbase 서버 |
| machsql 이력 | `$MACHBASE_HOME/trc/machsql.history` | machsql 클라이언트 |
| `machloader.log` | 실행 디렉터리 | machloader |
| `machloader.err` | 실행 디렉터리 | machloader |
| Collector 로그 | `$MACHBASE_COLLECTOR_HOME/trc/` | Collector 프로세스 |

### 로그 디렉터리

Machbase 서버가 생성하는 로그는 모두 아래 디렉터리에 저장됩니다.

```
$MACHBASE_HOME/trc/
```

이 디렉터리에 기록되는 주요 파일:

- `machbase.trc` — 서버 메인 로그. 시작/종료, 오류, 경고, 진단 정보
- `machbase.trc.<날짜>` — 날짜별로 롤오버된 이전 로그 파일

로그 파일이 과도하게 커지면 디스크 공간을 소진할 수 있습니다. `TRACE_LOG_LEVEL` 설정으로 로깅 수준을 조정하고, 운영 환경에서는 불필요하게 상세한 레벨을 사용하지 않도록 합니다.

### 이 섹션의 구성

- [Trace Log 설정](/dbms/operations-configuration-recovery/diagnosis-observability/#configuration-trace-log) — `TRACE_LOG_LEVEL` 파라미터로 로깅 수준 제어
- [서버 로그](/dbms/operations-configuration-recovery/diagnosis-observability/#log-server-logs) — `machbase.trc` 분석과 주요 오류 패턴
- [machsql 로그](/dbms/operations-configuration-recovery/diagnosis-observability/#log-logs-machsql) — machsql 실행 이력 확인
- [machloader 로그](/dbms/operations-configuration-recovery/diagnosis-observability/#log-logs-machloader) — 데이터 적재 오류와 통계 확인
- [Collector 로그](/dbms/operations-configuration-recovery/diagnosis-observability/#log-logs-collector) — Collector 수집 상태 진단

<a id="configuration-trace-log"></a>
<a id="log-diagnosis-logs-configuration-trace-log"></a>

### Trace Log 설정

Machbase 서버의 로깅 범위는 `TRACE_LOG_LEVEL` 프로퍼티로 제어합니다. 이 값은 모듈별 trace flag를 OR로 조합한 비트마스크이며, 추가 비트를 활성화하면 기록되는 로그 범주와 세부 정보가 늘어납니다. 로그 범위를 넓히면 디스크 I/O가 증가해 서버 성능에 영향을 줄 수 있으므로 운영 환경에서는 필요한 비트만 활성화합니다.

#### TRACE_LOG_LEVEL 설정

`$MACHBASE_HOME/conf/machbase.conf` 파일에서 설정합니다.

```
TRACE_LOG_LEVEL = 277
```

각 비트 플래그는 독립적으로 동작하며, 여러 플래그를 합산하여 설정할 수 있습니다. 기본값은 `277`이며, `MM_1 + QP_1 + SM_1 + XM_1` 조합입니다.

| 값 | 모듈 |
|----|------|
| 1 | MM_1 |
| 2 | MM_2 |
| 4 | QP_1 |
| 8 | QP_2 |
| 16 | SM_1 |
| 32 | SM_2 |
| 64 | CC_1 |
| 128 | CC_2 |
| 256 | XM_1 |
| 512 | XM_2 |
| 1024 | LM_1 |
| 2048 | LM_2 |
| 4096 | RP_1 |
| 8192 | RP_2 |
| 65536 | MISC_1 |
| 131072 | MISC_2 |
| 262144 | DEBUG |

운영 환경에서는 기본값을 기준으로 유지하고, 특정 모듈 진단이 필요한 경우에만 해당 비트를 일시적으로 추가합니다.

#### 런타임 변경

서버를 재시작하지 않고도 `ALTER SYSTEM` 명령으로 즉시 변경할 수 있습니다.

```sql
-- 현재 TRACE_LOG_LEVEL 확인
SELECT name, value
  FROM v$property
 WHERE name = 'TRACE_LOG_LEVEL';

-- 런타임 변경 (MM_1 + QP_1 + SM_1 + XM_1)
ALTER SYSTEM SET TRACE_LOG_LEVEL = 277;

-- QP_2를 추가한 진단 설정
ALTER SYSTEM SET TRACE_LOG_LEVEL = 285;
```

#### 권장 설정

| 환경 | TRACE_LOG_LEVEL | 이유 |
|------|----------------|------|
| 운영 (정상) | 277 | 기본 모듈 1단계 로그 |
| QP 진단 | 285 | 기본값 + QP_2 |
| Storage 진단 | 309 | 기본값 + SM_2 |
| 개발/디버깅 | 262144 포함 | DEBUG 비트 포함. 운영 환경에 비권장 |

> **주의**: `TRACE_LOG_LEVEL`이 높으면 로그 파일 크기가 빠르게 증가합니다. 디스크 공간을 정기적으로 확인하고, 진단 완료 후에는 반드시 운영 수준으로 복원하십시오.

<a id="log-server-logs"></a>
<a id="log-diagnosis-logs-log-server-logs"></a>

### 서버 로그

Machbase 서버의 메인 로그 파일은 `$MACHBASE_HOME/trc/machbase.trc`입니다. 서버 시작/종료, 오류, 경고, 백업/복구 등 서버 동작 전반이 기록됩니다.

#### 로그 파일 위치

```
$MACHBASE_HOME/trc/machbase.trc
```

날짜가 바뀌면 이전 로그 파일은 날짜가 포함된 이름으로 보존됩니다.

```
$MACHBASE_HOME/trc/machbase.trc           # 현재 로그
$MACHBASE_HOME/trc/machbase.trc.20240115  # 롤오버된 이전 로그
```

#### 로그 형식

각 로그 라인은 다음 형식을 따릅니다.

```
[YYYY-MM-DD HH:MM:SS.mmm] [레벨] [모듈] 메시지
```

예시:

```
[2024-01-15 09:00:01.123] [INFO] [SERVER] Machbase server started. Version=8.6.0
[2024-01-15 09:00:01.450] [INFO] [STORAGE] Checkpoint completed. elapsed=1230ms
[2024-01-15 10:45:22.001] [ERROR] [NETWORK] Connection refused. client=192.168.1.100
[2024-01-15 11:30:55.321] [WARN] [STORAGE] Disk usage reached 85%. used_ratio=85, ratio_cap=95
```

#### 로그 레벨 설정

로그 상세 수준은 `TRACE_LOG_LEVEL`로 조정합니다. 자세한 내용은 [Trace Log 설정](/dbms/operations-configuration-recovery/diagnosis-observability/#log-diagnosis-logs-configuration-trace-log)을 참조하십시오.

#### 주요 오류 패턴과 분석

##### 연결 오류 패턴

클라이언트가 연결하지 못하거나 갑자기 연결이 끊어지는 경우 아래 패턴을 확인합니다.

```
[ERROR] [NETWORK] Connection refused. client=<IP>
[ERROR] [NETWORK] Session disconnected unexpectedly. session_id=<ID>
[ERROR] [NETWORK] Max session count reached. max=<N>
```

**조치**: `MAX_SESSION_COUNT` 파라미터 확인, 비정상 세션 정리(`ALTER SYSTEM KILL SESSION`), 네트워크 방화벽 규칙 점검.

##### 디스크 풀 패턴

디스크 여유 공간이 부족하면 다음 패턴이 나타납니다.

```
[WARN]  [STORAGE] Disk usage reached 85%. used_ratio=85, ratio_cap=95
[ERROR] [STORAGE] Disk full. Data append suspended. path=/machbase/dbs
[ERROR] [STORAGE] Failed to write data file. errno=28 (No space left on device)
```

**조치**: 불필요한 파일 제거, 오래된 데이터 Retention Policy 적용, 디스크 확장.

##### 메모리 부족 (OOM) 패턴

```
[ERROR] [MEMORY] Memory allocation failed. requested=<SIZE>bytes
[ERROR] [QUERY]  Query aborted due to memory limit. sess_id=<ID>
```

**조치**: `MAX_QPX_MEM` 파라미터 확인, 불필요한 세션 종료, 시스템 메모리 여유 확보.

##### 체크포인트 및 백업 로그

```
[INFO] [STORAGE] Checkpoint started.
[INFO] [STORAGE] Checkpoint completed. elapsed=2340ms
[INFO] [BACKUP]  Backup started. path=/backup/20240115
[INFO] [BACKUP]  Backup completed. elapsed=125s, size=2.3GB
```

체크포인트가 과도하게 오래 걸리면 (`elapsed` 값이 수십 초 이상) 디스크 I/O 부하를 점검합니다.

##### 서버 시작/종료 로그

```
[INFO] [SERVER] Machbase server starting. version=8.6.0, pid=12345
[INFO] [SERVER] Storage recovery started.
[INFO] [SERVER] Storage recovery completed.
[INFO] [SERVER] Machbase server started. port=5656
[INFO] [SERVER] Machbase server shutting down. reason=SIGTERM
[INFO] [SERVER] Machbase server stopped.
```

비정상 종료 시에는 `SIGKILL` 또는 `Killed`가 함께 기록됩니다. `/var/log/syslog`에서 OOM Killer 동작 여부도 함께 확인합니다.

#### 로그 파일 검색

```bash
# 오늘 발생한 ERROR 로그 확인
grep '\[ERROR\]' $MACHBASE_HOME/trc/machbase.trc

# 특정 날짜 범위에서 스토리지 관련 경고 확인
grep '2024-01-15.*STORAGE' $MACHBASE_HOME/trc/machbase.trc

# 최근 100줄 실시간 모니터링
tail -f -n 100 $MACHBASE_HOME/trc/machbase.trc
```

#### 로그 파일 관리

로그 파일이 누적되면 디스크 공간을 소비합니다. 오래된 로그 파일은 주기적으로 압축하거나 삭제하십시오.

```bash
# 30일 이상 된 로그 파일 목록 확인
find $MACHBASE_HOME/trc/ -name "machbase.trc.*" -mtime +30

# 30일 이상 된 로그 파일 삭제
find $MACHBASE_HOME/trc/ -name "machbase.trc.*" -mtime +30 -delete
```

<a id="log-logs-machsql"></a>
<a id="log-diagnosis-logs-log-logs-machsql"></a>

### machsql 로그

`machsql`은 Machbase 서버에 직접 접속하는 대화형 SQL 클라이언트 도구입니다. machsql은 별도의 로그 파일을 생성하지 않지만, 실행한 SQL 명령의 이력은 히스토리 파일에 기록됩니다.

#### SQL 실행 이력 (History)

machsql을 대화형 모드로 실행하면 입력한 모든 SQL 명령이 히스토리 파일에 저장됩니다.

**기본 위치**:
```
$MACHBASE_HOME/trc/machsql.history
```

이 파일은 Machbase 홈의 `trc` 디렉터리에 생성됩니다.

#### 히스토리 파일 확인

```bash
# 최근 실행 이력 확인
cat $MACHBASE_HOME/trc/machsql.history

# 최근 50개 이력만 확인
tail -50 $MACHBASE_HOME/trc/machsql.history

# 특정 키워드를 포함한 이력 검색
grep -i 'sensor_log' $MACHBASE_HOME/trc/machsql.history
```

#### machsql 내에서 이력 조회

machsql 실행 중에 방향키(위/아래)를 눌러 이전 명령을 탐색할 수 있습니다.

```sql
-- machsql 실행
$ machsql -u sys -p manager -s 127.0.0.1

-- 접속 후 이력 활용 예시
Mach> SELECT * FROM sensor_log LIMIT 10;  -- 실행 후 히스토리에 저장됨
```

#### machsql 실행 로그 (리다이렉션)

특정 SQL 스크립트 실행 결과를 파일로 저장하려면 셸 리다이렉션을 사용합니다.

```bash
# SQL 파일 실행 결과를 파일로 저장
machsql -u sys -p manager -s 127.0.0.1 -f query.sql > result.log 2>&1

# 단일 SQL을 임시 스크립트로 실행
echo "SELECT count(*) FROM sensor_log;" > /tmp/count.sql
machsql -u sys -p manager -s 127.0.0.1 -f /tmp/count.sql > count.log
```

#### 비대화형 모드에서의 오류 출력

스크립트 형태로 machsql을 실행할 때 발생하는 오류는 표준 오류(stderr)로 출력됩니다.

```bash
# 오류만 별도 파일로 저장
machsql -u sys -p manager -s 127.0.0.1 -f setup.sql \
  > /dev/null 2> setup.err

# 오류 발생 여부 확인
if [ -s setup.err ]; then
    echo "오류 발생:"
    cat setup.err
fi
```

#### 주요 machsql 옵션

| 옵션 | 설명 |
|------|------|
| `-s <HOST>` | 서버 주소 |
| `-P <PORT>` | 서버 포트 (기본값: 5656) |
| `-u <USER>` | 사용자 이름 |
| `-p <PASS>` | 패스워드 |
| `-f <FILE>` | SQL 스크립트 파일 실행 |
| `-o <FILE>` | 결과 출력 파일 지정 |

> **참고**: machsql 이력 파일은 `$MACHBASE_HOME/trc/machsql.history`에 저장됩니다.

<a id="log-logs-machloader"></a>
<a id="log-diagnosis-logs-log-logs-machloader"></a>

### machloader 로그

`machloader`는 CSV, TXT 등의 파일을 Machbase에 대량 적재하는 도구입니다. 실행 중에 발생한 오류와 통계 정보를 로그 파일에 기록합니다.

#### 로그 파일 종류

machloader는 실행 시 현재 작업 디렉터리에 두 개의 로그 파일을 생성합니다.

| 파일 이름 | 용도 |
|---------|------|
| `machloader.log` | 적재 통계 (처리 건수, 오류 건수, 소요 시간) |
| `machloader.err` | 오류가 발생한 레코드와 오류 메시지 |

로그 파일 이름은 `-l` 옵션으로 변경할 수 있습니다.

```bash
# 기본 로그 파일명 사용
machloader -i -t sensor_log -d data.csv -r csv

# 사용자 지정 로그 파일명
machloader -i -t sensor_log -d data.csv -r csv -l /logs/load_20240115
# /logs/load_20240115.log, /logs/load_20240115.err 생성
```

#### machloader.log — 적재 통계

적재 완료 후 처리 현황 요약이 기록됩니다.

```
Mach Load Started...
Total: 1000000 records
Loaded: 998523 records
Error: 1477 records
Elapsed: 45.23 seconds
Load rate: 22082 records/sec
```

| 항목 | 설명 |
|------|------|
| Total | 입력 파일의 전체 레코드 수 |
| Loaded | 성공적으로 적재된 레코드 수 |
| Error | 오류로 처리하지 못한 레코드 수 |
| Elapsed | 총 소요 시간 |
| Load rate | 초당 처리 건수 |

#### machloader.err — 오류 레코드

적재에 실패한 레코드의 원본 데이터와 오류 이유가 기록됩니다.

```
[2024-01-15 10:23:45] Line=1024, Error=Column type mismatch: column=temperature, value=N/A
2024-01-15T10:00:00,sensor-001,N/A,60.5

[2024-01-15 10:23:45] Line=2048, Error=Timestamp out of range: column=_arrival_time
2024-01-15T25:00:00,sensor-002,25.3,60.1
```

오류 메시지와 함께 원본 레코드가 기록되므로, 오류 레코드를 수정하여 재처리할 수 있습니다.

#### 오류 레코드 재처리

오류 레코드를 수정하여 재적재하는 절차입니다.

```bash
# 1단계: 오류 레코드 추출 (짝수 줄 = 원본 데이터)
grep -v '^\[' machloader.err > error_records.csv

# 2단계: 오류 원인 분석
grep 'Error=' machloader.err | sort | uniq -c | sort -rn

# 3단계: 데이터 수정 후 재적재
machloader -i -t sensor_log -d error_records_fixed.csv -r csv
```

#### 오류 허용 설정

적재 중 오류가 발생해도 계속 진행하려면 `-e` 옵션으로 허용할 오류 건수를 지정합니다.

```bash
# 오류 100건까지 허용하고 계속 진행
machloader -i -t sensor_log -d data.csv -r csv -e 100

# 오류 건수 제한 없이 계속 진행 (0 = 무제한)
machloader -i -t sensor_log -d data.csv -r csv -e 0
```

#### 주요 적재 오류 유형

| 오류 유형 | 원인 | 조치 |
|---------|------|------|
| Column type mismatch | 데이터 타입 불일치 (문자열 → 숫자 등) | 소스 데이터 형식 확인 및 수정 |
| Timestamp out of range | 유효하지 않은 날짜/시간 값 | 타임스탬프 형식과 범위 확인 |
| String too long | 문자열이 컬럼 최대 길이 초과 | 테이블 컬럼 길이 확인 또는 데이터 트리밍 |
| Duplicate primary key | 기본키 중복 (Fixed/Lookup 테이블) | 중복 레코드 제거 후 재적재 |

#### 적재 성능 모니터링

대용량 파일 적재 중 진행 상황을 확인합니다.

```bash
# 적재 중 처리 건수 실시간 확인 (다른 터미널에서)
tail -f machloader.log

# 오류 레코드 실시간 확인
tail -f machloader.err
```

적재 완료 후에는 오류 건수를 반드시 확인하고, 오류 비율이 높으면 소스 데이터 품질을 점검하십시오.

<a id="log-logs-collector"></a>
<a id="log-diagnosis-logs-log-logs-collector"></a>

### Collector 로그

Machbase Collector는 외부 데이터 소스로부터 데이터를 실시간으로 수집하여 Machbase에 적재하는 프로세스입니다. Collector의 동작 상태와 오류는 전용 로그 파일에 기록됩니다.

#### 로그 파일 위치

Collector 로그는 기본적으로 `$MACHBASE_HOME/trc/` 디렉터리에 저장됩니다.

```
$MACHBASE_HOME/trc/
```

Collector 설정 파일에서 로그 파일 경로와 이름을 별도로 지정할 수 있습니다. 설정 파일에서 `LOG_DIR` 또는 `LOG_FILE` 항목을 확인하십시오.

#### 로그 파일 유형

| 파일 | 내용 |
|------|------|
| `collector.log` (또는 설정에 따른 이름) | 수집 시작/종료, 성공/실패 건수, 연결 상태 |

#### 주요 로그 항목

##### 수집 시작/종료

```
[2024-01-15 09:00:05.001] [INFO] Collector started. source=mqtt://broker:1883, target=SENSOR_LOG
[2024-01-15 18:00:00.001] [INFO] Collector stopped. reason=SIGTERM
```

##### 수집 통계

```
[2024-01-15 09:10:00.001] [INFO] Stats: received=12500, inserted=12498, error=2, queue_size=0
[2024-01-15 09:20:00.001] [INFO] Stats: received=25000, inserted=24995, error=5, queue_size=0
```

| 항목 | 설명 |
|------|------|
| received | 소스로부터 수신한 레코드 수 |
| inserted | Machbase에 성공적으로 적재한 레코드 수 |
| error | 적재에 실패한 레코드 수 |
| queue_size | 내부 버퍼에 대기 중인 레코드 수 |

##### 연결 오류 패턴

소스 연결에 실패하거나 Machbase 서버에 연결할 수 없을 때 기록됩니다.

```
[2024-01-15 10:30:00.001] [ERROR] Connection failed. source=mqtt://broker:1883, reason=Connection refused
[2024-01-15 10:30:05.001] [WARN]  Reconnecting... attempt=1, next_retry=10s
[2024-01-15 10:30:15.001] [INFO]  Reconnected. source=mqtt://broker:1883
```

**조치**: 소스 서버의 상태와 네트워크 경로를 점검합니다. Collector는 일반적으로 재연결을 자동으로 시도합니다.

##### 큐 오버플로 패턴

소스에서 데이터가 유입되는 속도가 Machbase에 적재하는 속도보다 빠를 때 발생합니다.

```
[2024-01-15 11:00:00.001] [WARN] Queue overflow detected. queue_size=100000, dropped=523
[2024-01-15 11:00:00.001] [WARN] Slow insert detected. avg_insert_time=250ms
```

**조치**:
- Machbase 서버의 리소스 상태(CPU, 디스크 I/O) 확인
- Collector 배치 크기(`BATCH_SIZE`) 조정
- 필요 시 Collector 인스턴스 수 증가

##### Machbase 적재 오류

```
[2024-01-15 11:30:00.001] [ERROR] Insert failed. table=SENSOR_LOG, error=Column type mismatch: column=value
[2024-01-15 11:30:00.001] [ERROR] Insert failed. table=SENSOR_LOG, error=Disk full
```

**조치**:
- 타입 불일치: 소스 데이터 형식과 테이블 스키마를 비교
- 디스크 풀: 디스크 사용량 확인 및 공간 확보 ([디스크 사용량 확인](/dbms/operations-configuration-recovery/diagnosis-observability/#monitoring-capacity-capacity-disk) 참조)

#### 수집 상태 확인

Collector가 실행 중인 경우 V$STREAMS 가상 테이블에서도 상태를 조회할 수 있습니다.

```sql
-- STREAM 기반 Collector 상태 확인
SELECT name, state, last_ex_time, error_msg
  FROM v$streams
 ORDER BY name;
```

#### 로그 실시간 모니터링

```bash
# Collector 로그 실시간 확인
tail -f $MACHBASE_HOME/trc/collector.log

# 오류 이벤트만 필터링
grep '\[ERROR\]\|\[WARN\]' $MACHBASE_HOME/trc/collector.log

# 시간대별 수집 통계 확인
grep 'Stats:' $MACHBASE_HOME/trc/collector.log | tail -20
```

#### 수집 통계 점검 체크리스트

정기적으로 Collector 로그를 확인할 때 아래 항목을 점검합니다.

- `error` 건수가 `received` 대비 1% 이상인 경우 → 소스 데이터 품질 점검
- `queue_size`가 지속적으로 증가하는 경우 → 처리 지연 확인
- 재연결 로그가 반복되는 경우 → 소스 서버 또는 네트워크 점검
- 로그에 장시간 통계 메시지가 없는 경우 → Collector 프로세스 생존 여부 확인

<a id="item"></a>

## 메타 테이블 활용

메타 테이블은 Machbase의 스키마 정보(테이블 정의, 컬럼, 인덱스, 사용자 등)를 조회할 수 있는 읽기 전용 시스템 테이블입니다. 테이블 이름은 모두 `M$`로 시작합니다. 사용자가 직접 데이터를 추가하거나 변경할 수 없으며, DDL 명령 실행 결과가 자동으로 반영됩니다.

### 메타 테이블 목록

| 테이블 이름 | 용도 |
|-----------|------|
| M$SYS_TABLES | 사용자가 생성한 테이블 목록과 타입 |
| M$SYS_TABLE_PROPERTY | 테이블에 적용된 속성 정보 |
| M$SYS_COLUMNS | 테이블 컬럼 정의 (타입, 길이 등) |
| M$SYS_INDEXES | 인덱스 정의 |
| M$SYS_INDEX_COLUMNS | 인덱스를 구성하는 컬럼 정보 |
| M$SYS_TABLESPACES | 테이블스페이스 목록 |
| M$SYS_TABLESPACE_DISKS | 테이블스페이스가 사용하는 디스크 경로 |
| M$SYS_USERS | 등록된 사용자 목록 |
| M$SYS_VIEWS | 뷰 정의 SQL 텍스트 |
| M$SYS_USER_ACCESS | 테이블별 사용자 권한 |
| M$RETENTION | Retention Policy 정보 |
| M$TABLES | M$ 메타 테이블 자체 목록 |
| M$COLUMNS | M$ 메타 테이블의 컬럼 목록 |

### 주요 테이블 컬럼

#### M$SYS_TABLES

| 컬럼명 | 설명 |
|-------|------|
| NAME | 테이블 이름 |
| TYPE | 테이블 타입 (0: Log, 1: Fixed, 3: Volatile, 4: Lookup, 5: Key Value, 6: Tag) |
| ID | 테이블 식별자 |
| USER_ID | 테이블 생성 사용자 식별자 |
| COLCOUNT | 컬럼 수 |
| FLAG | 서브 타입 (1: Tag Data, 2: Rollup, 4: Tag Meta, 8: Tag Stat) |

#### M$SYS_COLUMNS

| 컬럼명 | 설명 |
|-------|------|
| NAME | 컬럼명 |
| TYPE | 컬럼 데이터 타입 |
| TABLE_ID | 소속 테이블 식별자 |
| LENGTH | 컬럼 최대 길이 |
| PART_PAGE_COUNT | 파티션당 페이지 수 |
| MINMAX_CACHE_SIZE | MIN-MAX 캐시 크기 |

#### M$SYS_INDEXES

| 컬럼명 | 설명 |
|-------|------|
| NAME | 인덱스 이름 |
| TYPE | 인덱스 타입 |
| TABLE_ID | 소속 테이블 식별자 |
| COLCOUNT | 인덱스 컬럼 수 |
| MAX_LEVEL | 최대 LSM 레벨 |

### SQL 예제

#### 전체 테이블 목록 조회

```sql
-- 사용자 테이블 전체 목록
SELECT name, type, colcount
  FROM m$sys_tables
 ORDER BY name;
```

타입 값의 의미: `0` = Log 테이블, `1` = Fixed 테이블, `3` = Volatile 테이블, `6` = Tag 테이블

#### 특정 테이블 정의 조회

```sql
-- SENSOR_LOG 테이블의 메타 정보
SELECT name, type, colcount, flag
  FROM m$sys_tables
 WHERE name = 'SENSOR_LOG';
```

#### 테이블의 컬럼 정보 조회

```sql
-- SENSOR_LOG 테이블의 컬럼 목록
SELECT c.name AS col_name,
       c.type AS col_type,
       c.length
  FROM m$sys_columns c
  JOIN m$sys_tables  t ON c.table_id = t.id
 WHERE t.name = 'SENSOR_LOG'
 ORDER BY c.id;
```

#### 인덱스 목록 조회

```sql
-- 특정 테이블에 생성된 인덱스 목록
SELECT i.name AS idx_name,
       i.type AS idx_type,
       i.colcount
  FROM m$sys_indexes i
  JOIN m$sys_tables  t ON i.table_id = t.id
 WHERE t.name = 'SENSOR_LOG';
```

#### 인덱스 컬럼 확인

```sql
-- 인덱스를 구성하는 컬럼 확인
SELECT ic.name AS col_name,
       ic.index_type
  FROM m$sys_index_columns ic
  JOIN m$sys_indexes i ON ic.index_id = i.id
  JOIN m$sys_tables  t ON i.table_id = t.id
 WHERE t.name = 'SENSOR_LOG';
```

#### 테이블스페이스 디스크 경로 확인

```sql
-- 테이블스페이스가 사용하는 물리 경로
SELECT ts.name AS tbs_name,
       d.path,
       d.io_thread_count
  FROM m$sys_tablespace_disks d
  JOIN m$sys_tablespaces ts ON d.tablespace_id = ts.id;
```

#### 사용자 목록 조회

```sql
-- 등록된 사용자와 패스워드 정책 확인
SELECT user_id, name, pwd_policy_level, valid_before
  FROM m$sys_users;
```

#### Retention Policy 확인

```sql
-- 설정된 Retention Policy 목록
SELECT policy_name, duration, interval
  FROM m$retention;
```

> **참고**: 메타 테이블은 읽기 전용입니다. `INSERT`, `UPDATE`, `DELETE` 명령은 오류를 반환합니다. 스키마를 변경하려면 반드시 `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE` 등의 DDL 명령을 사용하십시오.

<a id="item-2"></a>

## 가상 테이블 활용

가상 테이블(Virtual Table)은 Machbase 서버의 실시간 운영 상태를 테이블 형태로 표현합니다. 테이블 이름은 모두 `V$`로 시작하며 읽기 전용입니다. 일반 테이블과 JOIN하여 다양한 진단 정보를 조합할 수 있습니다.

### 주요 가상 테이블 목록

| 카테고리 | 테이블 이름 | 용도 |
|---------|-----------|------|
| 세션/시스템 | V$SESSION | 현재 접속 세션 정보 |
| 세션/시스템 | V$STMT | 실행 중인 SQL 문 |
| 세션/시스템 | V$PROPERTY | 현재 서버 설정값 |
| 세션/시스템 | V$SYSMEM | 시스템 메모리 사용량 |
| 세션/시스템 | V$SYSSTAT | 시스템 통계 정보 |
| 세션/시스템 | V$SYSTIME | 시스템 시간 통계 |
| 세션/시스템 | V$VERSION | 서버 버전 정보 |
| 세션/시스템 | V$HTTP_STATUS | HTTP 서비스 상태 |
| Result Cache | V$RS_CACHE_LIST | 결과 캐시 목록 |
| Result Cache | V$RS_CACHE_STAT | 결과 캐시 통계 |
| 스토리지 | V$STORAGE | 스토리지 파일 크기 요약 |
| 스토리지 | V$STORAGE_USAGE | 디스크 사용량과 한계 비율 |
| 스토리지 | V$STORAGE_TABLES | 테이블별 스토리지 사용량 |
| 스토리지 | V$STORAGE_MOUNT_DATABASES | 마운트된 백업 데이터베이스 |
| 태그 Rollup | V$ROLLUP | Rollup 작업 상태 |
| 스트림 | V$STREAMS | Stream 쿼리 실행 상태 |
| 라이선스 | V$LICENSE_INFO | 라이선스 정보 |

---

### V$SESSION — 현재 세션 정보

MACHBASE 서버에 접속된 세션의 목록과 상태를 표시합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| ID | 세션 식별자 |
| CLOSED | 연결이 닫혀있는지 여부 |
| USER_ID | 사용자 식별자 |
| LOGIN_TIME | 접속 시각 |
| CLIENT_TYPE | 접속 클라이언트 타입 |
| USER_NAME | 사용자 이름 |
| USER_IP | 사용자 IP 주소 |
| SQL_LOGGING | 해당 세션의 Trace Log 메시지 기록 여부 |
| IDLE_TIMEOUT | 유휴 상태 세션 종료 시간 (초) |
| QUERY_TIMEOUT | 쿼리 응답 대기 시간 |
| RDB_BUSY_TIMEOUT_MS | RDB 쓰기 충돌 대기 시간 (밀리초) |

```sql
-- 현재 접속 세션 목록
SELECT id, user_name, user_ip, client_type, login_time
  FROM v$session
 WHERE closed = 0
 ORDER BY login_time;
```

---

### V$STMT — 실행 중인 SQL 문

현재 실행 중이거나 대기 중인 SQL 문의 정보를 표시합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| ID | 쿼리 식별자 |
| SESS_ID | 쿼리를 실행한 세션 식별자 |
| STATE | 쿼리 상태 |
| RECORD_SIZE | SELECT 수행 시 결과 레코드 크기 |
| QUERY | 쿼리 구문 |

```sql
-- 실행 중인 쿼리 확인
SELECT id, sess_id, state, query
  FROM v$stmt
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%'
    OR state LIKE 'Append in progress%';
```

> **참고**: `V$STMT`에는 `elapsed_time` 컬럼이 없습니다. 장시간 실행 쿼리를 추적하려면 `V$SESTIME`의 `ACCUM_MSEC` 값과 결합하여 분석하십시오.

---

### V$PROPERTY — 현재 설정값

서버에 설정된 모든 프로퍼티 값을 조회합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| NAME | 프로퍼티 이름 |
| VALUE | 현재 설정값 |
| TYPE | 데이터 타입 |
| DEFLT | 기본값 |
| MIN | 최솟값 |
| MAX | 최댓값 |

```sql
-- 특정 설정값 확인
SELECT name, value, deflt
  FROM v$property
 WHERE name IN ('PORT_NO', 'TRACE_LOG_LEVEL', 'MAX_SESSION_COUNT');

-- 기본값과 다른 설정만 조회
SELECT name, value, deflt
  FROM v$property
 WHERE value != deflt
 ORDER BY name;
```

---

### V$STORAGE_USAGE — 디스크 사용량

저장 시스템의 디스크 사용 현황을 표시합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| TOTAL_SPACE | 데이터 디렉터리가 위치한 스토리지의 총 용량 |
| USED_SPACE | 사용 중인 용량 |
| USED_RATIO | 사용량 비율 (%) |
| RATIO_CAP | 사용량 한계 (이 값 초과 시 데이터 입력 중단) |

```sql
-- 디스크 사용량 확인
SELECT total_space, used_space, used_ratio, ratio_cap
  FROM v$storage_usage;
```

`USED_RATIO`가 `RATIO_CAP`에 근접하면 데이터 적재와 인덱스 구축이 중단됩니다. 정기적으로 모니터링하고 용량을 확보해야 합니다.

---

### V$RS_CACHE_LIST / V$RS_CACHE_STAT — Result Cache 상태

#### V$RS_CACHE_LIST

| 컬럼 이름 | 설명 |
|---------|------|
| TOUCH_TIME | 캐시를 마지막으로 사용하거나 생성한 시각 |
| USER_ID | 캐시를 생성한 사용자 |
| QUERY | 캐시를 만든 쿼리문 |
| TIME_SPENT | 결과 생성까지 경과 시간 |
| RECORD_COUNT | 결과 레코드 개수 |
| HIT_COUNT | 캐시 히트 횟수 |

#### V$RS_CACHE_STAT

| 컬럼 이름 | 설명 |
|---------|------|
| CACHE_COUNT | 현재 캐시 개수 |
| CACHE_HIT | 총 캐시 히트 횟수 |
| AGGR_HIT | 집계 결과의 캐시 히트 횟수 |
| CACHE_REPLACED | 캐시 교체 횟수 |
| CACHE_MEMORY_USAGE | 캐시 메모리 사용량 |

```sql
-- Result Cache 전체 통계
SELECT cache_count, cache_hit, aggr_hit,
       cache_replaced, cache_memory_usage
  FROM v$rs_cache_stat;

-- 히트율이 높은 캐시 쿼리 확인
SELECT query, hit_count, record_count, time_spent
  FROM v$rs_cache_list
 ORDER BY hit_count DESC
 LIMIT 10;
```

---

### V$ROLLUP — Rollup 상태

Tag 데이터의 Rollup 작업 상태를 표시합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| ID | Rollup 작업 ID |
| ROLLUP_TABLE | Rollup 테이블 이름 |
| SOURCE_TABLE | 집계 대상 테이블 이름 |
| COLUMN_NAME | 집계 대상 컬럼 |
| INTERVAL_TIME | 실행 주기 (밀리초) |
| LAST_WAKEUP_TIME | 최근 실행 시각 |
| ENABLED | 활성화 여부 (1/0) |
| LAST_ELAPSED_MSEC | 직전 실행에 걸린 시간 (밀리초) |
| RUN_STATE | 스레드 상태 (I=초기화, S=대기, R=실행중) |

```sql
-- Rollup 작업 상태 확인
SELECT rollup_table, source_table, column_name,
       interval_time, enabled, last_elapsed_msec, run_state
  FROM v$rollup
 ORDER BY rollup_table;

-- 비활성화된 Rollup 확인
SELECT rollup_table, source_table, enabled
  FROM v$rollup
 WHERE enabled = 0;
```

---

### V$STREAMS — Stream 상태

등록된 Stream 쿼리의 실행 상태를 표시합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| NAME | Stream 이름 |
| LAST_EX_TIME | 마지막 실행 시각 |
| TABLE_NAME | 검색 대상 테이블 이름 |
| END_RID | 마지막으로 읽은 RID |
| STATE | 현재 상태 |
| QUERY_TXT | 원본 Stream 쿼리 |
| ERROR_MSG | 마지막 오류 메시지 |
| FREQUENCY | 최소 대기 시간 (나노초, 0이면 매 레코드마다 실행) |

```sql
-- Stream 실행 상태 확인
SELECT name, state, last_ex_time, error_msg
  FROM v$streams
 ORDER BY name;

-- 오류가 발생한 Stream 확인
SELECT name, state, error_msg
  FROM v$streams
 WHERE error_msg IS NOT NULL AND error_msg != '';
```

---

### V$LICENSE_INFO — 라이선스 정보

| 컬럼 이름 | 설명 |
|---------|------|
| ID | 라이선스 ID |
| ISSUE_DATE | 발행일 |
| TYPE | 라이선스 유형 |
| CUSTOMER | 고객사 이름 |
| PROJECT | 프로젝트 이름 |
| INSTALL_DATE | 설치일 |
| VIOLATE_STATUS | 라이선스 위반 상태 |
| VIOLATE_MSG | 라이선스 위반 메시지 |

```sql
-- 라이선스 정보와 위반 상태 확인
SELECT id, type, customer, issue_date,
       install_date, violate_status, violate_msg
  FROM v$license_info;
```

`VIOLATE_STATUS`가 0이 아니거나 `VIOLATE_MSG`에 내용이 있으면 라이선스 정책 위반 상태입니다. 즉시 Machbase 지원팀에 문의하십시오.

---

### V$SYSMEM — 시스템 메모리 사용량

| 컬럼 이름 | 설명 |
|---------|------|
| ID | 메모리 매니저 식별자 |
| NAME | 메모리 매니저 이름 |
| USAGE | 현재 사용량 |
| MAX_USAGE | 기록된 최대 사용량 |

```sql
-- 메모리 매니저별 사용량 확인
SELECT name, usage, max_usage
  FROM v$sysmem
 ORDER BY usage DESC;
```

---

### 전체 가상 테이블 목록 확인

```sql
-- 현재 서버에서 조회 가능한 V$ 가상 테이블 전체 목록
SELECT name
  FROM v$tables
 WHERE name LIKE 'V$%'
 ORDER BY name;
```

> **참고**: 가상 테이블은 읽기 전용입니다. 또한 클러스터 에디션에서만 제공되는 테이블(V$NODE_STATUS, V$REPLICATION 등)은 Standard 에디션에서 조회되지 않습니다. `V$TABLES`로 조회 가능한 테이블 목록을 먼저 확인하십시오.

<a id="monitoring-capacity"></a>

## 모니터링과 용량 관리

Machbase 서버를 안정적으로 운영하려면 주기적으로 서버 상태, 세션, 디스크, 메모리를 점검해야 합니다. 문제가 발생하기 전에 징후를 발견하는 것이 장애 예방의 핵심입니다.

### 정기 점검 항목

| 점검 항목 | 권장 주기 | 주요 확인 내용 |
|---------|---------|--------------|
| 서버 상태 | 매일 | 프로세스 실행 여부, 버전, 포트 |
| 세션 | 매일 | 접속 세션 수, 장시간 실행 쿼리 |
| 디스크 사용량 | 매일 | 데이터 디렉터리 사용률, 여유 공간 |
| 메모리 사용량 | 매일 | 시스템 메모리 여유, 프로세스 RSS |
| 백업 완료 여부 | 매일 (백업 실행 후) | 백업 성공 로그, 파일 존재 여부 |
| 장애 징후 | 이상 발생 시 | 오류 로그, 느린 쿼리, 연결 실패 |

### 빠른 점검 SQL

아래 쿼리는 서버에 접속 후 즉시 실행하여 주요 상태를 한눈에 확인합니다.

```sql
-- 서버 버전 확인
SELECT binary_signature FROM v$version;

-- 서버 설정 포트 확인
SELECT name, value FROM v$property WHERE name = 'PORT_NO';

-- 현재 접속 세션 수
SELECT count(*) AS session_count FROM v$session WHERE closed = 0;

-- 디스크 사용량 요약
SELECT used_ratio, ratio_cap FROM v$storage_usage;

-- 실행 중인 쿼리
SELECT sess_id, state, query
  FROM v$stmt
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%'
    OR state LIKE 'Append in progress%';
```

### 이 섹션의 구성

- [서버 상태 확인](/dbms/operations-configuration-recovery/diagnosis-observability/#status-check-state-server) — 서버 프로세스 상태, 버전, 포트 확인
- [세션과 실행 쿼리 확인](/dbms/operations-configuration-recovery/diagnosis-observability/#execution-session) — 접속 세션 목록, 실행 중인 쿼리, 세션 강제 종료
- [디스크 사용량 확인](/dbms/operations-configuration-recovery/diagnosis-observability/#capacity-disk) — 테이블별 디스크 사용량, OS 레벨 디스크 확인
- [메모리 사용량 확인](/dbms/operations-configuration-recovery/diagnosis-observability/#memory-capacity) — 프로세스 메모리, Result Cache 상태
- [백업 검증](/dbms/operations-configuration-recovery/diagnosis-observability/#validation-backup) — 백업 완료 후 무결성 검증 절차
- [장애 징후 확인](/dbms/operations-configuration-recovery/diagnosis-observability/#failure) — 디스크 풀, OOM, 느린 쿼리 등 장애 징후와 즉각 조치

<a id="status-check-state-server"></a>
<a id="monitoring-capacity-status-check-state-server"></a>

### 서버 상태 확인

Machbase 서버의 실행 여부와 기본 상태를 확인하는 방법을 설명합니다. OS 레벨 명령과 SQL 쿼리를 함께 사용합니다.

#### 서버 실행 여부 확인

##### machadmin으로 확인

`machadmin -e` 명령은 서버 프로세스의 실행 상태를 간단히 확인합니다.

```bash
# 서버 상태 확인
machadmin -e

# 출력 예시 (실행 중)
Machbase server is running with PID(12345).

# 출력 예시 (중지됨)
[Error] Machbase server is not running.
```

##### 프로세스 직접 확인

```bash
# Machbase 서버 프로세스 확인
pgrep -la machbased

# 포트 Listen 여부 확인 (기본 포트 5656)
ss -tlnp | grep 5656
```

#### 서버 버전과 시작 시간 확인

서버에 접속한 후 `V$VERSION` 가상 테이블로 버전 정보를 조회합니다.

```sql
-- 서버 버전 정보
SELECT binary_signature, edition
  FROM v$version;

-- 주요 버전 번호만 조회
SELECT binary_db_major_version AS major,
       binary_db_minor_version AS minor,
       binary_signature        AS version_string
  FROM v$version;
```

출력 예시:

```
BINARY_SIGNATURE        EDITION
----------------------  --------
8.6.0.official-LINUX    Standard
```

#### 서버 설정 확인

현재 서버에 적용된 주요 설정값을 확인합니다.

```sql
-- 포트 번호 확인
SELECT name, value
  FROM v$property
 WHERE name = 'PORT_NO';

-- 주요 설정 한 번에 확인
SELECT name, value
  FROM v$property
 WHERE name IN (
   'PORT_NO',
   'MAX_SESSION_COUNT',
   'TRACE_LOG_LEVEL',
   'DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC',
   'DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC'
 )
 ORDER BY name;

-- 기본값과 다른 설정만 조회
SELECT name, value, deflt
  FROM v$property
 WHERE value != deflt
 ORDER BY name;
```

#### HTTP 서비스 상태 확인

Machbase의 임베디드 HTTP 엔드포인트 상태를 확인합니다.

```sql
SELECT http_port,
       thread_count,
       connect_count,
       service_success_count,
       service_failure_count
  FROM v$http_status;
```

#### 라이선스 유효성 확인

```sql
-- 라이선스 정보와 위반 상태 확인
SELECT id, type, customer, issue_date,
       violate_status, violate_msg
  FROM v$license_info;
```

`VIOLATE_STATUS`가 0이 아닌 경우 라이선스 정책 위반 상태입니다.

#### 서버 시작/종료 이력 확인

서버 로그에서 시작/종료 이력을 확인합니다.

```bash
# 서버 시작 이력
grep 'server started\|server starting' $MACHBASE_HOME/trc/machbase.trc

# 서버 종료 이력
grep 'server stopped\|shutting down' $MACHBASE_HOME/trc/machbase.trc

# 비정상 종료 확인
grep 'SIGKILL\|Killed\|ABNORMAL' $MACHBASE_HOME/trc/machbase.trc
```

#### 점검 체크리스트

| 항목 | 명령/쿼리 | 정상 상태 |
|------|----------|---------|
| 프로세스 실행 | `machadmin -e` | `running` |
| 포트 Listen | `ss -tlnp \| grep 5656` | 5656 포트 확인 |
| 버전 확인 | `SELECT * FROM v$version` | 예상 버전 일치 |
| 라이선스 | `SELECT violate_status FROM v$license_info` | 0 (정상) |
| 디스크 사용률 | `SELECT used_ratio FROM v$storage_usage` | ratio_cap 미만 |

<a id="execution-session"></a>
<a id="monitoring-capacity-execution-session"></a>

### 세션과 실행 쿼리 확인

현재 접속된 세션 목록과 실행 중인 쿼리를 확인하고, 문제가 있는 세션을 강제 종료하는 방법을 설명합니다.

#### 현재 세션 목록 확인

`V$SESSION` 가상 테이블에서 현재 서버에 접속된 모든 세션을 조회합니다.

```sql
-- 현재 접속 세션 전체 목록
SELECT id, user_name, user_ip, client_type, login_time
  FROM v$session
 WHERE closed = 0
 ORDER BY login_time;
```

```sql
-- 세션 수 요약
SELECT count(*) AS active_session_count
  FROM v$session
 WHERE closed = 0;
```

##### V$SESSION 주요 컬럼

| 컬럼 이름 | 설명 |
|---------|------|
| ID | 세션 식별자 |
| USER_NAME | 접속 사용자 이름 |
| USER_IP | 클라이언트 IP 주소 |
| CLIENT_TYPE | 클라이언트 타입 (JDBC, ODBC, CLI 등) |
| LOGIN_TIME | 접속 시각 |
| CLOSED | 0 = 활성, 1 = 종료됨 |
| IDLE_TIMEOUT | 유휴 세션 자동 종료 시간 (초) |
| QUERY_TIMEOUT | 쿼리 타임아웃 시간 |

#### 실행 중인 쿼리 확인

`V$STMT` 가상 테이블에서 현재 서버에서 처리 중인 SQL 문을 조회합니다.

```sql
-- 실행/Fetch/Append 진행 중인 쿼리 조회
SELECT id, sess_id, state, query
  FROM v$stmt
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%'
    OR state LIKE 'Append in progress%';
```

```sql
-- 세션 정보와 함께 실행 중인 쿼리 확인
SELECT s.id        AS session_id,
       s.user_name,
       s.user_ip,
       st.id       AS stmt_id,
       st.state,
       st.query
  FROM v$session s
  JOIN v$stmt    st ON s.id = st.sess_id
 WHERE st.state LIKE 'Execute in progress%'
    OR st.state LIKE 'Fetch in progress%'
    OR st.state LIKE 'Append in progress%'
 ORDER BY s.login_time;
```

> **참고**: `V$STMT`에는 `elapsed_time` 컬럼이 없습니다. 실행 시간 통계가 필요한 경우 `V$SESTIME`의 `ACCUM_MSEC` 값을 참조하십시오.

#### 세션별 시간 통계

`V$SESTIME`에서 세션별로 누적 실행 시간 통계를 확인할 수 있습니다.

```sql
-- 세션별 누적 실행 시간 확인
SELECT st.sid, s.user_name, s.user_ip,
       st.id      AS time_unit_id,
       st.accum_msec,
       st.max_msec
  FROM v$sestime st
  JOIN v$session s ON st.sid = s.id
 WHERE s.closed = 0
 ORDER BY st.accum_msec DESC;
```

#### 특정 세션 강제 종료

문제가 있는 세션(장시간 블로킹, 잘못된 쿼리 등)을 강제로 종료합니다.

```sql
-- 특정 세션 강제 종료 (세션 ID = 7)
ALTER SYSTEM KILL SESSION 7;
```

강제 종료 전에 반드시 세션 ID를 `V$SESSION`에서 확인하고, 해당 세션이 처리 중인 트랜잭션이 없는지 확인하십시오.

```sql
-- 종료 대상 세션 확인
SELECT id, user_name, user_ip, login_time
  FROM v$session
 WHERE id = 7;

-- 해당 세션의 실행 중인 쿼리 확인
SELECT id, state, query
  FROM v$stmt
 WHERE sess_id = 7;

-- 확인 후 종료
ALTER SYSTEM KILL SESSION 7;
```

#### 세션 메모리 사용량 확인

```sql
-- 세션별 메모리 사용량
SELECT sm.sid,
       s.user_name,
       sm.id     AS mem_manager_id,
       sm.usage  AS memory_bytes
  FROM v$sesmem sm
  JOIN v$session s ON sm.sid = s.id
 WHERE s.closed = 0
 ORDER BY sm.usage DESC;
```

#### 최대 세션 수 설정 확인

```sql
-- 현재 설정된 최대 세션 수
SELECT name, value
  FROM v$property
 WHERE name = 'MAX_SESSION_COUNT';

-- 현재 세션 수와 최대 세션 수 비교
SELECT (SELECT value FROM v$property WHERE name = 'MAX_SESSION_COUNT') AS max_sessions,
       (SELECT count(*) FROM v$session WHERE closed = 0)               AS current_sessions;
```

현재 세션 수가 최대 세션 수의 80%를 초과하면 새 연결 실패 위험이 있습니다. `MAX_SESSION_COUNT` 값을 조정하거나 오래된 세션을 정리하십시오.

#### 세션 설정 변경

특정 세션의 타임아웃 설정을 변경합니다.

```sql
-- 현재 세션의 쿼리 타임아웃 설정 (단위: 초)
ALTER SESSION SET QUERY_TIMEOUT = 300;

-- 현재 세션의 유휴 타임아웃 설정 (단위: 초, 0 = 무제한)
ALTER SESSION SET IDLE_TIMEOUT = 1800;
```

<a id="capacity-disk"></a>
<a id="monitoring-capacity-capacity-disk"></a>

### 디스크 사용량 확인

Machbase 데이터 파일이 저장된 디스크의 사용량을 SQL과 OS 명령으로 확인하는 방법을 설명합니다. 디스크가 가득 차면 데이터 적재와 인덱스 구축이 자동으로 중단되므로 정기적인 모니터링이 필수입니다.

#### 스토리지 사용량 개요

`V$STORAGE_USAGE`는 Machbase 데이터 디렉터리가 위치한 스토리지의 전체 사용 현황을 보여줍니다.

```sql
-- 스토리지 사용량 확인
SELECT total_space,
       used_space,
       used_ratio,
       ratio_cap
  FROM v$storage_usage;
```

| 컬럼 | 설명 |
|------|------|
| TOTAL_SPACE | 스토리지 전체 용량 (MiB) |
| USED_SPACE | 사용 중인 용량 (MiB) |
| USED_RATIO | 사용률 (%) |
| RATIO_CAP | 허용 최대 사용률 (%). 이 값 초과 시 데이터 입력 중단 |

`USED_RATIO`가 `RATIO_CAP`에 근접하면 즉시 조치가 필요합니다.

#### 테이블별 디스크 사용량

`V$STORAGE_TABLES`에서 각 테이블이 스토리지에서 점유한 용량을 확인합니다.

```sql
-- 테이블별 스토리지 사용량 (큰 순서대로)
SELECT id, type, status, storage_usage
  FROM v$storage_tables
 ORDER BY storage_usage DESC;
```

테이블 이름을 함께 조회하려면 메타 테이블과 JOIN합니다.

```sql
-- 테이블 이름과 스토리지 사용량
SELECT t.name          AS table_name,
       t.type          AS table_type,
       vs.storage_usage AS used_bytes,
       round(vs.storage_usage / 1073741824.0, 2) AS used_gb
  FROM v$storage_tables vs
  JOIN m$sys_tables t ON vs.id = t.id
 ORDER BY vs.storage_usage DESC;
```

#### 컬럼별 디스크 사용량

특정 테이블에서 용량을 많이 차지하는 컬럼을 파악합니다.

```sql
-- 특정 테이블의 컬럼별 파일 크기 확인
SELECT dc.id           AS column_id,
       mc.name         AS column_name,
       dc.disk_file_size AS disk_bytes,
       round(dc.disk_file_size / 1073741824.0, 2) AS disk_gb
  FROM v$storage_dc_table_columns dc
  JOIN m$sys_tables  mt ON dc.table_id = mt.id
  JOIN m$sys_columns mc ON dc.id = mc.id AND mc.table_id = mt.id
 WHERE mt.name = 'SENSOR_LOG'
 ORDER BY dc.disk_file_size DESC;
```

#### 인덱스 파일 크기 확인

```sql
-- 인덱스 파일 크기 확인
SELECT di.id           AS index_id,
       mi.name         AS index_name,
       di.disk_file_size AS disk_bytes
  FROM v$storage_dc_table_indexes di
  JOIN m$sys_tables  mt ON di.table_id = mt.id
  JOIN m$sys_indexes mi ON di.id = mi.id
 WHERE mt.name = 'SENSOR_LOG'
 ORDER BY di.disk_file_size DESC;
```

#### 테이블스페이스 정보 확인

```sql
-- 테이블스페이스와 디스크 경로 확인
SELECT ts.name AS tablespace_name,
       d.path,
       d.io_thread_count
  FROM v$storage_dc_tablespace_disks d
  JOIN v$storage_dc_tablespaces ts ON d.tablespace_id = ts.id;
```

#### OS 레벨 디스크 확인

SQL 조회와 함께 OS 명령으로 디스크 여유 공간을 확인합니다.

```bash
# 전체 파티션 디스크 사용량
df -h

# Machbase 데이터 디렉터리 사용량
df -h $MACHBASE_HOME/dbs/

# 데이터 디렉터리 내 파일 크기 합계
du -sh $MACHBASE_HOME/dbs/

# 큰 파일 상위 20개 확인
du -sh $MACHBASE_HOME/dbs/*/ | sort -rh | head -20
```

#### 디스크 풀 임박 시 조치

`USED_RATIO`가 `RATIO_CAP`의 90% 이상에 도달하면 아래 조치를 취합니다.

##### 1. 불필요한 파일 제거

```bash
# 오래된 트레이스 로그 압축
gzip $MACHBASE_HOME/trc/machbase.trc.2024*

# 30일 이상 된 로그 파일 삭제
find $MACHBASE_HOME/trc/ -name "*.trc.*" -mtime +30 -delete
```

##### 2. Retention Policy로 오래된 데이터 삭제

```sql
-- 특정 시점 이전 데이터 삭제 (Log 테이블)
DELETE FROM sensor_log BEFORE TO_DATE('2023-01-01', 'YYYY-MM-DD');

-- 삭제 후 테이블 통계 확인
SELECT id, storage_usage FROM v$storage_tables
 ORDER BY storage_usage DESC;
```

##### 3. RATIO_CAP 조정

`DISK_USED_RATIO_CAP`은 설정 파일에서 관리합니다. 실제 디스크 공간 확보 없이 이 설정만 높이면 OS 레벨에서 실제 디스크가 가득 찰 수 있으므로 주의합니다.

```sql
-- 현재 DISK_USED_RATIO_CAP 설정 확인
SELECT name, value FROM v$property WHERE name = 'DISK_USED_RATIO_CAP';
```

#### 주기적 모니터링 스크립트 예시

```bash
#!/bin/bash
# check_disk.sh — 디스크 사용량 경보 스크립트

THRESHOLD=80

cat > /tmp/check_disk.sql <<'SQL'
SELECT used_ratio FROM v$storage_usage;
SQL

USED=$(machsql -u sys -p manager -s 127.0.0.1 -f /tmp/check_disk.sql \
  2>/dev/null | awk '/^[[:space:]]*[0-9]+(\\.[0-9]+)?[[:space:]]*$/ {print int($1); exit}')

if [ "$USED" -gt "$THRESHOLD" ]; then
    echo "[WARN] Machbase disk usage: ${USED}% (threshold: ${THRESHOLD}%)"
    df -h $MACHBASE_HOME/dbs/
fi
```

<a id="memory-capacity"></a>
<a id="monitoring-capacity-memory-capacity"></a>

### 메모리 사용량 확인

Machbase 서버의 메모리 사용 현황을 SQL과 OS 명령으로 확인하는 방법을 설명합니다. 메모리 부족은 쿼리 오류, 서버 불안정, OOM Killer 강제 종료로 이어질 수 있으므로 주의가 필요합니다.

#### 시스템 메모리 사용량

`V$SYSMEM`은 Machbase 내부의 메모리 매니저별 사용 현황을 표시합니다.

```sql
-- 메모리 매니저별 현재 사용량 및 최대 사용량
SELECT name,
       usage                           AS current_bytes,
       max_usage                       AS peak_bytes,
       round(usage / 1048576.0, 1)     AS current_mb,
       round(max_usage / 1048576.0, 1) AS peak_mb
  FROM v$sysmem
 ORDER BY usage DESC;
```

| 컬럼 | 설명 |
|------|------|
| NAME | 메모리 매니저 이름 |
| USAGE | 현재 사용 중인 메모리 (바이트) |
| MAX_USAGE | 서버 시작 이후 기록된 최대 사용량 |

#### 세션별 메모리 사용량

```sql
-- 세션별 메모리 사용량 (상위 10개)
SELECT sm.sid,
       s.user_name,
       s.user_ip,
       sum(sm.usage)                        AS total_bytes,
       round(sum(sm.usage) / 1048576.0, 1)  AS total_mb
  FROM v$sesmem sm
  JOIN v$session s ON sm.sid = s.id
 WHERE s.closed = 0
 GROUP BY sm.sid, s.user_name, s.user_ip
 ORDER BY total_bytes DESC
 LIMIT 10;
```

메모리를 많이 사용하는 세션을 파악하면 `MAX_QPX_MEM` 설정 조정이나 해당 세션 종료 여부를 결정하는 데 도움이 됩니다.

#### Result Cache 메모리 상태

Result Cache가 활성화된 경우, 캐시 메모리 사용량을 확인합니다.

```sql
-- Result Cache 통계
SELECT cache_count,
       cache_hit,
       aggr_hit,
       cache_replaced,
       cache_memory_usage,
       round(cache_memory_usage / 1048576.0, 1) AS cache_mb
  FROM v$rs_cache_stat;
```

`cache_replaced` 값이 지속적으로 증가하면 캐시 메모리가 부족하여 캐시가 자주 교체되고 있는 것입니다. 전역 Result Cache 메모리 한도는 `machbase.conf`의 `RS_CACHE_MAX_MEMORY_SIZE` 파라미터로 조정한 뒤 재시작하여 적용합니다.

#### Page Cache 상태

```sql
-- Page Cache 현재 상태
SELECT max_mem_size,
       cur_mem_size,
       page_cnt,
       round(cur_mem_size / 1048576.0, 1) AS cur_mb,
       round(max_mem_size / 1048576.0, 1) AS max_mb
  FROM v$storage_dc_pagecache;
```

#### Volatile 테이블 메모리

Volatile 테이블은 메모리에만 데이터를 저장합니다.

```sql
-- Volatile 테이블스페이스 메모리 사용량
SELECT round(max_mem_size / 1048576.0, 1) AS max_mb,
       round(cur_mem_size / 1048576.0, 1) AS current_mb
  FROM v$storage_dc_volatile_table;
```

#### OS 레벨 메모리 확인

Machbase 프로세스의 실제 메모리 사용량을 OS 레벨에서 확인합니다.

```bash
# 시스템 전체 메모리 상태
free -h

# Machbase 프로세스의 메모리 사용량
top -b -n 1 -p $(pgrep machbased) | tail -3

# RSS(상주 메모리), VSZ(가상 메모리) 확인
ps aux | grep machbased | grep -v grep

# /proc에서 상세 메모리 정보 확인
cat /proc/$(pgrep machbased)/status | grep -i 'vmrss\|vmsize\|vmswap'
```

#### 메모리 관련 주요 설정

```sql
-- 메모리 관련 설정 확인
SELECT name, value, deflt
  FROM v$property
 WHERE name IN (
   'MAX_QPX_MEM',
   'RS_CACHE_MAX_MEMORY_SIZE',
   'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE',
   'TAG_CACHE_MAX_MEMORY_SIZE'
 )
 ORDER BY name;
```

| 파라미터 | 설명 |
|---------|------|
| MAX_QPX_MEM | 세션당 최대 쿼리 메모리 (바이트) |
| RS_CACHE_MAX_MEMORY_SIZE | Result Cache 최대 메모리 |
| VOLATILE_TABLESPACE_MEMORY_MAX_SIZE | Volatile 테이블스페이스 최대 메모리 |
| TAG_CACHE_MAX_MEMORY_SIZE | Tag 테이블 캐시 최대 메모리 |

#### 메모리 부족 징후 대응

##### 쿼리 메모리 부족 오류

```
[ERROR] [QUERY] Query aborted due to memory limit. sess_id=5
```

```ini
# machbase.conf
MAX_QPX_MEM = 536870912   # 세션당 512MB
```

##### 시스템 메모리 부족

```bash
# OOM Killer 발동 여부 확인 (Ubuntu/Debian)
grep 'Out of memory\|oom_kill' /var/log/syslog | tail -20

# OOM Killer 발동 여부 확인 (RHEL/CentOS)
grep 'Out of memory\|oom_kill' /var/log/messages | tail -20

# dmesg에서 확인
dmesg | grep -i 'oom\|killed process'
```

OOM Killer가 `machbased` 프로세스를 종료한 경우, 서버 재시작 후 메모리 설정을 검토합니다.

<a id="validation-backup"></a>
<a id="monitoring-capacity-validation-backup"></a>

### 백업 검증

백업이 완료된 후 해당 백업 파일이 실제로 복구 가능한 상태인지 검증하는 절차를 설명합니다. 백업 파일이 존재하더라도 손상된 경우 복구에 실패할 수 있으므로, 정기적인 검증이 필요합니다.

#### 백업 완료 확인

백업 실행 후 서버 로그에서 완료 여부를 확인합니다.

```bash
# 백업 완료 로그 확인
grep 'Backup completed\|Backup failed' $MACHBASE_HOME/trc/machbase.trc | tail -10
```

정상 완료 시:
```
[2024-01-15 03:00:15.001] [INFO] [BACKUP] Backup completed. path=/backup/20240115, elapsed=125s
```

백업 실패 시:
```
[2024-01-15 03:00:15.001] [ERROR] [BACKUP] Backup failed. path=/backup/20240115, reason=Disk full
```

#### 백업 파일 존재 여부 확인

```bash
# 백업 디렉터리 크기 확인
du -sh /backup/20240115/

# 백업 파일 목록 확인
ls -lh /backup/20240115/

# 최소한의 필수 파일 존재 여부
ls /backup/20240115/backup.dat /backup/20240115/meta.dbs-* 2>/dev/null
```

#### Mount를 이용한 백업 검증

가장 확실한 검증 방법은 백업 데이터베이스를 마운트하여 실제 데이터를 조회하는 것입니다. 마운트는 운영 데이터베이스에 영향을 주지 않습니다.

##### 1단계: 백업 데이터베이스 마운트

```sql
-- 백업을 testdb라는 이름으로 마운트
MOUNT DATABASE '/backup/20240115' TO testdb;
```

##### 2단계: 마운트 상태 확인

```sql
-- 마운트된 데이터베이스 목록 확인
SELECT name, path, backup_begin_time, backup_end_time,
       db_begin_time, db_end_time
  FROM v$storage_mount_databases;
```

##### 3단계: 마운트된 데이터 조회

```sql
-- 마운트된 테이블 조회 (testdb 접두어 사용)
SELECT count(*) FROM testdb.sys.sensor_log;

-- 데이터 범위 확인
SELECT min(_arrival_time) AS earliest,
       max(_arrival_time) AS latest,
       count(*)           AS total_rows
  FROM testdb.sys.sensor_log;

-- 일부 레코드 샘플 확인
SELECT * FROM testdb.sys.sensor_log LIMIT 10;
```

##### 4단계: 마운트 해제

검증 완료 후 마운트를 해제합니다.

```sql
UMOUNT DATABASE testdb;
```

#### 백업 파일 무결성 체크섬 확인

파일 수준의 무결성을 확인합니다.

```bash
# 백업 직후 체크섬 생성 및 저장
find /backup/20240115/ -type f | sort | xargs md5sum > /backup/20240115.md5

# 이후 검증 시 체크섬 비교
md5sum -c /backup/20240115.md5
```

체크섬 불일치가 발생하면 해당 파일이 손상된 것이며, 그 백업 세트는 복구에 사용할 수 없습니다.

#### 백업 검증 자동화

정기 백업 스크립트에 검증 단계를 포함합니다.

```bash
#!/bin/bash
# backup_and_verify.sh

BACKUP_PATH="/backup/$(date +%Y%m%d)"
DB_USER="sys"
DB_PASS="manager"
DB_HOST="127.0.0.1"

# 1. 백업 실행
cat > /tmp/backup.sql <<SQL
BACKUP DATABASE INTO DISK = '${BACKUP_PATH}';
SQL
machsql -u $DB_USER -p $DB_PASS -s $DB_HOST -f /tmp/backup.sql > /tmp/backup.log 2>&1

if [ $? -eq 0 ]; then
    echo "[OK] Backup completed: $BACKUP_PATH"
else
    echo "[FAIL] Backup failed. Check /tmp/backup.log"
    exit 1
fi

# 2. 체크섬 생성
find $BACKUP_PATH -type f | sort | xargs md5sum > ${BACKUP_PATH}.md5
echo "[OK] Checksum created: ${BACKUP_PATH}.md5"

# 3. 마운트 검증
cat > /tmp/verify_backup.sql <<SQL
MOUNT DATABASE '${BACKUP_PATH}' TO verify_db;
SELECT count(*) FROM verify_db.sys.sensor_log;
UMOUNT DATABASE verify_db;
SQL
ROW_COUNT=$(machsql -u $DB_USER -p $DB_PASS -s $DB_HOST -f /tmp/verify_backup.sql \
  2>/dev/null | awk '/^[[:space:]]*[0-9]+[[:space:]]*$/ {print $1; exit}')

if [ -n "$ROW_COUNT" ] && [ "$ROW_COUNT" -gt 0 ]; then
    echo "[OK] Backup verified. Row count: $ROW_COUNT"
else
    echo "[WARN] Backup mount verification may have failed. Check manually."
fi
```

#### 백업 보관 정책

| 백업 유형 | 보관 기간 | 검증 주기 |
|---------|---------|---------|
| 일별 백업 | 7일 | 매 백업 후 |
| 주별 백업 | 4주 | 주 1회 |
| 월별 백업 | 12개월 | 월 1회 |

오래된 백업 파일은 정기적으로 삭제하여 디스크 공간을 확보합니다.

```bash
# 7일 이상 된 일별 백업 삭제
find /backup/ -maxdepth 1 -type d -name "20*" -mtime +7 -exec rm -rf {} \;
```

> **중요**: 백업 검증은 백업 완료 직후뿐 아니라 정기적으로(최소 월 1회) 수행해야 합니다. 장애 발생 시 검증되지 않은 백업은 복구 실패로 이어질 수 있습니다.

<a id="failure"></a>
<a id="monitoring-capacity-failure"></a>

### 장애 징후 확인

장애가 발생하기 전에 징후를 발견하여 선제적으로 대응하는 것이 중요합니다. 아래 패턴들을 정기적으로 확인하거나, 이상 증상이 보일 때 단계적으로 점검합니다.

#### 디스크 풀 징후

##### 징후

- 데이터 적재가 갑자기 중단됨
- machbase.trc에 디스크 관련 오류가 반복됨
- Machbase 오류: "Disk full" 또는 "errno=28"

##### 확인 방법

```bash
# OS 레벨 디스크 확인
df -h

# Machbase 데이터 디렉터리 특정 확인
df -h $MACHBASE_HOME/dbs/
```

```sql
-- 스토리지 사용률과 한계 확인
SELECT used_ratio, ratio_cap
  FROM v$storage_usage;
```

```bash
# 서버 로그에서 디스크 관련 오류 확인
grep -i 'disk full\|errno=28\|No space left' $MACHBASE_HOME/trc/machbase.trc | tail -20
```

##### 즉각 조치

1. 오래된 트레이스 로그 삭제: `find $MACHBASE_HOME/trc/ -name "*.trc.*" -mtime +30 -delete`
2. 오래된 데이터 삭제: `DELETE FROM <table> BEFORE TO_DATE('...', 'YYYY-MM-DD');`
3. `DISK_USED_RATIO_CAP` 설정 검토 (실제 공간 확보 병행 필수)

---

#### 메모리 과다 사용 징후

##### 징후

- 서버 프로세스가 갑자기 종료됨
- 쿼리 실행 시 메모리 부족 오류 발생
- 시스템 응답이 매우 느려짐

##### 확인 방법

```bash
# 시스템 전체 메모리 확인
free -h

# Machbase 프로세스 메모리 사용량
ps aux | grep machbased | grep -v grep

# OOM Killer 발동 여부 확인
grep 'Out of memory\|oom_kill' /var/log/syslog 2>/dev/null | tail -10
dmesg | grep -i 'oom\|killed process' | tail -10
```

```sql
-- 메모리 매니저별 사용량
SELECT name, round(usage/1048576.0, 1) AS mb, round(max_usage/1048576.0, 1) AS peak_mb
  FROM v$sysmem
 ORDER BY usage DESC;

-- 메모리 과다 사용 세션 확인
SELECT sm.sid, s.user_name, round(sum(sm.usage)/1048576.0, 1) AS mb
  FROM v$sesmem sm
  JOIN v$session s ON sm.sid = s.id
 WHERE s.closed = 0
 GROUP BY sm.sid, s.user_name
 ORDER BY mb DESC;
```

##### 즉각 조치

1. 메모리 과다 세션 강제 종료: `ALTER SYSTEM KILL SESSION <id>;`
2. `MAX_QPX_MEM` 설정으로 세션당 쿼리 메모리 제한
3. Volatile 테이블 또는 Result Cache 메모리 설정 검토

---

#### 세션 과다 징후

##### 징후

- 새로운 연결이 거부됨
- machbase.trc에 "Max session count reached" 오류 발생

##### 확인 방법

```sql
-- 현재 세션 수와 최대 세션 수 비교
SELECT (SELECT value FROM v$property WHERE name = 'MAX_SESSION_COUNT') AS max_sessions,
       (SELECT count(*) FROM v$session WHERE closed = 0)               AS current_sessions;

-- 오래 접속된 세션 확인 (오늘보다 하루 이상 이전)
SELECT id, user_name, user_ip, login_time
  FROM v$session
 WHERE closed = 0
 ORDER BY login_time ASC
 LIMIT 20;
```

##### 즉각 조치

1. 불필요한 세션 정리: `ALTER SYSTEM KILL SESSION <id>;`
2. `MAX_SESSION_COUNT` 값 검토 및 상향
3. 클라이언트 애플리케이션의 커넥션 풀 설정 점검

---

#### 느린 쿼리 징후

##### 징후

- 평소보다 쿼리 응답이 느림
- 애플리케이션 타임아웃 오류 발생
- 서버 CPU 사용률이 지속적으로 높음

##### 확인 방법

```sql
-- 현재 실행 중인 쿼리 확인
SELECT id, sess_id, state, query
  FROM v$stmt
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%'
    OR state LIKE 'Append in progress%';

-- 세션별 누적 실행 시간 확인 (큰 순서)
SELECT st.sid, s.user_name,
       st.accum_msec, st.max_msec
  FROM v$sestime st
  JOIN v$session s ON st.sid = s.id
 WHERE s.closed = 0
 ORDER BY st.accum_msec DESC
 LIMIT 10;
```

```sql
-- 시스템 전반 통계 확인
SELECT name, value
  FROM v$sysstat
 ORDER BY name;
```

##### 즉각 조치

1. 오래 실행 중인 쿼리의 세션 강제 종료
2. 쿼리 실행 계획 확인 (인덱스 누락 여부)
3. 필요한 모듈 비트를 추가해 `TRACE_LOG_LEVEL`을 일시적으로 높여 상세 로그 수집

---

#### Rollup/Stream 이상 징후

##### 확인 방법

```sql
-- Rollup 비활성화 또는 오류 확인
SELECT rollup_table, source_table, enabled, run_state, last_elapsed_msec
  FROM v$rollup
 WHERE enabled = 0 OR run_state != 'S';

-- Stream 오류 확인
SELECT name, state, error_msg
  FROM v$streams
 WHERE error_msg IS NOT NULL AND error_msg != '';
```

---

#### 장애 발생 시 즉각 조치 체크리스트

장애 또는 이상 증상 발생 시 아래 순서로 점검합니다.

| 단계 | 확인 항목 | 명령/쿼리 |
|------|---------|---------|
| 1 | 서버 프로세스 실행 여부 | `machadmin -e` |
| 2 | 서버 로그 오류 확인 | `tail -100 $MACHBASE_HOME/trc/machbase.trc` |
| 3 | 디스크 사용률 | `df -h` 및 `SELECT used_ratio FROM v$storage_usage` |
| 4 | 메모리 여유 | `free -h` |
| 5 | OOM 발생 여부 | `dmesg \| grep -i oom` |
| 6 | 세션 과다 여부 | `SELECT count(*) FROM v$session WHERE closed = 0` |
| 7 | 실행 중인 쿼리 | `SELECT * FROM v$stmt WHERE state LIKE 'Execute in progress%'` |
| 8 | 라이선스 위반 | `SELECT violate_status FROM v$license_info` |

체크리스트 점검 후 원인이 파악되면 해당 섹션의 조치 지침을 따릅니다. 원인이 불명확하면 `TRACE_LOG_LEVEL`을 높여 상세 로그를 수집한 뒤 Machbase 지원팀에 로그를 제공하십시오.
