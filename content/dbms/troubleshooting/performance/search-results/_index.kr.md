---
type: docs
title: '16.5.2 검색 결과가 예상과 다를 때'
weight: 20
---

쿼리가 오류 없이 실행됐는데 결과가 비어 있거나, 중복 데이터가 보이거나, 집계 값이 맞지 않는 경우 이 섹션을 참고하십시오.

## 결과가 비어 있을 때

다음 순서로 확인합니다.

### 1단계: 데이터 존재 여부 확인

```sql
SELECT COUNT(*) FROM sensor_tag;
```

건수가 `0`이면 데이터가 아직 입력되지 않은 것입니다. [입력이 실패할 때](../../item/failure/)를 참고하십시오.

### 2단계: 시간 범위 확인

Machbase의 타임스탬프는 나노초(ns) 단위입니다. 밀리초나 초 단위의 값을 그대로 사용하면 시간 범위가 극히 짧거나 아예 벗어납니다.

```sql
-- 실제 저장된 시간 범위 확인
SELECT MIN(time), MAX(time) FROM sensor_tag WHERE name = 'sensor-01';
```

쿼리의 시간 조건과 실제 저장된 시간 범위가 겹치는지 확인합니다.

```sql
-- 나쁜 예: 밀리초 단위 값을 나노초 컬럼과 비교
SELECT * FROM sensor_tag WHERE time > 1705276200000;

-- 좋은 예: TO_DATE 함수 사용
SELECT * FROM sensor_tag
WHERE time > TO_DATE('2024-01-15 09:30:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 3단계: 태그명 대소문자 확인

TAG 테이블의 `name` 값은 대소문자를 구별합니다. `Sensor-01`과 `sensor-01`은 서로 다른 태그입니다.

```sql
-- 실제 저장된 태그명 확인
SELECT DISTINCT name FROM sensor_tag WHERE name LIKE '%sensor%';
```

### 4단계: 타임존 설정 확인

서버와 클라이언트의 타임존 설정이 다를 경우 시간 범위 조건이 의도와 다르게 동작할 수 있습니다.

```sql
SELECT * FROM v$property WHERE name = 'DEFAULT_TIMEZONE';
```

서버 타임존이 `UTC`인데 현지 시간으로 조건을 입력하면 결과가 달라집니다. 아래를 참고하십시오.

## 타임존 이슈

서버 타임존과 클라이언트 기대 시간대가 다를 때 발생합니다.

**확인**

```sql
-- 서버 기본 타임존 확인
SELECT * FROM v$property WHERE name = 'DEFAULT_TIMEZONE';

-- 현재 서버 시각 확인
SELECT NOW();
```

**해결 방법**

- 쿼리에서 명시적으로 타임존을 변환합니다.

```sql
-- UTC 서버에서 KST(+9) 기준으로 조회할 때
SELECT * FROM sensor_tag
WHERE time > TO_DATE('2024-01-15 00:00:00', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '9' HOUR
  AND time < TO_DATE('2024-01-16 00:00:00', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '9' HOUR;
```

- 또는 `machbase.conf`에서 `DEFAULT_TIMEZONE`을 클라이언트 환경에 맞게 설정합니다.

## 중복 데이터가 보일 때

### TAG 테이블의 특성

TAG 테이블은 동일한 `name`과 `time` 조합이 중복으로 입력될 수 있습니다. Append 방식은 중복 체크 없이 순차 기록하는 것이 기본 동작입니다.

**확인 방법**

```sql
-- 특정 시간에 중복 값이 있는지 확인
SELECT name, time, COUNT(*) AS cnt
FROM sensor_tag
WHERE name = 'sensor-01'
  AND time BETWEEN TO_DATE('2024-01-15', 'YYYY-MM-DD')
               AND TO_DATE('2024-01-16', 'YYYY-MM-DD')
GROUP BY name, time
HAVING COUNT(*) > 1;
```

**해결 방법**

- 중복 제거가 필요한 조회에서는 `DISTINCT`를 사용합니다.

```sql
SELECT DISTINCT name, time, value FROM sensor_tag WHERE name = 'sensor-01';
```

- 정기 집계에는 ROLLUP을 활용합니다. ROLLUP은 중복 데이터를 집계하므로 자연스럽게 중복이 희석됩니다.

## 집계 결과가 다를 때

### ROLLUP 갱신 지연

ROLLUP 테이블은 실시간으로 갱신되지 않습니다. 가장 최근에 입력된 데이터가 아직 ROLLUP에 반영되지 않아 집계 결과에 차이가 생길 수 있습니다.

**확인 방법**

```sql
-- 원본 테이블의 집계
SELECT name, AVG(value)
FROM sensor_tag
WHERE name = 'sensor-01'
  AND time > ADD_TIME(SYSDATE, '0/0/0 -1:0:0')
GROUP BY name;

-- ROLLUP 테이블의 집계
SELECT name, AVG(avg_value)
FROM sensor_tag_rollup_1min
WHERE name = 'sensor-01'
  AND time > ADD_TIME(SYSDATE, '0/0/0 -1:0:0')
GROUP BY name;
```

두 결과의 차이가 크다면 ROLLUP이 지연된 것입니다.

**즉시 갱신**

```sql
ALTER SYSTEM FLUSH ROLLUP;
```

이 명령을 실행하면 아직 처리되지 않은 데이터를 즉시 ROLLUP 테이블에 반영합니다. 단, 대용량 데이터가 쌓인 경우 완료까지 시간이 걸릴 수 있습니다.
