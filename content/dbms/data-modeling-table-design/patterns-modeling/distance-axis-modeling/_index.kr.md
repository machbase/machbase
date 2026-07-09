---
type: docs
title: '4.3.2 거리축 모델링'
weight: 20
---

거리(위치)를 기준 축으로 하는 데이터 모델링 패턴입니다. 파이프라인 검사, 도로 센서, 레이저 스캔 등에 적용합니다.

## 기본 패턴

```sql
CREATE TAG TABLE pipeline_thickness (
    pipe_id   VARCHAR(32) PRIMARY KEY,
    distance  DOUBLE      BASEDISTANCE,    -- 단위: 미터
    thickness DOUBLE,
    temp      DOUBLE
);
```

## 구간 데이터 조회

```sql
-- 파이프 ID별 0~50m 구간 데이터 조회
SELECT pipe_id, distance, thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
  AND distance BETWEEN 0.0 AND 50.0
ORDER BY distance;

-- 임계치 이하 구간 조회
SELECT pipe_id, distance, thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
  AND thickness < 8.0   -- 두께가 8mm 미만인 구간
ORDER BY distance;
```

## 거리 기반 집계

```sql
-- 10m 구간별 평균 두께
SELECT pipe_id,
       FLOOR(distance / 10.0) * 10 AS segment_start,
       AVG(thickness) AS avg_thickness,
       MIN(thickness) AS min_thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
GROUP BY pipe_id, FLOOR(distance / 10.0) * 10
ORDER BY segment_start;
```

## 시간 + 거리 복합 모델링

검사 시각과 위치를 함께 관리해야 하는 경우, 시간축 TAG 테이블에 거리 컬럼을 추가합니다.

```sql
-- 시간축 + 위치 정보 함께 저장
CREATE TAG TABLE inspection_data (
    inspector  VARCHAR(64) PRIMARY KEY,
    time       DATETIME    BASETIME,
    distance   DOUBLE,      -- 위치 컬럼 (축은 아님)
    thickness  DOUBLE,
    defect     SHORT
);

-- 특정 날짜·구간 조회
SELECT inspector, time, distance, thickness
FROM inspection_data
WHERE inspector = 'INSPECTOR-01'
  AND time BETWEEN '2024-01-01' AND '2024-01-02'
  AND distance BETWEEN 100.0 AND 200.0
ORDER BY time;
```
