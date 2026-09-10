---
title: FLUID サーバー
weight: 160
toc: true
---

## FLUID server
リバースプロキシは、クライアントの要求を受けてサーバーへ転送し、その応答をクライアントへ返す
仲介サーバーです。サーバーの負荷分散やセキュリティ強化などに利用できます。

{{< figure src="../img/fluid-proxy.jpg" width="700" >}}

- リバースプロキシ
- 静的コンテンツの配信
- Auto Cert（無停止での証明書自動更新）
- TCP ソケットのリバースプロキシ


## コマンドライン
```bash
fluid serve --config <path>
```

| フラグ | 短縮形 | 必須 | 説明 |
|:-------------------|:------------:|:----:|:----------------------|
| `--config <file>` | `-c <file>` | O | |
| `--verbose` | `-v` | | 詳細なログを出力 |
| `--my-id <id>` | | | サーバー ID。デフォルトの0では乱数を生成 |
| `--dry-run` | | | 設定ファイルのエラーを確認 |

## 利用例
YAML 設定ファイルを使って、さまざまな構成に対応できます。

### Auto Cert
```
HttpServer:
- Name: http_server
  Listen: 0.0.0.0:auto-cert

AutoCert:
  Email: admin@example.com
  StoreDir: /data/fluid/autocert
  Blacklist:
  - stress.com
```
### ドメインによる接続先の切り替え
```
HttpRouter:
- Host: [ db.example.com ]
  Route:
  - Proxy:
      Destination:
      - http://192.168.0.36:8684
- Host: [ demo.example.com ]
  Route:
  - Proxy:
      Destination:
      - http://192.168.0.85:8080
```

### パスによる接続先の切り替え
```
HttpRouter:
- Host: [ db.example.com ]              # 単一ホストのマッチャー
  Route:
  - Path:
    - \~ /db/
    Proxy:
      Destination:
      - http://192.168.0.36:5654
  - Proxy:
      Destination:
      - http://192.168.0.85:8080
```

### 複数サーバーによる負荷分散
```
HttpRouter:
- Host: [ db.example.com ]
  Route:
  - Proxy:
      Destination:
      - http://192.168.0.35:8684
      - http://192.168.0.36:8684
```

### 静的コンテンツの配信
```
HttpRouter:
- Host:
  - doc.example.com
  - endoc.example.com
  Route:
  - Static:
      RootDir: /data/fluid/htdocs
    Rewriter: |
      REWRITE( path("/") )
```

### AccessPolicy によるアクセス制御
```
HttpRouter:
- Host: [ demo.example.com ]
  Route:
  - Proxy:
      Destination:
      - http://192.168.0.85:8080
  AccessPolicy: allow-all

AccessPolicy:
- Name: allow-all
  Policy: NONE
- Name: allow-only-local
  Policy: ALLOW
  Allow:
  - \~ 127.0.
- Name: deny-only-local
  Policy: DENY
  Deny:
  - \g 127.0.0.*            # glob 一致
```

### TCP リバースプロキシ
```
TcpServer:
- Name: tcp_5210
  Listen: 0.0.0.0:5210
  Destination: [ 192.168.0.110:22 ]
  AccessPolicy: allow-all
- Name: tcp_5213
  Listen: 0.0.0.0:5213
  Destination: [ 192.168.0.113:22 ]
  AccessPolicy: allow-all
```
