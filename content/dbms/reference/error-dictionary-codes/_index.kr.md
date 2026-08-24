---
type: docs
title: '18.7 오류 코드 사전'
weight: 90
toc: true
---

Machbase 오류는 machsql, 드라이버 예외 메시지와 서버 trace 로그에 표시됩니다. 이 페이지는
Machbase 8.7.0의 대표 오류를 정리합니다.
8.5 원본의 전체 오류 코드 표는 [8.5 전체 오류 코드 레퍼런스](./original-8-5-full/)를
함께 참고하십시오.

오류 메시지는 실행 경로에 따라 `ERR-02010: ...` 형식의 문자열 또는 드라이버별 예외로
노출됩니다. 메시지 문구는 제품 개선 과정에서 바뀔 수 있으므로 애플리케이션에서는 문자열이
아니라 오류 코드를 기준으로 처리합니다.

## SQL 파서와 함수 오류

| 코드 | 메시지 | 대표 원인 |
|------|--------|-----------|
| `ERR-02009` | `Insufficient parser memory.` | SQL 파서 메모리 부족 |
| `ERR-02010` | `Syntax error: near token (%s).` | SQL 문법 오류 |
| `ERR-02011` | `Unrecognized token (%s).` | 인식할 수 없는 토큰 사용 |
| `ERR-02034` | `Invalid format of time expression.` | 시간 표현식 형식 오류 |
| `ERR-02035` | `Function [%s] does not exist.` | 존재하지 않는 함수 호출 |
| `ERR-02036` | `Function [%s] has an invalid argument.` | 함수 인자 개수 또는 값 오류 |
| `ERR-02037` | `Function [%s] argument data type does not match.` | 함수 인자 타입 불일치 |
| `ERR-02040` | `Invalid time range.` | 허용되지 않는 시간 범위 |

## 테이블, 컬럼, 입력 데이터 오류

| 코드 | 메시지 | 대표 원인 |
|------|--------|-----------|
| `ERR-02014` | `Column name is duplicated: (%s).` | 중복 컬럼명 사용 |
| `ERR-02015` | `Invalid column type: (%s).` | 지원하지 않는 컬럼 타입 지정 |
| `ERR-02024` | `Table %s already exists.` | 같은 이름의 테이블이 이미 존재 |
| `ERR-02025` | `Table %s does not exist.` | 대상 테이블이 존재하지 않음 |
| `ERR-02026` | `The number of insert values and that of columns are mismatched.` | INSERT 컬럼 수와 값 수 불일치 |
| `ERR-02030` | `Column name (%s) does not exist.` | 존재하지 않는 컬럼 지정 |

## 시스템 리소스 오류

| 코드 | 메시지 | 대표 원인 |
|------|--------|-----------|
| `ERR-01007` | `There is no available disk space for writing <%lld>bytes to the file<%s>, errno = %d.` | 데이터 파일을 기록할 디스크 공간 부족 |
| `ERR-01346` | `Current Allocate Memory / PROCESS_MAX_SIZE (%llu/%llu), increase PROCESS_MAX_SIZE property and restart.` | `PROCESS_MAX_SIZE` 한도 초과 |

## 오류 코드 확인 방법

- machsql 또는 드라이버에서 반환하는 오류 문자열을 확인합니다.
- 서버 로그는 `$MACHBASE_HOME/trc/` 아래의 trace 로그를 확인합니다.

오류 발생 후 원인을 파악하기 어렵다면 [서버 로그 분석](/dbms/operations-configuration-recovery/diagnosis-observability/#log-diagnosis-logs-log-server-logs)과 [장애 징후 확인](/dbms/operations-configuration-recovery/diagnosis-observability/#monitoring-capacity-failure) 섹션을 참고하십시오.
