---
title : 'Python'
type : docs
weight: 30
---

## Python 모듈 사용 개요

마크베이스에서는 Python 모듈을 지원한다. 모듈을 설치함으로써 마크베이스 서버와 CLI 방식으로 값을 주고 받을 수 있는 클래스를 제공한다. 이를 활용해서 Python에서 쉽게 마크베이스에 질의 형태로 값을 입력하거나 삭제, 테이블 생성, 삭제 등 다양한 명령어를 사용할 수 있다.

## 사용 환경 설정

**리눅스**

이를 사용하기 위해서는 간단한 환경 설정과 라이브러리 파일들이 필요하다. 먼저 $LD_LIBRARY_PATH에 $MACHBASE_HOME/lib 디렉터리가 등록되어있는지 확인한다. CLI를 이용해서 마크베이스에 접속하기 때문에 `libmachbasecli_dll.so` 파일이 라이브러리 폴더에 존재해야 한다. 그리고 $MACHBASE_HOME/3rd-party/python3-module 폴더에 있는 machbaseAPI-1.0.tar.gz를 압축 해제후 `python setup.py install` 명령을 통해 사용하려는 Python에 모듈을 설치한다.

**윈도우**

먼저 %MACHBASE_HOME%/3rd-party/python3-module 폴더에 있는 machbaseAPI-1.0.zip을 압축 해제 후 `python setup.py install` 명령을 통해 사용하려는 Python에 모듈을 설치한다.

## Class 생성

마크베이스 Python 모듈을 사용하기 위해서 해당 클래스를 선언해야 한다.

해당 클래스 명은 machbase이다.

```python
from machbaseAPI import machbase
```

## 접속과 접속해제

### machbase.open(aHost, aUser, aPw, aPort)

마크베이스에 접속하는 함수이다. 알맞은 파라미터 값을 입력했을시에 DB에 접속 성공했는지 실패했는지를 반환한다. 정상 종료시 1, 실패시 0을 반환한다.

### machbase.close()

마크베이스 접속을 해제하는 함수이다. 정상 종료시 1, 실패시 0을 반환한다.

### machbase.isConnected()

선언한 클래스가 해당 서버에 접속중인지 아닌지를 판별하는 함수이다. 접속 중일 때 1, 접속 중이 아닐 때 0을 반환한다.

## 명령어 실행 및 사용자 편의 함수

### machbase.execute(aSql)

서버에 접속되어 있을 때 해당 서버에 질의문을 전송하는 명령어이다. 정상적으로 실행되었을 때 1, 실패하거나 에러가 발생했을 시에는 0을 반환한다.

마크베이스에서 지원하지 않는 UPDATE를 제외하고 모든 명령어들을 사용할 수 있다.

결과를 한꺼번에 return하는 구조이기 때문에 SELECT 구문을 사용하는 경우 메모리 부족 오류가 발생할 수 있다. 따라서 SELECT 구문은 machbase.select() 함수를 사용한다.

### machbase.append(aTableName, aTypes, aValues, aFormat)

마크베이스에서 지원하는 Append 프로토콜을 사용할 수 있는 함수이다.

데이터를 입력하게 될 테이블명, 각 컬럼들의 타입의 딕셔너리, 그리고 입력할 값들을 JSON 형태로 입력하고 dateformat을 지정해 주면 Append를 실행할 수 있다.

정상적으로 실행하였다면 1, 실패시에는 0을 반환한다.

|  타입명  |  값 |
|:--------:|:---:|
| short    | 4   |
| ushort   | 104 |
| integer  | 8   |
| uinteger | 108 |
| long     | 12  |
| ulong    | 112 |
| float    | 16  |
| double   | 20  |
| datetime | 6   |
| varchar  | 5   |
| ipv4     | 32  |
| ipv6     | 36  |
| text     | 49  |
| binary   | 97  |


### machbase.tables()

접속한 서버에 있는 모든 테이블들의 정보를 반환한다. 정상적으로 실행되었다면 1, 실패했을 시에는 0을 반환한다.

### machbase.columns(aTableName)

접속한 서버에 있는 해당 테이블 내의 컬럼들의 정보를 반환한다. 정상적으로 실행되었다면 1, 실패했을 시에는 0을 반환한다.

## 결과 확인

마크베이스 Python 모듈에서 모든 결과값은 JSON으로 반환된다.

다양한 환경에서 활용하기 쉬운 형태의 결과를 반환하는 것으로 채택하였다.

### machbase.result()

위쪽에서 설명하였던 함수들은 실행 결과들을 해당 함수의 반환값으로 나타내지 않고 성공, 실패 여부만 반환한다. 함수들의 결과값은 이 함수의 반환값으로만 얻을 수 있다.

## SELECT 결과 확인

machbase.execute() 함수로 SELECT 결과를 읽어오면 모든 결과를 한번에 읽기때문에 많은 메모리가 필요하며 경우에 따라서 메모리 부족 오류가 발생할 수 있다.

따라서 SELECT 구문의 경우에는 한 레코드씩 결과를 얻을 수 있는 함수를 사용해야 한다.

