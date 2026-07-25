---
type: docs
title: '17.10.3 task-map'
weight: 30
toc: true
---

이 페이지는 사용자 태스크별 수행 방법과 참조 문서를 매핑합니다. AI 에이전트가 "어떻게 X를 하나요?" 유형의 질문에 답할 때 참조합니다.

## 데이터 저장

| 태스크 | 수행 방법 | 참조 문서 |
|--------|-----------|-----------|
| 센서/시계열 데이터 저장 | TAG 테이블 생성 후 Append API 사용 | [TAG 테이블](/dbms/tag-table-usage/), [Append](/dbms/application-integration/concepts-common/#append-api-batch) |
| 로그/이벤트 데이터 저장 | LOG 테이블 생성 후 Append API 또는 INSERT 사용 | [LOG 테이블](/dbms/log-table-usage/) |
| CSV/파일 일괄 입력 | machloader `-i` 옵션으로 파일 로드 | [machloader](/dbms/application-integration/data-input-load-export/#file-import-machloader) |
| LOOKUP 마스터 데이터 관리 | LOOKUP 테이블 INSERT/UPDATE/DELETE | [LOOKUP 테이블](/dbms/lookup-table-usage/) |
| 실시간 스트림 입력 | Collector 또는 Fluentd 플러그인 | [Collector](/dbms/operations-configuration-recovery/collector/), [Fluentd](/dbms/log-table-usage/fluentd-pipeline/) |

## 데이터 조회 / 분석

| 태스크 | 수행 방법 | 참조 문서 |
|--------|-----------|-----------|
| 특정 태그의 최신값 조회 | `SELECT ... FROM TAG TABLE t RECENT 1` | [SELECT RECENT](../../../reference/sql/syntax-dictionary-sql/select-syntax/) |
| 시간 범위 집계 조회 | ROLLUP 테이블 활용 또는 `GROUP BY` | [ROLLUP](/dbms/tag-rollup-usage/overview-use-criteria/#rollup) |
| 복잡한 조회를 단계별로 구성 | Standard Edition에서 비재귀 `WITH`/CTE 사용 | [WITH / CTE](/dbms/reference/sql/syntax-dictionary-sql/cte-syntax/) |
| 텍스트/로그 검색 | LOG 테이블에 `WHERE text LIKE` 또는 전문 검색 | [LOG 테이블](/dbms/log-table-usage/) |
| 시계열 보간 / 시리즈 분석 | `SERIES BY` 절 사용 | [SELECT 문법](../../../reference/sql/syntax-dictionary-sql/select-syntax/) |
| 복수 태그 비교 조회 | `FROM TAG TABLE t WHERE name IN (...)` | [TAG 테이블](/dbms/tag-table-usage/) |
| 집계 결과 빠른 조회 | ROLLUP 결과 테이블 SELECT | [ROLLUP](/dbms/tag-rollup-usage/overview-use-criteria/#rollup) |

## 사용자 / 보안

| 태스크 | 수행 방법 | 참조 문서 |
|--------|-----------|-----------|
| 사용자 생성 | `CREATE USER username IDENTIFIED BY password` | [사용자 관리](/dbms/security-access-control/account/) |
| 권한 부여 | `GRANT privilege ON object TO user` | [GRANT/REVOKE](/dbms/security-access-control/privileges/#grant-revoke) |
| AUTH KEY 등록 | `CREATE AUTH KEY` + 공개키 파일 등록 | [AUTH KEY](../../../security-access-control/authentication-auth-key/) |
| 원격 접속 허용 | 설정 파일 `BIND_IP_ADDRESS`, `PORT_NO` 확인 및 방화벽 설정 | [원격 접속](/dbms/security-access-control/access-control/) |
| 비밀번호 변경 | `ALTER USER username IDENTIFIED BY new_password` | [사용자 관리](/dbms/security-access-control/account/) |

## 운영 / 유지보수

| 태스크 | 수행 방법 | 참조 문서 |
|--------|-----------|-----------|
| 데이터 백업 | `BACKUP DATABASE INTO DISK = '/path'` | [BACKUP/RESTORE](/dbms/operations-configuration-recovery/backup-restore-mount/) |
| 백업 데이터 마운트 | `MOUNT DATABASE '/path' TO mount_name` | [MOUNT](/dbms/operations-configuration-recovery/backup-restore-mount/#database-mount) |
| 느린 쿼리 중지 | `v$stmt` 확인 후 `ALTER SYSTEM KILL SESSION` | [operations-checklist](../operations-checklist/) |
| 서버 상태 확인 | `machadmin -c` 또는 `SELECT * FROM v$session` | [operations-checklist](../operations-checklist/) |
| 이상 데이터 정정 | LOOKUP: UPDATE/DELETE, TAG: data UPDATE 후 필요 시 ROLLUP_REBUILD | [제약 사항](../constraints-index/) |
| 디스크 사용량 확인 | `SELECT * FROM v$tablespace` | [operations-checklist](../operations-checklist/) |

## 자동화

| 태스크 | 수행 방법 | 참조 문서 |
|--------|-----------|-----------|
| 집계 자동화 (ROLLUP) | `CREATE ROLLUP` 후 자동 실행 | [ROLLUP](/dbms/tag-rollup-usage/overview-use-criteria/#rollup) |
| ROLLUP 수동 재구성 | `EXEC ROLLUP_REBUILD(table_name, tag_name, start_time, end_time)` (Standard Edition) | [ROLLUP](/dbms/tag-rollup-usage/overview-use-criteria/#rollup) |
| 이벤트 기반 처리 | `CREATE STREAM` + 처리 쿼리 정의 | [STREAM](/dbms/operations-configuration-recovery/automation-stream/#stream) |
| 데이터 보존 정책 | RETENTION 설정 (LOG 테이블) | [LOG 테이블](/dbms/log-table-usage/) |
| STREAM 시작/중지 | `EXEC STREAM_START(name)` / `EXEC STREAM_STOP(name)` | [STREAM](/dbms/operations-configuration-recovery/automation-stream/#stream) |
