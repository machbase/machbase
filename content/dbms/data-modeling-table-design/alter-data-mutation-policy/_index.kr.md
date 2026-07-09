---
type: docs
title: '4.3 데이터 변경 정책'
weight: 20
---
Machbase는 테이블 타입에 따라 UPDATE, DELETE, TRUNCATE 지원 범위가 명확하게 구분됩니다. 시계열 특성상 대부분의 테이블은 삽입 후 변경을 제한하며, 일부 테이블만 수정·삭제를 허용합니다.

## 테이블 타입별 데이터 변경 지원 범위

| 테이블 타입 | UPDATE | DELETE | TRUNCATE |
|------------|--------|--------|---------|
| TAG | O (태그/축 조건) | O (BEFORE 또는 tag/axis 조건) | X |
| LOG | X | O (BEFORE/OLDEST/EXCEPT/전체 삭제) | O |
| RDB | O (WHERE 유무 모두) | O | O |
| VOLATILE | O (by PK) | O | X |
| LOOKUP | O (by PK/일반 조건) | O (by PK/일반 조건) | X |

> TRUNCATE는 LOG와 RDB 테이블에서만 지원됩니다. TAG, VOLATILE, LOOKUP 테이블에 TRUNCATE를 실행하면 오류가 발생합니다.

## 변경이 제한되는 이유

LOG 테이블은 시계열 데이터의 **불변성(immutability)** 원칙을 따릅니다. 수집된 이벤트 로그는 원칙적으로 사후에 수정하지 않으며, 이를 통해 저장 구조 최적화와 높은 삽입 처리량을 달성합니다. TAG 테이블은 태그/축 조건으로 대상 범위를 명확히 지정한 경우에만 실제 데이터 UPDATE를 허용합니다. 수정이 빈번한 상태 정보·설정 값은 VOLATILE 또는 LOOKUP 테이블에 저장하는 것이 권장됩니다.

## 각 정책 상세

