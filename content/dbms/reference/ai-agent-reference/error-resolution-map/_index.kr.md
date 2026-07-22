---
type: docs
title: '17.10.11 error-resolution-map'
weight: 110
toc: true
---

이 페이지는 Machbase 사용 중 발생하는 주요 오류 상황별 원인과 해결 방법을 매핑합니다.

## 오류 해결 맵

| 오류 상황 | 오류 내용 | 즉시 조치 | 참조 문서 |
|-----------|-----------|-----------|-----------|
| 서버 접속 불가 | `Connection refused` | `machadmin -c`로 서버 상태 확인 → 미기동 시 `machadmin -u`로 시작 | [서버 시작 문제](/dbms/troubleshooting/server-connection/#start-server) |
| 인증 실패 | `Authentication failed` | 비밀번호 또는 AUTH KEY 파일 경로/권한 확인 | [인증 실패](/dbms/troubleshooting/server-connection/#failure-authentication) |
| 권한 없음 | `Insufficient privilege (ERR-02186)` | `GRANT privilege ON object TO user` 실행 | [GRANT/REVOKE](/dbms/security-access-control/privileges/#grant-revoke) |
| 테이블 미존재 | `Table not found (ERR-02058)` | `SELECT name FROM m$sys_tables` 로 테이블명 확인 후 `CREATE TABLE` | [DDL 문법](../../../reference/sql/syntax-dictionary-sql/ddl-syntax/) |
| PK 중복 | `Duplicate key (ERR-01003)` | LOOKUP 테이블: `UPDATE` 또는 입력 데이터 중복 확인 | [DML 문법](../../../reference/sql/syntax-dictionary-sql/dml-syntax/) |
| 디스크 부족 | `Disk full (ERR-00303)` | `df -h` 및 `v$tablespace` 확인 후 불필요 파일 정리 | [메모리/디스크 문제](/dbms/troubleshooting/performance/#memory-out-of) |
| CSV 입력 실패 | `Type mismatch` / `parse error` | machloader 옵션 확인: `-E`(에러 허용), `-D`(구분자), `-f`(날짜 형식) | [CSV import 실패](/dbms/troubleshooting/item/#failure-csv-import) |
| ROLLUP 결과 이상 | 집계값이 예상과 다름 | `ALTER SYSTEM FLUSH ROLLUP` 실행 후 재확인, `v$rollup` status 점검 | [ROLLUP 문제](/dbms/tag-rollup-usage/overview-use-criteria/#rollup) |
| STREAM 멈춤 | `v$streams` 상태가 STOPPED | `EXEC STREAM_START('stream_name')` 실행, 로그에서 원인 확인 | [STREAM 문제](/dbms/troubleshooting/automation/#execution-stream) |
| Cluster 노드 이상 | 노드 상태 DISCONNECTED | `machclusterctl status`로 상태 확인 후 해당 노드 재시작 | [Cluster 노드 이상](/dbms/troubleshooting/cluster/#node-state-status-abnormal-cluster) |

## SDK / 드라이버 오류

| 오류 상황 | 오류 내용 | 원인 | 조치 |
|-----------|-----------|------|------|
| Go `Begin()` 호출 실패 | `not supported` 또는 panic | Go 드라이버에 Transaction 미구현 | Transaction 제거 또는 JDBC/ODBC 사용 |
| Python `?` 플레이스홀더 오류 | `Syntax error` / 바인딩 실패 | machbaseAPI는 `%s` 방식만 지원 | `?` → `%s` 또는 `%(name)s` 로 변경 |
| 활성 TRANSACTION 테이블 트랜잭션 안의 TAG 쓰기 실패 | `not supported` | TRANSACTION 테이블 트랜잭션에 비 TRANSACTION 쓰기를 포함함 | TRANSACTION 테이블 트랜잭션 종료 후 TAG 쓰기 실행 |
| Append 후 데이터 미반영 | 즉시 SELECT 결과 없음 | Append 버퍼 미플러시 | `executeAppendClose()` / `flush()` 호출 확인 |
| REST API HTTPS 오류 | `SSL certificate error` | 인증서 미설정 또는 자체 서명 인증서 | `-k` 옵션(curl) 또는 인증서 등록 |

## 오류 코드 빠른 참조

| 오류 코드 | 의미 |
|-----------|------|
| ERR-00303 | 디스크 공간 부족 |
| ERR-01003 | PK 중복 (Duplicate key) |
| ERR-02058 | 테이블 미존재 (Table not found) |
| ERR-02186 | 권한 없음 (Insufficient privilege) |

전체 오류 코드 목록: [에러 코드 사전](../../../reference/error-dictionary-codes/)

## 로그 파일 위치

| 로그 | 경로 |
|------|------|
| 서버 메인 로그 | `$MACHBASE_HOME/trc/machbase.trc` |
| Cluster Broker 로그 | `$MACHBASE_HOME/trc/broker.trc` |
| machloader 오류 로그 | 실행 시 `-l` 옵션으로 지정한 경로 |

## 참조

- 운영 모니터링 쿼리: [operations-checklist](../operations-checklist/)
- 문제 해결 전체: [Troubleshooting](../../../troubleshooting/)
