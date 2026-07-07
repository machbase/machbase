---
type: docs
title: '메모리 설정'
weight: 40
---

Machbase의 메모리 설정은 서버 전체 프로세스 한도, 로그 테이블 버퍼, Result Cache, Volatile 테이블 등 여러 레이어로 구성됩니다. 각 설정값을 시스템 RAM에 맞게 적절히 조정하면 성능과 안정성을 모두 높일 수 있습니다.

## 프로세스 최대 메모리

### PROCESS_MAX_SIZE

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

**권장**: 시스템 전체 RAM의 60~70% 수준으로 설정합니다. 운영 체제와 다른 프로세스가 사용하는 메모리를 고려해야 합니다.

## 로그 테이블 버퍼 메모리

### DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE

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

**권장**: 물리적 RAM의 50~80%로 설정합니다.

### DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE

서버 시작 시 미리 확보해 두는 메모리 크기입니다. 초기 데이터 입력 시 메모리 할당으로 인한 성능 저하를 방지합니다.

| 항목 | 값 |
|------|----|
| 기본값 | 100MB |
| 재시작 필요 | 예 |

메모리가 충분한 환경에서만 활성화를 권장합니다.

## Result Cache 메모리

Result Cache는 반복 실행되는 쿼리의 결과를 메모리에 저장하여 응답 시간을 단축합니다.

### RS_CACHE_MAX_MEMORY_SIZE

Result Cache 전체가 사용할 수 있는 최대 메모리입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 512MB |
| 재시작 필요 | 예 |

```ini
# machbase.conf
RS_CACHE_MAX_MEMORY_SIZE = 1073741824   # 1GB
```

### RS_CACHE_MAX_MEMORY_PER_QUERY

단일 쿼리의 결과를 캐시할 때 허용하는 최대 메모리입니다. 이 값을 초과하는 결과는 캐시에 저장되지 않습니다.

| 항목 | 값 |
|------|----|
| 기본값 | 16MB |
| 재시작 필요 | 예 |

```ini
# machbase.conf
RS_CACHE_MAX_MEMORY_PER_QUERY = 33554432   # 32MB
```

### RS_CACHE_MAX_RECORD_PER_QUERY

단일 쿼리 결과의 최대 레코드 수입니다. 이 수를 초과하는 결과는 캐시에 저장되지 않습니다.

| 항목 | 값 |
|------|----|
| 기본값 | 10,000 (배포 설정 파일에서는 50,000으로 설정될 수 있음) |
| 재시작 필요 | 예 |

```ini
# machbase.conf
RS_CACHE_MAX_RECORD_PER_QUERY = 50000
```

## Volatile·Lookup 테이블 메모리

### VOLATILE_TABLESPACE_MEMORY_MAX_SIZE

시스템 전체의 Volatile 테이블과 Lookup 테이블이 사용할 수 있는 총 메모리 한도입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 2GB |
| 재시작 필요 | 예 |

## 메모리 설정 권장 가이드

서버의 RAM 크기에 따른 주요 파라미터 권장값 예시입니다.

| RAM | `PROCESS_MAX_SIZE` | `DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE` | `RS_CACHE_MAX_MEMORY_SIZE` |
|-----|--------------------|--------------------------------------------|---------------------------|
| 16GB | 10GB | 8GB | 512MB |
| 32GB | 22GB | 16GB | 1GB |
| 64GB | 44GB | 32GB | 2GB |
| 128GB | 90GB | 64GB | 4GB |

> **참고**: 위 값은 Machbase 단독 운영 시의 예시입니다. 동일 서버에 다른 서비스가 함께 운영되는 경우 그에 맞게 조정합니다.

## 현재 메모리 사용 확인

```sql
-- 서버 메모리 사용 현황
SELECT * FROM v$sysstat WHERE name LIKE '%memory%' OR name LIKE '%mem%';

-- Result Cache 상태
SELECT name, value FROM v$property WHERE name LIKE 'RS_CACHE%';
```
