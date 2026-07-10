---
title: '9.9 활용 패턴과 시나리오'
weight: 90
toc: true
---
LOOKUP 테이블의 활용 패턴과 시나리오를 다룬다.


<a id="use-cases-lookup"></a>

## 활용 사례

LOOKUP 테이블은 다음과 같은 데이터를 저장하는 데 적합하다.

<a id="lookup-pattern-data-types"></a>

## 적합한 데이터 유형

| 유형 | 예시 |
|------|------|
| 코드 테이블 | 국가 코드, 언어 코드, 상태 코드 |
| 기준 정보 | 설비 목록, 제품 분류, 부서 정보 |
| 실시간 갱신 참조 | 환율 테이블, 임계값 설정 |
| 태그 메타데이터 대체 | 센서 정보 (소규모) |

<a id="lookup-pattern-code-table"></a>

## 코드 테이블

```sql
CREATE LOOKUP TABLE country_code (
    code   VARCHAR(4)   PRIMARY KEY,
    name   VARCHAR(64),
    region VARCHAR(32)
);

INSERT INTO country_code VALUES ('KR', '대한민국', 'Asia');
INSERT INTO country_code VALUES ('US', '미국', 'America');
UPDATE country_code SET name = 'United States' WHERE code = 'US';
```

상태 코드나 알람 코드도 같은 방식으로 관리한다.

```sql
CREATE LOOKUP TABLE status_code (
    code  VARCHAR(16) PRIMARY KEY,
    label VARCHAR(64),
    color VARCHAR(16)
);

SELECT e.event_time, e.device_id, c.label
FROM event_log e
JOIN status_code c ON e.status = c.code;
```

<a id="lookup-pattern-equipment-master"></a>

## 설비 마스터

```sql
CREATE LOOKUP TABLE equipment_master (
    equip_id   VARCHAR(32) PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    dept       VARCHAR(64),
    install_dt DATETIME
);
```

TAG 테이블의 센서 데이터와 JOIN하면 위치, 부서, 단위 같은 기준 정보를 함께 조회할 수 있다.

```sql
SELECT d.name, m.location, m.dept, d.time, d.value
FROM sensor_data d
JOIN equipment_master m ON d.name = m.equip_id
WHERE m.dept = 'Production'
  AND d.time >= NOW - 3600000000000;
```

<a id="lookup-pattern-threshold"></a>

## 임계값 설정

```sql
CREATE LOOKUP TABLE threshold_config (
    sensor_name VARCHAR(64) PRIMARY KEY,
    low_limit   DOUBLE,
    high_limit  DOUBLE,
    alert_level SHORT
);

-- 실시간 임계값 변경
UPDATE threshold_config SET high_limit = 85.0 WHERE sensor_name = 'TEMP-01';
```

임계값 테이블은 TAG 데이터와 결합해 알람 조건을 판단하는 데 사용한다.

```sql
SELECT s.name, s.time, s.value, t.high_limit
FROM sensor_data s
JOIN threshold_config t ON s.name = t.sensor_name
WHERE s.time >= NOW - 60000000000
  AND s.value > t.high_limit;
```

<a id="lookup-pattern-sequence-master"></a>

## SEQUENCE 기반 이력 번호

작은 규모의 관리 이력이나 운영 이벤트에 순번이 필요하면 SEQUENCE 컬럼을 사용할 수 있다.

```sql
CREATE LOOKUP TABLE operation_note (
    seq        LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    target_id  VARCHAR(64),
    note       VARCHAR(512),
    created_at DATETIME
);

INSERT INTO operation_note
VALUES (NEXTVAL(seq), 'TEMP-01', 'threshold changed', NOW);
```

대량 원본 이력은 LOOKUP보다 LOG 테이블에 저장한다.

<a id="lookup-pattern-not-suitable"></a>

## 부적합한 경우

- 건수가 수백만 건을 초과하는 대용량 데이터 → RDB 테이블 권장
- UPDATE 불필요한 추가 전용 이력 → LOG 테이블 권장
- 센서 계측값 → TAG 테이블 권장
- 재시작 후 사라져도 되는 최신 상태 캐시 → VOLATILE 테이블 권장
