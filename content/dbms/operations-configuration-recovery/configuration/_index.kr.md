---
type: docs
title: '13.2 설정 운영'
weight: 20
toc: true
---
Machbase의 설정 파일 구조와 주요 파라미터를 다룹니다. 환경에 맞게 조정하면 성능과 안정성을 크게 향상시킬 수 있습니다.

## 설정 파일 개요

Machbase의 모든 설정은 `$MACHBASE_HOME/conf/machbase.conf` 파일에서 관리합니다. 이 파일은 키-값 쌍으로 구성되며, 서버 시작 시 읽혀 적용됩니다.

일부 설정은 서버를 재시작해야만 적용되고, 일부는 `ALTER SYSTEM SET` 명령어로 서버 실행 중에 즉시 변경할 수 있습니다. 변경 가능 여부는 각 파라미터 설명에서 확인합니다.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [설정 파일 위치와 적용 절차](/dbms/operations-configuration-recovery/configuration/#file-config-configuration) | machbase.conf 구조, 변경 후 재시작 절차, 백업 방법 |
| [Runtime 변경 가능 설정과 재시작 필요 설정](/dbms/operations-configuration-recovery/configuration/#alter-start-restart-configuration-runtime) | ALTER SYSTEM SET 사용법, 런타임 변경 가능 파라미터 목록 |
| [주요 설정 파라미터](/dbms/operations-configuration-recovery/configuration/#parameters-configuration) | 파라미터 전체 요약표 (기본값, 재시작 필요 여부, 설명) |
| [메모리 설정](/dbms/operations-configuration-recovery/configuration/#memory-configuration) | PROCESS_MAX_SIZE, RS_CACHE 메모리 튜닝 |
| [세션과 네트워크 설정](/dbms/operations-configuration-recovery/configuration/#network-session-configuration) | PORT_NO, MAX_SESSION_COUNT, 타임아웃 설정 |
| [스토리지와 체크포인트 설정](/dbms/operations-configuration-recovery/configuration/#storage-checkpoint-configuration) | 데이터 경로, 체크포인트 주기, Direct I/O |
| [타임존](/dbms/operations-configuration-recovery/configuration/#timezone) | 서버·클라이언트 타임존, machsql/machloader/REST API 설정 |


<a id="file-config-configuration"></a>

## 설정 파일 위치와 적용 절차

### 설정 파일 위치

Machbase의 설정 파일은 다음 경로에 있습니다.

```
$MACHBASE_HOME/conf/machbase.conf
```

서버를 시작할 때 이 파일을 읽어 모든 파라미터를 초기화합니다. 파일이 없으면 내장된 기본값으로 동작합니다.

### 설정 파일 구조

`machbase.conf`는 `파라미터명 = 값` 형식으로 구성됩니다. `#`으로 시작하는 줄은 주석으로 처리됩니다.

```ini
# 네트워크 포트 설정
PORT_NO = 5656

# 최대 세션 수
MAX_SESSION_COUNT = 4096

# 프로세스 최대 메모리 (8GB)
PROCESS_MAX_SIZE = 8589934592

# 데이터 저장 경로 ('?'는 $MACHBASE_HOME을 의미)
DBS_PATH = ?/dbs

# 체크포인트 주기 (초)
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 120
```

### 설정 변경 절차

설정을 변경하는 방법은 파라미터의 종류에 따라 다릅니다.

#### 재시작이 필요한 설정

포트 번호, 데이터 경로, 일부 버퍼 크기처럼 서버 초기화 시에만 적용되는 설정은 파일을 수정한 뒤 서버를 재시작해야 합니다.

```bash
# 1. 설정 파일 수정
vi $MACHBASE_HOME/conf/machbase.conf

# 2. 서버 재시작
machadmin -s
machadmin -u
```

#### 런타임 즉시 적용 설정

`MAX_SESSION_COUNT`, `PROCESS_MAX_SIZE`, `PVO_CACHE_ENABLE` 등 일부 파라미터는 `ALTER SYSTEM SET` 명령어로 서버를 재시작하지 않고 즉시 변경할 수 있습니다. Result Cache의 `RS_CACHE_*` 전역 기본값은 설정 파일을 수정하고 재시작하여 적용하며, 현재 세션의 Result Cache 동작은 `ALTER SESSION SET RS_CACHE_ENABLE = ...`처럼 세션 단위로 변경합니다. 자세한 내용은 [Runtime 변경 가능 설정](/dbms/operations-configuration-recovery/configuration/#alter-start-restart-configuration-runtime)을 참고합니다.

### 설정 파일 백업

설정 파일을 변경하기 전에 현재 파일을 백업해 두는 것을 권장합니다.

```bash
cp $MACHBASE_HOME/conf/machbase.conf \
   $MACHBASE_HOME/conf/machbase.conf.bak.$(date +%Y%m%d)
```

운영 환경에서는 설정 변경 이력을 Git 등 버전 관리 시스템으로 관리하면 변경 추적과 롤백이 용이합니다.

### 현재 설정값 확인

서버 실행 중에는 `v$property` 뷰로 현재 적용된 설정값을 확인할 수 있습니다.

```sql
-- 전체 설정 조회
SELECT name, value FROM v$property ORDER BY name;

-- 특정 파라미터 조회
SELECT name, value FROM v$property WHERE name = 'PORT_NO';

-- 키워드로 검색
SELECT name, value FROM v$property WHERE name LIKE 'RS_CACHE%';
```

<a id="alter-start-restart-configuration-runtime"></a>

## Runtime 변경 가능 설정과 재시작 필요 설정

Machbase의 설정 파라미터는 적용 시점에 따라 두 가지로 나뉩니다.

- **런타임 변경 가능**: 서버 실행 중 `ALTER SYSTEM SET`으로 즉시 적용
- **재시작 필요**: `machbase.conf` 수정 후 서버 재시작 시에만 적용

### ALTER SYSTEM SET 사용법

```sql
ALTER SYSTEM SET 파라미터명 = 값;
```

변경한 값은 서버 재시작 전까지 메모리에만 적용됩니다. 재시작 후에도 유지하려면 `machbase.conf`도 함께 수정해야 합니다.

#### 설정 변경 예시

```sql
-- 최대 세션 수 변경
ALTER SYSTEM SET MAX_SESSION_COUNT = 2048;

-- PVO Statement Cache 비활성화
ALTER SYSTEM SET PVO_CACHE_ENABLE = 0;
```

#### 설정 확인

변경한 값이 올바르게 적용되었는지 `v$property`로 확인합니다.

```sql
-- 특정 파라미터 확인
SELECT name, value FROM v$property WHERE name = 'MAX_SESSION_COUNT';
```

### 런타임 변경 가능 파라미터

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

### 재시작이 필요한 파라미터

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

### 변경 사항을 영구 반영하는 절차

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

<a id="parameters-configuration"></a>

## 주요 설정 파라미터

이 페이지는 Machbase 운영에서 자주 사용하는 주요 파라미터를 범주별로 정리합니다. 전체 파라미터 목록과 상세 설명은 `v$property` 뷰를 조회하거나 각 세부 설정 페이지를 참고합니다.

현재 적용된 설정값은 다음 SQL로 확인합니다.

```sql
SELECT name, value, type FROM v$property ORDER BY name;
```

### 네트워크 및 접속

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `PORT_NO` | 5656 | 예 | 클라이언트 연결 TCP 포트 |
| `HTTP_PORT_NO` | 5657 | 예 | REST API HTTP 포트 |
| `HTTP_ENABLE` | 1 | 예 | REST API 서비스 사용 여부 |
| `GRANT_REMOTE_ACCESS` | 1 | 예 | 원격 접속 허용 (0: 로컬 전용) |
| `BIND_IP_ADDRESS` | 0.0.0.0 | 예 | 리스너 바인드 IP 주소 |

### 세션 및 쿼리

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `MAX_SESSION_COUNT` | 4096 | 아니오 | 최대 동시 세션 수 |
| `MAX_STMT_COUNT_PER_SESSION` | 1024 | 예 | 세션당 최대 Statement 수 |
| `SESSION_IDLE_TIMEOUT_SEC` | 0 | 아니오 | 세션 유휴 타임아웃 (0: 무제한) |
| `SESSION_QUERY_TIMEOUT_SEC` | 0 | 예 | 쿼리 실행 타임아웃 기본값 (0: 무제한) |
| `MAX_QPX_MEM` | 1GB | 예 | 쿼리 실행기 최대 메모리 (GROUP BY, ORDER BY 등) |

### 메모리

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `PROCESS_MAX_SIZE` | 8GB | 아니오 | 서버 프로세스 최대 메모리 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE` | 8GB | 예 | 로그 테이블 최대 메모리 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE` | 100MB | 예 | 시작 시 사전 확보 메모리 |
| `VOLATILE_TABLESPACE_MEMORY_MAX_SIZE` | 2GB | 예 | Volatile·Lookup 테이블 총 메모리 한도 |

### Result Cache (RS_CACHE)

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `RS_CACHE_ENABLE` | 1 | 예 | Result Cache 전역 기본 활성화 여부 |
| `RS_CACHE_TIME_BOUND_MSEC` | 1000 | 예 | 캐시 저장 기준 실행 시간 (밀리초) |
| `RS_CACHE_MAX_MEMORY_SIZE` | 512MB | 예 | Result Cache 최대 메모리 |
| `RS_CACHE_MAX_MEMORY_PER_QUERY` | 16MB | 예 | 쿼리당 캐시 최대 메모리 |
| `RS_CACHE_MAX_RECORD_PER_QUERY` | 10000 | 예 | 쿼리당 캐시 최대 레코드 수 |
| `RS_CACHE_APPROXIMATE_RESULT_ENABLE` | 0 | 예 | 근사값 모드 (1: 빠르지만 부정확할 수 있음) |

### 스토리지

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `DBS_PATH` | `?/dbs` | 예 | 데이터베이스 파일 저장 경로 |
| `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC` | 120 | 예 | 테이블 체크포인트 주기 (초) |
| `DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC` | 120 | 예 | 인덱스 체크포인트 주기 (초) |
| `DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC` | 3 | 예 | 파티션 flush 주기 (초) |
| `DISK_TABLESPACE_DIRECT_IO_WRITE` | 1 | 예 | 쓰기 Direct I/O 사용 여부 |
| `DISK_TABLESPACE_DIRECT_IO_READ` | 0 | 예 | 읽기 Direct I/O 사용 여부 |

### CPU 및 스레드

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `CPU_COUNT` | 1 | 예 | 사용 CPU 수 (0: 전체) |
| `CPU_PARALLEL` | 1 | 예 | CPU당 병렬 스레드 수 |
| `DISK_IO_THREAD_COUNT` | 3 | 예 | 디스크 I/O 스레드 수 |
| `INDEX_BUILD_THREAD_COUNT` | 3 | 예 | 인덱스 빌드 스레드 수 |
| `QUERY_PARALLEL_FACTOR` | 0 | 예 | 병렬 쿼리 실행 스레드 수 |

### 로그 및 진단

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `TRACE_LOGFILE_PATH` | `?/trc` | 예 | 트레이스 로그 파일 경로 |
| `TRACE_LOGFILE_SIZE` | 10MB | 예 | 로그 파일 최대 크기 |
| `TRACE_LOGFILE_COUNT` | 1000 | 예 | 최대 로그 파일 수 |
| `TRACE_LOG_LEVEL` | 277 | 아니오 | 로그 상세 수준 (모듈별 비트 조합) |
| `DUMP_APPEND_ERROR` | 0 | 아니오 | Append 오류 trc 기록 여부 |

### Tag 테이블

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `TAG_CACHE_ENABLE` | 31 | 예 | Tag 캐시 사용 범위 (비트 OR) |
| `TAG_CACHE_MAX_MEMORY_SIZE` | 512MB | 아니오 | Tag 캐시 풀당 최대 메모리 |
| `TAG_PARTITION_COUNT` | 4 | 예 | Tag 테이블 파티션 수 |
| `TAG_DATA_PART_SIZE` | 16MB | 예 | Tag 데이터 파티션 크기 |
| `TAGDATA_AUTO_META_INSERT` | 2 | 예 | 미등록 TAG_NAME 자동 삽입 동작 |

<a id="memory-configuration"></a>

## 메모리 설정

Machbase의 메모리 설정은 서버 전체 프로세스 한도, 로그 테이블 버퍼, Result Cache, Volatile 테이블 등 여러 레이어로 구성됩니다. 각 설정값을 시스템 RAM에 맞게 적절히 조정하면 성능과 안정성을 모두 높일 수 있습니다.

### 프로세스 최대 메모리

#### PROCESS_MAX_SIZE

`machbased` 프로세스 전체가 사용할 수 있는 최대 메모리 크기입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 8GB (8,589,934,592 bytes) |
| 최솟값 | 32MB |
| 재시작 필요 | 아니오 |

이 한도를 초과하면 서버는 데이터 입력을 중단하거나 오류로 처리하고, 인덱스 빌드 속도를 낮춰 메모리 사용량을 줄이려 시도합니다. 성능이 크게 저하되므로, 메모리 사용 원인을 파악하고 충분한 값으로 설정합니다.

```ini
# machbase.conf
PROCESS_MAX_SIZE = 17179869184   # 16GB
```

```sql
-- 런타임 변경
ALTER SYSTEM SET PROCESS_MAX_SIZE = 17179869184;
```

**설정 기준**: 운영 체제와 함께 실행하는 프로세스의 예약분을 제외하고, 입력 버퍼·캐시·인덱스
빌드·쿼리 처리의 최대 사용량을 합산하여 설정합니다. 변경 전후의 프로세스 RSS, swap과 OOM
로그를 확인합니다.

### 로그 테이블 버퍼 메모리

#### DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE

로그(컬럼형) 테이블의 데이터 입력 버퍼가 사용할 수 있는 최대 메모리입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 8GB |
| 최솟값 | 256MB |
| 재시작 필요 | 예 |

이 값을 초과하면 메모리가 여유 공간 이하로 줄어들 때까지 데이터 입력이 대기하여 성능이 저하됩니다.

```ini
# machbase.conf
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE = 8589934592   # 8GB
```

**설정 기준**: `PROCESS_MAX_SIZE`와 다른 캐시 상한 안에서 입력 대기와 프로세스 RSS를 함께
관찰하며 단계적으로 조정합니다. 물리 메모리만을 기준으로 고정 비율을 적용하지 않습니다.

#### DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE

서버 시작 시 미리 확보해 두는 메모리 크기입니다. 초기 데이터 입력 시 메모리 할당으로 인한 성능 저하를 방지합니다.

| 항목 | 값 |
|------|----|
| 기본값 | 100MB |
| 재시작 필요 | 예 |

메모리가 충분한 환경에서만 활성화를 권장합니다.

### Result Cache 메모리

Result Cache는 반복 실행되는 쿼리의 결과를 메모리에 저장하여 응답 시간을 단축합니다.

#### RS_CACHE_MAX_MEMORY_SIZE

Result Cache 전체가 사용할 수 있는 최대 메모리입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 512MB |
| 재시작 필요 | 예 |

```ini
# machbase.conf
RS_CACHE_MAX_MEMORY_SIZE = 1073741824   # 1GB
```

#### RS_CACHE_MAX_MEMORY_PER_QUERY

단일 쿼리의 결과를 캐시할 때 허용하는 최대 메모리입니다. 이 값을 초과하는 결과는 캐시에 저장되지 않습니다.

| 항목 | 값 |
|------|----|
| 기본값 | 16MB |
| 재시작 필요 | 예 |

```ini
# machbase.conf
RS_CACHE_MAX_MEMORY_PER_QUERY = 33554432   # 32MB
```

#### RS_CACHE_MAX_RECORD_PER_QUERY

단일 쿼리 결과의 최대 레코드 수입니다. 이 수를 초과하는 결과는 캐시에 저장되지 않습니다.

| 항목 | 값 |
|------|----|
| 기본값 | 10,000 (배포 설정 파일에서는 50,000으로 설정될 수 있음) |
| 재시작 필요 | 예 |

```ini
# machbase.conf
RS_CACHE_MAX_RECORD_PER_QUERY = 50000
```

### Volatile·Lookup 테이블 메모리

#### VOLATILE_TABLESPACE_MEMORY_MAX_SIZE

시스템 전체의 Volatile 테이블과 Lookup 테이블이 사용할 수 있는 총 메모리 한도입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 2GB |
| 재시작 필요 | 예 |

### 메모리 설정 권장 가이드

서버의 RAM 크기에 따른 주요 파라미터 권장값 예시입니다.

| RAM | `PROCESS_MAX_SIZE` | `DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE` | `RS_CACHE_MAX_MEMORY_SIZE` |
|-----|--------------------|--------------------------------------------|---------------------------|
| 16GB | 10GB | 8GB | 512MB |
| 32GB | 22GB | 16GB | 1GB |
| 64GB | 44GB | 32GB | 2GB |
| 128GB | 90GB | 64GB | 4GB |

> **참고**: 위 값은 Machbase 단독 운영 시의 예시입니다. 동일 서버에 다른 서비스가 함께 운영되는 경우 그에 맞게 조정합니다.

### 현재 메모리 사용 확인

```sql
-- 서버 메모리 사용 현황
SELECT * FROM v$sysstat WHERE name LIKE '%memory%' OR name LIKE '%mem%';

-- Result Cache 상태
SELECT name, value FROM v$property WHERE name LIKE 'RS_CACHE%';
```

<a id="network-session-configuration"></a>

## 세션과 네트워크 설정

클라이언트 연결 포트, 최대 세션 수, 타임아웃 등 네트워크와 세션에 관련된 설정을 설명합니다.

### 포트 설정

#### PORT_NO

클라이언트가 Machbase 서버에 연결하는 TCP 포트 번호입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 5656 |
| 범위 | 1024 ~ 65535 |
| 재시작 필요 | 예 |

```ini
# machbase.conf
PORT_NO = 5656
```

#### HTTP_PORT_NO

REST API 서비스가 사용하는 HTTP 포트 번호입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 5657 |
| 범위 | 1024 ~ 65535 |
| 재시작 필요 | 예 |

```ini
# machbase.conf
HTTP_PORT_NO = 5657
HTTP_ENABLE  = 1   # REST API 활성화 (0: 비활성)
```

#### BIND_IP_ADDRESS

리스너가 바인드할 IP 주소를 지정합니다. `0.0.0.0`은 모든 네트워크 인터페이스를 의미합니다.

| 항목 | 값 |
|------|----|
| 기본값 | 0.0.0.0 |
| 재시작 필요 | 예 |

특정 네트워크 인터페이스로만 접속을 허용하려면 해당 IP를 지정합니다.

```ini
# machbase.conf — 특정 IP만 허용
BIND_IP_ADDRESS = 192.168.1.100
```

#### GRANT_REMOTE_ACCESS

원격지에서 데이터베이스에 접근할 수 있는지를 결정합니다. 0으로 설정하면 루프백(127.0.0.1)에서만 접속이 가능합니다.

| 항목 | 값 |
|------|----|
| 기본값 | 1 (허용) |
| 재시작 필요 | 예 |

### 세션 수 설정

#### MAX_SESSION_COUNT

동시에 연결할 수 있는 세션의 최대 수입니다. 이 한도를 초과하면 신규 연결이 거부됩니다.

| 항목 | 값 |
|------|----|
| 기본값 | 4096 |
| 최솟값 | 64 |
| 재시작 필요 | 아니오 |

```sql
-- 런타임 변경
ALTER SYSTEM SET MAX_SESSION_COUNT = 2048;
```

#### MAX_STMT_COUNT_PER_SESSION

세션 하나가 생성할 수 있는 Statement(PreparedStatement 포함)의 최대 수입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 1024 |
| 최솟값 | 512 |
| 재시작 필요 | 예 |

### 타임아웃 설정

#### SESSION_IDLE_TIMEOUT_SEC

세션이 아무 작업도 하지 않을 때 연결을 자동으로 종료하는 시간(초)입니다. 0으로 설정하면 타임아웃이 없습니다.

| 항목 | 값 |
|------|----|
| 기본값 | 0 (무제한) |
| 재시작 필요 | 아니오 |

```sql
-- 30분 유휴 시 세션 종료
ALTER SYSTEM SET SESSION_IDLE_TIMEOUT_SEC = 1800;
```

#### SESSION_QUERY_TIMEOUT_SEC

단일 쿼리의 최대 실행 시간(초)입니다. 이 시간을 초과하면 쿼리가 자동으로 취소됩니다. 0으로 설정하면 타임아웃이 없습니다.

| 항목 | 값 |
|------|----|
| 기본값 | 0 (무제한) |
| 재시작 필요 | 예 |

```sql
-- 현재 세션의 쿼리 타임아웃 60초 설정
ALTER SESSION SET SESSION_QUERY_TIMEOUT = 60;
```

### 현재 세션 확인

`v$session` 뷰로 현재 연결된 세션 목록과 상태를 확인합니다.

```sql
-- 전체 세션 목록
SELECT * FROM v$session;

-- 현재 세션 수
SELECT COUNT(*) FROM v$session;

-- 활성 쿼리가 있는 세션
SELECT s.id AS session_id, s.user_name, st.query, st.state
  FROM v$session s
  JOIN v$stmt st ON s.id = st.sess_id
 WHERE st.state LIKE 'Execute in progress%'
    OR st.state LIKE 'Fetch in progress%'
    OR st.state LIKE 'Append in progress%';
```

### 설정 확인

```sql
-- 세션·네트워크 관련 파라미터 전체 확인
SELECT name, value
  FROM v$property
 WHERE name IN (
   'PORT_NO', 'HTTP_PORT_NO', 'MAX_SESSION_COUNT',
   'SESSION_IDLE_TIMEOUT_SEC', 'SESSION_QUERY_TIMEOUT_SEC',
   'GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS'
 )
 ORDER BY name;
```

<a id="storage-checkpoint-configuration"></a>

## 스토리지와 체크포인트 설정

데이터 저장 경로, 디스크 I/O 방식, 체크포인트 주기를 올바르게 설정하면 데이터 안전성과 쓰기 성능을 균형 있게 유지할 수 있습니다.

### 데이터 저장 경로

#### DBS_PATH

Machbase 데이터베이스 파일이 저장되는 기본 경로입니다. `?`는 `$MACHBASE_HOME`을 의미합니다.

| 항목 | 값 |
|------|----|
| 기본값 | `?/dbs` |
| 재시작 필요 | 예 |

```ini
# machbase.conf
DBS_PATH = ?/dbs
```

별도 디스크나 볼륨을 사용하려면 절대 경로로 지정합니다.

```ini
# SSD 별도 마운트 경로 지정 예시
DBS_PATH = /data/machbase/dbs
```

경로를 변경한 뒤에는 기존 데이터를 새 경로로 이동하고 서버를 재시작해야 합니다.

### 체크포인트 설정

체크포인트는 메모리에 있는 변경 데이터를 디스크에 주기적으로 기록하는 작업입니다. 주기가 짧으면 I/O 부하가 증가하고, 너무 길면 재시작 시 복구 시간이 길어집니다.

#### DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC

로그(컬럼형) 테이블의 체크포인트 주기입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 120초 |
| 최솟값 | 1초 |
| 재시작 필요 | 예 |

```ini
# machbase.conf
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 120
```

#### DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC

인덱스의 체크포인트 주기입니다. 너무 길게 설정하면 인덱스 빌드 오류가 발생할 수 있습니다.

| 항목 | 값 |
|------|----|
| 기본값 | 120초 |
| 최솟값 | 1초 |
| 재시작 필요 | 예 |

#### DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC

컬럼 파티션 파일을 디스크에 기록하는 최소 주기입니다. 파티션이 가득 차면 이 주기와 관계없이 즉시 기록됩니다.

| 항목 | 값 |
|------|----|
| 기본값 | 3초 |
| 최솟값 | 0초 |
| 재시작 필요 | 예 |

```ini
# machbase.conf
DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC = 3
```

### Direct I/O 설정

Direct I/O를 사용하면 OS 페이지 캐시를 거치지 않고 디스크에 직접 쓰므로 쓰기 지연 예측이 가능해지고 메모리 효율이 높아집니다.

#### DISK_TABLESPACE_DIRECT_IO_WRITE

데이터 쓰기 연산에 Direct I/O를 사용할지 여부입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 1 (사용) |
| 재시작 필요 | 예 |

> **주의**: ZFS처럼 Direct I/O를 지원하지 않는 파일 시스템을 사용한다면 0으로 설정합니다.

```ini
# machbase.conf
DISK_TABLESPACE_DIRECT_IO_WRITE = 1
```

#### DISK_TABLESPACE_DIRECT_IO_READ

데이터 읽기 연산에 Direct I/O를 사용할지 여부입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 0 (미사용) |
| 재시작 필요 | 예 |

#### DISK_TABLESPACE_DIRECT_IO_FSYNC

Direct I/O 사용 시 fsync 수행 여부입니다. Direct I/O 환경에서는 fsync 없이도 일반적으로 데이터 유실이 없으나, 전원 차단이 발생할 수 있는 환경이라면 1로 설정합니다.

| 항목 | 값 |
|------|----|
| 기본값 | 0 (fsync 미사용) |
| 재시작 필요 | 예 |

#### DISK_TABLESPACE_SYNCHRONOUS

디스크 테이블스페이스 파일의 동기화 정책입니다.

| 값 | 모드 | 설명 |
|----|------|------|
| 0 | OFF | 동기화하지 않음 |
| 1 | NORMAL | 더블라이트 파일 쓰기와 백업 시 동기화 (기본값) |
| 2 | FULL | NORMAL 포함, 디스크 파일 close 및 end RID 조정 시 동기화 |
| 3 | EXTRA | FULL 포함, 모든 write마다 동기화 |

### 디스크 I/O 스레드

#### DISK_IO_THREAD_COUNT

데이터를 디스크에 기록하는 I/O 전담 스레드 수입니다. 스토리지의 병렬 처리 성능에 맞게 조정합니다.

| 항목 | 값 |
|------|----|
| 기본값 | 3 |
| 최솟값 | 1 |
| 재시작 필요 | 예 |

### 설정 최적화 가이드

| 환경 | 권장 설정 |
|------|-----------|
| SSD (NVMe) | `DISK_TABLESPACE_DIRECT_IO_WRITE=1`, `DISK_IO_THREAD_COUNT=4~8` |
| HDD | `DISK_TABLESPACE_DIRECT_IO_WRITE=0`, `DISK_IO_THREAD_COUNT=2~4` |
| 고가용성 요구 | `DISK_TABLESPACE_SYNCHRONOUS=2`, 체크포인트 주기 60~120초 |
| 고처리량 요구 | `DISK_TABLESPACE_SYNCHRONOUS=0 또는 1`, 체크포인트 주기 120~300초 |
| ZFS 파일 시스템 | `DISK_TABLESPACE_DIRECT_IO_WRITE=0` |

### 현재 설정 확인

```sql
SELECT name, value
  FROM v$property
 WHERE name LIKE 'DISK_%'
    OR name = 'DBS_PATH'
 ORDER BY name;
```

<a id="timezone"></a>

## 타임존

Machbase는 모든 시각(DATETIME) 값을 내부적으로 **UTC 나노초** 단위로 저장합니다. 클라이언트가 데이터를 읽거나 쓸 때, 세션에 설정된 타임존에 따라 변환이 이루어집니다.

### 타임존 동작 원리

Machbase의 타임존은 세 가지 레이어로 구분됩니다.

| 레이어 | 적용 범위 | 설정 방법 |
|--------|-----------|-----------|
| 서버 타임존 | 서버 기본값. 클라이언트가 타임존을 지정하지 않으면 이 값이 세션에 적용됨 | `machbase.conf`의 `TIMEZONE` 프로퍼티 또는 OS 기본 타임존 |
| 세션 타임존 | 개별 연결(세션)에 적용. 서버 타임존을 재정의 | 연결 문자열의 `TIMEZONE` 파라미터, machsql의 `-z` 옵션 |
| 표시 타임존 | 데이터를 출력할 때 변환하는 기준 타임존 | REST API 헤더 또는 쿼리 파라미터 |

#### 동작 규칙

1. 서버는 OS의 기본 타임존을 읽어 초기값으로 사용합니다. `machbase.conf`에서 `TIMEZONE`을 명시하면 OS 설정을 무시합니다.
2. 클라이언트가 타임존을 지정하지 않고 연결하면 서버의 타임존이 세션에 적용됩니다.
3. 클라이언트가 연결 시 타임존을 명시하면 해당 세션은 지정된 타임존으로 동작합니다.

### Machbase 타임존 형식

Machbase는 `+HHMM` 또는 `-HHMM` 형식의 5자리 오프셋을 사용합니다.

```
+0900   # UTC+9 (한국 표준시 KST)
+0000   # UTC
-0500   # UTC-5 (미국 동부 표준시 EST)
+0530   # UTC+5:30 (인도 표준시 IST)
```

### 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [서버 타임존 설정](/dbms/operations-configuration-recovery/configuration/#timezone-server-configuration) | `TIMEZONE` 프로퍼티 설정, OS 타임존과의 관계 |
| [machsql -z](/dbms/operations-configuration-recovery/configuration/#machsql-z) | machsql 세션 타임존 설정 옵션 |
| [machloader -z](/dbms/operations-configuration-recovery/configuration/#machloader-z) | CSV 데이터 로드 시 타임존 지정 |
| [CLI/JDBC/.NET TIMEZONE 연결 옵션](/dbms/operations-configuration-recovery/configuration/#connection-cli-jdbc-net-timezone) | 연결 문자열에서 타임존 지정 |
| [REST API 타임존 응답](/dbms/operations-configuration-recovery/configuration/#timezone-rest-api) | HTTP 헤더로 응답 타임존 지정 |

<a id="timezone-server-configuration"></a>
<a id="timezone-timezone-server-configuration"></a>

### 서버 타임존 설정

서버 타임존은 모든 클라이언트 세션의 기본 타임존이 됩니다. 클라이언트가 연결 시 타임존을 별도로 지정하지 않으면 서버 타임존이 세션에 자동으로 적용됩니다.

#### TIMEZONE 프로퍼티

`machbase.conf`의 `TIMEZONE` 프로퍼티로 서버 기본 타임존을 설정합니다.

```ini
# machbase.conf
TIMEZONE = +0900   # 한국 표준시 (KST)
```

| 항목 | 값 |
|------|----|
| 기본값 | 설정하지 않으면 OS의 타임존을 사용 |
| 형식 | `+HHMM` 또는 `-HHMM` (5자리 오프셋) |
| 재시작 필요 | 예 |

`TIMEZONE`을 `machbase.conf`에 명시하지 않으면 서버가 운영 체제의 기본 타임존을 읽어 사용합니다. 예측 가능한 동작을 위해 운영 환경에서는 명시적으로 설정하는 것을 권장합니다.

#### 변경 방법

1. `machbase.conf`를 편집합니다.

```bash
vi $MACHBASE_HOME/conf/machbase.conf
```

2. `TIMEZONE` 값을 원하는 오프셋으로 설정합니다.

```ini
TIMEZONE = +0000   # UTC로 변경
```

3. 서버를 재시작합니다.

```bash
machadmin -s
machadmin -u
```

#### 현재 서버 타임존 확인

서버가 실행 중일 때 `machsql`에서 다음 명령어로 현재 타임존을 확인합니다.

```sql
SHOW TIMEZONE;
```

```
Mach> show timezone;
Timezone : +0900
```

`v$property` 뷰로도 확인할 수 있습니다.

```sql
SELECT name, value FROM v$property WHERE name = 'TIMEZONE';
```

#### 주의 사항

- 서버 타임존을 변경하면 이후 연결되는 모든 세션의 기본 타임존이 바뀝니다. 기존 데이터는 UTC로 저장되어 있으므로 데이터 자체는 변경되지 않고, 표시되는 시각만 달라집니다.
- 클러스터 환경에서는 모든 노드의 타임존을 동일하게 설정해야 합니다.
- 타임존이 다른 클라이언트가 혼재하는 환경에서는 서버를 UTC(`+0000`)로 설정하고 각 클라이언트에서 세션 타임존을 지정하는 방식이 혼선을 줄이는 데 효과적입니다.

<a id="machsql-z"></a>
<a id="timezone-machsql-z"></a>

### machsql -z

`machsql`은 `-z` 옵션으로 세션 타임존을 지정할 수 있습니다. 이 옵션을 사용하면 해당 세션에서 조회하는 DATETIME 값이 지정된 타임존 기준으로 변환되어 표시됩니다.

#### 사용법

```bash
machsql -z +-HHMM [기타 옵션]
```

##### 예시

```bash
# KST(UTC+9)로 접속
machsql -u SYS -p MANAGER -z +0900

# UTC로 접속
machsql -u SYS -p MANAGER -z +0000

# EST(UTC-5)로 접속
machsql -u SYS -p MANAGER -z -0500
```

#### 동작 방식

`-z` 옵션으로 지정한 타임존은 해당 `machsql` 세션에만 적용됩니다. 서버의 기본 타임존 설정은 변경되지 않습니다.

```
mach@localhost:~$ machsql -u SYS -p MANAGER -z +0900

Mach> show timezone;
Timezone : +0900

Mach> SELECT sysdate FROM v$tables LIMIT 1;
SYSDATE
----------------------------------
2026-07-07 10:30:00 000:000:000
```

같은 서버에 UTC로 접속하면 9시간 차이가 납니다.

```
mach@localhost:~$ machsql -u SYS -p MANAGER -z +0000

Mach> SELECT sysdate FROM v$tables LIMIT 1;
SYSDATE
----------------------------------
2026-07-07 01:30:00 000:000:000
```

#### 세션 내 타임존 확인

접속 후 현재 세션의 타임존을 확인합니다.

```sql
SHOW TIMEZONE;
```

#### 주의 사항

- `-z` 옵션을 지정하지 않으면 서버의 기본 타임존이 세션에 적용됩니다.
- 데이터가 저장될 때는 내부적으로 UTC로 변환되어 저장됩니다. `-z` 옵션은 표시와 입력 해석에만 영향을 미칩니다.
- INSERT 또는 Append로 데이터를 입력할 때 DATETIME 값도 세션 타임존을 기준으로 해석하여 UTC로 변환한 뒤 저장합니다.

<a id="machloader-z"></a>
<a id="timezone-machloader-z"></a>

### machloader -z

`machloader`는 CSV 등 텍스트 파일의 데이터를 Machbase에 대량으로 로드하거나 내보내는 도구입니다. `-z` 옵션으로 DATETIME 값의 해석 기준 타임존을 지정할 수 있습니다.

#### 사용법

```bash
machloader -z +-HHMM [기타 옵션]
```

#### 데이터 로드 시 타임존 지정

CSV 파일에 포함된 DATETIME 값을 지정한 타임존으로 해석하여 UTC로 변환한 뒤 저장합니다.

```bash
# KST(UTC+9) 기준 DATETIME이 담긴 CSV 파일을 로드
machloader -i -t sensor_data -d data.csv -z +0900
```

위 명령어는 `data.csv`의 DATETIME 컬럼 값을 KST 시각으로 간주하고, UTC로 변환하여 `sensor_data` 테이블에 저장합니다.

예를 들어 CSV 파일에 `2026-07-07 10:00:00`이 있으면, 이를 KST(+09:00)로 해석하여 UTC 기준 `2026-07-07 01:00:00`으로 변환해 저장합니다.

#### 데이터 추출 시 타임존 지정

데이터를 파일로 내보낼 때도 `-z` 옵션으로 출력 타임존을 지정합니다.

```bash
# 테이블 데이터를 KST 기준으로 CSV 파일에 내보내기
machloader -o -t sensor_data -d output.csv -z +0900
```

내보낸 CSV 파일의 DATETIME 값이 지정된 타임존 기준으로 변환되어 출력됩니다.

#### 주의 사항

- `-z` 옵션을 지정하지 않으면 서버의 기본 타임존이 적용됩니다.
- 로드와 추출 방향 모두 동일한 타임존 옵션(`-z`)을 사용합니다.
- 원본 데이터의 실제 타임존과 `-z` 옵션에 지정한 값이 일치하지 않으면 시각이 잘못 저장됩니다. CSV 파일이 어떤 타임존 기준으로 생성되었는지 먼저 확인합니다.
- 대용량 데이터를 로드할 때 타임존 변환은 성능에 거의 영향을 주지 않습니다.

<a id="connection-cli-jdbc-net-timezone"></a>
<a id="timezone-connection-cli-jdbc-net-timezone"></a>

### CLI/JDBC/.NET TIMEZONE 연결 옵션

CLI, ODBC, JDBC, .NET 드라이버를 사용하여 Machbase에 연결할 때 연결 문자열에 `TIMEZONE` 파라미터를 추가하면 해당 세션의 타임존을 지정할 수 있습니다.

#### CLI / ODBC 연결 문자열

ODBC 및 CLI 드라이버의 연결 문자열에 `TIMEZONE` 파라미터를 포함합니다.

```
SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;NLS_USE=UTF8;PORT_NO=5656;TIMEZONE=+0900
```

`TIMEZONE`을 지정하지 않으면 서버의 기본 타임존이 적용됩니다.

#### JDBC 연결 문자열

JDBC URL에서는 쿼리 파라미터 형식으로 타임존을 지정합니다.

```
jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900
```

##### Java 코드 예시

```java
String url = "jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900";
Connection conn = DriverManager.getConnection(url, "SYS", "MANAGER");
```

#### .NET 연결 문자열

.NET 드라이버도 동일한 방식으로 `TIMEZONE`을 연결 문자열에 추가합니다.

```
SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;TIMEZONE=+0900
```

#### Python (PyMachbase)

Python 드라이버에서는 `connect()` 함수의 `timezone` 파라미터로 지정합니다.

```python
import machbase_neo_connector as mach

conn = mach.connect(
    host="127.0.0.1",
    port=5656,
    user="SYS",
    password="MANAGER",
    timezone="+0900"
)
```

#### 타임존 적용 우선순위

동일한 연결에서 여러 타임존 설정이 충돌할 경우 다음 순서로 우선순위가 결정됩니다.

1. 연결 문자열의 `TIMEZONE` 파라미터 (가장 높음)
2. 서버의 `TIMEZONE` 프로퍼티 (`machbase.conf`)
3. 서버 OS의 기본 타임존 (가장 낮음)

#### 주의 사항

- 타임존은 세션 단위로 적용됩니다. 연결 풀을 사용하는 경우, 풀에서 가져온 연결의 타임존이 예상과 다를 수 있습니다. 연결 풀 초기화 시 타임존 파라미터를 명시적으로 지정하는 것을 권장합니다.
- 타임존 오프셋은 `+HHMM` 또는 `-HHMM` 형식의 5자리여야 합니다. 예: `+0900`, `-0500`.

<a id="timezone-rest-api"></a>
<a id="timezone-timezone-rest-api"></a>

### REST API 타임존 응답

Machbase REST API를 사용할 때 HTTP 요청 헤더에 타임존을 지정하면, 응답에 포함된 DATETIME 값이 해당 타임존 기준으로 변환되어 반환됩니다.

#### 요청 헤더에서 타임존 지정

`The-Timezone-Machbase` 헤더를 사용하여 응답 타임존을 지정합니다.

```
The-Timezone-Machbase: +0900
```

##### curl 예시

```bash
# KST(UTC+9) 기준으로 쿼리 결과 조회
curl -H "Authorization: Basic $(echo -n 'SYS:MANAGER' | base64)" \
     -H "The-Timezone-Machbase: +0900" \
     -G "http://127.0.0.1:5657/machbase" \
     --data-urlencode 'q=SELECT sysdate FROM v$tables LIMIT 1'
```

응답 JSON의 `timezone` 필드에 적용된 타임존 값이 반환됩니다.

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "sysdate",
      "type": 6,
      "length": 31
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "sysdate": "2026-07-07 10:30:00 000:000:000"
    }
  ]
}
```

#### UTC 기준으로 조회

```bash
# UTC 기준으로 조회
curl -H "Authorization: Basic $(echo -n 'SYS:MANAGER' | base64)" \
     -H "The-Timezone-Machbase: +0000" \
     -G "http://127.0.0.1:5657/machbase" \
     --data-urlencode 'q=SELECT sysdate FROM v$tables LIMIT 1'
```

```json
{
  "timezone": "+0000",
  "data": [
    {
      "sysdate": "2026-07-07 01:30:00 000:000:000"
    }
  ]
}
```

#### 타임존 미지정 시 동작

`The-Timezone-Machbase` 헤더를 포함하지 않으면 서버의 기본 타임존(`machbase.conf`의 `TIMEZONE` 값 또는 OS 타임존)이 적용됩니다.

#### 데이터 입력 시 타임존 적용

REST API로 데이터를 INSERT할 때도 동일한 헤더를 사용하면 DATETIME 값이 지정 타임존으로 해석되어 UTC로 변환 후 저장됩니다.

```bash
curl -X POST \
     -H "Authorization: Basic $(echo -n 'SYS:MANAGER' | base64)" \
     -H "Content-Type: application/json" \
     -H "The-Timezone-Machbase: +0900" \
     -d '{"q":"INSERT INTO sensor VALUES(TO_DATE(\"2026-07-07 10:00:00\"), 25.3)"}' \
     "http://127.0.0.1:5657/machbase"
```

위 예시에서 `2026-07-07 10:00:00`은 KST로 해석되어 UTC 기준 `2026-07-07 01:00:00`으로 저장됩니다.

#### 주의 사항

- 헤더 이름은 `The-Timezone-Machbase`이며, 대소문자를 구분하지 않는 HTTP 표준에 따라 처리됩니다.
- 오프셋 형식은 `+HHMM` 또는 `-HHMM`(5자리)이어야 합니다.
