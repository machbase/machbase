---
title: '8.3 생성, 변경, 삭제'
weight: 30
toc: true
---

TRANSACTION 테이블의 DDL(CREATE, ALTER, DROP) 관련 내용을 다룹니다. TRANSACTION 테이블은
관계형 데이터 모델을 사용하므로, 스키마를 만들 때 PRIMARY KEY, UNIQUE INDEX, 일반 인덱스,
AUTO_INCREMENT 사용 여부를 함께 결정합니다.

<a id="create-rdb-table"></a>

## TRANSACTION 테이블 생성

TRANSACTION 테이블은 무수식 `CREATE TABLE`, 전체 이름을 사용한 `CREATE TRANSACTION TABLE`,
축약형 `CREATE TXN TABLE`로 생성합니다. 세 문법의 결과는 같습니다. 다음 예제처럼 공개 문서와
운영 스크립트에서는 테이블 유형을 분명히 드러내는 `CREATE TRANSACTION TABLE` 사용을 권장합니다.

```sql
CREATE TRANSACTION TABLE product_catalog (
    product_id LONG PRIMARY KEY,
    category   VARCHAR(64),
    name       VARCHAR(256),
    price      DOUBLE,
    updated_at DATETIME
);
```

최소 하나 이상의 컬럼이 필요합니다. 업무 데이터처럼 행을 식별해야 하는 경우에는 PRIMARY KEY를 명시합니다.

```sql
-- 다음 두 문장도 TRANSACTION 테이블을 생성합니다.
CREATE TABLE customer (id LONG PRIMARY KEY, name VARCHAR(64));
CREATE TXN TABLE supplier (id LONG PRIMARY KEY, name VARCHAR(64));

-- LOG 테이블은 LOG 유형을 명시합니다.
CREATE LOG TABLE application_event (event_time DATETIME, message VARCHAR(256));
```

이전 공개 명칭인 `CREATE RDB TABLE`과 `CREATE TRX TABLE`은 지원하지 않습니다. TRANSACTION
테이블은 Standard Edition 전용입니다. Cluster Edition은 위 세 TRANSACTION 생성 문법을 모두
거부하지만 `CREATE LOG TABLE`은 지원합니다.

```sql
CREATE TRANSACTION TABLE order_history (
    order_id  LONG PRIMARY KEY,
    customer  VARCHAR(64),
    item_id   INTEGER,
    amount    DOUBLE,
    status    VARCHAR(16),
    order_time DATETIME
);
```

<a id="create-rdb-primary-key-index"></a>

## PRIMARY KEY, UNIQUE INDEX, 일반 인덱스 생성

PRIMARY KEY는 컬럼 정의에서 지정하거나, 테이블 생성 후 `CREATE PRIMARY KEY INDEX` 문으로 생성합니다.

```sql
CREATE TRANSACTION TABLE inventory (
    item_id   LONG,
    warehouse VARCHAR(32),
    qty       INTEGER,
    updated_at DATETIME
);

CREATE PRIMARY KEY INDEX idx_pk_inventory ON inventory(item_id);
```

고유해야 하는 컬럼이나 컬럼 조합에는 테이블 생성 후 UNIQUE INDEX를 생성합니다. 컬럼 정의에
`UNIQUE`를 붙이거나 `UNIQUE(column)` 제약조건을 선언하는 문법은 지원하지 않습니다.

```sql
CREATE UNIQUE INDEX uidx_product_catalog_name
ON product_catalog(name);
```

조회, UPDATE, DELETE 조건에 자주 사용하는 컬럼에는 일반 인덱스를 생성합니다.

```sql
CREATE INDEX idx_inventory_warehouse ON inventory(warehouse);
CREATE INDEX idx_order_status_time ON order_history(status, order_time);
```

