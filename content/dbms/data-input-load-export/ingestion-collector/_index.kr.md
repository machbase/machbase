---
type: docs
title: 'Collector 기반 수집'
weight: 40
---

Machbase Collector는 로컬 파일, TCP/UDP 소켓, SFTP 원격 파일, ODBC 연결 데이터베이스 등 다양한 외부 소스에서 데이터를 수집하여 Machbase 테이블에 자동으로 적재하는 컴포넌트입니다. 데몬 형태로 상시 동작하며, JSON 설정 파일을 통해 수집 소스와 적재 대상을 연결합니다.

## 수집 파이프라인 구조

```
                        ┌────────────────────────────────┐
  [로컬 CSV 파일]  ──→  │                                │
  [TCP/UDP 소켓]   ──→  │     Machbase Collector          │ ──→ [Machbase DB]
  [SFTP 원격 파일] ──→  │   (내부 큐 버퍼 + Append API)  │
  [ODBC DB 쿼리]   ──→  │                                │
                        └────────────────────────────────┘
```

Collector는 소스에서 수신한 데이터를 내부 큐에 버퍼링한 후, 설정된 배치 크기 또는 flush 주기가 되면 Machbase Append API로 일괄 적재합니다. INSERT가 아닌 Append 방식을 사용하므로 고속 수집이 가능합니다.

## 주요 특징

- **무중단 파일 감시:** 지정 디렉터리에 새 파일이 생성되면 자동으로 감지하여 적재합니다.
- **위치 추적(position tracking):** 파일 오프셋을 기록해 중단 후 재시작 시 이어서 수집합니다.
- **다중 소스 동시 수집:** 하나의 Collector 인스턴스에서 여러 소스를 병렬로 처리합니다.
- **연결 장애 버퍼링:** 대상 서버 연결이 끊기더라도 로컬 버퍼에 저장 후 복구 시 재전송합니다.
- **유연한 파싱:** CSV, JSON, 정규식 등 다양한 데이터 형식을 지원합니다.

## 설치 위치

```bash
$MACHBASE_HOME/bin/machcollector         # Collector 실행 파일
$MACHBASE_HOME/bin/machcollectoradmin    # Collector 관리 CLI
$MACHBASE_HOME/conf/collector/           # 설정 파일 디렉터리
$MACHBASE_HOME/trc/                      # 트레이스 로그 디렉터리
```

## 설정 파일 기본 구조

Collector 설정은 JSON 형식으로 작성합니다.

```json
{
  "name": "my-collector",
  "source": {
    "type": "FILE",
    "path": "/data/sensor/*.csv"
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

## Collector 기동 및 관리

```bash
# Collector manager 기동
machcollectoradmin --startup

# Collector 생성 및 시작 (SQL)
CREATE COLLECTOR localhost.my_collector FROM "/path/to/my_collector.json";
ALTER COLLECTOR localhost.my_collector START;

# 상태 확인
machcollectoradmin --status-collector=localhost.my_collector

# Collector 중지
ALTER COLLECTOR localhost.my_collector STOP;
```

## 하위 섹션

| 섹션 | 설명 |
|------|------|
| [Collector를 사용해야 하는 경우](./use-cases-collector/) | Collector 도입 판단 기준과 적합한 사용 사례 |
| [파일 Collector](./file-collector/) | 로컬 파일 감시 및 CSV/텍스트 파일 수집 |
| [socket Collector](./socket-collector/) | TCP/UDP 소켓으로 수신되는 데이터 수집 |
| [SFTP Collector](./sftp-collector/) | 원격 SFTP 서버에서 파일을 내려받아 수집 |
| [ODBC Collector](./odbc-collector/) | ODBC 연결을 통한 외부 DB 데이터 수집 |
| [Collector 템플릿과 정규식](./template-regex-collector/) | CSV, JSON, REGEX 템플릿 설정과 활용 |
| [Collector 오류 처리](./error-handling-collector/) | 오류 유형별 원인 분석과 복구 절차 |

## 참고

- Collector 수집 성능 튜닝: [../../performance-tuning/performance-tuning/ingestion-performance-tuning-collector](../../performance-tuning/performance-tuning/ingestion-performance-tuning-collector)
- Collector 레퍼런스: [../../reference/collector](../../reference/collector)
- 파일/소켓 수집 시나리오: [../../scenario-guides/file-ingestion-collector](../../scenario-guides/file-ingestion-collector)