### machbase.select(aSql)

서버에 접속되어 있을 때 해당 서버에 SELECT 질의문을 전송하는 명령어이다. 정상적으로 실행되었을 때 1, 실패하거나 에러가 발생했을 시에는 0을 반환한다.

SELECT 구문만 사용이 가능하며, 모든 결과를 한번에 가져오는 machbase.execute() 함수와 달리 machbase.fetch()함수를 사용해서 1 레코드 씩 결과를 얻을 수 있다.

### machbase.fetch()

machbase.select(aSql) 함수의 결과를 한 레코드 씩 읽어온다.

return 값은 성공여부와 결과값으로 성공여부는 1과 0으로 표시되고, 결과값은 한 레코드의 결과가 json 형식으로 return 된다.

### machbase.selectClose()

한번 선택된 machbase.select()의 결과는 다른 machbase.select()나 machbase.execute() 함수가 호출될 때까지 open된 상태로 존재한다.

이 것을 명시적으로 닫아주는 것이 machbase.selectClose() 함수이다.

### machbase.select() 예제

```python
db = machbase()
if db.open('127.0.0.1','SYS','MANAGER', 5656) is 0 :
    return db.result()
 
query = 'SELECT * from sample_table'
while True:
    is_success, result = db.fetch()
    if is_success is 0:
        break;
 
    res = json.loads(result)
 
db.selectClose()
if db.close() is 0 :
    return db.result()
```
## 예제

간단한 예제들을 통해서 마크베이스 Python 모듈을 사용하는 방법을 알아보자

$MACHBASE_HOME/sample/python 파일들을 이용해서 확인할 수 있다. 해당 디렉터리에는 간편하게 테스트를 해 볼 수 있게 해주는 Makefile과 데이터를 만들어주는 MakeData.py 파일이 있다. Makefile 내부 변수 중 PYPATH의 값을 마크베이스 Python 모듈이 설치된 파이썬으로 지정해야 정상 작동한다. 기본값은 마크베이스 패키지에 설치된 파이썬으로 지정되어 있다. 또한 파이썬에서 모듈을 독자적으로 실행하기 위해서는 __init__.py 파일이 필요하므로 해당 디렉터리에 파일이 존재하는지 확인하도록 하다.

```bash
[mach@localhost]$ cd $MACHBASE_HOME/sample/python
[mach@localhost python]$ ls -l
total 20
-rw-rw-r-- 1 mach mach    0 Oct  7 14:37 __init__.py
-rw-rw-r-- 1 mach mach  764 Oct  7 14:37 MakeData.py
-rw-rw-r-- 1 mach mach  593 Oct  7 14:58 Makefile
-rw-rw-r-- 1 mach mach  664 Oct  7 14:37 Sample1Connect.py
-rw-rw-r-- 1 mach mach 2401 Oct  7 14:37 Sample2Simple.py
-rw-rw-r-- 1 mach mach 1997 Oct  7 14:37 Sample3Append.py
```

### Connect

아래의 예제는 서버에 접속해서 질의를 실행하고 결과값을 반환하는 단순한 함수이다. 각각의 함수들이 실패(0)를 반환했을 때에 결과값을 반환하는 경우는 에러 결과를 반환하기 위함이다. 정상적으로 실행된다면 m$tables 테이블의 값들 개수가 반환 된다.

파일 이름은 Sample1Connect.py이다.

```python
from machbaseAPI import machbase
def connect():
    db = machbase()
    if db.open('127.0.0.1','SYS','MANAGER',5656) is 0 :
        return db.result()
    if db.execute('select count(*) from m$tables') is 0 :
        return db.result()
    result = db.result()
    if db.close() is 0 :
        return db.result()
    return result
if __name__=="__main__":
    print connect()
```

```bash
[mach@localhost python]$ make run_sample1
/home/machbase/machbase_home/webadmin/flask/Python/bin/python Sample1Connect.py
{"count(*)":"13"}
```

### Simple

아래 예제를 이용해서 단순하게 마크베이스에 파이썬을 이용해서 테이블을 만들고 값을 입력하고 입력된 값을 추출해서 확인하는 예제이다. 파일 이름은 Sample2Simple.py이다.

