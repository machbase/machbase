---
type: docs
title: 'Collector template 사전'
weight: 10
---

Collector template은 수집한 원시 데이터를 Machbase 테이블 컬럼에 매핑하는 파싱 방식을 정의합니다. 설정 파일의 `template` 섹션에서 지정합니다.

## 지원 템플릿 타입

| 타입 | 설명 |
|------|------|
| `CSV` | 구분자로 분리된 텍스트 파싱 |
| `JSON` | JSON 형식 데이터 파싱 |
| `REGEX` | 정규식 캡처 그룹으로 파싱 |

---

## CSV 템플릿

쉼표(`,`) 또는 지정한 구분자로 분리된 텍스트 데이터를 파싱합니다.

### 파라미터

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `type` | 필수 | string | `"CSV"` |
| `separator` | 선택 | string | 구분자 (기본값: `","`) |
| `columns` | 필수 | array | 컬럼 매핑 정의 배열 |
| `columns[].name` | 필수 | string | 대상 테이블 컬럼 이름 |
| `columns[].type` | 필수 | string | 컬럼 데이터 타입 |
| `columns[].index` | 필수 | integer | CSV 필드 인덱스 (0부터 시작) |
| `columns[].format` | 선택 | string | 시간 파싱 포맷 (DATETIME 타입인 경우) |
| `skip_header` | 선택 | integer | 건너뛸 헤더 행 수 (기본값: `0`) |

### 예시

입력 데이터:
```text
sensor-01,2024-01-01 10:00:00,23.5
sensor-02,2024-01-01 10:00:00,45.1
```

설정:
```json
{
  "template": {
    "type": "CSV",
    "separator": ",",
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
    "skip_header": 1,
    "columns": [
      {"name": "name",  "type": "VARCHAR",  "index": 0},
      {"name": "time",  "type": "DATETIME", "index": 1, "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value", "type": "DOUBLE",   "index": 2}
    ]
  }
}
```

---

## JSON 템플릿

JSON 형식 데이터를 파싱하고 JSON path로 컬럼 값을 추출합니다.

### 파라미터

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `type` | 필수 | string | `"JSON"` |
| `columns` | 필수 | array | 컬럼 매핑 정의 배열 |
| `columns[].name` | 필수 | string | 대상 테이블 컬럼 이름 |
| `columns[].type` | 필수 | string | 컬럼 데이터 타입 |
| `columns[].path` | 필수 | string | JSON 필드 경로 (점 표기법) |
| `columns[].format` | 선택 | string | 시간 파싱 포맷 (DATETIME 타입인 경우) |
| `root` | 선택 | string | 반복 데이터의 루트 경로 |

### 예시

입력 데이터:
```json
{"sensor": "sensor-01", "ts": "2024-01-01T10:00:00Z", "temp": 23.5}
```

설정:
```json
{
  "template": {
    "type": "JSON",
    "columns": [
      {"name": "name",  "type": "VARCHAR",  "path": "sensor"},
      {"name": "time",  "type": "DATETIME", "path": "ts", "format": "YYYY-MM-DDTHH24:MI:SSZ"},
      {"name": "value", "type": "DOUBLE",   "path": "temp"}
    ]
  }
}
```

중첩 JSON 구조:
```json
{"device": {"id": "sensor-01"}, "reading": {"time": "2024-01-01 10:00:00", "value": 23.5}}
```

```json
{
  "template": {
    "type": "JSON",
    "columns": [
      {"name": "name",  "type": "VARCHAR",  "path": "device.id"},
      {"name": "time",  "type": "DATETIME", "path": "reading.time", "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value", "type": "DOUBLE",   "path": "reading.value"}
    ]
  }
}
```

배열 루트 사용:
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
      {"name": "time",  "type": "DATETIME", "path": "time", "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value", "type": "DOUBLE",   "path": "value"}
    ]
  }
}
```

---

## REGEX 템플릿

정규식 캡처 그룹으로 텍스트 데이터를 파싱합니다. 로그 파일 등 비정형 텍스트 수집에 적합합니다.

### 파라미터

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `type` | 필수 | string | `"REGEX"` |
| `pattern` | 필수 | string | 정규식 패턴 (캡처 그룹 포함) |
| `columns` | 필수 | array | 컬럼 매핑 정의 배열 |
| `columns[].name` | 필수 | string | 대상 테이블 컬럼 이름 |
| `columns[].type` | 필수 | string | 컬럼 데이터 타입 |
| `columns[].group` | 필수 | integer 또는 string | 캡처 그룹 번호 또는 이름 |
| `columns[].format` | 선택 | string | 시간 파싱 포맷 |

### 예시

입력 데이터:
```text
[2024-01-01 10:00:00] sensor-01 23.5 OK
```

설정 (그룹 번호 사용):
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

이름 있는 캡처 그룹 사용:
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

## 컬럼 데이터 타입 값

| 값 | Machbase 타입 |
|----|--------------|
| `"VARCHAR"` | VARCHAR |
| `"INTEGER"` | INTEGER |
| `"LONG"` | BIGINT |
| `"DOUBLE"` | DOUBLE |
| `"FLOAT"` | FLOAT |
| `"DATETIME"` | DATETIME |
| `"IPV4"` | IPV4 |
| `"IPV6"` | IPV6 |
| `"TEXT"` | TEXT |

## DATETIME 포맷 문자열

| 포맷 | 의미 |
|------|------|
| `YYYY` | 4자리 연도 |
| `MM` | 2자리 월 |
| `DD` | 2자리 일 |
| `HH24` | 24시간제 시 |
| `MI` | 분 |
| `SS` | 초 |
| `FF3` | 밀리초 |
| `FF6` | 마이크로초 |
| `FF9` | 나노초 |
