---
title: '9.8 제약, 오류, 문제 해결'
weight: 80
toc: true
---
LOOKUP 테이블의 제약 사항, 발생 가능한 오류, 문제 해결 방법을 다룹니다.


<a id="too-many-lookup-predicate-update-delete-row"></a>

## LOOKUP 일반 조건식 UPDATE/DELETE 주의사항

LOOKUP 테이블은 non-PK, 범위, 문자열, 날짜, 논리 조합과 JSON path 조건으로 여러 행을
UPDATE하거나 DELETE할 수 있습니다. 일반 조건식은 조건에 맞는 모든 행에 적용되므로 변경 전에
동일한 조건으로 대상 범위를 확인합니다.

```sql
SELECT COUNT(*)
FROM equipment
WHERE location = 'A동'
  AND status = 'INACTIVE';

UPDATE equipment
SET status = 'RETIRED'
WHERE location = 'A동'
  AND status = 'INACTIVE';
```

Primary key 컬럼 자체는 `SET` 절에서 변경할 수 없습니다. 모든 행을 삭제하려면 WHERE 절을
생략할 수 있습니다.

<a id="error-lookup-json-path-primary-key"></a>

## LOOKUP JSON primary key 오류

LOOKUP 테이블은 `JSON` 타입을 일반 컬럼으로 지원하지만, `JSON` 컬럼을 primary key로
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

Primary key는 row를 안정적으로 식별해야 합니다. JSON 컬럼은 저장·조회·조건 검색·갱신에는
쓸 수 있지만 primary key 타입으로는 허용되지 않습니다.

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
| 규모 판단 | 메모리, 인덱스와 갱신 부하를 실제 워크로드로 검증 |
| BASETIME / BASEDISTANCE | 미지원 |

### 규모 판단

LOOKUP 테이블은 기준 정보의 반복 조회와 갱신에 적합합니다. 행 수만으로 한계를 정하지 말고
Primary key와 보조 인덱스의 메모리 사용량, 입력·갱신 빈도와 조회 조건을 실제 데이터로
측정합니다. 명시적 트랜잭션이나 관계형 DML이 필요하면 RDB 테이블을 선택합니다.

### Append API

```bash
# LOOKUP 테이블에는 INSERT 문 또는 SDK Append API 사용
```

### 주의사항

- LOOKUP 테이블에 시계열 데이터를 저장하지 않습니다. 계측값은 TAG 테이블을 사용합니다.
- PRIMARY KEY 중복 삽입 시 오류가 발생합니다.
- 테이블 전체를 교체해야 하면 조건 없는 DELETE 후 INSERT 패턴을 사용합니다. LOOKUP 테이블은
  TRUNCATE를 지원하지 않습니다.

---

**다음 읽을 내용**
- [VOLATILE 테이블 설계](/dbms/volatile-table-usage/)
