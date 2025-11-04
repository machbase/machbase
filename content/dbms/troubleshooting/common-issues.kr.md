---
title: '일반적인 문제 및 해결 방법'
type: docs
weight: 10
---

## 빠른 문제 해결 가이드

이 가이드는 Machbase 작업 시 가장 일반적으로 발생하는 문제와 해결 방법을 다룹니다.

## 연결 문제

### 서버에 연결할 수 없음

**증상**: 클라이언트 도구가 Machbase 서버에 연결 실패

**일반적인 원인**:
1. 서버가 실행되지 않음
2. 잘못된 포트 번호
3. 방화벽이 연결 차단
4. 네트워크 구성 문제

**해결 방법**:

```bash
# 서버가 실행 중인지 확인
ps -ef | grep machbase

# 서버 상태 확인
machadmin -s

# 서버가 실행 중이 아니면 시작
machbase

# machbase.conf에서 포트 구성 확인
grep PORT_NO $MACHBASE_HOME/conf/machbase.conf
```

### 연결 타임아웃

**증상**: 연결 시도가 타임아웃됨

**해결 방법**:
- 네트워크 연결 확인
- machbase.conf에서 MACHBASE_PORT_NO 확인
- 포트를 차단하는 방화벽이 없는지 확인
- 최대 연결 수 제한에 도달했는지 확인

```sql
-- 현재 연결 확인
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

```sql
-- 대량 삽입에는 APPEND 사용 (더 빠름)
INSERT /*+ APPEND */ INTO table_name VALUES (...);

-- 태그 테이블의 경우 대량 로딩에 csvimport 사용
csvimport -t TAG_TABLE -d data.csv

-- 메모리 설정 확인 및 조정
-- machbase.conf에서:
TAGDATA_CACHE_MAX_SIZE = 2G  -- 더 나은 성능을 위해 증가
```

### 느린 SELECT 성능

**증상**: 쿼리가 너무 오래 걸림

**해결 방법**:

```sql
-- EXPLAIN을 사용하여 쿼리 플랜 분석
EXPLAIN SELECT * FROM tag WHERE name = 'TAG_001';

-- 태그 테이블의 경우 시간 범위 지정 필요
SELECT * FROM tag
WHERE name = 'TAG_001'
  AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-31');

-- 집계 쿼리에 롤업 테이블 사용
SELECT rollup('hour', 1, time), AVG(value)
FROM tag
GROUP BY rollup('hour', 1, time);

-- 자주 조회되는 컬럼에 인덱스 생성
CREATE INDEX idx_column ON table_name (column_name);
```

## 테이블 생성 문제

### PRIMARY KEY / BASETIME 누락 에러

**증상**: `ERR-02253: Mandatory column definition (PRIMARY KEY / BASETIME) is missing`

**해결 방법**:

```sql
-- 태그 테이블은 PRIMARY KEY와 BASETIME 모두 필요
CREATE TAG TABLE tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

### 가변 길이 컬럼 에러

**증상**: `ERR-01851: Variable length columns are not allowed in tag table`

**해결 방법**: 이 에러는 구 버전(< 5.6)에서 발생합니다. 버전 5.6+ 이상으로 업그레이드하거나 고정 길이 컬럼을 사용하세요.

## 데이터 삽입 문제

### SUMMARIZED 값 범위 초과

**증상**:
- `ERR-02341: SUMMARIZED value is greater than UPPER LIMIT`
- `ERR-02342: SUMMARIZED value is less than LOWER LIMIT`

**해결 방법**: 값이 LSL/USL 제한을 초과합니다. 제한을 조정하거나 입력 데이터를 수정하세요.

```sql
-- 현재 제한 확인
SELECT * FROM _table_meta;

-- 제한 업데이트
UPDATE table_name METADATA SET lsl = 0, usl = 1000 WHERE name = 'TAG_001';

-- 또는 제한 비활성화
UPDATE table_name METADATA SET lsl = NULL, usl = NULL WHERE name = 'TAG_001';
```

### 태그 메타데이터를 찾을 수 없음

**증상**: 데이터를 삽입할 수 없습니다, 태그명을 찾을 수 없음

**해결 방법**: 먼저 메타데이터에 태그명 등록

```sql
-- 태그 메타데이터 삽입
INSERT INTO tag_table METADATA VALUES ('TAG_001');

-- 그 다음 데이터 삽입
INSERT INTO tag_table VALUES ('TAG_001', NOW, 100);
```

