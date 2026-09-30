---
title: '일반적인 문제 및 해결 방법'
type: docs
weight: 10
---

## 빠른 문제 해결 가이드

이 가이드는 Machbase 작업 시 가장 일반적으로 발생하는 문제와 해결 방법을 다룹니다.

## 연결 문제

### 서버에 연결할 수 없음

**증상**: 클라이언트 도구가 Machbase 서버에 연결하지 못함

**일반적인 원인**:

1. 서버가 실행되지 않음
2. 잘못된 포트 번호
3. 방화벽이 연결 차단
4. 네트워크 구성 문제

**해결 방법**:

```bash
# Check if server is running
ps -ef | grep machbase

# Check server status
machadmin -e

# Start server if not running
machadmin -u

# Verify port configuration in machbase.conf
grep PORT_NO $MACHBASE_HOME/conf/machbase.conf
```

### 연결 타임아웃

**증상**: 연결 시도가 타임아웃됨

**해결 방법**:

- 네트워크 연결 확인
- `machbase.conf`에서 `PORT_NO` 확인
- 포트를 차단하는 방화벽이 없는지 확인
- 최대 연결 수 제한에 도달했는지 확인

```sql
-- Check current connections
SELECT * FROM v$session;
```

## 성능 문제

### 느린 INSERT 성능

**증상**: 데이터 삽입이 예상보다 느림

**일반적인 원인**:

1. APPEND 대신 INSERT 사용
2. 배치 작업을 사용하지 않음
3. 메모리 할당 부족
4. 너무 많은 인덱스

**해결 방법**:

대량 입력에는 APPEND API나 APPEND 모드의 CSV 도구를 사용합니다. SQL의 `INSERT /*+ APPEND */` 주석으로는 INSERT를 APPEND 프로토콜로 전환할 수 없습니다.

```bash
# Bulk load into a tag table (default append mode)
csvimport -t TAG_TABLE -d data.csv
```

```properties
# machbase.conf: example that sets the TAG cache limit per pool to 2 GiB
TAG_CACHE_MAX_MEMORY_SIZE = 2147483648
```

전체 캐시 용량은 이 값에 `TAG_CACHE_POOL_COUNT`를 곱한 값입니다. 물리 메모리와 다른 프로세스의 메모리 사용량에 맞게 조정하세요.

### 느린 SELECT 성능

**증상**: 쿼리가 너무 오래 걸림

**해결 방법**:

```sql
-- Use EXPLAIN to analyze query plan
EXPLAIN SELECT * FROM tag WHERE name = 'TAG_001';

-- For tag tables, ensure time range is specified
SELECT * FROM tag
WHERE name = 'TAG_001'
  AND time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD') AND TO_DATE('2024-01-31', 'YYYY-MM-DD');

-- Use rollup tables for aggregation queries
SELECT rollup('hour', 1, time), AVG(value)
FROM tag
GROUP BY rollup('hour', 1, time);

-- Create indexes on frequently queried columns
CREATE INDEX idx_column ON table_name (column_name);
```

## 테이블 생성 문제

### PRIMARY KEY / BASETIME 누락 에러

**증상**: `ERR-02253: Mandatory column definition (PRIMARY KEY / BASETIME) is missing`

**해결 방법**:

```sql
-- Tag tables require both PRIMARY KEY and BASETIME
CREATE TAG TABLE tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

### 가변 길이 컬럼 에러

**증상**: `ERR-01851: Variable length columns are not allowed in tag table`

**해결 방법**: 이 에러는 구 버전(< 5.6)에서 발생합니다. 5.6 이상 버전으로 업그레이드하거나 고정 길이 컬럼을 사용하세요.

## 데이터 삽입 문제

### SUMMARIZED 값 범위 초과

**증상**:

- `ERR-02341: SUMMARIZED value is greater than UPPER LIMIT`
- `ERR-02342: SUMMARIZED value is less than LOWER LIMIT`

**해결 방법**: 값이 LSL/USL 제한을 벗어났습니다. 제한을 조정하거나 입력 데이터를 수정하세요. 다음은 `table_name`에 `LOWER LIMIT`/`UPPER LIMIT` 속성을 가진 메타데이터 컬럼 `lsl`/`usl`을 정의한 경우의 예입니다. 이 기능은 Standard Edition에서 사용할 수 있습니다. 자세한 내용은 [LSL/USL](../../table-types/tag-tables/lsl-usl-limits/)을 참조하세요.

```sql
-- Check current limits
SELECT * FROM _table_name_meta;

-- Update limits
UPDATE table_name METADATA SET lsl = 0, usl = 1000 WHERE name = 'TAG_001';

-- Or disable limits
UPDATE table_name METADATA SET lsl = NULL, usl = NULL WHERE name = 'TAG_001';
```

### 태그 메타데이터를 찾을 수 없음

**증상**: 태그명을 찾을 수 없어 데이터를 삽입할 수 없음

**해결 방법**: 먼저 메타데이터에 태그명을 등록합니다.

```sql
-- Insert tag metadata
INSERT INTO tag_table METADATA VALUES ('TAG_001');

-- Then insert data
INSERT INTO tag_table VALUES ('TAG_001', NOW, 100);
```

## 메모리 문제

### 메모리 부족 에러

**증상**: 서버 크래시 또는 메모리 에러 반환

**해결 방법**:

1. **현재 메모리 사용량 확인**

```sql
SELECT * FROM V$SESMEM;
```

2. **`machbase.conf`에서 메모리 설정 조정**

   설정 항목과 단위는 [프로퍼티](../../configuration/property/)를 확인하세요. TAG 캐시의 전체 용량은 풀별 값에 풀 개수를 곱한 값입니다.

```conf
# Example that sets the TAG cache limit per pool to 4 GiB
TAG_CACHE_MAX_MEMORY_SIZE = 4294967296