```python
import re
import json
from machbaseAPI import machbase
def insert():
    db = machbase()
    if db.open('127.0.0.1','SYS','MANAGER',5656) is 0 :
        return db.result()
    db.execute('drop table sample_table')
    db.result()
    if db.execute('create table sample_table(d1 short, d2 integer, d3 long, f1 float, f2 double, name varchar(20), text text, bin binary, v4 ipv4, v6 ipv6, dt datetime)') is 0:
        return db.result()
    db.result()
    for i in range(1,10):
        sql = "INSERT INTO SAMPLE_TABLE VALUES ("
        sql += str((i - 5) * 6552) #short
        sql += ","+ str((i - 5) * 42949672) #integer
        sql += ","+ str((i - 5) * 92233720368547758L) #long
        sql += ","+ "1.234"+str((i-5)*7) #float
        sql += ","+ "1.234"+str((i-5)*61) #double
        sql += ",'id-"+str(i)+"'" #varchar
        sql += ",'name-"+str(i)+"'" #text
        sql += ",'aabbccddeeff'" #binary
        sql += ",'192.168.0."+str(i)+"'" #ipv4
        sql += ",'::192.168.0."+str(i)+"'" #ipv6
        sql += ",TO_DATE('2015-08-0"+str(i)+"','YYYY-MM-DD')" #date
        sql += ")";
        if db.execute(sql) is 0 :
            return db.result()
        else:
            print db.result()
        print str(i)+" record inserted."
    query = "SELECT d1, d2, d3, f1, f2, name, text, bin, to_hex(bin), v4, v6, to_char(dt,'YYYY-MM-DD') as dt from SAMPLE_TABLE";
    if db.execute(query) is 0 :
        return db.result()
    result = db.result()
    for item in re.findall('{[^}]+}',result):
        res = json.loads(item)
        print "d1 : "+res.get('d1')
        print "d2 : "+res.get('d2')
        print "d3 : "+res.get('d3')
        print "f1 : "+res.get('f1')
        print "f2 : "+res.get('f2')
        print "name : "+res.get('name')
        print "text : "+res.get('text')
        print "bin : "+res.get('bin')
        print "to_hex(bin) : "+res.get('to_hex(bin)')
        print "v4 : "+res.get('v4')
        print "v6 : "+res.get('v6')
        print "dt : "+res.get('dt')
    if db.close() is 0 :
        return db.result()
    return result
if __name__=="__main__":
    print insert()
```

```bash
[mach@loclahost python]$ make run_sample2
/home/machbase/machbase_home/webadmin/flask/Python/bin/python Sample2Simple.py
{"EXECUTE RESULT":"Execute Success"}
1 record inserted.
{"EXECUTE RESULT":"Execute Success"}
2 record inserted.
{"EXECUTE RESULT":"Execute Success"}
3 record inserted.
{"EXECUTE RESULT":"Execute Success"}
4 record inserted.
{"EXECUTE RESULT":"Execute Success"}
5 record inserted.
{"EXECUTE RESULT":"Execute Success"}
6 record inserted.
{"EXECUTE RESULT":"Execute Success"}
7 record inserted.
{"EXECUTE RESULT":"Execute Success"}
8 record inserted.
{"EXECUTE RESULT":"Execute Success"}
9 record inserted.
d1 : 26208
d2 : 171798688
d3 : 368934881474191032
f1 : 1.23428
f2 : 1.23424
name : id-9
text : name-9
bin : 616162626363646465656666
to_hex(bin) : 616162626363646465656666
v4 : 192.168.0.9
v6 : ::192.168.0.9
...
```

### Append

마크베이스에서 고속으로 데이터를 입력할 수 있는 Append 방식 또한 파이썬 모듈을 활용해서 사용할 수 있다. 아래의 예제는 고속으로 데이터를 입력하는 예제이다. 컬럼 정보 및 초기화를 위한 접속 클래스 db, Append를 하기 위한 접속용 클래스 db2를 선언하여 각각의 함수를 활용하는 방식을 사용했다. 파일 이름은 Sample3Append.py이다.

```python
import re
import json
from machbaseAPI import machbase
def append():
#init,columns start
    db = machbase()
    if db.open('127.0.0.1','SYS','MANAGER',5656) is 0 :
        return db.result()
    db.execute('drop table sample_table')
    db.result()
    if db.execute('create table sample_table(d1 short, d2 integer, d3 long, f1 float, f2 double, name varchar(20), text text, bin binary, v4 ipv4, v6 ipv6, dt datetime)') is 0:
        return db.result()
    db.result()
    tableName = 'sample_table'
    db.columns(tableName)
    result = db.result()
    if db.close() is 0 :
        return db.result()
#init, colums end
#append start
    db2 = machbase()
    if db2.open('127.0.0.1','SYS','MANAGER',5656) is 0 :
        return db2.result()
    types = []
    for item in re.findall('{[^}]+}',result):
        types.append(json.loads(item).get('type'))
    values = []
    with open('data.txt','r') as f:
        for line in f.readlines():
            v = []
            i = 0
            for l in line[:-1].split(','):
                t = int(types[i])
                if t == 4 or t == 8 or t == 12 or t == 104 or t == 108 or t == 112:
                    #short   integer    long       ushort      uinteger     ulong
                    v.append(int(l))
                elif t == 16 or t == 20:
                    #float      double
                    v.append(float(l))
                else:
                    v.append(l)
                i+=1
            values.append(v)
    db2.append(tableName, types, values, 'YYYY-MM-DD HH24:MI:SS')
    result = db2.result()
    if db2.close() is 0 :
        return db2.result()
#append end
    return result
if __name__=="__main__":
    print append()
```

```bash
[mach@localhost python]$ make run_sample3
/home/machbase/machbase_home/webadmin/flask/Python/bin/python Sample3Append.py
{"EXECUTE RESULT":"Append success"}
```
