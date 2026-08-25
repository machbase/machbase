---
type: docs
title: '17.8.6 evidence-map'
weight: 60
toc: true
---

AI 응답의 공개 근거는 이 사이트의 canonical reference를 사용합니다. 내부 issue, pull request,
commit hash와 소스 트리 경로는 제품 사용자가 검증할 수 있는 안정적인 공개 근거가 아니므로
응답에 노출하지 않습니다.

## 기능별 공개 근거

| 사실 범주 | 우선 참조 |
|---|---|
| 논리 database, `USE`, 세 부분 객체 이름 | [다중 database](/dbms/operations-configuration-recovery/multi-database/) |
| 사용자, AUTH KEY, 비밀번호 정책 | [계정·권한·접속 제어](/dbms/security-access-control/) |
| SQL grammar와 지원 구문 | [SQL 레퍼런스](/dbms/reference/sql/) |
| Python, Go, JDBC, Node.js, .NET API | [개발 도구 연동](/dbms/development-tools-integration/) |
| Named Bind와 영향 행 수 | [애플리케이션 연동](/dbms/development-tools-integration/) |
| 시스템 뷰와 메타 테이블 열 | [시스템 카탈로그](/dbms/reference/log-logs-system-catalog/) |
| Edition·table type·SDK 제한 | [지원 범위와 제약](/dbms/reference/support-scope-constraints/) |
| 오류 코드 의미 | [오류 코드 사전](/dbms/reference/error-dictionary-codes/) |

## 검증 규칙

1. reference의 문법, 열, 타입과 예제를 먼저 확인합니다.
2. 설치 버전과 SDK 최소 버전 조건을 함께 확인합니다.
3. 운영 명령은 실제 배포본의 `--help`와 현재 상태를 대조합니다.
4. 실행 가능한 예제는 고유한 임시 객체에서 검증하고 정리합니다.
5. 공개 문서와 실제 배포가 다르면 추측하지 말고 `확인 필요:`로 표시합니다.

성능 우위, 보안 강도, 기본값과 제한 수치는 환경이나 버전에 따라 달라질 수 있습니다. 공개
reference에 명시되지 않은 단정은 생성하지 않습니다.
