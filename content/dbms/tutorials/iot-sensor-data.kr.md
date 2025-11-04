---
type: docs
title: '튜토리얼 1: IoT 센서 데이터'
weight: 10
---

Machbase Tag 테이블을 사용하여 IoT 센서 데이터를 수집하고 분석하는 방법을 학습합니다. 이 튜토리얼은 온도 및 습도 센서를 사용하는 실제 시나리오를 시뮬레이션합니다.

## 시나리오

다음과 같은 창고 모니터링 시스템을 구축합니다:
- 서로 다른 구역에 10개의 온도/습도 센서 배치
- 각 센서에서 10초마다 측정값 수집
- 추세를 추적하고 이상 징후 식별 필요
- 30일간의 과거 데이터 보관 필요

**목표**: 센서 데이터를 효율적으로 저장하고 실시간 모니터링 및 과거 분석을 위해 쿼리합니다.

## 학습 내용

- 센서 데이터를 위한 Tag 테이블 생성
- 고빈도 센서 측정값 삽입
- 센서 ID 및 시간 범위별 쿼리
- 자동 롤업 통계 활용
- 데이터 보존 구현

## 사전 요구 사항

- Machbase 설치 및 실행
- machsql 클라이언트 연결
- 15분의 시간

## 단계 1: Tag 테이블 생성

Tag 테이블은 (ID, 타임스탬프, 값) 구조의 센서 데이터에 최적화되어 있습니다.

```sql
CREATE TAGDATA TABLE warehouse_sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED,
    humidity DOUBLE SUMMARIZED
);
```

**스키마 이해하기**:
- `sensor_id`: 각 센서의 고유 식별자
- `time`: 측정값이 기록된 타임스탬프
- `temperature`, `humidity`: 측정하는 값
- `SUMMARIZED`: Machbase에 자동 통계 생성 지시

**테이블 확인**:
```sql
SHOW TABLE warehouse_sensors;
```

## 단계 2: 센서 데이터 삽입

다른 센서의 샘플 측정값을 삽입합니다:

```sql
-- Zone 1 센서
INSERT INTO warehouse_sensors VALUES ('zone1-temp01', NOW, 22.5, 55.2);
INSERT INTO warehouse_sensors VALUES ('zone1-temp01', NOW, 22.7, 55.0);
INSERT INTO warehouse_sensors VALUES ('zone1-temp01', NOW, 22.6, 55.1);

-- Zone 2 센서
INSERT INTO warehouse_sensors VALUES ('zone2-temp01', NOW, 21.3, 60.5);
INSERT INTO warehouse_sensors VALUES ('zone2-temp01', NOW, 21.5, 60.3);
INSERT INTO warehouse_sensors VALUES ('zone2-temp01', NOW, 21.4, 60.7);

-- Zone 3 센서
INSERT INTO warehouse_sensors VALUES ('zone3-temp01', NOW, 23.1, 52.8);
INSERT INTO warehouse_sensors VALUES ('zone3-temp01', NOW, 23.3, 52.5);
INSERT INTO warehouse_sensors VALUES ('zone3-temp01', NOW, 23.2, 52.6);
```

**실제 프로덕션 환경에서는** 다음을 사용하여 데이터를 삽입합니다:
- 애플리케이션에서 CLI/ODBC API 사용
- 대량 삽입을 위한 Machbase APPEND 프로토콜
- CSV 가져오기 도구

## 단계 3: 최근 데이터 쿼리

모든 센서의 최신 측정값 조회:

```sql
-- 최근 10분간의 데이터
SELECT * FROM warehouse_sensors
DURATION 10 MINUTE;
```

특정 센서의 최신 측정값 조회:

```sql
SELECT * FROM warehouse_sensors
WHERE sensor_id = 'zone1-temp01'
DURATION 1 HOUR;
```

## 단계 4: 롤업 통계 활용

Tag 테이블은 자동으로 통계를 생성합니다. 시간별 평균 조회:

```sql
-- 센서의 시간별 통계 조회
SELECT
    sensor_id,
    time,
    min_temperature,
    max_temperature,
    avg_temperature,
    avg_humidity
FROM warehouse_sensors
WHERE sensor_id = 'zone1-temp01'
  AND rollup = hour;
```

