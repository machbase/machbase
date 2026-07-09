---
type: docs
title: '13.2.3 주요 설정 파라미터'
weight: 30
---

이 페이지는 Machbase 운영에서 자주 사용하는 주요 파라미터를 범주별로 정리합니다. 전체 파라미터 목록과 상세 설명은 `v$property` 뷰를 조회하거나 각 세부 설정 페이지를 참고합니다.

현재 적용된 설정값은 다음 SQL로 확인합니다.

```sql
SELECT name, value, type FROM v$property ORDER BY name;
```

## 네트워크 및 접속

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `PORT_NO` | 5656 | 예 | 클라이언트 연결 TCP 포트 |
| `HTTP_PORT_NO` | 5657 | 예 | REST API HTTP 포트 |
| `HTTP_ENABLE` | 1 | 예 | REST API 서비스 사용 여부 |
| `GRANT_REMOTE_ACCESS` | 1 | 예 | 원격 접속 허용 (0: 로컬 전용) |
| `BIND_IP_ADDRESS` | 0.0.0.0 | 예 | 리스너 바인드 IP 주소 |

## 세션 및 쿼리

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `MAX_SESSION_COUNT` | 4096 | 아니오 | 최대 동시 세션 수 |
| `MAX_STMT_COUNT_PER_SESSION` | 1024 | 예 | 세션당 최대 Statement 수 |
| `SESSION_IDLE_TIMEOUT_SEC` | 0 | 아니오 | 세션 유휴 타임아웃 (0: 무제한) |
| `SESSION_QUERY_TIMEOUT_SEC` | 0 | 예 | 쿼리 실행 타임아웃 기본값 (0: 무제한) |
| `MAX_QPX_MEM` | 1GB | 예 | 쿼리 실행기 최대 메모리 (GROUP BY, ORDER BY 등) |

## 메모리

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `PROCESS_MAX_SIZE` | 8GB | 아니오 | 서버 프로세스 최대 메모리 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE` | 8GB | 예 | 로그 테이블 최대 메모리 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE` | 100MB | 예 | 시작 시 사전 확보 메모리 |
| `VOLATILE_TABLESPACE_MEMORY_MAX_SIZE` | 2GB | 예 | Volatile·Lookup 테이블 총 메모리 한도 |

## Result Cache (RS_CACHE)

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `RS_CACHE_ENABLE` | 1 | 예 | Result Cache 전역 기본 활성화 여부 |
| `RS_CACHE_TIME_BOUND_MSEC` | 1000 | 예 | 캐시 저장 기준 실행 시간 (밀리초) |
| `RS_CACHE_MAX_MEMORY_SIZE` | 512MB | 예 | Result Cache 최대 메모리 |
| `RS_CACHE_MAX_MEMORY_PER_QUERY` | 16MB | 예 | 쿼리당 캐시 최대 메모리 |
| `RS_CACHE_MAX_RECORD_PER_QUERY` | 10000 | 예 | 쿼리당 캐시 최대 레코드 수 |
| `RS_CACHE_APPROXIMATE_RESULT_ENABLE` | 0 | 예 | 근사값 모드 (1: 빠르지만 부정확할 수 있음) |

## 스토리지

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `DBS_PATH` | `?/dbs` | 예 | 데이터베이스 파일 저장 경로 |
| `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC` | 120 | 예 | 테이블 체크포인트 주기 (초) |
| `DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC` | 120 | 예 | 인덱스 체크포인트 주기 (초) |
| `DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC` | 3 | 예 | 파티션 flush 주기 (초) |
| `DISK_TABLESPACE_DIRECT_IO_WRITE` | 1 | 예 | 쓰기 Direct I/O 사용 여부 |
| `DISK_TABLESPACE_DIRECT_IO_READ` | 0 | 예 | 읽기 Direct I/O 사용 여부 |

## CPU 및 스레드

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `CPU_COUNT` | 1 | 예 | 사용 CPU 수 (0: 전체) |
| `CPU_PARALLEL` | 1 | 예 | CPU당 병렬 스레드 수 |
| `DISK_IO_THREAD_COUNT` | 3 | 예 | 디스크 I/O 스레드 수 |
| `INDEX_BUILD_THREAD_COUNT` | 3 | 예 | 인덱스 빌드 스레드 수 |
| `QUERY_PARALLEL_FACTOR` | 0 | 예 | 병렬 쿼리 실행 스레드 수 |

## 로그 및 진단

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `TRACE_LOGFILE_PATH` | `?/trc` | 예 | 트레이스 로그 파일 경로 |
| `TRACE_LOGFILE_SIZE` | 10MB | 예 | 로그 파일 최대 크기 |
| `TRACE_LOGFILE_COUNT` | 1000 | 예 | 최대 로그 파일 수 |
| `TRACE_LOG_LEVEL` | 277 | 아니오 | 로그 상세 수준 (모듈별 비트 조합) |
| `DUMP_APPEND_ERROR` | 0 | 아니오 | Append 오류 trc 기록 여부 |

## Tag 테이블

| 파라미터 | 기본값 | 재시작 필요 | 설명 |
|----------|--------|-------------|------|
| `TAG_CACHE_ENABLE` | 31 | 예 | Tag 캐시 사용 범위 (비트 OR) |
| `TAG_CACHE_MAX_MEMORY_SIZE` | 512MB | 아니오 | Tag 캐시 풀당 최대 메모리 |
| `TAG_PARTITION_COUNT` | 4 | 예 | Tag 테이블 파티션 수 |
| `TAG_DATA_PART_SIZE` | 16MB | 예 | Tag 데이터 파티션 크기 |
| `TAGDATA_AUTO_META_INSERT` | 2 | 예 | 미등록 TAG_NAME 자동 삽입 동작 |
