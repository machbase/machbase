---
type: docs
title: 'LOOKUP JSON 컬럼 정의 (planned: dbms-nfx#3696; JSON primary key 제외)'
weight: 60
---

> **계획된 기능**: LOOKUP 테이블의 JSON 컬럼 지원은 dbms-nfx#3696에서 개발 중입니다. 현재 버전(8.6)에서는 아직 사용할 수 없습니다.

## 개요

LOOKUP 테이블에 JSON 타입 컬럼을 추가할 수 있게 되면, 구조화되지 않은 메타데이터를 유연하게 저장하고 조회할 수 있습니다. TAG 메타데이터에서 JSON 컬럼을 활용하는 것과 유사한 방식으로 동작할 예정입니다.

## 예상 사용 예시 (향후 지원 예정)

```sql
-- JSON 컬럼을 포함한 LOOKUP 테이블 생성 (예정)
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    name      VARCHAR(100),
    config    JSON
);

-- JSON 데이터 삽입
INSERT INTO device_config VALUES (
    'DEV-01',
    '온도 센서 A',
    '{"location": "zone-1", "threshold": {"high": 85.0, "low": 5.0}}'
);

-- JSON 필드 조회
SELECT device_id, name, config->'location' AS location
FROM device_config;
```

## 제약 사항 (예정)

- JSON 컬럼은 PRIMARY KEY로 지정할 수 없습니다.
- JSON 컬럼에 대한 인덱스 생성은 지원되지 않을 예정입니다.

## 현재 대안

현재 버전에서는 JSON 데이터를 `VARCHAR` 또는 `TEXT` 컬럼으로 문자열 형태로 저장하는 방법을 사용합니다.

```sql
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    name      VARCHAR(100),
    config    VARCHAR(4096)  -- JSON 문자열 저장
);
```

> TAG 메타데이터에서의 JSON 컬럼 활용 방법은 [TAG 테이블 설계](/dbms/data-modeling-table-design/table-types-design-type/design-tag-dbms-nfx/) 문서를 참고하세요.
