---
title: API 보안
type: docs
weight: 60
---

토큰은 HTTP API와 MQTT 클라이언트 인증에 사용됩니다.
생성된 키(X.509)는 MQTT TLS 연결에 사용됩니다.

## 토큰 생성

1. 좌측 메뉴에서 <img src="/neo/security/img/key_icon.jpg" width=47 style="display:inline"> 아이콘을 선택합니다.

2. 상단 좌측 영역의 `+` 아이콘 <img src="/neo/security/img/token_add_icon.jpg" width=216 style="display:inline">을 클릭합니다.

3. 관리를 위한 이름 "Name"을 입력하고 유효 기간을 설정합니다 (기본값은 오늘 기준 10년).

4. "Issue token" 버튼을 누르면 API 토큰이 생성됩니다.

{{< figure src="/neo/security/img/token_gen.jpg" width=509px >}}

5. 생성된 토큰을 복사할 수 있는 마지막 기회이며 화면을 닫으면 동일한 토큰을 다시 생성할 수 없습니다.

{{< figure src="/neo/security/img/token_gen_result.jpg" width=509px >}}

6. 쉘에서 명령어로 웹 GUI에서 처럼 토큰을 생성/관리할 수 있습니다.
  - `token gen <name>`
  - `token list`
  - `token del <id>`

```sh
sys machbase-neo 2026-09-14 09:46:43
> token gen "my api token";
nt_4_9jShk5SlIimfUFzN3OSfCGLAccVx3U3erqGxPPgitoL

> token list;
┌────────┬────┬─────────────────┬──────┬───────────────────┬─────────────────────┬─────────────────────┬───────────┐
│ ROWNUM │ ID │ NAME            │ USER │ TOKEN             │ CREATED             │ EXPIRES             │ LAST USED │
├────────┼────┼─────────────────┼──────┼───────────────────┼─────────────────────┼─────────────────────┼───────────┤
│      2 │  4 │ my api token    │ SYS  │ nt_4_9jSh****itoL │ 2026-09-14 09:47:03 │ 2036-09-14 09:47:03 │           │
└────────┴────┴─────────────────┴──────┴───────────────────┴─────────────────────┴─────────────────────┴───────────┘

> token del 4;
Token deleted successfully.
```

## X.509 인증서 생성

1. 좌측 메뉴에서 <img src="/neo/security/img/key_icon.jpg" width=47 style="display:inline"> 아이콘을 선택합니다.

2. 좌측 중앙 영역의 `+` 아이콘 <img src="/neo/security/img/cert_add_icon.jpg" width=192 style="display:inline">을 클릭합니다.

3. 관리를 위한 이름 "Name"과 유형 "Type" 그리고 유효 기간을 설정합니다 (기본값은 오늘 기준 10년).

4. "Generate certificate" 버튼을 누르면 인증서가 생성됩니다.

{{< figure src="/neo/security/img/cert_gen.jpg" width=512px >}}

5. “Download *.zip” 버튼을 클릭하거나 각 파일 내용을 복사해 저장합니다.
생성된 인증서를 다운로드할 수 있는 마지막 기회이며 화면을 닫으면 동일한 인증서를 다시 생성할 수 없습니다.

{{< figure src="/neo/security/img/cert_gen_result.jpg" width=512px >}}

6. 쉘에서 명령어로 웹 GUI에서 처럼 인증서를 생성/관리할 수 있습니다.
  - `key gen <name>`
  - `key list`
  - `key del <id>`

