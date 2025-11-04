---
type: docs
title: '튜토리얼 4: 참조 데이터'
weight: 40
---

Machbase Lookup 테이블을 사용하여 참조 데이터와 마스터 데이터를 관리하는 방법을 학습합니다. 이 튜토리얼은 장치 레지스트리, 설정 테이블 및 차원 데이터를 유지 관리하는 방법을 보여줍니다.

## 시나리오

다음과 같은 IoT 플랫폼을 관리합니다:
- 여러 시설에 1,000개 이상의 센서 배포
- 장치 메타데이터 (위치, 유형, 소유자, 설치 날짜)
- 설정 세팅
- 심화된 쿼리를 위해 시계열 데이터와 JOIN 필요

**목표**: 거의 변경되지 않지만 자주 읽히는 장치 레지스트리 및 설정 데이터를 저장합니다.

## 학습 내용

- 참조 데이터를 위한 Lookup 테이블 생성
- 마스터/차원 데이터 저장
- 시계열 테이블과의 JOIN 연산
- 장치 메타데이터 관리
- 설정 테이블 유지 관리

## 사전 요구 사항

- Machbase 설치 및 실행
- machsql 클라이언트 연결
- 기본 SQL 지식
- 10분의 시간

## 단계 1: Lookup 테이블 생성

Lookup 테이블은 참조 데이터에 최적화된 디스크 기반 테이블입니다:

```sql
-- 장치 레지스트리
CREATE LOOKUP TABLE devices (
    device_id VARCHAR(50),
    device_name VARCHAR(100),
    device_type VARCHAR(50),
    location VARCHAR(200),
    facility VARCHAR(100),
    installed_date DATETIME,
    owner VARCHAR(100),
    status VARCHAR(20)
);

-- 장치 유형 카탈로그
CREATE LOOKUP TABLE device_types (
    type_code VARCHAR(50),
    type_name VARCHAR(100),
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    specifications VARCHAR(500)
);

-- 시설 정보
CREATE LOOKUP TABLE facilities (
    facility_code VARCHAR(50),
    facility_name VARCHAR(100),
    address VARCHAR(200),
    city VARCHAR(100),
    country VARCHAR(50),
    manager VARCHAR(100)
);
```

## 단계 2: 참조 데이터 삽입

```sql
-- 장치 유형 추가
INSERT INTO device_types VALUES (
    'TEMP-001', 'Temperature Sensor', 'Acme Corp', 'TempMaster 3000',
    'Range: -40 to 125C, Accuracy: ±0.5C'
);
INSERT INTO device_types VALUES (
    'HUM-001', 'Humidity Sensor', 'Acme Corp', 'HumidityPro 200',
    'Range: 0-100%, Accuracy: ±2%'
);
INSERT INTO device_types VALUES (
    'PRESS-001', 'Pressure Sensor', 'SensorTech', 'PressSense 500',
    'Range: 0-1000 PSI, Accuracy: ±1%'
);

-- 시설 추가
INSERT INTO facilities VALUES (
    'FAC-NY-01', 'New York Warehouse', '123 Industrial Ave', 'New York', 'USA', 'John Smith'
);
INSERT INTO facilities VALUES (
    'FAC-LA-01', 'Los Angeles Distribution Center', '456 Commerce Blvd', 'Los Angeles', 'USA', 'Jane Doe'
);
INSERT INTO facilities VALUES (
    'FAC-CHI-01', 'Chicago Manufacturing Plant', '789 Factory St', 'Chicago', 'USA', 'Bob Johnson'
);

-- 장치 추가
INSERT INTO devices VALUES (
    'sensor-ny-temp-001', 'NY Warehouse Zone A Temp', 'TEMP-001',
    'Zone A, Row 5, Shelf 3', 'FAC-NY-01',
    TO_DATE('2024-01-15', 'YYYY-MM-DD'), 'Facilities Team', 'ACTIVE'
);
INSERT INTO devices VALUES (
    'sensor-ny-temp-002', 'NY Warehouse Zone B Temp', 'TEMP-001',
    'Zone B, Row 2, Shelf 1', 'FAC-NY-01',
    TO_DATE('2024-01-15', 'YYYY-MM-DD'), 'Facilities Team', 'ACTIVE'
);
INSERT INTO devices VALUES (
    'sensor-la-hum-001', 'LA DC Humidity Monitor', 'HUM-001',
    'Main Floor, Section 3', 'FAC-LA-01',
    TO_DATE('2024-02-20', 'YYYY-MM-DD'), 'Operations', 'ACTIVE'
);
INSERT INTO devices VALUES (
    'sensor-chi-press-001', 'Chicago Line 1 Pressure', 'PRESS-001',
    'Production Line 1, Station 5', 'FAC-CHI-01',
    TO_DATE('2023-11-10', 'YYYY-MM-DD'), 'Manufacturing', 'MAINTENANCE'
);
```

