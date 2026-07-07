---
type: docs
title: 'LOOKUP/VOLATILE 인덱스 튜닝'
weight: 30
---

LOOKUP 테이블과 VOLATILE 테이블은 모두 PRIMARY KEY에 자동으로 인덱스가 생성됩니다. 각 테이블의 인덱스 특성과 한계를 이해하면 적절한 데이터 모델링 결정을 내릴 수 있습니다.

## LOOKUP 테이블 인덱스

### PK 자동 B-Tree 인덱스

LOOKUP 테이블을 생성하면 PRIMARY KEY 컬럼에 B-Tree 인덱스가 자동으로 생성됩니다. 소규모 기준 정보를 키로 빠르게 조회하는 패턴에 최적화되어 있습니다.

```sql
CREATE LOOKUP TABLE device_master (
    device_id   VARCHAR(64) PRIMARY KEY,  -- B-Tree 인덱스 자동 생성
    device_name VARCHAR(128),
    location    VARCHAR(256),
    category    VARCHAR(32)
);
```

```sql
-- PK 조회: B-Tree 인덱스 사용, 빠름
SELECT * FROM device_master WHERE device_id = 'DEV-1234';

-- JOIN 시 PK 기준 조회: 효율적
SELECT l.device_id, l.level, d.location
FROM device_log l, device_master d
WHERE l.device_id = d.device_id
DURATION 1 HOUR;
```

### non-PK 컬럼 조회는 전체 스캔

LOOKUP 테이블에는 PK 이외의 컬럼에 추가 인덱스를 생성할 수 없습니다. PK가 아닌 컬럼으로 필터링하면 테이블 전체를 순차 스캔합니다.

```sql
-- 전체 스캔: location 컬럼에 인덱스 없음
SELECT * FROM device_master WHERE location = 'Seoul';

-- 전체 스캔: category 컬럼에 인덱스 없음
SELECT * FROM device_master WHERE category = 'temperature';
```

이 때문에 LOOKUP 테이블은 **데이터 크기를 제한**하는 것이 중요합니다. 수십만 건 이상의 기준 정보를 LOOKUP 테이블에 저장하고 non-PK 컬럼으로 자주 필터링한다면 성능 문제가 발생할 수 있습니다.

### LOOKUP 테이블 사용 가이드라인

```
권장 데이터 규모: 수천 ~ 수만 건
PK 조회 응답 시간: O(log n), 매우 빠름
non-PK 조회 응답 시간: O(n), 건수에 비례
```

| 사용 패턴 | 적합성 |
|----------|-------|
| device_id로 장치 정보 조회 | 적합 (PK 사용) |
| location으로 장치 목록 검색 | 부적합 (전체 스캔) |
| 소수의 기준 코드 테이블 | 적합 |
| 수십만 건 이상의 기준 정보 | 부적합 → LOG 테이블 + 인덱스 검토 |

## VOLATILE 테이블 인덱스

### PK 자동 Red-Black 트리 인덱스

VOLATILE 테이블은 메모리 기반 테이블로, PRIMARY KEY 컬럼에 Red-Black 트리 인덱스가 자동으로 생성됩니다. 모든 작업이 메모리에서 수행되므로 삽입, 조회, 수정, 삭제 모두 매우 빠릅니다.

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

### non-PK 컬럼 조회는 전체 스캔

VOLATILE 테이블도 non-PK 컬럼에 대한 추가 인덱스를 생성할 수 없습니다. 그러나 데이터가 메모리에 있으므로 전체 스캔도 디스크 기반 테이블보다 훨씬 빠릅니다.

```sql
-- 전체 메모리 스캔: status 컬럼에 인덱스 없음
-- 건수가 적으면 충분히 빠름
SELECT * FROM device_status WHERE status = 'ERROR';
```

VOLATILE 테이블은 **현재 상태를 보관하는 소규모 인메모리 테이블**로 사용하는 것이 목적에 맞습니다. 전체 스캔을 수행해도 메모리 내에서 처리되므로 수만 건 수준에서는 추가 최적화가 필요 없습니다.

### VOLATILE 테이블 특성 요약

| 특성 | 내용 |
|-----|------|
| 인덱스 구조 | Red-Black 트리 (PK 자동) |
| 저장 위치 | 메모리 (재시작 시 데이터 소멸) |
| PK 조회 복잡도 | O(log n) |
| non-PK 조회 | 전체 메모리 스캔 |
| 추가 인덱스 | 생성 불가 |
| 적합한 규모 | 수만 건 이하 |

## 대용량 기준 정보가 필요한 경우

LOOKUP 테이블의 크기 제한과 non-PK 인덱스 부재로 인해 다음 시나리오에서는 대안을 고려합니다.

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

단, LOG 테이블은 Append 전용이므로 기준 정보 갱신 패턴에 맞게 설계가 필요합니다.

## 핵심 정리

| 항목 | LOOKUP | VOLATILE |
|------|--------|---------|
| 기본 인덱스 | B-Tree (PK) | Red-Black 트리 (PK) |
| 추가 인덱스 생성 | 불가 | 불가 |
| non-PK 조회 | 전체 스캔 (느림) | 전체 메모리 스캔 (상대적으로 빠름) |
| 데이터 지속성 | 영구 | 재시작 시 소멸 |
| 권장 규모 | 수만 건 이하 | 수만 건 이하 |
| 최적화 방향 | PK 설계에 조회 패턴 반영 | 크기 자체가 작으므로 추가 최적화 불필요 |
