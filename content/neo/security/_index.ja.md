---
toc: true
title: APIセキュリティ
type: docs
weight: 60
---

トークンは、HTTP APIとMQTTクライアントの認証に使用します。
生成したキー（X.509）は、MQTTのTLS接続に使用します。

## トークンの生成

1. 左側のメニューで<img src="/neo/security/img/key_icon.jpg" width=47 style="display:inline">アイコンを選択します。

2. 左上の領域で`+`アイコン<img src="/neo/security/img/token_add_icon.jpg" width=216 style="display:inline">をクリックします。

3. 管理用の「Name」を入力し、有効期間を設定します（既定値は今日から10年間）。

4. 「Issue token」ボタンを押すと、APIトークンが生成されます。

{{< figure src="/neo/security/img/token_gen.jpg" width=509px >}}

5. 生成したトークンをコピーできるのは、この画面が最後です。画面を閉じると同じトークンを再表示できません。

{{< figure src="/neo/security/img/token_gen_result.jpg" width=509px >}}

6. Web UIと同様に、シェルコマンドでもトークンを生成・管理できます。
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

## X.509証明書の生成

1. 左側のメニューで<img src="/neo/security/img/key_icon.jpg" width=47 style="display:inline">アイコンを選択します。

2. 左中央の領域で`+`アイコン<img src="/neo/security/img/cert_add_icon.jpg" width=192 style="display:inline">をクリックします。

3. 管理用の「Name」、「Type」、有効期間を設定します（既定値は今日から10年間）。

4. 「Generate certificate」ボタンを押すと、証明書が生成されます。

{{< figure src="/neo/security/img/cert_gen.jpg" width=512px >}}

5. 「Download *.zip」ボタンをクリックするか、各ファイルの内容をコピーして保存します。
生成した証明書をダウンロードできるのは、この画面が最後です。画面を閉じると同じ証明書を再生成できません。

{{< figure src="/neo/security/img/cert_gen_result.jpg" width=512px >}}

6. Web UIと同様に、シェルコマンドでも証明書を生成・管理できます。
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

**新しいキーの登録**

たとえば、client-id `myapp01`の新しいキーを生成して`myapp001.zip`をダウンロードすると、
アーカイブには`myapp001_cert.pem`、`myapp001_key.pem`、`server.pem`が含まれています。

```
$ ls -al ./mayapp01*
-rw-r--r--  1 eirny  staff  936 Feb 20 19:33 ./mayapp01_cert.pem
-rw-------  1 eirny  staff  227 Feb 20 19:33 ./mayapp01_key.pem
-rw-------  1 eirny  staff 1119 Feb 20 19:33 ./server.pem
```

- `*_cert.pem` : サーバーが署名したクライアント用のX.509証明書
- `*_key.pem` : クライアントの秘密鍵
- `server.pem` : サーバーのX.509証明書

## HTTPのトークン認証 {#http-토큰-인증}

machbase-neoのHTTP APIは、トークン認証に対応しています。

サーバーの起動時にコマンドラインオプション`--http-enable-token-auth true`を指定すると、すべてのHTTP API呼び出しで登録済みのトークンを`Authorization`ヘッダーに送信する必要があります。`--http-enable-token-auth`の設定と、`Authorization`ヘッダーへのトークン指定の有無によるサーバーの動作は、次のとおりです。

| `--http-enable-token-auth` | `Authorization`ヘッダー | サーバーの動作                       |
|:---------------------------|:-----------------------:|:-------------------------------------|
| true                       | あり                    | トークン発行者の権限で動作           |
|                            | なし                    | 401 Unauthorized                     |
| false（または未指定）      | あり                    | トークン発行者の権限で動作           |
|                            | なし                    | `sys`権限で動作                      |

```
machbase-neo serve --http-enable-token-auth true
```

サーバーの起動ログで、HTTPトークン認証が有効になったことを確認できます。

