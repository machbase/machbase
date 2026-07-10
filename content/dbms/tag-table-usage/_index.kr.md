---
title: '5. TAG 테이블 활용'
weight: 50
toc: true
---

TAG 테이블은 태그 이름과 시간 또는 거리 축을 기준으로 계측 데이터를 저장하는 테이블입니다. ROLLUP을 제외한 TAG 테이블의 구조, 메타데이터, 입력, 조회, 보정, 운영을 다루며, ROLLUP은 별도 장에서 설명합니다.

## 이 장의 구성

| 절 | 내용 |
|----|------|
| [개요와 사용 기준](./overview-use-criteria/) | TAG 테이블의 개념과 사용 기준 |
| [테이블 구조와 스키마](./table-structure-schema/) | 컬럼 설계, 스토리지 전략, 중복 제거 |
| [생성, 변경, 삭제](./create-alter-drop/) | TAG 테이블 DDL과 속성 설정 |
| [데이터 입력과 변경](./data-input-mutation/) | INSERT, CSV 임포트, REST API, SDK 입력 |
| [조회와 분석](./query-analysis/) | 시간·거리 범위 조회, 통계, REST API 조회 |
| [인덱스와 성능](./index-performance/) | 자동 인덱스, METADATA 인덱스, TAG/KV 인덱스 |
| [운영과 데이터 생명주기](./operations-lifecycle/) | 데이터 삭제, 중복 제거 운영 |
| [제약, 오류, 문제 해결](./constraints-errors-troubleshooting/) | UPDATE 조건 오류, SET 대상 오류, 제약사항 |
| [활용 패턴과 시나리오](./patterns-scenarios/) | IoT, 에너지, 차량 추적 활용 사례 |
| [TAG 메타데이터](./tag-metadata/) | 메타데이터 CRUD, JSON 메타데이터, path 인덱스 |
| [시간축과 거리축 TAG](./time-distance-axis/) | 시간축·거리축 설계와 조회 패턴 |
| [TAG data UPDATE와 데이터 보정](./tag-data-update-correction/) | 시계열 데이터 직접 정정, 보정 이력 패턴 |
| [tagmetaimport와 메타데이터 일괄 등록](./tagmetaimport/) | CSV 기반 메타데이터 일괄 로드 |
| [TAG cache와 운영 튜닝](./tag-cache-operations/) | TAG 캐시 초기화와 크기 설정 |