## 메모리 문제

### 메모리 부족 에러

**증상**: 서버 크래시 또는 메모리 에러 반환

**해결 방법**:

1. **현재 메모리 사용량 확인**:
```sql
SELECT * FROM v$memstat;
```

2. **machbase.conf에서 메모리 설정 조정**:
```conf
# 캐시 크기 증가
TAGDATA_CACHE_MAX_SIZE = 4G
LOOKUP_CACHE_MAX_SIZE = 512M

# 버퍼 크기 조정
APPEND_BUFFER_SIZE = 128M
SELECT_BUFFER_SIZE = 64M
```

3. **구성 변경 후 서버 재시작**:
```bash
machadmin -k  # 서버 종료
machbase      # 서버 시작
```

상세한 메모리 에러 해결 방법은 [메모리 에러](../memory-error)를 참조하세요.

## 롤업 문제

### 종속 ROLLUP 테이블 존재

**증상**: `ERR-02651: Dependent ROLLUP table exists`

**해결 방법**: 종속성의 역순으로 롤업 테이블 삭제

```sql
-- 롤업 종속성 확인
SELECT * FROM m$sys_tables WHERE type = 'KEYVALUE';

-- 역순으로 삭제
DROP ROLLUP rollup_hour;
DROP ROLLUP rollup_min;
DROP ROLLUP rollup_sec;
DROP TABLE tag_table;
```

### 롤업이 업데이트되지 않음

**증상**: 롤업 데이터가 오래됨

**해결 방법**:

```sql
-- 강제 롤업 실행
EXEC ROLLUP_FORCE('rollup_name');

-- 롤업 상태 확인
SELECT * FROM v$rollup;

-- 롤업 재시작
EXEC ROLLUP_STOP('rollup_name');
EXEC ROLLUP_START('rollup_name');
```

## 인덱스 문제

### 인덱스를 삭제할 수 없음

**증상**: 인덱스 삭제 실패

**해결 방법**: 테이블을 사용 중인 활성 세션이 없는지 확인

```sql
-- 활성 세션 확인
SELECT * FROM v$session;

-- 필요시 세션 종료 (주의!)
EXEC KILL_SESSION(session_id);

-- 그 다음 인덱스 삭제
DROP INDEX index_name;
```

## 라이선스 문제

### 라이선스 만료

**증상**: 서버가 시작되지 않습니다, 라이선스 에러

**해결 방법**:

```bash
# 라이선스 상태 확인
machadmin -L

# 새 라이선스 설치
machadmin -i new_license_file.dat
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
-- 데이터베이스 상태 확인
SELECT * FROM v$database;

-- 재마운트 전에 언마운트
ALTER DATABASE database_name CLOSE;

-- 데이터베이스 마운트
ALTER DATABASE database_name MOUNT 'path/to/database';
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
# 클러스터 상태 확인
machcoordinatoradmin -s

# 필요시 코디네이터 재시작
machcoordinatoradmin -k
machcoordinator
```

## 문제를 피하기 위한 모범 사례

1. **정기 모니터링**:
   - 서버 로그를 정기적으로 모니터링
   - v$ 테이블을 통해 성능 메트릭 확인
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

- 특정 에러 메시지는 [에러 코드](../error-code)를 검토하세요
- 메모리 관련 문제는 [메모리 에러](../memory-error)를 확인하세요
- `$MACHBASE_HOME/trc/`의 서버 로그를 참조하세요
- 로그 파일과 에러 세부 정보와 함께 Machbase 지원팀에 문의하세요

## 진단 명령어

문제 해결에 유용한 명령어:

```sql
-- 서버 상태 확인
SELECT * FROM v$version;
SELECT * FROM v$instance;

-- 성능 모니터링
SELECT * FROM v$memstat;
SELECT * FROM v$session;
SELECT * FROM v$sqlstat;

-- 테이블 정보 확인
SELECT * FROM m$sys_tables;
SELECT * FROM m$sys_users;
SELECT * FROM m$sys_table_property;
```

## 로그 파일 위치

문제 해결을 위한 중요한 로그 파일:

```bash
# 서버 로그
$MACHBASE_HOME/trc/machbase-{pid}.trc

# 백업 로그
$MACHBASE_HOME/trc/backup.trc

# 롤업 로그
$MACHBASE_HOME/trc/rollup.trc

# 에러 로그
$MACHBASE_HOME/trc/error.trc
```
