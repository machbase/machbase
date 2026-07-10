---
type: docs
title: '17.1.6 전체 SQL 레퍼런스'
weight: 95
tocSort: true
---


## datatypes


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

로그 테이블의 바이너리 컬럼은 이미지나 문서 같은 비정형 데이터를 저장하기
위한 일반 타입입니다. TEXT와 동일하게 최대 64MB까지 저장할 수 있습니다.
Lookup 및 Volatile 테이블은 `BINARY` 컬럼을 허용하지 않습니다.

Tag 테이블의 `BINARY(n)`은 센서 프레임용 고정 길이 변형입니다.
유효 길이는 1~32K-1(32767)바이트입니다. SQL에서는 `X'...'`, `B'...'`,
`O'...'` binary literal을 사용할 수 있으며, 소문자 prefix도 지원합니다.
기존 호환성을 위해 문자열 형태의 `'0x...'` 입력도 계속 사용할 수 있습니다.
대상 `BINARY(n)` 길이를 초과하는 입력은 source 종류와 무관하게
`[ERR-02233: Error occurred at column (n): (Invalid insert value.)]` 오류를 냅니다.
메타데이터는 선언된 바이트 길이를 반환하지만, SQL `LENGTH(binary_col)`와
machsql 텍스트 출력은 짧은 입력값에 붙은 뒤쪽 0 패딩을 제외합니다.
machsql은 `0x` 없는 대문자 헥스로 출력합니다. 이 고정 길이 `BINARY(n)`은
Tag 테이블에서만 지원됩니다. 자세한 입력 형식은
[Binary 컬럼](/dbms/tag-table-usage/table-structure-schema/#original-85-binary-columns)을 참고하십시오.

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
|binary|SQL_BINARY|SQL_BINARY|SQL_C_BINARY|char *|바이너리 데이터|
|json|SQL_JSON|SQL_JSON|SQL_C_CHAR|json_t|json 데이터 타입|

## ddl


> **참고**: Machbase 8.5 이상에서는 일반 사용자가 이 문서의 `CREATE`/`DROP` 계열 구문을 실행할 때 `MACHBASEDB`에 대한 데이터베이스 권한이 필요할 수 있습니다. 자세한 권한 부여 방법은 [사용자 관리](/dbms/reference/sql/#grantrevoke)의 `GRANT/REVOKE`를 참고하세요.

## CREATE TABLE

### Syntax

**create_table_stmt:**

![create_table_stmt](/images/sql/ddl/create_table_stmt.png)

**column_list:**

![column_list](/images/sql/ddl/column_list.png)

**column_property_list:**

![column_property_list](/images/sql/ddl/column_property_list.png)

**table_property_list:**

![table_property_list](/images/sql/ddl/table_property_list.png)

**column_type:**

![column_type](/images/sql/ddl/column_type.png)

**with_rollup:**

![with_rollup](/images/sql/ddl/with_rollup_opt.png)

#### LOG 테이블 생성 예제

```sql
-- create log table 예제
CREATE TABLE ctest (id INTEGER, name VARCHAR(20), sipv4 IPV4, dipv6 IPV6, comment TEXT);
```

#### TAG 테이블 생성 예제

태그 테이블은 `PRIMARY KEY` 컬럼과 축(axis) 컬럼이 필요합니다. 시간축은 `DATETIME BASETIME` 또는 `DATETIME BASE TIME`을 사용하고, 거리축은 `DOUBLE`, `LONG`, `ULONG` 타입에 `BASE DISTANCE` 또는 `BASEDISTANCE`를 사용합니다. `SUMMARIZED`는 선택 속성이며 rollup/statistics가 필요한 값 컬럼에 지정합니다.

```sql
-- create tag table 예제
CREATE TAG TABLE tag_time (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
CREATE TAG TABLE tag_time_ext (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED, value2 FLOAT, int_column INT);
CREATE TAG TABLE tag_distance (name VARCHAR(20) PRIMARY KEY, distance_m DOUBLE BASE DISTANCE, value DOUBLE, quality INT);
CREATE TAG TABLE tag_distance_meta (name VARCHAR(20) PRIMARY KEY, distance_m LONG BASEDISTANCE, value DOUBLE) METADATA (route_id VARCHAR(20));
```

거리축 컬럼은 `DOUBLE`, `LONG`, `ULONG`만 허용합니다. `WITH ROLLUP`은 시간축 Tag 테이블에서만 사용할 수 있습니다.
TAG 메타데이터의 `JSON` 컬럼과 `JSON INDEX(...)` 선언은 [Tag 메타데이터](/dbms/tag-table-usage/tag-metadata/#original-85-tag-metadata) 문서를 참고하십시오.

#### 테이블 및 컬럼 이름

테이블 이름 또는 컬럼 이름은 영숫자(alphanumeric characters) 로 이루어집니다. 특수문자를 사용하기 위해서는 쌍따옴표(`"`) 를 사용합니다.

```sql
CREATE TABLE special_tbl ( "with.dot" INTEGER );
```

#### IF NOT EXISTS

테이블이 있는 경우 오류가 발생하지 않도록 합니다. 그러나 기존 테이블의 구조가 CREATE TABLE 문에 표시된 구조와 동일한지는 확인하지 않습니다.

같은 타입의 테이블에 대해서만 해당 기능이 동작합니다.



### 테이블 종류

|테이블 종류|설명|
|--|--|
|LOG|CREATE TABLE 사이에 아무런 키워드를 넣지 않았다면 Log Table이 생성됩니다.|
|VOLATILE|VOLATILE_TABLE은 모든 데이터가 임시 메모리에 상주하는 임시 테이블이며 로그 테이블을 조인하여 결과를 향상시킵니다만, Machbase 서버가 종료 되자마자 사라집니다.|
|LOOKUP|VOLATILE_TABLE과 마찬가지로 LOOKUP_TABLE은 메모리의 모든 데이터를 저장함으로써 빠른 쿼리 처리를 수행 할 수 있습니다.|


### 테이블 프로퍼티(Table Property)

Table에 대한 속성을 지정합니다.

|프로퍼티 이름|사용 가능한 테이블 종류|
|--|--|
|TAG_PARTITION_COUNT|TAG TABLE|
|TAG_DATA_PART_SIZE| TAG TABLE|
|TAG_STAT_ENABLE|	 TAG TABLE|
|TAG_DUPLICATE_CHECK_DURATION|	 TAG TABLE|
|VARCHAR_FIXED_LENGTH_MAX| TAG table |

#### TAG_PARTITION_COUNT(Default:4)

TAG Table에 대해 지원되는 속성으로 TAG 테이블을 내부적으로 몇 개의 파티션 테이블에 저장할 것인지 결정합니다. TAG의 수나 서버의 성능에 따라 설정해야 합니다.

#### TAG_DATA_PART_SIZE(Default:16MB)

TAG Table에 대해 지원되는 속성으로 파티션 테이블 별 데이터 사이즈를 결정합니다.

#### TAG_STAT_ENABLE(Default:1)

TAG Table에 대해 지원되는 속성으로 TAG ID 별 통계 정보 저장 여부를 결정합니다.

#### TAG_DUPLICATE_CHECK_DURATION(Default:0, Max:43200)

TAG Table에 대해 지원되는 속성으로 현재 시스템시간을 기준으로 중복 제거가 가능한 기간을 분단위로 설정합니다.
현재 시스템시간으로부터 설정된 기간 이내의 데이터에 한해서 중복을 제거할 수 있으며 0일 경우 중복제거를 수행하지 않습니다.

#### VARCHAR_FIXED_LENGTH_MAX (Default: 15, Max: 127)

내부 파일에 저장할 VARCHAR 컬럼의 최대 길이를 지정합니다.

### 컬럼 프로퍼티(Column Property)

Column에 대한 속성을 지정합니다.

|프로퍼티 이름|사용 가능한 테이블 종류|
|--|--|
|PART_PAGE_COUNT|LOG TABLE|
|PAGE_VALUE_COUNT|LOG TABLE|
|MAX_CACHE_PART_COUNT|LOG TABLE|
|MINMAX_CACHE_SIZE|LOG TABLE|

**PART_PAGE_COUNT**

이 프로퍼티는 하나의 파티션이 가지는 Page의 개수를 나타냅니다. 하나의 파티션이 가지는 Value의 개수는 PART_PAGE_COUNT * PAGE_VALUE_COUNT가 됩니다.

**PAGE_VALUE_COUNT**

이 프로퍼티는 하나의 Page가 가지는 Value의 개수를 나타냅니다.

**MAX_CACHE_PART_COUNT (Default : 0)**

이 프로퍼티는 성능 향상을 위한 캐시 영역을 설정하는 것입니다.

마크베이스 가 파티션에 접근할 때 해당 파티션의 메타 정보를 메모리에 담고 있는 구조체를 먼저 찾게 되는데, 몇 개의 파티션 정보를 메모리에 담고 있을지 결정합니다. 크면 클수록 성능에 도움이 될 것이나, 메모리 사용량이 늘어납니다. 최소값은 1 최대값은 65535입니다.

**MINMAX_CACHE_SIZE (Default : 10240)**

이 프로퍼티는 해당 Column의 MINMAX를 위한 캐시 메모리를 얼마나 사용할 것인지 지정하는 것입니다. 0번째 Hidden Column인 _ARRIVAL_TIME의 경우 기본적으로 100MB으로 지정이 됩니다. 하지만 다른 Column들은 기본적으로 10KB로 지정되어 있습니다. 이 크기는 Table의 생성 이후에도 "ALTER TABLE MODIFY" 구문을 통해서 이 값은 변경이 가능합니다.

**NOT NULL Constraint**

컬럼 값에 NULL을 허용하지 않을 경우 NOT NULL을 지정하고, 허용할 경우(Default)에는 생략합니다.

테이블 생성 이후에 정의된 이 제약조건을 삭제하거나 추가하기 위해서는 ALTER TABLE MODIFY COLUMN 명령으로 제약조건을 변경할 수 있습니다.

```sql
-- 컬럼 c1은 not null로, c2는 not null 제약 조건 없이 생성합니다.
CREATE TABLE t1(c1 INTEGER NOT NULL, c2 VARCHAR(200));
```

**Pre-defined System Columns**

Create Table 문을 이용하여 테이블을 생성하면 시스템은 두 개의 사전 정의된 시스템 컬럼을 추가로 생성합니다. _ARRIVAL_TIME 및 _RID컬럼입니다.

_ARRIVAL_TIME 컬럼은 DATETIME 타입의 컬럼으로 INSERT 문이나 AppendData로 데이터를 삽입하는 시점의 시스템 time을 기준으로 삽입되며, 해당 값은 생성된 레코드의 unique key로 사용될 수 있습니다. 이 컬럼의 값은 순서가 보장되는 경우(과거-현재 순으로) machloader나 INSERT 문에서 값을 지정하여 삽입할 수 있습니다. DURATION 조건절을 이용하여 데이터를 검색할 경우, 이 컬럼의 값을 기준으로 데이터를 검색합니다.

_RID 컬럼은 특정 레코드가 갖는 유일한 값으로 시스템이 생성합니다. 이 컬럼의 데이터 타입은 64bit 정수이며, 이 컬럼에 대해서는 사용자가 값을 지정할 수 없고 인덱스도 생성할 수 없습니다. 데이터 INSERT시에 자동으로 생성됩니다. _RID 컬럼의 값으로 레코드를 검색할 수 있습니다.

```sql
create volatile table t1111 (i1 integer);
Created successfully.
Mach> desc t1111;

----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
_ARRIVAL_TIME                 datetime            8
I1                            integer             4

Mach>insert into t1111 values (1);
1 row(s) inserted.
Mach>select _rid from t1111;
_rid
-----------------------
0
[1] row(s) inserted.

Mach>select i1 from t1111 where _rid = 0;
i1
--------------
1
[1] row(s) selected.
```

### Min Max Cache

#### Min-Max Cache 개념

일반적으로 Disk DBMS에서는 특정 값을 인덱스를 활용하여 검색할 경우 해당 인덱스가 포함된 디스크 영역에 대해 접근하고, 해당 값이 포함된 최종 디스크 페이지를 찾아가도록 구현되어 있습니다.

반면, 마크베이스는 시계열 정보를 유지하기 위해 시간순으로 파티션 되어있는 구조이며, 이것은 특정한 하나의 인덱스 정보가 시간순으로 조각조각의 파일로 나누어져 있다는 의미입니다. 따라서, 마크베이스의 인덱스를 이용할 때는 이러한 파티션으로 조각나 있는 인덱스 파일을 순차적으로 검색합니다.

만일 검색해야 할 대상 데이터의 범위가 1000개의 파티션으로 나뉘어져 있다면 1000번의 파일을 매번 열어서 검색해야 한다는 의미입니다. 비록 효율적인 컬럼형 데이터베이스 구조로 설계되어 있긴 하나, 이러한 I/O 비용이 인덱스 파티션 개수의 크기에 비례하기 때문에 그 성능을 향상하기 위한 방법이 MINMAX_CACHE 구조입니다.

이 MINMAX_CACHE는 해당 파티션의 인덱스 파일 정보를 메모리에 담고 있는 구조체로서 해당 컬럼의 최소 및 최대 값을 메모리에 유지하는 연속된 메모리 공간입니다. 이런 구조를 유지함으로써 특정 값이 포함된 파티션을 검색할 경우 그 값이 해당 인덱스의 최소값 보다 작거나 최대 값보다 클 경우에는 아예 해당 파티션을 건너뛸 수 있기 때문에 고성능의 데이터 분석이 가능해집니다.

![When you find a value "85"](/images/sql/ddl/whenyoufindavalue85.png)

위의 그림에서 볼 수 있듯이 85라는 값을 찾기 위해서 5개의 파티션 중에서 MIN/MAX에 포함된 1번과 5번 파티션만을 실제로 검색하게 되며, 2, 3, 4 번 파티션은 아예 건너뛰는 모습을 볼 수 있습니다.

#### Min-Max Cache 컬럼

테이블 생성 시에 특정 컬럼에 대해 MINMAX Cache를 사용할 것인지 결정할 수 있습니다.

만일 이 컬럼이 minmax_cache_size가 0이 아닌 값으로 설정되었으면, 해당 컬럼에 인덱스 검색 시 MINMAX Cache가 동작하게 되며, MINMAX_CACHE_SIZE = 0일 경우에는 동작하지 않습니다.

이런 MINMAX Cache를 사용할 때 다음과 같은 사항에 주의합니다.
1. MINMAX Cache 는 해당 컬럼에 인덱스를 명시적으로 생성하지 않아도 적용됩니다.
2. 모든 컬럼의 default는  MINMAX_CACHE_SIZE가 10KB로 설정되있고 Alter Table 구문을 활용하여 적정한 크기의 메모리 크기를 재설정할 수 있습니다.
3. 숨어있는 컬럼인 _arrival_time은 디폴트로 100MB이며, 자동으로 MINMAX Cache 메모리를 사용합니다.
4. VARCHAR 타입의 경우에는 MINMAX Cache 의 대상이 되지 않습니다. 따라서 VARCHAR 타입을 명시적으로 캐시 사용 여부를 지정하면, 에러가 발생합니다.
5. 해당 테이블이 하나 생성될 때 프로퍼티에 설정된  MINMAX_CACHE_SIZE 만큼 최대 메모리가 더 사용될 수 있습니다. 파티션 개수가 늘수록 메모리가 점진적으로 늘어나 위의 최대 메모리만큼 늘어납니다.
6. 만일 해당 테이블에 레코드가 하나도 들어있지 않으면, MINMAX Cache  메모리는 전혀 할당되지 않습니다.

아래는 실제 MINMAX를 활용한 테이블 생성 예를 나타냅니다.

```sql
-- VARCHAR에 대한 MINMAX_CACHE_SIZE = 0은 의미상으로 허용됩니다.
CREATE TABLE ctest (id INTEGER, name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE = 0));
Created successfully.
Mach>

-- id 컬럼에 캐시가 적용되었습니다.
CREATE TABLE ctest2 (id INTEGER PROPERTY(MINMAX_CACHE_SIZE = 10240), name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE = 0));
Created successfully.
Mach>

-- id1, id2, id3 컬럼에 적용되었습니다.
CREATE TABLE ctest3 (id1 INTEGER PROPERTY(MINMAX_CACHE_SIZE = 10240), name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE = 0), id2 LONG PROPERTY(MINMAX_CACHE_SIZE = 1024), id3 IPV4 PROPERTY(MINMAX_CACHE_SIZE = 1024), id4 SHORT);
Created successfully.
Mach>

-- Column단위로 MINMAX_CACHE_SIZE가 지정되거나, 0으로 설정되었습니다.
CREATE TABLE ctest4 (id1 INTEGER PROPERTY(MINMAX_CACHE_SIZE=10240), name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE=0), id2 LONG PROPERTY(MINMAX_CACHE_SIZE=10240), id3 IPV4 PROPERTY(MINMAX_CACHE_SIZE=0), id4 SHORT);
Created successfully.
Mach>
```

### 기본 키(Primary Key)

Volatile/Lookup 테이블의 컬럼에 부여할 수 있는 제약 사항으로, 해당 컬럼의 값이
중복되는 것을 방지합니다. Lookup 테이블은 기본 키가 필수입니다. Volatile
테이블은 기본 키를 생략할 수 있지만, `INSERT ... ON DUPLICATE KEY UPDATE`
구문은 대상 테이블에 기본 키가 있을 때만 사용할 수 있습니다.

기본 키를 부여하면, 기본 키에 대응되는 레드-블랙 트리 인덱스가 생성됩니다.

### Sequence Column

#### SEQUENCE for Lookup Table

Lookup 테이블의 Unique한 Record를 생성하고 Data의 입력 순서를 결정하기 위해 위해 Sequence가 추가되었습니다.

이 기능은 Lookup 테이블에서 datetime column을 사용하여 Record의 순서를 구분하는 방식을 사용했을 때

datetime 값이 중복될 경우 Record의 순서를 구분하기 어렵고 데이터 중복으로 인한 Application의 오류가 발생하는 등의 문제점을 해결하기 위해 추가되었습니다.

#### Lookup 테이블 생성 시 Sequence 설정

Create Table SQL 문으로 Lookup 테이블을 생성할 때 Sequence로 사용할 컬럼에 PROPERTY 절을 추가하여 Sequence를 설정하겠다고 명시하면 됩니다.

Sequence로 설정할 컬럼은 LONG datatype(64bit, unsigned)만 지원하며 이외의 datatype은 지원하지 않습니다.

추가로, Sequence의 시작값을 설정할 수 있는데 1로 설정한 경우 Sequence가 1부터 시작이 됩니다. (0이나 음수는 지원 안함)

```sql
CREATE LOOKUP TABLE table_name (v1 LONG PROPERTY(SEQUENCE=1) PRIMARY KEY, v2 VARCHAR(10));
```

#### Sequence 컬럼의 사용

Lookup 테이블의 Sequence 컬럼은 기본적으로 일반 Long 컬럼과 동일하게 사용이 가능하며 이렇게 사용할 경우 Sequence 값은 자동으로 증가하지 않습니다.

Sequence 컬럼에 직접 값을 입력하는 것이 허용되며 심지어 중복 값을 입력하는 것도 가능합니다.

대신, Sequence 기능을 사용하려면 nextval 이라는 새로 추가된 Sequence 전용 Function을 사용하여 Sequence값을 증가시키는 방식으로 사용해야 합니다.

내부적으로는 Sequence로 설정된 컬럼의 값 중 가장 큰 값에 대해 저장하고 있기 때문에 이후에 nextval Function을 사용하여 입력할 때 Sequence 컬럼 값 중 가장 큰 값 + 1 의 값이 저장됩니다.

Sequence 컬럼 사용 예:

```sql
-- Sequence 컬럼에 nextval Function을 사용하여 다음 Sequence 값 입력
INSERT INTO table_name (v1, v2) values (nextval(v1), 'aaaa');

-- Sequence 컬럼에 직접 값을 입력
INSERT INTO table_name (v1, v2) values (100, 'aaaa');

-- Sequence 컬럼에 연산을 통한 값을 입력
INSERT INTO table_name (v1, v2) values (100 + 1, 'aaaa');

-- Sequence 컬럼을 포함한 Lookup 테이블에 대한 정상 Select
SELECT v1, v2 FROM table_name;

-- Sequence 컬럼에 대한 잘못된 Select (nextval 컬럼은 insert 시에만 사용 가능)
SELECT nextval(v1), v2 FROM table_name;
```

## CREATE VIEW / DROP VIEW

VIEW는 `SELECT` 결과를 이름 있는 논리 객체로 저장해 재사용하는 기능입니다.
테이블과 달리 데이터를 별도로 저장하지 않으며, 조회 시 저장된 정의 SQL이 다시
전개되어 실행됩니다.

```sql
CREATE VIEW v_example AS
SELECT id, name
FROM t1;

DROP VIEW v_example;
```

`CREATE OR REPLACE VIEW`, `DROP VIEW IF EXISTS`, `SHOW VIEWS`, `M$SYS_VIEWS`,
성능/제한, Tag / `BINARY` 예제까지 포함한 전체 설명은 [VIEW](/dbms/reference/sql/#view) 문서를
참조하세요.

## DROP TABLE

**drop_table_stmt:**

![drop_table_stmt](/images/sql/ddl/drop_table_stmt.png)

```sql
drop_table_stmt ::= 'DROP TABLE' table_name
```

지정된 테이블을 삭제합니다. 단, 해당 테이블을 검색 중인 다른 세션이 존재할 경우에는 에러를 내면서 실패합니다.

```sql
--예제
DROP TABLE TableName;
```


## CREATE TABLESPACE

**create_tablespace_stmt:**

![create_tablespace_stmt](/images/sql/ddl/create_tablespace_stmt.png)

**datadisk_list:**

![datadisk_list](/images/sql/ddl/datadisk_list.png)

**data_disk:**

![data_disk](/images/sql/ddl/data_disk.png)

**data_disk_property:**

![data_disk_property](/images/sql/ddl/data_disk_property.png)

```sql
create_tablespace_stmt ::= 'CREATE TABLESPACE' tablespace_name 'DATADISK' datadisk_list
datadisk_list ::= data_disk ( ',' data_disk )*
data_disk ::= disk_name data_disk_property
data_disk_property ::= '(' 'DISK_PATH' '=' '"' path '"' ( ',' 'PARALLEL_IO' '=' number )? ')'
```
```sql
-- 예제
create tablespace tbs1 datadisk disk1 (disk_path=""); -- $MACHBASE_HOME/dbs/ 에 생성
create tablespace tbs1 datadisk disk1 (disk_path="tbs1_disk1"); -- $MACHBASE_HOME/dbs/tbs1_disk1 에 생성되며 이때 tbs1_disk1폴더가 존재해야 합니다.
create tablespace tbs2 datadisk disk1 (disk_path="tbs2_disk1", parallel_io = 5);
create tablespace tbs1 datadisk disk1 (disk_path="tbs1_disk1", parallel_io = 10), disk2 (disk_path="tbs1_disk2"), disk3 (disk_path="tbs1_disk3");
```

CREATE TABLESPACE 구문은 로그 Table 또는 로그 Table의 Index가 저장될 Tablespace를 $MACHBASE_HOME/dbs/ 에 생성합니다.

Tablespace는 여러 개의 Disk를 가질 수 있습니다. Table과 Index의 데이터를 저장하는 각각의 Partition File들이 저장될 때, Tablespace에 속한 Data Disk들에 분산되어 저장됩니다.

만약 2개 이상의 Disk를 사용 시 Index와 Table의 여러 File이 각 Disk에 분산 저장되고, 각각의 Device에서 Parallel 하게 IO가 수행되어 Disk 개수가 늘어날수록 Disk I/O Throughput 이 높아져 다량의 Data를 빠르게 Disk에 저장할 수 있는 이점이 있습니다.

또한, Table과 Index의 Tablespace를 별도로 생성하고 각각 다른 Disk를 정의할 경우, Physical Disk의 재구성 없이, Logical 하게 Table과 Index의 I/O를 분리할 수 있습니다.

#### DATA DISK

Tablespace에 속한 Disk를 정의합니다. 각 Disk는 다음과 같은 속성을 가집니다.

|속성|설명|
|--|--|
|data_disk_property|Disk의 속성을 지정합니다.|
|disk_name|Disk 객체의 이름을 지정합니다. 추후에 Alter Tablespace구문을 통해서 Disk객체의 속성을 변경할 때 사용합니다.|
|disk_path|Disk의 Directory Path를 지정합니다. 이 Directory는 Create 되어 있어야 합니다. 상대 Path로 Path를 지정시 $MACHBASE_HOME/dbs 기준으로 PATH를 찾습니다. 예를 들어 PATH='disk1'일 경우 Disk Path를 $MACHBASE_HOME/dbs/disk1으로 인식합니다.|
|parallel_io|Disk의 IO Request를 Parallel하게 몇 개까지 허용할 지를 결정합니다. (DEF: 3, MIN: 1, MAX: 128)|

## DROP TABLESPACE

**drop_tablespace_stmt:**

![drop_tablespace_stmt](/images/sql/ddl/drop_tablespace_stmt.png)

```sql
drop_table_stmt ::= 'DROP TABLESPACE' tablespace_name
```

지정된 Tablespace를 삭제합니다. 하지만 Tablespace에 생성된 객체가 존재하는 경우, 삭제가 실패합니다.

```sql
--예제
DROP TABLESPACE TablespaceName;
```

## CREATE INDEX

**create_index_stmt:**

![create_index_stmt](/images/sql/ddl/create_index_stmt.png)

**index_type:**

![index_type](/images/sql/ddl/index_type.png)

**table_space:**

![table_space](/images/sql/ddl/table_space.png)

**index_property_list:**

![index_property_list](/images/sql/ddl/index_property_list.png)

```sql
create_index_stmt ::= 'CREATE' 'INDEX' index_name 'ON' table_name '(' column_name ')' index_type? table_space? index_property_list?
index_type ::= 'INDEX_TYPE' ( 'LSM' | 'KEYWORD' | 'BITMAP' | 'REDBLACK' )
table_space ::= 'TABLESPACE' table_space_name
index_property_list ::= ( 'MAX_LEVEL' | 'PAGE_SIZE' | 'BITMAP_ENCODE' | 'PART_VALUE_COUNT' ) '=' value
```

##### Index Type

생성할 Index Type을 지정합니다. Keyword Index가 아닌 경우 Index Type을 지정하지 않으면 Table Type에 따라서 Default Index Type으로 Index가 생성됩니다.

|Table Type|Default Index Type|
|--|--|
|Volatile Table|REDBLACK|
|Lookup Table|REDBLACK|
|Log Table|LSM|

##### KEYWORD Index

텍스트 검색을 위한 인덱스로써 로그 테이블의 varchar와 text 컬럼에만 생성 가능하며, 단일 컬럼에 대해서만 생성할 수 있습니다.

##### LSM Index

LSM(Log Structure Merge) Index로 Big Data에 저장 및 검색에 최적화된 Index입니다. LSM Index들의 Partition들은 Level 별로 유지되고 하위 Level의 Partition들이 Merge되어 상위 Level로 이동합니다. 그리고 상위 Level의 Partition 생성에 사용된 하위 Partition들은 삭제됩니다.

이러한 Index Level Partition Building은 Background Thread 에 의해서 수행됩니다. 상위 Level Partition은 하위 Level의 Partition 들이 Merge되어 하나의 Partition으로 생성되기 때문에 Index를 통한 검색 시 다음과 같은 장점이 존재합니다.

1. Key가 중복된 경우, 한 번만 저장되기 때문에 Key 저장을 위한 Disk Space가 절약됩니다.
2. 여러 개의 Partition에 대한 Searching보다 하나의 Index Partition에 대한 검색 시 File Open 및 Close 비용이 줄어들고, 접근하는 Index Page의 개수 또한 줄어듭니다.

##### LSM Index Property

|항목|설명|
|--|--|
|MAX_LEVEL<br>(DEFAULT = 3, MIN = 0, MAX = 3 )|LSM Index의 최대 Level로서 현재 3이 최대값입니다. 그리고 하나의 Partition의 최대 Record 건수는 2억건을 초과할 수 없습니다. 각 Level의 Partition 크기는 이전 Partition의 Value 개수 * 10입니다. 예를 들면 MAX_LEVEL = 3, PART_VALUE_COUNT가 100,000 이면 Level 0 = 100,000, Level 1 = 1,000,0000, Level 2 = 10,000,000, Level 3 = 100,000,000 입니다. 만약 마지막 Level의 Partition Size가 2억건을 초과하면 Index 생성이 실패합니다.|
|PAGE_SIZE<br>(DEFAULT = 512 * 1024, MIN = 32 * 1024,MAX = 1 * 1024 * 1024)|Index의 Key Value와 Bitmap 값이 저장되는 Page의 크기를 지정합니다. Default는 512K입니다.|
|BITMAP_ENCODE<br>(DEFAULT = EQUAL, RANGE)|인덱스의 Bitmap 타입을 설정합니다. BITMAP_ENCODE=EQUAL(기본값)의 경우 키값과 같은 값에 대한 bitmap을 생성하고 BITMAP=RANGE인 경우 키값의 range에 따른 bitmap을 생성합니다. 질의 조건으로 = 을 주로 사용하는 경우 BITMAP_ENCODE=EQUAL로, 특정 범위값을 질의 조건으로 주로 사용하는 경우 BITMAP_ENCODE=RANGE로 설정하는 편이 좋습니다. BITMAP=RANGE인 경우 생성 비용은 EQUAL에 비해서 약간 증가합니다.|

##### BITMAP 인덱스

데이터 분석을 위한 인덱스로서, 로그 테이블에만 생성 가능합니다. 그리고 varchar, text, binary를 제외한 모든 컬럼에 생성 가능하며, 단일 컬럼에 대해서만 생성할 수 있습니다.

##### RED-BLACK 인덱스

실시간 데이터 검색을 위한 메모리 인덱스로서, Volatile/Lookup 테이블에만 생성 가능합니다. 그리고 이 테이블의 모든 컬럼에 생성 가능하며 단일 컬럼에 대해서만 생성할 수 있습니다.

##### Index Property

LSM Index 에서 적용할 수 있는 Property 는 다음과 같습니다.

##### PART_VALUE_COUNT

Index의 Partition에 저장되는 Row 개수를 나타냅니다.

```sql
--예제
-- c1 컬럼에 index가 적용되었습니다.
CREATE INDEX index1 on table1 ( c1 );
-- LSM 인덱스를 명시적으로 적용합니다.
CREATE INDEX index_lsm on table1 ( c1 ) INDEX_TYPE LSM;
-- varchar type의 var_column에 keyword index가 적용되고 page_size의 단위는 100000가 되었습니다.
CREATE INDEX index2 on table1 (var_column) INDEX_TYPE KEYWORD PAGE_SIZE=100000;
```

##### JSON path 인덱스

JSON 컬럼의 특정 멤버에 인덱스를 만들 때는 기존 JSONPath arrow 문법과 JSON dot 축약 문법을 모두 사용할 수 있습니다.

```sql
CREATE TAG TABLE tag_log (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON
);

-- JSON dot 축약 문법
CREATE INDEX tag_log_sensor_idx ON tag_log (value.sensor.name);

-- 기존 JSONPath arrow 문법
CREATE INDEX tag_log_metric_idx ON tag_log (value->'$.metric');

-- 배열 index와 double quoted key
CREATE INDEX tag_log_item_idx ON tag_log (value.items[0]."product-id");
```

JSON 컬럼 이름이 double quote로 생성되었거나 keyword 컬럼 이름을 사용하는 경우에도 기존 arrow DDL을 사용할 수 있습니다.

```sql
CREATE TAG TABLE tag_log_q (
    name    VARCHAR(40) PRIMARY KEY,
    time    DATETIME BASETIME,
    "value" JSON
);

CREATE INDEX tag_log_q_idx ON tag_log_q ("value"->'$.sensor.name');

CREATE TAG TABLE tag_log_kw (
    name   VARCHAR(40) PRIMARY KEY,
    time   DATETIME BASETIME,
    "LEFT" JSON
);

CREATE INDEX tag_log_kw_idx ON tag_log_kw (left->'$.sensor.name');
```

문자열 비교 조건은 JSON path 인덱스를 사용할 수 있습니다. 숫자 또는 boolean 의미의 비교 조건은 문자열 정렬과 숫자 정렬이 다를 수 있으므로 JSON path 인덱스 range 조건으로 사용하지 않습니다.

TAGDATA 메타데이터의 JSON path 인덱스 사용법은 [Tag 메타데이터](/dbms/tag-table-usage/tag-metadata/#original-85-tag-metadata) 및 [Tag 테이블 인덱스](/dbms/tag-table-usage/index-performance/#original-85-tag-indexes) 문서를 참고하십시오.


## DROP INDEX

**drop_index_stmt:**

![drop_index_stmt](/images/sql/ddl/drop_index_stmt.png)

```sql
drop_index_stmt ::= 'DROP INDEX' index_name
```

지정된 인덱스를 삭제합니다. 단, 해당 테이블을 검색 중인 다른 세션이 존재할 경우에는 에러를 내면서 실패합니다.


```sql
-- 예제
DROP INDEX IndexName;
```


##  ALTER TABLE

ALTER TABLE 구문은 지정된 테이블의 스키마 정보를 변경시키기 위한 용도로 사용되며 Log Table 만 사용 가능합니다.

### ALTER TABLE SET

이 구문은 Table의 Property를 변경하는 구문입니다. 현재 동적으로 변경 가능한 Property는 없습니다.

### ALTER TABLE ADD COLUMN

**alter_table_add_stmt:**

![alter_table_add_stmt](/images/sql/ddl/alter_table_add_stmt.png)

```sql
alter_table_add_stmt ::= 'ALTER TABLE' table_name 'ADD COLUMN' '(' column_name column_type ( 'DEFAULT' value )? ')'
```

이 구문은 테이블에 특정 컬럼을 실시간으로 추가하는 기능입니다. 컬럼의 이름과 타입을 추가하고, DEFAULT 구문을 통해 기본 데이터 값을 설정할 수 있습니다.

```sql
-- 예제-1
alter table atest2 add column (id4 float);

-- 예제-2
alter table atest2 add column (id6 double  default 5);
alter table atest2 add column (id7 ipv4  default '192.168.0.1');
alter table atest2 add column (id8 varchar(4) default 'hello');
```

### ALTER TABLE DROP COLUMN

**alter_table_drop_stmt:**

![alter_table_drop_stmt](/images/sql/ddl/alter_table_drop_stmt.png)

```sql
alter_table_drop_stmt ::= 'ALTER TABLE' table_name 'DROP COLUMN' '(' column_name ')'
```

이 구문은 테이블에 특정 컬럼을 실시간으로 삭제하는 기능입니다.

```sql
-- 예제
alter table atest2 drop column (id4);
alter table atest2 drop column (id8);
```

### ALTER TABLE RENAME COLUMN

**alter_table_column_rename_stmt:**

![alter_table_column_rename_stmt](/images/sql/ddl/alter_table_column_rename_stmt.png)

```sql
alter_table_column_rename_stmt ::= 'ALTER TABLE' table_name 'RENAME COLUMN' old_column_name 'TO' new_column_name
```

이 구문은 테이블의 특정 컬럼명을 변경하는 기능입니다.

```sql
-- 예제
alter table atest2 rename column id7 to id7_rename;
```

### ALTER TABLE MODIFY COLUMN

**alter_table_modify_stmt:**

![alter_table_modify_stmt](/images/sql/ddl/alter_table_modify_stmt.png)

```sql
alter_table_modify_stmt ::= 'ALTER TABLE' table_name 'MODIFY COLUMN' ( '(' column_name 'VARCHAR' '(' new_size ')' ')' | column_name ( 'NOT'? 'NULL' | 'SET' 'MINMAX_CACHE_SIZE' '=' value ) )
```

이 구문은 테이블의 특정 컬럼의 속성을 변경하는 것입니다. 현재는 VARCHAR 타입의 컬럼 길이와 그외 타입에 대한 MINMAX CACHE 속성과 NOT NULL 제약조건을 수정하는 것이 가능합니다.

**VARCHAR SIZE**

이 구문은 VARCHAR 타입의 컬럼 길이만 변경하는 것을 지원합니다. 이 동작은 기존의 데이터를 보존하기 위해 그 길이가 줄어들 수는 없으며, 언제나 증가해야 합니다.

```sql
ALTER TABLE table_name MODIFY COLUMN (column_name VARCHAR(new_size));
```

```sql
-- 예제 : TABLE 이 이렇게 만들어졌다고 가정하자.
-- create table atest5 (id integer, name varchar(5), id3 double, id4 float);

-- 에러 발생: 다른 타입으로 변경할 수 없습니다.
alter table atest5 modify column (id varchar(10));

-- 에러 발생: VARCHAR 길이를 더 작게 할 수 없습니다.
alter table atest5 modify column (name varchar(3));

-- 에러 발생: VARCHAR의 최대 크기 32767 이상 넘을 수 없습니다.
alter table atest5 modify column (name varchar(32768));

-- 성공
alter table atest5 modify column (name varchar(128));
```

**MINMAX_CACHE_SIZE**

이 구문은 특정 컬럼에 대해 MINMAX_CACHE_SIZE를 변경합니다.

```sql
ALTER TABLE table_name MODIFY COLUMN column_name SET MINMAX_CACHE_SIZE=value;
```

```sql
-- 예제 : TABLE 이 이렇게 만들어졌다고 가정하자.
create table atest9 (id integer, name varchar(100));

-- 에러: VARCHAR에는 적용 안 됩니다.
alter table atest9 modify column name set minmax_cache_size=0;
[ERR-02139 : MINMAX CACHE is not allowed for VARCHAR column(NAME).]

-- 변경 성공
alter table atest9 modify column id set minmax_cache_size=10240;
```

**NOT NULL**

컬럼에 NOT NULL 제약 조건을 추가합니다. NOT NULL 제약 조건을 추가할 경우 NULL값이 있는 컬럼에 대해서는 DDL연산이 실패합니다.

만약 컬럼에 NULL값을 허용하고 싶은 경우에는 다음 절의 MODIFY COLUMN NULL 명령어를 이용합니다.

```sql
ALTER TABLE table_name MODIFY COLUMN column_name NOT NULL;
```

```sql
-- t1.c1에 NOT NULL 제약조건을 추가합니다.
alter table t1 modify column c1 not null;
```

**NULL**

NOT NULL 제약조건을 해제합니다. LSM 인덱스의 min_max 캐시로 인한 성능 향상을 얻을 수 없습니다.
NULL 값의 입력이 가능해집니다.

```sql
ALTER TABLE table_name MODIFY COLUMN column_name NULL;
```

```sql
-- t1.c1에 NOT NULL 제약조건을 해제합니다.
alter table t1 modify column c1 null;
```


### ALTER TABLE RENAME TO

**alter_table_rename_stmt:**

![alter_table_rename_stmt](/images/sql/ddl/alter_table_rename_stmt.png)

```sql
alter_table_rename_stmt ::= 'ALTER TABLE' table_name 'RENAME TO' new_name
```

테이블의 이름을 변경합니다.

메타 테이블들은 이름을 변경할 수 없고, 변경될 이름에 $문자는 사용할 수 없습니다. 테이블 이름 변경은 Log 테이블에 대해서만 가능합니다.

```sql
-- worker 테이블의 이름을 employee로 변경합니다.
ALTER TABLE worker RENAME TO employee;
```

### ALTER TABLE ADD RETENTION

**alter_table_add_retention_stmt:**

```sql
alter_table_add_retention_stmt ::=  'ALTER TABLE' table_name 'ADD RETENTION' policy_name
```

![alter_table_add_retention_stmt](/images/sql/ddl/alter_table_add_retention_stmt.png)

```sql
ALTER TABLE tag ADD RETENTION policy_1d_1h;
```


### ALTER TABLE DROP RETENTION

**alter_table_drop_retention_stmt:**

```sql
alter_table_drop_retention_stmt ::=  'ALTER TABLE' table_name 'DROP RETENTION'
```

![alter_table_drop_retention_stmt](/images/sql/ddl/alter_table_drop_retention_stmt.png)

```sql
ALTER TABLE tag DROP RETENTION;
```

## ALTER TABLESPACE

ALTER TABLESPACE 구문은 지정된 Tablespace에 관련된 정보를 변경하는데 사용됩니다.

### ALTER TABLESPACE MODIFY DATADISK

이 구문은 Tablespace의 DATADISK의 속성을 변경하는데 사용됩니다.

**alter_tablespace_stmt:**

![alter_tablespace_stmt](/images/sql/ddl/alter_tablespace_stmt.png)

```sql
alter_tablespace_stmt ::= 'ALTER TABLESPACE' table_name 'MODIFY DATADISK' disk_name 'SET' 'PARALLEL_IO' '=' value
```

```sql
-- 예제
ALTER TABLESPACE tbs1 MODIFY DATADISK disk1 SET PARALLEL_IO = 10;
```

## TRUNCATE TABLE

**truncate_table_stmt:**

![truncate_table_stmt](/images/sql/ddl/truncate_table_stmt.png)

```sql
truncate_table_stmt ::= 'TRUNCATE TABLE' table_name
```

```sql
-- ctest 테이블의 모든 데이터를 삭제합니다.
Mach> truncate table ctest;
Truncated successfully.
```

지정된 테이블에 존재하는 모든 데이터를 삭제합니다. 단, 해당 테이블을 검색 중인 다른 세션이 존재할 경우에는 에러를 내면서 실패합니다.

## CREATE ROLLUP

**create_rollup_stmt:**

![create_rollup_stmt](/images/sql/ddl/create_rollup_stmt.png)

```sql
create_rollup_stmt ::= 'CREATE ROLLUP' rollup_name 'ON' src_table_name '('src_table_column')' 'INTERVAL' number ('SEC' | 'MIN' | 'HOUR')
```

```sql
-- tag table의 value 칼럼을 대상으로 rollup을 생성합니다.
Mach> CREATE ROLLUP _rollup_tag_value_sec ON tag(value) INTERVAL 1 SEC;
Executed successfully
```

JSON 컬럼의 멤버 값을 rollup 기준 값으로 사용할 때는 기존 JSONPath arrow 문법과 JSON dot 축약 문법을 모두 사용할 수 있습니다.

```sql
CREATE TAG TABLE tag_json (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON
);

-- JSON dot 축약 문법
CREATE ROLLUP tag_json_metric_ru
ON tag_json (value.metric)
INTERVAL 1 SEC;

-- 기존 JSONPath arrow 문법
CREATE ROLLUP tag_json_metric_arrow_ru
ON tag_json (value->'$.metric')
INTERVAL 1 SEC;

-- 배열 index와 double quoted key
CREATE ROLLUP tag_json_item_ru
ON tag_json (value.items[0]."metric-id")
INTERVAL 1 SEC;
```

기존 arrow 문법의 quoted 컬럼 이름과 keyword 컬럼 이름도 계속 사용할 수 있습니다.

```sql
CREATE TAG TABLE tag_json_q (
    name    VARCHAR(40) PRIMARY KEY,
    time    DATETIME BASETIME,
    "value" JSON
);

CREATE ROLLUP tag_json_q_ru
ON tag_json_q ("value"->'$.metric')
INTERVAL 1 SEC;

CREATE TAG TABLE tag_json_kw (
    name   VARCHAR(40) PRIMARY KEY,
    time   DATETIME BASETIME,
    "LEFT" JSON
);

CREATE ROLLUP tag_json_kw_ru
ON tag_json_kw (left->'$.metric')
INTERVAL 1 SEC;
```

> Rollup 생성 후 원본 이상 데이터 보정에 따라 기존 집계 결과를 다시 만들어야 하는 경우에는 [Rollup Rebuild 사용자 가이드](/dbms/tag-rollup-usage/rollup-rebuild/#original-85-rollup-rebuild)를 참고하십시오.

```sql
create_conditional_rollup_stmt ::= 'CREATE ROLLUP' rollup_name
                                   ( 'ON' src_table_name '('src_table_column')'
                                   | 'FROM' src_rollup_table_name )
                                   'INTERVAL' number ('SEC' | 'MIN' | 'HOUR')
                                   'WHERE' predicate
```

```sql
-- 조건부 rollup: value2 = 0 인 데이터만 집계
Mach> CREATE ROLLUP _rollup_tag_value_min_ok
      ON tag(value)
      INTERVAL 1 MIN
      WHERE value2 = 0;
Executed successfully
```

```sql
create_custom_rollup_stmt ::= 'CREATE ROLLUP' rollup_name
                              'INTO' '(' dest_table_name ')'
                              'AS' '(' select_stmt ')'
                              'INTERVAL' number ('SEC' | 'MIN' | 'HOUR')
                              [ 'WAKEUP INTERVAL' number ('SEC' | 'MIN' | 'HOUR') ]
```

```sql
-- 사용자 정의 SELECT 집계를 대상 TAG 테이블로 저장하는 custom rollup 생성
Mach> CREATE ROLLUP rollup_stock_1m
      INTO (stock_rollup_1m)
      AS (
        SELECT code,
               DATE_TRUNC('minute', time) AS time,
               SUM(price)                 AS sum_price,
               COUNT(*)                   AS cnt
          FROM stock_tick
         GROUP BY code, time
      )
      INTERVAL 1 MIN;
Executed successfully
```

주의사항
- 조건부 rollup의 `WHERE`는 `ON/FROM` 문법에서 사용합니다.
- Custom Rollup의 `WHERE`는 `SELECT` 내부에서만 사용합니다.
- `INTERVAL ... WHERE ...` 형태의 외부 WHERE는 Custom 문법에서 지원하지 않습니다.
- 자세한 제약/운영 패턴은 [Custom Rollup: 사용자 정의 집계](/dbms/tag-rollup-usage/custom-rollup/#original-85-rollup-custom)를 참고합니다.


## DROP ROLLUP

**drop_rollup_stmt:**

![drop_rollup_stmt](/images/sql/ddl/drop_rollup_stmt.png)

```sql
drop_rollup_stmt ::= 'DROP ROLLUP' rollup_name
```

```sql
-- rollup을 삭제합니다.
Mach> DROP ROLLUP _rollup_tag_value_sec;
Executed successfully
```

## ALTER ROLLUP

롤업 워커를 제어하고 wakeup 주기를 조정합니다.

```sql
alter_rollup_start_stop_stmt ::= 'ALTER ROLLUP' rollup_name ( 'START' | 'STOP' )
alter_rollup_force_stmt      ::= 'ALTER ROLLUP' rollup_name 'FORCE'
alter_rollup_wakeup_stmt     ::= 'ALTER ROLLUP' rollup_name 'WAKEUP'
alter_rollup_wakeup_int_stmt ::= 'ALTER ROLLUP' rollup_name 'SET WAKEUP INTERVAL' number ( 'SEC' | 'MIN' | 'HOUR' )
```

예시
```sql
-- 롤업 스레드 시작/중지
ALTER ROLLUP _rollup_tag_value_sec START;
ALTER ROLLUP _rollup_tag_value_sec STOP;

-- 지금 바로 깨우고 즉시 반환
ALTER ROLLUP _rollup_tag_value_sec WAKEUP;

-- 즉시 집계 실행 후 완료까지 대기
ALTER ROLLUP _rollup_tag_value_sec FORCE;

-- wakeup 주기 단축(롤업 주기의 약수만 허용)
ALTER ROLLUP _rollup_tag_value_sec SET WAKEUP INTERVAL 1 SEC;
```

규칙
- wakeup 주기는 0보다 커야 하고 롤업 주기보다 클 수 없으며, 롤업 주기의 정수배여야 합니다. 위반 시 에러를 반환합니다.
- `WAKEUP`은 스레드를 깨우기만 하고 바로 반환합니다. 즉시 실행과 완료 대기가 필요할 때는 `FORCE`를 사용합니다.

## CREATE RETENTION

**create_retention_stmt:**

![create_retention_stmt](/images/sql/ddl/create_retention_stmt.png)

```sql
create_retention_stmt ::= 'CREATE RETENTION' policy_name 'DURATION' duration ( 'MONTH' | 'DAY' ) 'INTERVAL' interval ( 'DAY' | 'HOUR' )
```

```sql
-- retention policy를 생성합니다.
Mach> CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;
Executed successfully
```

## DROP RETENTION

**drop_retention_stmt:**

![drop_retention_stmt](/images/sql/ddl/drop_retention_stmt.png)

```sql
drop_retention_stmt ::= 'DROP RETENTION' policy_name
```

```sql
-- retention policy를 삭제합니다.
Mach> DROP RETENTION policy_1d_1h;
Executed successfully
```

## dml


## INSERT

**insert_stmt:**

![insert_stmt](/images/sql/dml/insert_stmt.png)

**insert_column_list:**

![insert_column_list](/images/sql/dml/insert_column_list.png)

**value_list:**

![value_list](/images/sql/dml/value_list.png)

**set_list:**

![set_list](/images/sql/dml/set_list.png)

```sql
insert_stmt ::= 'INSERT INTO' table_name ( '(' insert_column_list ')' )? 'METADATA'? 'VALUES' '(' value_list ')' ( 'ON DUPLICATE KEY UPDATE' ( 'SET' set_list )? )?
insert_column_list ::= column_name ( ',' column_name )*
value_list ::= value ( ',' value )*
set_list ::= column_name '=' value ( ',' column_name '=' value )*
```

```sql
create table test (number int,name varchar(20));
Created successfully.
insert into test values (1,"test");
1 row(s) inserted.
insert into test(name,number) values ("test",2);
1 row(s) inserted.
```

특정 테이블에 값을 입력하는 구문입니다. 한 가지 특이한 점은 Column_List에서 지정되지 않은 컬럼에는 모두 NULL 값으로 채워진다는 것입니다. 이는 입력의 편의성과 저장 공간의 효율화를 위해 채택된 로그 파일의 특성을 고려한 정책입니다.

METADATA는 tag table에만 사용할 수 있습니다.

### INSERT ON DUPLICATE KEY UPDATE

마크베이스는 흔히 알려진 UPSERT 기능과 유사한 구문을 지원합니다.

기본 키가 지정된 Lookup/Volatile 테이블에 값을 입력할 때 사용할 수 있는 특수 구문으로, 기본 키 값이 중복되는 데이터가 이미 테이블에 존재하는 경우에는 기존 데이터의 값이 변경됩니다.
물론 키 값이 중복되는 데이터가 존재하지 않는 경우에는 새로운 데이터로 삽입됩니다.

이 구문을 사용하기 위해서 휘발성 테이블에 기본 키가 지정되어 있어야 합니다.

삽입되는 데이터의 컬럼 값과 갱신되는 데이터의 컬럼 값을 다르게 하고자 하는 경우, 또는 삽입되는 데이터의 컬럼 값이 아닌 다른 컬럼 값을 갱신하고자 하는 경우에는 SET 절을 추가로 입력할 수 있습니다.

* SET 절은 '컬럼=값'으로 구성되며, 각각을 콤마로 구분해야 합니다.
* SET 절에서 기본 키 값을 변경해서는 안 됩니다.

## INSERT SELECT

**insert_select_stmt:**

![insert_select_stmt](/images/sql/dml/insert_select_stmt.png)

```sql
insert_select_stmt ::= 'INSERT INTO' table_name ( '(' insert_column_list ')' )? select_stmt
```

특정 table에 대해서 SELECT 문의 수행 결과를 삽입하는 문장입니다. 기본적으로는 다른 DBMS와 유사하지만 다음의 차이점이 있습니다.

1. _ARRIVAL_TIME 컬럼 값은 select 및 INSERT 컬럼 리스트에서 지정되지 않으면 INSERT SELECT 문이 수행되는 시점의 시간 값으로 입력됩니다.
2. VARCHAR 타입의 컬럼에 대해서 삽입되는 입력값이 컬럼의 최대 길이보다 큰 경우, 오류를 발생시키지 않고 해당 컬럼의 최대 길이만큼 잘라서 입력됩니다.
3. 형 변환이 가능한 경우(숫자형->숫자형)에는 입력되는 컬럼 값에 맞게 삽입됩니다.
4. 수행 도중 오류가 발생한 경우 ROLLBACK되지 않습니다.
5. _ARRIVAL_TIME 컬럼의 값을 지정하여 삽입하는 경우, 새로 입력되는 값이 기존의 값보다 이전 시간을 갖고 있으면 입력되지 않습니다.

```sql
create table t1 (i1 integer, i2 varchar(60), i3 varchar(5));
Created successfully.

insert into t1 values (1, 'a', 'ddd' );
1 row(s) inserted.
insert into t1 values (2, 'kkkkkkkkkkkkkkkkkkkkk', 'c');
1 row(s) inserted.

insert into t1 select * from t1;
2 row(s) inserted.
create table t2 (i1 integer, i2 varchar(60), i3 varchar(5));

insert into t2 (_arrival_time, i1, i2, i3) select _arrival_time, * from t1;
4 row(s) inserted.
```

## UPDATE

* 5.5 부터 제공되는 기능입니다.

**update_stmt:**

![update_stmt](/images/sql/dml/update_stmt.png)

**update_expr_list:**

![update_expr_list](/images/sql/dml/update_expr_list.png)

**update_expr:**

![update_expr](/images/sql/dml/update_expr.png)

```sql
update_stmt ::= 'UPDATE' table_name ( 'METADATA' )? 'SET' update_expr_list 'WHERE' primary_key_column '=' value
update_expr_list ::= update_expr ( ',' update_expr)*
update_expr ::= column '=' value
```

INSERT ON DUPLICATE KEY UPDATE를 통한 UPSERT가 아닌 UPDATE 구문도 제공합니다.

역시 기본 키(Primary Key)가 지정된 Lookup/Volatile 테이블에 값을 입력할 때 사용할 수 있습니다. WHERE 절에는 기본 키의 일치 조건식을 작성해야 합니다.

### UPDATE METADATA

TAGDATA 테이블에 한해서 메타데이터를 업데이트하고자 할 때 사용합니다.

```sql
UPDATE TAG METADATA SET ...
```

* TAGDATA 테이블의 메타데이터는 INSERT ON DUPLICATE KEY UPDATE를 통해 입력하거나 수정할 수 없습니다.
* 현재 `TAG METADATA` 는 `WHERE NAME = ...` 뿐 아니라 메타데이터 컬럼 조건도 사용할 수 있습니다.
* `TIME`, `VALUE` 같은 데이터 컬럼은 `UPDATE ... METADATA` 에서 수정할 수 없습니다.
* `NAME` 과 메타데이터 컬럼만 수정할 수 있습니다.

```sql
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE status = 'READY';
```

## DELETE

**delete_stmt:**

![delete_stmt](/images/sql/dml/delete_stmt.png)

**time_unit:**

![time_unit](/images/sql/dml/time_unit.png)

```sql
delete_stmt ::= 'DELETE FROM' table_name ( 'OLDEST' number 'ROWS' | 'EXCEPT' number ( 'ROWS' | time_unit ) | 'BEFORE' datetime_expression )? 'NO WAIT'?
time_unit ::= 'DURATION' number time_unit ( ( 'BEFORE' | 'AFTER' ) number time_unit )?
```

마크베이스에서의 DELETE BEFORE 구문은 로그 테이블, Tag 테이블, Rollup table에 대해서 수행 가능합니다. 중간의 임의 위치에 있는 데이터를 삭제할 수 없으며, 임의의 위치부터 연속적으로 마지막(가장 오래된 로그) 레코드까지 지울 수 있도록 구현되었습니다.

이는 로그 데이터의 특성을 살린 정책으로서 한 번 입력되면 수정이 없고, 공간 확보를 위해 파일을 삭제하는 행위를 DB 형식으로 표현한 것입니다.

DURATION, OLDEST, EXCEPT 구문은 TAG 및 Rollup 테이블에 대해서는 사용할 수 없습니다.

```sql
-- 모두 삭제합니다.
DELETE FROM devices;

-- 가장 오래된 마지막 N건을 삭제합니다.
DELETE FROM devices OLDEST N ROWS;

-- 최근 N건을 제외하고 모두 삭제합니다.
DELETE FROM devices EXCEPT N ROWS;

-- 지금부터 N일치를 남기고 모두 삭제합니다.
DELETE FROM devices EXCEPT N DAY;

-- 2014년 6월 1일 이전의 데이터를 모두 삭제합니다.
DELETE FROM devices BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');

-- tag 데이터의 시간을 기준으로 삭제합니다.
DELETE FROM tag BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');

-- tag rollup 데이터를 시간 기준으로 삭제합니다.
DELETE FROM tag ROLLUP BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');
```

## DELETE WHERE

**delete_where_stmt:**

![delete_where_stmt](/images/sql/dml/delete_where_stmt.png)

```sql
delete_where_stmt ::= 'DELETE FROM' table_name 'WHERE' column_name '=' value
```

```sql
create volatile table t1 (i1 int primary key, i2 int);
Created successfully.
insert into t1 values (2,2);
1 row(s) inserted.
delete from t1 where i1 = 2;
1 row(s) deleted.
```

휘발성 테이블과 lookup 테이블에서 WHERE 절에 작성된 조건에 일치하는 레코드를 삭제할 수 있습니다.

* 기본 키가 지정된 휘발성 또는 lookup 테이블에 대해서만 수행 가능합니다.
* WHERE 절에는 (기본 키 컬럼) = (값) 조건만 허용되며, 다른 조건과 함께 작성할 수 없습니다.
* 기본 키 컬럼이 아닌 다른 컬럼을 조건에 사용할 수 없습니다.

### DELETE FROM TAG METADATA

TAGDATA 테이블의 메타데이터는 `DELETE FROM TAG METADATA` 로 삭제할 수 있습니다.
`WHERE` 절을 생략하면 해당 TAGDATA 테이블의 모든 메타데이터 행을 삭제합니다.

```sql
DELETE FROM tag METADATA;
DELETE FROM tag METADATA WHERE name = 'tag-1';
DELETE FROM tag METADATA WHERE status = 'STOP';
```

주의사항:

- `WHERE NAME = ...` 뿐 아니라 메타데이터 컬럼 조건을 사용할 수 있습니다.
- 삭제 대상 중 하나라도 실제 데이터 row를 가지고 있으면 문장 전체가 실패합니다.
- 사용 중인 tag의 메타데이터는 삭제할 수 없습니다.
- 전체 삭제 시에도 사용 중인 tag가 하나라도 있으면 일부만 삭제하지 않고 문장 전체가 실패합니다.
- tag name 컬럼명을 `name` 이 아닌 다른 이름으로 정의한 TAGDATA 테이블에서도 같은
  문법을 사용할 수 있습니다.

**delete_from_tag_where_stmt:**

![delete_from_tag_where_stmt](/images/sql/dml/delete_from_tag_where_stmt.png)

```sql
delete_from_tag_where_stmt ::= 'DELETE FROM' table_name 'ROLLUP'? 'WHERE' predicate
```

Tag 테이블 및 Rollup 테이블은 tag name, tag name과 시간 조건, 또는 시간 조건만으로 제한된 DELETE 조건식을 지원합니다.

시간 조건에는 `=`, `<`, `<=`, `BETWEEN`을 사용할 수 있습니다.

```sql
-- tag name 기준으로 삭제하는 예시입니다.
DELETE FROM tag WHERE tag_name = 'my_tag_2021';

-- tag name과 tag time 기준으로 삭제하는 예시입니다.
DELETE FROM tag WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');
DELETE FROM tag WHERE tag_name = 'my_tag_2021' AND tag_time BETWEEN TO_DATE('2021-07-01', 'YYYY-MM-DD') AND TO_DATE('2021-07-02', 'YYYY-MM-DD');

-- 시간 조건만으로 삭제하는 예시입니다.
DELETE FROM tag WHERE tag_time <= TO_DATE('2021-07-01', 'YYYY-MM-DD');

-- tag name 기준으로 rollup을 삭제하는 예시입니다.
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021';

-- tag name과 tag time 기준으로 rollup을 삭제하는 예시입니다.
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');

-- 시간 조건만으로 rollup을 삭제하는 예시입니다.
DELETE FROM tag ROLLUP WHERE tag_time BETWEEN TO_DATE('2021-07-01', 'YYYY-MM-DD') AND TO_DATE('2021-07-02', 'YYYY-MM-DD');
```

* 삭제 쿼리가 실행된 후에 삭제된 row가 저장 공간에서 물리적으로 삭제되기까지 걸리는 시간은 DBMS의 동작 상황에 따라서 다를 수 있습니다.

## LOAD DATA INFILE

**load_data_infile_stmt:**

![load_data_infile_stmt](/images/sql/dml/load_data_infile_stmt.png)

```sql
load_data_infile_stmt: 'LOAD DATA INFILE' file_name 'INTO TABLE' table_name ( 'TABLESPACE' tbs_name )? ( 'AUTO' ( 'BULKLOAD' | 'HEADUSE' | 'HEADUSE_ESCAPE' ) )? ( ( 'FIELDS' | 'COLUMNS' ) ( 'TERMINATED BY' char )? ( 'ENCLOSED BY' char )? )? ( 'TRIM' ( 'ON' | 'OFF' ) )? ( 'IGNORE' number ( 'LINES' | 'ROWS' ) )? ( 'MAX_LINE_LENGTH' number )? ( 'ENCODED BY' coding_name )? ( 'ON ERROR' ( 'STOP' | 'IGNORE' ) )?
```

CSV 포맷의 데이터 파일을 서버에서 직접 읽어서, 옵션에 따라 서버에서 직접 테이블 및 컬럼들을 생성하여 이를 입력하는 기능입니다.

각 옵션에 대해서 설명하면 다음과 같습니다.

|옵션|설명|
|--|--|
|AUTO mode_string<br><br>mode_string =<br><br>(BULKLOAD \| HEADUSE \| HEADUSE_ESCAPE)|해당 테이블을 생성하고 컬럼 타입(자동 생성 시 VARCHAR 타입) 및 컬럼명을 자동으로 생성합니다.<br>__BULKLOAD__: 데이터 한 개의 row를 하나의 컬럼으로 입력합니다. 컬럼으로 구분할 수 없는 데이터에 대해서 사용합니다.<br>__HEADUSE__: 데이터 파일의 첫 번째 라인에 기술되어 있는 컬럼명을 테이블의 컬럼명으로 사용하고, 그 라인에 기술된 수만큼의 컬럼을 생성합니다.<br>__HEADUSE_ESCAPE__: HEADUSE 옵션과 유사하지만, 컬럼명이 DB의 예약어와 같을 경우 발생할 수 있는 오류를 회피하기 위해 컬럼명의 앞뒤로 '_' 문자를 덧붙이고, 컬럼명에 특수문자가 존재하면 그 문자를 '_' 문자로 변경합니다.|
|(FIELDS\|COLUMNS) TERMINATED BY 'term_char'<br><br>ENCLOSED BY 'enclose_char'|데이터 라인을 파싱하기 위한 구분 문자(`term_char`)와 enclosing 문자(`enclose_char`)를 지정합니다. 일반적인 CSV 파일의 경우 구분 문자는 `,`이며 enclosing 문자는 `"`입니다.|
|ENCODED BY coding_name<br>coding_name =<br>{ UTF8(default) \| MS949 \| KSC5601 \| EUCJP \| SHIFTJIS \| BIG5 \| GB231280 }|데이터 파일의 인코딩 옵션을 지정합니다. 기본값은 UTF-8입니다.|
|TRIM (ON \| OFF)|컬럼의 빈 공간을 제거하거나 유지합니다. 기본값은 ON입니다.|
|IGNORE number (LINES \| ROWS)|숫자로 지정된 라인 또는 행만큼의 데이터를 무시합니다. CSV 포맷 파일의 헤더 등을 무시하거나 VCF 헤더를 무시하기 위해 사용합니다.|
|MAX_LINE_LENGTH|한 라인의 최대 길이를 지정합니다. 기본값은 512K이며, 데이터가 더 큰 경우에는 더 큰 값을 지정할 수 있습니다.|
|ON ERROR (STOP \| IGNORE)|입력 도중 에러가 발생할 경우 수행할 동작을 지정합니다. STOP인 경우 입력을 중단하고 IGNORE인 경우 에러가 발생한 라인을 건너뛰고 계속 입력합니다.<br>기본값은 IGNORE입니다.|

```sql
-- default field delimiter(,)와 field encloser(\")를 사용하여 데이터를 입력합니다.
LOAD DATA INFILE '/tmp/aaa.csv' INTO TABLE Sample_data ;

-- 하나의 컬럼을 갖는 NEWTABLE을 생성해서 한 라인을 한 컬럼으로 입력합니다.
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE NEWTABLE AUTO BULKLOAD;

-- CSV의 첫 번째 라인을 컬럼 정보로 이용하여 NEWTABLE을 생성하고 해당 테이블에 입력합니다.
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE NEWTABLE AUTO HEADUSE;

-- 첫 번째 라인은 무시하고 필드 구분자는 ;, enclosing 문자는 '로 지정해서 입력합니다.
LOAD DATA INFILE '/tmp/ccc.csv' INTO TABLE Sample_data FIELDS TERMINATED BY ';' ENCLOSED BY '\'' IGNORE 1 LINES ON ERROR IGNORE;
```

* AUTO 옵션을 사용하지 않는 경우 테이블의 모든 컬럼은 VARCHAR 또는 TEXT 타입으로 생성해야 합니다.

## select


## 목차

* [SELECT 구문](#select-구문)
* [FROM 절 없는 SELECT](#from-절-없는-select)
* [집합 연산자](#집합-연산자)
* [대상 목록](#대상-목록)
    * [CASE 문](#case-문)
* [FROM 절](#from-절)
    * [서브쿼리(인라인 뷰)](#서브쿼리인라인-뷰)
    * [저장 VIEW](#저장-view)
    * [조인(INNER JOIN)](#조인inner-join)
    * [INNER JOIN과 OUTER JOIN](#inner-join과-outer-join)
    * [PIVOT](#pivot)
* [WHERE 절](#where-절)
    * [서브쿼리 사용](#서브쿼리-사용)
    * [SEARCH 문](#search-문)
    * [ESEARCH 문](#esearch-문)
    * [NOT SEARCH 문](#not-search-문)
    * [REGEXP 문](#regexp-문)
    * [IN 문](#in-문)
    * [IN 문과 서브쿼리 사용](#in-문과-서브쿼리-사용)
    * [BETWEEN 문](#between-문)
    * [RANGE 문](#range-문)
* [GROUP BY / HAVING](#group-by--having)
* [ORDER BY](#order-by)
* [SERIES BY](#series-by)
* [LIMIT](#limit)
* [DURATION](#duration)
* [데이터 저장](#데이터-저장)


SELECT는 Machbase의 다양한 테이블에서 데이터를 조회, 필터링, 조작하는 데 사용되는 구문입니다.

## SELECT 구문

```sql
select_stmt UNION ALL select_stmt
```

```sql
SELECT target_list [FROM table_list]
[WHERE condition_expr]
[GROUP BY expr] [HAVING expr]
[ORDER BY expr [DESC]] [SERIES BY expr]
[LIMIT n[,n]]
[DURATION duration_expr];
```

일반적인 `SELECT` 문은 `FROM` 절을 사용합니다. 다만 단순 표현식은 `FROM` 절 없이도
실행할 수 있습니다.

## FROM 절 없는 SELECT

`FROM` 절 없이 실행하는 `SELECT`는 테이블을 조회하지 않고 상수, 문자열, 산술식,
단순 함수 결과를 1행으로 반환합니다. 서버 연결 확인이나 간단한 계산 결과를 즉시
확인할 때 사용할 수 있습니다.

```sql
select 1;
select 'alive';
select 1 + 2;
select abs(-7);
```

각 질의는 1건의 결과를 반환합니다.

다음과 같은 확장 구문은 지원하지 않습니다.

```sql
select distinct 1;
select 1 where 1 = 1;
select 1 order by 1;
select count(*);
select *;
```

지원하지 않는 구문은 보통 다음 오류를 반환합니다.

```text
ERR-02362: This statement is not supported.
```

`select *;`는 다음 오류를 반환할 수 있습니다.

```text
ERR-02039: No table specified in the target list.
```

`FROM` 절 없는 `SELECT`는 단순 표현식 1행 조회 용도입니다. 집계, 정렬, 조건절,
주기 옵션, 힌트와 같은 확장 구문은 사용할 수 없습니다.

## 집합 연산자

여러 SELECT 쿼리의 결과를 단일 쿼리 결과로 받고자 할 때 사용합니다. Machbase는
`UNION ALL` 집합 연산자만 지원합니다. 집합 연산자는 좌측과 우측의 SELECT 문이
(1) 같거나 호환 가능한 타입이고, (2) 쿼리 결과의 개수가 동일한 경우에만 실행할 수
있으며, 두 조건 중 하나라도 일치하지 않으면 에러로 처리됩니다.

데이터 타입 변환 및 호환성 확인은 다음 기준에 따라 수행됩니다.
* 부호 있는 정수 타입과 부호 없는 정수 타입은 호환되지 않습니다.
* 정수 타입은 실수 타입과 호환되며, 쿼리 결과는 실수 타입으로 변환되어 반환됩니다.
* 문자 타입은 다른 길이와 호환됩니다.
* IPv6 타입과 IPv4 타입은 호환되지 않습니다.
* 두 SELECT 문 중 좌측 쿼리의 컬럼명이 항상 사용됩니다.

사용 예

```sql
SELECT i1, i2 FROM table_1
UNION ALL
SELECT c1, c2 FROM table_2
```


## 대상 목록

SELECT 문의 대상이 되는 **컬럼 또는 서브쿼리의 목록**입니다.

대상 목록에 사용되는 서브쿼리는 WHERE 절에 사용되는 서브쿼리와 마찬가지로 두 개 이상의 값이나 두 개 이상의 결과 컬럼을 가지면 에러로 처리됩니다.

```sql
SELECT i1, i2 ...
SELECT i1 (Select avg(c1) FROM t1), i2 ...
```

## CASE 문

```sql
CASE <simple_case_expression|searched_case_expression> [else_clause] END

simple_case_expression ::=
    expr WHEN comparison_expr THEN return_expr
        [WHEN comparison_expr THEN return_expr ...]

searched_case_expression ::=
    WHEN condtion_expr THEN return EXPR [WHEN condtion_expr THEN return EXPR ...]

else_clause ::=
    ELSE else_value_expr
```

일반적인 프로그래밍 언어의 IF ... THEN ... ELSE 블록을 지원하는 표현식입니다. simple_case_expression은 하나의 컬럼 또는 표현식이 when 뒤에 나오는 comparison_expr의 값과 같을 때 return_expr의 형태로 실행되며, 이 when ... then 절은 원하는 만큼 반복할 수 있습니다.

searched_case_expression은 CASE 뒤에 표현식을 지정하지 않고 when 절에 비교 연산자를 포함하는 조건절을 기술합니다. 각 비교 연산의 결과가 true이면 then 절의 값이 반환됩니다. else 절은 when 절의 값이 만족되지 않을 때 (표현식이 NULL인 경우에도) else_value를 반환합니다.

```sql
select * from t1;
I1          I2
---------------------------
2           2
1           1
[2] row(s) selected.

select case i1 when 1 then 100 end from t1;
case i1 when 1 then 100 end
------------------------------
NULL
100
[2] row(s) selected.
```

simple_case_expression 예제에서 i1 컬럼의 값이 2이면 NULL이 반환됩니다.

```
select case when i1 > 0 then 100 when i1 > 1 then 200 end from t1;
case when i1 > 0 then 100 when i1 > 1 then 200 end
------------------------------------------
100
100
[2] row(s) selected.
```

searched_case_expression은 조건을 만족하는 첫 번째 조건을 반환하므로 100이 반환되며, 두 번째 조건은 실행되지 않습니다.


## FROM 절

FROM 절에는 테이블명 또는 인라인 뷰를 지정할 수 있습니다. 테이블 간의 조인을 수행하려면 테이블 또는 인라인 뷰를 쉼표(,)로 구분하여 나열합니다.

```sql
FROM table_name
```

table_name으로 지정된 테이블의 데이터를 조회합니다.

### 서브쿼리(인라인 뷰)

```sql
FROM (Select statement)
```

괄호로 묶인 서브쿼리의 내용에 대한 데이터를 조회합니다.

* Machbase 서버는 상관 서브쿼리를 지원하지 않으므로, 서브쿼리에서 외부 쿼리의 컬럼을 참조할 수 없습니다.

### 저장 VIEW

`FROM` 절에는 `CREATE VIEW`로 미리 정의한 저장 VIEW 이름도 사용할 수 있습니다.
저장 VIEW는 인라인 뷰와 달리 이름 있는 논리 객체이며, `DESC`, `SHOW VIEWS`,
`M$SYS_VIEWS`로 메타 정보를 확인할 수 있습니다.

```sql
SELECT *
FROM v_customer
WHERE id = 100;
```

저장 VIEW의 생성, 삭제, 메타 조회, 성능/제약, Tag / `BINARY` 예제는 [VIEW](/dbms/reference/sql/#view)
문서를 참조하세요.

### 조인(INNER JOIN)

```sql
JOIN(INNER JOIN)
```

두 테이블 table_1과 table_2를 조인합니다. 세 개 이상의 테이블이 나열된 경우 INNER JOIN을 사용할 수 있으며, 검색 조건과 조건절은 모두 WHERE 절에 기술합니다.

```sql
SELECT t1.i1, t2.i1 FROM t1, t2 WHERE t1.i1 = t2.i1 AND t1.i1 > 1 AND t2.i2 = 3;
```

### INNER JOIN과 OUTER JOIN

ANSI 스타일 INNER JOIN, LEFT OUTER JOIN, RIGHT OUTER JOIN을 지원합니다. FULL OUTER JOIN은 지원하지 않습니다.

```sql
FROM TABLE_1 [INNER|LEFT OUTER|RIGHT OUTER] JOIN TABLE_2 ON expression
```

ANSI 스타일 JOIN 절의 ON 절은 JOIN에 의해 수행되는 조건절을 사용합니다. OUTER JOIN 쿼리의 WHERE 절에 내부 테이블(ON 절의 조건이 만족되지 않으면 NULL로 채워지는 테이블)에 대한 절이 있으면 쿼리가 INNER JOIN으로 변환됩니다.

```sql
SELECT t1.i1, t2.i1 FROM t1 LEFT OUTER JOIN t2 ON (t1.i1 = t2.i1) WHERE t2.i2 = 1;
```

위 쿼리는 WHERE 절의 t2.i2 = 1 조건에 의해 INNER JOIN으로 변환됩니다.

### PIVOT

* PIVOT 구문은 Machbase 버전 5.6부터 지원됩니다.

**pivot_clause:**

![pivot_clause](/images/sql/select/pivot_clause.png)


PIVOT 문은 GROUP BY 출력의 집계 결과를 ROW로 표시하고 컬럼으로 재배열합니다.

인라인 뷰와 함께 사용되며 다음과 같이 수행됩니다.
* 인라인 뷰의 PIVOT 절에 사용되지 않은 컬럼에 대해 GROUP BY를 수행한 다음, PIVOT IN 절에 나열된 값에 대해 집계 함수를 수행합니다.
* 결과 그룹 컬럼과 집계 결과가 회전되어 컬럼으로 표시됩니다.

예를 들어, 다양한 센서에서 수집된 데이터에서 각 장치의 값을 집계합니다.
CASE 문을 통해 수행해야 하는 쿼리를 PIVOT 문을 통해 간단하게 표현할 수 있습니다.

```sql
-- w/o PIVOT
SELECT * FROM (
    SELECT
             regtime,
             SUM(CASE WHEN tagid = 'FRONT_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS front_axis_torque,
             SUM(CASE WHEN tagid = 'REAR_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS rear_axis_torque,
             SUM(CASE WHEN tagid = 'HOIST_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS hoist_axis_torque,
             SUM(CASE WHEN tagid = 'SLIDE_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS slide_axis_torque
    FROM     result_d
    WHERE    regtime BETWEEN TO_DATE('2018-12-07 00:00:00') AND TO_DATE('2018-12-08 05:00:00')
    GROUP BY regtime
) WHERE front_axis_torque >= 40 AND rear_axis_torque >= 20;

-- w/ PIVOT
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
    WHERE  regtime BETWEEN TO_DATE('2018-12-07 00:00:00') AND TO_DATE('2018-12-08 05:00:00')
) PIVOT (SUM(dvalue) FOR tagid IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE'))
WHERE front_axis_torque >= 40 AND rear_axis_torque >= 20;

-- Result
regtime                         'FRONT_AXIS_TORQUE'         'REAR_AXIS_TORQUE'          'HOIST_AXIS_TORQUE'         'SLIDE_AXIS_TORQUE'
------------------------------------------------------------------------------------------------------------------------------------------------------
2018-12-07 16:42:29 840:000:000 12158                       7244                        NULL                        NULL
2018-12-07 14:56:26 220:000:000 3308                        663                         NULL                        NULL
2018-12-07 12:20:13 844:000:000 3804                        113                         NULL                        NULL
2018-12-07 11:10:01 957:000:000 8729                        5384                        NULL                        NULL
2018-12-07 17:46:57 812:000:000 7500                        4559                        NULL                        NULL
2018-12-07 14:30:06 138:000:000 5080                        6817                        NULL                        -429
2018-12-07 13:09:20 464:000:000 5233                        1869                        -7253                       NULL
2018-12-07 15:43:03 539:000:000 7491                        4453                        NULL                        NULL
...
```


## WHERE 절

### 서브쿼리 사용

조건문에 서브쿼리를 사용할 수 있습니다. IN 절을 제외한 절에서 서브쿼리가 둘 이상의 레코드를 반환하거나, 서브쿼리에 둘 이상의 결과 컬럼이 있으면 지원되지 않습니다.

```sql
WHERE i1 = (SELECT MAX(c2) FROM T1)
```

조건 연산자의 우측에 괄호로 둘러싸서 서브쿼리를 사용합니다.

* Machbase 서버는 상관 서브쿼리를 지원하지 않으므로, 서브쿼리에서 외부 쿼리의 컬럼을 참조할 수 없습니다.

### SEARCH 문

일반 데이터베이스와 동일한 구문입니다. 단, 키워드 인덱스가 등록되어 있어야 하며, 텍스트 검색을 위한 연산자 키워드로 "SEARCH"를 추가하여 추가 검색 작업이 가능합니다.

```sql
-- drop table realdual;
create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));

create keyword index idx1 on realdual (id2);
create keyword index idx2 on realdual (id3);

insert into realdual values(1, 'time time2', 'series series2');

select * from realdual;

select * from realdual where id2 search 'time';
select * from realdual where id3 search 'series' ;
select * from realdual where id2 search 'time' and id3 search 'series';
```

결과는 다음과 같습니다.

```sql
Mach> create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));
Created successfully.

Mach> create keyword index idx1 on realdual (id2);
Created successfully.

Mach> create keyword index idx2 on realdual (id3);
Created successfully.

Mach> insert into realdual values(1, 'time time2', 'series series2');
1 row(s) inserted.

Mach> select * from realdual;
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.

Mach> select * from realdual where id2 search 'time';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.

Mach> select * from realdual where id3 search 'series';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.

Mach> select * from realdual where id2 search 'time' and id3 search 'series';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.
```

### ESEARCH 문

ESEARCH 문은 ASCII 텍스트에 대한 확장 검색을 가능하게 하는 검색 키워드입니다. 이 확장을 위해 % 문자를 사용하여 원하는 패턴을 검색합니다. Like 연산에서 % 앞에 모든 레코드를 확인하면 ESEARCH의 장점은 이러한 경우에도 단어를 빠르게 찾을 수 있다는 것입니다. 이 기능은 영어 문자열(에러 문자열이나 코드)의 일부를 찾을 때 매우 유용할 수 있습니다.

```sql
-- Example

select id2 from realdual where id2 esearch 'bbb%';
id2
--------------------------------------------
bbb ccc1
aaa bbb1

[2] row(s) selected.

-- 검색 패턴 'bbb%'는 검색 결과에 bbb1도 포함합니다.


select id3 from realdual where id3 esearch '%cd%';
id3
--------------------------------------------
cdf def1
bcd/cdf1ad
abc, bcd1
[3] row(s) selected.

-- % 문자는 검색 패턴의 시작과 끝뿐만 아니라 중간에서도 작동합니다.

select id3 from realdual where id3 esearch '%cd%';
id3
--------------------------------------------
cdf def1
bcd/cdf1ad
abc, bcd1
[3] row(s) selected.
```

### NOT SEARCH 문

NOT SEARCH는 SEARCH 문에서 찾은 레코드 이외의 레코드에 대해 true를 반환하는 문입니다.

NOT ESEARCH는 사용할 수 없습니다.

```sql
create table t1 (id integer, i2 varchar(10));
create keyword index t1_i2 on t1(i2);
insert into t1 values (1, 'aaaa');
insert into t1 values (2, 'bbbb');

select id from t1 where i2 not search 'aaaa';

id
--------------------------------------------
2
[1] row(s) selected.
```

### REGEXP 문

REGEXP 문은 정규 표현식을 사용하여 데이터를 검색하는 데 사용됩니다. 일반적으로 특정 컬럼의 패턴을 정규 표현식을 사용하여 필터링합니다.

유의할 점은 REGEXP 절을 사용할 때 인덱스를 사용할 수 없으므로, 전체 검색 범위를 줄이기 위해 다른 컬럼에 인덱스 조건을 넣어 전체 검색 비용을 낮춰야 합니다.
특정 패턴을 확인하려면 SEARCH 또는 ESEARCH로 인덱스를 사용한 다음, 전체 데이터 수가 적은 상태에서 다시 REGEXP를 사용하면 전체 시스템의 효율성 향상에 도움이 됩니다.

```sql
Mach>
create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));
create table dual (id integer);
insert into dual values(1);
insert into realdual values(1, 'time1', 'series1 series21');
insert into realdual values(1, 'time2', 'series2 series22');
insert into realdual values(1, 'time3', 'series3 series32');


Mach> select * from realdual where id2 REGEXP 'time' ;
ID1         ID2                   ID3
------------------------------------------------------------
1           time3                 series3 series32
1           time2                 series2 series22
1           time1                 series1 series21
[3] row(s) selected.

Mach> select * from realdual where id2 REGEXP 'time[12]' ;
ID1         ID2                   ID3
------------------------------------------------------------
1           time2                 series2 series22
1           time1                 series1 series21
[2] row(s) selected.

Mach> select * from realdual where id2 REGEXP 'time[13]' ;
ID1         ID2                   ID3
------------------------------------------------------------
1           time3                 series3 series32
1           time1                 series1 series21
[2] row(s) selected.

Mach> select * from realdual where id2 regexp 'time[13]' and id3 regexp 'series[12]';
ID1         ID2                   ID3
------------------------------------------------------------
1           time1                 series1 series21
[1] row(s) selected.

Mach> select * from realdual where id2 NOT REGEXP 'time[12]';
ID1         ID2                   ID3
------------------------------------------------------------
1           time3                 series3 series32
[1] row(s) selected.

Mach> SELECT 'abcde' REGEXP 'a[bcd]{1,10}e' from dual;
'abcde' REGEXP 'a[bcd]{1,10}e'
---------------------------------
1
[1] row(s) selected.
```

### IN 문

```sql
column_name IN (value1, value2,...)
```

IN 문은 값 목록에서 만족하면 TRUE를 반환합니다. OR로 연결된 구문과 동일합니다.

### IN 문과 서브쿼리 사용

조건문에서 IN 문의 우측에 서브쿼리를 사용할 수 있습니다. 단, IN 조건의 좌측에 둘 이상의 컬럼을 지정하면 에러로 처리되며, 우측 서브쿼리에서 반환된 결과 집합이 좌측 컬럼 값에 존재하는지 확인합니다.

```sql
WHERE i1 IN (Select c1 from ...)
```

* Machbase 서버는 상관 서브쿼리를 지원하지 않으므로, 서브쿼리에서 외부 쿼리의 컬럼을 참조할 수 없습니다.

### BETWEEN 문

```sql
column_name BETWEEN value1 AND value2
```

BETWEEN 문은 컬럼의 값이 value1과 value2의 범위에 있으면 TRUE를 반환합니다.

### RANGE 문

```sql
column_name RANGE duration_spec;

-- duration_spec : integer (YEAR | WEEK | HOUR | MINUTE | SECOND);
```

주어진 컬럼에 대한 시간 조건을 쉽게 지정할 수 있는 Range 연산자를 제공합니다. Range 연산자는 (BEFORE 키워드로 지정된) 특정 시간을 지정하는 대신, 현재 시간으로부터 시간 범위를 연산 대상으로 지정합니다. 이 연산자를 사용하면 원하는 시간 범위 내의 결과 레코드를 쉽게 조회할 수 있습니다.

```sql
select * from test where id < 2 and c1 range 1 hour;
ID          C1
-----------------------------------------------
1           2014-07-25 09:28:53 706:707:001
[1] row(s) selected.
```


## GROUP BY / HAVING

GROUP BY 절은 SELECT 문의 결과를 특정 컬럼을 기준으로 그룹화하는 데 사용됩니다. 집계 함수를 사용하여 그룹별로 정렬하거나 집계할 때 사용됩니다. 그룹은 GROUP BY 절에 지정된 컬럼에 대해 동일한 컬럼 값을 가진 레코드를 의미합니다. GROUP BY 절 뒤에 HAVING 절을 결합하여 그룹 선택에 대한 조건식을 설정할 수 있습니다. 즉, GROUP BY 절로 구성된 모든 그룹 중 HAVING 절에 지정된 조건식을 만족하는 그룹만 조회됩니다.

```sql
SELECT ...
GROUP BY { col_name | expr } ,...[ HAVING <search_condition> ]

select id1, avg(id2) from exptab where id2 group by id1 order by id1;
id1 컬럼을 기준으로 id2의 평균값을 구합니다.
```


## ORDER BY

ORDER BY 절은 쿼리 결과를 오름차순 또는 내림차순으로 정렬합니다. ASC 또는 DESC와 같은 정렬 옵션을 지정하지 않으면 ORDER BY 절은 기본적으로 오름차순으로 정렬합니다. ORDER BY 절이 지정되지 않으면 조회될 레코드의 순서는 쿼리에 따라 달라집니다.

```sql
SELECT ...
ORDER BY {col_name | expr} [ASC | DESC]

select id1, avg(id2) from exptab where id2 group by id1 order by id1;
id1 컬럼을 기준으로 id2의 평균값을 구합니다.
```


## SERIES BY

SERIES BY 절은 정렬된 결과 집합을 SERIES BY 조건을 만족하는 연속적인 결과 값으로 추출합니다. ORDER BY 절이 지정되지 않으면 _ARRIVAL_TIME 컬럼 값을 사용하여 정렬된 결과를 생성합니다. 따라서 GROUP BY 절을 사용하거나 _ARRIVAL_TIME 컬럼이 없는 volatile 테이블 또는 lookup 테이블에 대한 쿼리인 경우 ORDER BY 절을 사용해야 합니다.

조건절을 만족하는 결과 값은 동일한 SERIESNUM() 함수의 반환 값을 가집니다.

```sql
예를 들어, 다음 데이터에 대해

CREATE TABLE T1 (C1 INTEGER, C2 INTEGER);
INSERT INTO T1 VALUES (0, 1);

INSERT INTO T1 VALUES (1, 2);

INSERT INTO T1 VALUES (2, 3);

INSERT INTO T1 VALUES (3, 2);

INSERT INTO T1 VALUES (4, 1);

INSERT INTO T1 VALUES (5, 2);

INSERT INTO T1 VALUES (6, 3);

INSERT INTO T1 VALUES (7, 1);


다음 쿼리는 다음 출력을 생성합니다:

SELECT C1,C2 FROM T1 ORDER BY C1 SERIES BY C2>1;
C1          C2
---------------------------
1           2
2           3
3           2
5           2
6           3

C2 컬럼의 값이 1보다 큰 경우 C1의 RANGE 값을 알고 싶다면 SERIESNUM 함수로 각 레코드가 어느 그룹에 포함되는지 출력하여 범위를 결정할 수 있습니다.
```


## LIMIT

LIMIT 절은 출력할 레코드 수를 제한하는 데 사용됩니다. 결과 집합의 첫 번째 행부터 마지막 행까지 출력할 정수를 지정할 수 있습니다.

```sql
LIMIT [offset,] row_count

select id1, avg(id2) from exptab where id2 group by id1 order by id1 LIMIT 10;
```


## DURATION

DURATION은 _arrival_time을 기준으로 데이터 조회 범위를 쉽게 결정할 수 있는 키워드입니다. BEFORE 문과 함께 사용하여 특정 시점의 특정 범위의 데이터를 설정합니다. 이 DURATION을 사용하면 검색 성능을 극적으로 높이고 시스템 부하를 극적으로 줄일 수 있습니다. 보다 자세한 사용법은 다음을 참조하십시오.

```sql
DURATION Number TimeSpec [BEFORE/AFTER Number TimeSpec]
DURATION FROM expr TO expr
TimeSpec : YEAR | MONTH | WEEK |  DAY | HOUR | MINUTE | SECOND
```

`DURATION FROM expr TO expr`는 명시적인 `_arrival_time` 범위를 조회합니다. `expr`에는
`TO_DATE(value, format)` 같은 datetime 표현식을 사용할 수 있습니다.

```sql
create table t8(i1 integer);
insert into t8 values(1);
insert into t8 values(2);

select i1 from t8;

-- Without BEFORE clause
select i1 from t8 duration 2 second;
select i1 from t8 duration 1 minute;
select i1 from t8 duration 1 hour;
select i1 from t8 duration 1 day;
select i1 from t8 duration 1 week;
select i1 from t8 duration 1 month;
select i1 from t8 duration 1 year;

-- Using full DURATION statement
select i1 from t8 duration 1 second before 1 day;
select i1 from t8 duration 1 minute before 1 day;
select i1 from t8 duration 1 hour before 1 day;
select i1 from t8 duration 1 day before 1 day;
select i1 from t8 duration 1 week before 1 day;
select i1 from t8 duration 1 month before 1 day;
select i1 from t8 duration 1 year before 1 day;

-- Using explicit range
select i1 from t8
duration from to_date('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
       to to_date('2030-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

결과는 다음과 같습니다.

```sql
Mach> create table t8(i1 integer);
Created successfully.

Mach> insert into t8 values(1);
1 row(s) inserted.

Mach> insert into t8 values(2);
1 row(s) inserted.

Mach> select i1 from t8;
i1
--------------
2
1
[2] row(s) selected.

## BEFORE 절 없이
Mach> select i1 from t8 duration 2 second;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 minute;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 hour;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 day;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 week;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 month;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 year;
i1
--------------
2
1
[2] row(s) selected.

-- Using full DURATION statement
Mach> select i1 from t8 duration 1 second before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 minute before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 hour before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 day before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 week before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 month before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 year before 1 day;
i1
--------------
[0] row(s) selected.
```


## 데이터 저장

쿼리 결과를 CSV 데이터 파일로 직접 저장합니다.

```sql
SAVE DATA INTO 'file_name.csv' [HEADER ON|OFF] [(FIELDS | COLUMNS) [TERMINATED BY 'char'] [ENCLOSED BY 'char']] [ENCODED BY coding_name] AS select query;
```

옵션은 다음과 같습니다.

|옵션|설명|
|--|--|
|HEADER (ON\|OFF)|생성될 CSV 파일의 첫 줄에 컬럼명을 출력할지 여부를 결정합니다. 기본값은 OFF입니다.|
|(FIELDS\|COLUMNS) TERMINATED BY 'term_char'<br><br>ENCLOSED BY 'enclose_char'|생성될 CSV 파일의 필드 구분자와 enclosing 문자를 지정합니다.|
|ENCODED BY coding_name<br><br>coding_name = ( UTF8, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280 )|출력 데이터 파일의 인코딩 형식을 지정합니다. 기본값은 UTF8입니다.|

```sql
SAVE DATA INTO '/tmp/aaa.csv' AS select * from t1;
-- select 문을 실행하고 결과를 '/tmp/aaa.csv' 파일에 csv 형식으로 작성합니다.

SAVE DATA INTO '/tmp/ccc.csv' HEADER ON FIELDS TERMINATED BY ';' ENCLOSED BY '\'' ENCODED BY MS949 AS select * from t1 where i1 > 100;
-- select 문을 실행하고 결과를 /tmp/ccc.csv 파일에 작성합니다. 필드 구분자와 enclosing 문자를 지정하고, 저장된 데이터의 인코딩을 MS949로 설정합니다.
```

## select-hint


# Index

* [소개](#introduction)
* [PARALLEL](#parallel)
* [NOPARALLEL](#noparallel)
* [FULL](#full)
* [NO_INDEX](#no_index)
* [ROLLUP_TABLE](#rollup_table)
* [RID_RANGE](#rid_range)
* [SCAN_FORWARD, SCAN_BACKWARD](#scan_forward-scan_backward)


## 소개

SELECT 문에서 활용 가능한 힌트들을 정리했습니다.

##  PARALLEL

병렬 쿼리 실행 시 사용할 병렬 처리 계수를 지정합니다.

```sql
SELECT /*+ PARALLEL(table_name, parallel_factor) */ ...
```

```sql
Mach> CREATE TABLE log_parallel_test (sensor VARCHAR(32), frequency DOUBLE, value DOUBLE, ts DATETIME);
Mach> CREATE INDEX idx_ts ON log_parallel_test (ts);

Mach> EXPLAIN SELECT /*+ PARALLEL(log_parallel_test, 8) */ sensor, frequency, avg(value)
      FROM log_parallel_test
      WHERE ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD') and ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')
      GROUP BY sensor, frequency;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  GROUP AGGREGATE
   PARALLEL INDEX SCAN
    *BITMAP RANGE (table id:3, column id:4, index id:4)
    [KEY RANGE]
     * ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD')
     * ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')
[7] row(s) selected.
```


##  NOPARALLEL

병렬 처리를 사용하지 않도록 강제합니다.

```sql
SELECT /*+ NOPARALLEL(table_name) */ ...
```

```sql
Mach> CREATE TABLE log_parallel_test (sensor VARCHAR(32), frequency DOUBLE, value DOUBLE, ts DATETIME);
Mach> CREATE INDEX idx_ts ON log_parallel_test (ts);

Mach> EXPLAIN SELECT /*+ NOPARALLEL(log_parallel_test) */ sensor, frequency, avg(value)
      FROM log_parallel_test
      WHERE ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD') and ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')
      GROUP BY sensor, frequency;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  GROUP AGGREGATE
   INDEX SCAN
    *BITMAP RANGE (table id:5, column id:4, index id:6)
    [KEY RANGE]
     * ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD')
     * ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')
[7] row(s) selected.
```


##  FULL

INDEX SCAN을 사용하지 않도록 지정합니다.

```sql
SELECT /*+ FULL(table_name) */ ...
```

```sql
Mach> CREATE TABLE log_full_test (sensor VARCHAR(32), I1 INTEGER);
Mach> CREATE INDEX idx_I1 ON log_full_test (I1);

Mach> EXPLAIN SELECT * FROM log_full_test WHERE I1 = 1;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:14, column id:2, index id:15)
   [KEY RANGE]
    * I1 = 1
[5] row(s) selected.

Mach> EXPLAIN SELECT /*+ FULL(log_full_test) */ * FROM log_full_test WHERE I1 = 1;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  FULL SCAN
[2] row(s) selected.
```


##  NO_INDEX

지정한 인덱스를 사용하지 않도록 합니다.

```sql
SELECT /*+ NO_INDEX(table_name,index_name) */ ...
```

```sql
Mach> CREATE TABLE log_no_index_test (sensor VARCHAR(32), I1 INTEGER, I2 INTEGER);
Mach> CREATE INDEX idx_I1 ON log_no_index_test (I1);
Mach> CREATE INDEX idx_I2 ON log_no_index_test (I2);

Mach> EXPLAIN SELECT * FROM log_no_index_test WHERE I1 = 1;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (t:7, c:1, i:8) with BLOOMFILTER
   [KEY RANGE]
    * I1 = 1
[5] row(s) selected.

Mach> EXPLAIN SELECT /*+ NO_INDEX(log_no_index_test,idx_I1) */ * FROM log_no_index_test WHERE I1 = 1;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  FULL SCAN
[2] row(s) selected.

Mach> EXPLAIN SELECT * FROM log_no_index_test WHERE I1 = 1 or I2 = 2;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   INDEX (OR)
    *BITMAP RANGE (table id:21, column id:2, index id:22)
    *BITMAP RANGE (table id:21, column id:3, index id:23)
   [KEY RANGE]
    * I1 = 1 or I2 = 2
[7] row(s) selected.

Mach> EXPLAIN SELECT /*+ NO_INDEX(log_no_index_test, idx_I1) */ * FROM log_no_index_test WHERE I1 = 1 or I2 = 2;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  FULL SCAN
[2] row(s) selected.

Mach> EXPLAIN SELECT * FROM log_no_index_test WHERE I1 = 1 and I2 = 2;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:21, column id:2, index id:22)
   *BITMAP RANGE (table id:21, column id:3, index id:23)
   [KEY RANGE]
    * I1 = 1
    * I2 = 2
[7] row(s) selected.

Mach> EXPLAIN SELECT /*+ NO_INDEX(log_no_index_test, idx_I1) */ * FROM log_no_index_test WHERE I1 = 1 and I2 = 2;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:21, column id:3, index id:23)
   [KEY RANGE]
    * I2 = 2
   [FILTER]
    * I1 = 1
[7] row(s) selected.
Elapsed time: 0.001
Mach>
Mach>
Mach> EXPLAIN SELECT /*+ NO_INDEX(log_no_index_test, idx_I2) */ * FROM log_no_index_test WHERE I1 = 1 and I2 = 2;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:21, column id:2, index id:22)
   [KEY RANGE]
    * I1 = 1
   [FILTER]
    * I2 = 2
[7] row(s) selected.
```


##  ROLLUP_TABLE

조건 롤업이 여러 개 있을 때 특정 롤업 테이블을 강제로 선택합니다. 힌트가 있으면 자동 선택 규칙보다 항상 우선합니다.

```sql
SELECT /*+ ROLLUP_TABLE(rollup_table_name) */ ...
```

- 힌트가 없으면 동일한 주기/값 컬럼/JSON PATH 후보 중 조건 없는 롤업이 우선 선택됩니다.
- 조건 롤업을 반드시 써야 하는 경우 힌트로 지정합니다.
- `FIRST()`/`LAST()`를 사용한다면 `EXTENSION` 롤업을 힌트로 지정해야 합니다.

```sql
SELECT /*+ ROLLUP_TABLE(_tag_rollup_cond_1s) */
       rollup('sec', 30, time) AS rt, AVG(value), COUNT(value)
FROM   tag_bulk
WHERE  name = 'dev9'
  AND  time BETWEEN '2020-01-02 00:00:00' AND '2020-01-02 00:10:00'
GROUP BY rt
ORDER BY rt;
```


##  RID_RANGE

RID 범위를 지정하여 해당 범위 내에서만 연산하도록 합니다.

```sql
SELECT /*+ RID_RANGE(table_name,number,number) */ ...
```

```sql
Mach> SELECT /*+ RID_RANGE(TEST,45,50) */ _RID, * FROM TEST;
_RID                 I1
------------------------------------
49                   1
48                   1
47                   1
46                   1
45                   1
[5] row(s) selected.
```


##  SCAN_FORWARD, SCAN_BACKWARD

LOG 테이블의 스캔 방향을 지정합니다. `SCAN_FORWARD`는 가장 오래된 입력 레코드부터, `SCAN_BACKWARD`는 가장 최근 입력 레코드부터 조회합니다.

표준 에디션의 LOG 테이블에만 적용됩니다.

```sql
SELECT /*+ SCAN_FORWARD(table_name) */ ...
SELECT /*+ SCAN_BACKWARD(table_name) */ ...
```

```sql
Mach> SELECT /*+ SCAN_FORWARD(mytbl) */  _ARRIVAL_TIME, VALUE FROM mytbl LIMIT 10;
_ARRIVAL_TIME                   VALUE
----------------------------------------------------------------
2017-01-01 00:00:49 500:000:000 0
2017-01-01 00:01:39 500:000:000 1
2017-01-01 00:02:29 500:000:000 2
2017-01-01 00:03:19 500:000:000 3
2017-01-01 00:04:09 500:000:000 4
2017-01-01 00:04:59 500:000:000 5
2017-01-01 00:05:49 500:000:000 6
2017-01-01 00:06:39 500:000:000 7
2017-01-01 00:07:29 500:000:000 8
2017-01-01 00:08:19 500:000:000 9
[10] row(s) selected.

Mach> SELECT /*+ SCAN_BACKWARD(mytbl) */ _ARRIVAL_TIME, VALUE FROM mytbl LIMIT 10;
_ARRIVAL_TIME                   VALUE
----------------------------------------------------------------
2017-02-27 20:53:19 500:000:000 9
2017-02-27 20:52:29 500:000:000 8
2017-02-27 20:51:39 500:000:000 7
2017-02-27 20:50:49 500:000:000 6
2017-02-27 20:49:59 500:000:000 5
2017-02-27 20:49:09 500:000:000 4
2017-02-27 20:48:19 500:000:000 3
2017-02-27 20:47:29 500:000:000 2
2017-02-27 20:46:39 500:000:000 1
2017-02-27 20:45:49 500:000:000 0
[10] row(s) selected.
```

## time-expressions


## 개요

상대 시간 표현은 알려진 기준 시점으로부터의 차이를 SQL 문 안에서 직접 기술할 수 있도록 해 줍니다. 최근 계측 데이터를 필터링하거나 향후 작업을 예약하고, 보조 함수 호출 없이 시계열 윈도를 정렬해야 하는 운영자에게 유용합니다.

> **참고**: 이 기능은 Machbase 8.0.50 이상에서 지원됩니다.

## 빠르게 살펴보기

1. 최근 1시간 데이터를 조회합니다.
   ```sql
   SELECT * FROM sensor_log WHERE event_time > now - 1h;
   ```
2. 2일 6시간 이후까지의 일정을 확인합니다.
   ```sql
   SELECT * FROM maintenance_plan WHERE planned_at < now + 2d6h;
   ```
3. 하위 초 단위까지 세그먼트를 결합합니다.
   ```sql
   SELECT to_char(now + 3s125ms10us4ns, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn');
   ```

## 구문 요약

- 리터럴은 공백 없이 이어지는 `<숫자><단위>` 세그먼트 하나 이상으로 작성합니다.
- 단위는 소문자를 사용하며, 서로 다른 크기는 이어 붙여 표현합니다(`2h30m`).
- `+` 또는 `-` 접두어를 붙이거나 산술식을 사용할 수 있습니다(`now - 90m`, `sample_time + 15s` 등).
- 숫자 뒤에 단위를 붙이지 않으면 나노초 단위로 해석됩니다.
- 상대 리터럴은 `INTERVAL`로 평가되며, `DATETIME`에 더하거나 빼면 결과 역시 `DATETIME`이 됩니다.

## 지원 단위

| 접미사 | 의미             | 예시     | 동일한 기간             |
|--------|------------------|---------|---------------------|
| `ns`   | 나노초           | `500ns` | 500 나노초            |
| `us`   | 마이크로초       | `20us`  | 0.00002초           |
| `ms`   | 밀리초           | `15ms`  | 0.015초             |
| `s`    | 초               | `45s`   | 45초                |
| `m`    | 분               | `30m`   | 30분                |
| `h`    | 시간             | `12h`   | 12시간              |
| `d`    | 일               | `7d`    | 7일                 |
| `w`    | 주               | `2w`    | 14일                |

> **참고**: 월과 연은 길이가 일정하지 않아 지원하지 않습니다. 지원하지 않는 접미사(`1y`, `1mo` 등)를 사용하면 invalid time expression 오류(`ERR-02034`)가 발생합니다.

## 복합 리터럴 작성

- 가독성을 위해 가장 큰 단위부터 작성합니다(`5d4h30m`).
- 값이 0인 세그먼트는 생략합니다. `4h15m0s`보다는 `4h15m`이 좋습니다.
- 세그먼트 순서는 바뀌어도 되지만 일관성을 유지하면 실수를 줄일 수 있습니다. `1h30m`과 `30m1h`는 동일하게 평가됩니다.
- 긴 간격은 SQL 문자열 리터럴에서 밑줄로 구분할 수 없으므로 주석(`/* +1d12h30m */`)을 달거나 SQL 변수에 저장해 문서화하는 방식을 권장합니다.

## 활용 패턴

### 시간 구간 필터링

```sql
-- 최근 24시간 기록
SELECT *
  FROM rtrollup
 WHERE time BETWEEN now - 1d AND now;

-- 최근 10분 이내 발생한 알람
SELECT alert_id, level, occurred_at
  FROM alert_log
 WHERE occurred_at >= sysdate - 10m;
```

### 향후 작업 예약

```sql
-- 다음 영업일 + 2시간 이내 실행할 작업
SELECT job_id, scheduled_at
  FROM job_queue
 WHERE scheduled_at <= now + 1d2h;

-- 30분 후에 예정된 정비 일정을 등록
INSERT INTO device_schedule (device_id, maintenance_due)
VALUES ('device-001', now + 30m);
```

### 시간 기반 필터와 조인

```sql
-- 특정 시간 범위의 데이터 선택
SELECT device_id, ts, value
  FROM metrics_stream
 WHERE ts BETWEEN now - 15m AND now
   AND device_id = 'sensor-01';

-- 상대 오프셋을 이용해 두 소스를 조인
SELECT a.ts, a.value AS raw_value, b.value AS calibrated
  FROM raw_metrics a
  JOIN calibration b
    ON b.ts BETWEEN a.ts - 500ms AND a.ts + 500ms;
```

### DATETIME 값과 캐스팅

```sql
SELECT to_char(to_date('2024-05-01', 'YYYY-MM-DD') + 3d,
               'YYYY-MM-DD');                              -- 2024-05-04
SELECT to_char(to_date('2024-05-01 08:00:00',
                       'YYYY-MM-DD HH24:MI:SS') - 4h15m,
               'YYYY-MM-DD HH24:MI:SS');                   -- 2024-05-01 03:45:00
SELECT to_char(to_date('2024-05-01', 'YYYY-MM-DD') + 2h30m45s250ms,
               'YYYY-MM-DD HH24:MI:SS mmm');               -- 2024-05-01 02:30:45 250
```

문자열 리터럴은 interval 산술에서 `DATETIME`으로 암시적 변환되지 않습니다. 먼저
`TO_DATE`로 변환해야 합니다.

### 순수 숫자와 혼합

```sql
-- 숫자 리터럴은 기본적으로 나노초이므로 정확히 1초가 더해집니다.
SELECT event_time + 1000000000 AS event_time_plus_1s
  FROM events;

-- 250나노초를 뺍니다.
SELECT event_time - 250 AS event_time_minus_250ns
  FROM events;
```

## 동작 및 제한 사항

- 정밀도는 나노초까지 지원합니다. 64비트 범위를 넘으면 오버플로가 발생합니다.
- 산술 연산은 일반 우선순위를 따릅니다. 괄호 → 곱셈/나눗셈 → 덧셈/뺄셈 순이며, 연산이 길어질 때는 괄호를 사용하세요.
- 인터벌 비교는 최종 `DATETIME` 값을 기준으로 이루어집니다. 인터벌 자체는 `ORDER BY` 절에서 사용할 수 없습니다.
- 이 기능은 스탠더드 에디션에서 제공되며, 구버전 지원 여부는 릴리스 노트를 확인하십시오.

## 오류 처리

| 시나리오                                | 오류 코드                 | 해결 방법                                     |
|----------------------------------------|---------------------------|----------------------------------------------|
| 지원하지 않는 접미사(`1y`, `5mo`)      | `ERR-02034` invalid time expression | 지원 단위(`30d` 등)로 교체합니다.             |
| 단위 누락(`now + 10`)                   | 나노초로 해석됨            | 분/초 등을 의도했다면 명시적으로 접미사를 붙입니다. |
| 값이 너무 큰 리터럴(`1000000d`)        | `ERR_OVERFLOW_INTERVAL`   | 크기를 줄이거나 반복 처리로 로직을 나눕니다. |
| 숫자가 아닌 문자가 포함됨(`1h3xm`)     | Invalid time expression   | 오탈자를 수정합니다(`1h3m`).                  |

## 모범 사례

- 팀 전체가 소문자 접미사를 사용하도록 표준화하세요.
- 자주 쓰는 오프셋은 구성 테이블에 저장해 재사용과 감사에 활용합니다.
- 복잡한 표현식에는 유지보수를 돕는 주석을 남깁니다(`-- subtract 1 business week`).
- 리터럴을 동적으로 생성할 때는 잘못된 접미사가 주입되지 않도록 입력 값을 검증합니다.

## 문제 해결 체크리스트

- **예상과 다른 범위**: `now`와 계산된 경계를 함께 출력해 오프셋을 검증합니다.
- **잘못된 단위**: 숫자만 입력하면 나노초로 처리된다는 점을 기억하고, 사람이 읽기 쉬운 단위가 필요하면 `s`, `m`, `h` 등을 붙입니다.
- **함수와의 조합**: 윈도 함수나 집계 필터와 함께 사용할 때는 서브쿼리에서 리터럴을 평가해 문장당 한 번만 계산되도록 합니다.

## 자주 묻는 질문

- **`ADD_TIME`과 함께 사용할 수 있나요?** 가능합니다. `ADD_TIME(now, '0/0/0 0:15:0') + 30s`처럼 함수와 리터럴을 연결할 수 있습니다.
- **리터럴을 변수에 저장할 수 있나요?** 상대 시간 리터럴은 쿼리 실행 시 평가되므로 변수에 저장할 수 없습니다. 대신 반복해서 사용할 쿼리에 직접 포함시키세요.
- **영업일 기준으로 계산하려면?** 상대 리터럴은 절대 시간 간격만 처리합니다. 영업일 계산은 애플리케이션 로직이나 캘린더 테이블을 활용하세요.

## 참고 치트시트

```
패턴             의미
--------------  --------------------------------------------
now - 5m        정확히 5분 전 시각
sysdate + 1d    시스템 시간 기준 24시간 후(내일)
col_ts + 90s    컬럼 값을 90초 뒤로 이동
TO_DATE('2024-01-01','YYYY-MM-DD') + 2w  날짜 값에 14일을 더함
value + 250     `value`에 250나노초를 더함
```

상대 시간 표현은 보조 함수 없이도 정밀하고 읽기 쉬운 시간 연산을 제공합니다. `WHERE` 절, 계산 컬럼, Projection, 프로시저 코드 등 표현식을 사용할 수 있는 어디에서나 활용해 Machbase 분석을 간결하고 유지보수하기 쉽게 만드세요.

## user-manage


# Index

* [CREATE USER](#create-user)
* [DROP USER](#drop-user)
* [ALTER USER](#alter-user)
* [PASSWORD POLICY](#password-policy)
* [AUTH KEY 파일 생성](#auth-key-파일-생성)
* [AUTH KEY를 포함한 사용자 생성](#auth-key를-포함한-사용자-생성)
* [AUTH KEY 관리](#auth-key-관리)
* [AUTH KEY 메타 조회](#auth-key-메타-조회)
* [CONNECT](#connect)
* [GRANT/REVOKE](#grantrevoke)
* [Managing User Example](#managing-user-example)


## CREATE USER

**create_user_stmt:**

![create_user_stmt](/images/sql/user/create_user_stmt.png)

```sql
create_user_stmt ::= 'CREATE USER' user_name 'IDENTIFIED BY' password
```

사용자를 생성하는 구문입니다:

```sql
-- Example
CREATE USER new_user IDENTIFIED BY password
```

비밀번호 정책을 함께 지정하려면 다음 확장 구문을 사용합니다.

```sql
CREATE USER user_name IDENTIFIED BY password PASSWORD POLICY { NONE | LOW | HIGH }
```

예제:

```sql
CREATE USER app_user IDENTIFIED BY "Aa!StrongPwd1" PASSWORD POLICY LOW;
CREATE USER ops_user IDENTIFIED BY "Bb@StrongPwd2" PASSWORD POLICY HIGH;
```
사용자명은 생성 시 대문자로 변환되어 저장됩니다. 예를 들어 `CREATE USER app_user ...`로 생성하면
메타 테이블과 `V$` 뷰에서는 `APP_USER`로 조회됩니다. 이후 접속이나 권한 부여 구문에서도 같은 사용자명으로
처리됩니다.


## DROP USER

**drop_user_stmt:**

![drop_user_stmt](/images/sql/user/drop_user_stmt.png)

```sql
drop_user_stmt ::= 'DROP USER' user_name
```

사용자를 삭제하는 구문은 다음과 같습니다. SYS 사용자는 삭제할 수 없으며, 삭제하려는 사용자가 이미 생성한 테이블이 있으면 오류가 표시됩니다.

```sql
-- Example
DROP USER old_user
```


## ALTER USER

**alter_user_pwd_stmt:**

![alter_user_pwd_stmt](/images/sql/user/alter_user_pwd_stmt.png)

```sql
alter_user_pwd_stmt ::= 'ALTER USER' user_name 'IDENTIFIED BY' password
```

사용자는 다음 구문을 통해 비밀번호를 변경할 수 있습니다.

```sql
-- Example
ALTER USER user1 IDENTIFIED BY password
```

비밀번호를 변경하면서 정책도 함께 변경할 수 있습니다.

```sql
ALTER USER user_name IDENTIFIED BY password PASSWORD POLICY { NONE | LOW | HIGH }
```

정책을 변경할 때는 새 비밀번호를 함께 지정해야 합니다. `ALTER USER user_name PASSWORD POLICY HIGH`처럼 정책만 단독으로 변경하는 구문은 허용되지 않습니다.


## PASSWORD POLICY

비밀번호 정책은 `CREATE USER`와 `ALTER USER ... IDENTIFIED BY ...`에서 비밀번호 강도를 검증하는 기능입니다. 정책을 지정하지 않으면 기존 호환성을 위해 `NONE`이 적용됩니다.

정책 종류:

- `NONE`
  - 비밀번호 강도 제약이 없습니다.
  - 비밀번호 만료 시각(`VALID_BEFORE`)은 `NULL`입니다.
- `LOW`
  - 최소 길이 10자 이상이어야 합니다.
  - 대문자, 소문자, 특수문자를 포함해야 합니다.
  - 5자리 이상 연속 숫자, 증가/감소 숫자 연번, 키보드 연속 문자열은 사용할 수 없습니다.
  - 비밀번호 만료 시각(`VALID_BEFORE`)은 `NULL`입니다.
- `HIGH`
  - `LOW` 규칙을 모두 적용합니다.
  - 현재 비밀번호와 최근 24개 이내의 과거 비밀번호를 재사용할 수 없습니다.
  - 비밀번호 설정 시점부터 90일 후로 만료 시각(`VALID_BEFORE`)이 자동 설정됩니다.

정책 적용 예:

```sql
CREATE USER user1 IDENTIFIED BY "Aa!StrongPwd1";
CREATE USER user2 IDENTIFIED BY "Bb@StrongPwd2" PASSWORD POLICY LOW;
CREATE USER user3 IDENTIFIED BY "Cc#StrongPwd3" PASSWORD POLICY HIGH;

ALTER USER user2 IDENTIFIED BY "Dd$NewPwd44";
ALTER USER user2 IDENTIFIED BY "Ee%NewPwd55" PASSWORD POLICY LOW;
ALTER USER user3 IDENTIFIED BY "Ff#NewPwd66" PASSWORD POLICY NONE;
```

주의 사항:

- `ALTER USER ... IDENTIFIED BY ...`는 해당 사용자에 저장된 정책으로 새 비밀번호를 검증합니다.
- `ALTER USER ... IDENTIFIED BY ... PASSWORD POLICY ...`는 새 정책으로 새 비밀번호를 검증합니다.
- 정책을 `HIGH`로 설정하거나 `HIGH` 사용자의 비밀번호를 변경하면 `VALID_BEFORE`가 현재 시각 기준 90일 뒤로 갱신됩니다.
- 정책을 `LOW` 또는 `NONE`으로 설정하면 `VALID_BEFORE`는 `NULL`로 갱신됩니다.
- 만료된 계정은 로그인할 수 없으므로 본인 계정으로 비밀번호를 변경할 수 없습니다. 관리자 계정에서 새 비밀번호로 리셋해야 합니다.

정책과 만료 시각은 `M$SYS_USERS`에서 확인할 수 있습니다.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
FROM M$SYS_USERS;
```

`PWD_POLICY_LEVEL` 값은 `0 = NONE`, `1 = LOW`, `2 = HIGH`를 의미합니다. `VALID_BEFORE`는 값이 있을 때 `YYYY-MM-DD` 형식으로 표시됩니다.
## AUTH KEY 파일 생성

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

AUTH KEY 인증은 클라이언트 측 개인키 파일과 Machbase 사용자에 등록된 공개키를 사용합니다.
일반적으로 `openssl`로 키 쌍을 생성하고, 개인키는 클라이언트 호스트에 보관하며, 공개키만
Machbase에 등록합니다.

지원되는 알고리즘과 키 크기는 다음과 같습니다.

| 공개키 알고리즘 | 지원 키 파라미터 | 지원 서명 스킴 | 해시 |
| --- | --- | --- | --- |
| ECDSA | P-256, P-384, P-521 | `ECDSA` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PKCS1_V15` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PSS` | SHA-256 |

`AUTH_SIG_SCHEME`를 생략하면 키 알고리즘에 따라 기본 스킴을 사용합니다.

- ECDSA 키: `ECDSA`
- RSA 키: `RSA_PKCS1_V15`

RSA-PSS를 사용하려면 클라이언트 접속 옵션에서 `AUTH_SIG_SCHEME=RSA_PSS`를 명시합니다.
등록된 공개키 타입과 클라이언트가 요청한 서명 스킴이 맞지 않으면 인증이 실패합니다.

ECDSA P-256 키 생성 예:

```bash
openssl ecparam -name prime256v1 -genkey -noout -out app_user_ecdsa.key
openssl ec -in app_user_ecdsa.key -pubout -out app_user_ecdsa.pub
chmod 600 app_user_ecdsa.key
```

ECDSA P-384, P-521 키 생성 예:

```bash
openssl ecparam -name secp384r1 -genkey -noout -out app_user_ecdsa_p384.key
openssl ec -in app_user_ecdsa_p384.key -pubout -out app_user_ecdsa_p384.pub

openssl ecparam -name secp521r1 -genkey -noout -out app_user_ecdsa_p521.key
openssl ec -in app_user_ecdsa_p521.key -pubout -out app_user_ecdsa_p521.pub
```

RSA 2048-bit 키 생성 예:

```bash
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -pubout -out app_user_rsa.pub
chmod 600 app_user_rsa.key
```

RSA 3072-bit, 4096-bit 키를 사용하려면 `openssl genrsa`의 마지막 인자를 각각 `3072`, `4096`으로 지정합니다.

공개키를 SQL에 넣을 때는 PEM 파일을 줄바꿈이 `\n`으로 이스케이프된 한 줄 문자열로
변환합니다.

```bash
awk '{printf "%s\\n", $0}' app_user_ecdsa.pub
```

명령 출력 결과를 `CREATE USER ... WITH AUTH KEY` 또는 `ALTER USER ... ADD AUTH KEY`의
`key` 값으로 사용합니다.

다음 예는 생성한 공개키로 등록 SQL 파일을 만드는 방법입니다.

```bash
KEY_ESCAPED=$(awk '{printf "%s\\n", $0}' app_user_ecdsa.pub)

cat > add_app_user_key.sql <<EOF
ALTER USER app_user ADD AUTH KEY (
    key='${KEY_ESCAPED}',
    valid_before='2047-12-31',
    comment='openssl generated ecdsa key'
);
EOF
```

## AUTH KEY를 포함한 사용자 생성

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

Machbase는 비밀번호 인증과 함께 공개키 기반 challenge 인증용 AUTH KEY를 사용자에 등록할 수 있습니다.

```sql
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial key'
);
```

설명:

- `key`에는 PEM 형식 공개키를 넣습니다.
- SQL 문장 안에서는 PEM 줄바꿈을 `\n`으로 입력할 수 있습니다.
- `valid_before`는 `YYYY-MM-DD` 형식을 사용합니다.
- `valid_before`에는 시각이 포함된 datetime 형식(`YYYY-MM-DD HH24:MI:SS`)을 사용할 수 없습니다.
- `comment`는 현재 AUTH KEY 문법에서 필수입니다.
- `CREATE USER ... WITH AUTH KEY`로 생성한 첫 키는 즉시 활성 상태(`ACTIVATED=1`)로 등록됩니다.
- 사용자는 비밀번호와 AUTH KEY를 동시에 보유할 수 있습니다. 실제 인증은 클라이언트의 `AUTH_MODE` 선택에 따라 비밀번호 또는 challenge 중 하나만 수행되며, 실패 시 다른 방식으로 자동 fallback하지 않습니다.

## AUTH KEY 관리

### AUTH KEY 추가

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAqO+tddiAQzsT8iajPy5QJPamIlyq2zB01wgHSTs3OOrvw0uKoFQD\ncqKaDzRya73LETXIEev3nwhGCnG4SjedMHj3EH9/rRJphFtv/dzw0OHum/UhVulR\nIXUYzrTbKPTQ+qyjS8UXTteMncf9OOh4AQyS4+iJW+U344fxymR8USRgZ25N9jhf\n2gkKnn5YSPZHf8ZHQGeA7OXANBwPmH5dQwfqghXRa7Nk1hmkIAnQQXCBJW/Lin+x\nwQfqv8DVwNaiziz77voPwaeD5akq1JYWvcPlOnh+NN3tpu5gudke/t/In4NFJ3W9\n4unVcYIfxcdDSoht3AMObGmuDazOjQJFGQIDAQAB\n-----END RSA PUBLIC KEY-----\n',
    valid_before='2048-01-31',
    comment='rollover candidate'
);
```

추가된 키는 즉시 활성 상태(`ACTIVATED=1`)로 생성됩니다. 롤오버 기간에는 한 사용자에 여러 활성 AUTH KEY를 둘 수 있습니다.

### AUTH KEY 활성화 / 비활성화

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

- 비활성화된 키는 challenge 인증에 사용할 수 없습니다.
- 한 사용자에 여러 AUTH KEY를 보유할 수 있습니다.

### AUTH KEY 유효기간 변경

```sql
ALTER USER app_user ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';
```

- `VALID_BEFORE`가 지난 키는 인증에 사용할 수 없습니다.
- 입력 형식은 `YYYY-MM-DD`이며, 시각이 포함된 datetime 형식은 허용되지 않습니다.

### AUTH KEY 삭제

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

- 삭제된 키는 즉시 인증에 사용할 수 없습니다.
- 사용자 삭제 시 해당 사용자의 AUTH KEY 메타도 함께 정리됩니다.

## AUTH KEY 메타 조회

등록된 AUTH KEY 메타는 `V$USER_AUTH_KEYS`에서 조회할 수 있습니다.

주요 컬럼:

- `KEY_ID`: AUTH KEY 식별자
- `USER_NAME`: AUTH KEY 소유 사용자
- `KEY_ALGO`: 키 알고리즘 (`RSA`, `ECDSA`)
- `KEY_PARAM`: 키 파라미터
  - RSA 키: 비트 길이 예) `2048`
  - EC 키: 곡선 이름 예) `P-256`, `P-384`, `P-521`
- `ACTIVATED`: 활성화 여부
- `VALID_AFTER`, `VALID_BEFORE`: 유효 기간
- `COMMENT`: 사용자 메모
- `PUBKEY`: PEM 형식 공개키 본문

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name='APP_USER'
 ORDER BY key_id;
```

공개키 본문까지 확인하려면 `PUBKEY` 컬럼을 조회합니다.

```sql
SELECT key_id, user_name, pubkey
  FROM V$USER_AUTH_KEYS
 WHERE user_name='APP_USER'
 ORDER BY key_id;
```


## CONNECT

**user_connect_stmt:**

![user_connect_stmt](/images/sql/user/user_connect_stmt.png)

```sql
user_connect_stmt: 'CONNECT' user_name '/' password
```

사용자는 애플리케이션을 종료하지 않고 다음 구문을 통해 다른 사용자로 재연결할 수 있습니다.

```sql
-- Example
CONNECT user1/password;
```


## GRANT/REVOKE

![grant_stmt](/images/sql/user/grant_stmt.png)

![revoke_stmt](/images/sql/user/revoke_stmt.png)

![priv_value](/images/sql/user/priv_value.png)

GRANT 문을 통해 사용자에게 권한을 부여하고, REVOKE 문을 통해 이미 부여된 권한을 회수합니다.

기본 예제:

```sql
-- user1에게 mytable에 대한 SELECT 권한 부여
GRANT SELECT ON mytable TO user1;

-- user1에게 mytable에 대한 모든 권한 부여
GRANT ALL ON mytable TO user1;
```

```sql
-- user1에게 부여된 mytable에 대한 UPDATE 권한 취소
REVOKE UPDATE ON mytable FROM user1;

-- user1에게 부여된 mytable에 대한 모든 권한 취소
REVOKE ALL ON mytable FROM user1;
```

### 테이블 권한

테이블에 대한 권한을 부여할 때는 다음과 같이 사용합니다.

- `table`
- `user.table`
- `db.user.table`

권한 종류:

- `SELECT`
- `INSERT`
- `DELETE`
- `UPDATE`
- `ALL`

예제:

```sql
GRANT SELECT ON sensor_log TO reader;
GRANT SELECT, INSERT ON sys.sensor_log TO writer;
REVOKE INSERT ON sys.sensor_log FROM writer;
GRANT ALL ON machbasedb.sys.sensor_log TO app_user;
```

### Machbase 8.5 이상: 데이터베이스 권한

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

Machbase 8.5 이상에서는 `MACHBASEDB`를 대상으로 데이터베이스 범위 권한을 부여할 수 있습니다.

```sql
GRANT CREATE ON machbasedb TO ddl_user;
GRANT DROP ON machbasedb TO ddl_user;
GRANT ALTER ON machbasedb TO ops_user;
GRANT BACKUP ON machbasedb TO backup_user;
GRANT MOUNT ON machbasedb TO mount_user;
GRANT DDL ON machbasedb TO deploy_user;
GRANT ALL ON machbasedb TO admin_user;
```

데이터베이스 범위에서 사용할 수 있는 권한:

- `CREATE`
- `DROP`
- `ALTER`
- `MOUNT`
- `BACKUP`
- `DDL`
- `ALL`

여기서 `DDL`은 `CREATE + DROP` 묶음입니다.

### `ALL`의 의미

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

`ALL`은 항상 같은 뜻이 아닙니다. 대상에 따라 의미가 달라집니다.

- `GRANT ALL ON machbasedb TO user1`
  - 데이터베이스 범위 전체 권한을 부여합니다.
- `GRANT ALL ON sys.table1 TO user1`
  - 해당 테이블에 대한 전체 DML 권한을 부여합니다.

즉, `MACHBASEDB`에 대한 `ALL`과 테이블에 대한 `ALL`은 같은 문법이지만 용도가 다릅니다.

### 데이터베이스 이름에 직접 DML 권한을 부여할 수 없는 경우

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

다음과 같이 데이터베이스 이름 `MACHBASEDB`에 `SELECT`, `INSERT`, `DELETE`, `UPDATE`를 직접 부여하는 방식은 사용할 수 없습니다.

```sql
GRANT SELECT ON machbasedb TO user1;
GRANT INSERT ON machbasedb TO user1;
REVOKE DELETE ON machbasedb FROM user1;
REVOKE UPDATE ON machbasedb FROM user1;
```

이 경우에는 다음과 같은 오류가 발생합니다.

```sql
[ERR-02186: Invalid database name.]
```

조회나 입력 권한을 주려면 반드시 테이블을 지정해야 합니다.

```sql
GRANT SELECT ON sys.sensor_log TO user1;
GRANT INSERT ON sys.sensor_log TO user1;
```

### 데이터베이스 대상 이름은 `MACHBASEDB`를 사용

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

데이터베이스 범위 권한을 부여할 때는 `MACHBASEDB`를 사용합니다.

```sql
GRANT BACKUP ON machbasedb TO backup_user;
REVOKE BACKUP ON machbasedb FROM backup_user;
```

잘못된 데이터베이스 이름을 지정하면 오류가 발생합니다.

```sql
GRANT BACKUP ON typo TO backup_user;
```

```sql
[ERR-02186: Invalid database name.]
```

### 데이터베이스 권한이 필요한 작업

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

다음 작업은 테이블 권한이 아니라 `MACHBASEDB`에 대한 데이터베이스 권한이 필요합니다.

- `CREATE TABLE`, `DROP TABLE`
- `CREATE VIEW`, `DROP VIEW`
- `CREATE INDEX`, `DROP INDEX`
- `CREATE ROLLUP`, `DROP ROLLUP`
- `CREATE TABLESPACE`, `DROP TABLESPACE`
- `CREATE RETENTION`, `DROP RETENTION`
- `ALTER SYSTEM`
- `BACKUP DATABASE`
- `MOUNT DATABASE`, `UNMOUNT DATABASE`

예를 들어 일반 사용자가 `CREATE VIEW`를 실행하려면 다음과 같이 `CREATE` 권한을 부여해야 합니다.

```sql
GRANT CREATE ON machbasedb TO user1;
```

### 사용자 생성 시 기본 권한

사용자를 생성하면 기본적으로 다음 권한을 가집니다.

- `SELECT`
- `INSERT`
- `DELETE`
- `UPDATE`
- `CREATE`
- `DROP`

다음 권한은 기본 권한에 포함되지 않으므로 필요할 때 명시적으로 부여해야 합니다.

- `ALTER`
- `MOUNT`
- `BACKUP`

### 권한과 테이블 유형 제약은 별개

권한이 있어도 테이블 유형 자체의 제약은 그대로 적용됩니다.

- `LOG`, `TAG` 테이블은 제품 특성상 `UPDATE`를 사용할 수 없습니다.
- `VOLATILE`, `LOOKUP` 테이블은 모든 DML을 사용할 수 있지만, 조회/수정/삭제 시 `WHERE` 절은 기본키 기반으로 작성해야 합니다.

즉, 권한을 부여한다고 해서 지원하지 않는 DML이 가능해지는 것은 아닙니다.

### 자주 사용하는 권한 부여 예제

```sql
-- 특정 테이블 조회만 허용
GRANT SELECT ON sys.sensor_log TO reader;

-- 특정 테이블 조회와 입력 허용
GRANT SELECT, INSERT ON sys.sensor_log TO writer;

-- 일반 사용자에게 DDL만 허용
GRANT DDL ON machbasedb TO deploy_user;

-- ALTER SYSTEM 허용
GRANT ALTER ON machbasedb TO ops_user;

-- 백업 허용
GRANT BACKUP ON machbasedb TO backup_user;

-- 마운트/언마운트 허용
GRANT MOUNT ON machbasedb TO mount_user;
```


## Managing User Example

위 쿼리의 예제와 결과입니다.

```
############################################
## SYS 계정으로 연결
############################################
Mach> create user demo identified by 'demo';
Created successfully.

Mach> drop user demo;
Dropped successfully.

Mach> create user demo1 identified by 'demo1';
Created successfully.

Mach> create user demo2 identified by 'demo2';
Created successfully.

Mach> alter user demo2 identified by 'demo22';
Altered successfully.

Mach> create table demo1_table (id integer);
Created successfully.

Mach> create bitmap index demo1_table_index1 on demo1_table(id);
Created successfully.

Mach> insert into demo1_table values(99991);
1 row(s) inserted.

Mach> insert into demo1_table values(99992);
1 row(s) inserted.

Mach> insert into demo1_table values(99993);
1 row(s) inserted.

Mach> select * from demo1_table;
ID
--------------
99993
99992
99991
[3] row(s) selected.

#Error: 연결된 사용자는 삭제할 수 없습니다.
Mach> drop user SYS;
[ERR-02083 : Drop user error. You cannot drop yourself(SYS).]

############################################
## DEMO1 연결
############################################
Mach> connect demo1/demo1;
Connected successfully.

#Error: 다른 사용자의 계정 비밀번호를 변경할 수 없습니다
Mach> alter user demo2 identified by 'demo22';
[ERR-02085 : ALTER user error. The user(DEMO2) does not have ALTER privileges.]

Mach> alter user demo1 identified by demo11;
Altered successfully.

#Error: 잘못된 비밀번호
Mach> connect demo1/demo11234;
[ERR-02081 : User authentication error. Invalid password (DEMO11234).]

## 올바른 비밀번호
Mach> connect demo1/demo11;
Connected successfully.

Mach> create table demo1_table (id integer);
Created successfully.

Mach> create bitmap index demo1_table_index1 on demo1_table(id);
Created successfully.

Mach> insert into demo1_table values(1);
1 row(s) inserted.

Mach> insert into demo1_table values(2);
1 row(s) inserted.

Mach> insert into demo1_table values(3);
1 row(s) inserted.

Mach> select * from demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.

Mach> select * from demo1.demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.

############################################
## SYS로 다시 연결
############################################
Mach> connect SYS/MANAGER;
Connected successfully.

Mach> select * from demo1_table;
ID
--------------
99993
99992
99991
[3] row(s) selected.

Mach> select * from demo1.demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.

Mach> drop user demo1;
[ERR-02084 : DROP user error. The user's tables still exist. Drop those tables first.]

Mach> connect demo1/demo11;
Connected successfully.

Mach> drop table demo1_table;
Dropped successfully.

Mach> connect SYS/MANAGER;
Connected successfully.

Mach> drop user demo1;
Dropped successfully.
```

## sys-session-manage


# 목차

* [ALTER SYSTEM](#alter-system)
    * [KILL SESSION](#kill-session)
    * [CANCEL SESSION](#cancel-session)
    * [CHECK DISK_USAGE](#check-disk_usage)
    * [INSTALL LICENSE](#install-license)
    * [INSTALL LICENSE (PATH)](#install-license-path)
    * [SET](#set)
    * [SET PVO CACHE](#set-pvo-cache)
    * [FLUSH PVO_CACHE](#flush-pvo_cache)
* [ALTER SESSION](#alter-session)
    * [SET SQL_LOGGING](#set-sql_logging)
    * [SET DEFAULT_DATE_FORMAT](#set-default_date_format)
    * [SET SHOW_HIDDEN_COLS](#set-show_hidden_cols)
    * [SET FEEDBACK_APPEND_ERROR](#set-feedback_append_error)
    * [SET MAX_QPX_MEM](#set-max_qpx_mem)
    * [SET SESSION_IDLE_TIMEOUT_SEC](#set-session_idle_timeout_sec)
    * [SET QUERY_TIMEOUT](#set-query_timeout)


## ALTER SYSTEM

시스템 전역 자원을 관리하거나 설정을 변경할 때 사용하는 구문입니다.

> **참고**: Machbase 8.5 이상에서는 일반 사용자가 `ALTER SYSTEM`을 실행하려면 `GRANT ALTER ON machbasedb TO user_name;` 형태의 권한이 필요합니다. 자세한 내용은 [사용자 관리](/dbms/reference/sql/#grantrevoke)의 `GRANT/REVOKE`를 참고하세요.

### KILL SESSION

**alter_system_kill_session_stmt:**

![alter_system_kill_session_stmt](/images/sql/sys/alter_system_kill_session_stmt.png)

```sql
alter_system_kill_session_stmt: 'ALTER SYSTEM KILL SESSION' number
```

세션 ID를 지정해 해당 세션을 강제로 종료합니다.

- SYS 사용자만 실행할 수 있으며, 자신의 세션이나 권한이 없는 세션을 대상으로 하면 `[ERR-03025: Not enough privileges to manipulate the session. (<sid>)]`가 반환됩니다.
- 세션 ID가 없으면 `ERR_MM_SESSION_ID_NOT_FOUND` 오류가 반환됩니다.
- 연결을 즉시 끊어야 할 때 사용합니다. 대상 세션의 접속이 종료되고 실행 중인 트랜잭션은 롤백됩니다.

예시
```sql
-- SYS 계정에서 확인 후 종료
SELECT id, user_id, client_type FROM v$session;
ALTER SYSTEM KILL SESSION 12;
```

### CANCEL SESSION

**alter_system_cancel_session_stmt:**

![alter_system_cancel_session_stmt](/images/sql/sys/alter_system_cancel_session_stmt.png)

```sql
alter_system_cancel_session_stmt ::= 'ALTER SYSTEM CANCEL SESSION' number
```

세션 ID를 지정해 해당 세션에서 수행 중인 작업을 취소합니다.

- 연결을 끊지 않고 현재 실행 중인 SQL만 중단합니다. 대상 세션에서는 `[ERR-03027: This statement has been canceled.]` 오류가 발생합니다.
- 같은 사용자 또는 SYS만 취소할 수 있습니다. 다른 사용자가 취소하면 `[ERR-03026: You should log in with the same user name in the target session. Now (<me>) Target(<them>)]`를 반환합니다.
- 자기 자신의 세션을 취소하려 하면 `[ERR-03025: Not enough privileges to manipulate the session. (<sid>)]`가 반환됩니다.
- 세션 ID가 없으면 `ERR_MM_SESSION_ID_NOT_FOUND` 오류가 반환됩니다.

예시
```sql
-- 세션 A: 대상 SID 확인
SELECT id, user_id, client_type FROM v$session;

-- 세션 B (같은 사용자 또는 SYS): 실행 중인 문장만 취소
ALTER SYSTEM CANCEL SESSION 6;
```

### CHECK DISK_USAGE

**alter_system_check_disk_stmt:**

![alter_system_check_disk_stmt](/images/sql/sys/alter_system_check_disk_stmt.png)

```sql
alter_system_check_disk_stmt ::= 'ALTER SYSTEM CHECK DISK_USAGE'
```

V$STORAGE에서 로그 테이블의 디스크 사용량을 나타내는 `DC_TABLE_FILE_SIZE` 값을 재계산합니다.

프로세스 장애나 정전이 발생하면 디스크 사용량이 부정확해질 수 있습니다. 이 명령은 파일 시스템에서 값을 다시 읽어 정확한 사용량을 반영하지만, 파일 시스템에 부담을 줄 수 있으므로 필요할 때만 사용해야 합니다.

### INSTALL LICENSE

**alter_system_install_license_stmt:**

![alter_system_install_license_stmt](/images/sql/sys/alter_system_install_license_stmt.png)

```sql
alter_system_install_license_stmt ::= 'ALTER SYSTEM INSTALL LICENSE'
```

라이선스 파일을 기본 경로(`$MACHBASE_HOME/conf/license.dat`)에 설치합니다.

설치 전 라이선스 적합성을 검증하며, 검증에 성공하면 설치가 완료됩니다.

### INSTALL LICENSE (PATH)

**alter_system_install_license_path_stmt:**

![alter_system_install_license_path_stmt](/images/sql/sys/alter_system_install_license_path_stmt.png)

```sql
alter_system_install_license_path_stmt: ::= 'ALTER SYSTEM INSTALL LICENSE' '=' "'" path "'"
```

지정한 경로에 라이선스 파일을 설치합니다.

경로에 파일이 없거나 손상된 라이선스 파일을 지정하면 오류가 발생합니다. 경로는 절대 경로여야 하며, 설치 전 라이선스 적합성을 검증합니다.

### SET

**alter_system_set_stmt:**

![alter_system_set_stmt](/images/sql/sys/alter_system_set_stmt.png)

```sql
alter_system_set_stmt ::= 'ALTER SYSTEM SET' prop_name '=' value
```

변경 가능한 속성 목록은 다음과 같습니다.
* QUERY_PARALLEL_FACTOR
* DEFAULT_DATE_FORMAT
* TRACE_LOG_LEVEL
* DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE
* MAX_SESSION_COUNT
* SESSION_IDLE_TIMEOUT_SEC
* PROCESS_MAX_SIZE
* TAG_CACHE_MAX_MEMORY_SIZE

숫자 속성에 대해서는 확장 표현식을 지원합니다.

지원 구문
- 직접 대입(숫자 또는 문자열):
  - `ALTER SYSTEM SET <name> = <value>;`
- 플래그 추가(비트 OR):
  - `ALTER SYSTEM SET <name> = <name> | <number>;`
  - `ALTER SYSTEM SET <name> = <number> | <name>;`
- 플래그 제거(비트 AND + NOT):
  - `ALTER SYSTEM SET <name> = <name> & ~<number>;`
  - `ALTER SYSTEM SET <name> = ~<number> & <name>;`

리터럴 규칙
- `<number>`는 10진수(`123`) 또는 16진수(`0x7B`, `0X7B`)를 허용합니다.
- 비트 연산 표현식은 숫자 속성에만 허용됩니다. 비숫자 속성에는 오류가 발생합니다.
- `0xABCD` 같은 문자열 리터럴을 설정하려면 따옴표를 사용합니다.
  - `ALTER SYSTEM SET <name> = '0xABCD';`

주의사항
- 비트 연산 표현식에서 사용하는 속성 이름은 좌변과 동일해야 합니다.
- 기존 비표현식 동작은 변경되지 않습니다.

예시
```sql
-- TRACE_LOG_LEVEL을 16진수로 설정
ALTER SYSTEM SET TRACE_LOG_LEVEL=0x00000003;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

-- 플래그 추가(비트 OR)
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL | 0x00000004;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = 0x00000008 | TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = 16 | TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

-- 플래그 제거(비트 AND + NOT)
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL & ~0x00000001;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = ~0x00000002 & TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = ~4 & TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

-- 비숫자 속성은 비트 연산 표현식에 사용할 수 없음(오류)
ALTER SYSTEM SET TRACE_LOG_LEVEL = 1 | DEFAULT_DATE_FORMAT;
ALTER SYSTEM SET DEFAULT_DATE_FORMAT = DEFAULT_DATE_FORMAT | 1;

-- 10진수 직접 대입
ALTER SYSTEM SET TRACE_LOG_LEVEL=277;
```

### SET PVO CACHE

Standard 에디션에서만 동작하는 글로벌 PVO Statement Cache 관련 속성을 런타임에 조정합니다. `PVO_CACHE_ENABLE`, `PVO_CACHE_MAX_MEMORY_SIZE`, `PVO_CACHE_MAX_PLANS_PER_SQL`, `PVO_CACHE_MAX_SQL_ENTRIES`는 즉시 반영되며, `PVO_CACHE_SHARD_COUNT`는 초기화 시점 값으로 서버 재시작이 필요합니다. 메모리·엔트리 한도는 샤드 수에 따라 분배되어 적용됩니다.

```sql
ALTER SYSTEM SET PVO_CACHE_ENABLE = 1;
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 268435456;
ALTER SYSTEM SET PVO_CACHE_MAX_PLANS_PER_SQL = 512;
ALTER SYSTEM SET PVO_CACHE_MAX_SQL_ENTRIES = 0;
```

### FLUSH PVO_CACHE

PVO Statement Cache만 비웁니다. Result Cache와는 독립적으로 동작하며, DDL이 성공적으로 실행될 때도 내부적으로 PVO 캐시가 flush 됩니다.

```sql
ALTER SYSTEM FLUSH PVO_CACHE;
```


## ALTER SESSION

개별 세션 단위로 자원을 관리하거나 설정을 변경할 때 사용하는 구문입니다.

### SET SQL_LOGGING

**alter_session_sql_logging_stmt:**

![alter_session_sql_logging_stmt](/images/sql/sys/alter_session_sql_logging_stmt.png)

```sql
alter_session_sql_logging_stmt ::= 'ALTER SESSION SET SQL_LOGGING' '=' flag
```

세션의 트레이스 로그에 메시지를 남길지 여부를 지정합니다.

다음과 같은 비트 플래그 값을 사용할 수 있습니다.
* 0x1: 파싱·검증·최적화 단계 로그
* 0x2: DDL 수행 결과 로그

따라서 값이 2이면 DDL 로그만 기록되고, 값이 3이면 오류와 DDL 로그가 함께 기록됩니다.
아래는 세션의 로깅 플래그를 변경해 오류 로그를 남기는 예시입니다.

```sql
Mach> alter session set SQL_LOGGING=1;
Altered successfully.
Mach> exit
```

### SET DEFAULT_DATE_FORMAT

**alter_session_set_defalut_dateformat_stmt:**

![alter_session_set_defalut_dateformat_stmt](/images/sql/sys/alter_session_set_defalut_dateformat_stmt.png)

```sql
alter_session_set_defalut_dateformat_stmt ::= 'ALTER SESSION SET DEFAULT_DATE_FORMAT' '=' date_format
```
Sets the default format for Datetime data types for this session.

서버가 시작되면 시스템 속성 **DEFAULT_DATE_FORMAT** 값이 각 세션에도 설정됩니다.
속성을 변경하지 않았다면 세션 기본값은 `"YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"`입니다.
이 구문을 사용하면 시스템 전체 설정과 무관하게 특정 세션의 날짜 형식을 변경할 수 있습니다.
각 세션에 설정된 기본 날짜 형식은 V$SESSION에서 확인 가능합니다. 아래는 값을 조회하고 변경하는 예시입니다.

```sql
Mach> CREATE TABLE time_table (time datetime);
Created successfully.

Mach> SELECT DEFAULT_DATE_FORMAT from v$session;
default_date_format
-----------------------------------------------
YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn
[1] row(s) selected.

Mach> INSERT INTO time_table VALUES(TO_DATE('2016/11/12'));
[ERR-00300: Invalid date value.(2016/11/12)]

Mach> ALTER SESSION SET DEFAULT_DATE_FORMAT='YYYY/MM/DD';
Altered successfully.

Mach> SELECT DEFAULT_DATE_FORMAT from v$session;

default_date_format
----------------------------------------------
YYYY/MM/DD
[1] row(s) selected.

Mach> INSERT INTO time_table VALUES(TO_DATE('2016/11/12'));
1 row(s) inserted.

Mach> SELECT * FROM time_table;

TIME
----------------------------------
2016/11/12

[1] row(s) selected.
```

### SET SHOW_HIDDEN_COLS

**alter_session_set_hidden_column_stmt:**

![alter_session_set_hidden_column_stmt](/images/sql/sys/alter_session_set_hidden_column_stmt.png)

```sql
alter_session_set_hidden_column_stmt ::= 'ALTER SESSION SET SHOW_HIDDEN_COLS' '=' ( '0' | '1' )
```

세션에서 `SELECT *`를 실행할 때 숨김 컬럼(`_arrival_time`)을 함께 출력할지 결정합니다.

서버가 시작되면 전역 속성 SHOW_HIDDEN_COLS 값이 각 세션에 0으로 설정됩니다.
세션 기본 동작을 바꾸고 싶다면 이 값을 1로 변경하면 됩니다.
각 세션의 SHOW_HIDDEN_COLS 값은 V$SESSION에서 확인할 수 있습니다.


```sql
Mach> SELECT * FROM  v$session;
ID                   CLOSED      USER_ID     LOGIN_TIME                      SQL_LOGGING SHOW_HIDDEN_COLS
-----------------------------------------------------------------------------------------------------------------
DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE
------------------------------------------------------------------------------------------------------
1                    0           1           2015-04-29 17:23:56 248:263:000 3           0
YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011
[1] row(s) selected.
Mach> ALTER SESSION SET SHOW_HIDDEN_COLS=1;
Altered successfully.
Mach> SELECT * FROM v$session;
_ARRIVAL_TIME                   ID                   CLOSED      USER_ID     LOGIN_TIME                      SQL_LOGGING
--------------------------------------------------------------------------------------------------------------------------------
SHOW_HIDDEN_COLS DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE
------------------------------------------------------------------------------------------------------------------------
1970-01-01 09:00:00 000:000:000 1                    0           1           2015-04-29 17:23:56 248:263:000 3
1           YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011
[1] row(s) selected.
```

### SET FEEDBACK_APPEND_ERROR

**alter_session_set_feedback_append_err_stmt:**

![alter_session_set_feedback_append_err_stmt](/images/sql/sys/alter_session_set_feedback_append_err_stmt.png)

```sql
alter_session_set_feedback_append_err_stmt ::= 'ALTER SESSION SET FEEDBACK_APPEND_ERROR' '=' ( '0' | '1' )
```

세션에서 발생한 Append 에러 메시지를 클라이언트 프로그램으로 전달할지 여부를 설정합니다.

값은 다음과 같습니다.
* 0 = 에러 메시지를 보내지 않음
* 1 = 에러 메시지를 전송

아래는 사용 예시입니다.

```sql
mach> ALTER SESSION SET FEEDBACK_APPEND_ERROR=0;
Altered successfully.
```

### SET MAX_QPX_MEM

**alter_session_set_max_qpx_mem_stmt:**

![alter_session_set_max_qpx_mem_stmt](/images/sql/sys/alter_session_set_max_qpx_mem_stmt.png)

```sql
alter_session_set_max_qpx_mem_stmt ::= 'ALTER SESSION SET MAX_QPX_MEM' '=' value
```

세션에서 실행되는 단일 SQL이 GROUP BY, DISTINCT, ORDER BY 연산을 수행할 때 사용할 수 있는 최대 메모리를 지정합니다.

설정한 한도를 초과해 메모리를 할당하려고 하면 SQL 실행이 중단되고 오류로 처리됩니다.
오류 발생 시 쿼리를 포함한 오류 코드와 메시지가 `machbase.trc`에 기록됩니다.

```sql
Mach> ALTER SESSION SET MAX_QPX_MEM=1073741824;
Altered successfully.

Mach> SELECT * FROM v$session;
ID                   CLOSED      USER_ID     LOGIN_TIME                      CLIENT_TYPE
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
USER_NAME                                                                         USER_IP                                                                           SQL_LOGGING SHOW_HIDDEN_COLS
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FEEDBACK_APPEND_ERROR DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE MAX_QPX_MEM          RS_CACHE_ENABLE      RS_CACHE_TIME_BOUND_MSEC
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
RS_CACHE_MAX_MEMORY_PER_QUERY RS_CACHE_MAX_RECORD_PER_QUERY RS_CACHE_APPROXIMATE_RESULT_ENABLE IDLE_TIMEOUT         QUERY_TIMEOUT
-----------------------------------------------------------------------------------------------------------------------------------------------
14                   0           1           2021-03-08 16:33:01 503:181:809 CLI
NULL                                                                              192.168.0.194                                                                     11          0
1                     YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011            1073741824           1                    1000
16777216                      50000                         0                                  0                    0
[1] row(s) selected.
Elapsed time: 0.001
```

- SQL 문이 최대 메모리를 초과했을 때의 trc 로그 예시

```sql
[2021-03-08 16:36:32 P-69000 T-140515328653056][INFO] DML FAILURE (2E10000084:Memory allocation error (alloc'd: 1048595, max: 1048576).)
```

- SQL 문이 최대 메모리를 초과했을 때 machsql 에러 메시지 예시

```sql
Mach> select * from tag order by value DESC, time ASC;
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
[ERR-00132: Memory allocation error (alloc'd: 1048595, max: 1048576).]
[0] row(s) selected.
Elapsed time: 0.447
```

### SET SESSION_IDLE_TIMEOUT_SEC

**alter_session_set_session_idle_timeout_sec_stmt:**

![alter_session_set_session_idle_timeout_sec_stmt](/images/sql/sys/alter_session_set_session_idle_timeout_sec_stmt.png)

```sql
alter_session_set_session_idle_timeout_sec_stmt ::= 'ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC' '=' value
```

세션이 유휴 상태일 때 연결을 유지할 최대 시간을 지정합니다.
초 단위로 설정하며, 지정한 시간이 지나면 해당 세션이 종료됩니다.
설정된 유휴 제한 시간은 V$SESSION에서 확인할 수 있습니다.

```sql
Mach> ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC=200;
Altered successfully.


Mach> SELECT IDLE_TIMEOUT FROM V$SESSION;
IDLE_TIMEOUT
-----------------------
200
[1] row(s) selected.
```

### SET QUERY_TIMEOUT

**alter_session_set_query_timeout_stmt:**

![alter_session_set_query_timeout_stmt](/images/sql/sys/alter_session_set_query_timeout_stmt.png)

```sql
alter_session_set_query_timeout_stmt ::= 'ALTER SESSION SET QUERY_TIMEOUT' '=' value
```

세션에서 쿼리를 실행할 때 서버 응답을 기다리는 최대 시간을 지정합니다.
초 단위로 설정하며, 지정한 시간을 초과하면 쿼리가 자동으로 중단됩니다.
세션에 설정된 QUERY_TIMEOUT 값은 V$SESSION에서 확인할 수 있습니다.

```sql
Mach> ALTER SESSION SET QUERY_TIMEOUT=200;
Altered successfully.

Mach> SELECT QUERY_TIMEOUT FROM V$SESSION;
QUERY_TIMEOUT
-----------------------
200
[1] row(s) selected.
```

## view


## 목차

* [저장 VIEW란?](#저장-view란)
* [Machbase에서 VIEW를 쓰는 이유](#machbase에서-view를-쓰는-이유)
* [기본 문법](#기본-문법)
* [기본 사용 예제](#기본-사용-예제)
* [컬럼 이름 결정 규칙](#컬럼-이름-결정-규칙)
* [지원되는 VIEW 형태](#지원되는-view-형태)
* [Machbase 특화 사용 예제](#machbase-특화-사용-예제)
* [메타 확인과 운영 점검](#메타-확인과-운영-점검)
* [성능과 제한](#성능과-제한)
* [자주 실패하는 사례](#자주-실패하는-사례)

## 저장 VIEW란?

이 문서에서 설명하는 VIEW는 `FROM (SELECT ...)` 형태의 인라인 뷰가 아니라,
`CREATE VIEW`로 저장해 두고 반복해서 사용하는 **저장 VIEW**입니다.

VIEW는 `SELECT` 결과를 이름 있는 논리 객체로 저장해 재사용하는 기능입니다.

* VIEW는 데이터를 별도로 저장하지 않습니다.
* 조회 시 저장된 VIEW 정의 SQL이 내부적으로 다시 전개되어 실행됩니다.
* 테이블처럼 `SELECT` 대상이 될 수 있지만, 물리 테이블을 대신 저장하는 기능은 아닙니다.
* 현재 문서 범위에서 확인된 사용 방식은 `CREATE VIEW`, `DROP VIEW`, `SELECT`,
  `DESC`, `SHOW VIEWS`, `M$SYS_VIEWS`, `EXPLAIN`입니다.

즉, VIEW는 "데이터를 복사해서 보관하는 기능"이 아니라, 자주 사용하는 조회식을
이름으로 고정해 재사용하는 기능으로 이해하면 됩니다.

## Machbase에서 VIEW를 쓰는 이유

Machbase에서 VIEW는 다음과 같은 상황에 특히 유용합니다.

* 반복해서 사용하는 조회 SQL을 간단한 이름으로 고정하고 싶을 때
* 복잡한 `JOIN`, `GROUP BY`, `CASE`, `UNION ALL`을 여러 곳에서 재사용하고 싶을 때
* Tag 테이블의 `BINARY` 컬럼을 `extract_*()` 함수로 해석한 결과를 논리 컬럼처럼
  노출하고 싶을 때
* 운영 중 `SHOW VIEWS`, `DESC`, `M$SYS_VIEWS`, `EXPLAIN`으로 메타 정보와 실행 계획을
  함께 확인하고 싶을 때

Machbase의 테이블 특성은 VIEW 위에서도 그대로 중요합니다.

* Lookup / Volatile 테이블 기반 VIEW는 원본 테이블의 기본 키 조건이 여전히 중요합니다.
* Tag 테이블 기반 VIEW는 `name`, `time` 조건과 `EXPLAIN` 결과를 함께 보는 것이 좋습니다.
* VIEW는 원본 테이블의 인덱스와 optimizer 판단을 이용하므로, 성능은 원본 조회식의
  영향을 그대로 받습니다.

## 기본 문법

### VIEW 생성

```sql
CREATE VIEW view_name AS
SELECT ...
FROM ...;
```

```sql
CREATE VIEW view_name (col1, col2, ...) AS
SELECT ...
FROM ...;
```

```sql
CREATE OR REPLACE VIEW view_name AS
SELECT ...
FROM ...;
```

* `view_name`은 `db.user.view_name` 형태의 schema-qualified 이름도 사용할 수 있습니다.
* `CREATE OR REPLACE VIEW`는 기존 VIEW 정의를 교체합니다.
* 같은 이름의 객체가 이미 table 등 VIEW가 아닌 객체이면 교체되지 않고 에러를 반환합니다.
* 현재 검증된 구현에서는 `CREATE OR REPLACE VIEW` 후에도 같은 object id를 유지합니다.
* 교체용 새 정의의 검증에 실패하면 기존 VIEW 정의는 그대로 유지됩니다.

### VIEW 삭제

```sql
DROP VIEW view_name;
DROP VIEW IF EXISTS view_name;
```

* `DROP VIEW IF EXISTS`는 대상이 없어도 통과합니다.
* 다른 VIEW가 해당 VIEW를 참조하고 있으면 `DROP VIEW`는 차단됩니다.
* `DROP TABLE view_name`으로 VIEW를 삭제할 수는 없습니다.

### 메타 확인

```sql
SHOW VIEWS;
DESC view_name;

SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS;
```

## 기본 사용 예제

다음 예제는 가장 단순한 Lookup 기반 VIEW입니다.

```sql
CREATE LOOKUP TABLE customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR(20),
    city VARCHAR(20),
    amount INTEGER
);

CREATE VIEW v_customer AS
SELECT id, name, city, amount
FROM customer;

SELECT name, city
FROM v_customer
WHERE id = 100;
```

컬럼 이름을 명시하고 싶다면 컬럼 리스트를 함께 줄 수 있습니다.

```sql
CREATE VIEW v_customer_short (cust_id, cust_name) AS
SELECT id, name
FROM customer;

SELECT cust_id, cust_name
FROM v_customer_short
WHERE cust_id = 100;
```

기존 VIEW 정의를 바꿀 때는 `CREATE OR REPLACE VIEW`를 사용합니다.

```sql
CREATE VIEW v_customer_amount AS
SELECT id, amount
FROM customer;

CREATE OR REPLACE VIEW v_customer_amount AS
SELECT id, amount * 10 AS amount
FROM customer
WHERE id <= 10;
```

## 컬럼 이름 결정 규칙

### 명시 컬럼 리스트를 준 경우

```sql
CREATE VIEW v_sales (sales_id, sales_name) AS
SELECT id, name
FROM t_sales;
```

이 경우 VIEW의 공식 컬럼명은 `sales_id`, `sales_name`입니다.

### 명시 컬럼 리스트를 생략한 경우

컬럼명은 다음 순서로 결정됩니다.

1. `SELECT` alias
2. 단일 컬럼 참조의 원본 컬럼명
3. 그 외 표현식은 자동 생성 이름(`EXPR1`, `EXPR2`, ...)

```sql
CREATE VIEW v_expr AS
SELECT id,
       name AS user_name,
       val + 10
FROM t1;
```

위 예제의 결과 컬럼명은 `ID`, `USER_NAME`, `EXPR3` 형태가 됩니다.

### `UNION ALL` VIEW의 컬럼명

`UNION ALL` VIEW는 가장 왼쪽 `SELECT`의 target 이름을 따릅니다.

```sql
CREATE VIEW v_union AS
SELECT id FROM t1
UNION ALL
SELECT id FROM t2;
```

따라서 `DESC v_union`에서는 `ID`가 보이고, `SELECT id FROM v_union`도 정상 동작합니다.

## 지원되는 VIEW 형태

현재 검증된 VIEW 형태는 다음과 같습니다.

* 단순 projection과 predicate
* expression, 함수, 상수, `CASE`
* `JOIN`
* subquery 포함 VIEW
* nested VIEW
* `GROUP BY`, `HAVING`
* `DISTINCT`
* `UNION ALL`

예를 들면 다음과 같은 VIEW가 모두 현재 구현 범위에서 검증되었습니다.

```sql
CREATE VIEW v_expr_case AS
SELECT id,
       CASE WHEN amount >= 100 THEN 'VIP' ELSE 'NORMAL' END AS grade,
       UPPER(city) AS city_upper
FROM customer;
```

```sql
CREATE VIEW v_city_sum AS
SELECT city, SUM(amount) AS total_amount
FROM customer
GROUP BY city
HAVING SUM(amount) >= 100;
```

```sql
CREATE VIEW v_union AS
SELECT id FROM customer WHERE city = 'SEOUL'
UNION ALL
SELECT id FROM customer WHERE city = 'BUSAN';
```

```sql
CREATE VIEW v_nested AS
SELECT id, total_amount
FROM v_city_sum
JOIN (
    SELECT city AS city_name, COUNT(*) AS city_cnt
    FROM customer
    GROUP BY city
) x
ON v_city_sum.city = x.city_name;
```

## Machbase 특화 사용 예제

### Tag / BINARY 컬럼 해석

Tag 테이블의 `BINARY` 컬럼을 해석해 논리 컬럼처럼 사용하는 것은 Machbase에서
실제 활용도가 높은 VIEW 패턴입니다.

```sql
CREATE TAG TABLE dam (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    frame BINARY(16)
);

CREATE VIEW damdata AS
SELECT name,
       time,
       extract_bit(frame, 0) AS bit0,
       extract_ulong(frame, 0, 16) AS u16,
       extract_long(frame, 0, 16) AS s16,
       extract_float(frame, 0) AS f32,
       extract_scaled_double(frame, 0, 12, 0, 0.5, 0.5) AS sd12
FROM dam;
```

```sql
SELECT name, time, bit0, u16, s16, f32, sd12
FROM damdata
WHERE name = 'main'
  AND time >= TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND time <  TO_DATE('2024-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time;
```

이 경우에도 성능 확인은 원본 Tag 테이블과 마찬가지로 `name`, `time` 조건과
`EXPLAIN` 결과를 함께 보는 것이 좋습니다.

### 스키마와 인용부호 이름

VIEW 이름은 schema-qualified 이름과 quoted identifier를 모두 사용할 수 있습니다.

```sql
CREATE VIEW machbasedb.sys.v_local AS
SELECT id, val
FROM other_user.v_src
WHERE id >= 2;

CREATE VIEW "V_QUOTED" AS
SELECT id, val
FROM t1;

CREATE VIEW v_dep AS
SELECT id
FROM "V_QUOTED"
WHERE val >= 20;
```

* 같은 이름의 VIEW가 서로 다른 schema에 있어도 schema-qualified 이름으로 구분됩니다.
* quoted VIEW를 참조하는 dependent VIEW가 있으면 `DROP VIEW`는 차단됩니다.

## 메타 확인과 운영 점검

### `SHOW VIEWS`

`SHOW VIEWS`는 현재 사용자가 볼 수 있는 VIEW 목록과 정의 SQL을 함께 보여줍니다.

출력 컬럼은 다음과 같습니다.

* `USER_NAME`
* `DB_NAME`
* `VIEW_NAME`
* `VIEW_SQL`

```sql
SHOW VIEWS;
```

### `M$SYS_VIEWS`

`M$SYS_VIEWS`는 VIEW 정의 SQL을 확인하는 공개 메타 인터페이스입니다.

```sql
SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS
WHERE VIEW_NAME = 'V_CUSTOMER';
```

다음과 같은 상황에서 유용합니다.

* VIEW 목록 확인
* 특정 VIEW의 정의 SQL 확인
* `CREATE OR REPLACE VIEW` 후 정의 변경 여부 확인

### `DESC`, `M$SYS_TABLES`, `M$SYS_COLUMNS`

```sql
DESC v_customer;

SELECT ID, NAME, TYPE
FROM M$SYS_TABLES
WHERE TYPE = 7;

SELECT TABLE_ID, ID, NAME, TYPE, LENGTH
FROM M$SYS_COLUMNS
WHERE TABLE_ID = (
    SELECT ID
    FROM M$SYS_TABLES
    WHERE TYPE = 7
      AND NAME = 'V_CUSTOMER'
);
```

* `DESC`는 VIEW의 노출 컬럼명과 타입을 보여줍니다.
* `M$SYS_TABLES`에서는 VIEW를 `TYPE = 7`로 확인할 수 있습니다.
* `M$SYS_COLUMNS`에서는 VIEW 컬럼 구성을 확인할 수 있습니다.
* `CREATE OR REPLACE VIEW`를 수행해도 `M$SYS_TABLES.ID`는 유지되고,
  `M$SYS_VIEWS.VIEW_SQL`이 새 정의로 갱신됩니다.

### `EXPLAIN`

VIEW는 물리 데이터를 따로 갖지 않기 때문에, 실제 성능은 원본 조회식과 optimizer
판단에 좌우됩니다. 운영에서는 `EXPLAIN`으로 실행 경로를 먼저 확인하는 것이 좋습니다.

```sql
EXPLAIN
SELECT *
FROM v_customer
WHERE id = 3;
```

## 성능과 제한

### 인덱스와 predicate pushdown

다음과 같은 경우에는 원본 테이블 쪽으로 조건이 잘 내려가 인덱스를 사용할 가능성이 높습니다.

* base column을 그대로 노출한 단순 projection VIEW
* 컬럼 이름만 바꾼 VIEW
* VIEW 내부에 단순 filter가 있고, outer predicate가 base column과 직접 연결되는 경우

다음과 같은 경우에는 full scan으로 돌아갈 수 있으므로 `EXPLAIN` 확인이 중요합니다.

* `DISTINCT`가 들어간 VIEW 위의 outer predicate
* `id + 1 AS id2`처럼 계산식으로 만든 컬럼 기준 predicate

### 단순 저장 VIEW 최적화

현재 검증된 구현에서는 단순한 저장 VIEW에 대해 다음 최적화가 적용될 수 있습니다.

* outer query가 실제로 참조하는 컬럼만 남기도록 projection을 줄이는 경로
* `COUNT(*)`와 pushdown 가능한 조건 조합에서 상단 projection을 우회하는 빠른 경로

반대로 `SELECT *`, `DISTINCT`, `GROUP BY`, `HAVING`, set-op, window, join이 무거운
형태는 전체 projection 경로로 처리될 수 있습니다.

### VIEW 정의 SQL 길이 제한

현재 검증된 구현에서는 `AS` 뒤의 VIEW 정의 SQL(`SELECT` 본문)이 최대 `256KB`까지
지원됩니다.

초과 시 다음 계열 오류를 반환합니다.

```text
ERR-02010: Syntax error: near token (VIEW_SQL_TOO_LONG).
```

### 삭제와 의존성

* dependent VIEW가 있으면 `DROP VIEW`는 차단됩니다.
* 의존성 판정은 실제 참조 객체 기준으로 수행됩니다.
* 이름이 문자열 리터럴이나 alias에만 들어 있는 경우는 dependency로 취급되지 않습니다.

## 자주 실패하는 사례

### 컬럼 수 불일치

```sql
CREATE VIEW v_bad (c1, c2, c3) AS
SELECT id, val
FROM t1;
```

### 자기 자신을 직접 참조하는 재귀 VIEW

```sql
CREATE VIEW v_recursive AS
SELECT id
FROM v_recursive;
```

### 중복 컬럼명과 `_RID`

```sql
CREATE VIEW v_dup AS
SELECT id AS c1, val AS c1
FROM t1;

CREATE VIEW v_rid (_RID) AS
SELECT id
FROM t1;
```

### VIEW가 아닌 객체를 `CREATE OR REPLACE VIEW`로 덮어쓰기

```sql
CREATE OR REPLACE VIEW t1 AS
SELECT id
FROM src_t1;
```

### 예약 이름 또는 잘못된 경로 사용

```sql
CREATE VIEW v$bad AS
SELECT id
FROM t1;

CREATE VIEW _tag_bad AS
SELECT id
FROM t1;

CREATE VIEW no_such_db.sys.v_bad AS
SELECT id
FROM t1;
```

### VIEW를 `DROP TABLE`로 삭제

```sql
DROP TABLE v_customer;
```

이 경우 VIEW는 삭제되지 않으며 에러가 반환됩니다.

## 관련 문서

* [DDL](/dbms/reference/sql/#ddl)
* [SELECT](/dbms/reference/sql/#select)

## functions


## 오류 처리

|오류 유형|코드|발생 조건|
|---|---|---|
|인자 타입 오류|`ERR-02036`, `ERR-02037`|숫자 타입이 아닌 값을 넣었거나 `PI`에 인자를 전달한 경우|
|실행 오류|`ERR-02317`|`SQRT`의 음수 입력, `MOD`의 0 나누기, `LOG`의 잘못된 밑/값, `EXP`/`POWER`의 범위 초과 등|

입력이 `NULL`이면 결과도 `NULL`입니다.

## ABS

이 함수는 숫자형 컬럼에 대해 동작하며, 값을 양수로 변환하여 실수로 반환합니다.

```sql
ABS(column_expr)
```

```sql
Mach> CREATE TABLE abs_table (c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO abs_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO abs_table VALUES(2, 2.0, 'sqltest');
1 row(s) inserted.

Mach> INSERT INTO abs_table VALUES(3, 3.0, 'sqltest');
1 row(s) inserted.

Mach> SELECT ABS(c1), ABS(c2) FROM abs_table;
SELECT ABS(c1), ABS(c2) from abs_table;
ABS(c1)                     ABS(c2)
-----------------------------------------------------------
3                           3
2                           2
1                           1
[3] row(s) selected.
```


## ADD_TIME

이 함수는 주어진 datetime 컬럼에 대해 날짜 및 시간 연산을 수행합니다. 년, 월, 일, 시, 분, 초 단위의 증감 연산을 지원하며, 밀리초, 마이크로초, 나노초에 대한 연산은 지원하지 않습니다. Diff 형식은 "Year/Month/Day Hour:Minute:Second"입니다. 각 항목은 양수 또는 음수 값을 가질 수 있습니다.

```sql
ADD_TIME(column,time_diff_format)
```

```sql
Mach> CREATE TABLE add_time_table (id INTEGER, dt DATETIME);
Created successfully.

Mach> INSERT INTO  add_time_table VALUES(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(2, TO_DATE('2000-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(3, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(4, TO_DATE('2013-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(5, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(6, TO_DATE('2014-12-30 23:22:33 444:555:666'));
1 row(s) inserted.

Mach> SELECT ADD_TIME(dt, '1/0/0 0:0:0') FROM add_time_table;
ADD_TIME(dt, '1/0/0 0:0:0')
----------------------------------
2015-12-30 23:22:33 444:555:666
2015-12-30 11:22:33 444:555:666
2014-11-11 01:02:03 004:005:006
2013-11-11 01:02:03 004:005:006
2001-11-11 01:02:03 004:005:006
2000-11-11 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '0/0/0 1:1:1') FROM add_time_table;
ADD_TIME(dt, '0/0/0 1:1:1')
----------------------------------
2014-12-31 00:23:34 444:555:666
2014-12-30 12:23:34 444:555:666
2013-11-11 02:03:04 004:005:006
2012-11-11 02:03:04 004:005:006
2000-11-11 02:03:04 004:005:006
1999-11-11 02:03:04 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '1/1/1 0:0:0') FROM add_time_table;
ADD_TIME(dt, '1/1/1 0:0:0')
----------------------------------
2016-01-31 23:22:33 444:555:666
2016-01-31 11:22:33 444:555:666
2014-12-12 01:02:03 004:005:006
2013-12-12 01:02:03 004:005:006
2001-12-12 01:02:03 004:005:006
2000-12-12 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '-1/0/0 0:0:0') FROM add_time_table;
ADD_TIME(dt, '-1/0/0 0:0:0')
----------------------------------
2013-12-30 23:22:33 444:555:666
2013-12-30 11:22:33 444:555:666
2012-11-11 01:02:03 004:005:006
2011-11-11 01:02:03 004:005:006
1999-11-11 01:02:03 004:005:006
1998-11-11 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '0/0/0 -1:-1:-1') FROM add_time_table;
ADD_TIME(dt, '0/0/0 -1:-1:-1')
----------------------------------
2014-12-30 22:21:32 444:555:666
2014-12-30 10:21:32 444:555:666
2013-11-11 00:01:02 004:005:006
2012-11-11 00:01:02 004:005:006
2000-11-11 00:01:02 004:005:006
1999-11-11 00:01:02 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '-1/-1/-1 0:0:0') FROM add_time_table;
ADD_TIME(dt, '-1/-1/-1 0:0:0')
----------------------------------
2013-11-29 23:22:33 444:555:666
2013-11-29 11:22:33 444:555:666
2012-10-10 01:02:03 004:005:006
2011-10-10 01:02:03 004:005:006
1999-10-10 01:02:03 004:005:006
1998-10-10 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-1/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
[2] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-2/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
4           2013-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT ADD_TIME(TO_DATE('2000-12-01 00:00:00 000:000:001'), '-1/0/0 0:0:-1') FROM add_time_table;
ADD_TIME(TO_DATE('2000-12-01 00:00:00 000:000:001'), '-1/0/0 0:0:-1')
------------------------------------------
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
[6] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-2/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
4           2013-11-11 01:02:03 004:005:006
[3] row(s) selected.
```

## APPROX_PERCENTILE {#approx_percentile-family}

```
APPROX_PERCENTILE
APPROX_MEDIAN
APPROX_P05
APPROX_P10
APPROX_P90
APPROX_P95
```

이 함수들은 원시 값을 모두 정렬하지 않고 제한된 크기의 summary를 유지해 분위값을 근사합니다. 입력 데이터가 매우 크고, 작은 오차를 허용할 수 있을 때 유용합니다.

```sql
APPROX_PERCENTILE(value, ratio)
APPROX_MEDIAN(value)
APPROX_P05(value)
APPROX_P10(value)
APPROX_P90(value)
APPROX_P95(value)
```

- `value`는 숫자형이어야 합니다.
- `ratio`는 `0.0` 이상 `1.0` 이하의 상수여야 합니다.
- 반환 타입은 `DOUBLE`입니다.
- `NULL` 값은 무시합니다.

`APPROX_MEDIAN(value)`는 근사 중앙값이며, `APPROX_P05`, `APPROX_P10`, `APPROX_P90`, `APPROX_P95`는 자주 쓰는 분위값을 위한 축약형입니다.

```sql
SELECT APPROX_PERCENTILE(latency_ms, 0.95) AS ap95,
       APPROX_MEDIAN(latency_ms) AS amedian,
       APPROX_P05(latency_ms) AS ap05
FROM api_log;
```


## AREA {#area}

`AREA(y, x)`는 숫자형 `(x, y)` 점들로 이루어진 곡선 아래 면적을 정확하게 계산하는 집계 함수입니다.

```sql
AREA(y, x)
```

- 두 인자는 모두 숫자형이어야 합니다.
- 둘 중 하나라도 `NULL`인 행은 무시합니다.
- 유효한 점이 2개 미만이면 결과는 `NULL`입니다.
- 반환 타입은 `DOUBLE`입니다.

```sql
SELECT AREA(power_kw, sample_sec)
FROM power_log;
```


## AVG

이 함수는 숫자형 컬럼에 대해 동작하는 집계 함수로, 해당 컬럼의 평균 값을 출력합니다.

```sql
AVG(column_name)
```

```sql
Mach> CREATE TABLE avg_table (id1 INTEGER, id2 INTEGER);
Created successfully.

Mach> INSERT INTO avg_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(null, 4);
1 row(s) inserted.

Mach> SELECT id1, AVG(id2) FROM avg_table GROUP BY id1;
id1         AVG(id2)
-------------------------------------------
2                2
NULL             4
1                2
```


## BITAND / BITOR

이 함수는 두 개의 입력 값을 64비트 부호 있는 정수로 변환하고 비트 단위 AND/OR 연산의 결과를 반환합니다. 입력 값은 반드시 정수형이어야 하며, 출력 값은 64비트 부호 있는 정수입니다.

0보다 작은 정수 값의 경우, 플랫폼에 따라 다른 결과가 나올 수 있으므로 uinteger 및 ushort 타입만 사용하는 것을 권장합니다.

```sql
BITAND (<expression1>, <expression2>)
BITOR (<expression1>, <expression2>)
```

```sql
Mach> CREATE TABLE bit_table (i1 INTEGER, i2 UINTEGER, i3 FLOAT, i4 DOUBLE, i5 SHORT, i6 VARCHAR(10));
Created successfully.

Mach> INSERT INTO bit_table VALUES (-1, 1, 1, 1, 2, 'aaa');
1 row(s) inserted.

Mach> INSERT INTO bit_table VALUES (-2, 2, 2, 2, 3, 'bbb');
1 row(s) inserted.

Mach> SELECT BITAND(i1, i2) FROM bit_table;
BITAND(i1, i2)
-----------------------
2
1
[2] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i2, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
-1          1           1                           1                           2           aaa
[1] row(s) selected.

Mach> SELECT BITOR(i5, 1) FROM bit_table WHERE BITOR(i5, 1) = 3;
BITOR(i5, 1)
-----------------------
3
3
[2] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITOR(i2, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
-1          1           1                           1                           2           aaa
[1] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i3, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i4, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITAND(i5, 1) FROM bit_table WHERE BITAND(i5, 1) = 1;
BITAND(i5, 1)
-----------------------
1
[1] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITOR(i6, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITOR] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITOR(i1, i2) FROM bit_table;
BITOR(i1, i2)
-----------------------
-2
-1
[2] row(s) selected.

Mach> SELECT BITAND(i1, i3) FROM bit_table;
BITAND(i1, i3)
-----------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITOR(i1, i6) FROM bit_table;
BITOR(i1, i6)
-----------------------
[ERR-02037 : Function [BITOR] argument data type is mismatched.]
[0] row(s) selected.
```


## COUNT

이 함수는 주어진 컬럼의 레코드 개수를 구하는 집계 함수입니다.

```sql
COUNT(column_name)
```

```sql
Mach> CREATE TABLE count_table (id1 INTEGER, id2 INTEGER);
Created successfully.

Mach> INSERT INTO count_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(null, 4);
1 row(s) inserted.

Mach> SELECT COUNT(*) FROM count_table;
COUNT(*)
-----------------------
7
[1] row(s) selected.

Mach> SELECT COUNT(id1) FROM count_table;
COUNT(id1)
-----------------------
6
[1] row(s) selected.
```


## CUME_DIST {#cume_dist}

`CUME_DIST(value, threshold)`는 `value`가 `threshold` 이하인 행의 누적 비율을 반환합니다.

```sql
CUME_DIST(value, threshold)
```

- 이 함수는 윈도우 함수가 아니라 집계 함수입니다.
- 두 인자는 모두 숫자형이어야 합니다.
- `threshold`는 상수여야 합니다.
- 반환 값은 `0.0` 이상 `1.0` 이하의 `DOUBLE`입니다.

```sql
SELECT CUME_DIST(latency_ms, 100)
FROM api_log;
```


## DATE_TRUNC

이 함수는 주어진 datetime 값을 '시간 단위'와 '시간 범위'까지만 표시되는 새로운 datetime 값으로 반환합니다.

```sql
DATE_TRUNC (field, date_val [, count])
```

```sql
Mach> CREATE TABLE trunc_table (i1 INTEGER, i2 DATETIME);
Created successfully.

Mach> INSERT INTO trunc_table VALUES (1, TO_DATE('1999-11-11 1:2:0 4:5:1'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (2, TO_DATE('1999-11-11 1:2:0 5:5:2'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (3, TO_DATE('1999-11-11 1:2:1 6:5:3'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (4, TO_DATE('1999-11-11 1:2:1 7:5:4'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (5, TO_DATE('1999-11-11 1:2:2 8:5:5'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (6, TO_DATE('1999-11-11 1:2:2 9:5:6'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (7, TO_DATE('1999-11-11 1:2:3 10:5:7'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (8, TO_DATE('1999-11-11 1:2:3 11:5:8'));
1 row(s) inserted.

Mach> SELECT COUNT(*), DATE_TRUNC('second', i2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
2                    1999-11-11 01:02:00 000:000:000
2                    1999-11-11 01:02:01 000:000:000
2                    1999-11-11 01:02:02 000:000:000
2                    1999-11-11 01:02:03 000:000:000
[4] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('second', i2, 2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
4                    1999-11-11 01:02:00 000:000:000
4                    1999-11-11 01:02:02 000:000:000
[2] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('nanosecond', i2, 2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
1                    1999-11-11 01:02:00 004:005:000
1                    1999-11-11 01:02:00 005:005:002
1                    1999-11-11 01:02:01 006:005:002
1                    1999-11-11 01:02:01 007:005:004
1                    1999-11-11 01:02:02 008:005:004
1                    1999-11-11 01:02:02 009:005:006
1                    1999-11-11 01:02:03 010:005:006
1                    1999-11-11 01:02:03 011:005:008
[8] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('nsec', i2, 1000000000) tm FROM trunc_table group by tm ORDER BY 2; //Same as DATE_TRUNC('sec', i2, 1)
COUNT(*)             tm
--------------------------------------------------------
2                    1999-11-11 01:02:00 000:000:000
2                    1999-11-11 01:02:01 000:000:000
2                    1999-11-11 01:02:02 000:000:000
2                    1999-11-11 01:02:03 000:000:000
[4] row(s) selected.
```

시간 단위별로 허용되는 시간 범위는 다음과 같습니다.

* nanosecond, microsecond, milisecond 단위 및 약어는 5.5.6부터 사용 가능합니다.
* week는 일요일부터 시작합니다.

|시간 단위|시간 범위|
|--|--|
|nanosecond (nsec)|1000000000 (1 second)|
|microsecond (usec)|60000000 (60 seconds)|
|milisecond (msec)|60000 (60 seconds)|
|second (sec)|86400 (1 day)|
|minute (min)|1440 (1 day)|
|hour|24 (1 day)|
|day|1|
|week|1|
|month|1|
|year|1|

예를 들어, DATE_TRUNC('second', time, 120)을 입력하면 반환되는 값은 **2분마다** 표시되며, 이는 DATE_TRUNC('minute', time, 2)와 동일합니다.

## DATE_BIN
이 함수는 지정한 기준 시각(`origin`)을 기준으로 주어진 datetime 값을 `time unit`과
`time range`로 구간(bin) 처리합니다.

```sql
DATE_BIN(field, count, source [, origin])
```

- `origin`을 지정하면 해당 시각을 기준으로 버킷을 계산합니다.
- `origin`을 생략하면 서버 로컬 타임존의 `1970-01-01 00:00:00`을 기준으로 버킷을 계산합니다.
- `count`는 1 이상의 정수여야 합니다.

`DATE_TRUNC()` 또는 `ROLLUP()`과 같은 로컬 타임존 경계로 버킷을 맞추고 싶으면
`origin`을 생략한 3-인자 형식을 사용하면 됩니다. 반대로 서버 타임존과 무관하게 항상
동일한 경계를 사용해야 하면 4-인자 형식으로 `origin`을 명시해야 합니다.

예를 들어, 서버 타임존이 `UTC+09:00`일 때 과거에는 `DATE_BIN(..., 0)` 대신
타임존 보정이 적용된 `origin` 값을 직접 넣어야 로컬 시간 경계에 맞출 수 있었지만,
이제는 `DATE_BIN(field, count, source)`만으로 같은 효과를 얻을 수 있습니다.

```sql
Mach> CREATE TABLE log (time DATETIME);
Created successfully.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 00:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 01:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 02:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 03:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 04:00:00'));
1 row(s) inserted.

Mach> SELECT TIME, DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00')) FROM log ORDER BY time;
TIME                            DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00'))
---------------------------------------------------------------------------------------------
2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 01:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 02:00:00 000:000:000 2000-01-01 02:00:00 000:000:000
2000-01-01 03:00:00 000:000:000 2000-01-01 02:00:00 000:000:000
2000-01-01 04:00:00 000:000:000 2000-01-01 04:00:00 000:000:000
[5] row(s) selected.
```

로컬 타임존 경계를 기준으로 버킷을 계산하는 예는 다음과 같습니다.

```sql
Mach> CREATE TABLE t3521 (ts DATETIME);
Created successfully.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 00:30:00'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 02:59:59'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 03:00:00'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 08:00:00'));
1 row(s) inserted.

Mach> SELECT ts,
             DATE_BIN('hour', 3, ts) AS date_bin_3arg,
             DATE_TRUNC('hour', ts, 3) AS date_trunc_3arg
        FROM t3521
    ORDER BY ts;
ts                              date_bin_3arg                   date_trunc_3arg
----------------------------------------------------------------------------------------------------
2000-01-01 00:30:00 000:000:000 2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 02:59:59 000:000:000 2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 03:00:00 000:000:000 2000-01-01 03:00:00 000:000:000 2000-01-01 03:00:00 000:000:000
2000-01-01 08:00:00 000:000:000 2000-01-01 06:00:00 000:000:000 2000-01-01 06:00:00 000:000:000
[4] row(s) selected.
```

시간 단위별 허용 범위는 다음과 같습니다.

* nanosecond, microsecond, milisecond 단위 및 약어는 5.5.6부터 사용할 수 있습니다.
* week는 7일과 같습니다.

|시간 단위|
|----:|
|nanosecond (nsec)|
|microsecond (usec)|
|milisecond (msec)|
|second (sec)|
|minute (min)|
|hour|
|day|
|week|
|month|
|year|


## DAYOFWEEK

이 함수는 주어진 datetime 값의 요일을 나타내는 자연수를 반환합니다.

[TO_CHAR (time, 'DAY')](#to_char)와 의미적으로 동일하지만, 여기서는 정수를 반환합니다.

```sql
DAYOFWEEK(date_val)
```

반환되는 자연수는 아래 표와 같이 요일을 나타냅니다.

|반환값|요일|
|--|--|
|0|일요일|
|1|월요일|
|2|화요일|
|3|수요일|
|4|목요일|
|5|금요일|
|6|토요일|


## DECODE

이 함수는 지정한 컬럼 값을 search 값들과 비교하여 일치하면 해당 return 값을 반환합니다. 일치하는 search 값이 없으면 default 값을 반환하며, default를 생략하면 NULL을 반환합니다.

```sql
DECODE(column, [search, return],.. default)
```

```sql
Mach> CREATE TABLE decode_table (id1 VARCHAR(11));
Created successfully.

Mach> INSERT INTO decode_table VALUES('decodetest1');
1 row(s) inserted.

Mach> INSERT INTO decode_table VALUES('decodetest2');
1 row(s) inserted.

Mach> SELECT id1, DECODE(id1, 'decodetest1', 'result1', 'decodetest2', 'result2', 'DEFAULT') FROM decode_table;
id1          DECODE(id1, 'decodetest1', 'result1', 'decodetest2', 'result2', 'DEFAULT')
---------------------------------------------------------
decodetest2  result2
decodetest1  result1
[2] row(s) selected.

Mach> SELECT id1, DECODE(id1, 'codetest', 2, 99) FROM decode_table;
id1          DECODE(id1, 'codetest', 2, 99)
-----------------------------------------------
decodetest2  99
decodetest1  99
[2] row(s) selected.

Mach> SELECT DECODE(id1, 'decodetest1', 2) FROM decode_table;
DECODE(id1, 'decodetest1', 2)
--------------------------------
NULL
2
[2] row(s) selected.

Mach> SELECT DECODE(id1, 'codetest', 2) FROM decode_table;
DECODE(id1, 'codetest', 2)
-----------------------------
NULL
NULL
[2] row(s) selected.
```


## EXTRACT_*

바이너리 프레임에서 비트를 추출하는 함수 모음입니다.
`EXTRACT_*`는 빅엔디안, `EXTRACT_LE_*`는 리틀엔디안 모델을 사용합니다.
모든 함수는 `BINARY/VARBINARY`를 입력으로 받으며 frame이 NULL이면 결과도 NULL입니다.

**엔디안 모델**

- `EXTRACT_*`: MSB 우선 (`bit 0`은 `byte[0]`의 MSB)
- `EXTRACT_LE_*`: LSB 우선 (`bit 0`은 `byte[0]`의 LSB)
- 비트 인덱스는 프레임 전체 기준으로 0부터 시작합니다.

**공통 규칙**

- 단일 비트: `0 <= bit_pos < frame_bits`
- 범위 추출: `start_bit >= 0`, `1 <= bit_count <= 64`,
  `start_bit + bit_count <= frame_bits`
- `EXTRACT_FLOAT*`는 32비트, `EXTRACT_DOUBLE*`는 64비트를 읽습니다.
- signed 추출은 2의 보수(two's complement)로 해석하고 64비트로 부호 확장합니다.
- 범위 오류: `ERR_QP_INVALID_ARG_VALUE` (`ERR-02229` 계열)
- 인자 타입 오류: `ERR_QP_FUNCTION_ARG_TYPE`

### EXTRACT_BIT

```
EXTRACT_BIT(frame, bit_pos) / EXTRACT_LE_BIT(frame, bit_pos) → TINYINT
```

단일 비트를 0 또는 1로 반환합니다.

```sql
-- frame = 0x80 (1000 0000)
SELECT EXTRACT_BIT(frame, 0)    AS be_bit0,
       EXTRACT_LE_BIT(frame, 0) AS le_bit0
FROM t;
```

### EXTRACT_LONG, EXTRACT_ULONG

```
EXTRACT_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LE_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LONG(frame, start_bit, bit_count) → BIGINT
EXTRACT_LE_LONG(frame, start_bit, bit_count) → BIGINT
```

1~64비트를 부호 없는/2의 보수 정수로 읽습니다.

```sql
-- frame = 0x12 34
SELECT EXTRACT_ULONG(frame, 0, 16)    AS be_u16,  -- 0x1234
       EXTRACT_LE_ULONG(frame, 0, 16) AS le_u16   -- 0x3412
FROM t;
```

### EXTRACT_FLOAT,EXTRACT_DOUBLE

```
EXTRACT_FLOAT(frame, start_bit) → FLOAT
EXTRACT_LE_FLOAT(frame, start_bit) → FLOAT
EXTRACT_DOUBLE(frame, start_bit) → DOUBLE
EXTRACT_LE_DOUBLE(frame, start_bit) → DOUBLE
```

32/64비트를 IEEE754 float/double로 재해석하며, 지정한 비트 구간이 frame 안에
들어와야 합니다.

```sql
SELECT EXTRACT_FLOAT(frame, 0)      AS be_f32,
       EXTRACT_LE_FLOAT(frame, 0)   AS le_f32,
       EXTRACT_DOUBLE(frame, 64)    AS be_f64,
       EXTRACT_LE_DOUBLE(frame, 64) AS le_f64
FROM sensor_bin;
```

### EXTRACT_SCALED_DOUBLE

```
EXTRACT_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
EXTRACT_LE_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
```

1~64비트를 `signed=0`이면 부호 없는 값, `signed=1`이면 2의 보수 signed 값으로
읽고 `raw * scale + offset`을 반환합니다.

```sql
-- 20비트 센서값, scale 0.01, offset -40.0
SELECT EXTRACT_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0)    AS be_value,
       EXTRACT_LE_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0) AS le_value
FROM t_bin;
```


## FIRST / LAST

각 그룹에서 '기준 값'으로 정렬한 순서 기준으로 가장 앞(또는 마지막) 레코드의 특정 값을 반환하는 집계 함수입니다.

* FIRST: 정렬 순서에서 가장 앞 레코드의 값을 반환합니다.
* LAST: 정렬 순서에서 마지막 레코드의 값을 반환합니다.

```sql
FIRST(sort_expr, return_expr)
LAST(sort_expr, return_expr)
```

```sql
Mach> create table firstlast_table (id integer, name varchar(20), group_no integer);
Created successfully.
Mach> insert into firstlast_table values (1, 'John', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (2, 'Grey', 1);
1 row(s) inserted.
Mach> insert into firstlast_table values (5, 'Ryan', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (4, 'Andrew', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (7, 'Kyle', 1);
1 row(s) inserted.
Mach> insert into firstlast_table values (6, 'Ross', 1);
1 row(s) inserted.

Mach> select group_no, first(id, name) from firstlast_table group by group_no;
group_no    first(id, name)
-------------------------------------
1           Grey
0           John
[2] row(s) selected.


Mach> select group_no, last(id, name) from firstlast_table group by group_no;
group_no    last(id, name)
-------------------------------------
1           Kyle
0           Ryan
```


## FROM_UNIXTIME

정수로 입력된 32비트 UNIXTIME 값을 datetime 타입으로 변환합니다. (UNIX_TIMESTAMP는 datetime 데이터를 32비트 UNIXTIME 정수로 변환합니다.)

```sql
FROM_UNIXTIME(unix_timestamp_value)
```

```sql
Mach> SELECT FROM_UNIXTIME(315540671) FROM TEST;
FROM_UNIXTIME(315540671)
----------------------------------
1980-01-01 11:11:11 000:000:000

Mach> SELECT FROM_UNIXTIME(UNIX_TIMESTAMP('2001-01-01')) FROM unix_table;
FROM_UNIXTIME(UNIX_TIMESTAMP('2001-01-01'))
------------------------------------------
2001-01-01 00:00:00 000:000:000
```


## FROM_TIMESTAMP

1970-01-01 09:00 이후 경과한 나노초 값을 datetime 타입으로 변환합니다.

(TO_TIMESTAMP()는 datetime 타입을 1970-01-01 09:00 이후 경과 나노초 값으로 변환합니다.)

```sql
FROM_TIMESTAMP(nanosecond_time_value)
```

```sql
Mach> SELECT FROM_TIMESTAMP(1562302560007248869) FROM TEST;
FROM_TIMESTAMP(1562302560007248869)
--------------------------------------
2019-07-05 13:56:00 007:248:869
```

sysdate와 now는 현재 시각 기준 1970-01-01 09:00 이후 경과한 나노초 값을 의미하므로 FROM_TIMESTAMP()에 바로 사용할 수 있습니다.

물론 변환하지 않아도 결과는 동일합니다. sysdate/now를 나노초 단위로 연산할 때 유용합니다.

```sql
Mach> select sysdate, from_timestamp(sysdate) from test_tbl;
sysdate                         from_timestamp(sysdate)
-------------------------------------------------------------------
2019-07-05 14:00:59 722:822:443 2019-07-05 14:00:59 722:822:443
[1] row(s) selected.

Mach> select sysdate, from_timestamp(sysdate-1000000) from test_tbl;
sysdate                         from_timestamp(sysdate-1000000)
-------------------------------------------------------------------
2019-07-05 14:01:05 130:939:525 2019-07-05 14:01:05 129:939:525      -- 1 ms (1,000,000 ns) 차이가 발생함
[1] row(s) selected.
```


## GROUP_CONCAT

이 함수는 그룹 내 해당 컬럼 값들을 문자열로 이어 붙여 반환하는 집계 함수입니다.

{{< callout type="warning" >}}
이 함수는 Cluster Edition에서 사용할 수 없습니다.
{{< /callout >}}

```sql
GROUP_CONCAT(
     [DISTINCT] column
     [ORDER BY { unsigned_integer | column }
     [ASC | DESC] [, column ...]]
     [SEPARATOR str_val]
)
```

* DISTINCT: 중복 값은 한 번만 연결합니다.
* ORDER BY: 지정한 컬럼 값을 기준으로 연결 순서를 정렬합니다.
* SEPARATOR: 컬럼 값을 연결할 때 사용할 구분자 문자열입니다. 기본값은 쉼표(,)입니다.

구문 관련 주의사항은 다음과 같습니다.

* 하나의 컬럼만 지정할 수 있으며, 여러 컬럼을 붙이려면 TO_CHAR()와 CONCAT 연산자(||)로 하나의 표현식으로 만들어야 합니다.
* ORDER BY에는 연결 대상 컬럼 외의 컬럼도 지정할 수 있으며, 여러 컬럼을 지정할 수 있습니다.
* SEPARATOR에는 문자열 상수만 지정할 수 있으며, 문자열 컬럼은 지정할 수 없습니다.

```sql
Mach> CREATE TABLE concat_table(id1 INTEGER, id2 DOUBLE, name VARCHAR(10));
Created successfully.

Mach> INSERT INTO concat_table VALUES (1, 2, 'John');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (2, 1, 'Ram');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (3, 2, 'Zara');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (4, 2, 'Jill');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (5, 1, 'Jack');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (6, 1, 'Jack');
1 row(s) inserted.


Mach> SELECT GROUP_CONCAT(name) AS G_NAMES FROM concat_table GROUP BY id2;
G_NAMES
------------------------------------------------------------------------------------
Jack,Jack,Ram
Jill,Zara,John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(DISTINCT name) AS G_NAMES FROM concat_table GROUP BY Id2;
G_NAMES
------------------------------------------------------------------------------------
Jack,Ram
Jill,Zara,John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(name SEPARATOR '.') G_NAMES FROM concat_table GROUP BY Id2;
G_NAMES
------------------------------------------------------------------------------------
Jack.Jack.Ram
Jill.Zara.John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(name ORDER BY id1) G_NAMES, GROUP_CONCAT(id1 ORDER BY id1) G_SORTID FROM concat_table GROUP BY id2;
G_NAMES
------------------------------------------------------------------------------------
G_SORTID
------------------------------------------------------------------------------------
Ram,Jack,Jack
2,5,6
John,Zara,Jill
1,3,4
[2] row(s) selected.
```


## INSTR

이 함수는 대상 문자열에서 패턴 문자열이 시작하는 위치 인덱스를 반환합니다. 인덱스는 1부터 시작합니다.

* 패턴이 없으면 0을 반환합니다.
* 찾을 패턴의 길이가 0이거나 NULL이면 NULL을 반환합니다.

```sql
INSTR(target_string, pattern_string)
```

```sql
Mach> CREATE TABLE string_table(c1 VARCHAR(20));
Created successfully.

Mach> INSERT INTO string_table VALUES ('abstract');
1 row(s) inserted.

Mach> INSERT INTO string_table VALUES ('override');
1 row(s) inserted.

Mach> SELECT c1, INSTR(c1, 'act') FROM string_table;
c1                    INSTR(c1, 'act')
------------------------------------------
override              0
abstract              6
[2] row(s) selected.
```


## LEAST / GREATEST

여러 컬럼/값을 입력하면 LEAST는 최소값, GREATEST는 최대값을 반환합니다.

입력 값이 1개이거나 없으면 오류로 처리됩니다. 입력 값이 NULL이면 NULL을 반환합니다. 따라서 입력이 컬럼인 경우 함수로 미리 변환해야 합니다.
비교할 수 없는 컬럼(BLOB, TEXT 등)이 포함되거나 비교를 위한 타입 변환이 불가능하면 오류로 처리됩니다.

```sql
LEAST(value_list, value_list,...)
GREATEST(value_list, value_list,...)
```

```sql
Mach> CREATE TABLE lgtest_table(c1 INTEGER, c2 LONG, c3 VARCHAR(10), c4 VARCHAR(5));
Created successfully.

Mach> INSERT INTO lgtest_table VALUES (1, 2, 'abstract', 'ace');
1 row(s) inserted.

Mach> INSERT INTO lgtest_table VALUES (null, 100, null, 'bag');
1 row(s) inserted.

Mach> SELECT LEAST (c1, c2) FROM lgtest_table;
LEAST (c1, c2)
-----------------------
NULL
1
[2] row(s) selected.

Mach> SELECT LEAST (c1, c2, -1) FROM lgtest_table;
LEAST (c1, c2, -1)
-----------------------
NULL
-1
[2] row(s) selected.

Mach> SELECT GREATEST(c3, c4) FROM lgtest_table;
GREATEST(c3, c4)
--------------------
NULL
ace
[2] row(s) selected.

Mach> SELECT LEAST(c3, c4) FROM lgtest_table;
LEAST(c3, c4)
-----------------
NULL
abstract
[2] row(s) selected.

Mach> SELECT LEAST(NVL(c3, 'aa'), c4) FROM lgtest_table;
LEAST(NVL(c3, 'aa'), c4)
----------------------------
aa
abstract
[2] row(s) selected.
```


## LENGTH

문자열 컬럼의 길이를 반환합니다. 반환 값은 영문(ASCII) 기준 바이트 수입니다.

```sql
LENGTH(column_name)
```

```sql
Mach> CREATE TABLE length_table (id1 INTEGER, id2 DOUBLE, name VARCHAR(15));
Created successfully.

Mach> INSERT INTO length_table VALUES(1, 10, 'Around the Horn');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(NULL, 20, 'Alfreds Futterkiste');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(3, NULL, 'Antonio Moreno');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(4, 40, NULL);
1 row(s) inserted.

Mach> select * FROM length_table;
ID1         ID2                         NAME
-------------------------------------------------------------
4           40                          NULL
3           NULL                        Antonio Moreno
NULL        20                          Alfreds Futterk
1           10                          Around the Horn
[4] row(s) selected.

Mach> select id1 * 10 FROM length_table;
id1 * 10
-----------------------
40
30
NULL
10
[4] row(s) selected.

Mach> select * FROM length_table Where id1 > 1 and id2 < 50;
ID1         ID2                         NAME
-------------------------------------------------------------
4           40                          NULL
[1] row(s) selected.

Mach> select name || ' with null concat' FROM length_table;
name || ' with null concat'
------------------------------------
NULL
Antonio Moreno with null concat
Alfreds Futterk with null concat
Around the Horn with null concat
[4] row(s) selected.

Mach> select LENGTH(name) FROM length_table;
LENGTH(name)
---------------
NULL
14
15
15
[4] row(s) selected.
```


## LOWER

영문 문자열을 소문자로 변환합니다.

```sql
LOWER(column_name)
```

```sql
Mach> CREATE TABLE lower_table (name VARCHAR(20));
Created successfully.

Mach> INSERT INTO lower_table VALUES('');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('James Backley');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('Alfreds Futterkiste');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('Antonio MORENO');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES (NULL);
1 row(s) inserted.

Mach> SELECT LOWER(name) FROM lower_table;
LOWER(name)
------------------------
NULL
antonio moreno
alfreds futterkiste
james backley
NULL
[5] row(s) selected.
```


## LPAD / RPAD

입력 문자열이 지정 길이가 될 때까지 왼쪽(LPAD) 또는 오른쪽(RPAD)에 문자를 채웁니다.

마지막 파라미터 char는 생략할 수 있으며, 생략 시 공백(' ')으로 채웁니다.
입력 값이 지정 길이보다 길면 문자를 덧붙이지 않고 앞에서부터 지정 길이만큼만 반환합니다.

```sql
LPAD(str, len, padstr)
RPAD(str, len, padstr)
```

```sql
Mach> CREATE TABLE pad_table (c1 integer, c2 varchar(15));
Created successfully.

Mach> INSERT INTO pad_table VALUES (1, 'Antonio');
1 row(s) inserted.

Mach> INSERT INTO pad_table VALUES (25, 'Johnathan');
1 row(s) inserted.

Mach> INSERT INTO pad_table VALUES (30, 'M');
1 row(s) inserted.

Mach> SELECT LPAD(to_char(c1), 5, '0') FROM pad_table;
LPAD(to_char(c1), 5, '0')
-----------------------------
00030
00025
00001
[3] row(s) selected.

Mach> SELECT RPAD(to_char(c1), 5, '0') FROM pad_table;
RPAD(to_char(c1), 5, '0')
-----------------------------
30000
25000
10000
[3] row(s) selected.

Mach> SELECT LPAD(c2, 5) FROM pad_table;
LPAD(c2, 5)
---------------
    M
Johna
Anton
[3] row(s) selected.

Mach> SELECT RPAD(c2, 5) FROM pad_table;
RPAD(c2, 5)
---------------
M
Johna
Anton
[3] row(s) selected.

Mach> SELECT RPAD(c2, 10, '***') FROM pad_table;
RPAD(c2, 10, '***')
-----------------------
M*********
Johnathan*
Antonio***
[3] row(s) selected.
```


## LTRIM / RTRIM

이 함수는 첫 번째 인자에서 패턴 문자열에 포함된 문자를 제거합니다. LTRIM은 왼쪽에서 오른쪽으로, RTRIM은 오른쪽에서 왼쪽으로 패턴에 포함된 문자를 검사하며, 패턴에 없는 문자를 만날 때까지 제거합니다. 모든 문자가 패턴에 포함되어 있으면 NULL을 반환합니다.

패턴을 지정하지 않으면 공백(' ')을 기준으로 공백을 제거합니다.

```sql
LTRIM(column_name, pattern)
RTRIM(column_name, pattern)
```

```sql
Mach> CREATE TABLE trim_table1(name VARCHAR(10));
Created successfully.

Mach> INSERT INTO trim_table1 VALUES ('   smith   ');
1 row(s) inserted.

Mach> SELECT ltrim(name) FROM trim_table1;
ltrim(name)
---------------
smith
[1] row(s) selected.

Mach> SELECT rtrim(name) FROM trim_table1;
rtrim(name)
---------------
   smith
[1] row(s) selected.

Mach> SELECT ltrim(name, ' s') FROM trim_table1;
ltrim(name, ' s')
---------------------
mith
[1] row(s) selected.

Mach> SELECT rtrim(name, 'h ') FROM trim_table1;
rtrim(name, 'h ')
---------------------
   smit
[1] row(s) selected.

Mach> CREATE TABLE trim_table2 (name VARCHAR(10));
Created successfully.

Mach> INSERT INTO trim_table2 VALUES ('ddckaaadkk');
1 row(s) inserted.

Mach> SELECT ltrim(name, 'dc') FROM trim_table2;
ltrim(name, 'dc')
---------------------
kaaadkk
[1] row(s) selected.

Mach> SELECT rtrim(name, 'dk') FROM trim_table2;
rtrim(name, 'dk')
---------------------
ddckaaa
[1] row(s) selected.

Mach> SELECT ltrim(name, 'dckak') FROM trim_table2;
ltrim(name, 'dckak')
------------------------
NULL
[1] row(s) selected.

Mach> SELECT rtrim(name, 'dckak') FROM trim_table2;
rtrim(name, 'dckak')
------------------------
NULL
[1] row(s) selected.
```


## MAX

지정한 숫자 컬럼의 최대값을 반환하는 집계 함수입니다.

```sql
MAX(column_name)
```

```sql
Mach> CREATE TABLE max_table (c INTEGER);
Created successfully.

Mach> INSERT INTO max_table VALUES(10);
1 row(s) inserted.

Mach> INSERT INTO max_table VALUES(20);
1 row(s) inserted.

Mach> INSERT INTO max_table VALUES(30);
1 row(s) inserted.

Mach> SELECT MAX(c) FROM max_table;
MAX(c)
--------------
30
[1] row(s) selected.
```


## MEDIAN {#median}

`MEDIAN(value)`는 숫자식의 정확한 중앙값을 반환합니다. 현재 구현에서는 `PERCENTILE_CONT(value, 0.5)`와 같은 방식으로 동작합니다.

```sql
MEDIAN(value)
```

- `value`는 숫자형이어야 합니다.
- `NULL` 값은 무시합니다.
- 반환 타입은 `DOUBLE`입니다.

```sql
SELECT MEDIAN(temp_c)
FROM sensor_log;
```


## MIN

지정한 숫자 컬럼의 최소값을 반환하는 집계 함수입니다.

```sql
MIN(column_name)
```

```sql
Mach> CREATE TABLE min_table(c1 INTEGER);
Created successfully.

Mach> INSERT INTO min_table VALUES(1);
1 row(s) inserted.

Mach> INSERT INTO min_table VALUES(22);
1 row(s) inserted.

Mach> INSERT INTO min_table VALUES(33);
1 row(s) inserted.

Mach> SELECT MIN(c1) FROM min_table;
MIN(c1)
--------------
1
[1] row(s) selected.
```


## NVL

컬럼 값이 NULL이면 지정한 값으로 대체하고, NULL이 아니면 원래 값을 반환합니다.

```sql
NVL(string1, replace_with)
```

```sql
Mach> CREATE TABLE nvl_table (c1 varchar(10));
Created successfully.

Mach> INSERT INTO nvl_table VALUES ('Johnathan');
1 row(s) inserted.

Mach> INSERT INTO nvl_table VALUES (NULL);
1 row(s) inserted.

Mach> SELECT NVL(c1, 'Thomas') FROM nvl_table;
NVL(c1, 'Thomas')
---------------------
Thomas
Johnathan
```

## NEXTVAL

`NEXTVAL(sequence_column)`은 Lookup 테이블의 Sequence 컬럼에 대해 다음 값을 반환합니다.

```sql
NEXTVAL(sequence_column)
```

- `NEXTVAL`은 `INSERT` 문에서만 사용할 수 있습니다.
- 인자는 `PROPERTY(SEQUENCE=...)`로 설정된 컬럼이어야 합니다.
- Sequence 컬럼 생성과 예제는 [Sequence Column](/dbms/reference/sql/#sequence-column)을 참고하십시오.

```sql
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-a');
```


## ROUND

입력 값의 지정한 자릿수(입력 자릿수 + 1)를 반올림한 결과를 반환합니다. 자릿수를 생략하면 소수점 0자리에서 반올림합니다. 음수를 지정해 정수부 자리에서 반올림할 수 있습니다.

```sql
ROUND(column_name, [decimals])
```

```sql
Mach> CREATE TABLE round_table (c1 DOUBLE);
Created successfully.

Mach> INSERT INTO round_table VALUES (1.994);
1 row(s) inserted.

Mach> INSERT INTO round_table VALUES (1.995);
1 row(s) inserted.

Mach> SELECT c1, ROUND(c1, 2) FROM round_table;
c1                          ROUND(c1, 2)
-----------------------------------------------------------
1.995                       2
1.994                       1.99
```


## ROWNUM

SELECT 결과 행에 번호를 부여합니다.

SELECT에서 사용하는 서브쿼리나 인라인 뷰 내부에서 사용할 수 있습니다. 인라인 뷰의 Target List에서 ROWNUM()을 사용한 경우 외부에서 참조할 수 있도록 Alias를 지정해야 합니다.

```sql
ROWNUM()
```

**사용 가능한 절**

이 함수는 SELECT의 Target List, GROUP BY, ORDER BY 절에서 사용할 수 있습니다. WHERE와 HAVING 절에서는 사용할 수 없습니다. 결과 번호로 WHERE/HAVING을 제어하려면 인라인 뷰에서 ROWNUM()을 계산한 뒤, 외부 쿼리의 WHERE/HAVING에서 참조해야 합니다.

|사용 가능 절|사용 불가 절|
|--|--|
|Target List / GROUP BY / ORDER BY|WHERE / HAVING|

```sql
Mach> CREATE TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO rownum_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(2, 2.0, 'Second Row');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(3, 3.3, 'Third Row');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(4, 4.3, 'Fourth Row');
1 row(s) inserted.

Mach> SELECT INNER_RANK, c3 AS NAME
    2 FROM   (SELECT ROWNUM() AS INNER_RANK, * FROM rownum_table)
    3 WHERE  INNER_RANK < 3;
INNER_RANK           NAME
------------------------------------
1                    Fourth Row
2                    Third Row
[2] row(s) selected.
```

**정렬로 인한 결과 번호 변화**

SELECT에 ORDER BY 절이 있으면 Target List의 ROWNUM() 결과가 순차적으로 부여되지 않을 수 있습니다. 이는 ROWNUM()이 ORDER BY보다 먼저 처리되기 때문입니다. 순차 번호가 필요하면 ORDER BY를 포함한 쿼리를 인라인 뷰로 만든 뒤, 외부 SELECT에서 ROWNUM()을 호출하세요.

```sql
Mach> CREATE TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO rownum_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(2, 2.0, 'John');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(3, 3.3, 'Sarah');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(4, 4.3, 'Micheal');
1 row(s) inserted.

Mach> SELECT ROWNUM(), c2 AS SORT, c3 AS NAME
    2 FROM   ( SELECT * FROM rownum_table ORDER BY c3 );
ROWNUM()             SORT                        NAME
-----------------------------------------------------------------
1                    1                           NULL
2                    2                           John
3                    4.3                         Micheal
4                    3.3                         Sarah
[4] row(s) selected.
```


## SERIESNUM

SERIES BY로 그룹화된 시리즈에서 각 레코드가 몇 번째인지 나타내는 번호를 반환합니다. 반환 타입은 BIGINT이며, SERIES BY 절을 사용하지 않으면 항상 1을 반환합니다.

```sql
SERIESNUM()
```

```sql
Mach> CREATE TABLE T1 (C1 INTEGER, C2 INTEGER);
Created successfully.

Mach> INSERT INTO T1 VALUES (0, 1);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (2, 3);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (3, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (4, 1);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (5, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (6, 3);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (7, 1);
1 row(s) inserted.


Mach> SELECT SERIESNUM(), C1, C2 FROM T1 ORDER BY C1 SERIES BY C2 > 1;
SERIESNUM() C1 C2
-------------------------------------------------
1 1 2
1 2 3
1 3 2
2 5 2
2 6 3
[5] row(s) selected.
```


## STDDEV / STDDEV_POP

이 함수는 입력 컬럼의 표준편차와 모표준편차를 반환하는 집계 함수입니다. 각각 VARIANCE와 VAR_POP 값의 제곱근에 해당합니다.

```sql
STDDEV(column)
STDDEV_POP(column)
```

```sql
Mach> CREATE TABLE stddev_table(c1 INTEGER, C2 DOUBLE);

Mach> INSERT INTO stddev_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (2, 1);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (3, 2);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (4, 2);
1 row(s) inserted.

Mach> SELECT c2, STDDEV(c1) FROM stddev_table GROUP BY c2;
c2                          STDDEV(c1)
-----------------------------------------------------------
1                           0.707107
2                           0.707107
[2] row(s) selected.

Mach> SELECT c2, STDDEV_POP(c1) FROM stddev_table GROUP BY c2;
c2                          STDDEV_POP(c1)
-----------------------------------------------------------
1                           0.5
2                           0.5
[2] row(s) selected.
```


## SUBSTR

이 함수는 문자열 컬럼을 START부터 SIZE 길이만큼 잘라 반환합니다.

* START는 1부터 시작하며 0이면 NULL을 반환합니다.
* SIZE가 문자열 길이보다 크면 전체 문자열을 반환합니다.
SIZE는 선택 사항이며 생략하면 문자열 길이가 사용됩니다.

```sql
SUBSTRING(column_name, start, [length])
```

```sql
Mach> CREATE TABLE substr_table (c1 VARCHAR(10));
Created successfully.

Mach> INSERT INTO substr_table values('ABCDEFG');
1 row(s) inserted.

Mach> INSERT INTO substr_table values('abstract');
1 row(s) inserted.

Mach> SELECT SUBSTR(c1, 1, 1) FROM substr_table;
SUBSTR(c1, 1, 1)
--------------------
a
A
[2] row(s) selected.

Mach> SELECT SUBSTR(c1, 3, 3) FROM substr_table;
SUBSTR(c1, 3, 3)
--------------------
str
CDE
[2] row(s) selected.

Mach> SELECT SUBSTR(c1, 2) FROM substr_table;
SUBSTR(c1, 2)
-----------------
bstract
BCDEFG
[2] row(s) selected.

Mach> drop table substr_table;
Dropped successfully.

Mach> CREATE TABLE substr_table (c1 VARCHAR(10));
Created successfully.

Mach> INSERT INTO substr_table values('ABCDEFG');
1 row(s) inserted.

Mach> SELECT SUBSTR(c1, 1, 1) FROM substr_table;
SUBSTR(c1, 1, 1)
--------------------
A
[1] row(s) selected.

Mach> SELECT SUBSTR(c1, 3, 3) FROM substr_table;
SUBSTR(c1, 3, 3)
--------------------
CDE
[1] row(s) selected.

Mach> SELECT SUBSTR(c1, 2) FROM substr_table;
SUBSTR(c1, 2)
-----------------
BCDEFG
[1] row(s) selected.
```


## SUBSTRING_INDEX

입력된 count만큼 구분자(delim)를 찾을 때까지의 부분 문자열을 반환합니다. count가 음수이면 문자열 끝에서부터 구분자를 찾고, 구분자를 찾은 위치부터 문자열 끝까지 반환합니다.

count가 0이거나 문자열에 구분자가 없으면 NULL을 반환합니다.

```sql
SUBSTRING_INDEX(expression, delim, count)
```

```sql
Mach> CREATE TABLE substring_table (url VARCHAR(30));
Created successfully.

Mach> INSERT INTO substring_table VALUES('www.machbase.com');
1 row(s) inserted.

Mach> SELECT SUBSTRING_INDEX(url, '.', 1) FROM substring_table;
SUBSTRING_INDEX(url, '.', 1)
----------------------------------
www
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', 2) FROM substring_table;
SUBSTRING_INDEX(url, '.', 2)
----------------------------------
www.machbase
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', -1) FROM substring_table;
SUBSTRING_INDEX(url, '.', -1)
----------------------------------
com
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(url, '.', 2), '.', -1) FROM substring_table;
SUBSTRING_INDEX(SUBSTRING_INDEX(url, '.', 2), '.', -1)
-------------------------------------------
machbase
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', 0) FROM substring_table;
SUBSTRING_INDEX(url, '.', 0)
----------------------------------
NULL
[1] row(s) selected.
```


## SUM

숫자 컬럼의 합계를 반환하는 집계 함수입니다.

```sql
SUM(column_name)
```

```sql
Mach> CREATE TABLE sum_table (c1 INTEGER, c2 INTEGER);
Created successfully.

Mach> INSERT INTO sum_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(3, 4);
1 row(s) inserted.

Mach> SELECT c1, SUM(c1) from sum_table group by c1;
c1          SUM(c1)
------------------------------------
2           6
3           3
1           3
[3] row(s) selected.

Mach> SELECT c1, SUM(c2) from sum_table group by c1;
c1          SUM(c2)
------------------------------------
2           6
3           4
1           6
[3] row(s) selected.
```


## SUMSQ

SUMSQ는 숫자 값들의 제곱합을 반환합니다.

```sql
SUMSQ(value)
```

```sql
Mach> CREATE TABLE sumsq_table (c1 INTEGER, c2 INTEGER);
Created successfully.

Mach> INSERT INTO sumsq_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (1, 3);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (2, 4);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (2, 5);
1 row(s) inserted.

Mach> SELECT c1, SUMSQ(c2) FROM sumsq_table GROUP BY c1;
c1          SUMSQ(c2)
------------------------------------
2           41
1           14
[2] row(s) selected.
```


## SYSDATE / NOW

SYSDATE는 함수가 아닌 의사 컬럼으로, 시스템 현재 시간을 반환합니다.

NOW는 SYSDATE와 동일한 기능이며, 사용자 편의를 위해 제공합니다.

```sql
SYSDATE
NOW
```

```sql
Mach> SELECT SYSDATE, NOW FROM t1;

SYSDATE                         NOW
-------------------------------------------------------------------
2017-01-16 14:14:53 310:973:000 2017-01-16 14:14:53 310:973:000
```


## TO_CHAR

주어진 데이터 타입을 문자열 타입으로 변환합니다. 타입에 따라 format_string을 지정할 수 있지만, 바이너리 타입에는 사용할 수 없습니다.

```sql
TO_CHAR(column)
```

**TO_CHAR: 기본 데이터 타입**

기본 데이터 타입은 아래와 같이 문자열 형태로 변환됩니다.

```sql
Mach> CREATE TABLE fixed_table (id1 SHORT, id2 INTEGER, id3 LONG, id4 FLOAT, id5 DOUBLE, id6 IPV4, id7 IPV6, id8 VARCHAR (128));
Created successfully.

Mach> INSERT INTO fixed_table values(200, 19234, 1234123412, 3.14, 7.8338, '192.168.0.1', '::127.0.0.1', 'log varchar');
1 row(s) inserted.

Mach> SELECT '[ ' || TO_CHAR(id1) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id1) || ' ]'
------------------------------------------------------------------------------------
[ 200 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id2) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id2) || ' ]'
------------------------------------------------------------------------------------
[ 19234 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id3) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id3) || ' ]'
------------------------------------------------------------------------------------
[ 1234123412 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id4) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id4) || ' ]'
------------------------------------------------------------------------------------
[ 3.140000 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id5) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id5) || ' ]'
------------------------------------------------------------------------------------
[ 7.833800 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id6) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id6) || ' ]'
------------------------------------------------------------------------------------
[ 192.168.0.1 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id7) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id7) || ' ]'
------------------------------------------------------------------------------------
[ 0000:0000:0000:0000:0000:0000:7F00:0001 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id8) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id8) || ' ]'
------------------------------------------------------------------------------------
[ log varchar ]
[1] row(s) selected.
```

**TO_CHAR: 부동소수점 숫자**

* 5.5.6 버전부터 지원

float와 double 값을 문자열로 변환합니다.
포맷 표현식은 반복해서 사용할 수 없으며 '[letter][number]' 형태로 입력해야 합니다.

|포맷 표현식|설명|
|--|--|
|F / f|컬럼 값의 소수점 자릿수를 지정합니다. 입력 가능한 최대 값은 30입니다.|
|N / n|소수점 자릿수를 지정하고 정수부 3자리마다 콤마(,)를 삽입합니다. 입력 가능한 최대 값은 30입니다.|

```sql
Mach> create table float_table (i1 float, i2 double);
Created successfully.

Mach> insert into float_table values (1.23456789, 1234.5678901234567890);
1 row(s) inserted.

Mach> select TO_CHAR(i1, 'f8'), TO_CHAR(i2, 'N9') from float_table;
TO_CHAR(i1, 'f8')       TO_CHAR(i2, 'N9')
--------------------------------------------------------------
1.23456788              1,234.567890123
[1] row(s) selected.
```

**TO_CHAR: DATETIME 타입**

datetime 컬럼 값을 임의의 문자열로 변환하는 함수입니다. 이를 이용해 다양한 문자열을 생성하고 조합할 수 있습니다.

format_string을 생략하면 기본값은 "YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn"입니다.

|포맷 표현식|설명|
|--|--|
|YYYY|연도를 4자리 숫자로 변환합니다.|
|YY|연도를 2자리 숫자로 변환합니다.|
|MM|월을 2자리 숫자로 변환합니다.|
|MON|월을 3자리 영문 약어로 변환합니다. (예: JAN, FEB, MAY, ...)|
|DD|일을 2자리 숫자로 변환합니다.|
|DAY|요일을 3자리 영문 약어로 변환합니다. (예: SUN, MON, ...)|
|IW|ISO 8601 규칙에 따라 특정 연도의 주차를 1~53으로 변환합니다(요일 고려).<br> - 한 주의 시작은 월요일입니다.<br> - 첫 주는 전년도 마지막 주로 간주될 수 있습니다. 마찬가지로 마지막 주는 다음 해의 첫 주로 간주될 수 있습니다.<br>    자세한 내용은 ISO 8601을 참고하세요.|
|WW|요일을 고려하지 않고 특정 연도의 주차를 1~53으로 변환합니다.<br>즉, 1월 1일~1월 7일은 1로 변환됩니다.|
|W|요일을 고려하지 않고 특정 월의 주차를 1~5로 변환합니다.<br>즉, 3월 1일~3월 7일은 1로 변환됩니다.|
|HH|시간을 2자리 숫자로 변환합니다.|
|HH12|시간을 1~12 범위의 2자리 숫자로 변환합니다.|
|HH24|시간을 1~23 범위의 2자리 숫자로 변환합니다.|
|HH2, HH3, HH6|HH 뒤 숫자 단위로 시간을 절단합니다.<br><br>예를 들어 HH6을 사용하면 0~5는 0, 6~11은 6으로 표시합니다.<br>이 표현은 시간열 통계 계산에 유용합니다.<br>이 값은 24시간 기준으로 표시됩니다.|
|MI|분을 2자리 숫자로 표시합니다.|
|MI2, MI5, MI10, MI20, MI30|MI 뒤 숫자 단위로 분을 절단합니다.<br><br>예를 들어 MI30은 0~29분은 0, 30~59분은 30으로 표시합니다.<br>이 표현은 시간열 통계 계산에 유용합니다.|
|SS|초를 2자리 숫자로 표시합니다.|
|SS2, SS5, SS10, SS20, SS30|SS 뒤 숫자 단위로 초를 절단합니다.<br><br>예를 들어 SS30은 0~29초는 0, 30~59초는 30으로 표시합니다.<br>이 표현은 시간열 통계 계산에 유용합니다.|
|AM|시간을 AM/PM으로 표시합니다.|
|mmm|밀리초를 3자리 숫자로 표시합니다.<br><br>값 범위는 0~999입니다.|
|uuu|마이크로초를 3자리 숫자로 표시합니다.<br><br>값 범위는 0~999입니다.|
|nnn|나노초를 3자리 숫자로 표시합니다.<br><br>값 범위는 0~999입니다.|

```sql
Mach> CREATE TABLE datetime_table (id integer, dt datetime);
Created successfully.

Mach> INSERT INTO  datetime_table values(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(2, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(3, TO_DATE('2013-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(4, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> SELECT id, dt FROM datetime_table WHERE dt > TO_DATE('2000-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 11:22:33 444:555:666
3           2013-11-11 01:02:03 004:005:006
2           2012-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT id, dt FROM datetime_table WHERE dt > TO_DATE('2013-11-11 1:2:3') and dt < TO_DATE('2014-11-11 1:2:3');
id          dt
-----------------------------------------------
3           2013-11-11 01:02:03 004:005:006
[1] row(s) selected.

Mach> SELECT id, TO_CHAR(dt) FROM datetime_table;
id          TO_CHAR(dt)
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33 444:555:666
3           2013-11-11 01:02:03 004:005:006
2           2012-11-11 01:02:03 004:005:006
1           1999-11-11 01:02:03 004:005:006
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY')
-------------------------------------------------------------------------------------------------
4           2014
3           2013
2           2012
1           1999
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM')
-------------------------------------------------------------------------------------------------
4           2014-12
3           2013-11
2           2012-11
1           1999-11
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD')
-------------------------------------------------------------------------------------------------
4           2014-12-30
3           2013-11-11
2           2012-11-11
1           1999-11-11
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD TO_CHAR') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD TO_CHAR')
-------------------------------------------------------------------------------------------------
4           2014-12-30 TO_CHAR
3           2013-11-11 TO_CHAR
2           2012-11-11 TO_CHAR
1           1999-11-11 TO_CHAR
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS')
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33
3           2013-11-11 01:02:03
2           2012-11-11 01:02:03
1           1999-11-11 01:02:03
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.uuu.nnn') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33 444.555.666
3           2013-11-11 01:02:03 004.005.006
2           2012-11-11 01:02:03 004.005.006
1           1999-11-11 01:02:03 004.005.006
[4] row(s) selected.
```

**TO_CHAR: 지원하지 않는 타입**

현재 TO_CHAR는 바이너리 타입을 지원하지 않습니다.

일반 문자열로 변환할 수 없기 때문입니다. 화면에 출력하려면 TO_HEX() 함수로 16진 값을 출력해 확인할 수 있습니다.


## TO_DATE

지정한 포맷 문자열에 따라 문자열을 datetime 타입으로 변환합니다.

format_string을 생략하면 기본값은 "YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn"입니다.

```sql
-- default format is "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" if no format exists.
TO_DATE(date_string [, format_string])
```

```sql
Mach> CREATE TABLE to_date_table (id INTEGER, dt datetime);
Created successfully.

Mach> INSERT INTO  to_date_table VALUES(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(2, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(3, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(4, TO_DATE('2014-12-30 23:22:34 777:888:999', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn'));
1 row(s) inserted.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('1999-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 23:22:34 777:888:999
3           2014-12-30 11:22:33 444:555:666
2           2012-11-11 01:02:03 004:005:006
1           1999-11-11 01:02:03 004:005:006
[4] row(s) selected.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('2000-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 23:22:34 777:888:999
3           2014-12-30 11:22:33 444:555:666
2           2012-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('2012-11-11 1:2:3','YYYY-MM-DD HH24:MI:SS') and dt < TO_DATE('2014-11-11 1:2:3','YYYY-MM-DD HH24:MI:SS');
id          dt
-----------------------------------------------
2           2012-11-11 01:02:03 004:005:006
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999', 'YYYY') FROM to_date_table LIMIT 1;
id          TO_DATE('1999', 'YYYY')
-----------------------------------------------
4           1999-01-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12', 'YYYY-MM') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12', 'YYYY-MM')
-----------------------------------------------
4           1999.12.01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999', 'YYYY') FROM to_date_table LIMIT 1;
id          TO_DATE('1999', 'YYYY')
-----------------------------------------------
4           1999-01-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12', 'YYYY-MM') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12', 'YYYY-MM')
-----------------------------------------------
4           1999-12-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12', 'YYYY-MM-DD HH24:MI') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12', 'YYYY-MM-DD HH24:MI')
-------------------------------------------------------
4           1999-12-31 13:12:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS')
-------------------------------------------------------
4           1999-12-31 13:12:32 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123', 'YYYY-MM-DD HH24:MI:SS mmm') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32 123', 'YYYY-MM-DD HH24:MI:SS mmm')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123:456', 'YYYY-MM-DD HH24:MI:SS mmm:uuu') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32 123:456', 'YYYY-MM-DD HH24:MI:SS mmm:uuu')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:456:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123:456:789', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn') FROM to_date_table LIMIT 1;
id           TO_DATE('1999-12-31 13:12:32 123:456:789', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:456:789
[1] row(s) selected.
```


## TO_DATE_SAFE

TO_DATE()와 유사하지만 변환에 실패하면 오류 없이 NULL을 반환합니다.

```sql
TO_DATE_SAFE(date_string [, format_string])
```

```sql
Mach> CREATE TABLE date_table (ts DATETIME);
Created successfully.

Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-01-01', 'YYYY-MM-DD'));
1 row(s) inserted.
Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-01-02', 'YYYY'));
1 row(s) inserted.
Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-12-32', 'YYYY-MM-DD'));
1 row(s) inserted.

Mach> SELECT ts FROM date_table;
ts
----------------------------------
NULL
NULL
2016-01-01 00:00:00 000:000:000
[3] row(s) selected.
```


## TO_HEX

컬럼 값이 NULL이면 NULL을 반환하고, NULL이 아니면 원래 값을 16진 문자열로 반환합니다. 출력 일관성을 위해 short, int, long 타입은 BIG ENDIAN으로 변환합니다.

```sql
TO_HEX(column)
```

```sql
Mach> CREATE TABLE hex_table (id1 SHORT, id2 INTEGER, id3 VARCHAR(10), id4 FLOAT, id5 DOUBLE, id6 LONG, id7 IPV4, id8 IPV6, id9 TEXT, id10 BINARY,
id11 DATETIME);
Created successfully.

Mach> INSERT INTO hex_table VALUES(256, 65535, '0123456789', 3.141592, 1024 * 1024 * 1024 * 3.14, 13513135446, '192.168.0.1', '::192.168.0.1', 'textext',
'binary', TO_DATE('1999', 'YYYY'));
1 row(s) inserted.

Mach> SELECT TO_HEX(id1), TO_HEX(id2), TO_HEX(id3), TO_HEX(id4), TO_HEX(id5), TO_HEX(id6), TO_HEX(id7), TO_HEX(id8), TO_HEX(id9), TO_HEX(id10), TO_HEX(id11)
FROM hex_table;
TO_HEX(id1)  TO_HEX(id2)  TO_HEX(id3)            TO_HEX(id4)  TO_HEX(id5)        TO_HEX(id6)        TO_HEX(id7)
-------------------------------------------------------------------------------------------------------------------------
TO_HEX(id8)                          TO_HEX(id9)
--------------------------------------------------------------------------------------------------------------------------
TO_HEX(id10)                                                                      TO_HEX(id11)
--------------------------------------------------------------------------------------------------------
0100   0000FFFF   30313233343536373839   D80F4940   1F85EB51B81EE941   0000000325721556   04C0A80001
06000000000000000000000000C0A80001   74657874657874
62696E617279                                                                      0CB325846E226000
[1] row(s) selected.
```


## TO_INET_STR

`TO_INET_STR(ipv4_value)`는 `IPV4` 값을 점으로 구분된 십진 문자열로 변환합니다.

```sql
TO_INET_STR(ipv4_value)
```

```sql
SELECT TO_INET_STR(TO_IPV4('192.168.0.1'));
```


## TO_IPV4 / TO_IPV4_SAFE

주어진 문자열을 IPv4 타입으로 변환합니다. 문자열을 숫자 값으로 변환할 수 없으면 TO_IPV4()는 오류를 반환하고 작업을 중단합니다.

반면 TO_IPV4_SAFE()는 오류 발생 시 NULL을 반환하므로 작업을 계속할 수 있습니다.

```sql
TO_IPV4(string_value)
TO_IPV4_SAFE(string_value)
```

```sql
Mach> CREATE TABLE ipv4_table (c1 varchar(100));
Created successfully.

Mach> INSERT INTO ipv4_table VALUES('192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipv4_table VALUES('     192.168.0.2    ');
1 row(s) inserted.

Mach> INSERT INTO ipv4_table VALUES(NULL);
1 row(s) inserted.

Mach> SELECT c1 FROM ipv4_table;
c1
------------------------------------------------------------------------------------
NULL
     192.168.0.2
192.168.0.1
[3] row(s) selected.

Mach> SELECT TO_IPV4(c1) FROM ipv4_table;
TO_IPV4(c1)
------------------
NULL
192.168.0.2
192.168.0.1
[3] row(s) selected.

Mach> INSERT INTO ipv4_table VALUES('192.168.0.1.1');
1 row(s) inserted.

Mach> SELECT TO_IPV4(c1) FROM ipv4_table limit 1;
TO_IPV4(c1)
------------------
[ERR-02068 : Invalid IPv4 address format (192.168.0.1.1).]
[0] row(s) selected.

Mach> SELECT TO_IPV4_SAFE(c1) FROM ipv4_table;
TO_IPV4_SAFE(c1)
-------------------
NULL
NULL
192.168.0.2
192.168.0.1
[4] row(s) selected.
```


## TO_IPV6 / TO_IPV6_SAFE

주어진 문자열을 IPv6 타입으로 변환합니다. 문자열을 숫자 타입으로 변환할 수 없으면 TO_IPV6()는 오류를 반환하고 작업을 중단합니다.

반면 TO_IPV6_SAFE()는 오류 발생 시 NULL을 반환하므로 작업을 계속할 수 있습니다.

```sql
TO_IPV6(string_value)
TO_IPV6_SAFE(string_value)
```

```sql
Mach> CREATE TABLE ipv6_table (id varchar(100));
Created successfully.

Mach> INSERT INTO ipv6_table VALUES('::0.0.0.0');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0' || '.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('   ::127.0.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0.0.4  ');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('   ::FFFF:255.255.255.255   ');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('21DA:D3:0:2F3B:2AA:FF:FE28:9C5A');
1 row(s) inserted.

Mach> SELECT TO_IPV6(id) FROM ipv6_table;
TO_IPV6(id)
---------------------------------------------------------------
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.2
::127.0.0.1
::
[7] row(s) selected.

Mach> INSERT INTO ipv6_table VALUES('127.0.0.10.10');
1 row(s) inserted.

Mach> SELECT TO_IPV6(id) FROM ipv6_table limit 1;
TO_IPV6(id)
---------------------------------------------------------------
[ERR-02148 : Invalid IPv6 address format.(127.0.0.10.10)]
[0] row(s) selected.

Mach> SELECT TO_IPV6_SAFE(id) FROM ipv6_table;
TO_IPV6_SAFE(id)
---------------------------------------------------------------
NULL
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.2
::127.0.0.1
::
[8] row(s) selected.
```


## TO_NUMBER / TO_NUMBER_SAFE

주어진 문자열을 숫자(double)로 변환합니다. 문자열을 숫자 값으로 변환할 수 없으면 TO_NUMBER()는 오류를 반환하고 작업을 중단합니다.

반면 TO_NUMBER_SAFE()는 오류 발생 시 NULL을 반환하므로 작업을 계속할 수 있습니다.

```sql
TO_NUMBER(string_value)
TO_NUMBER_SAFE(string_value)
```

```sql
Mach> CREATE TABLE number_table (id varchar(100));
Created successfully.

Mach> INSERT INTO number_table VALUES('10');
1 row(s) inserted.

Mach> INSERT INTO number_table VALUES('20');
1 row(s) inserted.

Mach> INSERT INTO number_table VALUES('30');
1 row(s) inserted.

Mach> SELECT TO_NUMBER(id) from number_table;
TO_NUMBER(id)
------------------------------
30
20
10
[3] row(s) selected.

Mach> CREATE TABLE safe_table (id varchar(100));
Created successfully.

Mach> INSERT INTO safe_table VALUES('invalidnumber');
1 row(s) inserted.

Mach> SELECT TO_NUMBER(id) from safe_table;
TO_NUMBER(id)
------------------------------
[ERR-02145 : The string cannot be converted to number value.(invalidnumber)]
[0] row(s) selected.

Mach> SELECT TO_NUMBER_SAFE(id) from safe_table;
TO_NUMBER_SAFE(id)
------------------------------
NULL
[1] row(s) selected.
```


## TOP_K {#top_k}

`TOP_K(value, k)`는 가장 자주 등장한 `k`개의 숫자 값을 `value:count` 형식의 문자열로 반환합니다.

```sql
TOP_K(value, k)
```

- `value`는 숫자형이어야 합니다.
- `k`는 양의 정수 상수여야 합니다.
- `NULL` 값은 무시합니다.
- 반환 타입은 `VARCHAR`입니다.
- 정렬 기준은 빈도 내림차순이며, 빈도가 같으면 값 오름차순입니다.

```sql
SELECT TOP_K(alarm_code, 3)
FROM event_log;
```

예시 결과:

```text
101:532,205:317,301:90
```


## TO_TIMESTAMP

datetime 타입을 1970-01-01 09:00 이후 경과 나노초 값으로 변환합니다.

```sql
TO_TIMESTAMP(datetime_value)
```

```sql
Mach> create table datetime_tbl (c1 datetime);
Created successfully.

Mach> insert into datetime_tbl values ('2010-01-01 10:10:10');
1 row(s) inserted.

Mach> select to_timestamp(c1) from datetime_tbl;
to_timestamp(c1)
-----------------------
1262308210000000000
[1] row(s) selected.
```


## TRUNC

TRUNC 함수는 소수점 이하 n자리에서 잘라낸 값을 반환합니다.

n을 생략하면 0으로 간주하여 소수점을 모두 제거합니다. n이 음수이면 소수점 앞 n자리에서 잘라낸 값을 반환합니다.

```sql
TRUNC(number [, n])
```

```sql
Mach> CREATE TABLE trunc_table (i1 DOUBLE);
Created successfully.

Mach> INSERT INTO trunc_table VALUES (158.799);
1 row(s) inserted.

Mach> SELECT TRUNC(i1, 1), TRUNC(i1, -1) FROM trunc_table;
TRUNC(i1, 1)                TRUNC(i1, -1)
-----------------------------------------------------------
158.7                       150
[1] row(s) selected.

Mach> SELECT TRUNC(i1, 2), TRUNC(i1, -2) FROM trunc_table;
TRUNC(i1, 2)                TRUNC(i1, -2)
-----------------------------------------------------------
158.79                      100
[1] row(s) selected.
```


## TS_CHANGE_COUNT

특정 컬럼 값의 변경 횟수를 구하는 집계 함수입니다.

입력 데이터가 시간순으로 입력된다는 것을 보장할 수 없으므로 1) Join 또는 2) Inline view와 함께 사용할 수 없습니다.
현재 버전은 varchar를 제외한 타입만 지원합니다.

* **이 함수는 Cluster Edition에서 사용할 수 없습니다.**

```sql
TS_CHANGE_COUNT(column)
```

```sql
Mach> CREATE TABLE ipcount_table (id INTEGER, ip IPV4);
Created successfully.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.4');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.4');
1 row(s) inserted.

Mach> SELECT id, TS_CHANGE_COUNT(ip) from ipcount_table GROUP BY id;
id          TS_CHANGE_COUNT(ip)
------------------------------------
2           2
1           4
[2] row(s) selected.
```


## UNIX_TIMESTAMP

UNIX_TIMESTAMP는 유닉스 time() 시스템 콜 기준으로 date 타입 값을 32비트 정수로 변환하는 함수입니다. (FROM_UNIXTIME은 반대로 정수 값을 date 타입으로 변환합니다.)

```sql
UNIX_TIMESTAMP(datetime_value)
```

```sql
Mach> CREATE table unix_table (c1 int);
Created successfully.

Mach> INSERT INTO unix_table VALUES (UNIX_TIMESTAMP('2001-01-01'));
1 row(s) inserted.

Mach> SELECT * FROM unix_table;
C1
--------------
978274800
[1] row(s) selected.
```


## UPPER

영문 문자열을 대문자로 변환합니다.

```sql
UPPER(string_value)
```

```sql
Mach> CREATE TABLE upper_table(id INTEGER,name VARCHAR(10));
Created successfully.

Mach> INSERT INTO upper_table VALUES(1, '');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(2, 'James');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(3, 'sarah');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(4, 'THOMAS');
1 row(s) inserted.

Mach> SELECT id, UPPER(name) FROM upper_table;
id          UPPER(name)
----------------------------
4           THOMAS
3           SARAH
2           JAMES
1           NULL
[4] row(s) selected.
```


## VARIANCE / VAR_POP

지정한 숫자 컬럼의 분산을 반환하는 집계 함수입니다. VARIANCE는 표본 분산, VAR_POP은 모분산을 반환합니다.

```sql
VARIANCE(column_name)
VAR_POP(column_name)
```

```sql
Mach> CREATE TABLE var_table(c1 INTEGER, c2 DOUBLE);
Created successfully.

Mach> INSERT INTO var_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (2, 1);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (2, 2);
1 row(s) inserted.

Mach> SELECT VARIANCE(c1) FROM var_table;
VARIANCE(c1)
------------------------------
0.333333
[1] row(s) selected.

Mach> SELECT VAR_POP(c1) FROM var_table;
VAR_POP(c1)
------------------------------
0.25
[1] row(s) selected.
```


## YEAR / MONTH / DAY

입력 datetime 컬럼 값에서 각각 연, 월, 일을 추출해 정수로 반환합니다.

```sql
YEAR(datetime_col)
MONTH(datetime_col)
DAY(datetime_col)
```

```sql
Mach> CREATE TABLE extract_table(c1 DATETIME, c2 INTEGER);
Created successfully.

Mach> INSERT INTO extract_table VALUES (to_date('2001-01-01 12:30:00 000:000:000'), 1);
1 row(s) inserted.

Mach> SELECT YEAR(c1), MONTH(c1), DAY(c1) FROM extract_table;
year(c1)    month(c1)   day(c1)
----------------------------------------
2001        1           1
```


## ISNAN / ISINF

인자로 받은 숫자 값이 NaN 또는 Inf인지 판별합니다. NaN 또는 Inf이면 1, 그렇지 않으면 0을 반환합니다.

```sql
ISNAN(number)
ISINF(number)
```

다음 예제는 테이블에 이미 `NaN` 및 `Inf` 값이 들어 있는 경우를 가정합니다.
SQL `INSERT` 문에서 `nan` 또는 `inf` 토큰을 값으로 직접 입력할 수는 없습니다.

```sql
Mach> SELECT * FROM test;
I1                          I2                          I3
------------------------------------------------------------------------
1                           1                           1
nan                         inf                         0
NULL                        NULL                        NULL
[3] row(s) selected.


Mach> SELECT ISNAN(i1), ISNAN(i2), ISNAN(i3), i3 FROM test ;
ISNAN(i1)   ISNAN(i2)   ISNAN(i3)   i3
-----------------------------------------------------
0           0           0           1
1           0           0           0
NULL        NULL        NULL        NULL
[3] row(s) selected.

Mach> SELECT * FROM test WHERE ISNAN(i1) = 1;
I1                          I2                          I3
------------------------------------------------------------------------
nan                         inf                         0
[1] row(s) selected.
```

## JSON_SET

JSON 문서의 특정 경로에 SQL scalar 값을 JSON scalar로 저장합니다.

```sql
JSON_SET(json_doc, path, scalar)
```

```sql
Mach> SELECT JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE') FROM dual;
JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE')
--------------------------------------------------------------------------------
{"ship":{"status":"DONE"}}
[1] row(s) selected.
```

주의사항:

- `path` 는 full JSONPath를 사용해야 합니다.
- `JSON_SET(..., path, NULL)` 은 JSON `null` 을 저장합니다.
- JSON 문서 인자가 `NULL` 이면 결과는 SQL `NULL` 입니다.
- `path` 가 `NULL` 이거나 빈 문자열이면 오류가 발생합니다.
- object 경로 중심으로 지원합니다.
- array element 갱신 예: `$.items[0]` 는 지원하지 않습니다.

## JSON_SET_JSON

세 번째 인자를 JSON 문자열로 해석하여 object 또는 array subtree를 저장합니다.

```sql
JSON_SET_JSON(json_doc, path, json_text)
```

```sql
Mach> SELECT JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}') FROM dual;
JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}')
----------------------------------------------------------------------------
{"ship":{"owner":{"name":"machbase"}}}
[1] row(s) selected.
```

주의사항:

- `path` 는 full JSONPath를 사용해야 합니다.
- 세 번째 인자가 SQL `NULL` 이면 결과는 SQL `NULL` 입니다.
- 유효하지 않은 JSON 문자열은 오류가 발생합니다.
- object 경로 중심으로 지원합니다.
- array element 갱신은 지원하지 않습니다.

## JSON_REMOVE

JSON 문서에서 특정 멤버 또는 하위 경로를 제거합니다.

```sql
JSON_REMOVE(json_doc, path)
```

```sql
Mach> SELECT JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team') FROM dual;
JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team')
--------------------------------------------------------------------------
{"owner":{"name":"machbase"}}
[1] row(s) selected.
```

주의사항:

- `path` 는 full JSONPath를 사용해야 합니다.
- 존재하지 않는 경로는 no-op 으로 처리됩니다.
- `JSON_REMOVE(..., '$')` 는 허용되지 않습니다.
- JSON 문서 인자가 `NULL` 이면 결과는 SQL `NULL` 입니다.

## PI() {#pi}

`DOUBLE` 타입의 π 상수를 반환합니다.

```sql
SELECT PI();
```

```sql
Mach> SELECT PI();
PI()
------------------------------
3.141592653589793
[1] row(s) selected.
```

## SQRT() {#sqrt}

제곱근을 반환합니다.

```sql
SELECT SQRT(9), SQRT(2.25), SQRT(16.0);
```

```sql
Mach> SELECT SQRT(9), SQRT(2.25), SQRT(16.0);
SQRT(9)   SQRT(2.25)         SQRT(16.0)
-----------------------------------------------
3         1.5000000000000000  4
[1] row(s) selected.
```

## POWER() {#power}

`base`의 `exponent` 거듭제곱을 반환합니다.

```sql
SELECT POWER(2, 3), POWER(9, 0.5), POWER(4, -1);
```

```sql
Mach> SELECT POWER(2, 3), POWER(9, 0.5), POWER(4, -1);
POWER(2, 3)   POWER(9, 0.5)   POWER(4, -1)
------------------------------------------------
8             3.0000000000000000 0.2500000000000000
[1] row(s) selected.
```

## POW() {#pow}

`POWER()`의 별칭입니다.

```sql
SELECT POW(2, 3), POW(2, -1), POW(10, 0);
```

```sql
Mach> SELECT POW(2, 3), POW(2, -1), POW(10, 0);
POW(2, 3)   POW(2, -1)   POW(10, 0)
-----------------------------------------
8           0.5           1
[1] row(s) selected.
```

## LOG() {#log}

`LOG(n)`은 자연로그, `LOG(base, n)`은 지정한 밑의 로그를 계산합니다.

```sql
SELECT LOG(2, 8), LOG(100), LOG(10, 1000);
```

```sql
Mach> SELECT LOG(2, 8), LOG(100), LOG(10, 1000);
LOG(2, 8)   LOG(100)             LOG(10, 1000)
------------------------------------------------
3           4.605170185988092     3
[1] row(s) selected.
```

## LN() {#ln}

자연로그 `ln(n)`을 반환합니다.

```sql
SELECT LN(1), LN(10), LN(1000);
```

```sql
Mach> SELECT LN(1), LN(10), LN(1000);
LN(1)      LN(10)         LN(1000)
-----------------------------------
0          2.302585092994046 6.907755278982137
[1] row(s) selected.
```

## EXP() {#exp}

`e^n`을 반환합니다.

```sql
SELECT EXP(0), EXP(1), EXP(-1);
```

```sql
Mach> SELECT EXP(0), EXP(1), EXP(-1);
EXP(0)      EXP(1)         EXP(-1)
-----------------------------------
1           2.718281828459045 0.36787944117144233
[1] row(s) selected.
```

## FLOOR() {#floor}

음의 무한대 방향으로 내림합니다.

```sql
SELECT FLOOR(-1.2), FLOOR(3.9), FLOOR(-3.0);
```

```sql
Mach> SELECT FLOOR(-1.2), FLOOR(3.9), FLOOR(-3.0);
FLOOR(-1.2)  FLOOR(3.9)  FLOOR(-3.0)
-----------------------------------------
-2            3           -3
[1] row(s) selected.
```

## CEIL() {#ceil}

양의 무한대 방향으로 올림합니다.

```sql
SELECT CEIL(-1.2), CEIL(3.2), CEIL(-3.0);
```

```sql
Mach> SELECT CEIL(-1.2), CEIL(3.2), CEIL(-3.0);
CEIL(-1.2)  CEIL(3.2)  CEIL(-3.0)
-------------------------------------
-1           4          -3
[1] row(s) selected.
```

## SIN() {#sin}

라디안 입력, 사인값 반환.

```sql
SELECT SIN(0), SIN(PI()/2), SIN(PI());
```

```sql
Mach> SELECT SIN(0), SIN(PI()/2), SIN(PI());
SIN(0)      SIN(PI()/2)   SIN(PI())
------------------------------------
0           1             0
[1] row(s) selected.
```

## SLOPE {#slope}

`SLOPE(y, x)`는 숫자형 `(x, y)` 점들에 대한 선형 회귀 직선의 기울기를 계산합니다.

```sql
SLOPE(y, x)
```

- 두 인자는 모두 숫자형이어야 합니다.
- `NULL` 값은 무시합니다.
- 유효한 데이터가 부족하거나 `x` 분산이 0이면 결과는 `NULL`입니다.
- 반환 타입은 `DOUBLE`입니다.

```sql
SELECT SLOPE(temp_c, sample_sec)
FROM sensor_log;
```

## COS() {#cos}

라디안 입력, 코사인값 반환.

```sql
SELECT COS(0), COS(PI()), COS(PI()/2);
```

```sql
Mach> SELECT COS(0), COS(PI()), COS(PI()/2);
COS(0)      COS(PI())   COS(PI()/2)
-------------------------------------
1           -1          0
[1] row(s) selected.
```

## TAN() {#tan}

라디안 입력, 탄젠트값 반환.

```sql
SELECT TAN(0), TAN(PI()/4), TAN(PI());
```

```sql
Mach> SELECT TAN(0), TAN(PI()/4), TAN(PI());
TAN(0)      TAN(PI()/4)  TAN(PI())
-----------------------------------
0           1            0
[1] row(s) selected.
```

## MOD() {#mod}

몫을 0으로 절사한 기준으로 나머지를 계산합니다.

```sql
SELECT MOD(10, 3), MOD(11, 4), MOD(-10, 3), MOD(3.5, 0.5);
```

```sql
Mach> SELECT MOD(10, 3), MOD(11, 4), MOD(-10, 3), MOD(3.5, 0.5);
MOD(10, 3)  MOD(11, 4)  MOD(-10, 3)  MOD(3.5, 0.5)
-------------------------------------------------------
1           3           -1           0
[1] row(s) selected.
```

## MODE {#mode}

`MODE(value)`는 입력 집합에서 가장 자주 나타나는 숫자 값을 반환합니다.

```sql
MODE(value)
```

- `value`는 숫자형이어야 합니다.
- `NULL` 값은 무시합니다.
- 최빈값이 여러 개면 더 작은 값을 반환합니다.
- 현재 구현의 반환 타입은 `DOUBLE`입니다.

```sql
SELECT MODE(alarm_code)
FROM event_log;
```

## P05 / P10 / P90 / P95 {#p05-p10-p90-p95}

자주 쓰는 분위값을 빠르게 표현할 수 있도록 준비된 정확 분위수 축약 함수입니다.

```sql
P05(value)
P10(value)
P90(value)
P95(value)
```

- `value`는 숫자형이어야 합니다.
- `NULL` 값은 무시합니다.
- 반환 타입은 `DOUBLE`입니다.

`P05`, `P10`, `P90`, `P95`는 각각 `PERCENTILE_CONT(value, 0.05)`, `0.10`, `0.90`, `0.95`와 같은 의미입니다.

```sql
SELECT P05(response_ms),
       P10(response_ms),
       P90(response_ms),
       P95(response_ms)
FROM web_log;
```

## PERCENTILE_CONT / PERCENTILE_DISC {#percentile_cont-percentile_disc}

이 함수들은 숫자형 입력에 대해 정확한 분위값을 계산하는 집계 함수입니다.

```sql
PERCENTILE_CONT(value, ratio)
PERCENTILE_DISC(value, ratio)
```

- `value`는 숫자형이어야 합니다.
- `ratio`는 `0.0` 이상 `1.0` 이하의 상수여야 합니다.
- `PERCENTILE_CONT`는 필요하면 인접한 정렬 값 사이를 보간합니다.
- `PERCENTILE_DISC`는 목표 순위에 해당하는 실제 관측값 중 하나를 선택합니다.
- 현재 구현에서 두 함수 모두 반환 타입은 `DOUBLE`입니다.

```sql
SELECT PERCENTILE_CONT(latency_ms, 0.95) AS pcont95,
       PERCENTILE_DISC(latency_ms, 0.95) AS pdisc95
FROM api_log;
```

## QUANTILE {#quantile}

`QUANTILE(value, ratio)`는 숫자형 입력에 대해 정확한 연속 분위값을 계산합니다.

```sql
QUANTILE(value, ratio)
```

- `value`는 숫자형이어야 합니다.
- `ratio`는 `0.0` 이상 `1.0` 이하의 상수여야 합니다.
- 반환 타입은 `DOUBLE`입니다.
- 현재 구현에서는 `PERCENTILE_CONT`와 같은 연속 분위수 계열에 속합니다.

```sql
SELECT QUANTILE(cpu_usage, 0.75)
FROM host_metric;
```

## RAND() {#rand}

난수 값을 생성합니다.

```sql
SELECT RAND(5) = RAND(5) AS same_seed, RAND(7) = RAND(8) AS diff_seed, RAND() = RAND() AS diff_default;
```

```sql
Mach> SELECT RAND(5) = RAND(5) AS same_seed, RAND(7) = RAND(8) AS diff_seed, RAND() = RAND() AS diff_default FROM m$sys_users WHERE name = 'SYS';
same_seed   diff_seed   diff_default
------------------------------------
1           0           0
[1] row(s) selected.
```

`RAND(seed)`는 같은 시드면 동일한 값이 나오며, `RAND()`는 세션 내부 상태를 기반으로 `[0,1)` 범위의 값을 생성합니다.

## REGEXP_LIKE

`REGEXP_LIKE`는 문자열이 정규식 패턴과 일치하는지 검사합니다. Boolean 값을 반환하며
주로 `WHERE` 절에서 사용합니다.

```sql
REGEXP_LIKE(source, pattern)
REGEXP_LIKE(source, pattern, match_param)
```

- `source`는 `VARCHAR`여야 합니다.
- `pattern`은 상수 `VARCHAR` 정규식이어야 합니다.
- `match_param`은 선택 항목이며 상수 `VARCHAR`여야 합니다. `c`는 대소문자를
  구분하고, `i`는 대소문자를 구분하지 않습니다. 기본값은 `c`입니다.

```sql
SELECT *
FROM sensor_text
WHERE REGEXP_LIKE(message, 'error|warn', 'i');
```

## REGEXP_INSTR

`REGEXP_INSTR`는 정규식과 일치하는 위치를 1부터 시작하는 값으로 반환합니다. 일치하는
값이 없으면 `0`을 반환합니다.

```sql
REGEXP_INSTR(source, pattern[, position[, occurrence[, return_pos[, match_param]]]])
```

- `source`는 `VARCHAR`여야 합니다.
- `pattern`은 상수 `VARCHAR` 정규식이어야 합니다.
- `position`과 `occurrence`는 `1` 이상의 상수 정수입니다.
- `return_pos`는 상수 정수입니다. `0`은 시작 위치를 반환하고, `1`은 일치한 문자열
  다음 위치를 반환합니다.
- `match_param`은 `c` 또는 `i`를 사용할 수 있습니다. 기본값은 `c`입니다.

```sql
SELECT REGEXP_INSTR('TechOnTheNet', 'The', 1, 1, 1, 'i');
```

## REGEXP_SUBSTR

`REGEXP_SUBSTR`는 정규식과 일치하는 부분 문자열을 반환합니다.

```sql
REGEXP_SUBSTR(source, pattern[, position[, occurrence[, match_param]]])
```

- `source`는 `VARCHAR`여야 합니다.
- `pattern`은 상수 `VARCHAR` 정규식이어야 합니다.
- `position`과 `occurrence`는 `1` 이상의 상수 정수입니다.
- `match_param`은 `c` 또는 `i`를 사용할 수 있습니다. 기본값은 `c`입니다.

```sql
SELECT REGEXP_SUBSTR('TechOnTheNet', 'a|e|i|o|u', 1, 2, 'i');
```

## REGEXP_REPLACE

`REGEXP_REPLACE`는 정규식과 일치하는 문자열을 치환합니다.

```sql
REGEXP_REPLACE(source, pattern[, replacement[, position[, occurrence[, match_param]]]])
```

- `source`는 `VARCHAR`여야 합니다.
- `pattern`과 `replacement`는 상수 `VARCHAR` 값이어야 합니다.
- `replacement`를 생략하면 일치하는 문자열을 제거합니다.
- `position`은 `1` 이상의 상수 정수입니다.
- `occurrence`는 상수 정수입니다. `0`은 모든 일치 항목을 치환하고, `0`보다 큰 값은
  해당 번째 일치 항목만 치환합니다.
- `match_param`은 `c` 또는 `i`를 사용할 수 있습니다. 기본값은 `c`입니다.

```sql
SELECT REGEXP_REPLACE('TechOnTheNet', 'a|e|i|o|u', 'Z', 1, 2, 'i');
```

<a id="support-type-of-built-in-function"></a>
## 내장 함수 지원 타입

| |Short|Integer|Long|Float|Double|Varchar|Text|Ipv4|Ipv6|Datetime|Binary|
|--|--|--|--|--|--|--|--|--|--|--|--|
|ABS|o|o|o|o|o|x|x|x|x|x|x|
|ADD_TIME|x|x|x|x|x|x|x|x|x|o|x|
|APPROX_PERCENTILE / APPROX_MEDIAN / APPROX_P05 / APPROX_P10 / APPROX_P90 / APPROX_P95|o|o|o|o|o|x|x|x|x|x|x|
|AREA|o|o|o|o|o|x|x|x|x|x|x|
|AVG|o|o|o|o|o|x|x|x|x|x|x|
|BITAND / BITOR|o|o|o|x|x|x|x|x|x|x|x|
|COUNT|o|o|o|o|o|o|x|o|o|o|x|
|CUME_DIST|o|o|o|o|o|x|x|x|x|x|x|
|DATE_TRUNC|x|x|x|x|x|x|x|x|x|o|x|
|DECODE|o|o|o|o|o|o|x|o|x|o|x|
|FIRST / LAST|o|o|o|o|o|o|x|o|o|o|x|
|FROM_UNIXTIME|o|o|o|o|o|x|x|x|x|x|x|
|FROM_TIMESTAMP|o|o|o|o|o|x|x|x|x|x|x|
|GROUP_CONCAT|o|o|o|o|o|o|x|o|o|o|x|
|INSTR|x|x|x|x|x|o|o|x|x|x|x|
|LEAST / GREATEST|o|o|o|o|o|o|x|x|x|x|x|
|LENGTH|x|x|x|x|x|o|o|x|x|x|o|
|LOWER|x|x|x|x|x|o|x|x|x|x|x|
|LPAD / RPAD|x|x|x|x|x|o|x|x|x|x|x|
|LTRIM / RTRIM|x|x|x|x|x|o|x|x|x|x|x|
|MAX|o|o|o|o|o|o|x|o|o|o|x|
|MEDIAN|o|o|o|o|o|x|x|x|x|x|x|
|MIX|o|o|o|o|o|o|x|o|o|o|x|
|MODE|o|o|o|o|o|x|x|x|x|x|x|
|NVL|x|x|x|x|x|o|x|o|x|x|x|
|P05 / P10 / P90 / P95|o|o|o|o|o|x|x|x|x|x|x|
|PERCENTILE_CONT / PERCENTILE_DISC|o|o|o|o|o|x|x|x|x|x|x|
|QUANTILE|o|o|o|o|o|x|x|x|x|x|x|
|REGEXP_LIKE|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_INSTR|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_SUBSTR|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_REPLACE|x|x|x|x|x|o|x|x|x|x|x|
|SLOPE|o|o|o|o|o|x|x|x|x|x|x|
|TOP_K|o|o|o|o|o|x|x|x|x|x|x|
|ROUND|o|o|o|o|o|x|x|x|x|x|x|
|ROWNUM|o|o|o|o|o|o|o|o|o|o|o|
|SERIESNUM|o|o|o|o|o|o|o|o|o|o|o|
|STDDEV / STDDEV_POP|o|o|o|o|o|x|x|x|x|x|x|
|SUBSTR|x|x|x|x|x|o|x|x|x|x|x|
|SUBSTRING_INDEX|x|x|x|x|x|o|o|x|x|x|x|
|SUM|o|o|o|o|o|x|x|x|x|x|x|
|SYSDATE / NOW|x|x|x|x|x|x|x|x|x|x|x|
|TO_CHAR|o|o|o|o|o|o|x|o|o|o|x|
|TO_DATE / TO_DATE_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_HEX|o|o|o|o|o|o|o|o|o|o|o|
|TO_INET_STR|x|x|x|x|x|x|x|o|x|x|x|
|TO_IPV4 / TO_IPV4_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_IPV6 / TO_IPV6_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_NUMBER / TO_NUMBER_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_TIMESTAMP|x|x|x|x|x|x|x|x|x|o|x|
|TRUNC|o|o|o|o|o|x|x|x|x|x|x|
|TS_CHANGE_COUNT|o|o|o|o|o|x|x|o|o|o|x|
|UNIX_TIMESTAMP|o|o|o|o|o|x|x|x|x|x|x|
|UPPER|x|x|x|x|x|o|x|x|x|x|x|
|VARIANCE / VAR_POP|o|o|o|o|o|x|x|x|x|x|x|
|YEAR / MONTH / DAY|x|x|x|x|x|x|x|x|x|o|x|
|ISNAN / ISINF|o|o|o|o|o|x|x|x|x|x|x|


<a id="json-related-function"></a>
## JSON 관련 함수

이 함수들은 JSON 데이터 타입을 인자로 사용합니다.

|함수명|설명|비고|
|--|--|--|
|JSON_EXTRACT(JSON column name, 'json path')|값을 문자열 타입으로 반환합니다.<br>(값이 없으면 ERROR를 반환합니다.)| - JSON object or array : 모든 객체를 문자열로 변환해 반환합니다.<br> - String type : 그대로 반환합니다.<br> - Numeric type : 문자열로 변환해 반환합니다.<br> - boolean type : \"True\" 또는 \"False\"를 반환합니다.|
|JSON_EXTRACT_DOUBLE(JSON column name, 'json path')|값을 64비트 double 타입으로 반환합니다.<br>(값이 없으면 NULL을 반환합니다.)| - JSON object or array : NULL을 반환합니다.<br> - String type : 변환 가능하면 변환해 반환하고, 불가능하면 NULL을 반환합니다.<br> - Numeric type : 64비트 실수로 반환합니다.<br> - boolean type : \"True\"는 1.0, \"False\"는 0.0으로 반환합니다.|
|JSON_EXTRACT_INTEGER(JSON column name, 'json path')|값을 64비트 정수 타입으로 반환합니다.<br>(값이 없으면 NULL을 반환합니다.)| - JSON object or array : NULL을 반환합니다.<br> - String type : 변환 가능하면 변환해 반환하고, 불가능하면 NULL을 반환합니다.<br> - Numeric type : 64비트 정수로 반환합니다.<br> - boolean type : \"True\"는 1, \"False\"는 0으로 반환합니다.|
|JSON_EXTRACT_STRING(JSON column name, 'json path')|값을 문자열 타입으로 반환합니다.<br>(값이 없으면 NULL을 반환합니다.)<br>연산자(→)와 동일한 결과를 반환합니다.| - JSON object or array : 모든 객체를 문자열로 변환해 반환합니다.<br> - String type : 그대로 반환합니다. <br> - Numeric type : 문자열로 변환해 반환합니다. <br> - boolean type : \"True\" 또는 \"False\"를 반환합니다.|
|JSON_SET(json_doc, path, scalar)|지정한 경로에 SQL scalar 값을 JSON scalar로 저장한 새 JSON 문서를 반환합니다.| - `path` 는 full JSONPath를 사용합니다.<br> - `NULL` 값은 JSON `null` 로 저장됩니다.<br> - object 경로만 지원합니다.|
|JSON_SET_JSON(json_doc, path, json_text)|지정한 경로에 JSON 문자열을 object 또는 array subtree로 저장한 새 JSON 문서를 반환합니다.| - `path` 는 full JSONPath를 사용합니다.<br> - 세 번째 인자가 SQL `NULL` 이면 결과는 SQL `NULL` 입니다.<br> - 유효하지 않은 JSON 문자열은 오류가 발생합니다.|
|JSON_REMOVE(json_doc, path)|지정한 경로의 멤버 또는 subtree를 제거한 새 JSON 문서를 반환합니다.| - `path` 는 full JSONPath를 사용합니다.<br> - 존재하지 않는 경로는 no-op 입니다.<br> - `JSON_REMOVE(..., '$')` 는 허용되지 않습니다.|
|JSON_IS_VALID('json string')|json 문자열이 형식에 맞는지 확인합니다.| - 0 : False<br> - 1 : True|
|JSON_TYPEOF(JSON column name, 'json path')|값의 타입을 반환합니다.| - None : 키가 존재하지 않음<br> - Object : Object 타입<br> - Integer : 정수 타입<br> - Real : 실수 타입<br> - String : 문자열 타입<br> - True/False : Boolean<br> - Array : Array 타입<br> - Null : NULL|

```sql
Mach> CREATE TABLE jsontbl (name VARCHAR(20), jval JSON);
Created successfully.

Mach> INSERT INTO jsontbl VALUES("name1", '{"name":"test1"}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name2", '{"name":"test2", "value":123}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name3", '{"name":{"class1": "test3"}}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name4", '{"myarray": [1, 2, 3, 4]}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name5", '{"name":"error"');
[ERR-02233: Error occurred at column (2): (Error in json load.)]

Mach> SELECT name, JSON_EXTRACT_STRING(jval, '$.name') FROM jsontbl;
name                  JSON_EXTRACT_STRING(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 {"class1": "test3"}
name2                 test2
name1                 test1
[4] row(s) selected.

Mach> SELECT name, JSON_EXTRACT_INTEGER(jval, '$.myarray[1]') FROM jsontbl;
name                  JSON_EXTRACT_INTEGER(jval, '$.myarray[1]')
--------------------------------------------------------------------
name4                 2
name3                 NULL
name2                 NULL
name1                 NULL
[4] row(s) selected.

Mach> SELECT name, JSON_TYPEOF(jval, '$.name') FROM jsontbl;
name                  JSON_TYPEOF(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 None
name3                 Object
name2                 String
name1                 String
[4] row(s) selected.
```


<a id="json-operator"></a>
## JSON 연산자

`->` 연산자는 JSON 데이터의 객체에 접근할 때 사용합니다.

JSON_EXTRACT_STRING 함수와 동일한 결과를 반환합니다.

```sql
json_col -> 'json path'
```

JSON 컬럼의 멤버 값은 JSONPath를 사용하는 `->` 연산자와 dot 축약 문법으로 접근할 수 있습니다.

```sql
-- JSONPath arrow 문법
jval->'$.sensor.temperature'

-- JSON dot 축약 문법
jval.sensor.temperature
```

두 표현식은 같은 JSON 값을 조회합니다. 기존 `->` 연산자는 계속 사용할 수 있으며, dot 문법은 같은 값을 더 짧게 표현하기 위한 추가 문법입니다.

```sql
Mach> SELECT name, jval->'$.name' FROM jsontbl;
name                  JSON_EXTRACT_STRING(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 {"class1": "test3"}
name2                 test2
name1                 test1
[4] row(s) selected.

Mach> SELECT name, jval->'$.myarray[1]' FROM jsontbl;
name                  JSON_EXTRACT_INTEGER(jval, '$.myarray[1]')
--------------------------------------------------------------------
name4                 2
name3                 NULL
name2                 NULL
name1                 NULL
[4] row(s) selected.

Mach> SELECT name, jval->'$.name.class1' FROM jsontbl;
name                  jval->'$.name.class1'
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 test3
name2                 NULL
name1                 NULL
[4] row(s) selected
```

### JSONPath arrow 문법

arrow 문법은 JSONPath 문자열을 사용합니다.

```sql
jval->'$.name'
jval->'$.sensor.temperature'
jval->'$.items[0].name'
```

대괄호를 사용해 JSON key를 직접 지정할 수도 있습니다. key 이름에 점(`.`)이 포함된 경우에는 대괄호 문법을 사용합니다.

```sql
-- key 이름이 a.b인 경우
jval->'$["a.b"]'
jval->'$[a.b]'

-- 여러 단계 key를 대괄호로 지정
jval->'$[Plant1][Line1][Temperature]'

-- 점이 포함된 하나의 key 이름
jval->'$[Plant1.Line1.Temperature]'
```

`$[Plant1.Line1.Temperature]`는 `Plant1.Line1.Temperature`라는 하나의 key를 찾습니다. `Plant1`, `Line1`, `Temperature`를 단계별 key로 찾으려면 `$[Plant1][Line1][Temperature]` 또는 `$.Plant1.Line1.Temperature`를 사용합니다.

key 이름에 특수 문자나 점이 포함된 경우에는 다음처럼 따옴표가 있는 bracket 문법을 권장합니다.

```sql
jval->'$["a.b"]["c.d"]["e.f"]'
```

다음 문법은 지원하지 않습니다.

```sql
jval->'$."a.b"'
```

### JSON dot 축약 문법

JSON 컬럼 뒤에 멤버 이름을 붙여 JSON 값을 조회할 수 있습니다.

```sql
-- 단일 멤버
jval.name

-- 중첩 멤버
jval.sensor.temperature

-- 배열 index
jval.items[0].name

-- 특수 문자가 포함된 key
jval.items[0]."product-id"
```

dot 문법에서 double quote로 감싼 key는 대소문자와 특수 문자를 그대로 사용합니다.

```sql
SELECT name, jval."Camel-Key", jval.items[0]."product-id"
  FROM jsontbl
 ORDER BY name;
```

### WHERE 절 타입 비교

JSON 멤버 접근 결과는 조회할 때 문자열처럼 표시됩니다. 그러나 `WHERE` 절에서 숫자 타입 값과 비교하면 JSON 값을 숫자로 파싱해 숫자 비교를 수행합니다.

```sql
SELECT name
  FROM jsontbl
 WHERE jval->'$.value' > 100
 ORDER BY name;

SELECT name
  FROM jsontbl
 WHERE jval.value BETWEEN 10 AND 30
 ORDER BY name;

SELECT name
  FROM jsontbl
 WHERE jval.value IN (10, 20, 30)
 ORDER BY name;
```

지원되는 비교는 다음과 같습니다.

- JSON integer 값과 SQL integer 값 비교
- JSON real/double 값과 SQL numeric 값 비교
- JSON 숫자 문자열과 SQL numeric 값 비교
- JSON boolean 값과 문자열 `'true'`, `'false'` 비교
- `=`, `<>`, `<`, `<=`, `>`, `>=`, `BETWEEN`, literal `IN (...)`

SQL integer 값과 비교하는 경우 JSON integer는 정수로 비교하므로 `9007199254740992`와 `9007199254740993`처럼 double 정밀도 범위를 넘는 값도 서로 다른 값으로 비교할 수 있습니다.

문자 타입 값과 비교하면 기존처럼 문자열 비교를 수행합니다.

```sql
SELECT name
  FROM jsontbl
 WHERE jval->'$.name' = 'test1'
 ORDER BY name;
```

숫자 비교에서 JSON 값이 숫자로 해석될 수 없으면 조건에 매칭되지 않습니다. 오류로 처리하지 않습니다. 일반 `VARCHAR` 컬럼과 숫자 값의 비교 정책은 변경되지 않으며, 숫자 자동 비교는 JSON 멤버 접근식에만 적용됩니다.

### 이름 해석 규칙

일반 SQL의 컬럼 이름 해석이 JSON dot 해석보다 우선합니다.

```sql
SELECT t.jval.name
  FROM jsontbl t;
```

위 표현식은 먼저 일반 컬럼 이름으로 해석을 시도합니다. 일반 컬럼으로 해석되지 않고 `jval`이 JSON 컬럼이면 `jval.name`을 JSON 멤버 접근으로 처리합니다.

JSON dot 접근은 JSON 컬럼을 기준으로만 사용할 수 있습니다.

```sql
-- 지원하지 않음
(jval->'$.sensor').temperature
name.member
```

### 제한 사항

다음 문법은 지원하지 않습니다.

- wildcard: `jval.items[*].name`
- recursive descent: `jval..name`
- filter expression: `jval.items[?(@.price > 10)]`
- negative array index: `jval.items[-1]`
- single quoted key: `jval.'product-id'`
- dot 문법과 arrow 문법 혼합: `jval.items->'$.name'`
- JSON 컬럼이 아닌 컬럼의 dot 접근: `name.member`
- 임의 expression 뒤의 dot 접근: `(jval->'$.sensor').temperature`
- quoted member arrow path: `jval->'$."a.b"'`

`IN (SELECT ...)` 형태의 subquery `IN`에서는 JSON 멤버 값의 숫자 자동 비교를 지원하지 않습니다. literal `IN (...)`을 사용합니다.

<a id="window-function"></a>
## 윈도우 함수

윈도우 함수는 행 간 비교, 연산, 정의를 위한 함수이며 분석 함수 또는 랭킹 함수라고도 합니다.

SELECT 문에서만 사용할 수 있습니다.

### 윈도우 함수 구문

윈도우 함수는 반드시 OVER 절을 포함합니다.

```
WINDOW_FUNCTION (ARGUMENTS) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

* WINDOW_FUNCTION: 윈도우 함수 이름
* ARGUMENTS: 함수에 따라 0~N개의 인자를 지정할 수 있습니다.
* PARTITION BY clause: 전체 집합을 기준에 따라 작은 그룹으로 나눕니다. (생략 가능)
* ORDER BY clause: 정렬 기준이 되는 ORDER BY 절을 지정합니다. (생략 가능)

### 윈도우 함수 목록

#### LAG

파티션별 윈도우에서 이전 N번째 행의 값을 가져옵니다.

가져올 행이 없으면 NULL을 반환합니다.

```
LAG(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE TABLE lag_table (name varchar(10), dt datetime, value INTEGER);
Created successfully.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-01'), 1);
1 row(s) inserted.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-02'), 2);
1 row(s) inserted.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-03'), 3);
1 row(s) inserted.

-- Divide the set by name, sort by dt, and retrieve the first previous value.
Mach> SELECT name, dt, value, LAG(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lag_table;
name        dt                              value       LAG(value, 1)
---------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           NULL
name1       2024-01-02 00:00:00 000:000:000 2           1
name1       2024-01-03 00:00:00 000:000:000 3           2
[3] row(s) selected.
```


#### LEAD

파티션별 윈도우에서 N번째 다음 행의 값을 가져옵니다.

가져올 행이 없으면 NULL을 반환합니다.

```
LEAD(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE TABLE lead_table (name varchar(10), dt datetime, value INTEGER);
Created successfully.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-01'), 1);
1 row(s) inserted.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-02'), 2);
1 row(s) inserted.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-03'), 3);
1 row(s) inserted.

-- Divide the set by name, sort by dt, and retrieve the first and subsequent values.
Mach> SELECT name, dt, value, LEAD(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lead_table;
name        dt                              value       LEAD(value, 1)
----------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           2
name1       2024-01-02 00:00:00 000:000:000 2           3
name1       2024-01-03 00:00:00 000:000:000 3           NULL
[3] row(s) selected.
```


#### NTILE

`NTILE(n)`은 정렬된 행을 가능한 균등하게 `n`개의 버킷으로 나누고, 각 행이 속한 버킷 번호를 반환합니다.

```
NTILE(n) OVER ([PARTITION BY column_name] ORDER BY column_name)
```

- `n`은 양의 상수여야 합니다.
- `OVER (...)` 안의 `ORDER BY`는 필수입니다.
- 행 수가 균등하게 나누어지지 않으면 앞쪽 버킷이 한 행씩 더 가집니다.

```
Mach> SELECT user_id,
             score,
             NTILE(4) OVER (ORDER BY score) AS score_band
      FROM exam_result;
```
