---
title : 'RESTful API'
type : docs
weight: 50
---

## RESTful API 개요

Representational State Transfer (REST) 는 소프트웨어 구조 스타일 의 일종으로, 확장 가능한 웹 서비스에서 제공하는 인터페이스의 가이드라인과 모범적인 규범들로 구성되어 있다.

HTTP protocol에 정의된 4개의 Method 들이 Resource에 대한 CRUD를 정의한다.

| HTTP Method |  의미  |
|:-----------:|:------:|
| POST        | Create |
| GET         | Select |
| PUT         | Update |
| DELETE      | Delete |

마크베이스는 표준 RESTful API 방식이 아니라, POST와 GET method만을 이용하여 CRUD를 처리하는 방식으로 RESTful API라고 할 수 있다.

즉, 데이터 입력에는 POST method를 사용하고 나머지는 SQL query를 GET Method parameter로 전달하여 모든 작업을 할 수 있도록 구성되어 있다.

## Machbase RestAPI

Machbase에 웹서버를 내장하여 별도의 서버 구동 없이 Machbase에 직접 RestAPI를 수행하는 기능이다.

### RestAPI 지원 Machbase Edition

Standard / Cluster

## RestAPI 지원 Table 종류

Tag Table / Log Table / Lookup Table / Volatile Table

### Configuration 설정

machbase.conf 와 http.conf 두 가지 설정 파일이 존재한다.

* machbase.conf : Rest API를 사용하기 위해 HTTP 서버를 사용할 지와 최대 메모리 사용량 등 HTTP Server에 대한 설정을 저장
* http.conf : HTTP Web Server 자체에 대한 설정을 저장

설정 파일을 수정 하면 machbase 서버를 다시 시작해야 변경 내용이 적용된다.

#### 버전별 .conf 파일의 위치


**Standard Edition**

$MACHBASE_HOME/conf/machbase.conf

$MACHBASE_HOME/http/conf/http.conf

**Cluster Edition**

EACH_BROKER_HOME/conf/machbase.conf (Broker 별로 모두 수정)

EACH_BROKER_HOME/http/conf/http.conf (Broker 별로 모두 수정)


#### 각 .conf 파일 Property 설명

**machbase.conf (PROPERTY = VALUE 형태로 설정)**

| Property     | 설명                                                                                      |
|--------------|-------------------------------------------------------------------------------------------|
| HTTP_ENABLE  | 내장 웹 서버를 구동할 지 여부<br> 0 : 구동 안함, 1 : 구동                                     |
| HTTP_PORT_NO | 내장 웹 서버 접속 Port 번호<br> Port 범위 : 0 ~ 65535<br> Default : 5657                          |
| HTTP_MAX_MEM | 하나의 Web Session에서 사용할 최대 메모리<br> Min : 1048576 (1MB)<br> Default : 536870912 (512MB) |
| HTTP_AUTH    | 내장 웹 서버 사용 시 기본 인증을 사용할 지 여부<br> 0 : 인증 사용 안함, 1 : 인증 사용함       |

**http.conf (JSON 형식으로 설정)**

| Property                 | 설명                                                                                |
|--------------------------|-------------------------------------------------------------------------------------|
| document_root            | \$MACHBASE_HOME 기준의 html 파일 위치<br> Default : http/html ($MACHBASE_HOME/http/html) |
| max_request_size         | 1회 요청의 최대 요청 byte 크기 제한                                                 |
| request_timeout_ms       | 1회 요청의 최대 응답 대기 시간 (millisecond)                                        |
| enable_auth_domain_check | 도메인 인증을 활성화 할지 여부<br> "yes" or "no" 값으로 설정<br> Default : "no"             |
| reverse_proxy            | 요청 URL을 특정 URL로 변경<br> 참고: https://brainbackdoor.tistory.com/113              |

#### 각 .conf 파일 Sample

**machbase.conf**
```
#################################################################################
## Rest-API port
#################################################################################
HTTP_PORT_NO = 5657
  
#################################################################################
## Maximum memory per web session.
## Default Value: 536870912 (512MB)
#################################################################################
HTTP_MAX_MEM = 536870912
  
#################################################################################
## Min Value:     0
## Max Value:     1
## Default Value: 0
#
## Enable REST-API service.
#################################################################################
HTTP_ENABLE = 0
  
#################################################################################
## Min Value:     0
## Max Value:     1
## Default Value: 0
#
## Enable Basic Authentication for Rest-API service
#################################################################################
HTTP_AUTH = 0
```

**http.conf**
```
{
    "document_root":"http/html/",
    "max_request_size": "100000",
    "request_timeout_ms": "10000",
    "enable_auth_domain_check": "no",
    "reverse_proxy" : [["/machbase/tables", "http://127.0.0.1:55657/machbase"],
        ["/self_machbase_proxy", "http://127.0.0.1:55657/machbase"],
        ["/dead_proxy", "http://127.0.0.0/machbase"]]
}
```

### RestAPI 사용

DDL / DML / Append 수행 가능

```json
기본 요청 형식
 
http://addr:port/machbase?q=query&f=dateformat
 
응답 형식 DDL / Append / DML (except Select)
 
{"error_code":0, "error_message" :"Message", "data":[]}
 
응답 형식 DML (Select)
 
{"error_code":0, "error_message" :"Message", "columns":[Columns], "data":[Data]}
```

