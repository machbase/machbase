---
type: docs
title: '17.1 문제 해결 접근법'
weight: 10
toc: true
---
문제가 발생했을 때 무작정 설정을 바꾸거나 서버를 재시작하면 원인 파악이 어려워집니다. 아래 5단계 절차를 순서대로 따르면 원인을 빠르게 찾고 재발을 방지할 수 있습니다.

## 5단계 문제 해결 절차

**1단계: 증상 파악**
오류 메시지, 발생 시각, 영향 범위(특정 사용자/전체 서비스)를 기록합니다. 재현 가능한 문제인지 확인합니다.

**2단계: 서버 상태 확인**
서버 프로세스가 정상 실행 중인지, 연결이 가능한지 먼저 확인합니다.

```bash
machadmin -e
```

**3단계: 로그 파일 분석**
`$MACHBASE_HOME/trc/machbase.trc`에서 증상 발생 시각 전후의 오류 메시지를 확인합니다.

```bash
tail -100 $MACHBASE_HOME/trc/machbase.trc | grep -i "error\|warn"
```

**4단계: 진단 SQL 실행**
V$ 가상 테이블과 진단 명령으로 현재 서버 상태를 수집합니다.

```sql
SELECT id, login_time, user_name, user_ip, closed FROM v$session;
SELECT sess_id, id, state, record_size, query FROM v$stmt;
```

