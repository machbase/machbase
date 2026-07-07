---
type: docs
title: 'Runtime 변경 가능 설정과 재시작 필요 설정'
weight: 20
---

Machbase의 설정 파라미터는 적용 시점에 따라 두 가지로 나뉩니다.

- **런타임 변경 가능**: 서버 실행 중 `ALTER SYSTEM SET`으로 즉시 적용
- **재시작 필요**: `machbase.conf` 수정 후 서버 재시작 시에만 적용

## ALTER SYSTEM SET 사용법

```sql
ALTER SYSTEM SET 파라미터명 = 값;
```

변경한 값은 서버 재시작 전까지 메모리에만 적용됩니다. 재시작 후에도 유지하려면 `machbase.conf`도 함께 수정해야 합니다.

### 설정 변경 예시

```sql
-- Result Cache 비활성화
ALTER SYSTEM SET RS_CACHE_ENABLE = 0;

-- Result Cache 시간 기준 변경 (2초 이상 걸린 쿼리만 캐시)
ALTER SYSTEM SET RS_CACHE_TIME_BOUND_MSEC = 2000;

-- 최대 세션 수 변경
ALTER SYSTEM SET MAX_SESSION_COUNT = 2048;
```

### 설정 확인

변경한 값이 올바르게 적용되었는지 `v$property`로 확인합니다.

```sql
-- RS_CACHE 관련 설정 전체 확인
SELECT name, value FROM v$property WHERE name LIKE 'RS_CACHE%';

-- 특정 파라미터 확인
SELECT name, value FROM v$property WHERE name = 'MAX_SESSION_COUNT';
```

## 런타임 변경 가능 파라미터

다음 파라미터들은 서버 재시작 없이 즉시 변경할 수 있습니다.

| 파라미터 | 기본값 | 설명 |
|----------|--------|------|
| `RS_CACHE_ENABLE` | 1 | Result Cache 사용 여부 (0: 비활성, 1: 활성) |
| `RS_CACHE_TIME_BOUND_MSEC` | 1000 | 캐시 저장 기준 실행 시간 (밀리초) |
| `RS_CACHE_MAX_MEMORY_SIZE` | 512MB | Result Cache 최대 메모리 |
| `RS_CACHE_MAX_MEMORY_PER_QUERY` | 16MB | 쿼리당 캐시 최대 메모리 |
| `RS_CACHE_MAX_RECORD_PER_QUERY` | 10000 | 쿼리당 캐시 최대 레코드 수 |
| `MAX_SESSION_COUNT` | 4096 | 최대 동시 세션 수 |
| `PVO_CACHE_ENABLE` | 1 | PVO Statement Cache 사용 여부 |
| `PVO_CACHE_MAX_MEMORY_SIZE` | 256MB | Statement Cache 최대 메모리 |
| `PVO_CACHE_MAX_PLANS_PER_SQL` | 512 | SQL당 최대 플랜 수 |
| `PVO_CACHE_MAX_SQL_ENTRIES` | 0 (무제한) | SQL 캐시 최대 엔트리 수 |
| `DUMP_APPEND_ERROR` | 0 | Append 오류 시 trc 파일 기록 여부 |
| `FEEDBACK_APPEND_ERROR` | 1 | Append 오류 데이터 클라이언트 전송 여부 |

## 재시작이 필요한 파라미터

다음 파라미터들은 `machbase.conf`를 수정하고 서버를 재시작해야 적용됩니다.

| 파라미터 | 기본값 | 설명 |
|----------|--------|------|
| `PORT_NO` | 5656 | 클라이언트 연결 TCP 포트 |
| `HTTP_PORT_NO` | 5657 | REST API HTTP 포트 |
| `DBS_PATH` | `?/dbs` | 데이터베이스 파일 저장 경로 |
| `PROCESS_MAX_SIZE` | 8GB | 프로세스 최대 메모리 크기 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE` | 8GB | 로그 테이블 최대 메모리 |
| `CPU_COUNT` | 1 | 사용 CPU 수 |
| `DISK_IO_THREAD_COUNT` | 3 | 디스크 I/O 스레드 수 |
| `INDEX_BUILD_THREAD_COUNT` | 3 | 인덱스 빌드 스레드 수 |
| `GRANT_REMOTE_ACCESS` | 1 | 원격 접속 허용 여부 |
| `DISK_TABLESPACE_DIRECT_IO_WRITE` | 1 | 쓰기 Direct I/O 사용 여부 |
| `PVO_CACHE_SHARD_COUNT` | 16 | Statement Cache 샤드 수 |

## 변경 사항을 영구 반영하는 절차

런타임 변경으로 테스트한 설정을 영구적으로 적용하려면 설정 파일도 함께 수정합니다.

```bash
# 1. 런타임에서 먼저 테스트
# (machsql 또는 JDBC 연결 후)
# ALTER SYSTEM SET RS_CACHE_TIME_BOUND_MSEC = 2000;

# 2. 설정 파일에 반영
vi $MACHBASE_HOME/conf/machbase.conf
# RS_CACHE_TIME_BOUND_MSEC = 2000 으로 수정

# 3. 다음 재시작 시 자동 적용됨
```
