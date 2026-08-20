---
title: '8.6 인덱스와 성능'
weight: 60
toc: true
---

TRANSACTION 테이블의 PRIMARY KEY, UNIQUE INDEX, 일반 인덱스, JSON path 인덱스 생성 방법과
조회 성능 최적화 기준을 설명합니다.

<a id="index-tuning-rdb"></a>
<a id="index-strategy-rdb-primary-key-unique-normal"></a>

## 인덱스 유형과 생성

TRANSACTION 테이블은 BTREE 기반 PRIMARY KEY, UNIQUE INDEX, 일반 인덱스를 지원합니다.

| 구분 | 생성 방법 | 테이블당 개수 | 복합 컬럼 | NULL 처리 |
|------|-----------|---------------|-----------|-----------|
| PRIMARY KEY | 컬럼 `PRIMARY KEY` 또는 `CREATE PRIMARY KEY INDEX` | 1개 | 지원하지 않음 | 허용하지 않음 |
| UNIQUE INDEX | `CREATE UNIQUE INDEX` | 여러 개 | 지원 | NULL 포함 키는 서로 중복으로 보지 않음 |
| 일반 인덱스 | `CREATE INDEX` | 여러 개 | 지원 | 고유성 검사 없음 |

### PRIMARY KEY 인덱스

컬럼 정의에 `PRIMARY KEY`를 지정하면 해당 컬럼에 BTREE 인덱스가 자동으로 생성됩니다.

```sql
CREATE TRANSACTION TABLE product (
    product_id   INTEGER PRIMARY KEY,
    product_name VARCHAR(128),
    category     VARCHAR(64),
    price        DOUBLE,
    created_at   DATETIME
);
```

PRIMARY KEY 없이 테이블을 생성했다면 단일 컬럼에 `CREATE PRIMARY KEY INDEX`를 실행할 수
있습니다. TRANSACTION 테이블의 PRIMARY KEY는 테이블당 하나이며 복합 PRIMARY KEY는 지원하지
않습니다.

```sql
CREATE TRANSACTION TABLE orders (
    order_id LONG,
    customer VARCHAR(64),
    amount   DOUBLE,
    status   VARCHAR(16)
);

CREATE PRIMARY KEY INDEX idx_pk_order
ON orders(order_id);
```

<a id="unique-index-rdb"></a>

### UNIQUE INDEX

특정 컬럼이나 컬럼 조합의 중복을 막으려면 테이블을 생성한 뒤 `CREATE UNIQUE INDEX`를
실행합니다. `CREATE TABLE` 안에서 컬럼 뒤에 `UNIQUE`를 붙이거나 `UNIQUE(column)` 제약조건을
선언하는 문법은 지원하지 않습니다.

```sql
CREATE UNIQUE INDEX index_name
ON table_name(column_name [, ...]);
```

다음 예제는 이메일은 전체 테이블에서, 로그인 이름은 테넌트 안에서만 고유하도록 설정합니다.

```sql
CREATE TRANSACTION TABLE account (
    account_id LONG PRIMARY KEY,
    email      VARCHAR(128) NOT NULL,
    tenant_id  INTEGER NOT NULL,
    login_name VARCHAR(64) NOT NULL
);

-- 단일 컬럼 UNIQUE INDEX
CREATE UNIQUE INDEX uidx_account_email
ON account(email);

-- 복합 UNIQUE INDEX: 두 컬럼의 조합이 같을 때 중복
CREATE UNIQUE INDEX uidx_account_tenant_login
ON account(tenant_id, login_name);
```

| 상황 | 동작 |
|------|------|
| 기존 row에 중복 값이 있는 상태에서 생성 | `ERR-01418`을 반환하고 인덱스를 생성하지 않음 |
| 중복 값을 INSERT | `ERR-01418`을 반환하고 row를 추가하지 않음 |
| 기존 row를 중복 값으로 UPDATE | `ERR-01418`을 반환하고 기존 row를 유지 |
| UNIQUE 키에 NULL이 포함됨 | 다른 NULL 포함 키와 중복으로 판정하지 않음 |
| UNIQUE INDEX 삭제 | 해당 컬럼 또는 컬럼 조합의 고유성 검사를 제거 |

NULL 값도 허용하지 않으려면 UNIQUE INDEX를 구성하는 각 컬럼에 `NOT NULL`을 지정합니다.
인덱스 생성 결과는 다음과 같이 확인하고 삭제합니다.

```sql
SHOW INDEX uidx_account_email;

DROP INDEX uidx_account_email;
```

UNIQUE INDEX를 삭제한 뒤 중복 데이터를 저장하면 같은 인덱스를 다시 생성할 때 실패합니다.
중복 발생 시 기존 row를 갱신하는 방법은
[INSERT ON DUPLICATE KEY UPDATE](/dbms/rdb-table-usage/insert-on-duplicate-key-update/)를
참고하십시오.

### 일반 인덱스

PK가 아닌 컬럼을 반복 조회한다면 `CREATE INDEX`로 일반 인덱스를 생성합니다. 단일 컬럼과 복합
컬럼을 모두 지원합니다.

