---
type: docs
title: '시간축 TAG 테이블 설계'
weight: 10
---

시간축 TAG 테이블은 `BASETIME` 키워드를 사용하여 시간을 기준 축으로 삼는 시계열 테이블입니다.

## 최소 구성

TAG 테이블은 다음 세 가지 컬럼이 필수입니다.

| 컬럼 역할 | 타입 | 키워드 | 설명 |
|---------|------|--------|------|
| 태그 식별자 | `VARCHAR(n)` | `PRIMARY KEY` | 센서 이름 등 |
| 시간 | `DATETIME` | `BASETIME` | 시간축, 나노초 정밀도 |
| 값 | 숫자형 등 | — | 계측값 |

```sql
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);
```

## 다중 값 컬럼

하나의 TAG 테이블에 여러 계측값을 함께 저장할 수 있습니다.

```sql
CREATE TAG TABLE env_sensor (
    name        VARCHAR(64) PRIMARY KEY,
    time        DATETIME    BASETIME,
    temperature DOUBLE,
    humidity    DOUBLE,
    pressure    DOUBLE
);
```

## 데이터 삽입

```sql
-- 단건 INSERT
INSERT INTO sensor_data VALUES ('sensor-01', '2024-01-01 00:00:00', 23.5);

-- APPEND API (고속 대량 입력)
-- SDK에서 Append() 함수 사용
```

## 조회

```sql
-- 최근 1시간 데이터 조회
SELECT name, time, value
FROM sensor_data
WHERE name = 'sensor-01'
  AND time >= NOW - 3600000000000
ORDER BY time DESC;

-- 여러 태그 조회
SELECT name, time, value
FROM sensor_data
WHERE name IN ('sensor-01', 'sensor-02')
  AND time BETWEEN '2024-01-01' AND '2024-01-02';
```

## 시간 단위

`DATETIME` 컬럼에 나노초 정밀도로 값을 저장합니다. NOW 함수는 현재 시각을 나노초로 반환합니다.

| 단위 | 나노초 값 |
|------|---------|
| 1초 | 1,000,000,000 |
| 1분 | 60,000,000,000 |
| 1시간 | 3,600,000,000,000 |
| 1일 | 86,400,000,000,000 |
