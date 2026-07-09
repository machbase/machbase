---
type: docs
title: '5.12.2 데이터 보정 설계'
weight: 100
---

TAG 테이블의 실제 시계열 데이터는 `UPDATE`로 정정할 수 있습니다. 보정 이력을 남기거나
조회 시점의 보정 로직이 필요한 업무에서는 별도 보정 컬럼/이력 테이블 패턴을 함께 사용할
수 있습니다.

## 직접 UPDATE 패턴

잘못 적재된 값을 원본 TAG row에서 직접 수정합니다.

```sql
UPDATE sensor_data
   SET raw_value = 25.3,
       is_corrected = 1
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

UPDATE에는 태그 선택 조건과 BASETIME 조건이 필요합니다. `name`과 `time` 자체는 변경할 수
없습니다.

## 보정 플래그 패턴

원본 값과 보정 값을 모두 저장하고, 쿼리 시 보정 값을 우선 사용합니다. 원본 변경 이력까지
보존해야 하는 경우에 적합합니다.

```sql
CREATE TAG TABLE sensor_data (
    name          VARCHAR(64) PRIMARY KEY,
    time          DATETIME    BASETIME,
    raw_value     DOUBLE,
    corrected     DOUBLE,
    is_corrected  SHORT
);

SELECT name, time,
       CASE WHEN corrected IS NOT NULL THEN corrected ELSE raw_value END AS value
FROM sensor_data
WHERE name = 'sensor-01'
  AND time >= NOW - 3600000000000;
```

## 보정 이력 테이블 패턴

감사 추적이 필요하면 보정 내용을 별도 LOG/RDB 테이블에 기록합니다.

```sql
CREATE TABLE correction_log (
    sensor_name  VARCHAR(64),
    target_time  DATETIME,
    old_value    DOUBLE,
    new_value    DOUBLE,
    reason       VARCHAR(256),
    corrected_by VARCHAR(64)
);
```

## 주의사항

- 대량 UPDATE 전 동일 WHERE 조건으로 대상 row 수를 확인합니다.
- 이미 계산된 롤업을 사용하는 경우 UPDATE 후 `ROLLUP_REBUILD`를 계획합니다.
- 보정이 매우 빈번하고 이력 보존이 필수라면 보정 컬럼 또는 보정 이력 테이블을 함께 설계합니다.
