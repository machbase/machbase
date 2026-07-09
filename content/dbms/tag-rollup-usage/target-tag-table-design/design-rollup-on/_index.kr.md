---
type: docs
title: '6.3.1 ROLLUP 설계 가이드'
weight: 110
---

ROLLUP을 효과적으로 사용하려면 데이터 수집 패턴과 조회 패턴을 고려해 계층을 설계해야 합니다.

## ON vs FROM

| 구문 | 소스 | 사용 시점 |
|------|------|-----------|
| `ON table(column)` | TAG 테이블 원시 데이터 | 최하위 ROLLUP 생성 시 |
| `FROM rollup_table` | 기존 ROLLUP 테이블 | 상위(더 큰 단위) ROLLUP 생성 시 |

```sql
-- ON: 1초 롤업은 반드시 TAG 테이블에서
CREATE ROLLUP _ru_1s ON tag(value) INTERVAL 1 SEC;

-- FROM: 1분은 1초 롤업에서
CREATE ROLLUP _ru_1m FROM _ru_1s INTERVAL 1 MIN;

-- FROM: 1시간은 1분 롤업에서
CREATE ROLLUP _ru_1h FROM _ru_1m INTERVAL 1 HOUR;
```

## 주기 설계 원칙

1. **가장 작은 단위부터**: 최하위 ROLLUP 주기는 조회에서 필요한 최소 시간 단위여야 합니다.
2. **배수 관계 유지**: 상위 ROLLUP 주기는 하위 주기의 정수배여야 합니다.
3. **계층 수 최소화**: 통상 3단계(초→분→시간)면 충분합니다.

```
초 단위 분석 필요: 1SEC → 1MIN → 1HOUR
분 단위 분석 충분: 1MIN → 1HOUR
대용량 장기 보관:  5MIN → 1HOUR → 1DAY (별도 커스텀 롤업)
```

## 실전 설계 패턴

### 패턴 1: 표준 IoT 센서

```sql
CREATE ROLLUP _sensor_ru_1s  ON sensor_data(value) INTERVAL 1 SEC;
CREATE ROLLUP _sensor_ru_1m  FROM _sensor_ru_1s   INTERVAL 1 MIN;
CREATE ROLLUP _sensor_ru_1h  FROM _sensor_ru_1m   INTERVAL 1 HOUR;
```

### 패턴 2: 고속 수집 + 실시간 대시보드

```sql
-- 10초 단위 집계 (높은 빈도 대시보드)
CREATE ROLLUP _fast_ru_10s  ON fast_sensor(value) INTERVAL 10 SEC;
CREATE ROLLUP _fast_ru_1m   FROM _fast_ru_10s    INTERVAL 1 MIN;
CREATE ROLLUP _fast_ru_1h   FROM _fast_ru_1m     INTERVAL 1 HOUR;
```

### 패턴 3: 정상/알람 분리 집계

```sql
CREATE ROLLUP _sensor_all_1m  ON tag(value) INTERVAL 1 MIN;
CREATE ROLLUP _sensor_ok_1m   ON tag(value) INTERVAL 1 MIN WHERE quality = 1;
CREATE ROLLUP _sensor_alm_1m  ON tag(value) INTERVAL 1 MIN WHERE value > 90;
```

## ROLLUP 스토리지 예측

ROLLUP 테이블의 행 수 ≈ (전체 기간 / ROLLUP 주기) × 태그 개수

예: 태그 1만 개 × 1초 ROLLUP × 1년 = 약 3천억 행 → 스토리지 계획 필요

> 태그가 많을수록 ROLLUP 테이블 크기가 비례해 커집니다. 필요한 컬럼과 주기만 선택적으로 만드세요.

## 주의사항

- ROLLUP 생성 전에 입력된 데이터는 집계되지 않습니다. 과거 데이터가 있는 경우 `EXEC ROLLUP_FORCE`로 수동 집계하거나, Rebuild를 사용합니다.
- WITH ROLLUP으로 자동 생성된 롤업은 이름이 고정됩니다. 이름 충돌을 피하려면 수동으로 생성하세요.
