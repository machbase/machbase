---
type: docs
title: '9.9 Patterns and Scenarios'
weight: 90
toc: true
aliases:
  - /dbms/lookup-table-usage/reference-master-modeling/
---
This section covers LOOKUP usage patterns and scenarios.


<a id="use-cases-lookup"></a>

## Use Cases

LOOKUP tables are suitable for the following data.

<a id="lookup-pattern-data-types"></a>

## Suitable Data Types

| Type | Examples |
|------|------|
| Code tables | Country, language, and status codes |
| Reference data | Equipment lists, product categories, and departments |
| Reference values updated in real time | Exchange-rate tables and threshold settings |
| Alternative to tag metadata | Small sensor-information datasets |

<a id="lookup-pattern-code-table"></a>

<a id="patterns-reference-design"></a>

## Code Tables

```sql
CREATE LOOKUP TABLE ch9_pattern_country (
    code   VARCHAR(4)   PRIMARY KEY,
    name   VARCHAR(64),
    region VARCHAR(32)
);

INSERT INTO ch9_pattern_country VALUES ('KR', '대한민국', 'Asia');
INSERT INTO ch9_pattern_country VALUES ('US', '미국', 'America');
UPDATE ch9_pattern_country SET name = 'United States' WHERE code = 'US';

SELECT code, name FROM ch9_pattern_country ORDER BY code;
```

Two rows are returned. Only the US row's name has changed to `United States`.

Manage status and alarm codes the same way and join them to source events.

```sql
CREATE LOOKUP TABLE ch9_pattern_status (
    code  VARCHAR(16) PRIMARY KEY,
    label VARCHAR(64),
    color VARCHAR(16)
);
INSERT INTO ch9_pattern_status VALUES ('RUN',  '가동', 'green');
INSERT INTO ch9_pattern_status VALUES ('STOP', '정지', 'red');

CREATE LOG TABLE ch9_pattern_event (
    event_time DATETIME,
    device_id  VARCHAR(64),
    status     VARCHAR(16)
);
INSERT INTO ch9_pattern_event
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'DEV-01', 'RUN');
INSERT INTO ch9_pattern_event
VALUES (TO_DATE('2026-01-01 10:05:00', 'YYYY-MM-DD HH24:MI:SS'), 'DEV-01', 'STOP');
EXEC TABLE_FLUSH(ch9_pattern_event);

SELECT e.event_time, e.device_id, c.label
  FROM ch9_pattern_event e
  JOIN ch9_pattern_status c ON e.status = c.code
 ORDER BY e.event_time;
```

The two rows display the labels `가동` (running) and `정지` (stopped) instead of codes. An event with a
status missing from the code table is excluded by the INNER JOIN, so also check for missing codes.

<a id="lookup-pattern-equipment-master"></a>

## Equipment Master Data

```sql
CREATE LOOKUP TABLE ch9_pattern_equip (
    equip_id   VARCHAR(32) PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    dept       VARCHAR(64),
    install_dt DATETIME
);
INSERT INTO ch9_pattern_equip
VALUES ('TEMP-01', 'Boiler', 'Seoul', 'Production',
        TO_DATE('2025-01-01', 'YYYY-MM-DD'));
INSERT INTO ch9_pattern_equip
VALUES ('TEMP-02', 'Chiller', 'Busan', 'Facility',
        TO_DATE('2025-01-01', 'YYYY-MM-DD'));
```

Join sensor data in a TAG table to retrieve reference information such as location and department.

```sql
CREATE TAG TABLE ch9_pattern_sensor (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
INSERT INTO ch9_pattern_sensor
VALUES ('TEMP-01', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 90.0);
INSERT INTO ch9_pattern_sensor
VALUES ('TEMP-02', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 20.0);
EXEC TABLE_FLUSH(ch9_pattern_sensor);

SELECT d.name, m.location, m.dept, d.value
  FROM ch9_pattern_sensor d
  JOIN ch9_pattern_equip m ON d.name = m.equip_id
 WHERE m.dept = 'Production'
 ORDER BY d.name;
```

Only TEMP-01 is returned. The department predicate applies to a LOOKUP column, so changing it
changes the result set even when the TAG source data is unchanged.

<a id="lookup-pattern-threshold"></a>

## Threshold Settings

```sql
CREATE LOOKUP TABLE ch9_pattern_threshold (
    sensor_name VARCHAR(64) PRIMARY KEY,
    low_limit   DOUBLE,
    high_limit  DOUBLE,
    alert_level SHORT
);
INSERT INTO ch9_pattern_threshold VALUES ('TEMP-01', 0.0, 100.0, 1);
INSERT INTO ch9_pattern_threshold VALUES ('TEMP-02', 0.0, 100.0, 1);

-- Change the threshold in real time
UPDATE ch9_pattern_threshold SET high_limit = 85.0 WHERE sensor_name = 'TEMP-01';
```

Join the threshold table with TAG data to evaluate alarm conditions.

```sql
SELECT s.name, s.value, t.high_limit
  FROM ch9_pattern_sensor s
  JOIN ch9_pattern_threshold t ON s.name = t.sensor_name
 WHERE s.value > t.high_limit
 ORDER BY s.name;
```

Only TEMP-01 exceeds its threshold. The value 90 was normal under the previous limit of 100. Record
when thresholds change because the same source value can produce a different decision.

<a id="lookup-pattern-sequence-master"></a>

## SEQUENCE-Based History Numbers

Use a SEQUENCE column when small administrative histories or operational events need sequential identifiers.

```sql
CREATE LOOKUP TABLE ch9_pattern_note (
    seq        LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    target_id  VARCHAR(64),
    note       VARCHAR(512),
    created_at DATETIME
);

INSERT INTO ch9_pattern_note
VALUES (NEXTVAL(seq), 'TEMP-01', 'threshold changed', NOW);
INSERT INTO ch9_pattern_note
VALUES (NEXTVAL(seq), 'TEMP-02', 'inspection done', NOW);

SELECT seq, target_id FROM ch9_pattern_note ORDER BY seq;
```

The seq values are 1 and 2. Store large source histories in LOG rather than LOOKUP.

Clean up the example objects as follows.

```sql
DROP TABLE ch9_pattern_note;
DROP TABLE ch9_pattern_threshold;
DROP TABLE ch9_pattern_sensor;
DROP TABLE ch9_pattern_equip;
DROP TABLE ch9_pattern_event;
DROP TABLE ch9_pattern_status;
DROP TABLE ch9_pattern_country;
```

<a id="lookup-pattern-not-suitable"></a>

## Unsuitable Cases

- Data requiring explicit transactions and general relational DML → TRANSACTION recommended
- Append-only history requiring no UPDATE → LOG recommended
- Sensor measurements → TAG recommended
- Current-state caches that may be lost on restart → VOLATILE recommended
