---
type: docs
title: 'LOG 테이블 설계'
weight: 10
---

LOG 테이블은 이벤트·로그·패킷처럼 추가 전용(append-only) 데이터를 저장하는 기본 테이블 타입입니다. `CREATE TABLE` 문으로 생성하며, `_arrival_time` 컬럼이 자동으로 추가됩니다.

- **[활용 사례](/dbms/log-table-usage/patterns-scenarios/use-cases-log/)**
- **[_arrival_time 시간 모델](/dbms/log-table-usage/arrival-time-model/time-model-arrival-time/)**
- **[스키마 설계](/dbms/log-table-usage/table-structure-schema/log-table-design/design-schema-log/)**
- **[전문 검색 설계](/dbms/log-table-usage/text-search-keyword-index/design-text-search/)**
- **[네트워크 데이터 타입 설계](/dbms/log-table-usage/regex-network-query/design-type-network-data-types/)**
- **[제약 및 주의사항](/dbms/log-table-usage/constraints-errors-troubleshooting/limitations-log/)**
