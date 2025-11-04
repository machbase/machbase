---
type: docs
title: 'machsql 첫 단계'
weight: 30
---

Machbase의 대화형 SQL 명령줄 인터페이스인 machsql 사용법을 배웁니다. 이 가이드는 매일 사용할 필수 명령어와 워크플로우를 다룹니다.

## machsql이란 무엇인가요?

`machsql`은 Machbase의 대화형 SQL 클라이언트입니다. 다음 작업을 위한 명령 센터로 생각하세요:
- SQL 쿼리 실행
- 테이블 및 사용자 관리
- 시스템 정보 보기
- 데이터 가져오기/내보내기

## Machbase에 연결

### 기본 연결

```bash
machsql
```

다음 항목을 입력하라는 메시지가 표시됩니다:
- Server address (기본값: 127.0.0.1)
- User ID (기본값: SYS)
- Password (기본값: MANAGER)

### 매개변수를 사용한 연결

연결 세부 정보를 제공하여 프롬프트를 건너뜁니다:

```bash
machsql -s localhost -u SYS -p MANAGER
```

일반적인 옵션:

```bash
machsql -s 192.168.1.100     # 원격 서버에 연결
machsql -u myuser -p mypass  # 자격 증명 지정
machsql -P 7878              # 다른 포트 사용
machsql -f script.sql        # SQL 스크립트 파일 실행
```

## 필수 명령어

### SHOW 명령어

시스템 정보 표시:

```sql
-- 모든 테이블 나열
SHOW TABLES;

-- 테이블 구조 보기
SHOW TABLE sensor_data;

-- 인덱스 나열
SHOW INDEXES;

-- 사용자 나열
SHOW USERS;

-- 라이선스 정보 보기
SHOW LICENSE;

-- 디스크 사용량 확인
SHOW STORAGE;

-- 테이블스페이스 보기
SHOW TABLESPACES;

-- 활성 쿼리 보기
SHOW STATEMENTS;
```

### 테이블 생성

```sql
-- 간단한 로그 테이블
CREATE TABLE app_logs (
    level VARCHAR(10),
    message VARCHAR(1000)
);

-- 센서 데이터 테이블
CREATE TABLE temperatures (
    sensor_id VARCHAR(20),
    value DOUBLE
);

-- 여러 컬럼이 있는 테이블
CREATE TABLE device_data (
    device_id INTEGER,
    location VARCHAR(50),
    temperature DOUBLE,
    humidity DOUBLE,
    pressure DOUBLE
);
```

### 데이터 삽입

```sql
-- 단일 삽입
INSERT INTO temperatures VALUES ('sensor01', 25.3);

-- 다중 삽입
INSERT INTO app_logs VALUES ('INFO', 'Application started');
INSERT INTO app_logs VALUES ('WARN', 'High memory usage detected');
INSERT INTO app_logs VALUES ('ERROR', 'Connection timeout');
```

### 데이터 조회

```sql
-- 모든 레코드 가져오기
SELECT * FROM temperatures;

-- 타임스탬프와 함께
SELECT _arrival_time, * FROM temperatures;

-- 조건과 함께
SELECT * FROM app_logs WHERE level = 'ERROR';

-- 최근 데이터 (최근 10분)
SELECT * FROM temperatures DURATION 10 MINUTE;

-- 특정 시간 범위의 데이터
SELECT * FROM temperatures
DURATION 30 MINUTE BEFORE 1 HOUR;

-- 집계
SELECT sensor_id, AVG(value), MAX(value), MIN(value)
FROM temperatures
GROUP BY sensor_id;

-- 레코드 수 세기
SELECT COUNT(*) FROM app_logs;
```

### 데이터 삭제

```sql
-- 가장 오래된 100개 행 삭제
DELETE FROM app_logs OLDEST 100 ROWS;

-- 최근 1000개 행만 유지
DELETE FROM app_logs EXCEPT 1000 ROWS;

-- 7일 이상 된 데이터 삭제
DELETE FROM app_logs EXCEPT 7 DAYS;

-- 특정 날짜 이전 데이터 삭제
DELETE FROM app_logs
BEFORE TO_DATE('2025-01-01', 'YYYY-MM-DD');
```

### 테이블 관리

```sql
-- 테이블 삭제
DROP TABLE temperatures;

-- 테이블 초기화 (모든 데이터 삭제)
TRUNCATE TABLE app_logs;

-- 인덱스 생성
CREATE INDEX idx_sensor ON temperatures(sensor_id);
```

## _arrival_time 이해

Machbase의 모든 레코드는 자동으로 타임스탬프를 받습니다:

```sql
SELECT _arrival_time, * FROM temperatures;
```

출력:
```
_arrival_time                   SENSOR_ID    VALUE
--------------------------------------------------------
2025-10-10 14:23:45 123:456:789 sensor01     25.3
2025-10-10 14:23:40 987:654:321 sensor01     24.8
```

타임스탬프는 나노초 정밀도를 포함합니다!

## 시간 범위 작업

### DURATION 키워드

`DURATION` 키워드는 시간 기반 쿼리를 간단하게 만듭니다:

```sql
-- 최근 5분
SELECT * FROM temperatures DURATION 5 MINUTE;

-- 최근 1시간
SELECT * FROM temperatures DURATION 1 HOUR;

-- 최근 1일
SELECT * FROM temperatures DURATION 1 DAY;

-- 2시간 전부터 30분간
SELECT * FROM temperatures
DURATION 30 MINUTE BEFORE 2 HOUR;
```

## 텍스트 검색

컬럼 내 텍스트 검색:

