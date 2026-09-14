---
title: API Security
type: docs
weight: 60
---

The tokens are used for HTTP API and MQTT client authentication.
The generated keys (X.509) are used for MQTT TLS connections.

## Generate a Token

1. Select the <img src="/neo/security/img/key_icon.jpg" width=47 style="display:inline"> icon from the left menu.

2. Click the `+` icon <img src="/neo/security/img/token_add_icon.jpg" width=216 style="display:inline"> in the upper-left area.

3. Enter a "Name" for management and set the validity period (the default is 10 years from today).

4. Click the "Issue token" button to generate an API token.

{{< figure src="/neo/security/img/token_gen.jpg" width=509px >}}

5. This is your last chance to copy the generated token. It cannot be displayed again after you close the screen.

{{< figure src="/neo/security/img/token_gen_result.jpg" width=509px >}}

6. You can generate and manage tokens from the shell just as you can in the web UI.
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

## Generate an X.509 Certificate

1. Select the <img src="/neo/security/img/key_icon.jpg" width=47 style="display:inline"> icon from the left menu.

2. Click the `+` icon <img src="/neo/security/img/cert_add_icon.jpg" width=192 style="display:inline"> in the center-left area.

3. Set a "Name" for management, the "Type", and the validity period (the default is 10 years from today).

4. Click the "Generate certificate" button to generate a certificate.

{{< figure src="/neo/security/img/cert_gen.jpg" width=512px >}}

5. Click the "Download *.zip" button, or copy and save the contents of each file.
This is your last chance to download the generated certificate. The same certificate cannot be generated again after you close the screen.

{{< figure src="/neo/security/img/cert_gen_result.jpg" width=512px >}}

6. You can generate and manage certificates from the shell just as you can in the web UI.
  - `key gen <name>`
  - `key list`
  - `key del <id>`

```sh
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

**Registering a New Key**

For example, if you generate a new key for the client ID `myapp01` and download `myapp001.zip`,
the archive contains `myapp001_cert.pem`, `myapp001_key.pem`, and `server.pem`.

```
$ ls -al ./mayapp01*
-rw-r--r--  1 eirny  staff  936 Feb 20 19:33 ./mayapp01_cert.pem
-rw-------  1 eirny  staff  227 Feb 20 19:33 ./mayapp01_key.pem
-rw-------  1 eirny  staff 1119 Feb 20 19:33 ./server.pem
```

- `*_cert.pem`: the client X.509 certificate signed by the server
- `*_key.pem`: the client's private key
- `server.pem`: the server's X.509 certificate

## HTTP Token authentication

HTTP API of machbase-neo supports the token based authentication.

When starting the server with the `--http-enable-token-auth true` command-line option, every HTTP API call must send a pre-registered token in the `Authorization` header. The following table shows how the server behaves depending on the `--http-enable-token-auth` setting and whether the `Authorization` header contains a token.

| `--http-enable-token-auth` | `Authorization` header | Server behavior                        |
|:---------------------------|:----------------------:|:---------------------------------------|
| true                       | Present                | Uses the token issuer's privileges     |
|                            | Absent                 | 401 Unauthorized                       |
| false (or not set)         | Present                | Uses the token issuer's privileges     |
|                            | Absent                 | Uses `sys` privileges                   |

```
machbase-neo serve --http-enable-token-auth true
```

The starting log shows HTTP token authentication is enabled.

```
......
2023/02/20 20:14:29.878 INFO  neo neosvr           HTTP token authentication enabled
2023/02/20 20:14:29.878 INFO  neo neosvr           HTTP Listen tcp://127.0.0.1:5654
......
```

### HTTP Client using token

Set the token in the `Authorization: Bearer <token>` header when calling the API.

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

If the server is started with `--http-enable-token-auth true`, a request without an `Authorization` header or with an invalid token is rejected as follows.

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

If the token is invalid, the server returns `HTTP/1.1 401 Unauthorized` with the following error message.

```json
{"success":false, "reason":"missing valid token"}
```


## MQTT Token authentication

MQTT API of machbase-neo supports the token based authentication.

When the server uses `--mqtt-enable-token-auth true`, the MQTT CONNECT message must include a pre-registered token as the MQTT UserName.

```
machbase-neo serve --mqtt-enable-token-auth true
```

The starting log shows MQTT token authentication is enabled.

```
......
2023/02/21 13:43:11.178 INFO  neosvr           MQTT token authentication enabled
2023/02/21 13:43:11.180 INFO  mqtt-tcp         MQTT Listen tcp://127.0.0.1:5653
......
```

### MQTT client using token

Use the registered token as the `username` in the CONNECT message, and leave the `password` field empty.

```
mosquitto_pub -h 127.0.0.1 -p 5653 \
  --username nt_5_gbXSqzkwdpyV3sYF1gFBvPQBpOxXjAu4d3RIsWGqJiH \
    -t db/write/EXAMPLE            \
    -m '[ "wave.pi", `date +%s000000000`, 3.1415]'
```

If a client does not provide the correct token in the `username` field, the server will reject the CONNECT message.

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

