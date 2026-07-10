---
type: docs
title: '12.9 성능 진단 체크리스트'
weight: 90
---

성능 이슈가 발생하면 체계적인 순서로 상태를 확인해야 원인을 빠르게 파악할 수 있습니다. 아래 체크리스트를 순서대로 수행하면 대부분의 병목 원인을 10분 내에 찾을 수 있습니다.

## 1단계: 현재 실행 쿼리 확인

서버에서 지금 무슨 일이 일어나고 있는지 먼저 파악합니다.

```sql
-- 현재 Statement 상태 확인
SELECT sess_id, id AS stmt_id, state, record_size, query
FROM v$stmt
ORDER BY sess_id, id;

-- 현재 연결된 세션 확인
SELECT id, user_name, user_ip, login_time, client_type
FROM v$session
ORDER BY login_time DESC;
```

확인 포인트:
- Statement 상태가 Fetch/Execute 계열로 오래 남아 있는 쿼리가 있는가?
- Append 세션이 비정상적으로 많이 쌓여 있는가?
- 동시 세션 수가 `MAX_SESSION_COUNT` 한계에 근접했는가?

## 2단계: EXPLAIN으로 실행 계획 확인

느린 SELECT 쿼리가 특정되었다면 실행 계획을 확인합니다.

```sql
-- 실행 계획 확인
EXPLAIN SELECT * FROM sensor_log WHERE device_id = 'dev-01';

-- 시간 범위 조건을 포함한 쿼리 실행 계획
EXPLAIN SELECT * FROM sensor_log
WHERE device_id = 'dev-01'
  AND _ARRIVAL_TIME BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

**FULL SCAN**이 출력되면 해당 컬럼에 인덱스가 없거나 사용되지 않는 것입니다. 인덱스 생성 또는 쿼리 재작성을 검토하십시오.

| 실행 계획 출력 | 의미 | 조치 |
|--------------|------|------|
| `FULL SCAN` | 전체 테이블 스캔 | 인덱스 생성, 시간 범위 조건 추가 |
| `INDEX SCAN` | 인덱스 활용 중 | 정상 (인덱스 선택도 추가 확인) |
| `_ARRIVAL_TIME` 또는 `TIME`의 `BITMAP RANGE` | 시간 범위 조건 활용 중 | 정상 (조회 범위 적정성 확인) |

## 3단계: 인덱스 현황 확인

```sql
-- 특정 테이블의 인덱스 목록 확인
SELECT i.name, i.type, t.name AS table_name, i.colcount, i.key_compress, i.max_level
FROM m$sys_indexes i, m$sys_tables t
WHERE i.table_id = t.id
  AND t.name = 'SENSOR_LOG'
ORDER BY i.name;
```

확인 포인트:
- 조회 조건으로 자주 사용하는 컬럼에 인덱스가 있는가?
- Append 성능이 느리다면 인덱스가 너무 많지는 않은가? (인덱스마다 추가 쓰기 비용 발생)
- 사용하지 않는 인덱스가 있다면 `DROP INDEX`로 제거를 검토하십시오.

## 4단계: Result Cache 히트율 확인

반복적인 집계 쿼리가 느리면 Result Cache 동작 여부를 확인합니다.

```sql
SELECT cache_count, cache_hit, cache_replaced FROM v$rs_cache_stat;
```

**히트율 계산**:
```
히트율(%) = cache_hit / (cache_count + cache_hit) × 100
```

| 히트율 | 상태 | 조치 |
|--------|------|------|
| 70% 이상 | 양호 | 유지 |
| 30~70% | 보통 | `RS_CACHE_MAX_MEMORY_SIZE` 조정 검토 |
| 30% 미만 | 비효율 | 캐시 크기 확대 또는 `RS_CACHE_TIME_BOUND_MSEC` 조정 |

`cache_replaced`가 높다면 캐시 교체가 빈번하게 발생하는 것입니다. `RS_CACHE_MAX_MEMORY_SIZE`를 늘리거나 `RS_CACHE_MAX_MEMORY_PER_QUERY`를 줄여 더 많은 쿼리 결과를 캐시하십시오.

```sql
-- 현재 Result Cache 설정 확인
SELECT name, value FROM v$property
WHERE name LIKE 'RS_CACHE%';
```

## 5단계: 파티션 상태 확인

파티션이 과도하게 많거나 상태가 비정상이면 조회와 체크포인트 성능이 저하됩니다.

```sql
-- TAG 테이블의 기본 파티션 설정 확인
SELECT name, value
FROM v$property
WHERE name IN ('TAG_PARTITION_COUNT', 'TAG_DATA_PART_SIZE');

-- TAG 테이블별 파티션 설정 확인
SELECT id, name, value
FROM m$sys_table_property
WHERE name = 'TAG_PARTITION_COUNT';

