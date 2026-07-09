---
type: docs
title: 'JSON 컬럼 제약'
weight: 40
---

LOOKUP 테이블은 `JSON` 컬럼을 지원하지 않습니다. 참조 데이터에 유연한 속성이 필요하면
자주 조회하는 값은 별도 컬럼으로 분리하고, 유동적인 속성은 문자열로 직렬화하거나 RDB/TAG
테이블의 JSON 컬럼 사용을 검토합니다.

## 설계 예

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

## 조회와 갱신

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

## 설계 기준

| 상황 | 권장 접근 |
|------|----------|
| 조인/검색에 자주 쓰는 값 | 별도 컬럼 |
| 장비별로 다른 유동 속성 | 문자열 직렬화 또는 RDB/TAG JSON 컬럼 검토 |
| 숫자 조건 검색 | 일반 숫자 컬럼으로 분리 |
| primary key | 안정적인 식별자 컬럼 사용 |
| 고빈도 path 검색 | 별도 컬럼으로 추출 |

## 주의사항

- LOOKUP/VOLATILE 테이블에는 JSON 컬럼을 생성할 수 없습니다.
- JSON path 조건이나 JSON path 인덱스가 필요하면 RDB/TAG 테이블 사용을 검토합니다.