#### DDL Sample

```bash
### 테이블 생성 요청
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=create table test_table (name varchar(20), time datetime, value double)'
  
### 정상 응답
{"error_code":0, "error_message" :"No Error", "data":[]}
  
### 테이블 삭제 요청
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=drop table test_table'
  
### 정상 응답
{"error_code":0, "error_message" :"No Error", "data":[]}
```
#### DML Sample

```bash
### 로그 테이블 입력(Insert) 요청
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=insert into test_table values ("test", "1999-01-01 00:00:00", 0)'
  
### 정상 응답
{"error_code":0, "error_message" :"No Error", "data":[]}
  
### 로그 테이블 조회 요청
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from test_table'
  
### 정상 응답
{"error_code":0, "error_message": "", "columns" : [{"name":"NAME", "type":5, "length":20},{"name":"TIME", "type":6, "length":8},{"name":"VALUE", "type":20, "length":8}],"data" :[{"NAME":"test", "TIME":"1999-01-01 00:00:00 000:000:000", "VALUE":0.000}]}
```

#### APPEND Sample

```bash
### 로그 테이블 입력(Append) 요청
curl -X POST -H "Content-Type: application/json" "http://127.0.0.1:5657/machbase" -d '{"name":"test_table", "date_format":"YYYY-MM-DD","values":[["test", "1999-01-01 00:00:01", 1], ["test", "1999-01-01 00:00:02", 2], ["test", "1999-01-01 00:00:03", 3]]}'
  
### 정상 응답
{"error_code":0, "error_message" :"No Error", "data":[], "append_success":3, "append_failure":0}
```

#### Binary Append

Binary Append의 경우 Binary 데이터를 Base64로 인코딩 후 전송하면 서버에서 디코딩 후 저장하게 된다.

출력 시에는 바이너리 데이터가 Base64로 인코딩되어 반환된다.

입력 : Binary Data >> Base64 Encoding >> HTTP(POST) >> Base64 Decoding >> Append(BLOB Binary)

출력 : BLOB Binary >> Base64 Encoding >> HTTP (GET) >> Base64 Decoding >> Save or View Binary

#### Binary Append Sample

```bash
### 00 ~ FF까지의 256바이트 바이너리 데이터를 Base64로 인코딩 후 입력 / 출력 예
  
### 로그 테이블 입력(Append) 요청
curl  -X POST -H "Content-Type: application/json" "http://127.0.0.1:5657/machbase" -d '{"name":"test_table", "date_format":"YYYY-MM-DD","values":[["AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/w=="]]}'
  
### 정상 응답
{"error_code":0, "error_message" :"No Error", "data":[], "append_success":1, "append_failure":0}
  
### 로그 테이블 출력 요청
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from test_table';
  
### Base64 데이터 출력
{"error_code" :0, "error_message": "No Error", "columns" : [{"name":"V1", "type":57, "length":67108864}],"data" :[{"V1":"AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/w=="}]}
  
### machsql을 통한 HEX Dump 값 확인
select to_hex(v1) from test_table;
to_hex(v1)                                                                      
------------------------------------------------------------------------------------
000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F2021222324252627
28292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F404142434445464748494A4B4C4D4E4F
505152535455565758595A5B5C5D5E5F606162636465666768696A6B6C6D6E6F7071727374757677
78797A7B7C7D7E7F808182838485868788898A8B8C8D8E8F909192939495969798999A9B9C9D9E9F
A0A1A2A3A4A5A6A7A8A9AAABACADAEAFB0B1B2B3B4B5B6B7B8B9BABBBCBDBEBFC0C1C2C3C4C5C6C7
C8C9CACBCCCDCECFD0D1D2D3D4D5D6D7D8D9DADBDCDDDEDFE0E1E2E3E4E5E6E7E8E9EAEBECEDEEEF
F0F1F2F3F4F5F6F7F8F9FAFBFCFDFEFF                                                
[1] row(s) selected.
```

#### HTTP_AUTH Property 사용

Request Header에 'Authorization: Basic Base64String' 문자열을 포함하여 정상 유저임을 인증하도록 설정하는 옵션이다.

Base64 문자열은 ID@Host:Password 구조로 작성한다. (단, Host명은 정확하지 않아도 된다. ID, Password는 Machbase의 유저 정보를 입력해야 한다.)

**인증을 위한 Basic Base64String 생성 방법**
```bash
### ID: sys, Password: manager 일 경우의 생성 예
echo -n "sys@localhost:manager" | base64
  
### 생성된 Base64String
c3lzQGxvY2FsaG9zdDptYW5hZ2Vy
```

**Base64String 사용 Sample (HTTP_AUTH = 1 인 경우)**
```bash
### ID: sys, Password: manager 일 경우의 생성 예
echo -n "sys@localhost:manager" | base64
  
### 생성된 Base64String
c3lzQGxvY2FsaG9zdDptYW5hZ2Vy
```

