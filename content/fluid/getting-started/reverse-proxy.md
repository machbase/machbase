---
title: Fluid server
weight: 160
---

## FLUID server
Reverse Proxy란 클라이언트와 서버 간의 중개자 역할을 하는 서버로, 클라이언트로부터의 요청을 대신 받아 서버에 전달하고, 서버의 응답을 클라이언트에 전달하는 역할을 한다. 이를 통해 서버의 부하를 분산시키고 보안을 강화하는 등 다양한 기능을 수행할 수 있다.  

{{< figure src="../img/fluid-proxy.jpg" width="700" >}}

- Reverse proxy
- Static contents 지원
- Auto Cert(인증서 무중단 자동 갱신) 지원
- TCP socket reverse proxy 지원


## Command line
```bash
fluid serve --config <path>
```

| 플래그             | 단축 플래그  | 필수 |    설명               |
|:-------------------|:------------:|:----:|:----------------------|
| `--config <file>`  | `-c <file>`  | O    |                       |
| `--verbose`        | `-v`         |      | 다양한 log 정보 제공  |
| `--my-id <id>`     |              |      | server id, (default: 0, generate random number) |
| `--dry-run`        |              |      | 설정 파일의 오류를 확인 |

## 활용 예
config yaml file을 이용하여 다양하게 활용할 수 있다.

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
### domain에 따라 다른 서버로 연결
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

### 경로별로 다른 서버 접속
```
HttpRouter:
- Host: [ db.example.com ]              # single host matcher
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

### 복수의 서버를 이용한 부하 분산
```
HttpRouter:
- Host: [ db.example.com ]
  Route:
  - Proxy:
      Destination:
      - http://192.168.0.35:8684
      - http://192.168.0.36:8684
```

### Static contents 사용
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

### Access policy를 활용한 접근제어
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
  - \g 127.0.0.*            # glob match
```

### TCP reverse proxy
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
