---
type: docs
title: 'STREAM procedure syntax'
weight: 180
---

STREAM은 사용자가 정의한 `INSERT ... SELECT ...` 쿼리를 서버 내부에 등록해 자동 실행하는 처리 객체입니다. 한 번 생성하고 시작하면 중지하거나 삭제할 때까지 백그라운드에서 계속 실행됩니다.

> Standard Edition 중심으로 설계되었습니다. Cluster Edition에서도 생성과 실행이 가능하지만, 복잡한 조인이나 서브쿼리를 포함한 SQL은 Cluster 환경에서 지원되지 않을 수 있습니다.

## STREAM_CREATE

STREAM을 생성합니다.

```sql
EXEC STREAM_CREATE(stream_name, 'insert_select_sql')
```

| 매개변수 | 설명 |
|----------|------|
| `stream_name` | STREAM 이름 (identifier) |
| `insert_select_sql` | 실행할 `INSERT INTO ... SELECT ...` SQL 문자열 |

```sql
-- LOG 테이블의 이상 이벤트를 TAG 테이블로 변환하는 STREAM 생성
EXEC STREAM_CREATE(alarm_to_tag,
    'INSERT INTO sensor_alerts
     SELECT ''ALARM_COUNT'', _arrival_time, COUNT(*)
       FROM device_log
      WHERE severity = ''CRITICAL''
        AND _arrival_time >= sysdate - 10s');
```

> SQL 문자열 내부의 문자열 리터럴은 작은따옴표를 두 번(`''`) 사용해 이스케이프합니다.

## STREAM_START

등록된 STREAM을 시작합니다.

```sql
EXEC STREAM_START(stream_name)
```

```sql
EXEC STREAM_START(alarm_to_tag);
```

- 시작 후 백그라운드에서 `INSERT ... SELECT ...` 쿼리를 반복 실행합니다.
- 이미 실행 중인 STREAM에 대해 호출하면 오류 없이 무시됩니다.

## STREAM_STOP

실행 중인 STREAM을 중지합니다.

```sql
EXEC STREAM_STOP(stream_name)
```

```sql
EXEC STREAM_STOP(alarm_to_tag);
```

- 중지해도 STREAM 정의는 유지되며, 이후 `STREAM_START`로 재시작할 수 있습니다.

## STREAM_DESTROY

STREAM 정의를 삭제합니다.

```sql
EXEC STREAM_DESTROY(stream_name)
```

```sql
EXEC STREAM_DESTROY(alarm_to_tag);
```

- 실행 중인 STREAM은 먼저 `STREAM_STOP`으로 중지한 뒤 삭제해야 합니다.

## 전체 예시

```sql
-- 1. STREAM 생성
EXEC STREAM_CREATE(log_to_tag,
    'INSERT INTO error_count (name, time, value)
     SELECT ''error-rate'', _arrival_time, COUNT(*)
       FROM app_log
      WHERE level = ''ERROR''
        AND _arrival_time >= sysdate - 60s
     GROUP BY _arrival_time');

-- 2. STREAM 시작
EXEC STREAM_START(log_to_tag);

-- 3. 필요 시 중지
EXEC STREAM_STOP(log_to_tag);

-- 4. 재시작
EXEC STREAM_START(log_to_tag);

-- 5. 영구 삭제
EXEC STREAM_STOP(log_to_tag);
EXEC STREAM_DESTROY(log_to_tag);
```

## STREAM 상태 확인

```sql
SELECT * FROM v$stream;
```

## ROLLUP과의 차이

| 항목 | ROLLUP | STREAM |
|------|--------|--------|
| 대상 테이블 | TAG 테이블 전용 | 임의 테이블 (LOG, TAG, LOOKUP 등) |
| 집계 단위 | SEC / MIN / HOUR 고정 | 사용자가 SQL로 자유롭게 정의 |
| 결과 저장 | 내부 ROLLUP 테이블 | 사용자 지정 대상 테이블 |
| 변환 로직 | 고정 (SUM, COUNT, MIN, MAX, FIRST, LAST) | 임의 SQL (JOIN, 조건 필터 등) |

## 관련 문서

- [STREAM 처리 모델](/dbms/core-concepts/features-concepts/processing-model-stream/) — 개념 및 사용 사례
- [ROLLUP syntax](../rollup-syntax/) — 자동 집계 메커니즘
