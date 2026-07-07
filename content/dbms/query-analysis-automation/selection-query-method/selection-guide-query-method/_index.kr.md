---
type: docs
title: '조회 방식 선택 가이드'
weight: 10
---

분석 목적별로 최적의 조회 방식을 선택하는 기준을 정리합니다.

## 목적별 선택

### 최근 데이터 조회

```sql
-- 최근 1시간 데이터 (DURATION 권장)
SELECT name, time, value FROM tag DURATION 1 HOUR;

-- 특정 시간 범위 (WHERE 시간 조건)
SELECT name, time, value FROM tag
WHERE time BETWEEN '2024-01-15 00:00:00' AND '2024-01-15 23:59:59';
```

### 집계 분석

```sql
-- 태그별 1시간 평균 (GROUP BY)
SELECT name, DATE_TRUNC('hour', time) AS h, AVG(value)
FROM tag
GROUP BY name, h
ORDER BY name, h;

-- 사전 계산된 분 단위 집계 (ROLLUP, 더 빠름)
SELECT * FROM rollup(tag, '1 min', '2024-01-15', '2024-01-16');
```

### 여러 태그를 컬럼으로 배열

```sql
-- PIVOT으로 태그를 컬럼화
SELECT * FROM (SELECT time, name, value FROM tag DURATION 1 HOUR)
PIVOT (AVG(value) FOR name IN ('TEMP-01', 'TEMP-02', 'PRESS-01'));
```

### 결측 구간 채우기

```sql
-- INTERPOLATION 힌트로 누락 구간 선형 보간
SELECT /*+ INTERPOLATION(time) */ name, time, value
FROM tag DURATION 1 HOUR;
```

### 설정 정보 JOIN

```sql
-- TAG 데이터와 LOOKUP 설정을 JOIN
SELECT t.name, t.time, t.value, l.location, l.dept
FROM tag t
LEFT JOIN device_meta l ON t.name = l.sensor_id
WHERE t.time BETWEEN '2024-01-15 00:00:00' AND '2024-01-15 12:00:00';
```

### 실시간 변환·적재 자동화

STREAM을 사용하면 데이터가 삽입될 때마다 자동으로 쿼리가 실행되어 다른 테이블로 적재합니다. 상세는 [STREAM](../automation/stream/)을 참고하세요.
