---
title : 'Input tag data'
type: docs
weight: 10
---

There are various way to insert tag data.

## Input using the INSERT statement

The easiest way to insert data is through the INSERT statement.

This is used for the small data sets, but if you want to load large amounts of data quickly, use another method.

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

We put the three TAG values as the current time.


## Load all at once through a CSV file 

Machbase allows you to load large amounts of CSV files through a csvimport tool.

More details can be found through practical examples, and are described in brief below.

### CSV Format (data.csv)

```sql
TAG_0001, 2009-01-28 07:03:34 0:000:000, -41.98
TAG_0001, 2009-01-28 07:03:34 1:000:000, -46.50
TAG_0001, 2009-01-28 07:03:34 2:000:000, -36.16 ....
```

Prepare a csv file consisting of <tag name, time, value> as above.

Of course, the tag name TAG_0001 must be present in the tag meta.

Using the loading program csvimport

```sql
csvimport -t TAG -d data.csv -F "time YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" -l error.log
```

This loads data.csv into a table called TAG.

The -F option specifies the time format stored in the data.csv file.

In addition, -l error.log records the error that occurred when inputting as a separate file.


## Input via the RESTful API

For more detailed usage of the RESTful API, please refer to the following examples.

Syntax of Input API

Machbase provides the RESTful API as follows:

```
{
"values":[
    [TAG_NAME, TAG_TIME, VALUE], ## Specify Tagname,Time,Value. if you define additional columns, the columns and values are follows. 
    [ .... ].... 
],
"date_format":"Date Format" ## If you moit date_format, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn' is used as default.
}
```

It is requested the number of columns in the defined TAG schema to match the above structure.


## Input data via the SDK

Machbase provides standard development tools for a variety of languages, including:

* [C/C++ library](/dbms/sdk/cli-odbc)
* [Java library](/dbms/sdk/jdbc)
* [Python library](/dbms/sdk/python)
* [C# library](/dbms/sdk/dotnet)

Through these libraries, users can create various application programs according to their environment and input data to Machbase.