UNIQUE INDEX의 중복 및 NULL 처리는
[UNIQUE INDEX 생성과 동작](/dbms/rdb-table-usage/index-performance/#unique-index-rdb)에서,
일반 인덱스 설계 기준은
[인덱스와 성능](/dbms/rdb-table-usage/index-performance/)에서
다룹니다.

<a id="create-rdb-auto-increment"></a>

## AUTO_INCREMENT 사용

자동 증가 키가 필요한 경우 `LONG PRIMARY KEY AUTO_INCREMENT`를 사용합니다.

```sql
CREATE TRANSACTION TABLE device_master (
    id          LONG PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(80),
    site_code   VARCHAR(32),
    created_at  DATETIME
);
```

`AUTO_INCREMENT` 컬럼은 단일 64비트 정수 PRIMARY KEY에 사용합니다. INSERT 방식과 catalog 확인 방법은 [AUTO_INCREMENT](/dbms/rdb-table-usage/auto-increment/)에서 다룹니다.

<a id="alter-rdb-table"></a>

## TRANSACTION 테이블 변경

TRANSACTION 테이블은 컬럼 추가·삭제, 컬럼 이름 변경, 테이블 이름 변경을 지원합니다.
TRANSACTION 테이블에서는 `MODIFY COLUMN`을 사용하지 않습니다.

### 컬럼 추가

`ADD COLUMN`의 컬럼 정의는 괄호로 묶습니다. `DEFAULT`를 지정하면 기존 row에도 기본값이
적용됩니다.

```sql
ALTER TABLE product_catalog
ADD COLUMN (stock_qty INTEGER DEFAULT 0);
```

### 컬럼 삭제

```sql
ALTER TABLE product_catalog
DROP COLUMN (stock_qty);
```

PRIMARY KEY, UNIQUE INDEX, 일반 인덱스, JSON path 인덱스가 참조하는 컬럼은 바로 삭제할 수
없습니다. 해당 인덱스를 먼저 삭제한 뒤 컬럼을 삭제합니다. 테이블의 마지막 컬럼은 삭제할 수
없습니다.

```sql
DROP INDEX idx_inventory_warehouse;
ALTER TABLE inventory DROP COLUMN (warehouse);
```

### 컬럼과 테이블 이름 변경

```sql
ALTER TABLE product_catalog RENAME COLUMN name TO product_name;
ALTER TABLE product_catalog RENAME TO product_master;
```

이름을 변경해도 기존 row와 TRANSACTION 인덱스 정의는 유지됩니다. VIEW가 TRANSACTION 테이블이나 대상 컬럼을
참조하고 있으면 VIEW 정의가 깨지지 않도록 관련 `ALTER TABLE`과 `DROP TABLE`이 거부됩니다.
의존 VIEW를 먼저 삭제하거나 변경한 뒤 DDL을 실행합니다.

<a id="drop-rdb-table"></a>

## TRANSACTION 테이블 삭제

테이블을 삭제하려면 `DROP TABLE`을 사용합니다.

```sql
DROP TABLE product_master;
```

`DROP TABLE`은 테이블 정의, 데이터, 관련 인덱스를 삭제합니다. 운영 데이터는 삭제 전에 백업 또는 내보내기 절차를 먼저 수행합니다.

<a id="rdb-ddl-operation-notes"></a>

## DDL 운영 주의사항

- DDL은 운영 중인 DML과 충돌할 수 있으므로 변경 시간대를 분리합니다.
- 장시간 열린 트랜잭션이 있으면 DDL이 지연되거나 실패할 수 있습니다.
- 열린 TRANSACTION 결과 커서가 있으면 관련 DDL이 실패할 수 있으므로 커서를 닫은 뒤 실행합니다.
- TRANSACTION 테이블은 Standard Edition 전용입니다.
- TRANSACTION 테이블에는 TAG 전용 `METADATA`, `BASETIME`, `BASEDISTANCE` 절을 사용할 수 없습니다.
- DDL 변경 후에는 TRANSACTION 테이블의 백업 및 복원 검증 절차도 갱신합니다.

### 컬럼 DDL 실패 후 복구

`ADD COLUMN`과 `DROP COLUMN`은 catalog와 TRANSACTION 저장소를 함께 변경합니다. 서버 종료,
디스크 오류 등으로 작업이 중단되면 서버는 재시작 시 남은 DDL 상태를 검사하고 이전 스키마로
되돌리거나 완료된 변경을 정리합니다. 복구가 끝나기 전에는 같은 테이블의 DDL을 반복 실행하지
마십시오.

복구 후에는 다음 항목을 확인합니다.

1. `DESC table_name`으로 컬럼 구성을 확인합니다.
2. `SELECT`와 대표 `INSERT`를 실행해 기존 행과 새 행을 확인합니다.
3. 컬럼을 참조하는 인덱스와 VIEW가 정상인지 확인합니다.
4. 서버 로그에 DDL 복구 오류가 남아 있으면 추가 DDL을 중단하고 백업 상태를 점검합니다.

데이터 디렉터리의 저장 파일은 사용자가 직접 이동, 수정하거나 삭제하지 마십시오.
