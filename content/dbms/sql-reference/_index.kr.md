---
type: docs
title: 'SQL 문법 참조하기'
weight: 80
---

Machbase의 완전한 SQL 구문 레퍼런스입니다. 이 섹션은 모든 SQL 명령어, 데이터 타입, 함수 및 연산자에 대한 상세한 문서를 제공합니다.

## SQL 명령어 카테고리

### 데이터 정의 언어 (DDL)

- `CREATE TABLE` - LOG 테이블 생성
- `CREATE TAGDATA TABLE` - TAG 테이블 생성
- `CREATE VOLATILE TABLE` - VOLATILE 테이블 생성
- `CREATE LOOKUP TABLE` - LOOKUP 테이블 생성
- `ALTER TABLE` - 테이블 구조 수정
- `DROP TABLE` - 테이블 삭제
- `CREATE INDEX` - 인덱스 생성
- `DROP INDEX` - 인덱스 삭제

### 데이터 조작 언어 (DML)

- `INSERT` - 데이터 삽입
- `SELECT` - 데이터 조회
- `UPDATE` - 데이터 업데이트 (VOLATILE/LOOKUP 테이블)
- `DELETE` - 데이터 삭제
- `DURATION` - 시간 기반 쿼리 절

### 데이터 제어 언어 (DCL)

- `CREATE USER` - 데이터베이스 사용자 생성
- `ALTER USER` - 사용자 수정
- `DROP USER` - 사용자 삭제
- `GRANT` - 권한 부여
- `REVOKE` - 권한 취소

### 시스템 명령어

- `SHOW TABLES` - 테이블 목록
- `SHOW TABLE` - 테이블 구조 보기
- `SHOW USERS` - 사용자 목록
- `SHOW INDEXES` - 인덱스 목록
- `SHOW STORAGE` - 스토리지 정보 보기
- `SHOW LICENSE` - 라이선스 정보 보기

## 데이터 타입

### 숫자 타입
- `SHORT`, `INTEGER`, `LONG`
- `FLOAT`, `DOUBLE`

### 문자열 타입
- `CHAR(n)`, `VARCHAR(n)`

### 날짜/시간 타입
- `DATE`, `DATETIME`

### 바이너리 타입
- `BINARY(n)`

### 네트워크 타입
- `IPV4`, `IPV6`

## 함수

### 시간 함수
- `NOW`, `SYSDATE`
- `TO_DATE()`, `TO_TIMESTAMP()`
- `TO_CHAR()`
- `INTERVAL`

### 집계 함수
- `COUNT()`, `SUM()`, `AVG()`
- `MIN()`, `MAX()`
- `STDDEV()`, `VARIANCE()`

### 문자열 함수
- `UPPER()`, `LOWER()`
- `LENGTH()`, `SUBSTR()`
- `SEARCH` 키워드

### 수학 함수
- `ABS()`, `CEIL()`, `FLOOR()`
- `ROUND()`, `TRUNC()`
- `POWER()`, `SQRT()`

## Machbase 전용 기능

### DURATION 절

```sql
SELECT * FROM table DURATION n MINUTE|HOUR|DAY [BEFORE n MINUTE|HOUR|DAY];
```

### SEARCH 키워드

```sql
SELECT * FROM table WHERE column SEARCH 'keyword';
```

### Rollup 쿼리

```sql
SELECT * FROM tag_table WHERE rollup = sec|min|hour;
```

### 시간 기반 삭제

```sql
DELETE FROM table OLDEST n ROWS;
DELETE FROM table EXCEPT n ROWS|DAYS;
DELETE FROM table BEFORE datetime;
```

## 완전한 레퍼런스

완전한 SQL 구문 문서는 다음을 참조하세요:
- [SQL 레퍼런스](../../dbms/sql-ref/) - 상세한 SQL 명령어 레퍼런스

## 빠른 참조 예제

### 테이블 생성

```sql
-- TAG 테이블
CREATE TAGDATA TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- LOG 테이블
CREATE TABLE logs (
    level VARCHAR(10),
    message VARCHAR(2000)
);

-- VOLATILE 테이블
CREATE VOLATILE TABLE cache (
    key VARCHAR(100) PRIMARY KEY,
    value VARCHAR(500)
);

-- LOOKUP 테이블
CREATE LOOKUP TABLE devices (
    device_id INTEGER,
    name VARCHAR(100)
);
```

### 데이터 조회

```sql
-- 최근 데이터
SELECT * FROM sensors DURATION 1 HOUR;

-- 조건과 함께
SELECT * FROM logs WHERE level = 'ERROR' DURATION 1 DAY;

-- 집계
SELECT sensor_id, AVG(value) FROM sensors
DURATION 1 DAY GROUP BY sensor_id;

-- Rollup 쿼리
SELECT * FROM sensors WHERE rollup = hour DURATION 7 DAY;
```

### 사용자 관리

```sql
-- 사용자 생성
CREATE USER analyst IDENTIFIED BY 'password';

-- 권한 부여
GRANT SELECT ON sensors TO analyst;

-- 비밀번호 변경
ALTER USER analyst IDENTIFIED BY 'newpassword';
```

## 학습 경로

1. **시작하기**: 기본 DDL/DML 명령어
2. **학습하기**: Machbase 전용 기능 (DURATION, SEARCH)
3. **마스터하기**: 고급 쿼리 및 함수
4. **참조하기**: 구문 세부 사항은 이 섹션 참조

## 관련 문서

- [핵심 개념](../core-concepts/) - Machbase 이해하기
- [일반 작업](../common-tasks/querying/) - 쿼리 예제
- [튜토리얼](../tutorials/) - 실습 연습
