---
type: docs
title: '메모리 부족'
weight: 30
---

Machbase 서버가 OOM(Out of Memory) 오류를 내거나 갑자기 종료되는 경우 메모리 사용량과 설정 파라미터를 점검해야 합니다.

## 증상

- 서버 프로세스가 비정상 종료되고 트레이스 로그에 OOM 관련 메시지가 남음
- 쿼리 실행 중 `ERR: not enough memory` 오류 반환
- 시스템 전체의 메모리 사용률이 지속적으로 높게 유지됨
- Linux OOM Killer에 의해 Machbase 프로세스가 강제 종료됨

## 메모리 사용량 확인

### Machbase 내부 메모리 통계

```sql
SELECT name, usage, max_usage
  FROM v$sysmem
 ORDER BY usage DESC;
```

각 항목의 의미는 다음과 같습니다.

| 항목 | 설명 |
|------|------|
| `NAME` | 메모리 통계 항목 이름 |
| `USAGE` | 현재 사용량 |
| `MAX_USAGE` | 관측된 최대 사용량 |

### OS 레벨 메모리 확인

```bash
# 전체 메모리 사용량
free -h

# Machbase 프로세스의 메모리 사용량
ps aux | grep machbased | grep -v grep

# OOM Killer 이력 확인 (Linux)
dmesg | grep -i "oom\|out of memory" | tail -20
```

### 트레이스 로그에서 OOM 오류 확인

```bash
grep -i "out of memory\|OOM\|memory" $MACHBASE_HOME/trc/machbase.trc | tail -20
```

## 원인별 해결 방법

### 1. 결과 캐시 과다 사용

결과 캐시(`RS_CACHE`)가 메모리의 상당 부분을 점유하고 있는 경우 최대 크기를 줄입니다.

**확인**

```sql
SELECT * FROM v$property WHERE name LIKE 'RS_CACHE%';
```

**해결**

`machbase.conf`에서 최대 메모리 크기를 줄입니다.

```
RS_CACHE_MAX_MEMORY_SIZE = 268435456   # 256MB로 축소 (기본값 512MB)
```

설정 후 서버를 재시작합니다.

### 2. 대용량 쿼리 동시 실행

여러 세션에서 대용량 쿼리를 동시에 실행하면 쿼리별 임시 메모리가 합산되어 OOM이 발생할 수 있습니다.

**확인**

```sql
-- 현재 실행 중인 쿼리 목록
SELECT sess_id, id, state, record_size, query
FROM v$stmt
ORDER BY sess_id, id;
```

**해결**

문제가 되는 세션을 종료합니다.

```sql
ALTER SYSTEM KILL SESSION <sess_id>;
```

이후 동시 실행 쿼리 수를 줄이거나 쿼리에 시간 범위 조건을 추가하여 스캔 범위를 좁힙니다.

### 3. 버퍼 크기 과다 설정

`machbase.conf`의 버퍼 관련 파라미터가 물리 메모리에 비해 과하게 설정된 경우입니다.

**해결**

다음 파라미터를 조정합니다.

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| `RS_CACHE_MAX_MEMORY_SIZE` | 536870912 (512MB) | 결과 캐시 최대 메모리 |
| `TAG_CACHE_MAX_MEMORY_SIZE` | 134217728 (128MB) | TAG 캐시 메모리 |
| `DISK_COLUMNAR_TABLE_MINMAX_CACHE_MAX_SIZE` | 131072 (128MB) | MINMAX 캐시 크기 (KB 단위) |

물리 메모리가 8GB라면 위 세 항목의 합계가 2GB를 넘지 않도록 설정하십시오. 남은 메모리는 OS 및 쿼리 실행용으로 확보해야 합니다.

## OOM 재발 방지

**단기 조치**

- 결과 캐시와 TAG 캐시 크기를 현재 값의 50%로 줄입니다.
- 동시 접속 수를 `MAX_SESSION_COUNT` 파라미터로 제한합니다.

**장기 조치**

- 불필요한 데이터를 주기적으로 삭제하거나 아카이빙합니다.
- 대용량 쿼리는 시간 범위를 나눠 실행하도록 애플리케이션을 수정합니다.
- 물리 메모리 증설을 검토합니다.

## 메모리 설정 파라미터 요약

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| `RS_CACHE_ENABLE` | `1` | 결과 캐시 활성화 여부 (`0`으로 설정해 일시적으로 끌 수 있음) |
| `RS_CACHE_MAX_MEMORY_SIZE` | `536870912` | 결과 캐시 최대 메모리 (bytes) |
| `TAG_CACHE_MAX_MEMORY_SIZE` | `134217728` | TAG 캐시 최대 메모리 (bytes) |
| `MAX_SESSION_COUNT` | `1000` | 최대 동시 세션 수 |
