---
type: docs
title: '4.4 안티패턴'
weight: 40
toc: true
---
테이블 설계에서 피해야 할 대표적인 안티패턴을 다룹니다. 아래 패턴은 성능 저하, 운영 복잡도 증가, 데이터 손실로 이어질 수 있습니다.

- **[고빈도 LOOKUP 조회](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#high-frequency-lookup)**
- **[센서별 테이블 생성](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#per-sensor-create)**
- **[잘못된 타입 선택](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#table-types-selection-type-wrong)**
- **[VOLATILE 영속 저장 오용](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#storage-persistent-volatile)**
- **[시계열 데이터 TRANSACTION 오용](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#time-series-storage-misuse-rdb)**


<a id="high-frequency-lookup"></a>

## 고빈도 LOOKUP 조회

### 문제

문제는 조회 빈도 자체가 아니라, 계속 늘어나는 계측 이력을 LOOKUP에 저장하는 설계입니다.
LOOKUP은 전체 행과 인덱스를 메모리에 유지하므로 장기 시계열 이력이 쌓일수록 메모리 부담이
커집니다. 작은 기준 정보를 키로 반복 조회하는 용도에는 적합합니다.

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

시계열 계측값은 TAG 테이블에 저장합니다. 최신 값만 필요하면 VOLATILE 테이블을 캐시로 씁니다.

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
| 같은 센서 키로 이력 누적 | X (예제의 센서 키가 행을 식별) | O (태그 이름 아래 여러 계측 행 저장) |
| 지속 입력 경로 | 행 식별자 중심 | 시계열 Append API 사용 가능 |
| 시간 범위 조회 | 일반 조건 조회 | 태그·시간 축 조회 |

<a id="per-sensor-create"></a>

## 센서별 테이블 생성

### 문제

센서(태그)마다 별도 테이블을 생성하는 패턴입니다. 센서 수가 늘어날수록 DDL, 권한과 조회
대상도 함께 늘어나 운영 비용이 커집니다.

### 안티패턴 예시

```sql
-- 잘못된 설계: 센서마다 테이블 생성
CREATE TAG TABLE sensor_temp_01 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
CREATE TAG TABLE sensor_temp_02 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
CREATE TAG TABLE sensor_temp_03 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
-- ... 센서가 10,000개면 테이블도 10,000개
```

### 문제점

| 문제 | 설명 |
|------|------|
| 관리 복잡도 | 테이블 수만큼 DDL 관리 필요 |
| 쿼리 불편 | 여러 테이블을 결합해야 센서 간 집계 가능 |
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

데이터 특성에 맞지 않는 테이블 타입을 선택하는 대표적인 안티패턴입니다.

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
CREATE LOG TABLE error_log (
    level   SHORT,
    msg     VARCHAR(512),
    src     VARCHAR(128)
);
```

### 안티패턴 2: 센서 값을 LOG 테이블에 저장

```sql
-- 잘못됨: 센서 값을 LOG로 저장
CREATE LOG TABLE sensor_wrong (
    sensor_id VARCHAR(64),
    value     DOUBLE
    -- 태그별 시간 범위 집계 쿼리가 매우 비효율적
);
```

**올바른 설계**: TAG 테이블 사용

```sql
CREATE TAG TABLE sensor_measurements (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

### 안티패턴 3: 대용량 이력을 LOOKUP에 저장

```sql
-- 잘못됨: 관계형 트랜잭션이 필요한 주문 이력을 LOOKUP에 저장
CREATE LOOKUP TABLE order_history_wrong (
    order_id LONG PRIMARY KEY,
    customer VARCHAR(64)
    -- LOOKUP은 소규모 전용, 대용량에서 성능 저하
);
```

**올바른 설계**: TRANSACTION 테이블 사용

```sql
CREATE TRANSACTION TABLE order_history (
    order_id  LONG,
    customer  VARCHAR(64),
    item_id   INTEGER,
    amount    DOUBLE,
    status    VARCHAR(16)
);
-- UPDATE/DELETE/SELECT 모두 지원
UPDATE order_history SET status = 'SHIPPED' WHERE order_id = 1001;
```

### 안티패턴 4: 시계열 데이터를 TRANSACTION 테이블에 저장

TRANSACTION에도 시간 컬럼과 Append API를 사용할 수 있지만 TAG 전용 시간축 저장 구조와
ROLLUP은 제공되지 않습니다. 관계형 변경보다 계측 이력 수집과 집계가 중심이면 TAG를
검토합니다. 자세한 내용은 [시계열 데이터 TRANSACTION 오용](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#time-series-storage-misuse-rdb)을
참고하십시오.

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

- 서버가 종료되거나 재시작되면 테이블과 데이터가 소멸합니다.
- 서버 프로세스가 종료되는 장애에서도 메모리의 데이터를 복구할 수 없으므로,
  유일한 원본을 VOLATILE에 저장하면 데이터 손실로 이어집니다.

### 올바른 패턴

영구 보존이 필요한 데이터는 LOOKUP 또는 TRANSACTION 테이블에 저장합니다.

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

## 시계열 데이터 TRANSACTION 오용

### 문제

센서·IoT 계측값 같은 지속적인 시계열 데이터를 TRANSACTION 테이블에 저장하는 패턴입니다.
관계형 갱신이 필요하지 않다면 TAG 테이블의 태그·시간 축과 ROLLUP을 활용할 수 없으므로
조회와 운영 요구에 맞지 않습니다.

### 안티패턴 예시

```sql
-- 잘못됨: 센서 시계열 데이터를 TRANSACTION 테이블에 저장
CREATE TRANSACTION TABLE sensor_timeseries (
    sensor_id VARCHAR(64),
    ts        DATETIME,
    value     DOUBLE,
    unit      VARCHAR(16)
);
```

### 문제점

| 문제 | 설명 |
|------|------|
| 입력 의미 불일치 | 관계형 트랜잭션이 필요하지 않은 값에도 관계형 쓰기 경로 사용 |
| 시간 축 부재 | TAG의 BASETIME 기반 조회 구조를 사용할 수 없음 |
| 집계 기능 차이 | TAG 전용 ROLLUP을 사용할 수 없음 |

### 올바른 패턴

센서 계측값은 TAG 테이블에 저장합니다.

```sql
-- 올바름: TAG 테이블 사용
CREATE TAG TABLE sensor_history (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE,
    unit   VARCHAR(16)
);

-- Append API 고속 버퍼로 대량 입력 가능
-- 시간 단위 집계와 TAG 전용 최적화 활용 가능
SELECT name, DATE_TRUNC('hour', time, 1) AS hour, AVG(value), MAX(value)
FROM sensor_history
WHERE time >= NOW - 86400000000000
GROUP BY name, hour;
```

### TRANSACTION 테이블이 적합한 경우

TRANSACTION 테이블은 관계형 구조의 업무 데이터(주문, 재고, 설비 이력 등)에 씁니다. 시간 컬럼이 있더라도 UPDATE/DELETE가 필요한 업무 이력이라면 TRANSACTION 테이블을, 수정 없이 계속 쌓이는 고빈도 계측값이라면 TAG를 선택합니다.
