---
type: docs
title: 'TAG 메타데이터 삭제'
weight: 30
---

TAG 테이블의 메타데이터(sensor 이름/속성 정보)를 삭제하는 구문입니다.

## 문법

```sql
DELETE FROM table_name METADATA [WHERE condition];
```

WHERE 절을 생략하면 해당 TAG 테이블의 모든 메타데이터 행을 삭제합니다.

## 예시

```sql
-- 전체 메타데이터 삭제
DELETE FROM tag METADATA;

-- 특정 태그 메타데이터 삭제
DELETE FROM tag METADATA WHERE name = 'tag-1';

-- 메타데이터 컬럼 조건으로 삭제
DELETE FROM tag METADATA WHERE status = 'STOP';
```

## 주의사항

- WHERE name = '...' 뿐 아니라 메타데이터 컬럼 조건도 사용할 수 있습니다.
- 삭제 대상 중 하나라도 실제 데이터 row를 가지고 있으면 문장 전체가 실패합니다.
- 즉, 실제로 데이터가 입력된 태그의 메타데이터는 삭제할 수 없습니다.
- 전체 삭제 시에도 사용 중인 태그가 하나라도 있으면 일부만 삭제하지 않고 문장 전체가 실패합니다.
- tag name 컬럼명을 `name` 이 아닌 다른 이름으로 정의한 TAG 테이블에서도 같은 문법을 사용할 수 있습니다.
