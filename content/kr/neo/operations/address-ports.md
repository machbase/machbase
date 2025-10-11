---
title: IP 주소와 포트
type: docs
weight: 12
---

## 바인드 주소

machbase-neo는 보안을 위해 기본적으로 로컬호스트에서만 실행되고 대기합니다. 원격 호스트의 클라이언트가 네트워크로 데이터를 읽거나 쓰려면 실행 시 `--host <bind address>` 옵션으로 바인드 주소를 지정해야 합니다.

모든 주소에서 접속을 허용하려면 `0.0.0.0`을 사용하십시오.

```sh
machbase-neo serve --host 0.0.0.0
```

특정 주소에서만 접속을 허용하려면 호스트의 IP 주소를 지정합니다.

```sh
machbase-neo serve --host 192.168.1.10
```

## 수신 포트

프로토콜별 포트를 제어하는 플래그는 다음과 같습니다.

| flag             | default          | desc                                      |
|:-----------------|:----------------:|-------------------------------------------|
| `--shell-port`   | `5652`           | SSH 수신 포트                              |
| `--mqtt-port`    | `5653`           | MQTT 수신 포트                             |
| `--http-port`    | `5654`           | HTTP 수신 포트                             |
| `--grpc-port`    | `5655`           | gRPC 수신 포트                             |
| `--grpc-sock`    | `mach-grpc.sock` | gRPC 유닉스 도메인 소켓                    |
| `--grpc-insecure`| `false`          | gRPC 수신 포트에서 TLS 비활성화            |
| `--mach-port`    | `5656`           | JDBC/ODBC 드라이버용 Machbase 네이티브 포트 |

특정 네트워크 인터페이스에만 바인드하려면 아래 리슨 호스트/포트 플래그를 사용하십시오.

| flag                   | default                | desc                                  |
|:-----------------------|:-----------------------|---------------------------------------|
| `--mach-listen-host`   | `--host` 값            |                                       |
| `--mach-listen-port`   | `--mach-port` 값       |                                       |
| `--shell-listen-host`  | `--host` 값            |                                       |
| `--shell-listen-port`  | `--shell-port` 값      |                                       |
| `--grpc-listen-host`   | `--host` 값            |                                       |
| `--grpc-listen-port`   | `--grpc-port` 값       |                                       |
| `--grpc-listen-sock`   | `--grpc-sock` 값       |                                       |
| `--http-listen-host`   | `--host` 값            |                                       |
| `--http-listen-port`   | `--http-port` 값       |                                       |
| `--mqtt-listen-host`   | `--host` 값            |                                       |
| `--mqtt-listen-port`   | `--mqtt-port` 값       |                                       |
