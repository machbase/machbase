---
type: docs
title: '진단 명령어 모음'
weight: 20
---

문제 진단에 자주 사용하는 SQL과 명령을 모아두었습니다. 복사해서 바로 실행할 수 있습니다.

## 자주 쓰는 진단 SQL

### 서버 기본 정보

```sql
-- 서버 버전 확인
SELECT * FROM v$version;

-- 현재 세션 목록
SELECT sess_id, login_time, user_name, task_state FROM v$session;

-- 실행 중인 쿼리 (IDLE 제외)
SELECT sess_id, id, state, query FROM v$stmt WHERE state != 'IDLE';
```

### 스토리지

```sql
-- 디스크 사용량
SELECT * FROM v$storage_usage;

-- 테이블별 스토리지 사용량
SELECT * FROM v$storage_tables;
```

### 자동 처리 상태

```sql
-- ROLLUP 상태
SELECT * FROM v$rollup;

-- STREAM 상태
SELECT * FROM v$streams;
```

### 시스템 통계 및 설정

```sql
-- 오류 관련 통계
SELECT * FROM v$sysstat WHERE name LIKE '%ERROR%';

-- 현재 서버 설정값 조회
SELECT name, value FROM v$property WHERE name IN (
  'PORT_NO',
  'GRANT_REMOTE_ACCESS',
  'BIND_IP_ADDRESS',
  'MAX_SESSION_COUNT',
  'TRACE_LOG_LEVEL'
);

-- 메모리 사용 현황
SELECT * FROM v$sysmem;
```

### 메타 정보

```sql
-- 테이블 목록
SELECT name, type FROM m$sys_tables ORDER BY name;

-- 특정 테이블 컬럼 목록
SELECT name, type, length FROM m$sys_columns
WHERE table_name = 'MY_TABLE';

-- 사용자 목록
SELECT name FROM m$sys_users;
```

## machadmin 명령 모음

```bash
machadmin -c      # 서버 상태 확인
machadmin -s      # 서버 시작 (start)
machadmin -u      # 서버 정상 종료 (shutdown)
machadmin -k      # 서버 강제 종료 (kill)
machadmin -v      # 버전 확인
```

{{< callout type="warning" >}}
`machadmin -k`는 강제 종료 명령입니다. 정상 종료(`-u`)가 응답하지 않을 때만 사용합니다. 강제 종료 후에는 서버 재시작 시 복구 절차가 실행될 수 있습니다.
{{< /callout >}}

## 로그 파일 위치

| 파일 | 내용 |
|------|------|
| `$MACHBASE_HOME/trc/machbase.trc` | 서버 메인 로그 (오류, 경고, 운영 이벤트) |
| `$MACHBASE_HOME/trc/machsql.history` | machsql 대화형 세션의 SQL 실행 이력 |
| 실행 디렉터리의 `machloader.err` | machloader 적재 실패 레코드 |
| 실행 디렉터리의 `machloader.log` | machloader 처리 건수와 오류 통계 |
| `$MACHBASE_COLLECTOR_HOME/trc/` | Collector 수집 상태 로그 |

## 빠른 진단 순서

문제 발생 시 아래 순서대로 실행하면 대부분의 원인을 파악할 수 있습니다.

```bash
# 1. 서버 상태
machadmin -c

# 2. 최근 오류 로그
tail -50 $MACHBASE_HOME/trc/machbase.trc | grep -i "error\|warn"
```

```sql
-- 3. 세션 현황
SELECT COUNT(*) AS session_count FROM v$session;

-- 4. 실행 중인 쿼리
SELECT sess_id, id, state, query FROM v$stmt WHERE state != 'IDLE';

-- 5. 스토리지 현황
SELECT * FROM v$storage_usage;
```