**Base64String 사용 Sample (HTTP_AUTH = 1 인 경우)**
```bash
### Authorization을 넣지 않은 요청의 예
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from v$stmt'
  
### 에러 발생
{"error_code":3118, "error_message" :"There is No Authorization Header.", "data":[]}
  
### Request Header에 'Authorization:Base64String' 추가한 요청의 예
curl -H "Authorization: Basic c3lzQGxvY2FsaG9zdDptYW5hZ2Vy"  -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from v$stmt'
  
### 정상 응답
{"error_code":0, "error_message": "No Error", "columns" : [{"name":"ID", "type":8, "length":4},{"name":"SESS_ID", "type":8, "length":4},{"name":"STATE", "type":5, "length":64},{"name":"RECORD_SIZE", "type":8, "length":4},{"name":"QUERY", "type":5, "length":32767}],"data" :[{"ID":0, "SESS_ID":52, "STATE":"Fetch prepared", "RECORD_SIZE":0, "QUERY":"select * from v$stmt"}]}
```

#### 출력 소수점 Scale 지정 (s 옵션)

응답 데이터의 소수점을 몇자리까지 출력할 지 지정

0 ~ 9 값으로 설정 (범위 값이 아닐 경우 3으로 동작)

**소수점 5자리까지 출력 Sample (s=5)**
```bash
### 소수점 5자리까지 출력
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from test_table' --data-urlencode 's=5';
  
### 정상 응답
{"error_code" :0, "error_message": "", "columns" : [{"name":"C1", "type":16, "length":4},{"name":"C2", "type":20, "length":8}],"data" :[{"C1":12345.00000, "C2":1234.01235}]}
```

#### 데이터 Fetch 모드 변경 (m 옵션)

응답 data에 column 이름을 항상 붙여서 표시할 지 결정 (0 : 표시, 1 : 표시 안함)

**Default Fetch mode Sample (m=0)**

```bash
### fetch mode (m=0) 요청
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from tag limit 2' --data-urlencode 'm=0';
  
### 정상 응답 (Column Name을 포함한 결과 출력)
{"error_code" :0, "error_message": "", "columns" : [{"name":"NAME", "type":5, "length":20},{"name":"TIME", "type":6, "length":8},{"name":"VALUE", "type":20, "length":8}],
"data" :[{"NAME":"tag1", "TIME":"2001-09-09 10:46:40 000:000:000", "VALUE":1000000000.000}, {"NAME":"tag1", "TIME":"2001-09-09 10:46:41 000:000:000", "VALUE":1000000001.000}]}
```

**Advanced Fetch mode Sample (m=1)**

```bash
### fetch mode (m=1) 요청
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from tag limit 2' --data-urlencode 'm=1';
  
### 정상 응답 (Column Name이 생략된 결과 출력)
{"error_code" :0, "error_message": "", "columns" : [{"name":"NAME", "type":5, "length":20},{"name":"TIME", "type":6, "length":8},{"name":"VALUE", "type":20, "length":8}],
"data" :[["tag1", "2001-09-09 10:46:40 000:000:000", 1000000000.000], ["tag1", "2001-09-09 10:46:41 000:000:000", 1000000001.000]]}
```
#### NULL 값의 처리

DML의 처리 중 Insert나 Append 시 NULL 값은 그대로 null로 입력하면 된다.

**Append 시 NULL 값을 포함한 JSON Sample**

```json
[["data1", "data2", "data3"],["data11", "data12", "data13"],["data21", "data22", "data23"],[null,null,null]]
```

**Select 시의 NULL 값 포함 결과 Sample**
```json
[{"C1":null, "C2":null, "C3":null, "C4":null, "C5":null, "C6":null, "C7":null, "C8":null, "C9":null, "C10":null, "C11":null, "C12":null}]
```

### RestAPI for Tag Table 사용

Tag table에 접근할 수 있는 Historian like한 RestAPI를 제공한다.

기본 요청 형식으로 http://ipaddr:port/machiot/ 또는 http://ipaddr:port/machiot-rest-api/ 를 사용한다.

또한 URL에 아래와 같은 parameter를 넘길 수 있다.

| Parameter         | 설명             | Sample                                     |
|-------------------|------------------|--------------------------------------------|
| f 또는 DateFormat | date format 지정 | XXX?f=YYYY/MM/DD<br> XXX?DateFormat=YYYY/MM/DD |
|    s 또는 Scale   |    Scale 지정    | XXX?s=12<br> XXX?Scale=12                      |
|  m 또는 FetchMode |  fetch 모드 지정 | XXX?m=1<br> XXX?FetchMode=1                    |

#### Raw 데이터 처리 함수

#### Raw Value 입력 API

이 API는 주어진 테이블에 데이터를 대량으로 입력하는 함수이다. 

**URL**

http://ipaddr:port/machiot/datapoints/raw/{Table}

http://ipaddr:port/machiot/v1/datapoints/raw/{Table}

* HTTP method : POST
* Table : 입력할 대상 태그 테이블 

**사용법**

```bash
요청
curl  -X POST -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot-rest-api/datapoints/raw/tag"
-d '{"date_format":"YYYY-MM-DD HH24:MI:SS",
     "values":
       [
          ["tag1", "1999-01-01 00:00:00", 0],
          ["tag1", "1999-01-01 00:00:01", 1],
          ["tag1", "1999-01-01 00:00:02", 2]
        ]
     }';
응답
{
   "error_code":0,
   "error_message" :"No Error",
   "timezone":"+0900",
   "data":[],
   "append_success":3,
   "append_failure":0
}
```

