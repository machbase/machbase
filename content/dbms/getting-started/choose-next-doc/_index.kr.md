---
type: docs
title: '1.4 다음에 읽을 문서 선택하기'
weight: 40
toc: true
---

빠른 시작을 마쳤다면 사용 목적에 맞는 다음 문서를 선택합니다. 산업 IoT 센서 값을 저장하려는 경우, 금융 틱 데이터를 적재하려는 경우, 로그를 분석하려는 경우, 애플리케이션을 연결하려는 경우 각각 읽어야 할 문서가 다릅니다. 매뉴얼은 기능 이름보다 설계 질문을 기준으로 읽는 것이 효과적입니다.

다음 문서를 고를 때 네 가지 질문을 던져 보십시오. 데이터가 얼마나 자주 들어오는지, 시간 범위로 얼마나 자주 조회하는지, 원본을 얼마나 오래 보관해야 하는지, 집계나 롤업이 필요한지. 이 질문에 답하면 어떤 테이블과 어떤 기능을 먼저 공부할지 분명해집니다.

## 다음 경로

| 해야 할 일 | 다음 문서 |
| --- | --- |
| 산업 IoT 센서, 설비, 계측값 저장 | [TAG 테이블 설계](/dbms/tag-table-usage/) |
| 로그, 이벤트, 금융 틱 수신 이력 저장 | [LOG 테이블 설계](/dbms/log-table-usage/) |
| 장비명, 코드, 매핑 정보 관리 | [LOOKUP 설계](/dbms/lookup-table-usage/), [TRANSACTION 설계](/dbms/rdb-table-usage/), [LOOKUP과 TRANSACTION 비교](/dbms/data-modeling-table-design/table-types-selection-type/#comparison-rdb-vs-lookup) |
| SQL 문법 확인 | [SQL 레퍼런스](/dbms/reference/sql/), [SQL 입력](/dbms/development-tools-integration/data-input-load-export/#sql) |
| 애플리케이션 연결 | [애플리케이션 연동](/dbms/development-tools-integration/), [드라이버 가이드](/dbms/development-tools-integration/selection-integration-method/) |
| 운영 설정 변경 | [운영, 설정, 복구](/dbms/operations-configuration-recovery/) |

## 다음 문서에서 확인할 것

- TAG 문서: `NAME`, `BASETIME`, 값 컬럼을 기준으로 센서 계측값을 모델링하는 방법
- LOG 문서: 이벤트와 로그를 시간 순서로 계속 추가하는 설계
- LOOKUP/TRANSACTION 문서: 기준 정보, 매핑 정보, 조인 대상 데이터의 분리 방법
- 데이터 입력 문서: 실습용 `INSERT`가 아닌 운영 수집에 사용하는 Append API, machloader, Collector 경로
