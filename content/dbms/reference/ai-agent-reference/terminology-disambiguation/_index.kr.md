---
type: docs
title: '17.8.7 terminology-disambiguation'
weight: 70
toc: true
---

사용자 용어를 일반 데이터베이스 의미로 추측하지 말고 Machbase 정본에서 확인합니다.

| 용어 | 확인할 정본 |
|------|-------------|
| TAG, LOG, LOOKUP, VOLATILE, TRANSACTION | [핵심 개념](/dbms/core-concepts/)과 [테이블 타입 선택](/dbms/data-modeling-table-design/) |
| Append와 SQL INSERT | [연동 공통 개념](/dbms/development-tools-integration/concepts-common/) |
| ROLLUP | [ROLLUP 활용](/dbms/tag-rollup-usage/) |
| BASETIME, BASE DISTANCE, SUMMARIZED | [TAG 구조와 스키마](/dbms/tag-table-usage/table-structure-schema/) |
| AUTH KEY | [인증과 AUTH KEY](/dbms/security-access-control/authentication-auth-key/) |
| Broker, Warehouse | [Edition과 Cluster 개념](/dbms/core-concepts/concepts-edition/) |
| database, owner, tablespace | [다중 데이터베이스 운영](/dbms/operations-configuration-recovery/multi-database/) |

답변에서는 제품 객체명과 SQL keyword를 그대로 유지하고, 사용자가 일반 의미로 쓴 용어와
Machbase 객체가 다르면 먼저 구분합니다.
