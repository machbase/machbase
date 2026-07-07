---
type: docs
title: '가상 테이블 활용'
weight: 30
---

가상 테이블(Virtual Table)은 Machbase 서버의 실시간 운영 상태를 테이블 형태로 표현합니다. 테이블 이름은 모두 `V$`로 시작하며 읽기 전용입니다. 일반 테이블과 JOIN하여 다양한 진단 정보를 조합할 수 있습니다.

## 주요 가상 테이블 목록

| 카테고리 | 테이블 이름 | 용도 |
|---------|-----------|------|
| 세션/시스템 | V$SESSION | 현재 접속 세션 정보 |
| 세션/시스템 | V$STMT | 실행 중인 SQL 문 |
| 세션/시스템 | V$PROPERTY | 현재 서버 설정값 |
| 세션/시스템 | V$SYSMEM | 시스템 메모리 사용량 |
| 세션/시스템 | V$SYSSTAT | 시스템 통계 정보 |
| 세션/시스템 | V$SYSTIME | 시스템 시간 통계 |
| 세션/시스템 | V$VERSION | 서버 버전 정보 |
| 세션/시스템 | V$HTTP_STATUS | HTTP 서비스 상태 |
| Result Cache | V$RS_CACHE_LIST | 결과 캐시 목록 |
| Result Cache | V$RS_CACHE_STAT | 결과 캐시 통계 |
| 스토리지 | V$STORAGE | 스토리지 파일 크기 요약 |
| 스토리지 | V$STORAGE_USAGE | 디스크 사용량과 한계 비율 |
| 스토리지 | V$STORAGE_TABLES | 테이블별 스토리지 사용량 |
| 스토리지 | V$STORAGE_MOUNT_DATABASES | 마운트된 백업 데이터베이스 |
| 태그 Rollup | V$ROLLUP | Rollup 작업 상태 |
| 스트림 | V$STREAMS | Stream 쿼리 실행 상태 |
| 라이선스 | V$LICENSE_INFO | 라이선스 정보 |

---

## V$SESSION — 현재 세션 정보

MACHBASE 서버에 접속된 세션의 목록과 상태를 표시합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| ID | 세션 식별자 |
| CLOSED | 연결이 닫혀있는지 여부 |
| USER_ID | 사용자 식별자 |
| LOGIN_TIME | 접속 시각 |
| CLIENT_TYPE | 접속 클라이언트 타입 |
| USER_NAME | 사용자 이름 |
| USER_IP | 사용자 IP 주소 |
| SQL_LOGGING | 해당 세션의 Trace Log 메시지 기록 여부 |
| IDLE_TIMEOUT | 유휴 상태 세션 종료 시간 (초) |
| QUERY_TIMEOUT | 쿼리 응답 대기 시간 |

```sql
-- 현재 접속 세션 목록
SELECT id, user_name, user_ip, client_type, login_time
  FROM v$session
 WHERE closed = 0
 ORDER BY login_time;
```

---

## V$STMT — 실행 중인 SQL 문

현재 실행 중이거나 대기 중인 SQL 문의 정보를 표시합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| ID | 쿼리 식별자 |
| SESS_ID | 쿼리를 실행한 세션 식별자 |
| STATE | 쿼리 상태 |
| RECORD_SIZE | SELECT 수행 시 결과 레코드 크기 |
| QUERY | 쿼리 구문 |

```sql
-- 실행 중인 쿼리 확인 (IDLE 제외)
SELECT id, sess_id, state, query
  FROM v$stmt
 WHERE state != 'IDLE';
```

> **참고**: `V$STMT`에는 `elapsed_time` 컬럼이 없습니다. 장시간 실행 쿼리를 추적하려면 `V$SESTIME`의 `ACCUM_TICK` 값과 결합하여 분석하십시오.

---

## V$PROPERTY — 현재 설정값

서버에 설정된 모든 프로퍼티 값을 조회합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| NAME | 프로퍼티 이름 |
| VALUE | 현재 설정값 |
| TYPE | 데이터 타입 |
| DEFLT | 기본값 |
| MIN | 최솟값 |
| MAX | 최댓값 |

```sql
-- 특정 설정값 확인
SELECT name, value, deflt
  FROM v$property
 WHERE name IN ('PORT_NO', 'TRACE_LOG_LEVEL', 'MAX_SESSION_COUNT');

-- 기본값과 다른 설정만 조회
SELECT name, value, deflt
  FROM v$property
 WHERE value != deflt
 ORDER BY name;
```

---

## V$STORAGE_USAGE — 디스크 사용량

저장 시스템의 디스크 사용 현황을 표시합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| TOTAL_SPACE | 데이터 디렉터리가 위치한 스토리지의 총 용량 |
| USED_SPACE | 사용 중인 용량 |
| USED_RATIO | 사용량 비율 (%) |
| RATIO_CAP | 사용량 한계 (이 값 초과 시 데이터 입력 중단) |

```sql
-- 디스크 사용량 확인
SELECT total_space, used_space, used_ratio, ratio_cap
  FROM v$storage_usage;
```

`USED_RATIO`가 `RATIO_CAP`에 근접하면 데이터 적재와 인덱스 구축이 중단됩니다. 정기적으로 모니터링하고 용량을 확보해야 합니다.

---

## V$RS_CACHE_LIST / V$RS_CACHE_STAT — Result Cache 상태

### V$RS_CACHE_LIST

