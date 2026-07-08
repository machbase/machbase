---
type: docs
title: '대량 데이터 적재 파이프라인'
weight: 60
---

## 시나리오 개요

CSV 파일, 외부 데이터베이스, 또는 메모리 내 데이터 구조에서 대용량 데이터를 Machbase에 고속으로 적재하는 파이프라인을 설계합니다. 적재 방식별 특성을 비교하고, 상황에 맞는 최적의 전략을 선택하는 방법을 설명합니다.

---

## 1단계: 파이프라인 설계 원칙

### 적재 방식 선택 기준

| 방식 | 적합한 상황 | 처리량 | 비고 |
|------|------------|--------|------|
| **machloader** | CSV/텍스트 파일 일괄 적재 | 매우 높음 | 운영 자동화에 적합 |
| **Append API (JDBC)** | Java 애플리케이션 내 실시간 적재 | 높음 | 배치 크기 조절 가능 |
| **Append API (Python)** | 스크립트 기반 ETL, 분석 파이프라인 | 높음 | 간단한 구현 |
| **INSERT** | 소량 데이터, 트랜잭션 필요 시 | 낮음 | 대량 적재에는 부적합 |
| **REST API** | 외부 시스템에서 HTTP로 적재 | 중간 | 건수가 적을 때 |

> **원칙:** 대량 적재에는 반드시 Append API 또는 machloader를 사용하세요. INSERT는 Machbase의 컬럼 스토리지 구조에 최적화되어 있지 않아 대량 처리 시 성능이 크게 저하됩니다.

### 적재 대상 테이블 생성

```sql
-- LOG 테이블: 시계열 이벤트 로그 적재 예시
CREATE TABLE sensor_log (
    _arrival_time DATETIME,
    device_id     VARCHAR(64),
    sensor_type   VARCHAR(32),
    value         DOUBLE,
    quality       INTEGER
);

-- TAG 테이블: 센서 시계열 데이터 적재 예시
CREATE TAG TABLE sensor_tag (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

---

## 2단계: machloader를 이용한 CSV 대량 적재

machloader는 CSV 파일을 Machbase에 직접 적재하는 공식 CLI 도구입니다. 내부적으로 Append API를 사용하므로 INSERT보다 훨씬 빠릅니다.

### 기본 사용법

```bash
# CSV 파일을 sensor_log 테이블에 적재
machloader -i -t sensor_log -d /data/sensor_20240101.csv

# 헤더 행이 포함된 CSV (첫 번째 행을 컬럼명으로 처리)
machloader -i -t sensor_log -d /data/sensor_20240101.csv -H

# 인코딩 지정 (UTF-8 파일)
machloader -i -t sensor_log -d /data/sensor_20240101.csv -E UTF-8

# 파이프(|) 구분자 사용
machloader -i -t sensor_log -d /data/sensor_20240101.csv -E UTF-8 -D '|'
```

### CSV 파일 형식 예시

```csv
# 헤더 없는 CSV (컬럼 순서가 테이블 정의와 일치해야 함)
2024-01-01 00:00:01,DEVICE_A,TEMP,72.3,100
2024-01-01 00:00:01,DEVICE_A,PRESS,1.04,100
2024-01-01 00:00:02,DEVICE_B,TEMP,68.5,100
```

```csv
# 헤더 포함 CSV (-H 옵션 사용 시)
_arrival_time,device_id,sensor_type,value,quality
2024-01-01 00:00:01,DEVICE_A,TEMP,72.3,100
2024-01-01 00:00:01,DEVICE_A,PRESS,1.04,100
```

### 주요 옵션 정리

| 옵션 | 설명 | 예시 |
|------|------|------|
| `-i` | 입력(import) 모드 | 필수 |
| `-t` | 대상 테이블 이름 | `-t sensor_log` |
| `-d` | 입력 파일 경로 | `-d /data/file.csv` |
| `-H` | 첫 번째 행을 헤더로 처리 | |
| `-E` | 파일 인코딩 | `-E UTF-8` |
| `-D` | 필드 구분자 (기본: 쉼표) | `-D '|'` |
| `-n` | 오류 발생 시 건너뛸 행 수 | `-n 10` |
| `-e` | 오류 행을 저장할 파일 | `-e /tmp/err.csv` |
| `-b` | 배치 크기 (기본: 10000) | `-b 50000` |

### 배치 적재 자동화 스크립트

```bash
#!/bin/bash
# daily_load.sh - 전날 데이터 파일을 일괄 적재

