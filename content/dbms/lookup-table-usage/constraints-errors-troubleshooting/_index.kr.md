---
title: '9.8 제약, 오류, 문제 해결'
weight: 80
toc: true
---
LOOKUP 테이블의 제약 사항, 발생 가능한 오류, 문제 해결 방법을 다룹니다.


<a id="too-many-lookup-predicate-update-delete-row"></a>

## 다중 row 변경 범위

일반 predicate UPDATE/DELETE는 여러 row에 적용될 수 있습니다. 실행 전 같은 predicate로
대상 수를 확인하고 [일반 predicate UPDATE/DELETE](../predicate-update-delete/)의 계약을
따릅니다.

<a id="error-lookup-json-path-primary-key"></a>

## LOOKUP JSON primary key 오류

JSON column은 일반 column으로 사용할 수 있지만 PRIMARY KEY로 선언할 수 없습니다. 식별자를
별도 scalar column으로 두고 [JSON 컬럼과 조회](../json-column-query/)의 type·path 규칙을
따릅니다.

<a id="limitations-lookup"></a>

## 제약 및 주의사항

- PRIMARY KEY 정책은 [PRIMARY KEY 정책](../primary-key-policy/)을 참고합니다.
- memory 규모와 index 비용은 [인덱스와 성능](../index-performance/)에서 측정합니다.
- 시계열 원본은 TAG, 재시작 후 사라져도 되는 cache는 VOLATILE을 선택합니다.
- Append gate는 [SDK Append matrix](/dbms/development-tools-integration/sdk-support-scope/#append-table-type-matrix)를 따릅니다.
