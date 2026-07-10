---
title: '9.10 PRIMARY KEY 정책'
weight: 100
toc: true
---
LOOKUP 테이블의 PRIMARY KEY 설계 원칙과 정책을 다룹니다.


<a id="design-primary-key"></a>

## PRIMARY KEY 설계

LOOKUP 테이블은 `PRIMARY KEY`가 필수입니다. PRIMARY KEY는 행을 고유하게 식별하며, UPDATE/DELETE 연산의 기준이 됩니다.

### 기본 문법

```sql
CREATE LOOKUP TABLE table_name (
    pk_col   type    PRIMARY KEY,
    col2     type,
    ...
);
```

### 단일 컬럼 PRIMARY KEY

```sql
CREATE LOOKUP TABLE country_code (
    code     VARCHAR(4)  PRIMARY KEY,
    name     VARCHAR(64),
    region   VARCHAR(32)
);
```

### 복합 키가 필요한 경우

```sql
CREATE LOOKUP TABLE product_region_price (
    price_key  VARCHAR(64) PRIMARY KEY,
    product_id VARCHAR(32),
    region     VARCHAR(16),
    price      DOUBLE
);

-- 삽입
INSERT INTO product_region_price VALUES ('PROD-01:KR', 'PROD-01', 'KR', 99.0);
INSERT INTO product_region_price VALUES ('PROD-01:US', 'PROD-01', 'US', 79.0);

-- 조합 키 기반 UPDATE
UPDATE product_region_price SET price = 89.0
WHERE price_key = 'PROD-01:KR';
```

LOOKUP 테이블은 PRIMARY KEY 컬럼을 하나만 지정할 수 있습니다. 여러 컬럼의 조합이
비즈니스 키라면 조합 문자열 또는 대리키를 별도 PRIMARY KEY 컬럼으로 둡니다.

### PRIMARY KEY 타입 선택

| 타입 | 장점 | 단점 |
|------|------|------|
| `VARCHAR(n)` | 가독성, 의미 있는 키 | 문자열 비교 비용 |
| `INTEGER` / `LONG` | 비교 빠름, 저장 효율 | 의미 없음, 별도 매핑 필요 |

### 주의사항

- PRIMARY KEY 값은 중복될 수 없습니다.
- PRIMARY KEY 값은 변경할 수 없다 (변경 시 DELETE + INSERT).
- PRIMARY KEY 컬럼에는 인덱스가 자동 생성됩니다.
- PRIMARY KEY 컬럼은 하나만 지정합니다.

<a id="policy-lookup-primary-key"></a>

## PRIMARY KEY 정책

PRIMARY KEY 설계 시 고려할 정책과 모범 사례입니다.

### 자연키 vs 대리키

#### 자연키 (Natural Key)

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

#### 대리키 (Surrogate Key)

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

### PRIMARY KEY 불변 원칙

PRIMARY KEY 값은 변경하지 않는 것이 원칙입니다. 변경이 필요하면 DELETE + INSERT를 사용합니다.

```sql
-- 잘못된 패턴 (PK 변경은 DELETE + INSERT로)
-- UPDATE는 PK 변경 불가

-- 올바른 패턴
DELETE FROM country WHERE iso_code = 'OLD';
INSERT INTO country VALUES ('NEW', '새 국가명');
```

LOOKUP 테이블 DML은 개별 문장 단위로 실행합니다. 현재 빌드에서는 `BEGIN`/`COMMIT`으로 묶은
트랜잭션 안에서 LOOKUP DML을 실행할 수 없습니다.

### 복합 PRIMARY KEY 주의사항

- 복합 PK의 각 컬럼 순서가 인덱스 효율에 영향을 줍니다.
- 첫 번째 PK 컬럼이 주요 조회 조건이어야 합니다.
