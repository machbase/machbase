---
type: docs
title: 'STREAM 생성과 삭제'
weight: 20
---

## STREAM 생성

저장 프로시저 `STREAM_CREATE`로 STREAM을 등록합니다. 생성 시점에 쿼리 유효성을 검사합니다.

```sql
EXEC STREAM_CREATE(stream_name, stream_query_string);
```

| 파라미터 | 설명 |
|----------|------|
| stream_name | STREAM 이름 (DB 내에서 유일해야 함) |
| stream_query_string | `INSERT INTO ... SELECT ... FROM log_table [BY n SECOND | BY USER]` |

### 즉시 실행 STREAM (주기 없음)

새 행이 입력될 때마다 실행됩니다. 집계 함수(SUM, AVG 등)는 사용할 수 없습니다.

```sql
EXEC STREAM_CREATE('stream_realtime',
  'INSERT INTO alert_log
   SELECT time, device_id, value
   FROM   sensor_log
   WHERE  value > 95.0');
```

### 주기적 실행 STREAM (BY n SECOND)

설정한 초 단위마다 그 사이에 입력된 데이터를 처리합니다. 집계 함수를 사용할 수 있습니다.

```sql
EXEC STREAM_CREATE('stream_agg_10s',
  'INSERT INTO sensor_summary
   SELECT device_id, AVG(value), MAX(value), COUNT(*)
   FROM   sensor_log
   GROUP BY device_id
   BY 10 SECOND');
```

### 사용자 호출 STREAM (BY USER)

`EXEC STREAM_EXECUTE`를 호출하기 전까지 실행되지 않습니다.

```sql
EXEC STREAM_CREATE('stream_on_demand',
  'INSERT INTO report_table
   SELECT department, SUM(sales)
   FROM   daily_log
   GROUP BY department
   BY USER');
```

## STREAM 삭제

```sql
EXEC STREAM_DROP(stream_name);
```

> 실행 중인 STREAM은 삭제할 수 없습니다. 먼저 `EXEC STREAM_STOP`으로 중지해야 합니다.

```sql
-- 올바른 순서
EXEC STREAM_STOP('stream_realtime');
EXEC STREAM_DROP('stream_realtime');
```

## 쿼리 작성 규칙

- `INSERT INTO target_table SELECT ... FROM source_log_table` 형태만 허용됩니다.
- 소스 테이블은 LOG 테이블이어야 합니다.
- 쿼리 문자열 내 작은따옴표는 두 번(`''`)으로 이스케이프합니다.
- `BY` 절은 쿼리 문자열의 가장 마지막에 위치합니다.
