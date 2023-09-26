---
title : Python
type : docs
weight: 30
---

## Python Module Usage Overview

Machbase supports Python modules. By installing the module, it provides a class that can exchange values ​​with the Machbase server and the CLI method. You can use this to easily enter and delete values ​​in the query base in Python, create and delete tables, and so on.


## Preferences

Linux Platform

Simple configuration and library files are required to use this. First, make sure that $MAC_LIBRARY_PATH is registered in the $MACHBASE_HOME/lib directory. The `libmachbasecli_dll.so` file must exist in the library folder because you are accessing Machbase using the CLI. Then unzip machbaseAPI-1.0.tar.gz in the $MACHBASE_HOME/3rd-party/python3-module folder and install the module into the Python you want to use via the `python setup.py install` command.

Windows Platform

First, unzip machbaseAPI-1.0.zip in the %MACHBASE_HOME%/3rd-party/python3-module directory, and execute `python setup.py install` command to install the module into the Python.

## Creating Class
To use the Machbase Python module, you need to declare the class.

The class name is machbase.

```py
from machbaseAPI import machbase
```
 

## Connection and Disconnection

### machbase.open(aHost, aUser, aPw, aPort)

This is a function to connect to Machbase. When the appropriate parameter value is input, it returns whether connection to the DB is successful or failed. Returns 1 on success and 0 on failure.

### machbase.close()

This is a function to close the Machbase connection. Returns 1 on success and 0 on failure.

### machbase.isConnected()

This is a function that determines whether the declared class is connected to the server. Returns 1 when connected and 0 when not connected.


## Executing Commands and User Convenience Functions

### machbase.execute(aSql)

This is a command to send a query to the server when it is connected to the server. It returns 1 when it is normally executed, and 0 when it fails or an error occurs.

You can use any command except UPDATE which is not supported by Machbase.

### machbase.append(aTableName, aTypes, aValues, aFormat)
This is a function that can use Append protocol supported by Machbase.

Append can be executed by inputting the table name, the dictionary of the type of each column, and the values ​​to input in JSON format and specifying dateformat.
Returns 1 if executed normally, 0 otherwise.

|Type Name|Value|
|--|--|
|short|4|
|ushort|104|
|integer|8|
|uinteger|108|
|long|12|
|ulong|112|
|float|16|
|double|20|
|datetime|6|
|varchar|5|
|ipv4|32|
|ipv6|36|
|text|49|
|binary|97|

### machbase.tables()

Returns information about all tables in the connected server. Returns 1 if successful; 0 if unsuccessful.

### machbase.columns(aTableName)

Returns information about the columns in the corresponding table on the connected server. Returns 1 if successful; 0 if unsuccessful.


## Checking Results

In the Machbase Python module, all result values ​​are returned in JSON.

It is adopted to return the result in a form that is easy to use in various environments.

### machbase.result()

The functions described above do not represent the execution results as the return value of the function, but only return success or failure. The result of a function can be obtained only by the return value of this function.


## Examples

Let's see how to use the Machbase Python module with simple examples.

You can check using $MACHBASE_HOME/sample/python files. The directory has a Makefile that makes it easy to test and a MakeData.py file that creates the data. Make sure that the value of PYPATH in the Makefile is set to Python with the Machbase Python module installed. The default is specified in Python installed in the Machbase package. Also, you need to make __init__.py file to execute the module in Python independently, so make sure that the file exists in that directory.

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

The following example is a simple function that connects to the server, executes the query, and returns the result. If each function returns a failure value (0), it returns an error result. If successful, the number of values ​​in the m $ tables table is returned.

The file name is Sample1Connect.py.

```py
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

Using the example below, we simply create a table using Python in Machbase, input the value, and extract the input value to check. The file name is Sample2Simple.py.

```py
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

Append method to input data at high speed in Machbase can also be used by using Python module. The following example shows how to input data at high speed. We used a method of declaring a connection class db2 for the column information and initialization, and a connection class db2 for the Append, and using each function. The file name is Sample3Append.py.

```py
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
