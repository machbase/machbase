---
layout : post
title : 'Timezone'
type : docs
---

## 목차

* [Machbase의 Timezone](#machbase의-timezone)
* [Machbase의 Timezone 형식](#machbase의-timezone-형식)
    * [machsql](#machsql)
    * [machloader](#machloader)
    * [SDK](#sdk)
    * [Rest API](#rest-api)

## Machbase의 Timezone

Machbase는 각 클라이언트의 Timezone이 각 세션에서만 유효하다고 가정합니다.

일반적으로 타임존은 특정 시간을 나타내는 문자열로 지정됩니다.

```
"YYYY-MM-DD HH24:MI:SS ZZZ(Timezone String)"

예제)
"12:06:56.568+01:00"
"2006.07.10 at 15:08:56 -05:00"
"09  AM, GMT+09:00"
```

그러나 위의 방법은 매번 타임존을 기준으로 특정 시간을 지정해야 하는 불편함이 있을 뿐만 아니라, 대량의 데이터에 대해 타임존 값을 포함하면 데이터 전송량이 선형적으로 증가하는 문제가 있습니다.

따라서 Machbase는 클라이언트와 서버가 연결된 세션에 대해 타임존 속성을 지정하는 방법을 지원합니다.

다음은 Machbase가 제공하는 타임존 동작에 대한 단계별 설명입니다.

* 서버는 서버가 설치된 운영 체제에서 제공하는 기본 타임존을 기준으로 작동합니다.<br>
    즉, 설정을 하지 않으면 Machbase는 OS가 작동하는 타임존을 읽어서 사용합니다.

* 클라이언트 프로그램이 타임존을 설정하지 않고 서버에 연결하면, 클라이언트의 타임존은 서버의 타임존으로 설정됩니다.<br>
    즉, 서버에 설정된 TIMEZONE이 KST인 경우, 클라이언트도 KST로 작동한다는 의미입니다.

* 클라이언트 프로그램에서 타임존을 명시적으로 설정하면, 서버의 해당 세션은 클라이언트가 지정한 타임존에서 작동합니다.<br>
    즉, 서버에 설정된 TIMEZONE이 KST이더라도, 클라이언트가 연결할 때 타임존을 EDT로 설정하면 세션은 EDT로 작동합니다.

## Machbase의 Timezone 형식

Machbase는 사용 편의성을 높이고 복잡성을 제거하기 위해 5자로 구성된 하나의 형식만 제공합니다.

즉, 첫 번째 문자는 시간의 부호를 나타내는 + 또는 - 기호이고, 다음 두 문자는 00과 23 사이의 값을 갖습니다. 그리고 마지막 두 문자는 00에서 59까지의 시간을 갖는다고 가정합니다.

다음은 Machbase가 지원하는 TIMEZONE 형식을 보여줍니다.

```
예제)
TIMEZONE=+0900
TIMEZONE=-0900
```

### machsql
---

machsql을 시작할 때 다음 옵션을 통해 작동할 타임존을 설정할 수 있습니다.

```
-z, --timezone=+-HHMM
```

SHOW TIMEZONE 명령을 통해 현재 설정된 타임존을 확인할 수 있습니다.

```
SHOW TIMEZONE;

Mach> show timezone;
Timezone : +0900
```

### machloader
---

machloader를 실행할 때 다음 옵션을 통해 작동할 타임존을 설정할 수 있습니다.

```
-z, --timezone=+-HHMM
```

지정된 타임존으로 연결하며 시간 계산은 해당 타임존을 기준으로 작동합니다.

### SDK
---

연결 문자열에 TIMEZONE이 추가되었으며, 세션에 대한 타임존을 지정할 수 있습니다.

연결 문자열에 TIMEZONE을 지정하지 않으면 서버의 타임존을 기준으로 작동합니다.

이것은 CLI, ODBC, JDBC 및 DOTNET에서 동일합니다.

연결 문자열 예제

```
SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;NLS_USE=UTF8;PORT_NO=5656;TIMEZONE=+0300
```

### Rest API
---

Rest API는 작업을 요청할 때 HTTP 프로토콜 HEADER에 지정된 타임존을 기준으로 작동합니다.

헤더 이름은 The-Timezone-Machbase이며, 사용법은 다음과 같습니다.

```
Authorization: Basic XXXXXXXXXXXXXXXXXXX
...................
The-Timezone-Machbase: +0900
...............
```

위에서 설명한 것처럼 원하는 Timezone 문자열을 지정할 수 있습니다.

Timezone이 지정되지 않으면 서버의 Timezone으로 작동합니다.

요청 예제: UTC로 설정

```
curl -H "The-Timezone-Machbase: +0000" -G "http://127.0.0.1:${ITF_HTTP_PORT}/machbase" --data-urlencode 'q=select * from test_table order by c4 asc';
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "C1",
      "type": 4,
      "length": 6
    },
    {
      "name": "C2",
      "type": 8,
      "length": 11
    },
    {
      "name": "C3",
      "type": 5,
      "length": 20
    },
    {
      "name": "C4",
      "type": 6,
      "length": 31
    },
    {
      "name": "C5",
      "type": 32,
      "length": 15
    }
  ],
  "timezone": "+0000",
  "data": [
    {
      "C1": 1,
      "C2": 2,
      "C3": "test1",
      "C4": "1999-09-09 00:09:09 000:000:000",
      "C5": "127.0.0.1"
    },
  ]
}
```

결과 JSON의 "timezone" 항목에 설정된 타임존 값이 반환됩니다.
