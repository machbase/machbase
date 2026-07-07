---
type: docs
title: '타임존 연결 옵션'
weight: 20
---

Machbase는 모든 시간 데이터를 내부적으로 UTC nanosecond 정수로 저장합니다. 조회 시 어떤 timezone으로 표시할지는 연결 옵션 또는 SQL 함수로 제어합니다.

## 내부 저장 방식

```
저장: UTC 기준 nanosecond 정수 (예: 1720000000000000000)
표시: 서버 또는 연결 timezone에 따라 변환
```

timezone 설정 없이 조회하면 서버 또는 세션의 기본 timezone으로 표시됩니다. 한국 표준시(KST, UTC+9)처럼 특정 timezone으로 표시하려면 연결 시 timezone을 지정하거나 애플리케이션에서 변환합니다.

## 연결 시 timezone 설정

### JDBC

```java
// timezone 파라미터를 URL에 포함
String url = "jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900";
Connection conn = DriverManager.getConnection(url, "SYS", "MANAGER");

// 또는 Properties 사용
Properties props = new Properties();
props.setProperty("user", "SYS");
props.setProperty("password", "MANAGER");
props.setProperty("TIMEZONE", "+0900");
Connection conn = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/machbasedb", props);
```

### Python

```python
from machbaseAPI import connect

conn = connect(
    host='127.0.0.1',
    port=5656,
    user='SYS',
    password='MANAGER',
    timezone='Asia/Seoul'  # IANA timezone 이름
)
```

### .NET (MachClient)

```csharp
string connStr = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;" +
                 "PROTOCOL=4.0-full;TIMEZONE=Asia/Seoul";
MachConnection conn = new MachConnection(connStr);
conn.Open();
```

### ODBC

ODBC 연결 문자열에서 timezone을 설정할 수 있습니다. 드라이버 버전에 따라 지원 여부가 다르므로 14장 레퍼런스를 확인하세요.

```c
char connStr[] = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;"
                 "PROTOCOL=4.0-full;TIMEZONE=9";
// TIMEZONE 값: UTC offset (시간 단위), 예: KST = 9
```

## 쿼리에서 시간 문자열 처리

연결 timezone은 드라이버/세션 설정을 따릅니다. SQL에서는 `TO_CHAR`로 `DATETIME`
값을 문자열로 만들고, `TO_DATE`로 문자열을 `DATETIME` 값으로 변환합니다.

### TO_CHAR로 포맷 지정

```sql
SELECT name,
       TO_CHAR(time, 'YYYY-MM-DD HH24:MI:SS') AS time_text,
       value
FROM tag_table
WHERE name = 'sensor_01'
LIMIT 10;
```

### TO_DATE로 문자열 파싱

```sql
SELECT *
FROM tag_table
WHERE time >= TO_DATE('2024-07-03 09:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 연결 timezone과 쿼리 timezone의 관계

연결 시 timezone을 설정하면 `TO_CHAR`에서 timezone 인자를 생략했을 때 연결 timezone이 기본값으로 사용됩니다.

```sql
-- 연결 timezone이 Asia/Seoul일 때
SELECT TO_CHAR(time, 'YYYY-MM-DD HH24:MI:SS') FROM tag_table;
-- → KST로 표시됨

-- 연결 timezone이 UTC일 때
SELECT TO_CHAR(time, 'YYYY-MM-DD HH24:MI:SS') FROM tag_table;
-- → UTC로 표시됨
```

## SYSDATE vs NOW

Machbase에서 현재 시각을 나타내는 두 가지 표현이 있습니다.

| 표현 | 반환값 | 용도 |
|------|--------|------|
| `SYSDATE` | 현재 시각 (UTC nanosecond) | WHERE 조건, 기본값 |
| `NOW` | 현재 시각 | `SYSDATE`와 동일 |

두 표현은 동일한 값을 반환합니다. `SYSDATE`가 더 일반적으로 사용됩니다.

```sql
-- 최근 1시간 데이터 조회
SELECT * FROM tag_table WHERE time >= SYSDATE - 3600000000000;
-- 3600000000000 = 1시간을 nanosecond로 표현 (3600 * 10^9)

SELECT * FROM tag_table
WHERE name = 'sensor_01'
  AND time >= SYSDATE - 3600000000000;
```

### SYSDATE 연산

SYSDATE에 nanosecond 정수를 더하거나 빼는 방식으로 시간 범위를 계산합니다.

```text
-- 1시간 전
SYSDATE - 3600000000000

-- 1일 전
SYSDATE - 86400000000000

-- 30분 후
SYSDATE + 1800000000000
```

자주 사용하는 nanosecond 변환값:

| 단위 | nanosecond |
|------|-----------|
| 1초 | `1,000,000,000` |
| 1분 | `60,000,000,000` |
| 1시간 | `3,600,000,000,000` |
| 1일 | `86,400,000,000,000` |

## timezone 설정 권장사항

- **서비스 단위로 통일**: 같은 서비스 내의 모든 클라이언트는 동일한 timezone으로 연결합니다. timezone이 섞이면 조회 결과가 혼란스러워집니다.
- **UTC 저장, 표시만 변환**: 내부 저장은 항상 UTC이므로, timezone 설정은 표시 형식에만 영향을 줍니다. 데이터 정합성에 영향을 주지 않습니다.
- **IANA timezone 이름 사용**: `Asia/Seoul`, `America/New_York` 등 IANA timezone 이름을 사용합니다. `+09:00` 형식의 offset은 일부 드라이버에서 지원하지 않을 수 있습니다.
