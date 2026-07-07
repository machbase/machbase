---
type: docs
title: '세션과 네트워크 설정'
weight: 50
---

클라이언트 연결 포트, 최대 세션 수, 타임아웃 등 네트워크와 세션에 관련된 설정을 설명합니다.

## 포트 설정

### PORT_NO

클라이언트가 Machbase 서버에 연결하는 TCP 포트 번호입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 5656 |
| 범위 | 1024 ~ 65535 |
| 재시작 필요 | 예 |

```ini
# machbase.conf
PORT_NO = 5656
```

### HTTP_PORT_NO

REST API 서비스가 사용하는 HTTP 포트 번호입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 5657 |
| 범위 | 1024 ~ 65535 |
| 재시작 필요 | 예 |

```ini
# machbase.conf
HTTP_PORT_NO = 5657
HTTP_ENABLE  = 1   # REST API 활성화 (0: 비활성)
```

### BIND_IP_ADDRESS

리스너가 바인드할 IP 주소를 지정합니다. `0.0.0.0`은 모든 네트워크 인터페이스를 의미합니다.

| 항목 | 값 |
|------|----|
| 기본값 | 0.0.0.0 |
| 재시작 필요 | 예 |

특정 네트워크 인터페이스로만 접속을 허용하려면 해당 IP를 지정합니다.

```ini
# machbase.conf — 특정 IP만 허용
BIND_IP_ADDRESS = 192.168.1.100
```

### GRANT_REMOTE_ACCESS

원격지에서 데이터베이스에 접근할 수 있는지를 결정합니다. 0으로 설정하면 루프백(127.0.0.1)에서만 접속이 가능합니다.

| 항목 | 값 |
|------|----|
| 기본값 | 1 (허용) |
| 재시작 필요 | 예 |

## 세션 수 설정

### MAX_SESSION_COUNT

동시에 연결할 수 있는 세션의 최대 수입니다. 이 한도를 초과하면 신규 연결이 거부됩니다.

| 항목 | 값 |
|------|----|
| 기본값 | 4096 |
| 최솟값 | 64 |
| 재시작 필요 | 아니오 |

```sql
-- 런타임 변경
ALTER SYSTEM SET MAX_SESSION_COUNT = 2048;
```

### MAX_STMT_COUNT_PER_SESSION

세션 하나가 생성할 수 있는 Statement(PreparedStatement 포함)의 최대 수입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 1024 |
| 최솟값 | 512 |
| 재시작 필요 | 예 |

## 타임아웃 설정

### SESSION_IDLE_TIMEOUT_SEC

세션이 아무 작업도 하지 않을 때 연결을 자동으로 종료하는 시간(초)입니다. 0으로 설정하면 타임아웃이 없습니다.

| 항목 | 값 |
|------|----|
| 기본값 | 0 (무제한) |
| 재시작 필요 | 아니오 |

```sql
-- 30분 유휴 시 세션 종료
ALTER SYSTEM SET SESSION_IDLE_TIMEOUT_SEC = 1800;
```

### SESSION_QUERY_TIMEOUT_SEC

단일 쿼리의 최대 실행 시간(초)입니다. 이 시간을 초과하면 쿼리가 자동으로 취소됩니다. 0으로 설정하면 타임아웃이 없습니다.

| 항목 | 값 |
|------|----|
| 기본값 | 0 (무제한) |
| 재시작 필요 | 아니오 |

```sql
-- 쿼리 타임아웃 60초 설정
ALTER SYSTEM SET SESSION_QUERY_TIMEOUT_SEC = 60;
```

## 현재 세션 확인

`v$session` 뷰로 현재 연결된 세션 목록과 상태를 확인합니다.

```sql
-- 전체 세션 목록
SELECT * FROM v$session;

-- 현재 세션 수
SELECT COUNT(*) FROM v$session;

-- 활성 쿼리가 있는 세션
SELECT id, user_name, query, state
  FROM v$session
 WHERE state != 'IDLE';
```

## 설정 확인

```sql
-- 세션·네트워크 관련 파라미터 전체 확인
SELECT name, value
  FROM v$property
 WHERE name IN (
   'PORT_NO', 'HTTP_PORT_NO', 'MAX_SESSION_COUNT',
   'SESSION_IDLE_TIMEOUT_SEC', 'SESSION_QUERY_TIMEOUT_SEC',
   'GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS'
 )
 ORDER BY name;
```
