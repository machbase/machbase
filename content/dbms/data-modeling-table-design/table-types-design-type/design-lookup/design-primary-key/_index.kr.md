---
type: docs
title: 'PRIMARY KEY 설계'
weight: 20
---

LOOKUP 테이블은 `PRIMARY KEY`가 필수입니다. PRIMARY KEY는 행을 고유하게 식별하며, UPDATE/DELETE 연산의 기준이 됩니다.

## 기본 문법

```sql
CREATE LOOKUP TABLE table_name (
    pk_col   type    PRIMARY KEY,
    col2     type,
    ...
);
```

## 단일 컬럼 PRIMARY KEY

```sql
CREATE LOOKUP TABLE country_code (
    code     VARCHAR(4)  PRIMARY KEY,
    name     VARCHAR(64),
    region   VARCHAR(32)
);
```

## 복합 키가 필요한 경우

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

## PRIMARY KEY 타입 선택

| 타입 | 장점 | 단점 |
|------|------|------|
| `VARCHAR(n)` | 가독성, 의미 있는 키 | 문자열 비교 비용 |
| `INTEGER` / `LONG` | 비교 빠름, 저장 효율 | 의미 없음, 별도 매핑 필요 |

## 주의사항

- PRIMARY KEY 값은 중복될 수 없습니다.
- PRIMARY KEY 값은 변경할 수 없습니다 (변경 시 DELETE + INSERT).
- PRIMARY KEY 컬럼에는 자동으로 인덱스가 생성됩니다.
- PRIMARY KEY 컬럼은 하나만 지정합니다.
