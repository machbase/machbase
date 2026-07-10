---
type: docs
title: '12.4 입력 성능 튜닝'
weight: 40
toc: true
---
입력 방식은 네트워크 왕복, SQL 파싱, 버퍼링과 인덱스 유지 비용에 영향을 줍니다. 워크로드에
맞는 입력 경로를 선택하고 변경 전후 처리량과 지연을 측정합니다.

## Append API vs INSERT 비교

| 방식 | 전송 특성 | 적합한 상황 |
|------|-----------|-----------|
| **Append API** | 여러 행을 버퍼링하여 전송 | 지속적인 TAG/LOG 수집, RDB client batch 입력 |
| **INSERT (단건)** | SQL 문장마다 파싱하고 응답 | 소량 입력, 즉시 결과 확인 |
| **RDB 트랜잭션 INSERT** | 여러 RDB DML을 한 작업 단위로 처리 | 원자성이 필요한 관계형 업무 처리 |

> TAG와 LOG 테이블의 지속적인 대량 수집에는 Append API를 우선 검토합니다.

## 핵심 입력 성능 원칙

1. **입력 경로 선택**: TAG/LOG 수집에는 Append API, 관계형 작업에는 RDB DML 사용
2. **배치 크기 조정**: 너무 작으면 RTT 오버헤드, 너무 크면 flush 지연
3. **병렬 입력**: 여러 스레드에서 동시에 Append 실행
4. **인덱스 최소화**: 쓰기 경로에서 실제로 사용하는 인덱스만 유지
5. **네트워크 거리 최소화**: 가능하면 Machbase와 같은 호스트 또는 동일 네트워크

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [대량 입력 성능 튜닝](/dbms/performance-tuning/performance-tuning/#performance-tuning-bulk) | 배치 크기, 병렬 Append, machloader, _ARRIVAL_TIME 주의사항 |
| [Collector 수집 성능 튜닝](/dbms/performance-tuning/performance-tuning/#ingestion-performance-tuning-collector) | Collector 컴포넌트 튜닝, 수집 파이프라인 최적화 |


<a id="performance-tuning-bulk"></a>

## 대량 입력 성능 튜닝

대량 데이터를 빠르게 적재하려면 Append API와 올바른 배치 전략을 사용해야 합니다.

### 권장 배치 크기

| 데이터 특성 | 권장 배치 크기 | 이유 |
|------------|:---:|------|
| 소규모 센서 (< 100 태그) | 1,000건 | RTT 최소화 |
| 일반 IoT 데이터 | 5,000~10,000건 | 처리량과 레이턴시 균형 |
| 대규모 로그 수집 | 10,000건 이상 | 네트워크 효율 최대화 |

배치가 너무 작으면 네트워크 RTT가 지배적이 되고, 너무 크면 flush 지연이 발생합니다.

### Append API 사용 예시

```java
// JDBC - Append API로 대량 삽입
Connection conn = DriverManager.getConnection(url, props);
MachStatement stmt = (MachStatement) conn.createStatement();
ResultSet rs = stmt.executeAppendOpen("sensor_log", 100);
ResultSetMetaData rsmd = rs.getMetaData();

int batchSize = 10000;
for (int i = 0; i < totalRows; i++) {
    ArrayList<Object> row = new ArrayList<>();
    row.add("sensor-" + (i % 100));                 // name
    row.add(System.currentTimeMillis() * 1_000_000L); // time (ns)
    row.add(Math.random() * 100);                   // value
    stmt.executeAppendData(rsmd, row);

    if ((i + 1) % batchSize == 0) {
        stmt.executeAppendFlush();
    }
}
stmt.executeAppendClose();
```

```python
# Python - Append API
import json
import re
from machbaseAPI.machbaseAPI import machbase

db = machbase()
db.open(host, user, password, port)

table_name = "sensor_log"
db.columns(table_name)
columns = db.result()
types = [json.loads(item).get("type") for item in re.findall(r"{[^}]+}", columns)]

values = []
batch_size = 5000
for i, row in enumerate(data_source):
    values.append(row)
    if len(values) >= batch_size:
        db.append(table_name, types, values, "YYYY-MM-DD HH24:MI:SS")
        values.clear()

if values:
    db.append(table_name, types, values, "YYYY-MM-DD HH24:MI:SS")

db.close()
```

### 병렬 Append

멀티스레드로 여러 커넥션에서 동시에 Append하면 처리량이 선형에 가깝게 증가합니다.

```python
import threading

def append_worker(thread_id, data_chunk):
    db = machbase()
    db.open(host, user, password, port)
    db.append("sensor_log", types, data_chunk, "YYYY-MM-DD HH24:MI:SS")
    db.close()

# 4개 스레드로 병렬 Append
threads = []
for i in range(4):
    chunk = data[i::4]  # 데이터를 4등분
    t = threading.Thread(target=append_worker, args=(i, chunk))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

> Cluster Edition에서는 병렬 Append 시 Broker와 Warehouse 구성을 고려해 입력 경로를 분산하면 추가 성능 향상을 기대할 수 있습니다.

### 네트워크 병목 최소화

원격 연결 시 네트워크 RTT가 Append 성능에 직접 영향을 줍니다.

| 연결 유형 | RTT | 권장 배치 크기 |
|----------|-----|:---:|
| 로컬 (같은 호스트) | < 0.1ms | 1,000건 |
| LAN (같은 네트워크) | 1ms 미만 | 5,000건 |
| WAN/인터넷 | 10ms 이상 | 로컬 버퍼링 에이전트 사용 |

### machloader를 이용한 CSV 대량 적재

파일 기반 대량 적재는 machloader를 사용합니다.

```bash
# CSV 파일을 sensor_log 테이블에 적재
machloader -i -t sensor_log -d /data/sensor_log_20240101.csv

# 헤더 행이 있는 CSV
machloader -i -t sensor_log -d /data/sensor_with_header.csv -H

# 인코딩 지정
machloader -i -t sensor_log -d /data/utf8_data.csv -E UTF-8

# 구분자 지정
machloader -i -t sensor_log -d /data/sensor_pipe.txt -D '|'
```

machloader는 내부적으로 Append API를 사용하므로 INSERT보다 훨씬 빠릅니다.

### `_ARRIVAL_TIME` 역순 입력 주의

LOG 테이블에 `_ARRIVAL_TIME`을 명시해 과거 데이터를 입력할 때는 시간 역전이 과도하게 발생하지 않도록 입력 순서를 관리합니다.

```sql
-- 잘못된 패턴: 역순 삽입
INSERT INTO device_log (_arrival_time, value)
VALUES (TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10);
INSERT INTO device_log (_arrival_time, value)
VALUES (TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 20); -- 역순

-- 올바른 패턴: 시간 순서대로 삽입
INSERT INTO device_log (_arrival_time, value)
VALUES (TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10);
INSERT INTO device_log (_arrival_time, value)
VALUES (TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 20); -- 정순
```

과거 데이터를 소급 입력해야 하는 경우에는 machloader를 이용한 전용 적재 프로세스를 분리 운영하는 것을 권장합니다.

### flush 주기 설정

Append 데이터를 디스크에 flush하는 주기입니다.

```ini
# machbase.conf
DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC = 3  # 기본값 3초
```

| 설정값 | 특성 |
|--------|------|
| 1초 | 내구성 높음, I/O 부하 증가 |
| 3초 (기본) | 처리량과 내구성 균형 |
| 10초 이상 | 처리량 최대, 장애 시 최대 N초 데이터 손실 가능 |

<a id="ingestion-performance-tuning-collector"></a>

## Collector 수집 성능 튜닝

Collector는 외부 데이터 소스에서 데이터를 수집하여 Machbase에 적재하는 컴포넌트입니다. 데이터 유실 없이 최대 처리량을 달성하는 것이 목표입니다.

### 수집 성능 영향 요소

| 요소 | 영향 | 튜닝 방향 |
|------|------|-----------|
| 수집 주기 | 짧을수록 실시간성 높음, 오버헤드 증가 | 데이터 특성에 맞게 설정 |
| 배치 크기 | 클수록 왕복 감소, 메모리와 flush 지연 증가 | 작은 값부터 처리량과 지연 측정 |
| 네트워크 레이턴시 | 높을수록 지연 증가 | 로컬 또는 LAN 환경 권장 |
| 병렬 스레드 수 | 증가 시 처리량 향상 가능, CPU·연결 경쟁 발생 | CPU, 연결과 큐 지연으로 단계 조정 |
| Append 버퍼 크기 | 클수록 flush 횟수 감소 | 메모리와 내구성 균형 |

### 권장 수집 파이프라인 설계

**단일 소스 파이프라인**

```
[Sensor/Device] → [Collector Thread] → [Machbase Broker/Warehouse]
```

**다중 소스 병렬 파이프라인 (권장)**

```
[Source 1] → [Collector Thread 1] ─┐
[Source 2] → [Collector Thread 2] ─┼→ [Machbase Warehouse 노드들]
[Source 3] → [Collector Thread 3] ─┘
```

### 배치 크기와 flush 주기

| 데이터 특성 | 배치 크기 | flush 주기 | 설명 |
|------------|:---:|:---:|------|
| 고빈도 센서 (100Hz 이상) | 10,000건 | 1초 | 처리량 우선 |
| 일반 IoT (1Hz) | 1,000건 | 1~5초 | 균형 |
| 이벤트 로그 (불규칙) | 500건 | 5~10초 | 지연 허용 |
| 실시간 알람 | 1~10건 | 즉시 flush | 레이턴시 우선 |

### 병렬 스레드 수 설정

Cluster Edition에서는 Warehouse 노드 수에 맞게 병렬 스레드를 설정합니다.

```
권장 스레드 수 = Warehouse 노드 수 × 1~2
예: Warehouse 4노드 → 4~8개 Collector 스레드
```

Standard Edition에서는 CPU 코어 수를 기준으로 합니다.

```
권장 스레드 수 = CPU 코어 수의 1/2 ~ 2/3
예: 8코어 → 4~5개 스레드
```

### 병목 원인 진단

수집 속도가 느릴 때 Append 병목인지 네트워크 병목인지 구분합니다.

```sql
-- 현재 실행 중인 Append 관련 문장 확인
SELECT sess_id, id AS stmt_id, state, record_size, query
  FROM v$stmt
 WHERE query LIKE '%APPEND%'
 ORDER BY sess_id, id;
```

**Append 병목 징후:**
- CPU 사용률이 낮고 I/O wait가 높음 (`iostat -x 1`)
- → 인덱스 줄이기, SSD 사용, flush 주기 늘리기

**네트워크 병목 징후:**
- `ping` 또는 `iperf` 측정값이 예상보다 높음
- Collector 로그에 connection timeout 반복
- → Collector와 Machbase를 같은 서버/네트워크에 배치

### Collector 큐 모니터링

Collector가 처리하지 못한 데이터가 큐에 쌓이는지 모니터링합니다.

```bash
# Collector 로그에서 지연 또는 큐 관련 메시지 확인
grep -i "queue\|delay\|overflow\|slow" "$MACHBASE_HOME/trc/<collector-name>.trc" | tail -50
```

큐가 지속적으로 증가한다면:
1. 배치 크기 늘리기
2. 병렬 스레드 추가
3. flush 주기 조정
4. 데이터 소스 측 전송 속도 제한 검토
