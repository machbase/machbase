---
title: '8.2 테이블 구조와 스키마'
weight: 20
toc: true
---

TRANSACTION 테이블의 스키마 설계 방법과 컬럼 타입, PRIMARY KEY 및 UNIQUE INDEX 지정 방식을
설명합니다.

<a id="rdb-table-design"></a>

## TRANSACTION 테이블 설계

TRANSACTION 테이블은 Machbase 8.7.0에서 도입된 관계형 테이블로, SELECT·INSERT·UPDATE·DELETE를 모두 지원합니다. PRIMARY KEY 인덱스와 보조 인덱스를 함께 활용할 수 있습니다.

```sql
CREATE TRANSACTION TABLE order_history (
    order_id  LONG,
    item_id   INTEGER,
    qty       INTEGER,
    amount    DOUBLE
);

UPDATE order_history SET qty = 10 WHERE order_id = 1001;
DELETE FROM order_history WHERE order_id = 1001;
```

### 이 섹션의 구성

- **[활용 사례](/dbms/rdb-table-usage/overview-use-criteria/#use-cases-rdb)**
- **[스키마 설계](/dbms/rdb-table-usage/table-structure-schema/#rdb-table-design-design-schema-type-rdb)**
- **[PRIMARY KEY·UNIQUE INDEX·일반 인덱스 비교](/dbms/rdb-table-usage/index-performance/#index-strategy-rdb-primary-key-unique-normal)**
- **[UNIQUE INDEX 생성과 동작](/dbms/rdb-table-usage/index-performance/#unique-index-rdb)**
- **[AUTO_INCREMENT](/dbms/reference/sql/syntax-dictionary-sql/auto-increment-syntax/)**
- **[JSON 경로 인덱스](/dbms/rdb-table-usage/index-performance/#index-strategy-rdb-json-path)**
- **[트랜잭션 설계](/dbms/rdb-table-usage/transaction/#design-transaction-rdb)**
- **[UPDATE·DELETE 설계](/dbms/rdb-table-usage/data-input-mutation/#modeling-rdb-update-delete)**
- **[잠금·충돌·타임아웃 설계](/dbms/rdb-table-usage/locking-conflict-timeout/#design-locking-conflict-rdb-busy-timeout-ddl-dml)**
- **[자기 참조·INSERT SELECT](/dbms/rdb-table-usage/data-input-mutation/#reference-self-rdb-insert-select)**
- **[JOIN 설계](/dbms/rdb-table-usage/join-relational-query/#join-design-rdb)**
- **[백업·복원·마운트](/dbms/rdb-table-usage/backup-restore-mount/#design-backup-mount-rdb)**
- **[Append API](/dbms/rdb-table-usage/data-input-mutation/#unsupported-rejected-rdb-append-api)**
- **[SDK 지원 범위](/dbms/rdb-table-usage/data-input-mutation/#support-scope-rdb-sdk)**
- **[Edition 제한](/dbms/rdb-table-usage/constraints-errors-troubleshooting/#limitations-rdb-edition)**

<a id="rdb-table-design-design-schema-type-rdb"></a>

### 스키마 설계

#### 기본 문법

```sql
CREATE TRANSACTION TABLE table_name (
    col1 type1,
    col2 type2,
    ...
);
```

#### 컬럼 수 제약

최소 1개 이상의 컬럼이 필요합니다.

```sql
-- 정상: 컬럼 1개
CREATE TRANSACTION TABLE t1 (id INTEGER);

-- 정상: 컬럼 여러 개
CREATE TRANSACTION TABLE t2 (id INTEGER, name VARCHAR(64), cat VARCHAR(32), val DOUBLE);
```

#### 지원 데이터 타입

| 타입 | 설명 |
|------|------|
| `INTEGER` (`INT`) | 32비트 정수 |
| `LONG` | 64비트 정수 |
| `SHORT` | 16비트 정수 |
| `FLOAT` | 32비트 부동소수점 |
| `DOUBLE` | 64비트 부동소수점 |
| `DECIMAL(M,D)` | exact 고정소수점 (`NUMERIC`, `DEC`, `FIXED`, `NUMBER` alias) |
| `VARCHAR(n)` | 가변 문자열 |
| `DATETIME` | 날짜·시간 (나노초) |
| `IPV4` / `IPV6` | 네트워크 주소 |
| `JSON` | JSON 문서 |

DECIMAL의 precision, scale, 반올림과 클라이언트 매핑은 [DECIMAL과 NUMERIC 고정소수점
타입](/dbms/reference/sql/type-data-types-dictionary/decimal-numeric-fixed-point/)을 참고하십시오.

#### 설계 예시

##### 제품 카탈로그

```sql
CREATE TRANSACTION TABLE product_catalog (
    product_id   LONG,
    category     VARCHAR(64),
    name         VARCHAR(256),
    price        DECIMAL(18,2)
);

CREATE INDEX idx_prod_cat ON product_catalog(category);

-- 가격 변경
UPDATE product_catalog SET price = 19900 WHERE product_id = 42;
```

##### 트랜잭션 이력

```sql
CREATE TRANSACTION TABLE tx_history (
    tx_id        LONG,
    account_id   VARCHAR(32),
    tx_type      VARCHAR(16),
    amount       DECIMAL(24,4),
    tx_time      DATETIME,
    status       VARCHAR(16)
);

CREATE INDEX idx_tx_account ON tx_history(account_id);
CREATE INDEX idx_tx_time    ON tx_history(tx_time);

-- 상태 업데이트
UPDATE tx_history SET status = 'SETTLED' WHERE tx_id = 9999;
```

#### PRIMARY KEY 지정

컬럼 정의에 직접 `PRIMARY KEY`를 지정하거나, `CREATE PRIMARY KEY INDEX` 문으로 사후 생성할 수 있습니다. TRANSACTION 인덱스는 BTREE로 표시됩니다.

```sql
-- 컬럼 정의에서 PRIMARY KEY 지정
CREATE TRANSACTION TABLE product_catalog (
    product_id LONG PRIMARY KEY,
    name       VARCHAR(256),
    price      DECIMAL(18,2)
);
```

```sql
-- 또는 PRIMARY KEY 인덱스 사후 생성
CREATE TRANSACTION TABLE product_catalog (
    product_id LONG,
    name       VARCHAR(256),
    price      DECIMAL(18,2)
);

CREATE PRIMARY KEY INDEX idx_pk_product ON product_catalog(product_id);
```

#### UNIQUE 값 보장

TRANSACTION 테이블은 고유성 보장을 지원하지만 `CREATE TABLE` 안에서 컬럼 뒤에 `UNIQUE`를
붙이거나 `UNIQUE(column)` 제약조건을 선언하지 않습니다. 테이블을 먼저 생성한 뒤
`CREATE UNIQUE INDEX`를 실행합니다.

```sql
CREATE TRANSACTION TABLE account (
    account_id LONG PRIMARY KEY,
    email      VARCHAR(128) NOT NULL,
    name       VARCHAR(80)
);

CREATE UNIQUE INDEX uidx_account_email
ON account(email);
```

이후 같은 `email`을 INSERT하거나 기존 row의 `email`을 중복 값으로 UPDATE하면
`ERR-01418`이 반환됩니다. 단일·복합 UNIQUE INDEX, NULL 및 삭제 동작은
[UNIQUE INDEX 생성과 동작](/dbms/rdb-table-usage/index-performance/#unique-index-rdb)을
참고하십시오.

자동 번호가 필요한 단일 64비트 정수 PRIMARY KEY에는 `AUTO_INCREMENT`를 사용할 수 있습니다.

```sql
CREATE TRANSACTION TABLE device_master (
    id LONG PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(80),
    site_code VARCHAR(32)
);
```

`AUTO_INCREMENT`의 지원 타입, INSERT 방식, catalog 확인 방법은 [AUTO_INCREMENT](/dbms/reference/sql/syntax-dictionary-sql/auto-increment-syntax/)를 참고합니다.

#### 주의사항

- `METADATA` 절은 TAG 테이블 전용이므로 TRANSACTION 테이블에서는 사용할 수 없습니다.
- `BASETIME`, `BASEDISTANCE` 키워드도 사용할 수 없습니다.
- Cluster Edition에서는 TRANSACTION 테이블을 생성할 수 없습니다.
