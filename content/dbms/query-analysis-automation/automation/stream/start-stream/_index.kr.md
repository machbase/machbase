---
type: docs
title: 'STREAM 시작과 중지'
weight: 30
---

## STREAM 시작

등록된 STREAM을 실행합니다.

```sql
EXEC STREAM_START(stream_name);
```

한 번 시작된 STREAM은 서버 재시작 후에도 계속 동작합니다. 재시작 시 마지막으로 처리한 RID 이후 데이터부터 이어서 처리합니다.

```sql
-- 등록된 STREAM 시작
EXEC STREAM_START('stream_realtime');
EXEC STREAM_START('stream_agg_10s');
```

## STREAM 중지

```sql
EXEC STREAM_STOP(stream_name);
```

중지된 STREAM은 데이터를 처리하지 않으며, 새로 입력된 데이터도 누적하지 않습니다. 재시작 후에는 중지 시점 이후에 입력된 데이터도 처리합니다.

```sql
EXEC STREAM_STOP('stream_realtime');
```

## 시작 확인

`V$STREAMS`에서 현재 상태를 확인합니다.

```sql
SELECT NAME, STATE, LAST_EX_TIME
FROM   V$STREAMS
WHERE  NAME = 'stream_realtime';
```

| STATE 값 | 의미 |
|----------|------|
| RUNNING | 실행 중 |
| STOPPED | 중지됨 |
| ERROR | 오류 발생 |

## 모든 STREAM 상태 확인

```sql
SELECT NAME, STATE, LAST_EX_TIME, ERROR_MSG
FROM   V$STREAMS
ORDER BY NAME;
```

오류가 있는 STREAM은 `ERROR_MSG` 컬럼에서 원인을 확인합니다.
