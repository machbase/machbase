---
title: '9.13 일반 predicate UPDATE/DELETE'
weight: 130
toc: true
---

LOOKUP 테이블은 기본 키뿐 아니라 일반 조건식으로 여러 행을 수정하거나 삭제할 수 있습니다.
변경 전 같은 조건으로 대상 행 수를 확인하십시오.

<a id="condition-lookup-update"></a>

## UPDATE

조건에 맞는 모든 행을 갱신합니다. `SET` 표현식은 현재 행 값을 참조할 수 있지만 기본 키
컬럼 자체는 변경할 수 없습니다.

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
