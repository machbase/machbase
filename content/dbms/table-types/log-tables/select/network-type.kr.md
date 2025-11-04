---
title : 네트워크 데이터 타입 / 연산자
type: docs
weight: 50
---

Machbase는 네트워크 데이터 타입을 지원하며 SELECT 문에서 사용할 수 있는 함수를 지원합니다.

* IPv4 형식: 4바이트 주소 타입
* IPv6 형식: 16바이트 주소 타입
* 네트워크 마스크: IPv4 또는 IPv6에 대한 네트워크 마스크 지정 형식(/ 비트 수)


## IPv4

### INSERT

```sql
INSERT INTO table_name VALUES (value1,value2,value3,...);
```

```sql
CREATE TABLE addrtable (addr IPV4);
INSERT  INTO addrtable VALUES ('127.0.0.1');
INSERT  INTO addrtable VALUES ('127.0' || '.0.2');
INSERT  INTO addrtable VALUES ('127.0.0.3');
INSERT  INTO addrtable VALUES ('127.0.0.4');
INSERT  INTO addrtable VALUES ('127.0.0.5');
INSERT  INTO addrtable VALUES ('255.255.255.255');
```


### SELECT

```sql
SELECT  column_name,column_name FROM    table_name;
```

```sql
Mach> SELECT addr FROM addrtable WHERE addr = '127.0.0.3' or addr = '127.0.0.5';
addr           
------------------
127.0.0.5      
127.0.0.3      
[2] row(s) selected.
 
Mach> SELECT addr FROM addrtable WHERE addr > '127.0.0.3' AND addr < '127.0.0.5';
addr           
------------------
127.0.0.4      
[1] row(s) selected.
 
Mach> SELECT addr FROM addrtable WHERE addr <> '127.0.0.3';
addr           
------------------
255.255.255.255
127.0.0.5      
127.0.0.4      
127.0.0.2      
127.0.0.1      
[5] row(s) selected.
 
Mach> SELECT addr FROM addrtable WHERE addr = '127.0.0.*';
addr           
------------------
127.0.0.5      
127.0.0.4      
127.0.0.3      
127.0.0.2      
127.0.0.1      
[5] row(s) selected.
 
Mach> SELECT addr FROM addrtable WHERE addr = '*.0.0.*';
addr           
------------------
127.0.0.5      
127.0.0.4      
127.0.0.3      
127.0.0.2      
127.0.0.1      
[5] row(s) selected.
```

## IPv6

### INSERT

```sql
INSERT  INTO    table_name  VALUES  (value1,value2,value3,...);
```

```sql
CREATE TABLE addrtable6 (addr ipv6);
INSERT INTO addrtable6 VALUES ('::0.0.0.0');
INSERT INTO addrtable6 VALUES ('::127.0' || '.0.1');
INSERT INTO addrtable6 VALUES ('::127.0.0.3');
INSERT INTO addrtable6 VALUES ('::127.0.0.4');
INSERT INTO addrtable6 VALUES ('21DA:D3:0:2F3B:2AA:FF:FE28:9C5A');
INSERT INTO addrtable6 VALUES ('::FFFF:255.255.255.255');
```

### SELECT

```sql
SELECT  column_name,column_name FROM    table_name;
```

```sql
Mach> SELECT addr FROM addrtable6 WHERE addr = '::127.0.0.3' or addr = '::127.0.0.5';
addr                                                        
---------------------------------------------------------------
::127.0.0.3                  
[1] row(s) selected.
 
Mach> SELECT addr FROM addrtable6 WHERE addr > '::127.0.0.3' and addr < '::127.0.0.5';
addr                                                        
---------------------------------------------------------------
::127.0.0.4                     
[1] row(s) selected.
 
Mach> SELECT addr FROM addrtable6 WHERE addr <> '::127.0.0.3';
addr                                                        
---------------------------------------------------------------
::ffff:255-255.255.255
21da:d3::2f3b:2aa:ff:fe28:9c5a
::127.0.0.4
::127.0.0.1
::                     
[5] row(s) selected.
 
Mach> SELECT addr FROM addrtable6 WHERE addr >= '21DA::';
addr                                                        
---------------------------------------------------------------
21da:d3::2f3b:2aa:ff:fe28:9c5a                   
[1] row(s) selected.
 
Mach> SELECT addr FROM addrtable6 order by addr desc;
addr                                                        
---------------------------------------------------------------
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.1
::                   
[6] row(s) selected.
```

