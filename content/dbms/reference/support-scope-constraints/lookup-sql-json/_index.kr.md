---
type: docs
title: '17.8.5 LOOKUP SQL/JSON 지원표'
weight: 50
toc: true
---

이 페이지는 LOOKUP 테이블의 SQL 기능과 JSON 관련 제약을 정리합니다.

## 지원 현황

| 기능 | 지원 | 비고 |
|------|:---:|------|
| **기본 CRUD** | | |
| INSERT | O | 일반 INSERT 사용 |
| SELECT | O | PK 조건과 일반 predicate 모두 사용 가능 |
| UPDATE (PK 조건) | O | Primary key fast path 사용 |
| DELETE (PK 조건) | O | Primary key fast path 사용 |
| UPDATE (일반 predicate) | O | 조건에 맞는 Primary key 집합을 수집한 뒤 갱신 |
| DELETE (일반 predicate) | O | 조건에 맞는 Primary key 집합을 수집한 뒤 삭제 |
| **JSON 기능** | | |
| JSON 타입 컬럼 | O | 일반 컬럼으로 생성, 저장, 조회, 갱신 가능 |
| JSON path query (`$.key`) | O | `->`, `JSON_EXTRACT_*`, `JSON_TYPEOF`, `JSON_IS_VALID` 사용 가능 |
| JSON PK | X | JSON 컬럼은 primary key로 선언할 수 없음 |
| JSON path index | X | 별도 JSON path index는 지원하지 않음 |
| **기타** | | |
| Transaction | △ | 개별 DML 중심으로 사용 |
| Prepared Statement | O | Primary key 및 일반 predicate의 bind 지원 |
| Append API | △ | 일반 SQL INSERT가 기본이며, Append는 별도 LOOKUP append 정책을 따름 |

## LOOKUP JSON 컬럼 예

```sql
CREATE LOOKUP TABLE device_lookup
(
    id          VARCHAR(32) PRIMARY KEY,
    site        VARCHAR(32),
    status      VARCHAR(16),
    score       INTEGER,
    updated_at  DATETIME,
    meta        JSON
);

INSERT INTO device_lookup VALUES
(
    'dev-001',
    'SEOUL',
    'READY',
    30,
    TO_DATE('2026-06-01 10:00:00'),
    '{"region":"kr","level":3,"tags":["edge","main"]}'
);
```

JSON path는 SELECT, UPDATE, DELETE 조건에 사용할 수 있습니다.

```sql
SELECT id, status
FROM device_lookup
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;

UPDATE device_lookup
SET meta = JSON_SET(meta, '$.status', 'active')
WHERE meta->'$.region' = 'kr'
  AND status = 'READY';
```

## UPDATE/DELETE 조건

LOOKUP 테이블의 UPDATE와 DELETE는 Primary key 조건뿐 아니라 non-PK, 범위, 문자열, 날짜,
논리 조합과 JSON path 조건을 지원합니다. WHERE 절을 생략한 DELETE는 모든 row를 삭제합니다.

```sql
UPDATE device_lookup
SET status = 'ACTIVE',
    score = score + 10,
    meta = JSON_SET(meta, '$.state', 'active')
WHERE site = 'SEOUL'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;

DELETE FROM device_lookup
WHERE status = 'EXPIRED'
   OR updated_at < TO_DATE('2026-01-01 00:00:00');

DELETE FROM device_lookup;
```

`SET` 절에서는 현재 row의 컬럼 값을 참조할 수 있습니다. 단, primary key 컬럼 자체는
`SET` 절에서 변경할 수 없습니다.

## 제약과 주의사항

| 항목 | 내용 |
|------|------|
| JSON primary key | `JSON` 컬럼은 primary key로 사용할 수 없음 |
| JSON path index | JSON path별 전용 인덱스는 지원하지 않음 |
| JSON path 문자열 | 작은따옴표(`'$.key'`)를 사용해야 하며 큰따옴표는 식별자로 해석됨 |
| 숫자 비교 | `->` 대신 `JSON_EXTRACT_INTEGER`, `JSON_EXTRACT_DOUBLE` 등 타입별 함수를 권장 |
| 일반 predicate DML | 조건에 맞는 모든 row에 적용되므로 실행 전에 같은 조건으로 대상 범위 확인 |