## 단계 3: 참조 데이터 쿼리

```sql
-- 모든 활성 장치 조회
SELECT device_id, device_name, location, facility
FROM devices
WHERE status = 'ACTIVE';

-- 시설별 장치
SELECT device_id, device_name, device_type, location
FROM devices
WHERE facility = 'FAC-NY-01'
ORDER BY location;

-- 유지보수가 필요한 장치
SELECT device_id, device_name, facility, installed_date
FROM devices
WHERE status = 'MAINTENANCE';

-- 1년 이상 된 장치
SELECT device_id, device_name, installed_date, facility
FROM devices
WHERE installed_date < NOW - INTERVAL '365' DAY
ORDER BY installed_date;
```

## 단계 4: 참조 데이터 업데이트

Lookup 테이블은 UPDATE 및 DELETE를 지원합니다:

```sql
-- 장치 상태 업데이트
UPDATE devices
SET status = 'ACTIVE'
WHERE device_id = 'sensor-chi-press-001';

-- 장치 위치 변경
UPDATE devices
SET location = 'Zone C, Row 1, Shelf 2'
WHERE device_id = 'sensor-ny-temp-001';

-- 시설 관리자 업데이트
UPDATE facilities
SET manager = 'Sarah Williams'
WHERE facility_code = 'FAC-NY-01';

-- 장치 폐기
UPDATE devices
SET status = 'DECOMMISSIONED'
WHERE device_id = 'sensor-la-hum-001';
```

## 단계 5: 시계열 데이터와 JOIN

참조 데이터를 센서 측정값과 결합:

```sql
-- 먼저 센서 데이터 테이블 생성 (튜토리얼 1에서)
CREATE TAGDATA TABLE sensor_readings (
    sensor_id VARCHAR(50) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 샘플 측정값 삽입
INSERT INTO sensor_readings VALUES ('sensor-ny-temp-001', NOW, 22.5);
INSERT INTO sensor_readings VALUES ('sensor-ny-temp-002', NOW, 23.1);
INSERT INTO sensor_readings VALUES ('sensor-la-hum-001', NOW, 55.2);

-- 센서 데이터를 장치 정보와 JOIN
SELECT
    sr.sensor_id,
    d.device_name,
    d.location,
    d.facility,
    sr.value,
    sr.time
FROM sensor_readings sr
JOIN devices d ON sr.sensor_id = d.device_id
DURATION 1 HOUR;

-- 전체 컨텍스트와 함께 측정값 조회
SELECT
    sr.sensor_id,
    d.device_name,
    d.location,
    f.facility_name,
    f.city,
    dt.type_name,
    dt.manufacturer,
    sr.value
FROM sensor_readings sr
JOIN devices d ON sr.sensor_id = d.device_id
JOIN facilities f ON d.facility = f.facility_code
JOIN device_types dt ON d.device_type = dt.type_code
DURATION 1 HOUR;
```

## 단계 6: 설정 테이블 생성

애플리케이션 설정 저장:

```sql
CREATE LOOKUP TABLE system_config (
    config_key VARCHAR(100),
    config_value VARCHAR(500),
    config_type VARCHAR(50),
    description VARCHAR(500),
    updated_at DATETIME,
    updated_by VARCHAR(100)
);

-- 설정 추가
INSERT INTO system_config VALUES (
    'alert.temperature.max', '80.0', 'THRESHOLD',
    'Maximum temperature threshold in Celsius',
    NOW, 'admin'
);
INSERT INTO system_config VALUES (
    'alert.humidity.max', '75.0', 'THRESHOLD',
    'Maximum humidity threshold percentage',
    NOW, 'admin'
);
INSERT INTO system_config VALUES (
    'retention.sensor_data.days', '90', 'RETENTION',
    'Days to retain sensor data',
    NOW, 'admin'
);
INSERT INTO system_config VALUES (
    'alert.email', 'ops@company.com', 'CONTACT',
    'Alert notification email address',
    NOW, 'admin'
);

-- 설정 쿼리
SELECT config_key, config_value
FROM system_config
WHERE config_type = 'THRESHOLD';

-- 설정 업데이트
UPDATE system_config
SET config_value = '85.0',
    updated_at = NOW,
    updated_by = 'supervisor'
WHERE config_key = 'alert.temperature.max';
```

