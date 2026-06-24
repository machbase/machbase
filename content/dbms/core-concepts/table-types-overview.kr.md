---
type: docs
title: '테이블 타입: 완전 가이드'
weight: 20
---

데이터에 적합한 테이블 타입을 선택합니다. 이 가이드는 의사 결정 프레임워크, 성능 특성 및 실제 예제와 함께 Machbase 테이블 타입을 비교합니다.

## 5가지 테이블 타입

Machbase는 각각 다른 워크로드에 최적화된 특화 테이블 타입을 제공합니다:

1. **Tag 테이블** - 센서/장치 축 기반 데이터 (시간 또는 거리)
2. **Log 테이블** - 이벤트 스트림 및 로그
3. **Volatile 테이블** - 단일 primary-key 인덱스를 사용하는 비영구 메모리 테이블
4. **Lookup 테이블** - 단일 primary-key 메모리 인덱스를 사용하는 영구 참조 테이블
5. **RDB 테이블** - 선택적 primary key와 보조 인덱스를 지원하는 범용 디스크 row 테이블

## 빠른 결정 가이드

### 여기서 시작하세요

다음 질문에 답하여 테이블 타입을 찾으세요:

```
┌─────────────────────────────────────────────────┐
│ 어떤 종류의 데이터를 가지고 있나요?              │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
    영구적?                      임시?
        │                           │
        ▼                           ▼
    ┌───────┐                 ┌──────────┐
    │  예   │                 │ Volatile │
    └───┬───┘                 │  테이블  │
        │                     └──────────┘
        ▼
    센서/텔레메트리 데이터
    (ID, 축, 값)?
        │
    ┌───┴────┐
    │        │
   예       아니오
    │        │
    ▼        ▼
  Tag     Log/이벤트
  테이블    데이터?
            │
        ┌───┴────┐
        │        │
       예     아니오
        │        │
        ▼        ▼
      Log     단일 primary-key
      테이블   참조 데이터?
                  │
              ┌───┴────┐
              │        │
             예     아니오
              │        │
              ▼        ▼
           Lookup    RDB
            테이블    테이블
```

데이터가 영구 참조 데이터이고 모든 접근 경로가 하나의 primary key를 중심으로
설계된다면 Lookup 테이블을 선택합니다. 범용 디스크 row 스키마, 선택적 primary key,
보조 인덱스, JSON path 인덱스, 일반적인 인덱스 predicate가 필요하면 RDB 테이블을
선택합니다.

### 결정 표

| 데이터 | 권장 테이블 | 이유 |
|-----------|------------------|-----|
| 1000개 장치의 온도 센서 | **Tag 테이블** | 다중 센서, 시계열 값 |
| 애플리케이션 에러 로그 | **Log 테이블** | 이벤트 스트림, 유연한 스키마 |
| 라이브 사용자 세션 | **Volatile 테이블** | UPDATE 필요, 임시 |
| 장치 메타데이터/레지스트리 | **Lookup 테이블** | primary key 기반 영구 참조 데이터 |
| 주식 시장 틱 | **Tag 테이블** | 심볼을 태그로, 가격을 값으로 |
| 컨베이어 위치별 진동 데이터 | **Tag 테이블** | 거리축 기반 측정값 |
| HTTP 액세스 로그 | **Log 테이블** | 이벤트 기반, 많은 컬럼 |
| 장바구니 내용 | **Volatile 테이블** | 빈번한 업데이트, 세션 기반 |
| 제품 ID 기준 제품 카탈로그 | **Lookup 테이블** | 하나의 primary key로 접근하는 영구 참조 데이터 |
| 현재 알람 상태 | **RDB 테이블** | UPDATE/DELETE가 필요한 범용 디스크 row |
| 작업 큐 | **RDB 테이블** | row 변경과 인덱스 predicate |

## Tag 테이블 심층 분석

### 사용 시기

다음에 완벽합니다:
- IoT 센서 데이터 (온도, 습도, 압력)
- 산업 장비 원격 측정
- 스마트 미터
- GPS 추적
- 거리 기반 원격 측정 (주행거리, 컨베이어 길이, 선로 위치)
- `(sensor_id, time|distance, value)` 패턴을 가진 모든 데이터

### 구조

