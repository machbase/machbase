---
type: docs
title: '인덱싱 및 성능'
weight: 30
---

Machbase 인덱스가 작동하는 방식과 쿼리 성능을 최적화하는 방법을 배웁니다. 이 가이드는 인덱싱 전략, 자동 인덱스 관리 및 성능 튜닝을 다룹니다.

## 인덱싱 개요

Machbase는 각 테이블 타입에 대해 다른 인덱싱 전략을 사용하며, 모두 시계열 워크로드를 위해 설계되었습니다:

| 테이블 타입 | 인덱스 타입 | 관리 | 목적 |
|-----------|-----------|------------|---------|
| Tag | 3단계 파티션 | 자동 | 빠른 sensor_id + time 쿼리 |
| Log | LSM (선택) | 수동 | 빠른 컬럼 조회 |
| Volatile | Red-Black 트리 | 자동 | 빠른 PRIMARY KEY 액세스 |
| Lookup | LSM (선택) | 수동 | 빠른 컬럼 조회 |

**핵심 통찰력**: 대부분의 사용자는 수동으로 인덱스를 생성할 필요가 없습니다!

## Tag 테이블 인덱싱

### 자동 3단계 파티션 인덱스

Tag 테이블은 자동으로 정교한 인덱싱 시스템을 생성합니다:

**레벨 1: 태그 이름 인덱스**
- 특정 센서를 빠르게 찾음
- sensor_id에 의한 O(log n) 조회

**레벨 2: 시간 파티셔닝**
- 시간 범위별로 데이터 파티션
- 관련 없는 시간 기간 건너뜀

**레벨 3: 값 인덱스 (SUMMARIZED 컬럼용)**
- 파티션별 값 인덱스
- 빠른 범위 쿼리

### 작동 방식

```sql
CREATE TAGDATA TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
);

-- 내부적으로 Machbase가 생성:
-- 1. sensor_id에 대한 인덱스 (태그 이름)
-- 2. 시간 기반 파티션
-- 3. 각 파티션 내 temperature에 대한 인덱스
```

### 쿼리 최적화

**최적 쿼리** (3개 인덱스 레벨 모두 사용):
```sql
-- 빠름: sensor_id 인덱스 + 시간 파티션 + 값 인덱스 사용
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN '2025-10-10 00:00:00' AND '2025-10-10 23:59:59'
  AND temperature > 25.0;
```

**좋은 쿼리** (2개 인덱스 레벨 사용):
```sql
-- sensor_id + 시간 파티션 사용
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
DURATION 1 HOUR;
```

**느린 쿼리** (전체 스캔):
```sql
-- 모든 센서 스캔 (sensor_id 필터 없음)
SELECT * FROM sensors
WHERE temperature > 30.0;
```

### Rollup 테이블 인덱스

Rollup 테이블은 자동으로 인덱싱됩니다:

```sql
-- Rollup 쿼리 (매우 빠름, 사전 집계된 데이터)
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND rollup = hour
DURATION 7 DAY;

-- 사용 가능한 Rollup 레벨: sec, min, hour
```

### 모범 사례

**DO (해야 할 것)**:
- WHERE 절에 항상 sensor_id 포함
- 시간 필터 사용 (DURATION 또는 시간 범위)
- 통계를 위해 Rollup 테이블 쿼리
- Machbase가 인덱스를 자동 관리하도록 허용

**DON'T (하지 말아야 할 것)**:
- 수동 인덱스 생성 시도 (지원되지 않음)
- sensor_id 필터 없이 쿼리 (느린 전체 스캔)
- Rollup으로 충분할 때 원시 데이터 쿼리

## Log 테이블 인덱싱

### LSM 인덱스 (선택)

Log 테이블은 선택적으로 LSM (Log-Structured Merge) 인덱스를 생성할 수 있습니다:

```sql
-- Log 테이블 생성
CREATE TABLE app_logs (
    level VARCHAR(10),
    component VARCHAR(50),
    message VARCHAR(2000)
);

-- 자주 쿼리되는 컬럼에 LSM 인덱스 생성
CREATE INDEX idx_level ON app_logs(level);
CREATE INDEX idx_component ON app_logs(component);
```

### 인덱스 생성 시기

