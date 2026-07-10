---
type: docs
title: '15.5 Collector로 파일/소켓 데이터 수집하기'
weight: 70
toc: true
---

## 시나리오 개요

Machbase Collector는 로컬 파일, TCP/UDP 소켓, 시리얼 포트 등 외부 데이터 소스에서 데이터를 수집하여 자동으로 적재하는 컴포넌트입니다. 데몬 형태로 상시 동작하며, 설정 파일을 통해 수집 소스와 적재 대상 테이블을 연결합니다. 여기서는 CSV 파일 감시 수집과 TCP 소켓 수집을 중심으로 실전 설정 방법을 다룹니다.

---

## 수집 파이프라인 구조

```
                        ┌─────────────────────────────┐
  [로컬 CSV 파일]  ──→  │                             │
  [TCP 소켓 스트림] ──→ │     Machbase Collector       │ ──→ [Machbase DB]
  [UDP 패킷]       ──→  │   (배치 버퍼 + Append API)  │
  [시리얼 포트]    ──→  │                             │
                        └─────────────────────────────┘
```

Collector는 소스에서 수신한 데이터를 내부 큐에 버퍼링한 후, 설정된 배치 크기 또는 flush 주기가 되면 Machbase Append API로 일괄 적재합니다.

---

## 1단계: Collector 소개

### 주요 특징

- **무중단 파일 감시:** 지정 디렉터리에 새 파일이 생성되면 자동으로 감지하여 적재
- **위치 추적(position tracking):** 파일 오프셋을 기록해 중단 후 재시작 시 이어서 수집
- **다중 소스 동시 수집:** 하나의 Collector 인스턴스에서 여러 소스를 병렬로 처리
- **Append API 기반:** INSERT가 아닌 고속 Append로 적재

### Collector 설치 위치

```bash
$MACHBASE_HOME/bin/machcollector      # Collector 실행 파일
$MACHBASE_HOME/conf/collector/        # 설정 파일 디렉터리
$MACHBASE_HOME/trc/                   # 트레이스 로그 디렉터리
```

---

## 2단계: 파일 수집 설정 (CSV 파일 감시)

### 대상 테이블 생성

```sql
-- 파일 수집 대상 테이블 (LOG 테이블)
CREATE TABLE file_sensor_log (
    _arrival_time DATETIME,
    device_id     VARCHAR(64),
    sensor_type   VARCHAR(32),
    value         DOUBLE,
    quality       INTEGER
);
```

### Collector 템플릿 예시 (파일 소스)

Collector는 `machcollectoradmin --startup`으로 manager를 기동한 뒤, SQL의
`CREATE COLLECTOR`/`ALTER COLLECTOR` 구문으로 생성하고 제어합니다.
템플릿 파일은 운영 환경에 맞는 경로에 저장합니다.

```ini
########################################
# Machbase Collector - 파일 수집 템플릿 예시
########################################

# Machbase 연결 정보
DB_ADDR       = 127.0.0.1
DB_PORT       = 5656
DB_USER       = SYS
DB_PASSWORD   = MANAGER
DB_TABLE_NAME = file_sensor_log

# 수집 소스 유형: FILE
LOG_SOURCE    = FILE

# 감시할 디렉터리와 파일 패턴
COLLECTOR_FILE_WATCH_DIR  = /data/sensors/incoming
COLLECTOR_FILE_PATTERN    = sensor_*.csv

# 파일 인코딩
COLLECTOR_FILE_ENCODING   = UTF-8

# CSV 구분자 (기본: 쉼표)
COLLECTOR_FILE_DELIMITER  = ,

# 첫 번째 행 헤더 여부
COLLECTOR_FILE_HEADER     = YES

# 적재 대상 테이블
COLLECTOR_TARGET_TABLE    = file_sensor_log

# 배치 크기 (건수)
COLLECTOR_BATCH_SIZE      = 5000

# flush 주기 (초)
COLLECTOR_FLUSH_INTERVAL  = 3

# 수집 완료 파일 이동 디렉터리
COLLECTOR_FILE_DONE_DIR   = /data/sensors/done

# 오류 파일 이동 디렉터리
COLLECTOR_FILE_ERROR_DIR  = /data/sensors/error

# 트레이스 로그 레벨 (0: 없음, 1: 기본, 2: 상세)
COLLECTOR_TRACE_LEVEL     = 1
```

### 수집 대상 CSV 파일 형식

```csv
device_id,sensor_type,value,quality
DEVICE_A,TEMP,72.3,100
DEVICE_A,PRESS,1.04,100
DEVICE_B,TEMP,68.5,100
DEVICE_B,HUMID,55.2,100
```

