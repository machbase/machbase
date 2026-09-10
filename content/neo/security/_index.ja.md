---
toc: true
title: APIセキュリティ
type: docs
weight: 60
---

トークンは、HTTP APIとMQTTクライアントの認証に使用します。
生成したキー（X.509）は、MQTTのTLS接続とgRPC接続に使用します。

## キーとトークンの生成 {#키--토큰-생성}

### Web UI {#웹-ui}

1. 左側のメニューで<img src="/neo/security/img/key_icon.jpg" width=47 style="display:inline">アイコンを選択します。

2. 左上の領域で`+`アイコン<img src="/neo/security/img/key_add_icon.jpg" width=221 style="display:inline">をクリックします。

3. 一意の「Client Id」を入力し、有効期間を設定します（既定値は今日から3年間）。  
   「Generate」ボタンを押すと、クライアント用のキーファイルが生成されます。

{{< figure src="/neo/security/img/key_gen.jpg" width=927px >}}

4. 「Download *.zip」ボタンをクリックするか、各ファイルの内容をコピーして保存します。  
   同じキーを再生成することはできないため、この段階で必ずバックアップしてください。

### シェルコマンド {#셸-명령}

`machbase-neo shell key`サブコマンドで、クライアントのキーとトークンを管理できます。

**登録済みの認証キーとトークンの一覧**

```
machbase-neo shell key list
```

登録済みのclient-idと有効期間を表示します。

```
$ machbase-neo shell key list
┌────────┬──────────────────────┬───────────────────────────────┬───────────────────────────────┐
│ ROWNUM │ ID                   │ VALID FROM                    │ EXPIRE                        │
├────────┼──────────────────────┼───────────────────────────────┼───────────────────────────────┤
│      1 │ myid2                │ 2023-02-05 01:55:18 +0000 UTC │ 2033-02-02 01:55:18 +0000 UTC │
│      2 │ myid3                │ 2023-02-05 01:56:36 +0000 UTC │ 2033-02-02 01:56:36 +0000 UTC │
......
```

**既存のキー・トークンの削除**

```
machbase-neo shell key del <client-id>
```

```
$ machbase-neo shell key del myid2
deleted
```

**新しいキー・トークンの登録**

`machbase-neo shell key gen`サブコマンドは、指定したclient-idに新しいキーとトークンを生成します。  
`--output`オプションで保存先を指定すると、そのパスにキーとトークンを生成します。

```
machbase-neo shell key gen <client-id> --output <output_file>
```

たとえば、client-id `myapp01`の新しいキーを生成すると、`*_cert.pem`、`*_key.pem`、`*_token`ファイルが作成されます。

```
$ machbase-neo shell key gen myapp01 --output ./myapp01 
Save certificate ./myapp01_cert.pem
Save private key ./myapp01_key.pem
Save token ./myapp01_token
```

生成したファイルを確認します。

```
$ ls -al ./mayapp01*
-rw-r--r--  1 eirny  staff  782 Feb 20 19:33 ./mayapp01_cert.pem
-rw-------  1 eirny  staff  390 Feb 20 19:33 ./mayapp01_key.pem
-rw-------  1 eirny  staff   81 Feb 20 19:33 ./mayapp01_token
```

- `*_cert.pem` : サーバーが署名したクライアント用のX.509証明書
- `*_key.pem` : クライアントの秘密鍵
- `*_token` : クライアントのトークン文字列

トークン認証では、`*_token`ファイルの内容を使用します。

```
$ cat ./myapp01_token 
myapp01:b:d59310703c1ebf627f8b781fb50437326ec65b067257ebc72f07b12846761d17   
```

**サーバー証明書**

サーバー証明書を取得するには、`machbase-neo shell key server-cert --output <パス>`コマンドを使用します。

```
machbase-neo shell key server-cert --output ./machbase-neo.crt
```

## HTTPのトークン認証 {#http-토큰-인증}

machbase-neoのHTTP APIは、トークン認証に対応しています。

コマンドラインで`--http-enable-token-auth true`を指定するか、設定ファイルで`EnableTokenAuth = true`にすると、すべてのHTTP API呼び出しで登録済みのトークンを`Authorization`ヘッダーに送信する必要があります。

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

トークンファイルの内容を`Authorization: Bearer <token>`ヘッダーに設定して、APIを呼び出します。

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

`Authorization`ヘッダーを省略するか、不正なトークンを使用すると、以下のように拒否されます。

```
curl --output - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    -H "Authorization: Bearer http-api-app01:b:intended-wrong-value"
```

トークンが不正な場合は、`HTTP/1.1 401 Unauthorized`と以下のエラーメッセージが返されます。

```json
{"success":false,"reason":"invalid token"}
```


## MQTTのトークン認証 {#mqtt-토큰-인증}

machbase-neoのMQTT APIも、トークン認証に対応しています。

コマンドラインで`--mqtt-enable-token-auth true`を指定するか、設定ファイルで`EnableTokenAuth = true`にすると、MQTT CONNECTメッセージに登録済みのclient-idとトークン（ユーザー名）を含める必要があります。

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
    --username `cat ./mqtt-api-app01_token` \
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
