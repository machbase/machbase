---
type: docs
title: '트랜잭션 설계'
weight: 50
---

RDB 테이블은 트랜잭션을 지원합니다. `BEGIN`, `COMMIT`, `ROLLBACK` 문을 사용하여 INSERT·UPDATE·DELETE를 원자적으로 처리합니다.

## 기본 트랜잭션

```sql
BEGIN;
INSERT INTO orders VALUES (1001, 'CUST-001', 5, 49.99, 'PENDING');
INSERT INTO orders VALUES (1002, 'CUST-001', 3, 29.99, 'PENDING');
COMMIT;
```

## INSERT + UPDATE + DELETE 혼합

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

## 롤백

오류 발생 시 ROLLBACK으로 트랜잭션 전체를 취소합니다.

```sql
BEGIN;
UPDATE inventory SET qty = qty - 10 WHERE item_id = 42;
-- 오류 발생 시
ROLLBACK;
-- inventory는 변경 전 상태로 복원됨
```

## 대량 INSERT 최적화

대량 데이터를 삽입할 때는 트랜잭션 단위를 적절히 조절합니다.

```sql
-- 배치 INSERT (트랜잭션당 1,000건)
BEGIN;
INSERT INTO orders VALUES (...);
-- ... 1,000건 반복
COMMIT;
```

## 주의사항

- 장시간 열린 트랜잭션은 잠금 충돌을 유발할 수 있습니다.
- 트랜잭션 중 DDL 실행은 피합니다.
- 네트워크 오류 등으로 트랜잭션이 종료되면 자동으로 롤백됩니다.
- AUTO COMMIT 모드에서는 각 DML이 개별 트랜잭션으로 처리됩니다.
