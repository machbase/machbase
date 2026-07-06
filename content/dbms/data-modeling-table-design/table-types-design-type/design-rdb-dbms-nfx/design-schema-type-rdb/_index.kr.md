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
    col3 type3,
    col4 type4
    [, ...]
);
```

## 최소 컬럼 수 제약

RDB 테이블은 **최소 4개** 컬럼이 필요합니다. 4개 미만으로 생성하면 오류가 발생합니다.

```sql
-- 오류: 컬럼 수 부족
CREATE RDB TABLE t1 (id INTEGER, name VARCHAR(64));  -- ERROR

-- 정상: 4개 이상
CREATE RDB TABLE t1 (id INTEGER, name VARCHAR(64), cat VARCHAR(32), val DOUBLE);
```

## 지원 데이터 타입

| 타입 | 설명 |
|------|------|
| `INTEGER` (`INT`) | 32비트 정수 |
| `LONG` | 64비트 정수 |
| `SHORT` | 16비트 정수 |
| `FLOAT` | 32비트 부동소수점 |
| `DOUBLE` | 64비트 부동소수점 |
| `VARCHAR(n)` | 가변 문자열 (최대 n) |
| `DATETIME` | 날짜·시간 (나노초) |
| `IPV4` / `IPV6` | 네트워크 주소 |
| `JSON` | JSON 문서 |

## 설계 예시

### 제품 카탈로그 (대규모)

```sql
CREATE RDB TABLE product_catalog (
    product_id   LONG,
    category     VARCHAR(64),
    name         VARCHAR(256),
    price        DOUBLE
);

CREATE INDEX idx_prod_cat ON product_catalog(category);
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
```

## 주의사항

- `METADATA` 절은 TAG 테이블 전용으로, RDB 테이블에서는 사용할 수 없습니다.
- PRIMARY KEY 제약은 인덱스 형태로 지정합니다 (별도 `CREATE INDEX` 필요 — 다음 섹션 참고).
