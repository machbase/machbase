---
title: '9.6 인덱스와 성능'
weight: 60
toc: true
---
LOOKUP/VOLATILE 테이블의 인덱스 구조와 성능 튜닝을 다룬다.


<a id="index-tuning-lookup-volatile"></a>

## LOOKUP/VOLATILE 인덱스 튜닝

LOOKUP 테이블과 VOLATILE 테이블은 모두 PRIMARY KEY에 Red-Black 트리 인덱스가 자동 생성된다. 필요하면 non-PK 컬럼에도 Red-Black 보조 인덱스를 추가할 수 있다.

### LOOKUP 테이블 인덱스

#### PK 자동 Red-Black 트리 인덱스

LOOKUP 테이블을 생성하면 PRIMARY KEY 컬럼에 Red-Black 트리 인덱스가 자동으로 생성된다. 소규모 기준 정보를 키로 빠르게 조회하는 패턴에 최적화되어 있다.

```sql
CREATE LOOKUP TABLE device_master (
    device_id   VARCHAR(64) PRIMARY KEY,  -- Red-Black 트리 자동 생성
    device_name VARCHAR(128),
    location    VARCHAR(256),
    category    VARCHAR(32)
);
```

```sql
-- PK 조회: Red-Black 트리 인덱스 사용, 빠름
SELECT * FROM device_master WHERE device_id = 'DEV-1234';

-- JOIN 시 PK 기준 조회: 효율적
SELECT l.device_id, l.level, d.location
FROM device_log l, device_master d
WHERE l.device_id = d.device_id
DURATION 1 HOUR;
```

#### non-PK 컬럼 보조 인덱스

non-PK 컬럼에도 Red-Black 보조 인덱스를 생성할 수 있다. 보조 인덱스가 없는 컬럼으로 필터링하면 테이블 전체를 순차 스캔한다.

```sql
-- 자주 필터링하는 non-PK 컬럼에 보조 인덱스 생성
CREATE INDEX idx_device_master_location ON device_master(location);

SELECT * FROM device_master WHERE location = 'Seoul';

-- 인덱스가 없는 컬럼은 전체 스캔 가능
SELECT * FROM device_master WHERE category = 'temperature';
```

보조 인덱스는 조회를 빠르게 하지만 갱신 비용과 메모리 사용량이 늘어난다. 자주 사용하는 조건 컬럼에만 생성한다.

#### LOOKUP 테이블 사용 가이드라인

```
권장 데이터 규모: 수천 ~ 수만 건
PK 조회 응답 시간: O(log n), 매우 빠름
non-PK 조회 응답 시간: 보조 인덱스가 있으면 O(log n), 없으면 O(n)
```

| 사용 패턴 | 적합성 |
|----------|-------|
| device_id로 장치 정보 조회 | 적합 (PK 사용) |
| location으로 장치 목록 검색 | 보조 인덱스 생성 시 적합 |
| 소수의 기준 코드 테이블 | 적합 |
| 수십만 건 이상의 기준 정보 | 부적합 → LOG 테이블 + 인덱스 검토 |

### VOLATILE 테이블 인덱스

#### PK 자동 Red-Black 트리 인덱스

VOLATILE 테이블은 메모리 기반이며, PRIMARY KEY 컬럼에 Red-Black 트리 인덱스가 자동 생성된다. 모든 작업이 메모리에서 수행되므로 삽입·조회·수정·삭제 모두 매우 빠르다.

```sql
CREATE VOLATILE TABLE device_status (
    device_id   INTEGER PRIMARY KEY,  -- Red-Black 트리 자동 생성
    status      VARCHAR(20),
    last_updated DATETIME,
    error_count INTEGER
);
```

```sql
-- PK 조회: 인메모리 Red-Black 트리 사용, 매우 빠름 O(log n)
SELECT * FROM device_status WHERE device_id = 101;

-- PK 기준 업데이트: 빠름
UPDATE device_status SET status = 'RUNNING' WHERE device_id = 101;

-- PK 기준 삭제: 빠름
DELETE FROM device_status WHERE device_id = 101;
```

#### non-PK 컬럼 보조 인덱스

VOLATILE 테이블도 non-PK 컬럼에 Red-Black 보조 인덱스를 생성할 수 있다. 보조 인덱스가 없으면 전체 메모리 스캔이 발생하지만, 데이터가 메모리에 있으므로 디스크 기반 테이블보다 부담이 작다.

```sql
CREATE INDEX idx_device_status_status ON device_status(status);

SELECT * FROM device_status WHERE status = 'ERROR';
```

VOLATILE 테이블은 **현재 상태를 보관하는 소규모 인메모리 테이블**로 사용하는 것이 목적에 맞다. 반복 조회하는 non-PK 조건에만 보조 인덱스를 생성한다.