DATA_DIR="/data/sensors"
LOG_DIR="/var/log/machloader"
TABLE="sensor_log"
DATE=$(date -d "yesterday" +%Y%m%d)

mkdir -p "$LOG_DIR"

for FILE in "$DATA_DIR"/sensor_${DATE}_*.csv; do
    BASENAME=$(basename "$FILE" .csv)
    machloader -i -t "$TABLE" -d "$FILE" -H -E UTF-8 \
               -e "$LOG_DIR/${BASENAME}_err.csv" \
               >> "$LOG_DIR/${BASENAME}.log" 2>&1

    if [ $? -eq 0 ]; then
        echo "[$(date)] SUCCESS: $FILE"
        mv "$FILE" "$DATA_DIR/done/"
    else
        echo "[$(date)] FAILED:  $FILE (확인: $LOG_DIR/${BASENAME}.log)"
    fi
done
```

---

## 3단계: Append API를 이용한 프로그래밍 방식 (Python)

Python에서 `machbaseAPI` 패키지를 사용하면 애플리케이션 내에서 직접 고속 적재를 구현할 수 있습니다.

### 기본 Append 예시

```python
import json
import re
from machbaseAPI.machbaseAPI import machbase

HOST     = "localhost"
USER     = "SYS"
PASSWORD = "MANAGER"
PORT     = 5656

def get_column_types(db, table_name):
    """테이블의 컬럼 타입 목록을 반환합니다."""
    db.columns(table_name)
    columns_str = db.result()
    types = [
        json.loads(item).get("type")
        for item in re.findall(r"\{[^}]+\}", columns_str)
    ]
    return types

def load_csv_data(file_path, table_name="sensor_log"):
    db = machbase()
    db.open(HOST, USER, PASSWORD, PORT)

    types = get_column_types(db, table_name)

    batch_size = 5000
    values = []

    with open(file_path, "r", encoding="utf-8") as f:
        next(f)  # 헤더 건너뜀
        for line in f:
            cols = line.strip().split(",")
            values.append(cols)

            if len(values) >= batch_size:
                db.append(table_name, types, values, "YYYY-MM-DD HH24:MI:SS")
                values.clear()

    # 나머지 데이터 flush
    if values:
        db.append(table_name, types, values, "YYYY-MM-DD HH24:MI:SS")

    db.close()
    print(f"적재 완료: {file_path}")

load_csv_data("/data/sensor_20240101.csv")
```

---

## 4단계: 병렬 Append로 처리량 극대화

멀티스레드로 여러 연결에서 동시에 Append를 수행하면 처리량이 거의 선형으로 증가합니다.

```python
import json
import re
import threading
from machbaseAPI.machbaseAPI import machbase

HOST     = "localhost"
USER     = "SYS"
PASSWORD = "MANAGER"
PORT     = 5656
TABLE    = "sensor_log"
THREADS  = 4        # 권장: Warehouse 노드 수 × 1~2
BATCH    = 10000

def get_column_types():
    db = machbase()
    db.open(HOST, USER, PASSWORD, PORT)
    db.columns(TABLE)
    columns_str = db.result()
    types = [
        json.loads(item).get("type")
        for item in re.findall(r"\{[^}]+\}", columns_str)
    ]
    db.close()
    return types

