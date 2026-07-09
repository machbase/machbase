---
type: docs
title: '17.1.1.2.1 SAMPLING hint'
weight: 10
---

`SAMPLING` 힌트는 TAG 테이블의 대용량 시계열 데이터를 시간 구간별로 균일하게 샘플링해 반환합니다. 전체 데이터를 집계하지 않고 일부 대표 행만 빠르게 반환하므로 대시보드 트렌드 파악에 유용합니다.

> TAG 테이블 전용 힌트입니다. LOG, LOOKUP, VOLATILE 테이블에는 적용되지 않습니다.

## 문법

```sql
SELECT /*+ SAMPLING(time_column, 'interval', count) */ col1, col2, ...
  FROM tag_table
 WHERE ...;
```

| 매개변수 | 설명 |
|----------|------|
| `time_column` | BASETIME 컬럼 이름 |
| `'interval'` | 샘플링 시간 단위 (`'1 sec'`, `'1 min'`, `'1 hour'` 등) |
| `count` | 각 구간에서 반환할 최대 행 수 |

## 예시

```sql
-- 1시간 범위를 1분 단위로 샘플링 (구간당 1건)
SELECT /*+ SAMPLING(time, '1 min', 1) */ name, time, value
  FROM sensor_tag
 WHERE name = 'TEMP-01' DURATION 1 HOUR;

-- 24시간 데이터를 1시간 단위로 샘플링
SELECT /*+ SAMPLING(time, '1 hour', 1) */ name, time, value
  FROM sensor_tag
 WHERE name = 'TEMP-01' DURATION 1 DAY;

-- 여러 태그 동시 샘플링
SELECT /*+ SAMPLING(time, '5 min', 1) */ name, time, value
  FROM sensor_tag
 WHERE name IN ('TEMP-01', 'TEMP-02', 'PRESS-01') DURATION 1 DAY;
```

## SAMPLING vs ROLLUP

| 항목 | SAMPLING 힌트 | ROLLUP |
|------|--------------|--------|
| 동작 방식 | 구간별 N건 샘플 반환 | 구간별 AVG/MIN/MAX 집계 |
| 사전 계산 | X (조회 시 계산) | O (백그라운드 사전 계산) |
| 정확도 | 샘플 (근사치) | 정확한 집계 |
| 대시보드 활용 | 전체 추세 파악 | 정확한 통계 |
| 설정 필요 | X | O (CREATE ROLLUP 필요) |

**팁**: 실시간 대시보드에서 빠른 렌더링이 필요하면 SAMPLING, 정확한 집계 값이 필요하면 ROLLUP을 사용합니다.

## 주의사항

- 각 구간에서 실제 반환되는 행 수는 `count`이하이며, 데이터가 없는 구간은 행이 반환되지 않습니다.
- 샘플링은 임의성 없이 구간의 첫 번째 행부터 반환합니다.
- 정확한 통계(평균, 최솟값, 최댓값)가 필요하면 ROLLUP을 사용하십시오.

## 관련 문서

- [INTERPOLATION hint](../interpolation-hint/) — 누락 시간 구간 보간
- [SELECT hint syntax](../) — 전체 힌트 목록
- [ROLLUP syntax](../../rollup-syntax/) — 정확한 시간 단위 집계
