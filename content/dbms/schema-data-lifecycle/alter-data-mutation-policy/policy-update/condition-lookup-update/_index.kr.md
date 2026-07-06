---
type: docs
title: 'LOOKUP 일반 조건식 UPDATE (planned: dbms-nfx#3696)'
weight: 50
---

> **계획된 기능**: LOOKUP 테이블의 일반 조건식(non-PK 컬럼 기준) UPDATE는 dbms-nfx#3696에서 개발 중입니다. 현재 버전(8.6)에서는 PRIMARY KEY 기준 UPDATE만 지원됩니다.

## 현재 지원 범위

현재 LOOKUP 테이블의 UPDATE는 WHERE 조건에 관계없이 구문적으로는 실행되나, PRIMARY KEY 컬럼 기준 조건을 사용하는 것이 안전합니다.

```sql
-- 현재 권장: PK 기준 UPDATE
UPDATE alarm_threshold SET high_limit = 90.0
WHERE sensor_id = 'TEMP-01';  -- sensor_id = PK
```

## 향후 지원 예정 (dbms-nfx#3696)

일반 조건식이 지원되면 PK가 아닌 컬럼 기준으로도 UPDATE가 가능해집니다.

```sql
-- 향후 지원 예정: 특정 설비 유형의 임계값 일괄 변경
UPDATE alarm_threshold SET high_limit = 85.0
WHERE device_type = 'MOTOR';  -- device_type = non-PK 컬럼

-- 범위 조건
UPDATE device_config SET active = 0
WHERE last_seen < DATEADD('d', -30, NOW);
```

## 현재 대안

현재 PK가 아닌 조건으로 여러 행을 UPDATE해야 하는 경우:

1. **애플리케이션 레이어에서 PK 목록 조회 후 개별 UPDATE**:
```sql
-- 1단계: 해당 PK 목록 조회
SELECT sensor_id FROM alarm_threshold WHERE device_type = 'MOTOR';

-- 2단계: 각 PK에 대해 UPDATE 실행 (애플리케이션 루프)
UPDATE alarm_threshold SET high_limit = 85.0 WHERE sensor_id = 'TEMP-01';
UPDATE alarm_threshold SET high_limit = 85.0 WHERE sensor_id = 'TEMP-02';
...
```

2. **VOLATILE 테이블 활용**: 빈번한 일괄 UPDATE가 필요하다면 LOOKUP 대신 VOLATILE 테이블 고려

> LOOKUP JSON 컬럼 지원도 같은 이슈(#3696)에 포함되어 있습니다.
