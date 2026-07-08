---
type: docs
title: '가상 테이블 사전'
weight: 20
---

가상 테이블(동적 뷰)은 `V$` 접두사를 가지며 Machbase 서버의 실시간 운영 상태를 테이블 형태로 표현합니다. 읽기 전용이며 쿼리할 때마다 최신 상태를 반환합니다.

## 가상 테이블 목록

| 카테고리 | 테이블 이름 | 설명 |
|---------|------------|------|
| 세션/시스템 | `V$VERSION` | 서버 버전 정보 |
| 세션/시스템 | `V$SESSION` | 현재 접속 세션 목록 |
| 세션/시스템 | `V$STMT` | 실행 중인 SQL 문장 |
| 세션/시스템 | `V$PROPERTY` | 현재 서버 설정값 |
| 세션/시스템 | `V$SYSMEM` | 시스템 메모리 사용량 |
| 세션/시스템 | `V$SYSSTAT` | 시스템 통계 정보 |
| 세션/시스템 | `V$SYSTIME` | 시스템 시간 통계 |
| 세션/시스템 | `V$HTTP_STATUS` | HTTP 서비스 상태 |
| Result Cache | `V$RS_CACHE_LIST` | 결과 캐시 목록 |
| Result Cache | `V$RS_CACHE_STAT` | 결과 캐시 통계 |
| 스토리지 | `V$STORAGE` | 스토리지 파일 크기 요약 |
| 스토리지 | `V$STORAGE_USAGE` | 디스크 사용량과 한계 비율 |
| 스토리지 | `V$STORAGE_TABLES` | 테이블별 스토리지 사용량 |
| 스토리지 | `V$STORAGE_MOUNT_DATABASES` | 마운트된 백업 데이터베이스 |
| 태그 Rollup | `V$ROLLUP` | Rollup 작업 상태 |
| 스트림 | `V$STREAMS` | Stream 쿼리 실행 상태 |
| 라이선스 | `V$LICENSE_INFO` | 라이선스 정보 |
| 인덱스 | `V$INDEX_NODE_STATUS` | 인덱스 상태 |
| 잠금 | `V$MUTEX` | 잠금 현황 |

## V$VERSION

서버 버전 정보를 조회합니다.

| 컬럼 이름 | 설명 |
|----------|------|
| `BINARY_SIGNATURE` | 서버 버전 문자열 |

```sql
SELECT binary_signature FROM v$version;
```

## V$SESSION

현재 접속 세션의 목록과 상태를 표시합니다.

| 컬럼 이름 | 설명 |
|----------|------|
| `ID` | 세션 식별자 |
| `CLOSED` | 연결이 닫혀있는지 여부 (0: 활성) |
| `USER_ID` | 사용자 식별자 |
| `LOGIN_TIME` | 접속 시각 |
| `CLIENT_TYPE` | 접속 클라이언트 타입 |
| `USER_NAME` | 사용자 이름 |
| `USER_IP` | 사용자 IP 주소 |
| `SQL_LOGGING` | 해당 세션의 Trace Log 기록 여부 |
| `IDLE_TIMEOUT` | 유휴 상태 세션 종료 시간 (초) |
| `QUERY_TIMEOUT` | 쿼리 응답 대기 시간 |

```sql
-- 현재 활성 세션 목록
SELECT id, user_name, user_ip, client_type, login_time
  FROM v$session
 WHERE closed = 0
 ORDER BY login_time;
```

## V$STMT

현재 실행 중이거나 대기 중인 SQL 문의 정보를 표시합니다.

| 컬럼 이름 | 설명 |
|----------|------|
| `ID` | 쿼리 식별자 |
| `SESS_ID` | 쿼리를 실행한 세션 식별자 |
| `STATE` | 쿼리 상태 |
| `RECORD_SIZE` | SELECT 수행 시 결과 레코드 크기 |
| `QUERY` | 쿼리 구문 |

```sql
-- 실행 중인 쿼리 확인
SELECT id, sess_id, state, query
  FROM v$stmt
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%'
    OR state LIKE 'Append in progress%';
```

## V$PROPERTY

서버에 설정된 모든 프로퍼티 값을 조회합니다.

| 컬럼 이름 | 설명 |
|----------|------|
| `NAME` | 프로퍼티 이름 |
| `VALUE` | 현재 설정값 |
| `TYPE` | 데이터 타입 |
| `DEFLT` | 기본값 |
| `MIN` | 최솟값 |
| `MAX` | 최댓값 |

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

## V$STORAGE_USAGE

저장 시스템의 디스크 사용 현황을 표시합니다.

| 컬럼 이름 | 설명 |
|----------|------|
| `TOTAL_SPACE` | 데이터 디렉터리 스토리지의 총 용량 |
| `USED_SPACE` | 사용 중인 용량 |
| `USED_RATIO` | 사용량 비율 (%) |
| `RATIO_CAP` | 사용량 한계 (초과 시 데이터 입력 중단) |

```sql
SELECT total_space, used_space, used_ratio, ratio_cap
  FROM v$storage_usage;
```

## V$SYSMEM

시스템 메모리 사용량을 조회합니다.

| 컬럼 이름 | 설명 |
|----------|------|
| `ID` | 메모리 매니저 식별자 |
| `NAME` | 메모리 매니저 이름 |
| `USAGE` | 현재 사용량 |
| `MAX_USAGE` | 기록된 최대 사용량 |

```sql
SELECT name, usage, max_usage
  FROM v$sysmem
 ORDER BY usage DESC;
```

## V$STREAMS

등록된 Stream 쿼리의 실행 상태를 표시합니다.

| 컬럼 이름 | 설명 |
|----------|------|
| `NAME` | Stream 이름 |
| `LAST_EX_TIME` | 마지막 실행 시각 |
| `TABLE_NAME` | 검색 대상 테이블 이름 |
| `END_RID` | 마지막으로 읽은 RID |
| `STATE` | 현재 상태 |
| `QUERY_TXT` | 원본 Stream 쿼리 |
| `ERROR_MSG` | 마지막 오류 메시지 |
| `FREQUENCY` | 최소 대기 시간 (나노초) |

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

## V$LICENSE_INFO

서버 라이선스 정보를 조회합니다.

| 컬럼 이름 | 설명 |
|----------|------|
| `ID` | 라이선스 ID |
| `ISSUE_DATE` | 발행일 |
| `TYPE` | 라이선스 유형 |
| `CUSTOMER` | 고객사 이름 |
| `PROJECT` | 프로젝트 이름 |
| `INSTALL_DATE` | 설치일 |
| `VIOLATE_STATUS` | 라이선스 위반 상태 |
| `VIOLATE_MSG` | 라이선스 위반 메시지 |

```sql
SELECT id, type, customer, issue_date,
       install_date, violate_status, violate_msg
  FROM v$license_info;
```

## 전체 가상 테이블 목록 확인

```sql
-- 현재 서버에서 조회 가능한 V$ 가상 테이블 전체 목록
SELECT name
  FROM v$tables
 WHERE name LIKE 'V$%'
 ORDER BY name;
```

> 가상 테이블은 읽기 전용입니다. 클러스터 에디션에서만 제공되는 테이블(V$NODE_STATUS, V$REPLICATION 등)은 Standard 에디션에서 조회되지 않습니다.
