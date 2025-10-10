---
type: docs
title : 'RESTful API'
type : docs
weight: 50
---

## RESTful API Overview

Representational State Transfer (REST) is a type of [software architecture style](https://en.wikipedia.org/wiki/Architectural_pattern) that consists of guidelines and best practices for interfaces provided by scalable Web services.

The four methods defined in the HTTP protocol define the CRUD for the resource.

|HTTP Method| Meaning|
|--|--|
|POST | Create|
| GET | Select
|PUT | Update|
|DELETE | Delete|


Machbase is not a standard RESTful API, but rather a RESTful API that handles CRUD using only POST and GET methods.

That is, the POST method is used for data input and the rest is transmitted as a GET Method parameter to the SQL query so that all the operations can be performed.

## Machbase RestAPI

MachBase supports convenient and fast Rest API functions through the web server built into the server. 
Machbase Edition support embedded web server
All type of machbase editions are supported. (Standard / Cluster)

Location of version-specific .conf files

Standard edition

$MACHBASE_HOME/conf/machbase.conf $MACHBASE_HOME/http/conf/http.conf

Cluster edition

$EACH_BROKER_HOME/conf/machbase.conf (Modify by Broker) $EACH_BROKER_HOME/http/conf/http.conf (modify all per Broker)

Added properties for embedded web server
machbase.conf (set as PROPERTY = VALUE)

|Property |Description|
|--|--|
|HTTP_ENABLE|Whether to run the embedded web server 0: not driven, 1: driven|
|HTTP_PORT_NO|Embedded web server connection port number Port range: 0 ~ 65535 Default : 5657|
|HTTP_MAX_MEM|Maximum memory used by one Web Session Min: 1048576 (1MB) Default : 536870912 (512MB)|
|HTTP_AUTH|Whether to use Basic authentication when using the Embedded Web Server 0: Authentication not used, 1: Authentication enabled|

http.conf (set in JSON format)


|Property|Description|
|--|--|
|document_root |html file location based on $MACHBASE_HOME<br> Default : http/html ($MACHBASE_HOME/http/html) |
|max_request_size |Limit the maximum request byte size for one request|
|request_timeout_ms |Maximum response latency for one request (millisecond) |
|enable_auth_domain_check|Whether to enable domain authentication Set to "yes" or "no" value Default: "no" |
|reverse_proxy|change request url to specific url|

sample conf files

machbase.conf

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

http.conf

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

### DDL / DML / Append REST API Usage

```
Basic request format
  
http://addr:port/machbase?q=query&f=dateformat
  
Response DDL / Append / DML (except Select)
{"error_code":0, "error_message" :"Message", "data":[]}
  
Response DML (Select)
{"error_code":0, "error_message" :"Message", "columns":[Columns], "data":[Data]}
```

DDL Sample

```
### Request of creating a table
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=create table test_table (name varchar(20), time datetime, value double)'
   
### Normal response
{"error_code":0, "error_message" :"No Error", "data":[]}
   
### Request of dropping a table
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=drop table test_table'
   
### Normal response
{"error_code":0, "error_message" :"No Error", "data":[]}
```

DML Sample

```
### Request Log table data insert
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=insert into test_table values ("test", "1999-01-01 00:00:00", 0)'
   
### Response
{"error_code":0, "error_message" :"No Error", "data":[]}
   
### Request Log table select
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from test_table'
   
### Response
{"error_code":0, "error_message": "", "columns" : [{"name":"NAME", "type":5, "length":20},{"name":"TIME", "type":6, "length":8},{"name":"VALUE", "type":20, "length":8}],"data" :[{"NAME":"test", "TIME":"1999-01-01 00:00:00 000:000:000", "VALUE":0.000}]}
```

Append Sample

```
### Append some data to log table
curl -X POST -H "Content-Type: application/json" "http://127.0.0.1:5657/machbase" -d '{"name":"test_table", "date_format":"YYYY-MM-DD","values":[["test", "1999-01-01 00:00:01", 1], ["test", "1999-01-01 00:00:02", 2], ["test", "1999-01-01 00:00:03", 3]]}'
   
### Response
{"error_code":0, "error_message" :"No Error", "data":[], "append_success":3, "append_failure":0}
```

In the case of Binary Append, if binary data is encoded in Base64 and transmitted, the server will decode it and store it. When outputting, binary data is returned after being encoded in Base64.
Input : Binary Data >> Base64 Encoding >> HTTP(POST) >> Base64 Decoding >> Append(BLOB Binary)

Output : BLOB Binary >> Base64 Encoding >> HTTP (GET) >> Base64 Decoding >> Save or View Binary

Binary Append Sample

```
### Example of sending binary data. data should be encoded by Base64.
   
### Request append to log table
curl  -X POST -H "Content-Type: application/json" "http://127.0.0.1:5657/machbase" -d '{"name":"test_table", "date_format":"YYYY-MM-DD","values":[["AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/w=="]]}'
   
### Result
{"error_code":0, "error_message" :"No Error", "data":[], "append_success":1, "append_failure":0}
   
### Get data from log table
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from test_table';
   
### The Base64 encoded data are displaied
{"error_code" :0, "error_message": "No Error", "columns" : [{"name":"V1", "type":57, "length":67108864}],"data" :[{"V1":"AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/w=="}]}
   
### Can check data using machsql
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

Using HTTP Auth Property

This is an option to set authentication as a normal user by including the string 'Authorization: Basic Base64String' in the Request Header. Base64 string is written in ID@Host:Password structure. (However, the host name does not need to be correct. ID and password must be entered in Machbase user information.)

How to create a Basic Base64String for authorize

```
### In case of ID: sys, Password: manager , creating a Base64String
echo -n "sys@localhost:manager" | base64
   
### Result
c3lzQGxvY2FsaG9zdDptYW5hZ2Vy
```

Using Auth Sample (HTTP_AUTH = 1)

```
### Request of result without authorization clause
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from v$stmt'
   
### Error occurred
{"error_code":3118, "error_message" :"There is No Authorization Header.", "data":[]}
   
### Adding 'Authorization:Base64String' at the request header
curl -H "Authorization: Basic c3lzQGxvY2FsaG9zdDptYW5hZ2Vy"  -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from v$stmt'
   
### Normal response
{"error_code":0, "error_message": "No Error", "columns" : [{"name":"ID", "type":8, "length":4},{"name":"SESS_ID", "type":8, "length":4},{"name":"STATE", "type":5, "length":64},{"name":"RECORD_SIZE", "type":8, "length":4},{"name":"QUERY", "type":5, "length":32767}],"data" :[{"ID":0, "SESS_ID":52, "STATE":"Fetch prepared", "RECORD_SIZE":0, "QUERY":"select * from v$stmt"}]}
```

Changing floating point precision with s option

Specify how many decimal places of response data to output Set to a value from 0 to 9 (If it is not a range value, it operates as 3)

Sample (s=5)

```
### display result 5 decimal places
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from test_table' --data-urlencode 's=5';
   
### Normal response
{"error_code" :0, "error_message": "", "columns" : [{"name":"C1", "type":16, "length":4},{"name":"C2", "type":20, "length":8}],"data" :[{"C1":12345.00000, "C2":1234.01235}]}
```

Changing data Fetch mode (m option)

Default Fetch mode Sample (m=0)

```
### Request fetch mode (m=0)
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from tag limit 2' --data-urlencode 'm=0';
   
### Normal response (Conatains Column Name in result data)
{"error_code" :0, "error_message": "", "columns" : [{"name":"NAME", "type":5, "length":20},{"name":"TIME", "type":6, "length":8},{"name":"VALUE", "type":20, "length":8}],
"data" :[{"NAME":"tag1", "TIME":"2001-09-09 10:46:40 000:000:000", "VALUE":1000000000.000}, {"NAME":"tag1", "TIME":"2001-09-09 10:46:41 000:000:000", "VALUE":1000000001.000}]}
```

Advanced Fetch mode Sample (m=1)

```
### Request fetch mode (m=1)
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode 'q=select * from tag limit 2' --data-urlencode 'm=1';
   
### Normal response (Column Names are not included in results)
{"error_code" :0, "error_message": "", "columns" : [{"name":"NAME", "type":5, "length":20},{"name":"TIME", "type":6, "length":8},{"name":"VALUE", "type":20, "length":8}],
"data" :[["tag1", "2001-09-09 10:46:40 000:000:000", 1000000000.000], ["tag1", "2001-09-09 10:46:41 000:000:000", 1000000001.000]]}
```

Handling of NULL values

When inserting or appending during DML processing, a NULL value can be entered as null as it is.

JSON Sample for appending null values

```
[["data1", "data2", "data3"],["data11", "data12", "data13"],["data21", "data22", "data23"],[null,null,null]]
```

Sample result containing null values from SELECT

```
[{"C1":null, "C2":null, "C3":null, "C4":null, "C5":null, "C6":null, "C7":null, "C8":null, "C9":null, "C10":null, "C11":null, "C12":null}]
```

## RestAPI for Tag Table Usage

Machbase provides Historian-like RestAPI access to Tag Table.

The default request format is http://ipaddr:port/machiot/ or http://ipaddr:port/machiot-rest-api/

In addition, the following parameters can be handed over to the URL.

|Parameter|Description|Sample|
|--|--|--|
|f or DateFormat| set date format| XXX?f=YYYY/MM/DD<br> XXX?DateFormat=YYYY/MM/DD|
|m or FetchMode| set fetch mode| XXX?m=1<br> XXX?FetchMode=1|
|s or Scale| set scale| XXX?s=12<br> XXX?Scale=12|

### Raw data processing function

#### Raw Value Append API

This API is a function of appending a large amount of data into a given table.

URL

http://ipaddr:port/machiot/datapoints/raw/{Table}
http://ipaddr:port/machiot/v1/datapoints/raw/{Table}

* HTTP method : POST
* Table : Target tag table to be input

Usage

```
Request
curl  -X POST -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot-rest-api/datapoints/raw/tag"
-d '{"date_format":"YYYY-MM-DD HH24:MI:SS",
     "values":
       [
          ["tag1", "1999-01-01 00:00:00", 0],
          ["tag1", "1999-01-01 00:00:01", 1],
          ["tag1", "1999-01-01 00:00:02", 2]
        ]
     }';
