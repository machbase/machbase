---
type: docs
title: 'socket Collector'
weight: 30
---

socket Collector는 TCP 또는 UDP 소켓으로 수신되는 데이터를 실시간으로 수집하여 Machbase 테이블에 적재합니다. 네트워크를 통해 데이터를 전송하는 산업용 장비, IoT 게이트웨이, 애플리케이션 로그 수집기 등과 연동할 때 사용합니다.

## 소켓 타입 비교

| 구분 | TCP | UDP |
|------|-----|-----|
| 연결 방식 | 연결 지향 (3-way handshake) | 비연결 (연결 없이 전송) |
| 데이터 전달 보장 | 보장됨 | 보장되지 않음 (패킷 손실 가능) |
| 순서 보장 | 보장됨 | 보장되지 않음 |
| 적합한 경우 | 데이터 손실 없이 수집해야 할 때 | 고빈도 센서 데이터, 일부 손실 허용 시 |

## TCP 소켓 설정

### 대상 테이블 생성

```sql
CREATE TABLE tcp_event_log (
    client_ip  VARCHAR(40),
    event_code INTEGER,
    message    VARCHAR(1024),
    time       DATETIME
);
```

### Collector 설정 파일 (JSON)

`$MACHBASE_HOME/conf/collector/tcp_collector.json`:

```json
{
  "name": "tcp_collector",
  "source": {
    "type": "TCP",
    "host": "0.0.0.0",
    "port": 9090,
    "delimiter": "\n",
    "max_connections": 50
  },
  "template": {
    "type": "CSV",
    "separator": ",",
    "columns": [
      {"name": "client_ip",  "type": "VARCHAR",  "index": 0},
      {"name": "event_code", "type": "INTEGER",  "index": 1},
      {"name": "message",    "type": "VARCHAR",  "index": 2},
      {"name": "time",       "type": "DATETIME", "index": 3, "format": "YYYY-MM-DD HH24:MI:SS"}
    ]
  },
  "target": {
    "table": "tcp_event_log",
    "server": {
      "host": "127.0.0.1",
      "port": 5656,
      "user": "SYS",
      "password": "MANAGER"
    }
  }
}
```

### TCP 소스 파라미터

| 파라미터 | 필수 | 기본값 | 설명 |
|---------|------|--------|------|
| `type` | 필수 | - | `"TCP"` |
| `port` | 필수 | - | 수신 대기 포트 번호 |
| `host` | 선택 | `"0.0.0.0"` | 바인드 주소 (`"0.0.0.0"`이면 모든 인터페이스) |
| `delimiter` | 선택 | `"\n"` | 레코드 구분자 |
| `max_connections` | 선택 | 제한 없음 | 최대 동시 연결 수 |

## UDP 소켓 설정

### Collector 설정 파일 (UDP)

```json
{
  "name": "udp_sensor",
  "source": {
    "type": "UDP",
    "host": "0.0.0.0",
    "port": 9091,
    "buffer_size": 65536
  },
  "template": {
    "type": "CSV",
    "separator": ",",
    "columns": [
      {"name": "name",  "type": "VARCHAR",  "index": 0},
      {"name": "time",  "type": "DATETIME", "index": 1, "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value", "type": "DOUBLE",   "index": 2}
    ]
  },
  "target": {
    "table": "sensor_log",
    "server": {
      "host": "127.0.0.1",
      "port": 5656,
      "user": "SYS",
      "password": "MANAGER"
    }
  }
}
```

### UDP 소스 파라미터

| 파라미터 | 필수 | 기본값 | 설명 |
|---------|------|--------|------|
| `type` | 필수 | - | `"UDP"` |
| `port` | 필수 | - | 수신 대기 포트 번호 |
| `host` | 선택 | `"0.0.0.0"` | 바인드 주소 |
| `buffer_size` | 선택 | OS 기본값 | UDP 수신 버퍼 크기 (바이트) |

## 클라이언트에서 데이터 전송 예시

```python
# TCP로 Collector에 데이터를 전송하는 클라이언트 예시
import socket
import time

COLLECTOR_HOST = "localhost"
COLLECTOR_PORT = 9090

def send_events(events):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((COLLECTOR_HOST, COLLECTOR_PORT))
        for event in events:
            # 형식: client_ip,event_code,message,time\n
            line = f"{event['ip']},{event['code']},{event['msg']},{event['time']}\n"
            s.sendall(line.encode("utf-8"))
            time.sleep(0.001)

events = [
    {"ip": "192.168.0.10", "code": 200, "msg": "normal", "time": "2024-01-01 10:00:00"},
    {"ip": "192.168.0.11", "code": 500, "msg": "error",  "time": "2024-01-01 10:00:01"},
]
send_events(events)
```

## Collector 등록 및 시작

```bash
machcollectoradmin --startup
```

```sql
CREATE COLLECTOR localhost.tcp_collector
FROM "$MACHBASE_HOME/conf/collector/tcp_collector.json";

ALTER COLLECTOR localhost.tcp_collector START;
```

## 연결 상태 모니터링

```bash
# 포트가 정상적으로 열려 있는지 확인
netstat -tlnp | grep 9090

# 클라이언트 연결 수 확인
ss -tn state established '( dport = :9090 or sport = :9090 )' | wc -l

# 트레이스 로그에서 연결 이벤트 확인
grep -i "connect\|disconnect\|error" $MACHBASE_HOME/trc/machcollector.trc | tail -50
```

## 다중 클라이언트 연결

TCP 소켓 타입은 다수의 클라이언트가 동시에 연결하여 데이터를 전송할 수 있습니다. Collector는 클라이언트별로 독립적인 연결을 유지하고, 수신된 데이터를 내부 큐에 합쳐 Machbase에 일괄 적재합니다.

```
[클라이언트 A] ──TCP──┐
[클라이언트 B] ──TCP──┤──→ [Collector 내부 큐] ──Append──→ [Machbase]
[클라이언트 C] ──TCP──┘
```

`max_connections` 파라미터로 동시 연결 수를 제한할 수 있습니다. 초과 연결 시도는 거부됩니다.

## 연결 끊김 처리

TCP 클라이언트가 연결을 끊으면 Collector는 해당 연결을 정리합니다. Collector 자체는 계속 실행 상태를 유지하며 새로운 연결을 기다립니다. 클라이언트 측에서 재연결을 구현해야 합니다.

Machbase 서버와의 연결이 끊어지는 경우, Collector는 내부 큐에 데이터를 계속 버퍼링하고 재연결 후 적재를 재개합니다.

```json
{
  "target": {
    "reconnect_interval": 5,
    "reconnect_max_retry": 0
  }
}
```

| 파라미터 | 설명 |
|---------|------|
| `reconnect_interval` | 재연결 대기 시간 (초) |
| `reconnect_max_retry` | 재연결 최대 시도 횟수 (0이면 무한 재시도) |

## 참고

- UDP vs TCP 선택: [../use-cases-collector](../use-cases-collector)
- 템플릿 설정 상세: [../template-regex-collector](../template-regex-collector)
- 오류 처리: [../error-handling-collector](../error-handling-collector)
- TCP/UDP 소스 파라미터 전체 목록: [../../../reference/collector/dictionary-collector-source-type](../../../reference/collector/dictionary-collector-source-type)
