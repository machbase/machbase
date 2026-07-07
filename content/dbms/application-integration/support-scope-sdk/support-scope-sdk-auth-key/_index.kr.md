---
type: docs
title: 'SDK별 AUTH KEY 지원 범위 안내'
weight: 20
---

Machbase Neo는 사용자 이름/비밀번호 방식 외에 **AUTH KEY** 기반 인증을 지원합니다. AUTH KEY는 challenge-response 메커니즘을 사용하여 네트워크에 비밀번호를 평문으로 전송하지 않도록 설계된 인증 방식입니다.

## AUTH KEY 인증 방식 개요

AUTH KEY 인증의 동작 원리는 다음과 같습니다.

1. 클라이언트가 서버에 연결을 요청합니다.
2. 서버가 랜덤 **challenge** 값을 클라이언트에 전송합니다.
3. 클라이언트는 AUTH KEY와 challenge를 조합하여 **HMAC-SHA256** 서명을 생성합니다.
4. 서버가 서명을 검증하여 연결을 허용합니다.

이 방식은 비밀번호가 네트워크에 노출되지 않으므로 일반 TCP 연결 환경에서도 높은 보안을 제공합니다.

## AUTH KEY 발급

Machbase Neo 서버에서 계정별 AUTH KEY를 발급합니다.

```sql
-- SYS 계정으로 접속 후 AUTH KEY 발급
ALTER USER SYS SET AUTHKEY ON;

-- 발급된 AUTH KEY 확인
SELECT AUTHKEY FROM V$USER WHERE NAME = 'SYS';
```

발급된 AUTH KEY는 Base64로 인코딩된 문자열로 반환됩니다.

## SDK별 AUTH KEY 인증 지원 현황

| SDK | AUTH KEY 지원 | 지원 버전 | 설정 방법 |
|-----|:------------:|-----------|-----------|
| **JDBC** | O | Machbase 8.0 이상 | JDBC URL 파라미터 또는 Properties |
| **ODBC / CLI** | O | Machbase 8.0 이상 | `SQLConnect` 파라미터 |
| **Python** | O | Machbase 8.0 이상 | `connect()` 파라미터 |
| **.NET** | O | Machbase 8.0 이상 | 연결 문자열 파라미터 |
| **Go (native)** | O | Machbase 8.0 이상 | `Open()` 옵션 |
| **Go (database/sql)** | O | Machbase 8.0 이상 | DSN 파라미터 |
| **Node.js** | △ | 버전 확인 필요 | 연결 옵션 |
| **REST API** | O | Machbase 8.0 이상 | `Authorization` 헤더 |

## JDBC: AUTH KEY 인증 설정

### URL 파라미터 방식

```java
// JDBC URL에 authkey 파라미터 추가
String url = "jdbc:machbase://127.0.0.1:5656/MACHBASE?authkey=<BASE64_AUTH_KEY>";

Connection conn = DriverManager.getConnection(url, "SYS", "");
```

### Properties 방식

```java
Properties props = new Properties();
props.setProperty("user", "SYS");
props.setProperty("authkey", "<BASE64_AUTH_KEY>");

String url = "jdbc:machbase://127.0.0.1:5656/MACHBASE";
Connection conn = DriverManager.getConnection(url, props);
```

> **주의**: AUTH KEY 방식 사용 시 `password` 파라미터는 무시됩니다. 비밀번호 대신 AUTH KEY가 인증에 사용됩니다.

## ODBC / CLI: AUTH KEY 인증 설정

ODBC 연결 문자열에 `AUTHKEY` 속성을 추가합니다.

```c
// SQLDriverConnect 방식
SQLCHAR connStr[] = 
    "DSN=Machbase;UID=SYS;AUTHKEY=<BASE64_AUTH_KEY>;";

SQLDriverConnect(conn, NULL, connStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT);
```

또는 `odbc.ini` / `odbcinst.ini` 에 설정합니다.

```ini
[Machbase]
Driver   = /usr/local/machbase/lib/libmachbase_odbc.so
Server   = 127.0.0.1
Port     = 5656
Database = MACHBASE
UID      = SYS
AuthKey  = <BASE64_AUTH_KEY>
```

## Python: AUTH KEY 인증 설정

```python
from machbaseAPI import connect

conn = connect(
    host='127.0.0.1',
    port=5656,
    user='SYS',
    authkey='<BASE64_AUTH_KEY>'
)

cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM sensor_data")
print(cur.fetchone())
conn.close()
```

## .NET: AUTH KEY 인증 설정

연결 문자열에 `AuthKey` 파라미터를 추가합니다.

```csharp
using Mach.Data.MachClient;

string connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;" +
                    "AUTHKEY=<BASE64_AUTH_KEY>;PROTOCOL=4.0-full";

using var conn = new MachConnection(connString);
conn.Open();
```

## Go (native): AUTH KEY 인증 설정

```go
package main

import (
    mach "github.com/machbase/neo-client/machrpc"
)

func main() {
    db, err := mach.Open(
        "127.0.0.1:5656",
        "SYS",
        "",
        mach.WithAuthKey("<BASE64_AUTH_KEY>"),
    )
    if err != nil {
        panic(err)
    }
    defer db.Close()
}
```

## REST API: AUTH KEY 인증 설정

REST API는 먼저 AUTH KEY를 사용하여 JWT 토큰을 발급받고, 이후 요청에 토큰을 사용합니다.

### 토큰 발급

```bash
# AUTH KEY로 로그인하여 JWT 토큰 발급
curl -X POST "http://localhost:5657/web/api/login" \
  -H "Content-Type: application/json" \
  -d '{
    "loginName": "SYS",
    "authKey": "<BASE64_AUTH_KEY>"
  }'
```

응답 예시:

```json
{
  "success": true,
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
}
```

### 토큰을 이용한 API 호출

```bash
# Authorization 헤더에 Bearer 토큰 포함
curl -G "http://localhost:5657/db/query" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  --data-urlencode "q=SELECT COUNT(*) FROM sensor_data"
```

## 보안 권장 사항

1. **AUTH KEY는 파일로 안전하게 보관**하고 코드에 하드코딩하지 마세요. 환경 변수나 시크릿 관리 도구(HashiCorp Vault, AWS Secrets Manager 등)를 사용하세요.
2. **TLS/SSL 연결**과 병행하면 더욱 강력한 보안을 제공합니다.
3. AUTH KEY는 **주기적으로 갱신**하고, 사용하지 않는 계정의 AUTH KEY는 비활성화합니다.

```bash
# 환경 변수에서 AUTH KEY 읽기 예시 (Python)
import os
from machbaseAPI import connect

auth_key = os.environ.get('MACHBASE_AUTH_KEY')
conn = connect(host='127.0.0.1', port=5656, user='SYS', authkey=auth_key)
```
