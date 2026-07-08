---
type: docs
title: '상대 시간 표현 사전'
weight: 40
---

상대 시간 표현을 사용하면 `NOW`, `SYSDATE`와 같은 기준 시점으로부터의 차이를 SQL 문 안에서 직접 기술할 수 있습니다. 별도 함수 호출 없이 시계열 윈도우를 간결하게 표현할 때 유용합니다.

> 상대 시간 리터럴(`now - 1h` 형태)은 Machbase 8.0.50 이상에서 지원됩니다. 이전 버전에서는 `DATEADD`, `TO_DATE` 등의 함수를 사용합니다.

## 빠른 참조표

| 표현 | 예시 | 설명 |
|------|------|------|
| `NOW` / `now` | `now` | 현재 시각 (나노초 정밀도) |
| `SYSDATE` / `sysdate` | `sysdate` | 현재 시각 (`NOW`와 동일) |
| `now - offset` | `now - 1h` | 현재 시각에서 오프셋 뺄셈 |
| `now + offset` | `now + 30m` | 현재 시각에서 오프셋 덧셈 |
| `DATEADD(unit, n, time)` | `DATEADD('HOUR', -1, NOW())` | n 단위 더하기/빼기 |
| `DATEDIFF(unit, t1, t2)` | `DATEDIFF('SECOND', t1, t2)` | 두 시각의 차이 |
| `TO_DATE('...', 'format')` | `TO_DATE('2024-01-01', 'YYYY-MM-DD')` | 문자열을 DATETIME으로 변환 |
| `TO_TIMESTAMP(ns)` | `TO_TIMESTAMP(1704067200000000000)` | 나노초 정수를 DATETIME으로 변환 |
| 나노초 정수 직접 사용 | `value + 1000000000` | 나노초 단위 정수를 DATETIME에 더함 |

## 상대 시간 단위 (리터럴 접미사)

| 접미사 | 의미 | 예시 |
|--------|------|------|
| `ns` | 나노초 | `500ns` |
| `us` | 마이크로초 | `20us` |
| `ms` | 밀리초 | `15ms` |
| `s` | 초 | `45s` |
| `m` | 분 | `30m` |
| `h` | 시간 | `12h` |
| `d` | 일 | `7d` |
| `w` | 주 | `2w` (= 14일) |

> 월(`month`, `mo`)과 연(`year`, `y`)은 길이가 일정하지 않아 지원하지 않습니다. `30d` 또는 `365d`로 대체합니다.

## DATEADD 함수

함수 기반 날짜 연산입니다. 상대 시간 리터럴을 지원하지 않는 이전 버전 또는 복잡한 단위 계산에 사용합니다.

```sql
DATEADD(unit, n, datetime_expr)
```

| `unit` | 설명 |
|--------|------|
| `'NANOSECOND'` / `'NS'` | 나노초 |
| `'MICROSECOND'` / `'US'` | 마이크로초 |
| `'MILLISECOND'` / `'MS'` | 밀리초 |
| `'SECOND'` / `'SEC'` | 초 |
| `'MINUTE'` / `'MIN'` | 분 |
| `'HOUR'` | 시간 |
| `'DAY'` | 일 |
| `'WEEK'` | 주 |
| `'MONTH'` | 월 |
| `'YEAR'` | 연 |

```sql
-- 1시간 전
SELECT * FROM sensor_log WHERE time > DATEADD('HOUR', -1, NOW());

-- 30분 후
SELECT * FROM maintenance_plan WHERE scheduled_at < DATEADD('MINUTE', 30, NOW());
```

## DATEDIFF 함수

두 DATETIME 값의 차이를 지정 단위로 반환합니다.

```sql
DATEDIFF(unit, datetime1, datetime2)
```

```sql
-- 두 시각의 차이 (초 단위)
SELECT DATEDIFF('SECOND', start_time, end_time) AS elapsed_sec FROM job_log;

-- 경과 일수
SELECT DATEDIFF('DAY', created_at, NOW()) AS age_days FROM sensor_tag;
```

