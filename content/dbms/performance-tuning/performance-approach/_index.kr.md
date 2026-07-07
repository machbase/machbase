---
type: docs
title: '성능 문제 접근 순서'
weight: 10
---

성능 문제를 만나면 가장 먼저 해야 할 일은 원인을 좁히는 것입니다. 프로퍼티를 무작위로 수정하거나 인덱스를 무분별하게 추가하면 효과를 검증하기 어렵고 오히려 다른 문제를 유발할 수 있습니다. 다음 5단계를 순서대로 따르면 대부분의 성능 문제를 체계적으로 해결할 수 있습니다.

## 1단계: 병목 지점 파악

먼저 I/O, CPU, 메모리 중 어느 자원이 포화 상태인지 확인합니다.

**I/O 병목 확인**

```bash
# 디스크 I/O 사용률 확인 (1초 간격)
iostat -x 1

# %util 이 80% 이상이면 스토리지 I/O가 병목
# await 값이 높으면 디스크 응답 지연
```

**CPU 병목 확인**

```bash
# CPU 사용률 확인
top -d 1

# Machbase 프로세스의 CPU 사용률이 지속적으로 90% 이상이면
# QUERY_PARALLEL_FACTOR 또는 CPU_PARALLEL 설정 검토
```

**메모리 병목 확인**

```bash
# 메모리 사용량 확인
free -h

# Swap 사용이 증가하면 DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE 초과 가능성
# machbase.trc 에서 "slowdown" 키워드로 throttle 발생 여부 확인
grep -i slowdown $MACHBASE_HOME/trc/machbase.trc | tail -20
```

**병목 유형별 대응 방향**

| 병목 유형 | 주요 증상 | 대응 방향 |
|-----------|-----------|-----------|
| I/O 병목 | iostat %util 높음, 입력 속도 저하 | Direct I/O 설정, 디스크 분산, SSD 교체 |
| CPU 병목 | top CPU% 높음, 쿼리 응답 지연 | 병렬 쿼리 설정, 인덱스 추가, 쿼리 최적화 |
| 메모리 병목 | Swap 사용, Slowdown 로그 | MEMORY_MAX_SIZE 증가, 불필요 캐시 축소 |
| 네트워크 병목 | 원격 입력 속도만 저하 | 배치 크기 확대, 연결 수 줄이기 |

## 2단계: EXPLAIN으로 실행 계획 확인

I/O나 CPU 병목 없이 쿼리만 느리다면 실행 계획을 확인합니다. `EXPLAIN` 키워드를 쿼리 앞에 붙이면 실제 실행 없이 계획을 출력합니다.

```sql
EXPLAIN SELECT * FROM sensor_log
WHERE sensor_id = 'PUMP_01'
  AND _ARRIVAL_TIME BETWEEN TO_DATE('2025-01-01', 'YYYY-MM-DD')
                        AND TO_DATE('2025-01-02', 'YYYY-MM-DD');
```

### EXPLAIN 결과 해석

**INDEX SCAN (빠름)**

```
PLAN
-----
 PROJECT
  INDEX SCAN (SENSOR_LOG)
   *BITMAP RANGE (table id:1, column id:0, index id:0)
   [KEY RANGE]
    * _arrival_time BETWEEN TO_DATE('2025-01-01') AND TO_DATE('2025-01-02')
```

`INDEX SCAN`과 `_ARRIVAL_TIME`의 `BITMAP RANGE`가 나타나면 시간 범위 조건을 스캔 범위 축소에 활용하고 있습니다. LOG 테이블은 `_ARRIVAL_TIME` 컬럼에 기본 Min-Max Cache가 적용되어 범위 검색을 보조합니다.

**FULL SCAN (느림)**

```
PLAN
-----
 PROJECT
  FULL SCAN (SENSOR_LOG)
```

`FULL SCAN`이 나타나면 조건절이 `_ARRIVAL_TIME` 범위를 포함하지 않거나, 별도 인덱스가 없는 컬럼을 단독 조건으로 사용한 것입니다.

**TAG 테이블 EXPLAIN 예시**

```sql
EXPLAIN SELECT * FROM tag_data
WHERE name = 'PUMP_01'
  AND time BETWEEN TO_DATE('2025-01-01', 'YYYY-MM-DD')
               AND TO_DATE('2025-01-02', 'YYYY-MM-DD');
```

```
PLAN
-----
 PROJECT
  TAG READ (RAW)
   KEYVALUE INDEX SCAN (_TAG_DATA_0)
    [KEY RANGE]
     * time BETWEEN TO_DATE('2025-01-01') AND TO_DATE('2025-01-02')
   VOLATILE INDEX SCAN (_TAG_META)
    [KEY RANGE]
     * name='PUMP_01'
```

