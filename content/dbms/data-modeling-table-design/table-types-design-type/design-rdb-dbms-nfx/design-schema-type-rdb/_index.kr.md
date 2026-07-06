---
type: docs
title: '스키마 설계'
weight: 20
---

## 기본 문법

```sql
CREATE RDB TABLE table_name (
    col1 type1,
    col2 type2,
    ...
);
```

## 컬럼 수 제약

RDB 테이블은 **최소 1개** 이상의 컬럼이 필요합니다.

```sql
-- 정상: 컬럼 1개
CREATE RDB TABLE t1 (id INTEGER);

-- 정상: 컬럼 여러 개
CREATE RDB TABLE t2 (id INTEGER, name VARCHAR(64), cat VARCHAR(32), val DOUBLE);
```

## 지원 데이터 타입

| 타입 | 설명 |
|------|------|
| `INTEGER` (`INT`) | 32비트 정수 |
| `LONG` | 64비트 정수 |
| `SHORT` | 16비트 정수 |
| `FLOAT` | 32비트 부동소수점 |
| `DOUBLE` | 64비트 부동소수점 |
| `VARCHAR(n)` | 가변 문자열 |
| `DATETIME` | 날짜·시간 (나노초) |
| `IPV4` / `IPV6` | 네트워크 주소 |
| `JSON` | JSON 문서 |

## 설계 예시

### 제품 카탈로그

```sql
CREATE RDB TABLE product_catalog (
    product_id   LONG,
    category     VARCHAR(64),
    name         VARCHAR(256),
    price        DOUBLE
);

CREATE INDEX idx_prod_cat ON product_catalog(category);

-- 가격 변경
UPDATE product_catalog SET price = 19900 WHERE product_id = 42;
```

### 트랜잭션 이력

```sql
CREATE RDB TABLE tx_history (
    tx_id        LONG,
    account_id   VARCHAR(32),
    tx_type      VARCHAR(16),
    amount       DOUBLE,
    tx_time      DATETIME,
    status       VARCHAR(16)
);

CREATE INDEX idx_tx_account ON tx_history(account_id);
CREATE INDEX idx_tx_time    ON tx_history(tx_time);

-- 상태 업데이트
UPDATE tx_history SET status = 'SETTLED' WHERE tx_id = 9999;
```

## PRIMARY KEY 지정

RDB 테이블에서 PRIMARY KEY는 DDL 절 대신 `CREATE INDEX` 문으로 지정합니다. PK 인덱스는 Red-Black Tree를 사용합니다.

```sql
CREATE RDB TABLE product_catalog (
    product_id LONG,
    name       VARCHAR(256),
    price      DOUBLE
);

-- PRIMARY KEY 인덱스 생성 (자세한 내용은 다음 섹션 참고)
CREATE INDEX idx_pk_product ON product_catalog(product_id);
```

## 주의사항

- `METADATA` 절은 TAG 테이블 전용으로, RDB 테이블에서는 사용할 수 없습니다.
- `BASETIME`, `BASE DISTANCE` 키워드는 사용할 수 없습니다.
- Cluster Edition에서는 RDB 테이블을 생성할 수 없습니다.
