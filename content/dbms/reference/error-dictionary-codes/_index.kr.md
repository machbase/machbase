---
type: docs
title: '오류 코드 사전'
weight: 90
---

Machbase에서 발생하는 오류는 `error_code` 숫자와 `error_message` 텍스트로 반환됩니다. 이 섹션은 자주 발생하는 오류 코드를 유형별로 분류하여 원인과 조치 방법을 제공합니다.

오류 코드는 machsql, REST API 응답, 드라이버 예외 메시지에서 확인할 수 있습니다.

```sql
-- 마지막 오류 확인 (machsql)
SELECT ERRORMSG FROM dual;
```

## 연결 및 인증 오류

| 코드 | 메시지 | 원인 | 조치 |
|------|--------|------|------|
| `ERR-02100` | Connection refused | 서버 미기동 또는 포트 오류 | 서버 프로세스 상태와 포트 설정 확인 |
| `ERR-02101` | Authentication failed | 사용자명 또는 비밀번호 오류 | 계정 정보 확인 |
| `ERR-02102` | Account locked | 연속 로그인 실패로 계정 잠금 | SYS 계정으로 잠금 해제 또는 관리자 문의 |
| `ERR-02103` | Connection timeout | 네트워크 지연 또는 서버 과부하 | 타임아웃 설정 증가, 네트워크 상태 확인 |
| `ERR-02104` | Maximum sessions exceeded | 최대 세션 수 초과 | `MAX_SESSION_COUNT` 설정 확인 또는 유휴 세션 종료 |

## 권한 오류

| 코드 | 메시지 | 원인 | 조치 |
|------|--------|------|------|
| `ERR-02186` | Insufficient privilege | 해당 객체에 대한 권한 없음 | SYS 계정으로 권한 부여(`GRANT`) |
| `ERR-02190` | Permission denied | 시스템 수준 접근 거부 | 사용자 권한 검토 |
| `ERR-02191` | Object owned by another user | 다른 사용자 소유 객체 접근 | 객체 소유자 또는 권한 확인 |

## 객체(테이블/인덱스) 오류

| 코드 | 메시지 | 원인 | 조치 |
|------|--------|------|------|
| `ERR-02058` | Table not found | 테이블이 존재하지 않음 | 테이블 이름, 대소문자, 사용자 확인 |
| `ERR-02001` | Duplicate table name | 동일 이름의 테이블이 이미 존재 | `DROP TABLE` 후 재생성 또는 다른 이름 사용 |
| `ERR-02060` | Column not found | 컬럼이 존재하지 않음 | 컬럼 이름 및 테이블 정의 확인 |
| `ERR-02050` | Index not found | 인덱스가 존재하지 않음 | 인덱스 이름 확인 |
| `ERR-02051` | Duplicate index name | 동일 이름의 인덱스가 이미 존재 | 다른 인덱스 이름 사용 |
| `ERR-02070` | Table is not empty | 테이블에 데이터가 있어 조작 불가 | 데이터 삭제(`TRUNCATE`) 후 재시도 |

## 데이터 오류

| 코드 | 메시지 | 원인 | 조치 |
|------|--------|------|------|
| `ERR-01003` | Duplicate key | Primary Key 중복 | 입력 데이터 키 값 중복 제거 |
| `ERR-01010` | Value out of range | 컬럼 허용 범위 초과 | 데이터 타입과 허용 범위 확인 |
| `ERR-01011` | String too long | VARCHAR 최대 길이 초과 | 컬럼 길이 확인 또는 데이터 절삭 |
| `ERR-01012` | Null not allowed | NOT NULL 컬럼에 NULL 입력 시도 | 필수 값 포함 여부 확인 |

## SQL 문법 오류

| 코드 | 메시지 | 원인 | 조치 |
|------|--------|------|------|
| `ERR-01001` | Syntax error | SQL 문법 오류 | SQL 문법 확인 (키워드 오타, 괄호 불일치 등) |
| `ERR-01002` | Type mismatch | 컬럼 타입과 입력 값 타입 불일치 | 데이터 타입 변환(`TO_DATE`, `CAST` 등) 확인 |
| `ERR-01004` | Division by zero | 0으로 나누기 | `NULLIF` 또는 조건 추가로 방어 |
| `ERR-01005` | Invalid date format | 날짜 형식 오류 | `TO_DATE` 포맷 문자열 확인 |

## 시스템/리소스 오류

| 코드 | 메시지 | 원인 | 조치 |
|------|--------|------|------|
| `ERR-00303` | Disk full | 디스크 공간 부족 | 디스크 용량 확보 또는 `DISK_FULL_LIMIT_RATIO` 설정 확인 |
| `ERR-00304` | Out of memory | 메모리 부족 | 서버 메모리 확인, 불필요한 프로세스 종료 |
| `ERR-00305` | Too many open files | 파일 디스크립터 한도 초과 | OS `ulimit -n` 값 증가 |
| `ERR-00310` | Log file write error | 로그 파일 쓰기 실패 | 디스크 상태 및 권한 확인 |

## REST API 오류

| 코드 | 메시지 | 원인 |
|------|--------|------|
| `3126` | The requested URL for the REST API is not valid | 유효하지 않은 REST API 엔드포인트 요청 |

HTTP 상태 코드와 REST API `error_code` 관계는 [REST API 오류 처리](../../application-integration/rest-api/error-handling-rest-api/)를 참고하십시오.

## 오류 코드 확인 방법

```sql
-- 마지막 발생 오류 확인
SELECT ERRCODE, ERRORMSG FROM dual;

-- Stream 오류 메시지 확인
SELECT name, error_msg FROM v$streams WHERE error_msg IS NOT NULL;
```

오류 발생 후 원인을 파악하기 어렵다면 [서버 로그 분석](../../operations-configuration-recovery/diagnosis-observability/log-diagnosis-logs/log-server-logs/)과 [장애 징후 확인](../../operations-configuration-recovery/diagnosis-observability/monitoring-capacity/failure/) 섹션을 참고하십시오.
