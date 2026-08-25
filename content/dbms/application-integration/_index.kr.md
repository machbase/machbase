---
type: docs
title: '12. 애플리케이션 연동'
weight: 120
toc: true
---

이 장은 애플리케이션의 연동 방식 선택과 공통 운영 원칙을 다룹니다. SDK 설치, 함수,
완전한 코드는 [11장 개발 도구 연동](/dbms/development-tools-integration/)을 정본으로
사용합니다.

## 읽는 순서

1. [연동 방식 선택](selection-integration-method/)에서 언어와 입력 방식에 맞는 SDK를
   고릅니다.
2. [공통 연동 개념](concepts-common/)에서 인증, 시간값, binding, transaction, retry를
   확인합니다.
3. [드라이버별 가이드](guide-drivers/)에서 해당 SDK 레퍼런스로 이동합니다.
4. [데이터 입력과 반출](data-input-load-export/)에서 INSERT, Append, 파일 도구를
   선택합니다.
5. 단일 INSERT 결과 식별자가 필요하면 [ROWID와 INSERT 결과 ID](rowid-generated-id/)를
   확인합니다.
6. Fluentd, Grafana, Tableau는 [외부 도구 연동](external-tools/)의 공통 검증 절차를
   적용합니다.

## 문서 소유 범위

| 위치 | 정본 내용 |
|------|-----------|
| 11장 개발 도구 연동 | SDK 설치, 연결, API, 코드 |
| 12장 애플리케이션 연동 | 선택 기준, 공통 설계와 운영 흐름 |
| 18장 레퍼런스 | SQL 구문, 설정, 명령줄, 시스템 카탈로그 |

같은 SDK 코드를 여러 장에 복제하지 않습니다. 제품·SDK 버전에 따라 달라지는 API는 11장의
해당 드라이버 페이지에서 확인하고, 12장에서는 의사결정과 교차 SDK 원칙만 설명합니다.