#### Raw Value 추출 API

이 API는 주어진 테이블의 데이터를 얻는 함수이다.

직접 URL을 모두 지정하는 방법을 기본으로 지원하고, GET method의 인자로 넘기는 방법도 지원한다. 

아래의 URL에서 각각의 디렉토리명을 인자로 지정할 수도 있다. 

**URL**

http://ipaddr:port/machiot/datapoints/raw/{Table}/{TagNames}/{Start}/{End}/{Direction}/{Count}/{Offset}

http://ipaddr:port/machiot/v1/datapoints/raw/{Table}/{TagNames}/{Start}/{End}/{Direction}/{Count}/{Offset}

* HTTP method : GET
* Table : 데이터를 가져올 대상 테이블명 
* TagNames : 데이터를 가져올 대상 태그명
  * 이 태그명은 ,(콤마)로 구분해 복수의 Tag 결과를 하나의 Series로 얻을 수 있음.
* Start : 데이터를 추출할 시작 시간값을 나타냄. 
* End :  데이터를 추출할 마지막 시간값을 나타냄
    * 시간 포맷 아래와 같이 스페이스가 없는 형태와 있는 형태 둘다 지원한다. (curl로 테스트할 경우 부가형태를 활용할 수 있다)
        * 기본 형태 (스페이스 지원, 나노초까지 지원)
            * 연-월-일 시:분:초,밀리초
            * 연-월-일 시:분:초 밀리:마이크로:나노
        * 부가 형태 (스페이스 없음, 스페이스 대신 대문자 T를 사용하며, 밀리초까지 지원)
            * 연-월-일T시:분:초,밀리초
    * 사용예)
        * "2020-12-12"
        * "2020-12-12 03:22:22"
        * "2020-12-12 03:22:22 222:333:444"
        * "2020-12-12T03:22:22"
        * "2020-12-12T03:22:22,234"
* Direction (생략 가능)
    * 0 (디폴트): 디폴트 값으로서 입력된 순서대로 출력
    * 1 : 시간이 감소하는 방향으로 값을 출력
    * 2 : 시간이 증가하는 방향으로 값을 출력

* Count (생략 가능)

    * 0 (디폴트): 전체 데이터를 모두 출력
    * 기타 값 : 주어진 갯수 만큼 레코드를 출력

* Offset (생략 가능)
    * 0 (디폴트) : 건너뛰지 않는다. 
    * 기타 값 : 주어진 값 만큼 값을 건너 뜀

**사용법**

```bash
요청 (URL을 모두 지정하는 방법)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/raw/tag/tag-1/2001-09-09T00:00:00,000/2001-09-09T01:20:00,000/0/5/0"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "NAME",
      "type": 5,
      "length": 20
    },
    {
      "name": "TIME",
      "type": 6,
      "length": 31
    },
    {
      "name": "VALUE",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:00:01 000:000:000",
      "VALUE": 8001
    },
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:01:41 000:000:000",
      "VALUE": 8101
    },
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:03:21 000:000:000",
      "VALUE": 8201
    },
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:05:01 000:000:000",
      "VALUE": 8301
    },
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:06:41 000:000:000",
      "VALUE": 8401
    },
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:08:21 000:000:000",
      "VALUE": 8501
    }
  ]
}
 
요청(인자를 넘기는 방법)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/raw?Table=tag&amp;TagNames=tag-1&amp;Start=2001-09-09T00:00:00,000&amp;End=2001-09-09T01:20:00,000&amp;Direction=0&amp;Count=5&amp;Offset=0"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "NAME",
      "type": 5,
      "length": 20
    },
    {
      "name": "TIME",
      "type": 6,
      "length": 31
    },
    {
      "name": "VALUE",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:00:01 000:000:000",
      "VALUE": 8001
    },
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:01:41 000:000:000",
      "VALUE": 8101
    },
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:03:21 000:000:000",
      "VALUE": 8201
    },
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:05:01 000:000:000",
      "VALUE": 8301
    },
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:06:41 000:000:000",
      "VALUE": 8401
    }
  ]
}
  
요청 (다수의 태그(tag-1, tag-2, tag-3)를 지정하는 경우)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/raw/tag/tag-1,tag-2,tag-3/2001-09-09T00:00:00,000/2001-09-09T01:20:00,000/0/0/0";
응답
[
  {
    "NAME": "tag-1",
    "TIME": "2001-09-09 01:00:01 000:000:000",
    "VALUE": 8001
  },
  {
    "NAME": "tag-1",
    "TIME": "2001-09-09 01:01:41 000:000:000",
    "VALUE": 8101
  },
  {
    "NAME": "tag-2",
    "TIME": "2001-09-09 01:00:02 000:000:000",
    "VALUE": 8002
  },
  {
    "NAME": "tag-2",
    "TIME": "2001-09-09 01:01:42 000:000:000",
    "VALUE": 8102
  },
  {
    "NAME": "tag-3",
    "TIME": "2001-09-09 01:00:03 000:000:000",
    "VALUE": 8003
  },
  {
    "NAME": "tag-3",
    "TIME": "2001-09-09 01:01:43 000:000:000",
    "VALUE": 8103
  },
  {
    "NAME": "tag-3",
    "TIME": "2001-09-09 01:03:23 000:000:000",
    "VALUE": 8203
  }
]
```

