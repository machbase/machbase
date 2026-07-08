---
type: docs
title: '8.5 전체 SDK 레퍼런스'
weight: 95
tocSort: true
---


## jdbc


## JDBC 개요

자바 프로그래밍 언어로 만들어진 데이터베이스 조작 인터페이스의 집합을 JDBC(Java DataBase Connectivity)라고 합니다. 다양한 관계형 데이터베이스를 위해 일관된 인터페이스를 제공하는 API 집합으로서 프로그래머가 SQL 요구를 만드는데 사용할 일련의 객체지향 프로그램의 클래스들을 정의하고 있습니다. 즉, 어떤 데이터베이스를 사용하더라도 JDBC 드라이버만 제공된다면 코드 수정 없이 바로 적용 가능한 장점이 있습니다.

## 표준 JDBC 함수

[표준 함수 스펙 4.0](https://www.oracle.com/java/technologies/javase/javase-tech-database.html#corespec40)

## JDBC 인증 방식

> **참고**: AUTH KEY challenge 인증은 Machbase 8.5 이상에서 지원됩니다.

Machbase JDBC는 기존 비밀번호 인증과 함께 공개키 기반 challenge 인증을 지원합니다.

### 비밀번호 인증

기존과 동일하게 `user`, `password`를 사용합니다.

### AUTH KEY challenge 인증

challenge 인증은 다음 속성을 사용합니다.

- `AUTH_MODE`
  - `PASSWORD` 또는 `CHALLENGE`
- `AUTH_SIG_SCHEME`
  - `ECDSA`
  - `RSA_PKCS1_V15`
  - `RSA_PSS`
- `AUTH_KEY_FILE`
  - 로컬 PEM 개인키 파일 경로

설명:

- `AUTH_MODE=CHALLENGE`에서는 `password`를 인증에 사용하지 않습니다.
- `AUTH_KEY_FILE`은 필수입니다.
- `AUTH_SIG_SCHEME`를 생략하면 키 파일 기반으로 기본 스킴을 자동 선택합니다.
  - EC 키: `ECDSA`
  - RSA 키: `RSA_PKCS1_V15`
- 지원 키 파라미터는 ECDSA `P-256`, `P-384`, `P-521` 및 RSA `2048`, `3072`, `4096` bits입니다.
- RSA-PSS 인증을 사용하려면 `AUTH_SIG_SCHEME=RSA_PSS`를 명시합니다.
- `AUTH_KEY_FILE`만 주고 `AUTH_MODE`를 생략하면 내부적으로 `CHALLENGE`로 처리합니다.
- 개인키 파일은 절대 경로 사용을 권장합니다. 상대 경로는 JVM의 현재 작업 디렉터리 기준으로 해석됩니다.
- POSIX 환경에서는 개인키 파일 권한을 `600`으로 제한하는 것을 권장합니다.

### Properties 예제

```java
String sURL = "jdbc:machbase://127.0.0.1:5656/machbasedb";

Properties sProps = new Properties();
sProps.put("user", "app_user");
sProps.put("AUTH_MODE", "CHALLENGE");
sProps.put("AUTH_SIG_SCHEME", "ECDSA");
sProps.put("AUTH_KEY_FILE", "/opt/machbase/keys/app_user_ecdsa.pem");

Class.forName("com.machbase.jdbc.MachDriver");
Connection conn = DriverManager.getConnection(sURL, sProps);
```

### URL query string 예제

```text
jdbc:machbase://127.0.0.1:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_SIG_SCHEME=ECDSA&AUTH_KEY_FILE=/opt/machbase/keys/app_user_ecdsa.pem
```

다만 키 파일 경로를 URL에 포함하면 로그나 설정 덤프에 더 쉽게 노출될 수 있으므로, 일반적으로는 `Properties` 사용을 권장합니다.

### reconnect 동작

- 초기 연결이 `AUTH_MODE=CHALLENGE`였다면 reconnect도 challenge 인증을 다시 수행합니다.
- reconnect 시 이전 nonce나 signature를 재사용하지 않습니다.
- challenge 실패 시 password fallback을 자동으로 수행하지 않습니다.

## JDBC 연결 옵션

드라이버는 `Properties` 또는 URL query string으로 연결 옵션을 받습니다.
현재 DBMS standard 소스에서 처리하는 공개 옵션은 다음과 같습니다.

| 옵션 | 설명 |
| -- | -- |
| `user` / `password` | 비밀번호 인증 계정 정보 |
| `AUTH_MODE`, `AUTH_SIG_SCHEME`, `AUTH_KEY_FILE` | 위에서 설명한 challenge 인증 옵션 |
| `TIMEZONE` | `+0900` 같은 세션 timezone 문자열. 잘못된 timezone 문자열은 연결 설정 오류로 처리됩니다. |
| `randomHost` | `true`이면 파싱된 host 목록에서 연결 대상을 무작위로 선택합니다. |
| `maxStatements` | pooled connection에서 사용할 최대 cached statement 개수 |
| `CONNECTION_TIMEOUT` | socket connect timeout(초). `0`은 유한 timeout 없음 |
| `SOCKET_TIMEOUT` | socket read timeout(초). `0`은 유한 timeout 없음 |
| `characterEncoding` | 클라이언트 문자 인코딩 이름 |

## 확장 JDBC 함수

### setIpv4

```java
void setIpv4(int ind, String ipString)
```

PrepareStatement에서 IPv4 주소 타입을 입력하기 위한 함수입니다.

컬럼 인덱스와 IPv4 문자열을 인자로 받습니다.

### setIpv6

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

### executeAppendFlush

```java
int executeAppendFlush()
```

현재 append stream을 flush하고 pending append response를 확인합니다. 결과값으로 성공하면 1을 리턴합니다.

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

### getAppendFailureCount

```java
long getAppendFailureCount()
```
Statement에서 Append 프로토콜을 위한 것으로 실패한 개수를 리턴합니다.

결과값으로 실패한 개수를 리턴합니다.

### Batch append 구현 참고

소스에는 batch append 쓰기를 위한 내부 프로토콜 메서드 `executeAppendAll`, `executeAppendAllByTime`이 있습니다. 확인한 DBMS standard 소스에서는 공개 `MachStatement` 메서드로 노출되어 있지 않으므로, 별도 public wrapper가 제공되기 전에는 위에 문서화한 공개 append 메서드를 사용합니다.

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

SAMPLE_SRC = MakeData.java Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java

all: build

build:
    -@rm -rf *.class
    javac -classpath $(CLASSPATH) -d . $(SAMPLE_SRC)

create_table:
    machsql -s localhost -u sys -p manager -f createTable.sql

select_table:
    machsql -s localhost -u sys -p manager -f selectTable.sql

make_data_file:
    java -classpath $(CLASSPATH) MakeData

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
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . MakeData.java Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
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
                System.out.println("machbase JDBC connected.");
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
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . MakeData.java Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$ make run_sample1
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample1Connect
machbase JDBC connected.
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
     Release Version 8.5.4.develop
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved.
=================================================================
Machbase server address (Default:127.0.0.1):
Machbase rser ID  (Default:SYS)
Machbase user password: MANAGER
MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
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
                System.out.println("machbase JDBC connected.");

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
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . MakeData.java Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$ make run_sample2
make run_sample2
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample2Insert
machbase JDBC connected.
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
        MachPreparedStatement preStmt = null;
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss SSS");

        try
        {
            conn = connect();
            if( conn != null )
            {
                System.out.println("machbase JDBC connected.");

                stmt = conn.createStatement();
                preStmt = (MachPreparedStatement)conn.prepareStatement("INSERT INTO SAMPLE_TABLE VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");

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
MakeData.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$ make run_sample3
make run_sample3
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample3PrepareStmt
machbase JDBC connected.
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
Append 샘플 실행 전에 `make_data_file` target으로 data.txt를 생성합니다.

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
                System.out.println("machbase JDBC connected.");

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
machbase JDBC connected.
append open ok
append data start
......
append data end
append close ok
Append Result : success = 100000, failure = 0
timegap 6905594 in microseconds, 100000 records
8688.61 records/second
```

10,000건마다 점(.)을 표시하고 있으며, 입력 소요 시간을 알 수 있습니다.

```bash
## machsql을 이용하여 실제 입력된 건수를 확인해보자.
## Sample2Insert,Sample3PrepareStmt에서 입력한 건수와 함께 100018건이 입력된 것을 확인합니다.


[mach@localhost jdbc]$ machsql
=================================================================
     Machbase Client Query Utility
     Release Version 8.5.4.develop
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved.
=================================================================
Machbase server address (Default:127.0.0.1):
Machbase user ID  (Default:SYS)
Machbase user password: MANAGER
MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
mach> select count(*) from sample_table;
count(*)
-----------------------
100018
[1] row(s) selected.
```

## python


## 개요

이 문서는 2.3 패키지를 기준으로 정리했습니다. PyPI 패키지명은 `machbaseapi`(소문자)이고 구현은 순수 Python입니다(네이티브 `.so/.dll/.dylib` 불필요).

기존 `machbase` 사용 흐름은 유지됩니다.

- 패키지 설치명: `machbaseapi`
- 기존과 동일하게 `import machbaseAPI` 사용
- DB-API 방식 `connect()`, `cursor()` 지원
- `append*`는 `on_ack` 콜백을 추가할 수 있어 ACK 관찰 가능
- `append()`, `appendByTime()`, `appendData()`, `appendDataByTime()`는 타입 리스트를 생략해도 동작합니다. 서버 메타데이터 기반으로 타입을 자동 추론합니다.
- 2.3부터 append row의 마지막 일부 컬럼을 생략하면 append null-bit를 통해 `NULL`로 저장합니다.
- TAG 테이블은 `value` 컬럼까지 필수이며, 이후 추가 컬럼과 metadata 컬럼은 생략 시 `NULL`로 저장할 수 있습니다.
- 커넥션 풀 옵션(`pool_name`, `pool_size`, `pool_reset_session`) 미지원

아래 예제는 기존 `machbase` 클래스 기반 레거시 스크립트를 대상으로 합니다.

## 설치

### 요구 사항

- `pip`을 사용할 수 있는 Python 3.6 이상
- 접속 가능한 Machbase 서버와 계정 정보(기본 계정 `SYS/MANAGER`, 포트 `5656`)
- 2.3은 네이티브 라이브러리 의존성이 없습니다.

### PyPI에서 설치

```bash
pip3 install machbaseapi
```

`pip3`가 PATH에 없다면 `python3 -m pip install machbaseapi` 명령을 사용합니다.

### 모듈 확인

```bash
python3 - <<'PY'
from machbaseAPI import machbase, connect
print('machbase 클래스 import:', bool(machbase))
print('connect 함수 존재:', callable(connect))
print('module import:', __import__('machbaseAPI'))
PY
```

위 명령이 성공하면 패키지를 정상적으로 import하고 인스턴스를 생성할 수 있음을 의미합니다.

DB-API 방식 샘플도 바로 사용할 수 있습니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()
cur.execute('SELECT * FROM m$tables LIMIT 1')
print(cur.fetchall())
conn.close()
```

## 빠르게 시작하기

아래 스니펫은 로컬 서버에 접속해 샘플 테이블을 만들고, 데이터를 삽입한 뒤 조회하고 세션을 종료하는 흐름을 보여줍니다.

```python
#!/usr/bin/env python3
import json
from machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_sample')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = (
            "create table py_sample ("
            "ts datetime,"
            "device varchar(40),"
            "value double"
            ")"
        )
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        for seq in range(3):
            sql = (
                "insert into py_sample values ("
                f"to_date('2024-01-0{seq+1}','YYYY-MM-DD'),"
                f"'sensor-{seq}',"
                f"{20.5 + seq}"
                ")"
            )
            if db.execute(sql) == 0:
                raise SystemExit(db.result())
            print('insert result:', db.result())

        if db.select('select * from py_sample order by ts') == 0:
            raise SystemExit(db.result())

        while True:
            rc, payload = db.fetch()
            if rc == 0:
                break
            row = json.loads(payload)
            print('row:', row)

        db.selectClose()
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

## 결과 처리

대다수 `machbase` 메서드는 성공 시 `1`, 실패 시 `0`을 반환합니다. 호출 직후 `db.result()`를 사용하면 서버에서 반환한 JSON 형식의 페이로드를 확인할 수 있습니다. `select()` 결과를 순회할 때는 `(0, None)`가 반환될 때까지 `db.fetch()`를 반복 호출하고, 마지막에 `db.selectClose()`로 리소스를 해제합니다.

## 지원 API 매트릭스

| 클래스 | API | 설명 | 반환 |
| -- | -- | -- | -- |
| `machbase` | `open(host, user, password, port)` | 기본 계정과 포트로 Machbase 서버에 연결합니다. | 성공 시 `1`, 실패 시 `0` |
| `machbase` | `openEx(host, user, password, port, conn_str)` | 추가 연결 문자열 속성을 사용해 확장 연결을 수행합니다. | `1` 또는 `0` |
| `machbase` | `close()` | 현재 세션을 종료합니다. | `1` 또는 `0` |
| `machbase` | `isOpened()` | 핸들이 열려 있는지 확인합니다. | `1` 또는 `0` |
| `machbase` | `isConnected()` | 서버와의 연결 상태를 확인합니다. | `1` 또는 `0` |
| `machbase` | `execute(sql)` | SQL을 직접 실행합니다. `SELECT`, `WITH`, `DESC`, `DESCRIBE`, `SHOW`는 `select()`로 처리하고, 그 외 SQL은 `exec_direct()`로 실행합니다. | `1` 또는 `0` |
| `machbase` | `schema(sql)` | 스키마 관련 명령을 실행합니다. | `1` 또는 `0` |
| `machbase` | `tables()` | 모든 테이블의 메타데이터를 조회합니다. | `1` 또는 `0` |
| `machbase` | `columns(table_name)` | 특정 테이블의 컬럼 메타데이터를 조회합니다. | `1` 또는 `0` |
| `machbase` | `column(table_name)` | 저수준 카탈로그 호출로 컬럼 레이아웃을 가져옵니다. | `1` 또는 `0` |
| `machbase` | `statistics(table_name, user='SYS')` | CLI를 통해 테이블 통계를 요청합니다. | `1` 또는 `0` |
| `machbase` | `select(sql)` | 스트리밍 `SELECT` 또는 `DESC`를 실행합니다. | `1` 또는 `0` |
| `machbase` | `fetch()` | `select()` 호출 이후 다음 행을 가져옵니다. | `(rc, json_str)` |
| `machbase` | `selectClose()` | 열린 결과 집합 커서를 닫습니다. | `1` 또는 `0` |
| `machbase` | `result()` | 최신 JSON 페이로드를 반환합니다. | JSON 문자열 |
| `machbase` | `appendOpen(table_name, types=None)` | 컬럼 타입 코드를 지정하여 Append 프로토콜을 시작합니다. 생략 시 서버 메타데이터로 타입을 사용할 수 있습니다. | `1` 또는 `0` |
| `machbase` | `appendData(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', on_ack=None)` | 활성 Append 세션으로 행을 추가합니다. 타입 리스트를 생략하려면 두 번째 인자로 rows를 전달합니다. 호출 시 데이터 패킷을 즉시 전송합니다. | `1` 또는 `0` |
| `machbase` | `appendDataByTime(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None, on_ack=None)` | 명시적 타임스탬프로 행을 추가합니다. 타입 리스트를 생략하려면 두 번째 인자로 rows를 전달하고 `aTimes`로 타임스탬프를 지정합니다. 호출 시 데이터 패킷을 즉시 전송합니다. | `1` 또는 `0` |
| `machbase` | `appendFlush()` | 이미 전송된 Append 데이터의 pending response를 확인하는 동기화 지점입니다. 전송 지연 버퍼를 비우는 API가 아닙니다. | `1` 또는 `0` |
| `machbase` | `appendClose()` | Append 세션을 종료합니다. | `1` 또는 `0` |
| `machbase` | `append(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS')` | 열기·추가·닫기를 한 번에 처리하는 편의 함수입니다. 타입 리스트를 생략하려면 두 번째 인자로 rows를 전달합니다. | `1` 또는 `0` |
| `machbase` | `appendByTime(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None)` | 타임스탬프 인지 Append를 위한 편의 함수입니다. 타입 리스트를 생략하려면 두 번째 인자로 rows를 전달하고 `aTimes`로 타임스탬프를 지정합니다. | `1` 또는 `0` |

## DB-API 스타일 API (2.3)

| API | 설명 | 반환 |
| -- | -- | -- |
| `connect(**kwargs)` | DB-API 연결 생성. `host`, `port`, `user`, `password` 등은 키워드 인자로 전달합니다. | `MachbaseConnection` |
| `cursor(dictionary=True)` | 커서 생성 (`True`: dict, `False`: tuple) | `MachbaseCursor` |
| `cursor.execute(sql, params=None)` | SQL 실행 | `cursor` |
| `cursor.fetchone()` | 한 건 조회 | `tuple | dict | None` |
| `cursor.fetchmany(size)` | 최대 `size`건 조회 | `list` |
| `cursor.fetchall()` | 전체 조회 | `list` |
| `cursor.close()` | 커서 종료 | `None` |
| `cursor.rowcount` | 영향 행 수 | `int` |
| `connection.append(table, rows, types=None, times=None, strict=False)` | Append 프로토콜로 row를 추가합니다. 2.3부터 trailing 컬럼 생략 시 `NULL` padding을 적용합니다. | 입력 row 수 |

## 2.3 append 타입 생략과 trailing NULL padding (권장)

`append()`와 `appendByTime()`는 타입 리스트를 생략하고 호출할 수 있습니다.
두 번째 인자로 행 집합을 그대로 전달하면 서버 메타데이터 기반으로 처리합니다.
2.3부터는 입력 row의 마지막 일부 컬럼을 생략할 수 있고, 생략된 컬럼은 append null-bit를 통해 `NULL`로 저장됩니다.

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_auto')
        db.result()
        ddl = 'create table py_append_auto(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        rows = [
            ['2024-01-01 10:00:00', 'node-1', 30.0],
            ['2024-01-01 10:01:00', 'node-1', 30.5],
        ]
        if db.append('PY_APPEND_AUTO', rows) == 0:
            raise SystemExit(db.result())
        print('append without types result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### DB-API append trailing NULL 예제

`connect().append()`도 같은 trailing `NULL` padding 규칙을 사용합니다. 중간 컬럼을 건너뛰는 positional 입력은 지원하지 않으므로, 중간 값을 `NULL`로 입력하려면 해당 위치에 `None`을 명시합니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('drop table py_append_null')
except Exception:
    pass
cur.execute('create table py_append_null(ts datetime, name varchar(20), value double, note varchar(40))')

conn.append('PY_APPEND_NULL', [
    ['2024-01-01 10:00:00', 'sensor-1', 12.3],
    ['2024-01-01 10:00:01', 'sensor-2', None, 'manual null'],
])

cur.execute('select ts, name, value, note from py_append_null order by ts')
print(cur.fetchall())
conn.close()
```

첫 번째 row는 `note` 컬럼을 생략했으므로 `NULL`로 저장됩니다. 두 번째 row는 `value` 위치에 `None`을 명시했으므로 `value`가 `NULL`로 저장됩니다.

### TAG 테이블 append와 metadata NULL 예제

TAG 테이블은 `name`, `time`, `value`에 해당하는 값까지는 반드시 입력해야 합니다. `value` 뒤에 정의한 추가 컬럼 또는 metadata 컬럼은 생략할 수 있으며, 생략된 컬럼은 `NULL`로 저장됩니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('drop table py_tag_append_null')
except Exception:
    pass
cur.execute('''
    create tag table py_tag_append_null (
        name varchar(40) primary key,
        time datetime basetime,
        value double summarized,
        status varchar(20)
    ) metadata (
        site varchar(20),
        line integer
    )
''')

conn.append('PY_TAG_APPEND_NULL', [
    ['tag-1', '2024-01-01 10:00:00', 12.3],
])

cur.execute('select name, time, value, status, site, line from py_tag_append_null')
print(cur.fetchall())
conn.close()
```

위 예제에서 `status`, `site`, `line`은 모두 `NULL`로 저장됩니다. 반대로 `value`를 생략한 TAG append는 오류로 처리됩니다.

## API 참고 및 샘플 (legacy-style `machbase` class)

아래 예제는 2.3 패키지에서도 유지되는 legacy-style `machbase` 클래스를 사용합니다.
`getSessionId()`, `count()`, `checkBit()`와 같은 API는 예전 native 패키지에는 있었지만
현재 pure-Python 구현에서는 제공되지 않습니다. 필요 시 2.3 DB-API 예제를 참고하세요.

각 스크립트에서 호스트·포트·계정 정보를 환경에 맞게 수정하세요. 모든 예제는 독립 실행이 가능하며 `python3 script.py` 형태로 실행할 수 있습니다.

### 연결 관리

#### machbase.open(), machbase.isOpened(), machbase.isConnected(), machbase.close()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    print('isOpened before open:', db.isOpened())
    print('isConnected before open:', db.isConnected())

    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    print('isOpened after open:', db.isOpened())
    print('isConnected after open:', db.isConnected())

    if db.close() == 0:
        raise SystemExit(db.result())

    print('isOpened after close:', db.isOpened())
    print('isConnected after close:', db.isConnected())

if __name__ == '__main__':
    main()
```

#### machbase.openEx()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    conn_str = 'APP_NAME=python-demo'
    if db.openEx('127.0.0.1', 'SYS', 'MANAGER', 5656, conn_str) == 0:
        raise SystemExit(db.result())
    print('connected with openEx:', db.isConnected())
    if db.close() == 0:
        raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### DML과 결과 버퍼

#### machbase.execute(), machbase.result()

```python
#!/usr/bin/env python3
import json
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_exec_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_exec_demo(id integer, note varchar(32))'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        for idx in range(2):
            sql = f"insert into py_exec_demo values ({idx}, 'row-{idx}')"
            if db.execute(sql) == 0:
                raise SystemExit(db.result())
            print('insert result:', db.result())

        if db.execute('select * from py_exec_demo order by id') == 0:
            raise SystemExit(db.result())
        payload = db.result()
        print('select payload:', payload)
        rows = json.loads(payload)
        print('decoded rows:', rows)
        print('row count:', len(rows))
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### 스트리밍 SELECT 도우미

#### machbase.select(), machbase.fetch(), machbase.selectClose()

```python
#!/usr/bin/env python3
import json
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_select_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_select_demo(id integer, value double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        for idx in range(5):
            sql = f"insert into py_select_demo values ({idx}, {idx * 1.5})"
            if db.execute(sql) == 0:
                raise SystemExit(db.result())
            print('insert result:', db.result())

        if db.select('select id, value from py_select_demo order by id') == 0:
            raise SystemExit(db.result())

        fetched = 0
        while True:
            rc, payload = db.fetch()
            if rc == 0:
                break
            print('fetched row:', json.loads(payload))
            fetched += 1
        print('fetched rows:', fetched)

        db.selectClose()
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### 스키마 도우미

#### machbase.schema()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.schema('drop table py_schema_demo')
        print('schema drop rc:', rc)
        print('schema drop result:', db.result())

        ddl = 'create table py_schema_demo(name varchar(20), created datetime)'
        if db.schema(ddl) == 0:
            raise SystemExit(db.result())
        print('schema create result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### 메타데이터와 통계

#### machbase.tables(), machbase.columns(), machbase.column(), machbase.statistics()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        if db.tables() == 0:
            raise SystemExit(db.result())
        print('tables metadata:', db.result())

        if db.columns('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('columns metadata:', db.result())

        if db.column('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('column metadata:', db.result())

        if db.statistics('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('statistics output:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Append 프로토콜 기본기

`appendOpen()`, `appendData()`, `appendFlush()`, `appendClose()`를 조합하면 행을 효율적으로 스트리밍할 수 있습니다. 2.1 이후에는 타입을 생략하고 `appendOpen()`으로 시작할 수 있습니다.
`appendData()`와 `appendDataByTime()`는 호출 시 데이터 패킷을 즉시 전송합니다. `appendFlush()`는 이미 전송된 append 데이터의 pending response를 확인하는 동기화 지점입니다.

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_append_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_append_demo(ts datetime, device varchar(32), value double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        if db.appendOpen('PY_APPEND_DEMO') == 0:
            raise SystemExit(db.result())

        rows = [
            ['2024-01-01 09:00:00', 'sensor-a', 21.5],
            ['2024-01-01 09:05:00', 'sensor-b', 22.1],
        ]
        if db.appendData('PY_APPEND_DEMO', rows) == 0:
            raise SystemExit(db.result())
        print('appendData result:', db.result())

        if db.appendFlush() == 0:
            raise SystemExit(db.result())
        print('appendFlush result:', db.result())

        if db.appendClose() == 0:
            raise SystemExit(db.result())
        print('appendClose result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Append 편의 함수

#### machbase.append()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_auto')
        db.result()
        ddl = 'create table py_append_auto(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        values = [
            ['2024-01-01 10:00:00', 'node-1', 30.0],
            ['2024-01-01 10:01:00', 'node-1', 30.5],
        ]
        if db.append('PY_APPEND_AUTO', values) == 0:
            raise SystemExit(db.result())
        print('append() result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

#### machbase.appendDataByTime(), machbase.appendByTime()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_time')
        db.result()
        ddl = 'create table py_append_time(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        rows = [
            ['2024-01-01 11:00:00', 'node-2', 40.1],
            ['2024-01-01 11:01:00', 'node-2', 40.7],
        ]
        epoch_times = [1704106800, 1704106860]

        if db.appendOpen('PY_APPEND_TIME') == 0:
            raise SystemExit(db.result())
        if db.appendDataByTime('PY_APPEND_TIME', rows, aTimes=epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendDataByTime result:', db.result())
        db.appendClose()

        if db.appendByTime('PY_APPEND_TIME', rows, aTimes=epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendByTime result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### 진단 도우미

#### machbase.checkBit()

`checkBit()`는 기존 native 기반 버전에 있던 포인터 폭 확인용 API로, 2.3 순수 Python 패키지에서는 더 이상 제공되지 않습니다.

### 저수준 바인딩

2.3 순수 Python 패키지에서는 `get_library_path()`, `openDB()`, `execAppend*()` 또는 포인터 유틸리티 API(예: `getlAddr`, `getrAddr`)와 같은 저수준 `ctypes` 인터페이스를 제공하지 않습니다.
기존 C 레이어 직접 접근이 필요한 경우에는 2.0 이전 버전(네이티브 기반 패키지)을 사용하세요.

## go


## 개요

`machgo` 패키지는 Machbase 네이티브 프로토콜에 접근하기 위한 순수 Go 클라이언트입니다.
`machcli`와 동일한 API 스타일을 제공하면서 CGo 의존성이 없습니다.
완전한 Go 툴체인으로 네이티브 포트 성능이 필요하다면 `machgo`가 좋은 선택입니다.

### machgo를 사용하는 이유

- **CGo 의존성 없음**: 순수 Go 환경으로 빌드 및 배포 가능
- **네이티브 프로토콜 접근**: Machbase 네이티브 포트(기본 `5656`)로 연결
- **machcli와의 API 호환성**: 동일한 연결/쿼리/어펜더 패턴 재사용 가능
- **운영 친화적**: 컨테이너 환경 및 크로스 플랫폼 Go 배포에 적합

### 사전 요구사항

- **Machbase server**: native port로 접근 가능한 실행 중인 DBMS 또는 Neo 서버
- **Go 1.22+**: 최신 Go 버전 권장
- **네트워크 접근**: 네이티브 포트(기본 `5656`) 접근 가능

## 시작하기

### 설치

```sh
go get github.com/machbase/neo-client@latest
```

### Import

API 패키지와 `machgo` 클라이언트 패키지를 import합니다.

```go
import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)
```

### 설정

`machgo.Config`를 사용해 호스트/포트 및 동시성 옵션을 설정합니다.

```go
conf := &machgo.Config{
    Host:         "127.0.0.1", // Machbase 서버 호스트
    Port:         5656,          // Machbase 네이티브 포트
    MaxOpenConn:  0,             // 최대 연결 임계값
    MaxOpenQuery: 0,             // 최대 쿼리 동시성 제한
}

// 데이터베이스 인스턴스 생성
// API 사용 방식은 machcli와 동일
mdb, err := machgo.NewDatabase(conf)
if err != nil {
    panic(err)
}
```

#### 설정 매개변수

| 매개변수 | 설명 | 값 |
|-----------|-------------|--------|
| `MaxOpenConn` | 최대 오픈 연결 수 | `< 0`: 무제한<br>`0`: CPU 수 × 팩터<br>`> 0`: 지정된 제한 |
| `MaxOpenConnFactor` | MaxOpenConn이 0일 때의 승수 | 기본값: 1.5 |
| `MaxOpenQuery` | 최대 동시 쿼리 수 | `< 0`: 무제한<br>`0`: CPU 수 × 팩터<br>`> 0`: 지정된 제한 |
| `MaxOpenQueryFactor` | MaxOpenQuery가 0일 때의 승수 | 기본값: 1.5 |

#### FlowControl 동작

`MaxOpenConn`과 `MaxOpenQuery`는 FlowControl 제한값입니다.
둘 중 하나라도 `-1`로 설정하면 해당 제한이 비활성화됩니다(해당 축의 FlowControl 없음).

```go
conf := &machgo.Config{
    Host:         "127.0.0.1",
    Port:         5656,
    MaxOpenConn:  -1, // connection FlowControl 비활성화
    MaxOpenQuery: -1, // query FlowControl 비활성화
}
```

### 연결 설정

```go
ctx := context.Background()
conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
if err != nil {
    panic(err)
}
defer conn.Close()
```

인증 옵션:

- `api.WithPassword(user, password)`

### 연결 단위 튜닝 옵션

`machgo`는 `Connect()` 호출 시 연결별 오버라이드를 지원합니다.
즉, `machgo.Config`의 전역 기본값은 유지하면서 연결마다 다른 튜닝이 가능합니다.

#### 반복 SQL을 위한 StatementCache

하나의 connection lifetime 동안 동일 SQL을 반복 실행하는 경우,
준비된 statement를 재사용해 성능을 향상할 수 있습니다.

기본 모드는 `machgo.Config.StatementCache`에 설정하고,
연결별로 `api.WithStatementCache(...)`로 재정의할 수 있습니다.

```go  {linenos=table,linenostart=1,hl_lines=[5,16]}
// Connection A: statement 재사용을 적극적으로 사용
connA, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheAuto),
)
if err != nil {
    panic(err)
}
defer connA.Close()

// Connection B: 이 연결에서만 statement 재사용 비활성화
connB, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheOff),
)
if err != nil {
    panic(err)
}
defer connB.Close()
```

#### FetchRows pre-fetch 크기

`FetchRows`는 서버에서 한 번의 fetch 라운드에 미리 받아올 레코드 최대 개수를 제어합니다.
기본값은 `machgo.Config.FetchRows`에 설정하고,
연결별로 `api.WithFetchRows(...)`로 재정의할 수 있습니다.
기본값은 `1000`입니다.

{{< callout type="warning" >}}
워크로드 검증 없이 `FetchRows` 값을 과도하게 크게 또는 작게 설정하지 마세요.
네트워크 레이턴시와 쿼리 특성에 따라 부적절한 값은 급격한 성능 저하와 메모리 소비 증가를 유발할 수 있습니다.
{{< /callout >}}

```go  {linenos=table,linenostart=1,hl_lines=[5]}
// Connection C: 대량 스캔 워크로드를 위한 큰 pre-fetch
connC, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithFetchRows(5000),
)
if err != nil {
    panic(err)
}
defer connC.Close()
```

{{< callout type="warning" >}}
리소스 해제를 위해 연결에는 항상 `Close()`를 호출하세요.
{{< /callout >}}

## 데이터베이스 작업

### 단일 행 쿼리 (`QueryRow`)

정확히 한 행을 기대할 때 `QueryRow`를 사용합니다.

```go
var name = "tag1"
var tm time.Time
var val float64