## 단계 7: 장치 생명주기 관리

장치 생명주기 추적:

```sql
CREATE LOOKUP TABLE device_lifecycle (
    event_id INTEGER,
    device_id VARCHAR(50),
    event_type VARCHAR(50),
    event_date DATETIME,
    performed_by VARCHAR(100),
    notes VARCHAR(500)
);

-- 생명주기 이벤트 기록
INSERT INTO device_lifecycle VALUES (
    1, 'sensor-ny-temp-001', 'INSTALLED',
    TO_DATE('2024-01-15', 'YYYY-MM-DD'), 'Install Team', 'Initial installation'
);
INSERT INTO device_lifecycle VALUES (
    2, 'sensor-chi-press-001', 'MAINTENANCE',
    TO_DATE('2025-09-15', 'YYYY-MM-DD'), 'Maintenance Team', 'Scheduled maintenance'
);
INSERT INTO device_lifecycle VALUES (
    3, 'sensor-chi-press-001', 'CALIBRATED',
    TO_DATE('2025-09-15', 'YYYY-MM-DD'), 'Maintenance Team', 'Recalibrated after maintenance'
);

-- 장치 이력
SELECT
    d.device_id,
    d.device_name,
    dl.event_type,
    dl.event_date,
    dl.performed_by,
    dl.notes
FROM devices d
JOIN device_lifecycle dl ON d.device_id = dl.device_id
WHERE d.device_id = 'sensor-chi-press-001'
ORDER BY dl.event_date DESC;
```

## 직접 해보기

### 연습 1: 새 시설 추가

새 시설과 장치를 추가합니다:

<details>
<summary>해답</summary>

```sql
-- 시설 추가
INSERT INTO facilities VALUES (
    'FAC-SEA-01', 'Seattle Tech Center', '999 Innovation Way',
    'Seattle', 'USA', 'Mike Chen'
);

-- 새 시설에 장치 추가
INSERT INTO devices VALUES (
    'sensor-sea-temp-001', 'Seattle Server Room Temp', 'TEMP-001',
    'Server Room A, Rack 1', 'FAC-SEA-01',
    NOW, 'IT Team', 'ACTIVE'
);
INSERT INTO devices VALUES (
    'sensor-sea-hum-001', 'Seattle Server Room Humidity', 'HUM-001',
    'Server Room A, Rack 1', 'FAC-SEA-01',
    NOW, 'IT Team', 'ACTIVE'
);
```
</details>

### 연습 2: 유지보수 예정 장치 찾기

6개월 전에 설치된 장치를 찾는 쿼리를 생성합니다:

<details>
<summary>해답</summary>

```sql
SELECT
    d.device_id,
    d.device_name,
    d.installed_date,
    FLOOR((NOW - d.installed_date) / 86400) as days_installed,
    f.facility_name
FROM devices d
JOIN facilities f ON d.facility = f.facility_code
WHERE d.installed_date < NOW - INTERVAL '180' DAY
  AND d.status = 'ACTIVE'
ORDER BY d.installed_date ASC;
```
</details>

### 연습 3: 장치 인벤토리 보고서

시설 및 장치 유형별 요약 보고서를 생성합니다:

<details>
<summary>해답</summary>

```sql
SELECT
    f.facility_name,
    dt.type_name,
    COUNT(*) as device_count,
    SUM(CASE WHEN d.status = 'ACTIVE' THEN 1 ELSE 0 END) as active_count,
    SUM(CASE WHEN d.status = 'MAINTENANCE' THEN 1 ELSE 0 END) as maintenance_count
FROM devices d
JOIN facilities f ON d.facility = f.facility_code
JOIN device_types dt ON d.device_type = dt.type_code
GROUP BY f.facility_name, dt.type_name
ORDER BY f.facility_name, dt.type_name;
```
</details>

## 실제 패턴

### 패턴: 계층적 참조 데이터

