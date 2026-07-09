---
type: docs
title: '1.4 다음에 읽을 문서 선택하기'
weight: 40
toc: true
---

빠른 시작을 마쳤다면 사용 목적에 맞는 다음 문서를 선택합니다. 같은 Machbase DBMS를 사용하더라도 산업 IoT 센서 값을 저장하려는 사용자, 금융 틱 데이터를 적재하려는 사용자, 로그를 분석하려는 사용자, 애플리케이션을 연결하려는 사용자가 읽어야 할 다음 문서는 서로 다릅니다. Machbase DBMS 매뉴얼은 기능 이름보다 사용자의 설계 질문을 기준으로 읽는 것이 효과적입니다.

다음 문서를 고를 때는 네 가지 질문을 먼저 던져 보십시오. 데이터가 얼마나 자주 들어오는지, 시간 범위로 얼마나 자주 조회하는지, 원본을 얼마나 오래 보관해야 하는지, 집계나 롤업이 필요한지입니다. 이 질문에 답하고 나면 어떤 테이블과 어떤 기능을 먼저 공부해야 하는지 분명해집니다.

## 다음 경로

| 해야 할 일 | 다음 문서 |
| --- | --- |
| 산업 IoT 센서, 설비, 계측값 저장 | [TAG 테이블 설계](/dbms/tag-table-usage/) |
| 로그, 이벤트, 금융 틱 수신 이력 저장 | [LOG 테이블 설계](/dbms/log-table-usage/) |
| 장비명, 코드, 매핑 정보 관리 | [LOOKUP 설계](/dbms/lookup-table-usage/), RDB 지원 버전에서는 [RDB 설계](/dbms/rdb-table-usage/)와 [LOOKUP과 RDB 비교](/dbms/data-modeling-table-design/table-types-selection-type/comparison-rdb-vs-lookup/) |
| SQL 문법 확인 | [SQL 레퍼런스](/dbms/reference/sql/), [SQL 입력](/dbms/data-input-load-export/sql/) |
| 애플리케이션 연결 | [애플리케이션 연동](/dbms/application-integration/), [드라이버 가이드](/dbms/application-integration/guide-drivers/) |
| 운영 설정 변경 | [운영, 설정, 복구](/dbms/operations-configuration-recovery/) |

## 다음 문서에서 확인할 것

- TAG 문서에서는 `NAME`, `BASETIME`, 값 컬럼을 기준으로 센서 계측값을 모델링하는 방법을 확인합니다.
- LOG 문서에서는 이벤트와 로그를 시간 순서로 계속 추가하는 설계를 확인합니다.
- LOOKUP과 RDB 문서에서는 기준 정보, 매핑 정보, 조인 대상 데이터를 어떻게 나눌지 확인합니다.
- 데이터 입력 문서에서는 실습용 `INSERT`가 아니라 운영 수집에 사용하는 Append API, machloader, Collector 경로를 확인합니다.
