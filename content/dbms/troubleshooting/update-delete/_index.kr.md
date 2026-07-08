---
type: docs
title: 'UPDATE/DELETE 문제'
weight: 50
---

TAG 테이블과 LOOKUP 테이블의 UPDATE/DELETE는 LOG 테이블과 달리 여러 가지 제약이 있습니다. 이 섹션은 테이블 유형별 UPDATE/DELETE 제약과 그에 따른 일반적인 오류 상황을 다룹니다.

{{< callout type="info" >}}
**테이블 유형별 UPDATE/DELETE 지원 현황**

| 테이블 유형 | UPDATE | DELETE |
|-------------|--------|--------|
| LOG 테이블 | 미지원 | 제한적 지원 (파티션 삭제) |
| TAG 테이블 | 미지원 | tag 이름 조건 기반 지원 |
| LOOKUP 테이블 | PK 기반 지원 | PK 기반 지원 |
| Volatile 테이블 | 지원 | 지원 |
{{< /callout >}}

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [TAG data UPDATE가 거부될 때](./rejected-condition-tag-data-update-where/) | TAG 테이블 UPDATE 미지원과 대체 방법 |
| [TAG data UPDATE SET 대상 컬럼 오류](./column-error-tag-data-update-set/) | TAG 테이블 UPDATE 미지원과 컬럼별 제약 |
| [LOOKUP 일반 predicate UPDATE/DELETE가 거부될 때](./too-many-lookup-predicate-update-delete-row/) | 비-PK 조건 사용 시 오류 |
| [LOOKUP JSON 컬럼 생성 오류](./error-lookup-json-path-primary-key/) | LOOKUP 테이블 JSON 컬럼 제약 |
