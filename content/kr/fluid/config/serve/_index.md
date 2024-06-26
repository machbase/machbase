---
title: Server 설정 파일
weight: 320
---

## Server config file

### Top Level

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| MyID                 | int          |      | any number, 0 ~ 1000 |
| HttpServer           | obj array    |      | http listener 정보 목록 |
| HttpRouter           | obj array    | O    | http router 정보 목록 |
| HttpLog              | string       |      | http logger name    |
| TcpServer            | obj array    |      | tcp listener 정보 목록 |
| UdpServer            | obj array    |      | udp listener 정보 목록 |
| Relay                | obj array    |      | relay 정보 목록 |
| AccessPolicy         | obj array    |      | name of access policy |
| AutoCert             | obj          |      | auto certification (인증서 무중단 자동 갱신) 정보 |
| Log                  | obj array    |      | logger 정보 목록 |
| Verbose              | boolean      |      | --verbose, boolean(true, false) |
| ShutdownTimeout      | int          |      | shutdown max wait time in sec. |
| Broker               | obj          |      | broker 정보 |

### TcpServer
tcp listener 정보

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Name                 | string       |      | name of TcpServer   |
| Listen               | string       | O    | ip:port             |
| Destination          | string array |      | Destination 목록. 여러 개가 지정된 경우 round robin 방식으로 사용 |
| Routing              | string       |      | `random`, `hash-host` (src+dst), `hash` (src), default: `random` |
| Relay                | string       |      | relay name          |
| ConnectTimeout       | int          |      | connection timeout (sec) |
| KeepAlive            | int          |      | keep alive timeout (sec) |
| AccessPolicy         | string       |      | name of access policy |

### HttpServer
http listener 정보. `<ip_addr>:<port>` 또는 `<ip_addr>:auto-cert`  
`:auto-cert`가 설정되었다면, fluid는 `<ip_addr>:443`과 `<ip_addr>:80` 포트를 listen 하고 `Tls/Cert` 와 `Tls/Key` 설정을 무시한다.  
ex) 0.0.0.0:auto-cert

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Name                 | string       | O    | name of HttpServer |
| Listen               | string       | O    | ip:port             |
| ReadTimeout          | int          |      | read timeout, default: 0 |
| WriteTimeout         | int          |      | write timeout, default: 0 |
| IdleTimeout          | int          |      | idle timeout, default: 0           |
| SockLinger           | int          |      | SO_LINGER, default: 0 |
| SockDelay            | bool         |      | `true`로 설정되면 SO_NODELAY를 disable, default: false |
| TlsCert              | string       |      | certificate file의 경로 |
| TlsKey               | string       |      | key file의 경로      |
| AccessPolicy         | string       |      | name of access policy |

### UdpServer
udp listener 정보.  
수신된 udp 패킷을 내부 NATS의 설정된 Subject(`Topic`)로 전송한다.
| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Name                 | string       |      | name of UdpServer   |
| Listen               | string       | O    | ip:port             |
| Topic                | string       | O    | NATS subject        |
| DumpHex              | bool         |      | true로 설정되면 서버 로그에 수신된 패킷 전체를 dump한다. |

### HttpRouter
`Host` 항목에는 하단에 설명된 matcher를 사용할 수 있다.

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Server               | string array |      | name of HttpServer |
| Host                 | string array |      | name of HTTP Host   |
| Route                | obj array    |      |                     |
| Healthz              | obj          |      |                     |
| AccessPolicy         | string       |      | name of access policy |

### HttpRouter/Route
`Path`, `Method` 항목에는 하단에 설명된 matcher를 사용할 수 있다.
  
| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Path                 | string array |      |                     |
| Method               | string array |      |                     |
| Rewriter             | string       |      |                     |
| Proxy                | obj          |      |                     |
| Static               | obj          |      |                     |
| AccessPolicy         | string       |      | name of access policy |

### HttpRouter/Route/Proxy

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Destination          | string array |      |                     |
| Routing              | string       |      | random, hash, hash-host (default: hash) |
| InsecureSkipVerify   | bool         |      |                     |
| ForwardProxy         | string       |      |                     |
| Relay                | string       |      |                     |
| Timeout              | int          |      | default 3           |
| KeepAlive            | int          |      | network keep-alive if supproted |
| DisableKeepAlives    | bool         |      | if true, disables HTTP keep-alives |
| TLSHandshakeTimeout  | int          |      | default 10          |
| DisableCompression   | bool         |      | if true, prevents the Transport compression |
| MaxIdleConns         | int          |      | default 10          |
| MaxIdleConnsPerHost  | int          |      | default 2           |
| MaxConnsPerHost      | int          |      | default 0, no limit |
| IdleConnTimeout      | int          |      | default 60          |
| ResponseHeaderTimeout| int          |      | default 30          |
| ExpectContinueTimeout| int          |      | default 0           |
| ForceAttemptHTTP2    | int          |      | default false       |
| WriteBufferSize      | int          |      | if zero, default 4096 |
| ReadBufferSize       | int          |      | if zero, default 4096 |

