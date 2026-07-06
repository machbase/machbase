---
type: docs
title: 'TRUNCATE 정책'
weight: 40
---

TRUNCATE는 테이블의 모든 데이터를 빠르게 삭제하는 DDL 명령입니다. Machbase에서는 **LOG와 RDB 테이블에서만** 지원됩니다.

## 지원 테이블 확인

소스 코드(`qpvTruncateTable.c`) 기준으로 TRUNCATE는 LOG와 RDB 테이블에서만 허용됩니다. 다른 테이블 타입에 TRUNCATE를 실행하면 오류(`ERR_QP_TRUNCATE_NON_LOG_TABLE`)가 발생합니다.

| 테이블 타입 | TRUNCATE 지원 |
|------------|--------------|
| TAG | X |
| LOG | O |
| RDB | O |
| VOLATILE | X |
| LOOKUP | X |

## LOG 테이블 TRUNCATE

```sql
TRUNCATE TABLE sensor_log;
-- 테이블 구조는 유지되고 모든 데이터가 삭제됩니다.
```

## RDB 테이블 TRUNCATE

```sql
TRUNCATE TABLE orders;
-- 모든 주문 데이터 삭제. 테이블 스키마는 유지됩니다.
```

RDB 테이블의 TRUNCATE는 내부적으로 `DELETE FROM` 전체 행 삭제(`qrdDeleteAllRows`)로 구현됩니다.

## TRUNCATE vs DELETE 비교

| 항목 | TRUNCATE | DELETE (전체) |
|------|---------|---------------|
| 처리 방식 | DDL (단번에 처리) | DML (행 단위 처리) |
| 속도 | 빠름 | 느림 (대용량 시) |
| 롤백 | 불가 | 가능 (트랜잭션 내) |
| WHERE 조건 | 불가 | 가능 |
| 트리거 발생 | X | X |

## 주의 사항

- TRUNCATE는 되돌릴 수 없습니다. 실행 전 데이터 백업 여부를 반드시 확인하세요.
- TAG, VOLATILE, LOOKUP 테이블에 TRUNCATE를 실행하면 오류가 발생합니다. 이 경우 `DELETE FROM ... BEFORE NOW` (TAG/LOG) 또는 조건 없는 DELETE를 사용하세요.
- VOLATILE 테이블 전체 삭제: `DELETE FROM device_status;` (WHERE 없이 삭제 가능)