#### 전체 Tag 기준 Raw Value 삭제 API

이 API는 입력된 모든 태그에 대해 특정 시간 이전의 데이터를 모두 삭제한다. 

이 함수는 디스크의 용량이 부족하거나, 백업이 완료된 후 더 이상 필요하지 않은 데이터를 제거하는 데 유용하게 사용할 수 있다.

**URL**

http://ipaddr:port/machiot/datapoints/raw/{Table}/{BeforeTime}

http://ipaddr:port/machiot/v1/datapoints/raw/{Table}/{BeforeTime}

* HTTP method : DELETE
* Table : 삭제할 데이터가 저장된 테이블명
* BeforeTime : 삭제할 이전 시간의 데이터 범위 

**사용법**
```bash
요청
curl -X DELETE  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/raw/tag/2001-09-09T01:20:00,000";
응답
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "effect_rows": "1201",
  "data": []
}
```
#### 특정 Tag 기준 Raw Value 삭제 API

이 API는 특정 태그에 대해 특정 시간 이전의 데이터를 모두 삭제한다. 

이 함수는 디스크의 용량이 부족하거나, 백업이 완료된 후 더 이상 필요하지 않은 데이터를 제거하는 데 유용하게 사용할 수 있다.

**URL**

http://ipaddr:port/machiot/datapoints/raw/{Table}/{TagNames}/{BeforeTime}

http://ipaddr:port/machiot/v1/datapoints/raw/{Table}/{TagNames}/{BeforeTime}

* HTTP method : DELETE
* Table : 삭제할 데이터가 저장된 테이블명
* TagNames : 삭제할 대상 태그명들. ,(콤마)로 구분된 다수의 태그를 지정할 수 있음
* BeforeTime : 삭제할 이전 시간의 데이터 범위 

**사용법**

```bash
요청
curl -X DELETE  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/raw/tag/tag-2,tag-3/2001-09-09T01:20:00,000";
응답
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "effect_rows": "32",
  "data": []
}
```
#### 통계 데이터 처리 함수 

#### 통계 추출 API

이 API는 저장된 데이터에 대한 통계 결과를 빠르게 얻는 함수이다.

**URL**

http://ipaddr:port/machiot/datapoints/calculated/{Table}/{TagNames}/{Start}/{End}/{CalculationMode}/{Count}/{IntervalType}/{IntervalValue}

http://ipaddr:port/machiot/v1/datapoints/calculated/{Table}/{TagNames}/{Start}/{End}/{CalculationMode}/{Count}/{IntervalType}/{IntervalValue}

* HTTP method : GET
* Table : 데이터를 추출할 대상 테이블명
* TagNames : 대상 태그명 
    * 만일 다수의 태그를 지정할 경우에는 그 태그들에 대한 총 연산 결과가 출력됨. (각각의 태그에 대한 통계 결과를 얻고 싶을 경우 반복 호출해야 함)
* Start, End : 데이터를 얻고자 하는 시간 범위 지정 (Raw 데이터 추출 API 참조)
* Count : 데이터의 출력 갯수 
* CalculationMode : 얻고자 하는 통계 함수를 지정하며, ,(콤마)를 통해 다수의 통계 함수를 지정할 수 있다. (지정되는 함수명은 아래와 동일해야 한다)
    * min : 최소값 
    * max : 최대값 
    * sum : 값의 총합 
    * count : 값의 갯수
    * avg : 평균 값 
* IntervalType : 얻고자 하는 시간 종류 (시, 분, 초)
    * sec : 초 단위
    * min : 분 단위
    * hour : 시간 단위
* IntervalValue : 얻고자 하는 시간 유닛 단위 
    * 0보다 큰 값으로서 60의 약수로 지정한다. 
    * 주로 5, 10, 15, 30 등이 지정된다.

**사용법**

```bash
요청 (단일 통계함수)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/calculated/tag/tag-1/2001-09-09T00:00:00,000/2001-09-09T01:20:00,000/sum/5/min/5"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "time",
      "type": 6,
      "length": 31
    },
    {
      "name": "sum",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "time": "2001-09-09 01:00:00 000:000:000",
      "sum": 24303
    },
    {
      "time": "2001-09-09 01:05:00 000:000:000",
      "sum": 25203
    },
    {
      "time": "2001-09-09 01:10:00 000:000:000",
      "sum": 26103
    },
    {
      "time": "2001-09-09 01:15:00 000:000:000",
      "sum": 27003
    },
    {
      "time": "2001-09-09 01:20:00 000:000:000",
      "sum": 9201
    }
  ]
}
요청(다중 통계함수)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/calculated/tag/tag-1/2001-09-09T00:00:00,000/2001-09-09T01:20:00,000/sum,min,max/5/min/5"
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "time",
      "type": 6,
      "length": 31
    },
    {
      "name": "sum",
      "type": 20,
      "length": 17
    },
    {
      "name": "min",
      "type": 20,
      "length": 17
    },
    {
      "name": "max",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "time": "2001-09-09 01:00:00 000:000:000",
      "sum": 24303,
      "min": 8001,
      "max": 8201
    },
    {
      "time": "2001-09-09 01:05:00 000:000:000",
      "sum": 25203,
      "min": 8301,
      "max": 8501
    },
    {
      "time": "2001-09-09 01:10:00 000:000:000",
      "sum": 26103,
      "min": 8601,
      "max": 8801
    },
    {
      "time": "2001-09-09 01:15:00 000:000:000",
      "sum": 27003,
      "min": 8901,
      "max": 9101
    },
    {
      "time": "2001-09-09 01:20:00 000:000:000",
      "sum": 9201,
      "min": 9201,
      "max": 9201
    }
  ]
}
```

