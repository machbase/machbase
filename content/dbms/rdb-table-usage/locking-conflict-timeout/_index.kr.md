---
title: '8.11 잠금, 충돌, busy timeout'
weight: 110
toc: true
---

RDB 테이블의 동시 접근 방식과 쓰기 충돌, busy timeout 처리 방법을 설명합니다.

<a id="transaction-locking-conflict-rdb"></a>

## RDB 동시성과 잠금 범위

RDB 읽기 트랜잭션은 커밋된 스냅샷을 조회합니다. 다른 세션이 같은 RDB 테이블에 쓰기
트랜잭션을 열어 둔 상태에서
`INSERT`, `UPDATE`, `DELETE`를 실행하면 대기하거나 `Resource busy (RDB_TRANSACTION)` 오류가
발생할 수 있습니다.

RDB 잠금을 일반적인 행 단위 잠금으로 해석하면 안 됩니다. 서로 다른 행을 수정하더라도 같은
RDB 테이블에 대한 동시 쓰기는 충돌할 수 있습니다. 반면 다른 세션의 미커밋 쓰기가 있어도
읽기 트랜잭션은 커밋된 스냅샷을 조회할 수 있습니다.

| 상황 | 동작 |
|------|------|
| 같은 RDB 테이블의 동시 읽기 | 커밋된 스냅샷을 각각 조회합니다. |
| 다른 세션의 미커밋 쓰기 중 읽기 | 미커밋 행을 제외한 커밋 스냅샷을 조회합니다. |
| 같은 RDB 테이블의 동시 쓰기 | `RDB_BUSY_TIMEOUT_MS` 정책에 따라 대기하거나 실패합니다. |
| 활성 RDB 트랜잭션 중 같은 테이블 DDL | `Resource busy` 오류로 차단됩니다. |
| 열린 RDB 커서가 있는 세션의 `COMMIT`/`ROLLBACK` | 커서를 닫을 때까지 차단됩니다. |

RDB 트랜잭션 안에서는 RDB 테이블의 DML과 SELECT만 수행합니다. LOG, TAG, LOOKUP,
VOLATILE 테이블 쓰기와 DDL은 같은 RDB 트랜잭션에 포함할 수 없습니다.

## busy timeout 설정

`RDB_BUSY_TIMEOUT_MS`는 RDB 쓰기 충돌이 발생했을 때 세션이 기다리는 시간을 밀리초 단위로
지정합니다. 서버 설정의 기본값은 `30000`이며, 새 세션은 이 값을 복사합니다.

| 값 | 동작 |
|---:|------|
| `-1` | 세션 취소 또는 잠금 해제까지 계속 기다립니다. |
| `0` | 기다리지 않고 즉시 `Resource busy` 오류를 반환합니다. |
| 양수 | 지정한 밀리초 동안 기다린 뒤 오류를 반환합니다. |

현재 접속의 값을 변경하려면 다음 문을 실행합니다.

```sql
ALTER SESSION SET RDB_BUSY_TIMEOUT_MS = 5000;
```

설정 결과는 `V$SESSION`에서 확인합니다. SQL에서 현재 세션 ID를 반환하는 별도 함수는
제공하지 않으므로, 접속 사용자·클라이언트 주소·세션 ID를 함께 확인합니다.

```sql
SELECT id, user_name, user_ip, rdb_busy_timeout_ms
  FROM v$session
 WHERE closed = 0
 ORDER BY id;
```

장애를 빠르게 감지해야 하는 온라인 요청은 짧은 양수를 사용하고, 순차 배치처럼 선행
트랜잭션이 끝날 때까지 기다려도 되는 작업은 더 긴 값을 사용합니다. `-1`은 무기한 대기로
이어질 수 있으므로 취소와 상위 요청 timeout을 함께 구성합니다.

## 충돌 진단

RDB 쓰기 충돌은 `V$MUTEX`에 행 잠금으로 표시되지 않습니다. `V$MUTEX`는 서버 내부 뮤텍스
통계이므로 RDB 트랜잭션 잠금 소유자를 식별하는 용도로 사용하지 않습니다.

대기 중인 SQL과 접속 세션은 `V$STMT`, `V$SESSION`에서 확인합니다.

```sql
SELECT id, sess_id, state, query
  FROM v$stmt
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%';
```

```sql
SELECT id, user_name, user_ip, login_time, rdb_busy_timeout_ms
  FROM v$session
 WHERE closed = 0
 ORDER BY login_time;
```

위 조회만으로 잠금 소유 세션을 직접 매핑할 수는 없습니다. 애플리케이션 로그의 트랜잭션
시작 시각과 세션 ID, 서버 trace의 `RDB_TRANSACTION` busy 오류를 함께 확인합니다.

## 충돌 예방과 복구

1. `BEGIN` 후 필요한 RDB DML만 실행하고 즉시 `COMMIT` 또는 `ROLLBACK`합니다.
2. 외부 API 호출이나 긴 계산은 트랜잭션 밖에서 수행합니다.
3. 대량 UPDATE/DELETE는 대상 범위를 나누고 각 배치 사이에 커밋합니다.
4. 같은 RDB 테이블을 갱신하는 작업은 큐나 작업 분할 규칙으로 직렬화합니다.
5. `Resource busy (RDB_TRANSACTION)`는 제한된 횟수만 지수 백오프로 재시도합니다.
6. 연결이 비정상 종료되면 서버가 활성 RDB 트랜잭션을 롤백하지만, 클라이언트는 새 연결에서
   결과를 다시 조회해 반영 여부를 확인합니다.

```python
import time

def execute_with_retry(cursor, sql, max_retries=3):
    for attempt in range(max_retries):
        try:
            cursor.execute(sql)
            return
        except Exception as exc:
            if "RDB_TRANSACTION" not in str(exc) or attempt == max_retries - 1:
                raise
            time.sleep(0.1 * (2 ** attempt))
```

열린 커서 때문에 `COMMIT` 또는 `ROLLBACK`이 실패한 경우에는 해당 결과 집합과 statement를
먼저 닫은 뒤 트랜잭션 종료 문을 다시 실행합니다. 장시간 실행 세션을 종료해야 하면
`V$SESSION.ID`를 확인한 뒤 `ALTER SYSTEM KILL SESSION <session_id>`를 사용합니다. 강제 종료는
해당 세션의 미커밋 RDB 변경을 롤백하므로, 업무 영향과 대상 세션을 먼저 확인합니다.