```sql
-- "error"가 포함된 로그 찾기
SELECT * FROM app_logs
WHERE message SEARCH 'error';

-- "timeout" 또는 "connection"이 있는 로그 찾기
SELECT * FROM app_logs
WHERE message SEARCH 'timeout'
   OR message SEARCH 'connection';

-- "high"와 "memory"가 모두 있는 로그 찾기
SELECT * FROM app_logs
WHERE message SEARCH 'high memory';
```

## SQL 스크립트 실행

SQL 명령이 포함된 파일 실행:

```bash
machsql -f setup.sql
```

또는 machsql 내에서:

```sql
@/path/to/script.sql
```

## 쿼리 결과 내보내기

결과를 파일로 저장:

```bash
# CSV로 내보내기
machsql -s localhost -u SYS -p MANAGER \
  -f query.sql -o output.csv -r csv

# JSON으로 내보내기
machsql -s localhost -u SYS -p MANAGER \
  -f query.sql -o output.json -r json
```

## 팁과 요령

### 1. 명령 기록

화살표 키를 사용하여 이전 명령 탐색:
- **↑** - 이전 명령
- **↓** - 다음 명령

### 2. 자동 완성

`Tab`을 눌러 자동 완성:
- 테이블 이름
- 컬럼 이름
- SQL 키워드

### 3. 여러 줄 쿼리

machsql은 여러 줄 SQL을 지원합니다:

```sql
SELECT
    sensor_id,
    AVG(value) as avg_temp,
    MAX(value) as max_temp
FROM
    temperatures
WHERE
    _arrival_time > NOW() - INTERVAL '1' HOUR
GROUP BY
    sensor_id;
```

### 4. 조용한 출력

스크립트의 경우 배너 숨기기:

```bash
machsql -i  # or --silent
```

### 5. 타임존 설정

```bash
machsql -z +0900  # 한국 타임존
machsql -z -0500  # 미국 동부
```

## 일반 워크플로우

### 일일 모니터링

```sql
-- 최근 오류 확인
SELECT * FROM app_logs
WHERE level = 'ERROR'
DURATION 1 DAY;

-- 센서 상태 모니터링
SELECT sensor_id, COUNT(*), AVG(value)
FROM temperatures
DURATION 1 HOUR
GROUP BY sensor_id;

-- 데이터베이스 크기 확인
SHOW STORAGE;
```

### 데이터 정리

```sql
-- 30일간의 데이터만 유지
DELETE FROM app_logs EXCEPT 30 DAYS;

-- 오래된 센서 데이터 제거
DELETE FROM temperatures EXCEPT 7 DAYS;
```

### 성능 확인

```sql
-- 활성 쿼리 보기
SHOW STATEMENTS;

-- 인덱스 상태 확인
SHOW INDEXES;

-- 인덱스 빌드 진행 상황 보기
SHOW INDEXGAP;
```

## 사용자 관리

```sql
-- 사용자 생성
CREATE USER datauser IDENTIFIED BY 'password123';

-- 권한 부여
GRANT SELECT ON temperatures TO datauser;
GRANT INSERT ON temperatures TO datauser;

-- 비밀번호 변경
ALTER USER datauser IDENTIFIED BY 'newpassword';

-- 사용자 삭제
DROP USER datauser;
```

## 키보드 단축키

| 단축키 | 동작 |
|----------|--------|
| `Ctrl+C` | 현재 쿼리 취소 |
| `Ctrl+D` | machsql 종료 |
| `Ctrl+L` | 화면 지우기 |
| `↑` / `↓` | 명령 기록 탐색 |
| `Tab` | 자동 완성 |

## 도움말 얻기

machsql 내에서:

```sql
-- 도움말 표시
help

-- 명령 구문 얻기
help CREATE TABLE
help SELECT
help DELETE
```

## 문제 해결

### 연결 실패

```bash
# 서버가 실행 중인지 확인
machadmin -e

# 포트가 열려 있는지 확인
netstat -an | grep 5656
```

### 쿼리 시간 초과

```sql
-- 오래 실행되는 쿼리의 경우 시간 초과 증가
SET QUERY_TIMEOUT = 300;  -- 5분
```

### 메모리 부족

```sql
-- 결과 집합 제한
SELECT * FROM large_table LIMIT 1000;

-- 원시 데이터 대신 집계 사용
SELECT COUNT(*), AVG(value) FROM large_table;
```

## 다음 단계

이제 machsql 기본 사항을 알았습니다:

1. [**기본 개념**](../concepts/) - 테이블 타입과 아키텍처 이해
2. [**튜토리얼**](../../tutorials/) - 실습 예제 따라하기
3. [**SQL 레퍼런스**](../../sql-reference/) - 완전한 SQL 구문 가이드

## 빠른 참조 카드

```sql
-- 테이블 작업
SHOW TABLES;
SHOW TABLE tablename;
CREATE TABLE t (col TYPE);
DROP TABLE t;

-- 데이터 작업
INSERT INTO t VALUES (...);
SELECT * FROM t;
SELECT * FROM t DURATION 10 MINUTE;
DELETE FROM t EXCEPT 7 DAYS;

-- 시스템 정보
SHOW LICENSE;
SHOW STORAGE;
SHOW USERS;

-- 시간 쿼리
DURATION 5 MINUTE
DURATION 1 HOUR
DURATION 1 DAY
DURATION 30 MINUTE BEFORE 2 HOUR

-- 텍스트 검색
WHERE column SEARCH 'text'
```

---

**연습이 완벽을 만듭니다!** 자신의 데이터로 이러한 명령을 시도하여 machsql에 익숙해지세요.