#### 태그 메타 데이터 처리 함수 

이 섹션에서 사용되는 테이블의 구조는 아래와 같이 생성되었다.

```bash
curl -X GET "http://127.0.0.1:${ITF_HTTP_PORT}/machbase" --data-urlencode 'q=create tagdata table TAG (name_multi varchar(20) primary key, time_multi datetime basetime, value_multi double summarized, value2_multi short, value3_multi varchar(10)) metadata (myshortmeta short, baseip ipv4);';
```

#### 태그 정보 INSERT API

이 API는 사용할 태그를 등록할 때 사용한다.  Tag ID와 함께 테이블 생성 시 추가했던 metadata 컬럼의 갯수만큼 데이터를 입력한다. 

**URL**

http://ipaddr:port/machiot/tags/list/{TableName}

http://ipaddr:port/machiot/v1/tags/list/{TableName}

* HTTP method : POST
* TableName : 입력할 대상 태그 테이블명을 지정한다. 

**사용법**

```bash
요청
curl -X POST -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag" -d
       '{
        "values":[
            ["tag3", 0, "127.0.0.0"],
            ["tag4", 1, "127.0.0.1"],
            ["tag4", 1, "127.0.0.1"],
            ["tag5", 2, "127.0.0.2"]
         ]
        }';
응답
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "data": [],
  "append_success": 3,
  "append_failure": 1
}
#tag4의 중복 입력으로 에러 1건, 나머지 3건 성공
```

#### 태그 정보 SELECT API

**URL**

http://ipaddr:port/machiot/tags/list/{Table}/{TagName}

http://ipaddr:port/machiot/v1/tags/list/{Table}/{TagName}

* HTTP method : GET
* Table : 추출 대상 태그 테이블 
    * 만일 테이블명만 지정될 경우 모든 태그 이름의 리스트를 출력
* TagName : 추출 대상 태그명
    * 해당 태그의 상세 정보 출력 

**사용법**

```bash
요청(전체 태그명 얻기)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "name_multi",
      "type": 5,
      "length": 20
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "name_multi": "tag0"
    },
    {
      "name_multi": "tag1"
    },
    {
      "name_multi": "tag3"
    },
    {
      "name_multi": "tag4"
    },
    {
      "name_multi": "tag5"
    }
  ]
}
```

#### 태그 정보 UPDATE API

이 API는 부가 태그 정보에 대한 수정을 지원한다. 

PUT 혹은 PATCH 모두 지원되며, 입력시 사용되는 JSON 포맷의 값은 해당 테이블의 컬럼명과 동일해야 한다.

또한, 다수의 컬럼명을 지원하기 때문에 한번에 두개 이상의 컬럼의 값을 변경할 수 있다. 

**URL**

http://ipaddr:port/machiot/tags/list/{Table}/{TagName}

http://ipaddr:port/machiot/v1/tags/list/{Table}/{TagName}

* HTTP method : PUT / PATCH
* Table : 수정 대상 태그 테이블명
* TagName : 수정 대상 태그명 

**사용법**

```bash
요청(PUT 사용시)
curl -X PUT -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag/tag0" -d  '{"baseip":"192.168.0.1"}';
응답
{
   "error_code":0,
   "error_message" :"No Error",
   "timezone":"+0900",
   "effect_rows":"1",
   "data":[]
}
  
요청 (PATCH 사용시)
curl -X PATCH -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag/tag3" -d  '{"baseip":"255.255.255.0", "myshortmeta":9999 }';
응답
{
   "error_code":0,
   "error_message" :"No Error",
   "timezone":"+0900",
   "effect_rows":"1",
   "data":[]
}
```

#### 태그 정보 삭제 API

이 API는 지정된 태그를 삭제한다. 하지만 해당 태그에 raw 데이터가 존재할 경우 삭제에 실패한다. 

데이터가 존재하는 태그를 삭제하기 위해서는 해당 태그의 raw 데이터에 대한 삭제를 먼저 수행하고 난 뒤에 이 함수를 호출해야 한다. 

**URL**

http://ipaddr:port/machiot/tags/list/{Table}/{TagNames}

http://ipaddr:port/machiot/v1/tags/list/{Table}/{TagNames}

* HTTP method : DELETE
* Table: 삭제 대상 태그 테이블명
* TagName: 삭제할 대상 태그명

**사용법**