**사용 가능한 롤업 레벨**:
- `rollup = sec` - 초 단위 통계
- `rollup = min` - 분 단위 통계
- `rollup = hour` - 시간 단위 통계

## 단계 5: 추세 분석

높은 온도의 센서 찾기:

```sql
-- 최근 1시간 동안 23°C 이상인 센서
SELECT DISTINCT sensor_id, max_temperature
FROM warehouse_sensors
WHERE rollup = min
  AND max_temperature > 23.0
DURATION 1 HOUR;
```

모든 센서의 평균 계산:

```sql
-- 구역별 평균 온도 (최근 24시간)
SELECT
    sensor_id,
    AVG(avg_temperature) as daily_avg_temp,
    AVG(avg_humidity) as daily_avg_humidity
FROM warehouse_sensors
WHERE rollup = hour
DURATION 24 HOUR
GROUP BY sensor_id;
```

## 단계 6: Tag 메타데이터 처리

Tag 테이블에는 센서 정보를 위한 특별한 메타데이터 레이어가 있습니다:

```sql
-- 센서 메타데이터 삽입
INSERT INTO warehouse_sensors._META
VALUES ('zone1-temp01');

INSERT INTO warehouse_sensors._META
VALUES ('zone2-temp01');

INSERT INTO warehouse_sensors._META
VALUES ('zone3-temp01');

-- 메타데이터 쿼리
SELECT * FROM warehouse_sensors._META;
```

사용자 정의 메타데이터 컬럼 추가:

```sql
-- 위치 메타데이터 추가
ALTER TABLE warehouse_sensors._META
ADD COLUMN location VARCHAR(50);

-- 메타데이터 업데이트
UPDATE warehouse_sensors._META
SET location = 'North Warehouse'
WHERE name = 'zone1-temp01';

-- 메타데이터와 함께 쿼리
SELECT * FROM warehouse_sensors._META
WHERE location = 'North Warehouse';
```

## 단계 7: 데이터 보존 구현

30일간의 과거 데이터만 보관:

```sql
-- 30일 이전 데이터 삭제
DELETE FROM warehouse_sensors
BEFORE TO_DATE(TO_CHAR(SYSDATE - 30, 'YYYY-MM-DD'), 'YYYY-MM-DD');

-- 또는 EXCEPT를 사용하여 최근 30일 유지
DELETE FROM warehouse_sensors EXCEPT 30 DAYS;
```

**모범 사례**: 매일 이 정리 작업을 자동으로 실행하도록 cron 작업을 설정합니다.

## 단계 8: 이상 징후 모니터링

온도 급증을 감지하는 쿼리 생성:

```sql
-- 1시간 동안 온도 변화가 5°C 이상인 센서 찾기
SELECT
    sensor_id,
    max_temperature - min_temperature as temp_range,
    avg_temperature
FROM warehouse_sensors
WHERE rollup = hour
  AND (max_temperature - min_temperature) > 5.0
DURATION 24 HOUR;
```

## 직접 해보기

### 연습 1: 센서 추가

추가 센서의 데이터를 삽입합니다:

```sql
-- zone4 및 zone5 센서 추가
-- 다양한 온도 및 습도 범위 시도
INSERT INTO warehouse_sensors VALUES ('zone4-temp01', NOW, 20.1, 65.0);
-- 더 많은 측정값 추가...
```

### 연습 2: 경고 쿼리 생성

다음을 찾는 쿼리를 작성합니다:
- 습도가 70% 이상인 센서
- 최근 30분 이내

<details>
<summary>해답</summary>

```sql
SELECT sensor_id, humidity, time
FROM warehouse_sensors
WHERE humidity > 70.0
DURATION 30 MINUTE;
```

또는 롤업 사용:

```sql
SELECT sensor_id, max_humidity
FROM warehouse_sensors
WHERE rollup = min
  AND max_humidity > 70.0
DURATION 30 MINUTE;
```
</details>

### 연습 3: 과거 분석

최근 7일 동안 가장 뜨겁고 가장 차가운 센서를 찾습니다:

<details>
<summary>해답</summary>

