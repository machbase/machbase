---
type: docs
title: '5.2.1.4 스토리지 전략'
weight: 90
---

TAG 테이블의 데이터는 태그별로 분리된 컬럼 스토리지에 저장됩니다. 데이터 양과 조회 패턴에 따라 적절한 전략을 선택합니다.

## 단일 테이블 vs 다중 테이블

### 단일 TAG 테이블 (권장)

같은 종류의 센서는 하나의 TAG 테이블에 모아서 관리합니다.

```sql
-- 권장: 모든 온도 센서를 하나의 테이블로
CREATE TAG TABLE temperature_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

**장점**
- 관리 포인트 최소화
- 크로스-태그 집계 용이
- 운영 간소화

### 다중 TAG 테이블

측정 항목이 완전히 다른 경우(컬럼 구성이 다른 경우)만 테이블을 분리합니다.

```sql
-- 온도·습도 센서 (DOUBLE 값)
CREATE TAG TABLE thermo_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    temp  DOUBLE,
    humid DOUBLE
);

-- 진동 센서 (DOUBLE + BINARY 파형)
CREATE TAG TABLE vibration_sensor (
    name     VARCHAR(64) PRIMARY KEY,
    time     DATETIME    BASETIME,
    rms      DOUBLE,
    waveform BINARY
);
```

## 태그 수 관리

- 태그 수가 수십만 개를 초과하면 쿼리 성능이 저하될 수 있습니다.
- 센서 계층 구조를 태그 이름에 인코딩하여 관리합니다.
- 태그 이름이 매 레코드마다 고유한 값이 되는 설계는 피합니다 (안티패턴).

## 파티션 전략

Machbase는 `_arrival_time` 또는 `BASETIME` 기준으로 데이터를 내부적으로 파티션화합니다. 별도 파티션 설정 없이도 시간 범위 쿼리가 효율적으로 실행됩니다. 보존 기간 설정은 [운영 및 구성](/dbms/operations-configuration-recovery/)을 참고하십시오.