- [UPDATE 정책](/dbms/data-modeling-table-design/alter-data-mutation-policy/#policy-update): 테이블 타입별 UPDATE 허용 조건과 구문
- [DELETE 정책](/dbms/data-modeling-table-design/alter-data-mutation-policy/#policy-delete): 테이블 타입별 DELETE 허용 조건
- [TRUNCATE 정책](/dbms/data-modeling-table-design/alter-data-mutation-policy/#policy-truncate): TRUNCATE 지원 테이블과 동작 차이
- [TAG/KV DELETE 조건](/dbms/data-modeling-table-design/alter-data-mutation-policy/#condition-tag-kv-delete-before): BEFORE 조건 필수 규칙


<a id="policy-update"></a>

## UPDATE 정책

테이블 타입별 UPDATE 지원 범위와 구문을 정리합니다.

### 테이블 타입별 UPDATE 지원

| 테이블 타입 | UPDATE 지원 | 조건 |
|------------|------------|------|
| TAG | O | 태그 선택 조건과 BASETIME 조건이 필요. 메타데이터는 `UPDATE ... METADATA` 사용 |
| LOG | X | 미지원 |
| RDB | O | WHERE 유무 모두 가능 |
| VOLATILE | O | Primary key equality 조건. ON DUPLICATE KEY UPDATE도 지원 |
| LOOKUP | O | Primary key equality 조건과 일반 predicate 조건 지원 |

### RDB 테이블 UPDATE

RDB 테이블은 일반 관계형 DB와 동일한 UPDATE 구문을 지원합니다.

```sql
UPDATE orders SET status = 'SHIPPED', updated_at = NOW
WHERE order_id = 1001;

UPDATE inventory SET qty = qty - 5 WHERE item_id = 42;

UPDATE product_catalog SET discount = 0;
```

### VOLATILE 테이블 UPDATE

VOLATILE 테이블은 일반 UPDATE와 ON DUPLICATE KEY UPDATE(UPSERT)를 모두 지원합니다.

```sql
UPDATE device_status SET status = 'ALARM', value = 95.3
WHERE device_id = 'DEV-01';

INSERT INTO device_status VALUES ('DEV-01', 'ALARM', 95.3, NOW)
ON DUPLICATE KEY UPDATE SET status = 'ALARM', value = 95.3, updated_at = NOW;
```

### LOOKUP 테이블 UPDATE

LOOKUP 테이블은 PRIMARY KEY equality 조건과 일반 predicate 조건의 UPDATE를 모두 지원합니다.
조건에 맞는 모든 row가 갱신됩니다.

```sql
UPDATE alarm_threshold SET high_limit = 90.0, updated_at = NOW
WHERE sensor_id = 'TEMP-01';

UPDATE alarm_threshold
SET high_limit = high_limit + 5.0
WHERE device_type = 'MOTOR'
  AND active = 1;
```

> 일반 조건식 UPDATE는 여러 row에 적용될 수 있으므로 실행 전에 같은 조건으로 대상 범위를 확인합니다.

### TAG/LOG 테이블 UPDATE

TAG 데이터(실제 시계열 값)와 TAG 메타데이터 UPDATE는 구분해야 합니다.

- **TAG data UPDATE**: `UPDATE tag_table SET data_col = ... WHERE name ... AND time ...`
  구문으로 가능
- **TAG 메타데이터 UPDATE**: `UPDATE tag_table METADATA SET ...` 구문으로 가능
- **LOG 테이블 UPDATE**: 미지원

TAG data UPDATE는 태그 선택 조건과 BASETIME 조건이 모두 필요하며, `name`과 `time` 컬럼은
SET 대상으로 사용할 수 없습니다. 상세 내용은 하위 페이지를 참고하세요.

<a id="policy-update-policy-tag-data-update"></a>

### TAG data UPDATE 정책

TAG 테이블의 실제 시계열 데이터는 제한된 조건에서 UPDATE할 수 있습니다. UPDATE 대상은
명확한 태그 범위와 시간 범위로 한정해야 하며, 메타데이터 수정과는 구문을 구분합니다.

#### 기본 정책

TAG data UPDATE는 다음 원칙을 따릅니다.

1. WHERE 절에 태그 선택 조건(`name =`, `name IN`, `name LIKE`)이 있어야 합니다.
2. WHERE 절에 BASETIME 컬럼 조건이 있어야 합니다.
3. SET 대상은 실제 데이터 컬럼이어야 합니다.
4. `name`(PRIMARY KEY), `time`(BASETIME), 메타데이터 컬럼은 data UPDATE로 수정할 수 없습니다.

```sql
UPDATE tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2024-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

#### 메타데이터와의 구분

TAG 메타데이터 컬럼은 `UPDATE ... METADATA` 구문으로 수정합니다.

```sql
UPDATE tag METADATA
   SET location = 'zone-2'
 WHERE name = 'TEMP-01';
```

메타데이터 변경은 태그 속성을 수정하는 작업이며, 이미 적재된 시계열 row의 `value`나
보조 데이터 컬럼을 변경하지 않습니다.

#### 지원되는 조건

```sql
UPDATE tag
   SET value = value * 0.98
 WHERE name IN ('TEMP-01', 'TEMP-02')
   AND time BETWEEN TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-15 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND value > 0;
```

`OR`, 태그 선택 없는 조건, 시간 조건 없는 조건, 서브쿼리 기반 조건은 허용하지 않습니다.

#### 운영 고려사항

- 대량 UPDATE 전 같은 WHERE 조건으로 대상 row 수를 확인합니다.
- UPDATE 직후 원본 row는 변경되지만, 이미 만들어진 롤업은 즉시 갱신되지 않을 수 있습니다.
  필요한 롤업은 `ROLLUP_REBUILD`로 재구성합니다.
- 수집 직후 데이터를 수정해야 한다면 먼저 SELECT로 대상 row가 조회되는지 확인합니다.

<a id="policy-update-distinction-tag-data-update-metadata"></a>

### TAG data UPDATE와 UPDATE ... METADATA 구분

TAG 테이블에는 **실제 시계열 데이터**(time, value 등)와 **메타데이터**(METADATA 블록의
컬럼)가 있습니다. 두 영역 모두 수정할 수 있지만 구문과 제약이 다릅니다.

#### TAG 테이블 구조 복습

```sql
CREATE TAG TABLE tag (
    name     VARCHAR(20) PRIMARY KEY,
    time     DATETIME BASETIME,
    value    DOUBLE SUMMARIZED,
    status   INTEGER
) METADATA (
    location VARCHAR(40),
    dept     VARCHAR(20)
);
```

#### 실제 시계열 데이터 UPDATE

데이터 컬럼은 일반 `UPDATE` 문으로 수정합니다. WHERE 절에는 태그 선택 조건과 BASETIME
조건이 모두 필요합니다.

```sql
UPDATE tag
   SET value = 25.0,
       status = 1
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

`name`, `time`, 메타데이터 컬럼은 이 구문의 SET 대상이 아닙니다.

#### 메타데이터 UPDATE

TAG 메타데이터는 태그 속성 영역이며 `UPDATE ... METADATA` 구문으로 수정합니다.

```sql
UPDATE tag METADATA SET location = 'zone-2'
WHERE name = 'TEMP-01';

UPDATE tag METADATA SET dept = 'R&D', location = 'building-B'
WHERE name = 'TEMP-01';
```

메타데이터 변경은 해당 tag name의 속성을 바꾸는 작업이며, 개별 시계열 row의 `value`나
보조 데이터 컬럼 값을 변경하지 않습니다.

#### 구분 정리

| 대상 | UPDATE 구문 | 지원 여부 |
|------|------------|:--------:|
| 데이터 컬럼 (`value`, `status` 등) | `UPDATE tag SET ... WHERE name ... AND time ...` | O |
| 메타데이터 컬럼 (`location`, `dept` 등) | `UPDATE tag METADATA SET ...` | O |
| 태그 이름(PK) | 변경 불가 | X |
| 시간 축(BASETIME) | 변경 불가 | X |

#### 주의 사항

- 데이터 UPDATE는 대상 row 범위를 좁히기 위해 태그 조건과 시간 조건을 모두 요구합니다.
- 메타데이터 UPDATE는 태그 속성 변경이며, 시계열 값 정정 용도로 사용하지 않습니다.
- 롤업이 있는 테이블의 데이터 값을 정정한 뒤에는 필요한 롤업을 재구성합니다.

<a id="policy-update-tag-data-update-where-set-standard-only"></a>

### TAG data UPDATE WHERE/SET 지원 범위

TAG data UPDATE는 지원되지만, WHERE/SET 절에는 안전한 대상 범위를 보장하기 위한 제약이
있습니다.

#### 실행 가능한 구문

```sql
UPDATE tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE tag
   SET value = value * 0.98
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-15 11:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

#### 허용되는 WHERE/SET

- 태그 선택: `name =`, `name IN (...)`, `name LIKE ...`
- 시간 조건: `time =`, `BETWEEN`, 양쪽 범위, 한쪽 범위
- 추가 필터: 데이터 컬럼 predicate
- SET 대상: 실제 데이터 컬럼과 `SUMMARIZED` 데이터 컬럼

#### 허용되지 않는 범위

- WHERE 없는 UPDATE
- 태그 선택 조건 없는 UPDATE
- 시간 조건 없는 UPDATE
- `OR`, 서브쿼리, 집계식 기반 조건
- `name`, `time`, 메타데이터 컬럼 SET

#### 메타데이터 UPDATE

TAG 메타데이터는 별도 구문을 사용합니다.

```sql
UPDATE tag METADATA SET location = 'zone-2'
WHERE name = 'TEMP-01';
```

<a id="policy-delete"></a>

## DELETE 정책

테이블 타입별 DELETE 지원 범위와 조건을 정리합니다.

### 테이블 타입별 DELETE 지원

| 테이블 타입 | DELETE 지원 | 조건 |
|------------|------------|------|
| TAG | O | BEFORE 또는 tag/axis 조건 |
| LOG | O | BEFORE/OLDEST/EXCEPT 또는 전체 삭제 |
| RDB | O | 일반 WHERE 조건 자유 |
| VOLATILE | O | Primary key equality 조건 |
| LOOKUP | O | Primary key equality 조건과 일반 predicate 조건 지원 |

### RDB 테이블 DELETE

일반 관계형 DB와 동일하게 동작합니다.

```sql
-- WHERE 조건으로 삭제
DELETE FROM orders WHERE order_id = 1001;

-- 상태 기반 삭제
DELETE FROM orders WHERE status = 'CANCELLED';

-- 전체 삭제 (주의: RDB는 TRUNCATE로 대체 권장)
DELETE FROM temp_data;
```

### VOLATILE 테이블 DELETE

DELETE WHERE는 기본 키(PK)가 지정된 VOLATILE 테이블에서만 허용됩니다.

- WHERE 절에는 (기본 키 컬럼) = (값) 조건만 허용됩니다.
- 기본 키가 아닌 컬럼을 WHERE 조건으로 사용할 수 없습니다.

```sql
-- 조건 삭제
DELETE FROM device_status WHERE device_id = 'DEV-01';

-- 오래된 데이터처럼 PK가 아닌 조건으로 삭제해야 하면 먼저 PK 목록을 조회한 뒤 PK별로 삭제
SELECT device_id FROM device_status WHERE updated_at < NOW - 86400000000000;
DELETE FROM device_status WHERE device_id = 'DEV-01';
```

### LOOKUP 테이블 DELETE

LOOKUP 테이블은 PRIMARY KEY equality 조건과 일반 predicate 조건의 DELETE를 모두 지원합니다.
조건에 맞는 모든 row가 삭제됩니다.

```sql
-- PK 기준 삭제 (권장)
DELETE FROM alarm_threshold WHERE sensor_id = 'TEMP-01';

-- 일반 조건식 DELETE
DELETE FROM alarm_threshold
WHERE active = 0
   OR updated_at < TO_DATE('2026-01-01 00:00:00');
```

> 일반 조건식 DELETE는 여러 row에 적용될 수 있으므로 실행 전에 같은 조건으로 대상 범위를 확인합니다.

### LOG 테이블 DELETE

LOG 테이블은 다양한 DELETE 구문을 지원합니다.

```sql
DELETE FROM sensor_log OLDEST 1000 ROWS;   -- 가장 오래된 1000건 삭제
DELETE FROM sensor_log EXCEPT 1000 ROWS;   -- 최근 1000건을 제외하고 전체 삭제
DELETE FROM sensor_log EXCEPT 7 DAY;       -- 최근 7일 데이터를 제외하고 전체 삭제
DELETE FROM sensor_log;                    -- 전체 삭제
DELETE FROM sensor_log BEFORE '2024-01-01 00:00:00 000:000:000';  -- 특정 시점 이전 삭제
```

> DURATION, OLDEST, EXCEPT 구문은 TAG 및 Rollup 테이블에서는 사용할 수 없습니다.

### TAG 테이블 DELETE

TAG 테이블은 `BEFORE` 삭제와 `WHERE` 삭제를 모두 지원합니다. `BEFORE`는 특정 시점 이전 데이터를 일괄 삭제하고, `WHERE`는 태그 이름, 태그 이름과 축 조건, 또는 축 조건으로 삭제합니다.

```sql
-- TAG: 30일 이전 데이터 삭제
DELETE FROM tag BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- LOG: 특정 시각 이전 데이터 삭제
DELETE FROM sensor_log BEFORE '2024-01-01 00:00:00 000:000:000';
```

> `BEFORE` 시각은 현재 시각보다 과거여야 합니다. 미래 시각을 지정하면 오류가 발생합니다. 상세 내용은 [TAG/KV DELETE 허용 조건](/dbms/data-modeling-table-design/alter-data-mutation-policy/#condition-tag-kv-delete-before) 페이지를 참고하세요.

#### TAG 테이블 DELETE WHERE (조건부 삭제)

Tag 테이블은 tag name, tag name과 시간 조건, 또는 시간 조건만으로 DELETE WHERE를 지원합니다.
시간 조건에는 `=`, `<`, `<=`, `BETWEEN`을 사용할 수 있습니다.

```sql
-- tag name 기준 삭제
DELETE FROM tag WHERE tag_name = 'my_tag_2021';

-- tag name + 시간 기준 삭제
DELETE FROM tag WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');
DELETE FROM tag WHERE tag_name = 'my_tag_2021' AND tag_time BETWEEN TO_DATE('2021-07-01', 'YYYY-MM-DD') AND TO_DATE('2021-07-02', 'YYYY-MM-DD');

-- 시간 조건만으로 삭제
DELETE FROM tag WHERE tag_time <= TO_DATE('2021-07-01', 'YYYY-MM-DD');
```

> 삭제 후 물리적 공간 해제까지 시간이 걸릴 수 있습니다.

#### TAG ROLLUP DELETE WHERE

```sql
-- rollup을 tag name 기준으로 삭제
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021';

-- rollup을 tag name + 시간 기준으로 삭제
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');

-- 시간 조건만으로 rollup 삭제
DELETE FROM tag ROLLUP WHERE tag_time BETWEEN TO_DATE('2021-07-01', 'YYYY-MM-DD') AND TO_DATE('2021-07-02', 'YYYY-MM-DD');
```

### 하위 페이지

- [LOOKUP 일반 조건식 DELETE](/dbms/data-modeling-table-design/alter-data-mutation-policy/#condition-lookup-delete): 일반 predicate DELETE 지원 범위와 주의사항
- [TAG 메타데이터 삭제](/dbms/data-modeling-table-design/alter-data-mutation-policy/#delete-tag-metadata): TAG 테이블 메타데이터 삭제 구문

<a id="policy-delete-delete-tag-metadata"></a>

### TAG 메타데이터 삭제

TAG 테이블의 메타데이터(sensor 이름/속성 정보)를 삭제하는 구문입니다.

#### 문법

```sql
DELETE FROM table_name METADATA [WHERE condition];
```

WHERE 절을 생략하면 해당 TAG 테이블의 모든 메타데이터 행을 삭제합니다.

#### 예시

```sql
-- 전체 메타데이터 삭제
DELETE FROM tag METADATA;

-- 특정 태그 메타데이터 삭제
DELETE FROM tag METADATA WHERE name = 'tag-1';

-- 메타데이터 컬럼 조건으로 삭제
DELETE FROM tag METADATA WHERE status = 'STOP';
```

#### 주의사항

- WHERE name = '...' 뿐 아니라 메타데이터 컬럼 조건도 사용할 수 있습니다.
- 삭제 대상 중 하나라도 실제 데이터 row를 가지고 있으면 문장 전체가 실패합니다.
- 즉, 실제로 데이터가 입력된 태그의 메타데이터는 삭제할 수 없습니다.
- 전체 삭제 시에도 사용 중인 태그가 하나라도 있으면 일부만 삭제하지 않고 문장 전체가 실패합니다.
- tag name 컬럼명을 `name` 이 아닌 다른 이름으로 정의한 TAG 테이블에서도 같은 문법을 사용할 수 있습니다.

<a id="condition-tag-kv-delete-before"></a>

## TAG/KV DELETE 허용 조건과 BEFORE 조건

TAG, KV, LOG 테이블은 `BEFORE` 조건으로 특정 시점 이전 데이터를 일괄 삭제할 수 있습니다. LOG 테이블은 `OLDEST`, `EXCEPT`, `BEFORE` 등 로그 보존형 DELETE를 사용하고, TAG/KV 테이블은 `BEFORE` 외에도 태그 이름과 축 조건을 사용한 `WHERE` 삭제를 지원합니다.

### BEFORE 조건의 역할

`BEFORE` 조건은 오래된 데이터를 빠르게 정리할 때 사용하는 보존형 삭제 조건입니다. 지정한 시각은 현재 시각보다 과거여야 하며, 미래 시각을 지정하면 오류가 발생합니다.

### TAG 테이블 DELETE

```sql
-- 특정 날짜 이전 데이터 삭제
DELETE FROM tag BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- 특정 시각 이전 데이터 삭제
DELETE FROM tag BEFORE '2024-01-01 00:00:00 000:000:000';

-- NOW 기준 상대 시간
DELETE FROM tag BEFORE NOW - 7776000000000000;  -- 90일 이전 삭제
```

### LOG 테이블 DELETE

```sql
-- 30일 이전 데이터 삭제
DELETE FROM sensor_log BEFORE NOW - 2592000000000000;

-- 특정 날짜 이전 삭제
DELETE FROM event_log BEFORE TO_DATE('2023-12-31', 'YYYY-MM-DD');
```

### WHERE 조건 삭제와 구분

TAG/KV 테이블에서는 태그 이름 또는 축 조건으로 `WHERE` 삭제도 사용할 수 있습니다. 반면 LOG 테이블에서는 임의의 일반 `WHERE` 조건 삭제가 아니라 로그 전용 삭제 구문을 사용합니다.

```sql
-- TAG: tag name 기준 삭제 가능
DELETE FROM tag WHERE name = 'TEMP-01';

-- LOG: 일반 WHERE 조건 삭제는 사용하지 않음
DELETE FROM sensor_log WHERE value > 100.0;
-- → 오류 발생
```

### Retention Policy와의 관계

BEFORE 조건을 이용한 수동 DELETE 대신, [Retention Policy](/dbms/operations-configuration-recovery/policy-data-retention/)를 사용하면 지정된 주기마다 자동으로 오래된 데이터를 삭제할 수 있습니다. 운영 편의성 측면에서는 Retention Policy 설정이 권장됩니다.

```sql
-- 자동 삭제 정책 적용 (수동 DELETE 불필요)
ALTER TABLE sensor_log ADD RETENTION policy_30d;
```

### 주의 사항

- BEFORE 조건으로 삭제된 데이터는 복구할 수 없습니다.
- 대량 데이터 삭제 시 성능 영향이 있을 수 있으므로, 업무 시간 외 실행을 권장합니다.
- TAG 테이블의 경우 BEFORE 조건은 BASETIME 컬럼 기준으로 적용됩니다.

<a id="policy-truncate"></a>

## TRUNCATE 정책

TRUNCATE는 테이블의 모든 데이터를 빠르게 삭제하는 DDL 명령입니다. Machbase에서는 **LOG와 RDB 테이블에서만** 지원됩니다.

### 지원 테이블 확인

소스 코드(`qpvTruncateTable.c`) 기준으로 TRUNCATE는 LOG와 RDB 테이블에서만 허용됩니다. 다른 테이블 타입에 TRUNCATE를 실행하면 오류(`ERR_QP_TRUNCATE_NON_LOG_TABLE`)가 발생합니다.

| 테이블 타입 | TRUNCATE 지원 |
|------------|--------------|
| TAG | X |
| LOG | O |
| RDB | O |
| VOLATILE | X |
| LOOKUP | X |

### LOG 테이블 TRUNCATE

```sql
TRUNCATE TABLE sensor_log;
-- 테이블 구조는 유지되고 모든 데이터가 삭제됩니다.
```

### RDB 테이블 TRUNCATE

```sql
TRUNCATE TABLE orders;
-- 모든 주문 데이터 삭제. 테이블 스키마는 유지됩니다.
```

RDB 테이블의 TRUNCATE는 내부적으로 `DELETE FROM` 전체 행 삭제(`qrdDeleteAllRows`)로 구현됩니다.

### TRUNCATE vs DELETE 비교

| 항목 | TRUNCATE | DELETE (전체) |
|------|---------|---------------|
| 처리 방식 | DDL (단번에 처리) | DML (행 단위 처리) |
| 속도 | 빠름 | 느림 (대용량 시) |
| 롤백 | RDB는 트랜잭션 내 롤백 가능 | 가능 (트랜잭션 내) |
| WHERE 조건 | 불가 | 가능 |
| 트리거 발생 | X | X |

### 주의 사항

- LOG TRUNCATE는 실행 전 데이터 백업 여부를 반드시 확인하세요. RDB TRUNCATE는 명시적 트랜잭션 안에서 롤백할 수 있습니다.
- TAG, VOLATILE, LOOKUP 테이블에 TRUNCATE를 실행하면 오류가 발생합니다. 이 경우 `DELETE FROM ... BEFORE NOW` (TAG/LOG) 또는 조건 없는 DELETE를 사용하세요.
- VOLATILE 테이블 전체 삭제: `DELETE FROM device_status;` (WHERE 없이 삭제 가능)
