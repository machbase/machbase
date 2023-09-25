---
layout : post
title : 'Timezone'
type: docs
---

## 목차

* [마크베이스의 Timezone](#마크베이스의-timezone)
* [마크베이스의 Timezone 지원 형식](#마크베이스의-timezone-지원-형식)
    * [machsql](#machsql)
    * [machloader](#machloader)
    * [SDK](#sdk)
    * [Rest API](#rest-api)

## 마크베이스의 Timezone
마크베이스는 각 클라이언트의 타임존을 세션 단위에서 유효한 것으로 가정한다.

일반적으로는 특정한 시간을 나타내는 스트링으로 타임존을 지정하는 방식을 사용한다.
```
"YYYY-MM-DD HH24:MI:SS ZZZ(타임존스트링)"

예) 
"12:06:56.568+01:00"  
"2006.07.10 at 15:08:56 -05:00"
"09  AM, GMT+09:00"
```
그러나 위의 방식은 특정 시간을 매번 타임존을 기준으로 지정해야 하는 불편함이  있을 뿐만 아니라, 대량의 데이터에 대해서 모두 타임존의 값이 포함된 경우 데이터 전송량이 선형적으로 늘어나는 문제가  있다.

따라서 마크베이스에서는 클라이언트와 서버가 연결된 세션에 대해 타임존 속성을 지정하는 방식을 지원한다.

다음은, 마크베이스에서 제공하는 타임존이 동작에 대한 단계적 설명이다.

- 서버는 그 서버가 설치된 운영체제에서 제공하는 기본 타임존을 기준으로 동작한다.
즉, 아무런 설정을 하지  않았을 경우 마크베이스는 해당 운영체제가 동작하는 타임존을 읽어서 활용한다.

- 클라이언트 프로그램에서 타임존 설정없이 서버로 접속하면 해당 클라이언트의 타임존의 서버의 타임존으로 설정된다.
즉, 서버에서 설정된 TIMEZONE이 KST이라면, 클라이언트 역시 KST로 동작한다는 뜻이다.

- 클라이언트 프로그램에서 타임존을 명시적으로 설정한 경우에는 해당 서버의 해당 세션은 클라이언트에서 지정한 타임존으로 동작한다.
즉, 서버에서  설정된 TIMEZONE이 KST이라 하더라도, 만일 클라이언트가 접속시 EDT로 타임존을 설정한 경우에는 해당 세션은 EDT로 동작한다.

## 마크베이스의 Timezone 지원 형식
마크베이스는 사용상의 편의성 증진과 복잡성을 제거하기  위해 5자리의 문자로 구성된 단 한가지 포맷만을 제공한다.

즉, 첫번째 문자는 + 혹은 -의 기호로 시간의 부호를 나타내고, 이어지는 두개의 문자는 00에서 23 사이의 값을 가진다. 그리고, 마지막 두개의 문자는 00에서 59까지의 시간을 가지는 것으로 한다.

아래는 마크베이스에서 지원하는 TIMEZONE의 형식을 나타낸  것이다.
```
ex)
TIMEZONE=+0900
TIMEZONE=-0900
```

## machsql
machsql은 구동시 아래와 같은 옵션을 통해 동작할 타임존을 설정할 수 있다.
```
-z, --timezone=+-HHMM
```
SHOW TIMEZONE 명령을 통해 현재 자신이 설정된 타임존을 확인할 수 있다.
```
SHOW TIMEZONE;

Mach> show timezone;
Timezone : +0900
```
## machloader
machloader는  구동시 아래와 같은 옵션을 통해 동작할 타임존을 설정할 수 있다.
```
-z, --timezone=+-HHMM
```
지정된 타임존으로 접속하고, 시간 연산도 해당 타임존을 기준으로 동작한다.

## SDK
연결 스트링에 TIMEZONE이 추가되었으며, 해당 세션에 대한 타임존을 지정할 수 있다.

만일 연결 스트링에 TIMEZONE을 지정하지 않을 경우에는 서버의 타임존을 기준으로 동작한다.

이는 CLI, ODBC, JDBC, DOTNET 모두 동일한다.

`연결 string 예제`
```
SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;NLS_USE=UTF8;PORT_NO=5656;TIMEZONE=+0300
```
## Rest API
Rest API는 동작 요청시 HTTP 프로토콜의 HEADER에서 지정된 타임존을 기준으로 동작한다.

그 헤더의 이름은 `The-Timezone-Machbase으로 명명되었으며,  사용법은 아래와 같다.`
```
Authorization: Basic XXXXXXXXXXXXXXXXXXX
...................
The-Timezone-Machbase: +0900
...............
```
앞에서 기술한 바와 같이 원하는 타임존 스트링을 지정하면 된다.

타임존을 지정하지  않았을 경우에는 서버의 타임존으로 동작한다.

요청 예제 : UTC로 설정
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
결과 JSON에 "timezone" 항목에 설정된 타임존 값이 되돌아온다.
