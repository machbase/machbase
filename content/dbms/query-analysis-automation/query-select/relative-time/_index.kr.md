---
type: docs
title: '상대 시간 표현'
weight: 40
---

상대 시간 표현은 알려진 기준 시점으로부터의 차이를 SQL 문 안에서 직접 기술할 수 있도록 해 줍니다. 최근 계측 데이터를 필터링하거나 향후 작업을 예약하고, 보조 함수 호출 없이 시계열 윈도를 정렬해야 하는 운영자에게 유용합니다.

> **참고**: 이 기능은 Machbase 8.0.50 이상에서 지원됩니다.

## 빠르게 살펴보기

```sql
-- 최근 1시간 데이터 조회
SELECT * FROM sensor_log WHERE event_time > now - 1h;

-- 2일 6시간 이후까지의 일정 확인
SELECT * FROM maintenance_plan WHERE planned_at < now + 2d6h;

-- 하위 초 단위까지 세그먼트 결합
SELECT to_char(now + 3s125ms10us4ns, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn');
```

## 구문 요약

- 리터럴은 공백 없이 이어지는 `<숫자><단위>` 세그먼트 하나 이상으로 작성합니다.
- 단위는 소문자를 사용하며, 서로 다른 크기는 이어 붙여 표현합니다(`2h30m`).
- `+` 또는 `-` 접두어를 붙이거나 산술식을 사용할 수 있습니다(`now - 90m`, `sample_time + 15s` 등).
- 숫자 뒤에 단위를 붙이지 않으면 나노초 단위로 해석됩니다.
- 상대 리터럴은 `INTERVAL`로 평가되며, `DATETIME`에 더하거나 빼면 결과 역시 `DATETIME`이 됩니다.

## 지원 단위

| 접미사 | 의미 | 예시 | 동일한 기간 |
|--------|------|------|------------|
| `ns` | 나노초 | `500ns` | 500 나노초 |
| `us` | 마이크로초 | `20us` | 0.00002초 |
| `ms` | 밀리초 | `15ms` | 0.015초 |
| `s` | 초 | `45s` | 45초 |
| `m` | 분 | `30m` | 30분 |
| `h` | 시간 | `12h` | 12시간 |
| `d` | 일 | `7d` | 7일 |
| `w` | 주 | `2w` | 14일 |

> **참고**: 월과 연은 길이가 일정하지 않아 지원하지 않습니다. 지원하지 않는 접미사(`1y`, `1mo` 등)를 사용하면 `ERR-02034` (invalid time expression) 오류가 발생합니다.

## 복합 리터럴 작성

- 가독성을 위해 가장 큰 단위부터 작성합니다(`5d4h30m`).
- 값이 0인 세그먼트는 생략합니다. `4h15m0s`보다는 `4h15m`이 좋습니다.
- 세그먼트 순서는 바뀌어도 되지만 일관성을 유지하면 실수를 줄일 수 있습니다. `1h30m`과 `30m1h`는 동일하게 평가됩니다.

## 활용 패턴

### 시간 구간 필터링

```sql
-- 최근 24시간 기록
SELECT *
  FROM rtrollup
 WHERE time BETWEEN now - 1d AND now;

-- 최근 10분 이내 발생한 알람
SELECT alert_id, level, occurred_at
  FROM alert_log
 WHERE occurred_at >= sysdate - 10m;

-- 최근 15분, 특정 센서
SELECT device_id, ts, value
  FROM metrics_stream
 WHERE ts BETWEEN now - 15m AND now
   AND device_id = 'sensor-01';
```

### 향후 작업 예약

```sql
-- 다음 영업일 + 2시간 이내 실행할 작업
SELECT job_id, scheduled_at
  FROM job_queue
 WHERE scheduled_at <= now + 1d2h;

-- 30분 후 정비 일정 등록
INSERT INTO device_schedule (device_id, maintenance_due)
VALUES ('device-001', now + 30m);
```

### 시간 기반 조인

```sql
-- 상대 오프셋을 이용해 두 소스를 조인 (±500ms 범위)
SELECT a.ts, a.value AS raw_value, b.value AS calibrated
  FROM raw_metrics a
  JOIN calibration b
    ON b.ts BETWEEN a.ts - 500ms AND a.ts + 500ms;
```

### DATETIME 값과 캐스팅

```sql
SELECT to_char(to_date('2024-05-01', 'YYYY-MM-DD') + 3d,
               'YYYY-MM-DD');                              -- 2024-05-04

SELECT to_char(to_date('2024-05-01 08:00:00',
                       'YYYY-MM-DD HH24:MI:SS') - 4h15m,
               'YYYY-MM-DD HH24:MI:SS');                   -- 2024-05-01 03:45:00

SELECT to_char(to_date('2024-05-01', 'YYYY-MM-DD') + 2h30m45s250ms,
               'YYYY-MM-DD HH24:MI:SS mmm');               -- 2024-05-01 02:30:45 250
```

> 문자열 리터럴은 interval 산술에서 `DATETIME`으로 암시적 변환되지 않습니다. 먼저 `TO_DATE`로 변환해야 합니다.

### 순수 숫자 (나노초)

```sql
-- 숫자 리터럴은 기본적으로 나노초이므로 정확히 1초가 더해집니다.
SELECT event_time + 1000000000 AS event_time_plus_1s
  FROM events;

-- 250나노초를 뺍니다.
SELECT event_time - 250 AS event_time_minus_250ns
  FROM events;
```

## 동작 및 제한 사항

- 정밀도는 나노초까지 지원합니다. 64비트 범위를 넘으면 오버플로가 발생합니다.
- 인터벌 비교는 최종 `DATETIME` 값을 기준으로 이루어집니다. 인터벌 자체는 `ORDER BY` 절에서 사용할 수 없습니다.

## 오류 처리

| 시나리오 | 오류 코드 | 해결 방법 |
|----------|-----------|-----------|
| 지원하지 않는 접미사(`1y`, `5mo`) | `ERR-02034` | 지원 단위(`30d` 등)로 교체합니다. |
| 단위 누락(`now + 10`) | 나노초로 해석됨 | 의도가 분/초라면 명시적으로 접미사를 붙입니다. |
| 값이 너무 큰 리터럴(`1000000d`) | `ERR_OVERFLOW_INTERVAL` | 크기를 줄이거나 반복 처리로 나눕니다. |
| 숫자가 아닌 문자 포함(`1h3xm`) | Invalid time expression | 오탈자를 수정합니다(`1h3m`). |

## 참고 치트시트

```
패턴                                           의미
---------------------------------------------  ----------------------------------------
now - 5m                                       정확히 5분 전 시각
sysdate + 1d                                   시스템 시간 기준 24시간 후
col_ts + 90s                                   컬럼 값을 90초 뒤로 이동
TO_DATE('2024-01-01','YYYY-MM-DD') + 2w        날짜 값에 14일을 더함
value + 250                                    value에 250나노초를 더함
```