**5단계: 해당 섹션의 해결 방법 적용**
증상에 해당하는 섹션을 찾아 원인별 해결 방법을 적용합니다. 해결 후 동일 증상이 재발하지 않는지 모니터링합니다.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [증상 확인](/dbms/troubleshooting/troubleshooting/#symptom) | 증상별 빠른 진단 표, 첫 번째로 실행할 명령 |
| [진단 명령어 모음](/dbms/troubleshooting/troubleshooting/#diagnosis-commands) | 바로 복사해서 쓸 수 있는 진단 SQL과 명령 모음 |
| [로그 확인](/dbms/troubleshooting/troubleshooting/#log-logs) | 주요 로그 파일 목록, 로그 레벨 설정, 오류 분석 방법 |
| [오류 코드로 원인 찾기](/dbms/troubleshooting/troubleshooting/#cause-lookup-error-codes) | 자주 발생하는 오류 코드 표와 해결 방법 |


<a id="symptom"></a>

## 증상 확인

아래 표에서 현재 증상을 찾아 확인 항목과 해당 섹션으로 이동합니다.

### 증상별 빠른 진단 표

| 증상 | 먼저 확인할 항목 | 이동할 섹션 |
|------|----------------|------------|
| 서버 접속 불가 (Connection refused) | 프로세스 실행 여부 확인 | [서버가 시작되지 않을 때](/dbms/troubleshooting/server-connection/#start-server) |
| 서버 시작 실패 | `machbase.trc` 최근 오류 확인 | [서버가 시작되지 않을 때](/dbms/troubleshooting/server-connection/#start-server) |
| 원격 접속 불가 (로컬은 정상) | `GRANT_REMOTE_ACCESS` 설정, 방화벽 | [연결할 수 없을 때](/dbms/troubleshooting/server-connection/#connection) |
| 비밀번호/인증 오류 | 대소문자, AUTH KEY 등록 여부 | [인증이 실패할 때](/dbms/troubleshooting/server-connection/#failure-authentication) |
| 쿼리 결과 없음 | 데이터 존재 여부, 시간 범위 조건 | [검색 결과 문제](/dbms/troubleshooting/performance/#search-results) |
| 입력 속도 저하 | `v$stmt`로 실행 중인 쿼리 확인 | [쿼리 성능 문제](/dbms/troubleshooting/performance/#slow) |
| 메모리 부족 오류 | `v$sysmem`으로 메모리 현황 확인 | [메모리 부족](/dbms/troubleshooting/performance/#memory-out-of) |
| 데이터 입력 실패 | 오류 코드, 테이블 스키마 확인 | [데이터 입력 실패](/dbms/troubleshooting/item/#failure) |
| CSV 임포트 오류 | `machloader -b`로 지정한 bad file 확인 | [CSV 임포트 실패](/dbms/troubleshooting/item/#failure-csv-import) |
| UPDATE/DELETE 오류 | 테이블 타입, WHERE 조건 확인 | [UPDATE/DELETE 문제](/dbms/troubleshooting/update-delete/) |
| ROLLUP 결과 이상 | `v$rollup`으로 ROLLUP 상태 확인 | [ROLLUP 문제](/dbms/tag-rollup-usage/overview-use-criteria/#rollup) |
| STREAM 쿼리 미실행 | `v$streams`으로 STREAM 상태 확인 | [STREAM 문제](/dbms/troubleshooting/automation/#execution-stream) |
| 백업 실패 | 디스크 공간, 백업 경로 권한 확인 | [백업과 복구 문제](/dbms/troubleshooting/recovery-backup/#failure-backup-restore) |
| MOUNT 실패 | 백업 파일 존재 여부, 버전 확인 | [MOUNT 실패](/dbms/troubleshooting/recovery-backup/#failure-mount) |
| Cluster 노드 이상 | 노드 간 네트워크 연결 확인 | [Cluster 문제](/dbms/operations-configuration-recovery/cluster//) |

### 서버 상태 즉시 확인

문제가 발생하면 가장 먼저 서버 프로세스 상태를 확인합니다.

```bash
# 서버 프로세스 상태 확인
machadmin -e
```

정상 상태에서는 아래와 같이 출력됩니다.

```
Machbase server is running.
```

서버가 실행 중이 아니면 다음을 확인합니다.

```bash
# 서버 프로세스 직접 확인
ps aux | grep machbase

# 포트 사용 여부 확인 (기본 포트: 5656)
netstat -tlnp | grep 5656
```

### 현재 연결 상태 확인

서버에 접속할 수 있다면 현재 세션 수와 상태를 확인합니다.

```sql
-- 현재 세션 수
SELECT COUNT(*) FROM v$session;

-- 세션 목록
SELECT id, login_time, user_name, user_ip, closed FROM v$session;
```

세션 수가 비정상적으로 많으면 연결 풀 설정이나 최대 연결 수를 확인합니다. 실행 중인 쿼리가 있으면 다음으로 확인합니다.

```sql
-- 실행 중인 쿼리 확인
SELECT sess_id, id, state, record_size, query FROM v$stmt;
```

<a id="diagnosis-commands"></a>

## 진단 명령어 모음

문제 진단에 자주 쓰는 SQL과 명령 모음입니다. 복사해서 바로 실행할 수 있습니다.

### 자주 쓰는 진단 SQL

#### 서버 기본 정보

```sql
-- 서버 버전 확인
SELECT * FROM v$version;

-- 현재 세션 목록
SELECT id, login_time, user_name, user_ip, closed FROM v$session;

-- 실행 중인 statement 확인
SELECT sess_id, id, state, record_size, query FROM v$stmt;
```

#### 스토리지

```sql
-- 디스크 사용량
SELECT * FROM v$storage_usage;

-- 테이블별 스토리지 사용량
SELECT * FROM v$storage_tables;
```

#### 자동 처리 상태

```sql
-- ROLLUP 상태
SELECT * FROM v$rollup;

-- STREAM 상태
SELECT * FROM v$streams;
```

#### 시스템 통계 및 설정

```sql
-- 오류 관련 통계
SELECT * FROM v$sysstat WHERE name LIKE '%ERROR%';

-- 현재 서버 설정값 조회
SELECT name, value FROM v$property WHERE name IN (
  'PORT_NO',
  'GRANT_REMOTE_ACCESS',
  'BIND_IP_ADDRESS',
  'MAX_SESSION_COUNT',
  'TRACE_LOG_LEVEL'
);

-- 메모리 사용 현황
SELECT * FROM v$sysmem;
```

#### 메타 정보

```sql
-- 테이블 목록
SELECT name, type FROM m$sys_tables ORDER BY name;

-- 특정 테이블 컬럼 목록
SELECT name, type, length FROM m$sys_columns
WHERE table_name = 'MY_TABLE';

-- 사용자 목록
SELECT name FROM m$sys_users;
```

### machadmin 명령 모음

```bash
machadmin -e      # 서버 실행 상태 확인
machadmin -u      # 서버 시작
machadmin -s      # 서버 정상 종료
machadmin -k      # 서버 강제 종료 (kill)
machadmin -f      # 설치된 라이선스 정보 확인
```

{{< callout type="warning" >}}
`machadmin -k`는 강제 종료 명령입니다. 정상 종료(`-s`)가 응답하지 않을 때만 사용합니다. 강제 종료 후에는 서버 재시작 시 복구 절차가 실행될 수 있습니다.
{{< /callout >}}

### 로그 파일 위치

| 파일 | 내용 |
|------|------|
| `$MACHBASE_HOME/trc/machbase.trc` | 서버 메인 로그 (오류, 경고, 운영 이벤트) |
| `$MACHBASE_HOME/trc/machsql.history` | machsql 대화형 세션의 SQL 실행 이력 |
| `machloader -b`로 지정한 bad file | machloader 적재 실패 레코드 |
| `machloader -l`로 지정한 log file | machloader 처리 건수와 오류 통계 |
| `$MACHBASE_COLLECTOR_HOME/trc/` | Collector 수집 상태 로그 |

### 빠른 진단 순서

문제 발생 시 아래 순서대로 실행하면 대부분의 원인을 파악할 수 있습니다.

```bash
# 1. 서버 상태
machadmin -e

# 2. 최근 오류 로그
tail -50 $MACHBASE_HOME/trc/machbase.trc | grep -i "error\|warn"
```

```sql
-- 3. 세션 현황
SELECT COUNT(*) AS session_count FROM v$session;

-- 4. 실행 중인 쿼리
SELECT sess_id, id, state, record_size, query FROM v$stmt;

-- 5. 스토리지 현황
SELECT * FROM v$storage_usage;
```

<a id="log-logs"></a>

## 로그 확인

서버 동작과 오류는 `$MACHBASE_HOME/trc/` 디렉터리의 로그 파일에 기록됩니다. 문제가 생기면 로그 파일부터 확인하십시오.

### 주요 로그 파일

| 파일 | 내용 |
|------|------|
| `$MACHBASE_HOME/trc/machbase.trc` | 서버 메인 로그. 시작/종료, 오류, 경고, 운영 이벤트 기록 |
| `$MACHBASE_HOME/trc/machsql.history` | machsql 대화형 세션의 SQL 실행 이력 |
| `machloader -b`로 지정한 bad file | machloader 적재 실패 레코드 (행 단위) |
| `machloader -l`로 지정한 log file | machloader 처리 건수, 오류 건수 통계 |
| `$MACHBASE_COLLECTOR_HOME/trc/` | Collector 에이전트 수집 상태 로그 |

### 서버 메인 로그 확인 방법

#### 최근 오류 빠르게 확인

```bash
# 최근 100줄에서 오류와 경고 필터링
tail -100 $MACHBASE_HOME/trc/machbase.trc | grep -i "error\|warn"

# 최근 50줄 전체 확인
tail -50 $MACHBASE_HOME/trc/machbase.trc
```

#### 특정 시점 로그 검색

```bash
# 특정 날짜 로그 검색
grep "2024-01-15" $MACHBASE_HOME/trc/machbase.trc | head -50

# 오류만 추출
grep -i "error" $MACHBASE_HOME/trc/machbase.trc | tail -20
```

### 로그 레벨과 의미

`machbase.trc`의 로그 항목은 심각도에 따라 구분됩니다.

| 레벨 | 의미 | 조치 |
|------|------|------|
| `ERROR` | 즉시 조치가 필요한 오류. 서비스에 영향을 미침 | 원인을 파악하고 즉시 해결 |
| `WARN` | 경고. 즉각적인 장애는 없지만 성능 저하 또는 향후 문제 가능성 | 원인 파악 후 계획적으로 해결 |
| `INFO` | 일반 운영 정보. 서버 시작, 세션 연결, 정기 작업 완료 등 | 참고용, 별도 조치 불필요 |

### 로그 상세도 조정 (TRACE_LOG_LEVEL)

운영 중 특정 모듈의 동작을 상세히 추적할 때는 `TRACE_LOG_LEVEL`을 조정합니다.

```sql
-- 현재 로그 레벨 확인
SELECT name, value FROM v$property WHERE name = 'TRACE_LOG_LEVEL';

-- 기본값(277)으로 복원
ALTER SYSTEM SET TRACE_LOG_LEVEL = 277;
```

주요 레벨 값 (더해서 사용):

| 값 | 모듈 |
|----|------|
| 1 | MM_1 (Main Module 레벨 1) |
| 4 | QP_1 (Query Processor 레벨 1) |
| 16 | SM_1 (Storage Manager 레벨 1) |
| 256 | XM_1 (Cluster 쿼리 분산 레벨 1) |

기본값 277 = 1(MM_1) + 4(QP_1) + 16(SM_1) + 256(XM_1)

### 로그 순환 설정

로그 파일이 무한히 커지는 것을 방지하기 위해 두 가지 파라미터를 설정합니다.

```sql
-- 현재 설정 확인
SELECT name, value FROM v$property
WHERE name IN ('TRACE_FLUSH_INTERVAL', 'TRACE_TRUNCATE_THRESHOLD');
```

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| `TRACE_FLUSH_INTERVAL` | 3 (초) | 로그 버퍼를 파일에 기록하는 주기 |
| `TRACE_TRUNCATE_THRESHOLD` | 100MB | 이 크기를 초과하면 로그 파일을 순환 |

`machbase.conf`에서 영구 설정:

```properties
TRACE_FLUSH_INTERVAL       = 3
TRACE_TRUNCATE_THRESHOLD   = 104857600
```

### 로그에서 원인 파악하는 방법

로그 항목은 보통 다음 형식으로 기록됩니다.

```
[2024-01-15 10:23:45] [ERROR] [QP] ERR-02058: Table does not exist. (TABLE_NAME)
```

- **시각**: 문제 발생 시점 특정
- **레벨**: ERROR/WARN/INFO
- **모듈**: 어느 내부 모듈에서 발생했는지 (QP=쿼리 처리, SM=스토리지, MM=메인)
- **오류 코드**: `ERR-XXXXX` 형식의 코드로 [오류 코드로 원인 찾기](/dbms/troubleshooting/troubleshooting/#cause-lookup-error-codes) 섹션에서 상세 내용을 조회

서버 시작 실패의 경우 로그 파일 맨 끝부분에 원인이 기록됩니다.

```bash
tail -30 $MACHBASE_HOME/trc/machbase.trc
```

<a id="cause-lookup-error-codes"></a>

## 오류 코드로 원인 찾기

오류 메시지는 `ERR-XXXXX: 메시지` 형식으로 출력됩니다. 오류 코드로 원인과 해결 방법을 빠르게 찾을 수 있습니다.

### 오류 확인 방법

명령줄에서는 오류 발생 시 즉시 메시지가 출력됩니다. 별도의 `V$ERROR` fixed table은
제공되지 않으므로, 클라이언트 출력과 `$MACHBASE_HOME/trc/machbase.trc`를 함께 확인합니다.

```
[ERR-02025: Table MY_TABLE does not exist.]
```

### 자주 발생하는 오류 코드

#### 연결 오류

| 오류 코드 | 메시지 | 원인 | 해결 방법 |
|---------|--------|------|----------|
| ERR-02081 | Invalid username/password | 잘못된 사용자명 또는 비밀번호 | 사용자명/비밀번호 확인. SYS 기본 비밀번호는 MANAGER |

#### 권한 오류

권한 오류는 실행한 DDL/DML과 대상 객체에 따라 메시지가 달라질 수 있습니다. 오류 메시지에
`privilege`, `permission`, `not accessible` 등이 포함되면 SYS 계정 또는 권한 있는
계정으로 필요한 `GRANT`를 확인합니다.

#### 객체 오류

| 오류 코드 | 메시지 | 원인 | 해결 방법 |
|---------|--------|------|----------|
| ERR-02024 | Table already exists | 이미 존재하는 테이블명으로 생성 시도 | 다른 이름 사용 또는 기존 테이블 삭제 후 재생성 |
| ERR-02025 | Table does not exist | 존재하지 않는 테이블명 사용 | `SELECT name FROM m$sys_tables;`로 테이블명 확인 |
| ERR-02056 | Column name not found | 존재하지 않는 컬럼명 사용 | `DESC table_name;`으로 컬럼명 확인 |
| ERR-02186 | Invalid database name | 잘못된 database 이름 | MOUNT/UMOUNT 이름과 경로 확인 |

#### 데이터 오류

| 오류 코드 | 메시지 | 원인 | 해결 방법 |
|---------|--------|------|----------|
| ERR-01003 | Duplicate primary key | TAG 테이블에 중복 태그명 입력 | 입력 데이터의 PRIMARY KEY 값 확인 |
| ERR-02253 | Mandatory column missing | TAG 테이블에 PRIMARY KEY 또는 BASETIME 누락 | DDL에 PRIMARY KEY, BASETIME 컬럼 추가 |
| ERR-02341 | SUMMARIZED value exceeded upper limit | 입력값이 USL 초과 | `UPDATE table METADATA SET usl = NULL`로 제한 해제 |
| ERR-02342 | SUMMARIZED value below lower limit | 입력값이 LSL 미만 | `UPDATE table METADATA SET lsl = NULL`로 제한 해제 |

#### 시스템/리소스 오류

| 오류 코드 | 메시지 | 원인 | 해결 방법 |
|---------|--------|------|----------|
| ERR-00303 | Disk space is insufficient | 디스크 공간 부족 | `df -h`로 공간 확인 후 불필요한 데이터 삭제 |
| ERR-00131 | Memory allocation failed | 메모리 부족 | 쿼리 결과 범위를 줄이거나 `PROCESS_MAX_SIZE` 증가 |
| ERR-02651 | Dependent ROLLUP table exists | ROLLUP이 있는 TAG 테이블 삭제 시도 | ROLLUP 테이블을 먼저 삭제 후 TAG 테이블 삭제 |

### 오류 코드 범위별 분류

| 범위 | 분류 |
|------|------|
| ERR-001xx | 파일 및 디렉터리 오류 |
| ERR-002xx ~ 003xx | 메모리 및 시스템 리소스 오류 |
| ERR-020xx | 연결 및 인증 오류 |
| ERR-021xx ~ 022xx | 권한 및 객체 오류 |
| ERR-023xx ~ 025xx | 데이터 및 스키마 오류 |
| ERR-026xx | ROLLUP/STREAM 관련 오류 |

### 오류 코드를 찾지 못한 경우

위 표에 없는 오류 코드가 발생하면 다음을 수행합니다.

1. `$MACHBASE_HOME/trc/machbase.trc` 로그에서 동일 시각의 다른 메시지를 함께 확인합니다.
2. 오류 발생 직전에 실행한 SQL이나 작업을 기록합니다.
3. 서버 버전(`SELECT * FROM v$version;`)과 오류 재현 단계를 정리하여 Machbase 지원팀에 문의합니다.
