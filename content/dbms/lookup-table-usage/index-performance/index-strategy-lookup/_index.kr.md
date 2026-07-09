---
type: docs
title: '9.6.3 인덱스 전략'
weight: 60
---

LOOKUP 테이블은 PRIMARY KEY에 자동으로 Red-Black Tree 인덱스가 생성됩니다. 추가 조회 조건이 있는 경우 보조 인덱스를 생성합니다.

## 자동 PRIMARY KEY 인덱스

PRIMARY KEY 컬럼에는 자동으로 인덱스가 생성됩니다. 별도 `CREATE INDEX`가 필요하지 않습니다.

```sql
CREATE LOOKUP TABLE country_code (
    code   VARCHAR(4)  PRIMARY KEY,  -- 자동 인덱스
    name   VARCHAR(64),
    region VARCHAR(32)
);

-- PK 기반 조회 (인덱스 사용)
SELECT name FROM country_code WHERE code = 'KR';
```

## 보조 인덱스

PRIMARY KEY 외의 컬럼으로 자주 조회하는 경우 보조 인덱스를 생성합니다.

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

## 인덱스 조회 예시

```sql
-- PK 조회 (자동 인덱스)
SELECT * FROM equipment_master WHERE equip_id = 42;

-- 보조 인덱스 활용
SELECT equip_id, equip_name FROM equipment_master WHERE dept = '생산팀';
SELECT equip_id, location FROM equipment_master WHERE status = 'ACTIVE';
```

## 주의사항

- 건수가 수만 건 이하의 소규모 테이블은 인덱스 없이도 빠른 조회가 가능합니다.
- 인덱스는 INSERT/UPDATE 성능에 영향을 줄 수 있으므로 필요한 것만 생성합니다.
