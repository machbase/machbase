---
type: docs
title : 'JDBC'
type : docs
weight: 20
---

## JDBC 개요

자바 프로그래밍 언어로 만들어진 데이터베이스 조작 인터페이스의 집합을 JDBC(Java DataBase Connectivity)라고 합니다. 다양한 관계형 데이터베이스를 위해 일관된 인터페이스를 제공하는 API 집합으로서 프로그래머가 SQL 요구를 만드는데 사용할 일련의 객체지향 프로그램의 클래스들을 정의하고 있습니다. 즉, 어떤 데이터베이스를 사용하더라도 JDBC 드라이버만 제공된다면 코드 수정 없이 바로 적용 가능한 장점이 있습니다.

## 표준 JDBC 함수

[표준 함수 스펙 4.0](https://www.oracle.com/java/technologies/javase/javase-tech-database.html#corespec40)

## 확장 JDBC 함수

### setIPv4

```java
void setIpv4(int ind, String ipString)
```

PrepareStatement에서 IPv4 주소 타입을 입력하기 위한 함수입니다.

컬럼 인덱스와 IPv4 문자열을 인자로 받습니다.

### setIPv6

```java
void setIpv6(int ind, String ipString)
```
PrepareStatement에서 IPv6 주소 타입을 입력하기 위한 함수입니다.

컬럼 인덱스와 IPv6 문자열을 인자로 받습니다.

### executeAppendOpen

```java
ResultSet executeAppendOpen(String aTableName, int aErrorCheckCount)
```

Statement에서 Append 프로토콜을 쓰기 위한 것으로 프로토콜을 오픈합니다.

테이블 이름과 오류 검사 간격을 인자로 받습니다. 결과값으로 ResultSet을 리턴합니다. 

### executeAppendData

```java
int executeAppendData(ResultSetMetaData rsmd, ArrayList aData)
```

Statement에서 Append 프로토콜을 위한 것으로 실제 데이터를 입력합니다.

executeAppendOpen의 결과값인 ResultSet의 메타데이터와 입력하고자 하는 데이터를 인자로 받습니다. 결과값이 전송 버퍼에 저장되면 1이 리턴되고, 전송 버퍼가 차서 마크베이스로 전송되면 2가 리턴됩니다. 따라서 1 또는 2가 리턴되면 성공으로 판단하면 됩니다. 

### executeAppendDataByTime

```java
int executeAppendDataByTime(ResultSetMetaData rsmd, long aTime, ArrayList aData)
```

Statement에서 Append 프로토콜을 위한 것으로 실제 데이터를 시간 기준으로 입력합니다.

executeAppendOpen의 결과값인 ResultSet의 메타데이터와 설정하고자 하는 특정 시간대의 시간 값, 입력하고자 하는 데이터를 인자로 받습니다. 결과값이 전송 버퍼에 저장되면 1이 리턴됩니다.  

### executeAppendClose

```java
int executeAppendClose()
```

Statement에서 Append 프로토콜을 위한 것으로 statement를 종료합니다.

결과값으로 성공하면 1을 리턴합니다.

### executeSetAppendErrorCallback

```java
int executeSetAppendErrorCallback(MachAppendCallback aCallback)
```

Append 수행하는 도중에 에러가 발생하는 경우 에러를 출력하는 콜백 함수를 설정합니다.

에러 로그를 출력하는 콜백 함수를 인자로 받습니다. 결과값으로 성공하면 1이 리턴됩니다. 

### getAppendSuccessCount

```java
long getAppendSuccessCount()
```

Statement에서 Append 프로토콜을 위한 것으로 성공한 개수를 리턴합니다.

결과값으로 성공한 개수를 리턴합니다. 

### getAppendFailCount

```java
long getAppendFailCount()
```
Statement에서 Append 프로토콜을 위한 것으로 실패한 개수를 리턴합니다.

결과값으로 실패한 개수를 리턴합니다. 

## 응용 프로그램 개발

### JDBC 라이브러리 설치 확인

$MACHBASE_HOME/lib 디렉터리에 machbase.jar 파일이 있는지 확인합니다.

```bash
[mach@localhost ~]$ cd $MACHBASE_HOME/lib
[mach@localhost lib]$ ls -l machbase.jar
-rw-rw-r-- 1 mach mach 78599 Jun 18 10:00 machbase.jar
[mach@localhost lib]$
```

### Makefile 작성 가이드

$(MACHBASE_HOME)/lib/machbase.jar를 classpath에 지정해주어야 합니다. 다음은 Makefile 예시입니다.

```bash
CLASSPATH=".:$(MACHBASE_HOME)/lib/machbase.jar"
 
SAMPLE_SRC = Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
 
all: build
 
build:
    -@rm -rf *.class
    javac -classpath $(CLASSPATH) -d . $(SAMPLE_SRC)
 
create_table:
    machsql -s localhost -u sys -p manager -f createTable.sql
 
select_table:
    machsql -s localhost -u sys -p manager -f selectTable.sql
 
run_sample1:
    java -classpath $(CLASSPATH) Sample1Connect
 
run_sample2:
    java -classpath $(CLASSPATH) Sample2Insert
 
run_sample3:
    java -classpath $(CLASSPATH) Sample3PrepareStmt
 
run_sample4:
    java -classpath $(CLASSPATH) Sample4Append
 
clean:
    rm -rf *.class
```

### 컴파일 및 링크

다음과 같이 make 명령어를 수행하여 컴파일 및 링크를 수행합니다. 

```bash
[mach@localhost jdbc]$ make
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$
```

## Maven을 이용한 응용 프로그램 개발

Maven을 사용해서 마크베이스 JDBC(machjdbc)를 프로젝트로 가져올 수 있습니다.   
Machbase JDBC 드라이버는 [Maven Central Repository](https://mvnrepository.com/artifact/com.machbase/machjdbc)에서 찾을 수 있습니다.   

### machjdbc을 가져와서 사용하기

machjdbc를 프로젝트에 가져오려면, `pom.xml`를 열어서 아래의 내용을 `<dependencies>` 태그 안에 추가해 줍니다.
```
<dependency>
    <groupId>com.machbase</groupId>
    <artifactId>machjdbc</artifactId>
    <version>{{< jdbc_version >}}</version>
</dependency>
```
> 버전 번호인 {{< jdbc_version >}}은 Maven Central의 최신 버전으로 바꾸어도 됩니다.
<br>

그러면 아래처럼 `import` 구문을 이용해서 machjdbc를 소스 안에서 사용할 수 있습니다.
```
import com.machbase.jdbc.*;
```
<br><br>

## JDBC 샘플

### 접속 예제

마크베이스 JDBC 드라이버를 이용하여 마크베이스 서버에 접속하는 예제 프로그램을 작성해 보기로 합니다. 소스 파일명을 Sample1Connect.java로 합니다.

> [Tips] _arrival_time 컬럼은 디폴트로 표시되지 않습니다.<br>
> 따라서 _arrival_time 컬럼을 표시하려면, 연결 문자열에 show_hidden_cols=1 을 추가하면 됩니다.<br><br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;아래 예제 소스에서 접속 문자열을 다음과 같이 수정하면 됩니다.<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;String sURL = "jdbc:machbase://localhost:5656/machbasedb?show_hidden_cols=1";

```java
import java.util.*;
import java.sql.*;
import com.machbase.jdbc.*;
 
public class Sample1Connect
{
    public static Connection connect()
    {
        Connection conn = null;
        try
        {
            String sURL = "jdbc:machbase://localhost:5656/machbasedb";
 
            Properties sProps = new Properties();
            sProps.put("user", "sys");
            sProps.put("password", "manager");
 
            Class.forName("com.machbase.jdbc.MachDriver");
            conn = DriverManager.getConnection(sURL, sProps);
        }
        catch ( ClassNotFoundException ex )
        {
            System.err.println("Exception : unable to load mach jdbc driver class");
        }
        catch ( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        return conn;
    }
 
    public static void main(String[] args) throws Exception
    {
        Connection conn = null;
 
        try
        {
            conn = connect();
            if( conn != null )
            {
                System.out.println("mach JDBC connected.");
            }
        }
        catch( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        finally
        {
            if( conn != null )
            {
                conn.close();
                conn = null;
            }
        }
    }
}
```

이제 소스 코드를 컴파일하고 실행합니다. 이미 작성한 Makefile을 이용합니다.

```bash
[mach@localhost jdbc]$ make
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$ make run_sample1
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample1Connect
mach JDBC connected.
```

### 데이터 입력 및 출력 예제 (1) 직접 입/출력

마크베이스 JDBC 드라이버를 이용하여 데이터를 입력하고 출력하는 예제를 작성하여 보기로 합니다.

소스 파일명은 Sample2Insert.java 라고 합니다.

먼저, machsql 프로그램을 이용하여 필요한 테이블을 생성하여야 합니다.
예제에서는 sample_table이라는 테이블을 미리 생성한 뒤에 샘플 코드를 이용하는 방식을 사용했습니다.

```bash
[mach@localhost jdbc]$ machsql
=================================================================
     Machbase Client Query Utility
     Release Version 3.5.0.826b8f2.official
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved.
=================================================================
Machbase server address (Default:127.0.0.1):
Machbase rser ID  (Default:SYS)
Machbase user password: MANAGER
MACHBASE_CONNECT_MODE=INET, PORT=5656
mach> create table sample_table(d1 short, d2 integer, d3 long, f1 float, f2 double, name varchar(20), text text, bin binary, v4 ipv4, v6 ipv6, dt datetime);
Created successfully.
mach> exit
[mach@localhost jdbc]$
```

```java
import java.util.*;
import java.sql.*;
import com.machbase.jdbc.*;
 
public class Sample2Insert
{
    public static Connection connect()
    {
        Connection conn = null;
        try
        {
 
            String sURL = "jdbc:machbase://localhost:5656/machbasedb";
 
            Properties sProps = new Properties();
            sProps.put("user", "sys");
            sProps.put("password", "manager");
 
            Class.forName("com.machbase.jdbc.MachDriver");
 
            conn = DriverManager.getConnection(sURL, sProps);
 
        }
        catch ( ClassNotFoundException ex )
        {
            System.err.println("Exception : unable to load mach jdbc driver class");
        }
        catch ( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
 
        return conn;
    }
 
 
    public static void main(String[] args) throws Exception
    {
        Connection conn = null;
        Statement stmt = null;
        String sql;
 
        try
        {
            conn = connect();
            if( conn != null )
            {
                System.out.println("mach JDBC connected.");
 
                stmt = conn.createStatement();
 
                for(int i=1; i<10; i++)
                {
                    sql = "INSERT INTO SAMPLE_TABLE VALUES (";
                    sql += (i - 5) * 6552;//short
                    sql += ","+ ((i - 5) * 429496728);//integer
                    sql += ","+ ((i - 5) * 922337203685477580L);//long
                    sql += ","+ 1.23456789+"e"+((i<=5)?"":"+")+((i-5)*7);//float
                    sql += ","+ 1.23456789+"e"+((i<=5)?"":"+")+((i-5)*61);//double
                    sql += ",'id-"+i+"'";//varchar
                    sql += ",'name-"+i+"'";//text
                    sql += ",'aabbccddeeff'";//binary
                    sql += ",'192.168.0."+i+"'";//ipv4
                    sql += ",'::192.168.0."+i+"'";
                    sql += ",TO_DATE('2014-08-0"+i+"','YYYY-MM-DD')";//dt
                    sql += ")";
 
                    stmt.execute(sql);
 
                    System.out.println( i+" record inserted.");
                }
 
                String query = "SELECT d1, d2, d3, f1, f2, name, text, bin, to_hex(bin), v4, v6, to_char(dt,'YYYY-MM-DD') as dt from SAMPLE_TABLE";
                ResultSet rs = stmt.executeQuery(query);
                while( rs.next () )
                {
                    short d1 = rs.getShort("d1");
                    int d2 = rs.getInt("d2");
                    long d3 = rs.getLong("d3");
                    float f1 = rs.getFloat("f1");
                    double f2 = rs.getDouble("f2");
                    String name = rs.getString("name");
                    String text = rs.getString("text");
                    String bin = rs.getString("bin");
                    String hexbin = rs.getString("to_hex(bin)");
                    String v4 = rs.getString("v4");
                    String v6 = rs.getString("v6");
                    String dt = rs.getString("dt");
 
                    System.out.print("d1: " + d1);
                    System.out.print(", d2: " + d2);
                    System.out.print(", d3: " + d3);
                    System.out.print(", f1: " + f1);
                    System.out.print(", f2: " + f2);
                    System.out.print(", name: " + name);
                    System.out.print(", text: " + text);
                    System.out.print(", bin: " + bin);
                    System.out.print(", hexbin: "+hexbin);
                    System.out.print(", v4: " + v4);
                    System.out.print(", v6: " + v6);
                    System.out.println(", dt: " + dt);
 
                }
                rs.close();
            }
        }
        catch( SQLException se )
        {
            System.err.println("SQLException : " + se.getMessage());
        }
        catch( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        finally
        {
            if( stmt != null )
            {
                stmt.close();
                stmt = null;
            }
            if( conn != null )
            {
                conn.close();
                conn = null;
            }
        }
    }
}
```
이제 소스 코드를 컴파일하고 실행합니다. 이미 작성한 Makefile을 이용합니다.

```bash
[mach@localhost jdbc]$ make
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$ make run_sample2
make run_sample2
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample2Insert
mach JDBC connected.
1 record inserted.
2 record inserted.
3 record inserted.
4 record inserted.
5 record inserted.
6 record inserted.
7 record inserted.
8 record inserted.
9 record inserted.
d1: 26208, d2: 1717986912, d3: 3689348814741910320, f1: 1.2345679E28, f2: 1.23456789E244, name: id-9, text: name-9, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.9, v6: 0:0:0:0:0:0:c0a8:9, dt: 2014-08-09
d1: 19656, d2: 1288490184, d3: 2767011611056432740, f1: 1.2345678E21, f2: 1.23456789E183, name: id-8, text: name-8, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.8, v6: 0:0:0:0:0:0:c0a8:8, dt: 2014-08-08
d1: 13104, d2: 858993456, d3: 1844674407370955160, f1: 1.23456788E14, f2: 1.23456789E122, name: id-7, text: name-7, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.7, v6: 0:0:0:0:0:0:c0a8:7, dt: 2014-08-07
d1: 6552, d2: 429496728, d3: 922337203685477580, f1: 1.2345679E7, f2: 1.23456789E61, name: id-6, text: name-6, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.6, v6: 0:0:0:0:0:0:c0a8:6, dt: 2014-08-06
d1: 0, d2: 0, d3: 0, f1: 1.2345679, f2: 1.23456789, name: id-5, text: name-5, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.5, v6: 0:0:0:0:0:0:c0a8:5, dt: 2014-08-05
d1: -6552, d2: -429496728, d3: -922337203685477580, f1: 1.2345679E-7, f2: 1.23456789E-61, name: id-4, text: name-4, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.4, v6: 0:0:0:0:0:0:c0a8:4, dt: 2014-08-04
d1: -13104, d2: -858993456, d3: -1844674407370955160, f1: 1.2345679E-14, f2: 1.23456789E-122, name: id-3, text: name-3, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.3, v6: 0:0:0:0:0:0:c0a8:3, dt: 2014-08-03
d1: -19656, d2: -1288490184, d3: -2767011611056432740, f1: 1.2345679E-21, f2: 1.23456789E-183, name: id-2, text: name-2, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.2, v6: 0:0:0:0:0:0:c0a8:2, dt: 2014-08-02
d1: -26208, d2: -1717986912, d3: -3689348814741910320, f1: 1.2345679E-28, f2: 1.23456789E-244, name: id-1, text: name-1, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.1, v6: 0:0:0:0:0:0:c0a8:1, dt: 2014-08-01
```

### 데이터 입력 및 출력 예제 (2) PreparedStatement 이용한 입력

PreparedStatement를 이용하여 데이터를 입력하고 출력하는 예제를 작성하여 보기로 합니다.

소스 파일명은 Sample3PrepareStmt.java 로 합니다.

```java
import java.util.*;
import java.sql.*;
import java.text.SimpleDateFormat;
import com.machbase.jdbc.*;
 
public class Sample3PrepareStmt
{
    public static Connection connect()
    {
        Connection conn = null;
        try
        {
            String sURL = "jdbc:machbase://localhost:5656/machbasedb";
 
            Properties sProps = new Properties();
            sProps.put("user", "sys");
            sProps.put("password", "manager");
 
            Class.forName("com.machbase.jdbc.MachDriver");
 
            conn = DriverManager.getConnection(sURL, sProps);
 
        }
        catch ( ClassNotFoundException ex )
        {
            System.err.println("Exception : unable to load mach jdbc driver class");
        }
        catch ( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        return conn;
    }
 
    public static void main(String[] args) throws Exception
    {
        Connection conn = null;
        Statement stmt = null;
        machPreparedStatement preStmt = null;
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss SSS");
 
        try
        {
            conn = connect();
            if( conn != null )
            {
                System.out.println("mach JDBC connected.");
 
                stmt = conn.createStatement();
                preStmt = (machPreparedStatement)conn.prepareStatement("INSERT INTO SAMPLE_TABLE VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
 
                String ipStr = null;
                String dateStr = null;
                for(int i=1; i<10; i++)
                {
                    ipStr = String.format("172.16.0.%d",i);
                    dateStr = String.format("2014-08-09 12:23:34 %03d", i);
                    byte[] bin = new byte[20];
                    for(int j=0;j<20;j++){
                        bin[j]=(byte)(Math.random()*255);
                    }
                    java.util.Date day = sdf.parse(dateStr);
                    java.sql.Date sqlDate = new java.sql.Date(day.getTime());
 
                    preStmt.setShort(1, (i-5) * 3276 );
                    preStmt.setInt(2, (i-5) * 214748364 );
                    preStmt.setLong(3, (i-5) * 922337203685477580L );
                    preStmt.setFloat(4, 1.23456789101112131415*Math.pow(10,i));
                    preStmt.setDouble(5, 1.23456789101112131415*Math.pow(10,i*10));
                    preStmt.setString(6, String.format("varchar-%d",i));
                    preStmt.setString(7, String.format("text-%d",i));
                    preStmt.setBytes(8, bin);
                    preStmt.setIpv4(9, ipStr);
                    preStmt.setIpv6(10, "::"+ipStr);
                    preStmt.setDate(11, sqlDate);
                    preStmt.executeUpdate();
 
                    System.out.println( i+" record inserted.");
                }
 
                //date type format : YYYY-MM-DD HH24:MI:SS mmm:uuu:nnnn
                String query = "SELECT d1, d2, d3, f1, f2, name, text, bin, to_hex(bin), v4, v6, to_char(dt,'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn') as dt from SAMPLE_TABLE";
                ResultSet rs = stmt.executeQuery(query);
                while( rs.next () )
                {
                    short d1 = rs.getShort("d1");
                    int d2 = rs.getInt("d2");
                    long d3 = rs.getLong("d3");
                    float f1 = rs.getFloat("f1");
                    double f2 = rs.getDouble("f2");
                    String name = rs.getString("name");
                    String text = rs.getString("text");
                    String bin = rs.getString("bin");
                    String hexbin = rs.getString("to_hex(bin)");
                    String v4 = rs.getString("v4");
                    String v6 = rs.getString("v6");
                    String dt = rs.getString("dt");
 
                    System.out.print("d1: " + d1);
                    System.out.print(", d2: " + d2);
                    System.out.print(", d3: " + d3);
                    System.out.print(", f1: " + f1);
                    System.out.print(", f2: " + f2);
                    System.out.print(", name: " + name);
                    System.out.print(", text: " + text);
                    System.out.print(", bin: " + bin);
                    System.out.print(", hexbin: "+hexbin);
                    System.out.print(", v4: " + v4);
                    System.out.print(", v6: " + v6);
                    System.out.println(", dt: " + dt);
                }
                rs.close();
            }
        }
        catch( SQLException se )
        {
            System.err.println("SQLException : " + se.getMessage());
        }
        catch( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        finally
        {
            if( stmt != null )
            {
                stmt.close();
                stmt = null;
            }
            if( conn != null )
            {
                conn.close();
                conn = null;
            }
        }
    }
}
```
이제 소스 코드를 컴파일하고 실행해 봅니다. 이미 작성한 Makefile을 이용합니다.

Sample2Insert.java에서 입력한 데이터가 함께 출력되고 있다는 점에 유의해야 합니다.

```bash
[mach@localhost jdbc]$ make
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . Sample1Connect.java
Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$ make run_sample3
make run_sample3
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample3PrepareStmt
Mach JDBC connected.
1 record inserted.
2 record inserted.
3 record inserted.
4 record inserted.
5 record inserted.
6 record inserted.
7 record inserted.
8 record inserted.
9 record inserted.
d1: 13104, d2: 858993456, d3: 3689348814741910320, f1: 754454.6, f2: 453821.380752063, name:
varchar-9, text: text-9, bin: ?+,??r?J?????S)n?, hexbin:
A4C9A8D491D6728B4AACB39EE5FC5300296EFA9F, v4: 172.16.0.9, v6: 0:0:0:0:0:0:ac10:9, dt:
2014-08-09 12:23:34 009:000:000
?h???a?, hexbin: 6C20F09329ABBA3E7DE501C30DA368D6EFC961EF, v4: 172.16.0.8, v6:
0:0:0:0:0:0:ac10:8, dt: 2014-08-09 12:23:34 008:000:000
d1: 6552, d2: 429496728, d3: 1844674407370955160, f1: 2664182.0, f2: 1357910.1926900472, name:
varchar-7, text: text-7, bin: ????Uls?q?H?I?&(?, hexbin:
B5A0A2EFA185556C73BF719448BD49C92628F8C6, v4: 172.16.0.7, v6: 0:0:0:0:0:0:ac10:7, dt:
2014-08-09 12:23:34 007:000:000
d1: 3276, d2: 214748364, d3: 922337203685477580, f1: 443847.1, f2: 9342855.256576871, name:
varchar-6, text: text-6, bin: ??>x??Eu?? ?Iw??+n, hexbin:
BC973E78F5B44575D6CC15F94977DAE62B6E1D0E, v4: 172.16.0.6, v6: 0:0:0:0:0:0:ac10:6, dt:
2014-08-09 12:23:34 006:000:000
d1: 0, d2: 0, d3: 0, f1: 1283723.1, f2: 1771261.2019240903, name: varchar-5, text: text-5,
bin: &== j?j3?? T??y?
??, hexbin: 263D3D1C6AF56A33F79D0C54A5C479A4030AFE8B, v4: 172.16.0.5, v6: 0:0:0:0:0:0:ac10:5,
dt: 2014-08-09 12:23:34 005:000:000
d1: -3276, d2: -214748364, d3: -922337203685477580, f1: 9447498.0, f2: 7529392.937964935,
name: varchar-4, text: text-4, bin: ?Sw ??)? ?h2?E??/?, hexbin:
C653771DD2DF29CDB30ED96832E745D3D7A52FD2, v4: 172.16.0.4, v6: 0:0:0:0:0:0:ac10:4, dt:
2014-08-09 12:23:34 004:000:000
d1: -6552, d2: -429496728, d3: -1844674407370955160, f1: 9589634.0, f2: 5994172.201347323,
name: varchar-3, text: text-3, bin: 9aB,.????L/?=3,?`?f, hexbin:
3961422C2EA39BE6F2964C2FCD3D332C8960A466, v4: 172.16.0.3, v6: 0:0:0:0:0:0:ac10:3, dt:
2014-08-09 12:23:34 003:000:000
d1: -9828, d2: -644245092, d3: -2767011611056432740, f1: 7409537.5, f2: 2313739.6613546023,
name: varchar-2, text: text-2, bin: _? N?3 ?? ??~H ??= 8, hexbin:
5F84144EF63320F3C718B0FD7E4809A4CB3D1838, v4: 172.16.0.2, v6: 0:0:0:0:0:0:ac10:2, dt:
2014-08-09 12:23:34 002:000:000
d1: -13104, d2: -858993456, d3: -3689348814741910320, f1: 596626.75, f2: 2649492.1936065694,
name: varchar-1, text: text-1, bin: ???d??Wu$v? 7m?-, hexbin:
E8D0C564B4EB57E59B08752476FC07376DBF2D14, v4: 172.16.0.1, v6: 0:0:0:0:0:0:ac10:1, dt:
2014-08-09 12:23:34 001:000:000
d1: 26208, d2: 1717986912, d3: 3689348814741910320, f1: 1.2345679E28, f2: 1.23456789E244,
name: id-9, text: name-9, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.9, v6: 0:0:0:0:0:0:c0a8:9, dt: 2014-08-09 00:00:00 000:000:000
d1: 19656, d2: 1288490184, d3: 2767011611056432740, f1: 1.2345678E21, f2: 1.23456789E183,
name: id-8, text: name-8, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.8, v6: 0:0:0:0:0:0:c0a8:8, dt: 2014-08-08 00:00:00 000:000:000
d1: 13104, d2: 858993456, d3: 1844674407370955160, f1: 1.23456788E14, f2: 1.23456789E122,
name: id-7, text: name-7, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.7, v6: 0:0:0:0:0:0:c0a8:7, dt: 2014-08-07 00:00:00 000:000:000
d1: 6552, d2: 429496728, d3: 922337203685477580, f1: 1.2345679E7, f2: 1.23456789E61, name:
id-6, text: name-6, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.6, v6:
0:0:0:0:0:0:c0a8:6, dt: 2014-08-06 00:00:00 000:000:000
d1: 0, d2: 0, d3: 0, f1: 1.2345679, f2: 1.23456789, name: id-5, text: name-5, bin:
aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.5, v6: 0:0:0:0:0:0:c0a8:5, dt:
2014-08-05 00:00:00 000:000:000
d1: -6552, d2: -429496728, d3: -922337203685477580, f1: 1.2345679E-7, f2: 1.23456789E-61,
name: id-4, text: name-4, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.4, v6: 0:0:0:0:0:0:c0a8:4, dt: 2014-08-04 00:00:00 000:000:000
d1: -13104, d2: -858993456, d3: -1844674407370955160, f1: 1.2345679E-14, f2: 1.23456789E-122,
name: id-3, text: name-3, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.3, v6: 0:0:0:0:0:0:c0a8:3, dt: 2014-08-03 00:00:00 000:000:000
d1: -19656, d2: -1288490184, d3: -2767011611056432740, f1: 1.2345679E-21, f2: 1.23456789E-183,
name: id-2, text: name-2, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.2, v6: 0:0:0:0:0:0:c0a8:2, dt: 2014-08-02 00:00:00 000:000:000
d1: -26208, d2: -1717986912, d3: -3689348814741910320, f1: 1.2345679E-28, f2: 1.23456789E-244,
name: id-1, text: name-1, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.1, v6: 0:0:0:0:0:0:c0a8:1, dt: 2014-08-01 00:00:00 000:000:000
```

### 확장 함수 Append 예제

마크베이스 JDBC 드라이버는 많은 건수의 데이터를 빠르게 업로드하기 위한 Append 프로토콜을 지원합니다.

다음은 Append 프로토콜 사용 예제입니다. 
이전 예제에 사용된 sample_table을 그대로 이용합니다.

소스 파일명은 Sample4Append.java 라고 합니다.
data.txt에 있는 내용을 sample_table에 입력합니다.
CLI append 예제에 이용한 data.txt 파일을 복사하여 사용하기로 합니다.

```java
import java.util.*;
import java.sql.*;
import java.io.*;
import java.text.SimpleDateFormat;
import java.math.BigDecimal;
import com.machbase.jdbc.*;
 
 
public class Sample4Append
{
    protected static final String sTableName = "sample_table";
    protected static final int sErrorCheckCount = 100;
 
    public static Connection connect()
    {
        Connection conn = null;
        try
        {
            String sURL = "jdbc:machbase://localhost:5656/machbasedb";
 
            Properties sProps = new Properties();
            sProps.put("user", "sys");
            sProps.put("password", "manager");
 
            Class.forName("com.machbase.jdbc.MachDriver");
 
            conn = DriverManager.getConnection(sURL, sProps);
 
        }
        catch ( ClassNotFoundException ex )
        {
            System.err.println("Exception : unable to load mach jdbc driver class");
        }
        catch ( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        return conn;
    }
 
    public static void main(String[] args) throws Exception
    {
        Connection conn = null;
        MachStatement stmt = null;
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Calendar cal = Calendar.getInstance();
        String filename = "data.txt";
 
        try
        {
            conn = connect();
            if( conn != null )
            {
                System.out.println("Mach JDBC connected.");
 
                stmt = (MachStatement)conn.createStatement();
 
                ResultSet rs = stmt.executeAppendOpen(sTableName, sErrorCheckCount);
                ResultSetMetaData rsmd = rs.getMetaData();
 
                System.out.println("append open ok");
 
                MachAppendCallback cb = new MachAppendCallback() {
                        @Override
                        public void onAppendError(long aErrNo, String aErrMsg, String aRowMsg) {
                             System.out.format("Append Error : [%05d - %s]\n%s\n", aErrNo, aErrMsg, aRowMsg);
                        }
                    };
 
                stmt.executeSetAppendErrorCallback(cb);
 
                System.out.println("append data start");
                BufferedReader in = new BufferedReader(new FileReader(filename));
                String buf = null;
                int cnt = 0;
                long dt;
 
                long startTime = System.nanoTime();
 
                while( (buf = in.readLine()) != null )
                {
                    ArrayList<Object> sBuf = new ArrayList<Object>();
                    StringTokenizer st = new StringTokenizer(buf,",");
                    for(int i=0; st.hasMoreTokens() ;i++ )
                    {
                        switch(i){
                            case 7://binary case
                                sBuf.add(new ByteArrayInputStream(st.nextToken().getBytes())); break;
                            case 10://date case
                                java.util.Date day = sdf.parse(st.nextToken());
                                cal.setTime(day);
                                dt = cal.getTimeInMillis()*1000000; //make nanotime
                                sBuf.add(dt);
                                break;
                            default:
                                sBuf.add(st.nextToken()); break;
                        }
                    }
 
                    if( stmt.executeAppendData(rsmd, sBuf) != 1 )
                    {
                        System.err.println("Error : AppendData error");
                        break;
                    }
 
                    if( (cnt++%10000) == 0 )
                    {
                        System.out.print(".");
                    }
                    sBuf = null;
 
                }
                System.out.println("\nappend data end");
 
                long endTime = System.nanoTime();
                stmt.executeAppendClose();
                System.out.println("append close ok");
                System.out.println("Append Result : success = "+stmt.getAppendSuccessCount()+", failure = "+stmt.getAppendFailureCount());
                System.out.println("timegap " + ((endTime - startTime)/1000) + " in microseconds, " + cnt + " records" );
 
                try {
                    BigDecimal records = new BigDecimal( cnt );
                    BigDecimal gap = new BigDecimal( (double)(endTime - startTime)/1000000000 );
                    BigDecimal rps = records.divide(gap, 2, BigDecimal.ROUND_UP );
 
                    System.out.println( rps + " records/second" );
                } catch(ArithmeticException ae) {
                    System.out.println( cnt + " records/second");
                }
 
                rs.close();
            }
        }
        catch( SQLException se )
        {
            System.err.println("SQLException : " + se.getMessage());
        }
        catch( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        finally
        {
            if( stmt != null )
            {
                stmt.close();
                stmt = null;
            }
            if( conn != null )
            {
                conn.close();
                conn = null;
            }
        }
    }
}
```

Append를 할 때 date 타입 데이터는 반드시 long 타입의 나노초 단위 시간으로 변환하여 전송하여야 합니다.

```bash
[mach@localhost jdbc]$ make run_sample4
make run_sample4
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample4Append;
Mach JDBC connected.
append open ok
append data start
......
append data end
append close ok
Append Result : success = 60000, failure = 0
timegap 6905594 in microseconds, 60000 records
8688.61 records/second
```

10,000건마다 점(.)을 표시하고 있으며, 입력 소요 시간을 알 수 있습니다.

```bash
## machsql을 이용하여 실제 입력된 건수를 확인해보자.
## Sample2Insert,Sample3PrepareStmt에서 입력한 건수와 함께 60018건이 입력된 것을 확인합니다.
 
 
[mach@localhost jdbc]$ machsql
=================================================================
     Machbase Client Query Utility
     Release Version 3.0.0
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved.
=================================================================
Machbase server address (Default:127.0.0.1):
Machbase user ID  (Default:SYS)
Machbase user password: MANAGER
MACH_CONNECT_MODE=INET, PORT=5656
mach> select count(*) from sample_table;
count(*)            
-----------------------
60018               
[1] row(s) selected.
```
