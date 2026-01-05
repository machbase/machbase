---
title : '데이터 타입'
type: docs
weight: 10
---

# Index

* [Data Type Table](#data-type-table)
* [SQL DataType Table](#sql-datatype-table)

## Data Type Table

|Type Name|Description|Value Range|NULL Value|
|--|--|--|--|
|short|16비트 부호 있는 정수 데이터 타입|-32767 ~ 32767|-32768|
|ushort|16비트 부호 없는 정수 데이터 타입|0 ~ 65534|65535|
|integer|32비트 부호 있는 정수 데이터 타입|-2147483647 ~ 2147483647|-2147483648|
|uinteger|32비트 부호 없는 정수 데이터 타입|0 ~ 4294967294|4294967295|
|long|64비트 부호 있는 정수 데이터 타입|-9223372036854775807 ~ 9223372036854775807|-9223372036854775808|
|ulong|64비트 부호 없는 정수 데이터 타입|0~18446744073709551614|18446744073709551615|
|float|32비트 부동 소수점 데이터 타입|-|-|
|double|64비트 부동 소수점 데이터 타입|-|-|
|datetime|시간 및 날짜|1970-01-01 00:00:00 000:000:000 ~ 2262-04-11 23:47:16.854:775:807|-|
|varchar|가변 길이 문자열 (UTF-8)|Length : 1 ~ 32768 (32K)|-|
|ipv4|버전 4 인터넷 주소 타입 (4 바이트)|"0.0.0.0" ~ "255.255.255.255"|-|
|ipv6|버전 6 인터넷 주소 타입 (16 바이트)|"0000:0000:0000:0000:0000:0000:0000:0000" ~ "FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF"|-|
|text|텍스트 데이터 타입 (키워드 인덱스 생성 가능)|Length : 0 ~ 64M|-|
|binary|바이너리(Log: 0~64M) / 태그 고정 길이(1~32K-1)|Log: 0 ~ 64M<br>Tag: 1 ~ 32767 bytes|-|
|json|json 데이터 타입|json data length : 1 ~ 32768 (32K)<br><br>json path length : 1 ~ 512|-|

### short

C 언어의 16비트 부호 있는 정수 데이터와 동일합니다. 최소 음수 값의 경우 NULL로 인식됩니다. "int16"으로 표시될 수 있습니다.

### integer

C 언어의 32비트 부호 있는 정수 데이터와 동일합니다. 최소 음수 값의 경우 NULL로 인식됩니다. "int32" 또는 "int"로 표시될 수 있습니다.

### long

C 언어의 64비트 부호 있는 정수 데이터와 동일합니다. 최소 음수 값의 경우 NULL로 인식됩니다. "int64"로 표시될 수 있습니다.

### float

C 언어의 32비트 부동 소수점 데이터 타입 float와 동일합니다. 양수 최대값의 경우 NULL로 인식됩니다.

### double

C 언어의 64비트 부동 소수점 데이터 타입 double과 동일합니다. 양수 최대값의 경우 NULL로 인식됩니다.

### datetime

Machbase에서 이 타입은 1970년 1월 1일 자정 이후 경과된 시간의 나노초 값을 유지합니다.

따라서 Machbase는 모든 datetime 타입 관련 함수에서 나노초 단위까지 값을 처리하는 기능을 제공합니다.

### varchar

가변 길이 문자열 데이터 타입이며 최대 32K 바이트까지 생성할 수 있습니다.

이 길이 기준은 영문 한 문자 기준이므로 UTF-8에서 출력할 실제 문자 수와는 다르며 적절한 길이로 설정해야 합니다.

### IPv4

Internet Protocol 버전 4에서 사용하는 주소를 저장할 수 있는 타입입니다.

내부적으로 4바이트를 사용하여 표현되며 "0.0.0.0"부터 "255.255.255.255"까지 표현할 수 있습니다.

### IPv6

Internet Protocol 버전 6에서 사용하는 주소를 저장할 수 있는 타입입니다.

내부적으로 16바이트가 표현되며 "0000:0000:0000:0000:0000:0000:0000:0000"부터 "FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF"까지 표현할 수 있습니다.
데이터 입력 시 축약 타입도 지원하므로 다음과 같이 : 기호를 사용하여 표현할 수 있습니다.

* "::FFFF:1232": 모든 선행 0
* "::FFFF:192.168.0.3": IPv4 타입 호환성 지원
* "::192.168.3.1": 더 이상 사용되지 않는 IPv4 타입 호환성 지원

### text

VARCHAR 크기를 초과하는 텍스트나 문서를 저장하기 위한 데이터 타입입니다.

이 데이터 타입은 키워드 인덱스를 통해 검색할 수 있으며 최대 64메가바이트의 텍스트를 저장할 수 있습니다.
이 타입은 주로 대용량 텍스트 파일을 별도 컬럼으로 저장하고 검색하는 데 사용됩니다.

### binary

로그/룩업/볼라타일 테이블의 바이너리 컬럼은 비정형 데이터를 저장하기 위한
일반 타입입니다. 인덱스를 생성할 수 없으며 TEXT와 동일하게 최대 64MB까지
저장할 수 있습니다.

Tag 테이블의 `BINARY(n)`은 센서 프레임용 고정 길이 변형입니다.
유효 길이는 1~32K-1(32767)바이트이며, 입력은 헥스 문자열(0x 접두 선택)만
허용합니다. 홀수 자릿수는 상위 니블을 0으로, 선언 길이보다 짧으면 0x00으로
패딩합니다. 길이 초과나 비-헥스 문자는
`[ERR-02233: Error occurred at column (n): (Invalid insert value.)]` 오류를 냅니다.
`LENGTH` 및 메타데이터는 선언된 바이트 길이를 반환하며, machsql은 `0x` 없는
대문자 헥스로 출력합니다. 이 고정 길이 `BINARY(n)`은 Tag 테이블에서만
지원됩니다.

### json

json 데이터를 저장하기 위한 데이터 타입입니다.

Json은 "Key-Value" 쌍으로 구성된 데이터 객체를 텍스트 형식으로 저장하는 포맷입니다.

데이터의 최대 크기는 varchar 타입과 동일한 32K 바이트입니다.


## SQL Datatype Table

다음 표는 Machbase 데이터 타입에 해당하는 SQL 데이터 타입과 C 데이터 타입을 보여줍니다.

|Machbase Datatype|Machbase CLI Datatype|SQL Datatype|C Datatype|Basic types for C|Description|
|--|--|--|--|--|--|
|short|SQL_SMALLINT|SQL_SMALLINT|SQL_C_SSHORT|int16_t (short)|16비트 부호 있는 정수 데이터 타입|
|ushort|SQL_USMALLINT|SQL_SMALLINT|SQL_C_USHORT|uint16_t (unsigned short)|16비트 부호 없는 정수 데이터 타입|
|integer|SQL_INTEGER|SQL_INTEGER|SQL_C_SLONG|int32_t (int)|32비트 부호 있는 정수 데이터 타입|
|uinteger|SQL_UINTEGER|SQL_INTEGER|SQL_C_ULONG|uint32_t (unsigned int)|32비트 부호 없는 정수 데이터 타입|
|long|SQL_BIGINT|SQL_BIGINT|SQL_C_SBIGINT|int64_t (long long)|64비트 부호 있는 정수 데이터 타입|
|ulong|SQL_UBIGINT|SQL_BIGINT|SQL_C_UBIGINT|uint64_t (unsigned long long)|64비트 부호 없는 정수 데이터 타입|
|float|SQL_FLOAT|SQL_REAL|SQL_C_FLOAT|float|32비트 부동 소수점 데이터 타입|
|double|SQL_DOUBLE|SQL_FLOAT, SQL_DOUBLE|SQL_C_DOUBLE|double|64비트 부동 소수점 데이터 타입|
|datetime|SQL_TIMESTAMP<br><br>SQL_TIME|SQL_TYPE_TIMESTAMP<br><br>SQL_BIGINT<br><br>SQL_TYPE_TIME|SQL_C_TYPE_TIMESTAMP<br><br>SQL_C_UBIGINT<br><br>SQL_C_TIME|char * (YYYY-MM-DD HH24:MI:SS)<br><br>int64_t (timestamp: nano seconds)<br>struct tm|시간 및 날짜|
|varchar|SQL_VARCHAR|SQL_VARCHAR|SQL_C_CHAR|char *|문자열|
|ipv4|SQL_IPV4|SQL_VARCHAR|SQL_C_CHAR|char * (ip 문자열 입력)<br><br>unsigned char[4]|버전 4 인터넷 주소 타입|
|ipv6|SQL_IPV6|SQL_VARCHAR|SQL_C_CHAR|char * (ip 문자열 입력)<br><br>unsigned char[16]|버전 6 인터넷 주소 타입|
|text|SQL_TEXT|SQL_LONGVARCHAR|SQL_C_CHAR|char *|텍스트|
|binary|SQL_BINARY|SQL_BINARY|SQL_C_BINARY|char *|태그 테이블용 고정 길이 바이너리|
|json|SQL_JSON|SQL_JSON|SQL_C_CHAR|json_t|json 데이터 타입|
