---
title: '7. LOG 테이블 활용'
weight: 70
toc: true
---

LOG 테이블은 시간순으로 지속 입력되는 이벤트와 로그 데이터를 저장하는 기본 테이블입니다. 구조, 입력 경로, 텍스트 검색, 수집 파이프라인, 운영 방법 순으로 설명합니다.

## 이 장의 구성

| 절 | 내용 |
|----|------|
| [개요와 사용 기준](./overview-use-criteria/) | LOG 테이블의 특성과 적용 판단 기준 |
| [테이블 구조와 스키마](./table-structure-schema/) | 컬럼 구성, 데이터 타입 선택, 스키마 설계 |
| [생성, 변경, 삭제](./create-alter-drop/) | CREATE, DROP, TRUNCATE 구문 |
| [데이터 입력과 변경](./data-input-mutation/) | INSERT, Append, Import, LOAD DATA |
| [조회와 분석](./query-analysis/) | SELECT, DURATION, JOIN 활용 |
| [인덱스와 성능](./index-performance/) | LSM, BITMAP, KEYWORD 인덱스 튜닝 |
| [운영과 데이터 생명주기](./operations-lifecycle/) | 데이터 삭제와 보존 정책 |
| [제약, 오류, 문제 해결](./constraints-errors-troubleshooting/) | 지원하지 않는 기능과 주의사항 |
| [활용 패턴과 시나리오](./patterns-scenarios/) | 로그 저장, 텍스트 검색, 집계 분석 예제 |
| [_arrival_time 시간 모델](./arrival-time-model/) | 자동 시각 컬럼의 특성과 조회 |
| [텍스트 검색과 KEYWORD 인덱스](./text-search-keyword-index/) | SEARCH, ESEARCH, LIKE, REGEXP |
| [네트워크 타입 조회](./regex-network-query/) | IPV4/IPV6 저장과 비교 |
| [Collector 기반 수집](./collector-ingestion/) | LOG 대상 스키마와 record mapping |

Fluentd 설치·buffer·retry 설정은
[외부 도구 연동](/dbms/development-tools-integration/external-tools/fluentd/)을 참고하십시오.
