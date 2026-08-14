---
type: docs
title: '18.8.10 호환성 및 XMA protocol compatibility'
weight: 100
toc: true
---

XMA(eXtended Machbase Architecture) 프로토콜은 Machbase 서버와 클라이언트 드라이버(JDBC, ODBC, Python, Go 등) 사이의 통신 프로토콜입니다. 프로토콜 버전이 맞지 않으면 연결 실패나 기능 제한이 발생할 수 있습니다.

## 프로토콜 버전 호환 표

| 서버 버전 | 8.5 클라이언트 드라이버 | 8.7.0 클라이언트 드라이버 |
|-----------|:---------------------:|:---------------------:|
| **8.7.0 서버** | 제한적 호환 | 완전 호환 |
| **8.5 서버** | 완전 호환 | 하위 호환, 8.7.0 이름 API 미지원 |

- **완전 호환**: 모든 기능이 정상 동작합니다.
- **제한적 호환**: 기본 연결은 가능하나 8.7.0 신규 기능(AUTH KEY 확장 등)이 동작하지 않을 수 있습니다.
- **하위 호환**: 8.5 서버 범위의 기능만 사용 가능합니다.

## 8.7.0 XMA 프로토콜 주요 변경 사항

### AUTH KEY 인증 확장

8.7.0에서 AUTH KEY challenge 인증 프로토콜이 확장되었습니다.

- 지원 서명 방식: `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`
- 8.5 이하 드라이버는 신규 서명 방식(`RSA_PSS`)을 지원하지 않을 수 있습니다.
- AUTH KEY 인증을 사용하는 경우 드라이버를 8.7.0으로 업데이트하십시오.

```text
-- AUTH KEY 등록 (서버)
ALTER USER app_user ADD AUTH KEY (
    KEY='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    VALID_BEFORE='2047-12-31'
);
```

### 연결 문자열 호환성

Machbase SQLCLI와 ODBC에서 AUTH KEY 관련 파라미터:

```ini
AUTH_MODE=CHALLENGE;
AUTH_KEY_FILE=./private_key.pem;
AUTH_SIG_SCHEME=ECDSA;
```

8.5 드라이버는 `AUTH_SIG_SCHEME` 파라미터를 무시할 수 있습니다.

### Nullable 메타데이터

8.7.0 서버와 8.7.0 클라이언트 SDK를 함께 사용하면 SELECT 결과 컬럼의 NULL 가능 여부를
`NO_NULLS`, `NULLABLE`, `UNKNOWN`의 세 상태로 확인할 수 있습니다. 정확한 Nullable
상태를 사용하려면 서버와 클라이언트 SDK가 모두 이 기능을 지원해야 합니다.

한쪽이 구버전이어도 연결과 쿼리는 기존 방식으로 동작하지만 Nullable 값은 다음과 같이
제한됩니다.

| SDK | 구버전 조합에서의 값 |
|-----|----------------------|
| Machbase SQLCLI | `SQLDescribeCol()`과 `SQLColAttribute()`는 `0`, IRD는 `2` |
| ODBC | `SQLDescribeCol()`과 `SQLColAttribute()`는 `0`, IRD는 `2` |
| JDBC | 기존 반환값 `0` |
| Node.js | `ColumnNullable.Unknown` (`2`) |
| Python | `None` |
| .NET | `DBNull.Value` |

구버전 조합에서 반환된 `0`은 실제 스키마의 `NOT NULL`을 보장하지 않을 수 있습니다.
애플리케이션이 Nullable 값에 따라 처리 방식을 결정한다면 서버와 SDK를 함께
업그레이드합니다. API별 사용법은
[Nullable 메타데이터 지원 범위](/dbms/development-tools-integration/#support-scope-sdk-nullable-metadata)를
참고합니다.

### Named Bind Parameter

Machbase 8.7.0에서 추가된 이름 기반 SDK API는 8.7.0 클라이언트와 서버가 함께 필요합니다.
기존 `?` positional Prepared Statement는 이전 버전 조합에서도 사용할 수 있습니다.

| 클라이언트와 서버 조합 | `?` positional | `:name` SQL과 ordinal bind | 이름 기반 SDK API |
|---|:---:|:---:|:---:|
| 8.7.0 클라이언트 + 8.7.0 서버 | O | O | O |
| 8.5 클라이언트 + 8.7.0 서버 | O | O | X |
| 8.7.0 클라이언트 + 8.5 서버 | O | 서버 구현 범위 | X |
| 8.5 클라이언트 + 8.5 서버 | O | 서버 구현 범위 | X |

8.5 클라이언트는 새 이름 setter를 제공하지 않지만, 8.7.0 서버가 해석한 `:name` SQL을
기존 ordinal API로 바인딩할 수 있습니다. 반대로 8.7.0 클라이언트의 이름 기반 API를 이전
서버에 사용하면 자동으로 SQL을 다시 작성하지 않고 unsupported 오류를 반환합니다.

| SDK | 이전 서버에서의 대표 오류 |
|---|---|
| C/C++ SQLCLI | SQLSTATE `HYC00` |
| JDBC | SQLSTATE `0A000` |
| Node.js/TypeScript | `ERR_MACHBASE_NAMED_BIND_UNSUPPORTED` |
| Python | PREPARE 전 `NotSupportedError`, SQLSTATE `0A000` |

Python API 2.4의 prepared cursor는 protocol 4.0.3 미만 연결에서 named marker를 서버에
PREPARE하기 전에 거부합니다. 이 오류는 cursor가 이미 보유한 cached statement를 해제하거나
교체하지 않습니다. 구형 서버를 계속 사용해야 하면 `%s` 또는 `?` positional marker를
사용합니다.

.NET의 `MachParameterCollection`은 파라미터를 client-side typed literal로 렌더링한 뒤
ExecDirect로 실행하므로 위 서버 Prepared Named Bind 호환 표의 이름 기반 SDK API에
포함하지 않습니다. 다만 `:name` marker 사용은 protocol 4.0.3 연결을 확인하며 이전
서버에서는 `MachException`을 반환합니다.

문법과 SDK별 사용법은
[Named Bind Parameter syntax](/dbms/reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/)를
참고하십시오.

## 드라이버 버전 확인

JDBC:

```java
Connection conn = DriverManager.getConnection(url, props);
DatabaseMetaData meta = conn.getMetaData();
System.out.println("Driver: " + meta.getDriverVersion());
```

Machbase SQLCLI와 ODBC:

```c
SQLGetInfo(conn, SQL_DRIVER_VER, buf, sizeof(buf), NULL);
```

## 업그레이드 권장 사항

1. 서버와 드라이버를 같은 메이저 버전(8.7.0)으로 함께 업그레이드하십시오.
2. 드라이버를 순차적으로 업그레이드하는 경우, 업그레이드 기간 동안 8.5 드라이버가 8.7.0 서버에 제한적으로 연결될 수 있음을 인지하십시오.
3. AUTH KEY 인증을 사용하는 경우 드라이버를 가장 먼저 업그레이드하십시오.
4. Nullable 메타데이터를 애플리케이션 로직에 사용하는 경우 서버와 SDK를 모두 8.7.0으로
   업그레이드하십시오.
5. Named Bind Parameter의 이름 기반 SDK API를 사용하는 경우 서버와 SDK를 모두 8.7.0으로
   업그레이드하십시오.