```sql
-- 가장 뜨거운 센서
SELECT sensor_id, MAX(max_temperature) as highest_temp
FROM warehouse_sensors
WHERE rollup = hour
DURATION 7 DAY
GROUP BY sensor_id
ORDER BY highest_temp DESC
LIMIT 1;

-- 가장 차가운 센서
SELECT sensor_id, MIN(min_temperature) as lowest_temp
FROM warehouse_sensors
WHERE rollup = hour
DURATION 7 DAY
GROUP BY sensor_id
ORDER BY lowest_temp ASC
LIMIT 1;
```
</details>

## 실제 적용

다음을 통해 프로덕션 환경으로 확장합니다:

### 1. 대량 삽입 API 사용

개별 INSERT 대신 APPEND 프로토콜을 사용합니다:

```c
// C/CLI 예제
SQLAppendOpen(stmt, "warehouse_sensors");
SQLAppendDataV(stmt, "zone1-temp01", time_val, 22.5, 55.2);
SQLAppendDataV(stmt, "zone1-temp01", time_val, 22.7, 55.0);
// ... 더 많은 레코드
SQLAppendClose(stmt);
```

### 2. 모니터링 대시보드 생성

```sql
-- 실시간 대시보드 쿼리
SELECT
    sensor_id,
    temperature,
    humidity,
    time
FROM warehouse_sensors
DURATION 5 MINUTE
ORDER BY time DESC;
```

### 3. 자동 경고 설정

```bash
#!/bin/bash
# check_sensors.sh - cron을 통해 5분마다 실행

machsql -s localhost -u SYS -p MANAGER -f - <<EOF
SELECT sensor_id, temperature
FROM warehouse_sensors
WHERE temperature > 30.0
DURATION 5 MINUTE;
EOF
```

### 4. 애플리케이션과 통합

SDK를 사용하여 연결:
- **Python**: machbase-python을 통해 연결
- **Java**: JDBC 드라이버 사용
- **C/C++**: CLI/ODBC API
- **REST API**: HTTP 기반 통합

## 성능 팁

1. **배치 삽입**: 대용량 데이터를 위해 APPEND 프로토콜 사용
2. **롤업 사용**: 통계를 위해 원시 데이터 대신 롤업 테이블 쿼리
3. **시간 범위 제한**: WHERE 절에 항상 시간 조건 사용
4. **적절한 인덱싱**: Tag 테이블은 자동 인덱스 - 관리 불필요

## 일반 패턴

### 패턴: 다중 값 센서

```sql
-- 여러 측정값을 가진 센서
CREATE TAGDATA TABLE multi_sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED,
    pressure DOUBLE SUMMARIZED,
    vibration DOUBLE SUMMARIZED,
    rpm DOUBLE SUMMARIZED
);
```

### 패턴: 계층적 센서 ID

```sql
-- 구조화된 이름 사용
-- 형식: building-floor-room-type-number
INSERT INTO warehouse_sensors
VALUES ('building1-floor2-roomA-temp-01', NOW, 22.5, 55.0);

-- 패턴으로 쿼리
SELECT * FROM warehouse_sensors
WHERE sensor_id LIKE 'building1-floor2%'
DURATION 1 HOUR;
```

## 달성한 내용

✓ 센서 데이터를 위한 Tag 테이블 생성
✓ 시계열 측정값 삽입
✓ 센서 ID 및 시간별 데이터 쿼리
✓ 자동 롤업 통계 사용
✓ 센서 메타데이터 관리
✓ 데이터 보존 구현
✓ 이상 징후 감지 쿼리 구축

## 다음 단계

- **튜토리얼 2**: [애플리케이션 로그](../application-logs/) - Log 테이블 학습
- **심화 학습**: [Tag 테이블 레퍼런스](../../table-types/tag-tables/) - 고급 기능
- **일반 작업**: [데이터 가져오기](../../common-tasks/importing-data/) - 대량 로딩

## 핵심 요점

1. **Tag 테이블**은 (sensor_id, time, value) 데이터에 최적화됨
2. **SUMMARIZED** 컬럼은 자동 통계 생성 가능
3. **롤업 쿼리**는 즉시 집계(min, max, avg) 제공
4. **메타데이터 테이블**은 센서 정보를 별도로 저장
5. **시간 기반 삭제**는 데이터 보존을 효율적으로 관리

---

**훌륭합니다!** 이제 Machbase에서 IoT 센서 데이터를 처리하는 방법을 알게 되었습니다. [튜토리얼 2: 애플리케이션 로그](../application-logs/)로 계속 진행하세요!
