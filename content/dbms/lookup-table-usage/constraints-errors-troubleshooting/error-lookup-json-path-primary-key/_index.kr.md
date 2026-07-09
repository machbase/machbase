---
type: docs
title: 'LOOKUP JSON primary key 오류'
weight: 40
---

LOOKUP 테이블은 `JSON` 타입 컬럼을 일반 컬럼으로 지원하지만, `JSON` 컬럼을 primary key로
선언할 수는 없습니다.

## 증상

```sql
CREATE LOOKUP TABLE device_config (
    config JSON PRIMARY KEY,
    note   VARCHAR(32)
);
```

위와 같이 실행하면 JSON 컬럼을 primary key로 사용할 수 없다는 오류가 발생합니다.

## 원인

Primary key는 row를 안정적으로 식별해야 합니다. LOOKUP 테이블의 JSON 컬럼은 저장, 조회,
조건 검색, 갱신에는 사용할 수 있지만 primary key 타입으로는 허용되지 않습니다.

## 해결 방법

식별자는 별도 컬럼으로 분리하고 JSON은 일반 컬럼으로 둡니다.

```sql
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(64) PRIMARY KEY,
    config    JSON
);

INSERT INTO device_config VALUES (
    'DEV-001',
    '{"status":"active","version":"1.0"}'
);
```

JSON 내부 값으로 조회해야 하면 JSON path 조건을 사용합니다.

```sql
SELECT device_id
FROM device_config
WHERE config->'$.status' = 'active';
```

## 관련 주의사항

- JSON path 문자열은 작은따옴표(`'$.status'`)로 작성합니다.
- 큰따옴표(`"$.status"`)는 SQL 식별자로 해석되어 컬럼 이름 오류가 발생할 수 있습니다.
