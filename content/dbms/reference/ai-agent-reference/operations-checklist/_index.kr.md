---
type: docs
title: '17.8.10 operations-checklist'
weight: 100
toc: true
---

운영 답변은 [운영 체크리스트](/dbms/operations-configuration-recovery/checklist/)를 정본으로
사용하고 다음 안전 순서를 적용합니다.

1. 증상, 발생 시각, 전체 오류와 대상 database·node·table을 식별합니다.
2. `machadmin -e`, 관련 `V$` 뷰와 로그로 현재 상태를 읽기 전용으로 확인합니다.
3. 정상 동작과 장애 상태를 구분하고 변경이 필요한 근거를 제시합니다.
4. 변경 대상, 영향, downtime, rollback과 성공 조건을 명시합니다.
5. 사용자의 승인 범위를 확인한 뒤 한 단계씩 실행하고 결과를 재확인합니다.

서버 재시작, 세션 종료, 데이터 삭제, 설정 변경, backup 복구와 cluster node 변경을
진단 명령처럼 자동 제안하지 않습니다. 명령과 SQL은 해당
[운영 장](/dbms/operations-configuration-recovery/)에서 확인합니다.
