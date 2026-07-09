---
type: docs
title: '9.10.2 PRIMARY KEY 정책'
weight: 70
---

LOOKUP 테이블의 PRIMARY KEY 설계 시 고려해야 할 정책과 모범 사례를 설명합니다.

## 자연키 vs 대리키

### 자연키 (Natural Key)

비즈니스 의미를 갖는 값을 그대로 PRIMARY KEY로 사용합니다.

```sql
-- 국가 코드: 표준화된 자연키
CREATE LOOKUP TABLE country (
    iso_code VARCHAR(4) PRIMARY KEY,  -- ISO 3166-1 alpha-2
    name     VARCHAR(64)
);
```

**장점**: 의미 파악 쉬움, 별도 조회 불필요
**단점**: 키 변경 시 참조 무결성 문제

### 대리키 (Surrogate Key)

SEQUENCE 컬럼이나 UUID처럼 의미 없는 값을 PRIMARY KEY로 사용합니다.

```sql
-- 설비 마스터: 대리키
CREATE LOOKUP TABLE equipment (
    equip_id  LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    code      VARCHAR(32),          -- 비즈니스 키
    name      VARCHAR(128)
);
CREATE INDEX idx_equip_code ON equipment(code);
```

**장점**: 불변, 조인 효율적
**단점**: 코드-ID 변환 필요

## PRIMARY KEY 불변 원칙

PRIMARY KEY 값은 변경하지 않는 것을 원칙으로 합니다. 변경이 필요하면 DELETE + INSERT를 사용합니다.

```sql
-- 잘못된 패턴 (PK 변경은 DELETE + INSERT로)
-- UPDATE는 PK 변경 불가

-- 올바른 패턴
DELETE FROM country WHERE iso_code = 'OLD';
INSERT INTO country VALUES ('NEW', '새 국가명');
```

LOOKUP 테이블 DML은 개별 문장 단위로 실행합니다. 현재 빌드에서는 `BEGIN`/`COMMIT`으로 묶은
트랜잭션 안에서 LOOKUP DML을 실행할 수 없습니다.

## 복합 PRIMARY KEY 주의사항

- 복합 PK의 각 컬럼 순서가 인덱스 효율에 영향을 줍니다.
- 첫 번째 PK 컬럼이 주요 조회 조건이어야 합니다.
