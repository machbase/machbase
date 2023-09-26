---
title : '자료형'
type: docs
weight: 10
---

## 데이터 타입 테이블

|타입명|설명|값 범위|NULL 값|
|-----|--|----|----|
|short|16비트 부호 있는 정수형 데이터 타입|-32767 ~ 32767|-32768|
|ushort|16비트 무부호 정수형 데이터 타입|0 ~ 65534|65535|
|integer|32비트 부호 있는 정수형 데이터 타입|-2147483647 ~ 2147483647|-2147483648|
|uinteger|32비트 무부호 정수형 데이터 타입|0 ~ 4294967294|4294967295
|long|64비트 부호 있는 정수형 데이터 타입|-9223372036854775807 ~ 9223372036854775807|-9223372036854775808|
|ulong|64비트 무부호 정수형 데이터 타입|0~18446744073709551614|18446744073709551615|
|float|32비트 부동 소수점 테이타 타입|-|-|
|double|64비트 부동 소수점 테이타 타입|-|-|
|datetime|시간 및 날짜|1970-01-01 00:00:00 000:000:000 ~ 2262-04-11 23:47:16.854:775:807|-|
|varchar|가변길이 문자열 (UTF-8)|길이 : 1 ~ 32768 (32K)|-|
|ipv4|Version 4의 인터넷 주소 타입 (4 바이트)|"0.0.0.0" ~ "255.255.255.255"|-
|ipv6|Version 6의 인터넷 주소 타입 (16 바이트)|"0000:0000:0000:0000:0000:0000:0000:0000" ~ "FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF"|-|
|text|텍스트 데이터형 (키워드 인덱스 생성가능)|길이 : 0 ~ 64M|-|
|binary|바이너리 데이터형<br>(인덱스 생성 불가능)|길이 : 0 ~ 64M|-|
|json|json 데이터 타입|json data 길이 : 1 ~ 32768 (32K)<br>json path 길이 : 1 ~ 512|-|

### short

C 언어의 16비트 부호있는 정수형 데이터와 동일하다. 최소 음수값에 대해서는 NULL로 인식한다. "int16" 이라고 표시해도 된다.

### integer

C 언어의 32비트 부호있는 정수형 데이터와 동일하다. 최소 음수값에 대해서는 NULL로 인식한다. "int32" 또는 "int" 라고 표시해도 된다.

### long

C 언어의 64비트 부호있는 정수형 데이터와 동일하다. 최소 음수값에 대해서는 NULL로 인식한다. "int64" 라고 표시해도 된다.

### float

C 언어의 32비트 부동 소수점 데이터타입 float와 동일하다. 양수 최대값에 대해 NULL로 인식한다.

### double

C 언어의 64비트 부동 소수점 데이터타입 double과 동일하다. 양수 최대값에 대해 NULL로 인식한다.

### datetime

마크베이스에서는 이 타입은 1970년 1월 1일 자정 이후에 흘러간 시간의 나노값을 유지한다.

따라서, 마크베이스는 datetime 타입 관련 모든 함수에 대해서 nano 단위까지 값을 처리할 수 있도록 제공한다.

### varchar

가변 문자열 데이터 타입이며, 길이는 최대 32K byte까지 생성이 가능하다.

이 길이의 기준은 영문 1자를 기준으로 한 것이기 때문에 UTF-8에서 표현하는 실제 출력되는 문자 개수와는 서로 다르며, 적절한 길이로 설정해야 한다.

### IPv4

이 타입은 인터넷 프로토콜 버전 4에서 사용되는 주소를 저장할 수 있는 타입이다.

내부적으로 4바이트를 사용하여 표현하고 있으며, "0.0.0.0" 부터 "255.255.255.255"까지 모두 표현 가능하다.

### IPv6

이 타입은 인터넷 프로토콜 버전 6에서 사용되는 주소를 저장할 수 있는 타입이다.

내부적으로 16바이트를 사용하여 표현하고 있으며, "0000:0000:0000:0000:0000:0000:0000:0000" 부터 "FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF" 까지 표현 가능하다.

데이터 입력시에는 축약형도 지원하기 때문에 : 기호를 활용하여 다음과 같이 표현할 수 있다.
* "::FFFF:1232" : 앞자리가 모두 0일 경우 
* "::FFFF:192.168.0.3" : IPv4 형 호환형 지원 
* "::192.168.3.1" : deprecated 된 IPv4 형 호환형 지원

### text

이 타입은 VARCHAR 의 크기를 넘어선 문자열 혹은 문서를 저장하기 위한 데이터 타입이다.