```sql
-- 단일 컬럼 인덱스
CREATE INDEX idx_product_name
ON product(product_name);

-- 복합 인덱스
CREATE INDEX idx_product_category_name
ON product(category, product_name);
```

일반 인덱스는 조회 속도를 높이지만 INSERT, UPDATE, DELETE 시 인덱스 갱신 비용이 늘어납니다.
실제로 자주 사용하는 조건 컬럼에만 생성합니다.

## 인덱스 설계와 조회 성능

PK와 일반 인덱스는 주요 조회 조건과 컬럼 순서에 맞춰 설계합니다.

| 조회 패턴 | 권장 설계 |
|----------|-----------|
| 단일 키 조회 (`WHERE id = ?`) | 해당 컬럼을 PRIMARY KEY로 지정 |
| 특정 non-PK 컬럼 반복 조회 | 해당 컬럼에 일반 인덱스 생성 |
| 여러 컬럼 조합 반복 조회 | 조건의 선두 컬럼 순서로 복합 인덱스 생성 |
| PK와 다른 조건을 함께 조회 | PK로 먼저 row를 좁힌 뒤 나머지 조건 필터링 |
| 드물게 사용하는 조건 | 전체 스캔 비용과 인덱스 유지 비용을 비교한 뒤 결정 |

### PRIMARY KEY 조회

```sql
-- 단일 PK 조회
SELECT * FROM product
WHERE product_id = 1001;

-- PK 범위 조회
SELECT * FROM product
WHERE product_id BETWEEN 1000 AND 2000;
```

### non-PK 컬럼 조회

인덱스가 없는 non-PK 조건은 전체 스캔이 될 수 있습니다. 반복해서 사용하는 조건에는 인덱스를
생성합니다.

```sql
CREATE INDEX idx_product_name
ON product(product_name);

SELECT * FROM product
WHERE product_name = 'Widget A';
```

### 복합 인덱스의 컬럼 순서

복합 인덱스는 선두 컬럼부터 조건에 포함될 때 효과가 큽니다. 다음 인덱스는 `category`만
사용하거나 `category`와 `product_name`을 함께 사용하는 조회에 적합합니다.

```sql
CREATE INDEX idx_product_category_name
ON product(category, product_name);

SELECT * FROM product
WHERE category = 'electronics'
  AND product_name = 'Widget A';
```

여러 non-PK 조건을 각각 조회한다면 하나의 복합 인덱스와 여러 단일 인덱스 중 실제 쿼리 빈도와
쓰기 비용이 낮은 구성을 선택합니다. 운영 쿼리와 실행 계획을 확인한 뒤 인덱스를 추가합니다.

### 결과 집합 크기 제한

인덱스를 사용하더라도 불필요하게 많은 row를 반환하면 전송과 후속 처리 비용이 증가합니다.

```sql
-- 필요한 row만 조회
SELECT * FROM product LIMIT 100;

-- 집계 결과만 반환
SELECT category, COUNT(*), AVG(price)
FROM product
GROUP BY category;
```

<a id="index-strategy-rdb-json-path"></a>

## JSON path 인덱스

`JSON` 타입 컬럼이 있는 TRANSACTION 테이블에서는 JSON path 인덱스를 생성할 수 있습니다.
JSON path 조건이 실제 인덱스 경로로 처리되는지는 실행 계획으로 확인합니다.

```sql
CREATE TRANSACTION TABLE device_state (
    device_id VARCHAR(64),
    ts        DATETIME,
    state     JSON,
    region    VARCHAR(32)
);

-- state.status와 state.code에 JSON path 인덱스 생성
CREATE INDEX idx_state_status
ON device_state(state->'$.status');

CREATE INDEX idx_state_code
ON device_state(state->'$.code');
```

```sql
SELECT device_id, ts, state
FROM device_state
WHERE state->'$.status' = 'ALARM';

SELECT device_id, ts
FROM device_state
WHERE region = 'KR'
  AND state->'$.code' = '500';
```

중첩 구조가 복잡하거나 자주 조회하는 JSON 값은 일반 컬럼으로 분리한 뒤 일반 인덱스를 적용하는
편이 효율적일 수 있습니다.

```sql
CREATE TRANSACTION TABLE device_state_v2 (
    device_id VARCHAR(64),
    ts        DATETIME,
    status    VARCHAR(16),
    code      INTEGER,
    region    VARCHAR(32),
    extra     JSON
);

CREATE INDEX idx_ds_status
ON device_state_v2(status);
```

## 핵심 정리

| 목적 | 권장 방법 |
|------|-----------|
| row 식별과 중복·NULL 차단 | 단일 컬럼 PRIMARY KEY |
| 업무 키 또는 컬럼 조합의 중복 차단 | UNIQUE INDEX, 필요하면 `NOT NULL` 함께 지정 |
| non-PK 조건 조회 | 자주 사용하는 조건 컬럼에 일반 인덱스 생성 |
| 여러 컬럼 조합 조회 | 조건 순서를 반영한 복합 인덱스 생성 |
| JSON 내부 값 조회 | JSON path 인덱스와 일반 컬럼 분리를 실행 계획으로 비교 |
| 쓰기 성능 유지 | 사용하지 않는 인덱스를 제거하고 필요한 인덱스만 유지 |