`TAG READ (RAW)` 아래의 `KEYVALUE INDEX SCAN`과 `VOLATILE INDEX SCAN`은 TAG 데이터와 메타데이터 경로를 사용하고 있음을 의미합니다. 태그 이름과 시간 범위를 함께 지정하는 것이 TAG 테이블의 기본 최적 조회 패턴입니다.

### 실행 계획 개선 방법

| 현재 실행 계획 | 원인 | 개선 방법 |
|---------------|------|-----------|
| FULL SCAN (LOG) | `_ARRIVAL_TIME` 조건 없음 | WHERE 절에 시간 범위 추가 |
| FULL SCAN (LOG) | 다른 컬럼 단독 조건 | 해당 컬럼에 LSM 인덱스 생성 |
| FULL SCAN (TAG) | `name` 조건 없음 | WHERE 절에 태그 이름 조건 추가 |
| TAG READ가 느림 | 시간 범위가 너무 넓음 | 조회 범위를 좁히거나 ROLLUP 사용 |

## 3단계: V$STMT, V$SESSION으로 현재 실행 쿼리 확인

쿼리가 오래 실행 중이거나 세션이 쌓이는 경우, 내부 뷰로 현황을 파악합니다.

**현재 실행 중인 세션 확인**

```sql
-- 현재 연결된 세션 목록
SELECT id, user_name, user_ip, login_time, client_type
FROM v$session
ORDER BY login_time DESC;
```

| 컬럼 | 설명 |
|------|------|
| `id` | 세션 ID |
| `user_name` | 접속 계정 |
| `user_ip` | 클라이언트 IP |
| `login_time` | 로그인 시각 |
| `client_type` | 클라이언트 종류 |

**현재 실행 중인 쿼리 확인**

```sql
-- 현재 Statement 상태 확인
SELECT sess_id, id AS stmt_id, state, record_size, query
FROM v$stmt
ORDER BY sess_id, id
LIMIT 5;
```

| 컬럼 | 설명 |
|------|------|
| `sess_id` | 세션 ID |
| `stmt_id` | Statement ID |
| `state` | Statement 상태 |
| `record_size` | 결과 레코드 크기 |
| `query` | SQL 텍스트 |

**특정 세션 강제 종료**

```sql
-- 세션 강제 종료 (session_id = 5)
ALTER SESSION CLOSE 5;
```

## 4단계: 인덱스·캐시·프로퍼티 조정

병목 지점과 원인이 파악되면 범위를 좁혀 조정합니다.

**인덱스 관련 조정**

```sql
-- LOG 테이블에 특정 컬럼 인덱스 추가
CREATE INDEX idx_sensor_id ON sensor_log (sensor_id) INDEX_TYPE LSM;

-- 인덱스 생성 후 EXPLAIN으로 개선 확인
EXPLAIN SELECT * FROM sensor_log WHERE sensor_id = 'PUMP_01';
```

**캐시 관련 조정**

```sql
-- 전역 MINMAX 기본값 확인
SELECT name, value
FROM v$property
WHERE name = 'DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE';

-- LOG 테이블 컬럼별 MINMAX 설정 확인
SELECT name, minmax_cache_size
FROM m$sys_columns
WHERE table_id = (
  SELECT id FROM m$sys_tables WHERE name = 'SENSOR_LOG'
)
ORDER BY id;
```

`machbase.conf`에서 LOG 테이블 `_ARRIVAL_TIME`의 기본 MINMAX 캐시 크기를 늘리면 시간 범위 스캔의 파티션 프루닝 효율을 높일 수 있습니다.

```
DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE = 209715200  # 200MB
```

**프로퍼티 조정**

```
# 쿼리 병렬도 설정 (CPU 코어 수의 50~75% 권장)
QUERY_PARALLEL_FACTOR = 4

# 입력 버퍼 최대 메모리 (물리 메모리의 50~80%)
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE = 17179869184
```

## 5단계: 모델 재설계 (최후 수단)

위 4단계를 모두 적용했는데도 성능이 기대치에 미치지 못한다면, 데이터 모델 자체를 재검토합니다.

**재설계가 필요한 신호**

- LOG 테이블에 수천 개 센서 데이터를 저장하고 있으며, 센서별 조회가 느리다 → TAG 테이블로 전환 검토
- TAG 테이블에 이벤트 로그를 저장하고 있으며, 전체 시간 범위 스캔이 잦다 → LOG 테이블로 전환 검토
- 컬럼이 50개 이상인 LOG 테이블에서 입력 성능이 나오지 않는다 → 컬럼 수 최소화 또는 테이블 분리

**재설계 시 고려사항**

재설계는 데이터 마이그레이션을 수반하므로 운영 중단 계획이 필요합니다. 가능하면 새 테이블을 병행 생성한 뒤 신규 데이터부터 이관하고, 구 테이블의 히스토리 데이터는 별도 아카이브 정책으로 처리하는 방식을 권장합니다.

자세한 모델링 원칙은 **[모델링 성능 튜닝](../performance-tuning-modeling/)** 을 참고하십시오.