```bash
요청 (데이터가 있는 태그의 경우)
curl -X DELETE -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag/tag0";
응답 (에러)
{
   "error_code":2324,
   "error_message" :"Cannot delete tagmeta. there exist data with deleted_tag key.",
   "timezone":"+0900",
   "data":[]
}
 
 
요청 (데이터가 모두 삭제된 태그의 경우)
curl -X DELETE -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag/tag4";
응답 (성공)
{
   "error_code":0,
   "error_message" :"No Error",
   "timezone":"+0900",
   "effect_rows":"1",
   "data":[]
}
```

#### 기타 함수

#### 시간 범위 얻기 API

이 API는 지정된 테이블 및 태그의 데이터에 대한 전체의 시간 범위(최소, 최대)를 얻는다. 

**URL**

http://ipaddr:port/machiot/tags/range/{Table}/{TagName}

http://ipaddr:port/machiot/v1/tags/range/{Table}/{TagName}

* HTTP method : GET
* Table : 추출한 대상 테이블명 
* TagName : 추출할 태그명
    * 지정하지 않았을 경우 전체 시간 범위 반환(이때 태그명은 ALL로 되돌아온다)

**사용법**

```bash
요청 (전체 테이블 범위)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/range/tag"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "name",
      "type": 5,
      "length": 3
    },
    {
      "name": "min",
      "type": 6,
      "length": 31
    },
    {
      "name": "max",
      "type": 6,
      "length": 31
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "name": "ALL",
      "min": "2001-09-09 01:00:00 000:000:000",
      "max": "2032-09-09 10:46:49 000:000:000"
    }
  ]
}
  
요청(특정 태그 tag-1, tag-2에 대한 시간 범위)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/range/tag/tag-1,tag-2"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "name",
      "type": 5,
      "length": 20
    },
    {
      "name": "min",
      "type": 6,
      "length": 31
    },
    {
      "name": "max",
      "type": 6,
      "length": 31
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "name": "tag-1",
      "min": "2001-09-09 01:00:01 000:000:000",
      "max": "2001-09-21 12:31:41 000:000:000"
    },
    {
      "name": "tag-2",
      "min": "2001-09-09 01:00:02 000:000:000",
      "max": "2001-09-21 12:31:42 000:000:000"
    }
  ]
}
```

#### 최소 value 얻기 API

이 API는 지정된 테이블 혹은 태그에 존재하는 최소 Value를 얻는다.

**URL**

http://ipaddr:port/machiot/tags/min/{Table}/{TagName}

http://ipaddr:port/machiot/v1/tags/min/{Table}/{TagName}

* HTTP method : GET
* Table : 추출한 대상 테이블명 
* TagName : 추출할 태그명
    * 지정하지 않았을 경우 해당 테이블의 최소 value만을 출력

**사용법**

```bash
요청 (전체 테이블)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/min/tag"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "min",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "min": 0.0
    }
  ]
}
 
 
요청 (특정 태그 tag-1, tag-2)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/min/tag/tag-1,tag-2";
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "name",
      "type": 5,
      "length": 100
    },
    {
      "name": "time",
      "type": 6,
      "length": 31
    },
    {
      "name": "min",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "name": "tag-1",
      "time": "2001-09-09 10:46:42 000:000:000",
      "min": 10001.0
    },
    {
      "name": "tag-2",
      "time": "2001-09-09 10:46:43 000:000:000",
      "min": 10002.0
    }
  ]
}
```

#### 최대 value 얻기 API

이 API는 지정된 테이블 혹은 태그에 존재하는 최대 Value를 얻는다.

**URL**

http://ipaddr:port/machiot/tags/max/{Table}/{TagName}

http://ipaddr:port/machiot/v1/tags/max/{Table}/{TagName}

* HTTP method : GET
* Table : 추출한 대상 테이블명 
* TagName : 추출할 태그명
    * 지정하지 않았을 경우 해당 테이블의 최대 value만을 출력

**사용법**

```bash
요청 (전체 테이블)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/max/tag"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "max",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "max": 10000000000.0
    }
  ]
}
 
 
요청 (특정 태그 tag-1, tag-2)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/max/tag/tag-1,tag-2";
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "name",
      "type": 5,
      "length": 100
    },
    {
      "name": "time",
      "type": 6,
      "length": 31
    },
    {
      "name": "max",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "name": "tag-1",
      "time": "2001-09-09 13:12:12 000:000:000",
      "max": 9999999991.0
    },
    {
      "name": "tag-2",
      "time": "2001-09-09 13:12:13 000:000:000",
      "max": 9999999992.0
    }
  ]
}
```

#### 최초 row 얻기 API

이 API는 지정된 테이블 혹은 태그에 존재하는 가장 작은 time값의 row를 얻는다.

**URL**

http://ipaddr:port/machiot/tags/first/{Table}/{TagName}

http://ipaddr:port/machiot/v1/tags/first/{Table}/{TagName}

* HTTP method : GET
* Table : 추출한 대상 테이블명 
* TagName : 추출할 태그명
    * 지정하지 않았을 경우 해당 테이블의 최초 row를 출력

**사용법**

