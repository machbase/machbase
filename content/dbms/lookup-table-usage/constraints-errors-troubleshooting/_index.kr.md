---
title: '9.8 제약, 오류, 문제 해결'
weight: 80
toc: true
---
제약, 오류, 문제 해결에 해당하는 세부 문서를 모았습니다.


<a id="too-many-lookup-predicate-update-delete-row"></a>

## LOOKUP 일반 predicate UPDATE/DELETE 범위가 클 때

LOOKUP 테이블의 일반 predicate `UPDATE`/`DELETE`는 지원됩니다. 다만 조건에 맞는 모든
row에 적용되므로, 의도보다 많은 row가 변경되거나 삭제되지 않도록 대상 범위를 확인해야 합니다.

### 증상

- UPDATE/DELETE가 성공했지만 예상보다 많은 row가 변경됨
- JSON path 또는 범위 조건이 넓어 다수 row가 대상이 됨

### 진단

실행 전 같은 조건으로 대상 row 수를 확인합니다.

```sql
SELECT COUNT(*)
FROM equipment
WHERE location = 'A동'
  AND status = 'inactive';
```

필요하면 대상 key를 함께 확인합니다.

```sql
SELECT eq_id, location, status
FROM equipment
WHERE location = 'A동'
  AND status = 'inactive';
```

### 해결 방법

- 단건 변경은 primary key 조건을 사용합니다.
- 일괄 변경은 조건을 더 좁히고, 변경 전후 count를 확인합니다.
- JSON 숫자 조건은 타입별 함수를 사용합니다.

```sql
UPDATE equipment
SET status = 'retired'
WHERE location = 'A동'
  AND status = 'inactive'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') < 2;
```

<a id="error-lookup-json-path-primary-key"></a>

## LOOKUP JSON primary key 오류

LOOKUP 테이블은 `JSON` 타입 컬럼을 일반 컬럼으로 지원하지만, `JSON` 컬럼을 primary key로
선언할 수는 없습니다.

### 증상

```sql
CREATE LOOKUP TABLE device_config (
    config JSON PRIMARY KEY,
    note   VARCHAR(32)
);
```

위와 같이 실행하면 JSON 컬럼을 primary key로 사용할 수 없다는 오류가 발생합니다.

### 원인

Primary key는 row를 안정적으로 식별해야 합니다. LOOKUP 테이블의 JSON 컬럼은 저장, 조회,
조건 검색, 갱신에는 사용할 수 있지만 primary key 타입으로는 허용되지 않습니다.

### 해결 방법

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

### 관련 주의사항

- JSON path 문자열은 작은따옴표(`'$.status'`)로 작성합니다.
- 큰따옴표(`"$.status"`)는 SQL 식별자로 해석되어 컬럼 이름 오류가 발생할 수 있습니다.

<a id="limitations-lookup"></a>

## 제약 및 주의사항

### 제약 사항

| 항목 | 상태 |
|------|------|
| PRIMARY KEY | 필수 |
| Append API | 지원 |
| 대용량 (수천만 건 이상) | 미권장 |
| BASETIME / BASEDISTANCE | 미지원 |

### 규모 제한

LOOKUP 테이블은 소규모 참조 데이터에 최적화되어 있습니다. 건수가 수백만 건을 넘는 경우 성능이 저하될 수 있으며, 이 경우 RDB 테이블을 고려합니다.

| 규모 | 권장 타입 |
|------|---------|
| 수십만 건 이하 | LOOKUP |
| 수백만~수천만 건 | 경계 — 성능 테스트 필요 |
| 수천만 건 이상 | RDB 테이블 |

### Append API

```bash
# LOOKUP 테이블에는 INSERT 문 또는 SDK Append API 사용
```

### 주의사항

- LOOKUP 테이블에 시계열 데이터를 저장하지 않습니다. 계측값은 TAG 테이블을 사용합니다.
- PRIMARY KEY 중복 삽입 시 오류가 발생합니다.
- 테이블 전체를 교체해야 하는 경우, DELETE 후 INSERT 또는 TRUNCATE + INSERT 패턴을 사용합니다.

---

**다음 읽을 내용**
- [VOLATILE 테이블 설계](/dbms/volatile-table-usage/)
