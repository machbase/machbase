---
type: docs
title: 'VOLATILE 테이블 설계'
weight: 50
---

VOLATILE 테이블은 메모리에만 존재하는 임시 테이블입니다. 서버 재시작 시 데이터가 소멸되며, 세션 내 임시 집계·캐시 용도로 사용합니다.

- **[활용 사례](/dbms/volatile-table-usage/patterns-scenarios/use-cases-volatile/)**
- **[영속성 차이·DDL](/dbms/volatile-table-usage/create-alter-drop/differences-persistence-ddl/)**
- **[메모리 생명주기](/dbms/volatile-table-usage/memory-lifecycle/lifecycle-memory/)**
- **[PRIMARY KEY 설계](/dbms/volatile-table-usage/table-structure-schema/primary-key/design-primary-key/)**
- **[Red-Black 트리 인덱스](/dbms/volatile-table-usage/red-black-index/index-strategy-red-black/)**
- **[ON DUPLICATE KEY UPDATE](/dbms/volatile-table-usage/on-duplicate-key-update/on-duplicate-key-update/)**
- **[데이터 손실 위험](/dbms/volatile-table-usage/restart-data-loss/data-loss/)**