```sql
-- Time axis
CREATE TAG TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,    -- 태그 이름 (센서 식별자)
    time DATETIME BASETIME,               -- 타임스탬프
    value DOUBLE SUMMARIZED,              -- Rollup 대상 측정값
    other_value DOUBLE                    -- 추가 측정값
) WITH ROLLUP;

-- Distance axis
CREATE TAG TABLE conveyor_profile (
    line_id VARCHAR(20) PRIMARY KEY,
    distance_m DOUBLE BASE DISTANCE,
    vibration DOUBLE,
    temperature DOUBLE
);
```

### 주요 기능

**Rollup 통계 (시간축 전용)**:
```sql
-- 원시 데이터
INSERT INTO sensors VALUES ('sensor01', NOW, 25.3);

-- rollup 표현식으로 시간별 통계 쿼리
SELECT rollup('hour', 1, time) AS hour_time, AVG(value), COUNT(value)
FROM sensors
GROUP BY hour_time;
```

rollup 표현식은 `WITH ROLLUP`으로 테이블을 생성하거나 `CREATE ROLLUP`으로 rollup을
정의한 뒤 사용합니다. 거리축 Tag 테이블은 rollup 대신 거리 범위 조회와 버킷 집계를
사용합니다.

**메타데이터 계층**:
```sql
-- 센서 메타데이터를 위한 별도 테이블
SELECT * FROM sensors._META;

-- 사용자 정의 메타데이터 컬럼 추가
ALTER TABLE sensors._META ADD COLUMN location VARCHAR(100);
UPDATE sensors._META SET location = 'Building A' WHERE name = 'sensor01';
```

**성능**:
- 초당 수백만 건의 삽입
- tag + axis 범위에 의한 초고속 쿼리
- 자동 3단계 파티션 인덱싱

### 모범 사례

**DO (해야 할 것)**:
- 다중 센서 데이터에 사용 (하나의 테이블에 수천 개의 센서)
- Rollup 대상 컬럼을 SUMMARIZED로 표시
- 시간축 테이블의 통계를 위해 Rollup 테이블 쿼리
- 센서 정보를 위해 메타데이터 테이블 사용

**DON'T (하지 말아야 할 것)**:
- 각 센서마다 별도 테이블 생성
- 데이터 값 UPDATE 시도 (업데이트는 메타데이터 사용)
- 비센서 데이터에 사용

### 사용 사례 예시

```sql
-- 제조: 장비 센서
CREATE TAG TABLE equipment_telemetry (
    equipment_id VARCHAR(50) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED,
    vibration DOUBLE,
    rpm DOUBLE,
    power_consumption DOUBLE
);

-- 스마트 시티: 환경 모니터링
CREATE TAG TABLE air_quality (
    station_id VARCHAR(30) PRIMARY KEY,
    time DATETIME BASETIME,
    pm25 DOUBLE SUMMARIZED,
    pm10 DOUBLE,
    co2 DOUBLE,
    temperature DOUBLE
);

-- 거리축: 컨베이어/주행거리 프로파일
CREATE TAG TABLE route_profile (
    route_id VARCHAR(30) PRIMARY KEY,
    distance_m DOUBLE BASE DISTANCE,
    vibration DOUBLE,
    temperature DOUBLE
);
```

## Log 테이블 심층 분석

### 사용 시기

다음에 완벽합니다:
- 애플리케이션 로그
- 이벤트 스트림
- 액세스 로그
- 트랜잭션 로그
- 가변 스키마를 가진 타임스탬프 이벤트

### 구조

```sql
CREATE TABLE app_logs (
    level VARCHAR(10),
    component VARCHAR(50),
    message VARCHAR(2000),
    user_id INTEGER,
    ip_addr IPV4
    -- _arrival_time 자동 추가!
);
```

### 주요 기능

**자동 타임스탬프**:
```sql
-- 사용자 입력
INSERT INTO app_logs VALUES ('ERROR', 'DB', 'Connection timeout', 123, '192.168.1.1');

-- Machbase가 나노초 타임스탬프와 함께 저장
-- _arrival_time: 2025-10-10 14:23:45.123456789
```

