---
type: docs
title: 'SAMPLING 힌트'
weight: 10
---

`SAMPLING` 힌트는 TAG 테이블의 대용량 시계열 데이터를 시간 구간별로 균일하게 샘플링하여 반환합니다. 대시보드에서 전체 추세를 빠르게 파악할 때 유용합니다.

## 구문

```sql
SELECT /*+ SAMPLING(time_column, interval, count) */ ...
FROM tag_table
WHERE ...;
```

- `time_column`: BASETIME 컬럼 이름
- `interval`: 샘플링 시간 단위 (`'1 sec'`, `'1 min'`, `'1 hour'` 등)
- `count`: 각 구간에서 반환할 최대 행 수

## 예시

```sql
-- 1시간 범위를 1분 단위로 샘플링 (구간당 1건)
SELECT /*+ SAMPLING(time, '1 min', 1) */ name, time, value
FROM tag
WHERE name = 'TEMP-01' DURATION 1 HOUR;

-- 24시간 데이터를 1시간 단위로 샘플링
SELECT /*+ SAMPLING(time, '1 hour', 1) */ name, time, value
FROM tag
WHERE name = 'TEMP-01' DURATION 1 DAY;
```

## SAMPLING vs ROLLUP

| 항목 | SAMPLING 힌트 | ROLLUP |
|------|-------------|--------|
| 동작 방식 | 구간별 N건 샘플 반환 | 구간별 AVG/MIN/MAX 집계 |
| 사전 계산 | X (조회 시 계산) | O (백그라운드 사전 계산) |
| 정확도 | 샘플 (근사치) | 정확한 집계 |
| 대시보드 활용 | 전체 추세 파악 | 정확한 통계 |

**팁**: 실시간 대시보드에서 빠른 렌더링이 필요하면 SAMPLING, 정확한 집계 값이 필요하면 ROLLUP을 사용하세요.
