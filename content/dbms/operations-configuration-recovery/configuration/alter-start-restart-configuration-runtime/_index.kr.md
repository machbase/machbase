---
type: docs
title: '13.2.2 Runtime 변경 가능 설정과 재시작 필요 설정'
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
-- 최대 세션 수 변경
ALTER SYSTEM SET MAX_SESSION_COUNT = 2048;

-- PVO Statement Cache 비활성화
ALTER SYSTEM SET PVO_CACHE_ENABLE = 0;
```

### 설정 확인

변경한 값이 올바르게 적용되었는지 `v$property`로 확인합니다.

```sql
-- 특정 파라미터 확인
SELECT name, value FROM v$property WHERE name = 'MAX_SESSION_COUNT';
```

## 런타임 변경 가능 파라미터

다음 파라미터들은 서버 재시작 없이 즉시 변경할 수 있습니다.

| 파라미터 | 기본값 | 설명 |
|----------|--------|------|
| `MAX_SESSION_COUNT` | 4096 | 최대 동시 세션 수 |
| `PVO_CACHE_ENABLE` | 1 | PVO Statement Cache 사용 여부 |
| `PVO_CACHE_MAX_MEMORY_SIZE` | 256MB | Statement Cache 최대 메모리 |
| `PVO_CACHE_MAX_PLANS_PER_SQL` | 512 | SQL당 최대 플랜 수 |
| `PVO_CACHE_MAX_SQL_ENTRIES` | 0 (무제한) | SQL 캐시 최대 엔트리 수 |
| `DUMP_APPEND_ERROR` | 0 | Append 오류 시 trc 파일 기록 여부 |
| `PROCESS_MAX_SIZE` | 8GB | 서버 프로세스 최대 메모리 |
| `TAG_CACHE_MAX_MEMORY_SIZE` | 512MB | TAG 캐시 풀당 최대 메모리 |

## 재시작이 필요한 파라미터

다음 파라미터들은 `machbase.conf`를 수정하고 서버를 재시작해야 적용됩니다.

| 파라미터 | 기본값 | 설명 |
|----------|--------|------|
| `PORT_NO` | 5656 | 클라이언트 연결 TCP 포트 |
| `HTTP_PORT_NO` | 5657 | REST API HTTP 포트 |
| `DBS_PATH` | `?/dbs` | 데이터베이스 파일 저장 경로 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE` | 8GB | 로그 테이블 최대 메모리 |
| `CPU_COUNT` | 1 | 사용 CPU 수 |
| `DISK_IO_THREAD_COUNT` | 3 | 디스크 I/O 스레드 수 |
| `INDEX_BUILD_THREAD_COUNT` | 3 | 인덱스 빌드 스레드 수 |
| `GRANT_REMOTE_ACCESS` | 1 | 원격 접속 허용 여부 |
| `DISK_TABLESPACE_DIRECT_IO_WRITE` | 1 | 쓰기 Direct I/O 사용 여부 |
| `PVO_CACHE_SHARD_COUNT` | 16 | Statement Cache 샤드 수 |
| `RS_CACHE_*` | 항목별 상이 | Result Cache 전역 기본값 |

## 변경 사항을 영구 반영하는 절차

런타임 변경으로 테스트한 설정을 영구적으로 적용하려면 설정 파일도 함께 수정합니다.

```bash
# 1. 런타임에서 먼저 테스트
# (machsql 또는 JDBC 연결 후)
# ALTER SYSTEM SET MAX_SESSION_COUNT = 2048;

# 2. 설정 파일에 반영
vi $MACHBASE_HOME/conf/machbase.conf
# MAX_SESSION_COUNT = 2048 으로 수정

# 3. 다음 재시작 시 자동 적용됨
```