```sql
-- 조직 계층 구조
CREATE LOOKUP TABLE organizations (
    org_id VARCHAR(50),
    org_name VARCHAR(100),
    parent_org_id VARCHAR(50),
    org_level INTEGER
);

-- 지역 → 시설 → 구역 계층
INSERT INTO organizations VALUES ('ORG-USA', 'USA Operations', NULL, 1);
INSERT INTO organizations VALUES ('ORG-USA-EAST', 'East Region', 'ORG-USA', 2);
INSERT INTO organizations VALUES ('FAC-NY-01', 'NY Warehouse', 'ORG-USA-EAST', 3);

-- 계층과 함께 쿼리
SELECT
    o1.org_name as region,
    o2.org_name as facility,
    COUNT(d.device_id) as device_count
FROM organizations o1
JOIN organizations o2 ON o2.parent_org_id = o1.org_id
JOIN devices d ON d.facility = o2.org_id
WHERE o1.org_level = 2
GROUP BY o1.org_name, o2.org_name;
```

### 패턴: 사용자 권한

```sql
CREATE LOOKUP TABLE user_permissions (
    user_id VARCHAR(50),
    user_name VARCHAR(100),
    role VARCHAR(50),
    facility_access VARCHAR(50),
    permissions VARCHAR(200)
);

-- 액세스 권한 부여
INSERT INTO user_permissions VALUES (
    'user123', 'John Smith', 'FACILITY_MANAGER',
    'FAC-NY-01', 'READ,WRITE,CONFIGURE'
);

-- 권한 확인
SELECT permissions
FROM user_permissions
WHERE user_id = 'user123'
  AND facility_access = 'FAC-NY-01';
```

### 패턴: 심화된 분석

```sql
-- 분석을 위해 전체 컨텍스트와 함께 센서 측정값 조회
SELECT
    f.city,
    dt.manufacturer,
    AVG(sr.value) as avg_reading,
    COUNT(*) as reading_count
FROM sensor_readings sr
JOIN devices d ON sr.sensor_id = d.device_id
JOIN facilities f ON d.facility = f.facility_code
JOIN device_types dt ON d.device_type = dt.type_code
WHERE d.status = 'ACTIVE'
DURATION 24 HOUR
GROUP BY f.city, dt.manufacturer;
```

## 성능 팁

1. **자주 쿼리되는 컬럼에 인덱스**: 일반적인 조회 키에 인덱스 생성
2. **데이터를 최신 상태로 유지**: 정기적으로 참조 데이터 업데이트
3. **적절한 정규화**: 더 깔끔한 설계를 위해 참조 테이블 분리
4. **중소 규모 데이터셋에 사용**: Lookup 테이블은 <100만 행에서 가장 잘 작동

## Lookup vs Volatile 테이블

| 기능 | Lookup 테이블 | Volatile 테이블 |
|---------|-------------|----------------|
| **저장소** | 디스크 | 메모리 |
| **지속성** | 예 | 아니오 |
| **속도** | 느림 | 빠름 |
| **사용 사례** | 참조 데이터 | 실시간 캐시 |
| **데이터 볼륨** | 중-대형 | 소형 |

## 달성한 내용

✓ 참조 데이터를 위한 Lookup 테이블 생성
✓ 장치 레지스트리 및 메타데이터 저장
✓ 시계열 데이터와의 JOIN 연산 수행
✓ 설정 테이블 관리
✓ 장치 생명주기 추적
✓ 심화된 분석 쿼리 구축

## 다음 단계

- **핵심 개념**: [테이블 타입 개요](../../core-concepts/table-types-overview/) - 심화 학습
- **일반 작업**: [사용자 관리](../../common-tasks/user-management/) - 액세스 제어
- **레퍼런스**: [Lookup 테이블](../../table-types/lookup-tables/) - 고급 기능

## 핵심 요점

1. **Lookup 테이블**은 참조/마스터 데이터에 완벽함
2. **디스크 기반** 저장소는 데이터 지속성 보장
3. **JOIN 연산**은 컨텍스트로 시계열 데이터를 풍부하게 함
4. **UPDATE/DELETE**는 데이터 유지 관리에 지원됨
5. **장치 레지스트리**, **설정** 및 **차원 테이블**에 사용
6. **Tag/Log 테이블**과 결합하여 강력한 분석 수행

---

**축하합니다!** 네 가지 튜토리얼을 모두 완료했습니다! 이제 Machbase의 네 가지 테이블 타입을 모두 이해했습니다. [핵심 개념](../../core-concepts/) 섹션을 탐색하여 지식을 더 깊게 하세요!