Response
{
   "error_code":0,
   "error_message" :"No Error",
   "timezone":"+0900",
   "data":[],
   "append_success":3,
   "append_failure":0
}
```

#### Raw Value Select API


This API is a function of obtaining data from a given table.

It supports the method of directly specifying all URLs, and also supports the method of passing them to the factor of the GET method.

Each directory name may be designated as a factor in the URL below.

URL

```
http://ipaddr:port/machiot/datapoints/raw/{Table}/{TagNames}/{Start}/{End}/{Direction}/{Count}/{Offset}
http://ipaddr:port/machiot/v1/datapoints/raw/{Table}/{TagNames}/{Start}/{End}/{Direction}/{Count}/{Offset}
```

* HTTP method : GET
* Table : Target tag table to be selected
* TagNames : Target tag name to be selected<br>
    * This tag name can be divided into a comma and multiple tag results can be obtained in one series.
* Start : Indicates the starting time value of the data to be selected.
* End :  Indicates the last time value of the data to be selected.<br>
    * Time format: Both space-free and space-support forms are supported as shown below. (If tested with curl, additional forms can be used)
        * Basic form (space supported, up to nanoseconds)
            * YYYY-MM-DD HH:MI:SS, millis
            * YYYY-MM-DD HH:MI:SS milliSec:microSec:nanoSec
        * Additional Form (space not supported, Use uppercase T instead of space and support up to milliseconds)
            * YYYY-MM-DDTHH:MI:SS,millis
    * Example
        * "2020-12-12"
        * "2020-12-12 03:22:22"
        * "2020-12-12 03:22:22 222:333:444"
        * "2020-12-12T03:22:22"
        * "2020-12-12T03:22:22,234"
* Direction (Omitable)
    * 0 (Default): Output in the order entered
    * 1 : Output in the direction of time decrease
    * 2 : Output in the direction of time increase
* Count (Omitable)
    * 0 (Default): Output all data
    * Else : Output a given number of records
* Offset (Omitable)
    * 0 (Default) : Do not skip over
    * Else : Skip over a given value

Usage

```
Request (Directly specifying all URL)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/raw/tag/tag-1/2001-09-09T00:00:00,000/2001-09-09T01:20:00,000/0/5/0"
Request
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
 
