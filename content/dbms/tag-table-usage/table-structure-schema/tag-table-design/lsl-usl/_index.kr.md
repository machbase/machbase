---
type: docs
title: '5.2.1.6 LSL·USL 설계'
weight: 110
---

품질 관리나 설비 모니터링에서는 하한 규격값(LSL, Lower Specification Limit)과 상한 규격값(USL, Upper Specification Limit)을 함께 저장하여 이상 감지에 활용합니다.

## METADATA에 LSL·USL 저장

태그별로 고정된 규격값은 `LOWER LIMIT`과 `UPPER LIMIT` METADATA 컬럼에 저장합니다. 이
제약은 `SUMMARIZED` 값 컬럼에 적용됩니다.

```sql
CREATE TAG TABLE quality_sensor (
    name    VARCHAR(64) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   DOUBLE SUMMARIZED
) METADATA (
    lsl     DOUBLE LOWER LIMIT,   -- 하한 규격값
    usl     DOUBLE UPPER LIMIT,   -- 상한 규격값
    target  DOUBLE    -- 목표값
);

-- 센서 초기화 시 규격값 설정
INSERT INTO quality_sensor METADATA (name, lsl, usl, target)
VALUES ('QS-MOTOR-01', 70.0, 90.0, 80.0);
```

## 이상 감지 쿼리

```sql
-- 규격 이탈 데이터 조회
SELECT q.name, q.time, q.value, m.lsl, m.usl
FROM quality_sensor q
JOIN quality_sensor METADATA m ON q.name = m.name
WHERE q.time >= NOW - 3600000000000
  AND (q.value < m.lsl OR q.value > m.usl);
```

## 동적 LSL·USL 패턴

규격값이 시간에 따라 변하는 경우, 별도 LOOKUP 테이블에 저장합니다.

```sql
CREATE LOOKUP TABLE spec_limits (
    sensor_name VARCHAR(64) PRIMARY KEY,
    lsl         DOUBLE,
    usl         DOUBLE,
    updated_at  DATETIME
);

-- 규격값 변경
UPDATE spec_limits SET lsl = 68.0, usl = 92.0, updated_at = NOW
WHERE sensor_name = 'QS-MOTOR-01';
```

## 알람 임계값과의 차이

| 값 | 설명 |
|-----|------|
| LSL (Lower Spec Limit) | 품질 규격 하한 — 이 미만은 불량 |
| USL (Upper Spec Limit) | 품질 규격 상한 — 이 초과는 불량 |
| LCL (Lower Control Limit) | 통계적 관리 하한 (±3σ) |
| UCL (Upper Control Limit) | 통계적 관리 상한 (±3σ) |
