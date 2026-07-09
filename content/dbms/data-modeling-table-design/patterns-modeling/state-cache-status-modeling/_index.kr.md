---
type: docs
title: '4.3.3 상태·캐시 모델링'
weight: 30
---

디바이스나 센서의 현재 상태를 실시간으로 조회하기 위한 캐시 모델링 패턴입니다.

## 최신 상태 캐시 패턴

VOLATILE 테이블로 각 디바이스의 현재 상태를 캐싱합니다.

```sql
-- 상태 캐시 (VOLATILE)
CREATE VOLATILE TABLE device_status (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);

-- 상태 이력 (TAG 또는 LOG)
CREATE TAG TABLE device_status_history (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE,
    status VARCHAR(16)
);
```

## 상태 업데이트 흐름

```sql
-- 새 계측값 수신 시:
-- 1. TAG 테이블에 이력 저장
INSERT INTO device_status_history VALUES ('DEV-01', NOW, 78.5, 'WARNING');

-- 2. VOLATILE 캐시 업데이트 (ON DUPLICATE KEY UPDATE)
INSERT INTO device_status VALUES ('DEV-01', 'WARNING', 78.5, NOW)
ON DUPLICATE KEY UPDATE SET status = 'WARNING', value = 78.5, updated_at = NOW;
```

## 대시보드 조회 패턴

```sql
-- 현재 ALARM 상태인 모든 디바이스
SELECT device_id, status, value, updated_at
FROM device_status
WHERE status IN ('ALARM', 'WARNING')
ORDER BY updated_at DESC;

-- 특정 디바이스의 최신 상태
SELECT device_id, status, value, updated_at
FROM device_status
WHERE device_id = 'DEV-01';
```

## 상태 정의 참조 패턴

상태 코드의 의미는 LOOKUP 테이블에서 관리합니다.

```sql
CREATE LOOKUP TABLE status_definition (
    code    VARCHAR(16) PRIMARY KEY,
    label   VARCHAR(64),
    color   VARCHAR(16),
    severity SHORT
);

INSERT INTO status_definition VALUES ('NORMAL', '정상', 'green', 0);
INSERT INTO status_definition VALUES ('WARNING', '경고', 'yellow', 1);
INSERT INTO status_definition VALUES ('ALARM', '알람', 'red', 2);

-- JOIN 조회
SELECT d.device_id, s.label, s.color, d.value
FROM device_status d
JOIN status_definition s ON d.status = s.code
ORDER BY s.severity DESC;
```
