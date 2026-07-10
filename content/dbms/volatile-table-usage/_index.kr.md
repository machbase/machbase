---
title: '10. VOLATILE 테이블 활용'
weight: 100
toc: true
---

VOLATILE 테이블은 메모리에 데이터를 저장하는 임시 테이블입니다. 메모리 생명주기, 재시작 시 데이터 소실, UPSERT, 캐시/임시 집계 패턴 등 운영 전반을 다룹니다.

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
| [활용 패턴과 시나리오](./patterns-scenarios/) | 캐시, 임시 집계, 상태 관리 실무 예시 |
| [메모리 생명주기](./memory-lifecycle/) | 서버 수준 공유, 메모리 사용량, 자동 생성 패턴 |
| [재시작과 데이터 소실](./restart-data-loss/) | 데이터 손실 시나리오, 정기 플러시, 복구 스크립트 |
| [Red-Black 트리 인덱스](./red-black-index/) | 메모리 인덱스 구조, PK 자동 인덱스, 보조 인덱스 |
| [ON DUPLICATE KEY UPDATE](./on-duplicate-key-update/) | UPSERT 패턴, 카운터 패턴, 삽입값 갱신 |
| [상태 캐시와 임시 집계 패턴](./state-cache-temporary-aggregation/) | 실시간 캐시와 임시 집계 활용 |
| [메모리 모니터링과 캐시 재구성](./memory-monitoring-cache-rebuild/) | 메모리 사용량 감시와 캐시 재구축 |
