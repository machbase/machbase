---
type: docs
title: '공통 스키마와 데이터 생명주기 참고'
weight: 950
---

테이블과 인덱스를 정의하고, 데이터를 갱신·삭제하며, 보존 기간을 자동으로 관리하는 방법을 설명합니다.

## 이 장의 구성

- **[스키마 객체 정의](/dbms/schema-data-lifecycle/schema-objects-definition/)** — 테이블·인덱스·뷰 생성, 변경, 삭제
- **[데이터 변경 정책](/dbms/schema-data-lifecycle/alter-data-mutation-policy/)** — 테이블 타입별 UPDATE·DELETE·TRUNCATE 규칙
- **[데이터 보존 정책](/dbms/schema-data-lifecycle/policy-data-retention/)** — Retention Policy로 오래된 데이터 자동 삭제
- **[테이블 타입별 관리 가능 범위](/dbms/schema-data-lifecycle/table-types-type-manageable/)** — 타입별 DDL·DML 지원 현황 요약
- **[스키마 변경 체크리스트](/dbms/schema-data-lifecycle/checklist-schema-alter/)** — 운영 중 스키마 변경 시 확인 사항
