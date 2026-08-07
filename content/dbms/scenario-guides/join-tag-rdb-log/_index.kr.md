---
type: docs
title: '16.2 TAG + TRANSACTION + LOG 조인 대시보드'
weight: 40
toc: true
---

TAG(시계열), TRANSACTION(관계형), LOG(이벤트) 세 가지 테이블 유형을 하나의 SQL로 조인할 수 있습니다. 장비별 최신 센서값, 장비 마스터 정보, 시스템 이벤트 로그를 통합해 운영 대시보드를 구성하는 시나리오입니다.

## 시나리오 구성도

```
[센서 데이터]  → TAG 테이블   (sensor_tag)     ─┐
[장비 마스터]  → TRANSACTION 테이블   (equipment)       ─┼→ 통합 대시보드 쿼리
[시스템 이벤트] → LOG 테이블  (system_event_log) ─┘
```

## 테이블 스키마 설계

테이블별 역할에 맞게 스키마를 설계합니다.

```sql
-- 1. TAG 테이블: 센서 시계열 데이터
CREATE TAG TABLE sensor_tag (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 2. TRANSACTION 테이블: 장비 마스터 (관계형 참조 데이터)
CREATE TRANSACTION TABLE equipment (
    eq_id      VARCHAR(32),
    eq_name    VARCHAR(128),
    location   VARCHAR(64),
    threshold  DOUBLE,
    owner      VARCHAR(64)
);

-- 3. LOG 테이블: 시스템 이벤트 (시간순 이벤트 기록)
CREATE LOG TABLE system_event_log (
    eq_id    VARCHAR(32),
    severity VARCHAR(10),
    message  VARCHAR(1024)
);
```

## 장비 마스터 데이터 등록

TRANSACTION 테이블에 장비 기준 정보를 등록합니다:

```sql
INSERT INTO equipment VALUES ('EQ-001', '압축기 #1', 'A동 3층', 85.0, '홍길동');
INSERT INTO equipment VALUES ('EQ-002', '펌프 #2',   'B동 1층', 72.0, '이영희');
INSERT INTO equipment VALUES ('EQ-003', '모터 #3',   'C동 2층', 90.0, '박철수');
```

## TAG + TRANSACTION 조인: 현재 센서값 + 장비 정보

각 태그의 최신값과 장비 마스터를 조인해 상태 현황을 조회합니다.

```sql
-- 최신 센서값과 장비 마스터 조인
SELECT
    e.eq_id,
    e.eq_name,
    e.location,
    RECENT_ROW.latest_time,
    RECENT_ROW.latest_value,
    e.threshold,
    CASE
        WHEN RECENT_ROW.latest_value > e.threshold THEN '경보'
        WHEN RECENT_ROW.latest_value > e.threshold * 0.9 THEN '주의'
        ELSE '정상'
    END AS status
FROM equipment e
JOIN (
    SELECT name, RECENT(time, 1) AS latest_time, RECENT(value, 1) AS latest_value
    FROM sensor_tag
    GROUP BY name
) RECENT_ROW ON e.eq_id = RECENT_ROW.name;
```

## TAG + LOG 시간 기반 상관 분석

센서값 이상과 시스템 이벤트의 시간적 연관성을 분석합니다.

```sql
-- 경보 발생 시점 전후 10분 이벤트 확인
SELECT
    t.name,
    t.time AS sensor_time,
    t.value,
    l.message AS event_message,
    l._arrival_time AS event_time
FROM sensor_tag t
JOIN system_event_log l
  ON t.name = l.eq_id
 AND l._arrival_time BETWEEN ADD_TIME(t.time, '0/0/0 0:-10:0')
                         AND ADD_TIME(t.time, '0/0/0 0:10:0')
WHERE t.value > 80
  AND t.time > ADD_TIME(SYSDATE, '0/0/-1 0:0:0')
ORDER BY t.time;
```

## 복합 집계 대시보드 쿼리

장비별 최근 1시간 평균값, 이벤트 건수를 한 번에 조회합니다.

```sql
SELECT
    e.eq_id,
    e.eq_name,
    e.location,
    AVG(t.value)   AS avg_1h,
    MAX(t.value)   AS max_1h,
    MIN(t.value)   AS min_1h,
    COUNT(t.value) AS sample_count,
    (SELECT COUNT(*) FROM system_event_log l
      WHERE l.eq_id = e.eq_id
        AND l._arrival_time > ADD_TIME(SYSDATE, '0/0/0 -1:0:0')) AS event_count_1h
FROM equipment e
JOIN sensor_tag t
  ON e.eq_id = t.name
WHERE t.time > ADD_TIME(SYSDATE, '0/0/0 -1:0:0')
GROUP BY e.eq_id, e.eq_name, e.location
ORDER BY avg_1h DESC;
```

## 임계값 초과 장비 목록 조회

임계값을 초과한 장비와 담당자를 즉시 확인합니다.

```sql
SELECT
    e.eq_id,
    e.eq_name,
    e.owner,
    RECENT_ROW.latest_value,
    e.threshold,
    ROUND(RECENT_ROW.latest_value / e.threshold * 100, 1) AS pct
FROM equipment e
JOIN (
    SELECT name, RECENT(value, 1) AS latest_value
    FROM sensor_tag
    GROUP BY name
) RECENT_ROW ON e.eq_id = RECENT_ROW.name
WHERE RECENT_ROW.latest_value > e.threshold
ORDER BY pct DESC;
```

## 성능 고려사항

| 항목 | 권장 사항 |
|------|-----------|
| TAG RECENT 조회 | 태그 수가 많을 경우 GROUP BY name으로 그룹화 |
| TRANSACTION JOIN | 장비 마스터처럼 관계형 참조 데이터와 조인 |
| LOG 기간 필터 | `_arrival_time` 조건을 반드시 포함해 스캔 범위 제한 |
| 복합 조인 | 서브쿼리 또는 Standard Edition의 CTE로 단계 분리 시 가독성·성능 향상 |

> TAG 테이블과 LOG 테이블을 시간 범위로 조인할 때는 검색 범위(`BETWEEN`)를 최대한 좁혀 전체 스캔을 방지하십시오.