### HttpRouter/Route/Static

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| RootDir              | string       |      |                     |

### HttpRouter/Healthz

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Path                 | string       |      | default `/healthz`  |
| Status               | int          |      | default `200`       |
| Text                 | string       |      | default `ready.`    |
| AccessPolicy         | string       |      | name of access policy |

### AutoCert

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Email                | string       |      |                     |
| Blacklist            | string array |      |                     |
| RenewBefore          | int          |      | days                |

- Shared store

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Store                | string       |      |                     |
| Replica              | int          |      |                     |
| Broker               | string array |      |                     |
| MaxReconnect         | int          |      | if negative, never give up trying to reconnect |

- Directory store

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| StoreDir             | string       |      |                     |

### AccessPolicy
`Allow`, `Deny` 항목에는 하단에 설명된 matcher를 사용할 수 있다.

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Name                 | string       | O    |                     |
| Policy               | string       | O    | NONE, DENY, ALLOW, DENY_ALLOW, ALLOW_DENY |
| Allow                | string array |      | White list          |
| Deny                 | string array |      | Black list          |

### Relay

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Name                 | string       | O    |                     |
| Broker               | string array |      | if empty, use internal broker |
| InTopic              | string       | O    |                     |
| OutTopic             | string       | O    |                     |
| ConnectTimeout       | int          |      | default 3           |
| ReadTimeout          | int          |      | default 3           |
| WriteTimeout         | int          |      | default 3           |

### Broker

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| ServerName           | string       |      | default: `fluid_`+host_addr |
| Listen               | string       | O    | broker listen address, default: `127.0.0.1:3000` |
| ClientAdvertise      | string       |      |                     |
| StoreDir             | string       | O    |                     |
| ReadyTimeout         | int          |      | sec. default: `5`   |
| LogTime              | bool         |      | default: `true`     |
| NoLog                | bool         |      | default: `false`    |
| LogSizeLimit         | int          |      | default: `104857600` (100M) |
| LogMaxFiles          | int          |      | default: `1`        |
| TraceVerbose         | bool         |      | default: `false`    |
| Authorization        | string       |      |                     |
| JetStream            | bool         |      | default: `true`     |
| JetStreamMaxMemory   | int          |      | default: `1073741824` (1G) |
| JetStreamMaxStore    | int          |      | default: `5250048000` (5G) |
| Cluster              | obj          |      | enable cluster      |
| Routes               | string array |      | cluster routing     |

### Broker/Cluster

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Name                 | string       | O    | node name           |
| Listen               | string       | O    | cluster node listen addr (host:port) |
| Advertise            | string       |      | advertise address   |
| NoAdvertise          | bool         |      | default: `false`    |
| ConnectRetries       | int          |      |                     |
| PoolSize             | int          |      |                     |

### Log

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Name                 | string       | O    | logger name         |
| Level                | string       | O    | DEBUG, INFO, WARN, ERROR |
| AddSource            | bool         |      | add source code file name and line |
| Format               | string       |      | `json`, `text`, `dev` |
| File                 | obj          |      | file logger config    |
| Tee                  | string array |      | tee logger, array of logger names |

If `File` and `Tee` is not defined, it will printout the log into stdout.

### Log/File

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Filename             | string       |      | file path           |
| MaxSize              | int          |      | max log file size in MB |
| MaxAge               | int          |      | how many days log backups are kept |
| MaxBackups           | int          |      | how many log backups are kept      |
| LocalTime            | bool         |      | use local time instead of UTC      |
| Compress             | bool         |      | compress log backup files          |

### matcher 정보
| matcher              | prefix | 예제                 |
|:---------------------|:------:|:---------------------|
| prefix match         | `\~`   | `\~ /db/`            |
| glob match           | `\g`   | `\g /web/*`          |
| exact match          | 없음   | `/web`               |
| regular expression   | `\r`   | `\r .+(.yml|.yaml)$` |
| expr evaluator       | `\e`   | `\e hasSuffix(PATH, '.yml')` |
