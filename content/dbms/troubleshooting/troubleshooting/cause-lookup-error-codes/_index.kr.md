---
type: docs
title: '오류 코드로 원인 찾기'
weight: 40
---

Machbase의 오류 메시지는 `ERR-XXXXX: 메시지` 형식으로 출력됩니다. 오류 코드로 원인과 해결 방법을 빠르게 찾을 수 있습니다.

## machsql에서 오류 확인 방법

```sql
-- machsql에서 마지막 오류 메시지 확인
SELECT * FROM v$error;
```

명령줄에서는 오류 발생 시 즉시 메시지가 출력됩니다.

```
[ERR-02058: Table 'MY_TABLE' does not exist.]
```

## 자주 발생하는 오류 코드

### 연결 오류

| 오류 코드 | 메시지 | 원인 | 해결 방법 |
|---------|--------|------|----------|
| ERR-02100 | Connection failed | 서버 미실행 또는 포트 차단 | 서버 상태 확인, 방화벽 규칙 검토 |
| ERR-02101 | Authentication failed | 잘못된 사용자명 또는 비밀번호 | 사용자명/비밀번호 확인. SYS 기본 비밀번호는 MANAGER |
| ERR-02102 | Max session count exceeded | 동시 접속 수 초과 | `MAX_SESSION_COUNT` 증가 또는 유휴 세션 정리 |
| ERR-02103 | Remote access is not allowed | 원격 접속 비허용 설정 | `GRANT_REMOTE_ACCESS = 1` 설정 후 재시작 |

### 권한 오류

| 오류 코드 | 메시지 | 원인 | 해결 방법 |
|---------|--------|------|----------|
| ERR-02186 | Insufficient privileges | 해당 작업에 대한 권한 없음 | SYS 계정으로 접속 후 `GRANT` 실행 |
| ERR-02187 | Object not accessible | 다른 사용자 객체에 접근 불가 | 객체 소유자에게 권한 요청 또는 SYS로 접속 |

### 객체 오류

| 오류 코드 | 메시지 | 원인 | 해결 방법 |
|---------|--------|------|----------|
| ERR-02058 | Table does not exist | 존재하지 않는 테이블명 사용 | `SELECT name FROM m$sys_tables;`로 테이블명 확인 |
| ERR-02059 | Column does not exist | 존재하지 않는 컬럼명 사용 | `SELECT name FROM m$sys_columns WHERE table_name='T';`로 확인 |
| ERR-02060 | Object already exists | 이미 존재하는 이름으로 생성 시도 | 다른 이름 사용 또는 기존 객체 삭제 후 재생성 |

### 데이터 오류

| 오류 코드 | 메시지 | 원인 | 해결 방법 |
|---------|--------|------|----------|
| ERR-01003 | Duplicate primary key | TAG 테이블에 중복 태그명 입력 | 입력 데이터의 PRIMARY KEY 값 확인 |
| ERR-02253 | Mandatory column missing | TAG 테이블에 PRIMARY KEY 또는 BASETIME 누락 | DDL에 PRIMARY KEY, BASETIME 컬럼 추가 |
| ERR-02341 | SUMMARIZED value exceeded upper limit | 입력값이 USL 초과 | `UPDATE table METADATA SET usl = NULL`로 제한 해제 |
| ERR-02342 | SUMMARIZED value below lower limit | 입력값이 LSL 미만 | `UPDATE table METADATA SET lsl = NULL`로 제한 해제 |

### 시스템/리소스 오류

| 오류 코드 | 메시지 | 원인 | 해결 방법 |
|---------|--------|------|----------|
| ERR-00303 | Disk space is insufficient | 디스크 공간 부족 | `df -h`로 공간 확인 후 불필요한 데이터 삭제 |
| ERR-00131 | Memory allocation failed | 메모리 부족 | 쿼리 결과 범위를 줄이거나 `PROCESS_MAX_SIZE` 증가 |
| ERR-02651 | Dependent ROLLUP table exists | ROLLUP이 있는 TAG 테이블 삭제 시도 | ROLLUP 테이블을 먼저 삭제 후 TAG 테이블 삭제 |

## 오류 코드 범위별 분류

| 범위 | 분류 |
|------|------|
| ERR-001xx | 파일 및 디렉터리 오류 |
| ERR-002xx ~ 003xx | 메모리 및 시스템 리소스 오류 |
| ERR-020xx | 연결 및 인증 오류 |
| ERR-021xx ~ 022xx | 권한 및 객체 오류 |
| ERR-023xx ~ 025xx | 데이터 및 스키마 오류 |
| ERR-026xx | ROLLUP/STREAM 관련 오류 |

## 오류 코드를 찾지 못한 경우

위 표에 없는 오류 코드가 발생하면 다음을 수행합니다.

1. `$MACHBASE_HOME/trc/machbase.trc` 로그에서 동일 시각의 다른 메시지를 함께 확인합니다.
2. 오류 발생 직전에 실행한 SQL이나 작업을 기록합니다.
3. 서버 버전(`SELECT * FROM v$version;`)과 오류 재현 단계를 정리하여 Machbase 지원팀에 문의합니다.
