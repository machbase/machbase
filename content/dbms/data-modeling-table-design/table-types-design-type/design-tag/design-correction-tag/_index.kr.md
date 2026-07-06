---
type: docs
title: '데이터 보정 설계'
weight: 100
---

TAG 테이블은 UPDATE를 지원하지 않으므로, 잘못 입력된 데이터를 수정하려면 별도의 보정 컬럼이나 패턴을 사용합니다.

## 보정 플래그 패턴

원본 값과 보정 값을 모두 저장하고, 쿼리 시 보정 값을 우선 사용합니다.

```sql
CREATE TAG TABLE sensor_data (
    name          VARCHAR(64) PRIMARY KEY,
    time          DATETIME    BASETIME,
    raw_value     DOUBLE,       -- 원본 계측값
    corrected     DOUBLE,       -- 보정값 (NULL이면 raw_value 사용)
    is_corrected  SHORT         -- 0=원본, 1=보정됨
);

-- 조회 시 보정값 우선 사용
SELECT name, time,
       CASE WHEN corrected IS NOT NULL THEN corrected ELSE raw_value END AS value
FROM sensor_data
WHERE name = 'sensor-01'
  AND time >= NOW - 3600000000000;
```

## 보정 이력 테이블 패턴

보정 이력을 별도 LOG 테이블에 기록합니다.

```sql
-- 보정 이력
CREATE TABLE correction_log (
    sensor_name VARCHAR(64),
    target_time DATETIME,
    old_value   DOUBLE,
    new_value   DOUBLE,
    reason      VARCHAR(256),
    corrected_by VARCHAR(64)
);
```

## 주의사항

- TAG 테이블 데이터는 물리적으로 수정할 수 없습니다.
- 보정이 빈번하게 필요한 데이터라면 TAG 테이블 대신 다른 타입을 고려합니다.
- 보정 컬럼을 추가하면 스토리지 사용량이 증가합니다.
