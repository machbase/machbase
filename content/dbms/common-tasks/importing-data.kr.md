---
type: docs
title: '데이터 가져오기'
weight: 20
---

다양한 방법을 사용하여 Machbase로 데이터를 효율적으로 로드하는 방법을 학습합니다: CSV 가져오기, 대량 로딩 및 실시간 수집. 데이터 볼륨과 요구사항에 맞는 적절한 방법을 선택하세요.

## 가져오기 방법 개요

| 방법 | 최적 용도 | 속도 | 복잡도 |
|--------|----------|-------|------------|
| machloader (CSV) | 일회성 가져오기, 파일 | 빠름 | 쉬움 |
| APPEND API | 대용량 연속 데이터 | 가장 빠름 | 중간 |
| INSERT 문 | 소규모 데이터셋, 테스트 | 느림 | 쉬움 |
| REST API | 웹 애플리케이션 | 중간 | 쉬움 |

## machloader를 이용한 CSV 가져오기

### 기본 CSV 가져오기

```bash
# CSV 파일 가져오기
machloader -t tablename -d csv -i data.csv

# 옵션 사용
machloader -t sensors -d csv -i sensor_data.csv -F ','
```

### CSV 파일 형식

```csv
sensor01,2025-10-10 14:00:00,25.3,55.2
sensor01,2025-10-10 14:00:01,25.4,55.1
sensor02,2025-10-10 14:00:00,22.1,60.5
```

**중요**: CSV 컬럼은 테이블 스키마 순서와 일치해야 합니다.

### machloader 옵션

```bash
machloader \
  -s 127.0.0.1          # 서버 주소
  -u SYS                # 사용자명
  -p MANAGER            # 비밀번호
  -P 5656               # 포트
  -t tablename          # 테이블 이름
  -d csv                # 데이터 형식
  -i data.csv           # 입력 파일
  -F ','                # 필드 구분자 (기본값: 쉼표)
  -R '\n'               # 레코드 구분자 (기본값: 개행)
  -e error.log          # 오류 로그 파일
  -b 10000              # 배치 크기 (커밋당 행 수)
```

### 완전한 예제

```bash
# 샘플 CSV 생성
cat > sensors.csv <<EOF
sensor01,2025-10-10 14:00:00,25.3
sensor01,2025-10-10 14:00:01,25.4
sensor02,2025-10-10 14:00:00,22.1
EOF

# 테이블 생성
machsql -f - <<EOF
CREATE TABLE sensor_data (
    sensor_id VARCHAR(20),
    timestamp DATETIME,
    value DOUBLE
);
EOF

# CSV 가져오기
machloader -t sensor_data -d csv -i sensors.csv

# 확인
machsql -f - <<EOF
SELECT COUNT(*) FROM sensor_data;
EOF
```

### 대용량 파일 가져오기

```bash
# 대용량 파일의 경우 배치 크기 증가
machloader -t sensors -d csv -i large_data.csv -b 50000

# 진행 상황 모니터링
tail -f $MACHBASE_HOME/trc/machloader.log
```

## APPEND 프로토콜 (대량 삽입 API)

### APPEND를 사용하는 이유?

- **가장 빠른** 방법 (초당 수백만 행)
- **배치 커밋**으로 효율성 향상
- **논블로킹** 쓰기
- **최적 용도**: 대용량 연속 데이터

### C/CLI 예제

```c
#include "machbase_cli.h"

int main() {
    SQLHENV env;
    SQLHDBC conn;
    SQLHSTMT stmt;

    // 연결 (간결성을 위해 생략)...

    // 명령문 할당
    SQLAllocStmt(conn, &stmt);

    // APPEND 열기
    SQLAppendOpen(stmt, "sensor_data");

    // 행 추가
    for (int i = 0; i < 100000; i++) {
        char sensor_id[20];
        SQL_TIMESTAMP_STRUCT time_val;
        double value;

        sprintf(sensor_id, "sensor%02d", i % 10);
        // ... time_val 및 value 설정

        SQLAppendDataV(stmt, sensor_id, &time_val, value);
    }

    // 닫기 (배치 커밋)
    SQLAppendClose(stmt);

    // 정리...
    return 0;
}
```

### Java JDBC 예제

```java
import com.machbase.jdbc.*;

Connection conn = DriverManager.getConnection(url, user, password);

// Appender 생성
Appender appender = ((MachConnection)conn).createAppender("sensor_data");

// 행 추가
for (int i = 0; i < 100000; i++) {
    appender.append(
        "sensor" + (i % 10),
        new Timestamp(System.currentTimeMillis()),
        25.3 + Math.random()
    );
}

// 커밋
appender.close();
conn.close();
```

