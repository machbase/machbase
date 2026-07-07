---
type: docs
title: '메모리 사용량 확인'
weight: 40
---

Machbase 서버의 메모리 사용 현황을 SQL과 OS 명령으로 확인하는 방법을 설명합니다. 메모리 부족은 쿼리 오류, 서버 불안정, OOM Killer 강제 종료로 이어질 수 있으므로 주의가 필요합니다.

## 시스템 메모리 사용량

`V$SYSMEM`은 Machbase 내부의 메모리 매니저별 사용 현황을 표시합니다.

```sql
-- 메모리 매니저별 현재 사용량 및 최대 사용량
SELECT name,
       usage                           AS current_bytes,
       max_usage                       AS peak_bytes,
       round(usage / 1048576.0, 1)     AS current_mb,
       round(max_usage / 1048576.0, 1) AS peak_mb
  FROM v$sysmem
 ORDER BY usage DESC;
```

| 컬럼 | 설명 |
|------|------|
| NAME | 메모리 매니저 이름 |
| USAGE | 현재 사용 중인 메모리 (바이트) |
| MAX_USAGE | 서버 시작 이후 기록된 최대 사용량 |

## 세션별 메모리 사용량

```sql
-- 세션별 메모리 사용량 (상위 10개)
SELECT sm.sid,
       s.user_name,
       s.user_ip,
       sum(sm.usage)                        AS total_bytes,
       round(sum(sm.usage) / 1048576.0, 1)  AS total_mb
  FROM v$sesmem sm
  JOIN v$session s ON sm.sid = s.id
 WHERE s.closed = 0
 GROUP BY sm.sid, s.user_name, s.user_ip
 ORDER BY total_bytes DESC
 LIMIT 10;
```

메모리를 많이 사용하는 세션을 파악하면 `MAX_QPX_MEM` 설정 조정이나 해당 세션 종료 여부를 결정하는 데 도움이 됩니다.

## Result Cache 메모리 상태

Result Cache가 활성화된 경우, 캐시 메모리 사용량을 확인합니다.

```sql
-- Result Cache 통계
SELECT cache_count,
       cache_hit,
       aggr_hit,
       cache_replaced,
       cache_memory_usage,
       round(cache_memory_usage / 1048576.0, 1) AS cache_mb
  FROM v$rs_cache_stat;
```

`cache_replaced` 값이 지속적으로 증가하면 캐시 메모리가 부족하여 캐시가 자주 교체되고 있는 것입니다. `RS_CACHE_MAX_MEMORY_SIZE` 파라미터로 캐시 메모리 한도를 늘릴 수 있습니다.

## Page Cache 상태

```sql
-- Page Cache 현재 상태
SELECT max_mem_size,
       cur_mem_size,
       page_cnt,
       round(cur_mem_size / 1048576.0, 1) AS cur_mb,
       round(max_mem_size / 1048576.0, 1) AS max_mb
  FROM v$storage_dc_pagecache;
```

## Volatile 테이블 메모리

Volatile 테이블은 메모리에만 데이터를 저장합니다.

```sql
-- Volatile 테이블스페이스 메모리 사용량
SELECT round(max_mem_size / 1048576.0, 1) AS max_mb,
       round(cur_mem_size / 1048576.0, 1) AS current_mb
  FROM v$storage_dc_volatile_table;
```

## OS 레벨 메모리 확인

Machbase 프로세스의 실제 메모리 사용량을 OS 레벨에서 확인합니다.

```bash
# 시스템 전체 메모리 상태
free -h

# Machbase 프로세스의 메모리 사용량
top -b -n 1 -p $(pgrep machbased) | tail -3

# RSS(상주 메모리), VSZ(가상 메모리) 확인
ps aux | grep machbased | grep -v grep

# /proc에서 상세 메모리 정보 확인
cat /proc/$(pgrep machbased)/status | grep -i 'vmrss\|vmsize\|vmswap'
```

## 메모리 관련 주요 설정

```sql
-- 메모리 관련 설정 확인
SELECT name, value, deflt
  FROM v$property
 WHERE name IN (
   'MAX_QPX_MEM',
   'RS_CACHE_MAX_MEMORY_SIZE',
   'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE',
   'TAG_CACHE_MAX_MEMORY_SIZE'
 )
 ORDER BY name;
```

| 파라미터 | 설명 |
|---------|------|
| MAX_QPX_MEM | 세션당 최대 쿼리 메모리 (바이트) |
| RS_CACHE_MAX_MEMORY_SIZE | Result Cache 최대 메모리 |
| VOLATILE_TABLESPACE_MEMORY_MAX_SIZE | Volatile 테이블스페이스 최대 메모리 |
| TAG_CACHE_MAX_MEMORY_SIZE | Tag 테이블 캐시 최대 메모리 |

## 메모리 부족 징후 대응

### 쿼리 메모리 부족 오류

```
[ERROR] [QUERY] Query aborted due to memory limit. sess_id=5
```

```sql
-- MAX_QPX_MEM 런타임 조정 (세션당 512MB)
ALTER SYSTEM SET MAX_QPX_MEM = 536870912;
```

### 시스템 메모리 부족

```bash
# OOM Killer 발동 여부 확인 (Ubuntu/Debian)
grep 'Out of memory\|oom_kill' /var/log/syslog | tail -20

# OOM Killer 발동 여부 확인 (RHEL/CentOS)
grep 'Out of memory\|oom_kill' /var/log/messages | tail -20

# dmesg에서 확인
dmesg | grep -i 'oom\|killed process'
```

OOM Killer가 `machbased` 프로세스를 종료한 경우, 서버 재시작 후 메모리 설정을 검토합니다.