## 네트워크 마스크

네트워크 마스크는 특정 주소가 특정 네트워크에 포함되는지 여부를 지정하는 표현 형식입니다. Machbase는 네트워크 마스크 타입 및 관련 연산자를 지원합니다.

### 마스크 표현 타입

일반적인 네트워크 표현과 같이, 네트워크 주소는 / 기호와 끝에 비트 수로 표현됩니다.

```
'192.128.0.0/16'
'FFFF::192.128.99.0/32'
```

### 마스크 연산자

**CONTAINS**

이 연산자는 왼쪽에 네트워크 마스크가 있어야 하고 오른쪽에 네트워크 주소 데이터 타입이 있어야 합니다. 즉, 입력 주소가 주어진 네트워크 마스크에 포함되는지 확인합니다. NOT 연산자를 함께 사용할 수 있습니다.

```sql
SELECT addr FROM addrtable  WHERE '192.0.0.0/16'    CONTAINS    addr;
SELECT addr FROM addrtable  WHERE '192.128.99.0/32' NOT CONTAINS    addr;
```

**CONTAINED**

CONTAINS와 반대로, 네트워크 주소가 왼쪽에 있고 네트워크 마스크가 오른쪽에 있습니다. 왼쪽 주소가 오른쪽 마스크의 일부인지 확인합니다.

```sql
SELECT addr FROM addrtable  WHERE addr CONTAINED '192.0.0.0/16';
SELECT addr FROM addrtable  WHERE addr NOT CONTAINED '192.128.99.0/32';
```

### 마스크 사용 예제

네트워크 마스크 타입을 사용한 검색 예제는 다음과 같습니다.