Request (Passing factors)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/raw?Table=tag&amp;TagNames=tag-1&amp;Start=2001-09-09T00:00:00,000&amp;End=2001-09-09T01:20:00,000&amp;Direction=0&amp;Count=5&amp;Offset=0"
Response
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
  
Request (When specifying multiple tags (tag-1, tag-2, tag-3))
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/raw/tag/tag-1,tag-2,tag-3/2001-09-09T00:00:00,000/2001-09-09T01:20:00,000/0/0/0";
Response
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

#### All Tag-based Raw Value Delete API

This API deletes all data prior to a specific time for all entered tags.

This function can be usefully used to remove data that is no longer needed after disk capacity is insufficient or backup is completed.

URL

```
http://ipaddr:port/machiot/datapoints/raw/{Table}/{BeforeTime}
http://ipaddr:port/machiot/v1/datapoints/raw/{Table}/{BeforeTime}
```

* HTTP method : DELETE
* Table : Target tag table to be deleted
* BeforeTime : Indicates time value which all data before it will deleted

Usage

```
Request
curl -X DELETE  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/raw/tag/2001-09-09T01:20:00,000";
Response
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "effect_rows": "1201",
  "data": []
}
```

#### Specific Tag-based Raw Value deletion API

This API deletes all data prior to a specific time for a specific tag.