**인덱스 생성하는 경우**:
- WHERE 절에 자주 사용되는 컬럼
- 쿼리 성능이 느린 경우
- 적당한 카디널리티를 가진 컬럼 (고유 값이 너무 많지 않음)

**인덱스 생략하는 경우**:
- 시간으로만 쿼리하는 경우
- 매우 높은 카디널리티를 가진 컬럼
- 쓰기 성능이 중요한 경우

### LSM 인덱스 특성

**장점**:
- 쓰기 중심 워크로드에 최적화
- 쓰기 시 블로킹 없음
- 자동 유지 관리

**LSM 작동 방식**:
1. 새 쓰기는 메모리 버퍼로
2. 주기적으로 디스크 세그먼트로 플러시
3. 백그라운드 병합 프로세스가 세그먼트 결합
4. 읽기는 세그먼트 전체 검색

### 인덱스 구축

```sql
-- 인덱스 상태 확인
SHOW INDEXES;

-- 인덱스 구축 진행 상황 확인
SHOW INDEXGAP;

-- 인덱스는 백그라운드에서 구축 (블로킹 없음)
```

### 쿼리 최적화

**인덱스 사용**:
```sql
-- 빠름: idx_level 사용
SELECT * FROM app_logs
WHERE level = 'ERROR'
DURATION 1 HOUR;
```

**인덱스 미사용**:
```sql
-- 느림: 전체 스캔, 하지만 여전히 시간 파티셔닝 사용
SELECT * FROM app_logs
WHERE message SEARCH 'timeout'
DURATION 1 HOUR;
```

## Volatile 테이블 인덱싱

### 자동 Red-Black 트리

Volatile 테이블은 PRIMARY KEY에 대해 자동으로 인메모리 인덱스를 생성합니다:

```sql
CREATE VOLATILE TABLE device_status (
    device_id INTEGER PRIMARY KEY,  -- 자동 인덱싱
    status VARCHAR(20),
    last_updated DATETIME
);
```

### 성능 특성

- **조회**: PRIMARY KEY로 O(log n)
- **삽입**: O(log n)
- **업데이트**: O(log n)
- **삭제**: O(log n)

모든 작업이 인메모리에서 수행 (매우 빠름!).

### 쿼리 최적화

**빠름**:
```sql
-- PRIMARY KEY 인덱스 사용
SELECT * FROM device_status WHERE device_id = 101;
UPDATE device_status SET status = 'RUNNING' WHERE device_id = 101;
DELETE FROM device_status WHERE device_id = 101;
```

**느림**:
```sql
-- 전체 스캔 (status에 인덱스 없음)
SELECT * FROM device_status WHERE status = 'ERROR';
```

## Lookup 테이블 인덱싱

### LSM 인덱스 (Log 테이블과 동일)

```sql
CREATE LOOKUP TABLE devices (
    device_id INTEGER,
    device_name VARCHAR(100),
    location VARCHAR(200)
);

-- 자주 쿼리되는 컬럼에 인덱스 생성
CREATE INDEX idx_device_id ON devices(device_id);
CREATE INDEX idx_location ON devices(location);
```

Log 테이블 인덱싱과 동일한 원칙입니다.

## 시간 기반 파티셔닝

### 자동 파티셔닝

모든 디스크 기반 테이블 (Tag, Log, Lookup)은 시간 기반 파티셔닝을 사용합니다:

```
파티션 구조:
┌──────────────────────────────────────┐
│ 파티션 1: 1주차 (10월 1-7)           │
│   - 이번 주 데이터                   │
│   - 별도 인덱스                      │
│   - 최적화된 압축                    │
├──────────────────────────────────────┤
│ 파티션 2: 2주차 (10월 8-14)          │
│   - 이번 주 데이터                   │
│   - 별도 인덱스                      │
│   - 최적화된 압축                    │
├──────────────────────────────────────┤
│ 파티션 3: 3주차 (10월 15-21)         │
│   - 활성 파티션                      │
│   - 덜 압축됨 (쓰기용)               │
└──────────────────────────────────────┘
```

### 이점

**쿼리 성능**:
- 관련 파티션만 스캔
- 오래된/미래 파티션 건너뜀
- 병렬 파티션 스캔