> **주의:** `_arrival_time` 컬럼은 Collector가 수집 시각을 자동으로 기록합니다. CSV 파일에 포함하지 않거나, 포함할 경우 `YYYY-MM-DD HH24:MI:SS` 형식이어야 합니다.

---

## 3단계: TCP 소켓 수집 설정

네트워크 장비나 소프트웨어에서 TCP로 직접 데이터를 전송하는 경우의 설정입니다.

### 대상 테이블 생성

```sql
-- TCP 소켓 수집 대상 테이블
CREATE TABLE tcp_event_log (
    _arrival_time DATETIME,
    client_ip     VARCHAR(40),
    event_code    INTEGER,
    message       VARCHAR(1024)
);
```

### Collector 설정 파일 예시 (TCP 소켓 소스)

`$MACHBASE_HOME/conf/collector/tcp_collector.conf`:

```ini
########################################
# Machbase Collector - TCP 소켓 수집 설정
########################################

# Machbase 연결 정보
COLLECTOR_SERVER_HOST     = localhost
COLLECTOR_SERVER_PORT     = 5656
COLLECTOR_SERVER_USER     = SYS
COLLECTOR_SERVER_PASSWORD = MANAGER

# 수집 소스 유형: TCP
COLLECTOR_SOURCE_TYPE     = TCP

# Collector가 리슨할 TCP 포트
COLLECTOR_TCP_LISTEN_PORT = 9000

# 연결 허용 IP 범위 (CIDR 표기 또는 ALL)
COLLECTOR_TCP_ALLOW_IP    = 192.168.0.0/24

# 메시지 구분자 (개행 문자 기준)
COLLECTOR_TCP_DELIMITER   = \n

# 필드 구분자 (한 줄 내 필드 분리)
COLLECTOR_FIELD_DELIMITER = ,

# 적재 대상 테이블
COLLECTOR_TARGET_TABLE    = tcp_event_log

# 배치 크기
COLLECTOR_BATCH_SIZE      = 1000

# flush 주기 (초)
COLLECTOR_FLUSH_INTERVAL  = 1

# 클라이언트 재연결 대기 시간 (초)
COLLECTOR_TCP_RECONNECT_INTERVAL = 5

# 최대 동시 연결 수
COLLECTOR_TCP_MAX_CONNECTIONS    = 50

COLLECTOR_TRACE_LEVEL     = 1
```

### 클라이언트에서 데이터 전송 예시

```python
# TCP로 Collector에 데이터 전송하는 클라이언트 예시
import socket
import time

COLLECTOR_HOST = "localhost"
COLLECTOR_PORT = 9000

def send_events(events):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((COLLECTOR_HOST, COLLECTOR_PORT))
        for event in events:
            # 형식: client_ip,event_code,message\n
            line = f"{event['client_ip']},{event['code']},{event['msg']}\n"
            s.sendall(line.encode("utf-8"))
            time.sleep(0.001)

events = [
    {"client_ip": "192.168.0.10", "code": 200, "msg": "normal"},
    {"client_ip": "192.168.0.11", "code": 500, "msg": "error occurred"},
]
send_events(events)
```

---

## 4단계: 수집 주기와 배치 크기 설정

데이터 특성에 따라 배치 크기와 flush 주기를 조정합니다.

| 데이터 특성 | 배치 크기 | flush 주기 | 설명 |
|------------|:--------:|:----------:|------|
| 고빈도 센서 (100Hz 이상) | 10,000건 | 1초 | 처리량 우선 |
| 일반 IoT (1Hz) | 1,000~5,000건 | 1~5초 | 균형 |
| 이벤트 로그 (불규칙) | 500건 | 5~10초 | 지연 허용 |
| 실시간 알람 | 1~10건 | 즉시 flush | 레이턴시 우선 |

```ini
# 고빈도 센서 설정 예시
COLLECTOR_BATCH_SIZE      = 10000
COLLECTOR_FLUSH_INTERVAL  = 1

# 실시간 알람 설정 예시
COLLECTOR_BATCH_SIZE      = 1
COLLECTOR_FLUSH_INTERVAL  = 0   # 0이면 즉시 flush
```

---

## 5단계: 병렬 스레드 수 설정

Collector의 병렬 스레드 수는 Machbase 에디션과 구성에 따라 다르게 설정합니다.

```ini
# Standard Edition: CPU 코어 수의 1/2 ~ 2/3
# 예: 8코어 서버 → 4~5개 스레드
COLLECTOR_WORKER_THREADS  = 4

# Cluster Edition: Warehouse 노드 수 × 1~2
# 예: Warehouse 4노드 → 4~8개 스레드
COLLECTOR_WORKER_THREADS  = 8
```

