---
type: docs
title: 'Collector source type 사전'
weight: 20
---

Collector source type은 데이터를 수집하는 입력 채널의 종류를 지정합니다. 설정 파일의 `source.type` 파라미터로 지정합니다.

## 지원 소스 타입 목록

| 소스 타입 | 설명 |
|-----------|------|
| `FILE` | 로컬 파일 감시 및 수집 |
| `TCP` | TCP 소켓 수신 |
| `UDP` | UDP 패킷 수신 |
| `SERIAL` | 시리얼 포트 수신 |
| `HTTP` | HTTP 요청 수신 |
| `MQTT` | MQTT 브로커 구독 |

---

## FILE

로컬 파일 시스템의 파일을 감시하고 새로운 내용을 수집합니다. 로그 파일, CSV 파일 등의 수집에 사용합니다.

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `type` | 필수 | string | `"FILE"` |
| `path` | 필수 | string | 감시할 파일의 절대 경로 또는 glob 패턴 |
| `polling_interval` | 선택 | integer | 파일 변경 감지 주기 (밀리초, 기본값: 1000) |
| `start_from_end` | 선택 | boolean | 수집 시작 시 기존 내용 무시 여부 (기본값: false) |
| `encoding` | 선택 | string | 파일 인코딩 (기본값: `"utf-8"`) |

```json
{
  "source": {
    "type": "FILE",
    "path": "/var/log/sensor/*.log",
    "polling_interval": 500,
    "start_from_end": true
  }
}
```

---

## TCP

TCP 소켓으로 수신되는 데이터를 수집합니다. 네트워크를 통해 데이터를 전송하는 장치나 애플리케이션과 연동합니다.

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `type` | 필수 | string | `"TCP"` |
| `port` | 필수 | integer | 수신 대기 포트 번호 |
| `host` | 선택 | string | 바인드 주소 (기본값: `"0.0.0.0"`) |
| `delimiter` | 선택 | string | 레코드 구분자 (기본값: `"\n"`) |
| `max_connections` | 선택 | integer | 최대 동시 연결 수 |

```json
{
  "source": {
    "type": "TCP",
    "host": "0.0.0.0",
    "port": 9090,
    "delimiter": "\n"
  }
}
```

---

## UDP

UDP 패킷으로 수신되는 데이터를 수집합니다. 실시간성이 중요하고 패킷 손실을 허용할 수 있는 환경에서 사용합니다.

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `type` | 필수 | string | `"UDP"` |
| `port` | 필수 | integer | 수신 대기 포트 번호 |
| `host` | 선택 | string | 바인드 주소 (기본값: `"0.0.0.0"`) |
| `buffer_size` | 선택 | integer | UDP 수신 버퍼 크기 (바이트) |

```json
{
  "source": {
    "type": "UDP",
    "host": "0.0.0.0",
    "port": 9091
  }
}
```

---

## SERIAL

시리얼 포트(RS-232, RS-485 등)를 통해 수신되는 데이터를 수집합니다. 산업용 센서, 계측 장비 연동에 사용합니다.

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `type` | 필수 | string | `"SERIAL"` |
| `port` | 필수 | string | 시리얼 포트 경로 (예: `/dev/ttyS0`, `COM1`) |
| `baud_rate` | 필수 | integer | 전송 속도 (예: `9600`, `115200`) |
| `data_bits` | 선택 | integer | 데이터 비트 수 (기본값: `8`) |
| `stop_bits` | 선택 | integer | 정지 비트 수 (기본값: `1`) |
| `parity` | 선택 | string | 패리티 설정 (`"none"`, `"even"`, `"odd"`) |
| `delimiter` | 선택 | string | 레코드 구분자 (기본값: `"\n"`) |

```json
{
  "source": {
    "type": "SERIAL",
    "port": "/dev/ttyS0",
    "baud_rate": 9600,
    "data_bits": 8,
    "stop_bits": 1,
    "parity": "none"
  }
}
```

---

## HTTP

HTTP 요청으로 수신되는 데이터를 수집합니다. 웹훅, IoT 게이트웨이, REST 클라이언트와 연동합니다.

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `type` | 필수 | string | `"HTTP"` |
| `port` | 필수 | integer | HTTP 수신 포트 번호 |
| `host` | 선택 | string | 바인드 주소 (기본값: `"0.0.0.0"`) |
| `path` | 선택 | string | 수신 경로 (기본값: `"/"`) |
| `method` | 선택 | string | 허용 HTTP 메서드 (기본값: `"POST"`) |

```json
{
  "source": {
    "type": "HTTP",
    "host": "0.0.0.0",
    "port": 8080,
    "path": "/data"
  }
}
```

---

## MQTT

MQTT 브로커에서 지정한 토픽을 구독하여 데이터를 수집합니다. IoT 디바이스와의 연동에 적합합니다.

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `type` | 필수 | string | `"MQTT"` |
| `broker` | 필수 | string | MQTT 브로커 주소 (예: `"tcp://localhost:1883"`) |
| `topic` | 필수 | string | 구독할 토픽 (와일드카드 지원: `+`, `#`) |
| `client_id` | 선택 | string | MQTT 클라이언트 ID |
| `username` | 선택 | string | 브로커 인증 사용자명 |
| `password` | 선택 | string | 브로커 인증 비밀번호 |
| `qos` | 선택 | integer | QoS 수준 (`0`, `1`, `2`, 기본값: `0`) |
| `clean_session` | 선택 | boolean | 클린 세션 사용 여부 (기본값: `true`) |

```json
{
  "source": {
    "type": "MQTT",
    "broker": "tcp://mqtt-broker:1883",
    "topic": "sensors/+/data",
    "client_id": "machbase-collector-01",
    "qos": 1
  }
}
```