```sql
CREATE TABLE ip_table (addr4 IPV4, addr6 IPV6);
 
INSERT INTO ip_table VALUES ('192.0.0.1','FFFF::192.0.0.1');
INSERT INTO ip_table VALUES ('192.0.10.1','FFFF::192.0.10.1');
INSERT INTO ip_table VALUES ('192.128.0.1','FFFF::192.128.0.1');
INSERT INTO ip_table VALUES ('192.128.99.128','FFFF::192.128.99.128');
INSERT INTO ip_table VALUES ('192.128.99.64','FFFF::192.128.99.64');
INSERT INTO ip_table VALUES ('192.128.99.32','FFFF::192.128.99.32');
INSERT INTO ip_table VALUES ('192.128.99.16','FFFF::192.128.99.16');
INSERT INTO ip_table VALUES ('192.128.99.8','FFFF::192.128.99.8');
INSERT INTO ip_table VALUES ('192.128.99.4','FFFF::192.128.99.4');
INSERT INTO ip_table VALUES ('192.128.99.2','FFFF::192.128.99.2');
INSERT INTO ip_table VALUES ('192.128.99.1','FFFF::192.128.99.1');
 
Mach> SELECT addr4 FROM ip_table WHERE '192.0.0.0/16' CONTAINS addr4;
addr4
-----------
192.0.10.1
192.0.0.1
[2] row(s) selected.
 
Mach> SELECT addr4 FROM ip_table WHERE '192.128.0.0/16' CONTAINS addr4;
addr4
-----------
192.128.99.1
192.128.99.2
192.128.99.4
192.128.99.8
192.128.99.16
192.128.99.32
192.128.99.64
192.128.99.128
192.128.0.1
[9] row(s) selected.
 
Mach> SELECT addr4 FROM ip_table WHERE '192.0.10.0/24' CONTAINS addr4;
addr4
--------------------------------------------------------------------
192.0.10.1
[1] row(s) selected.
 
Mach> SELECT addr4 FROM ip_table WHERE '192.128.99.0/31' CONTAINS addr4;
addr4
-------------------------------------------------------
192.128.99.1
[1] row(s) selected.
 
Mach> SELECT addr4 FROM ip_table WHERE '192.128.99.0/32' NOT CONTAINS addr4;
addr4
-----------
192.128.99.1
192.128.99.2
192.128.99.4
192.128.99.8
192.128.99.16
192.128.99.32
192.128.99.64
192.128.99.128
192.128.0.1
192.0.10.1
192.0.0.1
[11] row(s) selected.
 
Mach> SELECT addr4 FROM ip_table WHERE addr4 CONTAINED '192.0.0.0/16';
addr4
-------------------------------------
192.0.10.1
192.0.0.1
[2] row(s) selected.
 
Mach> SELECT addr4 FROM ip_table WHERE addr4 CONTAINED '192.128.0.0/16';
addr4
-------------------------------------
192.128.99.1
192.128.99.2
192.128.99.4
192.128.99.8
192.128.99.16
192.128.99.32
192.128.99.64
192.128.99.128
192.128.0.1
[9] row(s) selected.
 
Mach> SELECT addr4 FROM ip_table WHERE addr4 CONTAINED '192.0.10.0/24';
addr4
----------------------------
192.0.10.1
[1] row(s) selected.
 
Mach> SELECT addr4 FROM ip_table WHERE addr4 not CONTAINED '192.128.99.0/32';
addr4
-------------------------------------------------
192.128.99.1
192.128.99.2
192.128.99.4
192.128.99.8
192.128.99.16
192.128.99.32
192.128.99.64
192.128.99.128
192.128.0.1
192.0.10.1
192.0.0.1
[11] row(s) selected.
 
Mach> SELECT addr6 FROM ip_table WHERE 'FFFF::192.0.0.0/104' CONTAINS addr6;
addr6
-------------------------------------
ffff::c080:6301
ffff::c080:6302
ffff::c080:6304
ffff::c080:6308
ffff::c080:6310
ffff::c080:6320
ffff::c080:6340
ffff::c080:6380
ffff::c080:1
ffff::c000:a01
ffff::c000:1
[11] row(s) selected.
 
Mach> SELECT addr6 FROM ip_table WHERE 'FFFF::192.128.0.0/112' CONTAINS addr6;
addr6
------------------------------------
ffff::c080:6301
ffff::c080:6302
ffff::c080:6304
ffff::c080:6308
ffff::c080:6310
ffff::c080:6320
ffff::c080:6340
ffff::c080:6380
ffff::c080:1
[9] row(s) selected.
 
Mach> SELECT addr6 FROM ip_table WHERE 'FFFF::192.0.10.0/120' CONTAINS addr6;
addr6
------------------------------------------------
ffff::c000:a01
[1] row(s) selected.
 
Mach> SELECT addr6 FROM ip_table WHERE 'FFFF::192.128.99.0/31' CONTAINS addr6;
addr6
---------------------------------------------
ffff::c080:6301
ffff::c080:6302
ffff::c080:6304
ffff::c080:6308
ffff::c080:6310
ffff::c080:6320
ffff::c080:6340
ffff::c080:6380
ffff::c080:1
ffff::c000:a01
ffff::c000:1
[11] row(s) selected.
 
Mach> SELECT addr6 FROM ip_table WHERE 'FFFF::192.128.99.0/32' not CONTAINS addr6;
addr6
-------------------------------------
[0] row(s) selected.
 
Mach> SELECT addr6 FROM ip_table WHERE addr6 CONTAINED 'FFFF::192.0.0.0/104';
addr6
-------------------------------------
ffff::c080:6301
ffff::c080:6302
ffff::c080:6304
ffff::c080:6308
ffff::c080:6310
ffff::c080:6320
ffff::c080:6340
ffff::c080:6380
ffff::c080:1
ffff::c000:a01
ffff::c000:1
[11] row(s) selected.
 
Mach> SELECT addr6 FROM ip_table WHERE addr6 CONTAINED 'FFFF::192.128.0.0/112';
addr6
-------------------------------------
ffff::c080:6301
ffff::c080:6302
ffff::c080:6304
ffff::c080:6308
ffff::c080:6310
ffff::c080:6320
ffff::c080:6340
ffff::c080:6380
ffff::c080:1
[9] row(s) selected.
 
Mach> SELECT addr6 FROM ip_table WHERE addr6 CONTAINED 'FFFF::192.0.10.0/120';
addr6
-------------------------------------
ffff::c000:a01
[1] row(s) selected.
 
Mach> SELECT addr6 FROM ip_table WHERE addr6 not CONTAINED 'FFFF::192.128.99.0/32';
addr6
-------------------------------------
[0] row(s) selected.
```
