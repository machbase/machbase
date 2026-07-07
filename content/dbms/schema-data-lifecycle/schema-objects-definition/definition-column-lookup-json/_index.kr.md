---
type: docs
title: 'LOOKUP JSON 컬럼 정의'
weight: 60
---

> 현재 빌드에서는 LOOKUP 테이블의 `JSON` 타입 컬럼을 사용할 수 없습니다. `CREATE LOOKUP TABLE ... JSON`은 오류가 발생합니다.

## 개요

LOOKUP 테이블에 구조화되지 않은 속성을 보관해야 하면 `VARCHAR` 컬럼에 JSON 문자열을 저장합니다. JSON 내부 필드를 자주 조건으로 사용해야 하는 값은 별도 컬럼으로 분리합니다.

## 대안 예시

```sql
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    name      VARCHAR(100),
    config    VARCHAR(4096)
);

-- JSON 데이터 삽입
INSERT INTO device_config VALUES (
    'DEV-01',
    '온도 센서 A',
    '{"location": "zone-1", "threshold": {"high": 85.0, "low": 5.0}}'
);

-- JSON 문자열 전체 조회
SELECT device_id, name, config
FROM device_config
WHERE device_id = 'DEV-01';
```

## 제약 사항

- LOOKUP 테이블에서는 `JSON` 타입 컬럼을 생성할 수 없습니다.
- JSON 문자열 내부 필드에는 인덱스를 생성할 수 없습니다.
- JSON 문자열 내부 필드를 SQL JSON path 조건으로 필터링할 수 없습니다.

## 권장 설계

필터링이나 조인이 필요한 필드는 별도 컬럼으로 분리합니다.

```sql
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    name      VARCHAR(100),
    location  VARCHAR(64),
    high_limit DOUBLE,
    config    VARCHAR(4096)
);
```

> TAG 메타데이터의 JSON 지원 범위는 별도로 확인해야 합니다.
