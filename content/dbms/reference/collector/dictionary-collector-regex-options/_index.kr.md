---
type: docs
title: 'Collector regex/options 사전'
weight: 30
---

Collector의 REGEX 템플릿에서 사용하는 정규식 패턴 옵션과 자주 쓰는 패턴 예시를 정리합니다.

## 정규식 플래그 옵션

REGEX 템플릿의 `pattern` 파라미터에 인라인 플래그를 사용하여 매칭 동작을 제어합니다.

| 플래그 | 인라인 표기 | 설명 |
|--------|------------|------|
| Case Insensitive | `(?i)` | 대소문자 구분 없이 매칭 |
| Multiline | `(?m)` | `^`, `$`가 각 줄의 시작과 끝에 매칭 |
| Dotall | `(?s)` | `.`이 줄바꿈 문자(`\n`)도 포함하여 매칭 |
| 복합 사용 | `(?im)` | 여러 플래그 동시 적용 |

```json
{
  "template": {
    "type": "REGEX",
    "pattern": "(?i)error:\\s+(.+)",
    "columns": [
      {"name": "message", "type": "VARCHAR", "group": 1}
    ]
  }
}
```

## 캡처 그룹 유형

### 번호 있는 캡처 그룹

괄호로 묶어 캡처 그룹을 정의합니다. 그룹 번호는 왼쪽 괄호 기준으로 1부터 순서대로 부여됩니다.

```text
패턴:  (\d{4}-\d{2}-\d{2}) (\S+) ([\d.]+)
그룹:    1번                2번    3번
```

설정:
```json
"columns": [
  {"name": "time",  "type": "DATETIME", "group": 1},
  {"name": "name",  "type": "VARCHAR",  "group": 2},
  {"name": "value", "type": "DOUBLE",   "group": 3}
]
```

### 이름 있는 캡처 그룹

`(?P<이름>패턴)` 문법으로 그룹에 이름을 지정합니다. 이름으로 참조하면 패턴 변경 시 컬럼 매핑을 수정하지 않아도 됩니다.

```text
패턴:  (?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<sensor>\S+) (?P<val>[\d.]+)
```

설정:
```json
"columns": [
  {"name": "time",  "type": "DATETIME", "group": "ts"},
  {"name": "name",  "type": "VARCHAR",  "group": "sensor"},
  {"name": "value", "type": "DOUBLE",   "group": "val"}
]
```

### 비캡처 그룹

`(?:패턴)`은 매칭에 사용하지만 캡처하지 않습니다. 그룹 번호에 영향을 주지 않습니다.

```text
패턴:  (?:INFO|WARN|ERROR):\s+(\S+)\s+([\d.]+)
그룹:                         1번    2번
```

## 자주 쓰는 패턴

### 타임스탬프

```text
# YYYY-MM-DD HH:MM:SS
(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})

# YYYY-MM-DDTHH:MM:SSZ (ISO 8601)
(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)

# DD/Mon/YYYY:HH:MM:SS (Apache 로그)
(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})

# Unix timestamp (정수)
(\d{10,13})
```

### IP 주소

```text
# IPv4
(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})

# IPv6 (축약 포함)
([0-9a-fA-F:]{2,39})
```

### 숫자

```text
# 정수
(-?\d+)

# 부동소수점
(-?[\d]+(?:\.[\d]+)?)

# 과학적 표기법 포함
(-?[\d]+(?:\.[\d]+)?(?:[eE][+-]?\d+)?)
```

### 로그 레벨

```text
# INFO, WARN, ERROR, DEBUG
(INFO|WARN(?:ING)?|ERROR|DEBUG|FATAL)

# 대괄호로 감싼 레벨
\[(INFO|WARN|ERROR|DEBUG)\]
```

### 파일 경로

```text
# Unix 경로
(/(?:[^/\s]+/)*[^/\s]*)

# 파일명만 (확장자 포함)
(\w[\w.-]+\.\w+)
```

## 패턴 예제: 로그 파일 파싱

### Apache/Nginx 액세스 로그

```text
입력: 192.168.1.1 - - [01/Jan/2024:10:00:00 +0000] "GET /api/data HTTP/1.1" 200 1234
```

```json
{
  "template": {
    "type": "REGEX",
    "pattern": "(?P<ip>\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}) \\S+ \\S+ \\[(?P<ts>[^\\]]+)\\] \"(?P<method>\\S+) (?P<path>\\S+)[^\"]*\" (?P<status>\\d+) (?P<size>\\d+)",
    "columns": [
      {"name": "client_ip", "type": "IPV4",     "group": "ip"},
      {"name": "time",      "type": "DATETIME",  "group": "ts", "format": "DD/Mon/YYYY:HH24:MI:SS"},
      {"name": "method",    "type": "VARCHAR",   "group": "method"},
      {"name": "path",      "type": "VARCHAR",   "group": "path"},
      {"name": "status",    "type": "INTEGER",   "group": "status"},
      {"name": "size",      "type": "LONG",      "group": "size"}
    ]
  }
}
```

### 센서 데이터 로그

```text
입력: [2024-01-01 10:00:05.123] SENSOR sensor-01 TEMP=23.5 HUM=65.2
```

```json
{
  "template": {
    "type": "REGEX",
    "pattern": "\\[(?P<ts>\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}\\.\\d{3})\\] \\S+ (?P<sensor>\\S+) TEMP=(?P<temp>[\\d.]+) HUM=(?P<hum>[\\d.]+)",
    "columns": [
      {"name": "time",        "type": "DATETIME", "group": "ts",     "format": "YYYY-MM-DD HH24:MI:SS.FF3"},
      {"name": "name",        "type": "VARCHAR",  "group": "sensor"},
      {"name": "temperature", "type": "DOUBLE",   "group": "temp"},
      {"name": "humidity",    "type": "DOUBLE",   "group": "hum"}
    ]
  }
}
```

## 주의 사항

- JSON 설정 파일 내에서 정규식 패턴은 백슬래시(`\`)를 이중으로 이스케이프(`\\`)해야 합니다.
- 패턴이 줄 전체를 매칭하지 않아도 됩니다. 패턴에 매칭되는 첫 번째 위치부터 캡처 그룹을 추출합니다.
- 매칭되지 않는 행은 건너뜁니다. 로그 파일의 헤더나 구분선은 패턴에 매칭되지 않으면 자동으로 무시됩니다.
- 정규식 성능을 위해 `.*`와 같은 탐욕적 패턴보다는 명시적 패턴(`[^\]]+` 등)을 사용합니다.
