---
title: 시작하기
weight: 100
---

## 소개

`fluid`는 빠르고 유연한 Network Proxy Server로 다음을 지원한다.
- FLUID reverse proxy
- FLUID back-connection relay proxy

{{< children_toc />}}

## 설정

`fluid`는 yaml 형식으로 설정파일을 작성한다.

### FLUID server 설정 예제

<details>
<summary>serve_1.yaml</summary>
<div markdown="1">

```yaml
MyID: 1 # Change

HttpRouter:
- Host: [ example.com ]              # single host matcher
  Route:
  - Path:
    - \~ /api/
    Proxy:
      Destination:
      - http://10.0.1.1:8888
- Host: [ 127.0.0.1, '\g local*' ]    # multiple host matcher
  Server: [ http_8081, http_8080 ]
  Healthz:
    Path: /healthz
    AccessPolicy: allow-only-local
  Statz:
    Path: /statz
    AccessPolicy: allow-only-local
  AccessPolicy: allow-all
  Route:
  - Path:
    - \~ /db/                     # prefix match
    - \g /web/*                   # glob match
    -    /web                     # exact match
    Proxy:
      Destination:
      - http://127.0.0.1:5654
      - http://127.0.0.1:5654
      Routing: hash                 # random, hash, hash-host (default: hash)
      Relay: local-relay
    # Rewriter: |
    #   REWRITE(topic(trimSuffix(HOST, ":8080") | replace(".", "_")))
    AccessPolicy: allow-only-local
  - Path:
    - \r .+(.yml|.yaml)$          # regular expression
    - \e hasSuffix(PATH, '.yml')  # expr evaluator
    Static:
      RootDir: ./serve/test/
    Rewriter: |                     # multiline script, 'let' for a variable
      let rpath = trimPrefix(PATH, "/static/test/");
      let file = hasSuffix(rpath, ".yaml") ? trimSuffix(rpath, ".yaml") : trimSuffix(rpath, ".yml");
      REWRITE(path("/" + file + ".yaml"))
    AccessPolicy: allow-all
HttpLog: access-log

# http listener '<ip_addr>:<port>' or '<ip_addr>:auto-cert'
# If ':auto-cert' is specified, fluid listens <ip_addr>:443 and <ip_addr>:80 ports
# and the Tls/Cert and Tls/Key configurations are ignored.
# ex) 0.0.0.0:auto-cert
HttpServer:
- Name: http_8080
  Listen: 127.0.0.1:8080
  TlsCert:  # set path for certficate (.PEM) to enable https
  TlsKey:   # set path for key (.PEM) to enable https
  AccessPolicy: allow-only-local
- Name: http_8081
  Listen: 127.0.0.1:8081
  AccessPolicy: allow-all

TcpServer:
- Name: tcp_8088
  Listen: 127.0.0.1:8088
  Destination: [ 127.0.0.1:5652 ]
  Relay: local-relay
  AccessPolicy: allow-only-local

Relay:
- Name: local-relay
  InTopic:  net-over-nats.to-fluid
  OutTopic: net-over-nats.from-fluid

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

AutoCert:
  Email: admin@example.com
  Store: fluid-auto-cert
  Replica: 1
  Blacklist:
  - stress.com

Log:
- Name: console-log  # "default" is reserved for the fluid default logger
  Level: INFO        # DEBUG, INFO, WARN, ERROR
  AddSource: true
  Format: dev        # json, text, dev, http
- Name: file-log     # "default" is reserved for the fluid default logger
  Level: DEBUG       # DEBUG, INFO, WARN, ERROR
  File:
    Filename: ./tmp/fluid.log
    MaxSize: 2       # max file size in MB
    MaxAge: 3        # maximum number of days to retain old log files
    MaxBackups: 5    # maximum number of old log files to retain
    LocalTime: true  # set false to use UTC
    Compress: false  # set true to use gzip compress      
- Name: access-log
  Level: DEBUG       # DEBUG, INFO, WARN, ERROR
  Format: http
  File:
    Filename: ./tmp/fluid-http.log
    MaxSize: 2       # max file size in MB
    MaxAge: 3        # maximum number of days to retain old log files
    MaxBackups: 5    # maximum number of old log files to retain
    LocalTime: true  # set false to use UTC
    Compress: false  # set true to use gzip compress      
- Name: tee-log
  Default: true
  Tee:
  - console-log
  - file-log

Broker:
  Listen: 127.0.0.1:3000
  StoreDir: ./tmp/data
  Authorization: s3creT
  Debug: true
  LogFile: ./tmp/fluid-nats.log
  NoLog: true
```

</div>
</details>

### FLUID serve broker 설정 예제
<details>
<summary>serve_brkd.yaml</summary>
<div markdown="1">

```yaml
MyID: 10 # Change Me

Broker:
  Host: 127.0.0.1
  Port: 3000
  StoreDir: ./tmp/data
  Authorization: s3creT
  Debug: true
  LogFile: ./tmp/fluid-nats.log
  NoLog: true
```

</div>
</details>

### FLUID relay 설정 예제
<details>
<summary>relay_1.yaml</summary>
<div markdown="1">

```yaml
Relay:
- Broker:
  - nats://s3creT@127.0.0.1:3000
  Topic:  net-over-nats.from-fluid
  Channel: 1024
  ReadBufferSize: 524288 #512K
  Destination:
  - Host: 127.0.0.1/32
    Port: 5652-5654

Logs:
- Name: console-log
  Level: DEBUG # DEBUG, INFO, WARN, ERROR
  Default: true
  File:
    Filename: #./tmp/relay-1.log # default is stdout
    Append: true     # set false to create a new log file when fluid (re)starts
    MaxSize: 2       # max file size in MB
    MaxAge: 3        # maximum number of days to retain old log files
    MaxBackups: 5    # maximum number of old log files to retain
    LocalTime: true  # set false to use UTC
    Compress: false  # set true to use gzip compress
```

</div>
</details>
