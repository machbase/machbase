---
type: docs
title: '4.4 안티패턴'
weight: 30
---
Machbase 테이블 설계에서 피해야 할 대표적인 안티패턴을 설명합니다. 이러한 패턴은 성능 저하, 운영 복잡도 증가, 데이터 손실로 이어질 수 있습니다.

- **[고빈도 LOOKUP 조회](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#high-frequency-lookup)**
- **[센서별 테이블 생성](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#per-sensor-create)**
- **[잘못된 타입 선택](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#table-types-selection-type-wrong)**
- **[VOLATILE 영속 저장 오용](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#storage-persistent-volatile)**
- **[시계열 데이터 RDB 오용](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#time-series-storage-misuse-rdb)**


<a id="high-frequency-lookup"></a>

## 고빈도 LOOKUP 조회

### 문제

LOOKUP 테이블을 초고빈도 시계열 데이터 조회에 사용하는 패턴입니다. LOOKUP 테이블은 소규모 참조 데이터에 최적화되어 있으며, 대량 시계열 데이터의 고속 조회에는 부적합합니다.

### 안티패턴 예시

```sql
-- 잘못된 설계: 센서 계측값을 LOOKUP 테이블에 저장
CREATE LOOKUP TABLE sensor_data_wrong (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    ts         DATETIME
);

-- LOOKUP은 한 센서당 한 행만 저장 가능 (PK 중복 불가)
-- 시계열 이력 저장 불가
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.3, NOW);
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.5, NOW);  -- PK 중복 오류
```

### 올바른 패턴

시계열 계측값은 TAG 테이블에 저장합니다. 최신 값만 필요하면 VOLATILE 테이블을 캐시로 사용합니다.

```sql
-- 올바른 설계: 이력은 TAG 테이블
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);

-- 최신값 캐시는 VOLATILE 테이블
CREATE VOLATILE TABLE sensor_latest (
    sensor_id VARCHAR(64) PRIMARY KEY,
    value     DOUBLE,
    updated_at DATETIME
);
```

### 결과

| | 안티패턴 (LOOKUP) | 올바른 설계 (TAG) |
|-|-----------------|-----------------|
| 이력 저장 | X (PK 중복 불가) | O |
| 고속 입력 | 느림 | 빠름 (Append API) |
| 시간 범위 조회 | 불가 | O |

<a id="per-sensor-create"></a>

## 센서별 테이블 생성

### 문제

센서(태그)마다 별도의 테이블을 생성하는 패턴입니다. 센서 수가 늘어날수록 테이블 수가 폭발적으로 증가하여 관리가 불가능해집니다.

### 안티패턴 예시

```sql
-- 잘못된 설계: 센서마다 테이블 생성
CREATE TAG TABLE sensor_temp_01 (...);
CREATE TAG TABLE sensor_temp_02 (...);
CREATE TAG TABLE sensor_temp_03 (...);
-- ... 센서가 10,000개면 테이블도 10,000개
```

### 문제점

| 문제 | 설명 |
|------|------|
| 관리 복잡도 | 테이블 수만큼 DDL 관리 필요 |
| 쿼리 불편 | 크로스-센서 집계 불가 |
| 메타데이터 증가 | 시스템 카탈로그 부하 |
| 신규 센서 추가 | 매번 DDL 실행 필요 |

### 올바른 패턴

센서 이름을 PRIMARY KEY로 하는 하나의 TAG 테이블에 모든 센서 데이터를 저장합니다.

```sql
-- 올바른 설계: 모든 온도 센서를 하나의 테이블로
CREATE TAG TABLE temperature_sensor (
    name   VARCHAR(128) PRIMARY KEY,
    time   DATETIME     BASETIME,
    value  DOUBLE
);

-- 모든 센서 데이터를 하나의 테이블에 삽입
INSERT INTO temperature_sensor VALUES ('TEMP-01', NOW, 23.5);
INSERT INTO temperature_sensor VALUES ('TEMP-02', NOW, 24.1);
INSERT INTO temperature_sensor VALUES ('TEMP-10000', NOW, 22.9);
```

### 장점

- 신규 센서 추가 시 DDL 불필요 (새 태그 이름으로 INSERT만 하면 됨)
- 크로스-센서 집계 용이
- 운영 관리 포인트 최소화

<a id="table-types-selection-type-wrong"></a>

## 잘못된 타입 선택

데이터 특성에 맞지 않는 테이블 타입을 선택하는 대표적인 안티패턴을 설명합니다.

### 안티패턴 1: 이벤트 로그를 TAG 테이블에 저장

```sql
-- 잘못됨: 이벤트 로그를 TAG로 저장
CREATE TAG TABLE error_log_wrong (
    name   VARCHAR(256) PRIMARY KEY,  -- 이벤트 내용이 태그 이름이 됨
    time   DATETIME     BASETIME,
    level  SHORT
);
-- 문제: 이벤트마다 고유 이름 → 태그 수 폭발
```

**올바른 설계**: LOG 테이블 사용

```sql
CREATE TABLE error_log (
    level   SHORT,
    msg     VARCHAR(512),
    src     VARCHAR(128)
);
```

### 안티패턴 2: 센서 값을 LOG 테이블에 저장

```sql
-- 잘못됨: 센서 값을 LOG로 저장
CREATE TABLE sensor_wrong (
    sensor_id VARCHAR(64),
    value     DOUBLE
    -- 태그별 시간 범위 집계 쿼리가 매우 비효율적
);
```

**올바른 설계**: TAG 테이블 사용

```sql
CREATE TAG TABLE sensor_data (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

### 안티패턴 3: 대용량 이력을 LOOKUP에 저장

```sql
-- 잘못됨: 수천만 건 주문 이력을 LOOKUP에
CREATE LOOKUP TABLE order_history_wrong (
    order_id LONG PRIMARY KEY,
    customer VARCHAR(64)
    -- LOOKUP은 소규모 전용, 대용량에서 성능 저하
);
```

**올바른 설계**: RDB 테이블 사용

```sql
CREATE RDB TABLE order_history (
    order_id  LONG,
    customer  VARCHAR(64),
    item_id   INTEGER,
    amount    DOUBLE,
    status    VARCHAR(16)
);
-- UPDATE/DELETE/SELECT 모두 지원
UPDATE order_history SET status = 'SHIPPED' WHERE order_id = 1001;
```

### 안티패턴 4: 시계열 데이터를 RDB에 저장

시계열 데이터(센서값)를 RDB 테이블에 저장하면 시간 범위 쿼리 성능이 나쁘고, Append API의 고속 버퍼 최적화도 사용할 수 없습니다. 자세한 내용은 [시계열 데이터 RDB 오용](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#time-series-storage-misuse-rdb) 항목을 참고하십시오.

<a id="storage-persistent-volatile"></a>

## VOLATILE 영속 저장 오용

### 문제

VOLATILE 테이블에 영구 보존이 필요한 데이터를 저장하는 패턴입니다.

### 안티패턴 예시

```sql
-- 잘못됨: 중요 설정을 VOLATILE에 저장
CREATE VOLATILE TABLE critical_config (
    key_name VARCHAR(64) PRIMARY KEY,
    value    VARCHAR(256)
);

INSERT INTO critical_config VALUES ('license_key', 'XXXX-XXXX-XXXX');
INSERT INTO critical_config VALUES ('max_connections', '1000');
-- 서버 재시작 시 모든 설정 소멸!
```

### 문제점

- 서버 재시작, 장애, OOM 등 어떤 상황에서도 데이터가 소멸됩니다.
- 운영 중 데이터 소멸로 서비스 장애가 발생합니다.

### 올바른 패턴

영구 보존이 필요한 데이터는 LOOKUP 또는 RDB 테이블에 저장합니다.

```sql
-- 올바름: 설정은 LOOKUP 테이블
CREATE LOOKUP TABLE app_config (
    key_name VARCHAR(64) PRIMARY KEY,
    value    VARCHAR(256)
);

INSERT INTO app_config VALUES ('max_connections', '1000');
-- 서버 재시작 후에도 데이터 유지
```

### VOLATILE의 올바른 용도

VOLATILE 테이블은 **재생성 가능한 캐시 데이터**에만 사용합니다.

| 적합 | 부적합 |
|------|--------|
| 센서 최신값 캐시 | 원본 트랜잭션 데이터 |
| 실시간 집계 결과 | 중요 설정 값 |
| 세션 임시 상태 | 감사 로그 |
| 대시보드 캐시 | 사용자 정보 |

<a id="time-series-storage-misuse-rdb"></a>

## 시계열 데이터 RDB 오용

### 문제

센서·IoT 계측값과 같은 대량 시계열 데이터를 RDB 테이블에 저장하는 패턴입니다. RDB 테이블은 UPDATE/DELETE를 포함한 일반 관계형 워크로드에 최적화되어 있으며, 초고빈도 시계열 수집에는 부적합합니다.

### 안티패턴 예시

```sql
-- 잘못됨: 센서 시계열 데이터를 RDB에 저장
CREATE RDB TABLE sensor_timeseries (
    sensor_id VARCHAR(64),
    ts        DATETIME,
    value     DOUBLE,
    unit      VARCHAR(16)
);
```

### 문제점

| 문제 | 설명 |
|------|------|
| Append API 고속 버퍼 미적용 | RDB의 Append는 트랜잭션 기반으로, TAG·LOG의 초고속 버퍼 최적화가 없음 |
| 시계열 최적화 없음 | 시간 범위 집계 성능이 TAG 테이블 대비 저하 |
| 시계열 압축 없음 | TAG 테이블의 시계열 압축 알고리즘 미적용 |
| 시계열 분석 기능 미흡 | TAG 전용 ROLLUP, FIRST, LAST 등 시계열 최적화 미지원 |

### 올바른 패턴

센서 계측값은 TAG 테이블에 저장합니다.

```sql
-- 올바름: TAG 테이블 사용
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE,
    unit   VARCHAR(16)
);

-- Append API 고속 버퍼로 대량 입력 가능
-- 시간 단위 집계와 TAG 전용 최적화 활용 가능
SELECT name, DATE_TRUNC('hour', time, 1) AS hour, AVG(value), MAX(value)
FROM sensor_data
WHERE time >= NOW - 86400000000000
GROUP BY name, hour;
```

### RDB 테이블이 적합한 경우

RDB 테이블은 관계형 구조의 업무 데이터(주문, 재고, 설비 이력 등)에 사용합니다. 시간 컬럼이 있더라도 UPDATE/DELETE가 필요한 업무 이력이라면 RDB를, 수정 없이 계속 쌓이는 고빈도 계측값이라면 TAG를 선택합니다.
