---
title: '10.12 Red-Black 트리 인덱스'
weight: 120
toc: true
---

<a id="index-strategy-red-black"></a>

## Red-Black 트리 인덱스

VOLATILE의 PRIMARY KEY와 보조 인덱스 설계는
[인덱스와 성능](/dbms/volatile-table-usage/index-performance/)을 정본으로 사용합니다.

VOLATILE 인덱스는 메모리에 저장되며 서버 재시작 때 데이터와 함께 사라집니다. 반복하는
PK 이외 조건에만 보조 인덱스를 추가하고, 데이터와 인덱스의 전체 메모리 사용량을 함께
측정하십시오.

정확한 `CREATE INDEX` 문법과 테이블 타입별 지원 범위는
[INDEX syntax](/dbms/reference/sql/syntax-dictionary-sql/index-syntax/)를 참고하십시오.