### Python 예제

```python
import machbase

conn = machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')

# appender 생성
appender = conn.create_appender('sensor_data')

# 행 추가
for i in range(100000):
    appender.append(
        f'sensor{i % 10:02d}',
        '2025-10-10 14:00:00',
        25.3 + i * 0.1
    )

# 커밋
appender.close()
conn.close()
```

## 일반 INSERT 문

### 단일 삽입

```sql
INSERT INTO sensor_data VALUES ('sensor01', NOW, 25.3);
```

### 배치 삽입

```sql
-- 대용량 데이터셋에는 권장하지 않음
INSERT INTO sensor_data VALUES ('sensor01', NOW, 25.3);
INSERT INTO sensor_data VALUES ('sensor02', NOW, 22.1);
INSERT INTO sensor_data VALUES ('sensor03', NOW, 23.5);
-- 1000행 이상의 경우 APPEND API 사용
```

### 매개변수화된 삽입

```python
cur = conn.cursor()

# 단일 매개변수화된 삽입
cur.execute("INSERT INTO sensor_data VALUES (?, ?, ?)",
            ('sensor01', '2025-10-10 14:00:00', 25.3))

# 배치 매개변수화된 삽입
data = [
    ('sensor01', '2025-10-10 14:00:01', 25.4),
    ('sensor02', '2025-10-10 14:00:01', 22.1),
    ('sensor03', '2025-10-10 14:00:01', 23.5)
]
cur.executemany("INSERT INTO sensor_data VALUES (?, ?, ?)", data)

conn.commit()
```

## Tag 테이블 가져오기

### Tag 테이블용 CSV

```csv
sensor01,2025-10-10 14:00:00,25.3,55.2
sensor01,2025-10-10 14:00:01,25.4,55.1
sensor02,2025-10-10 14:00:00,22.1,60.5
```

```bash
machloader -t warehouse_sensors -d csv -i tag_data.csv
```

### Tag 테이블용 APPEND

```c
SQLAppendOpen(stmt, "warehouse_sensors");

SQLAppendDataV(stmt,
    "sensor01",                    // 태그 이름
    &time_val,                     // BASETIME
    25.3,                          // temperature
    55.2);                         // humidity

SQLAppendClose(stmt);
```

## 오류 처리

### 가져오기 전 데이터 검증

```bash
# CSV 형식 확인
head -10 data.csv

# 행 수 세기
wc -l data.csv

# 잘못된 문자 확인
file data.csv
```

### 가져오기 오류 처리

```bash
# 오류 캡처
machloader -t sensors -d csv -i data.csv -e errors.log 2>&1 | tee import.log

# 오류 로그 확인
cat errors.log

# 실패한 행 재시도
# (오류 로그에서 실패한 행을 추출하여 재가져오기)
```

### 일반적인 문제

**문제 1: 컬럼 수 불일치**
```
Error: Column count mismatch
```
**해결책**: CSV 컬럼이 테이블 스키마와 일치하는지 확인

**문제 2: 데이터 타입 불일치**
```
Error: Invalid data type
```
**해결책**: CSV의 데이터 타입 검증

**문제 3: 중복 기본 키** (Volatile/Lookup 테이블)
```
Error: Duplicate key
```
**해결책**: 중복 제거 또는 UPDATE 사용

## 성능 최적화

### 1. 대용량 데이터셋에 APPEND 사용

```
< 1,000행      → INSERT 문
1,000-100,000  → machloader (CSV)
> 100,000      → APPEND API
연속 스트림     → APPEND API
```

### 2. 배치 크기 조정

```bash
# 작은 배치 (더 안전함)
machloader -t sensors -d csv -i data.csv -b 1000

# 큰 배치 (더 빠름)
machloader -t sensors -d csv -i data.csv -b 100000
```

### 3. 병렬 로딩

```bash
# 대용량 파일 분할
split -l 1000000 large_data.csv chunk_

# 병렬로 로드
machloader -t sensors -d csv -i chunk_aa &
machloader -t sensors -d csv -i chunk_ab &
machloader -t sensors -d csv -i chunk_ac &
wait
```

### 4. 대량 로드 중 인덱싱 비활성화

