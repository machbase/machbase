---
type: docs
title: '5.10.4 TAG 테이블 메타데이터 조회'
weight: 60
---

TAG 테이블은 시계열 데이터를 저장하는 태그 테이블 본체와 별도로 **메타데이터 테이블**을 가집니다. 메타데이터 테이블은 내부적으로 `_tablename_META`라는 이름의 LOOKUP 테이블로 관리되며, 각 태그(센서)에 대한 부가 정보를 저장합니다.

## 메타데이터 테이블 구조

TAG 테이블 생성 시 `METADATA` 절로 메타데이터 컬럼을 정의합니다.

```sql
CREATE TAG TABLE tag (
    name     VARCHAR(80) PRIMARY KEY,
    time     DATETIME BASETIME,
    value    DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(200),
    factory  VARCHAR(100),
    unit     VARCHAR(20)
);
```

위 예시에서 메타데이터 테이블은 `tag_meta`(`_TAG_META`)로 자동 생성됩니다.

## 메타데이터 조회

```sql
-- 전체 태그 메타데이터 조회
SELECT * FROM tag_meta;

-- 특정 조건으로 필터링
SELECT name, location, factory
FROM tag_meta
WHERE factory = 'factory1';

-- 전체 태그 이름 목록 조회
SELECT name FROM tag_meta;
```

## 메타데이터 삽입 및 관리

### 태그 데이터와 함께 메타데이터 등록

```sql
-- METADATA 키워드로 태그 삽입 시 메타데이터 동시 등록
INSERT INTO tag METADATA VALUES ('sensor1', 'factory1', 'building-A', 'celsius');
INSERT INTO tag METADATA VALUES ('sensor2', 'factory2', 'building-B', 'kPa');
```

### 메타데이터만 별도 수정

```sql
-- 기존 태그의 메타데이터 업데이트
UPDATE tag_meta SET location = 'building-C' WHERE name = 'sensor1';

-- 메타데이터 직접 삽입
INSERT INTO tag_meta (name, location, factory, unit)
VALUES ('sensor3', 'factory1', 'building-A', 'celsius');
```

## 메타데이터 컬럼 추가

운영 중에 메타데이터 컬럼을 추가할 수 있습니다.

```sql
ALTER TABLE tag METADATA ADD COLUMN (install_date DATETIME);
ALTER TABLE tag METADATA ADD COLUMN (manufacturer VARCHAR(100));
```

> 메타데이터 컬럼 추가는 즉시 반영되며, 기존 행의 신규 컬럼 값은 NULL로 설정됩니다.

## TAG 데이터와 메타데이터 JOIN

```sql
-- 시계열 데이터에 메타데이터를 결합하여 조회
SELECT
    t.time,
    t.name,
    t.value,
    m.location,
    m.factory
FROM tag t, tag_meta m
WHERE t.name = m.name
  AND t.time >= NOW - 3600000000000
ORDER BY t.time DESC;
```

## 메타데이터 조건으로 TAG 데이터 필터링

```sql
-- 특정 공장의 센서 데이터만 조회
SELECT t.time, t.name, t.value
FROM tag t
WHERE t.name IN (
    SELECT name FROM tag_meta WHERE factory = 'factory1'
)
AND t.time >= NOW - 86400000000000;

-- 특정 위치의 센서 평균값 집계
SELECT m.location, AVG(t.value) AS avg_value
FROM tag t, tag_meta m
WHERE t.name = m.name
  AND t.time >= NOW - 3600000000000
GROUP BY m.location;
```

## 태그 수 및 통계 조회

```sql
-- 전체 태그(센서) 수
SELECT COUNT(*) FROM tag_meta;

-- 공장별 센서 수
SELECT factory, COUNT(*) AS sensor_count
FROM tag_meta
GROUP BY factory;

-- 특정 조건에 해당하는 태그 이름 목록
SELECT name FROM tag_meta
WHERE location LIKE 'building-A%'
ORDER BY name;
```

## 메타데이터 테이블 직접 접근

메타데이터 테이블은 일반 LOOKUP 테이블처럼 직접 접근할 수 있습니다.

```sql
-- _META 접미사 이름으로 직접 조회 (내부 이름)
SELECT * FROM _TAG_META;

-- 또는 별칭 이름으로 조회
SELECT * FROM tag_meta;
```

> `tag_meta`와 `_TAG_META`는 동일한 테이블을 가리킵니다. 가독성을 위해 `tag_meta` 형식을 사용하는 것을 권장합니다.
