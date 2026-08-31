---
type: docs
title: '17.8.8 sql-generation-rules'
weight: 80
toc: true
---

AI가 SQL을 생성할 때 적용할 검증 순서입니다. 실제 문법은
[SQL 레퍼런스](/dbms/reference/sql/)가 정본입니다.

## 생성 전 확인

1. 서버 버전과 Edition을 확인합니다.
2. 대상 database, owner, 테이블 타입과 `DESC` 결과를 확인합니다.
3. [SQL 문법 사전](/dbms/reference/sql/syntax-dictionary-sql/)에서 statement 형식을 확인합니다.
4. [함수 사전](/dbms/reference/sql/dictionary/)에서 인자와 반환 타입을 확인합니다.
5. [지원 범위](/dbms/reference/support-scope-constraints/)에서 Edition·테이블 제약을 확인합니다.

## 생성 규칙

- 다른 DBMS의 keyword, 함수, hint나 transaction 동작을 추측해 사용하지 않습니다.
- identifier를 parameter marker로 대체하지 않습니다.
- 시간·거리 범위, DELETE와 UPDATE는 예상 대상 행을 먼저 조회할 수 있게 작성합니다.
- 결과 순서가 필요하면 `ORDER BY`를 명시합니다.
- 변경 예제에는 결과 확인과 cleanup을 포함합니다.

오류가 발생하면 문법을 임의로 변형하지 말고 전체 오류와 schema를
[문제 해결](/dbms/troubleshooting/) 절차로 확인합니다.
