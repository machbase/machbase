---
type: docs
title: '2.1.3 시간 모델과 _arrival_time'
weight: 30
---

Machbase DBMS에서 시간은 테이블 유형에 따라 다르게 표현됩니다. LOG 테이블은 시스템이 데이터를 수신한 시각을 자동으로 기록하고, TAG 테이블은 사용자가 명시적으로 정의한 시간 컬럼을 시간 축으로 사용합니다. LOOKUP, VOLATILE, RDB 테이블에는 필수 시간축이 없으며, 필요한 경우 사용자가 일반 DATETIME 컬럼을 정의합니다. 이 차이를 이해하면 조회 조건 작성과 스키마 설계에서 혼동을 줄일 수 있습니다.

## LOG 테이블의 `_arrival_time`

LOG 테이블을 생성하면 Machbase는 `_arrival_time`이라는 DATETIME 컬럼을 자동으로 추가합니다. 이 컬럼은 사용자가 정의하지 않아도 항상 존재하며, 해당 행이 서버에 입력된 시각을 나노초 정밀도로 기록합니다.

```sql
-- 사용자는 두 컬럼만 정의했지만
CREATE TABLE device_events (
    device_id VARCHAR(20),
    status    VARCHAR(20)
);

-- _arrival_time은 자동으로 추가되어 세 컬럼이 존재한다
-- SHOW CREATE TABLE device_events;
-- => device_id VARCHAR(20), status VARCHAR(20), _arrival_time DATETIME
```

`_arrival_time`은 데이터가 서버에 도달한 시각이므로, 센서에서 측정한 실제 발생 시각과 네트워크 지연이나 수집기 버퍼링 시간만큼 차이가 날 수 있습니다. 이벤트가 실제로 발생한 시각이 중요하다면 별도의 DATETIME 컬럼을 정의해 사용자가 직접 값을 입력해야 합니다.

### `_arrival_time` 기반 조회

시간 범위 조회에서 `_arrival_time`을 WHERE 조건에 명시하거나, Machbase의 `DURATION` 구문을 사용할 수 있습니다.

```sql
-- 직접 조건 지정
SELECT device_id, status
FROM device_events
WHERE _arrival_time >= TO_DATE('2026-07-03 09:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND _arrival_time <  TO_DATE('2026-07-03 10:00:00', 'YYYY-MM-DD HH24:MI:SS');

-- DURATION 구문 (최근 1시간)
SELECT device_id, status
FROM device_events
DURATION 1 HOUR;
```

`DURATION` 구문은 내부적으로 `_arrival_time`을 기준으로 동작합니다.

## TAG 테이블의 BASETIME 컬럼

TAG 테이블은 `_arrival_time`이 없습니다. 대신 사용자가 테이블 생성 시 `BASETIME` 속성을 붙인 DATETIME 컬럼을 시간 축으로 사용합니다.

```sql
CREATE TAG TABLE sensor_values (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,        -- 사용자 정의 시간 축
    value DOUBLE SUMMARIZED
);
```

여기서 `time` 컬럼에 입력하는 값은 센서가 측정한 실제 시각입니다. 서버 수신 시각이 아니라 발생 시각을 직접 제어할 수 있으므로, 늦게 도착한 데이터도 올바른 시간 위치에 기록됩니다.

```sql
-- 측정 시각을 직접 지정
INSERT INTO sensor_values
VALUES ('temp_sensor_01', TO_DATE('2026-07-03 08:55:00', 'YYYY-MM-DD HH24:MI:SS'), 23.1);
```

## 두 시간 모델의 비교

| 항목 | LOG: `_arrival_time` | TAG: BASETIME 컬럼 |
| --- | --- | --- |
| 설정 방법 | 자동 추가 (사용자 정의 불필요) | `BASETIME` 속성으로 명시 |
| 의미 | 서버 수신 시각 | 사용자가 지정한 이벤트/측정 시각 |
| 정밀도 | 나노초 | 나노초 |
| 늦게 도착한 데이터 | 수신 시각으로 기록됨 | 원래 측정 시각으로 기록 가능 |
| 조회 기준 | `_arrival_time` 또는 `DURATION` | BASETIME 컬럼 이름으로 조회 |

LOOKUP, VOLATILE, RDB 테이블의 DATETIME 컬럼은 일반 컬럼입니다. 자동 `_arrival_time`이나
`BASETIME` 의미가 붙지 않으므로, 시간 범위 조회나 보관 정책을 시계열 테이블과 같은 방식으로
기대하면 안 됩니다.

## 어느 모델을 선택해야 하는가

**`_arrival_time`(LOG 테이블)이 적합한 경우**

- 서버 수신 순서가 곧 이벤트 순서인 경우
- 데이터 수신 지연이 매우 짧고 무시할 수 있는 경우
- 스키마에 별도의 시간 컬럼 없이도 시간 기반 조회가 필요한 경우

**BASETIME(TAG 테이블)이 적합한 경우**

- 센서 측정 시각이 정확해야 하는 계측값 데이터
- 네트워크 지연이나 수집기 버퍼링으로 인해 실제 발생 시각이 수신 시각과 다를 수 있는 경우
- 태그 이름과 시간 축으로 계측값을 조회해야 하는 경우

## 다음 읽을 내용

- [시계열 데이터 이해하기](../time-series/) — 시계열 데이터의 본질
- [LOG 테이블 설계](/dbms/log-table-usage/) — `_arrival_time`을 활용한 이벤트 테이블 설계
- [TAG 테이블 설계](/dbms/tag-table-usage/) — BASETIME을 활용한 계측값 테이블 설계