## TO_DATE 함수

문자열을 DATETIME 타입으로 변환합니다.

```sql
TO_DATE('datetime_string', 'format')
```

| 포맷 토큰 | 의미 |
|-----------|------|
| `YYYY` | 4자리 연도 |
| `MM` | 2자리 월 |
| `DD` | 2자리 일 |
| `HH24` | 24시간제 시 |
| `MI` | 분 |
| `SS` | 초 |
| `mmm` | 밀리초 |
| `uuu` | 마이크로초 |
| `nnn` | 나노초 |

```sql
SELECT * FROM sensor_tag
 WHERE time >= TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

## 활용 패턴

### 시간 구간 필터링

```sql
-- 최근 1시간 데이터 (상대 시간 리터럴)
SELECT * FROM sensor_tag WHERE time > now - 1h;

-- 최근 1시간 데이터 (DATEADD 함수)
SELECT * FROM sensor_tag WHERE time > DATEADD('HOUR', -1, NOW());

-- 최근 24시간 기록
SELECT * FROM app_log WHERE _arrival_time BETWEEN now - 1d AND now;

-- 최근 10분 이내 알람
SELECT alert_id, level, occurred_at FROM alert_log
 WHERE occurred_at >= sysdate - 10m;
```

### 복합 시간 표현

```sql
-- 2일 6시간 15분 후
SELECT * FROM maintenance_plan WHERE planned_at < now + 2d6h15m;

-- 하위 초 단위 조합
SELECT TO_CHAR(now + 3s125ms10us4ns, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn');
```

### TO_DATE 결과에 오프셋 적용

```sql
-- 문자열 날짜에 3일 추가
SELECT TO_CHAR(TO_DATE('2024-05-01', 'YYYY-MM-DD') + 3d, 'YYYY-MM-DD');
-- 결과: 2024-05-04

-- 문자열 날짜에서 4시간 15분 빼기
SELECT TO_CHAR(
    TO_DATE('2024-05-01 08:00:00', 'YYYY-MM-DD HH24:MI:SS') - 4h15m,
    'YYYY-MM-DD HH24:MI:SS'
);
-- 결과: 2024-05-01 03:45:00
```

### 나노초 정수 직접 사용

숫자 리터럴은 나노초로 해석됩니다.

```sql
-- 1초 = 1,000,000,000 나노초
SELECT event_time + 1000000000 AS event_time_plus_1s FROM events;

-- 250나노초 빼기
SELECT event_time - 250 AS event_time_minus_250ns FROM events;
```

## 제한사항

- 상대 시간 리터럴(`1h`, `30m` 등)은 Machbase 8.0.50 이상에서만 지원됩니다.
- 월(`mo`)과 연(`y`) 단위는 리터럴로 지원하지 않습니다. `DATEADD('MONTH', n, time)` 함수를 사용합니다.
- 문자열 리터럴은 interval 산술에서 DATETIME으로 암시적 변환되지 않으므로 `TO_DATE()`로 먼저 변환해야 합니다.
- 인터벌 자체는 `ORDER BY` 절에서 사용할 수 없습니다.

## 오류 처리

| 상황 | 오류 | 해결 방법 |
|------|------|-----------|
| 지원하지 않는 접미사(`1y`, `5mo`) | `ERR-02034` invalid time expression | 지원 단위(`365d`, `30d` 등)로 교체 |
| 단위 누락(`now + 10`) | 나노초로 해석됨 | 의도한 단위 접미사 명시 |
| 너무 큰 값(`1000000d`) | `ERR_OVERFLOW_INTERVAL` | 값 범위 축소 |

## 관련 문서

- [상대 시간 표현](/dbms-8.5/sql-reference/time-expressions/) — 8.5 레퍼런스 상세