다중 소스를 수집할 때는 소스별 템플릿을 준비하고 Collector를 별도로 생성합니다.

```bash
# Collector manager 기동
machcollectoradmin --startup
```

```sql
CREATE COLLECTOR localhost.file_sensor
FROM "$MACHBASE_HOME/collector/file_sensor.tpl";

ALTER COLLECTOR localhost.file_sensor START;
ALTER COLLECTOR localhost.file_sensor STOP;
```

---

## 6단계: 큐 모니터링 방법

Collector의 내부 큐 상태를 트레이스 로그로 모니터링합니다.

```bash
# Collector 트레이스 로그에서 큐 지연·오버플로우 확인
grep -i "queue\|delay\|overflow\|slow" \
    "$MACHBASE_COLLECTOR_HOME/trc/machcollector.trc" | tail -50
```

```bash
# 실시간 로그 모니터링
tail -f "$MACHBASE_COLLECTOR_HOME/trc/machcollector.trc" | grep -i "queue\|error\|flush"
```

로그에서 확인할 주요 메시지:

| 메시지 키워드 | 의미 | 대응 방법 |
|--------------|------|-----------|
| `queue full` / `overflow` | 수신 속도 > 적재 속도 | 배치 크기 늘리기, 스레드 추가 |
| `flush delay` | flush 지연 | flush 주기 단축, I/O 환경 점검 |
| `connection timeout` | Machbase 연결 끊김 | 네트워크 점검, 재연결 설정 확인 |
| `slow append` | Append 속도 저하 | 인덱스 수 줄이기, SSD 사용 검토 |

```sql
-- Machbase에서 Append 세션 상태 확인
SELECT sess_id, state, record_size, query
  FROM v$stmt
 WHERE query LIKE '%APPEND%';
```

---

## 7단계: 장애 대응

### 재연결 설정

Machbase 서버 재시작 또는 네트워크 단절 시 Collector가 자동으로 재연결하도록 설정합니다.

```ini
# 재연결 대기 시간 (초)
COLLECTOR_RECONNECT_INTERVAL    = 5

# 재연결 최대 시도 횟수 (0이면 무한 재시도)
COLLECTOR_RECONNECT_MAX_RETRY   = 0

# 연결 실패 시 수신 데이터를 로컬에 임시 저장
COLLECTOR_OFFLINE_BUFFER_ENABLE = YES
COLLECTOR_OFFLINE_BUFFER_DIR    = /data/collector_buffer
COLLECTOR_OFFLINE_BUFFER_SIZE   = 1024   # MB
```

### 큐 오버플로우 대처

큐가 지속적으로 가득 차는 경우 단계별로 조치합니다.

1. **배치 크기 조정:** `COLLECTOR_BATCH_SIZE`를 한 단계씩 늘리고 메모리와 flush 지연을 확인합니다.
2. **병렬 스레드 추가:** `COLLECTOR_WORKER_THREADS`를 단계적으로 늘립니다.
3. **flush 주기 조정:** 가능하면 `COLLECTOR_FLUSH_INTERVAL`을 늘려 I/O 횟수를 줄입니다.
4. **소스 전송 속도 제한:** 데이터 소스 측에서 전송 속도를 제한합니다.
5. **수평 확장:** Collector 인스턴스를 여러 대 실행하여 소스를 분산합니다.

### 파일 수집 위치 추적 초기화

파일 오프셋 정보가 손상되거나 처음부터 재수집해야 할 때:

```bash
# Collector를 중지하고 position 파일 삭제 후 재시작
machcollectoradmin --stop-collector=localhost.file_sensor

rm -f "$MACHBASE_HOME/var/collector/file_collector.pos"

machcollectoradmin --start-collector=localhost.file_sensor
```

---

## Collector 시작/중지 명령

```bash
# Collector 시작
machcollectoradmin --start-collector=localhost.file_sensor

# Collector 상태 확인
machcollectoradmin --status-collector=localhost.file_sensor

# Collector 중지
machcollectoradmin --stop-collector=localhost.file_sensor

# 서버 부팅 시 자동 시작 등록 (systemd)
# /etc/systemd/system/machcollector-file.service 에 등록
```

---

## 참고

- Collector 수집 성능 튜닝: [../../performance-tuning/performance-tuning/ingestion-performance-tuning-collector](/dbms/performance-tuning/performance-tuning/#ingestion-performance-tuning-collector)
- 대량 적재 파이프라인: [/dbms/scenario-guides/bulk-pipeline/](/dbms/scenario-guides/bulk-pipeline/)
- Fluentd 로그 파이프라인: [../log-logs-pipeline-connection-fluentd](/dbms/log-table-usage/fluentd-pipeline/#log-logs-pipeline-connection-fluentd)
