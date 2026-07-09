---
type: docs
title: 'RDB 트랜잭션/잠금 충돌'
weight: 40
---

Machbase의 RDB 테이블(일반 테이블)은 표준 RDBMS와 마찬가지로 트랜잭션과 잠금(lock)을 지원합니다. 여러 세션이 같은 행에 동시에 쓰기 작업을 시도하거나, 트랜잭션을 오랫동안 완료하지 않으면 잠금 충돌이 발생해 다른 세션이 대기 상태에 빠질 수 있습니다.

> **참고:** TAG 테이블과 LOG 테이블은 Append 전용 구조로 트랜잭션 잠금이 없습니다. 잠금 충돌은 RDB 테이블(일반 테이블)에서만 발생합니다.

## 잠금 충돌이 발생하는 상황

- 여러 세션이 같은 RDB 테이블의 동일 행에 동시에 `UPDATE` 또는 `DELETE` 실행
- `BEGIN TRANSACTION` 이후 `COMMIT`이나 `ROLLBACK` 없이 장시간 방치
- 배치 작업이 대용량 `UPDATE`를 실행하는 동안 다른 세션이 같은 테이블에 접근
- 클라이언트 프로그램 오류로 트랜잭션이 열린 채 연결이 끊어진 경우

## 잠금 현황 확인

### 잠금을 보유한 세션 확인

```sql
SELECT * FROM v$mutex;
```

`v$mutex`에 항목이 있다면 현재 잠금을 보유 중인 세션이 있는 것입니다.

### 대기 중인 세션 확인

```sql
SELECT sess_id, state, query FROM v$stmt WHERE state = 'WAIT';
```

`state`가 `WAIT`인 세션이 있다면 다른 세션의 잠금 해제를 기다리고 있는 것입니다.

### 전체 세션 상태 확인

```sql
SELECT s.id AS session_id, s.login_time, s.user_name, s.user_ip,
       st.id AS stmt_id, st.state AS stmt_state, st.query
FROM v$session s
LEFT JOIN v$stmt st ON s.id = st.sess_id
ORDER BY s.id;
```

## 장시간 트랜잭션 강제 종료

잠금을 오래 보유한 세션의 session id를 확인한 뒤 강제로 종료합니다.

```sql
-- 잠금 보유 세션 확인
SELECT * FROM v$mutex;

-- 해당 세션 강제 종료
ALTER SYSTEM KILL SESSION <sess_id>;
```

`KILL SESSION`은 실행 중인 트랜잭션을 자동으로 롤백하고 세션을 종료합니다. 이후 대기 중이던 세션이 잠금을 획득하여 작업을 재개합니다.

## 예방 방법

### 1. 트랜잭션 범위 최소화

트랜잭션 내에서 처리하는 작업을 최소화하고, 작업 완료 즉시 `COMMIT`합니다.

```sql
-- 나쁜 예: 트랜잭션 내에서 오랜 처리
BEGIN TRANSACTION;
-- 복잡한 계산이나 외부 API 호출...
UPDATE sensor_meta SET status = 'done' WHERE id = 1;
COMMIT;

-- 좋은 예: 계산은 트랜잭션 밖에서, 쓰기만 트랜잭션 내에서
-- (복잡한 계산 먼저 수행)
BEGIN TRANSACTION;
UPDATE sensor_meta SET status = 'done' WHERE id = 1;
COMMIT;
```

### 2. 적절한 autocommit 설정

애플리케이션에서 autocommit을 활성화하면 각 DML 문이 자동으로 커밋됩니다. 명시적인 트랜잭션이 필요한 경우에만 `BEGIN TRANSACTION`을 사용합니다.

### 3. 동시 업데이트 피하기

여러 스레드나 프로세스가 같은 행을 동시에 갱신하는 설계를 피합니다.

- 갱신 대상 행이 겹치지 않도록 파티셔닝합니다.
- 큐(queue) 구조를 활용해 순차적으로 처리합니다.

### 4. 클라이언트 예외 처리

클라이언트 프로그램에서 예외가 발생했을 때 반드시 `ROLLBACK` 또는 연결 종료 처리를 하여 열린 트랜잭션이 남지 않도록 합니다.

```python
# Python 예시
try:
    conn.execute("BEGIN TRANSACTION")
    conn.execute("UPDATE sensor_meta SET status = 'done' WHERE id = 1")
    conn.execute("COMMIT")
except Exception as e:
    conn.execute("ROLLBACK")  # 반드시 롤백 처리
    raise
```

## TAG/LOG 테이블과의 차이

| 항목 | RDB 테이블 | TAG/LOG 테이블 |
|------|-----------|----------------|
| 트랜잭션 지원 | O | X |
| 잠금(Lock) | O | X |
| UPDATE/DELETE | O | 제한적 |
| 잠금 충돌 가능성 | O | X |

TAG 테이블과 LOG 테이블은 Append 구조로 설계되어 잠금 충돌이 발생하지 않습니다. 대량의 시계열 데이터를 빠르게 입력해야 하는 경우 TAG 또는 LOG 테이블 사용을 권장합니다.
