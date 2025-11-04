---
title: Relay 설정 파일
weight: 340
---

## Relay config file

### Top Level

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Verbose              | boolean      |      |                     |
| Relay                | obj array    |      |                     |
| Log                  | obj array    |      |                     |
| ShutdownTimeout      | int          |      | shutdown max wait time in sec. |


### Relay

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Broker               | string array | O    | 설정되지 않았다면 `--broker` flag으로 설정한 default broker를 사용 |
| Topic                | string       | O    | 설정되지 않았다면 `--topic` flag으로 설정한 default topic을 사용 |
| Destination          | obj array    | O    |                     |
| ReadBufferSize       | int          |      | default 32768 (32K) |
| Channel              | int          |      | channel buffer size, default 1000 |


### Destination

| 키                   | 타입         | 필수 |    설명             |
|:---------------------|:------------:|:----:|:--------------------|
| Net                  | string       |      | default `tcp`       |
| Host                 | string       |      | CIDR format, ex: `192.168.1.1/24` |
| Port                 | string       |      | 쉼표(,)로 구분되는 port 범위. ex: `8080,5652-5656` |


## Examples

### Simple

```yaml
Relay:
- Broker:
  - nats://secret@127.0.0.1:3000
  Topic:  net-over-nats.from-fluid
  Channel: 1024
  ReadBufferSize: 524288 #512K
  Destination:
  - Host: '127.0.0.1/32'
    Port: 5652-5654

Logs:
- Name: console-log
  Level: INFO     # DEBUG, INFO, WARN, ERROR
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
