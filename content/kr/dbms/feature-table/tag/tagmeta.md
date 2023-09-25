---
title : '태그 메타(태그 이름) 관리'
type: docs
weight: 20
---

## 태그 메타의 개념

태그 메타는 마크베이스에서 저장될 임의의 태그가 가질 이름과 부가 정보를 나타낸다.

즉, 특정 장비에 존재하는 태그가 3개라고 한다면, 이 태그를 나타내는 임의의 이름과 관련 부가 정보가 필요한데, 이것을 모두 태그의 메타 정보라고 한다.

이 태그 메타는 최소한 이름이 존재할 수 있으며,  부가적으로 필요하다면 해당 장비에 맞는 다양한 종류의 데이터 타입을 지정할 수 있도록 되어 있다.

## 이름만으로 이뤄진 태그 메타

### 태그 메타의 생성

아래는 가장 기본적인 태그 메타가 생성되는 TAG 테이블의 생성 명령어이다.

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);
Mach> desc tag;
[ COLUMN ]                             
----------------------------------------------------------------
NAME                          TYPE                LENGTH       
----------------------------------------------------------------
NAME                          varchar             20                 
TIME                          datetime            31             
VALUE                         double              17
```

위는 기본적인 TAG 테이블을 생성한 것이며, 태그 메타에 대한 별도의 정보는 보이지 않는다.

이 경우 태그 메타는 VARCHAR(20)의 기본적인 이름만을 가진다.

### 태그 메타의 입력

이제 TAG1 이라는 이름을 갖는 하나의 태그 정보를 입력해 보자.

```sql
Mach> insert into tag metadata values ('TAG_0001');
1 row(s) inserted.
```

위의 질의를 통해서 TAG_0001 이라는 이름을 갖는 하나의 태그를 생성하였다.

### 태그 메타의 출력

마크베이스에서는 입력된 태그 메타의 정보를 확인하기 위한 특별한 테이블인 \_tag\_meta 를 제공한다.

따라서, 사용자는 다음과 같은 질의를 통해서 마크베이스에 입력된 모든 태그의 정보를 확인할 수 있다.

```sql
Mach> select * from _tag_meta;
ID                   NAME                 
----------------------------------------------
1                    TAG_0001             
[1] row(s) selected.
```

위의 질의를 통해서 TAG_0001 이라는 NAME을 갖는 하나의 태그를 생성하였다.

ID는 내부적으로 관리되는 값으로서 자동으로 부여된다.

### 태그 메타의 수정

마크베이스는 입력된 태그 메타 정보를 수정할 수 있도록 해 주는데, 다음과 같이 이름이 수정 가능하다.

```sql
Mach> update tag metadata set name = 'NEW_0001' where NAME = 'TAG_0001';
1 row(s) updated.
 
Mach> select * from _tag_meta;
ID                   NAME                 
----------------------------------------------
1                    NEW_0001             
[1] row(s) selected.
```

위와 같이 이름이 TAG_0001에서 NEW_0001로 수정된 것을 확인할 수 있다.

### 태그 메타의 삭제

아래와 같이 실제 태그 메타의 정보를 삭제할 수 있다.

```sql
Mach> delete from tag metadata where name = 'NEW_0001';
1 row(s) deleted.
 
Mach> select * from _tag_meta;
ID                   NAME                 
----------------------------------------------
[0] row(s) selected.
```

주의할 점은 태그 테이블에 실제 데이터가 해당 태그 메타를 참조하지 않을 때 태그 메타 삭제가 가능하다.

## 추가 정보를 갖는 태그 메타

### 태그 메타의 생성

아래는 태그 메타의 정보에 16비트 정수와 시간 그리고, IPv4 의 정보를 부가적으로 더 추가해서 만들어 본다.

주의할 점은 일단 생성된 태그 메타에 대해 값은 수정할 수 있지만, 그 구조는 수정할 수 없다는 것이다.

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized)
metadata (type short, create_date datetime, srcip ipv4) ;
 
Mach> desc tag;
[ COLUMN ]                             
----------------------------------------------------------------
NAME                          TYPE                LENGTH       
----------------------------------------------------------------
NAME                          varchar             20                 
TIME                          datetime            31             
VALUE                         double              17                 
[ META-COLUMN ]                             
----------------------------------------------------------------
NAME                          TYPE                LENGTH       
----------------------------------------------------------------
TYPE                          short               6              
CREATE_DATE                   datetime            31             
SRCIP                         ipv4                15   
```

