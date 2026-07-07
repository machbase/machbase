---
type: docs
title: 'INTERPOLATION 힌트'
weight: 20
---

`INTERPOLATION` 힌트는 TAG 테이블의 시계열 데이터에서 누락된 시간 구간을 자동으로 채워 반환합니다.

## 구문

```sql
SELECT /*+ INTERPOLATION(time_column) */ ...
FROM tag_table
WHERE ...;
```

## 기본 예시

```sql
-- 1분 간격 데이터에서 누락 구간을 선형 보간
SELECT /*+ INTERPOLATION(time) */ name, time, value
FROM tag
WHERE name = 'TEMP-01' DURATION 1 HOUR;
```

누락된 타임스탬프 구간에 대해 인접 값 사이를 선형 보간(linear interpolation)한 행이 자동으로 채워져 반환됩니다.

## INTERPOLATION과 함께 사용

```sql
-- 보간 + 특정 태그
SELECT /*+ INTERPOLATION(time) */ name, time, value
FROM tag
WHERE name IN ('TEMP-01', 'TEMP-02') DURATION 1 DAY;
```

## 보간 방식

- **선형 보간**: 앞뒤 실제 값 사이를 직선으로 보간
- 누락 구간의 시작/끝에 실제 데이터가 없으면 보간을 수행하지 않습니다.

## 활용 패턴

```sql
-- 보간 후 PIVOT으로 컬럼화
SELECT * FROM (
    SELECT /*+ INTERPOLATION(time) */ name, time, value
    FROM tag WHERE DURATION 1 HOUR
) PIVOT (AVG(value) FOR name IN ('TEMP-01', 'TEMP-02', 'PRESS-01'));
```

## INTERPOLATION vs SERIES BY

| 항목 | INTERPOLATION 힌트 | SERIES BY |
|------|-----------------|---------|
| 용도 | 누락 시간 구간 채우기 | 연속 조건 만족 구간 추출 |
| 대상 | TAG 테이블 | 모든 테이블 |
| 결과 | 보간된 행 자동 추가 | 조건 만족 행만 반환 |
