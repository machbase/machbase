---
type: docs
title: '파일 Collector'
weight: 20
---

파일 Collector는 로컬 파일 시스템의 지정 디렉터리를 감시하고, 새로운 파일이 생성되거나 기존 파일에 내용이 추가되면 해당 데이터를 읽어 Machbase 테이블에 적재합니다. CSV, 구분자 기반 텍스트, 정규식으로 파싱 가능한 로그 파일 등을 지원합니다.

## 동작 원리

```
[감시 디렉터리] ──새 파일 감지──→ [읽기 + 파싱] ──Append API──→ [Machbase]
                                        │
                               [처리 완료 파일 이동]
                                (done 디렉터리)
```

파일 Collector는 내부적으로 파일 오프셋(position)을 추적합니다. Collector가 비정상 종료된 후 재시작하더라도, 마지막으로 읽은 위치부터 이어서 수집하므로 데이터 중복이나 누락을 방지합니다.

## 기본 설정

### 대상 테이블 생성

```sql
CREATE TABLE file_sensor_log (
    name          VARCHAR(64),
    time          DATETIME,
    value         DOUBLE,
    quality       INTEGER
);
```

### Collector 설정 파일 (JSON)

`$MACHBASE_HOME/conf/collector/file_sensor.json`:

```json
{
  "name": "file_sensor",
  "source": {
    "type": "FILE",
    "path": "/data/sensors/incoming/sensor_*.csv",
    "polling_interval": 1000,
    "encoding": "utf-8"
  },
  "template": {
    "type": "CSV",
    "separator": ",",
    "skip_header": 1,
    "columns": [
      {"name": "name",    "type": "VARCHAR",  "index": 0},
      {"name": "time",    "type": "DATETIME", "index": 1, "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value",   "type": "DOUBLE",   "index": 2},
      {"name": "quality", "type": "INTEGER",  "index": 3}
    ]
  },
  "target": {
    "table": "file_sensor_log",
    "server": {
      "host": "127.0.0.1",
      "port": 5656,
      "user": "SYS",
      "password": "MANAGER"
    }
  }
}
```

### 수집 대상 CSV 파일 형식

```csv
name,time,value,quality
DEVICE_A,2024-01-01 10:00:00,72.3,100
DEVICE_A,2024-01-01 10:00:01,72.5,100
DEVICE_B,2024-01-01 10:00:00,68.5,100
```

## 소스 파라미터 상세

| 파라미터 | 필수 | 기본값 | 설명 |
|---------|------|--------|------|
| `type` | 필수 | - | `"FILE"` |
| `path` | 필수 | - | 감시할 파일 경로 또는 glob 패턴 |
| `polling_interval` | 선택 | `1000` | 파일 변경 감지 주기 (밀리초) |
| `start_from_end` | 선택 | `false` | `true`이면 기존 파일 내용을 무시하고 새로 추가되는 내용만 수집 |
| `encoding` | 선택 | `"utf-8"` | 파일 인코딩 |

## 파일 회전(rotation) 처리

파일 회전이란 로그 파일이 일정 크기나 시간이 지나면 새 파일로 교체되는 동작입니다. 파일 Collector는 glob 패턴으로 감시 대상을 지정하므로, 새 파일이 패턴에 매칭되면 자동으로 감지하여 수집을 시작합니다.

```json
{
  "source": {
    "type": "FILE",
    "path": "/var/log/app/access_*.log",
    "start_from_end": false
  }
}
```

> **주의:** `start_from_end`를 `true`로 설정하면 Collector 시작 시점에 이미 존재하는 파일의 기존 내용을 무시합니다. 신규 수집 환경에서 과거 데이터를 제외할 때 유용합니다.

## 처리 완료 파일 이동

수집이 완료된 파일을 별도 디렉터리로 이동하거나 삭제하는 설정을 추가할 수 있습니다. 이를 통해 감시 디렉터리에 처리된 파일이 누적되는 것을 방지합니다.

```json
{
  "source": {
    "type": "FILE",
    "path": "/data/incoming/*.csv",
    "done_path": "/data/done",
    "error_path": "/data/error"
  }
}
```

| 파라미터 | 설명 |
|---------|------|
| `done_path` | 수집 완료 파일을 이동할 디렉터리 경로 |
| `error_path` | 파싱 오류가 발생한 파일을 이동할 디렉터리 경로 |

## Collector 등록 및 시작

```bash
# Collector manager 기동
machcollectoradmin --startup
```

```sql
-- Collector 생성
CREATE COLLECTOR localhost.file_sensor
FROM "$MACHBASE_HOME/conf/collector/file_sensor.json";

-- Collector 시작
ALTER COLLECTOR localhost.file_sensor START;

-- 상태 확인
-- machcollectoradmin --status-collector=localhost.file_sensor

-- Collector 중지
ALTER COLLECTOR localhost.file_sensor STOP;
```

## 수집 상태 확인

```bash
# 트레이스 로그에서 파일 수집 상태 확인
tail -50 $MACHBASE_HOME/trc/machcollector.trc

# 파일 읽기, 오류 메시지 필터링
grep -i "file\|read\|error\|skip" $MACHBASE_HOME/trc/machcollector.trc | tail -50
```

트레이스 로그에서 확인할 수 있는 주요 메시지:

| 메시지 키워드 | 의미 |
|-------------|------|
| `new file detected` | 새 파일 감지 |
| `file read complete` | 파일 읽기 완료 |
| `parse error` | 데이터 파싱 실패 (해당 행 건너뜀) |
| `append flush` | 배치 데이터 Machbase에 적재 |

## 위치 추적 초기화

파일 오프셋 정보를 초기화하고 처음부터 재수집해야 하는 경우:

```bash
# Collector 중지
machcollectoradmin --stop-collector=localhost.file_sensor

# position 파일 삭제
rm -f $MACHBASE_HOME/var/collector/file_sensor.pos

# Collector 재시작
machcollectoradmin --start-collector=localhost.file_sensor
```

## 참고

- 템플릿 설정 상세: [../template-regex-collector](../template-regex-collector)
- 오류 처리: [../error-handling-collector](../error-handling-collector)
- FILE 소스 파라미터 전체 목록: [../../../reference/collector/dictionary-collector-source-type](../../../reference/collector/dictionary-collector-source-type)
- 파일 수집 시나리오 가이드: [../../../scenario-guides/file-ingestion-collector](../../../scenario-guides/file-ingestion-collector)
