---
type: docs
title: 'Machbase DBMS 매뉴얼'
weight: 30
toc: true
---

Machbase DBMS 매뉴얼에 오신 것을 환영합니다. 이 문서는 Machbase 8.7.0을 기준으로
설치, 테이블 타입별 활용, 애플리케이션 개발, 운영, 보안과 레퍼런스를 제공합니다.

## 매뉴얼 구성

| 장 | 제목 | 내용 |
|----|------|------|
| 1 | [처음 시작하기](./getting-started/) | 개요, 접속 확인, 빠른 시작, 기본 명령 |
| 2 | [핵심 개념](./core-concepts/) | 테이블 유형, 시간 모델, ROLLUP, Retention Policy |
| 3 | [설치, 배포, 업그레이드](./installation-deployment-upgrade/) | 설치 준비, Standard Edition, Cluster Edition, 업그레이드 |
| 4 | [테이블 타입 선택과 스키마 설계](./data-modeling-table-design/) | 타입 결정, 스키마, 변경 정책과 모델링 패턴 |
| 5 | [TAG 테이블 활용](./tag-table-usage/) | TAG 구조, 메타데이터, 입력, 조회, 보정, 운영 |
| 6 | [TAG 테이블을 위한 ROLLUP 활용](./tag-rollup-usage/) | ROLLUP 설계, 생성, 조회, 재구성, 운영, 성능 튜닝 |
| 7 | [LOG 테이블 활용](./log-table-usage/) | LOG 구조, 입력, 텍스트 검색과 Collector mapping |
| 8 | [TRANSACTION 테이블 활용](./rdb-table-usage/) | TRANSACTION 스키마, DML, 트랜잭션, JOIN, 백업·복원 |
| 9 | [LOOKUP 테이블 활용](./lookup-table-usage/) | 기준 정보, PRIMARY KEY, JSON, 일반 predicate DML, JOIN |
| 10 | [VOLATILE 테이블 활용](./volatile-table-usage/) | 메모리 테이블, UPSERT, 상태 캐시, 재시작과 데이터 소실 |
| 11 | [개발 및 애플리케이션 연동](./development-tools-integration/) | 연동 방식, 공통 개념과 언어별 SDK/API |
| 12 | [성능 튜닝](./performance-tuning/) | 쿼리 성능, 수집 성능, 캐시 튜닝 |
| 13 | [운영, 설정, 복구](./operations-configuration-recovery/) | 서버 관리, 백업, Cluster 운영 |
| 14 | [계정, 권한, 접속 제어](./security-access-control/) | 계정, 권한, AUTH KEY와 접속 제어 |
| 15 | [시나리오 가이드](./scenario-guides/) | 실전 시나리오별 단계별 가이드 |
| 16 | [문제 해결](./troubleshooting/) | 오류 진단 및 해결 방법 |
| 17 | [레퍼런스](./reference/) | SQL 문법, 함수, 설정, 시스템 카탈로그 |
