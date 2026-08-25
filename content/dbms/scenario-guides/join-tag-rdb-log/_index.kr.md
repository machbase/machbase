---
type: docs
title: '15.3 TAG·TRANSACTION·LOG 조인'
weight: 30
toc: true
---

TAG 센서값, TRANSACTION 장비 마스터, LOG 이벤트를 고유 키와 시간 범위로 결합합니다.

## 테이블과 데이터 준비

```sql
CREATE TAG TABLE sc15_join_tag (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

CREATE TRANSACTION TABLE sc15_join_equipment (
    eq_id     VARCHAR(32),
    eq_name   VARCHAR(64),
    threshold DOUBLE
);

CREATE LOG TABLE sc15_join_event (
    eq_id    VARCHAR(32),
    severity VARCHAR(10),
    message  VARCHAR(256)
);

INSERT INTO sc15_join_equipment VALUES ('EQ-001', '압축기 1', 85.0);
INSERT INTO sc15_join_equipment VALUES ('EQ-002', '펌프 2', 72.0);

INSERT INTO sc15_join_tag METADATA VALUES ('EQ-001');
INSERT INTO sc15_join_tag METADATA VALUES ('EQ-002');
INSERT INTO sc15_join_tag VALUES ('EQ-001', SYSDATE, 88.5);
INSERT INTO sc15_join_tag VALUES ('EQ-002', SYSDATE, 65.0);

INSERT INTO sc15_join_event VALUES ('EQ-001', 'WARN', 'temperature threshold');
EXEC TABLE_FLUSH(sc15_join_tag);
```

## TAG + TRANSACTION 최신 상태 조인

```sql
WITH latest AS (
    SELECT t.name, t.time, t.value
      FROM sc15_join_tag t
      JOIN v$sc15_join_tag_stat s
        ON t.name = s.name
       AND t.time = s.recent_row_time
)
SELECT e.eq_id, e.eq_name, l.time, l.value, e.threshold,
       CASE WHEN l.value > e.threshold THEN 'ALARM' ELSE 'NORMAL' END AS state
  FROM sc15_join_equipment e
  JOIN latest l
    ON e.eq_id = l.name
 ORDER BY e.eq_id;
```

구현되지 않은 `RECENT()` 함수 대신 TAG 통계 뷰의 최신 시각을 사용합니다.

## TAG + LOG 시간 범위 조인

```sql
SELECT t.name, t.time AS sensor_time, t.value,
       l._arrival_time AS event_time, l.severity, l.message
  FROM sc15_join_tag t
  JOIN sc15_join_event l
    ON t.name = l.eq_id
   AND l._arrival_time BETWEEN ADD_TIME(t.time, '0/0/0 0:-10:0')
                           AND ADD_TIME(t.time, '0/0/0 0:10:0')
 WHERE t.value > 80
 ORDER BY t.time, l._arrival_time;
```

시간 조인은 양쪽 데이터량을 크게 늘릴 수 있습니다. TAG 이름과 LOG 장비 ID로 먼저 대상을
좁히고, 서비스가 요구하는 최소 시간 범위를 사용합니다.

## 정리

```sql
DROP TABLE sc15_join_event;
DROP TABLE sc15_join_tag;
DROP TABLE sc15_join_equipment;
```