**전문 검색**:
```sql
-- SEARCH 사용 전 KEYWORD 인덱스 생성
CREATE INDEX idx_app_logs_message ON app_logs(message) INDEX_TYPE KEYWORD;

-- 빠른 텍스트 검색
SELECT * FROM app_logs
WHERE message SEARCH 'timeout'
  AND level = 'ERROR';
```

**유연한 스키마**:
- 임의 개수의 컬럼
- 임의 데이터 타입
- 고정 패턴 불필요

**성능**:
- 초당 수백만 건의 삽입
- 최신 데이터가 먼저 반환 (자동 정렬)
- 빠른 조회를 위한 선택적 LSM 인덱싱

### 모범 사례

**DO (해야 할 것)**:
- 가변 이벤트 데이터에 사용
- 텍스트 쿼리에 SEARCH 활용
- 시간 기반 쿼리에 DURATION 사용
- 보존 정책 구현

**DON'T (하지 말아야 할 것)**:
- 센서 데이터에 사용 (대신 Tag 테이블 사용)
- 참조 데이터 저장 (Lookup 테이블 사용)
- 키에 의한 UPDATE/DELETE 기대

### 사용 사례 예시

```sql
-- 애플리케이션 모니터링
CREATE TABLE application_events (
    app_name VARCHAR(50),
    event_type VARCHAR(50),
    severity VARCHAR(20),
    message VARCHAR(2000),
    user_id INTEGER,
    session_id VARCHAR(100),
    stack_trace VARCHAR(4000)
);

-- 웹 서버 액세스 로그
CREATE TABLE http_access (
    method VARCHAR(10),
    uri VARCHAR(1000),
    status_code INTEGER,
    response_time INTEGER,
    client_ip IPV4,
    user_agent VARCHAR(500),
    referer VARCHAR(500)
);

-- 금융 거래
CREATE TABLE transactions (
    transaction_id VARCHAR(50),
    account_id INTEGER,
    transaction_type VARCHAR(30),
    amount DOUBLE,
    currency VARCHAR(3),
    status VARCHAR(20),
    description VARCHAR(500)
);
```

## Volatile 테이블 심층 분석

### 사용 시기

다음에 완벽합니다:
- 실시간 대시보드
- 세션 관리
- 라이브 상태 보드
- 캐싱 계층
- primary key 기반 UPDATE/DELETE가 필요한 임시 데이터

### 구조

```sql
CREATE VOLATILE TABLE live_status (
    device_id INTEGER PRIMARY KEY,    -- 업데이트를 위해 PRIMARY KEY 필요
    status VARCHAR(20),
    last_value DOUBLE,
    last_updated DATETIME
);
```

### 주요 기능

**키에 의한 UPDATE 및 DELETE**:
```sql
-- 기존 레코드 업데이트
UPDATE live_status
SET status = 'RUNNING', last_value = 25.3, last_updated = NOW
WHERE device_id = 101;

-- 특정 레코드 삭제
DELETE FROM live_status WHERE device_id = 101;
```

**비영구 메모리 primary-key 테이블**:
- 모든 데이터가 RAM에 상주
- 단일 primary-key 메모리 인덱스 사용
- 매우 빠른 읽기/쓰기
- 초당 수만 건의 작업

**경고: 비영구적**:
- 서버 재시작 시 데이터 손실
- 종료 전에 중요한 데이터 아카이브

### 모범 사례

**DO (해야 할 것)**:
- 빠른 조회를 위해 PRIMARY KEY 사용
- 데이터 볼륨을 작게 유지 (RAM에 의해 제한)
- Log/Tag 테이블로 주기적 아카이브
- 현재 상태에만 사용

**DON'T (하지 말아야 할 것)**:
- 영구적이어야 하는 데이터 저장
- 대용량 스트리밍 데이터에 사용
- 재시작 후 데이터 생존 기대

### 사용 사례 예시

```sql
-- 실시간 장비 상태
CREATE VOLATILE TABLE equipment_status (
    equipment_id INTEGER PRIMARY KEY,
    online CHAR(1),
    current_temp DOUBLE,
    current_pressure DOUBLE,
    last_heartbeat DATETIME
);

-- 활성 사용자 세션
CREATE VOLATILE TABLE user_sessions (
    session_token VARCHAR(100) PRIMARY KEY,
    user_id INTEGER,
    ip_address IPV4,
    login_time DATETIME,
    last_activity DATETIME,
    expires_at DATETIME
);

-- 라이브 모니터링 캐시
CREATE VOLATILE TABLE monitoring_cache (
    metric_key VARCHAR(100) PRIMARY KEY,
    metric_value VARCHAR(500),
    updated_at DATETIME
);
```

