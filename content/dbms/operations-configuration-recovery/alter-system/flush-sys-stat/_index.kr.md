---
type: docs
title: '13.3.9 FLUSH SYS_STAT'
weight: 90
---

```sql
ALTER SYSTEM FLUSH SYS_STAT;
```

쿼리 최적화기(Query Optimizer)가 사용하는 시스템 통계 정보를 최신 상태로 갱신합니다.

## 동작 설명

Machbase의 쿼리 최적화기는 테이블 크기, 컬럼 분포, 인덱스 선택도 등의 통계 정보를 바탕으로 효율적인 실행 계획을 수립합니다. 이 통계 정보는 주기적으로 자동 갱신되지만, 대량의 데이터 변경이 있는 경우 통계가 현재 상태를 반영하지 못할 수 있습니다.

`FLUSH SYS_STAT`를 실행하면 현재 데이터 상태를 기반으로 통계 정보를 즉시 갱신합니다.

## 사용 시점

| 상황 | 설명 |
|---|---|
| 대량 데이터 적재 후 | 많은 양의 데이터가 추가된 직후 통계를 최신 상태로 갱신 |
| 쿼리 실행 계획이 비효율적일 때 | 최적화기가 오래된 통계를 기반으로 잘못된 계획을 선택할 때 |
| 성능 테스트 전 | 통계 기반의 일관된 실행 계획을 보장하기 위해 |

## 사용 예시

```sql
-- 대량 데이터 적재 후 통계 갱신
INSERT INTO sensor_log SELECT * FROM sensor_log_stage;
ALTER SYSTEM FLUSH SYS_STAT;

-- 갱신 후 실행 계획 확인
EXPLAIN SELECT * FROM sensor_log WHERE sensor_id = 'TAG_001';
```

> **참고**: 갱신 작업은 테이블 크기에 따라 수 초에서 수십 초가 걸릴 수 있습니다. 통계 갱신 중에도 서버는 정상적으로 쿼리를 처리합니다.
