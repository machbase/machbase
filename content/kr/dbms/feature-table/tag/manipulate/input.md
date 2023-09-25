---
title : '태그 데이터의 입력'
type: docs
weight: 10
---

태그 데이터를 입력하기 위해서는 아래와 같은 다양한 방법을 활용할 수 있다.

## INSERT 구문을 통해 입력하기

가장 간단한 방법으로 아래와 같이 INSERT 구문을 통해 입력할 수 있다.

간단하게 테스트 용도로 할 수 있는 방법이고, 만일 대량의 데이터를 빨리 넣고자 할 경우에는 다른 방법을 활용한다.

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);
Executed successfully.
 
Mach>  insert into tag metadata values ('TAG_0001');
1 row(s) inserted.
 
Mach> insert into tag values('TAG_0001', now, 0);
1 row(s) inserted.
 
Mach> insert into tag values('TAG_0001', now, 1);
1 row(s) inserted.
 
Mach> insert into tag values('TAG_0001', now, 2);
1 row(s) inserted.
 
Mach> select * from tag where name = 'TAG_0001';
NAME                  TIME                            VALUE                      
--------------------------------------------------------------------------------------
TAG_0001              2018-12-19 17:41:37 806:901:728 0                          
TAG_0001              2018-12-19 17:41:42 327:839:368 1                          
TAG_0001              2018-12-19 17:41:43 812:782:202 2                          
[3] row(s) selected.
```

위와 같이 3개의 TAG 값을 현재의 시간으로 넣어 보았다.

## CSV 파일을 통해 한꺼번에 로딩하기

마크베이스는 csvimport 라는 도구를 통해서 CSV 파일 대량으로 로딩할 수 있도록 해 준다.

더 자세한 내용은 실제 예제를 통해서 파악할 수 있으며, 아래에 간단하게 기술한다.

### CSV 파일 형태 (data.csv)

```
TAG_0001, 2009-01-28 07:03:34 0:000:000, -41.98
TAG_0001, 2009-01-28 07:03:34 1:000:000, -46.50
TAG_0001, 2009-01-28 07:03:34 2:000:000, -36.16
....
```

위와 같이 <태그명, 시간, 값> 으로 구성된 csv 파일 준비한다.

물론, 태그명 TAG_0001이 존재해야 한다.
```

### 로딩 프로그램 csvimport  사용

```bash
csvimport -t TAG -d data.csv -F "time YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" -l error.log
```

TAG라는 테이블에 data.csv를 로딩한다.

그리고, -F 옵션은 data.csv에 저장된 시간 포맷을 지정하는 것인데, 현재 파일은 나노 단위까지 값을 넣을 수 있도록 되어 있다.

또한, -l error.log 는 입력시 발생한 에러에 대해 별도의 파일로 기록하는 것이다.

## RESTful API를 통해 입력하기

RESTful API의 더 자세한 사용법은 다음의 활용 예제를 참고하도록 한다.


### 입력 API 문법

마크베이스는 다음과 같이 RESTful API를 제공한다.

```
{
 "values":[
     [TAG_NAME, TAG_TIME, VALUE],  # 태그명,시간,값을 입력한다. TAG 형태에 따라 부가 컬럼 추가 필요
     [ .... ]....
 ],
 "date_format":"Date Format"       # date_format은 생략시 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn' 로 설정된다.
}
```

정의된 TAG 스키마의  컬럼 갯수만큼의 값을 위의 구조와 일치되도록 요청한다.


## SDK를 통해 데이터 입력하기

마크베이스는 아래와 같은 다양한 언어의 표준 개발 툴을 제공하고 있다.

* [C/C++ library](/kr/dbms/sdk/cli_odbc)
* [Java library](/kr/dbms/sdk/jdbc)
* [Python library](/kr/dbms/sdk/python)
* [C# library](/kr/dbms/sdk/dotnet)

이러한 라이브러리를 통해서 사용자는 자신의 환경에 따라 다양한 형태의 응용 프로그램을 작성하여 마크베이스에 대한 데이터 입력이 가능하다.