**데이터 관리**:
- 쉬운 보존 (오래된 파티션 삭제)
- 파티션별 압축
- 효율적인 백업/복원

### 쿼리 최적화

**좋음** (1개 파티션 스캔):
```sql
SELECT * FROM logs DURATION 1 DAY;
```

**느림** (여러 파티션 스캔):
```sql
SELECT * FROM logs DURATION 30 DAY;
```

**매우 느림** (모든 파티션 스캔):
```sql
SELECT * FROM logs;  -- 시간 필터 없음!
```

## 쿼리 최적화 전략

### 1. 항상 시간 필터 사용

**나쁨**:
```sql
SELECT * FROM sensors WHERE sensor_id = 'sensor01';
```

**좋음**:
```sql
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
DURATION 1 HOUR;
```

### 2. DURATION 키워드 사용

**좋음** (최적화된 구문):
```sql
SELECT * FROM logs DURATION 1 HOUR;
```

**덜 최적** (수동 시간 필터):
```sql
SELECT * FROM logs
WHERE _arrival_time >= NOW - INTERVAL '1' HOUR;
```

### 3. 원시 데이터가 아닌 Rollup 쿼리

**좋음** (즉각적인 결과):
```sql
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND rollup = hour
DURATION 7 DAY;
```

**느림** (수백만 행):
```sql
SELECT sensor_id, AVG(temperature)
FROM sensors
WHERE sensor_id = 'sensor01'
DURATION 7 DAY
GROUP BY sensor_id;
```

### 4. 결과 세트 제한

**좋음**:
```sql
SELECT * FROM logs DURATION 1 HOUR LIMIT 1000;
```

**나쁨**:
```sql
SELECT * FROM logs;  -- 수백만 행 반환!
```

### 5. 높은 선택성을 가진 컬럼에 인덱스 사용

**좋은 인덱스** (적당한 카디널리티):
```sql
-- level: ERROR, WARN, INFO (낮은 카디널리티 - 좋음!)
CREATE INDEX idx_level ON logs(level);
```

**나쁜 인덱스** (매우 높은 카디널리티):
```sql
-- message: 수백만 개의 고유 값 (인덱스 생성 금지!)
CREATE INDEX idx_message ON logs(message);  -- 이렇게 하지 마세요!
```

## 압축

### 자동 압축

Machbase는 자동으로 데이터를 압축합니다:

**논리적 압축** (컬럼형):
- 각 컬럼이 별도로 압축
- 패턴 기반 압축
- 10-100배 압축 비율

**물리적 압축** (블록):
- 디스크 블록 압축
- 사용자에게 투명
- 추가 2-5배 압축

### 압축 특성

| 테이블 타입 | 압축 방법 | 일반 비율 |
|-----------|-------------------|---------------|
| Tag | 컬럼형 + 블록 | 50-100배 |
| Log | 컬럼형 + 블록 | 10-50배 |
| Volatile | 없음 (인메모리) | 1배 |
| Lookup | 블록 레벨 | 2-5배 |

### 성능에 미치는 영향

**읽기**:
- 압축된 데이터를 더 빠르게 읽음 (I/O 감소)
- 압축 해제 오버헤드 최소
- 대규모 스캔에 순 이익

**쓰기**:
- 먼저 메모리에 버퍼링
- 플러시 중 압축
- 쓰기 시간 페널티 없음

## 성능 모니터링

### 테이블 통계 확인

```sql
-- 테이블 정보 보기
SHOW TABLE sensors;

-- 스토리지 사용량 보기
SHOW STORAGE;

-- 테이블스페이스 정보 보기
SHOW TABLESPACES;
```

### 쿼리 모니터링

```sql
-- 활성 쿼리 보기
SHOW STATEMENTS;

-- 느린 쿼리 확인
-- (장시간 실행 쿼리가 여기에 표시됨)
```

### 인덱스 상태

```sql
-- 인덱스 확인
SHOW INDEXES;

-- 인덱스 구축 진행 상황 보기
SHOW INDEXGAP;
```

## 성능 튜닝

### 서버 구성

주요 매개변수 (machbase.conf):

