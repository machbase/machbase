---
type: docs
title: '메모리 설정 튜닝'
weight: 30
---

Machbase 서버의 안정적인 운영을 위해서는 캐시, 처리 공간, OS 예약분을 고려한 전체 메모리 예산 계획이 필요합니다.

## 전체 메모리 배분 원칙

```
전체 물리 메모리 (예: 64GB)
  ├── OS 및 기타 프로세스:  ~20%   (~12.8 GB)
  ├── 캐시 (Result + PVO):  30~40% (~19~25 GB)
  │    ├── RS_CACHE_MAX_MEMORY_SIZE     (예: 8 GB)
  │    └── PVO_CACHE_MAX_MEMORY_SIZE    (예: 256 MB)
  └── Machbase 처리 공간:   나머지
       (정렬·집계 버퍼, 인덱스 빌드, 세션 처리 등)
```

- 캐시 합산이 전체 메모리의 40%를 넘지 않도록 유지합니다.
- 메모리 여유가 충분할 때만 캐시를 늘리고, 인덱스 빌드 등 일시적으로 메모리를 많이 쓰는 작업이 있을 때는 캐시 한도를 보수적으로 설정합니다.

## RS_CACHE_MAX_MEMORY_SIZE 설정

전체 Result Cache가 사용할 수 있는 최대 메모리 크기입니다.

| 항목 | 값 |
|-----|---|
| 최솟값 | 32 KB |
| 최댓값 | 2^64 - 1 바이트 |
| 기본값 | 512 MB |
| 런타임 변경 | 가능 (`ALTER SYSTEM SET`) |

```sql
-- Result Cache 메모리 한도를 2GB로 설정
ALTER SYSTEM SET RS_CACHE_MAX_MEMORY_SIZE = 2147483648;
```

```
# machbase.conf
RS_CACHE_MAX_MEMORY_SIZE = 2147483648
```

## Min-Max Cache 조정

Min-Max Cache는 컬럼의 파티션별 최솟값·최댓값 정보를 메모리에 유지하여, 조회 시 불필요한 파티션을 건너뛰는 파티션 프루닝(pruning)을 가속합니다.

관련 프로퍼티: `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE`

| 항목 | 값 |
|-----|---|
| 기본값 | 약 10 KB |
| 런타임 변경 | 불가 (서버 재시작 필요) |

**파티션 수가 많을수록 Min-Max Cache에 필요한 메모리가 증가**합니다. 파티션이 수천 개 이상인 대규모 TAG 테이블에서는 기본값이 부족할 수 있습니다.

| 환경 | 권장 MINMAX_CACHE_SIZE |
|-----|----------------------|
| 소규모 (파티션 수백 개 이하) | 기본값 유지 |
| 중규모 (파티션 수천 개) | 100 KB |
| 대규모 TAG 테이블 (파티션 수만 개) | 1 MB 이상 |

```
# machbase.conf (서버 재시작 필요)
DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE = 1048576
```

## PROCESS_MAX_SIZE로 프로세스 메모리 상한 설정

`PROCESS_MAX_SIZE`는 Machbase 서버 프로세스가 사용할 수 있는 최대 메모리 크기를 바이트 단위로 제한합니다. OOM killer 발생 전에 Machbase 스스로 메모리 사용을 억제하는 안전망 역할을 합니다.

```
# machbase.conf
PROCESS_MAX_SIZE = 51539607552   # 48 GB
```

## 메모리 부족 신호 및 진단

| 신호 | 의미 | 조치 |
|-----|------|------|
| OOM killer 로그 (`/var/log/syslog` 또는 `dmesg`) | 메모리 초과로 프로세스 강제 종료 | `PROCESS_MAX_SIZE` 설정, 캐시 한도 축소 |
| `free -h`에서 swap 사용량 급증 | 물리 메모리 부족으로 swap 활용 | 캐시 한도 축소 또는 메모리 증설 |
| `RS_CACHE_MAX_MEMORY_SIZE`에 `CACHE_MEMORY_USAGE`가 근접 | Result Cache 포화 | `RS_CACHE_MAX_MEMORY_SIZE` 증설 또는 캐시 정책 조정 |

```bash
# 현재 메모리 사용 현황 확인
free -h

# swap 사용량 추세 확인
vmstat 5 10
```

```sql
-- Result Cache 메모리 사용량 확인
SELECT
    cache_count,
    cache_memory_usage / 1024 / 1024 AS cache_memory_mb,
    cache_replaced
FROM v$rs_cache_stat;
```

## 설정 변경 순서 권장 사항

1. `free -h` 및 `V$RS_CACHE_STAT`으로 현재 상태 파악
2. 필요한 캐시 크기 계산 후 `RS_CACHE_MAX_MEMORY_SIZE` 조정 (`ALTER SYSTEM SET`으로 런타임 적용)
3. Min-Max Cache 조정이 필요하면 `machbase.conf` 수정 후 서버 재시작
4. 변경 후 일정 시간 모니터링하여 `CACHE_REPLACED`, swap 사용량 등 재확인