## Lookup 테이블 심층 분석

### 사용 시기

다음에 완벽합니다:
- 장치 레지스트리
- 구성 테이블
- 카테고리/차원 테이블
- 마스터 데이터
- 하나의 primary key로 접근하는 영구 참조 데이터

### 구조

```sql
CREATE LOOKUP TABLE devices (
    device_id VARCHAR(20) PRIMARY KEY,
    device_name VARCHAR(100),
    location VARCHAR(200),
    device_type VARCHAR(50),
    owner VARCHAR(100)
);
```

### 주요 기능

**primary key 기반 전체 CRUD 지원**:
```sql
-- Insert
INSERT INTO devices VALUES ('sensor01', 'Sensor A', 'Building 1', 'Temperature', 'Facilities');

-- Update
UPDATE devices SET location = 'Building 2' WHERE device_id = 'sensor01';

-- Delete
DELETE FROM devices WHERE device_id = 'sensor01';

-- Select
SELECT * FROM devices WHERE device_id = 'sensor01';
```

**시계열과의 JOIN**:
```sql
-- 장치 정보로 센서 데이터 강화
SELECT s.*, d.device_name, d.location
FROM sensors s
JOIN devices d ON s.sensor_id = d.device_id
WHERE s.time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
                 AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

**영구 데이터와 메모리 primary-key 인덱스**:
- 데이터는 재시작 후에도 유지
- 단일 primary-key 메모리 인덱스로 빠른 key 접근 지원
- 전체 DML은 primary-key predicate 중심으로 사용

### 모범 사례

**DO (해야 할 것)**:
- 참조/마스터 데이터에 사용
- Tag/Log 테이블과 JOIN
- 접근 경로를 primary key 중심으로 설계
- 데이터 볼륨을 적절하게 유지 (<1M 행 이상적)

**DON'T (하지 말아야 할 것)**:
- 고빈도 삽입에 사용
- 시계열 데이터 저장
- 초당 수백만 건의 쓰기 기대

### 사용 사례 예시

```sql
-- 장치 레지스트리
CREATE LOOKUP TABLE device_registry (
    device_id VARCHAR(50) PRIMARY KEY,
    device_name VARCHAR(100),
    device_type VARCHAR(50),
    location VARCHAR(200),
    installation_date DATETIME,
    status VARCHAR(20)
);

-- 구성 관리
CREATE LOOKUP TABLE system_config (
    config_key VARCHAR(100) PRIMARY KEY,
    config_value VARCHAR(500),
    config_category VARCHAR(50),
    description VARCHAR(500)
);

-- 사용자 관리
CREATE LOOKUP TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(200),
    role VARCHAR(50),
    created_at DATETIME
);
```

## RDB 테이블 심층 분석

### 사용 시기

다음에 적합합니다:
- 장비 마스터 데이터
- 알람 룰 및 현재 알람 상태
- 작업 큐
- Tag 또는 Log 데이터와 조인하는 차원 테이블
- 영구 저장과 인덱스 predicate가 필요한 범용 디스크 row 데이터

### 구조

```sql
CREATE RDB TABLE device_master (
    id         INTEGER PRIMARY KEY,
    name       VARCHAR(64) NOT NULL,
    site       VARCHAR(32) DEFAULT 'SEOUL',
    state      VARCHAR(16),
    info       JSON,
    updated_at DATETIME
);
```

### 주요 기능

**디스크 row 대상 전체 DML 지원**:
```sql
INSERT INTO device_master(id, name, state) VALUES (1, 'pump-01', 'READY');

UPDATE device_master
   SET state = 'RUNNING'
 WHERE id = 1;

DELETE FROM device_master
 WHERE id = 1;
