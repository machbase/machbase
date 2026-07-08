---
type: docs
title: 'Collector 템플릿과 정규식'
weight: 60
---

Collector 템플릿은 수집한 원시 텍스트 데이터를 Machbase 테이블 컬럼에 매핑하는 파싱 방식을 정의합니다. 설정 파일의 `template` 섹션에서 지정합니다.

## 지원 템플릿 타입

| 타입 | 설명 | 적합한 데이터 형식 |
|------|------|-------------------|
| `CSV` | 구분자 기반 텍스트 파싱 | CSV 파일, 쉼표/탭 구분 텍스트 |
| `JSON` | JSON 형식 파싱 | JSON Lines, REST API 응답 |
| `REGEX` | 정규식 캡처 그룹 파싱 | 로그 파일, 비정형 텍스트 |

## CSV 템플릿

쉼표 또는 지정한 구분자로 분리된 텍스트 데이터를 파싱합니다.

### 파라미터

| 파라미터 | 필수 | 기본값 | 설명 |
|---------|------|--------|------|
| `type` | 필수 | - | `"CSV"` |
| `separator` | 선택 | `","` | 필드 구분자 |
| `skip_header` | 선택 | `0` | 건너뛸 헤더 행 수 |
| `columns` | 필수 | - | 컬럼 매핑 배열 |
| `columns[].name` | 필수 | - | 대상 테이블 컬럼 이름 |
| `columns[].type` | 필수 | - | 컬럼 데이터 타입 |
| `columns[].index` | 필수 | - | CSV 필드 인덱스 (0부터 시작) |
| `columns[].format` | 선택 | - | DATETIME 파싱 포맷 |

### CSV 템플릿 예시

입력 데이터:
```text
name,time,value
sensor-01,2024-01-01 10:00:00,23.5
sensor-02,2024-01-01 10:00:01,45.1
```

설정:
```json
{
  "template": {
    "type": "CSV",
    "separator": ",",
    "skip_header": 1,
    "columns": [
      {"name": "name",  "type": "VARCHAR",  "index": 0},
      {"name": "time",  "type": "DATETIME", "index": 1, "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value", "type": "DOUBLE",   "index": 2}
    ]
  }
}
```

탭 구분자 사용:
```json
{
  "template": {
    "type": "CSV",
    "separator": "\t",
    "columns": [
      {"name": "name",  "type": "VARCHAR",  "index": 0},
      {"name": "time",  "type": "DATETIME", "index": 1, "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value", "type": "DOUBLE",   "index": 2}
    ]
  }
}
```

## JSON 템플릿

JSON 형식 데이터를 파싱하고 JSON path로 컬럼 값을 추출합니다.

### 파라미터

| 파라미터 | 필수 | 기본값 | 설명 |
|---------|------|--------|------|
| `type` | 필수 | - | `"JSON"` |
| `root` | 선택 | - | 반복 데이터의 루트 경로 (점 표기법) |
| `columns` | 필수 | - | 컬럼 매핑 배열 |
| `columns[].name` | 필수 | - | 대상 테이블 컬럼 이름 |
| `columns[].type` | 필수 | - | 컬럼 데이터 타입 |
| `columns[].path` | 필수 | - | JSON 필드 경로 (점 표기법) |
| `columns[].format` | 선택 | - | DATETIME 파싱 포맷 |

### JSON 템플릿 예시

단순 JSON:
```json
{"sensor": "sensor-01", "ts": "2024-01-01 10:00:00", "temp": 23.5}
```

```json
{
  "template": {
    "type": "JSON",
    "columns": [
      {"name": "name",  "type": "VARCHAR",  "path": "sensor"},
      {"name": "time",  "type": "DATETIME", "path": "ts",   "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value", "type": "DOUBLE",   "path": "temp"}
    ]
  }
}
```

중첩 JSON 구조:
```json
{"device": {"id": "s-01"}, "reading": {"time": "2024-01-01 10:00:00", "value": 23.5}}
```

```json
{
  "template": {
    "type": "JSON",
    "columns": [
      {"name": "name",  "type": "VARCHAR",  "path": "device.id"},
      {"name": "time",  "type": "DATETIME", "path": "reading.time",  "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value", "type": "DOUBLE",   "path": "reading.value"}
    ]
  }
}
```

배열을 포함한 JSON (`root` 사용):
```json
{"data": [{"name": "s1", "time": "2024-01-01 10:00:00", "value": 23.5}]}
```

```json
{
  "template": {
    "type": "JSON",
    "root": "data",
    "columns": [
      {"name": "name",  "type": "VARCHAR",  "path": "name"},
      {"name": "time",  "type": "DATETIME", "path": "time",  "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value", "type": "DOUBLE",   "path": "value"}
    ]
  }
}
```

## REGEX 템플릿

정규식 캡처 그룹으로 텍스트 데이터를 파싱합니다. 로그 파일 등 비정형 텍스트 수집에 적합합니다.

### 파라미터

