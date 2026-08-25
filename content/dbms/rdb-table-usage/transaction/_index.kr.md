---
title: '8.10 트랜잭션'
weight: 100
toc: true
---
TRANSACTION 테이블의 DML은 `BEGIN`, `COMMIT`, `ROLLBACK`으로 하나의 작업 단위로 묶을 수
있습니다. `BEGIN TRANSACTION`이 아니라 `BEGIN`을 사용합니다.

<a id="design-transaction-rdb"></a>

## 실행 예제

```sql
CREATE TRANSACTION TABLE txn_orders (
    order_id LONG PRIMARY KEY,
    item_id  LONG,
    qty      INTEGER,
    status   VARCHAR(16)
);

CREATE TRANSACTION TABLE txn_inventory (
    item_id LONG PRIMARY KEY,
    qty     INTEGER
);

CREATE TRANSACTION TABLE txn_reservations (
    order_id LONG PRIMARY KEY,
    item_id  LONG
);

INSERT INTO txn_inventory VALUES (42, 10);
INSERT INTO txn_reservations VALUES (1001, 42);

BEGIN;
INSERT INTO txn_orders VALUES (1001, 42, 1, 'ORDERED');
UPDATE txn_inventory SET qty = qty - 1 WHERE item_id = 42;
DELETE FROM txn_reservations WHERE order_id = 1001;
COMMIT;

BEGIN;
UPDATE txn_inventory SET qty = 0 WHERE item_id = 42;
ROLLBACK;

SELECT item_id, qty FROM txn_inventory;

DROP TABLE txn_reservations;
DROP TABLE txn_inventory;
DROP TABLE txn_orders;
```

## 트랜잭션 경계

- 활성 트랜잭션에서는 TRANSACTION 테이블의 DML과 SELECT를 수행합니다.
- LOG, TAG, LOOKUP, VOLATILE 쓰기와 DDL은 활성 TRANSACTION 트랜잭션과 섞지 않습니다.
- 중첩 `BEGIN`, Savepoint와 중첩 트랜잭션은 지원하지 않습니다.
- 일반 constraint 오류는 실패한 statement를 되돌립니다. 이후 처리 여부를 명확히 결정하고
  필요하면 `ROLLBACK`합니다.
- 연결이 종료되면 해당 세션의 열린 트랜잭션은 롤백됩니다.
- 열린 결과 커서가 있으면 `COMMIT` 또는 `ROLLBACK`이 실패할 수 있으므로 결과 집합을 먼저
  닫습니다.

## 운영 지침

- 장시간 열린 트랜잭션과 지나치게 큰 배치는 잠금 충돌과 복구 비용을 늘립니다.
- 재시도할 수 있는 작업 단위로 나누고, 성공한 범위를 애플리케이션에 기록합니다.
- AUTO COMMIT 여부와 트랜잭션 API는 드라이버별로 확인합니다.
- DDL과 백업 작업은 진행 중인 트랜잭션과 시간대를 분리합니다.

드라이버별 지원 범위는
[개발 도구 연동](/dbms/development-tools-integration/)을 참고하십시오.
