---
type: docs
title: 'SDK별 AUTH KEY 지원 범위 안내'
weight: 20
---

Machbase는 사용자 이름/비밀번호 방식 외에 **AUTH KEY challenge 인증**을 지원합니다.
서버에는 사용자의 공개키를 등록하고, 클라이언트는 개인키 파일로 서버 challenge에
서명합니다. 비밀번호를 연결 문자열에 넣지 않고 키 기반으로 접속할 때 사용합니다.

## AUTH KEY 인증 방식 개요

1. 서버 사용자에 공개키를 AUTH KEY로 등록합니다.
2. 클라이언트가 `AUTH_MODE=CHALLENGE`로 연결을 요청합니다.
3. 서버가 challenge 값을 보냅니다.
4. 클라이언트가 `AUTH_KEY_FILE` 개인키로 challenge에 서명합니다.
5. 서버가 등록된 공개키로 서명을 검증하고 연결을 허용합니다.

지원되는 서명 방식은 `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`입니다. 키 파일만으로 방식을
추론할 수 있는 경우에는 `AUTH_SIG_SCHEME`을 생략할 수 있습니다.

## AUTH KEY 등록과 조회

사용자를 생성할 때 공개키를 함께 등록할 수 있습니다.

```text
CREATE USER app_auth_key
WITH AUTH KEY (
    KEY='-----BEGIN RSA PUBLIC KEY-----\n...\n-----END RSA PUBLIC KEY-----\n',
    VALID_BEFORE='2047-12-31',
    COMMENT='key only user'
);
```

기존 사용자에 AUTH KEY를 추가할 수도 있습니다.

```text
ALTER USER app_auth_key ADD AUTH KEY (
    KEY='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    VALID_BEFORE='2047-12-31',
    COMMENT='second key'
);
```

등록된 키는 `V$USER_AUTH_KEYS`에서 확인합니다.

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
FROM v$user_auth_keys
WHERE user_name = 'APP_AUTH_KEY'
ORDER BY key_id;
```

키를 비활성화, 활성화, 삭제할 때는 `key_id`를 지정합니다.

```text
ALTER USER app_auth_key DEACTIVATE AUTH KEY ID 3;
ALTER USER app_auth_key ACTIVATE AUTH KEY ID 3;
ALTER USER app_auth_key DROP AUTH KEY ID 3;
```

## SDK별 AUTH KEY 인증 지원 현황

| SDK | AUTH KEY 지원 | 설정 방법 |
|-----|:------------:|-----------|
| **machsql** | O | `-K <private-key-file>`, `--auth-sig-scheme` |
| **ODBC / CLI** | O | 연결 문자열 `AUTH_MODE`, `AUTH_KEY_FILE`, `AUTH_SIG_SCHEME` |
| **JDBC** | O | JDBC Properties 또는 URL 속성 |
| **Go / Python / Node.js / .NET** | X | 현재 드라이버 연결 옵션에 challenge 인증 설정 없음 |
| **REST API** | 별도 방식 | `HTTP_AUTH` 기반 Basic Authentication 설정 사용 |

## machsql 예제

```bash
cat > /tmp/auth_key_check.sql <<'SQL'
SELECT COUNT(*) FROM v$tables;
SQL

machsql -s 127.0.0.1 -P 5656 \
  -u app_auth_key \
  -K ./auth_ecdsa_p256.pem \
  --auth-sig-scheme=ECDSA \
  -i -f /tmp/auth_key_check.sql
```

RSA 키를 사용할 때는 서명 방식을 지정합니다.

```bash
machsql -s 127.0.0.1 -P 5656 \
  -u app_auth_key \
  -K ./auth_rsa_2048.pem \
  --auth-sig-scheme=RSA_PSS \
  -i -f /tmp/auth_key_check.sql
```

## ODBC / CLI 연결 문자열

```ini
SERVER=127.0.0.1;
UID=APP_AUTH_KEY;
CONNTYPE=1;
PORT_NO=5656;
NLS_USE=UTF8;
TIMEZONE=+0900;
AUTH_MODE=CHALLENGE;
AUTH_KEY_FILE=./auth_ecdsa_p256.pem;
AUTH_SIG_SCHEME=ECDSA;
```

`AUTH_MODE=CHALLENGE`를 지정하면 `AUTH_KEY_FILE`이 필수입니다. 잘못된 파일 경로,
키와 맞지 않는 `AUTH_SIG_SCHEME`, 등록되지 않은 사용자 키는 연결 실패로 처리됩니다.

## JDBC 예제

```java
Properties props = new Properties();
props.setProperty("user", "app_auth_key");
props.setProperty("AUTH_MODE", "CHALLENGE");
props.setProperty("AUTH_KEY_FILE", "/path/to/auth_ecdsa_p256.pem");
props.setProperty("AUTH_SIG_SCHEME", "ECDSA");

String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";
Connection conn = DriverManager.getConnection(url, props);
```

키 알고리즘으로 서명 방식을 추론할 수 있는 경우에는 `AUTH_SIG_SCHEME`을 생략할 수
있습니다.

## REST API와 AUTH KEY

이 페이지의 AUTH KEY challenge 인증은 DB 포트(기본 5656)에 접속하는 드라이버/CLI
인증 방식입니다. REST API(기본 5657)는 별도의 로그인 토큰 발급 엔드포인트나 Bearer
토큰 교환 방식으로 AUTH KEY를 처리하지 않습니다. REST API 인증은 `machbase.conf`의
`HTTP_AUTH` 설정에 따라 Basic Authentication을 사용합니다.

## 보안 권장 사항

1. 개인키 파일은 파일 권한을 제한하고 애플리케이션 설정 또는 시크릿 관리 도구로
   배포합니다.
2. 공개키는 사용자별로 등록하고, 사용하지 않는 키는 `DEACTIVATE` 또는 `DROP`합니다.
3. `VALID_BEFORE`를 설정해 키 만료 시점을 운영 정책에 맞게 관리합니다.
4. 네트워크 구간 보호가 필요한 환경에서는 TLS/SSL 터널 또는 보안 네트워크와 함께
   사용합니다.
