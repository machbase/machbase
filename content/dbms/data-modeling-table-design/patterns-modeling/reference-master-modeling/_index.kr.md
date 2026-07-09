---
type: docs
title: '4.3.5 참조·마스터 모델링'
weight: 50
---

코드 테이블, 설비 마스터, 사용자 정보 등 참조 데이터를 LOOKUP 테이블로 모델링하는 패턴입니다.

## 계층적 코드 체계

```sql
-- 대분류 코드
CREATE LOOKUP TABLE category_main (
    code  VARCHAR(8)  PRIMARY KEY,
    label VARCHAR(64)
);

-- 중분류 코드 (대분류 참조)
CREATE LOOKUP TABLE category_sub (
    code      VARCHAR(16) PRIMARY KEY,
    main_code VARCHAR(8),
    label     VARCHAR(64)
);

CREATE INDEX idx_sub_main ON category_sub(main_code);
```

## 설비 계층 마스터

```sql
-- 공장 마스터
CREATE LOOKUP TABLE factory (
    factory_id VARCHAR(16) PRIMARY KEY,
    name       VARCHAR(64),
    location   VARCHAR(128)
);

-- 라인 마스터 (공장 참조)
CREATE LOOKUP TABLE production_line (
    line_id    VARCHAR(16) PRIMARY KEY,
    factory_id VARCHAR(16),
    name       VARCHAR(64)
);

-- 설비 마스터 (라인 참조)
CREATE LOOKUP TABLE equipment (
    equip_id   VARCHAR(32) PRIMARY KEY,
    line_id    VARCHAR(16),
    equip_name VARCHAR(128),
    equip_type VARCHAR(32),
    install_dt DATETIME
);

CREATE INDEX idx_equip_line ON equipment(line_id);
CREATE INDEX idx_equip_type ON equipment(equip_type);
```

## 마스터 조인 조회 패턴

```sql
-- 센서 데이터 + 설비 정보 조인
SELECT s.name AS sensor_id,
       e.equip_name,
       l.name AS line_name,
       f.name AS factory_name,
       s.time,
       s.value
FROM sensor_data s
JOIN equipment e     ON s.name = e.equip_id
JOIN production_line l ON e.line_id = l.line_id
JOIN factory f       ON l.factory_id = f.factory_id
WHERE f.factory_id = 'F01'
  AND s.time >= NOW - 3600000000000;
```
