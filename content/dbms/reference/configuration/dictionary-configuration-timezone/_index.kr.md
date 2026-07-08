---
type: docs
title: 'Timezone 설정 사전'
weight: 50
---

Machbase는 서버 및 클라이언트 별로 타임존을 설정할 수 있습니다. datetime 값은 내부적으로 UTC 나노초로 저장되며, 타임존 설정은 입출력 변환에만 영향을 줍니다.

## 서버 타임존 프로퍼티

| 프로퍼티 | 기본값 | 설명 |
|----------|--------|------|
| `DEFAULT_TIMEZONE` | UTC | 서버 기본 타임존. 클라이언트가 타임존을 지정하지 않으면 이 값을 사용합니다 |

`machbase.conf`에서 설정합니다.

```
DEFAULT_TIMEZONE = Asia/Seoul
```

서버 재시작 없이 동적으로 변경할 수도 있습니다.

```sql
ALTER SYSTEM SET DEFAULT_TIMEZONE = 'Asia/Seoul';
```

## 지원 타임존 표현 형식

| 형식 | 예시 | 설명 |
|------|------|------|
| UTC | `UTC` | 협정 세계시 |
| IANA 지역명 | `Asia/Seoul`, `America/New_York`, `Europe/London` | IANA 타임존 데이터베이스 기준 |
| UTC 오프셋 | `+09:00`, `-05:30`, `+0900`, `-0530` | UTC 기준 오프셋 |

## 클라이언트별 타임존 설정

### machsql

`-z` 또는 `--timezone` 옵션으로 세션 타임존을 지정합니다.

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -z +0900
machsql -s 127.0.0.1 -u SYS -p MANAGER --timezone=Asia/Seoul
```

### machloader

`-z` 또는 `--timezone` 옵션으로 가져오기/내보내기 시 datetime 변환 타임존을 지정합니다.

```bash
machloader -i -d data.csv -t table_name -z +0900
machloader -o -d data.csv -t table_name -z Asia/Seoul
```

### JDBC

JDBC 연결 문자열의 `timeZone` 속성으로 지정합니다.

```
jdbc:machbase://127.0.0.1:5656/machbase?timeZone=Asia/Seoul
```

### REST API

쿼리 파라미터 `tz`로 지정합니다.

```
GET /db/query?q=SELECT+*+FROM+table&tz=Asia/Seoul
```

### Go 드라이버

연결 문자열에 `tz` 파라미터를 추가합니다.

```go
dsn := "tcp://127.0.0.1:5656?tz=Asia/Seoul"
```

## 타임존 우선순위

클라이언트에서 타임존을 명시하면 서버의 `DEFAULT_TIMEZONE` 설정보다 우선 적용됩니다.

```
클라이언트 지정 타임존 > DEFAULT_TIMEZONE 서버 설정 > UTC(내부 저장 형식)
```

## 타임존 변환 예시

`Asia/Seoul` (+09:00) 타임존을 사용하는 경우, UTC `2024-01-01 00:00:00`은 다음과 같이 표시됩니다.

```sql
-- machsql에서 타임존 설정 시
Mach> SET TIMEZONE = 'Asia/Seoul';
Mach> SELECT TO_CHAR(_ARRIVAL_TIME, 'YYYY-MM-DD HH24:MI:SS') FROM sensor_data LIMIT 1;
2024-01-01 09:00:00
```
