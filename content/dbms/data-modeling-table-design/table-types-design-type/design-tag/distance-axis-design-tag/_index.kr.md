---
type: docs
title: '거리축 TAG 테이블 설계'
weight: 20
---

거리축 TAG 테이블은 시간 대신 거리(위치)를 기준 축으로 사용합니다. 파이프라인 검사, 도로 센서, 레이더 등 위치 기반 데이터에 적합합니다.

## 구성

`BASETIME` 대신 `BASE DISTANCE` 키워드를 사용합니다.

```sql
CREATE TAG TABLE pipeline_inspection (
    name      VARCHAR(64) PRIMARY KEY,
    distance  DOUBLE      BASE DISTANCE,
    thickness DOUBLE,
    defect    SHORT
);
```

| 컬럼 역할 | 타입 | 키워드 |
|---------|------|--------|
| 태그 식별자 | `VARCHAR(n)` | `PRIMARY KEY` |
| 거리 | `DOUBLE` | `BASE DISTANCE` |
| 값 | 숫자형 등 | — |

## 사용 예시

```sql
-- 0~100m 구간 데이터 조회
SELECT name, distance, thickness
FROM pipeline_inspection
WHERE name = 'pipe-01'
  AND distance BETWEEN 0.0 AND 100.0
ORDER BY distance;

-- 특정 지점 근방 데이터
SELECT name, distance, defect
FROM pipeline_inspection
WHERE name = 'pipe-01'
  AND distance >= 50.0 AND distance <= 50.5;
```

## 시간축과의 차이

| 항목 | 시간축 (`BASETIME`) | 거리축 (`BASE DISTANCE`) |
|------|---------------------|------------------------|
| 축 타입 | `DATETIME` | `DOUBLE` |
| 단위 | 나노초 시각 | 미터, 킬로미터 등 임의 단위 |
| 정렬 | 시간 순서 | 거리 순서 |
| 주요 쿼리 | 시간 범위 | 거리 범위 |

## 주의사항

- `BASE DISTANCE` 컬럼은 `DOUBLE` 타입만 사용 가능합니다.
- 하나의 TAG 테이블에 `BASETIME`과 `BASE DISTANCE`를 동시에 지정할 수 없습니다.
