---
type: docs
title: '대량 입력 성능 튜닝'
weight: 10
---

대량 데이터를 빠르게 적재하려면 Append API와 올바른 배치 전략을 사용해야 합니다.

## 권장 배치 크기

| 데이터 특성 | 권장 배치 크기 | 이유 |
|------------|:---:|------|
| 소규모 센서 (< 100 태그) | 1,000건 | RTT 최소화 |
| 일반 IoT 데이터 | 5,000~10,000건 | 처리량과 레이턴시 균형 |
| 대규모 로그 수집 | 10,000건 이상 | 네트워크 효율 최대화 |

배치가 너무 작으면 네트워크 RTT가 지배적이 되고, 너무 크면 flush 지연이 발생합니다.

## Append API 사용 예시

```java
// JDBC - Append API로 대량 삽입
MachConnection conn = (MachConnection) DriverManager.getConnection(url, props);
MachAppendWriter appender = conn.getAppendWriter("sensor_log",
    MachAppendWriter.RETURN_SUCC);

int batchSize = 10000;
for (int i = 0; i < totalRows; i++) {
    Object[] row = new Object[]{
        "sensor-" + (i % 100),                    // name
        System.currentTimeMillis() * 1_000_000L,   // time (ns)
        Math.random() * 100                         // value
    };
    appender.append(row);

    if ((i + 1) % batchSize == 0) {
        appender.flush();  // 명시적 flush
    }
}
appender.close();
```

```python
# Python - Append API
conn = machbaseapi.connect(host, port, user, password)
cursor = conn.cursor()

batch = []
batch_size = 5000
for i, row in enumerate(data_source):
    batch.append(row)
    if len(batch) >= batch_size:
        cursor.append("sensor_log", batch)
        batch.clear()

if batch:
    cursor.append("sensor_log", batch)  # 나머지 처리
```

## 병렬 Append

멀티스레드로 여러 커넥션에서 동시에 Append하면 처리량이 선형에 가깝게 증가합니다.

```python
import threading

def append_worker(thread_id, data_chunk):
    conn = machbaseapi.connect(host, port, user, password)
    cursor = conn.cursor()
    cursor.append("sensor_log", data_chunk)
    conn.close()

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

> Cluster Edition에서는 병렬 Append 시 각 스레드가 다른 Active 노드에 연결하면 추가 성능 향상이 가능합니다.

## 네트워크 병목 최소화

원격 연결 시 네트워크 RTT가 Append 성능에 직접 영향을 줍니다.

| 연결 유형 | RTT | 권장 배치 크기 |
|----------|-----|:---:|
| 로컬 (같은 호스트) | < 0.1ms | 1,000건 |
| LAN (같은 네트워크) | 1ms 미만 | 5,000건 |
| WAN/인터넷 | 10ms 이상 | 로컬 버퍼링 에이전트 사용 |

## machloader를 이용한 CSV 대량 적재

파일 기반 대량 적재는 machloader를 사용합니다.

```bash
# CSV 파일을 sensor_log 테이블에 적재
machloader -i -t sensor_log -f /data/sensor_log_20240101.csv -d ,

# 헤더 행이 있는 CSV
machloader -i -t sensor_log -f /data/sensor_with_header.csv -d , -H

# 인코딩 지정
machloader -i -t sensor_log -f /data/utf8_data.csv -d , -e utf8
```

machloader는 내부적으로 Append API를 사용하므로 INSERT보다 훨씬 빠릅니다.

## `_ARRIVAL_TIME` 역순 입력 주의

LOG 테이블에 INSERT 또는 Append 시 데이터는 반드시 **시간 순서대로** 입력해야 합니다.

```sql
-- 잘못된 패턴: 역순 삽입
INSERT INTO device_log (ts, value) VALUES ('2024-01-02 00:00:00', 10);
INSERT INTO device_log (ts, value) VALUES ('2024-01-01 00:00:00', 20); -- 역순! 오류 또는 성능 저하

-- 올바른 패턴: 시간 순서대로 삽입
INSERT INTO device_log (ts, value) VALUES ('2024-01-01 00:00:00', 10);
INSERT INTO device_log (ts, value) VALUES ('2024-01-02 00:00:00', 20); -- 정순
```

과거 데이터를 소급 입력해야 하는 경우에는 machloader를 이용한 전용 적재 프로세스를 분리 운영하는 것을 권장합니다.

## flush 주기 설정

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
