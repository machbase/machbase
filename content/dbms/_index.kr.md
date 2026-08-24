---
type: docs
title: 'Machbase DBMS 매뉴얼'
weight: 30
toc: true
---

Machbase DBMS 매뉴얼에 오신 것을 환영합니다. 이 문서는 Machbase 8.7.0을 기준으로 작성되었으며, 설치부터 테이블 타입별 활용, 개발 도구 연동, 애플리케이션 연동, 운영, 보안, 레퍼런스까지 Machbase의 기능을 다룹니다.

## 매뉴얼 구성

| 장 | 제목 | 내용 |
|----|------|------|
| 1 | [처음 시작하기](./getting-started/) | 개요, 접속 확인, 빠른 시작, 기본 명령 |
| 2 | [핵심 개념](./core-concepts/) | 테이블 유형, 시간 모델, ROLLUP, Retention Policy |
| 3 | [설치, 배포, 업그레이드](./installation-deployment-upgrade/) | 설치 준비, Standard Edition, Cluster Edition, 업그레이드 |
| 4 | [테이블 타입 개념과 선택](./data-modeling-table-design/) | 테이블 타입 비교, 선택 기준, 모델링 패턴과 안티패턴 |
| 5 | [TAG 테이블 활용](./tag-table-usage/) | TAG 구조, 메타데이터, 입력, 조회, 보정, 운영 |
| 6 | [TAG 테이블을 위한 ROLLUP 활용](./tag-rollup-usage/) | ROLLUP 설계, 생성, 조회, 재구성, 운영, 성능 튜닝 |
| 7 | [LOG 테이블 활용](./log-table-usage/) | LOG 구조, 입력, 텍스트 검색, Collector, Fluentd |
| 8 | [TRANSACTION 테이블 활용](./rdb-table-usage/) | TRANSACTION 스키마, DML, 트랜잭션, JOIN, 백업·복원 |
| 9 | [LOOKUP 테이블 활용](./lookup-table-usage/) | 기준 정보, PRIMARY KEY, JSON, 일반 predicate DML, JOIN |
| 10 | [VOLATILE 테이블 활용](./volatile-table-usage/) | 메모리 테이블, UPSERT, 상태 캐시, 재시작과 데이터 소실 |
| 11 | [개발 도구 연동](./development-tools-integration/) | Machbase SQLCLI, ODBC, JDBC, Python, Node.js, .NET, Go SDK/API |
| 12 | [애플리케이션 연동](./application-integration/) | 연동 방식 선택, 공통 개념, SDK 실무 예제 |
| 13 | [성능 튜닝](./performance-tuning/) | 쿼리 성능, 수집 성능, 캐시 튜닝 |
| 14 | [운영, 설정, 복구](./operations-configuration-recovery/) | 서버 관리, 백업, Cluster 운영 |
| 15 | [보안과 접근 제어](./security-access-control/) | 계정, 권한, AUTH KEY |
| 16 | [시나리오 가이드](./scenario-guides/) | 실전 시나리오별 단계별 가이드 |
| 17 | [문제 해결](./troubleshooting/) | 오류 진단 및 해결 방법 |
| 18 | [레퍼런스](./reference/) | SQL 문법, 함수, 설정, 시스템 카탈로그 |
