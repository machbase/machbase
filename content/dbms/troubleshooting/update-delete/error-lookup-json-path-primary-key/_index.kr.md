---
type: docs
title: 'LOOKUP JSON path 또는 JSON primary key 오류 (planned: dbms-nfx#3696)'
weight: 40
---

LOOKUP 테이블에서 JSON 타입 컬럼을 사용할 때, JSON 경로(JSON path) 조건 또는 JSON 컬럼을 PRIMARY KEY로 사용하려 하면 오류가 발생할 수 있습니다.

{{< callout type="warning" >}}
**현재 제약사항 (planned: dbms-nfx#3696)**

LOOKUP 테이블에서 JSON 경로 기반 PRIMARY KEY 지정 및 JSON path 조건 필터링은 현재 개발 중입니다. 이 기능은 향후 지원 예정입니다.
{{< /callout >}}

## 증상

다음과 같은 상황에서 오류가 발생합니다.

```
[ERR-02XXX]: JSON path expression is not supported as PRIMARY KEY
[ERR-02XXX]: JSON path condition is not supported in LOOKUP table filter
```

## 원인과 제약 유형

### 1. JSON 컬럼을 PRIMARY KEY로 지정

JSON 타입 컬럼 또는 JSON 경로 표현식을 LOOKUP 테이블의 PRIMARY KEY로 지정하는 기능은 현재 지원되지 않습니다.

```sql
-- 오류: JSON 경로를 PK로 사용 (미지원)
CREATE TABLE device_config (
    config JSON,
    PRIMARY KEY (config->'$.device_id')  -- JSON path PK 미지원
);
```

### 2. JSON 경로 조건으로 LOOKUP 필터링

JSON 컬럼에서 JSON path 표현식을 WHERE 절 조건으로 사용한 UPDATE/DELETE가 정확하게 동작하지 않을 수 있습니다.

```sql
-- 오류 또는 예상치 못한 동작: JSON path 조건 필터링
DELETE FROM device_config WHERE config->'$.status' = 'inactive';

-- 오류: JSON 중첩 키로 UPDATE
UPDATE device_config SET config->'$.version' = '2.0'
WHERE config->'$.device_id' = 'DEV-001';
```

## 임시 해결 방법

### 방법 1: 별도 식별자 컬럼 사용

JSON 데이터에서 식별자가 될 값을 별도의 VARCHAR 컬럼으로 분리하고, 해당 컬럼을 PRIMARY KEY로 사용합니다.

```sql
-- 권장: 식별자를 별도 컬럼으로 분리
CREATE TABLE device_config (
    device_id VARCHAR(64) PRIMARY KEY,  -- 식별자를 별도 컬럼으로
    config    VARCHAR(4096)              -- JSON을 문자열로 저장
);

-- INSERT
INSERT INTO device_config VALUES ('DEV-001', '{"status":"active","version":"1.0"}');

-- UPDATE (PK 기반, 정상 동작)
UPDATE device_config
SET config = '{"status":"inactive","version":"1.0"}'
WHERE device_id = 'DEV-001';
```

### 방법 2: 애플리케이션에서 JSON 파싱

JSON 조건 필터링이 필요한 경우 데이터베이스에서 전체 데이터를 조회한 후, 애플리케이션 레이어에서 JSON을 파싱하여 대상을 식별합니다.

```sql
-- 전체 또는 일부 데이터 조회
SELECT device_id, config FROM device_config;
```

애플리케이션에서 JSON을 파싱하여 조건에 맞는 `device_id`를 추출한 후, PK 기반으로 UPDATE/DELETE를 실행합니다.

```sql
-- 애플리케이션에서 식별한 PK로 처리
UPDATE device_config SET config = '...' WHERE device_id = 'DEV-001';
```

## 현재 지원되는 JSON 사용 방법

LOOKUP 테이블에서 JSON 컬럼은 다음과 같이 사용할 수 있습니다.

```sql
-- JSON 컬럼 생성 (지원)
CREATE TABLE device_config (
    device_id VARCHAR(64) PRIMARY KEY,
    config    JSON
);

-- JSON 데이터 삽입 (지원)
INSERT INTO device_config VALUES ('DEV-001', '{"status":"active"}');

-- PK 기반 SELECT (지원)
SELECT config FROM device_config WHERE device_id = 'DEV-001';

-- PK 기반 UPDATE (config 전체 교체, 지원)
UPDATE device_config
SET config = '{"status":"inactive"}'
WHERE device_id = 'DEV-001';
```

## 향후 지원 예정

JSON 경로 기반 PRIMARY KEY 및 JSON path 조건 필터링은 `planned: dbms-nfx#3696`으로 계획 중입니다. 최신 릴리스 노트를 확인하십시오.