#### VOLATILE 테이블 특성 요약

| 특성 | 내용 |
|-----|------|
| 인덱스 구조 | Red-Black 트리 (PK 자동) |
| 저장 위치 | 메모리 (재시작 시 데이터 소멸) |
| PK 조회 복잡도 | O(log n) |
| non-PK 조회 | 보조 인덱스 또는 전체 메모리 스캔 |
| 추가 인덱스 | Red-Black 보조 인덱스 생성 가능 |
| 적합한 규모 | 수만 건 이하 |

### 대용량 기준 정보가 필요한 경우

LOOKUP 테이블의 크기와 보조 인덱스 갱신 비용 때문에 다음 시나리오에서는 대안을 고려한다.

**시나리오**: 수십만 건의 장치 기준 정보를 저장하고, 여러 컬럼으로 필터링해야 하는 경우

```sql
-- 대안: LOG 테이블 + LSM/BITMAP 인덱스
CREATE TABLE device_master_log (
    device_id   VARCHAR(64),
    device_name VARCHAR(128),
    location    VARCHAR(256),
    category    VARCHAR(32),
    updated_at  DATETIME
);

-- non-PK 컬럼에 인덱스 생성 가능
CREATE INDEX idx_location ON device_master_log (location);
CREATE INDEX idx_category ON device_master_log (category) INDEX_TYPE BITMAP;
```

단, LOG 테이블은 Append 전용이므로 기준 정보 갱신 패턴에 맞게 설계해야 한다.

### 핵심 정리

| 항목 | LOOKUP | VOLATILE |
|------|--------|---------|
| 기본 인덱스 | Red-Black 트리 (PK) | Red-Black 트리 (PK) |
| 추가 인덱스 생성 | Red-Black 보조 인덱스 가능 | Red-Black 보조 인덱스 가능 |
| non-PK 조회 | 보조 인덱스 또는 전체 스캔 | 보조 인덱스 또는 전체 메모리 스캔 |
| 데이터 지속성 | 영구 | 재시작 시 소멸 |
| 권장 규모 | 수만 건 이하 | 수만 건 이하 |
| 최적화 방향 | PK와 반복 조회 컬럼에만 인덱스 설계 | 소규모 유지, 반복 조회 컬럼에만 인덱스 설계 |

<a id="original-85-lookup-indexes"></a>

## Lookup 인덱스 생성 및 관리


Lookup 테이블은 RED-BLACK 인덱스를 지원한다. `INDEX_TYPE LSM`을
지정해도 RED-BLACK 인덱스가 생성된다. `KEYWORD` 인덱스는 LOG 테이블에서만 사용할 수 있다.

```sql
CREATE LOOKUP TABLE lookup_table (code INTEGER PRIMARY KEY, name VARCHAR(20));
CREATE INDEX idx_lookup_name ON lookup_table(name) INDEX_TYPE REDBLACK;
```

<a id="index-strategy-lookup"></a>

## 인덱스 전략

LOOKUP 테이블은 PRIMARY KEY에 Red-Black Tree 인덱스가 자동 생성된다. 추가 조회 조건이 있으면 보조 인덱스를 생성한다.

### 자동 PRIMARY KEY 인덱스

PRIMARY KEY 컬럼에는 인덱스가 자동 생성된다. 별도 `CREATE INDEX`가 필요 없다.

```sql
CREATE LOOKUP TABLE country_code (
    code   VARCHAR(4)  PRIMARY KEY,  -- 자동 인덱스
    name   VARCHAR(64),
    region VARCHAR(32)
);

-- PK 기반 조회 (인덱스 사용)
SELECT name FROM country_code WHERE code = 'KR';
```

### 보조 인덱스

PRIMARY KEY 외의 컬럼으로 자주 조회하면 보조 인덱스를 생성한다.

```sql
CREATE LOOKUP TABLE equipment_master (
    equip_id   INTEGER     PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    dept       VARCHAR(64),
    status     VARCHAR(16)
);

-- 부서별 조회용 인덱스
CREATE INDEX idx_equip_dept ON equipment_master(dept);

-- 상태 필터용 인덱스
CREATE INDEX idx_equip_status ON equipment_master(status);
```

### 인덱스 조회 예시

```sql
-- PK 조회 (자동 인덱스)
SELECT * FROM equipment_master WHERE equip_id = 42;

-- 보조 인덱스 활용
SELECT equip_id, equip_name FROM equipment_master WHERE dept = '생산팀';
SELECT equip_id, location FROM equipment_master WHERE status = 'ACTIVE';
```

### 주의사항

- 수만 건 이하의 소규모 테이블은 인덱스 없이도 빠르게 조회할 수 있다.
- 인덱스는 INSERT/UPDATE 성능에 영향을 줄 수 있으므로 필요한 것만 생성한다.
