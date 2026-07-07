---
type: docs
title: 'STREAM 처리 모델'
weight: 20
---

STREAM은 Machbase DBMS에서 입력 데이터를 자동으로 변환하거나 집계해 다른 테이블에 저장하는 처리 객체입니다. 사용자가 정의한 `INSERT ... SELECT ...` 쿼리를 서버 내부 스트림으로 등록하고, 시작(START)한 뒤 중지(STOP)하거나 삭제(DROP)할 때까지 동작합니다.

## STREAM이란

STREAM을 한 문장으로 정의하면 "지정한 `INSERT ... SELECT ...` 변환 쿼리를 서버 내부에 등록해 자동 실행하는 객체"입니다. 데이터베이스 서버 내부에서 배경 스레드로 동작하므로, 한 번 생성하고 시작하면 중지하거나 삭제할 때까지 계속 실행됩니다.

```sql
-- STREAM 생성 예시: LOG 테이블의 이상 이벤트를 TAG 테이블로 변환
EXEC STREAM_CREATE(alarm_to_tag,
    'INSERT INTO sensor_alerts SELECT ''ALARM_COUNT'', _arrival_time, value FROM device_log WHERE severity = ''CRITICAL''');

-- 시작
EXEC STREAM_START(alarm_to_tag);

-- 중지
EXEC STREAM_STOP(alarm_to_tag);

-- 삭제
EXEC STREAM_DROP(alarm_to_tag);
```

## ROLLUP과의 차이

ROLLUP과 STREAM은 모두 데이터를 가공해 다른 형태로 저장한다는 점에서 비슷해 보이지만, 역할과 적용 범위가 다릅니다.

| 항목 | ROLLUP | STREAM |
| --- | --- | --- |
| 대상 테이블 | TAG 테이블 전용 | 임의 테이블 (LOG, TAG, LOOKUP 등) |
| 집계 단위 | SEC / MIN / HOUR 고정 | 사용자가 SQL로 자유롭게 정의 |
| 결과 저장 위치 | 내부 ROLLUP 테이블 | 사용자가 지정한 대상 테이블 |
| 변환 로직 | 고정 (SUM, COUNT, MIN, MAX, FIRST, LAST) | 임의 SQL (JOIN, 조건 필터, 문자열 변환 등) |
| 설정 방법 | `WITH ROLLUP` 절로 테이블 생성 시 지정 | `EXEC STREAM_CREATE`로 별도 생성 |

## 주요 사용 사례

**LOG → TAG 변환**

비정형 이벤트 로그에서 특정 조건을 만족하는 이벤트를 집계해 TAG 테이블의 계측값으로 변환합니다. 예를 들어 10초마다 로그에서 오류 건수를 세어 TAG 테이블에 저장하면, ROLLUP과 결합해 시간별 오류율 트렌드를 빠르게 조회할 수 있습니다.

**파생 집계 테이블 생성**

원시 데이터를 ROLLUP이 지원하지 않는 사용자 정의 시간 구간(예: 15분, 30분)으로 집계해 별도 테이블에 저장합니다.

**데이터 정제 및 필터링**

수집 단계에서 들어온 노이즈 데이터나 이상값을 필터링하고, 정제된 값만 TAG 테이블에 적재합니다.

## Cluster Edition 주의사항

STREAM은 Standard Edition 중심으로 설계되었습니다. Cluster Edition에서도 STREAM 생성과 실행이 가능하지만, 복잡한 조인이나 서브쿼리를 포함한 SQL은 Cluster 환경에서 지원되지 않을 수 있습니다. Cluster Edition에서 STREAM을 사용하려면 대상 SQL을 Cluster 환경에서 먼저 검증하십시오.

## 다음 읽을 내용

- [ROLLUP 통계의 역할](../role-statistics-rollup/) — 자동 집계 메커니즘의 상세 내용
- [ROLLUP vs STREAM](/dbms/core-concepts/terminology-distinction/rollup-vs-stream/) — 두 기능의 차이와 선택 기준
- [Retention Policy의 역할](../role-retention-policy/) — 자동 데이터 삭제 정책 개념