```sh

sys machbase-neo 2026-09-14 09:48:33
sys machbase-neo 2026-09-14 13:06:03
> key gen -t ecdsa "my_client_cert";
id=2
-----BEGIN CERTIFICATE-----
MIICjjCCAfCgAwIBAgIRAM6q5O9/ly2HshwRM4wzOPcwCgYIKoZIzj0EAwQwgZIx
CzAJBgNVBAYTAkNBMREwDwYDVQQHEwhTYW4gSm9zZTEdMBsGA1UECQwUMzAwMyBO
IEZpcnN0IFN0ICMyMDYxDjAMBgNVBBETBTk1MTM0MRUwEwYDVQQKEwxtYWNoYmFz
ZS5jb20xEzARBgNVBAsMClImRCBDZW50ZXIxFTATBgNVBAMTDG1hY2hiYXNlLW5l
bzAeFw0yNjA5MTQwNDA2MDlaFw0zNjA5MTEwNDA2MDlaMBcxFTATBgNVBAMMDGFu
b3RoZXJfY2VydDBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABOIr0Uj+d8cI2bOT
+TLaDsxKtkmA7s1KGXMgsISg5iHFvSO1W205z6wPrzfaUHP3QFBTtCRbUD7UFokL
R6WiEYGjgaAwgZ0wDgYDVR0PAQH/BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMC
BggrBgEFBQcDATAMBgNVHRMBAf8EAjAAMB8GA1UdIwQYMBaAFOljpIF4iVCNw3br
tW/Ds4lv4Jb7MD0GA1UdEQQ2MDSCDGFub3RoZXJfY2VydIYkdXJuOm1hY2hiYXNl
Om5lbzpjbGllbnQ6YW5vdGhlcl9jZXJ0MAoGCCqGSM49BAMEA4GLADCBhwJBAjCp
PUwvoaRrlZB8Zu/FW4SSXVugmDQBPpDpBBN/nbvbKAMAi3n/fvFswp6dfLgD1APo
KGiHGonXG0Rpx0uXFgsCQgDlAFVwAY+S6bpdRIRYV0neA7fqnqfPxo4HV3otfd5p
iLHmOUgNxuFfq/C0qKwk2R07mNWtl437HwdUUGb0po0qGA==
-----END CERTIFICATE-----

-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIGvf58K/e7FmQW74ZCv5gCvKnBeDemTkM83eD2V/cHuroAoGCCqGSM49
AwEHoUQDQgAE4ivRSP53xwjZs5P5MtoOzEq2SYDuzUoZcyCwhKDmIcW9I7VbbTnP
rA+vN9pQc/dAUFO0JFtQPtQWiQtHpaIRgQ==
-----END EC PRIVATE KEY-----


Caution:
  This is the last chance to copy and store the PRIVATE KEY.
  It will not be shown again.

> key list;
┌────────┬────┬────────────────┬─────────────────────┬─────────────────────┐
│ ROWNUM │ ID │ NAME           │ NOT VALID BEFORE    │ NOT VALID AFTER     │
├────────┼────┼────────────────┼─────────────────────┼─────────────────────┤
│      1 │  2 │ my_client_cert │ 2026-09-14 12:57:33 │ 2036-09-11 12:57:33 │
└────────┴────┴────────────────┴─────────────────────┴─────────────────────┘

> key del 2;
Key deleted successfully.
```

**새 키/토큰 등록**

예를 들어 client-id `myapp01`에 대한 새로운 키를 생성하고 `myapp001.zip`파일을 다운로드 받으면
그 안에는 `myapp001_cert.pem`, `myapp001_key.pem`과 `server.pem` 파일이 포함되어 있습니다.

```
$ ls -al ./mayapp01*
-rw-r--r--  1 eirny  staff  936 Feb 20 19:33 ./mayapp01_cert.pem
-rw-------  1 eirny  staff  227 Feb 20 19:33 ./mayapp01_key.pem
-rw-------  1 eirny  staff 1119 Feb 20 19:33 ./server.pem
```

- `*_cert.pem` : 서버가 서명한 클라이언트용 X.509 인증서
- `*_key.pem`  : 클라이언트의 개인 키
- `server.pem` : 서버의 X.509 인증서

## HTTP 토큰 인증

machbase-neo HTTP API는 토큰 기반 인증을 지원합니다.

서버를 시작할 때 명령줄 옵션 `--http-enable-token-auth true`를 설정하면, 모든 HTTP API 호출 시 사전에 등록된 토큰을 `Authorization` 헤더로 전송해야 합니다. `--http-enable-token-auth`를 설정과 `Authorization` 헤더에 토큰 지정 여부에 따른 서버 동작은 아래의 표와 같습니다.


| `--http-enable-token-auth` | `Authorization` 헤더 | 서버 응답             |
|:---------------------------|:------------------:|:---------------------|
| true                       | O                  | 토큰 발급자의 권한으로 동작 |
|                            | X                  | 401 Unauthorized     |
| false (or not set)         | O                  | 토큰 발급자의 권한으로 동작 |
|                            | X                  | sys 권한으로 동작       |

```
machbase-neo serve --http-enable-token-auth true
```

서버 시작 로그에서 HTTP 토큰 인증이 활성화되었음을 확인할 수 있습니다.

```
......
2023/02/20 20:14:29.878 INFO  neo neosvr           HTTP token authentication enabled
2023/02/20 20:14:29.878 INFO  neo neosvr           HTTP Listen tcp://127.0.0.1:5654
......
```

### 토큰 사용 HTTP 클라이언트

토큰 파일 내용을 `Authorization: Bearer <token>` 헤더에 설정해 API를 호출합니다.

{{< tabs >}}
{{< tab name="HTTP" >}}

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select current_user()
Authorization: Bearer nt_5_gbXSqzkwdpyV3sYF1gFBvPQBpOxXjAu4d3RIsWGqJiH
```
~~~

{{< /tab >}}
{{< tab name="cURL" >}}
```
curl --output - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select current_user()" \
    -H "Authorization: Bearer nt_5_gbXSqzkwdpyV3sYF1gFBvPQBpOxXjAu4d3RIsWGqJiH"
