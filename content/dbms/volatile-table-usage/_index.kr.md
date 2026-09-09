---
type: docs
title: '10. VOLATILE 테이블 활용'
weight: 100
toc: true
---

VOLATILE 테이블은 서버 프로세스 범위에서 공유되는 메모리 테이블입니다. 재시작 시 데이터
소실, UPSERT와 재생성 가능한 캐시 패턴을 다룹니다.

## 이 장의 구성

| 절 | 내용 |
|----|------|
| [개요와 사용 기준](./overview-use-criteria/) | VOLATILE 테이블의 특성과 적용 판단 기준 |
| [테이블 구조와 스키마](./table-structure-schema/) | PRIMARY KEY 설계, 컬럼 타입, 스키마 구성 |
| [생성, 변경, 삭제](./create-alter-drop/) | CREATE VOLATILE TABLE, DROP, 영속성 차이 |
| [데이터 입력과 변경](./data-input-mutation/) | INSERT, ON DUPLICATE KEY UPDATE, DELETE |
| [조회와 분석](./query-analysis/) | SELECT, 조건 조회, LIKE |
| [인덱스와 성능](./index-performance/) | Red-Black 트리 인덱스, PK 인덱스 |
| [운영과 데이터 생명주기](./operations-lifecycle/) | 운영 절차와 데이터 관리 |
| [제약, 오류, 문제 해결](./constraints-errors-troubleshooting/) | 기능 제약, 오류 대응 |
