---
type: docs
title: '18.8.10 operations-checklist'
weight: 100
toc: true
---

AI 에이전트는 운영 명령을 생성하기 전에 Edition, 서버 상태, 변경 영향과 승인 범위를 먼저
확인해야 합니다. 조회와 상태 수집을 우선하고, 재시작·세션 종료·설정 변경을 자동 실행하지
않습니다.

## 안전한 상태 확인

```bash
machadmin -e
```

```sql
SELECT * FROM V$VERSION;
SELECT ID, USER_NAME, CLOSED FROM V$SESSION ORDER BY ID;
SELECT ID, SESS_ID, STATE, QUERY FROM V$STMT ORDER BY ID;
SELECT * FROM V$STORAGE_USAGE;
SELECT * FROM V$SYSMEM;
SELECT * FROM V$ROLLUP;
```

`machadmin -c`는 상태 확인이 아니라 database 생성 옵션이므로 사용하지 않습니다.

## 판단 순서

1. 오류 발생 시각과 전체 `ERR-` 메시지를 보존합니다.
2. 서버·네트워크·인증·SQL 중 실패 단계를 구분합니다.
3. 같은 시각의 서버 로그와 세션·statement 상태를 확인합니다.
4. 설정값은 `V$PROPERTY`, schema는 `M$SYS_*` 정본에서 조회합니다.
5. 조치 전 영향 범위, 되돌림 방법과 완료 조건을 명시합니다.

세션 종료, ROLLUP 강제 처리, database 백업·복구, 노드 변경은 사용자 승인과 대상 식별 없이
생성하거나 실행하지 않습니다. 고정 사용률이나 주기 대신 운영 환경의 용량 계획과 SLO를
기준으로 경고 임계값을 정합니다.

## 주요 정본

| 목적 | 정본 |
|---|---|
| 문제 해결 절차 | [17. 문제 해결](/dbms/troubleshooting/) |
| 세션·스토리지·ROLLUP 뷰 | [시스템 카탈로그](/dbms/reference/log-logs-system-catalog/) |
| 현재 설정과 범위 | [설정 사전](/dbms/reference/configuration/dictionary-configuration/) |
| 권한 현황 | [권한 관리](/dbms/security-access-control/privileges/) |
| 오류 코드 의미 | [오류 코드 사전](/dbms/reference/error-dictionary-codes/) |
