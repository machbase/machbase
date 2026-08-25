---
type: docs
title: '13.6 PVO Cache와 메모리 튜닝'
weight: 60
toc: true
---

SQL 실행 계획을 재사용하는 PVO Cache와 LOG 테이블의 범위 조회를 돕는 Min-Max Cache,
서버 프로세스의 메모리 상한을 함께 설명합니다.

## 주요 메모리 기능

| 기능 | 용도 | 주요 설정 |
|------|------|-----------|
| PVO Cache | 동일 SQL의 실행 계획 재사용 | `PVO_CACHE_*` |
| Min-Max Cache | 파티션별 최솟값·최댓값으로 불필요한 파티션 건너뛰기 | `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE`, 컬럼 `MINMAX_CACHE_SIZE` |
| 프로세스 메모리 상한 | 서버 프로세스의 최대 메모리 사용량 제한 | `PROCESS_MAX_SIZE` |

PVO Cache는 실행 계획을 저장하며 SELECT 결과를 저장하지 않습니다. 반복 조회 결과를 재사용해야
한다면 애플리케이션 캐시를 사용합니다.

<a id="pvo-cache"></a>

## PVO Cache 운영

PVO(Partition Value Object) Cache는 SQL 실행 계획을 메모리에 저장하여 동일한 SQL을 다시
실행할 때 파싱과 최적화 비용을 줄입니다. Standard Edition에서 지원합니다.

바인드 변수를 사용하면 SQL 텍스트를 일정하게 유지할 수 있어 실행 계획 재사용에 유리합니다.
사용자, 기본 날짜 형식, 시간대, 숨김 컬럼 표시 여부, 쿼리 병렬도와 같은 세션 속성이 다르면
별도의 캐시 항목이 만들어질 수 있습니다.

### 주요 프로퍼티

| 프로퍼티 | 기본값 | 설명 |
|----------|--------|------|
| `PVO_CACHE_ENABLE` | 1 | PVO Cache 활성화 여부 |
| `PVO_CACHE_MAX_MEMORY_SIZE` | 256 MB | 전체 캐시 메모리 상한 |
| `PVO_CACHE_MAX_PLANS_PER_SQL` | 512 | SQL 하나에 저장할 최대 실행 계획 수 |
| `PVO_CACHE_MAX_SQL_ENTRIES` | 0 | 최대 SQL 항목 수. 0은 제한 없음 |
| `PVO_CACHE_SHARD_COUNT` | 16 | 캐시 shard 수. 변경 후 서버 재시작 필요 |

`machbase.conf`에서 초기값을 설정합니다.

```text
PVO_CACHE_ENABLE            = 1
PVO_CACHE_MAX_MEMORY_SIZE   = 268435456
PVO_CACHE_MAX_PLANS_PER_SQL = 512
PVO_CACHE_MAX_SQL_ENTRIES   = 0
PVO_CACHE_SHARD_COUNT       = 16
```

`PVO_CACHE_SHARD_COUNT`를 제외한 PVO Cache 프로퍼티는 실행 중에 변경할 수 있습니다.

```text
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 536870912;
ALTER SYSTEM SET PVO_CACHE_MAX_PLANS_PER_SQL = 256;
```

이 값은 예시입니다. 현재값과 memory 예산을 확인한 뒤 maintenance 절차에서 적용하며, 변경
전후 지연과 memory를 비교합니다.

### 상태 확인

전체 상태는 `V$PVO_CACHE_STAT`, SQL별 상세 항목은 `V$PVO_CACHE_LIST`에서 확인합니다.

```sql
SELECT * FROM V$PVO_CACHE_STAT;

SELECT TOUCH_TIME, QUERY, HIT_COUNT, HANDLE_COUNT
FROM V$PVO_CACHE_LIST
ORDER BY HIT_COUNT DESC
LIMIT 10;
```

| 지표 | 확인 사항 |
|------|-----------|
| `CACHE_HIT`, `CACHE_MISS` | 실행 계획 재사용과 새 계획 생성 추세 |
| `CACHE_MEMORY_USAGE` | 현재 사용량이 메모리 상한에 접근하는지 확인 |
| `EVICT_COUNT` | 공간 부족으로 실행 계획이 자주 제거되는지 확인 |
| `INVALIDATE_COUNT` | DDL 변경으로 실행 계획이 자주 무효화되는지 확인 |
| `SINGLEFLIGHT_WAIT` | 같은 SQL의 동시 계획 생성 대기가 많은지 확인 |

`EVICT_COUNT`가 계속 증가하고 서버 메모리에 여유가 있다면
`PVO_CACHE_MAX_MEMORY_SIZE`를 늘립니다. DDL이 잦아 `INVALIDATE_COUNT`가 증가하는 경우에는
캐시 크기보다 스키마 변경 빈도를 먼저 검토합니다.

<a id="tuning-memory-configuration"></a>

## 메모리 설정 튜닝

캐시와 입력 버퍼의 상한뿐 아니라 정렬, 집계, 인덱스 생성, 동시 세션이 일시적으로 사용하는
메모리까지 포함하여 물리 메모리 예산을 잡습니다. 운영체제와 같은 호스트의 다른 프로세스가
사용할 메모리도 남겨야 합니다.

### Min-Max Cache

Min-Max Cache는 LOG 테이블 컬럼의 파티션별 최솟값과 최댓값을 유지하여 범위 조건에 맞지 않는
파티션을 건너뛰도록 돕습니다.

| 설정 | 설명 |
|------|------|
| `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE` | `_ARRIVAL_TIME` 컬럼에 사용하는 기본 캐시 크기. 기본 100 MB |
| 컬럼 `MINMAX_CACHE_SIZE` | 일반 LOG 컬럼별 캐시 크기. 기본 0 |

```text
DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE = 104857600
```

일반 컬럼은 생성 시 `PROPERTY(MINMAX_CACHE_SIZE = ...)`를 지정하거나 `ALTER TABLE ... MODIFY
COLUMN ... SET MINMAX_CACHE_SIZE`로 변경합니다. 자주 사용하는 범위 조건 컬럼에만 적용하고,
파티션 수가 많을수록 메모리 사용량이 늘어나는 점을 고려합니다.

### PROCESS_MAX_SIZE

`PROCESS_MAX_SIZE`는 Machbase 서버 프로세스가 사용할 수 있는 최대 메모리를 바이트 단위로
제한합니다.

```text
PROCESS_MAX_SIZE = 51539607552
```

OOM killer 기록이나 swap 사용량 증가가 관찰되면 PVO Cache, Min-Max Cache, 입력 버퍼의 상한과
동시 작업량을 함께 점검합니다.

```bash
free -h
vmstat 5 10
```

설정을 변경한 뒤에는 동일한 쿼리 부하에서 PVO Cache 지표, 응답 시간, 프로세스 메모리와 swap
추세를 함께 비교합니다.
