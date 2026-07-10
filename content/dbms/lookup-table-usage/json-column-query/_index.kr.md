---
title: '9.12 JSON 컬럼 제약과 JSON 조회'
weight: 120
toc: true
---
LOOKUP 테이블의 JSON 컬럼 제약과 JSON 조건 조회를 다룬다.


<a id="condition-query-lookup-json"></a>

## LOOKUP JSON 조건 조회

LOOKUP 테이블의 `JSON` 컬럼은 JSON path 조건 조회에 사용할 수 있다.

### 기본 조회

```sql
CREATE LOOKUP TABLE sensor_config (
    sensor_id VARCHAR(80) PRIMARY KEY,
    location  VARCHAR(200),
    config    JSON
);

INSERT INTO sensor_config VALUES (
    'TEMP-01',
    'factory1',
    '{"unit":"celsius","level":3,"threshold":{"high":90.0}}'
);

SELECT sensor_id, config
FROM sensor_config
WHERE config->'$.unit' = 'celsius';
```

### 타입별 추출 함수

숫자 값을 숫자로 비교할 때는 타입별 JSON 추출 함수를 사용한다.

```sql
SELECT sensor_id
FROM sensor_config
WHERE JSON_EXTRACT_INTEGER(config, '$.level') >= 3
  AND JSON_EXTRACT_DOUBLE(config, '$.threshold.high') > 80.0;
```

### JSON 상태 확인

```sql
SELECT sensor_id
FROM sensor_config
WHERE JSON_IS_VALID(config) = 1
  AND JSON_TYPEOF(config, '$.threshold') = 'Object';
```

### 주의사항

- JSON path 문자열은 작은따옴표(`'$.unit'`)로 작성한다. 큰따옴표는 SQL 식별자로 해석된다.
- `->` 연산자는 path 값을 문자열처럼 비교할 때 사용한다.
- JSON path별 전용 인덱스는 지원하지 않는다. 대량 LOOKUP 테이블에서 자주 검색하는 JSON 값은 별도 컬럼으로 분리한다.

<a id="design-column-lookup-json"></a>

## JSON 컬럼 제약

LOOKUP 테이블은 `JSON` 컬럼을 지원하지 않는다. 참조 데이터에 유연한 속성이 필요하면
자주 조회하는 값은 별도 컬럼으로 분리하고, 유동적인 속성은 문자열로 직렬화하거나 RDB/TAG
테이블의 JSON 컬럼을 검토한다.

### 설계 예

```sql
-- 실패: LOOKUP 테이블에는 JSON 컬럼을 만들 수 없음
CREATE LOOKUP TABLE sensor_config (
    sensor_id VARCHAR(64) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

```sql
-- 대안: 자주 조회하는 속성을 일반 컬럼으로 분리
CREATE LOOKUP TABLE sensor_config (
    sensor_id VARCHAR(64) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    unit      VARCHAR(16),
    level     INTEGER
);
```

### 조회와 갱신

```sql
SELECT sensor_id
FROM sensor_config
WHERE site = 'SEOUL'
  AND unit = 'Celsius'
  AND level >= 3;

UPDATE sensor_config
SET status = 'ACTIVE'
WHERE sensor_id = 'TEMP-01';
```

### 설계 기준

| 상황 | 권장 접근 |
|------|----------|
| 조인/검색에 자주 쓰는 값 | 별도 컬럼 |
| 장비별로 다른 유동 속성 | 문자열 직렬화 또는 RDB/TAG JSON 컬럼 검토 |
| 숫자 조건 검색 | 일반 숫자 컬럼으로 분리 |
| primary key | 안정적인 식별자 컬럼 사용 |
| 고빈도 path 검색 | 별도 컬럼으로 추출 |

### 주의사항

- LOOKUP/VOLATILE 테이블에는 JSON 컬럼을 생성할 수 없다.
- JSON path 조건이나 JSON path 인덱스가 필요하면 RDB/TAG 테이블을 검토한다.

<a id="definition-column-lookup-json"></a>

## LOOKUP JSON 컬럼 제약

LOOKUP 테이블은 `JSON` 컬럼을 지원하지 않는다. 유연한 속성이 필요한 참조 데이터는
자주 조회하는 값을 일반 컬럼으로 분리하고, 유동적인 속성은 문자열로 직렬화하거나 RDB/TAG
테이블의 JSON 컬럼을 검토한다.

### 컬럼 정의

```sql
-- 실패: LOOKUP 테이블에는 JSON 컬럼을 만들 수 없음
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

### 대안 스키마와 조회

```sql
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    region    VARCHAR(16),
    level     INTEGER,
    limits    VARCHAR(512)
);

SELECT device_id, limits
FROM device_config
WHERE region = 'kr'
  AND level >= 3;
```

### 값 갱신

```sql
UPDATE device_config
SET status = 'ACTIVE'
WHERE site = 'SEOUL';

UPDATE device_config
SET limits = '{"high":85.0,"low":5.0,"verified":1}'
WHERE device_id = 'DEV-01';
```

### 제약 사항

- LOOKUP/VOLATILE 테이블에는 JSON 컬럼을 생성할 수 없다.
- JSON path 조건이나 JSON path 인덱스가 필요하면 RDB/TAG 테이블을 검토한다.
- 자주 검색하는 값은 LOOKUP 일반 컬럼으로 분리한다.
