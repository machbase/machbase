---
title: '6. TAG 테이블을 위한 ROLLUP 활용'
weight: 60
toc: true
---

ROLLUP은 TAG 테이블의 시계열 데이터를 시간 단위로 집계해 조회 성능을 높이는 기능입니다. 이 장에서는 ROLLUP의 설계, 생성, 조회, 운영, 재구성, 성능 튜닝을 다룹니다.

## 이 장의 구성

| 절 | 내용 |
|----|------|
| [ROLLUP 개요와 사용 기준](./overview-use-criteria/) | ROLLUP 동작 원리와 도입 판단 기준 |
| [ROLLUP 대상 TAG 테이블 설계](./target-tag-table-design/) | 계층 설계, ON/FROM 선택, 스토리지 예측 |
| [ROLLUP 생성과 삭제](./create-delete-rollup/) | CREATE ROLLUP / DROP ROLLUP 구문과 예시 |
| [ROLLUP 조회 문법](./query-syntax-rollup/) | rollup() 함수, 집계 함수, 힌트 사용법 |
| [조건 ROLLUP](./conditional-rollup/) | WHERE 필터로 조건부 집계 |
| [Custom ROLLUP](./custom-rollup/) | 사용자 정의 SELECT 기반 집계 |
| [확장 ROLLUP](./extension-rollup/) | EXTENSION 키워드와 FIRST/LAST 지원 |
| [JSON SUMMARIZED ROLLUP](./json-summarized-rollup/) | JSON 컬럼 내 숫자 필드 집계 |
| [ROLLUP 제어와 상태 확인](./ingestion-control-rollup/) | START/STOP/WAKEUP/FORCE, V$ROLLUP, ROLLUPGAP |
| [ROLLUP_REBUILD](./rollup-rebuild/) | DROP·재생성과 범위 재계산 선택 절차 |
| [ROLLUP 성능 튜닝](./performance-tuning-rollup/) | 계층 설계, 힌트, WAKEUP INTERVAL 조정 |
| [ROLLUP 활용 시나리오](./patterns-scenarios/) | IoT 센서, OHLC, 에너지 소비량 등 실전 예제 |

지원 여부는 [ROLLUP 지원 범위](/dbms/reference/support-scope-constraints/rollup/)를,
결과 지연과 불일치 진단은 [ROLLUP 문제 해결](/dbms/troubleshooting/rollup/)을 참고하십시오.
