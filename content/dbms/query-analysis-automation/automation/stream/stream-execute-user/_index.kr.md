---
type: docs
title: 'BY USER와 STREAM_EXECUTE'
weight: 40
---

`BY USER`로 생성된 STREAM은 사용자가 명시적으로 `EXEC STREAM_EXECUTE`를 호출해야만 실행됩니다. 배치 처리 완료 시점이나 특정 이벤트 발생 시 집계를 트리거하는 패턴에 적합합니다.

## 생성

```sql
EXEC STREAM_CREATE('stream_on_demand',
  'INSERT INTO hourly_report
   SELECT DATE_TRUNC(''hour'', time), device_id, SUM(value), COUNT(*)
   FROM   sensor_log
   GROUP BY 1, device_id
   BY USER');

EXEC STREAM_START('stream_on_demand');
```

`STREAM_START` 없이는 `STREAM_EXECUTE`를 호출해도 실행되지 않습니다.

## 수동 실행

```sql
EXEC STREAM_EXECUTE(stream_name);
```

호출 시 마지막 실행 이후 새로 추가된 증분 데이터에 대해서만 쿼리가 실행됩니다. 이전에 처리한 데이터는 다시 처리하지 않습니다.

```sql
-- 배치 로드 완료 후 수동 집계 실행
EXEC STREAM_EXECUTE('stream_on_demand');
```

## BY USER vs 주기 실행 비교

| 항목 | BY n SECOND | BY USER |
|------|-------------|---------|
| 실행 시점 | 매 n초 자동 실행 | 명시적 호출 시만 실행 |
| 적용 사례 | 실시간 집계 | 배치 완료 트리거, 테스트 |
| 집계 함수 | 사용 가능 | 사용 가능 |

## 주의사항

- `BY USER` STREAM이 START 상태가 아닌데 EXECUTE를 호출하면 오류가 발생합니다.
- `BY USER` 없이 일반 쿼리(주기 없음)로 생성된 STREAM에 EXECUTE를 호출하면 오류가 발생합니다.

```sql
-- 실행 전 상태 확인
SELECT NAME, STATE FROM V$STREAMS WHERE NAME = 'stream_on_demand';
-- STATE = 'RUNNING' 이어야 EXECUTE 가능
```