### 태그 메타의 입력

이름 뿐만 아니라 부가 정보가 있는 상태에서 아래와 같이 입력해서 정보를 확인할 수 있다.

```sql
Mach> insert into tag metadata(name) values ('TAG_0001');
1 row(s) inserted.
 
Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP          
-------------------------------------------------------------------------------------------------------------
1                    TAG_0001              NULL        NULL                            NULL           
[1] row(s) selected.
```

위와 같이 NAME 외 다른 컬럼에는 NULL이 입력된 것을 알 수 있다.

이제 부가 정보를 아래와  같이 더 넣어 보자.

```sql
Mach> insert into tag metadata values ('TAG_0002', 99, '2010-01-01', '1.1.1.1');
1 row(s) inserted.
 
Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP          
-------------------------------------------------------------------------------------------------------------
1                    TAG_0001              NULL        NULL                            NULL           
2                    TAG_0002              99          2010-01-01 00:00:00 000:000:000 1.1.1.1        
[2] row(s) selected.
```

부가 정보를 위와 같이 넣었고, 각 태그 메타가 주어진 풍부한 정보를 가질 수 있게 되었다.

### 태그 메타의 수정

이제 TAG_0001의 타입을 NULL에서 11로 수정해 보자.

```sql
Mach> update tag metadata set type = 11 where name = 'TAG_0001';
1 row(s) updated.
 
Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP          
-------------------------------------------------------------------------------------------------------------
2                    TAG_0002              99          2010-01-01 00:00:00 000:000:000 1.1.1.1        
1                    TAG_0001              11          NULL                            NULL           
[2] row(s) selected.
```

위와 같이 수정되었다.

즉,  UPDATE 구문을 통해 모든 필드의 값을 수정할 수 있다.

단, 반드시 WHERE 절에 NAME이 지정되어야 하는 것은 공통적인 제약 사항이다.

## RESTful API를 통한 태그 메타 조회

### 모든 태그 리스트 얻기

아래는 마크베이스 포함된 모든 태그의 리스트를 얻는 예제이다.

```bash
Host:~$ curl  -G  "http://192.168.0.148:5001/machiot-rest-api/tags/list"
{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"NAME": "TAG_0001"},
          {"NAME": "TAG_0002"}]}
Host:~$
```

### 특정 태그의 시간 범위 얻기

아래는 원하는 태그가 가지고 있는 데이터의 최소 및 최대 시간 범위를 얻는 예제이다.

이기능은 특정 태그의 차트를 그릴 때 매우 유용하다.

#### 문법

```
{MWA URL}/machiot-rest-api/tags/range/  # Time Range of whole DB
{MWA URL}/machiot-rest-api/tags/range/{TagName}  # Time Range of a specific Tag
```

#### 전체 시간 범위

```
Host:~$ curl  -G  "http://192.168.0.148:5001/machiot-rest-api/tags/range/"
{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"MAX": "2018-02-10 10:00:00 000:000:000", "MIN": "2018-01-01 01:00:00 000:000:000"}]}
```

#### 특정 태그의 시간 범위

```
Host:~$ curl  -G  "http://192.168.0.148:5001/machiot-rest-api/tags/range/TAG_0001"
{"ErrorCode": 0, "ErrorMessage": "", "Data": [{"MAX": "2018-01-10 10:00:00 000:000:000", "MIN": "2018-01-01 01:00:00 000:000:000"}]}
Host:~$
Host:~$ curl  -G  "http://192.168.0.148:5001/machiot-rest-api/tags/range/TAG_0002"
{"ErrorCode": 0, "ErrorMessage": "", "Data": [{"MAX": "2018-02-10 10:00:00 000:000:000", "MIN": "2018-02-01 01:00:00 000:000:000"}]}
```