-- 특정 TAG 테이블의 내부 데이터 테이블 수 확인
SELECT COUNT(*) AS tag_data_table_count
FROM m$sys_tables
WHERE name LIKE '_SENSOR_TAG_DATA_%';
```

확인 포인트:
- 파티션 수가 예상보다 많은가? (오래된 파티션 정리 필요)
- 데이터가 특정 파티션에만 집중되어 있지 않은가?

오래된 데이터를 정리해야 한다면 테이블 타입별로 지원되는 DML과 보존 정책을 먼저 확인합니다. 이 빌드에서는 `ALTER TABLE ... DROP PARTITION BEFORE ...` 문법을 사용할 수 없습니다.

## 6단계: 시스템 리소스 확인

Machbase 내부 상태가 정상이어도 OS 수준 리소스가 부족하면 성능이 저하됩니다.

**CPU 확인**

```bash
top -b -n 1 | head -20
```

- `machbased` 프로세스의 CPU 사용률이 지속적으로 100% 이상이면 CPU 병목입니다.
- 다른 프로세스가 CPU를 과도하게 점유하고 있는지 확인하십시오.

**디스크 I/O 확인**

```bash
iostat -x 1 5
```

- `%util`이 90% 이상이면 I/O 포화 상태입니다.
- `await`(I/O 대기 시간)이 높으면 디스크 응답이 느린 것입니다.
- SSD 교체 또는 `DISK_IO_THREAD_COUNT` 조정을 검토하십시오.

**메모리 확인**

```bash
free -h
```

- `available` 메모리가 전체의 10% 미만이면 메모리 부족 상태입니다.
- swap 사용량이 증가하고 있다면 즉시 조치가 필요합니다.
- `RS_CACHE_MAX_MEMORY_SIZE`와 `PROCESS_MAX_SIZE`를 낮추는 것을 검토하십시오.

## 증상별 해결 방안

| 증상 | 의심 원인 | 해결 방법 |
|------|-----------|-----------|
| SELECT 느림 | 인덱스 없음, FULL SCAN | `CREATE INDEX`, 시간 범위 조건 추가 |
| Append 느림 | 인덱스 과다, I/O 포화 | 불필요 인덱스 제거, SSD 사용 |
| 메모리 계속 증가 | 캐시 설정 과다 | `RS_CACHE_MAX_MEMORY_SIZE` 줄이기 |
| 집계 쿼리 느림 | ROLLUP 미사용 | ROLLUP 생성 및 활용 |
| 반복 쿼리 느림 | Result Cache 비효율 | `RS_CACHE_TIME_BOUND_MSEC` 낮추기 |
| 서버 재시작 후 느림 | 체크포인트 너무 길었음 | `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC` 조정 |
| Cluster Append 느림 | 네트워크 병목, 배치 크기 작음 | `INSERT_RECORD_COUNT_PER_NODE` 상향, 10GbE 확인 |
| 특정 노드에 부하 집중 | 태그 해시 불균등 분산 | `TAG_PARTITION_COUNT` 조정, 태그명 재설계 |

## 빠른 진단 쿼리 모음

```sql
-- 1. 현재 실행 중인 쿼리 전체 확인
SELECT s.id AS session_id, s.user_name, st.id AS stmt_id, st.state, st.query
FROM v$session s, v$stmt st
WHERE s.id = st.sess_id
ORDER BY s.id, st.id;

-- 2. Append 현황 확인
SELECT count(*) AS append_session_count
FROM v$stmt WHERE query LIKE '%APPEND%';

-- 3. Result Cache 히트율 계산
SELECT
  cache_count,
  cache_hit,
  cache_replaced,
  ROUND(cache_hit * 100.0 / NULLIF(cache_count + cache_hit, 0), 1) AS hit_rate_pct
FROM v$rs_cache_stat;

-- 4. 프로퍼티 설정 일괄 확인 (체크포인트/캐시 관련)
SELECT name, value FROM v$property
WHERE name IN (
  'DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC',
  'DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC',
  'RS_CACHE_MAX_MEMORY_SIZE',
  'RS_CACHE_TIME_BOUND_MSEC',
  'DISK_IO_THREAD_COUNT'
);

-- 5. TAG 파티션 관련 기본 설정 확인
SELECT name, value
FROM v$property
WHERE name IN ('TAG_PARTITION_COUNT', 'TAG_DATA_PART_SIZE');

SELECT id, name, value
FROM m$sys_table_property
WHERE name = 'TAG_PARTITION_COUNT';
```

## 진단 순서 요약

```
성능 이슈 발생
      │
      ▼
1단계: v$stmt, v$session → 실행 중인 쿼리 파악
      │
      ▼
2단계: EXPLAIN → FULL SCAN 여부 확인
      │
      ├─ FULL SCAN 있음 → 인덱스 생성 또는 쿼리 수정
      │
      ▼
3단계: M$SYS_INDEXES → 인덱스 과다/부족 확인
      │
      ▼
4단계: v$rs_cache_stat → Result Cache 히트율 확인
      │
      ▼
5단계: v$table_stat → 파티션 상태 확인
      │
      ▼
6단계: top / iostat / free → OS 리소스 확인
      │
      ├─ I/O 포화 → SSD 교체, DISK_IO_THREAD_COUNT 조정
      ├─ 메모리 부족 → 캐시 설정 낮추기
      └─ CPU 포화 → 병렬 쿼리 조정, 쿼리 분산
```