This function can be usefully used to remove data that is no longer needed after disk capacity is insufficient or backup is completed.

URL

```
http://ipaddr:port/machiot/datapoints/raw/{Table}/{TagNames}/{BeforeTime}
http://ipaddr:port/machiot/v1/datapoints/raw/{Table}/{TagNames}/{BeforeTime}
```

* HTTP method : DELETE
* Table : Target tag table to be deleted
* TagNames : Target tag names to be deleted. You can specify multiple tags separated by a comma.
* BeforeTime : Indicates time value which all data before it will deleted

Usage

```
Request
curl -X DELETE  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/raw/tag/tag-2,tag-3/2001-09-09T01:20:00,000";
Response
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "effect_rows": "32",
  "data": []
}
```

### Statistical data processing function 

#### Statistical Data Select API

This API is a function that quickly obtains statistical results for stored data.

URL

```
http://ipaddr:port/machiot/datapoints/calculated/{Table}/{TagNames}/{Start}/{End}/{CalculationMode}/{Count}/{IntervalType}/{IntervalValue}
http://ipaddr:port/machiot/v1/datapoints/calculated/{Table}/{TagNames}/{Start}/{End}/{CalculationMode}/{Count}/{IntervalType}/{IntervalValue}
```

* HTTP method : GET
* Table : Target tag table to be selected
    * TagNames : Target tag names to be selected. You can specify multiple tags separated by a comma.
* If multiple tags are specified, the total operation result for those tags is output. (If you want to get statistical results for each tag, you have to call it tag by tag)
* Start, End : Specify the time range in which data is to be obtained (Lookup Raw Value Select API)
* Count : Number of result
* CalculationMode : Target statistical function to be obtained. You can specify multiple statistical functions separated by a comma. (The function name must be the same as below)
    * min : Minimum value
    * max : Maximum value
    * sum : Sum of values
    * count : Count of values
    * avg : Average of values
* IntervalType : Desired time unit type of values
    * sec : Per second
    * min : Per minute
    * hour : Per hour
* IntervalValue : Desired time unit of IntervalType
    * A value greater than 0 is specified as a minor number of 60.
    * Mainly 5, 10, 15, and 30 are designated.

Usage