```properties
# 메모리 설정
BUFFER_POOL_SIZE = 2G          # 공유 버퍼 캐시
VOLATILE_TABLESPACE_SIZE = 1G  # Volatile 테이블 메모리

# 쓰기 성능
CHECKPOINT_INTERVAL_SEC = 600  # 체크포인트 주기
LOG_BUFFER_SIZE = 64M          # 쓰기 버퍼 크기

# 쿼리 성능
MAX_QPX_MEM = 512M             # 쿼리당 메모리 제한
QUERY_TIMEOUT = 60             # 쿼리 타임아웃 (초)
```

### 애플리케이션 최적화

**배치 쓰기**:
```c
// 대량 삽입에 APPEND 프로토콜 사용
SQLAppendOpen(stmt, "sensors");
for (int i = 0; i < 10000; i++) {
    SQLAppendDataV(stmt, sensor_id, time, value);
}
SQLAppendClose(stmt);  // 배치 커밋
```

**연결 풀링**:
- 연결 재사용
- 연결 오버헤드 방지
- 일반적으로 10-20 연결

**쿼리 결과 제한**:
```sql
-- UI 쿼리의 경우 항상 결과 제한
SELECT * FROM logs DURATION 1 HOUR LIMIT 100;
```

## 일반적인 성능 문제

### 문제 1: 시간 필터 없는 느린 쿼리

**문제**:
```sql
SELECT * FROM sensors WHERE sensor_id = 'sensor01';
-- 느림: 모든 파티션 스캔
```

**솔루션**:
```sql
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
DURATION 1 HOUR;  -- 빠름: 1개 파티션 스캔
```

### 문제 2: 분석을 위해 원시 데이터 쿼리

**문제**:
```sql
SELECT AVG(temperature) FROM sensors DURATION 7 DAY;
-- 느림: 수백만 행 집계
```

**솔루션**:
```sql
SELECT AVG(avg_temperature) FROM sensors
WHERE rollup = hour
DURATION 7 DAY;  -- 빠름: 사전 계산된 데이터 집계
```

### 문제 3: Log 테이블에 인덱스 누락

**문제**:
```sql
-- 인덱스 없이 느림
SELECT * FROM logs WHERE level = 'ERROR' DURATION 1 DAY;
```

**솔루션**:
```sql
CREATE INDEX idx_level ON logs(level);
-- 이제 빠름!
```

### 문제 4: 큰 결과 세트

**문제**:
```sql
SELECT * FROM logs DURATION 30 DAY;
-- 수백만 행 반환!
```

**솔루션**:
```sql
-- 대신 집계
SELECT level, COUNT(*) FROM logs
DURATION 30 DAY
GROUP BY level;

-- 또는 결과 제한
SELECT * FROM logs DURATION 30 DAY LIMIT 1000;
```

## 모범 사례 요약

1. **항상 시간 필터 사용** (DURATION 또는 시간 범위)
2. **분석을 위해 Rollup 쿼리** (Tag 테이블)
3. **자주 쿼리되는 컬럼에 인덱스 생성** (Log/Lookup 테이블)
4. **결과 세트 제한** (LIMIT 절 사용)
5. **배치 쓰기 사용** (APPEND 프로토콜)
6. **Machbase가 인덱스 관리하도록 허용** (Tag/Volatile 테이블)
7. **쿼리 성능 모니터링** (SHOW STATEMENTS)
8. **데이터 보존 구현** (오래된 데이터 DELETE)

## 다음 단계

- **지식 적용**: [일반 작업](../../common-tasks/querying/) - 쿼리 최적화
- **더 배우기**: [테이블 타입](../../table-types/) - 상세 테이블 문서
- **문제 해결**: [문제 해결](../../troubleshooting/) - 성능 문제

## 핵심 요점

1. **Tag 테이블**은 자동 3단계 파티션 인덱스 사용
2. **Log/Lookup 테이블**은 선택적 LSM 인덱스 사용 가능
3. **Volatile 테이블**은 자동 인메모리 인덱스 사용
4. **시간 기반 파티셔닝**은 자동이며 필수
5. 최적 성능을 위해 **항상 시간으로 필터링**
6. 분석을 위해 **원시 데이터가 아닌 Rollup 쿼리**
7. **대부분의 사용자는 수동 인덱스를 생성하지 않음** - 자동입니다!

---

인덱싱을 마스터하고 Machbase의 전체 성능 잠재력을 발휘하세요!
