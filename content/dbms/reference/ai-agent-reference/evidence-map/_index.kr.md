---
type: docs
title: '17.8.6 evidence-map'
weight: 60
toc: true
---

답변의 주장 유형에 맞는 공개 근거를 선택합니다.

| 주장 유형 | 우선 근거 |
|----------|-----------|
| SQL 문법·함수·타입 | [SQL 레퍼런스](/dbms/reference/sql/) |
| Edition·테이블·SDK 지원 | [지원 범위와 제약](/dbms/reference/support-scope-constraints/) 및 [SDK 지원 범위](/dbms/development-tools-integration/sdk-support-scope/) |
| 설정 키·기본값 | [설정 레퍼런스](/dbms/reference/configuration/)와 배포본 설정 파일 |
| 시스템 상태 컬럼 | [시스템 카탈로그](/dbms/reference/log-logs-system-catalog/) |
| CLI option | [명령행 도구](/dbms/reference/command-line-tools/)와 배포본 `--help` |
| 오류 의미·조치 | [오류 코드](/dbms/reference/error-dictionary-codes/) 및 [문제 해결](/dbms/troubleshooting/) |
| 운영 절차 | [운영, 설정, 복구](/dbms/operations-configuration-recovery/) |

## 검증 규칙

- 버전과 Edition 조건을 근거와 함께 보존합니다.
- 예제 결과를 일반 보장이나 성능 수치로 확대하지 않습니다.
- 공개 정본에 없는 사실은 확인 필요 상태로 남깁니다.
- 내부 개발 이력은 공개 매뉴얼 링크를 대신하지 않습니다.
