---
type: docs
title: 'RDB 인덱스 튜닝 (TODO(verify))'
weight: 40
---

> **TODO(verify)**: 이 페이지의 내용은 Machbase Standard Edition의 RDB 테이블 인덱스 동작에 대한 현재 파악된 내용을 기반으로 작성되었습니다. 일부 세부 동작은 버전에 따라 다를 수 있으며, 공식 소스로 검증이 필요합니다.

RDB 테이블은 Machbase Standard Edition에서 제공하는 관계형 데이터 테이블입니다. 일반적인 RDBMS와 유사하게 B-Tree 기반 인덱스를 사용합니다.

## PK 자동 B-Tree 인덱스

RDB 테이블을 생성하면 PRIMARY KEY 컬럼에 B-Tree 인덱스가 자동으로 생성됩니다.

```sql
CREATE TABLE product (
    product_id   INTEGER PRIMARY KEY,  -- B-Tree 인덱스 자동 생성
    product_name VARCHAR(128),
    category     VARCHAR(64),
    price        DOUBLE,
    created_at   DATETIME
);
```

```sql
-- PK 조회: B-Tree 인덱스 사용, 효율적
SELECT * FROM product WHERE product_id = 1001;

-- PK 범위 조회
SELECT * FROM product
WHERE product_id BETWEEN 1000 AND 2000;
```

## 추가 인덱스 생성 (TODO(verify))

RDB 테이블의 일반 컬럼에 대한 추가 인덱스 생성은 현재 제한적입니다. 지원 여부와 지원하는 인덱스 유형은 Machbase 버전 및 에디션에 따라 다를 수 있으므로, 실제 운영 환경 적용 전에 공식 문서 또는 지원팀을 통해 확인하시기 바랍니다.

## PK 설계에 조회 패턴 반영

추가 인덱스 생성이 제한적인 환경에서는 **PK 설계 단계에서 주요 조회 패턴을 반영**하는 것이 가장 효과적인 튜닝 전략입니다.

### 단일 컬럼 PK

가장 자주 사용하는 조회 조건이 하나의 컬럼인 경우 해당 컬럼을 PK로 지정합니다.

```sql
-- product_id로 주로 조회하는 경우
CREATE TABLE product (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(128),
    price DOUBLE
);
```

### 복합 PK (Composite Primary Key)

여러 컬럼의 조합으로 조회하는 경우 복합 PK를 활용합니다. B-Tree 인덱스는 선두 컬럼부터 순서대로 활용됩니다.

```sql
-- category + product_id 조합으로 자주 조회하는 경우
CREATE TABLE product (
    category   VARCHAR(64),
    product_id INTEGER,
    name       VARCHAR(128),
    price      DOUBLE,
    PRIMARY KEY (category, product_id)  -- 복합 PK
);
```

```sql
-- PK 선두 컬럼(category) 사용: 인덱스 효과적으로 활용
SELECT * FROM product WHERE category = 'electronics' AND product_id = 1001;
SELECT * FROM product WHERE category = 'electronics';

-- PK 선두 컬럼 미포함: 전체 스캔 가능성
SELECT * FROM product WHERE product_id = 1001;
```

### WHERE 조건과 PK 설계 원칙

| 조회 패턴 | 권장 PK 설계 |
|----------|------------|
| 단일 키로 조회 (`WHERE id = ?`) | 해당 컬럼을 단일 PK |
| 두 컬럼 조합으로 조회 (`WHERE a = ? AND b = ?`) | (a, b) 복합 PK |
| 범위 + 등가 혼합 (`WHERE type = ? AND id > ?`) | (type, id) 복합 PK (등가 조건을 선두에) |
| 선두 컬럼만으로도 조회 | 복합 PK 선두에 해당 컬럼 배치 |

## 조회 성능 최적화 패턴

### PK 컬럼을 WHERE 조건에 포함

```sql
-- 효율적: PK 컬럼(product_id) 사용
SELECT * FROM product WHERE product_id = 1001;

-- 비효율적: PK 컬럼 미포함 → 전체 스캔
SELECT * FROM product WHERE product_name = 'Widget A';
```

### 복합 PK에서 선두 컬럼 우선 사용

B-Tree 인덱스는 선두 컬럼부터 순서대로 활용됩니다. 복합 PK `(a, b, c)`가 있을 때:

```sql
-- 인덱스 활용: 선두 컬럼(a) 포함
SELECT * FROM t WHERE a = 1;
SELECT * FROM t WHERE a = 1 AND b = 2;
SELECT * FROM t WHERE a = 1 AND b = 2 AND c = 3;

-- 인덱스 미활용: 선두 컬럼(a) 미포함
SELECT * FROM t WHERE b = 2;
SELECT * FROM t WHERE c = 3;
```

### 결과 집합 크기 제한

```sql
-- 대용량 테이블 전체 조회는 피함
SELECT * FROM product LIMIT 100;

-- 집계로 요약
SELECT category, COUNT(*), AVG(price)
FROM product
GROUP BY category;
```

## 핵심 정리

| 항목 | 권장 사항 |
|------|---------|
| PK 인덱스 | B-Tree 자동 생성, 별도 조치 불필요 |
| 추가 인덱스 | TODO(verify): 지원 여부 공식 확인 필요 |
| PK 설계 | 주요 조회 패턴의 컬럼을 PK 또는 복합 PK 선두에 배치 |
| WHERE 조건 | PK 또는 PK 선두 컬럼 포함 권장 |
| non-PK 조건 조회 | 데이터 크기를 작게 유지하거나 PK 재설계 검토 |
