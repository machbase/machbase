---
type: docs
title: '트랜잭션 설계'
weight: 50
---

RDB 테이블은 트랜잭션을 지원합니다. `BEGIN`, `COMMIT`, `ROLLBACK` 문을 사용하여 데이터 일관성을 보장합니다.

## 기본 트랜잭션

```sql
BEGIN;
INSERT INTO order_history VALUES (1001, 'CUST-001', 5, 49.99, NOW, 'PENDING');
INSERT INTO order_history VALUES (1002, 'CUST-001', 3, 29.99, NOW, 'PENDING');
COMMIT;
```

## 롤백

```sql
BEGIN;
INSERT INTO order_history VALUES (1003, 'CUST-002', 1, 9.99, NOW, 'PENDING');
-- 오류 발생 시
ROLLBACK;
```

## 트랜잭션 격리 수준

Machbase RDB 테이블은 기본적으로 READ COMMITTED 격리 수준을 사용합니다.

## 대량 INSERT 최적화

대량 데이터를 삽입할 때는 트랜잭션 단위를 적절히 조절합니다.

```sql
-- 배치 INSERT (트랜잭션당 1,000건)
BEGIN;
INSERT INTO order_history VALUES (...);
INSERT INTO order_history VALUES (...);
-- ... 1,000건
COMMIT;
```

## 주의사항

- 장시간 열린 트랜잭션은 잠금 충돌을 유발할 수 있습니다.
- 트랜잭션 중 DDL 실행은 피합니다.
- 네트워크 오류 등으로 트랜잭션이 종료되면 자동으로 롤백됩니다.
- AUTO COMMIT 모드에서는 각 DML이 개별 트랜잭션으로 처리됩니다.