```
Request (single statistical function)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/v1/datapoints/calculated/tag/tag-1/2001-09-09T00:00:00,000/2001-09-09T01:20:00,000/sum/5/min/5"
Response
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
Request (multiple statistical function)
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

### Tag metadata processing function

The schema of the table used in this section was created as follows.

```
curl -X GET "http://127.0.0.1:${ITF_HTTP_PORT}/machbase" --data-urlencode 'q=create tagdata table TAG (name_multi varchar(20) primary key, time_multi datetime basetime, value_multi double summarized, value2_multi short, value3_multi varchar(10)) metadata (myshortmeta short, baseip ipv4);';
```

#### Tag Information INSERT API

This API is used to register tags to be used. 

Enter data as many as the number of metadata columns added when creating a table with the Tag

```
http://ipaddr:port/machiot/tags/list/{TableName}
http://ipaddr:port/machiot/v1/tags/list/{TableName}
```

* HTTP method : POST
* TableName : Target tag table to be input.

Usage

```
Request
curl -X POST -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag" -d
       '{
        "values":[
            ["tag3", 0, "127.0.0.0"],
            ["tag4", 1, "127.0.0.1"],
            ["tag4", 1, "127.0.0.1"],
            ["tag5", 2, "127.0.0.2"]
         ]
        }';
Response
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

#### Tag Information SELECT API

URL

```
http://ipaddr:port/machiot/tags/list/{Table}/{TagName}
http://ipaddr:port/machiot/v1/tags/list/{Table}/{TagName}
```

* HTTP method : GET
* Table : Target tag table to be selected
    * Print a list of all tag names if only table name is specified
* TagName : Target tag name to be selected
    * Print the tag details

Usage

```
Request (select all tag names)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag"
Response
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

#### Tag Information UPDATE API

This API supports modification of additional tag information.

Both PUT and PATCH are supported, and the value of the JSON format used at the time of input must be the same as the column name of the table.

Since multiple column names are supported, values of two or more columns can be changed at once.

URL

```
http://ipaddr:port/machiot/tags/list/{Table}/{TagName}
http://ipaddr:port/machiot/v1/tags/list/{Table}/{TagName}
```

* HTTP method : PUT / PATCH
* Table : Target tag table to be updated
* TagName : Target tag name to be updated

Usage

```
Request (PUT)
curl -X PUT -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag/tag0" -d  '{"baseip":"192.168.0.1"}';
Response
{
   "error_code":0,
   "error_message" :"No Error",
   "timezone":"+0900",
   "effect_rows":"1",
   "data":[]
}
  
Request (PATCH)
curl -X PATCH -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag/tag3" -d  '{"baseip":"255.255.255.0", "myshortmeta":9999 }';
Response
{
   "error_code":0,
   "error_message" :"No Error",
   "timezone":"+0900",
   "effect_rows":"1",
   "data":[]
}
```

#### Tag Information DELETE API

This API deletes the specified tag. However, if raw data is present in the tag, deletion fails.

In order to delete a tag in which raw data exists, this function must be called after performing the deletion of raw data for that tag.

URL

```
http://ipaddr:port/machiot/tags/list/{Table}/{TagNames}
http://ipaddr:port/machiot/v1/tags/list/{Table}/{TagNames}
```

* HTTP method : DELETE
* Table: Target tag table to be deleted
* TagName: Target tag name to be deleted

Usage

```
Request (Try to delete tag with raw data)
curl -X DELETE -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag/tag0";
Response (Error)
{
   "error_code":2324,
   "error_message" :"Cannot delete tagmeta. there exist data with deleted_tag key.",
   "timezone":"+0900",
   "data":[]
}
 
 
Request (Try to delete tag without raw data)
curl -X DELETE -H "Content-Type: application/json" "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/list/tag/tag4";
Response (Success)
{
   "error_code":0,
   "error_message" :"No Error",
   "timezone":"+0900",
   "effect_rows":"1",
   "data":[]
}
```

### Other functions

#### Time range lookup API

This API obtains an overall time range (minimum and maximum) for data of the specified table and tag.

URL

```
http://ipaddr:port/machiot/tags/range/{Table}/{TagName}
http://ipaddr:port/machiot/v1/tags/range/{Table}/{TagName}
```

* HTTP method : GET
* Table : Target tag table to be selected
* TagName : Target tag name to be selected
    * If not specified, return the whole tag time range (the tag name will be returned to ALL).

Usage

```
Request (Whole tag range)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/range/tag"
Response
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
  
Request (Time range of each specified tag)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/range/tag/tag-1,tag-2"
Response
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

#### Minimum value API

This API gets the minimum Value existing in the specified table or tag.

URL

```
http://ipaddr:port/machiot/tags/min/{Table}/{TagName}
http://ipaddr:port/machiot/v1/tags/min/{Table}/{TagName}
```

