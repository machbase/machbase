---
type: docs
title: '15.1 실시간 상태 대시보드'
weight: 10
toc: true
---

TAG 테이블의 최신값과 LOOKUP 테이블의 임계값을 결합해 현재 상태를 계산합니다. 예제는
`SC15_DASHBOARD_` 접두사를 사용하며 마지막에 객체를 정리합니다.

## 사전 준비

```sql
CREATE TAG TABLE sc15_dashboard_tag (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

CREATE LOOKUP TABLE sc15_dashboard_threshold (
    tag_name   VARCHAR(64) PRIMARY KEY,
    warn_value DOUBLE,
    crit_value DOUBLE
);

INSERT INTO sc15_dashboard_tag METADATA VALUES ('TEMP_01');
INSERT INTO sc15_dashboard_tag METADATA VALUES ('TEMP_02');
INSERT INTO sc15_dashboard_tag METADATA VALUES ('PRESS_01');

INSERT INTO sc15_dashboard_tag VALUES ('TEMP_01', SYSDATE, 72.3);
INSERT INTO sc15_dashboard_tag VALUES ('TEMP_02', SYSDATE, 88.1);
INSERT INTO sc15_dashboard_tag VALUES ('PRESS_01', SYSDATE, 1.04);

INSERT INTO sc15_dashboard_threshold VALUES ('TEMP_01', 80.0, 90.0);
INSERT INTO sc15_dashboard_threshold VALUES ('TEMP_02', 80.0, 90.0);
INSERT INTO sc15_dashboard_threshold VALUES ('PRESS_01', 1.10, 1.20);

EXEC TABLE_FLUSH(sc15_dashboard_tag);
```

## 1단계: 최신 센서값 조회

한 태그의 최신값은 역방향 스캔과 `LIMIT 1`로 조회할 수 있습니다.

```sql
SELECT /*+ SCAN_BACKWARD(sc15_dashboard_tag) */
       name, time, value
  FROM sc15_dashboard_tag
 WHERE name = 'TEMP_01'
 LIMIT 1;
```

여러 태그는 TAG 통계 뷰의 `RECENT_ROW_TIME`과 원본 테이블을 조인합니다.

```sql
SELECT t.name, t.time, t.value
  FROM sc15_dashboard_tag t
  JOIN v$sc15_dashboard_tag_stat s
    ON t.name = s.name
   AND t.time = s.recent_row_time
 ORDER BY t.name;
```

## 2단계: 상태 판정

```sql
WITH latest AS (
    SELECT t.name, t.time, t.value
      FROM sc15_dashboard_tag t
      JOIN v$sc15_dashboard_tag_stat s
        ON t.name = s.name
       AND t.time = s.recent_row_time
)
SELECT l.name,
       l.time AS last_time,
       l.value AS current_value,
       CASE
         WHEN l.value >= c.crit_value THEN 'CRITICAL'
         WHEN l.value >= c.warn_value THEN 'WARNING'
         ELSE 'NORMAL'
       END AS status
  FROM latest l
  JOIN sc15_dashboard_threshold c
    ON l.name = c.tag_name
 ORDER BY l.name;
```

대시보드 API는 이 쿼리의 결과를 반환하고, 연결 실패와 오래된 `LAST_TIME`을 별도 상태로
표현하는 것이 좋습니다. 폴링 간격은 고정값을 복사하지 말고 데이터 유입 주기, 허용 지연,
동시 사용자와 쿼리 비용을 측정해 정합니다.

Grafana 등 외부 도구의 설치와 연결은
[외부 도구 연동](/dbms/development-tools-integration/external-tools/)을 참고하십시오.

## 3단계: 정리

```sql
DROP TABLE sc15_dashboard_threshold;
DROP TABLE sc15_dashboard_tag;
```
