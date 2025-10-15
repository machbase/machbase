---
title: API 보안
type: docs
weight: 60
---

## 키 & 토큰 생성

### 웹 UI

1. 좌측 메뉴에서 <img src="./img/key_icon.jpg" width=47 style="display:inline"> 아이콘을 선택합니다.

2. 상단 좌측 영역의 `+` 아이콘 <img src="./img/key_add_icon.jpg" width=221 style="display:inline">을 클릭합니다.

3. 고유한 “Client Id”를 입력하고 유효 기간을 설정합니다(기본값은 오늘 기준 3년).  
   “Generate” 버튼을 누르면 해당 클라이언트용 키 파일이 생성됩니다.

{{< figure src="./img/key_gen.jpg" width=927px >}}

4. “Download *.zip” 버튼을 클릭하거나 각 파일 내용을 복사해 저장합니다.  
   키는 다시 생성할 수 없으므로 이 단계가 유일한 백업 기회입니다.

### 셸 명령

`machbase-neo shell key` 서브커맨드를 통해 클라이언트 키와 토큰을 관리할 수 있습니다.

**등록된 인증 키와 토큰 조회**

```
machbase-neo shell key list
```

등록된 client-id와 유효 기간이 표시됩니다.

```
$ machbase-neo shell key list
┌────────┬──────────────────────┬───────────────────────────────┬───────────────────────────────┐
│ ROWNUM │ ID                   │ VALID FROM                    │ EXPIRE                        │
├────────┼──────────────────────┼───────────────────────────────┼───────────────────────────────┤
│      1 │ myid2                │ 2023-02-05 01:55:18 +0000 UTC │ 2033-02-02 01:55:18 +0000 UTC │
│      2 │ myid3                │ 2023-02-05 01:56:36 +0000 UTC │ 2033-02-02 01:56:36 +0000 UTC │
......
```

**기존 키/토큰 삭제**

```
machbase-neo shell key del <client-id>
```

```
$ machbase-neo shell key del myid2
deleted
```

**새 키/토큰 등록**

`machbase-neo shell key gen` 서브커맨드는 지정한 client-id에 대해 새로운 키와 토큰을 생성합니다.  
`--output` 옵션으로 저장 경로를 지정하면 해당 경로 아래에 키와 토큰이 생성됩니다.

```
machbase-neo shell key gen <client-id> --output <output_file>
```

예를 들어 client-id `myapp01`에 대한 새로운 키를 생성하면 `*_cert.pem`, `*_key.pem`, `*_token` 파일이 생성됩니다.

```
$ machbase-neo shell key gen myapp01 --output ./myapp01 
Save certificate ./myapp01_cert.pem
Save private key ./myapp01_key.pem
Save token ./myapp01_token
```

생성된 파일을 확인합니다.

```
$ ls -al ./mayapp01*
-rw-r--r--  1 eirny  staff  782 Feb 20 19:33 ./mayapp01_cert.pem
-rw-------  1 eirny  staff  390 Feb 20 19:33 ./mayapp01_key.pem
-rw-------  1 eirny  staff   81 Feb 20 19:33 ./mayapp01_token
```

- `*_cert.pem` : 서버가 서명한 클라이언트용 X.509 인증서
- `*_key.pem` : 클라이언트의 개인 키
- `*_token` : 클라이언트 토큰 문자열

토큰 기반 인증 시 `*_token` 파일의 내용을 사용합니다.

```
$ cat ./myapp01_token 
myapp01:b:d59310703c1ebf627f8b781fb50437326ec65b067257ebc72f07b12846761d17   
```

**서버 인증서**

서버 인증서를 내려받으려면 `machbase-neo shell key server-cert --output <경로>` 명령을 사용합니다.

```
machbase-neo shell key server-cert --output ./machbase-neo.crt
```

## HTTP 토큰 인증

machbase-neo HTTP API는 토큰 기반 인증을 지원합니다.

명령줄 옵션 `--http-enable-token-auth true` 또는 설정 파일에서 `EnableTokenAuth = true`로 설정하면, 모든 HTTP API 호출 시 사전에 등록된 토큰을 `Authorization` 헤더로 전송해야 합니다.

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

### 토큰을 사용하는 HTTP 클라이언트

토큰 파일 내용을 `Authorization: Bearer <token>` 헤더에 설정해 API를 호출합니다.

```
curl --output - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    -H "Authorization: Bearer `cat ./http-api-app01_token`"
```

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "wave.sin", 1675851592000000000, 0 ],
      [ "wave.cos", 1675851592000000000, 1 ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.866708ms"
}
```

`Authorization` 헤더를 생략하거나 잘못된 토큰을 사용하면 다음과 같이 거부됩니다.

```
curl --output - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    -H "Authorization: Bearer http-api-app01:b:intended-wrong-value"
```

올바르지 않은 토큰일 경우 `HTTP/1.1 401 Unauthorized`와 함께 다음과 같은 에러 메시지가 반환됩니다.

```json
{"success":false,"reason":"invalid token"}
```


## MQTT 토큰 인증

machbase-neo의 MQTT API 역시 토큰 기반 인증을 지원합니다.

명령줄에서 `--mqtt-enable-token-auth true` 옵션을 사용하거나 설정 파일에서 `EnableTokenAuth = true`로 지정하면, MQTT CONNECT 메시지에 사전에 등록한 client-id와 토큰(사용자명)을 포함해야 합니다.

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

### 토큰을 사용하는 MQTT 클라이언트

CONNECT 메시지의 `username`에 등록된 토큰을 사용하고 `password`는 비워 둡니다.

```
mosquitto_pub -h 127.0.0.1 -p 5653 \
    --username `cat ./mqtt-api-app01_token` \
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

## MQTT X.509 authentication

When machbase-neo starts with `--mqtt-enable-tls true` command line option or set `Tls.Enabled = true` in the configurationfile,
machbase-neo accepts TLS (a.k.a SSL) connections from clients. 
If TLS is enabled, it ignores token based authentication and accepts only connection that finished ssl-handshaking successfully 
with pre-registered X.509 certificates.

{{< callout >}}
When TLS option is applied, machbase-neo mqtt server ignores `username` and `password` fields of CONNECT message.
Do not specify those values. But still need to set `client-id` for the clarity.
{{< /callout >}}

### MQTT client using X.509

A client should use the pre-registered client-id and key and certificate those were generated as the above section.
Apply client-id for the `client-id` of CONNECT message and do not set the `username` and `password`.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    --id myapp01            \
    --cert ./myapp01_cert.pem \
    --key ./myapp01_key.pem   \
    --cafile ./machbase-neo.crt --insecure \
    -t db/append/EXAMPLE            \
    -m '[ "wave.pi", `date +%s000000000`, 3.1415]'
```

- `--id` apply `client-id` that was used for generating key
- `--cert` client's certifcate file which was generated as `*_cert.pem`
- `--key` client's key file that was generated as `*_key.pem`
- `--cafile` set server's certificate since the client's certificate is singed by server. see below to know how to get this file.
- `--insecure` additionally required because server's certificate is self-signed one.
