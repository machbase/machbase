---
type: docs
title: 'LOOKUP JSON 컬럼 생성 오류'
weight: 40
---

LOOKUP 테이블에 JSON 타입 컬럼을 생성하려 하면 오류가 발생합니다.

{{< callout type="warning" >}}
**현재 제약사항**

현재 Machbase 8.6 빌드에서 LOOKUP 테이블은 JSON 타입 컬럼을 지원하지 않습니다.
JSON 데이터는 문자열 컬럼에 저장하거나, JSON 타입을 지원하는 테이블 유형을 사용합니다.
{{< /callout >}}

## 증상

다음과 같은 상황에서 오류가 발생합니다.

```
[ERR-02173: Cannot create columns with data type (JSON) in VOLATILE / LOOKUP table.]
```

## 원인과 제약 유형

### 1. LOOKUP 테이블에 JSON 컬럼 생성

LOOKUP 테이블에서는 JSON 타입 컬럼을 만들 수 없습니다.

```sql
-- 오류: LOOKUP 테이블 JSON 컬럼 미지원
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(64) PRIMARY KEY,
    config    JSON
);
```

### 2. JSON 경로 조건 또는 JSON primary key

LOOKUP 테이블에 JSON 컬럼을 만들 수 없으므로, JSON 경로를 primary key나
UPDATE/DELETE 조건으로 사용하는 방식도 사용할 수 없습니다.

```sql
-- LOOKUP JSON 컬럼 생성이 먼저 실패하므로 사용할 수 없는 패턴
DELETE FROM device_config WHERE config->'$.status' = 'inactive';
```

## 임시 해결 방법

### 방법 1: 별도 식별자 컬럼 사용

JSON 데이터에서 식별자가 될 값을 별도의 VARCHAR 컬럼으로 분리하고, 해당 컬럼을 PRIMARY KEY로 사용합니다.

```sql
-- 권장: 식별자를 별도 컬럼으로 분리
CREATE LOOKUP TABLE device_config (
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

## JSON 타입이 필요한 경우

JSON 타입 컬럼과 JSON path 조건을 데이터베이스에서 직접 사용해야 한다면 LOOKUP 테이블이
아닌 지원 가능한 테이블 유형을 사용합니다. 예를 들어 TAG 테이블은 JSON 컬럼과 JSON path
인덱스를 지원합니다.

```sql
CREATE TAG TABLE sensor_config (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME BASETIME,
    value  DOUBLE SUMMARIZED,
    config JSON
);
```
