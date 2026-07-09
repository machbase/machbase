---
type: docs
title: '10.9.1 활용 사례'
weight: 10
---

VOLATILE 테이블이 적합한 대표적인 활용 사례를 소개합니다.

## 적합한 데이터 유형

| 유형 | 설명 |
|------|------|
| 실시간 집계 캐시 | 최근 N분 집계 결과를 캐싱 |
| 세션 상태 저장 | 애플리케이션 세션 데이터 |
| 임시 조인 중간 테이블 | 복잡한 쿼리 최적화용 중간 결과 |
| 최신 값 캐시 (Last Known Value) | 센서별 최신 계측값 |
| 대시보드 캐시 | 자주 조회되는 집계 데이터 |

## 예시: 최신 센서 값 캐시

```sql
CREATE VOLATILE TABLE sensor_latest (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);

-- 최신 값 업데이트 (ON DUPLICATE KEY UPDATE 사용)
INSERT INTO sensor_latest VALUES ('TEMP-01', 25.3, NOW)
ON DUPLICATE KEY UPDATE SET value = 25.3, updated_at = NOW;

-- 현재 모든 센서 최신값 조회
SELECT sensor_id, value, updated_at FROM sensor_latest;
```

## 예시: 실시간 집계 캐시

```sql
CREATE VOLATILE TABLE recent_summary (
    key_id    VARCHAR(64) PRIMARY KEY,
    sensor_id VARCHAR(64),
    base_ts   DATETIME,
    avg_val   DOUBLE,
    max_val   DOUBLE,
    count     INTEGER
);

-- 1시간마다 집계 갱신
DELETE FROM recent_summary;

INSERT INTO recent_summary
SELECT name,
       name, MAX(DATE_TRUNC('hour', time, 1)), AVG(value), MAX(value), COUNT(*)
FROM sensor_data
WHERE time >= NOW - 3600000000000
GROUP BY name;
```

## 부적합한 경우

- 서버 재시작 후에도 데이터가 필요한 경우 → LOOKUP 또는 RDB 테이블
- 대용량 데이터 → 메모리 부족 위험