이 데이터 타입은 키워드 인덱스를 통해 검색이 가능하며, 최대 64메가 바이트의 텍스트를 저장할 수 있다.
이 타입은 주로 큰 텍스트 파일을 별도의 컬럼으로 저장하고, 검색하기 위한 용도로 사용된다.

### binary

이 타입은 비정형 데이터를 컬럼형태로 저장하기 위해 지원되는 타입이다.

이미지나 동영상 혹은 음성과 같은 바이너리 데이터를 저장하는데 사용되는데 이 타입에 대해 인덱스를 생성하여 검색할 수 없다.
저장하기 위한 최대 데이터 크기는 TEXT 타입과 동일하게 64 메가 바이트까지 가능하다.

### json

이 타입은 json 데이터를 저장하기 위해 지원되는 타입이다.

json이란, "Key-Value"의 쌍으로 이루어진 데이터 오브젝트를 텍스트형으로 저장한 포맷이다.
저장하기 위한 최대 데이터 크기는 varchar 타입과 동일하게 32K byte까지 생성이 가능하다.

## SQL 자료형 표

아래는, 마크베이스 자료형과 대응되는 SQL 자료형, C 자료형을 표로 나타냈다.

| Machbase Datatype | Machbase CLI Datatype             | SQL Datatype                                      | C Datatype                                          | Basic types for C                                                                       | Description           |
| - | - | - | - | ------ | --- |
| short             | SQL_SMALLINT                      | SQL_SMALLINT                                      | SQL_C_SSHORT                                        | int16_t (short)                                                                         | 16비트 부호 있는 정수형 데이터 타입 |
| ushort            | SQL_USMALLINT                     | SQL_SMALLINT                                      | SQL_C_USHORT                                        | uint16_t (unsigned short)                                                               | 16비트 무부호 정수형 데이터 타입   |
| integer           | SQL_INTEGER                       | SQL_INTEGER                                       | SQL_C_SLONG                                         | int32_t (int)                                                                           | 32비트 부호 있는 정수형 데이터 타입 |
| uinteger          | SQL_UINTEGER                      | SQL_INTEGER                                       | SQL_C_ULONG                                         | uint32_t (unsigned int)                                                                 | 32비트 무부호 정수형 데이터 타입   |
| long              | SQL_BIGINT                        | SQL_BIGINT                                        | SQL_C_SBIGINT                                       | int64_t (long long)                                                                     | 64비트 부호 있는 정수형 데이터 타입 |
| ulong             | SQL_UBIGINT                       | SQL_BIGINT                                        | SQL_C_UBIGINT                                       | uint64_t (unsigned long long)                                                           | 64비트 무부호 정수형 데이터 타입   |
| float             | SQL_FLOAT                         | SQL_REAL                                          | SQL_C_FLOAT                                         | float                                                                                   | 32비트 부동 소수점 데이터 타입    |
| double            | SQL_DOUBLE                        | SQL_FLOAT, SQL_DOUBLE                             | SQL_C_DOUBLE                                        | double                                                                                  | 64비트 부동 소수점 데이터 타입    |
| datetime          | SQL_TIMESTAMP<br><br><br>SQL_TIME | SQL_TYPE_TIMESTAMP<br>SQL_BIGINT<br>SQL_TYPE_TIME | SQL_C_TYPE_TIMESTAMP<br>SQL_C_UBIGINT<br>SQL_C_TIME | char \* (YYYY-MM-DD HH24:MI:SS 출력 포맷)<br>int64_t (timestamp: nano seconds)<br>struct tm | 시간 및 날짜               |
| varchar           | SQL_VARCHAR                       | SQL_VARCHAR                                       | SQL_C_CHAR                                          | char \*                                                                                 | 문자열                   |
| ipv4              | SQL_IPV4                          | SQL_VARCHAR                                       | SQL_C_CHAR                                          | char \* (ip 문자열 입력)<br>unsigned char[4]                                                 | Version 4 인터넷 주소 타입   |
| ipv6              | SQL_IPV6                          | SQL_VARCHAR                                       | SQL_C_CHAR                                          | char \* (ip 문자열 입력)<br>unsigned char[16]                                                | Version 6 인터넷 주소 타입   |
| text              | SQL_TEXT                          | SQL_LONGVARCHAR                                   | SQL_C_CHAR                                          | char \*                                                                                 | 텍스트                   |
| binary            | SQL_BINARY                        | SQL_BINARY                                        | SQL_C_BINARY                                        | char \*                                                                                 | 바이너리 데이터              |
| json              | SQL_JSON                          | SQL_JSON                                          | SQL_C_CHAR                                          | json_t                                                                                  | json 데이터 타입           |
