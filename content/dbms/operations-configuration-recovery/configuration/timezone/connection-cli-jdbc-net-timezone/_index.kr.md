---
type: docs
title: 'CLI/JDBC/.NET TIMEZONE 연결 옵션'
weight: 40
---

CLI, ODBC, JDBC, .NET 드라이버를 사용하여 Machbase에 연결할 때 연결 문자열에 `TIMEZONE` 파라미터를 추가하면 해당 세션의 타임존을 지정할 수 있습니다.

## CLI / ODBC 연결 문자열

ODBC 및 CLI 드라이버의 연결 문자열에 `TIMEZONE` 파라미터를 포함합니다.

```
SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;NLS_USE=UTF8;PORT_NO=5656;TIMEZONE=+0900
```

`TIMEZONE`을 지정하지 않으면 서버의 기본 타임존이 적용됩니다.

## JDBC 연결 문자열

JDBC URL에서는 쿼리 파라미터 형식으로 타임존을 지정합니다.

```
jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900
```

### Java 코드 예시

```java
String url = "jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900";
Connection conn = DriverManager.getConnection(url, "SYS", "MANAGER");
```

## .NET 연결 문자열

.NET 드라이버도 동일한 방식으로 `TIMEZONE`을 연결 문자열에 추가합니다.

```
SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;TIMEZONE=+0900
```

## Python (PyMachbase)

Python 드라이버에서는 `connect()` 함수의 `timezone` 파라미터로 지정합니다.

```python
import machbase_neo_connector as mach

conn = mach.connect(
    host="127.0.0.1",
    port=5656,
    user="SYS",
    password="MANAGER",
    timezone="+0900"
)
```

## 타임존 적용 우선순위

동일한 연결에서 여러 타임존 설정이 충돌할 경우 다음 순서로 우선순위가 결정됩니다.

1. 연결 문자열의 `TIMEZONE` 파라미터 (가장 높음)
2. 서버의 `TIMEZONE` 프로퍼티 (`machbase.conf`)
3. 서버 OS의 기본 타임존 (가장 낮음)

## 주의 사항

- 타임존은 세션 단위로 적용됩니다. 연결 풀을 사용하는 경우, 풀에서 가져온 연결의 타임존이 예상과 다를 수 있습니다. 연결 풀 초기화 시 타임존 파라미터를 명시적으로 지정하는 것을 권장합니다.
- 타임존 오프셋은 `+HHMM` 또는 `-HHMM` 형식의 5자리여야 합니다. 예: `+0900`, `-0500`.
