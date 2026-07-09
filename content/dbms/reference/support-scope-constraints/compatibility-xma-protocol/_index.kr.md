---
type: docs
title: '17.8.10 호환성 및 XMA protocol compatibility'
weight: 100
---

XMA(eXtended Machbase Architecture) 프로토콜은 Machbase 서버와 클라이언트 드라이버(JDBC, ODBC, Python, Go 등) 사이의 통신 프로토콜입니다. 서버와 드라이버의 프로토콜 버전이 맞지 않으면 연결이 실패하거나 일부 기능이 동작하지 않을 수 있습니다.

## 프로토콜 버전 호환 표

| 서버 버전 | 8.5 클라이언트 드라이버 | 8.6 클라이언트 드라이버 |
|-----------|:---------------------:|:---------------------:|
| **8.6 서버** | 제한적 호환 | 완전 호환 |
| **8.5 서버** | 완전 호환 | 하위 호환 |

- **완전 호환**: 모든 기능이 정상 동작합니다.
- **제한적 호환**: 기본 연결은 가능하나 8.6 신규 기능(AUTH KEY 확장 등)이 동작하지 않을 수 있습니다.
- **하위 호환**: 8.5 서버 범위의 기능만 사용 가능합니다.

## 8.6 XMA 프로토콜 주요 변경 사항

### AUTH KEY 인증 확장

8.6에서 AUTH KEY challenge 인증 프로토콜이 확장되었습니다.

- 지원 서명 방식: `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`
- 8.5 이하 드라이버는 신규 서명 방식(`RSA_PSS`)을 지원하지 않을 수 있습니다.
- AUTH KEY 인증을 사용하는 경우 드라이버를 8.6으로 업데이트하세요.

```text
-- AUTH KEY 등록 (서버)
ALTER USER app_user ADD AUTH KEY (
    KEY='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    VALID_BEFORE='2047-12-31'
);
```

### 연결 문자열 호환성

ODBC/CLI에서 AUTH KEY 관련 파라미터:

```ini
AUTH_MODE=CHALLENGE;
AUTH_KEY_FILE=./private_key.pem;
AUTH_SIG_SCHEME=ECDSA;
```

8.5 드라이버는 `AUTH_SIG_SCHEME` 파라미터를 무시할 수 있습니다.

## 드라이버 버전 확인

JDBC:

```java
Connection conn = DriverManager.getConnection(url, props);
DatabaseMetaData meta = conn.getMetaData();
System.out.println("Driver: " + meta.getDriverVersion());
```

ODBC/CLI:

```c
SQLGetInfo(conn, SQL_DRIVER_VER, buf, sizeof(buf), NULL);
```

## 업그레이드 권장 사항

1. 서버와 드라이버를 같은 메이저 버전(8.6)으로 함께 업그레이드하세요.
2. 드라이버를 순차적으로 업그레이드하는 경우, 업그레이드 기간 동안 8.5 드라이버가 8.6 서버에 제한적으로 연결될 수 있음을 인지하세요.
3. AUTH KEY 인증을 사용하는 경우 드라이버를 가장 먼저 업그레이드하세요.
