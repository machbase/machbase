---
title: '9.6 인덱스와 성능'
weight: 60
toc: true
---
LOOKUP/VOLATILE 테이블의 인덱스 구조와 성능 튜닝을 다룹니다.


<a id="index-tuning-lookup-volatile"></a>
<a id="original-85-lookup-indexes"></a>
<a id="index-strategy-lookup"></a>

## LOOKUP/VOLATILE 인덱스 튜닝

LOOKUP 테이블과 VOLATILE 테이블은 모두 PRIMARY KEY에 Red-Black 트리 인덱스가 자동 생성됩니다.
LOOKUP의 전체 행과 인덱스는 SQL 조회 중 메모리에 상주합니다. 필요하면 non-PK 컬럼에도
Red-Black 보조 인덱스를 추가할 수 있습니다.

### LOOKUP 테이블 인덱스

#### PK 자동 Red-Black 트리 인덱스

LOOKUP 테이블을 생성하면 PRIMARY KEY 컬럼에 Red-Black 트리 인덱스가 자동으로 생성됩니다.
인덱스 항목은 해당 key의 전체 컬럼 값이 들어 있는 메모리 행을 가리킵니다. 따라서 영속
테이블이지만 조회 실행 경로는 메모리 기반이며, 소규모 기준 정보를 key로 반복 조회하는
패턴에 최적화되어 있습니다.

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

non-PK 컬럼에도 Red-Black 보조 인덱스를 생성할 수 있습니다. 보조 인덱스가 없는 컬럼으로 필터링하면 테이블 전체를 순차 스캔합니다.

```sql
-- 자주 필터링하는 non-PK 컬럼에 보조 인덱스 생성
CREATE INDEX idx_device_master_location ON device_master(location);

SELECT * FROM device_master WHERE location = 'Seoul';

-- 인덱스가 없는 컬럼은 전체 스캔 가능
SELECT * FROM device_master WHERE category = 'temperature';
```

보조 인덱스는 조회를 빠르게 하지만 갱신 비용과 메모리 사용량이 늘어납니다. 자주 사용하는 조건 컬럼에만 생성합니다.

#### LOOKUP 테이블 사용 가이드라인

Primary key와 Red-Black 보조 인덱스의 조회 비용은 트리 크기에 따라 증가하고, 인덱스가 없는
조건은 메모리에 적재된 전체 행을 스캔합니다. 행 수만으로 사용 한계를 정하지 말고 전체 행의
실제 크기, 가변 길이 값, 인덱스 수, 조회와 갱신 비율을 같은 워크로드로 측정합니다. 서버
기동 시 영속 데이터를 모두 읽어 메모리 행과 인덱스를 구성하므로 기동 시간도 함께 확인합니다.

| 사용 패턴 | 적합성 |
|----------|-------|
| device_id로 장치 정보 조회 | 적합 (PK 사용) |
| location으로 장치 목록 검색 | 보조 인덱스 생성 시 적합 |
| 소수의 기준 코드 테이블 | 적합 |
| 전체 행이 서버 메모리에 들어가지 않는 대규모 기준 정보 | RDB 테이블 검토 |
| 관계형 트랜잭션이 필요한 기준 정보 | RDB 테이블 검토 |

### VOLATILE 테이블 인덱스

#### PK 자동 Red-Black 트리 인덱스

VOLATILE 테이블은 메모리 기반이며, PRIMARY KEY 컬럼에 Red-Black 트리 인덱스가 자동 생성됩니다. 모든 작업이 메모리에서 수행되므로 삽입·조회·수정·삭제 모두 매우 빠릅니다.

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

VOLATILE 테이블도 non-PK 컬럼에 Red-Black 보조 인덱스를 생성할 수 있습니다. 보조 인덱스가 없으면 전체 메모리 스캔이 발생하지만, 데이터가 메모리에 있으므로 디스크 기반 테이블보다 부담이 작습니다.

```sql
CREATE INDEX idx_device_status_status ON device_status(status);

SELECT * FROM device_status WHERE status = 'ERROR';
```

VOLATILE 테이블은 **현재 상태를 보관하는 소규모 인메모리 테이블**로 사용하는 것이 목적에 맞습니다. 반복 조회하는 non-PK 조건에만 보조 인덱스를 생성합니다.

#### VOLATILE 테이블 특성 요약

| 특성 | 내용 |
|-----|------|
| 인덱스 구조 | Red-Black 트리 (PK 자동) |
| 저장 위치 | 메모리 (재시작 시 데이터 소멸) |
| PK 조회 복잡도 | O(log n) |
| non-PK 조회 | 보조 인덱스 또는 전체 메모리 스캔 |
| 추가 인덱스 | Red-Black 보조 인덱스 생성 가능 |
| 규모 판단 | 메모리 사용량과 재시작 시 재구성 비용 측정 |

### 대용량 기준 정보가 필요한 경우

LOOKUP 테이블의 크기와 보조 인덱스 갱신 비용 때문에 다음 시나리오에서는 대안을 고려합니다.

**시나리오**: 장치 기준 정보를 여러 컬럼으로 필터링하고 변경 이력도 함께 보존해야 하는 경우

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

단, LOG 테이블은 Append 전용이므로 기준 정보 갱신 패턴에 맞게 설계해야 합니다.

### 핵심 정리

| 항목 | LOOKUP | VOLATILE |
|------|--------|---------|
| 기본 인덱스 | Red-Black 트리 (PK) | Red-Black 트리 (PK) |
| 추가 인덱스 생성 | Red-Black 보조 인덱스 가능 | Red-Black 보조 인덱스 가능 |
| non-PK 조회 | 보조 인덱스 또는 전체 스캔 | 보조 인덱스 또는 전체 메모리 스캔 |
| 조회 데이터 위치 | 전체 행이 메모리에 상주 | 전체 행이 메모리에 상주 |
| 데이터 지속성 | 영속 저장본에서 재구성 | 재시작 시 소멸 |
| 규모 판단 | 행·인덱스 메모리, 기동 시간과 갱신 부하 측정 | 메모리와 재구성 비용 측정 |
| 최적화 방향 | PK와 반복 조회 컬럼에만 인덱스 설계 | 소규모 유지, 반복 조회 컬럼에만 인덱스 설계 |
