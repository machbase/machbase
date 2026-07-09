---
title: '10. VOLATILE 테이블 활용'
weight: 100
toc: true
---

VOLATILE 테이블은 메모리에 데이터를 저장하는 임시 테이블입니다. 이 장은 메모리 생명주기, 재시작 시 데이터 소실, UPSERT, 캐시/임시 집계 패턴을 다룹니다.

## 이 장의 구성

| 절 | 내용 |
|----|------|
| [개요와 사용 기준](./overview-use-criteria/) | 개요와 사용 기준 관련 문서를 정리합니다. |
| [테이블 구조와 스키마](./table-structure-schema/) | 테이블 구조와 스키마 관련 문서를 정리합니다. |
| [생성, 변경, 삭제](./create-alter-drop/) | 생성, 변경, 삭제 관련 문서를 정리합니다. |
| [데이터 입력과 변경](./data-input-mutation/) | 데이터 입력과 변경 관련 문서를 정리합니다. |
| [조회와 분석](./query-analysis/) | 조회와 분석 관련 문서를 정리합니다. |
| [인덱스와 성능](./index-performance/) | 인덱스와 성능 관련 문서를 정리합니다. |
| [운영과 데이터 생명주기](./operations-lifecycle/) | 운영과 데이터 생명주기 관련 문서를 정리합니다. |
| [제약, 오류, 문제 해결](./constraints-errors-troubleshooting/) | 제약, 오류, 문제 해결 관련 문서를 정리합니다. |
| [활용 패턴과 시나리오](./patterns-scenarios/) | 활용 패턴과 시나리오 관련 문서를 정리합니다. |
| [메모리 생명주기](./memory-lifecycle/) | 메모리 생명주기 관련 문서를 정리합니다. |
| [재시작과 데이터 소실](./restart-data-loss/) | 재시작과 데이터 소실 관련 문서를 정리합니다. |
| [Red-Black 트리 인덱스](./red-black-index/) | Red-Black 트리 인덱스 관련 문서를 정리합니다. |
| [ON DUPLICATE KEY UPDATE](./on-duplicate-key-update/) | ON DUPLICATE KEY UPDATE 관련 문서를 정리합니다. |
| [상태 캐시와 임시 집계 패턴](./state-cache-temporary-aggregation/) | 상태 캐시와 임시 집계 패턴 관련 문서를 정리합니다. |
| [메모리 모니터링과 캐시 재구성](./memory-monitoring-cache-rebuild/) | 메모리 모니터링과 캐시 재구성 관련 문서를 정리합니다. |
