---
type: docs
title: '시계열 데이터 RDB 오용'
weight: 50
---

## 문제

센서·IoT 계측값과 같은 대량 시계열 데이터를 RDB 테이블에 저장하는 패턴입니다.

## 안티패턴 예시

```sql
-- 잘못됨: 센서 시계열 데이터를 RDB에 저장
CREATE RDB TABLE sensor_timeseries (
    sensor_id VARCHAR(64),
    ts        DATETIME,
    value     DOUBLE,
    unit      VARCHAR(16)
);
```

## 문제점

| 문제 | 설명 |
|------|------|
| Append API 미지원 | 고속 대량 입력 불가, INSERT 문만 사용 |
| 시계열 최적화 없음 | 시간 범위 집계 성능이 TAG 테이블 대비 저하 |
| 압축 없음 | TAG 테이블의 시계열 압축 알고리즘 미적용 |
| 분석 함수 미지원 | TIME_BUCKET, FIRST, LAST 등 시계열 함수 미지원 |

## 올바른 패턴

센서 계측값은 TAG 테이블에 저장합니다.

```sql
-- 올바름: TAG 테이블 사용
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE,
    unit   VARCHAR(16)
);

-- Append API로 고속 입력 가능
-- 시계열 집계 함수 활용 가능
SELECT name, TIME_BUCKET('1h', time) AS hour, AVG(value), MAX(value)
FROM sensor_data
WHERE time >= NOW - 86400000000000
GROUP BY name, hour;
```

## RDB 테이블이 적합한 경우

RDB 테이블은 관계형 구조의 업무 데이터(주문 이력, 설비 이력 등)에 사용합니다. 시간 컬럼이 있더라도 데이터의 본질이 이벤트·이력이라면 LOG 또는 RDB를 선택하고, 고빈도 계측값이라면 TAG를 선택합니다.
