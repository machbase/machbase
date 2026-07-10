---
title: '9. LOOKUP 테이블 활용'
weight: 90
toc: true
---

LOOKUP 테이블은 소규모 기준 정보와 마스터 데이터를 빠르게 참조하기 위한 테이블이다. PRIMARY KEY 기반 구조, JSON/SEQUENCE, predicate DML, JOIN 활용을 다룬다.

## 이 장의 구성

| 절 | 내용 |
|----|------|
| [개요와 사용 기준](./overview-use-criteria/) | LOOKUP 테이블의 용도와 적합한 사용 조건 |
| [테이블 구조와 스키마](./table-structure-schema/) | 컬럼 구성, PK 구조, 스키마 설계 |
| [생성, 변경, 삭제](./create-alter-drop/) | DDL: CREATE, ALTER, DROP |
| [데이터 입력과 변경](./data-input-mutation/) | INSERT, Append, 리로드, 삭제 |
| [조회와 분석](./query-analysis/) | SELECT, JOIN, 조건 조회 |
| [인덱스와 성능](./index-performance/) | Red-Black 인덱스, 보조 인덱스, 튜닝 |
| [운영과 데이터 생명주기](./operations-lifecycle/) | 백업·복구, 데이터 영속성 |
| [제약, 오류, 문제 해결](./constraints-errors-troubleshooting/) | 제한 사항, 오류 원인과 대응 |
| [활용 패턴과 시나리오](./patterns-scenarios/) | 코드 테이블, 기준 정보, 임계값 관리 |
| [PRIMARY KEY 정책](./primary-key-policy/) | 자연키 vs 대리키, PK 불변 원칙 |
| [SEQUENCE 컬럼](./sequence-column/) | 자동 증가 번호 설정과 NEXTVAL 사용법 |
| [JSON 컬럼과 JSON 조회](./json-column-query/) | JSON 컬럼 지원 범위, path 조건 조회, primary key 제약 |
| [일반 predicate UPDATE/DELETE](./predicate-update-delete/) | non-PK 조건 기반 UPDATE/DELETE |
| [참조·마스터 데이터 모델링](./reference-master-modeling/) | 코드 참조, 메타데이터, 임계값 JOIN 패턴 |
| [LOOKUP 권한과 predicate DML 성능](./privilege-predicate-performance/) | 권한 설정, DML 성능 고려사항 |