* HTTP method : GET
* Table : Target tag table to be selected
* TagName : Target tag name to be selected
    * If not specified, return the minimum value of the table

Usage

```
Request (Minimum value of whole table)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/min/tag"
Response
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
 
 
Request (Minimum value of each specified tag)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/min/tag/tag-1,tag-2";
Response
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

#### Maximum value API

This API gets the maximum Value existing in the specified table or tag.

URL

```
http://ipaddr:port/machiot/tags/max/{Table}/{TagName}
http://ipaddr:port/machiot/v1/tags/max/{Table}/{TagName}
```

* HTTP method : GET
* Table : Target tag table to be selected
* TagName : Target tag name to be selected
    * If not specified, return the maximum value of the table

Usage

```
Request (Maximum value of the table)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/max/tag"
Response
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
 
 
Request (Maximum value of each specified tag)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/max/tag/tag-1,tag-2";
Response
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

#### First row API

This API gets the row with the smallest time value that exists in the specified table or tag.

URL

```
http://ipaddr:port/machiot/tags/first/{Table}/{TagName}
http://ipaddr:port/machiot/v1/tags/first/{Table}/{TagName}
```

* HTTP method : GET
* Table : Target tag table to be selected 
* TagName : Target tag name to be selected
    * If not specified, return the row with the smallest time value of the table

Usage

```
Request (Earliest row data of the table)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/first/tag"
Response
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
 
 
Request (Earliest row data of each specified tag)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/first/tag/tag-1,tag-2";
Response
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

#### Last row API

This API gets the row with the largest time value that exists in the specified table or tag.

URL

```
http://ipaddr:port/machiot/tags/last/{Table}/{TagName}
http://ipaddr:port/machiot/v1/tags/last/{Table}/{TagName}
```

* HTTP method : GET
* Table : Target tag table to be selected 
* TagName : Target tag name to be selected
    * If not specified, return the row with the largest time value of the table

Usage

```
Request (Latest row data of the table)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/last/tag"
Response
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
 
 
Request (Latest row data of each specified tag)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/last/tag/tag-1,tag-2";
Response
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

#### Record count API

This API obtains the number of records present in the specified table or tag.

URL

```
http://ipaddr:port/machiot/tags/count/{Table}/{TagNames}
```

```
http://ipaddr:port/machiot/tags/cnt/{Table}/{TagNames}
http://ipaddr:port/machiot/v1/tags/count/{Table}/{TagNames}
```

```
http://ipaddr:port/machiot/v1/tags/cnt/{Table}/{TagNames}
```

* HTTP method : GET
* Table : Target tag table to be counted
* TagName : Target tag name to be counted
    * If not specified, output the total number of records in the table.

Usage

```
Request (Total number of records in the table)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/count/tag"
Response
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
 
 
Request (Records count of each specified tag)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/count/tag/tag-1,tag-2";
Response
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

#### Disk usage API

This API approximates the disk usage in use by the specified table or tag.

URL

```
http://ipaddr:port/machiot/tags/disksize/{Table}/{TagNames}
http://ipaddr:port/machiot/v1/tags/disksize/{Table}/{TagNames}
```

* HTTP method : GET
* Table : Target tag table to be measured
* TagName : Target tag name to be measured
    * If not specified, output the total disk usage for that table.

Usage

```
Request (Total disk usage for table)
curl -X GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/disksize/tag/"
Response
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
 
Request (Disk usage of each specified tag)
curl -X  GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/disksize/tag/tag-1,tag-2"
Response
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

#### Rollup request API

This API requests compulsory execution for a specific rollup table. Through this, it is forced to calculate statistical values that have not yet been calculated.

If you call this API, you can wait for seconds to minutes depending on the situation, so you should use it carefully.

URL

```
http://ipaddr:port/machiot//rollup/{Table}
http://ipaddr:port/machiot/v1//rollup/{Table}
```

* HTTP method : GET
* Table : Target table to be execute rollup

Usage

```
Request
curl -X HTTP GET  "http://127.0.0.1:${ITF_HTTP_PORT}/machiot/tags/rollup/tag"
Response
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "data": []
}
```