row := conn.QueryRow(
    ctx,
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY time DESC LIMIT 1`,
    name,
)
if err := row.Err(); err != nil {
    panic(err)
}
if err := row.Scan(&tm, &val); err != nil {
    panic(err)
}

fmt.Println("name:", name, "time:", tm.Local(), "value:", val)
```

### 다중 행 쿼리 (`Query`)

여러 행 결과를 가져올 때 `Query`를 사용합니다.

```go
rows, err := conn.Query(
    ctx,
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY time DESC LIMIT 10`,
    "tag1",
)
if err != nil {
    panic(err)
}
defer rows.Close()

for rows.Next() {
    var tm time.Time
    var val float64

    if err := rows.Scan(&tm, &val); err != nil {
        panic(err)
    }
    fmt.Println("time:", tm.Local(), "value:", val)
}
```

### 데이터 수정 (`Exec`)

INSERT, DELETE, DDL 문 실행에는 `Exec`를 사용합니다.

```go
result := conn.Exec(
    ctx,
    `INSERT INTO example_table VALUES(?, ?, ?)`,
    "tag1", time.Now(), 3.14,
)
if err := result.Err(); err != nil {
    panic(err)
}

fmt.Println("RowsAffected:", result.RowsAffected())
fmt.Println("Message:", result.Message())
```

## 고성능 대량 입력 (`Appender`)

고처리량 입력에는 전용 연결과 함께 `Appender`를 사용합니다.

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

for i := range 10_000 {
    if err := apd.Append("tag1", time.Now(), float64(i)); err != nil {
        panic(err)
    }
}
```

appender는 애플리케이션이 `Append()` 요청한 데이터를 버퍼에 쌓아두다가 지정된 임계값에 도달해야만 서버로 전송합니다.
임계값은 bytes 크기, rows 수, 버퍼에서 가장 오래된 레코드의 인입 시간과 가장 최근 레코드간의 시간 차이를 설정할 수 있으며,
이 중 한 가지라도 임계값을 초과할 경우 버퍼를 서버로 전송합니다.

서버 전송 버퍼 임계값은 아래 옵션으로 조정할 수 있습니다.

- `WithBatchMaxRows(rows)` : 기본값 `512`, 최소값 `1`
- `WithBatchMaxBytes(bytes)` : 기본값 `512KB`, 최소값 `4KB`
- `WithBatchMaxDelay(duration)` : 기본값 `5ms`, 최소값 `1ms`
- `WithBatchMaxDelay(0)`을 설정하면 시간 기반 임계조건을 사용하지 않습니다.

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

apd.WithBatchMaxBytes(1024 * 1024).    // 1 MB 임계값
    WithBatchMaxRows(2000).            // row 수 임계값
    WithBatchMaxDelay(500 * time.Millisecond) // 최대 지연 임계값
```

Appender flush 예시:

`Flush()`는 프로그래밍 방식으로 flush를 수행하는 메서드입니다.
임계값 기반 자동 flush 동작과 달리, bytes/rows/delay 임계값 설정과 무관하게 현재 버퍼의 레코드를 즉시 서버로 전송합니다.

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

{{< callout type="warning" >}}
활성 appender를 사용하는 연결에서 일반 쿼리를 함께 실행하지 마세요.
append 워크로드에는 별도 연결을 사용하세요.
{{< /callout >}}

## 전체 예제

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)

func main() {
    conf := &machgo.Config{
        Host:         "127.0.0.1",
        Port:         5656,
        MaxOpenConn:  -1,
        MaxOpenQuery: -1,
    }

    mdb, err := machgo.NewDatabase(conf)
    if err != nil {
        log.Fatal(err)
    }

    ctx := context.Background()
    conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    result := conn.Exec(ctx, `
        CREATE TAG TABLE IF NOT EXISTS sample_data (
            name VARCHAR(100) PRIMARY KEY,
            time DATETIME BASETIME,
            value DOUBLE
        )
    `)
    if err := result.Err(); err != nil {
        log.Fatal(err)
    }

    for i := 0; i < 5; i++ {
        result := conn.Exec(
            ctx,
            `INSERT INTO sample_data VALUES (?, ?, ?)`,
            fmt.Sprintf("sensor_%d", i),
            time.Now(),
            float64(i)*1.5,
        )
        if err := result.Err(); err != nil {
            log.Fatal(err)
        }
    }

    result = conn.Exec(ctx, `EXEC TABLE_FLUSH(sample_data)`)
    if err := result.Err(); err != nil {
        log.Fatal(err)
    }

    rows, err := conn.Query(ctx,
        `SELECT name, time, value FROM sample_data ORDER BY time`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    for rows.Next() {
        var name string
        var tm time.Time
        var value float64

        if err := rows.Scan(&name, &tm, &value); err != nil {
            log.Fatal(err)
        }
        fmt.Printf("Name: %s, Time: %s, Value: %.2f\n",
            name, tm.Local().Format(time.RFC3339), value)
    }
}
```

이 워크플로우는 `machcli`와 의도적으로 동일하게 만들어졌으며, 기존 코드를 최소 변경으로 마이그레이션할 수 있습니다.

## go-driver


## 개요
`github.com/machbase/neo-client` 패키지는 Machbase용 표준 Go `database/sql` 드라이버를 제공합니다.
이 드라이버는 네이티브 TCP 클라이언트를 기반으로 하며, 네이티브 포트(기본 `5656`)를 사용합니다.

애플리케이션이나 프레임워크가 Go의 `database/sql` 인터페이스를 요구한다면 이 드라이버를 사용하세요.
`database/sql` 호환이 필요 없는 신규 코드라면 일반적으로 `machgo`가 더 적합합니다.

### 사전 요구사항

- **Machbase server**: native port로 접근 가능한 실행 중인 DBMS 또는 Neo 서버
- **Go 1.22+**: `github.com/machbase/neo-client`에서 요구
- **계정 정보**: 유효한 Machbase 사용자 계정

## 시작하기

### 설치

```sh
go get github.com/machbase/neo-client@latest
```

### Import

드라이버 패키지는 blank identifier로 import합니다.
드라이버 이름 `machbase`로 자동 등록되므로 별도의 `sql.Register()` 호출은 필요하지 않습니다.

```go
import (
    "context"
    "database/sql"
    "fmt"
    "strings"

    _ "github.com/machbase/neo-client"
)
```

## 연결

### DSN 형식

가장 간단한 DSN은 `server` 키를 사용하는 방식입니다.

```text
server=tcp://sys:manager@127.0.0.1:5656
```

여기에 세미콜론으로 구분된 옵션을 추가할 수 있습니다.

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=777;statement_cache=off;io_metrics=true
```

#### 지원되는 DSN 키

| 키 | 설명 |
|----|------|
| `server`       | `tcp://user:password@127.0.0.1:5656` 형식의 서버 URL |
| `host`, `port` | 서버 호스트와 포트를 별도로 지정 |
| `user`         | 로그인 사용자 |
| `password`     | 로그인 비밀번호 |
| `fetch_rows`   | 한 번의 round trip에서 가져올 행 수 |
| `statement_cache` | statement cache 모드: `auto`, `on`, `off` |
| `io_metrics`   | I/O metrics 활성화 여부: `true`, `false` |
| `alternative_servers` | `127.0.0.2:5656` 형식의 대체 서버 주소 |
| `alternative_host`, `alternative_port` | 대체 서버 호스트와 포트를 별도로 지정 |

## 조회 예제

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"strings"

	_ "github.com/machbase/neo-client"
)

func main() {
	fields := []string{
		"server=tcp://sys:manager@127.0.0.1:5656",
		"fetch_rows=777",
		"statement_cache=off",
		"io_metrics=true",
	}

	db, err := sql.Open("machbase", strings.Join(fields, ";"))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()

	rows, err := db.QueryContext(ctx, `SELECT * FROM M$SYS_TABLES ORDER BY NAME`)
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	columns, err := rows.Columns()
	if err != nil {
		panic(err)
	}
	fmt.Println("Columns:", columns)

	var (
		name        string
		typ         int
		dbID        int64
		id          int64
		userID      int
		columnCount int
		flag        int
	)

	for rows.Next() {
		if err := rows.Scan(&name, &typ, &dbID, &id, &userID, &columnCount, &flag); err != nil {
			panic(err)
		}
		fmt.Println(name, typ, dbID, id, userID, columnCount, flag)
	}

	if err := rows.Err(); err != nil {
		panic(err)
	}
}
```

## 입력 예제

다음 예제는 `EXAMPLE`이라는 태그 테이블에 행을 삽입합니다.

```sql
CREATE TAG TABLE IF NOT EXISTS example (
    name VARCHAR(100) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
);
```

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"strings"
	"time"

	_ "github.com/machbase/neo-client"
)

func main() {
	fields := []string{
		"server=tcp://sys:manager@127.0.0.1:5656",
		"fetch_rows=777",
		"statement_cache=off",
	}

	db, err := sql.Open("machbase", strings.Join(fields, ";"))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()
	ts := time.Now()

	for i := 0; i < 10; i++ {
		result, err := db.ExecContext(
			ctx,
			`INSERT INTO EXAMPLE VALUES (?, ?, ?)`,
			"example-client",
			ts.Add(time.Second*time.Duration(i)),
			3.14*float64(i),
		)
		if err != nil {
			panic(err)
		}

		affected, err := result.RowsAffected()
		if err != nil {
			panic(err)
		}
		fmt.Println("Rows affected:", affected)
	}
}
```

## 참고 사항 및 제한 사항

- 파라미터는 `?` 형태의 positional placeholder를 사용하며, named parameter는 지원하지 않습니다.
- `database/sql`의 connection pooling은 일반적인 `sql.DB` 방식대로 동작합니다.
- 명시적 트랜잭션은 지원하지 않으므로 `Begin`, `BeginTx`는 오류를 반환합니다.
- `LastInsertId()`는 지원하지 않습니다.
- 파라미터 타입은 드라이버 구현을 따릅니다. 일반적인 SQL 타입, `time.Time`, `[]byte`, `net.IP`는 지원하지만 `bool` 파라미터는 지원하지 않습니다.

## nodejs


## 개요

Machbase TypeScript 클라이언트(`@machbase/ts-client`)는 Machbase CMI 프로토콜을 순수 TypeScript로 구현한 라이브러리입니다. Node.js 애플리케이션이 네이티브 바인딩 없이도 Machbase(스탠더드 에디션) 서버에 연결해 SQL 실행, 결과 조회, Prepared Statement 처리, 로그 데이터 Append를 수행할 수 있습니다.

이 문서는 설치 방법, 핵심 API, 실용적인 예제, 테스트 흐름, 주의해야 할 동작 특성을 다룹니다.

## 설치

### 요구 사항

- Node.js 18 이상(LTS 권장)
- 접속 가능한 Machbase 서버(스탠더드 에디션)

### npm에서 설치

패키지 매니저로 설치합니다.

```bash
npm install @machbase/ts-client
# or
yarn add @machbase/ts-client
# or
pnpm add @machbase/ts-client
```

### 오프라인 설치

Machbase에서 `.tgz` 패키지를 전달받은 경우:

```bash
# example file name; your version may differ
npm install ./machbase-ts-client-1.0.0.tgz
```

### 설치 확인

```bash
node -e "const { createConnection } = require('@machbase/ts-client'); console.log(typeof createConnection === 'function' ? 'ts-client import ok' : 'ts-client import failed')"
```

> **참고**: 이 클라이언트는 Node.js에서 TCP 소켓을 사용하며, 브라우저용 라이브러리(웹소켓 전송)를 제공하지 않습니다.
> DBMS standard 소스의 패키지 버전은 `@machbase/ts-client` 1.0.0입니다.
>
> 이 문서의 기본 계정(`SYS`/`MANAGER`)은 로컬 테스트용 예시입니다. 운영 환경에서는 전용 계정과 비밀번호를 사용하세요.

## 빠르게 시작하기

아래 예제는 로컬 서버에 연결해 샘플 테이블을 생성하고 데이터를 삽입·조회한 뒤 세션을 종료하는 흐름을 보여줍니다.

```typescript
// src/example.ts
import { createConnection } from '@machbase/ts-client';

const conn = createConnection({
  host: process.env.MACH_HOST ?? '127.0.0.1',
  port: +(process.env.MACH_PORT ?? 5656),
  user: process.env.MACH_USER ?? 'SYS',
  password: process.env.MACH_PASS ?? 'MANAGER',
});

await conn.connect();
const [rows] = await conn.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
console.log(rows);
await conn.end();
```

### CommonJS 예제

```javascript
// quickstart.js (CommonJS, Node 18+)
const { createConnection } = require('@machbase/ts-client');

async function main() {
  const conn = createConnection({
    host: '127.0.0.1',
    user: 'SYS',
    password: 'MANAGER',
    port: 5656,
  });
  await conn.connect();

  const [rows] = await conn.query('SELECT * FROM V$TABLES ORDER BY NAME LIMIT ?', [10]);
  console.table(rows);

  await conn.end();
}

main().catch(err => console.error('Unexpected failure:', err));
```

> **트랜잭션 안내:** Machbase는 모든 명령을 자동 커밋합니다. `BEGIN`, `COMMIT`, `ROLLBACK` 같은 명령은 항상 에러를 반환하므로, 트랜잭션을 지원하지 않음을 확인하는 용도로만 사용하십시오.

### Machbase 페이사드

익숙한 Node.js SQL 클라이언트 스타일을 선호한다면 `createConnection()`으로 제공되는 페이사드를 사용할 수 있습니다.

```javascript
// facade-basic.js (CommonJS)
const { createConnection } = require('@machbase/ts-client');

async function bootstrap() {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  try {
    const [rows, fields] = await conn.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [3]);
    console.log('rows', rows, 'fields', fields?.map(f => f.name));

    await new Promise((resolve, reject) =>
      conn.query('SELECT VALUE FROM V$SYSSTAT WHERE NAME = ?', ['SERVER_VERSION'], (err, result) => {
        if (err) return reject(err);
        console.log('callback result', result);
        resolve();
      })
    );
  } finally {
    await conn.end();
  }
}

bootstrap().catch(console.error);
```

페이사드는 콜백과 `.promise()`를 모두 지원하고, 실패 시 `QueryError`를 반환하며, 서버 메시지를 그대로 전달합니다.

> **페이사드 제약:** `beginTransaction`, `commit`, `rollback`은 Machbase가 SQL 트랜잭션을 지원하지 않으므로 즉시 `QueryError`를 반환합니다. LOG/TAG 테이블에 대한 `UPDATE`도 서버 오류로 바로 실패합니다.

## 자주 발생하는 문제

- **ECONNREFUSED** – 서버가 실행 중인지(`machadmin -u`), 호스트와 포트가 맞는지, 방화벽이 리스너 포트(기본 5656)의 TCP 연결을 허용하는지 확인하세요.
- **Authentication failed** – 사용자/비밀번호를 다시 확인하고 대상 데이터베이스가 생성되어 있는지(`machadmin -c`) 점검하세요.

## API 참조

### 연결 관리

#### createConnection(config)

Machbase 리스너에 네트워크 세션을 열고 CMI 핸드셰이크를 완료합니다.

| 매개변수 | 타입 | 기본값 | 설명 |
|-----------|------|---------|-------------|
| `host` | string | `127.0.0.1` | Machbase 서버 IP 또는 호스트명 |
| `port` | number | `5656` | 리스너 포트 |
| `user` | string | – | 데이터베이스 사용자(기본 `SYS`) |
| `password` | string | – | 비밀번호(기본 `MANAGER`) |
| `database` | string | `data` | 데이터베이스 이름 |
| `clientId` | string | `NPM` | 서버 로그에 표시될 클라이언트 ID |
| `showHiddenColumns` | boolean | `false` | 메타데이터에 숨김 컬럼 포함 여부 |
| `timezone` | string | 빈 값 | 선택적 타임존 식별자 |
| `connectTimeout` | number | 5000 | 소켓 연결 타임아웃(ms) |
| `queryTimeout` | number | 60000 | 명령별 타임아웃(ms) |

```javascript
const conn = createConnection({ host: '192.168.1.10', user: 'SYS', password: 'MANAGER' });
await conn.connect();
```

소켓 연결 실패, 인증 오류, 핸드셰이크 응답 이상 시 프로미스가 reject됩니다.

#### connect()

서버와의 연결을 엽니다.

```javascript
await conn.connect();
```

#### end()

소켓 연결을 종료합니다. `end()` 호출 이후 추가 작업을 시도하면 에러가 발생합니다.

```javascript
await conn.end();
```

### SQL 실행

#### execute(sql, values?)

결과 집합을 반환하지 않을 수도 있는 명령을 실행합니다. DDL(`CREATE`, `ALTER`, `DROP`)이나 DML(`INSERT`, `UPDATE`, `DELETE`)에 사용하십시오.

```javascript
const [create] = await conn.execute('CREATE TABLE demo (ID INTEGER, NAME VARCHAR(32))');
console.log('Rows affected:', create.affectedRows); // -> 0 for DDL

const [insert] = await conn.execute("INSERT INTO demo VALUES (1, 'alpha')");
console.log('Rows affected:', insert.affectedRows); // -> 1

await expectTransactionUnsupported(conn, 'COMMIT');
```

통합 테스트에서 사용하는 보조 함수:

```javascript
async function expectTransactionUnsupported(conn, sql) {
  try {
    await conn.execute(sql);
    throw new Error(`Expected ${sql} to fail because Machbase does not support transactions.`);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.log(`${sql} expected failure:`, msg);
  }
}
```

#### query(sql, values?)

행을 반환하는 쿼리를 실행합니다. 반환값은 `[rows, fields]` 형태의 2요소 튜플입니다.

```javascript
const [rows, fields] = await conn.query('SELECT ID, NAME FROM demo ORDER BY ID');
console.table(rows);
```

### Prepared Statement 사용

#### prepare(sql)

서버에 Prepared Statement를 생성합니다.

```javascript
const stmt = await conn.prepare('SELECT NAME FROM demo WHERE ID = ?');
try {
  const [rows] = await stmt.execute([1]);
  console.log(rows); // -> [ { NAME: 'alpha' } ]
} finally {
  await stmt.close();
}
```

반환된 객체에서 제공하는 메서드는 다음과 같습니다.

- `execute(parameters?)` – 문을 실행하고 `[rowsOrPacket, fields]`를 반환합니다.
- `getColumns()` – 컬럼 메타데이터 캐시를 반환합니다.
- `getLastMessage()` – 최근 서버 메시지를 확인합니다.
- `getStatementId()` – 내부 Statement ID를 조회합니다.
- `close()` – 서버 리소스를 정리합니다. 여러 번 호출해도 안전합니다.

#### Prepared Statement Examples

**Prepared SELECT 재사용:**

```javascript
const select = await conn.prepare('SELECT DEVICE_ID, SENSOR_VALUE FROM sensors WHERE DEVICE_ID = ?');
for (const { id } of samples) {
  const [rows] = await select.execute([id]);
  console.log(`selected ${id}:`, rows);
}
await select.close();
```

**Prepared Upsert:**

```javascript
const upsert = await conn.prepare(
  'INSERT INTO devices (DEVICE_ID, SENSOR_VALUE) VALUES (?, ?) ' +
  'ON DUPLICATE KEY UPDATE SET SENSOR_VALUE = ?',
);
const [result] = await upsert.execute([deviceId, firstValue, firstValue]);
console.log('Affected rows:', result.affectedRows);
await upsert.close();
```

**타입 지정 인자와 NULL 처리:**

```javascript
await update.execute([
  { value: null, type: 'varchar' },
  { value: new Date(), type: 'varchar' },
  { value: 'sensor-200', type: 'varchar' },
]);
```

실행 예제 스크립트는 보통 `npm run build` 후 `dist/examples/` 아래에 생성됩니다. 예제는 일반적으로 `MACHBASE_EXAMPLE_*`, `MACHBASE_SMOKE_*`, 마지막으로 `SYS/MANAGER@127.0.0.1` 순서로 접속 정보를 찾습니다.

### Append Protocol

#### appendBatch(table, columns, rows, options?)

`CMI_APPEND_BATCH_PROTOCOL`을 사용해 **로그 테이블**에 행을 추가합니다. 사용자에게 보이는 컬럼만 전달하면 됩니다(로그 테이블에는 `_arrival_time`, `_rid`가 자동 포함됩니다).

```javascript
const appendResult = await conn.appendBatch(
  'sensor_log',
  [
    { name: 'ID', type: 'int32' },
    { name: 'NAME', type: 'varchar' },
    { name: 'VALUE', type: 'float64' },
  ],
  [
    [1, 'alpha', 0.5],
    { values: [2, 'bravo', 1.25], arrivalTime: Date.now() * 1_000_000 },
  ],
);
console.log('Appended rows:', appendResult.rowsAppended);
```

지원 컬럼 타입: `int32`, `int64`, `float64`, `varchar`.

- `rows`는 값 배열 또는 `{ values, arrivalTime }` 객체 배열을 받을 수 있습니다. `null`은 Machbase 센티널 값으로 자동 인코딩됩니다.
- `options`는 `arrivalTime`(기본값 1개) 또는 `arrivalTimes`(행별 배열)를 지정할 수 있습니다.

반환값은 `{ table, rowsAppended, rowsFailed, message }` 형태입니다.

> **팁**: "column count does not match" 오류는 대상 테이블이 로그 테이블이 아니거나, 컬럼 순서가 스키마와 일치하지 않을 때 발생합니다. TAG 테이블에는 `appendOpen()`을 사용하세요.

#### appendOpen(table, columns, options?)

경량 Append 세션을 엽니다. 기본적으로 네이티브 APPEND open/data/close 흐름을 사용하며, 성공한 네이티브 쓰기는 청크별 응답을 반환하지 않습니다.

```javascript
const stream = await conn.appendOpen('sensor_log', [
  { name: 'ID', type: 'int32' },
  { name: 'NAME', type: 'varchar' },
  { name: 'VALUE', type: 'float64' },
]);

await stream.append([
  [1, 'alpha', 0.5],
  [2, 'bravo', 1.25],
]);

await stream.append({ values: [3, 'charlie', 2.5] });
await stream.close();
```

네이티브 Append를 끄고 Prepared Statement 기반으로 강제하려면 `MACHBASE_NATIVE_APPEND=0`을 설정하세요. 서버가 특정 테이블 타입이나 세션에서 네이티브 Append를 지원하지 않으면 페이사드가 자동으로 Prepared Statement 방식으로 폴백합니다.

TAG 테이블의 `DATETIME` 컬럼에는 `Date` 객체 또는 `bigint` epoch 값을 전달하세요.

#### append(rows) on an append stream

열린 Append 스트림으로 하나 이상의 행을 전송합니다.

```javascript
const frames = await stream.append([
  ['S-001', new Date(), 1.0],
  ['S-002', new Date(Date.now() + 1), 2.0],
]);
console.log('frames sent:', frames);
```

네이티브 모드에서는 최대 처리량을 위해 성공 응답이 생략되며, 오류가 있을 때만 실패 패킷이 반환됩니다.

### Helper Methods

#### ping()

`SELECT 1 FROM V$TABLES`로 연결 상태를 점검합니다.

```javascript
await conn.ping();
```

#### promise()

익숙한 `.promise()`와 같은 형태의 래퍼를 제공합니다.

```javascript
const p = conn.promise();
await p.ping();
const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
```

#### escape, escapeId, format

SQL 문자열을 안전하게 구성하기 위한 유틸리티입니다.

```javascript
const safeName = conn.escapeId('table_name');
const safeValue = conn.escape('user input');
```

## 테스트 및 진단

### 스크립트

- `npm run build` – TypeScript 컴파일
- `npm run lint` – `src/`에 ESLint 수행
- `npm run smoke` – 선택적 스모크 테스트(환경변수 없으면 생략)
- `npm test` – 통합 스위트(실서버 필요)
  1. 로그 테이블 생성
  2. 샘플 데이터 INSERT/SELECT
  3. 자리기반 바인딩 준비문 시연
  4. append 부하 테스트(기본: 5배치 x 200행) 및 건수 검증
  5. 각 단계에서 `COMMIT`을 호출하여 트랜잭션 미지원 동작 확인
  6. Machbase 페이사드와 `UPDATE` 제한 동작 검증

샘플 출력:

```text
COMMIT expected failure: Expected COMMIT to fail because Machbase does not support transactions.
machbase-facade-basic callback query returned 3 rows.
machbase-facade-update-log-fails message: UPDATE is not supported for LOG tables.
append-batch progress: batch 4/5 { table: 'TS_CLIENT_IT_...', rowsAppended: 200, rowsFailed: 0 }
append-batch final count: 1004
```

