---
type: docs
title: '4.5 모델링 패턴'
weight: 50
toc: true
---
실제 운영 환경에서 자주 쓰이는 데이터 모델링 패턴을 다룹니다.

- **[시간축 모델링](/dbms/data-modeling-table-design/patterns-modeling/#time-axis-modeling)**
- **[거리축 모델링](/dbms/data-modeling-table-design/patterns-modeling/#distance-axis-modeling)**
- **[상태·캐시 모델링](/dbms/data-modeling-table-design/patterns-modeling/#state-cache-status-modeling)**
- **[이벤트·로그 모델링](/dbms/data-modeling-table-design/patterns-modeling/#event-log-modeling-logs)**
- **[참조·마스터 모델링](/dbms/data-modeling-table-design/patterns-modeling/#reference-master-modeling)**
- **[영속·임시 혼합 패턴](/dbms/data-modeling-table-design/patterns-modeling/#persistent-temporary)**
- **[INSERT·UPDATE 패턴](/dbms/data-modeling-table-design/patterns-modeling/#insert-update)**
- **[JOIN·메타데이터 설계](/dbms/data-modeling-table-design/patterns-modeling/#join-metadata-design)**
- **[복합 타입 조합 패턴](/dbms/data-modeling-table-design/patterns-modeling/#table-types-patterns-combined-type)**


<a id="time-axis-modeling"></a>

## 시간축 모델링

시간을 기준 축으로 삼는 패턴으로, 센서 계측값·에너지 모니터링·환경 데이터 등에 적합합니다.

### 기본 패턴: TAG 테이블

```sql
CREATE TAG TABLE power_meter (
    meter_id  VARCHAR(32) PRIMARY KEY,
    time      DATETIME    BASETIME,
    kwh       DOUBLE,
    voltage   DOUBLE,
    current   DOUBLE
) METADATA (
    location  VARCHAR(64),
    phase     SHORT,
    rating_kw DOUBLE
);
```

### 시간 범위 집계

```sql
-- 1시간 단위 평균 전력 (최근 24시간)
SELECT meter_id,
       DATE_TRUNC('hour', time, 1) AS hour,
       AVG(kwh) AS avg_kwh,
       MAX(kwh) AS peak_kwh
FROM power_meter
WHERE time >= NOW - 86400000000000
GROUP BY meter_id, hour
ORDER BY meter_id, hour;
```

### 다중 해상도 저장 패턴

원시 데이터(고해상도)와 집계 데이터(저해상도)를 별도 테이블에 나누어 저장합니다.

```sql
-- 원시 데이터 (초 단위)
CREATE TAG TABLE power_raw (
    meter_id VARCHAR(32) PRIMARY KEY,
    time     DATETIME    BASETIME,
    kwh      DOUBLE
);

-- 1분 집계 (VOLATILE 또는 별도 TAG로 캐싱)
CREATE VOLATILE TABLE power_1min (
    key_id   VARCHAR(80) PRIMARY KEY,
    meter_id VARCHAR(32),
    ts       DATETIME,
    avg_kwh  DOUBLE,
    max_kwh  DOUBLE
);
```

### 시간대 처리

내부적으로 UTC 기준 시각을 저장하므로, 표시할 때 타임존 변환을 적용합니다.

```sql
-- UTC → KST 변환 (UTC+9)
SELECT meter_id,
       time + 32400000000000 AS time_kst,
       kwh
FROM power_meter
WHERE meter_id = 'MTR-001'
  AND time >= '2024-01-01 00:00:00';
```

<a id="distance-axis-modeling"></a>

## 거리축 모델링

거리(위치)를 기준 축으로 삼는 패턴으로, 파이프라인 검사·도로 센서·레이저 스캔 등에 적합합니다.

### 기본 패턴

```sql
CREATE TAG TABLE pipeline_thickness (
    pipe_id   VARCHAR(32) PRIMARY KEY,
    distance  DOUBLE      BASEDISTANCE,    -- 단위: 미터
    thickness DOUBLE,
    temp      DOUBLE
);
```

### 구간 데이터 조회

```sql
-- 파이프 ID별 0~50m 구간 데이터 조회
SELECT pipe_id, distance, thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
  AND distance BETWEEN 0.0 AND 50.0
ORDER BY distance;

-- 임계치 이하 구간 조회
SELECT pipe_id, distance, thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
  AND thickness < 8.0   -- 두께가 8mm 미만인 구간
ORDER BY distance;
```

### 거리 기반 집계

```sql
-- 10m 구간별 평균 두께
SELECT pipe_id,
       FLOOR(distance / 10.0) * 10 AS segment_start,
       AVG(thickness) AS avg_thickness,
       MIN(thickness) AS min_thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
GROUP BY pipe_id, FLOOR(distance / 10.0) * 10
ORDER BY segment_start;
```

### 시간 + 거리 복합 모델링

검사 시각과 위치를 함께 관리해야 하면 시간축 TAG 테이블에 거리 컬럼을 추가합니다.

```sql
-- 시간축 + 위치 정보 함께 저장
CREATE TAG TABLE inspection_data (
    inspector  VARCHAR(64) PRIMARY KEY,
    time       DATETIME    BASETIME,
    distance   DOUBLE,      -- 위치 컬럼 (축은 아님)
    thickness  DOUBLE,
    defect     SHORT
);

-- 특정 날짜·구간 조회
SELECT inspector, time, distance, thickness
FROM inspection_data
WHERE inspector = 'INSPECTOR-01'
  AND time BETWEEN '2024-01-01' AND '2024-01-02'
  AND distance BETWEEN 100.0 AND 200.0
ORDER BY time;
```

<a id="state-cache-status-modeling"></a>

## 상태·캐시 모델링

디바이스나 센서의 현재 상태를 실시간 조회하기 위한 캐시 모델링 패턴입니다.

### 최신 상태 캐시 패턴

VOLATILE 테이블로 각 디바이스의 현재 상태를 캐싱합니다.

```sql
-- 상태 캐시 (VOLATILE)
CREATE VOLATILE TABLE device_status (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);

-- 상태 이력 (TAG 또는 LOG)
CREATE TAG TABLE device_status_history (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE,
    status VARCHAR(16)
);
```

### 상태 업데이트 흐름

```sql
-- 새 계측값 수신 시:
-- 1. TAG 테이블에 이력 저장
INSERT INTO device_status_history VALUES ('DEV-01', NOW, 78.5, 'WARNING');

-- 2. VOLATILE 캐시 업데이트 (ON DUPLICATE KEY UPDATE)
INSERT INTO device_status VALUES ('DEV-01', 'WARNING', 78.5, NOW)
ON DUPLICATE KEY UPDATE SET status = 'WARNING', value = 78.5, updated_at = NOW;
```

### 대시보드 조회 패턴

```sql
-- 현재 ALARM 상태인 모든 디바이스
SELECT device_id, status, value, updated_at
FROM device_status
WHERE status IN ('ALARM', 'WARNING')
ORDER BY updated_at DESC;

-- 특정 디바이스의 최신 상태
SELECT device_id, status, value, updated_at
FROM device_status
WHERE device_id = 'DEV-01';
```

### 상태 정의 참조 패턴

상태 코드의 의미는 LOOKUP 테이블에서 관리합니다.

```sql
CREATE LOOKUP TABLE status_definition (
    code    VARCHAR(16) PRIMARY KEY,
    label   VARCHAR(64),
    color   VARCHAR(16),
    severity SHORT
);

INSERT INTO status_definition VALUES ('NORMAL', '정상', 'green', 0);
INSERT INTO status_definition VALUES ('WARNING', '경고', 'yellow', 1);
INSERT INTO status_definition VALUES ('ALARM', '알람', 'red', 2);

-- JOIN 조회
SELECT d.device_id, s.label, s.color, d.value
FROM device_status d
JOIN status_definition s ON d.status = s.code
ORDER BY s.severity DESC;
```

<a id="event-log-modeling-logs"></a>

## 이벤트·로그 모델링

시스템 이벤트, 알람, 감사 로그를 LOG 테이블로 모델링하는 패턴입니다.

### 계층적 이벤트 모델

```sql
-- 알람 이벤트 LOG 테이블
CREATE LOG TABLE alarm_event (
    severity    SHORT,          -- 1=INFO, 2=WARN, 3=ERROR, 4=CRITICAL
    category    VARCHAR(32),    -- 카테고리
    source      VARCHAR(64),    -- 발생 소스
    message     VARCHAR(512),
    src_ip      IPV4            -- 발생 IP (있는 경우)
);

-- 시스템 감사 LOG 테이블
CREATE LOG TABLE audit_log (
    user_id    VARCHAR(64),
    action     VARCHAR(32),    -- INSERT, UPDATE, DELETE, LOGIN 등
    target     VARCHAR(128),   -- 대상 테이블/리소스
    detail     TEXT,           -- 상세 내용 (전문 검색 대상)
    result     VARCHAR(8)      -- SUCCESS, FAILURE
);

CREATE KEYWORD INDEX idx_audit_detail ON audit_log(detail);
```

### 알람 집계 패턴

```sql
-- 최근 1시간 심각도별 알람 수
SELECT severity, COUNT(*) AS cnt
FROM alarm_event
WHERE _arrival_time >= NOW - 3600000000000
GROUP BY severity
ORDER BY severity DESC;

-- 소스별 알람 현황 (최근 24시간)
SELECT source, COUNT(*) AS total,
       SUM(CASE WHEN severity = 4 THEN 1 ELSE 0 END) AS critical_cnt
FROM alarm_event
WHERE _arrival_time >= NOW - 86400000000000
GROUP BY source
ORDER BY total DESC;
```

### 로그 레벨 필터 패턴

```sql
-- ERROR 이상 로그 조회 (최근 10분)
SELECT _arrival_time, source, message
FROM alarm_event
WHERE severity >= 3
  AND _arrival_time >= NOW - 600000000000
ORDER BY _arrival_time DESC
LIMIT 100;
```

### 전문 검색 패턴

```sql
-- 특정 키워드를 포함하는 감사 로그 조회
SELECT _arrival_time, user_id, action, target
FROM audit_log
WHERE detail SEARCH 'password'
  AND _arrival_time >= NOW - 86400000000000;
```

<a id="reference-master-modeling"></a>

## 참조·마스터 모델링

코드 테이블, 설비 마스터, 사용자 정보 등 참조 데이터를 LOOKUP 테이블로 모델링하는 패턴입니다.

### 계층적 코드 체계

```sql
-- 대분류 코드
CREATE LOOKUP TABLE category_main (
    code  VARCHAR(8)  PRIMARY KEY,
    label VARCHAR(64)
);

-- 중분류 코드 (대분류 참조)
CREATE LOOKUP TABLE category_sub (
    code      VARCHAR(16) PRIMARY KEY,
    main_code VARCHAR(8),
    label     VARCHAR(64)
);

CREATE INDEX idx_sub_main ON category_sub(main_code);
```

### 설비 계층 마스터

```sql
-- 공장 마스터
CREATE LOOKUP TABLE factory (
    factory_id VARCHAR(16) PRIMARY KEY,
    name       VARCHAR(64),
    location   VARCHAR(128)
);

-- 라인 마스터 (공장 참조)
CREATE LOOKUP TABLE production_line (
    line_id    VARCHAR(16) PRIMARY KEY,
    factory_id VARCHAR(16),
    name       VARCHAR(64)
);

-- 설비 마스터 (라인 참조)
CREATE LOOKUP TABLE equipment (
    equip_id   VARCHAR(32) PRIMARY KEY,
    line_id    VARCHAR(16),
    equip_name VARCHAR(128),
    equip_type VARCHAR(32),
    install_dt DATETIME
);

CREATE INDEX idx_equip_line ON equipment(line_id);
CREATE INDEX idx_equip_type ON equipment(equip_type);
```

### 마스터 조인 조회 패턴

계측 테이블에는 설비 식별자를 저장하고, 공장·라인·설비 이름 같은 속성은 LOOKUP 테이블에
한 번만 저장합니다. 조회할 때 계측 테이블의 시간 범위를 먼저 제한한 뒤 설비 식별자로
LOOKUP 테이블을 조인합니다. 실제 조인 구문과 실행 계획 확인 방법은
[JOIN·서브쿼리](/dbms/tag-table-usage/query-analysis/)을 참고하십시오.

<a id="persistent-temporary"></a>

## 영속·임시 혼합 패턴

영속 테이블(TAG, LOG, TRANSACTION, LOOKUP)과 임시 테이블(VOLATILE)을 조합해 성능과 데이터 무결성을 함께 확보하는 패턴입니다.

### 원본 + 집계 캐시 패턴

원본 데이터는 영속 테이블에, 집계 결과는 VOLATILE 테이블에 저장합니다.

```sql
-- 원본 데이터 (TAG, 영속)
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);

-- 집계 캐시 (VOLATILE, 임시)
CREATE VOLATILE TABLE sensor_recent_avg (
    key_id    VARCHAR(64) PRIMARY KEY,
    sensor_id VARCHAR(64),
    base_ts   DATETIME,
    avg_val   DOUBLE,
    max_val   DOUBLE,
    cnt       INTEGER
);
```

### 캐시 갱신 패턴

```sql
-- 주기적 집계 갱신 (1시간마다 실행)
DELETE FROM sensor_recent_avg;

INSERT INTO sensor_recent_avg
SELECT name AS key_id,
       name,
       MAX(DATE_TRUNC('hour', time, 1)) AS base_ts,
       AVG(value),
       MAX(value),
       COUNT(*)
FROM sensor_data
WHERE time >= NOW - 3600000000000 * 2  -- 최근 2시간 재계산
GROUP BY name;
```

`INSERT ... SELECT`에는 `ON DUPLICATE KEY UPDATE`를 붙이지 않습니다. 캐시를 재구성할 때는
기존 캐시를 삭제한 뒤 다시 적재합니다.

### 대시보드 조회 최적화

```sql
-- 캐시 우선 조회, 없으면 원본에서 계산
SELECT sensor_id, base_ts, avg_val, max_val
FROM sensor_recent_avg
WHERE base_ts >= NOW - 86400000000000
ORDER BY sensor_id, base_ts;
```

### 장애 복구

서버 재시작으로 VOLATILE 캐시가 소멸되면 원본 TAG 테이블에서 재계산합니다.

```sql
-- 캐시 재구성 (서버 재시작 후)
DELETE FROM sensor_recent_avg;

INSERT INTO sensor_recent_avg
SELECT name,
       name, MAX(DATE_TRUNC('hour', time, 1)), AVG(value), MAX(value), COUNT(*)
FROM sensor_data
WHERE time >= NOW - 86400000000000  -- 최근 24시간 재구성
GROUP BY name;
```

<a id="insert-update"></a>

## INSERT·UPDATE 패턴

이 절에서는 모델링에 필요한 쓰기 경로 선택만 정리합니다. 같은 DML 예제를 여러 장에서
반복하지 않도록 실제 구문은 각 테이블 장과 애플리케이션 입력 문서에서 다룹니다.

| 테이블 타입 | INSERT | UPDATE | DELETE | UPSERT |
|-----------|--------|--------|--------|--------|
| TAG | INSERT / Append API | O (태그/시간 조건) | O | X |
| LOG | INSERT / Append API | X | O (BEFORE/OLDEST/EXCEPT) | X |
| TRANSACTION | INSERT / SDK Append API | O (WHERE 유무 모두) | O | ON DUPLICATE KEY UPDATE |
| LOOKUP | INSERT / Append API | O (일반 조건식, PK 변경 제외) | O (일반 조건식 또는 전체 삭제) | ON DUPLICATE KEY UPDATE |
| VOLATILE | INSERT | O (by PK) | O | ON DUPLICATE KEY UPDATE |

지속적인 TAG·LOG 입력은 Append API, 서버가 읽을 수 있는 파일의 일괄 적재는
`LOAD DATA INFILE`, 클라이언트 파일은 `machloader`를 우선 검토합니다. 자세한 선택 기준은
[데이터 입력·적재·반출](/dbms/development-tools-integration/data-input-load-export/)을 참고하십시오.

<a id="join-metadata-design"></a>

## JOIN·메타데이터 설계

여러 테이블 타입을 조합할 때는 다음 원칙을 적용합니다.

1. 작은 테이블(LOOKUP)을 드라이빙 테이블 쪽에 배치합니다.
2. JOIN 조건 컬럼에 인덱스를 생성합니다.
3. WHERE 절로 레코드를 최대한 줄인 뒤 JOIN합니다.
4. TAG 속성을 함께 조회하는 목적이라면 별도 LOOKUP 대신 METADATA가 적합한지 검토합니다.

재현 가능한 조인 예제는 [TAG 조회와 분석](/dbms/tag-table-usage/query-analysis/)과
[LOOKUP 조회와 분석](/dbms/lookup-table-usage/query-analysis/)을 참고하십시오.

<a id="table-types-patterns-combined-type"></a>

## 복합 타입 조합 패턴

실제 운영 시스템에서 여러 테이블 타입을 조합하는 대표적인 설계 패턴입니다.

### 제조 설비 모니터링 시스템

```
┌─────────────────────────────────────────────────┐
│           설비 모니터링 시스템                     │
├──────────────┬──────────────┬───────────────────┤
│ TAG 테이블   │ LOG 테이블   │ LOOKUP 테이블      │
│ sensor_data  │ alarm_event  │ equipment_master   │
│ (계측값 이력) │ (알람 이벤트) │ (설비 기준 정보)   │
├──────────────┴──────────────┴───────────────────┤
│             VOLATILE 테이블                      │
│             sensor_latest (최신값 캐시)           │
└─────────────────────────────────────────────────┘
```

### 물류·주문 관리 시스템 (Standard Edition)

```
┌─────────────────────────────────────────────────┐
│              물류 관리 시스템                     │
├──────────────┬──────────────┬───────────────────┤
│ TRANSACTION 테이블   │ LOG 테이블   │ LOOKUP 테이블      │
│ orders       │ delivery_log │ product_master     │
│ (주문 관리)  │ (배송 이벤트) │ (제품 기준 정보)   │
│ UPDATE/DELETE│              │                   │
├──────────────┴──────────────┴───────────────────┤
│             VOLATILE 테이블                      │
│             order_status_cache (현재 상태 캐시)  │
└─────────────────────────────────────────────────┘
```

### 패턴 요약

| 역할 | 권장 타입 | 이유 |
|------|---------|------|
| 고빈도 계측값 이력 | TAG | Append API 고속 버퍼, 시계열 최적화 |
| 이벤트·알람 로그 | LOG | 추가 전용, 도착 시각 자동 |
| 관계형 업무 (UPDATE/DELETE) | TRANSACTION | SELECT/INSERT/UPDATE/DELETE 모두 지원 |
| 기준·코드 정보 | LOOKUP | PK 식별과 일반 조건식 UPDATE/DELETE, 영속 |
| 실시간 상태 캐시 | VOLATILE | 메모리 속도, UPSERT |

---

다음으로 읽을 내용:
- [SELECT의 GROUP BY와 집계](/dbms/reference/sql/syntax-dictionary-sql/select-syntax/)
- [운영 및 구성](/dbms/operations-configuration-recovery/)
