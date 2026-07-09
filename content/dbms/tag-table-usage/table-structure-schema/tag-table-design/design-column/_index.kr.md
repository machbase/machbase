---
type: docs
title: '5.2.1.1 값 컬럼 설계'
weight: 60
---

TAG 테이블의 값 컬럼(BASETIME 또는 BASEDISTANCE 이외의 컬럼)은 계측값을 저장합니다.

## 지원 타입

| 타입 | 설명 | 저장 크기 |
|------|------|---------|
| `DOUBLE` | 64비트 부동소수점 | 8바이트 |
| `FLOAT` | 32비트 부동소수점 | 4바이트 |
| `LONG` | 64비트 정수 | 8바이트 |
| `INTEGER` (`INT`) | 32비트 정수 | 4바이트 |
| `SHORT` | 16비트 정수 | 2바이트 |
| `VARCHAR(n)` | 가변 문자열 | 최대 n바이트 |

## 권장 타입 선택

| 데이터 | 권장 타입 |
|--------|---------|
| 온도, 습도, 압력 등 아날로그 값 | `DOUBLE` |
| 카운터, 상태 코드 | `INTEGER` |
| 플래그, 이진 상태 | `SHORT` |
| 에너지, 유량 누적값 | `DOUBLE` 또는 `LONG` |
| 태그 문자열 값 | `VARCHAR(n)` |

## 다중 값 컬럼 설계

한 테이블에 여러 계측항목을 함께 저장할 때는 NULL 값이 발생할 수 있습니다. 계측항목이 서로 동시에 수집되는 경우에 적합합니다.

```sql
CREATE TAG TABLE weather_station (
    name        VARCHAR(64) PRIMARY KEY,
    time        DATETIME    BASETIME,
    temperature DOUBLE,     -- 항상 수집
    humidity    DOUBLE,     -- 항상 수집
    wind_speed  DOUBLE,     -- 옵션
    rainfall    DOUBLE      -- 옵션
);
```

## NULL 허용 설계

TAG 테이블 값 컬럼은 기본적으로 NULL을 허용합니다. 특정 태그가 일부 항목만 수집하는 경우 나머지 컬럼에 NULL을 삽입합니다.

```sql
-- wind_speed와 rainfall이 없는 경우
INSERT INTO weather_station VALUES ('WS-01', NOW, 22.5, 65.0, NULL, NULL);
```