```
{{< /tab >}}
{{< /tabs >}}

```json
{
  "data": {
    "columns": [ "current_user()" ],
    "types": [ "string" ],
    "rows": [
      [ "SYS" ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "492.25µs"
}
```

서버에 `--http-enable-token-auth true`를 설정한 상태에서 `Authorization` 헤더를 생략하거나 잘못된 토큰을 사용하면 다음과 같이 거부됩니다.

{{< tabs >}}
{{< tab name="HTTP" >}}

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select current_user()
Authorization: Bearer intended-wrong-value
```
~~~

{{< /tab >}}
{{< tab name="cURL" >}}
```
curl --output - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select current_user()" \
    -H "Authorization: Bearer intended-wrong-value"
```
{{< /tab >}}
{{< /tabs >}}

올바르지 않은 토큰일 경우 `HTTP/1.1 401 Unauthorized`와 함께 다음과 같은 에러 메시지가 반환됩니다.

```json
{"success":false, "reason":"missing valid token"}
```


## MQTT 토큰 인증

machbase-neo의 MQTT API 역시 토큰 기반 인증을 지원합니다.

서버에 `--mqtt-enable-token-auth true` 를 사용하면, MQTT CONNECT 메시지에 사전에 등록한 토큰을 MQTT UserName으로 포함해야 합니다.

```
machbase-neo serve --mqtt-enable-token-auth true
```

서버 로그에서 MQTT 토큰 인증이 활성화되었음을 확인할 수 있습니다.

```
......
2023/02/21 13:43:11.178 INFO  neosvr           MQTT token authentication enabled
2023/02/21 13:43:11.180 INFO  mqtt-tcp         MQTT Listen tcp://127.0.0.1:5653
......
```

### 토큰 사용 MQTT 클라이언트

CONNECT 메시지의 `username`에 등록된 토큰을 사용하고 `password`는 비워 둡니다.

```
mosquitto_pub -h 127.0.0.1 -p 5653 \
    --username nt_5_gbXSqzkwdpyV3sYF1gFBvPQBpOxXjAu4d3RIsWGqJiH \
    -t db/write/EXAMPLE            \
    -m '[ "wave.pi", `date +%s000000000`, 3.1415]'
```

올바른 토큰을 제공하지 않으면 서버가 CONNECT 메시지를 거부합니다.

```
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/write/EXAMPLE \
    -m '[ "wave.pi", `date +%s000000000`, 3.1415]'

Connection error: Connection Refused: not authorized.
Error: The connection was refused.
```

## MQTT X.509 인증

machbase-neo는 `--mqtt-enable-tls true` 명령줄 옵션 또는 설정 파일에서 `Tls.Enabled = true`로 시작하면,
클라이언트로부터 TLS(일명 SSL) 연결을 수신합니다.
TLS가 활성화되면 토큰 기반 인증은 무시되며, 사전에 등록된 X.509 인증서로 SSL 핸드셰이크를 성공적으로 완료한 연결만 허용합니다.

{{< callout >}}
TLS 옵션이 적용되면 machbase-neo MQTT 서버는 CONNECT 메시지의 `username`과 `password` 필드를 무시합니다.
해당 값들을 지정하지 마십시오. 하지만 명확성을 위해 `client-id`는 여전히 설정해야 합니다.
{{< /callout >}}

### X.509 사용 MQTT 클라이언트

클라이언트는 위 섹션에서 생성한 사전 등록된 client-id와 키, 인증서를 사용해야 합니다.
CONNECT 메시지의 `client-id`에는 등록된 client-id를 적용하고, `username`과 `password`는 설정하지 마십시오.


```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    --id myapp01            \
    --cert ./myapp01_cert.pem \
    --key ./myapp01_key.pem   \
    --cafile ./machbase-neo.crt --insecure \
    -t db/append/EXAMPLE            \
    -m '[ "wave.pi", `date +%s000000000`, 3.1415]'
```

- `--id` 키 생성 시 사용한 `client-id`를 지정합니다
- `--cert` `*_cert.pem`으로 생성된 클라이언트 인증서 파일입니다
- `--key` `*_key.pem`으로 생성된 클라이언트 키 파일입니다
- `--cafile` 클라이언트 인증서가 서버에 의해 서명되었으므로 서버 인증서를 지정합니다. 이 파일을 얻는 방법은 아래를 참조하세요.
- `--insecure` 서버 인증서가 자체 서명되었기 때문에 추가로 필요합니다.
