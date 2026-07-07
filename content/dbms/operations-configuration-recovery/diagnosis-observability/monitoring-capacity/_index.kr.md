---
type: docs
title: '모니터링과 용량 관리'
weight: 40
---

Machbase 서버를 안정적으로 운영하려면 주기적으로 서버 상태, 세션, 디스크, 메모리를 점검해야 합니다. 문제가 발생하기 전에 징후를 발견하는 것이 장애 예방의 핵심입니다.

## 정기 점검 항목

| 점검 항목 | 권장 주기 | 주요 확인 내용 |
|---------|---------|--------------|
| 서버 상태 | 매일 | 프로세스 실행 여부, 버전, 포트 |
| 세션 | 매일 | 접속 세션 수, 장시간 실행 쿼리 |
| 디스크 사용량 | 매일 | 데이터 디렉터리 사용률, 여유 공간 |
| 메모리 사용량 | 매일 | 시스템 메모리 여유, 프로세스 RSS |
| 백업 완료 여부 | 매일 (백업 실행 후) | 백업 성공 로그, 파일 존재 여부 |
| 장애 징후 | 이상 발생 시 | 오류 로그, 느린 쿼리, 연결 실패 |

## 빠른 점검 SQL

아래 쿼리는 서버에 접속 후 즉시 실행하여 주요 상태를 한눈에 확인합니다.

```sql
-- 서버 버전 확인
SELECT binary_signature FROM v$version;

-- 서버 설정 포트 확인
SELECT name, value FROM v$property WHERE name = 'PORT_NO';

-- 현재 접속 세션 수
SELECT count(*) AS session_count FROM v$session WHERE closed = 0;

-- 디스크 사용량 요약
SELECT used_ratio, ratio_cap FROM v$storage_usage;

-- 실행 중인 쿼리
SELECT sess_id, state, query
  FROM v$stmt
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%'
    OR state LIKE 'Append in progress%';
```

## 이 섹션의 구성

- [서버 상태 확인](./status-check-state-server/) — 서버 프로세스 상태, 버전, 포트 확인
- [세션과 실행 쿼리 확인](./execution-session/) — 접속 세션 목록, 실행 중인 쿼리, 세션 강제 종료
- [디스크 사용량 확인](./capacity-disk/) — 테이블별 디스크 사용량, OS 레벨 디스크 확인
- [메모리 사용량 확인](./memory-capacity/) — 프로세스 메모리, Result Cache 상태
- [백업 검증](./validation-backup/) — 백업 완료 후 무결성 검증 절차
- [장애 징후 확인](./failure/) — 디스크 풀, OOM, 느린 쿼리 등 장애 징후와 즉각 조치
