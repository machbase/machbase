---
type: docs
title: '16.8.3 task-map'
weight: 30
toc: true
---

사용자 작업별로 확인할 정본과 완료 조건을 연결합니다.

| 작업 | 확인 순서 | 완료 확인 |
|------|-----------|-----------|
| 처음 설치 | [설치](/dbms/installation-deployment-upgrade/) → [시작하기](/dbms/getting-started/) | 서버 상태, 연결, 샘플 조회 |
| 테이블 선택 | [선택 기준](/dbms/data-modeling-table-design/) → 해당 테이블 장 | Edition·DML·축·보존 요구 충족 |
| 대량 입력 | [연동 공통 개념](/dbms/development-tools-integration/concepts-common/) → SDK 페이지 | 성공/실패 건수와 flush 확인 |
| SQL 작성 | [SQL 레퍼런스](/dbms/reference/sql/) → [지원 범위](/dbms/reference/support-scope-constraints/) | 실제 schema와 결과 확인 |
| SDK 선택 | [연동 방식 선택](/dbms/development-tools-integration/selection-integration-method/) → [SDK 지원 범위](/dbms/development-tools-integration/sdk-support-scope/) | 서버·SDK 버전과 API 일치 |
| 성능 진단 | [성능 접근법](/dbms/performance-tuning/performance-approach/) → 증상별 튜닝 | 기준값과 변경 후 측정 비교 |
| 장애 진단 | [문제 해결](/dbms/troubleshooting/) → [오류 코드](/dbms/reference/error-codes/) | 원인, 조치, 재발 방지 기록 |
| 백업·복구 | [백업·복구](/dbms/operations-configuration-recovery/backup-restore-mount/) | 복원 또는 MOUNT 조회 검증 |

작업에 쓰기·삭제·재시작이 포함되면 대상과 영향 범위를 확정한 뒤 실행 절차를 선택합니다.