| 파라미터 | 필수 | 기본값 | 설명 |
|---------|------|--------|------|
| `type` | 필수 | - | `"REGEX"` |
| `pattern` | 필수 | - | 정규식 패턴 (캡처 그룹 포함) |
| `columns` | 필수 | - | 컬럼 매핑 배열 |
| `columns[].name` | 필수 | - | 대상 테이블 컬럼 이름 |
| `columns[].type` | 필수 | - | 컬럼 데이터 타입 |
| `columns[].group` | 필수 | - | 캡처 그룹 번호(정수) 또는 이름(문자열) |
| `columns[].format` | 선택 | - | DATETIME 파싱 포맷 |

### REGEX 템플릿 예시

입력 데이터:
```text
[2024-01-01 10:00:00] sensor-01 23.5 OK
```

그룹 번호 사용:
```json
{
  "template": {
    "type": "REGEX",
    "pattern": "\\[(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2})\\] (\\S+) ([\\d.]+)",
    "columns": [
      {"name": "time",  "type": "DATETIME", "group": 1, "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "name",  "type": "VARCHAR",  "group": 2},
      {"name": "value", "type": "DOUBLE",   "group": 3}
    ]
  }
}
```

이름 있는 캡처 그룹 사용 (패턴 변경 시 컬럼 매핑을 수정하지 않아도 됩니다):
```json
{
  "template": {
    "type": "REGEX",
    "pattern": "\\[(?P<ts>\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2})\\] (?P<sensor>\\S+) (?P<val>[\\d.]+)",
    "columns": [
      {"name": "time",  "type": "DATETIME", "group": "ts",     "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "name",  "type": "VARCHAR",  "group": "sensor"},
      {"name": "value", "type": "DOUBLE",   "group": "val"}
    ]
  }
}
```

## 자주 쓰는 정규식 패턴

### 타임스탬프

```text
# YYYY-MM-DD HH:MM:SS
(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})

# ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)

# 밀리초 포함
(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})

# Unix timestamp
(\d{10,13})
```

### IP 주소

```text
# IPv4
(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})

# IPv4 (엄격한 범위 검사)
((?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?))
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

## DATETIME 포맷 문자열

| 포맷 | 의미 | 예시 |
|------|------|------|
| `YYYY` | 4자리 연도 | `2024` |
| `MM` | 2자리 월 | `01` |
| `DD` | 2자리 일 | `31` |
| `HH24` | 24시간제 시 | `23` |
| `MI` | 분 | `59` |
| `SS` | 초 | `00` |
| `FF3` | 밀리초 (3자리) | `123` |
| `FF6` | 마이크로초 (6자리) | `123456` |
| `FF9` | 나노초 (9자리) | `123456789` |

자주 쓰는 포맷 조합:

| 포맷 문자열 | 매칭 예시 |
|------------|----------|
| `YYYY-MM-DD HH24:MI:SS` | `2024-01-01 10:00:00` |
| `YYYY-MM-DD HH24:MI:SS.FF3` | `2024-01-01 10:00:00.123` |
| `YYYY-MM-DDTHH24:MI:SSZ` | `2024-01-01T10:00:00Z` |
| `YYYYMMDD HH24MISS` | `20240101 100000` |

## 컬럼 데이터 타입

| 타입 값 | Machbase 타입 | 설명 |
|---------|--------------|------|
| `"VARCHAR"` | VARCHAR | 문자열 |
| `"INTEGER"` | INTEGER | 32비트 정수 |
| `"LONG"` | BIGINT | 64비트 정수 |
| `"DOUBLE"` | DOUBLE | 배정밀도 실수 |
| `"FLOAT"` | FLOAT | 단정밀도 실수 |
| `"DATETIME"` | DATETIME | 날짜/시각 |
| `"IPV4"` | IPV4 | IPv4 주소 |
| `"IPV6"` | IPV6 | IPv6 주소 |
| `"TEXT"` | TEXT | 긴 문자열 |

## 정규식 패턴 작성 시 주의사항

- JSON 설정 파일 내에서 백슬래시(`\`)는 이중으로 이스케이프(`\\`)해야 합니다. 예: `\d` → `\\d`.
- 패턴이 행 전체를 매칭하지 않아도 됩니다. 패턴에 매칭되는 첫 번째 위치부터 캡처 그룹을 추출합니다.
- 패턴에 매칭되지 않는 행은 자동으로 건너뜁니다. 헤더 행이나 구분선은 별도 처리가 필요 없습니다.
- 성능을 위해 `.*` 같은 탐욕적(greedy) 패턴보다 `[^\]]+` 같은 명시적 패턴을 사용합니다.

## 참고

- Collector template 파라미터 전체 목록: [../../../reference/collector/dictionary-collector-template](../../../reference/collector/dictionary-collector-template)
- 정규식 옵션 및 패턴 모음: [../../../reference/collector/dictionary-collector-regex-options](../../../reference/collector/dictionary-collector-regex-options)
- 파일 Collector 설정: [../file-collector](../file-collector)
- socket Collector 설정: [../socket-collector](../socket-collector)
