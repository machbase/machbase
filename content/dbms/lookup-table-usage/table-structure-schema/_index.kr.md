---
title: '9.2 테이블 구조와 스키마'
weight: 20
toc: true
---
LOOKUP 테이블의 구조와 스키마 설계를 다룹니다.


<a id="lookup-table-design"></a>

## LOOKUP 테이블 설계

LOOKUP 테이블은 코드 테이블과 기준 정보를 저장하는 타입입니다. PRIMARY KEY로 각 행을
식별하고 Primary key equality 조건의 UPDATE/DELETE를 지원하며 디스크에 영속 저장됩니다.

- **[활용 사례](/dbms/lookup-table-usage/patterns-scenarios/#use-cases-lookup)**
- **[PRIMARY KEY 설계](/dbms/lookup-table-usage/primary-key-policy/#design-primary-key)**
- **[컬럼 및 시퀀스 설계](/dbms/lookup-table-usage/sequence-column/#design-column-lookup-sequence)**
- **[JSON 컬럼과 조회](/dbms/lookup-table-usage/json-column-query/#condition-query-lookup-json)**
- **[참조 설계 패턴](/dbms/lookup-table-usage/reference-master-modeling/#patterns-reference-design)**
- **[인덱스 전략](/dbms/lookup-table-usage/index-performance/#index-strategy-lookup)**
- **[PRIMARY KEY 정책](/dbms/lookup-table-usage/primary-key-policy/#policy-lookup-primary-key)**
- **[PRIMARY KEY 기반 UPDATE·DELETE](/dbms/lookup-table-usage/data-input-mutation/#update-lookup-basic)**
- **[백업·복구 지원 범위](/dbms/lookup-table-usage/operations-lifecycle/#recovery-support-scope-backup-lookup)**
- **[제약 및 주의사항](/dbms/lookup-table-usage/constraints-errors-troubleshooting/#limitations-lookup)**