```sql
-- 인덱스가 있는 Log/Lookup 테이블의 경우
-- 가져오기 전 인덱스 삭제
DROP INDEX idx_sensor_id;

-- 데이터 가져오기
-- (machloader 또는 APPEND 사용)

-- 가져오기 후 인덱스 재생성
CREATE INDEX idx_sensor_id ON sensors(sensor_id);
```

## 데이터 검증

### 가져오기 전 확인

```sql
-- 테이블 스키마 확인
SHOW TABLE sensor_data;

-- 테이블 존재 확인
SHOW TABLES;

-- 컬럼 타입이 CSV 데이터와 일치하는지 확인
```

### 가져오기 후 검증

```sql
-- 가져온 행 수 세기
SELECT COUNT(*) FROM sensor_data;

-- NULL 값 확인
SELECT COUNT(*) FROM sensor_data WHERE value IS NULL;

-- 시간 범위 확인
SELECT MIN(_arrival_time), MAX(_arrival_time) FROM sensor_data;

-- 데이터 분포 확인
SELECT sensor_id, COUNT(*) FROM sensor_data GROUP BY sensor_id;
```

## 실제 예제

### 예제 1: 일일 로그 가져오기

```bash
#!/bin/bash
# daily_import.sh

DATE=$(date +%Y%m%d)
LOG_FILE="/logs/app_${DATE}.log"
TABLE="app_logs"

# 로그를 CSV로 변환
awk '{print $1","$2","$3}' $LOG_FILE > /tmp/import.csv

# 가져오기
machloader -t $TABLE -d csv -i /tmp/import.csv -e /tmp/errors_${DATE}.log

# 결과 확인
echo "Imported $(machsql -i -f - <<< "SELECT COUNT(*) FROM $TABLE WHERE _arrival_time >= SYSDATE - 1;" | tail -1) rows"

# 정리
rm /tmp/import.csv
```

### 예제 2: 실시간 센서 스트림

```python
import machbase
import time

conn = machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')

while True:
    # 배치용 appender 생성
    appender = conn.create_appender('sensors')

    # 1000개 읽기 수집
    for i in range(1000):
        sensor_id = f'sensor{i % 100:03d}'
        value = read_sensor(sensor_id)  # 센서 읽기 함수
        appender.append(sensor_id, time.time(), value)

    # 배치 커밋
    appender.close()

    # 다음 배치 전 대기
    time.sleep(10)
```

### 예제 3: CSV 파일 모니터링

```bash
#!/bin/bash
# monitor_csv.sh - 새 CSV 파일 가져오기

WATCH_DIR="/data/csv"
ARCHIVE_DIR="/data/archive"
TABLE="sensor_data"

inotifywait -m -e create "$WATCH_DIR" --format '%f' | while read FILE; do
    if [[ $FILE == *.csv ]]; then
        echo "Importing $FILE..."
        machloader -t $TABLE -d csv -i "$WATCH_DIR/$FILE"

        if [ $? -eq 0 ]; then
            mv "$WATCH_DIR/$FILE" "$ARCHIVE_DIR/"
            echo "Success: $FILE"
        else
            echo "Error: $FILE" | mail -s "Import Error" admin@company.com
        fi
    fi
done
```

## 모범 사례

1. **대용량 연속 데이터에 APPEND API 사용**
2. **일회성 CSV 가져오기에 machloader 사용**
3. **더 나은 성능을 위해 배치 작업 수행**
4. **가져오기 전 데이터 검증**
5. **오류 모니터링 및 실패한 행 재시도**
6. **가능한 경우 대용량 가져오기 병렬화**
7. **먼저 소규모 데이터셋으로 테스트**

## 문제 해결

**느린 가져오기 속도**:
- 배치 크기 증가
- INSERT 대신 APPEND 사용
- 네트워크 지연 확인
- 서버 리소스 확인 (CPU, 디스크 I/O)

**메모리 부족**:
- 배치 크기 감소
- 대용량 파일 분할
- 서버 메모리 설정 확인

**연결 타임아웃**:
- 연결 타임아웃 증가
- 네트워크 안정성 확인
- 서버 로드 확인

## 다음 단계

- **데이터 조회**: [데이터 조회하기](../querying/) - 가져온 데이터 조회
- **사용자 관리**: [사용자 관리](../user-management/) - 가져오기 사용자 권한
- **튜토리얼**: [IoT 센서 데이터](../../tutorials/iot-sensor-data/) - 완전한 가져오기 예제

---

데이터 가져오기를 마스터하고 시계열 데이터를 Machbase로 효율적으로 로드하세요!
