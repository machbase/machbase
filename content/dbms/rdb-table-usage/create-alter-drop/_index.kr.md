---
title: '8.3 생성, 변경, 삭제'
weight: 30
toc: true
---

RDB 테이블의 DDL(CREATE, ALTER, DROP) 관련 내용을 다룬다. RDB 테이블은 관계형 데이터 모델을 사용하므로, 스키마를 만들 때 PRIMARY KEY, 인덱스, AUTO_INCREMENT 사용 여부를 함께 결정한다.

<a id="create-rdb-table"></a>

## RDB 테이블 생성

RDB 테이블은 `CREATE RDB TABLE` 문으로 생성한다.

```sql
CREATE RDB TABLE product_catalog (
    product_id LONG PRIMARY KEY,
    category   VARCHAR(64),
    name       VARCHAR(256),
    price      DOUBLE,
    updated_at DATETIME
);
```

최소 하나 이상의 컬럼이 필요하다. 업무 데이터처럼 행을 식별해야 하는 경우에는 PRIMARY KEY를 명시한다.

```sql
CREATE RDB TABLE order_history (
    order_id  LONG PRIMARY KEY,
    customer  VARCHAR(64),
    item_id   INTEGER,
    amount    DOUBLE,
    status    VARCHAR(16),
    order_time DATETIME
);
```

<a id="create-rdb-primary-key-index"></a>

## PRIMARY KEY와 인덱스 생성

PRIMARY KEY는 컬럼 정의에서 지정하거나, 테이블 생성 후 `CREATE PRIMARY KEY INDEX` 문으로 생성한다.

```sql
CREATE RDB TABLE inventory (
    item_id   LONG,
    warehouse VARCHAR(32),
    qty       INTEGER,
    updated_at DATETIME
);

CREATE PRIMARY KEY INDEX idx_pk_inventory ON inventory(item_id);
```

조회, UPDATE, DELETE 조건에 자주 사용하는 컬럼에는 보조 인덱스를 생성한다.

```sql
CREATE INDEX idx_inventory_warehouse ON inventory(warehouse);
CREATE INDEX idx_order_status_time ON order_history(status, order_time);
```

인덱스 설계 기준은 [RDB 인덱스와 JSON path 인덱스](/dbms/rdb-table-usage/rdb-index-json-path/)에서 다룬다.

<a id="create-rdb-auto-increment"></a>

## AUTO_INCREMENT 사용

자동 증가 키가 필요한 경우 `LONG PRIMARY KEY AUTO_INCREMENT`를 사용한다.

```sql
CREATE RDB TABLE device_master (
    id          LONG PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(80),
    site_code   VARCHAR(32),
    created_at  DATETIME
);
```

`AUTO_INCREMENT` 컬럼은 단일 64비트 정수 PRIMARY KEY에 사용한다. INSERT 방식과 catalog 확인 방법은 [AUTO_INCREMENT](/dbms/rdb-table-usage/auto-increment/)에서 다룬다.

<a id="drop-rdb-table"></a>

## RDB 테이블 삭제

테이블을 삭제하려면 `DROP TABLE`을 사용한다.

```sql
DROP TABLE product_catalog;
```

`DROP TABLE`은 테이블 정의, 데이터, 관련 인덱스를 삭제한다. 운영 데이터는 삭제 전에 백업 또는 내보내기 절차를 먼저 수행한다.

<a id="rdb-ddl-operation-notes"></a>

## DDL 운영 주의사항

- DDL은 운영 중인 DML과 충돌할 수 있으므로 변경 시간대를 분리한다.
- 장시간 열린 트랜잭션이 있으면 DDL이 지연되거나 실패할 수 있다.
- RDB 테이블은 Standard Edition 전용이다.
- RDB 테이블에는 TAG 전용 `METADATA`, `BASETIME`, `BASEDISTANCE` 절을 사용할 수 없다.
- 백업·복구 정책에는 RDB sidecar 파일 포함 여부를 함께 확인한다.