| 컬럼 이름 | 설명 |
|---------|------|
| TOUCH_TIME | 캐시를 마지막으로 사용하거나 생성한 시각 |
| USER_ID | 캐시를 생성한 사용자 |
| QUERY | 캐시를 만든 쿼리문 |
| TIME_SPENT | 결과 생성까지 경과 시간 |
| RECORD_COUNT | 결과 레코드 개수 |
| HIT_COUNT | 캐시 히트 횟수 |

### V$RS_CACHE_STAT

| 컬럼 이름 | 설명 |
|---------|------|
| CACHE_COUNT | 현재 캐시 개수 |
| CACHE_HIT | 총 캐시 히트 횟수 |
| AGGR_HIT | 집계 결과의 캐시 히트 횟수 |
| CACHE_REPLACED | 캐시 교체 횟수 |
| CACHE_MEMORY_USAGE | 캐시 메모리 사용량 |

```sql
-- Result Cache 전체 통계
SELECT cache_count, cache_hit, aggr_hit,
       cache_replaced, cache_memory_usage
  FROM v$rs_cache_stat;

-- 히트율이 높은 캐시 쿼리 확인
SELECT query, hit_count, record_count, time_spent
  FROM v$rs_cache_list
 ORDER BY hit_count DESC
 LIMIT 10;
```

---

## V$ROLLUP — Rollup 상태

Tag 데이터의 Rollup 작업 상태를 표시합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| ID | Rollup 작업 ID |
| ROLLUP_TABLE | Rollup 테이블 이름 |
| SOURCE_TABLE | 집계 대상 테이블 이름 |
| COLUMN_NAME | 집계 대상 컬럼 |
| INTERVAL_TIME | 실행 주기 (밀리초) |
| LAST_WAKEUP_TIME | 최근 실행 시각 |
| ENABLED | 활성화 여부 (1/0) |
| LAST_ELAPSED_MSEC | 직전 실행에 걸린 시간 (밀리초) |
| RUN_STATE | 스레드 상태 (I=초기화, S=대기, R=실행중) |

```sql
-- Rollup 작업 상태 확인
SELECT rollup_table, source_table, column_name,
       interval_time, enabled, last_elapsed_msec, run_state
  FROM v$rollup
 ORDER BY rollup_table;

-- 비활성화된 Rollup 확인
SELECT rollup_table, source_table, enabled
  FROM v$rollup
 WHERE enabled = 0;
```

---

## V$STREAMS — Stream 상태

등록된 Stream 쿼리의 실행 상태를 표시합니다.

| 컬럼 이름 | 설명 |
|---------|------|
| NAME | Stream 이름 |
| LAST_EX_TIME | 마지막 실행 시각 |
| TABLE_NAME | 검색 대상 테이블 이름 |
| END_RID | 마지막으로 읽은 RID |
| STATE | 현재 상태 |
| QUERY_TXT | 원본 Stream 쿼리 |
| ERROR_MSG | 마지막 오류 메시지 |
| FREQUENCY | 최소 대기 시간 (나노초, 0이면 매 레코드마다 실행) |

```sql
-- Stream 실행 상태 확인
SELECT name, state, last_ex_time, error_msg
  FROM v$streams
 ORDER BY name;

-- 오류가 발생한 Stream 확인
SELECT name, state, error_msg
  FROM v$streams
 WHERE error_msg IS NOT NULL AND error_msg != '';
```

---

## V$LICENSE_INFO — 라이선스 정보

| 컬럼 이름 | 설명 |
|---------|------|
| ID | 라이선스 ID |
| ISSUE_DATE | 발행일 |
| TYPE | 라이선스 유형 |
| CUSTOMER | 고객사 이름 |
| PROJECT | 프로젝트 이름 |
| INSTALL_DATE | 설치일 |
| VIOLATE_STATUS | 라이선스 위반 상태 |
| VIOLATE_MSG | 라이선스 위반 메시지 |

```sql
-- 라이선스 정보와 위반 상태 확인
SELECT id, type, customer, issue_date,
       install_date, violate_status, violate_msg
  FROM v$license_info;
```

`VIOLATE_STATUS`가 0이 아니거나 `VIOLATE_MSG`에 내용이 있으면 라이선스 정책 위반 상태입니다. 즉시 Machbase 지원팀에 문의하십시오.

---

## V$SYSMEM — 시스템 메모리 사용량

| 컬럼 이름 | 설명 |
|---------|------|
| ID | 메모리 매니저 식별자 |
| NAME | 메모리 매니저 이름 |
| USAGE | 현재 사용량 |
| MAX_USAGE | 기록된 최대 사용량 |

```sql
-- 메모리 매니저별 사용량 확인
SELECT name, usage, max_usage
  FROM v$sysmem
 ORDER BY usage DESC;
```

---

## 전체 가상 테이블 목록 확인

```sql
-- 현재 서버에서 조회 가능한 V$ 가상 테이블 전체 목록
SELECT name
  FROM v$tables
 WHERE name LIKE 'V$%'
 ORDER BY name;
```

> **참고**: 가상 테이블은 읽기 전용입니다. 또한 클러스터 에디션에서만 제공되는 테이블(V$NODE_STATUS, V$REPLICATION 등)은 Standard 에디션에서 조회되지 않습니다. `V$TABLES`로 조회 가능한 테이블 목록을 먼저 확인하십시오.