## 튜토리얼

### 빠른 시작 (로그 테이블)

```javascript
// quickstart-log.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', port: 5656, user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_LOG_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE LOG TABLE "${table}" (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)`);
    await conn.execute(`INSERT INTO "${table}" VALUES (1, 'A', 0.5)`);
    const [rows] = await conn.query(`SELECT * FROM "${table}" ORDER BY ID`);
    console.table(rows);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### Prepared Statement 재사용

```javascript
// prepared-reuse.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_VOL_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE VOLATILE TABLE "${table}" (ID INTEGER PRIMARY KEY, NAME VARCHAR(64))`);
    for (let i = 1; i <= 3; i++) await conn.execute(`INSERT INTO "${table}" VALUES (${i}, 'N${i}')`);
    const stmt = await conn.prepare(`SELECT NAME FROM "${table}" WHERE ID = ?`);
    try {
      for (const id of [1, 2, 3]) {
        const [rows] = await stmt.execute([id]);
        console.log(id, rows[0]?.NAME);
      }
    } finally {
      await stmt.close();
    }
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### 로그 테이블 배치 Append

```javascript
// append-batch.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_LOGAPP_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE LOG TABLE "${table}" (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)`);
    const result = await conn.appendBatch(
      table,
      [
        { name: 'ID', type: 'int32' },
        { name: 'NAME', type: 'varchar' },
        { name: 'VALUE', type: 'float64' },
      ],
      [[1, 'X', 0.5], [2, 'Y', 1.25]],
    );
    console.log(result);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### TAG 테이블 스트리밍 Append

```javascript
// append-tag-stream.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_TAG_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE TAG TABLE "${table}" (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)`);
    const stream = await conn.appendOpen(table, [
      { name: 'NAME', type: 'varchar' },
      { name: 'TIME', type: 'int64' },
      { name: 'VALUE', type: 'float64' },
    ]);
    const now = Date.now();
    await stream.append([
      ['T-0001', new Date(now), 1.0],
      ['T-0002', new Date(now + 1), 2.0],
    ]);
    await stream.close();
    const [rows] = await conn.query(`SELECT COUNT(*) AS CNT FROM "${table}"`);
    console.log('count', rows[0]?.CNT);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

> 네이티브 모드는 기본 활성화입니다. 비활성화하려면 `MACHBASE_NATIVE_APPEND=0`을 설정하세요. 성공 시 청크별 응답은 생략되고, 오류만 실패 응답으로 전달됩니다.

### Promise 래퍼와 Ping

```javascript
// promise-and-ping.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  try {
    const p = conn.promise();
    await p.ping(); // SELECT 1 FROM V$TABLES
    const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
    console.log(rows.map(r => r.NAME));
  } finally {
    await conn.end();
  }
})();
```

## 동작 특성과 한계

### 트랜잭션

Machbase는 모든 명령을 자동 커밋합니다. `BEGIN`, `COMMIT`, `ROLLBACK` 같은 트랜잭션 키워드는 항상 실패하며, 래퍼도 `QueryError`(`ERR_MACHBASE_NO_TX`)를 통해 동일하게 알립니다.

```javascript
try {
  await conn.execute('COMMIT');
} catch (err) {
  console.log('Expected error:', err.message);
  // Error: Machbase does not support transactions
}
```

### 결과 버퍼링 및 페이지네이션

래퍼의 `query` 메서드는 전체 결과 집합을 버퍼링한 뒤 반환합니다. 대용량 테이블에서는 `ORDER BY … LIMIT` 쿼리나 기본 키 범위를 이용해 직접 페이지를 나누세요.

### 파라미터 바인딩

지원 타입은 `int32`, `int64`, `float64`, `varchar` 등 범용 스칼라 타입입니다. `null`을 전달할 경우 명시적 타입을 함께 지정하세요.

```javascript
{ value: null, type: 'varchar' }
```

### Append 프로토콜

로그 테이블에는 `appendBatch`를, 점진적 유입이 필요한 경우 스트리밍 도우미(`appendOpen`/`append`)를 사용하세요. 특정 테이블 타입(예: TAG 테이블)에서 스트리밍을 지원하지 않으면 준비된 문 반복 방식으로 자동 대체됩니다. 운영 시에는 데이터를 청크로 나누고 `rowsFailed`를 확인하는 패턴이 안전합니다.

### 오류 처리

오류는 기본 `Error` 객체(래퍼 사용 시 `QueryError`)로 전달됩니다. 문제를 진단하려면 `error.message` 또는 `QueryError`의 `code`, `sql` 필드를 확인하세요. 통합 테스트는 존재하지 않는 테이블 조회와 지원하지 않는 `UPDATE`를 일부러 실행해 오류 메시지가 충분히 설명적인지 확인합니다.

### 테이블 타입별 SQL 유의사항

- **LOG/TAG 테이블**은 `SELECT`, `INSERT`, `DELETE`를 지원하며 `UPDATE`는 사용할 수 없습니다.
- **VOLATILE/LOOKUP 테이블**은 모든 DML을 지원하지만, 인덱스를 올바르게 사용하려면 `WHERE` 절에 기본 키 조건을 포함해야 합니다.

## 모범 사례

1. **항상 연결을 닫기**: `try...finally` 블록으로 `conn.end()`가 호출되도록 보장하세요.
2. **Prepared Statement 재사용**: 한 번 생성한 후 여러 번 실행하면 성능이 향상됩니다.
3. **배치 입력 활용**: 단건 INSERT 대신 `appendBatch`나 `appendOpen`으로 대량 적재를 수행하세요.
4. **오류 처리**: DB 작업을 `try...catch`로 감싸고 적절히 로깅합니다.
5. **커넥션 풀 사용**: 운영 환경에서는 커넥션 풀을 도입해 동시 요청을 안정적으로 처리하세요.
6. **쿼리 파라미터화**: SQL 인젝션을 방지하려면 문자열 결합 대신 바인딩(`?` 플레이스홀더)을 사용하세요.

## 변경 이력

### 2025-10-08

- npm, yarn, pnpm 및 오프라인 `.tgz` 설치 절차를 일반 사용자 관점으로 정리했습니다.
- Node.js 전용 런타임 제약과 연결 문제 해결 팁을 보강했습니다.
- 테이블 타입별 SQL 제약 사항을 동작 특성 섹션에 통합했습니다.

### 2025-10-03

- TAG 스트리밍 예제를 추가하고 기본 `MACHBASE_NATIVE_APPEND` 동작을 문서화했습니다.
- 네이티브 Append가 불가능할 때 Prepared Statement로 자동 폴백하는 동작을 정리했습니다.

### 2025-10-02

- Machbase 페이사드(`createConnection`, `QueryError`, `.promise()`, 페이사드 준비문)를 도입했습니다.
- 콜백/프로미스 흐름과 LOG/TAG `UPDATE` 거부 동작에 대한 통합 검증을 확장했습니다.

### 2025-09-30

- 자리기반 Prepared Statement를 추가했습니다.
- 로그 테이블용 `appendBatch`와 null 처리, 통계 반환을 추가했습니다.
- 트랜잭션, 페이지네이션, 파라미터 바인딩, append 청크, 오류 처리 예제와 통합 검증을 보강했습니다.

## dotnet


## 목차 {#index}

