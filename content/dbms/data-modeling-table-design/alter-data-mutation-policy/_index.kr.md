---
type: docs
title: '4.3 데이터 변경 정책'
weight: 30
toc: true
---

테이블 타입에 따라 `UPDATE`, `DELETE`, `TRUNCATE` 지원 범위가 다릅니다. 이 페이지는
데이터 모델을 선택할 때 필요한 정책만 요약합니다. 정확한 문법과 제약은 연결된 SQL
레퍼런스를 기준으로 확인하십시오.

## 테이블 타입별 데이터 변경 지원 범위

| 테이블 타입 | UPDATE | DELETE | TRUNCATE |
|------------|--------|--------|----------|
| TAG | 태그 선택 조건과 BASETIME 조건 필요 | `BEFORE` 또는 태그/축 조건 | X |
| LOG | X | `BEFORE`, `OLDEST`, `EXCEPT`, 전체 삭제 | O |
| TRANSACTION | O | O | O |
| VOLATILE | 기본 키 조건 | 기본 키 조건 또는 전체 삭제 | X |
| LOOKUP | 일반 조건식, PK 변경 불가 | 일반 조건식 또는 전체 삭제 | X |

LOG 테이블은 적재한 이벤트를 수정하지 않는 구조입니다. 수정이 잦은 상태·설정 정보는
VOLATILE, LOOKUP 또는 TRANSACTION 테이블에 저장하십시오.

<a id="policy-update"></a>

## UPDATE 정책

### TRANSACTION, VOLATILE, LOOKUP

- TRANSACTION은 일반 관계형 `UPDATE`와 트랜잭션을 지원합니다.
- VOLATILE은 기본 키 일치 조건으로 대상을 지정합니다.
- LOOKUP은 일반 조건식을 사용할 수 있지만 기본 키 컬럼 자체는 바꿀 수 없습니다.

LOOKUP의 지원 predicate와 표현식은
[LOOKUP predicate UPDATE](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/lookup-predicate-update-syntax/)를
참고하십시오.

<a id="policy-update-policy-tag-data-update"></a>
<a id="policy-update-distinction-tag-data-update-metadata"></a>
<a id="policy-update-tag-data-update-where-set-standard-only"></a>

### TAG data UPDATE

TAG의 실제 시계열 데이터와 메타데이터는 서로 다른 구문으로 수정합니다.

| 대상 | 구문 | 핵심 제약 |
|------|------|-----------|
| 시계열 데이터 | `UPDATE tag_table SET ... WHERE ...` | 태그 선택 조건과 BASETIME 조건이 모두 필요 |
| 메타데이터 | `UPDATE tag_table METADATA SET ...` | TAG 메타데이터 전용 구문 사용 |

TAG data UPDATE는 Standard Edition의 논리 TAG 테이블에서 지원합니다. 태그 이름,
BASETIME, 메타데이터 컬럼은 `SET` 대상이 될 수 없습니다. 수정한 구간에 구체화된 롤업이
있다면 `ROLLUP_REBUILD`로 다시 생성하십시오.

문법과 허용 표현식은 다음 레퍼런스가 정본입니다.

- [TAG data UPDATE](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/tag-data-update-syntax/)
- [TAG data UPDATE WHERE/SET 제약](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/tag-data-update-where-set-constraints/)
- [TAG 메타데이터](/dbms/tag-table-usage/tag-metadata/)

LOG 테이블은 `UPDATE`를 지원하지 않습니다.

<a id="policy-delete"></a>

## DELETE 정책

### TRANSACTION, VOLATILE, LOOKUP

- TRANSACTION은 일반 `WHERE` 조건으로 삭제할 수 있습니다.
- VOLATILE은 기본 키 조건으로 삭제하거나 조건 없이 전체 행을 삭제할 수 있습니다.
- LOOKUP은 일반 조건식으로 삭제하거나 `WHERE` 없이 전체 행을 삭제할 수 있습니다.

LOOKUP의 지원 predicate는
[LOOKUP predicate DELETE](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/lookup-predicate-delete-syntax/)를
참고하십시오.

### LOG

LOG는 임의의 일반 `WHERE` 조건 대신 로그 보존형 삭제 구문을 사용합니다.

```sql
DELETE FROM sensor_log OLDEST 1000 ROWS;
DELETE FROM sensor_log EXCEPT 7 DAY;
DELETE FROM sensor_log BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');
DELETE FROM sensor_log;
```

<a id="condition-tag-kv-delete-before"></a>

### TAG/KV

TAG/KV는 `BEFORE`로 오래된 데이터를 정리하거나, 태그 이름과 축 조건을 사용해 대상을
지정합니다. `BEFORE` 시각은 현재보다 과거여야 합니다.

```sql
DELETE FROM tag BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');
DELETE FROM tag WHERE name = 'TEMP-01';
DELETE FROM tag
 WHERE name = 'TEMP-01'
   AND time < TO_DATE('2024-01-01', 'YYYY-MM-DD');
```

수동 보존 삭제를 반복해야 한다면
[Retention Policy](/dbms/operations-configuration-recovery/policy-data-retention/)를
사용하십시오.

<a id="delete-tag-metadata"></a>
<a id="policy-delete-delete-tag-metadata"></a>

### TAG 메타데이터

TAG 메타데이터는 `DELETE FROM table_name METADATA` 구문으로 삭제합니다. 대상 중 실제
데이터가 있는 태그가 하나라도 있으면 문장 전체가 실패합니다.

```sql
DELETE FROM tag METADATA WHERE name = 'TEMP-01';
```

상세 조건은 [TAG 메타데이터](/dbms/tag-table-usage/tag-metadata/)를 참고하십시오.

<a id="policy-truncate"></a>

## TRUNCATE 정책

`TRUNCATE TABLE`은 LOG와 TRANSACTION에서만 지원합니다. 스키마와 인덱스 정의는
유지하고 모든 행을 제거합니다.

```sql
TRUNCATE TABLE sensor_log;
TRUNCATE TABLE orders;
```

| 항목 | TRUNCATE | DELETE |
|------|----------|--------|
| 대상 | 테이블 전체 | 타입에 따라 전체 또는 조건 지정 |
| `WHERE` | 불가 | 지원 범위 안에서 가능 |
| TRANSACTION 롤백 | 명시적 트랜잭션에서 가능 | 명시적 트랜잭션에서 가능 |

삭제 전 백업과 재입력 경로를 확인하십시오. TAG는 지원되는 `BEFORE` 또는 태그/축 조건을,
VOLATILE과 LOOKUP의 전체 삭제는 조건 없는 `DELETE`를 사용합니다.
