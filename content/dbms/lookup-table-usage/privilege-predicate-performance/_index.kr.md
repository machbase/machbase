---
title: '9.15 LOOKUP 권한과 predicate DML 성능'
weight: 150
toc: true
---
LOOKUP 테이블의 권한 모델과 predicate DML 성능 특성을 다룬다.


<a id="privileges-lookup-update-delete-target-select"></a>

## LOOKUP UPDATE/DELETE 권한

LOOKUP 테이블의 `UPDATE`와 `DELETE`는 primary key 조건과 일반 predicate 조건을 모두
지원한다. 권한 검사는 사용자가 실행한 DML 종류를 기준으로 수행한다.

### 권한 기준

| 작업 | 필요한 권한 |
|------|-------------|
| SELECT | `SELECT` |
| UPDATE | `UPDATE` |
| DELETE | `DELETE` |

일반 predicate `UPDATE`/`DELETE` 실행 중 내부적으로 대상 row를 찾더라도 별도
`SELECT` 권한을 추가로 요구하지 않는다.

```sql
-- UPDATE 권한이 있으면 일반 predicate UPDATE 가능
UPDATE device_config
SET status = 'inactive'
WHERE region = 'ASIA';

-- DELETE 권한이 있으면 일반 predicate DELETE 가능
DELETE FROM device_config
WHERE last_seen < TO_DATE('2026-01-01 00:00:00');
```

### 권한 설정 예

```sql
GRANT UPDATE ON sys.device_config TO ops_user;
GRANT DELETE ON sys.device_config TO ops_user;
```

대상 범위를 사용자가 직접 확인하도록 하려면 `SELECT` 권한을 별도로 부여한다.

```sql
GRANT SELECT ON sys.device_config TO ops_user;
```

<a id="performance-considerations-lookup-predicate-dml"></a>

## LOOKUP 일반 predicate DML 성능 고려사항

Primary key 조건 `UPDATE`/`DELETE`는 PK 해시 경로를 사용한다. 일반
predicate `UPDATE`/`DELETE`는 조건에 맞는 대상 row를 찾은 뒤 변경을 적용하므로, 범위가
넓으면 PK 단건 처리보다 비용이 커질 수 있다.

### 권장 패턴

#### 1. 단건 변경은 PK 조건 사용

```sql
UPDATE device_meta
SET status = 'ACTIVE'
WHERE device_id = 'DEV-001';

DELETE FROM device_meta
WHERE device_id = 'DEV-001';
```

#### 2. 일괄 변경 전 대상 범위 확인

```sql
SELECT COUNT(*)
FROM device_meta
WHERE location = 'Building-A'
  AND status = 'INACTIVE';

UPDATE device_meta
SET status = 'RETIRED'
WHERE location = 'Building-A'
  AND status = 'INACTIVE';
```

#### 3. JSON 조건은 타입별 함수 사용

```sql
UPDATE device_meta
SET meta = JSON_SET(meta, '$.state', 'active')
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;
```

숫자 비교에는 `->`보다 `JSON_EXTRACT_INTEGER`, `JSON_EXTRACT_DOUBLE` 같은 타입별 함수를
사용한다.

### 성능 요약

| DML 유형 | 특성 | 권장 사용 |
|----------|------|-----------|
| PK 조건 UPDATE/DELETE | PK 해시 경로 | 단건 또는 명확한 PK 대상 |
| non-PK predicate UPDATE/DELETE | 조건에 맞는 row를 찾아 적용 | 소규모/중간 규모 일괄 변경, 사전 count 권장 |
| JSON path 조건 DML | JSON path 평가 비용 포함 | 자주 쓰는 조건은 별도 컬럼화 |

참조 데이터 용도에 맞게 작고 명확한 범위로 유지하는 것이 좋다.