```
......
2023/02/20 20:14:29.878 INFO  neo neosvr           HTTP token authentication enabled
2023/02/20 20:14:29.878 INFO  neo neosvr           HTTP Listen tcp://127.0.0.1:5654
......
```

### トークンを使用するHTTPクライアント {#토큰-사용-http-클라이언트}

トークンを`Authorization: Bearer <token>`ヘッダーに設定して、APIを呼び出します。

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

サーバーに`--http-enable-token-auth true`を指定している場合、`Authorization`ヘッダーを省略するか、不正なトークンを使用すると、次のように拒否されます。

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

トークンが不正な場合は、`HTTP/1.1 401 Unauthorized`と以下のエラーメッセージが返されます。

```json
{"success":false, "reason":"missing valid token"}
```


## MQTTのトークン認証 {#mqtt-토큰-인증}

machbase-neoのMQTT APIも、トークン認証に対応しています。

サーバーで`--mqtt-enable-token-auth true`を使用すると、MQTT CONNECTメッセージのMQTT UserNameに登録済みのトークンを指定する必要があります。

```
machbase-neo serve --mqtt-enable-token-auth true
```

サーバーログで、MQTTトークン認証が有効になったことを確認できます。

```
......
2023/02/21 13:43:11.178 INFO  neosvr           MQTT token authentication enabled
2023/02/21 13:43:11.180 INFO  mqtt-tcp         MQTT Listen tcp://127.0.0.1:5653
......
```

### トークンを使用するMQTTクライアント {#토큰-사용-mqtt-클라이언트}

CONNECTメッセージの`username`に登録済みのトークンを使用し、`password`は空にします。

```
mosquitto_pub -h 127.0.0.1 -p 5653 \
  --username nt_5_gbXSqzkwdpyV3sYF1gFBvPQBpOxXjAu4d3RIsWGqJiH \
    -t db/write/EXAMPLE            \
    -m "[\"wave.pi\", $(date +%s)000000000, 3.1415]"
```

正しいトークンを指定しない場合、サーバーはCONNECTメッセージを拒否します。

```
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/write/EXAMPLE \
    -m "[\"wave.pi\", $(date +%s)000000000, 3.1415]"

Connection error: Connection Refused: not authorized.
Error: The connection was refused.
```

## MQTTのX.509認証 {#mqtt-x509-인증}

machbase-neoをコマンドラインオプション`--mqtt-enable-tls true`、または設定ファイルの`Tls.Enabled = true`で起動すると、
クライアントからTLS（SSLとも呼ばれる）接続を受け付けます。
TLSが有効な場合、トークン認証は無視し、登録済みのX.509証明書でSSLハンドシェイクに成功した接続だけを許可します。

{{< callout >}}
TLSオプションを適用すると、machbase-neoのMQTTサーバーは、CONNECTメッセージの`username`と`password`フィールドを無視します。
これらの値は指定しないでください。ただし、明確に識別するために`client-id`は引き続き設定してください。
{{< /callout >}}

### X.509を使用するMQTTクライアント {#x509-사용-mqtt-클라이언트}

クライアントは、前述の手順で生成・登録したclient-id、キー、証明書を使用する必要があります。
CONNECTメッセージの`client-id`には登録したclient-idを設定し、`username`と`password`は設定しないでください。


```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    --id myapp01            \
    --cert ./myapp01_cert.pem \
    --key ./myapp01_key.pem   \
    --cafile ./machbase-neo.crt --insecure \
    -t db/append/EXAMPLE            \
    -m "[\"wave.pi\", $(date +%s)000000000, 3.1415]"
```

- `--id` キーの生成時に使用した`client-id`を指定します
- `--cert` `*_cert.pem`として生成されたクライアント証明書ファイルです
- `--key` `*_key.pem`として生成されたクライアントキーファイルです
- `--cafile` クライアント証明書はサーバーが署名しているため、サーバー証明書を指定します。取得方法は前述のサーバー証明書の説明を参照してください。
- `--insecure` サーバー証明書のホスト名検証を省略します。この例では、証明書の名前と接続先ホスト名が一致しない場合に指定します。
