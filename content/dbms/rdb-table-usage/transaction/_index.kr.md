---
title: '8.10 트랜잭션'
weight: 100
toc: true
---

TRANSACTION 테이블의 트랜잭션 사용법과 설계 지침을 다룹니다.


<a id="design-transaction-rdb"></a>

## 트랜잭션 설계

TRANSACTION 테이블은 `BEGIN`, `COMMIT`, `ROLLBACK`으로 INSERT·UPDATE·DELETE를 하나의 트랜잭션으로
처리할 수 있습니다. `BEGIN TRANSACTION` 같은 별도 구문은 사용하지 않습니다.

### 기본 트랜잭션

```sql
BEGIN;
INSERT INTO orders VALUES (1001, 'CUST-001', 5, 49.99, 'PENDING');
INSERT INTO orders VALUES (1002, 'CUST-001', 3, 29.99, 'PENDING');
COMMIT;
```

### INSERT + UPDATE + DELETE 혼합

```sql
BEGIN;
-- 새 주문 생성
INSERT INTO orders VALUES (1003, 'CUST-002', 1, 9.99, 'PENDING');
-- 재고 차감
UPDATE inventory SET qty = qty - 1 WHERE item_id = 1003;
-- 오래된 임시 예약 삭제
DELETE FROM reservations WHERE order_id = 1003;
COMMIT;
```

### 롤백

오류 발생 시 ROLLBACK으로 트랜잭션 전체를 취소합니다.

```sql
BEGIN;
UPDATE inventory SET qty = qty - 10 WHERE item_id = 42;
-- 오류 발생 시
ROLLBACK;
-- inventory는 변경 전 상태로 복원됨
```

### 트랜잭션 경계

- 활성 트랜잭션에서는 TRANSACTION 테이블의 DML과 SELECT를 수행합니다.
- LOG, TAG, LOOKUP, VOLATILE 테이블에 대한 쓰기와 DDL은 활성 TRANSACTION 테이블 트랜잭션 안에서
  차단됩니다. 비 TRANSACTION 테이블의 SELECT는 수행할 수 있습니다.
- 중첩 `BEGIN`은 지원하지 않습니다.
- 트랜잭션이 없는 상태의 `COMMIT`과 `ROLLBACK`은 변경 없이 성공합니다.
- 일반적인 constraint 오류는 실패한 statement만 되돌리고 트랜잭션은 유지합니다. 오류를
  확인한 뒤 후속 문을 실행하거나 명시적으로 `ROLLBACK`합니다.
- 연결이 종료되면 해당 세션의 활성 TRANSACTION 테이블 트랜잭션은 롤백됩니다.
- 같은 세션에 열린 TRANSACTION 결과 커서가 있으면 `COMMIT`과 `ROLLBACK`이
  `Resource busy (TRANSACTION)`로 실패합니다. 결과 집합을 닫은 뒤 다시 실행합니다.

### 대량 INSERT 처리

대량 데이터 삽입 시 트랜잭션 단위를 적절히 조절합니다.

```sql
-- 배치 INSERT (트랜잭션당 1,000건)
BEGIN;
INSERT INTO orders VALUES (...);
-- ... 1,000건 반복
COMMIT;
```

### 주의사항

- 장시간 열린 트랜잭션은 잠금 충돌을 유발할 수 있습니다.
- 트랜잭션 중 DDL 실행은 피합니다.
- 네트워크 오류 등으로 트랜잭션이 종료되면 자동으로 롤백됩니다.
- AUTO COMMIT 모드에서는 각 DML이 개별 트랜잭션으로 처리됩니다.
- Savepoint와 중첩 트랜잭션은 지원하지 않습니다.
- SDK의 `setAutoCommit(false)`, `BeginTransaction()` 같은 편의 API 지원 여부는 드라이버마다
  다릅니다. [SDK별 지원 범위](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-transaction-prepare-bind)를
  확인합니다.
