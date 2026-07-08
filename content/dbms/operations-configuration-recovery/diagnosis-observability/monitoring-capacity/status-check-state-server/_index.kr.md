---
type: docs
title: '서버 상태 확인'
weight: 10
---

Machbase 서버의 실행 여부와 기본 상태를 확인하는 방법을 설명합니다. OS 레벨 명령과 SQL 쿼리를 함께 사용합니다.

## 서버 실행 여부 확인

### machadmin으로 확인

`machadmin -e` 명령은 서버 프로세스의 실행 상태를 간단히 확인합니다.

```bash
# 서버 상태 확인
machadmin -e

# 출력 예시 (실행 중)
Machbase server is running with PID(12345).

# 출력 예시 (중지됨)
[Error] Machbase server is not running.
```

### 프로세스 직접 확인

```bash
# Machbase 서버 프로세스 확인
pgrep -la machbased

# 포트 Listen 여부 확인 (기본 포트 5656)
ss -tlnp | grep 5656
```

## 서버 버전과 시작 시간 확인

서버에 접속한 후 `V$VERSION` 가상 테이블로 버전 정보를 조회합니다.

```sql
-- 서버 버전 정보
SELECT binary_signature, edition
  FROM v$version;

-- 주요 버전 번호만 조회
SELECT binary_db_major_version AS major,
       binary_db_minor_version AS minor,
       binary_signature        AS version_string
  FROM v$version;
```

출력 예시:

```
BINARY_SIGNATURE        EDITION
----------------------  --------
8.6.0.official-LINUX    Standard
```

## 서버 설정 확인

현재 서버에 적용된 주요 설정값을 확인합니다.

```sql
-- 포트 번호 확인
SELECT name, value
  FROM v$property
 WHERE name = 'PORT_NO';

-- 주요 설정 한 번에 확인
SELECT name, value
  FROM v$property
 WHERE name IN (
   'PORT_NO',
   'MAX_SESSION_COUNT',
   'TRACE_LOG_LEVEL',
   'DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC',
   'DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC'
 )
 ORDER BY name;

-- 기본값과 다른 설정만 조회
SELECT name, value, deflt
  FROM v$property
 WHERE value != deflt
 ORDER BY name;
```

## HTTP 서비스 상태 확인

Machbase의 임베디드 HTTP 엔드포인트 상태를 확인합니다.

```sql
SELECT http_port,
       thread_count,
       connect_count,
       service_success_count,
       service_failure_count
  FROM v$http_status;
```

## 라이선스 유효성 확인

```sql
-- 라이선스 정보와 위반 상태 확인
SELECT id, type, customer, issue_date,
       violate_status, violate_msg
  FROM v$license_info;
```

`VIOLATE_STATUS`가 0이 아닌 경우 라이선스 정책 위반 상태입니다.

## 서버 시작/종료 이력 확인

서버 로그에서 시작/종료 이력을 확인합니다.

```bash
# 서버 시작 이력
grep 'server started\|server starting' $MACHBASE_HOME/trc/machbase.trc

# 서버 종료 이력
grep 'server stopped\|shutting down' $MACHBASE_HOME/trc/machbase.trc

# 비정상 종료 확인
grep 'SIGKILL\|Killed\|ABNORMAL' $MACHBASE_HOME/trc/machbase.trc
```

## 점검 체크리스트

| 항목 | 명령/쿼리 | 정상 상태 |
|------|----------|---------|
| 프로세스 실행 | `machadmin -e` | `running` |
| 포트 Listen | `ss -tlnp \| grep 5656` | 5656 포트 확인 |
| 버전 확인 | `SELECT * FROM v$version` | 예상 버전 일치 |
| 라이선스 | `SELECT violate_status FROM v$license_info` | 0 (정상) |
| 디스크 사용률 | `SELECT used_ratio FROM v$storage_usage` | ratio_cap 미만 |