* [개요](#overview)
* [설치](#install)
* [NuGet(통합 8.0.54)](#nuget-unified-connector)
* [레거시 NuGet(5.x) 설치](#install-connector-via-nuget-package-manager)
* [커넥션 문자열 참고](#connection-string-reference)
* [API 레퍼런스](#api-reference)
* [사용 예시](#usage-and-examples)
* [프로토콜 4.0-full 전체 API](#full-provider-apis-protocol-40-full)

## 개요 {#overview}

Machbase는 모든 지원 Machbase 와이어 프로토콜(2.1~4.0)을 포괄하는 범용 ADO.NET 프로바이더 **UniMachNetConnector**를 제공합니다. DBMS standard 소스의 현재 통합 패키지는 `UniMachNetConnector` 8.0.54이며 `net452`, `net5.0`, `net6.0`, `net7.0`, `net8.0` 타깃을 빌드합니다. 커넥터는 실행 시 커넥션 문자열을 참고해 올바른 프로토콜을 자동으로 협상하므로, 시계열 데이터 수집·질의 워크로드에도 별도 설정 없이 적합한 프로토콜을 선택합니다.

## 설치 {#install}

설치된 Machbase 서버·클라이언트에는 `$MACHBASE_HOME/lib/` 경로에 범용 .NET 프로바이더가
함께 배포됩니다. 표준 Linux 설치에는 예를 들어 `UniMachNetConnector-net50-8.0.54.dll`과
`machNetConnector-40-net50-3.2.1.dll` 같은 프로토콜별 어셈블리가 포함될 수 있습니다.
소스 프로젝트는 필요한 .NET SDK가 있을 때 추가 target-framework flavor도 빌드할 수 있습니다.

- **UniMachNetConnector**: 프레임워크에 구애받지 않는 진입점입니다. 소스 빌드 파일 이름은
  `UniMachNetConnector-net{452|50|60|70|80}-<version>.dll` 형식이며, 배포 대상
  프레임워크에 맞는 파일을 선택합니다.
- **레거시 프로토콜 커넥터**: `machNetConnector-XX-net{40|50|60|70|80}-<version>.dll`과 같이
  프로토콜별로 나뉜 어셈블리입니다. UniMachNetConnector가 필요 시 로드합니다.

응용 프로그램에서는 대상 프레임워크에 맞는 DLL을 참조하거나, 배포 시 실행 파일과 같은 위치에 함께 배치하면 됩니다.

## NuGet로 설치 (통합 커넥터, 8.0.54) {#nuget-unified-connector}

통합 커넥터의 패키지 ID는 `UniMachNetConnector`입니다. 새 프로젝트에서는 DLL 복사 대신 NuGet 패키지 참조 방식을 권장합니다.

- 지원 TFM: net452, net5.0, net6.0, net7.0, net8.0
- net5.0 이상 빌드는 self-contained입니다. net452 빌드는 소스 프로젝트 기준
  `System.ValueTuple` 4.5.0을 restore합니다.

### 빠른 시작(명령줄)

```bash
# 프로젝트 폴더에서 실행
dotnet add package UniMachNetConnector --version 8.0.54
dotnet build
```

소스(피드)를 명시적으로 제어해야 하면 참조 추가만 하고, 별도로 복원하세요.

```bash
dotnet add package UniMachNetConnector --version 8.0.54 --no-restore

# nuget.org 메타데이터를 강제로 갱신
dotnet nuget locals http-cache --clear
dotnet restore --no-cache --source https://api.nuget.org/v3/index.json
```

### Visual Studio

- 프로젝트 마우스 오른쪽 클릭 → NuGet 패키지 관리 → 찾아보기 → “UniMachNetConnector” 검색 → 8.0.54 선택 → 설치.

### 프로젝트 파일 예시

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.54" />
  <!-- 추가 Machbase 패키지 불필요 -->
  <!-- 대상 프레임워크: net452|net5.0|net6.0|net7.0|net8.0 -->
</ItemGroup>
```

### 로컬/사내 피드 사용(선택)

사내 레지스트리 또는 폴더 피드를 사용할 경우 다음과 같이 소스를 추가하고 복원합니다. 폴더 피드는 `UniMachNetConnector.8.0.54.nupkg`를 해당 디렉터리에 배치하면 됩니다.

```bash
# 1회 설정
dotnet nuget add source /path/to/local-nuget -n mach-local

# nuget.org와 병행 복원
dotnet restore --no-cache \
  --source /path/to/local-nuget \
  --source https://api.nuget.org/v3/index.json
```

권한 제약이 있는 환경에서는 패키지 캐시 경로를 절대 경로로 지정하세요.

```bash
PKG_DIR="$(pwd)/.nuget-packages"; mkdir -p "$PKG_DIR"
NUGET_PACKAGES="$PKG_DIR" dotnet restore --no-cache --source /path/to/local-nuget
NUGET_PACKAGES="$PKG_DIR" dotnet run --no-restore
```

> 팁: 게시 직후 NU1102(지정 버전을 찾지 못함)나 “incompatible with 'all' frameworks”가 보이면 보통 인덱싱/캐시 이슈입니다. `dotnet nuget locals http-cache --clear` 후 `--no-cache`로 복원하면 해결됩니다. 패키지는 net452 및 net5.0~net8.0을 지원합니다.

### 최소 사용 예시

```csharp
using Mach.Data.MachClient;

var cs = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var conn = new MachConnection(cs);
conn.Open();

using var cmd = new MachCommand("SELECT COUNT(*) FROM V$TABLES", conn);
var count = (long)cmd.ExecuteScalar();
Console.WriteLine($"Tables: {count}");
```

## 레거시 NuGet(5.x) 설치 {#install-connector-via-nuget-package-manager}

> **참고**: Machbase .NET Connector 5.0 패키지는 NuGet에 등록되어 있으며, 통합형 UniMachNetConnector가 도입되기 이전의 독립 배포본입니다.

Visual Studio를 사용하면 기존(통합 이전) .NET Connector도 NuGet에서 받을 수 있습니다. 아래 절차는 `machNetConnector5.0` 패키지를 설치하는 방법입니다. (새 프로젝트에는 통합형 `UniMachNetConnector` 8.0.54 사용을 권장합니다.)

1. Visual Studio에서 새 C# .NET 프로젝트를 생성합니다.
2. 솔루션 탐색기에서 프로젝트 이름을 마우스 오른쪽 클릭하고 **NuGet 패키지 관리**를 선택합니다.
3. NuGet 패키지 관리자 창이 열리면 상단의 **찾아보기** 탭을 선택하고 `machNet`을 검색합니다.
4. 검색 결과 목록에서 **machNetConnector5.0**을 선택하고 **설치**를 클릭합니다.
5. **변경 내용 미리 보기** 창이 나타나면 **확인**을 눌러 설치를 계속합니다.
6. 설치가 완료되면 솔루션 탐색기 > **종속성 → 패키지**에서 설치된 패키지를 확인할 수 있습니다.
7. `Program.cs`에 `using Mach.Data.MachClient;`를 추가하면 machNetConnector API를 사용할 수 있습니다.

> 어떤 NuGet을 써야 하나요?
> - 신규/업그레이드 앱: `UniMachNetConnector` 8.0.54 권장(net452 및 net5.0~net8.0 지원, 모든 프로토콜 및 4.0-full 포함).
> - 레거시 유지: 통합 패키지로 전환이 어려울 때만 `machNetConnector5.0`을 사용하세요.

## 커넥션 문자열 참고 {#connection-string-reference}

커넥션 문자열의 각 항목은 세미콜론(`;`)으로 구분합니다. 표의 한 행에 표시된 키워드는 서로 동일한 의미를 갖습니다.

| 키워드                                                         | 설명                                                                                                  | 예시                                             | 기본값  |
|----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------|---------|
| `DSN`, `SERVER`, `HOST`                                        | 호스트명 또는 IP 주소                                                                                 | `SERVER=127.0.0.1`                               | 없음    |
| `PORT`, `PORT_NO`                                              | 수신 포트                                                                                             | `PORT=5656`                                     | `5656`  |
| `USERID`, `USERNAME`, `USER`, `UID`                            | 사용자 이름                                                                                            | `UID=SYS`                                        | `SYS`   |
| `PASSWORD`, `PWD`                                              | 비밀번호                                                                                               | `PWD=manager`                                    | 없음    |
| `CONNECT_TIMEOUT`, `ConnectionTimeout`, `connectTimeout`       | 커넥션 타임아웃(밀리초)                                                                                | `CONNECT_TIMEOUT=10000`                          | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout`, `commandTimeout`          | 명령별 타임아웃(밀리초)                                                                               | `COMMAND_TIMEOUT=50000`                          | `60000` |
| `PROTOCOL`, `ProtocolVersion`, `MachProtocol`                  | 선호하는 와이어 프로토콜 (`2.1`, `3.0`, `4.0`, `4.0-full`, `auto`, `auto-full` 등). 입력하지 않으면 `4.0`을 사용합니다. | `PROTOCOL=auto`                                  | `4.0`   |

예시:

```csharp
var connectionString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;COMMAND_TIMEOUT=50000;PROTOCOL=4.0-full",
    host,
    port);
```

### 프로토콜 자동 감지 (`PROTOCOL=auto`)

서버 버전이 혼재된 환경이라면 `PROTOCOL=auto`를 지정해 UniMachNetConnector가 실행 시 적절한 레거시 프로토콜을 협상하도록 설정할 수 있습니다. 동작 방식은 다음과 같습니다.

- `PROTOCOL=auto`는 4.0 → 3.0 → 2.2 → 2.1 순서로 핸드셰이크를 시도하며, 커넥션 문자열에 전달한 호스트·포트·사용자·비밀번호·데이터베이스·`CONNECT_TIMEOUT` 값을 그대로 사용합니다.
- `PROTOCOL=auto-full`은 위와 같지만 서버가 4.0을 리턴하면 먼저 `4.0-full` 디스크립터를 시도하고, 필요시 제한 버전(4.0)으로 폴백합니다.
- `SERVER=hostA:5700,hostB:6000`처럼 여러 호스트를 지정하면 순차적으로 시도하며, 실패 메시지에는 각 호스트/프로토콜 조합이 기록되어 문제 지점을 파악할 수 있습니다.
- 자격 증명은 기존 레거시 드라이버와 동일하게 대문자로 변환됩니다. 기본 데이터베이스(`data`)를 사용하지 않는다면 `DATABASE=` 값을 명시하세요.
- `CONNECT_TIMEOUT` 값이 각 감지 라운드 트립에 적용됩니다. 예외 메시지에 `Protocol probe received an invalid response`가 보이면 포트·방화벽·TLS 설정을 다시 확인하십시오.

이미 서버 버전을 알고 있다면 `PROTOCOL=2.1`, `3.0`, `4.0`, `4.0-full`처럼 명시적으로 지정해 자동 감지를 건너뛸 수도 있습니다.

## API 레퍼런스 {#api-reference}

{{< callout type="warning" >}}
아래에 명시되지 않은 기능은 아직 구현되지 않았거나 정상적으로 동작하지 않을 수 있습니다.<br>
존재하지 않는 메서드나 필드를 호출하면 `NotImplementedException` 또는 `NotSupportedException`이 발생합니다.
{{< /callout >}}

### MachConnection

```cs
public sealed class MachConnection : DbConnection
```

Machbase와의 연결을 담당하는 클래스입니다. `DbConnection`과 동일하게 `IDisposable`을 구현하므로 `Dispose()` 호출이나 `using` 문으로 안전하게 해제할 수 있습니다.

#### 생성자

```
MachConnection(string aConnectionString)
```

커넥션 문자열을 입력 받아 `MachConnection` 인스턴스를 생성합니다.

#### Open

```cs
void Open()
```

커넥션 문자열을 사용해 실제 연결을 수립합니다.

#### Close

```cs
void Close()
```

열려 있는 연결을 종료합니다.

#### SetConnectAppendFlush

```cs
void SetConnectAppendFlush(bool activeFlush)
```

Append 작업 중 자동으로 flush를 수행할지 여부를 설정합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `State` | `System.Data.ConnectionState` 값을 나타냅니다. |
| `StatusString` | 현재 연결이 의존하는 `MachCommand`의 상태 문자열입니다. 내부 로깅용이므로 쿼리 상태 판단 용도로 사용하지 않는 것이 좋습니다. |

### MachCommand

```cs
public sealed class MachCommand : DbCommand
```

`MachConnection`을 통해 SQL 명령이나 Append 작업을 실행하는 클래스입니다. `DbCommand`와 마찬가지로 `IDisposable`을 구현합니다.

#### 생성자

```cs
MachCommand(string aQueryString, MachConnection aConn)
```

실행할 쿼리와 연결 객체를 지정해 인스턴스를 생성합니다.

```cs
MachCommand(MachConnection aConn)
```

쿼리가 필요 없는 Append 전용 커맨드를 생성합니다.

#### CreateParameter

```cs
MachParameter CreateParameter()
```

새로운 `MachParameter`를 생성합니다.

#### AppendOpen

```cs
MachAppendWriter AppendOpen(
    string aTableName,
    int aErrorCheckCount = 0,
    MachAppendOption option = MachAppendOption.None)
```

Append 세션을 열고 `MachAppendWriter`를 반환합니다.

* `aTableName`: 대상 테이블 이름
* `aErrorCheckCount`: 지정한 레코드 수마다 서버에 전송해 실패 여부를 확인합니다. 즉, 자동 `APPEND-FLUSH` 지점을 설정합니다.
* `option`: `None` 또는 `MicroSecTruncated` 옵션을 지정할 수 있습니다.

#### AppendData

```cs
void AppendData(MachAppendWriter writer, List<object> dataList)
```

리스트에 있는 값을 순서대로 Append 버퍼에 적재합니다. 각 값의 타입은 테이블 컬럼 타입과 일치해야 하며, 값이 부족하거나 초과하면 예외가 발생합니다.

> **참고**: `_arrival_time`을 `ulong`으로 직접 지정할 때는 Machbase가 기대하는 1970-01-01 UTC 기준 나노초 값을 입력해야 합니다.

```cs
void AppendDataWithTime(
    MachAppendWriter writer,
    List<object> dataList,
    DateTime arrivalTime)
```

`_arrival_time`을 `DateTime`으로 명시적으로 지정합니다.

```cs
void AppendDataWithTime(
    MachAppendWriter writer,
    List<object> dataList,
    ulong arrivalTime)
```

`_arrival_time`을 나노초 단위 `ulong`으로 지정합니다.

#### AppendFlush

```cs
void AppendFlush(MachAppendWriter writer)
```

버퍼에 쌓인 데이터를 즉시 서버로 전송합니다. 호출 주기가 짧을수록 장애 시 데이터 유실이 줄어들지만 처리량은 낮아집니다.

#### AppendClose

```cs
void AppendClose(MachAppendWriter writer)
```

Append 세션을 종료합니다. 내부적으로 `AppendFlush()` 호출 후 프로토콜을 마무리합니다.

#### ExecuteNonQuery

```cs
int ExecuteNonQuery()
```

쿼리를 실행하고 영향을 받은 레코드 수를 반환합니다. 주로 `INSERT`, `UPDATE`, `DELETE`, DDL에서 사용합니다.

#### ExecuteScalar

```cs
object ExecuteScalar()
```

쿼리를 실행하고 첫 번째 컬럼 값을 반환합니다.

#### ExecuteDbDataReader

```cs
DbDataReader ExecuteDbDataReader(CommandBehavior behavior)
```

쿼리를 실행하고 결과를 순차적으로 읽을 수 있는 `DbDataReader`를 반환합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `Connection` / `DbConnection` | 현재 연결된 `MachConnection`입니다. |
| `ParameterCollection` / `DbParameterCollection` | 바인딩에 사용할 파라미터 컬렉션입니다. |
| `CommandText` | 실행할 SQL 문자열입니다. |
| `CommandTimeout` | 서버 응답을 기다리는 최대 시간(밀리초)입니다. 값은 `MachConnection` 설정을 따르며 여기서는 조회만 가능합니다. |
| `FetchSize` | 서버에서 한 번에 가져올 레코드 수입니다. 기본값은 3000입니다. |
| `IsAppendOpened` | Append 세션이 열려 있는지 여부입니다. |

### MachDataReader

```cs
public sealed class MachDataReader : DbDataReader
```

Fetch된 결과를 순차적으로 읽는 리더입니다. `MachCommand.ExecuteDbDataReader()`로 획득한 객체만 사용할 수 있습니다.

#### GetName

```cs
string GetName(int ordinal)
```

지정한 인덱스의 컬럼 이름을 반환합니다.

#### GetDataTypeName

```cs
string GetDataTypeName(int ordinal)
```

Machbase 컬럼 타입 이름을 반환합니다.

#### GetFieldType

```cs
Type GetFieldType(int ordinal)
```

.NET 측 매핑 타입을 반환합니다.

#### GetOrdinal

```cs
int GetOrdinal(string name)
```

컬럼 이름에 해당하는 인덱스를 반환합니다.

#### GetValue

```cs
object GetValue(int ordinal)
```

현재 레코드의 값을 `object`로 반환합니다.

#### IsDBNull

```cs
bool IsDBNull(int ordinal)
```

해당 컬럼 값이 `NULL`인지 확인합니다.

#### GetValues

```cs
int GetValues(object[] values)
```

현재 레코드의 값을 배열에 채워 넣고 채워진 항목 수를 반환합니다.

#### Get*XXXX*

```cs
bool GetBoolean(int ordinal)
byte GetByte(int ordinal)
char GetChar(int ordinal)
short GetInt16(int ordinal)
int GetInt32(int ordinal)
long GetInt64(int ordinal)
DateTime GetDateTime(int ordinal)
string GetString(int ordinal)
decimal GetDecimal(int ordinal)
double GetDouble(int ordinal)
float GetFloat(int ordinal)
```

컬럼 값을 지정한 타입으로 반환합니다.

#### Read

```cs
bool Read()
```

다음 레코드를 읽습니다. 결과가 더 이상 없으면 `false`를 반환합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `FetchSize` | 서버에서 한 번에 가져올 레코드 수입니다. 기본값은 3000이며 여기에서는 수정할 수 없습니다. |
| `FieldCount` | 결과 컬럼 수입니다. |
| `this[int ordinal]` | `GetValue(int ordinal)`과 동일합니다. |
| `this[string name]` | `GetValue(GetOrdinal(name))`과 동일합니다. |
| `HasRows` | 결과가 존재하는지 여부입니다. |
| `RecordsAffected` | Fetch된 레코드 수를 나타냅니다. |

### MachParameterCollection

```cs
public sealed class MachParameterCollection :
    DbParameterCollection,
    IEnumerable<MachParameter>
```

`MachCommand`에 바인딩할 파라미터 집합을 관리하는 클래스입니다.

파라미터를 설정한 뒤 실행하면 해당 값이 함께 전송됩니다.

> 현재 버전에는 Prepared Statement 의미에서의 실행 계획 캐시가 구현되어 있지 않으므로, 동일한 쿼리를 반복 실행하더라도 성능은 첫 실행과 동일합니다.

#### Add

```cs
MachParameter Add(string parameterName, DbType dbType)
```

파라미터 이름과 타입을 지정해 `MachParameter`를 추가하고, 생성된 객체를 반환합니다.

```cs
int Add(object value)
```

값을 추가하고 추가된 인덱스를 반환합니다.

```cs
void AddRange(Array values)
```

단순 값 배열을 한 번에 추가합니다.

```cs
MachParameter AddWithValue(string parameterName, object value)
```

파라미터 이름과 값을 동시에 추가하고, 생성된 `MachParameter`를 반환합니다.

#### Contains

```cs
bool Contains(object value)
```

해당 값이 이미 추가되어 있는지 확인합니다.

```cs
bool Contains(string parameterName)
```

지정한 파라미터 이름이 존재하는지 확인합니다.

#### Clear

```cs
void Clear()
```

모든 파라미터를 제거합니다.

#### IndexOf

```cs
int IndexOf(object value)
```

해당 값이 있는 인덱스를 반환합니다.

```cs
int IndexOf(string parameterName)
```

파라미터 이름이 위치한 인덱스를 반환합니다.

#### Insert

```cs
void Insert(int index, object value)
```

지정한 위치에 값을 삽입합니다.

#### Remove

```cs
void Remove(object value)
```

해당 값을 포함한 파라미터를 제거합니다.

```cs
void RemoveAt(int index)
```

인덱스에 위치한 파라미터를 제거합니다.

```cs
void RemoveAt(string parameterName)
```

지정한 이름의 파라미터를 제거합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `Count` | 파라미터 개수입니다. |
| `this[int index]` | 해당 인덱스의 `MachParameter`입니다. |
| `this[string name]` | 이름과 일치하는 `MachParameter`입니다. |

### MachParameter

```cs
public sealed class MachParameter : DbParameter
```

개별 파라미터의 바인딩 정보를 저장하는 클래스입니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `ParameterName` | 파라미터 이름입니다. |
| `Value` | 전송할 값입니다. |
| `Size` | 값의 길이입니다. |
| `Direction` | `ParameterDirection` 값입니다. 기본값은 `Input`입니다. |
| `DbType` | .NET 측 DB 타입입니다. |
| `MachDbType` | Machbase 고유 타입입니다. |
| `IsNullable` | `NULL` 허용 여부입니다. |
| `HasSetDbType` | `DbType`이 설정되었는지 여부입니다. |

### MachException

```cs
public class MachException : DbException
```

Machbase에서 발생한 오류를 표현하는 예외 클래스입니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `MachErrorCode` | Machbase가 반환한 오류 코드입니다. |

### MachAppendWriter

```cs
public sealed class MachAppendWriter
```

Append 프로토콜을 다루기 위한 보조 클래스입니다. `MachCommand.AppendOpen()` 호출 시 인스턴스를 획득합니다.

#### SetErrorDelegator

```cs
void SetErrorDelegator(ErrorDelegateFuncType callback)

void ErrorDelegateFuncType(MachAppendException e);
```

Append 중 오류가 발생했을 때 호출할 델리게이트를 등록합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `SuccessCount` | 성공적으로 저장된 레코드 수입니다. `AppendClose()` 이후에 확인할 수 있습니다. |
| `FailureCount` | 실패한 레코드 수입니다. `AppendClose()` 이후에 설정됩니다. |
| `Option` | `AppendOpen()` 호출 시 사용한 `MachAppendOption` 값입니다. |

### MachAppendException

```cs
public sealed class MachAppendException : MachException
```

Append 과정에서 발생한 오류 정보를 추가로 제공하는 예외입니다. 서버가 반환한 오류 메시지를 그대로 전달하며, 실패한 레코드를 문자열로 확인할 수 있습니다.

#### GetRowBuffer

```cs
string GetRowBuffer()
```

오류가 발생한 원본 레코드를 문자열 형태로 반환합니다.

## 사용 예시 {#usage-and-examples}

### 연결

`MachConnection`을 생성해 `Open()`/`Close()`로 연결을 제어할 수 있습니다.

```csharp
var connString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;",
    SERVER_HOST,
    SERVER_PORT);

var connection = new MachConnection(connString);
connection.Open();
// ... 작업 ...
connection.Close();
```

`using` 문을 사용하면 `Close()`를 직접 호출하지 않아도 자원이 정리됩니다.

```csharp
var connString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;",
    SERVER_HOST,
    SERVER_PORT);

using (var connection = new MachConnection(connString))
{
    connection.Open();
    // ... 작업 ...
}
```

### 쿼리 실행

`MachCommand`로 SQL 구문을 실행할 수 있습니다.

```csharp
var connString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;",
    SERVER_HOST,
    SERVER_PORT);

using (var connection = new MachConnection(connString))
{
    connection.Open();

    const string sql = "CREATE TABLE tab1 ( col1 INTEGER, col2 VARCHAR(20) )";
    using var command = new MachCommand(sql, connection);
    command.ExecuteNonQuery();
}
```

### SELECT 실행

`MachCommand.ExecuteReader()`를 사용하면 `MachDataReader`로 결과를 순차적으로 읽을 수 있습니다.

```csharp
var connString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;",
    SERVER_HOST,
    SERVER_PORT);

using (var connection = new MachConnection(connString))
{
    connection.Open();

    using var command = new MachCommand("SELECT * FROM tab1", connection);
    using var reader = command.ExecuteReader();

    while (reader.Read())
    {
        for (var i = 0; i < reader.FieldCount; i++)
        {
            Console.WriteLine($"{reader.GetName(i)} : {reader.GetValue(i)}");
        }
    }
}
```

### 파라미터 바인딩

`MachParameterCollection`을 이용하면 시계열 조회 조건 등을 파라미터로 안전하게 전달할 수 있습니다.

```csharp
using var connection = new MachConnection(connString);
connection.Open();

const string sql = @"
    SELECT *
      FROM tab2
     WHERE CreatedDateTime < @CurrentTime
       AND CreatedDateTime >= @PastTime";

using var command = new MachCommand(sql, connection);

var now = DateTime.UtcNow;
var past = now.AddMinutes(-1);

command.ParameterCollection.Add(
    new MachParameter { ParameterName = "@CurrentTime", Value = now });
command.ParameterCollection.Add(
    new MachParameter { ParameterName = "@PastTime", Value = past });

using var reader = command.ExecuteReader();
while (reader.Read())
{
    Console.WriteLine($"{reader.GetName(0)} : {reader.GetValue(0)}");
}
```

### Append

Append 프로토콜을 사용하면 대량의 시계열 데이터를 빠르게 적재할 수 있습니다.

```csharp
using var connection = new MachConnection(connString);
connection.Open();

using var appendCommand = new MachCommand(connection);
var writer = appendCommand.AppendOpen("tab2");

var row = new List<object>();
for (var i = 1; i <= 100000; i++)
{
    row.Add(i);
    row.Add($"NAME_{i % 100}");

    appendCommand.AppendData(writer, row);
    row.Clear();

    if (i % 1000 == 0)
    {
        appendCommand.AppendFlush(writer);
    }
}

appendCommand.AppendClose(writer);
Console.WriteLine($"Success Count : {writer.SuccessCount}");
Console.WriteLine($"Failure Count : {writer.FailureCount}");
```

### Error Delegator 설정

Append 중 서버에서 오류가 발생하면 지정한 델리게이트가 호출됩니다.

```csharp
void AppendErrorDelegator(MachAppendException e)
{
    Console.WriteLine("====================");
    Console.WriteLine("Append error");
    Console.WriteLine(e.Message);
    Console.WriteLine(e.GetRowBuffer());
    Console.WriteLine("====================");
}

// 등록
writer.SetErrorDelegator(AppendErrorDelegator);
```

### 자동 AppendFlush 설정

`MachConnection.SetConnectAppendFlush(true)`로 설정하면 Append 중 일정 주기로 자동 flush가 실행됩니다.

```csharp
var connection = new MachConnection(connString);
connection.Open();
connection.SetConnectAppendFlush(true);
```

`false`로 설정하면 자동 flush가 비활성화됩니다.

## 프로토콜 4.0-full 전체 API {#full-provider-apis-protocol-40-full}

`PROTOCOL=4.0-full`을 사용하면 확장된 ADO.NET 표면을 사용할 수 있습니다. 8.0.54 소스
패키지에서 4.0 limited connector는 3.1.2, 4.0-full connector는 3.2.1입니다.
설치된 Linux 패키지는 `$MACHBASE_HOME/lib/` 아래에 net50 flavor만 포함할 수 있으므로,
다른 target framework가 필요하면 소스 빌드 또는 NuGet restore 산출물을 사용하십시오.

- `UniMachNetConnector-net50-8.0.54.dll` – DBMS Standard Linux 패키지에서 흔히 설치되는 universal entry point
- `machNetConnector-40-net50-3.1.2.dll` – protocol 4.0 limited connector
- `machNetConnector-40-net50-3.2.1.dll` – protocol 4.0-full connector

### 4.0-full에서 추가된 주요 타입

- `MachDbProviderFactory`: `Mach.Data` invariant 이름으로 프로바이더를 등록/생성할 수 있습니다.
- `MachConnectionStringBuilder`: 키워드 오타 없이 커넥션 문자열을 구성할 수 있습니다.
- `MachDataAdapter`, `MachRowUpdating`, `MachRowUpdated`: `DataTable`/`DataSet` 기반 워크플로를 지원합니다.
- `MachCommandBuilder`: SELECT 문으로부터 INSERT/DELETE(조건에 따라 UPDATE) 구문을 자동 생성합니다. 로그·태그 테이블은 UPDATE를 허용하지 않는다는 점에 유의하십시오.

### 전체 API 활성화

```csharp
var connString =
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
```

UPDATE/DELETE가 필요한 경우에는 Lookup/Volatile 테이블을 사용하고, 로그·태그 테이블은 Append 전용으로 유지하십시오.

### 커넥션 문자열 빌더 사용

```csharp
var builder = new MachConnectionStringBuilder
{
    Server = "127.0.0.1",
    Port = 5656,
    UserID = "SYS",
    Password = "MANAGER"
};

builder["PROTOCOL"] = "4.0-full";

using var connection = new MachConnection(builder.ConnectionString);
connection.Open();
```

### 예시: MachDataAdapter로 append

Lookup 테이블을 `DataTable`로 가져온 뒤 새 레코드를 추가하고 `MachDataAdapter`로 다시 반영할 수 있습니다.

```csharp
using Mach.Data.MachClient;
using System.Data;

var connString =
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

var adapter = new MachDataAdapter(
    "SELECT id, name FROM dotnet_lookup_demo ORDER BY id",
    connection);
var builder = new MachCommandBuilder(adapter);

var table = new DataTable();
adapter.Fill(table);

var newRow = table.NewRow();
newRow["id"] = 2001;
newRow["name"] = "Inserted from MachDataAdapter";
table.Rows.Add(newRow);

adapter.Update(table);
```

> **Tip**: 전송 전 SQL을 확인하려면 `MachDataAdapter.MachRowUpdating` / `MachRowUpdated` 이벤트를 구독하십시오.

```csharp
adapter.MachRowUpdating += (sender, args) =>
{
    Console.WriteLine(
        $"About to run {args.StatementType} with SQL: {args.Command?.CommandText}");
};
```

### 예시: DbProviderFactory 활용

`MachDbProviderFactory.Instance`를 사용하면 `DbProviderFactories`, Dapper 등 프로바이더 중립 구성에 Machbase를 연결할 수 있습니다.

```csharp
using System.Data.Common;
using Mach.Data.MachClient;

DbProviderFactory factory = MachDbProviderFactory.Instance;

using DbConnection connection = factory.CreateConnection()!;
connection.ConnectionString =
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
connection.Open();

using DbCommand command = connection.CreateCommand();
command.CommandText = "SELECT COUNT(*) FROM dotnet_lookup_demo";
var count = (long)command.ExecuteScalar();

Console.WriteLine($"Lookup rows: {count}");
```

설정 기반 애플리케이션에서 팩터리를 자동으로 노출하려면 시작 시 `MachDbProviderFactory.Register()`를 한 번 호출해 `DbProviderFactories.GetFactory("Mach.Data")`가 동일한 인스턴스를 반환하도록 구성하십시오.

`4.0-full` 프로토콜은 Machbase 7.x 이상 서버에서만 사용 가능합니다. 더 낮은 버전에서는 `PROTOCOL=4.0`(제한된 기능) 또는 2.x/3.x 프로토콜을 사용해야 합니다.

## cli-odbc


CLI란 [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)/[IEC](https://en.wikipedia.org/wiki/International_Electrotechnical_Commission) 9075-3:2003에 정의된 소프트웨어 개발 표준입니다.

CLI는 데이터베이스에 어떻게 SQL을 전달하고, 결과 값을 어떻게 받고 분석해야 하는지에 대한 함수 및 명세를 정의하고 있습니다. 이 CLI는 1990년 초창기에 개발되었고, C 와 COBOL 언어 만을 위해 개발되었고, 현재까지 그 스펙이 유지되고 있습니다.

현재까지 가장 널리 알려진 표준 인터페이스는 ODBC(Open Database Connectivity)로서 클라이언트 프로그램이 데이터베이스의 종류와 무관하게 데이터베이스 접속할 수 있는 방법을 제시해 주고 있습니다. 현재 최신 ODBC API 버전은 3.52 로서 ISO와 X/Open 표준에 정의되어 있습니다.


## 표준 CLI 함수
표준 함수의 사용법에 대해서는 다음과 같은 링크를 참조합니다.

* [위키피디아](https://en.wikipedia.org/wiki/Call_Level_Interface)
* [오픈그룹 문서](https://www2.opengroup.org/ogsys/catalog/c451)

다음의 함수를 참고하면 됩니다.

| | | | |
|--|--|--|--|
| SQLAllocConnect   | SQLDisconnect     | SQLGetDescField  | SQLPrepare        |
| SQLAllocEnv       | SQLDriverConnect  | SQLGetDescRec    | SQLPrimaryKeys    |
| SQLAllocHandle    | SQLExecDirect     | SQLGetDiagRec    | SQLStatistics     |
| SQLAllocStmt      | SQLExecute        | SQLGetEnvAttr    | SQLRowCount       |
| SQLBindCol        | SQLFetch          | SQLGetFunctions  | SQLSetConnectAttr |
| SQLBindParameter+ | SQLFreeConnect    | SQLGetInfo       | SQLSetDescField   |
| SQLColAttribute   | SQLFreeEnv        | SQLGetStmtAttr   | SQLSetDescRec     |
| SQLColumns        | SQLFreeHandle     | SQLGetTypeInfo   | SQLSetEnvAttr     |
| SQLConnect        | SQLFreeStmt       | SQLNativeSQL     | SQLSetStmtAttr    |
| SQLCopyDesc       | SQLGetConnectAttr | SQLNumParams     | SQLStatistics     |
| SQLDescribeCol    | SQLGetData        | SQLNumResultCols | SQLTables         |

## 접속을 위한 연결 스트링
CLI를 통해 접속을 하기 위해서는 연결 스트링을 만들어야 하며, 각각의 내용은 다음과 같습니다.

| 연결 스트링 항목명  | 항목 설명 |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|         DSN         | 데이터 소스 명을 지정합니다.<br> ODBC에서는 리소스가 담긴 파일의 섹션 명을 기술하고, CLI에서는 서버명 혹은 IP 주소를 지정합니다.  |
|        DBNAME       | Machbase의 DB명을 기술합니다.  |
|        SERVER       | Machbase가 위치하는 서버의 호스트 명 혹은 IP 주소를 가리킵니다.  |
|       NLS_USE       | 서로 사용할 언어 종류를 설정합니다.(현재 사용되지 않으며, 차후 확장을 위해 유지합니다.)  |
|         UID         | 사용자 아이디  |
|         PWD         | 사용자 패스워드  |
|       PORT_NO       | 접속할 포트 번호  |
|       PORT_DIR      | 유닉스에서 Unix domain으로 접속할 경우 사용되는 파일 경로를 지정합니다.<br> (서버에서 수정했을 경우에 지정하며, 디폴트로는 지정하지 않아도 동작합니다.)  |
|       CONNTYPE      | 클라이언트와 서버의 접속 방법을 지정합니다.<br> 1: TCP/IP INET 으로 접속<br> 2: Unix Domain 으로 접속  |
|       COMPRESS      | Append 프로토콜을 압축할 것인지 나타냅니다.<br> 이 값이 0일 경우에는 압축하지 않고 전송합니다.<br> 이 값이 0보다 큰 임의의 값일 경우에는 그 값보다 Append 레코드가 클 경우에만 압축합니다.<br> 예) COMPRESS=512<br> 레코드 사이즈가 512보다 클 경우에만 압축하여 동작합니다.<br> 원격 접속일 경우 압축하면 전송 성능이 향상됩니다.  |
|   SHOW_HIDDEN_COLS  | 숨겨진 컬럼(_arrival_time)을 select * 로 수행시 보여줄 것인지 결정합니다.<br> 0일 경우에는 보이지 않으며, 1일 경우에 해당 컬럼의 정보가 출력됩니다.  |
|  CONNECTION_TIMEOUT | 최초 연결시에 얼마나 대기할 것이지 설정합니다.<br> 디폴트로는 30초가 설정되어 있습니다.<br> 만일 최초 연결시 서버의 응답이 30초 보다 더 느려지는 경우를 고려하면, 이 값을 더 크게 설정해야 합니다.<br> CONNECTION_TIMEOUT에서 0 값은 Timeout에 제한이 없음을 의미하며 연결이 실패할 때에도 무한정으로 대기하므로 되도록이면 사용하지 않는 편이 좋습니다.  |
|    SOCKET_TIMEOUT   | Protocol I/O에 시간이 걸리면 발생하는 timeout입니다.<br> Client에서 검사하여 대기 후 Disconnect를 수행합니다.<br> ORACLE의 Read Timeout과 같습니다. (MYSQL, MSSQL에서는 동일하게 SOCKET_TIMEOUT이라는 이름으로 사용합니다.)<br> Connection String에서 SOCKET_TIMEOUT=NN(초)로 설정하며 기본값은 30분(1800)으로 설정됩니다.  |
| ALTERNATIVE_SERVERS | cluster 버전을 사용 시, 여러 대의 브로커의 정보를 추가적으로 가지게 되는 설정입니다.<br> 다중의 브로커를 등록해두었을 시, 접속되어있던 브로커가 혹시 내려가게 된 경우에도 다른 브로커에 접속한 뒤, 입력하던 데이터를 계속해서 입력하게 됩니다.<br> 여러개의 브로커를 등록할 수 있으며, <서버 주소>:<서버 포트>의 값을 ',' 단위로 이어서 작성합니다.<br>  ex) ALTERNATIVE_SERVERS=192.168.0.10:20320,192.168.0.11:20320; |
|      AUTH_MODE      | 인증 방식입니다. 비밀번호 인증은 `PASSWORD`, 개인키 challenge 인증은 `CHALLENGE`를 사용합니다. `AUTH_KEY_FILE`만 지정하고 `AUTH_MODE`를 생략하면 CLI는 `CHALLENGE`로 처리합니다. |
|   AUTH_SIG_SCHEME   | `AUTH_MODE=CHALLENGE`에서 사용할 서명 스킴입니다. `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`를 지정할 수 있습니다. 생략하면 키 파일에서 기본 스킴을 추론합니다. |
|    AUTH_KEY_FILE    | `AUTH_MODE=CHALLENGE`에서 사용할 로컬 PEM 개인키 파일 경로입니다. challenge 인증에는 필수입니다. |

CLI 접속 예제는 다음과 같습니다.

```cpp
sprintf(connStr,"SERVER=127.0.0.1;COMPRESS=512;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

if (SQL_ERROR == SQLDriverConnect( gCon, NULL, (SQLCHAR *)connStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT )) {
   ...
}
```

## 확장 CLI 함수 (APPEND)
CLI 확장 함수는 Machbase 서버에 데이터를 초고속으로 입력하기 위해 제공되는 Append 프로토콜을 구현하기 위한 함수입니다.

이 함수는 크게 4가지의 함수로 구성되어 있는데, 채널의 오픈, 채널에 대한 데이터 입력, 채널의 플러쉬, 채널 클로징입니다.

### Append 프로토콜의 이해
Machbase에서 제공하는 Append 프로토콜은 비동기 방식으로 동작합니다. 비동기라 함은 클라이언트가 서버에게 요청한 특정 작업에 대한 응답이 서로 완전히 동기화되지 않고, 임의의 이벤트가 발생하는 순간에 발생하는 것을 의미합니다. 즉, 클라이언트가 Append를 수행했다고 하더라도, 그 수행에 대한 결과를 바로 얻거나 확인할 수 없으며, 서버에서 준비가 되는 임의의 시점에 그것을 확인할 수 있다는 것입니다. 이런 이유로 Append 프로토콜을 활용해서 응용 프로그램을 개발하는 개발자는 다음과 같은 내부 동작에 대한 이해를 가져야 합니다. 이후의 설명은 클라이언트가 언제 어떻게 서버에서 발생하는 비동기 에러를 검출하고 사용자에게 되돌여주는지에 대한 것입니다.

### Append 데이터의 전송
SQLExecute 혹은 SQLExecDirect()와 같은 일반적인 호출에서 Machbase는 즉시 그 결과를 클라이언트에게 되돌려주는 동기화 방식을 사용합니다. 그러나, SQLAppendDataV2()는 사용자 데이터가 입력된 이후 즉시 요청을 보내지 않습니다. 대신, 클라이언트 통신 버퍼가 모두 찰 때 까지 대기하고 있다가 모두 차면 그 이후에 한꺼번에 데이터를 클라이언트로 전송하게 됩니다. 이렇게 설계된 이유는 Append를 사용하는 클라이언트의 입력 데이터가 초당 수만에서 수십만 레코드를 가정하였기 때문에 고속의 데이터 전송을 위한 버퍼링 방식을 활용한 것입니다. 이런 이유로 만일 사용자가 임의로 해당 버퍼의 내용을 전송하고자 할 경우에는 SQLAppendFlush() 함수를 호출하여, 명시적으로 데이터를 입력할 수 있습니다.

### Append 데이터의 에러 확인
앞에서 언급한 바와 같이 Append 프로토콜은 버퍼링되어 비동기로 동작합니다. 특히, 서버에서 에러가 발생하지 않았을 경우에는 아무런 응답을 받지 않고, 에러가 발생했을 경우에만 에러를 검출하는 방식을 취하기 때문에 에러가 언제 어떻게 검출되는지 이해하는 것이 매우 중요합니다. 또한, 에러를 검출하는 비용이 상대적으로 매우 크기 때문에 레코드 입력시마다 매번 검사하는 것이 매우 비효율적으로 판단되어, 현재 Machbase에서는 명시적으로 다음과 같은 경우에만 에러를 검출하도록 되어 있습니다. 에러가 검출될 경우에는 사용자가 설정한 에러 콜백 함수를 매번 호출하게 됩니다.

1. 전송 버퍼가 모두 차고, 서버에게 명시적으로 데이터를 전송한 이후 검사
2. SQLAppendFlush() 내부에서 서버에게 명시적으로 데이터를 전송한 이후 검사
3. SQLAppendClose() 내부에서 종료 직전에 검사

즉, 기본적으로 위의 3가지 경우에만 에러를 검출하도록 되어 있어, I/O의 발생을 최소화하도록 설계되었습니다.

### 서버 에러 검사를 위한 부가 옵션
성능을 최대한으로 달성하기 위해 기본적으로 설정된 에러 검출 기법은 사용자가 원하는 경우 좀 더 빈번하게 검사하고, 이를 활용할 수 있습니다. 즉, SQLAppendOpen() 함수의 마지막 인자인 aErrorCheckCount를 조절함으로서 가능합니다. 이 값이 0일 경우에는 별도의 확인 동작을 하지 않고, 기본으로 동작합니다. 그러나, 만일 이 값이 0보다 클 경우에는 SQLAppendData()의 호출 횟수마다 명시적으로 에러를 검사하도록 되어 있습니다. 다시 말해 이 값이 10일 경우에는 10번의 Append 동작마다 에러를 검사하는 비용을 지불합니다. 따라서, 이 값이 작을 경우에는 에러 검출을 위한 시스템 리소스를 많이 사용하기 때문에 적절한 숫자로 조절하여 사용해야 합니다.

### 서버 에러 발생시 Trace 로그 남기기
만일 에러가 발생한 Append 데이터에 대해서 별도로 Trace 로그를 남기고자 할 경우에는 서버에 준비된 프로퍼티 DUMP_APPEND_ERROR 를 1로 설정합니다. 이렇게 설정하면, mach.trc 파일에 해당 에러를 발생시킨 레코드에 대한 명세가 파일로 기록됩니다. 단, 에러의 횟수가 과도할 경우 시스템 리소스의 사용량이 급격히 늘어나, Machbase의 전체 성능을 떨어뜨릴 수 있으므로 주의하여 사용해야 합니다.

### APPEND 함수 설명
#### SQLAppendOpen
```cpp
SQLRETURN SQLAppendOpen(SQLHSTMT   aStatementHandle,
                        SQLCHAR   *aTableName,
                        SQLINTEGER aErrorCheckCount );
```
이 함수는 대상 테이블에 대한 채널을 오픈합니다. 이후 이 채널을 닫아 주지 않으면 지속적으로 열린 상태가 유지됩니다.

하나의 연결에 대해 최대 1024개의 Statement 설정이 가능합니다. 각 Statement마다 SQLAppendOpen을 사용하면 됩니다.

1. aStatementHandle : Append를 수행할 Statement의 핸들을 나타냅니다.
2. aTableName : Append를 수행할 대상 테이블의 이름을 나타냅니다.
3. aErrorCheckCount : 몇 건의 데이터가 입력될 때 마다 서버의 에러를 검사할 것인지 결정합니다. 이 값이 0일 경우에는 임의로 에러를 검사하지 않습니다.

#### SQLAppendData (deprecated)
```cpp
SQLRETURN  SQLAppendData(SQLHSTMT StatementHandle, void *aData[]);
```
이 함수는 해당 채널에 대해 데이터를 입력하는 함수입니다.

* aData는 입력될 데이터의 포인터를 담고 있는 배열입니다. 배열의 개수는 Open시에 지정한 테이블이 보유하고 있는 컬럼의 개수와 일치해야 합니다.
* 리턴값은 SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, SQL_ERROR가 가능합니다. 특히, SQL_SUCCESS_WITH_INFO가 반환되었을 경우에는 입력된 특정 컬럼의 길이가 길어 잘리는 등의 오류가 있을 수 있으므로 결과를 다시 확인하여야 합니다.

**데이터 타입에 따른 설정**

숫자형 및 문자형
* float, double, short, int, long long, char * 과 같은 타입은 해당 값에 대한 포인터 설정 만으로 잘 동작합니다.

주소형
* ipv4 의 경우에는 5 바이트 무부호 문자(unsigned char)의 배열로 넘깁니다.
* 첫 번째 바이트는 4로 설정하고, 이후의 4바이트는 연속되는 주소값으로 설정합니다.
* 예를 들어, 127.0.0.1의 경우에는 5바이트 배열 0x04, 0x7f, 0x00, 0x00, 0x01 의 순으로 들어가게 됩니다.

```cpp
// 4개의 컬럼 정보를 가지는 테이블의 경우 (short(16), int(32), long(64), varchar)

testAppendIPFunc()
{
   short val1 = 0;
   int   val2 = 1;
   long long  val3 = 2;
   char *val4 = "my string";
   void *valueArray[4];

   valueArray[0] = (void *)&val1;
   valueArray[1] = (void *)&val2;
   valueArray[2] = (void *)&val3;
   valueArray[3] = (void *)val4;

   SQLAppendData(aStmt, valueArray);
}
```

**데이터 타입에 따른 설정**

datetime 형

* Machbase 는 내부적으로 나노 단위 시간 해상도 값을 가지기 때문에 클라이언트에서 시간을 설정할 때는 변환과정을 거쳐야 하며, 64비트 부호없는 정수형 값으로 표현됩니다. 따라서 적절한 변환을 위해서는 유닉스 라이브러리인 mktime을 이용하여 초로 변환한 이후에 나노 값을 더해주어야 합니다.
* ※ Machbase의 시간 = (1970년 1월 1일 이후로부터의 총 시간 (초)) * 1,000,000,000 + mili-second * 1,000,000 + micro-second * 1000 + nano-second;

```cpp
// Date String이 "연도-월-일 시:분:초 밀리:마이크로:나노" 형태로 입력될 경우 코드

testAppendDateStrFunc(char *aDateString)
{
    int yy, int mm, int dd, int hh, int mi, int ss;
    unsigned long t1;
    void *valueArray[5];
    sscanf(aDateString, "%d-%d-%d %d:%d:%d %d:%d:%d",
        &yy, &mm, &dd, &hh, &mi, &ss, &mmm, &uuu, &nnn);
    sTm.tm_year = yy - 1900;
    sTm.tm_mon = mm - 1;
    sTm.tm_mday = dd;
    sTm.tm_hour = hh;
    sTm.tm_min = mi;
    sTm.tm_sec = ss;
    t1 = mktime(&sTm);
    t1 = t1 * 1000000000L;
    t1 = t1 + (mmm*1000000L) + (uuu*1000) + nnn;

    valueArray[4] = &t1;
    SQLAppendData(aStmt, valueArray);
}
```

#### SQLAppendDataByTime(deprecated)

```cpp
SQLRETURN  SQLAppendDataByTime(SQLHSTMT StatementHandle, SQLBIGINT aTime, void *aData[]);
```
이 함수는 해당 채널에 대해 데이터를 입력하는 함수이며, DB에 저장되는 _arrival_time 값을 현재 시간이 아닌 특정 시간의 값으로 설정할 수 있습니다.

예를 들면, 1개월전 로그 파일에 있는 날짜를 그 당시의 날짜로 입력하고자 할때 사용됩니다.

* aTime은 _arrival_time으로 설정된 time 값입니다.
* aData는 입력될 데이터의 포인터를 담고 있는 배열입니다.
* 배열의 개수는 Open시에 지정한 테이블이 보유하고 있는 컬럼의 개수와 일치해야 합니다.

나머지 사항은 SQLAppendData()함수를 참고하여 작성하면 됩니다.

```cpp
// 4개의 컬럼 정보를 가지는 테이블의 경우  (short(16), int(32), long(64), varchar)

testAppendFuncWithTime()
{
   long long sTime = 1;
   short val1 = 0;
   int   val2 = 1;
   long long  val3 = 2;
   char *val4 = "my string";
   void *valueArray[4];

   valueArray[0] = (void *)&val1;
   valueArray[1] = (void *)&val2;
   valueArray[2] = (void *)&val3;
   valueArray[3] = (void *)val4;

   SQLAppendDataByTime(aStmt, sTime, valueArray);
}
```

#### SQLAppendDataV2

```cpp
SQLRETURN  SQLAppendDataV2(SQLHSTMT StatementHandle, SQL_APPEND_PARAM *aData);
```

이 함수는 Machbase 2.0 부터 새로 도입된 Append 함수로서, 기존의 함수에서 불편했던 입력 방식을 편리하게 대폭 개선한 함수입니다.

특히, 2.0에서 도입된 TEXT와 BINARY 타입의 경우는 SQLAppendDataV2() 함수에서만 입력이 가능합니다.

* 각 타입에 맞는 NULL 입력 가능
* VARCHAR 입력시 스트링 길이 입력 가능
* IPv4, IPv6 입력시 바이너리 및 스트링 형태의 데이터 입력 가능
* TEXT, BINARY 타입에 대한 데이터 길이 지정 가능

함수 인자는 다음과 같이 구성됩니다.

* aData는 SQL_APPEND_PARAM 이라는 인자배열을 가리키는 포인터입니다. 이 배열의 개수는 Open시에 지정한 테이블이 보유하고 있는 컬럼의 개수와 일치해야 합니다.
* 리턴값은 SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, SQL_ERROR 가 가능합니다. 특히, SQL_SUCCESS_WITH_INFO가 반환되었을 경우에는 입력된 특정 컬럼의 길이가 길어 잘리는 등의 오류가 있을 수 있으므로 결과를 다시 확인하여야 합니다.

아래는 실제로 V2에서 사용될 SQL_APPEND_PARAM 의 정의이며, 이 내용은 machbase_sqlcli.h 에 포함되어 있습니다.

```cpp
typedef struct machbaseAppendVarStruct
{
    unsigned int mLength;
    void *mData;
} machbaseAppendVarStruct;

/* for IPv4, IPv6 as bin or string representation */
typedef struct machbaseAppendIPStruct
{
    unsigned char   mLength; /* 0:null, 4:ipv4, 6:ipv6, 255:string representation */
    unsigned char   mAddr[16];
    char           *mAddrString;
} machbaseAppendIPStruct;

/* Date time*/
typedef struct machbaseAppendDateTimeStruct
{
    long long       mTime;
#if defined(SUPPORT_STRUCT_TM)
    struct tm       mTM;
#endif
    char           *mDateStr;
    char           *mFormatStr;
} machbaseAppendDateTimeStruct;

typedef union machbaseAppendParam
{
    short                        mShort;
    unsigned short               mUShort;
    int                          mInteger;
    unsigned int                 mUInteger;
    long long                    mLong;
    unsigned long long           mULong;
    float                        mFloat;
    double                       mDouble;
    machbaseAppendIPStruct       mIP;
    machbaseAppendVarStruct      mVar;     /* for all varying type */
    machbaseAppendVarStruct      mVarchar; /* alias */
    machbaseAppendVarStruct      mText;    /* alias */
    machbaseAppendVarStruct      mJson;    /* alias */
    machbaseAppendVarStruct      mBinary;  /* binary */
    machbaseAppendVarStruct      mBlob;    /* reserved alias */
    machbaseAppendVarStruct      mClob;    /* reserved alias */
    machbaseAppendDateTimeStruct mDateTime;
} machbaseAppendParam;

#define SQL_APPEND_PARAM machbaseAppendParam
```
위에서 볼 수 있듯이 내부적으로 machbaseAppendParam 이라는 공용 구조체가 하나의 인자를 담고 있는 구조입니다. 각 데이터 타입에 대해 데이터 및 스트링에 대한 길이 및 값을 명시적으로 입력할 수 있도록 되어 있습니다. 실제 사용 예는 다음과 같습니다.

**고정 길이 숫자형 타입의 입력**

고정 길이 숫자형 타입이라 함은 short, ushort, integer, uinteger, long, ulong, float, double 을 말합니다. 이 타입의 경우 SQL_APPEND_PARAM의 구조체 멤버에 직접 값을 대입함으로써 입력 가능합니다.

| 데이터베이스 타입 | NULL 매크로              | SQL_APPEND_PARAM 멤버 |
|-------------------|--------------------------|-----------------------|
|       SHORT       |   SQL_APPEND_SHORT_NULL  |         mShort        |
|       USHORT      |  SQL_APPEND_USHORT_NULL  |        mUShort        |
|      INTEGER      |  SQL_APPEND_INTEGER_NULL |        mInteger       |
|      UINTEGER     | SQL_APPEND_UINTEGER_NULL |       mUInteger       |
|        LONG       |   SQL_APPEND_LONG_NULL   |         mLong         |
|       ULONG       |   SQL_APPEND_ULONG_NULL  |         mULong        |
|       FLOAT       |   SQL_APPEND_FLOAT_NULL  |         mFloat        |
|       DOUBLE      |  SQL_APPEND_DOUBLE_NULL  |        mDouble        |

다음은 실제 값을 입력하는 예제입니다.

```cpp
// Table Schema가 8개의 컬럼이고, 각각 SHORT, USHORT, INTEGER, UINTEGER, LONG, ULONG, FLOAT, DOUBLE로 이루어진 것으로 가정합니다.

void testAppendExampleFunc()
{
    SQL_APPEND_PARAM sParam[8];

    /* fixed column */
    sParam[0].mShort = SQL_APPEND_SHORT_NULL;
    sParam[1].mUShort = SQL_APPEND_USHORT_NULL;
    sParam[2].mInteger = SQL_APPEND_INTEGER_NULL;
    sParam[3].mUInteger = SQL_APPEND_UINTEGER_NULL;
    sParam[4].mLong = SQL_APPEND_LONG_NULL;
    sParam[5].mULong = SQL_APPEND_ULONG_NULL;
    sParam[6].mFloat = SQL_APPEND_FLOAT_NULL;
    sParam[7].mDouble = SQL_APPEND_DOUBLE_NULL;

    SQLAppendDataV2(Stmt, sParam);

    /* FIXED COLUMN Value */
    sParam[0].mShort = 2;
    sParam[1].mUShort = 3;
    sParam[2].mInteger = 4;
    sParam[3].mUInteger = 5;
    sParam[4].mLong = 6;
    sParam[5].mULong = 7;
    sParam[6].mFloat = 8.4;
    sParam[7].mDouble = 10.9;

    SQLAppendDataV2(Stmt, sParam);
}
```

**날짜형 타입의 입력**

아래는 DATETIME형의 데이터를 입력하는 예입니다. 편의를 위해 몇가지의 매크로가 준비되어 있습니다.

SQL_APPEND_PARAM에서 mDateTime 멤버에 대한 조작을 수행합니다. 아래의 매크로는 mDateTime 구조체에서 mTime이라는 64비트 정수값에 대해 설정함으로써 날짜를 지정할 수 있습니다.

```cpp
typedef struct machbaseAppendDateTimeStruct
{
    long long       mTime;
#if defined(SUPPORT_STRUCT_TM)
    struct tm       mTM;
#endif
    char           *mDateStr;
    char           *mFormatStr;
} machbaseAppendDateTimeStruct;
```

| 매크로 | 설명 |
|-------------------------------|------------------------------------------------------------|
|    SQL_APPEND_DATETIME_NOW    | 현재의 클라이언트 시간을 입력합니다.                                                                                                                                                                                      |
| SQL_APPEND_DATETIME_STRUCT_TM | mDateTime의 struct tm 구조체인 mTM에 값을 설정하고, 그 값을 데이터베이스로 입력합니다.                                                                                                                                    |
|   SQL_APPEND_DATETIME_STRING  | mDateTime의 스트링형에 대한 값을 설정하고, 이를 데이터베이스로 입력합니다.<br> mDateStr : 실제 날짜 스트링 값이 할당<br> mFormatStr : 날짜 스트링에 대한 포맷 스트링 할당                                                         |
|    SQL_APPEND_DATETIME_NULL   | 날짜 컬럼의 값을 NULL로 입력합니다.                                                                                                                                                                                       |
|        임의의 64비트 값       | 이 값이 실제 datetime으로 입력됩니다.<br> 이 값을 1970년 1월 1일 이후로부터 나노세컨드 단위의 시간이 흐른 정수값을 나타냅니다. <br>예를 들어, 만일 이 값이 10억 (1,000,000,000) 이라면, 1970년 1월 1일 0시 0분 1초를 나타냅니다.(GMT) |

```cpp
// 다음은 각각의 경우에 대해 실제 값을 입력하는 예제입니다. 하나의 DATETIME 컬럼이 존재한다고 가정합니다.
void testAppendDateTimeFunc()
{
    SQL_APPEND_PARAM sParam[1];
    /* NULL 입력 */
    sParam[0].mDateTime.mTime   = SQL_APPEND_DATETIME_NULL;
    SQLAppendDataV2(Stmt, sParam);

    /* 현재 시간 입력 */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_NOW;
    SQLAppendDataV2(Stmt, sParam);

    /* 임의의 값 입력 :1970.1.1일 이후로부터의 현재까지 나노세컨드의 값 */
    sParam[0].mDateTime.mTime      = 1234;
    SQLAppendDataV2(Stmt, sParam);

    /*  스트링 포맷 기준 입력 */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRING;
    sParam[0].mDateTime.mDateStr   = "23/May/2014:17:41:28";
    sParam[0].mDateTime.mFormatStr = "DD/MON/YYYY:HH24:MI:SS";
    SQLAppendDataV2(Stmt, sParam);

    /*  struct tm의 값을 변경하여 입력 */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRUCT_TM;
    sParam[0].mDateTime.mTM.tm_year = 2000 - 1900;
    sParam[0].mDateTime.mTM.tm_mon  =  11;
    sParam[0].mDateTime.mTM.tm_mday  = 31;
    SQLAppendDataV2(Stmt, sParam);
}
```

**인터넷 주소형 타입의 입력**

아래는 IPv4와 IPv6 형의 데이터를 입력하는 예입니다. 이 역시 편의를 위해 몇가지의 매크로가 준비되어 있습니다. SQL_APPEND_PARAM에서 mLength 멤버에 대한 조작을 수행합니다.

```cpp
/* for IPv4, IPv6 as bin or string representation */
typedef struct machbaseAppendIPStruct
{
    unsigned char   mLength; /* 0:null, 4:ipv4, 6:ipv6, 255:string representation */
    unsigned char   mAddr[16];
    char           *mAddrString;
} machbaseAppendIPStruct;
```

| 매크로 (mLength 에 설정) | 설명                                     |
|--------------------------|------------------------------------------|
|    SQL_APPEND_IP_NULL    |        해당 컬럼에 NULL 값을 입력        |
|    SQL_APPEND_IP_IPV4    |        mAddr이 IPv4를 가지고 있음        |
|    SQL_APPEND_IP_IPV6    |        mAddr이 IPv6를 가지고 있음        |
|   SQL_APPEND_IP_STRING   | mAddrString이 주소 문자열을 가지고 있습니다. |

다음은 각각의 경우에 대해 실제 값을 입력하는 예제입니다.

```cpp
void testAppendIPFunc()
{
    SQL_APPEND_PARAM sParam[1];
    /* NULL */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_NULL;
    SQLAppendDataV2(Stmt, sParam);

    /* 배열을 직접 수정 */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV4;
    sParam[0].mIP.mAddr[0] = 127;
    sParam[0].mIP.mAddr[1] = 0;
    sParam[0].mIP.mAddr[2] = 0;
    sParam[0].mIP.mAddr[3] = 1;
    SQLAppendDataV2(Stmt, sParam);

    /* IPv4 from binary */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV4;
    *(in_addr_t *)(sParam[0].mIP.mAddr) = inet_addr("192.168.0.1");
    SQLAppendDataV2(Stmt, sParam);

    /* IPv4 : ipv4 from string */
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "203.212.222.111";
    SQLAppendDataV2(Stmt, sParam);

    /* IPv4 : ipv4 from invalid string */
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "ip address is not valid";
    SQLAppendDataV2(Stmt, sParam);                           // invalid IP value

    /* IPv6 : ipv6 from binary bytes */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV6;
    sParam[0].mIP.mAddr[0]  = 127;
    sParam[0].mIP.mAddr[1]  = 127;
    sParam[0].mIP.mAddr[2]  = 127;
    sParam[0].mIP.mAddr[3]  = 127;
    sParam[0].mIP.mAddr[4]  = 127;
    sParam[0].mIP.mAddr[5]  = 127;
    sParam[0].mIP.mAddr[6]  = 127;
    sParam[0].mIP.mAddr[7]  = 127;
    sParam[0].mIP.mAddr[8]  = 127;
    sParam[0].mIP.mAddr[9]  = 127;
    sParam[0].mIP.mAddr[10] = 127;
    sParam[0].mIP.mAddr[11] = 127;
    sParam[0].mIP.mAddr[12] = 127;
    sParam[0].mIP.mAddr[13] = 127;
    sParam[0].mIP.mAddr[14] = 127;
    sParam[0].mIP.mAddr[15] = 127;
    SQLAppendDataV2(Stmt, sParam);

    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "::127.0.0.1";
    SQLAppendDataV2(Stmt, sParam);

    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "FFFF:FFFF:1111:2222:3333:4444:7733:2123";
    SQLAppendDataV2(Stmt, sParam);
}
```

IP 타입을 문자열 (STRING) 로 입력할경우 SQLAppendDataV2 이후에 각각 자료형에 맞게 mLength가 4 또는 6으로 바뀌게 됩니다.
따라서 반복문에서 코딩할 경우 매번 SQLAppendDataV2() 전에, mLength 를 SQL_APPEND_IP_STRING 으로 지정해 주어야 합니다.

**가변 데이터형(문자 및 이진 데이터) 입력**

가변 데이터 형에는 VARCHAR 및 TEXT 그리고, BLOB과 CLOB이 포함됩니다. 기존함수에서는 VARCHAR 만이 지원되었고, 또한 스트링의 길이를 사용자가 입력할 수 있는 방법이 없었습니다. 그런 이유로 매번 strlen() 함수를 통해 길이를 얻어야 했지만, 함수 V2 부터는 사용자가 직접 가변 데이터형에 대한 길이를 지정할 수 있게 되었습니다. 따라서, 만일 사용자가 그 길이를 미리 알고 있다면, 더 빠르게 데이터를 입력할 수 있습니다. 내부적으로는 가변 데이터형이 하나의 구조체로 되어 있지만, 개발 편의를 위해 각 데이터타입에 따라 멤버를 별도로 만들어 놓았습니다.

```cpp
typedef struct machbaseAppendVarStruct
{
    unsigned int mLength;
    void *mData;
} machbaseAppendVarStruct;
```

가변 데이터형의 입력시에는 데이터의 길이를 mLength에 설정하고, 원시 데이터 포인터를 mData로 설정하면 됩니다. 만일 mLength의 길이가 정의된 스키마보다 클 경우에는 자동으로 잘려서 입력됩니다. 이때 SQLAppendDataV2() 함수는 SQL_SUCCESS_WITH_INFO을 리턴하게 되고, 더불어 관련 경고 메시지를 내부 구조체에 채웁니다. 이 경고 메시지를 확인하기 위해서는 SQLError() 함수를 이용하면 됩니다.

| 데이터베이스 타입 | NULL 매크로             | SQL_APPEND_PARAM 멤버 (mVar를 사용해도 무방함) |
|-------------------|-------------------------|:----------------------------------------------:|
|      VARCHAR      | SQL_APPEND_VARCHAR_NULL |                    mVarchar                    |
|        TEXT       |   SQL_APPEND_TEXT_NULL  |                      mText                     |
|        JSON       |   SQL_APPEND_JSON_NULL  |                      mJson                     |
|       BINARY      |  SQL_APPEND_BINARY_NULL |                     mBinary                    |
|        BLOB       |   SQL_APPEND_BLOB_NULL  |                      mBlob                     |
|        CLOB       |   SQL_APPEND_CLOB_NULL  |                      mClob                     |

다음은 각각의 환경에 대해 실제 값을 입력하는 예제입니다. 하나의 VARCHAR 컬럼이 존재한다고 가정합니다.

```sql
CREATE TABLE ttt (name VARCHAR(10));
```

```cpp

void testAppendVarcharFunc()
{
    SQL_APPEND_PARAM sParam[1];

    /*  VARCHAR : NULL */
    sParam[0].mVarchar.mLength = SQL_APPEND_VARCHAR_NULL;
    SQLAppendDataV2(Stmt, sParam); /* OK */

    /*  VARCHAR : string */
    strcpy(sVarchar, "MY VARCHAR");
    sParam[0].mVarchar.mLength = strlen(sVarchar);
    sParam[0].mVarchar.mData   = sVarchar;
    SQLAppendDataV2(Stmt, sParam); /* OK */

    /*  VARCHAR : Truncation! */
    strcpy(sVarchar, "MY VARCHAR9"); /* Truncation! */
    sParam[0].mVarchar.mLength = strlen(sVarchar);
    sParam[0].mVarchar.mData   = sVarchar;
    SQLAppendDataV2(Stmt, sParam);  /* SQL_SUCCESS_WITH_INFO */
}
```

다음은 Text 타입에 대한 입력 예제입니다.

```sql
CREATE TABLE ttt (doc TEXT);
```

```cpp
void testAppendFunc()
{
    SQL_APPEND_PARAM sParam[1];

    /*  TEXT : NULL */
    sParam[0].mText.mLength = SQL_APPEND_TEXT_NULL;
    SQLAppendDataV2(Stmt, sParam); /* OK */

    /*  TEXT : string */
    strcpy(sText, "This is the sample document for tutorial.");
    sParam[0].mVar.mLength = strlen(sText);
    sParam[0].mVar.mData   = sText;
    SQLAppendDataV2(Stmt, sParam); /* OK */
}
```

#### SQLAppendDataByTimeV2

```cpp
SQLRETURN  SQLAppendDataByTimeV2(SQLHSTMT StatementHandle, SQLBIGINT aTime, SQL_APPEND_PARAM  *aData);
```

이 함수는 해당 채널에 대해 데이터를 입력하는 함수이며, DB에 저장되는 _arrival_time 값을 현재 시간이 아닌 특정 시간의 값으로 설정할 수 있습니다. 예를 들면, 1개월전 로그 파일에 있는 날짜를 그 당시의 날짜로 입력하고자 할때 사용됩니다.

* aTime은 _arrival_time으로 설정될 time값입니다. 1970년 1월 1일 이후로부터의 현재까지 nano second 값을 입력해야 합니다. 또한 입력되는 값이 과거부터 현재순으로 순차적으로 정렬되어 있어야 합니다.
* aData는 입력될 데이터의 포인터를 담고 있는 배열입니다. 배열의 개수는 Open시에 지정한 테이블이 보유하고 있는 컬럼의 개수와 일치해야 합니다.

 나머지 사항은 SQLAppendDataV2()함수를 참고하여 작성하면 됩니다.

#### SQLAppendDataV3 및 SQLAppendDataByTimeV3

```cpp
SQLRETURN SQLAppendDataV3(SQLHSTMT aStmtHandle,
                          SQL_APPEND_PARAM *aData,
                          SQLINTEGER aColCount);

SQLRETURN SQLAppendDataByTimeV3(SQLHSTMT aStmtHandle,
                                SQLBIGINT aTime,
                                SQL_APPEND_PARAM *aData,
                                SQLINTEGER aColCount);
```

V3는 V2와 동일한 `SQL_APPEND_PARAM` 값을 사용하며 `aColCount`를 추가로 받습니다.
클라이언트가 전달하는 값 개수를 `SQLAppendOpen`으로 연 테이블 메타데이터에만 의존하지 않고 명시해야 할 때 사용합니다.

#### SQLAppendBatch 및 SQLAppendBatchByTime

```cpp
SQLRETURN SQLAppendBatch(SQLHSTMT aStmtHandle,
                         SQLCHAR *aTableName,
                         SQLINTEGER aRowCount,
                         SQLINTEGER aColCount,
                         SQL_APPEND_TYPES *aTypes,
                         SQL_APPEND_PARAM *aData);

SQLRETURN SQLAppendBatchByTime(SQLHSTMT aStmtHandle,
                               SQLCHAR *aTableName,
                               SQLBIGINT aTime,
                               SQLINTEGER aRowCount,
                               SQLINTEGER aColCount,
                               SQL_APPEND_TYPES *aTypes,
                               SQL_APPEND_PARAM *aData);
```

Batch append는 직사각형 row set을 한 번의 호출로 전송합니다. `aTypes`는 `SQL_APPEND_TYPE_*` 값 배열이고, `aData`는 row 순서로 배치한 `aRowCount * aColCount`개의 값입니다. JSON 컬럼에는 `SQL_APPEND_TYPE_JSON`을 사용할 수 있으며, 가변 이진/문자 payload용 BLOB/CLOB 타입 항목도 유지됩니다.

#### SQLAppendFlush

 ```cpp
 SQLRETURN SQLAppendFlush(SQLHSTMT StatementHandle);
 ```

 이 함수는 현재 채널 버퍼에 쌓여있는 데이터를 Machbase 서버로 즉시 전송합니다.

#### SQLAppendClose

 ```cpp
 SQLRETURN SQLAppendClose(SQLHSTMT   aStmtHandle,
                         SQLBIGINT* aSuccessCount,
                         SQLBIGINT* aFailureCount);
 ```

 이 함수는 현재 열린 채널을 닫습니다. 만일 열려지지 않은 채널이 존재할 경우 에러가 발생합니다.

* aSuccessCount : Append를 성공한 레코드 개수 값을 가집니다.
* aFailureCount : Append를 실패한 레코드 개수 값을 가집니다.

#### SQLAppendSetErrorCallback

```cpp
SQLRETURN SQLAppendSetErrorCallback(SQLHSTMT aStmtHandle, SQLAppendErrorCallback aFunc);
```

이 함수는 SQLAppendOpen()이 성공한 다음 Append시 에러가 발생했을 때 호출되는 콜백 함수를 설정합니다. 만일 이 함수를 설정하지 않을 경우에는 서버에 에러가 발생하더라도, 클라이언트에서는 무시하게 됩니다.

* aStmtHandle : 에러를 확인할 Statement를 지정합니다.
* aFunc : Append 실패시 호출할 함수 포인터를 지정합니다.

SQLAppendErrorCallback의 프로토타입은 다음과 같습니다.

```cpp
typedef void (*SQLAppendErrorCallback)(SQLHSTMT aStmtHandle,
                                     SQLINTEGER aErrorCode,
                                     SQLPOINTER aErrorMessage,
                                         SQLLEN aErrorBufLen,
                                     SQLPOINTER aRowBuf,
                                         SQLLEN aRowBufLen);
```

* aStatementHandle : 에러를 발생한 Statement 핸들
* aErrorCode : 에러의 원인이 된 32비트 에러 코드
* aErrorMessage : 해당 에러코드에 대한 문자열
* aErrorBufLen : aErrorMessage의 길이
* aRowBuf : 에러를 발생시킨 레코드의 상세 명세가 담긴 문자열
* aRowBufLen : aRowBuf의 길이

**에러 콜백(dumpError)의 사용 예**

```cpp
void dumpError(SQLHSTMT    aStmtHandle,
               SQLINTEGER  aErrorCode,
               SQLPOINTER  aErrorMessage,
               SQLLEN      aErrorBufLen,
               SQLPOINTER  aRowBuf,
               SQLLEN      aRowBufLen)
{
    char       sErrMsg[1024] = {0, };
    char       sRowMsg[32 * 1024] = {0, };

    if (aErrorMessage != NULL)
    {
        strncpy(sErrMsg, (char *)aErrorMessage, aErrorBufLen);
    }

    if (aRowBuf != NULL)
    {
        strncpy(sRowMsg, (char *)aRowBuf, aRowBufLen);
    }

    fprintf(stdout, "Append Error : [%d][%s]\n[%s]\n\n", aErrorCode, sErrMsg, sRowMsg);
}


......

    if( SQLAppendOpen(m_IStmt, TableName, aErrorCheckCount) != SQL_SUCCESS )
    {
        fprintf(stdout, "SQLAppendOpen error\n");
        exit(-1);
    }
    // 콜백을 설정합니다.
    assert(SQLAppendSetErrorCallback(m_IStmt, dumpError) == SQL_SUCCESS);

    doAppend(sMaxAppend);

    if( SQLAppendClose(m_IStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        fprintf(stdout, "SQLAppendClose error\n");
        exit(-1);
    }
}
```

#### SQLSetConnectAppendFlush

```cpp
SQLRETURN SQL_API SQLSetConnectAppendFlush(SQLHDBC hdbc, SQLINTEGER option)
```

Append에 의해서 입력된 데이터는 통신 버퍼에 기록되어 전송대기 상태에서 사용자가 SQLAppendFlush 함수를 호출하거나 통신 버퍼가 가득 차게 되면 서버로 전송됩니다. 사용자가 버퍼가 가득 차 있지 않아도 일정 주기로 서버에게 Append에 의한 데이터를 전송하게 하려면 이 함수를 이용하면 됩니다. 이 함수는 매 100ms 주기로 마지막으로 전송한 시간과 현재 시간의 차이를 계산하여 지정된 시간(설정하지 않은 경우에는 1초)가 지난 경우 통신 버퍼의 내용을 서버에 전달합니다.

매개변수는 다음과 같습니다.

* hdbc : DB의 connection handle입니다.
* option : 0이면 auto flush를 off, 0이 아닌 값이면 auto flush를 on으로 합니다.

연결되지 않은 hdbc에 대해서 실행하면 오류로 처리됩니다.

#### SQLSetStmtAppendInterval

```cpp
SQLRETURN SQL_API SQLSetStmtAppendInterval(SQLHSTMT hstmt, SQLINTEGER fValue)
```

SQLSetConnectAppendFlush를 이용해서 시간 단위 flush기능을 켰을 경우, 특정 statement에 대해서는 자동 flush를 끄거나 flush 주기를 조정하고 싶을 경우 이 함수를 사용합니다.

매개변수는 다음과 같습니다.

* hstmt : flush주기를 조정하고자 하는 statement handle입니다.
* fValue : flush주기를 조정하고자 하는 값입니다. 0이면 flush를 하지 않으며 단위는 ms입니다. 100ms마다 flush할지를 결정하는 스레드가 실행되므로 100의 배수로 설정합니다. 정확히 원하는 시점에 자동 flush가 실행되지는 않습니다. 1000이 기본 값입니다.

시간 기반 flush가 실행중이지 않은 경우라도 이 함수의 실행은 성공합니다.

**Error 확인 및 설명**

Append 관련 함수를 사용할때 에러를 확인하는 방법과 코드에 대한 설명입니다. CLI 함수에서 return 값이 SQL_SUCCESS가 아닌 경우 아래 코드를 이용하여 에러 메시지를 확인할 수 있습니다.

```cpp
SQLINTEGER errNo;
int msgLength;
char sqlState[6];
char errMsg[1024];

if (SQL_SUCCESS == SQLError ( env, con, stmt, (SQLCHAR *)sqlState, &errNo,
                              (SQLCHAR *)errMsg, 1024, &msgLength ))
{
    //error code값을 5자리 숫자로 지정합니다.
    printf("ERROR-%05d: %s\n", errNo, errMsg);
}
```

Append관련 함수에서 리턴되는 에러 메시지는 아래와 같습니다.

<table>
  <thead>
    <tr>
      <th>function</th>
      <th>message</th>
      <th>description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="7">SQLAppendOpen</td>
      <td>statement is already opened.</td>
      <td>중복으로 SQLAppendOpen을 하는 경우 발생합니다.</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>스트림 프로토콜 종료에 실패했습니다.</td>
    </tr>
    <tr>
      <td>Failed to read protocol.</td>
      <td>네트워크 읽기 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>column meta 정보 구조가 잘못됨</td>
    </tr>
    <tr>
      <td>cannot allocate memory.</td>
      <td>내부 버퍼 메모리 할당 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td>cannot allocate compress memory.</td>
      <td>압축 버퍼 메모리 할당 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>return값에 오류가 있습니다.</td>
    </tr>
    <tr>
      <td rowspan="3">SQLAppendData</td>
      <td>statement is not opened.</td>
      <td>AppendOpen을 하지 않고 AppendData를 call합니다.</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>varchar 타입 컬럼에 지정된 사이즈 보다 큰 데이터를 입력하는 경우 발생합니다.</td>
    </tr>
    <tr>
      <td>Failed to add binary.</td>
      <td>통신버퍼에 쓰기 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td rowspan="5">SQLAppendClose</td>
      <td>statement is not opened.</td>
      <td>AppendOpen상태가 아님.</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>스트림 프로토콜 종료에 실패했습니다.</td>
    </tr>
    <tr>
      <td>Failed to close buffer protocol.</td>
      <td>버퍼 프로토콜 종료에 실패했습니다.</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>column meta정보 구조가 잘못됩니다.</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>return값에 오류가 있습니다.</td>
    </tr>
    <tr>
      <td rowspan="2">SQLAppendFlush</td>
      <td>statement is not opened.</td>
      <td>AppendOpen상태가 아님</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>네트워크 쓰기 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td rowspan="2">SQLSetErrorCallback</td>
      <td>statement is not opened.</td>
      <td>AppendOpen상태가 아님.</td>
    </tr>
    <tr>
      <td>Protocol Error (not APPEND_DATA_PROTOCOL)</td>
      <td>통신 버퍼 읽기 결과가 APPEND_DATA_PROTOCOL 값이 아님.</td>
    </tr>
    <tr>
      <td rowspan="8">SQLAppendDataV2</td>
      <td>Invalid date format or date string.</td>
      <td>날짜/시간 유형이 잘못된 경우 발생.</td>
    </tr>
    <tr>
      <td>statement is not opened.</td>
      <td>AppendOpen상태가 아님.</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>바이너리 유형 열에 지정된 크기보다 큰 데이터를 입력하는 경우 발생</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>varchar 타입 컬럼에 지정된 사이즈 보다 큰 데이터를 입력하는 경우 발생합니다.</td>
    </tr>
    <tr>
      <td>Failed to add stream.</td>
      <td>통신버퍼에 쓰기 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td>IP address length is invalid.</td>
      <td>IPv4, IPv6 유형 구조의 mLength 값이 잘못 지정됩니다.</td>
    </tr>
    <tr>
      <td>IP string is invalid.</td>
      <td>IPv4 또는 IPv6 형식이 아님.</td>
    </tr>
    <tr>
      <td>Unknown data type has been specified.</td>
      <td>Machbase에서 사용하는 데이터 유형이 아님.</td>
    </tr>
  </tbody>
</table>

## 열 형식 매개변수 바인딩

이를 위해서 Machbase 5.5 이후 버전에서는 열 형색 매개변수 바인딩을 지원합니다. (행 형식 매개변수 바인딩은 아직 지원되지 않습니다.)

함수 SQLSetStmtAttr()의 인자 Attribute에 SQL_ATTR_PARAM_BIND_TYPE을 설정하고 인자 param에 SQL_PARAM_BIND_BY_COLUMN을 설정합니다. 바인드할 각  칼럼에 대해서 매개변수를 배열로 설정하고, 지시자 변수 또한 배열로 설정합니다. 이후 SQLBindParameter()를 이 매개변수를 전달하여 호출합니다.

아래 그림은 각 매개변수 배열에 대해 열 형식 바인딩이 동작하는 방식을 보여줍니다.

| Column A<br>(parameter A)             | Column B<br>(parameter B)             | Column C<br>(parameter C)             |
| ------------------------------------- | ------------------------------------- | ------------------------------------- |
| Value_Array<br>Indicator/length array | Value_Array<br>Indicator/length array | Value_Array<br>Indicator/length array |

아래 예제는 열 형식 매개변수 바인딩을 이용하여 대량의 데이터를 삽입하는 예제입니다.

```cpp
#define DESC_LEN 51
#define ARRAY_SIZE 10
SQLCHAR * Statement = "INSERT INTO Parts (PartID, Description, Price) VALUES (?, ?, ?)";

/* 바인드할 매개변수 배열 */
SQLUINTEGER PartIDArray[ARRAY_SIZE];
SQLCHAR DescArray[ARRAY_SIZE][DESC_LEN];
SQLREAL PriceArray[ARRAY_SIZE];
/* 바인드할 지사자 변수 배열 */
SQLINTEGER PartIDIndArray[ARRAY_SIZE], DescLenOrIndArray[ARRAY_SIZE], PriceIndArray[ARRAY_SIZE];
SQLUSMALLINT i, ParamStatusArray[ARRAY_SIZE];
SQLUINTEGER ParamsProcessed;

// Set the SQL_ATTR_PARAM_BIND_TYPE statement attribute to use
// column-wise binding.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_BIND_TYPE, SQL_PARAM_BIND_BY_COLUMN, 0);
// Specify the number of elements in each parameter array.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMSET_SIZE, ARRAY_SIZE, 0);
// Specify an array in which to return the status of each set of
// parameters.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_STATUS_PTR, ParamStatusArray, 0);
// Specify an SQLUINTEGER value in which to return the number of sets of
// parameters processed.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMS_PROCESSED_PTR, &ParamsProcessed, 0);
// Bind the parameters in column-wise fashion.
SQLBindParameter(hstmt, 1, SQL_PARAM_INPUT, SQL_C_ULONG, SQL_INTEGER, 5, 0,
    PartIDArray, 0, PartIDIndArray);
SQLBindParameter(hstmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, DESC_LEN - 1, 0,
    DescArray, DESC_LEN, DescLenOrIndArray);
SQLBindParameter(hstmt, 3, SQL_PARAM_INPUT, SQL_C_FLOAT, SQL_REAL, 7, 0,
    PriceArray, 0, PriceIndArray);
```

## 지원되는 문자열

마크베이스는 기본적으로 UTF-8 방식을 사용하여 문자열 데이터를 저장합니다.

UTF-8 이외의 방식으로 문자열을 입/출력하는 Windows의 경우 ODBC에서 아래와 같이 변환합니다.

|    OS   | Unicode/Non-Unicode |   문자열 변환  |                              Note                              |
|:-------:|:-------------------:|:--------------:|:--------------------------------------------------------------:|
| Windows | Unicode (UTF-16)    | UTF-16 ⟷ UTF-8 | N/A                                                            |
| Windows | Non-Unicode (MBCS)  | MBCS ⟷ UTF-8   | Windows 설정의 Non-Unicode 어플리케이션의 기본 문자열을 사용함 |
| Linux   | UTF-8               | N/A            | UTF-8 만 지원됨                                                |

## cli-odbc-example


## 응용 프로그램 개발

### CLI 설치 확인

마크베이스가 설치된 디렉터리의 include 및 lib에 다음과 같은 파일이 있으면 응용 프로그램을 개발할 수 있는 환경이 완비된 것입니다.


```bash
Mach@localhost:~/machbase_home$ ls -l include lib install/
include:
total 176
-rwxrwxr-x 1 mach mach 31449 Jun 18 19:26 machbase_sqlcli.h

install/:
total 12
-rw-rw-r-- 1 mach mach 1667 Jun 18 19:26 machbase_env.mk

lib:
total 16196
-rw-rw-r-- 1 mach mach  78603 Jun 18 19:26 machbase.jar
-rw-rw-r-- 1 mach mach 964290 Jun 18 19:26 libmachbasecli.a
```

### Makefile 작성 가이드

```bash
mach@localhost:~/machbase_home$ cd sample/
mach@localhost:~/machbase_home/sample$ cd cli/
mach@localhost:~/machbase_home/sample/cli$ ls
Makefile sample1_connect.c
```
마크베이스 패키지를 설치했다면, 다음 경로에 샘플 프로그램이 설치되어 있을 것입니다.

```makefile
include $(MACHBASE_HOME)/install/machbase_env.mk
INCLUDES += $(LIBDIR_OPT)/$(MACHBASE_HOME)/include

all : sample1_connect

sample1_connect : sample1_connect.o
    $(LD_CC) $(LD_FLAGS) $(LD_OUT_OPT)$@ $< $(LIB_OPT)machbasecli$(LIB_AFT) $(LIBDIR_OPT)$(MACHBASE_HOME)/lib $(LD_LIBS)

sample1_connect.o : sample1_connect.c
    $(COMPILE.cc) $(CC_FLAGS) $(INCLUDES) $(CC_OUT_OPT)$@ $<

clean :
    rm -f sample1_connect
```

### 컴파일 및 링크

주어진 샘플에 대해 다음과 같이 수행하면 실행 파일이 만들어집니다.

```bash
mach@localhost:~/machbase_home/sample/cli$ make
gcc -c -g -W -Wall -rdynamic -O3 -finline-functions -fno-omit-frame-pointer -fno-strict-aliasing -m64 -mtune=k8 -g -W -Wall -rdynamic -O3 -finline-functions -fno-omit-frame-pointer -fno-strict-aliasing -m64 -mtune=k8 -I/home/machbase/machbase_home/include -I. -L//home/machbase/machbase_home/include -osample1_connect.o sample1_connect.c
gcc -m64 -mtune=k8 -L/home/machbase/machbase_home/lib -osample1_connect sample1_connect.o -lmachbasecli -L/home/machbase/machbase_home/lib -lm -lpthread -ldl -lrt -rdynamic
mach@localhost:~/machbase_home/sample/cli$ ls -al
total 1196
drwxrwxr-x 2 mach mach 4096 Jun 18 20:15 .
drwxrwxr-x 4 mach mach 4096 Jun 18 19:26 ..
-rw-rw-r-- 1 mach mach 483 Jun 18 19:26 Makefile
-rwxrwxr-x 1 mach mach 1196943 Jun 18 20:15 sample1_connect
-rw-rw-r-- 1 mach mach 549 Jun 18 19:26 sample1_connect.c
-rw-rw-r-- 1 mach mach 8168 Jun 18 20:15 sample1_connect.o
```
필요에 따라 얼마든지 위의 샘플 Makefile을 수정하여 응용 프로그램을 작성할 수 있을 것입니다.

## 샘플 프로그램

### 접속 예제

CLI를 이용하여 접속하는 예제 프로그램을 작성해 보기로 합니다.

샘플 파일명은 sample1_connect.c 로 합니다.

MACHBASE_PORT_NO는 $MACHBASE_HOME/conf/machbase.conf 파일에 있는 PORT_NO 값과 같아야 합니다.

<details>
<summary>sample1_connect.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <machbase_sqlcli.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;

void connectDB()
{
    char connStr[1024];
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        printf("SQLAllocEnv error!!\n");
        exit(1);
    }
    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        printf("SQLAllocConnect error!!\n");
        SQLFreeEnv(gEnv);
        exit(1);
    }
    sprintf(connStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);
    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)connStr,
                                       SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        printf("connection error\n");
        if (SQL_SUCCESS == SQLError ( gEnv, gCon, NULL, NULL, &errNo,
                                      errMsg, 1024, &msgLength ))
        {
            printf("mach-%d : %s\n", errNo, errMsg);
        }
        SQLFreeEnv(gEnv);
        exit(1);
    }
    printf("connected ... \n");
}

void disconnectDB()
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLDisconnect(gCon))
    {
        printf("disconnect error\n");

        if( SQL_SUCCESS == SQLError( gEnv, gCon, NULL, NULL, &errNo,
                                     errMsg, 1024, &msgLength ))
        {
            printf("mach-%d : %s\n", errNo, errMsg);
        }
    }

    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

int main()
{
    connectDB();
    disconnectDB();
    return 0;
}
```

</div>
</details>

Makefile에 sample1_connect.c를 등록하고 컴파일하여 실행하면 다음과 같이 나옵니다.

```bash
[mach@localhost cli]$ make

[mach@localhost cli]$ ./sample1_connect
connected ...
```

### 데이터 입력 및 출력 예제

아래의 예제 소스에서는 CREATE TABLE 구문을 이용하여 테이블을 생성하고, 간단한 데이터 값들을 임의로 생성해서 INSERT 구문을 사용해서 데이터를 입력하고, SELECT 구문을 이용하여 데이터를 출력합니다. 이를 활용하여 직접 값을 입력하고 확인할 때 각 타입별로 어떻게 설정을 해야 하는지 알수 있을 것입니다.

샘플 파일명은 sample2_insert.c 라고 합니다.

<details>
<summary>sample2_insert.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB()
{
    char connStr[1024];
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];
    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        printf("SQLAllocEnv error!!\n");
        exit(1);
    }
    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        printf("SQLAllocConnect error!!\n");
        SQLFreeEnv(gEnv);
        exit(1);
    }
    sprintf(connStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);
    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)connStr,
                                       SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        printf("connection error\n");
        if (SQL_SUCCESS == SQLError ( gEnv, gCon, NULL, NULL, &errNo,
                                      errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
        SQLFreeEnv(gEnv);
        exit(1);
    }
    printf("connected ... \n");
}

void disconnectDB()
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];
    if (SQL_ERROR == SQLDisconnect(gCon)) {
        printf("disconnect error\n");
        if( SQL_SUCCESS == SQLError( gEnv, gCon, NULL, NULL, &errNo,
                                     errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
    }
    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg, SQLHSTMT stmt)
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];
    printf("ERROR : (%s)\n", aMsg);
    if (SQL_SUCCESS == SQLError( gEnv, gCon, stmt, NULL, &errNo,
                                 errMsg, 1024, &msgLength ))
    {
        printf(" mach-%d : %s\n", errNo, errMsg);
    }
    exit(-1);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT stmt;
    if (SQLAllocStmt(gCon, &stmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error", stmt);
    }
    if (SQLExecDirect(stmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        printf("sql_exec_direct error[%s] \n", aSQL);
        outError("sql_exec_direct error", stmt);
    }
    if (SQL_ERROR == SQLFreeStmt(stmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error", stmt);
    }
}

void prepareExecuteSQL(const char *aSQL)
{
    SQLHSTMT stmt;
    if (SQLAllocStmt(gCon, &stmt) == SQL_ERROR)
    {
        outError("AllocStmt error", stmt);
    }
    if (SQLPrepare(stmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        printf("Prepare error[%s]\n", aSQL);
        outError("Prepare error", stmt);
    }
    if (SQLExecute(stmt) == SQL_ERROR)
    {
        outError("prepared execute error", stmt);
    }
    if (SQL_ERROR == SQLFreeStmt(stmt, SQL_DROP))
    {
        outError("FreeStmt Error", stmt);
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE1", 1);
    executeDirectSQL("CREATE TABLE CLI_SAMPLE1(seq short, score integer, total long, percentage float, ratio double, id varchar(10), srcip ipv4, dstip ipv6, reg_date datetime, textlog text, image binary)", 0);
}

void selectTable()
{
    SQLHSTMT stmt;
    const char *aSQL = "SELECT seq, score, total, percentage, ratio, id, srcip, dstip, reg_date, textlog, image FROM CLI_SAMPLE1";
    int i=0;
    SQLLEN Len = 0;
    short seq;
    int score;
    long total;
    float percentage;
    double ratio;
    char id [11];
    char srcip[16];
    char dstip[40];
    SQL_TIMESTAMP_STRUCT regdate;
    char log [1024];
    char image[1024];
    if (SQLAllocStmt(gCon, &stmt) == SQL_ERROR) {
        outError("AllocStmt Error", stmt);
    }
    if (SQLPrepare(stmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR) {
        printf("Prepare error[%s] \n", aSQL);
        outError("Prepare error", stmt);
    }
    if (SQLExecute(stmt) == SQL_ERROR) {
        outError("prepared execute error", stmt);
    }
    SQLBindCol(stmt, 1, SQL_C_SHORT, &seq, 0, &Len);
    SQLBindCol(stmt, 2, SQL_C_LONG, &score, 0, &Len);
    SQLBindCol(stmt, 3, SQL_C_BIGINT, &total, 0, &Len);
    SQLBindCol(stmt, 4, SQL_C_FLOAT, &percentage, 0, &Len);
    SQLBindCol(stmt, 5, SQL_C_DOUBLE, &ratio, 0, &Len);
    SQLBindCol(stmt, 6, SQL_C_CHAR, id, sizeof(id), &Len);
    SQLBindCol(stmt, 7, SQL_C_CHAR, srcip, sizeof(srcip), &Len);
    SQLBindCol(stmt, 8, SQL_C_CHAR, dstip, sizeof(dstip), &Len);
    SQLBindCol(stmt, 9, SQL_C_TYPE_TIMESTAMP, &regdate, 0, &Len);
    SQLBindCol(stmt, 10, SQL_C_CHAR, log, sizeof(log), &Len);
    SQLBindCol(stmt, 11, SQL_C_CHAR, image, sizeof(image), &Len);
    while (SQLFetch(stmt) == SQL_SUCCESS)
    {
        printf("===== %d ========\n", i++);
        printf("seq = %d", seq);
        printf(", score = %d", score);
        printf(", total = %ld", total);
        printf(", percentage = %.2f", percentage);
        printf(", ratio = %g", ratio);
        printf(", id = %s", id);
        printf(", srcip = %s", srcip);
        printf(", dstip = %s", dstip);
        printf(", regdate = %d-%02d-%02d %02d:%02d:%02d",
               regdate.year, regdate.month, regdate.day,
               regdate.hour, regdate.minute, regdate.second);
        printf(", log = %s", log);
        printf(", image = %s\n", image);
    }
    if (SQL_ERROR == SQLFreeStmt(stmt, SQL_DROP))
    {
        outError("FreeStmt eror", stmt);
    }
}

void directInsert()
{
    int i;
    char query[2 * 1024];
    short seq;
    int score;
    long total;
    float percentage;
    double ratio;
    char id [11];
    char srcip [16];
    char dstip [40];
    char reg_date [40];
    char log [1024];
    char image [1024];
    for(i=1; i<10; i++)
    {
        seq = i;
        score = i+i;
        total = (seq + score) * 10000;
        percentage = (float)score/total;
        ratio = (double)seq/total;
        sprintf(id, "id-%d", i);
        sprintf(srcip, "192.168.0.%d", i);
        sprintf(dstip, "2001:0DB8:0000:0000:0000:0000:1428:%04d", i);
        sprintf(reg_date, "2015-03-31 15:26:%02d", i);
        sprintf(log, "text log-%d", i);
        sprintf(image, "binary image-%d", i);
        memset(query, 0x00, sizeof(query));
        sprintf(query, "INSERT INTO CLI_SAMPLE1 VALUES(%d, %d, %ld, %f, %f, '%s', '%s', '%s',TO_DATE('%s','YYYY-MM-DD HH24:MI:SS'),'%s','%s')",
                seq, score, total, percentage, ratio, id, srcip, dstip, reg_date, log, image);
        prepareExecuteSQL(query);
        printf("%d record inserted\n", i);
    }
}

int main()
{
    connectDB();
    createTable();
    directInsert();
    selectTable();
    disconnectDB();
    return 0;
}
```
</div>
</details>


Makefile에 sample2_insert.c를 등록하고 컴파일하여 실행하면 다음과 같이 나옵니다.

```bash
[mach@localhost cli]$ make

[mach@localhost cli]$ ./sample2_insert

connected ...
1 record inserted
2 record inserted
3 record inserted
4 record inserted
5 record inserted
6 record inserted
7 record inserted
8 record inserted
9 record inserted
===== 0 ========
seq = 9, score = 18, total = 270000, percentage = 0.00, ratio = 3.3e-05, id = id-9, srcip = 192.168.0.9, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0009, regdate = 2015-03-31 15:26:09, log = text log-9, image = 62696E61727920696D6167652D39
===== 1 ========
seq = 8, score = 16, total = 240000, percentage = 0.00, ratio = 3.3e-05, id = id-8, srcip = 192.168.0.8, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0008, regdate = 2015-03-31 15:26:08, log = text log-8, image = 62696E61727920696D6167652D38
===== 2 ========
seq = 7, score = 14, total = 210000, percentage = 0.00, ratio = 3.3e-05, id = id-7, srcip = 192.168.0.7, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0007, regdate = 2015-03-31 15:26:07, log = text log-7, image = 62696E61727920696D6167652D37
===== 3 ========
seq = 6, score = 12, total = 180000, percentage = 0.00, ratio = 3.3e-05, id = id-6, srcip = 192.168.0.6, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0006, regdate = 2015-03-31 15:26:06, log = text log-6, image = 62696E61727920696D6167652D36
===== 4 ========
seq = 5, score = 10, total = 150000, percentage = 0.00, ratio = 3.3e-05, id = id-5, srcip = 192.168.0.5, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0005, regdate = 2015-03-31 15:26:05, log = text log-5, image = 62696E61727920696D6167652D35
===== 5 ========
seq = 4, score = 8, total = 120000, percentage = 0.00, ratio = 3.3e-05, id = id-4, srcip = 192.168.0.4, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0004, regdate = 2015-03-31 15:26:04, log = text log-4, image = 62696E61727920696D6167652D34
===== 6 ========
seq = 3, score = 6, total = 90000, percentage = 0.00, ratio = 3.3e-05, id = id-3, srcip = 192.168.0.3, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0003, regdate = 2015-03-31 15:26:03, log = text log-3, image = 62696E61727920696D6167652D33
===== 7 ========
seq = 2, score = 4, total = 60000, percentage = 0.00, ratio = 3.3e-05, id = id-2, srcip = 192.168.0.2, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0002, regdate = 2015-03-31 15:26:02, log = text log-2, image = 62696E61727920696D6167652D32
===== 8 ========
seq = 1, score = 2, total = 30000, percentage = 0.00, ratio = 3.3e-05, id = id-1, srcip = 192.168.0.1, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0001, regdate = 2015-03-31 15:26:01, log = text log-1, image = 62696E61727920696D6167652D31
```

### Prepare Execute 예제

데이터를 binding하여 INSERT하는 예제 프로그램을 작성해 보자.

마크베이스에서 데이터를 binding 하는 방식으로 값을 입력할수 있는데 이를 이용할시에는 데이터의 값들의 타입들을 명확히 지정해주고, 긴 문자열 타입들의 경우에는 길이 값을 반드시 지정해줘야 합니다.

아래의 예제를 통해서 각 타입별로 데이터를 binding하는 방법을 알수 있습니다.

파일명은 sample3_prepare.c 라고 합니다.

<details>
<summary>sample3_prepare.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>
#include <time.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB()
{
    char sConnStr[1024];

    SQLINTEGER sErrorNo;
    SQLSMALLINT sMsgLength;
    SQLCHAR sErrorMsg[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        printf("SQLAllocEnv error!!\n");
        exit(1);
    }

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        printf("SQLAllocConnect error!!\n");
        SQLFreeEnv(gEnv);
        exit(1);
    }

    sprintf(sConnStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)sConnStr,
                                       SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        printf("connection error\n");

        if (SQL_SUCCESS == SQLError ( gEnv, gCon, NULL, NULL, &sErrorNo,
                                      sErrorMsg, 1024, &sMsgLength ))
        {
            printf(" mach-%d : %s\n", sErrorNo, sErrorMsg);
        }
        SQLFreeEnv(gEnv);
        exit(1);
    }

    printf("connected ... \n");

}

void disconnectDB()
{
    SQLINTEGER sErrorNo;
    SQLSMALLINT sMsgLength;
    SQLCHAR sErrorMsg[1024];

    if (SQL_ERROR == SQLDisconnect(gCon)) {
        printf("disconnect error\n");

        if( SQL_SUCCESS == SQLError( gEnv, gCon, NULL, NULL, &sErrorNo,
                                     sErrorMsg, 1024, &sMsgLength ))
        {
            printf(" mach-%d : %s\n", sErrorNo, sErrorMsg);
        }
    }

    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg, SQLHSTMT aStmt)
{
    SQLINTEGER sErrorNo;
    SQLSMALLINT sMsgLength;
    SQLCHAR sErrorMsg[1024];

    printf("ERROR : (%s)\n", aMsg);

    if (SQL_SUCCESS == SQLError( gEnv, gCon, aStmt, NULL, &sErrorNo,
                                 sErrorMsg, 1024, &sMsgLength ))
    {
        printf(" mach-%d : %s\n", sErrorNo, sErrorMsg);
    }
    exit(-1);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT sStmt;

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error", sStmt);
    }

    if (SQLExecDirect(sStmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        printf("sql_exec_direct error[%s] \n", aSQL);
        outError("sql_exec_direct error", sStmt);
    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error", sStmt);
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE", 1);
    executeDirectSQL("CREATE TABLE CLI_SAMPLE(seq short, score integer, total long, percentage float, ratio double, id varchar(10), srcip ipv4, dstip ipv6, reg_date datetime, tlog text, image binary)", 0);
}

void selectTable()
{
    SQLHSTMT sStmt;
    const char *aSQL = "SELECT seq, score, total, percentage, ratio, id, srcip, dstip, reg_date, tlog, image FROM CLI_SAMPLE";

    int i=0;
    short sSeq;
    int sScore;
    long sTotal;
    float sPercentage;
    double sRatio;
    char sId [20];
    char sSrcIp[20];
    char sDstIp[50];
    SQL_TIMESTAMP_STRUCT sRegDate;
    char sLog [1024];
    char sImage[1024];
    SQL_LEN sLen;

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR) {
        outError("AllocStmt Error", sStmt);
    }

    if (SQLPrepare(sStmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR) {
        printf("Prepare error[%s] \n", aSQL);
        outError("Prepare error", sStmt);
    }

    if (SQLExecute(sStmt) == SQL_ERROR) {
        outError("prepared execute error", sStmt);
    }

    SQLBindCol(sStmt, 1, SQL_C_SSHORT, &sSeq, 0, &sLen);
    SQLBindCol(sStmt, 2, SQL_C_SLONG, &sScore, 0, &sLen);
    SQLBindCol(sStmt, 3, SQL_C_SBIGINT, &sTotal, 0, &sLen);
    SQLBindCol(sStmt, 4, SQL_C_FLOAT, &sPercentage, 0, &sLen);
    SQLBindCol(sStmt, 5, SQL_C_DOUBLE, &sRatio, 0, &sLen);
    SQLBindCol(sStmt, 6, SQL_C_CHAR, sId, sizeof(sId), &sLen);
    SQLBindCol(sStmt, 7, SQL_C_CHAR, sSrcIp, sizeof(sSrcIp), &sLen);
    SQLBindCol(sStmt, 8, SQL_C_CHAR, sDstIp, sizeof(sDstIp), &sLen);
    SQLBindCol(sStmt, 9, SQL_C_TYPE_TIMESTAMP, &sRegDate, 0, &sLen);
    SQLBindCol(sStmt, 10, SQL_C_CHAR, sLog, sizeof(sLog), &sLen);
    SQLBindCol(sStmt, 11, SQL_C_CHAR, sImage, sizeof(sImage), &sLen);

    while (SQLFetch(sStmt) == SQL_SUCCESS)
    {
        printf("===== %d ========\n", i++);
        printf("seq = %d", sSeq);
        printf(", score = %d", sScore);
        printf(", total = %ld", sTotal);
        printf(", percentage = %.2f", sPercentage);
        printf(", ratio = %g", sRatio);
        printf(", id = %s", sId);
        printf(", srcip = %s", sSrcIp);
        printf(", dstip = %s", sDstIp);
        printf(", regdate = %d-%02d-%02d %02d:%02d:%02d",
               sRegDate.year, sRegDate.month, sRegDate.day,
               sRegDate.hour, sRegDate.minute, sRegDate.second);
        printf(", log = %s", sLog);
        printf(", image = %s\n", sImage);
    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP))
    {
        outError("FreeStmt eror", sStmt);
    }
}

void prepareInsert()
{
    SQLHSTMT sStmt;
    int i;
    short sSeq;
    int sScore;
    long sTotal;
    float sPercentage;
    double sRatio;
    char sId [20];
    char sSrcIp [20];
    char sDstIp [50];
    long reg_date;
    char sLog [100];
    char sImage [100];
    int sLength[5];

    const char *sSQL = "INSERT INTO CLI_SAMPLE VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )";

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR)
    {
        outError("AllocStmt error", sStmt);
    }

    if (SQLPrepare(sStmt, (SQLCHAR *)sSQL, SQL_NTS) == SQL_ERROR)
    {
        printf("Prepare error[%s]\n", sSQL);
        outError("Prepare error", sStmt);
    }

    for(i=1; i<10; i++)
    {
        sSeq = i;
        sScore = i+i;
        sTotal = (sSeq + sScore) * 10000;
        sPercentage = (float)(sScore+2)/sScore;
        sRatio = (double)(sSeq+1)/sTotal;
        sprintf(sId, "id-%d", i);
        sprintf(sSrcIp, "192.168.0.%d", i);
        sprintf(sDstIp, "2001:0DB8:0000:0000:0000:0000:1428:%04x", i);
        reg_date = i*10000;
        sprintf(sLog, "log-%d", i);
        sprintf(sImage, "image-%d", i);

        if (SQLBindParameter(sStmt,
                             1,
                             SQL_PARAM_INPUT,
                             SQL_C_SSHORT,
                             SQL_SMALLINT,
                             0,
                             0,
                             &sSeq,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 1", sStmt);
        }

        if (SQLBindParameter(sStmt,
                             2,
                             SQL_PARAM_INPUT,
                             SQL_C_SLONG,
                             SQL_INTEGER,
                             0,
                             0,
                             &sScore,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 2", sStmt);
        }

        if (SQLBindParameter(sStmt,
                             3,
                             SQL_PARAM_INPUT,
                             SQL_C_SBIGINT,
                             SQL_BIGINT,
                             0,
                             0,
                             &sTotal,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 3", sStmt);
        }

        if (SQLBindParameter(sStmt,
                             4,
                             SQL_PARAM_INPUT,
                             SQL_C_FLOAT,
                             SQL_FLOAT,
                             0,
                             0,
                             &sPercentage,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 4", sStmt);
        }

        if (SQLBindParameter(sStmt,
                             5,
                             SQL_PARAM_INPUT,
                             SQL_C_DOUBLE,
                             SQL_DOUBLE,
                             0,
                             0,
                             &sRatio,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 5", sStmt);
        }

        sLength[0] = strlen(sId);
        if (SQLBindParameter(sStmt,
                             6,
                             SQL_PARAM_INPUT,
                             SQL_C_CHAR,
                             SQL_VARCHAR,
                             0,
                             0,
                             sId,
                             0,
                             (SQLLEN *)&sLength[0]) == SQL_ERROR)
        {
            outError("BindParameter error 6", sStmt);
        }

        sLength[1] = strlen(sSrcIp);
        if (SQLBindParameter(sStmt,
                             7,
                             SQL_PARAM_INPUT,
                             SQL_C_CHAR,
                             SQL_IPV4,
                             0,
                             0,
                             sSrcIp,
                             0,
                             (SQLLEN *)&sLength[1]) == SQL_ERROR)
        {
            outError("BindParameter error 7", sStmt);
        }

        sLength[2] = strlen(sDstIp);
        if (SQLBindParameter(sStmt,
                             8,
                             SQL_PARAM_INPUT,
                             SQL_C_CHAR,
                             SQL_IPV6,
                             0,
                             0,
                             sDstIp,
                             0,
                             (SQLLEN *)&sLength[2]) == SQL_ERROR)
        {
            outError("BindParameter error 8", sStmt);
        }

        if (SQLBindParameter(sStmt,
                             9,
                             SQL_PARAM_INPUT,
                             SQL_C_SBIGINT,
                             SQL_DATE,
                             0,
                             0,
                             &reg_date,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 9", sStmt);
        }

        sLength[3] = strlen(sLog);
        if (SQLBindParameter(sStmt,
                             10,
                             SQL_PARAM_INPUT,
                             SQL_C_CHAR,
                             SQL_VARCHAR,
                             0,
                             0,
                             sLog,
                             0,
                             (SQLLEN *)&sLength[3]) == SQL_ERROR)
        {
            outError("BindParameter error 10", sStmt);
        }

        sLength[4] = strlen(sImage);
        if (SQLBindParameter(sStmt,
                             11,
                             SQL_PARAM_INPUT,
                             SQL_C_CHAR,
                             SQL_BINARY,
                             0,
                             0,
                             sImage,
                             0,
                             (SQLLEN *)&sLength[4]) == SQL_ERROR)
        {
            outError("BindParameter error 11", sStmt);
        }

        if( SQLExecute(sStmt) == SQL_ERROR) {
            outError("prepare execute error", sStmt);
        }

        printf("%d prepared record inserted\n", i);

    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP)) {
        outError("FreeStmt", sStmt);
    }
}

int main()
{
    connectDB();
    createTable();
    prepareInsert();
    selectTable();
    disconnectDB();

    return 0;
}
```

</div>
</details>

Makefile에 sample3_prepare.c를 등록하고 컴파일하여 실행하면 다음과 같이 나옵니다.

``` bash
[mach@localhost cli]$ make

[mach@localhost cli]$ ./sample3_prepare

connected ...
1 prepared record inserted
2 prepared record inserted
3 prepared record inserted
4 prepared record inserted
5 prepared record inserted
6 prepared record inserted
7 prepared record inserted
8 prepared record inserted
9 prepared record inserted
===== 0 ========
seq = 9, score = 18, total = 270000, percentage = 1.11, ratio = 3.7037e-05, id = id-9, srcip = 192.168.0.9, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0009, regdate = 1970-01-01 09:00:00, log = log-9, image = 696D6167652D39
===== 1 ========
seq = 8, score = 16, total = 240000, percentage = 1.12, ratio = 3.75e-05, id = id-8, srcip = 192.168.0.8, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0008, regdate = 1970-01-01 09:00:00, log = log-8, image = 696D6167652D38
===== 2 ========
seq = 7, score = 14, total = 210000, percentage = 1.14, ratio = 3.80952e-05, id = id-7, srcip = 192.168.0.7, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0007, regdate = 1970-01-01 09:00:00, log = log-7, image = 696D6167652D37
===== 3 ========
seq = 6, score = 12, total = 180000, percentage = 1.17, ratio = 3.88889e-05, id = id-6, srcip = 192.168.0.6, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0006, regdate = 1970-01-01 09:00:00, log = log-6, image = 696D6167652D36
===== 4 ========
seq = 5, score = 10, total = 150000, percentage = 1.20, ratio = 4e-05, id = id-5, srcip = 192.168.0.5, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0005, regdate = 1970-01-01 09:00:00, log = log-5, image = 696D6167652D35
===== 5 ========
seq = 4, score = 8, total = 120000, percentage = 1.25, ratio = 4.16667e-05, id = id-4, srcip = 192.168.0.4, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0004, regdate = 1970-01-01 09:00:00, log = log-4, image = 696D6167652D34
===== 6 ========
seq = 3, score = 6, total = 90000, percentage = 1.33, ratio = 4.44444e-05, id = id-3, srcip = 192.168.0.3, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0003, regdate = 1970-01-01 09:00:00, log = log-3, image = 696D6167652D33
===== 7 ========
seq = 2, score = 4, total = 60000, percentage = 1.50, ratio = 5e-05, id = id-2, srcip = 192.168.0.2, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0002, regdate = 1970-01-01 09:00:00, log = log-2, image = 696D6167652D32
===== 8 ========
seq = 1, score = 2, total = 30000, percentage = 2.00, ratio = 6.66667e-05, id = id-1, srcip = 192.168.0.1, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0001, regdate = 1970-01-01 09:00:00, log = log-1, image = 696D6167652D31
```

### 확장 함수 Append 예제

마크베이스에서는 대량의 데이터를 파일로부터 읽어서 고속으로 입력하는 방법으로 Append 프로토콜을 제공하고 있습니다. 이 Append 프로토콜을 이용하는 예제 프로그램을 작성해 보자.

먼저 마크베이스에서 제공하는 다양한 타입별로 append 하는 방식의 예제를 살펴보자. Append 방식은 각 타입별로 편리하게 입력해 줄 수 있도록 각각의 설정값들이 정해져 있습니다. 그러므로 모든 방법별로 사용하는 입력하는 방식에 대한 숙지를 한다면 더욱더 효율적으로 프로그램을 작성할 수 있을 것입니다. 아래쪽에 있는 예제 코드에 그 방법들이 모두 나와 있습니다.

파일명은 sample4_append1.c 라고 합니다.


<details>
<summary>sample4_append1.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>
#include <arpa/inet.h>

#if __linux__
#include <sys/time.h>
#endif

#if defined(SUPPORT_STRUCT_TM)
## include <time.h>
#endif

#define MACHBASE_PORT_NO 5656
#define MAX_APPEND_COUNT 0xFFFFFFFF
#define ERROR_CHECK_COUNT 100

#define ERROR -1
#define SUCCESS 0

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB();
void disconnectDB();
void outError(const char *aMsg);
void executeDirectSQL(const char *aSQL, int aErrIgnore);
void createTable();
void appendOpen();
void appendData();
int appendClose();
time_t getTimeStamp();

int main()
{
    unsigned int sCount=0;
    time_t sStartTime, sEndTime;

    connectDB();
    createTable();

    appendOpen();
    sStartTime = getTimeStamp();
    appendData();
    sEndTime = getTimeStamp();
    appendClose();

    printf("timegap = %ld microseconds for %d records\n", sEndTime - sStartTime, sCount);
    printf("%.2f records/second\n", ((double)sCount/(double)(sEndTime - sStartTime))*1000000);

    disconnectDB();
    return SUCCESS;
}

void connectDB()
{
    char sConnStr[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        outError("SQLAllocEnv error!!");
    }

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        outError("SQLAllocConnect error!!");
    }

    sprintf(sConnStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)sConnStr, SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        outError("connection error\n");
    }

    if (SQL_ERROR == SQLAllocStmt(gCon, &gStmt) )
    {
        outError("AllocStmt error");
    }

    printf("connected ... \n");
}

void disconnectDB()
{
    if( SQL_ERROR == SQLFreeStmt(gStmt, SQL_DROP) )
    {
        outError("SQLFreeStmt error");
    }

    if (SQL_ERROR == SQLDisconnect(gCon)) {
        outError("disconnect error");
    }
    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg)
{
    SQLINTEGER sErrorNo;
    SQLSMALLINT sMsgLength;
    SQLCHAR sErrorMsg[1024];

    printf("ERROR : (%s)\n", aMsg);
    if (SQL_SUCCESS == SQLError( gEnv, gCon, gStmt, NULL, &sErrorNo,
                                 sErrorMsg, 1024, &sMsgLength ))
    {
        printf(" mach-%d : %s\n", sErrorNo, sErrorMsg);
    }

    if( gStmt )
    {
        SQLFreeStmt(gStmt, SQL_DROP);
    }

    if( gCon )
    {
        SQLFreeConnect( gCon );
    }

    if( gEnv )
    {
        SQLFreeEnv( gEnv );
    }
    exit(ERROR);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT sStmt;

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error");
    }

    if (SQLExecDirect(sStmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        printf("sql_exec_direct error[%s] \n", aSQL);
        outError("sql_exec_direct error");
    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error");
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE", 1);
    executeDirectSQL("CREATE TABLE CLI_SAMPLE(short1 short, integer1 integer, long1 long, float1 float, double1 double, datetime1 datetime, varchar1 varchar(10), ip ipv4, ip2 ipv6, text1 text, bin1 binary)", 0);
}

void appendOpen()
{
    const char *sTableName = "CLI_SAMPLE";

    if( SQLAppendOpen(gStmt, (SQLCHAR *)sTableName, ERROR_CHECK_COUNT) != SQL_SUCCESS )
    {
        outError("SQLAppendOpen error");
    }

    printf("append open ok\n");
}

void appendData()
{
    SQL_APPEND_PARAM sParam[11];
    char sVarchar[10] = {0, };
    char sText[100] = {0, };
    char sBinary[100] = {0, };

    memset(sParam, 0, sizeof(sParam));

    /* NULL FOR ALL*/
    /* fixed column */
    sParam[0].mShort = SQL_APPEND_SHORT_NULL;
    sParam[1].mInteger = SQL_APPEND_INTEGER_NULL;
    sParam[2].mLong = SQL_APPEND_LONG_NULL;
    sParam[3].mFloat = SQL_APPEND_FLOAT_NULL;
    sParam[4].mDouble = SQL_APPEND_DOUBLE_NULL;
    /* datetime */
    sParam[5].mDateTime.mTime = SQL_APPEND_DATETIME_NULL;
    /* varchar */
    sParam[6].mVarchar.mLength = SQL_APPEND_VARCHAR_NULL;
    /* ipv4 */
    sParam[7].mIP.mLength = SQL_APPEND_IP_NULL;
    /* ipv6 */
    sParam[8].mIP.mLength = SQL_APPEND_IP_NULL;
    /* text */
    sParam[9].mText.mLength = SQL_APPEND_TEXT_NULL;
    /* binary */
    sParam[10].mBinary.mLength = SQL_APPEND_BINARY_NULL;
    SQLAppendDataV2(gStmt, sParam);

    /* FIXED COLUMN Value */
    sParam[0].mShort = 2;
    sParam[1].mInteger = 4;
    sParam[2].mLong = 6;
    sParam[3].mFloat = 8.4;
    sParam[4].mDouble = 10.9;
    SQLAppendDataV2(gStmt, sParam);

    /* DATETIME : absolute value */
    sParam[5].mDateTime.mTime = MACHBASE_UINT64_LITERAL(1000000000);
    SQLAppendDataV2(gStmt, sParam);

    /* DATETIME : current */
    sParam[5].mDateTime.mTime = SQL_APPEND_DATETIME_NOW;
    SQLAppendDataV2(gStmt, sParam);

    /* DATETIME : string format*/
    sParam[5].mDateTime.mTime = SQL_APPEND_DATETIME_STRING;
    sParam[5].mDateTime.mDateStr = "23/May/2014:17:41:28";
    sParam[5].mDateTime.mFormatStr = "DD/MON/YYYY:HH24:MI:SS";
    SQLAppendDataV2(gStmt, sParam);

    /* DATETIME : struct tm format*/
    sParam[5].mDateTime.mTime = SQL_APPEND_DATETIME_STRUCT_TM;
    sParam[5].mDateTime.mTM.tm_year = 2000 - 1900;
    sParam[5].mDateTime.mTM.tm_mon = 11;
    sParam[5].mDateTime.mTM.tm_mday = 31;
    SQLAppendDataV2(gStmt, sParam);

    /* VARCHAR : string */
    strcpy(sVarchar, "MY VARCHAR");
    sParam[6].mVar.mLength = strlen(sVarchar);
    sParam[6].mVar.mData = sVarchar;
    SQLAppendDataV2(gStmt, sParam);

    /* IPv4 : ipv4 from binary bytes */
    sParam[7].mIP.mLength = SQL_APPEND_IP_IPV4;
    sParam[7].mIP.mAddr[0] = 127;
    sParam[7].mIP.mAddr[1] = 0;
    sParam[7].mIP.mAddr[2] = 0;
    sParam[7].mIP.mAddr[3] = 1;
    SQLAppendDataV2(gStmt, sParam);

    /* IPv4 : ipv4 from binary */
    sParam[7].mIP.mLength = SQL_APPEND_IP_IPV4;
    *(in_addr_t *)(sParam[7].mIP.mAddr) = inet_addr("192.168.0.1");
    SQLAppendDataV2(gStmt, sParam);

    /* IPv4 : ipv4 from string */
    sParam[7].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[7].mIP.mAddrString = "203.212.222.111";
    SQLAppendDataV2(gStmt, sParam);

    /* IPv6 : ipv6 from binary bytes */
    sParam[8].mIP.mLength = SQL_APPEND_IP_IPV6;
    sParam[8].mIP.mAddr[0] = 127;
    sParam[8].mIP.mAddr[1] = 127;
    sParam[8].mIP.mAddr[2] = 127;
    sParam[8].mIP.mAddr[3] = 127;
    sParam[8].mIP.mAddr[4] = 127;
    sParam[8].mIP.mAddr[5] = 127;
    sParam[8].mIP.mAddr[6] = 127;
    sParam[8].mIP.mAddr[7] = 127;
    sParam[8].mIP.mAddr[8] = 127;
    sParam[8].mIP.mAddr[9] = 127;
    sParam[8].mIP.mAddr[10] = 127;
    sParam[8].mIP.mAddr[11] = 127;
    sParam[8].mIP.mAddr[12] = 127;
    sParam[8].mIP.mAddr[13] = 127;
    sParam[8].mIP.mAddr[14] = 127;
    sParam[8].mIP.mAddr[15] = 127;
    SQLAppendDataV2(gStmt, sParam);
    sParam[8].mIP.mLength = SQL_APPEND_IP_NULL; /* recover */

    /* TEXT : string */
    memset(sText, 'X', sizeof(sText));
    sParam[9].mVar.mLength = 100;
    sParam[9].mVar.mData = sText;
    SQLAppendDataV2(gStmt, sParam);

    /* BINARY : datas */
    memset(sBinary, 0xFA, sizeof(sBinary));
    sParam[10].mVar.mLength = 100;
    sParam[10].mVar.mData = sBinary;
    SQLAppendDataV2(gStmt, sParam);
}

int appendClose()
{
    SQLBIGINT sSuccessCount = 0;
    SQLBIGINT sFailureCount = 0;

    if( SQLAppendClose(gStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        outError("SQLAppendClose error");
    }

    printf("append close ok\n");
    printf("success : %ld, failure : %ld\n", sSuccessCount, sFailureCount);
    return sSuccessCount;
}

time_t getTimeStamp()
{
#if _WIN32 || _WIN64

#if defined(_MSC_VER) || defined(_MSC_EXTENSIONS)
#define DELTA_EPOCH_IN_MICROSECS 11644473600000000Ui64
#else
#define DELTA_EPOCH_IN_MICROSECS 11644473600000000ULL
#endif
    FILETIME sFT;
    unsigned __int64 sTempResult = 0;

    GetSystemTimeAsFileTime(&sFT);

    sTempResult |= sFT.dwHighDateTime;
    sTempResult <<= 32;
    sTempResult |= sFT.dwLowDateTime;

    sTempResult -= DELTA_EPOCH_IN_MICROSECS;
    sTempResult /= 10;

    return sTempResult;
#else
    struct timeval sTimeVal;
    int sRet;

    sRet = gettimeofday(&sTimeVal, NULL);

    if (sRet == 0)
    {
        return (time_t)(sTimeVal.tv_sec * 1000000 + sTimeVal.tv_usec);
    }
    else
    {
        return 0;
    }
#endif
}
```

</div>
</details>

Makefile에 sample4_append1.c를 등록하고 컴파일하여 실행하면 다음과 같이 나옵니다.

```bash
[mach@localhost cli]$ make sample4_append1
gcc -c -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -I/home/mach/machbase_home/include -I. -L//home/mach/machbase_home/include -osample4_append1.o sample4_append1.c
gcc -m64 -mtune=k8 -L/home/mach/machbase_home/lib -osample4_append1 sample4_append1.o -lmachbasecli -L/home/mach/machbase_home/lib -lm -lpthread -ldl -lrt -rdynamic
[mach@localhost cli]$ ./sample4_append1
connected ...
append open ok
append close ok
success : 13, failure : 0
timegap = 48 microseconds for 13 records
270833.33 records/second
[mach@localhost cli]$

You can check what is inserted after MACH_SQL.

Mach> select * from CLI_SAMPLE;
SHORT1 INTEGER1 LONG1 FLOAT1 DOUBLE1
-----------------------------------------------------------------------------------------------------------
DATETIME1 VARCHAR1 IP IP2
------------------------------------------------------------------------------------------------------------------------------
TEXT1
------------------------------------------------------------------------------------
BIN1
------------------------------------------------------------------------------------
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 203.212.222.111 NULL
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXX
FAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFA
FAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFA
FAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFA
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 203.212.222.111 NULL
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXX
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 203.212.222.111 7F7F:7F7F:7F7F:7F7F:7F7F:7F7F:7F7F:7F7F
NULL
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 203.212.222.111 NULL
NULL
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 192.168.0.1 NULL
NULL
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 127.0.0.1 NULL
NULL
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR NULL NULL
NULL
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 NULL NULL NULL
NULL
NULL
2 4 6 8.4 10.9
2014-05-23 17:41:28 000:000:000 NULL NULL NULL
NULL
NULL
2 4 6 8.4 10.9
2015-04-09 16:44:11 134:256:000 NULL NULL NULL
NULL
NULL
2 4 6 8.4 10.9
1970-01-01 09:00:01 000:000:000 NULL NULL NULL
NULL
NULL
2 4 6 8.4 10.9
1970-01-01 09:00:00 000:000:000 NULL NULL NULL
NULL
NULL
[12] row(s) selected.
```

이제 파일을 이용해서 고속으로 append하는 방식을 사용해 보자. 실제로 업무에서 사용되는 많은 양의 로그, 패킷등의 값들을 고속으로 입력하는 데 유용한 예제입니다. 파일명은 sample4_append2.c 라고 합니다.

미리 입력할 데이터를 data.txt에 저장해 두어야 합니다.

```bash
./make_data
```

미리 주어진 make_data.c 를 수정하면 상황에 맞게 data.txt 파일을 생성할 수 있습니다.


<details>
<summary>make_data.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <machbase_sqlcli.h>

#define MACHBASE_PORT_NO 5656
#define MAX_APPEND_COUNT 0xFFFFFFFF
#define ERROR_CHECK_COUNT 100

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB();
void disconnectDB();
void outError(const char *aMsg);
void executeDirectSQL(const char *aSQL, int aErrIgnore);
void createTable();
void appendOpen();
int appendData();
void appendClose();
time_t getTimeStamp();

int main()
{
    unsigned int sCount=0;
    time_t sStartTime, sEndTime;

    connectDB();
    createTable();

    appendOpen();
    sStartTime = getTimeStamp();
    sCount = appendData();
    sEndTime = getTimeStamp();

    appendClose();

    printf("timegap = %ld microseconds for %d records\n", sEndTime - sStartTime, sCount);
    printf("%.2f records/second\n", ((double)sCount/(double)(sEndTime - sStartTime))*1000000);

    disconnectDB();

    return 0;
}

void connectDB()
{
    char sConnStr[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        outError("SQLAllocEnv error!!");
    }

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        outError("SQLAllocConnect error!!");
    }

    sprintf(sConnStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)sConnStr, SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        outError("connection error!!");
    }

    if( SQL_ERROR == SQLAllocStmt(gCon, &gStmt) )
    {
        outError("SQLAllocStmt error!!");
    }

    printf("connected ... \n");
}

void disconnectDB()
{
    if( SQL_ERROR == SQLFreeStmt(gStmt, SQL_DROP) )
    {
        outError("SQLFreeStmt error");
    }

    if (SQL_ERROR == SQLDisconnect(gCon)) {
        outError("disconnect error");
    }

    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg)
{
    SQLINTEGER sErrorNo;
    SQLSMALLINT sMsgLength;
    SQLCHAR sErrorMsg[1024];

    printf("ERROR : (%s)\n", aMsg);

    if (SQL_SUCCESS == SQLError( gEnv, gCon, gStmt, NULL, &sErrorNo,
                                 sErrorMsg, 1024, &sMsgLength ))
    {
        printf(" mach-%d : %s\n", sErrorNo, sErrorMsg);
    }

    if( gStmt )
    {
        SQLFreeStmt( gStmt, SQL_DROP );
    }
    if( gCon )
    {
        SQLFreeConnect( gCon );
    }
    if( gEnv )
    {
        SQLFreeEnv( gEnv );
    }
    exit(-1);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT sStmt;

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error");
    }

    if (SQLExecDirect(sStmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("sql_exec_direct error");
    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error");
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE", 1);
    executeDirectSQL("CREATE TABLE CLI_SAMPLE(seq short, score integer, total long, percentage float, ratio double, id varchar(10), srcip ipv4, dstip ipv6, reg_date datetime, tlog text, image binary)", 0);

    printf("table created\n");
}

void appendOpen()
{
    const char *sTableName = "CLI_SAMPLE";

    if( SQLAppendOpen(gStmt, (SQLCHAR *)sTableName, ERROR_CHECK_COUNT) != SQL_SUCCESS )
    {
        outError("SQLAppendOpen error!!");
    }

    printf("append open ok\n");
}

int appendData()
{
    FILE *sFp;
    char sBuf[1024];
    int j;
    char *sToken;
    unsigned int sCount=0;
    SQL_APPEND_PARAM sParam[11];

    sFp = fopen("data.txt", "r");
    if( !sFp )
    {
        printf("file open error\n");
        exit(-1);
    }

    printf("append data start\n");

    memset(sBuf, 0, sizeof(sBuf));

    while( fgets(sBuf, 1024, sFp ) != NULL )
    {
        if( strlen(sBuf) < 1)
        {
            break;
        }

        j=0;
        sToken = strtok(sBuf,",");

        while( sToken != NULL )
        {
            memset(sParam+j, 0, sizeof(sParam));
            switch(j){
                case 0 : sParam[j].mShort = atoi(sToken); break; //short
                case 1 : sParam[j].mInteger = atoi(sToken); break; //int
                case 2 : sParam[j].mLong = atol(sToken); break; //long
                case 3 : sParam[j].mFloat = atof(sToken); break; //float
                case 4 : sParam[j].mDouble = atof(sToken); break; //double
                case 5 : //string
                case 9 : //text
                case 10 : //binary
                         sParam[j].mVar.mLength = strlen(sToken);
                         strcpy(sParam[j].mVar.mData, sToken);
                         break;
                case 6 : //ipv4
                case 7 : //ipv6
                         sParam[j].mIP.mLength = SQL_APPEND_IP_STRING;
                         strcpy(sParam[j].mIP.mAddrString, sToken);
                         break;
                case 8 : //datetime
                         sParam[j].mDateTime.mTime = SQL_APPEND_DATETIME_STRING;
                         strcpy(sParam[j].mDateTime.mDateStr, sToken);
                         sParam[j].mDateTime.mFormatStr = "DD/MON/YYYY:HH24:MI:SS";
                         break;
            }

            sToken = strtok(NULL, ",");

            j++;
        }
        if( SQLAppendDataV2(gStmt, sParam) != SQL_SUCCESS )
        {
            printf("SQLAppendData error\n");
            return 0;
        }
        if ( ((sCount++) % 10000) == 0)
        {
            printf(".");
        }

        if( ((sCount) % 100) == 0 )
        {
            if( SQLAppendFlush( gStmt ) != SQL_SUCCESS )
            {
                outError("SQLAppendFlush error");
            }
        }
        if (sCount == MAX_APPEND_COUNT)
        {
            break;
        }
    }

    printf("\nappend data end\n");

    fclose(sFp);

    return sCount;
}

void appendClose()
{
    SQLBIGINT sSuccessCount = 0;
    SQLBIGINT sFailureCount = 0;

    if( SQLAppendClose(gStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        outError("SQLAppendClose error");
    }

    printf("append close ok\n");
    printf("success : %ld, failure : %ld\n", sSuccessCount, sFailureCount);
}

time_t getTimeStamp()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec*1000000+tv.tv_usec;
}
```

</div>
</details>

Makefile에 sample4_append2.c를 등록하고 컴파일하여 실행하면 다음과 같이 나옵니다.

```bash
[mach@localhost cli]$ make
gcc -c -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -I/home/mach/machbase_home/include -I. -L//home/mach/machbase_home/include -osample4_append2.o sample4_append2.c
gcc -m64 -mtune=k8 -L/home/mach/machbase_home/lib -osample4_append2 sample4_append2.o -lmachbasecli -L/home/mach/machbase_home/lib -lm -lpthread -ldl -lrt -rdynamic
[mach@localhost cli]$ ./sample4_append2
connected ...
table created
append open ok
append data start
....................................................................................................
append data end
append close ok
success : 1000000, failure : 0
timegap = 1641503 microseconds for 1000000 records
609197.79 records/second
```

### 테이블 열 정보 획득 예제

테이블 열 정보를 획득하는 방법은 다양하지만 그중에 SQLDescribeCol과 SQLColumns를 이용한 방법을 살펴봅니다.

#### SQLDescribeCol

SQLDescribeCol은 테이블 열의 번호, 이름, 버퍼 크기, 길이, 타입 등을 가져오는 함수로 이를 이용해서 데이터베이스 내부에서 원하는 내용을 손쉽게 가져올수 있습니다.

예제 파일명은 sample5_describe.c 라고 합니다.


<details>
<summary>sample5_describe.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>
#include <time.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB()
{
    char connStr[1024];

    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        printf("SQLAllocEnv error!!\n");
        exit(1);
    }

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        printf("SQLAllocConnect error!!\n");
        SQLFreeEnv(gEnv);
        exit(1);
    }

    sprintf(connStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)connStr,
                                       SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        printf("connection error\n");

        if (SQL_SUCCESS == SQLError ( gEnv, gCon, NULL, NULL, &errNo,
                                      errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
        SQLFreeEnv(gEnv);
        exit(1);
    }

    if (SQLAllocStmt(gCon, &gStmt) == SQL_ERROR)
    {
        outError("AllocStmt error", gStmt);
    }

    printf("connected ... \n");

}

void disconnectDB()
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLDisconnect(gCon)) {
        printf("disconnect error\n");

        if( SQL_SUCCESS == SQLError( gEnv, gCon, NULL, NULL, &errNo,
                                     errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
    }

    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg, SQLHSTMT stmt)
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    printf("ERROR : (%s)\n", aMsg);

    if (SQL_SUCCESS == SQLError( gEnv, gCon, stmt, NULL, &errNo,
                                 errMsg, 1024, &msgLength ))
    {
        printf(" mach-%d : %s\n", errNo, errMsg);
    }
    exit(-1);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT stmt;

    if (SQLAllocStmt(gCon, &stmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error", stmt);
    }

    if (SQLExecDirect(stmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        printf("sql_exec_direct error[%s] \n", aSQL);
        outError("sql_exec_direct error", stmt);
    }

    if (SQL_ERROR == SQLFreeStmt(stmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error", stmt);
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE", 1);
    executeDirectSQL("CREATE TABLE CLI_SAMPLE(seq short, score integer, total long, percentage float, ratio double, id varchar(10), srcip ipv4, dstip ipv6, reg_date datetime, tlog text, image binary)", 0);

}

int main()
{
    char sSqlStr[] = "select * from cli_sample";
    SQLCHAR sColName[32];
    SQLSMALLINT sColType;
    SQLSMALLINT sColNameLen;
    SQLSMALLINT sNullable;
    SQLULEN sColLen;
    SQLSMALLINT sDecimalDigits;
    SQLLEN sOutlen;
    SQLCHAR* sData;
    SQLLEN sDisplaySize;
    int i;

    SQLSMALLINT sColumns;

    connectDB();

    createTable();

    if(SQLPrepare(gStmt, (SQLCHAR*)sSqlStr, SQL_NTS))
    {
        outError("sql prepare fail", gStmt);
        return -1;
    }

    if(SQLNumResultCols(gStmt, &sColumns) != SQL_SUCCESS )
    {
        printf("get col length error \n");
        return -1;
    }

    printf("----------------------------------------------------------------\n");
    printf("%32s%16s%10s\n","Name","Type","Length");
    printf("----------------------------------------------------------------\n");

    for(i = 0; i < sColumns; i++)
    {
        SQLDescribeCol(gStmt,
                       (SQLUSMALLINT)(i + 1),
                       sColName,
                       sizeof(sColName),
                       &sColNameLen,
                       &sColType,
                       (SQLULEN *)&sColLen,
                       &sDecimalDigits,
                       (SQLSMALLINT *)&sNullable);

        printf("%32s%16d%10d\n",sColName, sColType, sColLen);
    }

    printf("----------------------------------------------------------------\n");

    disconnectDB();

    return 0;
}
```

</div>
</details>

위의 파일을 추가하고 make를 실행하면 아래와 같이 원하는 열의 내용들이 나타나는 것을 볼 수 있습니다.

```bash
[mach@localhost cli]$ make

[mach@localhost cli]$ ./sample5_describe
connected ...
----------------------------------------------------------------
Name Type Length
----------------------------------------------------------------
SEQ 5 5
SCORE 4 10
TOTAL -5 19
PERCENTAGE 6 27
RATIO 8 27
ID 12 10
SRCIP 2104 15
DSTIP 2106 60
REG_DATE 9 31
TLOG 2100 67108864
IMAGE -2 67108864
----------------------------------------------------------------
[mach@localhost cli]$
```

#### SQLColumns

SQLColumns은 현재 테이블 내에 존재하는 컬럼들의 정보를 알아낼 수 있는 함수입니다. 마크베이스에서도 위와 같은 함수를 지원하고 있으며 이를 이용하여 컬럼 각각의 정보들을 알아낼 수 있습니다.

파일이름은 sample6_columns.c라고 합니다.


<details>
<summary>sample6_columns.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>

#include <time.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB()
{
    char connStr[1024];

    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        printf("SQLAllocEnv error!!\n");
        exit(1);
    }

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        printf("SQLAllocConnect error!!\n");
        SQLFreeEnv(gEnv);
        exit(1);
    }

    sprintf(connStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)connStr,
                                       SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        printf("connection error\n");

        if (SQL_SUCCESS == SQLError ( gEnv, gCon, NULL, NULL, &errNo,
                                      errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
        SQLFreeEnv(gEnv);
        exit(1);
    }

    if (SQLAllocStmt(gCon, &gStmt) == SQL_ERROR)
    {
        outError("AllocStmt error", gStmt);
    }

    printf("connected ... \n");

}

void disconnectDB()
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLDisconnect(gCon)) {
        printf("disconnect error\n");

        if( SQL_SUCCESS == SQLError( gEnv, gCon, NULL, NULL, &errNo,
                                     errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
    }

    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg, SQLHSTMT stmt)
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    printf("ERROR : (%s)\n", aMsg);

    if (SQL_SUCCESS == SQLError( gEnv, gCon, stmt, NULL, &errNo,
                                 errMsg, 1024, &msgLength ))
    {
        printf(" mach-%d : %s\n", errNo, errMsg);
    }
    exit(-1);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT stmt;

    if (SQLAllocStmt(gCon, &stmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error", stmt);
    }

    if (SQLExecDirect(stmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        printf("sql_exec_direct error[%s] \n", aSQL);
        outError("sql_exec_direct error", stmt);
    }

    if (SQL_ERROR == SQLFreeStmt(stmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error", stmt);
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE", 1);
    executeDirectSQL("CREATE TABLE CLI_SAMPLE(seq short, score integer, total long, percentage float, ratio double, id varchar(10), srcip ipv4, dstip ipv6, reg_date datetime, tlog text, image binary)", 0);
}

int main()
{
    SQLCHAR sColName[32];
    SQLSMALLINT sColType;
    SQLCHAR sColTypeName[16];
    SQLSMALLINT sColNameLen;
    SQLSMALLINT sColTypeLen;
    SQLSMALLINT sNullable;
    SQLULEN sColLen;
    SQLSMALLINT sDecimalDigits;
    SQLLEN sOutlen;
    SQLCHAR* sData;
    SQLLEN sDisplaySize;
    int i;

    SQLSMALLINT sColumns;

    connectDB();

    createTable();

    if(SQLColumns(gStmt, NULL, 0, NULL, 0, "cli_sample", SQL_NTS, NULL, 0) != SQL_SUCCESS)
    {
        printf("sql columns error!\n");
        return -1;
    }

    SQLBindCol(gStmt, 4, SQL_C_CHAR, sColName, sizeof(sColName), &sColNameLen);
    SQLBindCol(gStmt, 5, SQL_C_SSHORT, &sColType, 0, &sColTypeLen);
    SQLBindCol(gStmt, 6, SQL_C_CHAR, sColTypeName, sizeof(sColTypeName), NULL);
    SQLBindCol(gStmt, 7, SQL_C_SLONG, &sColLen, 0, NULL);

    printf("--------------------------------------------------------------------------------\n");
    printf("%32s%16s%16s%10s\n","Name","Type","TypeName","Length");
    printf("--------------------------------------------------------------------------------\n");

    while( SQLFetch(gStmt) != SQL_NO_DATA )
    {
        printf("%32s%16d%16s%10d\n",sColName, sColType, sColTypeName, sColLen);
    }
    printf("--------------------------------------------------------------------------------\n");

    disconnectDB();

    return 0;
}
```

</div>
</details>

위의 파일을 추가하고 make를 실행합니다. 결과는 다음과 같습니다.

```bash
[mach@localhost cli]$ make

[mach@localhost cli]$ ./sample6_columns
connected ...
--------------------------------------------------------------------------------
Name Type TypeName Length
--------------------------------------------------------------------------------
_ARRIVAL_TIME 93 DATE 31
SEQ 5 SMALLINT 5
SCORE 4 INTEGER 10
TOTAL -5 BIGINT 19
PERCENTAGE 6 FLOAT 27
RATIO 8 DOUBLE 27
ID 12 VARCHAR 10
SRCIP 2104 IPV4 15
DSTIP 2106 IPV6 60
REG_DATE 93 DATE 31
TLOG 2100 TEXT 67108864
IMAGE -2 BINARY 67108864
--------------------------------------------------------------------------------
```


## 멀티 쓰레드 append 예제

하나의 프로그램에서 여러 스레드를 이용해 여러 테이블에 append하는 예제입니다.

파일 이름은 sample8_multi_session_multi_table.c로 합니다.


<details>
<summary>sample8_multi_session_multi_table.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <machbase_sqlcli.h>

#define MACHBASE_PORT_NO       5656
#define ERROR_CHECK_COUNT   100

#define LOG_FILE_CNT        3
#define MAX_THREAD_NUM      LOG_FILE_CNT

#define RC_FAILURE          -1
#define RC_SUCCESS          0

#define UNUSED(aVar) do { (void)(aVar); } while(0)

char *gTableName[LOG_FILE_CNT] = {"table_f1", "table_f2", "table_event"};
char *gFileName[LOG_FILE_CNT] =  {"suffle_data1.txt","suffle_data2.txt","suffle_data3.txt"};

void printError(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char *aMsg);
int connectDB(SQLHENV *aEnv, SQLHDBC *aCon);
void disconnectDB(SQLHENV aEnv, SQLHDBC aCon);
int executeDirectSQL(SQLHENV aEnv, SQLHDBC aCon, const char *aSQL, int aErrIgnore);
int appendOpen(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char* aTableName);
int appendClose(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt);
int createTables(SQLHENV aEnv, SQLHDBC aCon);

/*
 * error code returned from CLI lib
 */
void printError(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char *aMsg)
{
    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;

    if( aMsg != NULL )
    {
        printf("%s\n", aMsg);
    }

    if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                 sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) == SQL_SUCCESS )
    {
        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);
    }
}

/*
 * error code returned from Machbase server
 */

void appendDumpError(SQLHSTMT    aStmt,
                     SQLINTEGER  aErrorCode,
                     SQLPOINTER  aErrorMessage,
                     SQLLEN      aErrorBufLen,
                     SQLPOINTER  aRowBuf,
                     SQLLEN      aRowBufLen)
{
    char       sErrMsg[1024] = {0, };
    char       sRowMsg[32 * 1024] = {0, };

    UNUSED(aStmt);

    if (aErrorMessage != NULL)
    {
        strncpy(sErrMsg, (char *)aErrorMessage, aErrorBufLen);
    }

    if (aRowBuf != NULL)
    {
        strncpy(sRowMsg, (char *)aRowBuf, aRowBufLen);
    }

    fprintf(stdout, "Append Error : [%d][%s]\n[%s]\n\n", aErrorCode, sErrMsg, sRowMsg);
}


int connectDB(SQLHENV *aEnv, SQLHDBC *aCon)
{
    char sConnStr[1024];

    if( SQLAllocEnv(aEnv) != SQL_SUCCESS )
    {
        printf("SQLAllocEnv error\n");
        return RC_FAILURE;
    }

    if( SQLAllocConnect(*aEnv, aCon) != SQL_SUCCESS )
    {
        printf("SQLAllocConnect error\n");

        SQLFreeEnv(*aEnv);
        *aEnv = SQL_NULL_HENV;

        return RC_FAILURE;
    }

    sprintf(sConnStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if( SQLDriverConnect( *aCon, NULL,
                          (SQLCHAR *)sConnStr,
                          SQL_NTS,
                          NULL, 0, NULL,
                          SQL_DRIVER_NOPROMPT ) != SQL_SUCCESS
      )
    {

        printError(*aEnv, *aCon, NULL, "SQLDriverConnect error");

        SQLFreeConnect(*aCon);
        *aCon = SQL_NULL_HDBC;

        SQLFreeEnv(*aEnv);
        *aEnv = SQL_NULL_HENV;

        return RC_FAILURE;
    }

    return RC_SUCCESS;
}


void disconnectDB(SQLHENV aEnv, SQLHDBC aCon)
{
    if( SQLDisconnect(aCon) != SQL_SUCCESS )
    {
        printError(aEnv, aCon, NULL, "SQLDisconnect error");
    }

    SQLFreeConnect(aCon);
    aCon = SQL_NULL_HDBC;

    SQLFreeEnv(aEnv);
    aEnv = SQL_NULL_HENV;
}


int executeDirectSQL(SQLHENV aEnv, SQLHDBC aCon, const char *aSQL, int aErrIgnore)
{
    SQLHSTMT sStmt = SQL_NULL_HSTMT;

    if( SQLAllocStmt(aCon, &sStmt) != SQL_SUCCESS )
    {
        if( aErrIgnore == 0 )
        {
            printError(aEnv, aCon, sStmt, "SQLAllocStmt Error");
            return RC_FAILURE;
        }
    }

    if( SQLExecDirect(sStmt, (SQLCHAR *)aSQL, SQL_NTS) != SQL_SUCCESS )
    {

        if( aErrIgnore == 0 )
        {
            printError(aEnv, aCon, sStmt, "SQLExecDirect Error");

            SQLFreeStmt(sStmt,SQL_DROP);
            sStmt = SQL_NULL_HSTMT;
            return RC_FAILURE;
        }
    }

    if( SQLFreeStmt(sStmt, SQL_DROP) != SQL_SUCCESS )
    {
        if (aErrIgnore == 0)
        {
            printError(aEnv, aCon, sStmt, "SQLFreeStmt Error");
            sStmt = SQL_NULL_HSTMT;
            return RC_FAILURE;
        }
    }
    sStmt = SQL_NULL_HSTMT;

    return RC_SUCCESS;
}


int appendOpen(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char* aTableName)
{
    if( aTableName == NULL )
    {
        printf("append open wrong table name");
        return RC_FAILURE;
    }

    if( SQLAppendOpen(aStmt, (SQLCHAR *)aTableName, ERROR_CHECK_COUNT) != SQL_SUCCESS )
    {
        printError(aEnv, aCon, aStmt, "SQLAppendOpen error");
        return RC_FAILURE;
    }
    return RC_SUCCESS;
}


int appendClose(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt)
{
    SQLBIGINT sSuccessCount = 0;
    SQLBIGINT sFailureCount = 0;

    if( SQLAppendClose(aStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        printError(aEnv, aCon, aStmt, "SQLAppendClose error");
        return RC_FAILURE;
    }

    printf("append result success : %ld, failure : %ld\n", sSuccessCount, sFailureCount);

    return RC_SUCCESS;
}


int createTables(SQLHENV aEnv, SQLHDBC aCon)
{
    int      i;
    char    *sSchema[] = { "srcip1 ipv4, srcip2 ipv6, srcport short, dstip1 ipv4, dstip2 ipv6, dstport short, data1 long, data2 long",
        "srcip1 ipv4, srcip2 ipv6, srcport short, dstip1 ipv4, dstip2 ipv6, dstport short, data1 long, data2 long",
        "machine ipv4, err integer, msg varchar(30)"
    };

    char sDropQuery[256];
    char sCreateQuery[256];

    for(i = 0; i < LOG_FILE_CNT; i++)
    {
        snprintf(sDropQuery, 256, "DROP TABLE %s", gTableName[i]);
        snprintf(sCreateQuery, 256, "CREATE TABLE %s ( %s )", gTableName[i], sSchema[i]);

        executeDirectSQL(aEnv, aCon, sDropQuery, 1);
        executeDirectSQL(aEnv, aCon, sCreateQuery, 0);
    }

    return RC_SUCCESS;
}


int appendF1(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, FILE *aFp)
{
    SQL_APPEND_PARAM sParam[8];
    SQLRETURN        sRC;

    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;

    char             sData[4][64];

    memset(sParam, 0, sizeof(sParam));

    fscanf(aFp, "%s %s %hd %s %s %hd %lld %lld\n",
           sData[0], sData[1], &sParam[2].mShort,
           sData[2], sData[3], &sParam[5].mShort,
           &sParam[6].mLong, &sParam[7].mLong);

    sParam[0].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = sData[0];

    sParam[1].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[1].mIP.mAddrString = sData[1];

    sParam[3].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[3].mIP.mAddrString = sData[2];

    sParam[4].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[4].mIP.mAddrString = sData[3];

    sRC = SQLAppendDataV2(aStmt, sParam);
    if( !SQL_SUCCEEDED(sRC) )
    {
        if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                     sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) != SQL_SUCCESS )
        {
            return RC_FAILURE;
        }

        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);

        if( sNativeError != 9604 &&
            sNativeError != 9605 &&
            sNativeError != 9606 )
        {
            return RC_FAILURE;
        }
        else
        {
            //data value error in one record, so return success to keep attending
        }
    }
    return RC_SUCCESS;
}


int appendF2(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, FILE* aFp)
{
    SQL_APPEND_PARAM sParam[8];
    SQLRETURN        sRC;

    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;

    char             sData[4][64];

    memset(sParam, 0, sizeof(sParam));

    fscanf(aFp, "%s %s %hd %s %s %hd %lld %lld\n",
           sData[0], sData[1], &sParam[2].mShort,
           sData[2], sData[3], &sParam[5].mShort,
           &sParam[6].mLong, &sParam[7].mLong);

    sParam[0].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = sData[0];

    sParam[1].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[1].mIP.mAddrString = sData[1];

    sParam[3].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[3].mIP.mAddrString = sData[2];

    sParam[4].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[4].mIP.mAddrString = sData[3];

    sRC = SQLAppendDataV2(aStmt, sParam);
    if( !SQL_SUCCEEDED(sRC) )
    {
        if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                     sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) != SQL_SUCCESS )
        {
            return RC_FAILURE;
        }

        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);

        if( sNativeError != 9604 &&
            sNativeError != 9605 &&
            sNativeError != 9606 )
        {
            return RC_FAILURE;
        }
        else
        {
            //data value error in one record, so return success to keep attending
        }
    }
    return RC_SUCCESS;
}


int appendEvent(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, FILE* aFp)
{
    SQL_APPEND_PARAM sParam[3];
    SQLRETURN        sRC;

    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;

    char             sData[2][20];

    memset(sParam, 0, sizeof(sParam));

    fscanf(aFp, "%s %d %s\n",sData[0], &sParam[1].mInteger, sData[1]);

    sParam[0].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = sData[0];

    sParam[2].mVarchar.mLength = strlen(sData[1]);
    sParam[2].mVarchar.mData = sData[1];

    sRC = SQLAppendDataV2(aStmt, sParam);
    if( !SQL_SUCCEEDED(sRC) )
    {
        if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                     sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) != SQL_SUCCESS )
        {
            return RC_FAILURE;
        }

        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);

        if( sNativeError != 9604 &&
            sNativeError != 9605 &&
            sNativeError != 9606 )
        {
            return RC_FAILURE;
        }
        else
        {
            //data value error in one record, so return success to keep attending
        }
    }
    return RC_SUCCESS;
}


void *eachThread(void *aIdx)
{
    SQLHENV    sEnv = SQL_NULL_HENV;
    SQLHDBC    sCon = SQL_NULL_HDBC;
    SQLHSTMT   sStmt[LOG_FILE_CNT] = {SQL_NULL_HSTMT,};

    FILE*      sFp;
    int        i;
    int        sLogType;

    int        sThrNo = *(int *)aIdx;

    // Alloc ENV and DBC
    if( connectDB(&sEnv, &sCon) == RC_SUCCESS )
    {
        printf("[%d]connectDB success.\n", sThrNo);
    }
    else
    {
        printf("[%d]connectDB failure.\n", sThrNo);
        goto error;
    }

    // set timed flush true
    if( SQLSetConnectAppendFlush(sCon, 1) != SQL_SUCCESS )
    {
        printError(sEnv, sCon, NULL, "SQLSetConnectAppendFlush Error");
        goto error;
    }

    for( i = 0; i < LOG_FILE_CNT; i++ )
    {
        // Alloc stmt
        if( SQLAllocStmt(sCon,&sStmt[i]) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLAllocStmt Error");
            goto error;
        }

        if( appendOpen(sEnv, sCon, sStmt[i], gTableName[i]) == RC_FAILURE )
        {
            printError(sEnv, sCon, sStmt[i], "SQLAppendOpen Error");
            goto error;
        }
        else
        {
            printf("[%d-%d]appendOpen success.\n", sThrNo, i);
        }

        if( SQLAppendSetErrorCallback(sStmt[i], appendDumpError) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLAppendSetErrorCallback Error");
            goto error;
        }

        // set timed flush interval as 2 seconds
        if( SQLSetStmtAppendInterval(sStmt[i], 2000) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLSetStmtAppendInterval Error");
            goto error;
        }
    }

    sFp = fopen((char*)gFileName[sThrNo], "rt");
    if( sFp == NULL )
    {
        printf("file open error - [%d][%s]\n", sThrNo, gFileName[sThrNo]);
    }
    else
    {
        printf("file open success - [%d][%s]\n", sThrNo, gFileName[sThrNo]);

        for( i = 0; !feof(sFp); i++ )
        {
            fscanf(sFp, "%d ", &sLogType);
            switch(sLogType)
            {
                case 1://f1
                    if( appendF1(sEnv, sCon, sStmt[0], sFp) == RC_FAILURE )
                    {
                        goto error;
                    }
                    break;
                case 2://f2
                    if( appendF2(sEnv, sCon, sStmt[1],sFp) == RC_FAILURE )
                    {
                        goto error;
                    }
                    break;
                case 3://event
                    if(appendEvent(sEnv, sCon, sStmt[2], sFp) == RC_FAILURE )
                    {
                        goto error;
                    }
                    break;
                default:
                    printf("unknown type error\n");
                    break;
            }

            if( (i%10000) == 0 )
            {
                fprintf(stdout, ".");
                fflush(stdout);
            }
        }
        printf("\n");

        fclose(sFp);
    }

    for( i = 0; i < LOG_FILE_CNT; i++)
    {
        printf("[%d-%d]appendClose start...\n", sThrNo, i);
        if( appendClose(sEnv, sCon, sStmt[i]) == RC_FAILURE )
        {
            printf("[%d-%d]appendClose failure\n", sThrNo, i);
        }
        else
        {
            printf("[%d-%d]appendClose success\n", sThrNo, i);
        }

        if( SQLFreeStmt(sStmt[i], SQL_DROP) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLFreeStmt Error");
        }
        sStmt[i] = SQL_NULL_HSTMT;
    }

    disconnectDB(sEnv, sCon);

    printf("[%d]disconnected.\n", sThrNo);

    pthread_exit(NULL);

error:
    for( i = 0; i < LOG_FILE_CNT; i++)
    {
        if( sStmt[i] != SQL_NULL_HSTMT )
        {
            appendClose(sEnv, sCon, sStmt[i]);

            if( SQLFreeStmt(sStmt[i], SQL_DROP) != SQL_SUCCESS )
            {
                printError(sEnv, sCon, sStmt[i], "SQLFreeStmt Error");
            }
            sStmt[i] = SQL_NULL_HSTMT;
        }
    }

    if( sCon != SQL_NULL_HDBC )
    {
        disconnectDB(sEnv, sCon);
    }

    pthread_exit(NULL);
}


int initTables()
{
    SQLHENV     sEnv  = SQL_NULL_HENV;
    SQLHDBC     sCon  = SQL_NULL_HDBC;

    if( connectDB(&sEnv, &sCon) == RC_SUCCESS )
    {
        printf("connectDB success.\n");
    }
    else
    {
        printf("connectDB failure.\n");
        goto error;
    }

    if( createTables(sEnv, sCon) == RC_SUCCESS )
    {
        printf("createTables success.\n");
    }
    else
    {
        printf("createTables failure.\n");
        goto error;
    }

    disconnectDB(sEnv, sCon);

    return RC_SUCCESS;

error:

    if( sCon != SQL_NULL_HDBC )
    {
        disconnectDB(sEnv, sCon);
    }

    return RC_FAILURE;
}


int main()
{
    pthread_t sThread[MAX_THREAD_NUM];
    int       sNum[MAX_THREAD_NUM];
    int       sRC;
    int       i;

    initTables();

    //
    //eachThread has own ENV,DBC and STMT
    //
    for(i = 0; i < MAX_THREAD_NUM; i++)
    {
        sNum[i] = i;

        sRC = pthread_create(&sThread[i], NULL, (void *)eachThread, (void*)&sNum[i]);
        if ( sRC != RC_SUCCESS )
        {
            printf("Error in Thread create[%d] : %d\n", i, sRC);
            return RC_FAILURE;
        }
    }

    for(i = 0; i < MAX_THREAD_NUM; i++)
    {
        sRC = pthread_join(sThread[i], NULL);
        if( sRC != RC_SUCCESS )
        {
            printf("Error in Thread[%d] : %d\n", i, sRC);
            return RC_FAILURE;
        }
        printf("%d thread join\n", i+1);
    }

    return RC_SUCCESS;
}
```

</div>
</details>

make 코드를 추가하고 실행 파일을 실행해 봅니다. 쓰레드를 이용하므로 출력 순서가 다를 수 있습니다. 실행 결과는 다음과 같습니다.

```bash
[mach@localhost cli]$ make sample8_multi_session_multi_table
gcc -c -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -I/home/mach/machbase_home/include -I. -L//home/mach/machbase_home/include -osample8_multi_session_multi_table.o sample8_multi_session_multi_table.c
gcc -m64 -mtune=k8 -L/home/mach/machbase_home/lib -osample8_multi_session_multi_table sample8_multi_session_multi_table.o -lmachbasecli  -L/home/mach/machbase_home/lib -lm -lpthread -ldl -lrt -rdynamic
[mach@localhost cli]$ ./sample8_multi_session_multi_table
connectDB success.
createTables success.
[0]connectDB success.
[1]connectDB success.
[2]connectDB success.
[1-0]appendOpen success.
[0-0]appendOpen success.
[2-0]appendOpen success.
[1-1]appendOpen success.
[2-1]appendOpen success.
[0-1]appendOpen success.
[1-2]appendOpen success.
[2-2]appendOpen success.
file open success - [1][suffle_data2.txt]
file open success - [2][suffle_data3.txt]
[0-2]appendOpen success.
file open success - [0][suffle_data1.txt]
.......................................................................................

[1-0]appendClose start...
..
[0-0]appendClose start...
append result success : 100000, failure : 0
[1-0]appendClose success
[1-1]appendClose start...
append result success : 100000, failure : 0
[1-1]appendClose success
[1-2]appendClose start...
append result success : 100000, failure : 0
[1-2]appendClose success
append result success : 100000, failure : 0
[0-0]appendClose success
[0-1]appendClose start...
.append result success : 100000, failure : 0
[0-1]appendClose success
[0-2]appendClose start...
append result success : 100000, failure : 0
[0-2]appendClose success

[2-0]appendClose start...
append result success : 100000, failure : 0
[2-0]appendClose success
[2-1]appendClose start...
append result success : 100000, failure : 0
[2-1]appendClose success
[2-2]appendClose start...
append result success : 100000, failure : 0
[2-2]appendClose success
[1]disconnected.
[2]disconnected.
[0]disconnected.
1 thread join
2 thread join
3 thread join
```

machsql을 통해 아래와 같이 결과를 확인할 수 있습니다.

```bash
[mach@localhost cli]$ machsql


=================================================================
     Machbase Client Query Utility
     Release Version 8.5.4.develop
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved.
=================================================================
Machbase Server Addr (Default:127.0.0.1) :
Machbase User ID  (Default:SYS)
Machbase User Password : manager
MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
Mach> select count(*) from table_f1;
count(*)
-----------------------
300000
[1] Row Selected.
Mach> select count(*) from table_f2;
count(*)
-----------------------
300000
[1] row(s) selected.
Mach> select count(*) from table_event;
count(*)
-----------------------
300000
[1] row(s) selected.
```