def append_worker(thread_id, data_chunk, types):
    db = machbase()
    db.open(HOST, USER, PASSWORD, PORT)

    batch = []
    for row in data_chunk:
        batch.append(row)
        if len(batch) >= BATCH:
            db.append(TABLE, types, batch, "YYYY-MM-DD HH24:MI:SS")
            batch.clear()

    if batch:
        db.append(TABLE, types, batch, "YYYY-MM-DD HH24:MI:SS")

    db.close()
    print(f"[Thread-{thread_id}] 완료: {len(data_chunk)}건")

def parallel_append(all_data):
    types = get_column_types()

    # 데이터를 스레드 수로 균등 분할
    chunks = [all_data[i::THREADS] for i in range(THREADS)]

    threads = []
    for i, chunk in enumerate(chunks):
        t = threading.Thread(target=append_worker, args=(i, chunk, types))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"병렬 적재 완료: 총 {len(all_data)}건")

# 사용 예시
all_rows = [...]  # 적재할 데이터 목록
parallel_append(all_rows)
```

> **Cluster Edition 고려사항:** Cluster Edition에서는 Broker 노드와 Warehouse 노드가 분리됩니다. 병렬 Append 시 각 스레드가 서로 다른 Warehouse 노드에 직접 연결하도록 구성하면 추가 성능 향상을 기대할 수 있습니다. 자세한 내용은 [../../cluster](../../cluster) 시나리오를 참고하세요.

---

## 5단계: 적재 진행 상황 모니터링

적재가 진행되는 동안 Machbase 시스템 뷰로 실시간 상태를 확인합니다.

```sql
-- 현재 실행 중인 Append 세션 확인
SELECT sess_id,
       id        AS stmt_id,
       state,
       record_size,
       query
  FROM v$stmt
 WHERE query LIKE '%APPEND%'
 ORDER BY sess_id, id;
```

```sql
-- 세션별 네트워크·쿼리 통계
SELECT id        AS sess_id,
       user_name,
       login_time,
       query_count,
       execute_count
  FROM v$session
 ORDER BY login_time DESC;
```

```sql
-- 테이블 행 수로 적재 진행 확인
SELECT COUNT(*) AS total_rows FROM sensor_log;

-- 가장 최근에 적재된 행의 시간 확인
SELECT MAX(_arrival_time) AS latest_arrival FROM sensor_log;
```

---

## 6단계: 오류 처리 전략

### machloader 오류 행 처리

machloader는 `-e` 옵션으로 오류 행을 별도 파일에 저장합니다.

```bash
machloader -i -t sensor_log -d /data/sensor.csv -H \
           -e /tmp/sensor_err.csv \
           -n 100   # 최대 100건까지 오류 허용 후 계속 진행
```

오류 파일을 검토한 뒤 데이터를 보정하여 재적재합니다.

```bash
# 오류 파일 확인
cat /tmp/sensor_err.csv

# 보정 후 재적재
machloader -i -t sensor_log -d /tmp/sensor_err_fixed.csv -H
```

### Python Append API 오류 처리

```python
def safe_append(db, table_name, types, values, fallback=True):
    """Append 실패 시 INSERT로 fallback하는 함수."""
    try:
        db.append(table_name, types, values, "YYYY-MM-DD HH24:MI:SS")
    except Exception as e:
        print(f"[WARN] Append 실패: {e}")
        if fallback:
            # 건별 INSERT로 재시도 (느리지만 안전)
            for row in values:
                try:
                    cols   = ", ".join(str(v) for v in row)
                    sql    = f"INSERT INTO {table_name} VALUES ({cols})"
                    db.execute(sql)
                except Exception as ex:
                    print(f"[ERROR] INSERT 실패: {ex} | row={row}")
```

### 부분 실패 대응 체크포인트 방식

대용량 파일을 청크 단위로 나누어 적재하고, 적재 완료한 오프셋을 파일에 기록하면 중단 후 이어서 적재할 수 있습니다.

```python
import os