```

**인덱스와 제약**:
```sql
CREATE INDEX idx_device_site ON device_master(site);
CREATE UNIQUE INDEX uidx_device_name ON device_master(name);
CREATE PRIMARY KEY INDEX pk_device_id ON device_master(id);
CREATE INDEX idx_device_owner ON device_master(info->'$.owner');
```

**Backup 및 Mount 통합**:
RDB 테이블 데이터는 database backup과 table backup image에 포함됩니다. Mounted database에서는 RDB 테이블과 view를 조회할 수 있지만 mounted RDB 객체는 read-only입니다.

### 모범 사례

**DO (해야 할 것)**:
- row 단위로 변경되는 영구 운영 상태에 사용
- 자주 사용하는 조회 조건에 인덱스 추가
- Tag 및 Log 데이터와 조인하는 차원 테이블로 사용
- Lookup의 단일 primary-key 모델이 부족할 때 사용

**DON'T (하지 말아야 할 것)**:
- 고속 센서 수집에 사용 (대신 Tag 또는 Log 테이블 사용)
- cluster edition에서 사용
- backend native SQL passthrough 기대

## 성능 비교

### 쓰기 성능

| 테이블 타입 | 초당 삽입 | UPDATE 지원 | DELETE 지원 |
|-----------|-------------|----------------|----------------|
| Tag | 수백만 건 | 메타데이터만 | 시간 기반 |
| Log | 수백만 건 | 불가 | 시간 기반 |
| Volatile | 수만 건 | PRIMARY KEY로 | PRIMARY KEY로 |
| Lookup | 수백 건 | 가능 | 가능 |
| RDB | 워크로드에 따라 다름 | 가능 | 가능 |

### 읽기 성능

| 테이블 타입 | 읽기 속도 | 최적 | 인덱스 타입 |
|-----------|-----------|----------|------------|
| Tag | 매우 빠름 | sensor_id + time | 3단계 파티션 |
| Log | 빠름 | 시간 범위 | 선택적 log 인덱스 |
| Volatile | 매우 빠름 | PRIMARY KEY | Red-black 트리 |
| Lookup | 빠름 | PRIMARY KEY | 메모리 primary-key 인덱스 |
| RDB | 빠름 | 인덱스 predicate | RDB 인덱스 |

### 스토리지

| 테이블 타입 | 스토리지 | 압축 | 지속성 |
|-----------|---------|-------------|-------------|
| Tag | 디스크 | 10-100배 | 예 |
| Log | 디스크 | 10-100배 | 예 |
| Volatile | 메모리 | 없음 | 아니오 |
| Lookup | 영구 데이터 + 메모리 인덱스 | 보통 | 예 |
| RDB | 디스크 | backend에 따라 다름 | 예 |

## 테이블 타입 결합

### 패턴: IoT 플랫폼

```sql
-- Tag: 센서 측정값
CREATE TAG TABLE sensor_data (...);

-- Lookup: 장치 레지스트리
CREATE LOOKUP TABLE devices (...);

-- RDB: 현재 장치 상태와 작업 큐
CREATE RDB TABLE device_state (...);

-- Volatile: 라이브 상태
CREATE VOLATILE TABLE device_status (...);

-- Log: 이벤트 및 알림
CREATE TABLE device_events (...);
```

### 패턴: 웹 애플리케이션

```sql
-- Log: 액세스 로그
CREATE TABLE http_access (...);

-- Log: 애플리케이션 로그
CREATE TABLE app_logs (...);

-- Volatile: 활성 세션
CREATE VOLATILE TABLE sessions (...);

-- Lookup: 사용자 계정
CREATE LOOKUP TABLE users (...);

-- RDB: 주문 및 workflow 상태
CREATE RDB TABLE orders (...);
```

### 패턴: 제조

```sql
-- Tag: 장비 센서
CREATE TAG TABLE equipment_telemetry (...);

-- Log: 생산 이벤트
CREATE TABLE production_log (...);

-- Volatile: 라인 상태
CREATE VOLATILE TABLE line_status (...);

-- Lookup: 장비 카탈로그
CREATE LOOKUP TABLE equipment_catalog (...);

