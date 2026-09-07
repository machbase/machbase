---
title: '9.13 일반 predicate UPDATE/DELETE'
weight: 130
toc: true
aliases:
  - /dbms/lookup-table-usage/privilege-predicate-performance/
---

LOOKUP 테이블은 기본 키뿐 아니라 일반 조건식으로 여러 행을 수정하거나 삭제할 수 있습니다.
변경 전 같은 조건으로 대상 행 수를 확인하십시오.

<a id="condition-lookup-update"></a>

## UPDATE

조건에 맞는 모든 행을 갱신합니다. `SET` 표현식은 현재 행 값을 참조할 수 있지만 기본 키
컬럼 자체는 변경할 수 없습니다.

LOOKUP UPDATE에는 `WHERE` 조건이 필요합니다. 전체 행을 갱신하려는 경우에도 지원되는
조건식을 명시합니다. `WHERE` 없이 전체 삭제가 가능한 DELETE와 구분하십시오.

```sql
SELECT COUNT(*)
  FROM equipment_master
 WHERE site = 'SEOUL' AND status = 'READY';

UPDATE equipment_master
   SET status = 'ACTIVE', score = score + 10
 WHERE site = 'SEOUL' AND status = 'READY';
```

<a id="condition-lookup-delete"></a>

## DELETE

조건에 맞는 모든 행을 삭제합니다. `WHERE`를 생략하면 테이블의 모든 행이 삭제됩니다.

```sql
SELECT COUNT(*)
  FROM equipment_master
 WHERE status = 'RETIRED';

DELETE FROM equipment_master
 WHERE status = 'RETIRED';
```

<a id="design-condition-lookup-update-delete"></a>

## 조건 설계 지침

1. 단건 변경에는 기본 키 조건을 사용합니다.
2. 일괄 변경 전 동일한 조건의 `SELECT COUNT(*)`로 영향 범위를 확인합니다.
3. 자주 필터링하는 JSON 값은 일반 컬럼으로 분리해 인덱스를 적용하는 방안을 검토합니다.
4. 기본 키를 바꿔야 한다면 기존 행을 삭제하고 새 키로 삽입합니다.

지원 연산자와 JSON 조건의 정확한 범위는 SQL 레퍼런스를 기준으로 확인하십시오.

- [LOOKUP predicate UPDATE](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/lookup-predicate-update-syntax/)
- [LOOKUP predicate DELETE](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/lookup-predicate-delete-syntax/)

## 권한과 성능

UPDATE와 DELETE에는 각각 대상 테이블의 `UPDATE`, `DELETE` 권한이 필요합니다. 애플리케이션이
변경 전후 값을 직접 조회할 때만 `SELECT`도 부여합니다. 권한 SQL은
[권한 관리](/dbms/security-access-control/privileges/)를 정본으로 사용합니다.

기본 키 equality는 단건 대상을 직접 찾고, 일반 조건식은 조건을 평가해 변경 대상을 수집합니다.
반복 단건 변경에는 prepared statement와 bind를 사용하고, 대량 변경은 같은 조건의 행 수와
실행 시간을 검증 환경에서 측정하십시오.
