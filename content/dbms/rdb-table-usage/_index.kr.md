---
title: '8. TRANSACTION 테이블 활용'
weight: 80
toc: true
---

TRANSACTION 테이블은 관계형 업무 데이터와 트랜잭션 처리가 필요한 데이터를 저장합니다. 스키마 설계부터 DML, 트랜잭션, 인덱스, JOIN, 백업까지 TRANSACTION 테이블 운영 전반을 다룹니다.

## 이 장의 구성

| 절 | 내용 |
|----|------|
| [개요와 사용 기준](./overview-use-criteria/) | TRANSACTION 테이블의 특성과 적용 판단 기준 |
| [테이블 구조와 스키마](./table-structure-schema/) | 컬럼 타입, PRIMARY KEY, 스키마 설계 |
| [생성, 변경, 삭제](./create-alter-drop/) | CREATE TABLE/TRANSACTION/TXN, ALTER, DROP 문법과 DDL 복구 |
| [데이터 입력과 변경](./data-input-mutation/) | INSERT, UPDATE, DELETE, INSERT SELECT |
| [조회와 분석](./query-analysis/) | SELECT, 집계, 필터링 |
| [인덱스와 성능](./index-performance/) | PRIMARY KEY·UNIQUE INDEX·일반·JSON path 인덱스와 튜닝 |
| [운영과 데이터 생명주기](./operations-lifecycle/) | 데이터 관리와 운영 절차 |
| [제약, 오류, 문제 해결](./constraints-errors-troubleshooting/) | Edition 제한, 기능 제약, 오류 대응 |
| [트랜잭션](./transaction/) | BEGIN/COMMIT/ROLLBACK, 배치 INSERT |
| [잠금, 충돌, busy timeout](./locking-conflict-timeout/) | 동시 쓰기 충돌, 세션 timeout, 진단과 재시도 |
| [JOIN과 관계형 조회 설계](./join-relational-query/) | TRANSACTION-LOOKUP, TRANSACTION-TAG, TRANSACTION-TRANSACTION JOIN |
| [TRANSACTION 백업, 복원, 마운트](./backup-restore-mount/) | 전체·테이블 백업, 복원, 읽기 전용 마운트 |
| [INSERT ON DUPLICATE KEY UPDATE](./insert-on-duplicate-key-update/) | TRANSACTION upsert 문법과 충돌 처리 |

여러 테이블 타입에 공통인 자동 번호 문법은
[AUTO_INCREMENT](/dbms/reference/sql/syntax-dictionary-sql/auto-increment-syntax/)를 참고하십시오.
