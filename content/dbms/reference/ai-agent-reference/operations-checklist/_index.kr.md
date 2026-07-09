---
type: docs
title: '17.10.10 operations-checklist'
weight: 100
---

이 페이지는 AI 에이전트가 Machbase 운영 상태를 진단하거나 운영 관련 질문에 답할 때 참조하는 체크리스트입니다.

## 일상 모니터링 쿼리

### 서버 상태 확인

```bash
# 서버 기동 여부 확인 (OS 명령)
machadmin -c
```

### 세션 / 쿼리 모니터링

```sql
-- 현재 접속 세션 수
SELECT COUNT(*) FROM v$session;

-- 전체 세션 목록
SELECT sess_id, id, user_name, login_time, state FROM v$session;

-- 실행 중인 쿼리 (IDLE 상태 제외)
SELECT sess_id, id, state, query FROM v$stmt WHERE state != 'IDLE';
```

### 디스크 / 저장소 모니터링

```sql
-- 테이블스페이스 사용량
SELECT * FROM v$tablespace;

-- 메모리 사용 통계
SELECT name, value FROM v$sys_stat WHERE name LIKE '%MEMORY%';
```

### ROLLUP 상태 모니터링

```sql
-- ROLLUP 목록 및 상태
SELECT name, table_name, status, last_run_time FROM v$rollup;

-- ROLLUP 강제 실행
ALTER SYSTEM FLUSH ROLLUP;
```

### STREAM 상태 모니터링

```sql
-- STREAM 목록 및 상태
SELECT * FROM v$streams;

-- STREAM 재시작
EXEC STREAM_START('stream_name');
```

### 오류 로그 확인

```bash
# 서버 로그 최근 100줄에서 ERROR 검색
tail -100 $MACHBASE_HOME/trc/machbase.trc | grep -i ERROR
```

## 장애 징후 확인 및 조치

| 증상 | 확인 방법 | 조치 |
|------|-----------|------|
| 서버 접속 불가 | `machadmin -c`, 포트(5656) 확인 | 서버 기동: `machadmin -u` |
| 쿼리 응답 느림 | `v$stmt` 확인, `EXPLAIN` 실행 | 불필요한 세션 종료, 인덱스 확인 |
| 메모리 경고 | `v$sys_stat WHERE name LIKE '%MEMORY%'` | 대용량 쿼리 종료, 메모리 설정 확인 |
| 디스크 부족 | `df -h`, `v$tablespace` | 불필요 파일 정리, MOUNT된 백업 언마운트 |
| ROLLUP 지연 | `v$rollup` 상태 확인 | `ALTER SYSTEM FLUSH ROLLUP` |
| STREAM 멈춤 | `v$streams` 상태 = STOPPED | `EXEC STREAM_START('name')` |
| 특정 쿼리 멈춤 | `v$stmt` 에서 실행 중인 쿼리 확인 | `ALTER SYSTEM KILL SESSION sess_id` |

## 세션 관리

```sql
-- 특정 세션 강제 종료
ALTER SYSTEM KILL SESSION 12345;

-- IDLE 세션 확인
SELECT sess_id FROM v$session
WHERE state = 'IDLE';
-- 위 결과를 기반으로 개별 KILL SESSION 실행
```

## 정기 점검 항목 (주간)

| 점검 항목 | 점검 방법 | 기준 |
|-----------|-----------|------|
| 오래된 세션 정리 | `v$session` 확인 후 `KILL SESSION` | 불필요한 유휴 세션 |
| 백업 실행 여부 | 백업 스크립트 로그 확인 | 최소 주 1회 |
| 사용자 / 권한 현황 | `SELECT * FROM m$sys_users` | 불필요한 계정 비활성화 |
| ROLLUP 상태 | `v$rollup` 상태 및 `last_run_time` | 비정상 status 없어야 함 |
| 디스크 사용량 추이 | `v$tablespace`, `df -h` | 80% 초과 시 조치 |
| 에러 로그 검토 | `machbase.trc` 파일 | ERROR / FATAL 없어야 함 |

## 자주 사용하는 시스템 테이블 / 뷰

| 이름 | 목적 |
|------|------|
| `v$session` | 현재 세션 목록 |
| `v$stmt` | 실행 중인 SQL 문 목록 |
| `v$tablespace` | 테이블스페이스(디스크) 사용량 |
| `v$sys_stat` | 서버 통계 (메모리, I/O 등) |
| `v$rollup` | ROLLUP 목록 및 상태 |
| `v$streams` | STREAM 목록 및 상태 |
| `m$sys_tables` | 테이블 메타데이터 |
| `m$sys_columns` | 컬럼 메타데이터 |
| `m$sys_users` | 사용자 목록 |
| `m$sys_grants` | 권한 목록 |

## 참조

- 오류별 해결 방법: [error-resolution-map](../error-resolution-map/)
- 백업/복구 절차: [BACKUP/RESTORE/MOUNT](../../../operations-configuration-recovery/backup-restore-mount/)
- 문제 해결 전체: [Troubleshooting](../../../troubleshooting/)