```bash
요청 (전체 테이블)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/first/tag"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "NAME",
      "type": 5,
      "length": 20
    },
    {
      "name": "TIME",
      "type": 6,
      "length": 31
    },
    {
      "name": "VALUE",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "NAME": "tag-0",
      "TIME": "2001-09-09 01:00:00 000:000:000",
      "VALUE": 8000.0
    }
  ]
}
 
 
요청 (특정 태그 tag-1, tag-2)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/first/tag/tag-1,tag-2";
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "NAME",
      "type": 5,
      "length": 20
    },
    {
      "name": "TIME",
      "type": 6,
      "length": 31
    },
    {
      "name": "VALUE",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "NAME": "tag-1",
      "TIME": "2001-09-09 01:00:01 000:000:000",
      "VALUE": 8001.0
    },
    {
      "NAME": "tag-2",
      "TIME": "2001-09-09 01:00:02 000:000:000",
      "VALUE": 8002.0
    }
  ]
}
```
#### 최후 row 얻기 API

이 API는 지정된 테이블 혹은 태그에 존재하는 가장 큰 time값의 row를 얻는다.

**URL**

http://ipaddr:port/machiot/tags/last/{Table}/{TagName}

http://ipaddr:port/machiot/v1/tags/last/{Table}/{TagName}

* HTTP method : GET
* Table : 추출한 대상 테이블명 
* TagName : 추출할 태그명
    * 지정하지 않았을 경우 해당 테이블의 최후 row를 출력

**사용법**
```bash
요청 (전체 테이블)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/last/tag"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "NAME",
      "type": 5,
      "length": 20
    },
    {
      "name": "TIME",
      "type": 6,
      "length": 31
    },
    {
      "name": "VALUE",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "NAME": "dummy",
      "TIME": "2032-09-09 10:46:49 000:000:000",
      "VALUE": 1000000009.0
    }
  ]
}
 
 
요청 (특정 태그 tag-1, tag-2)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/last/tag/tag-1,tag-2";
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "NAME",
      "type": 5,
      "length": 20
    },
    {
      "name": "TIME",
      "type": 6,
      "length": 31
    },
    {
      "name": "VALUE",
      "type": 20,
      "length": 17
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "NAME": "tag-1",
      "TIME": "2001-09-21 12:31:41 000:000:000",
      "VALUE": 999901.0
    },
    {
      "NAME": "tag-2",
      "TIME": "2001-09-21 12:31:42 000:000:000",
      "VALUE": 999902.0
    }
  ]
}
```

#### 레코드 갯수 얻기 API

이 API는 지정된 테이블 혹은 태그에 존재하는 레코드의 갯수를 얻는다. 

**URL**

http://ipaddr:port/machiot/tags/count/{Table}/{TagNames}

혹은 

http://ipaddr:port/machiot/tags/cnt/{Table}/{TagNames}

http://ipaddr:port/machiot/v1/tags/count/{Table}/{TagNames}

혹은

http://ipaddr:port/machiot/v1/tags/cnt/{Table}/{TagNames}

* HTTP method : GET
* Table : 추출한 대상 테이블명 
* TagName : 추출할 태그명
    * 지정하지 않았을 경우 해당 테이블의 전체 레코드 갯수 출력 

**사용법**

```bash
요청 (전체 테이블)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/count/tag"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "count",
      "type": 12,
      "length": 20
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "count": 1000001
    }
  ]
}
 
 
요청 (특정 태그 tag-1, tag-2)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/count/tag/tag-1,tag-2";
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "name",
      "type": 5,
      "length": 100
    },
    {
      "name": "count",
      "type": 12,
      "length": 20
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "name": "tag-1",
      "count": 10000
    },
    {
      "name": "tag-2",
      "count": 10000
    }
  ]
}
```

#### 디스크 사용량 얻기 API

이 API는 지정된 테이블 혹은 태그가 사용중인 디스크 사용량의 근사치를 얻는다. 

**URL**

http://ipaddr:port/machiot/tags/disksize/{Table}/{TagNames}

http://ipaddr:port/machiot/v1/tags/disksize/{Table}/{TagNames}

* HTTP method : GET
* Table : 추출한 대상 테이블명 
* TagName : 추출할 태그명
    * 지정하지 않았을 경우 해당 테이블의 전체 디스크 사용량 출력

**사용법**

```bash
요청 (전체 테이블)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/disksize/tag/"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "disksize",
      "type": 12,
      "length": 20
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "disksize": 276904448
    }
  ]
}
 
요청 (특정 태그 tag-1, tag-2)
curl -X  GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/disksize/tag/tag-1,tag-2"
응답
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "name",
      "type": 5,
      "length": 100
    },
    {
      "name": "disksize",
      "type": 12,
      "length": 20
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "name": "tag-1",
      "disksize": 240000
    },
    {
      "name": "tag-2",
      "disksize": 240000
    }
  ]
}
```

#### 롤업 요청  API

이 API는 특정 롤업 테이블에 대한 강제적인 수행을 요청한다. 이를 통해 아직 계산되지 않은 통계 값을 계산하도록 강제한다. 

이 API를 호출하면 상황에 따라 몇초에서 몇분까지 대기할 수 있으므로 신중하게 사용해야 한다. 

**URL**

http://ipaddr:port/machiot/rollup/{Table}

http://ipaddr:port/machiot/v1/rollup/{Table}

* HTTP method : GET
* Table : 강제로 롤업을 수행할 태그 테이블명 

**사용법**

```bash
요청
curl -X HTTP GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/rollup/tag"
응답
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "data": []
}
```
