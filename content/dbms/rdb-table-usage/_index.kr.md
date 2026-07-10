---
title: '8. RDB 테이블 활용'
weight: 80
toc: true
---

RDB 테이블은 관계형 업무 데이터와 트랜잭션 처리가 필요한 데이터를 저장한다. 스키마 설계부터 DML, 트랜잭션, 인덱스, JOIN, 백업까지 RDB 테이블 운영 전반을 다룬다.

## 이 장의 구성

| 절 | 내용 |
|----|------|
| [개요와 사용 기준](./overview-use-criteria/) | RDB 테이블의 특성과 적용 판단 기준 |
| [테이블 구조와 스키마](./table-structure-schema/) | 컬럼 타입, PRIMARY KEY, 스키마 설계 |
| [생성, 변경, 삭제](./create-alter-drop/) | CREATE RDB TABLE, ALTER, DROP 문법 |
| [데이터 입력과 변경](./data-input-mutation/) | INSERT, UPDATE, DELETE, INSERT SELECT |
| [조회와 분석](./query-analysis/) | SELECT, 집계, 필터링 |
| [인덱스와 성능](./index-performance/) | PK 인덱스, 보조 인덱스, 쿼리 최적화 |
| [운영과 데이터 생명주기](./operations-lifecycle/) | 데이터 관리와 운영 절차 |
| [제약, 오류, 문제 해결](./constraints-errors-troubleshooting/) | Edition 제한, 기능 제약, 오류 대응 |
| [활용 패턴과 시나리오](./patterns-scenarios/) | 주문 관리, 재고, 설비 이력 등 실무 예시 |
| [트랜잭션](./transaction/) | BEGIN/COMMIT/ROLLBACK, 배치 INSERT |
| [잠금, 충돌, busy timeout](./locking-conflict-timeout/) | 잠금 현황 확인, 충돌 예방, 타임아웃 설정 |
| [RDB 인덱스와 JSON path 인덱스](./rdb-index-json-path/) | PRIMARY KEY·보조 인덱스 전략, JSON 경로 인덱스 |
| [JOIN과 관계형 조회 설계](./join-relational-query/) | RDB-LOOKUP, RDB-TAG, RDB-RDB JOIN |
| [RDB 백업, 마운트, sidecar](./backup-mount-sidecar/) | 백업/복원 절차, sidecar 구조와 복구 |
| [Append API 미지원과 SDK 사용 범위](./sdk-append-scope/) | Append API 동작 방식, SDK별 지원 현황 |
