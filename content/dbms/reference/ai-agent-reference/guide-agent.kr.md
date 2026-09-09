---
type: docs
title: '16.8.1 Agent 사용 가이드'
weight: 10
toc: true
---

이 가이드는 Machbase 관련 질문을 문서 정본에 근거해 답변하는 순서를 정의합니다.

## 질문 분류

| 질문 유형 | 먼저 확인할 문서 |
|----------|------------------|
| 설치·업그레이드 | [설치, 배포, 업그레이드](/dbms/installation-deployment-upgrade/) |
| 테이블 선택·설계 | [테이블 타입 개념과 선택](/dbms/data-modeling-table-design/) |
| SQL 문법·함수 | [SQL 레퍼런스](/dbms/reference/sql/) |
| SDK·연동 | [개발 및 애플리케이션 연동](/dbms/development-tools-integration/) |
| 지원 여부·제약 | [지원 범위와 제약](/dbms/reference/support-scope-constraints/) |
| 운영·복구 | [운영, 설정, 복구](/dbms/operations-configuration-recovery/) |
| 오류·성능 | [문제 해결](/dbms/troubleshooting/) 및 [성능 튜닝](/dbms/performance-tuning/) |

## 응답 생성 순서

1. 질문에서 제품 버전, Edition, 테이블 타입, SDK와 작업 대상을 식별합니다.
2. [용어 구분](../terminology-disambiguation/)으로 Machbase 의미를 확인합니다.
3. [지원표](../support-matrix/)와 [제약 인덱스](../constraints-index/)를 확인합니다.
4. 문법·API·운영 절차의 canonical page에서 실제 형식을 확인합니다.
5. 예제는 전제 조건, 실행, 결과 확인과 정리를 포함해 작성합니다.
6. 불확실한 사실은 단정하지 않고 확인에 필요한 버전·명령·문서를 제시합니다.

## 근거와 링크

- 공개 답변에는 docs.machbase.com의 canonical URL을 사용합니다.
- 내부 issue, commit이나 소스 경로는 공개 제품 동작의 대체 근거로 사용하지 않습니다.
- 여러 문서가 충돌하면 최신 버전별 정본과 실제 지원 범위를 우선합니다.

## 안전

조회와 진단을 먼저 제시합니다. 데이터 삭제, 서버 재시작, 세션 종료, 설정 변경과 복구는
사용자의 대상과 승인 범위를 확인하지 않고 실행 단계로 제시하지 않습니다.
