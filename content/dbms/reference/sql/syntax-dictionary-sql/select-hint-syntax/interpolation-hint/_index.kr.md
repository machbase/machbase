---
type: docs
title: '17.1.1.2.2 INTERPOLATION hint'
weight: 20
toc: true
---

`INTERPOLATION` 힌트는 TAG 테이블의 시계열 데이터에서 누락된 시간 구간을 수학적으로 보간해 채워 반환합니다. 센서 오류, 네트워크 장애 등으로 빠진 데이터 구간을 연속적인 시계열로 처리할 때 사용합니다.

> TAG 테이블 전용 힌트입니다. LOG, LOOKUP, VOLATILE 테이블에는 적용되지 않습니다.

## 문법

```sql
SELECT /*+ INTERPOLATION(time_column [method interval_ns]) */ col1, col2, ...
  FROM tag_table
 WHERE ...;
```

| 매개변수 | 설명 |
|----------|------|
| `time_column` | BASETIME 컬럼 이름 |
| `method` | 보간 방법: `LINEAR` (선형, 기본값), `PREV` (이전 값 유지) |
| `interval_ns` | 보간 간격 (나노초 단위) |

## 예시

### 기본 선형 보간

```sql
-- 1분 간격 데이터에서 누락 구간을 선형 보간
SELECT /*+ INTERPOLATION(time) */ name, time, value
  FROM sensor_tag
 WHERE name = 'TEMP-01' DURATION 1 HOUR;
```

### 보간 방법 명시

```sql
-- LINEAR: 앞뒤 값 사이를 직선으로 보간 (60초 간격)
SELECT /*+ INTERPOLATION(value LINEAR 60000000000) */
       name, time, value
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS');

-- PREV: 이전 값으로 채우기 (60초 간격)
SELECT /*+ INTERPOLATION(status_code PREV 60000000000) */
       name, time, status_code
  FROM sensor_tag
 WHERE name = 'STATUS-01' DURATION 1 HOUR;
```

### PIVOT과 조합

```sql
-- 보간 후 PIVOT으로 태그별 컬럼화
SELECT * FROM (
    SELECT /*+ INTERPOLATION(time) */ name, time, value
      FROM sensor_tag
     WHERE DURATION 1 HOUR
) PIVOT (AVG(value) FOR name IN ('TEMP-01', 'TEMP-02', 'PRESS-01'));
```

## 보간 방법

| 방법 | 설명 |
|------|------|
| `LINEAR` | 누락 구간의 앞뒤 실제 값을 직선으로 연결해 보간 |
| `PREV` | 누락 구간을 직전 실제 값으로 채움 |

- 누락 구간의 시작 또는 끝에 실제 데이터가 없으면 보간을 수행하지 않습니다.
- 시간 범위 조건(`DURATION`, `BETWEEN`)이 명시된 쿼리에서 동작합니다. 시간 범위 없이 사용하면 전체 데이터를 대상으로 하여 성능에 영향을 줄 수 있습니다.

## INTERPOLATION vs SERIES BY

| 항목 | INTERPOLATION 힌트 | SERIES BY |
|------|--------------------|-----------|
| 용도 | 누락 시간 구간 채우기 | 연속 조건 만족 구간 추출 |
| 대상 | TAG 테이블 | 모든 테이블 |
| 결과 | 보간된 행 자동 추가 | 조건 만족 행만 반환 |

## 관련 문서

- [SAMPLING hint](../sampling-hint/) — 시간 구간별 샘플링
- [SELECT hint syntax](../) — 전체 힌트 목록
- [SERIES BY syntax](../../series-syntax/) — 연속 구간 추출
