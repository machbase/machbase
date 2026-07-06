---
type: docs
title: '센서별 테이블 생성'
weight: 20
---

## 문제

센서(태그)마다 별도의 테이블을 생성하는 패턴입니다. 센서 수가 늘어날수록 테이블 수가 폭발적으로 증가하여 관리가 불가능해집니다.

## 안티패턴 예시

```sql
-- 잘못된 설계: 센서마다 테이블 생성
CREATE TAG TABLE sensor_temp_01 (...);
CREATE TAG TABLE sensor_temp_02 (...);
CREATE TAG TABLE sensor_temp_03 (...);
-- ... 센서가 10,000개면 테이블도 10,000개
```

## 문제점

| 문제 | 설명 |
|------|------|
| 관리 복잡도 | 테이블 수만큼 DDL 관리 필요 |
| 쿼리 불편 | 크로스-센서 집계 불가 |
| 메타데이터 증가 | 시스템 카탈로그 부하 |
| 신규 센서 추가 | 매번 DDL 실행 필요 |

## 올바른 패턴

센서 이름을 PRIMARY KEY로 하는 하나의 TAG 테이블에 모든 센서 데이터를 저장합니다.

```sql
-- 올바른 설계: 모든 온도 센서를 하나의 테이블로
CREATE TAG TABLE temperature_sensor (
    name   VARCHAR(128) PRIMARY KEY,
    time   DATETIME     BASETIME,
    value  DOUBLE
);

-- 모든 센서 데이터를 하나의 테이블에 삽입
INSERT INTO temperature_sensor VALUES ('TEMP-01', NOW, 23.5);
INSERT INTO temperature_sensor VALUES ('TEMP-02', NOW, 24.1);
INSERT INTO temperature_sensor VALUES ('TEMP-10000', NOW, 22.9);
```

## 장점

- 신규 센서 추가 시 DDL 불필요 (새 태그 이름으로 INSERT만 하면 됨)
- 크로스-센서 집계 용이
- 운영 관리 포인트 최소화
