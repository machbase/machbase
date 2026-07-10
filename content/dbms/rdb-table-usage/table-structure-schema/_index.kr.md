---
title: '8.2 테이블 구조와 스키마'
weight: 20
toc: true
---

RDB 테이블의 스키마 설계 방법과 컬럼 타입, PRIMARY KEY 지정 방식을 설명한다.

<a id="rdb-table-design"></a>

## RDB 테이블 설계

RDB 테이블은 Machbase 8.6에서 도입된 관계형 테이블로, SELECT·INSERT·UPDATE·DELETE를 모두 지원한다. PRIMARY KEY 인덱스와 보조 인덱스를 함께 활용할 수 있다.

```sql
CREATE RDB TABLE order_history (
    order_id  LONG,
    item_id   INTEGER,
    qty       INTEGER,
    amount    DOUBLE
);

UPDATE order_history SET qty = 10 WHERE order_id = 1001;
DELETE FROM order_history WHERE order_id = 1001;
```

### 이 섹션의 구성

- **[활용 사례](/dbms/rdb-table-usage/patterns-scenarios/#use-cases-rdb)**
- **[스키마 설계](/dbms/rdb-table-usage/table-structure-schema/#rdb-table-design-design-schema-type-rdb)**
- **[PRIMARY KEY·UNIQUE·일반 인덱스 전략](/dbms/rdb-table-usage/rdb-index-json-path/#index-strategy-rdb-primary-key-unique-normal)**
- **[AUTO_INCREMENT](/dbms/rdb-table-usage/auto-increment/)**
- **[JSON 경로 인덱스](/dbms/rdb-table-usage/rdb-index-json-path/#index-strategy-rdb-json-path)**
- **[트랜잭션 설계](/dbms/rdb-table-usage/transaction/#design-transaction-rdb)**
- **[UPDATE·DELETE 설계](/dbms/rdb-table-usage/data-input-mutation/#modeling-rdb-update-delete)**
- **[잠금·충돌·타임아웃 설계](/dbms/rdb-table-usage/locking-conflict-timeout/#design-locking-conflict-rdb-busy-timeout-ddl-dml)**
- **[자기 참조·INSERT SELECT](/dbms/rdb-table-usage/data-input-mutation/#reference-self-rdb-insert-select)**
- **[JOIN 설계](/dbms/rdb-table-usage/join-relational-query/#join-design-rdb)**
- **[백업·마운트](/dbms/rdb-table-usage/backup-mount-sidecar/#design-backup-mount-rdb)**
- **[Append API](/dbms/rdb-table-usage/sdk-append-scope/#unsupported-rejected-rdb-append-api)**
- **[SDK 지원 범위](/dbms/rdb-table-usage/sdk-append-scope/#support-scope-rdb-sdk)**
- **[Edition 제한](/dbms/rdb-table-usage/constraints-errors-troubleshooting/#limitations-rdb-edition)**

<a id="rdb-table-design-design-schema-type-rdb"></a>

### 스키마 설계

#### 기본 문법

```sql
CREATE RDB TABLE table_name (
    col1 type1,
    col2 type2,
    ...
);
```

#### 컬럼 수 제약

최소 1개 이상의 컬럼이 필요하다.

```sql
-- 정상: 컬럼 1개
CREATE RDB TABLE t1 (id INTEGER);

-- 정상: 컬럼 여러 개
CREATE RDB TABLE t2 (id INTEGER, name VARCHAR(64), cat VARCHAR(32), val DOUBLE);
```

#### 지원 데이터 타입

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

#### 설계 예시

##### 제품 카탈로그

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

##### 트랜잭션 이력

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

#### PRIMARY KEY 지정

컬럼 정의에 직접 `PRIMARY KEY`를 지정하거나, `CREATE PRIMARY KEY INDEX` 문으로 사후 생성할 수 있다. RDB 인덱스는 BTREE로 표시된다.

```sql
-- 컬럼 정의에서 PRIMARY KEY 지정
CREATE RDB TABLE product_catalog (
    product_id LONG PRIMARY KEY,
    name       VARCHAR(256),
    price      DOUBLE
);
```

```sql
-- 또는 PRIMARY KEY 인덱스 사후 생성
CREATE RDB TABLE product_catalog (
    product_id LONG,
    name       VARCHAR(256),
    price      DOUBLE
);

CREATE PRIMARY KEY INDEX idx_pk_product ON product_catalog(product_id);
```

자동 번호가 필요한 단일 64비트 정수 PRIMARY KEY에는 `AUTO_INCREMENT`를 사용할 수 있다.

```sql
CREATE RDB TABLE device_master (
    id LONG PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(80),
    site_code VARCHAR(32)
);
```

`AUTO_INCREMENT`의 지원 타입, INSERT 방식, catalog 확인 방법은 [AUTO_INCREMENT](/dbms/rdb-table-usage/auto-increment/)를 참고한다.

#### 주의사항

- `METADATA` 절은 TAG 테이블 전용이므로 RDB 테이블에서는 사용할 수 없다.
- `BASETIME`, `BASEDISTANCE` 키워드도 사용할 수 없다.
- Cluster Edition에서는 RDB 테이블을 생성할 수 없다.