CHECKPOINT_FILE = "/tmp/load_checkpoint.txt"

def load_with_checkpoint(file_path, table_name, types, batch_size=5000):
    # 이전 체크포인트 읽기
    start_line = 0
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            start_line = int(f.read().strip())
        print(f"체크포인트에서 재개: {start_line}행부터")

    db = machbase()
    db.open(HOST, USER, PASSWORD, PORT)

    values = []
    current_line = 0

    with open(file_path, "r") as f:
        next(f)  # 헤더 건너뜀
        for line in f:
            current_line += 1
            if current_line <= start_line:
                continue

            values.append(line.strip().split(","))

            if len(values) >= batch_size:
                db.append(table_name, types, values, "YYYY-MM-DD HH24:MI:SS")
                values.clear()
                # 체크포인트 저장
                with open(CHECKPOINT_FILE, "w") as cf:
                    cf.write(str(current_line))

    if values:
        db.append(table_name, types, values, "YYYY-MM-DD HH24:MI:SS")

    db.close()
    # 완료 후 체크포인트 삭제
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
    print(f"적재 완료: 총 {current_line - start_line}건")
```

---

## 7단계: 적재 후 검증 쿼리

적재 완료 후 데이터 무결성을 검증합니다.

```sql
-- 적재된 총 건수 확인
SELECT COUNT(*) AS total_rows
  FROM sensor_log;

-- 날짜별 적재 건수 분포 확인
SELECT TO_CHAR(_arrival_time, 'YYYY-MM-DD') AS load_date,
       COUNT(*)                              AS row_count
  FROM sensor_log
 GROUP BY TO_CHAR(_arrival_time, 'YYYY-MM-DD')
 ORDER BY load_date DESC
 LIMIT 10;

-- 최신 적재 시각 확인
SELECT MAX(_arrival_time) AS latest_time,
       MIN(_arrival_time) AS oldest_time
  FROM sensor_log;

-- 장치별 데이터 건수 확인
SELECT device_id,
       COUNT(*)      AS row_count,
       MIN(value)    AS min_val,
       MAX(value)    AS max_val,
       AVG(value)    AS avg_val
  FROM sensor_log
 GROUP BY device_id
 ORDER BY device_id
 LIMIT 20;

-- TAG 테이블의 경우 통계 뷰로 빠르게 확인
SELECT name,
       row_count,
       min_time,
       max_time,
       recent_row_time
  FROM v$sensor_tag_stat
 ORDER BY name;
```

---

## Cluster Edition 고려사항

| 항목 | Standard Edition | Cluster Edition |
|------|-----------------|-----------------|
| 적재 대상 | Machbase 단일 노드 | Broker 또는 Warehouse 직접 연결 |
| 병렬 스레드 | CPU 코어 수 기준 | Warehouse 노드 수 × 1~2 |
| machloader | 단일 프로세스 | Warehouse별 분산 실행 가능 |
| 오류 처리 | 단순 재시도 | 노드 장애 시 다른 노드로 재연결 |

Cluster Edition에서 machloader를 사용할 때는 Broker 포트로 연결합니다.

```bash
# Cluster Edition: Broker 포트(5656)로 연결
machloader -i -t sensor_log -d /data/sensor.csv -H \
           -s localhost -u SYS -p MANAGER -P 5656
```

---

## 참고

- `_ARRIVAL_TIME` 역순 입력 주의사항: [../../performance-tuning/performance-tuning/performance-tuning-bulk](../../performance-tuning/performance-tuning/performance-tuning-bulk)
- 대량 입력 성능 튜닝: [../../performance-tuning/performance-tuning/performance-tuning-bulk](../../performance-tuning/performance-tuning/performance-tuning-bulk)
- Collector를 이용한 파일 수집: [../file-ingestion-collector](../file-ingestion-collector)