-- RDB: 알람 룰 및 활성 알람 상태
CREATE RDB TABLE alarm_state (...);
```

## 피해야 할 안티패턴

### 안티패턴 1: 사용 사례에 잘못된 테이블

**나쁨**: 센서 데이터에 Log 테이블 사용
```sql
-- 이렇게 하지 마세요!
CREATE TABLE sensors (sensor_id VARCHAR(20), value DOUBLE);
```

**좋음**: Tag 테이블 사용
```sql
CREATE TAG TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

### 안티패턴 2: 센서당 하나의 테이블

**나쁨**: 1000개 센서를 위한 1000개 테이블 생성
```sql
CREATE TAG TABLE sensor001 (...);
CREATE TAG TABLE sensor002 (...);
-- ... 998개의 테이블 더
```

**좋음**: 모든 센서를 위한 하나의 테이블
```sql
CREATE TAG TABLE all_sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    ...
);
```

### 안티패턴 3: Volatile에 기록 저장

**나쁨**: 영구 데이터에 Volatile 사용
```sql
-- 재시작 시 데이터 손실!
CREATE VOLATILE TABLE important_transactions (...);
```

**좋음**: Log 또는 Tag 테이블 사용
```sql
CREATE TABLE important_transactions (...);
```

### 안티패턴 4: Lookup으로 고빈도 쓰기

**나쁨**: Lookup 테이블로 수백만 건 삽입
```sql
-- 너무 느림!
CREATE LOOKUP TABLE sensor_readings (...);
```

**좋음**: Tag 또는 Log 테이블 사용
```sql
CREATE TAG TABLE sensor_readings (...);
```

## 마이그레이션 가이드

### 다른 데이터베이스에서

**PostgreSQL/MySQL에서**:
- 이벤트 테이블 → Log 테이블
- 운영 row 테이블 → RDB 테이블
- 시계열 테이블 → Tag 테이블
- 임시 테이블 → Volatile 테이블
- 차원 테이블 → Lookup 테이블

**InfluxDB에서**:
- Measurements → Tag 테이블
- Tags → Tag primary key + 메타데이터
- Fields → SUMMARIZED 값 컬럼 하나와 일반 값 컬럼

**MongoDB에서**:
- 시계열 컬렉션 → Tag/Log 테이블
- 참조 컬렉션 → Lookup 테이블
- Capped 컬렉션 → 보존이 있는 Log 테이블

## 요약 매트릭스

| 기능 | Tag | Log | Volatile | Lookup | RDB |
|---------|-----|-----|----------|--------|-----|
| **주요 용도** | 센서 | 이벤트 | 캐시 | 참조 | row 상태 |
| **스키마** | 고정 패턴 | 유연 | 유연 | 유연 | 유연 |
| **초당 쓰기** | 수백만 | 수백만 | 수만 | 수백 | 워크로드에 따라 다름 |
| **UPDATE** | 메타데이터 | 불가 | 가능 | 가능 | 가능 |
| **DELETE** | 시간 기반 | 시간 기반 | 키로 | 키로 | 가능 |
| **스토리지** | 디스크 | 디스크 | 메모리 | 디스크 | 디스크 |
| **지속성** | 예 | 예 | 아니오 | 예 | 예 |
| **Rollup** | 설정 시 | 불가 | 불가 | 불가 | 불가 |
| **최적 쿼리** | ID + time | 시간 | 키 | primary key | 인덱스 predicate |
| **압축** | 매우 높음 | 높음 | 없음 | 보통 | backend에 따라 다름 |

## 다음 단계

- **심층 분석**: [인덱싱 및 성능](../indexing/) - 쿼리 최적화
- **상세 레퍼런스**: [테이블 타입](../../table-types/) - 완전한 문서
- **실습**: [테이블 타입](../../table-types/) - 실제 예제로 연습

## 핵심 요점

1. **Tag 테이블**은 Rollup을 지원하는 센서/장치 데이터용
2. **Log 테이블**은 유연한 이벤트 스트림 및 로그용
3. **Volatile 테이블**은 인메모리, 업데이트 가능한 데이터용
4. **Lookup 테이블**은 영구 primary-key 참조 데이터용
5. **RDB 테이블**은 범용 디스크 row 데이터용
6. 완전한 솔루션을 위해 **타입 결합**
7. **현명하게 선택** - 테이블 타입이 성능 결정

---

테이블 선택을 마스터하고 효율적인 Machbase 애플리케이션을 구축하세요!