# Example that sets the maximum memory used by one query to 64 MiB
MAX_QPX_MEM = 67108864
```

3. **구성 변경 후 서버 재시작**

```bash
machadmin -s  # Shut down server normally
machadmin -u  # Start server
```

상세한 메모리 에러 해결 방법은 [메모리 에러](../memory-error)를 참조하세요.

## 롤업 문제

### 종속 ROLLUP 테이블 존재

**증상**: `ERR-02651: Dependent ROLLUP table exists`

**해결 방법**: 종속성의 역순으로 롤업 테이블을 삭제합니다.

```sql
-- Check rollup dependencies
SELECT * FROM V$ROLLUP;

-- Drop in reverse order
DROP ROLLUP rollup_hour;
DROP ROLLUP rollup_min;
DROP ROLLUP rollup_sec;
DROP TABLE tag_table;
```

### 롤업이 업데이트되지 않음

**증상**: 롤업 데이터가 최신 상태가 아님

**해결 방법**:

```sql
-- Force rollup execution
ALTER ROLLUP rollup_name FORCE;

-- Check rollup status
SELECT * FROM v$rollup;

-- Restart rollup
ALTER ROLLUP rollup_name STOP;
ALTER ROLLUP rollup_name START;
```

## 인덱스 문제

### 인덱스를 삭제할 수 없음

**증상**: 인덱스 삭제 실패

**해결 방법**: 테이블을 사용 중인 활성 세션이 없는지 확인합니다.

```sql
-- Check active sessions
SELECT * FROM v$session;

-- Kill sessions if necessary (carefully!): as SYS, check the target session_id
ALTER SYSTEM KILL SESSION session_id;

-- Then drop index
DROP INDEX index_name;
```

## 라이선스 문제

### 라이선스 만료

**증상**: 서버가 시작되지 않음, 라이선스 에러

**해결 방법**:

```bash
# Check license status
machadmin -f

# Install new license
machadmin -t new_license_file.dat
```

## 백업 및 복구 문제

### 데이터베이스를 마운트할 수 없음

**증상**: 마운트 작업 실패

**일반적인 원인**:

1. 데이터베이스 파일 손상
2. 호환되지 않는 버전
3. 파일이 여전히 사용 중

**해결 방법**:

```sql
-- Check database status
SELECT * FROM V$STORAGE_MOUNT_DATABASES;

-- Unmount before remounting
UNMOUNT DATABASE database_name;

-- Mount database
MOUNT DATABASE 'path/to/database' TO database_name;
```

## 클러스터 관련 문제

### 노드 통신 실패

**증상**: 노드 간 통신 불가

**해결 방법**:

1. 노드 간 네트워크 연결 확인
2. 코디네이터가 실행 중인지 확인
3. 방화벽 규칙 확인
4. 클러스터 구성 검토

```bash
# Check cluster status
machcoordinatoradmin --cluster-status

# Restart coordinator if needed
machcoordinatoradmin -s
machcoordinatoradmin -u
```

## 문제를 피하기 위한 모범 사례

1. **정기 모니터링**:
   - 서버 로그를 정기적으로 모니터링
   - V$ 테이블을 통해 성능 메트릭 확인
   - 중요한 에러에 대한 알림 설정

2. **적절한 구성**:
   - 충분한 메모리 할당
   - 적절한 파티션 수 구성
   - 합리적인 캐시 크기 설정

3. **데이터 관리**:
   - 데이터 라이프사이클 관리를 위한 보존 정책 사용
   - 중요한 데이터의 정기 백업
   - 디스크 공간 사용량 모니터링

4. **쿼리 최적화**:
   - 태그 쿼리에 항상 시간 범위 지정
   - 인덱스를 적절히 사용
   - 집계를 위해 롤업 테이블 활용

5. **용량 계획**:
   - 데이터 증가 예측
   - 피크 부하 계획
   - 인프라를 사전에 확장

## 추가 도움 받기

- 특정 에러 메시지는 [에러 코드](../error-code)를 검토하세요.
- 메모리 관련 문제는 [메모리 에러](../memory-error)를 확인하세요.
- `$MACHBASE_HOME/trc/`의 서버 로그를 참조하세요.
- 로그 파일과 에러 세부 정보를 첨부해 Machbase 지원팀에 문의하세요.

## 진단 명령어

문제 해결에 유용한 명령어:

```sql
-- Check server status
SELECT * FROM v$version;
SELECT * FROM V$SYSSTAT;

-- Monitor performance
SELECT * FROM V$SESMEM;
SELECT * FROM v$session;
SELECT * FROM V$STMT;

-- Check table information
SELECT * FROM m$sys_tables;
SELECT * FROM m$sys_users;
SELECT * FROM m$sys_table_property;
```

## 로그 파일 위치

문제 해결을 위한 주요 로그 파일:

```text
$MACHBASE_HOME/trc/machbase.trc
```

서버 에러, 백업, 롤업 동작은 이 트레이스 로그에서 확인합니다. 로그 레벨은 [TRACE_LOG_LEVEL](../trace-log/)로 조정할 수 있습니다. 로그 파일 분할이나 별도 파일 출력은 운영 설정에 따라 달라지므로, 고정된 `backup.trc`, `rollup.trc`, `error.trc` 파일이 항상 생성되지는 않습니다.

관리 작업의 자세한 내용은 [machadmin](../../tools-reference/machadmin/), [시스템/세션 관리](../../sql-reference/sys-session-manage/), [데이터베이스 마운트](../../advanced-features/database-mount/)를 참조하세요.
