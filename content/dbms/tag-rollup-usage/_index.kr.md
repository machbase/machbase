---
title: '6. TAG 테이블을 위한 ROLLUP 활용'
weight: 60
toc: true
---

ROLLUP은 TAG 테이블의 시계열 데이터를 시간 단위로 집계해 조회 성능을 높이는 기능입니다. 이 장은 ROLLUP 설계, 생성, 조회, 운영, 재구성, 성능 튜닝을 한곳에 모아 설명합니다.

## 이 장의 구성

| 절 | 내용 |
|----|------|
| [ROLLUP 개요와 사용 기준](./overview-use-criteria/) | ROLLUP 개요와 사용 기준 관련 문서를 정리합니다. |
| [ROLLUP 대상 TAG 테이블 설계](./target-tag-table-design/) | ROLLUP 대상 TAG 테이블 설계 관련 문서를 정리합니다. |
| [ROLLUP 생성과 삭제](./create-delete-rollup/) | ROLLUP 생성과 삭제 관련 문서를 정리합니다. |
| [ROLLUP 조회 문법](./query-syntax-rollup/) | ROLLUP 조회 문법 관련 문서를 정리합니다. |
| [조건 ROLLUP](./conditional-rollup/) | 조건 ROLLUP 관련 문서를 정리합니다. |
| [Custom ROLLUP](./custom-rollup/) | Custom ROLLUP 관련 문서를 정리합니다. |
| [확장 ROLLUP](./extension-rollup/) | 확장 ROLLUP 관련 문서를 정리합니다. |
| [JSON SUMMARIZED ROLLUP](./json-summarized-rollup/) | JSON SUMMARIZED ROLLUP 관련 문서를 정리합니다. |
| [FIRST / LAST 함수](./first-last-rollup/) | FIRST / LAST 함수 관련 문서를 정리합니다. |
| [주/월/연 단위 조회와 시간대 기준](./week-month-year-timezone-rollup/) | 주/월/연 단위 조회와 시간대 기준 관련 문서를 정리합니다. |
| [ROLLUP 시작, 중지, 즉시 수집](./ingestion-control-rollup/) | ROLLUP 시작, 중지, 즉시 수집 관련 문서를 정리합니다. |
| [ROLLUP 상태 확인](./state-check-rollup/) | ROLLUP 상태 확인 관련 문서를 정리합니다. |
| [ROLLUP 삭제와 부분 재구성](./delete-partial-rebuild-rollup/) | ROLLUP 삭제와 부분 재구성 관련 문서를 정리합니다. |
| [ROLLUP_REBUILD](./rollup-rebuild/) | ROLLUP_REBUILD 관련 문서를 정리합니다. |
| [ROLLUP 운영 주의사항](./operational-notes-rollup/) | ROLLUP 운영 주의사항 관련 문서를 정리합니다. |
| [ROLLUP 성능 튜닝](./performance-tuning-rollup/) | ROLLUP 성능 튜닝 관련 문서를 정리합니다. |
| [ROLLUP 제약과 Cluster Edition 지원 범위](./support-scope-rollup/) | ROLLUP 제약과 Cluster Edition 지원 범위 관련 문서를 정리합니다. |
| [ROLLUP 활용 시나리오](./patterns-scenarios/) | ROLLUP 활용 시나리오 관련 문서를 정리합니다. |
