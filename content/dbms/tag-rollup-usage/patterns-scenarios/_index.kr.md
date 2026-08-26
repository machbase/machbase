---
title: '6.12 ROLLUP 활용 시나리오'
weight: 120
toc: true
---

<a id="storage-sensor-data-rollup"></a>

## 센서 데이터 저장과 ROLLUP 분석

TAG 원시 데이터에 1분 ROLLUP을 만들고 gap을 확인한 뒤 시간 구간 집계를 조회합니다. 예제는
고유한 `SC6_` 객체를 사용하며 마지막에 정리합니다.

### 1단계: TAG 테이블과 데이터

```sql
CREATE TAG TABLE sc6_sensor (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

INSERT INTO sc6_sensor METADATA VALUES ('TEMP_01');
INSERT INTO sc6_sensor METADATA VALUES ('PRESS_01');

INSERT INTO sc6_sensor VALUES (
    'TEMP_01', TO_DATE('2026-08-25 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 20.0);
INSERT INTO sc6_sensor VALUES (
    'TEMP_01', TO_DATE('2026-08-25 10:00:30', 'YYYY-MM-DD HH24:MI:SS'), 22.0);
INSERT INTO sc6_sensor VALUES (
    'PRESS_01', TO_DATE('2026-08-25 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1.02);

EXEC TABLE_FLUSH(sc6_sensor);
```

대량 입력은 이 페이지에 SDK 코드를 복제하지 않고
[개발 도구 연동](/dbms/development-tools-integration/)의 현재 Append quickstart를 사용합니다.

### 2단계: ROLLUP 생성과 상태 확인

```sql
CREATE ROLLUP sc6_sensor_ru_1m
    ON sc6_sensor(value)
    INTERVAL 1 MIN;

SHOW ROLLUPGAP;
SELECT * FROM V$ROLLUP;
```

ROLLUP은 비동기로 원시 데이터를 처리합니다. 조회 결과를 검증하기 전에 대상 ROLLUP의 gap이
0인지 확인하십시오. 생성 직후 gap이 남아 있는 상태에서 집계 결과가 완성됐다고 가정하지
않습니다.

### 3단계: 구간 집계 조회

```sql
SELECT name,
       ROLLUP('min', 1, time) AS bucket_time,
       AVG(value) AS avg_value,
       MIN(value) AS min_value,
       MAX(value) AS max_value,
       COUNT(value) AS sample_count
  FROM sc6_sensor
 WHERE name = 'TEMP_01'
   AND time BETWEEN TO_DATE('2026-08-25 09:59:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2026-08-25 10:02:00', 'YYYY-MM-DD HH24:MI:SS')
 GROUP BY name, bucket_time
 ORDER BY bucket_time;
```

최근 원시 데이터는 `ADD_TIME(SYSDATE, ...)`로 범위를 제한합니다.

```sql
SELECT name, time, value
  FROM sc6_sensor
 WHERE name = 'TEMP_01'
   AND time >= ADD_TIME(SYSDATE, '0/0/0 0:-5:0')
 ORDER BY time DESC;
```

### 4단계: 정리

```sql
DROP ROLLUP sc6_sensor_ru_1m;
DROP TABLE sc6_sensor;
```

<a id="use-cases-rollup"></a>

## ROLLUP 활용 사례

| 요구사항 | 설계 시작점 |
|---|---|
| 실시간 대시보드 | 최근 구간은 원본, 장기 구간은 ROLLUP. gap을 함께 감시 |
| 정상 품질만 집계 | 조건부 ROLLUP의 predicate를 실제 품질 열과 대조 |
| OHLC·첫값·마지막값 | EXTENSION ROLLUP과 `FIRST`/`LAST` 지원 범위 확인 |
| 여러 태그 비교 | 같은 bucket과 시간 범위를 사용해 집계한 뒤 PIVOT 검토 |
| 누적 계량기 | 구간 `FIRST`와 `LAST` 차이, reset·wraparound 정책 정의 |

각 문법의 정본은 [ROLLUP SQL](/dbms/reference/sql/syntax-dictionary-sql/rollup-syntax/)과 이 장의
생성·조건·확장 ROLLUP 페이지를 사용하십시오. 고정된 간격 체인이나 성능 수치를 그대로
복사하지 말고 데이터 주기와 조회 구간을 측정해 결정합니다.
