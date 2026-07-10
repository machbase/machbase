---
title: '8.6 인덱스와 성능'
weight: 60
toc: true
---

RDB 테이블의 인덱스 설계와 조회 성능 최적화 방법을 다룬다.


<a id="index-tuning-rdb"></a>

## RDB 인덱스 튜닝

`CREATE RDB TABLE`로 생성하는 RDB 테이블은 PRIMARY KEY와 보조 인덱스를 조회 패턴에 맞게 설계해야 최적의 성능을 얻을 수 있다.

### PK 자동 B-Tree 인덱스

PRIMARY KEY를 선언하면 해당 컬럼에 B-Tree 인덱스가 자동 생성된다.

```sql
CREATE RDB TABLE product (
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

### 추가 인덱스 생성

일반 컬럼에 `CREATE INDEX`로 보조 인덱스를 만들 수 있다. PK가 아닌 컬럼을 반복 조회한다면 인덱스 생성을 검토한다.

```sql
CREATE INDEX idx_product_name ON product(product_name);
CREATE INDEX idx_product_category ON product(category);
CREATE INDEX idx_product_category_name ON product(category, name);
```

보조 인덱스는 조회 속도를 높이지만 INSERT/UPDATE/DELETE 시 인덱스 갱신 비용이 늘어난다. 실제로 자주 사용하는 조건 컬럼에만 생성한다.

### PK 설계에 조회 패턴 반영

PK와 보조 인덱스를 설계할 때 주요 조회 패턴을 반영하는 것이 가장 효과적인 튜닝 전략이다.

#### 단일 컬럼 PK

가장 빈번한 조회 조건이 하나의 컬럼이라면 해당 컬럼을 PK로 지정한다.

```sql
-- product_id로 주로 조회하는 경우
CREATE RDB TABLE product (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(128),
    price DOUBLE
);
```

#### 여러 조회 조건이 있는 경우

현재 빌드에서는 테이블 제약 형태의 복합 PRIMARY KEY 구문을 사용할 수 없다. 여러 컬럼 조합으로 자주 조회한다면 단일 PK와 보조 인덱스를 조합한다.

```sql
CREATE RDB TABLE product (
    product_id INTEGER PRIMARY KEY,
    category   VARCHAR(64),
    name       VARCHAR(128),
    price      DOUBLE
);

CREATE INDEX idx_product_category ON product(category);

-- PK 조회
SELECT * FROM product WHERE product_id = 1001;

-- 단일 컬럼 보조 인덱스 조회
SELECT * FROM product WHERE category = 'electronics';

-- 복합 보조 인덱스 조회
SELECT * FROM product
WHERE category = 'electronics'
  AND name = 'Widget A';
```

#### WHERE 조건과 PK 설계 원칙

| 조회 패턴 | 권장 PK 설계 |
|----------|------------|
| 단일 키로 조회 (`WHERE id = ?`) | 해당 컬럼을 단일 PK |
| 특정 컬럼으로 자주 조회 (`WHERE category = ?`) | 해당 컬럼에 추가 인덱스 생성 |
| PK와 보조 조건을 함께 조회 (`WHERE id = ? AND status = ?`) | PK로 먼저 레코드를 좁히고 보조 조건을 필터링 |
| 여러 non-PK 조건이 빈번함 | 복합 보조 인덱스 또는 컬럼별 인덱스를 실제 쿼리 빈도와 쓰기 비용으로 판단 |

### 조회 성능 최적화 패턴

#### PK 컬럼을 WHERE 조건에 포함

```sql
-- 효율적: PK 컬럼(product_id) 사용
SELECT * FROM product WHERE product_id = 1001;

-- 비효율적: PK 컬럼 미포함 → 전체 스캔
SELECT * FROM product WHERE product_name = 'Widget A';
```

#### non-PK 컬럼에는 필요한 인덱스 생성

```sql
-- 반복 조회하는 non-PK 컬럼
CREATE INDEX idx_product_name ON product(product_name);

SELECT * FROM product WHERE product_name = 'Widget A';
```

여러 컬럼 조합을 반복 조회한다면 복합 보조 인덱스를 활용한다. 복합 인덱스는 선두 컬럼부터 조건에 포함될 때 효과가 크다.

```sql
CREATE INDEX idx_product_category_name ON product(category, product_name);

-- 선두 컬럼(category)을 포함: 복합 인덱스 활용 가능
SELECT * FROM product
WHERE category = 'electronics'
  AND product_name = 'Widget A';
```

드물게 실행하는 조건까지 모두 인덱스로 만들면 쓰기 비용과 저장 공간이 증가한다. 운영 쿼리 로그나 애플리케이션 호출 빈도를 기준으로 인덱스 대상을 선정한다.

#### 결과 집합 크기 제한

```sql
-- 대용량 테이블 전체 조회는 피함
SELECT * FROM product LIMIT 100;

-- 집계로 요약
SELECT category, COUNT(*), AVG(price)
FROM product
GROUP BY category;
```

### 핵심 정리

| 항목 | 권장 사항 |
|------|---------|
| PK 인덱스 | B-Tree 자동 생성, 별도 조치 불필요 |
| 추가 인덱스 | `CREATE INDEX index_name ON table(column)` 또는 복합 보조 인덱스 사용 |
| PK 설계 | 단일 키 조회가 많은 컬럼을 PRIMARY KEY로 배치 |
| WHERE 조건 | PK 또는 인덱스 컬럼 포함 권장 |
| non-PK 조건 조회 | 반복 조회 컬럼에 추가 인덱스 생성 검토 |
