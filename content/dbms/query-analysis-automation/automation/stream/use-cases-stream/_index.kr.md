---
type: docs
title: 'STREAM 활용 사례'
weight: 10
---

STREAM은 데이터가 입력되는 시점에 자동으로 변환·필터링·집계를 처리합니다. 별도의 애플리케이션 없이 DB 레벨에서 실시간 파이프라인을 구성할 수 있습니다.

## 사례 1: 이벤트 필터링

원본 로그에서 특정 조건의 이벤트만 별도 테이블로 분리합니다.

```sql
-- 에러 이벤트만 분리
EXEC STREAM_CREATE('stream_error_filter',
  'INSERT INTO error_log
   SELECT time, source, message
   FROM   event_log
   WHERE  level = ''ERROR''');

EXEC STREAM_START('stream_error_filter');
```

## 사례 2: 실시간 1분 집계

매 60초마다 원본 데이터를 집계해 요약 테이블을 갱신합니다.

```sql
EXEC STREAM_CREATE('stream_agg_1min',
  'INSERT INTO event_summary
   SELECT source, COUNT(*), AVG(duration)
   FROM   event_log
   GROUP BY source
   BY 60 SECOND');

EXEC STREAM_START('stream_agg_1min');
```

## 사례 3: 데이터 변환 (ETL)

원본 테이블의 컬럼을 가공해 다른 테이블로 이동합니다.

```sql
EXEC STREAM_CREATE('stream_etl',
  'INSERT INTO processed_log
   SELECT time, UPPER(source), value * 1000
   FROM   raw_log
   WHERE  value IS NOT NULL');

EXEC STREAM_START('stream_etl');
```

## 사례 4: 수동 실행 (BY USER)

배치 작업이 완료된 시점에 명시적으로 집계를 트리거합니다.

```sql
-- BY USER 스트림 생성
EXEC STREAM_CREATE('stream_batch_aggr',
  'INSERT INTO batch_result
   SELECT DATE_TRUNC(''hour'', time), SUM(amount)
   FROM   transaction_log
   GROUP BY 1
   BY USER');

EXEC STREAM_START('stream_batch_aggr');

-- 배치 완료 후 수동 실행
EXEC STREAM_EXECUTE('stream_batch_aggr');
```

## 사례 5: 멀티 스트림 파이프라인

여러 STREAM을 연결해 단계적 처리를 구성합니다.

```
raw_log → stream_filter → filtered_log → stream_agg_1min → summary_log
```

```sql
-- 1단계: 필터
EXEC STREAM_CREATE('stream_s1',
  'INSERT INTO filtered_log SELECT * FROM raw_log WHERE status > 0');

-- 2단계: 집계
EXEC STREAM_CREATE('stream_s2',
  'INSERT INTO summary_log
   SELECT DATE_TRUNC(''minute'', time), COUNT(*), AVG(value)
   FROM   filtered_log GROUP BY 1
   BY 60 SECOND');

EXEC STREAM_START('stream_s1');
EXEC STREAM_START('stream_s2');
```
