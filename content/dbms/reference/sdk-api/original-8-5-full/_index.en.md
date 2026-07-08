---
type: docs
title: '8.5 Complete SDK Reference'
weight: 95
tocSort: true
---


## jdbc


## JDBC Overview

The set of database manipulation interfaces created in the Java programming language is called JDBC (Java DataBase Connectivity). A set of APIs that provide a consistent interface for a variety of relational databases, defining a set of object-oriented classes of classes that the programmer will use to build SQL requests. That is, if you use a JDBC driver, no matter which database you use, there is an advantage that you can apply it directly without modifying the code.


## Standard JDBC Functions

[Standard Function Specs 4.0](http://www.oracle.com/technetwork/java/javase/jdbc/index.html#corespec40)

## JDBC Authentication Modes

> **Note**: AUTH KEY challenge authentication is supported from Machbase 8.5 or later.

Machbase JDBC supports both the existing password authentication and public-key-based
challenge authentication.

### Password Authentication

Use `user` and `password` as before.

### AUTH KEY Challenge Authentication

Challenge authentication uses the following properties.

- `AUTH_MODE`
  - `PASSWORD` or `CHALLENGE`
- `AUTH_SIG_SCHEME`
  - `ECDSA`
  - `RSA_PKCS1_V15`
  - `RSA_PSS`
- `AUTH_KEY_FILE`
  - Local PEM private key file path

Notes:

- `password` is not used for authentication when `AUTH_MODE=CHALLENGE`.
- `AUTH_KEY_FILE` is required.
- If `AUTH_SIG_SCHEME` is omitted, the driver selects the default scheme from the key file.
  - EC key: `ECDSA`
  - RSA key: `RSA_PKCS1_V15`
- Supported key parameters are ECDSA `P-256`, `P-384`, `P-521` and RSA `2048`, `3072`,
  `4096` bits.
- To use RSA-PSS authentication, specify `AUTH_SIG_SCHEME=RSA_PSS`.
- If `AUTH_KEY_FILE` is provided and `AUTH_MODE` is omitted, the driver treats the
  connection as `CHALLENGE`.
- An absolute path is recommended for the private key file. Relative paths are resolved
  from the JVM working directory.
- On POSIX systems, restricting the private key file permission to `600` is recommended.

### Properties Example

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

### URL Query String Example

```text
jdbc:machbase://127.0.0.1:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_SIG_SCHEME=ECDSA&AUTH_KEY_FILE=/opt/machbase/keys/app_user_ecdsa.pem
```

However, using `Properties` is recommended because the key file path may be exposed more
easily in logs or configuration dumps when it is included in the URL.

### Reconnect Behavior

- If the initial connection used `AUTH_MODE=CHALLENGE`, reconnect performs challenge
  authentication again.
- Reconnect does not reuse a previous nonce or signature.
- If challenge authentication fails, the driver does not automatically fall back to
  password authentication.


## JDBC Connection Options

The driver accepts connection options either in `Properties` or in the URL query string.
The current DBMS standard source handles these public options:

| Option | Description |
| -- | -- |
| `user` / `password` | Password authentication credentials. |
| `AUTH_MODE`, `AUTH_SIG_SCHEME`, `AUTH_KEY_FILE` | Challenge authentication options described above. |
| `TIMEZONE` | Session timezone string such as `+0900`. Invalid timezone strings fail connection setup. |
| `randomHost` | When `true`, randomizes the selected host from the parsed host list before connecting. |
| `maxStatements` | Maximum cached statement count for pooled connections. |
| `CONNECTION_TIMEOUT` | Socket connect timeout in seconds. `0` means no finite timeout. |
| `SOCKET_TIMEOUT` | Socket read timeout in seconds. `0` means no finite timeout. |
| `characterEncoding` | Client character encoding name. |


## Extension JDBC Functions

### setIpv4

```java
void setIpv4(int ind, String ipString)
```

This is a function to input IPv4 address type in PrepareStatement.

Receives column index and IPv4 string as arguments.

### setIpv6

```java
void setIpv6(int ind, String ipString)
```

This is a function to input IPv6 address type in PrepareStatement.

Receives column index and IPv6 string as arguments.

### executeAppendOpen

```java
ResultSet executeAppendOpen(String aTableName, int aErrorCheckCount)
```

Opens the protocol to write the Append protocol in the Statement.

The table name and error checking interval are received as arguments. Returns a ResultSet with the result value.

### executeAppendData

```java
int executeAppendData(ResultSetMetaData rsmd, ArrayList aData)
```

Enters the actual data for the Append protocol in the statement.

Receives the metadata of the ResultSet, which is the result value of executeAppendOpen, and the data to input. When the result value is stored in the transfer buffer, 1 is returned. If the transfer buffer is transferred to Machbase, 2 is returned. Therefore, if 1 or 2 is returned, it is judged as success.

### executeAppendDataByTime

```java
int executeAppendDataByTime(ResultSetMetaData rsmd, long aTime, ArrayList aData)
```

Enters the actual data for the Append protocol on a time basis in the statement.

Receives the metadata of the ResultSet which is the result value of executeAppendOpen, the time value of the specific time zone to be set, and the data to input as arguments. If the result value is stored in the transmission buffer, 1 is returned.

### executeAppendFlush

```java
int executeAppendFlush()
```

Flushes the current append stream and checks the pending append response. If the result is successful, it returns 1.

### executeAppendClose

```java
int executeAppendClose()
```

Terminates the statement for the Append protocol in the statement.

If the result is a success, it returns 1.

### executeSetAppendErrorCallback

```java
int executeSetAppendErrorCallback(MachAppendCallback aCallback)
```

Sets a callback function that outputs an error if an error occurs during Append execution.

It takes a callback function that outputs an error log as an argument. If the result is successful, 1 is returned.

### getAppendSuccessCount

```java
long getAppendSuccessCount()
```

Returns the number of successes for the Append protocol in the Statement.

Returns the number of successful results.

### getAppendFailureCount

```java
long getAppendFailureCount()
```

Returns the number of failures for the Append protocol in the Statement.

Returns the number of failures as a result.

### Batch append implementation note

The source includes internal protocol methods named `executeAppendAll` and `executeAppendAllByTime` for batch-style append writes. They are not exposed as public `MachStatement` methods in the checked DBMS standard source; use the public append methods documented above unless a later public wrapper is provided.


## Application Development

### JDBC Library Installation Check
Verifies that the machbase.jar file exists in the $MACHBASE_HOME/lib directory.

```bash
[mach@localhost ~]$ cd $MACHBASE_HOME/lib
[mach@localhost lib]$ ls -l machbase.jar
-rw-rw-r-- 1 mach mach 78599 Jun 18 10:00 machbase.jar
[mach@localhost lib]$
```

### Makefile Creation Guide

$(MACHBASE_HOME)/lib/machbase.jar must be specified in the classpath. The following is an example of a Makefile.

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

### Compile and Link
Run the make command to compile and link as follows:

```bash
[mach@localhost jdbc]$ make
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . MakeData.java Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$
```

## Application Development with Maven

Maven can be used to import Machbase JDBC (machjdbc) to a project.
Machbase JDBC driver can be found at [Maven Central Repository](https://mvnrepository.com/artifact/com.machbase/machjdbc).

### Import and use machjdbc

To import machjdbc, open `pom.xml` and add this tag in `<dependencies>` tag.
```
<dependency>
    <groupId>com.machbase</groupId>
    <artifactId>machjdbc</artifactId>
    <version>{{< jdbc_version >}}</version>
</dependency>
```
> Version {{< jdbc_version >}} can be replaced by the latest version in Maven Central.
<br>

machjdbc can be used in source code by using `import` statement, as below.
```
import com.machbase.jdbc.*;
```
<br><br>

## JDBC Sample

### Connection Example

Let's write an example program that connects to a Machbase server using a Machbase JDBC driver. Name the source file Sample1Connect.java.


> [Tips] The _arrival_time column is not displayed by default.<br>
> Therefore, to display the _arrival_time column, add show_hidden_cols = 1 to the connection string.<br><br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;You can modify the connection string in the following example source as follows:<br>
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

Now compile and run the source code. Use the Makefile you have already created.

```bash
[mach@localhost jdbc]$ make
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . MakeData.java Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$ make run_sample1
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample1Connect
machbase JDBC connected.
```

### Data Input and Output Example (1) Direct I/O

Create and display an example that uses the Machbase JDBC driver to input and output data.

The name of the source file is called Sample2Insert.java.
First, you need to create the necessary tables using the machsql program.
In the example, we used the sample code to create a table called sample_table in advance.

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

Now compile and run the source code. Use the Makefile you have already created.

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

### Data Input and Output Example (2) PreparedStatement Input Used

Create and view an example that uses a PreparedStatement to input and output data.

The name of the source file is Sample3PrepareStmt.java.

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

Now compile and run the source code. Use the Makefile you have already created.

It should be noted that the data entered in Sample2Insert.java is output together.

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

### Extension Function Append Example

The Machbase JDBC driver supports the Append protocol to quickly upload large numbers of data.

The following is an example of using the Append protocol.
Use the sample_table used in the previous example.
The name of the source file is called Sample4Append.java.
Enter the contents of data.txt into sample_table.
Create `data.txt` with the `make_data_file` target before running the append sample.

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

When appending, date type data must be converted to long type nanosecond time.

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

Displays the dot (.) every 10,000, and can know the input time.

```bash
## Use machsql to check number actually entered.
## Confirm that 100018 are entered including those from Sample2Insert and Sample3PrepareStmt.


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


## Overview

This guide is updated for the 2.3 package: install name is lowercase `machbaseapi`, and the package is now implemented in pure Python (no native `.so/.dll/.dylib` dependency).

You can continue using `import machbaseAPI` and existing `machbase` call patterns.

- `machbaseAPI` package name on PyPI: `machbaseapi`
- Module import pattern: `import machbaseAPI`
- DB-API style: `connect()` and `cursor()` are available
- `append*` callbacks can be observed through optional `on_ack` in append APIs.
- `append()`, `appendByTime()`, `appendData()`, and `appendDataByTime()` can be called without explicit column type codes; Machbase metadata is used for type inference.
- In 2.3, trailing columns omitted from append rows are stored as `NULL` through append null-bit metadata.
- For TAG tables, values through the `value` column are required; later value/meta columns can be omitted and stored as `NULL`.
- Connection-pool options are intentionally unsupported in 2.3 (`pool_name`, `pool_size`, `pool_reset_session`)

The examples below target the `machbase` class, which remains the main entry point for legacy-style scripts.

## Installation

### Requirements

- Python 3.6 or later with `pip`.
- A reachable Machbase server and credentials (default `SYS/MANAGER` on port `5656`).
- No native Machbase shared library installation is required in 2.3.

### Install from PyPI

```bash
pip3 install machbaseapi
```

If `pip3` is not on your PATH, use `python3 -m pip install machbaseapi`.

### Verify the module

```bash
python3 - <<'PY'
from machbaseAPI import machbase, connect
print('machbase class import ok:', bool(machbase))
print('connect function exists:', callable(connect))
print('module import:', __import__('machbaseAPI'))
PY
```

A successful run confirms that the package can be imported and instantiated.

You can also run DB-API samples with `connect()`.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()
cur.execute('SELECT * FROM m$tables LIMIT 1')
print(cur.fetchall())
conn.close()
```

## Quick Start

The snippet below connects to a local server, creates a sample table, inserts rows, reads them back, and closes the session.

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

## Result Handling

Most `machbase` methods return `1` on success and `0` on failure. After each call, use `db.result()` to read the JSON-formatted payload emitted by the server. When iterating over `select()` results, call `db.fetch()` repeatedly until it returns `(0, None)`, then release resources with `db.selectClose()`.

## Supported API Matrix

| Class | API | Description | Return |
| -- | -- | -- | -- |
| `machbase` | `open(host, user, password, port)` | Connect to a Machbase server with default credentials and port. | `1` on success, `0` on failure |
| `machbase` | `openEx(host, user, password, port, conn_str)` | Extended connect with additional connection string attributes. | `1` or `0` |
| `machbase` | `close()` | Terminate the current session. | `1` or `0` |
| `machbase` | `isOpened()` | Check whether a handle has been opened. | `1` or `0` |
| `machbase` | `isConnected()` | Verify that the handle is connected to the server. | `1` or `0` |
| `machbase` | `execute(sql)` | Run SQL directly. `SELECT`, `WITH`, `DESC`, `DESCRIBE`, and `SHOW` are routed through `select()`; other statements are executed with `exec_direct()`. | `1` or `0` |
| `machbase` | `schema(sql)` | Execute schema-related statements. | `1` or `0` |
| `machbase` | `tables()` | Fetch metadata for all tables. | `1` or `0` |
| `machbase` | `columns(table_name)` | Fetch column metadata for a specific table. | `1` or `0` |
| `machbase` | `column(table_name)` | Retrieve column layout using the low-level catalog call. | `1` or `0` |
| `machbase` | `statistics(table_name, user='SYS')` | Request table statistics via the CLI. | `1` or `0` |
| `machbase` | `select(sql)` | Execute a streaming `SELECT` or `DESC`. | `1` or `0` |
| `machbase` | `fetch()` | Pull the next row after `select()`. | `(rc, json_str)` |
| `machbase` | `selectClose()` | Close an open result set cursor. | `1` or `0` |
| `machbase` | `result()` | Return the latest JSON payload. | JSON string |
| `machbase` | `appendOpen(table_name, types=None)` | Begin append protocol with column type codes. When omitted, metadata can be loaded from server-side schema. | `1` or `0` |
| `machbase` | `appendData(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', on_ack=None)` | Append rows using the active append session. To omit the type list, pass rows as the second argument. The data packet is sent immediately when called. | `1` or `0` |
| `machbase` | `appendDataByTime(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None, on_ack=None)` | Append rows with explicit epoch timestamps. To omit the type list, pass rows as the second argument and timestamps with `aTimes`. The data packet is sent immediately when called. | `1` or `0` |
| `machbase` | `appendFlush()` | Synchronization point that checks pending responses for already-sent append data. It is not a delayed-send buffer flush API. | `1` or `0` |
| `machbase` | `appendClose()` | Close the append session. | `1` or `0` |
| `machbase` | `append(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS')` | Convenience wrapper that opens, appends, and closes. To omit the type list, pass rows as the second argument. | `1` or `0` |
| `machbase` | `appendByTime(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None)` | Convenience wrapper for time-aware append. To omit the type list, pass rows as the second argument and timestamps with `aTimes`. | `1` or `0` |

## DB-API style API (2.3)

| API | Description | Return |
| -- | -- | -- |
| `connect(**kwargs)` | Create a DB-API connection. Pass options by keyword, for example `host`, `port`, `user`, and `password`. | `MachbaseConnection` |
| `cursor(dictionary=True)` | Create a cursor (`True`: dict rows, `False`: tuple rows) | `MachbaseCursor` |
| `cursor.execute(sql, params=None)` | Execute SQL statement | `cursor` |
| `cursor.fetchone()` | Fetch one row | `tuple | dict | None` |
| `cursor.fetchmany(size)` | Fetch up to `size` rows | `list` |
| `cursor.fetchall()` | Fetch all rows | `list` |
| `cursor.close()` | Close cursor | `None` |
| `cursor.rowcount` | Number of affected rows | `int` |
| `connection.append(table, rows, types=None, times=None, strict=False)` | Append rows through the append protocol. Since 2.3, omitted trailing columns are padded as `NULL`. | Number of input rows |

## 2.3 append without explicit column types and trailing NULL padding (recommended)

`append()` and `appendByTime()` can be called without a type list.
Pass rows as the second argument and let the server metadata drive type handling.
Since 2.3, rows may omit trailing columns, and omitted columns are stored as `NULL` through append null-bit metadata.

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

### DB-API append trailing NULL example

`connect().append()` follows the same trailing `NULL` padding rule. Positional input cannot skip middle columns; pass `None` explicitly when a middle column should be stored as `NULL`.

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

The first row omits `note`, so `note` is stored as `NULL`. The second row passes `None` at the `value` position, so `value` is stored as `NULL`.

### TAG table append and metadata NULL example

For TAG tables, values corresponding to `name`, `time`, and `value` are required. Additional columns and metadata columns after `value` can be omitted, and omitted columns are stored as `NULL`.

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

In this example, `status`, `site`, and `line` are stored as `NULL`. A TAG append that omits `value` fails.

## API Reference and Samples (Legacy-style `machbase` class)

The examples below use the legacy-style `machbase` class that remains available in the 2.3
package. Methods such as `getSessionId()`, `count()`, and `checkBit()` were available in
older native packages but are not provided by the current pure-Python implementation.

Update host, port, username, and password values as needed in each script. Every snippet is standalone and can be executed with `python3 script.py`.

### Connection management

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

### DML and result buffers

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

### Streaming SELECT helpers

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

### Schema helpers

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

### Metadata and statistics

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

### Append protocol primitives

`appendOpen()`, `appendData()`, `appendFlush()`, and `appendClose()` stream rows efficiently.
Since 2.1, you can omit column types; server metadata is used automatically.
`appendData()` and `appendDataByTime()` send data packets immediately when called. `appendFlush()` is a synchronization point that checks pending responses for already-sent append data.

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

### Convenience append helpers

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

### Diagnostics

#### machbase.checkBit()

`checkBit()` was used for native pointer-size checks in legacy releases and is not available in the 2.3 pure-Python package.

### Low-level bindings

The 2.3 package does not provide legacy ctypes helpers such as
`get_library_path()`, `openDB()`, `execAppend*()`, or pointer utility APIs.
For low-level C-layer access, please keep using the pre-2.0 package.

## go


## Overview

The `machgo` package is a pure Go client for Machbase native protocol access.
It provides the same API style as `machcli`, but without depending on CGo.
If you need native-port performance with a fully Go toolchain, `machgo` is a good choice.

### Why use machgo?

- **No CGo dependency**: Build and deploy with a pure Go environment
- **Native protocol access**: Connect through the Machbase native port (default `5656`)
- **API compatibility with machcli**: Reuse the same connection/query/appender patterns
- **Production-friendly**: Good fit for containerized and cross-platform Go deployments

### Prerequisites

- **Machbase server**: A running DBMS or Neo server instance reachable on the native port
- **Go 1.22+**: Recent Go version recommended
- **Network access**: Reachable native port (`5656` by default)

## Getting Started

### Install

```sh
go get github.com/machbase/neo-client@latest
```

### Import

Import the API package and `machgo` client package:

```go
import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)
```

### Configuration

Use `machgo.Config` to configure host/port and concurrency options:

```go
conf := &machgo.Config{
    Host:         "127.0.0.1", // Machbase server host
    Port:         5656,          // Machbase native port
    MaxOpenConn:  0,             // Max Connection threshold
    MaxOpenQuery: 0,             // Max Query concurrency limit
}

// Create a database instance
// API usage is the same as machcli
mdb, err := machgo.NewDatabase(conf)
if err != nil {
    panic(err)
}
```

#### Configuration Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `MaxOpenConn` | Maximum open connections | `< 0`: unlimited<br>`0`: CPU count × factor<br>`> 0`: specified limit |
| `MaxOpenConnFactor` | Multiplier when MaxOpenConn is 0 | Default: 1.5 |
| `MaxOpenQuery` | Maximum concurrent queries | `< 0`: unlimited<br>`0`: CPU count × factor<br>`> 0`: specified limit |
| `MaxOpenQueryFactor` | Multiplier when MaxOpenQuery is 0 | Default: 1.5 |

#### FlowControl behavior

`MaxOpenConn` and `MaxOpenQuery` are flow-control limits.
If you set either value to `-1`, that limit is disabled (no FlowControl on that dimension).

```go
conf := &machgo.Config{
    Host:         "127.0.0.1",
    Port:         5656,
    MaxOpenConn:  -1, // disable connection FlowControl
    MaxOpenQuery: -1, // disable query FlowControl
}
```

### Establishing Connection

```go
ctx := context.Background()
conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
if err != nil {
    panic(err)
}
defer conn.Close()
```

Authentication options:

- `api.WithPassword(user, password)`

### Connection-level tuning options

`machgo` supports per-connection overrides at `Connect()` time.
This lets you keep global defaults in `machgo.Config`, while tuning each connection differently.

#### StatementCache for repeated SQL

For the same SQL used repeatedly during a single connection lifetime,
statement reuse can improve performance by reusing prepared statements.

You can set a default mode in `machgo.Config.StatementCache`, and override per connection with `api.WithStatementCache(...)`.

```go {linenos=table,linenostart=1,hl_lines=[5,16]}
// Connection A: aggressive statement reuse
connA, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheAuto),
)
if err != nil {
    panic(err)
}
defer connA.Close()

// Connection B: disable statement reuse for this connection only
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

#### FetchRows pre-fetch size

`FetchRows` controls the maximum number of records pre-fetched from server in one fetch round.
Set `machgo.Config.FetchRows` as the default, and override per connection via `api.WithFetchRows(...)`.
The default value is `1000`.

{{< callout type="warning" >}}
Avoid setting `FetchRows` to excessively large or small values without workload validation.
Depending on network latency and query characteristics, an improper value can cause significant performance degradation and increased memory consumption.
{{< /callout >}}

```go {linenos=table,linenostart=1,hl_lines=[5]}
// Connection C: larger pre-fetch for scan-heavy workloads
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
Always call `Close()` on connections to release resources.
{{< /callout >}}

## Database Operations

### Single Row Query (`QueryRow`)

Use `QueryRow` when exactly one row is expected.

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

### Multiple Row Query (`Query`)

Use `Query` for multi-row results.

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

### Data Modification (`Exec`)

Use `Exec` for INSERT, DELETE, and DDL statements.

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

## High-Performance Bulk Insert (`Appender`)

For high-throughput ingestion, use `Appender` with a dedicated connection.

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

You can tune the client-side transfer buffer threshold to server with:

The appender accumulates data from `Append()` calls in an internal buffer and sends it to the server only when configured thresholds are reached.
You can configure thresholds by byte size, row count, and delay (the time gap between the oldest buffered record and the newest one).
If any one of these thresholds is exceeded, the buffered data is sent to the server.

- `WithBatchMaxRows(rows)` : default `512`, minimum `1`
- `WithBatchMaxBytes(bytes)`: default `512KB`, minimum `4KB`
- `WithBatchMaxDelay(duration)` : default `5ms`, minimum `1ms`
- `WithBatchMaxDelay(0)` disables the time-based threshold

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

apd.WithBatchMaxBytes(1024 * 1024).    // 1 MB threshold
    WithBatchMaxRows(2000).            // row-count threshold
    WithBatchMaxDelay(500 * time.Millisecond) // max delay threshold
```

Appender flush example:

`Flush()` is a programmatic flush method.
Unlike threshold-based auto flush behavior, it forces buffered records to be sent immediately regardless of configured byte/row/delay thresholds.

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

{{< callout type="warning" >}}
Do not run regular queries on a connection that currently owns an active appender.
Use a separate connection for append workloads.
{{< /callout >}}

## Complete Example

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

This workflow is intentionally identical to `machcli` so existing code can be migrated with minimal changes.

## go-driver


## Overview
The `github.com/machbase/neo-client` package provides a standard Go `database/sql` driver for Machbase.
It is built on top of the native TCP client and uses the native port (default `5656`).

Use this driver when your application or framework already depends on Go's `database/sql` interfaces.
For new code that does not require `database/sql`, `machgo` is usually the better choice.

### Prerequisites

- **Machbase server**: A running DBMS or Neo server instance reachable on the native port
- **Go 1.22+**: Required by `github.com/machbase/neo-client`
- **Credentials**: A valid Machbase user account

## Getting Started

### Install

```sh
go get github.com/machbase/neo-client@latest
```

### Import

Import the driver package with a blank identifier.
The driver registers itself automatically with the name `machbase`.

```go
import (
    "context"
    "database/sql"
    "fmt"
    "strings"

    _ "github.com/machbase/neo-client"
)
```

## Connection

### DSN format

The simplest DSN uses the `server` key:

```text
server=tcp://sys:manager@127.0.0.1:5656
```

You can also combine additional options as semicolon-separated key/value pairs:

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=777;statement_cache=off;io_metrics=true
```

#### Supported DSN keys

| Key | Description |
|-----|-------------|
| `server` | Server URL such as `tcp://user:password@127.0.0.1:5656` |
| `host`, `port` | Server host and port provided separately |
| `user` | Login user |
| `password` | Login password |
| `fetch_rows` | Number of rows fetched per round trip |
| `statement_cache` | Statement cache mode: `auto`, `on`, or `off` |
| `io_metrics` | Enable I/O metrics: `true` or `false` |
| `alternative_servers` | Alternate server address such as `127.0.0.2:5656` |
| `alternative_host`, `alternative_port` | Alternate server host and port provided separately |

## Query Example

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

## Insert Example

The following example inserts rows into a tag table named `EXAMPLE`.

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

## Notes and Limitations

- Use positional placeholders like `?`; named parameters are not supported.
- `database/sql` connection pooling works through `sql.DB` as usual.
- Explicit transactions are not supported, so `Begin` and `BeginTx` return an error.
- `LastInsertId()` is not supported.
- Parameter type support follows the driver implementation. Common SQL types, `time.Time`, `[]byte`, and `net.IP` are supported, but `bool` parameters are not.

## nodejs


## Overview

The Machbase TypeScript client (`@machbase/ts-client`) is a pure TypeScript implementation of the Machbase CMI protocol. It allows Node.js applications to connect to a Machbase (standard edition) server, execute SQL statements, fetch results, work with prepared statements, and append batches of log data without native bindings.

This document covers installation, core APIs, practical examples, testing flows, and important behavioural notes.

## Installation

### Requirements

- Node.js 18 or newer (LTS recommended)
- A reachable Machbase server (standard edition)

### Install from npm

Install via your package manager:

```bash
npm install @machbase/ts-client
# or
yarn add @machbase/ts-client
# or
pnpm add @machbase/ts-client
```

### Offline Installation

If you received a `.tgz` file from Machbase:

```bash
# example file name; your version may differ
npm install ./machbase-ts-client-1.0.0.tgz
```

### Verify Installation

```bash
node -e "const { createConnection } = require('@machbase/ts-client'); console.log(typeof createConnection === 'function' ? 'ts-client import ok' : 'ts-client import failed')"
```

> **Note**: This client targets Node.js and uses TCP sockets; it is not a browser library (no WebSocket transport).
> The DBMS standard source package version is `@machbase/ts-client` 1.0.0.
>
> The default credentials shown in this guide (`SYS`/`MANAGER`) are for local testing only. Use dedicated users and passwords in production.

## Quick Start

The snippet below connects to a local server, creates a sample table, inserts rows, reads them back, and closes the session.

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

### CommonJS Example

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

> **Transaction notice:** Machbase autocommits every statement. Commands such as `BEGIN`, `COMMIT`, or `ROLLBACK` always return an error and should only be used to detect the lack of transaction support.

### Machbase Facade

If you prefer a facade similar to other Node.js SQL clients, `createConnection()` also supports callback and promise flows.

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

The facade supports both callbacks and `.promise()`, surfaces `QueryError` for failed operations, and forwards server messages.

> **Facade limitations:** `beginTransaction`, `commit`, and `rollback` report `QueryError` immediately because Machbase does not support SQL transactions. `UPDATE` on LOG or TAG tables also fails fast with an explicit server error.

## Common Issues

- **ECONNREFUSED** – Verify the server is started (`machadmin -u`) and the host/port are correct, and that firewalls permit TCP to the listener port (default 5656).
- **Authentication failed** – Check user/password and that the target database is created (`machadmin -c`).

## API Reference

### Connection Management

#### createConnection(config)

Establishes a network session to the Machbase listener and completes the CMI handshake.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | string | `127.0.0.1` | IP or hostname of the Machbase server |
| `port` | number | `5656` | Listener port |
| `user` | string | – | Database user (commonly `SYS`) |
| `password` | string | – | Password (commonly `MANAGER`) |
| `database` | string | `data` | Database name |
| `clientId` | string | `NPM` | Client identifier shown in server logs |
| `showHiddenColumns` | boolean | `false` | Include hidden columns in metadata |
| `timezone` | string | empty | Optional time zone identifier |
| `connectTimeout` | number | 5000 | Socket connect timeout (ms) |
| `queryTimeout` | number | 60000 | Per-command timeout (ms) |

```javascript
const conn = createConnection({ host: '192.168.1.10', user: 'SYS', password: 'MANAGER' });
await conn.connect();
```

The promise rejects if the socket fails, authentication fails, or the handshake response is unexpected.

#### connect()

Opens the connection to the server.

```javascript
await conn.connect();
```

#### end()

Closes the underlying socket. After calling `end()`, any further operation will throw an error.

```javascript
await conn.end();
```

### Executing SQL

#### execute(sql, values?)

Runs a statement that does not necessarily return rows. Use it for DDL (`CREATE`, `ALTER`, `DROP`) or data modification (`INSERT`, `UPDATE`, `DELETE`).

```javascript
const [create] = await conn.execute('CREATE TABLE demo (ID INTEGER, NAME VARCHAR(32))');
console.log('Rows affected:', create.affectedRows); // -> 0 for DDL

const [insert] = await conn.execute("INSERT INTO demo VALUES (1, 'alpha')");
console.log('Rows affected:', insert.affectedRows); // -> 1

await expectTransactionUnsupported(conn, 'COMMIT');
```

Helper used in the integration suite:

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

Executes a statement that returns rows. The facade resolves with a two-element tuple `[rows, fields]`.

```javascript
const [rows, fields] = await conn.query('SELECT ID, NAME FROM demo ORDER BY ID');
console.table(rows);
```

### Prepared Statements

#### prepare(sql)

Creates a prepared statement on the server:

```javascript
const stmt = await conn.prepare('SELECT NAME FROM demo WHERE ID = ?');
try {
  const [rows] = await stmt.execute([1]);
  console.log(rows); // -> [ { NAME: 'alpha' } ]
} finally {
  await stmt.close();
}
```

Methods on the returned object:

- `execute(parameters?)` – runs the statement and resolves to `[rowsOrPacket, fields]`.
- `getColumns()` – returns cached column metadata.
- `getLastMessage()` – surfaces the last server message for the statement.
- `getStatementId()` – exposes the internal statement identifier.
- `close()` – frees the server resource; safe to call more than once.

#### Prepared Statement Examples

**Reusing a prepared SELECT:**

```javascript
const select = await conn.prepare('SELECT DEVICE_ID, SENSOR_VALUE FROM sensors WHERE DEVICE_ID = ?');
for (const { id } of samples) {
  const [rows] = await select.execute([id]);
  console.log(`selected ${id}:`, rows);
}
await select.close();
```

**Prepared upsert:**

```javascript
const upsert = await conn.prepare(
  'INSERT INTO devices (DEVICE_ID, SENSOR_VALUE) VALUES (?, ?) ' +
  'ON DUPLICATE KEY UPDATE SET SENSOR_VALUE = ?',
);
const [result] = await upsert.execute([deviceId, firstValue, firstValue]);
console.log('Affected rows:', result.affectedRows);
await upsert.close();
```

**Typed parameters and NULL values:**

```javascript
await update.execute([
  { value: null, type: 'varchar' },
  { value: new Date(), type: 'varchar' },
  { value: 'sensor-200', type: 'varchar' },
]);
```

Runnable example scripts are typically built into `dist/examples/` after `npm run build`. They commonly look for `MACHBASE_EXAMPLE_*` first, then `MACHBASE_SMOKE_*`, and finally fall back to `SYS/MANAGER@127.0.0.1`.

### Append Protocol

#### appendBatch(table, columns, rows, options?)

Appends rows to a **log table** using the `CMI_APPEND_BATCH_PROTOCOL`. Provide only user-visible columns (log tables implicitly contain `_arrival_time` and `_rid`).

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

Supported column types: `int32`, `int64`, `float64`, `varchar`.

- `rows` accepts either plain arrays or `{ values, arrivalTime }` objects. Nulls are automatically encoded using Machbase sentinel values.
- `options` may supply `arrivalTime` (single default) or `arrivalTimes` (array per row).

The promise resolves to `{ table, rowsAppended, rowsFailed, message }`.

> **Tip**: A "column count does not match" error usually means the target table is not a log table or the provided columns are not in schema order. Use `appendOpen()` for TAG tables.

#### appendOpen(table, columns, options?)

Opens a lightweight append session. By default native APPEND open/data/close is enabled, and successful native writes do not produce per-chunk responses.

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

To disable native append and force prepared-statement fallback, set `MACHBASE_NATIVE_APPEND=0`. If the server rejects native append for a given table type or session, the facade automatically falls back to prepared statements.

TAG tables expose a `DATETIME` column. Supply either `Date` objects or `bigint` epoch values.

#### append(rows) on an append stream

Sends one or more rows to the open append stream.

```javascript
const frames = await stream.append([
  ['S-001', new Date(), 1.0],
  ['S-002', new Date(Date.now() + 1), 2.0],
]);
console.log('frames sent:', frames);
```

In native mode, success responses are suppressed for maximum throughput; errors still return failure packets.

### Helper Methods

#### ping()

Health check using `SELECT 1 FROM V$TABLES`.

```javascript
await conn.ping();
```

#### promise()

Produces a promise-first wrapper mirroring the familiar `.promise()` behaviour.

```javascript
const p = conn.promise();
await p.ping();
const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
```

#### escape, escapeId, format

Convenience utilities for building SQL strings safely.

```javascript
const safeName = conn.escapeId('table_name');
const safeValue = conn.escape('user input');
```

## Testing & Diagnostics

### Scripts

- `npm run build` – compile TypeScript.
- `npm run lint` – run ESLint on `src/`.
- `npm run smoke` – optional smoke test (skipped without environment variables).
- `npm test` – full integration suite (requires a live server):
  1. Creates a log table.
  2. Inserts and selects sample data.
  3. Demonstrates prepared statements with positional binds.
  4. Performs stress append (default: 5 batches x 200 rows) and verifies row counts.
  5. Issues `COMMIT` in each stage to demonstrate the expected transaction failure.
  6. Exercises the Machbase facade and verifies that transactions or `UPDATE` on LOG/TAG tables raise `QueryError` immediately.

Sample console output:

```text
COMMIT expected failure: Expected COMMIT to fail because Machbase does not support transactions.
machbase-facade-basic callback query returned 3 rows.
machbase-facade-update-log-fails message: UPDATE is not supported for LOG tables.
append-batch progress: batch 4/5 { table: 'TS_CLIENT_IT_...', rowsAppended: 200, rowsFailed: 0 }
append-batch final count: 1004
```

## Tutorials

### Quickstart (Log Table)

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

### Prepared Statements (Reuse)

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

### Batch Append to a Log Table

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

### Streaming Append to a TAG Table

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

> Native mode is enabled by default. To disable it, set `MACHBASE_NATIVE_APPEND=0`. On success the server does not send a per-chunk response; errors are still returned.

### Promise Wrapper + Ping

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

## Behaviour Notes & Limitations

### Transactions

Machbase autocommits every statement. Transactional keywords such as `BEGIN`, `COMMIT`, or `ROLLBACK` always fail, and the facade mirrors that behaviour by calling the supplied callback with a `QueryError` (`ERR_MACHBASE_NO_TX`).

```javascript
try {
  await conn.execute('COMMIT');
} catch (err) {
  console.log('Expected error:', err.message);
  // Error: Machbase does not support transactions
}
```

### Result Buffering & Pagination

The facade connection's `query` method buffers the entire rowset before resolving. For large tables, page manually with `ORDER BY … LIMIT` queries or primary-key ranges.

### Parameter Binding

Typed binds cover the portable scalar set (`int32`, `int64`, `float64`, and `varchar`). When supplying `null`, pair it with a concrete type:

```javascript
{ value: null, type: 'varchar' }
```

### Append Protocol

Use `appendBatch` for log tables and the streaming helper (`appendOpen` / `append`) for scenarios that need incremental ingest. When the server does not support the streaming protocol for a given table type (for example TAG tables), the facade automatically falls back to a prepared-statement loop. The safe operating pattern is to chunk data, inspect `rowsFailed`, and retry if needed.

### Error Handling

Errors propagate as standard `Error` objects (or `QueryError` when using the facade). Inspect `error.message` or the `QueryError` fields (`code`, `sql`) to diagnose issues. The integration suite deliberately exercises missing-table queries and unsupported `UPDATE` statements to keep failure messages descriptive.

### Table Type SQL Semantics

- **LOG and TAG tables** support `SELECT`, `INSERT`, and `DELETE`, but not `UPDATE`.
- **VOLATILE and LOOKUP tables** support all DML, but queries must include the primary key in `WHERE` clauses for correct index access and performance.

## Best Practices

1. **Always close connections**: Use try-finally blocks to ensure `conn.end()` is called.
2. **Reuse prepared statements**: Create them once and execute multiple times for better performance.
3. **Batch inserts**: Use `appendBatch` or `appendOpen` for bulk data loading instead of individual INSERT statements.
4. **Handle errors**: Wrap database operations in try-catch blocks and log errors appropriately.
5. **Use connection pooling**: For production applications, implement connection pooling to manage multiple concurrent requests.
6. **Parameterize queries**: Always use parameter binding (`?` placeholders) instead of string concatenation to prevent SQL injection.

## Revision History

### 2025-10-08

- Added end-user installation steps for npm, yarn, pnpm, and offline `.tgz` packages.
- Clarified the Node.js-only runtime requirement and expanded common connection troubleshooting notes.
- Consolidated table-type SQL constraints in the behaviour notes.

### 2025-10-03

- Added the TAG streaming example and documented the default `MACHBASE_NATIVE_APPEND` behaviour.
- Documented automatic fallback from native append to prepared statements when streaming is not supported.

### 2025-10-02

- Introduced the Machbase facade (`createConnection`, `QueryError`, `.promise()`, and facade prepared statements).
- Expanded integration coverage for callbacks, promise flows, and rejected `UPDATE` on LOG/TAG tables.

### 2025-09-30

- Added prepared statements with positional parameter binding.
- Added `appendBatch` for log tables, including null handling and append result statistics.
- Added integration coverage and runnable examples for transactions, pagination, parameter binding, append chunking, and error handling.

## dotnet


## Index

* [Overview](#overview)
* [Install](#install)
* [NuGet (Unified 8.0.54)](#nuget-unified-connector)
* [NuGet (Legacy 5.x) — Package Manager](#install-connector-via-nuget-package-manager)
* [Connection String Reference](#connection-string-reference)
* [API Reference](#api-reference)
* [Usage and Examples](#usage-and-examples)
* [Full Provider APIs (Protocol 4.0-full)](#full-provider-apis-protocol-40-full)

## Overview

Machbase ships a universal ADO.NET provider, **UniMachNetConnector**, that wraps every supported Machbase wire protocol (2.1 through 4.0). The DBMS standard source currently identifies the unified package as `UniMachNetConnector` version 8.0.54 and builds target frameworks `net452`, `net5.0`, `net6.0`, `net7.0`, and `net8.0`. The connector automatically chooses the correct protocol at runtime based on the connection string.

## Install

The Machbase server and client installers include the universal .NET provider under `$MACHBASE_HOME/lib/`.
A standard Linux install can include the .NET 5.0 build, for example
`UniMachNetConnector-net50-8.0.54.dll`, together with protocol-specific assemblies such as
`machNetConnector-40-net50-3.2.1.dll`. The source project can build additional target-framework
flavors when the matching .NET SDK is available.

- **UniMachNetConnector** – the framework-neutral entry point. Source builds are named
  `UniMachNetConnector-net{452|50|60|70|80}-<version>.dll`, so choose the build that matches
  the target framework you deploy.
- **Legacy protocol connectors** – optional protocol-specific assemblies that the universal
  loader can activate on demand, such as `machNetConnector-XX-net{40|50|60|70|80}-<version>.dll`.

Reference the DLL that matches your application, or copy it next to your binaries when you deploy.

## Install via NuGet (Unified Connector, 8.0.54) {#nuget-unified-connector}

The unified provider package ID is `UniMachNetConnector`. This is the recommended way for new apps because it keeps your project self-contained without shipping loose DLLs.

- Supported target frameworks: net452, net5.0, net6.0, net7.0, net8.0.
- The net5.0 and newer builds are self-contained. The net452 build restores `System.ValueTuple`
  4.5.0, as reflected in the source project.

### Quick start (CLI)

```bash
# From your project folder
dotnet add package UniMachNetConnector --version 8.0.54
dotnet build
```

If you added the reference but need to control sources (CI, offline, or corporate feed), add first then restore explicitly:

```bash
dotnet add package UniMachNetConnector --version 8.0.54 --no-restore

# Restore from nuget.org only (force fresh metadata)
dotnet nuget locals http-cache --clear
dotnet restore --no-cache --source https://api.nuget.org/v3/index.json
```

### Visual Studio

- Right-click your project → Manage NuGet Packages → Browse tab → search “UniMachNetConnector” → select version 8.0.54 → Install.

### Project file example

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.54" />
  <!-- no other Machbase packages required -->
  <!-- targets: net452|net5.0|net6.0|net7.0|net8.0 -->
  <!-- keep AnyCPU/x64 per your app; Machbase server side is unaffected -->
</ItemGroup>
```

### Using a local or private feed (optional)

If your environment uses a local folder feed or an internal registry, point restore to those sources. For a folder feed, place `UniMachNetConnector.8.0.54.nupkg` under a directory and add it as a source:

```bash
# one-time setup
dotnet nuget add source /path/to/local-nuget -n mach-local

# restore using both nuget.org and the local feed
dotnet restore --no-cache \
  --source /path/to/local-nuget \
  --source https://api.nuget.org/v3/index.json
```

In CI or restricted accounts, prefer an explicit packages directory with an absolute path:

```bash
PKG_DIR="$(pwd)/.nuget-packages"; mkdir -p "$PKG_DIR"
NUGET_PACKAGES="$PKG_DIR" dotnet restore --no-cache --source /path/to/local-nuget
NUGET_PACKAGES="$PKG_DIR" dotnet run --no-restore
```

> Tip: If you recently published 8.0.54 and `dotnet add package` still reports an older version, clear the HTTP cache and use `--no-cache` as shown above. A transient “incompatible with 'all' frameworks” message is usually a side effect of failed restore, not a real TFM mismatch.

### Minimal usage sample

```csharp
using Mach.Data.MachClient;

var cs = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var conn = new MachConnection(cs);
conn.Open();

using var cmd = new MachCommand("SELECT COUNT(*) FROM V$TABLES", conn);
var count = (long)cmd.ExecuteScalar();
Console.WriteLine($"Tables: {count}");
```

## NuGet (Legacy 5.x) — Package Manager {#install-connector-via-nuget-package-manager}

> **Note**: .NET Connector 5.0 of Machbase has already enrolled to NuGet package! This 5.0 package is the legacy standalone distribution that predates the unified UniMachNetConnector.

If you use Visual Studio, you can still obtain the pre-unified connector from NuGet. The steps below install the legacy `machNetConnector5.0` package (use this only when you must target older code that predates the unified provider).

1. In Visual Studio, create a new C# .NET project.
2. When the project is created, activate context menu above project name at Solution Explorer and select "Manage NuGet Packages".
3. When NuGet Package Manager window is activated, select "Browse" tab on the upper left and search "machNet".
4. When the result is displayed on the left pane, select "machNetConnector5.0" and select "Install".
5. If Preview Changes window is activated, just select "OK" to continue to install.
6. When the package was installed successfully, you can confirm it at "Dependencies - Packages" on Solution Explorer.
7. Now, you can use machNetConnector by "using Mach.Data.MachClient" at Program.cs.

> Which NuGet should I use?
> - Prefer `UniMachNetConnector` 8.0.54 for new or upgraded apps. It supports net452 and net5.0–net8.0 and bundles all protocols, including the full provider surface (4.0-full).
> - Use `machNetConnector5.0` only for legacy scenarios where migrating to the unified package is not yet possible.

## Connection String Reference

Connection-string segments are separated by semicolons (`;`). Keywords listed in the same row are aliases.

| Keyword                                                         | Description                                                                                              | Example                                         | Default |
|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|-------------------------------------------------|---------|
| `DSN`, `SERVER`, `HOST`                                         | Hostname or IP address                                                                                    | `SERVER=127.0.0.1`                              | _(none)_|
| `PORT`, `PORT_NO`                                               | Listener port                                                                                             | `PORT=5656`                                    | `5656`  |
| `USERID`, `USERNAME`, `USER`, `UID`                             | Username                                                                                                  | `UID=SYS`                                       | `SYS`   |
| `PASSWORD`, `PWD`                                               | Password                                                                                                  | `PWD=manager`                                   | _(none)_|
| `CONNECT_TIMEOUT`, `ConnectionTimeout`, `connectTimeout`        | Connection timeout in milliseconds                                                                        | `CONNECT_TIMEOUT=10000`                        | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout`, `commandTimeout`           | Per-command timeout in milliseconds                                                                       | `COMMAND_TIMEOUT=50000`                        | `60000` |
| `PROTOCOL`, `ProtocolVersion`, `MachProtocol`                   | Preferred wire protocol (for example `2.1`, `3.0`, `4.0`, `4.0-full`, `auto`, `auto-full`). UniMachNetConnector defaults to `4.0` when omitted. | `PROTOCOL=auto`                                | `4.0`   |

Example:

```csharp
var connectionString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;COMMAND_TIMEOUT=50000;PROTOCOL=4.0-full",
    host,
    port);
```

### Protocol auto-detection (`PROTOCOL=auto`)

When your application connects to a mix of Machbase releases, set `PROTOCOL=auto` to let UniMachNetConnector negotiate the correct legacy handshake at runtime. The resolver works as follows:

- `PROTOCOL=auto` tests versions 4.0, 3.0, 2.2, then 2.1 in that order, using your supplied host, port, user, password, database, and `CONNECT_TIMEOUT`.
- `PROTOCOL=auto-full` behaves the same but, when the server reports protocol 4.0, the connector prefers the full-provider descriptor (`4.0-full`) before falling back to the limited surface area.
- Multiple hosts in `SERVER=hostA:5700,hostB:6000` are tried sequentially; each failure message records the per-host/per-protocol attempt so you can pinpoint unreachable versions.
- Credentials are upper-cased the same way as the legacy native drivers, so existing SYS/MANAGER test deployments work without change. Provide an explicit `DATABASE=` value when you do not use the default `data` catalog.
- The `CONNECT_TIMEOUT` governs each probe roundtrip. If you see `Protocol probe received an invalid response (missing result)` in the exception text, the handshake did not complete—verify the port, TLS/SSL settings, or firewall.

Explicit `PROTOCOL=2.1`, `3.0`, `4.0`, or `4.0-full` remain available when you already know the exact server version and want to skip auto-detection.

## API Reference

{{<callout type="warning">}}
Features not listed below may not be implemented yet or may not work correctly.<br>
If you call a method or field that is not a named instance, it generates NotImplementedException or a NotSupportedException.
{{</callout>}}

### MachConnection

```cs
public sealed class MachConnection : DbConnection
```

This class is responsible for linking with Machbase.

Because it inherits IDisposable like DbConnection, it supports disassociation through Dispose () or automatic disposition of object using using () statement.

#### Constructor
```
MachConnection(string aConnectionString)
```

Creates a MachConnection with a Connection String as input.


#### Open

```cs
void Open()
```

Attempts to connect to the connection string.

#### Close

```cs
void Close()
```

Closes the connection when connecting.

#### SetConnectAppendFlush

```cs
void SetConnectAppendFlush(bool activeFlush)
```

Set flush to be performed automatically during append.

#### Field

| Name | Description |
|--|--|
|State|Represents a System.Data.ConnectionState value.|
|StatusString|Indicates the state to be performed by the connected MachCommand.<br>This is used internally to decorate the Error Message and it is not appropriate to check the status of the query with this value because it indicates the state in which the operation started.|


### MachCommand

```cs
public sealed class MachCommand : DbCommand
```

A class that performs **SQL commands or APPEND** using MachConnection.

Since it inherits IDisposable like DbCommand, it supports object disposal through Dispose () or automatic disposal of object using using () statement

#### Constructor

```cs
MachCommand(string aQueryString, MachConnection)
```

Creates by typing the query to be executed along with the MachConnection object to be connected.

```cs
MachCommand(MachConnection)
```

Creates a MachConnection object to connect to. Use only if there is no query to perform (eg APPEND).


#### CreateParameter

```cs
MachParameter CreateParameter()
```

Creates a new MachParameter.

#### AppendOpen

```cs
MachAppendWriter AppendOpen(aTableName, aErrorCheckCount = 0, MachAppendOption = None)
```

Starts APPEND. Returns a MachAppendWriter object.

* aTableName: Target table name
* aErrorCheckCount: Each time the cumulative number of records entered by APPEND-DATA matches, it is checked whether it is sent to the server or not.<br>
  In other words, you are setting the automatic APPEND-FLUSH point.<br>
* MachAppendOption: Currently only one option is provided.
  * MachAppendOption.None: No options are attached.
  * MachAppendOption.MicroSecTruncated: When inputting the value of a DateTime object, enter the value expressed only up to microsecond.
  (The Ticks value of a DateTime object is expressed up to 100 nanoseconds.)

#### AppendData

```cs
void AppendData(MachAppendWriter aWriter, List<object> aDataList)
```

Through the MachAppendWriter object, it takes a list containing the data and enters it into the database.
- In the order of the data in the List, each datatype must match the datatype of the column represented in the table.
- If the data in the List is insufficient or overflows, an error occurs.

> **Note**: When representing a time value with a ulong object, simply do not enter the Tick value of the DateTime object. In that value, you must enter a value that excludes the DateTime Tick value that represents 1970-01-01.


```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, DateTime aArrivalTime)
```

Method that explicitly puts an _arrival_time value into a DateTime object in AppendData().

```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, ulong aArrivalTimeLong)
```

Method that can explicitly put _arrival_time value into a ulong object in AppendData(). Refer to AppendData() above for problems that may occur when typing a ulong value as an _arrival_time value.

#### AppendFlush

```cs
void AppendFlush(MachAppendWriter aWriter)
```

The data entered by AppendData() is immediately sent to the server to force data insert.<br>
The more frequently the call is made, the lower the data loss rate due to the system error and the faster the error check, although the performance is lowered.<br>
The less frequently the call is made, the more likely the data loss will occur and the error checking will be delayed, but the performance will increase significantly.

#### AppendClose

```cs
void AppendClose(MachAppendWriter aWriter)
```

Closes APPEND. Internally, after calling AppendFlush(), the actual protocol is internally finished.

#### ExecuteNonQuery

```cs
int ExecuteNonQuery()
```

Performs the input query. Returns the number of records affected by the query. It is usually used when performing queries except SELECT.

#### ExecuteScalar

```cs
object ExecuteScalar()
```

Performs the input query. Returns the first value of the query targetlist as an object. It is usually used when you want to perform a SELECT query, especially a SELECT (Scalar Query) with only one result, and get the result without a DbDataReader.

#### ExecuteDbDataReader

```cs
DbDataReader ExecuteDbDataReader(CommandBehavior aBehavior)
```

Executes the input query, generates a DbDataReader that can read the result of the query, and returns it.

#### Field

| Name | Description|
|--|--|
| Connection / DbConnection                   | Connected MachConnection.|
| ParameterCollection / DbParameterCollection | The MachParameterCollection to use for the Binding purpose.|
| CommandText                                 | Query string.|
| CommandTimeout                              | The amount of time it takes to perform a particular task, waiting for a response from the server.<br>It follows the values ​​set in MachConnection, where you can only reference values.|
| FetchSize                                   | The number of records to fetch from the server at one time . The default value is 3000.|
| IsAppendOpened                              | Determines if Append is already open when APPEND is at work|


### MachDataReader

```cs
public sealed class MachDataReader : DbDataReader
```

This is a class that reads fetch results. Only objects created with MachCommand.ExecuteDbDataReader () that can not be explicitly created are available.

#### GetName

```cs
string GetName(int ordinal)
```

Returns the ordinal column name.

#### GetDataTypeName

```cs
string GetDataTypeName(int ordinal)
```

Returns the datatype name of the ordinal column.

#### GetFieldType

```cs
Type GetFieldType(int ordinal)
```

Returns the datatype of the ordinal column.


#### GetOrdinal

```cs
int GetOrdinal(string name)
```

Returns the index at which the column name is located.


#### GetValue

```cs
object GetValue(int ordinal)
```

Returns the ordinal value of the current record.

#### IsDBNull

```cs
bool IsDBNull(int ordinal)
```

Returns whether the ordinal value of the current record is NULL.

#### GetValues

```cs
int GetValues(object[] values)
```

Sets all the values ​​of the current record and returns the number.

#### Get*xxxx*

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

Returns the ordinal column value according to the datatype.

#### Read

```cs
bool Read()
```

Reads the next record. Returns False if the result does not exist.

#### Field

| Name | Description|
|--|--|
| FetchSize         |The number of records to fetch from the server at one time. The default is 3000, which can not be modified here.|
| FieldCount        |Number of result columns.|
| this[int ordinal] |Equivalent to object GetValue (int ordinal).|
| this[string name] |Equivalent to object GetValue(GetOrdinal(name).|
| HasRows           |Indicates whether the result is present.|
| RecordsAffected   |Unlike MachCommand, here, it represents Fetch Count.|

### MachParameterCollection

```cs
public sealed class MachParameterCollection : DbParameterCollection, IEnumerable<MachParameter>
```

This is a class that binds parameters needed by MachCommand.

If you do this after binding, the values ​​are done together.

> Since the concept of Prepared Statement is not implemented, execution performance after Binding is the same as the performance performed first.

#### Add

```cs
MachParameter Add(string parameterName, DbType dbType)
```

Adds the MachParameter, specifying the parameter name and type. Returns the added MachParameter object.

```cs
int Add(object value)
```

Adds a value. Returns the index added.


```cs
void AddRange(Array values)
```

Adds an array of simple values.

```cs
MachParameter AddWithValue(string parameterName, object value)
```

Adds the parameter name and its value. Returns the added MachParameter object.|

#### Contains

```cs
bool Contains(object value)
```

Determines whether or not the corresponding value is added.

```cs
bool Contains(string value)
```

Determines whether or not the corresponding parameter name is added.

#### Clear

```cs
void Clear()
```

Deletes all parameters.

#### IndexOf

```cs
int IndexOf(object value)
```

Returns the index of the corresponding value.

```cs
int IndexOf(string parameterName)
```

Returns the index of the corresponding parameter name.

#### Insert

```cs
void Insert(int index, object value)
```

Adds the value to a specific index.

#### Remove

```cs
void Remove(object value)
```

Deletes the parameter including the value.

```cs
void RemoveAt(int index)
```

Deletes the parameter located at the index.

```cs
void RemoveAt(string parameterName)
```

Deletes the parameter with that name.

#### Field

| Name                 | Description                 |
| ----------------- | --------------------------------------- |
|Count              | Number of parameters|
|this[int index]    | Indicates the MachParameter at index.|
|this[string name]  | Indicates the MachParameter of the order in which the parameter names match.|

### MachParameter

```cs
public sealed class MachParameter : DbParameter
```

This is a class that contains the information that binds the necessary parameters to each MachCommand.

No special methods are supported.

#### Field

| Name            | Description                                                                          |
| ------------- | --------------------------------------------------------------------------------- |
|ParameterName|Parameter name|
|Value|Value|
|Size|Value size|
|Direction|ParameterDirection (Input / Output / InputOutput / ReturnValue)<br>The default value is Input.|
|DbType|DB Type|
|MachDbType|MACHBASE DB Type<br>May differ from DB Type.|
|IsNullable|Whether nullable|
|HasSetDbType|Whether DB Type is specified|


### MachException

```cs
public class MachException : DbException
```

This is a class that displays errors that appear in Machbase.

An error message is set, and all error messages  can be found in  MachErrorMsg .

#### Field

| Name| Description|
|--|--|
|int MachErrorCode|Error code provided by MACHBASE|

### MachAppendWriter

```cs
public sealed class MachAppendWriter
```

APPEND is supported as a separate class using MachCommand.
This is a class to support MACHBASE Append Protocol, not ADO.NET standard.

It is created with MachCommand's AppendOpen () without a separate constructor.

#### SetErrorDelegator

```cs
void SetErrorDelegator(ErrorDelegateFuncType aFunc)

void ErrorDelegateFuncType(MachAppendException e);
```

Specifies the ErrorDelegateFunc to call when an error occurs.

#### Field

| Name | Description |
|--|--|
|SuccessCount|Number of successful records. Is set after AppendClose().|
|FailureCount|The number of records that failed input. Set after AppendClose ().|
|Option|MachAppendOption received input during AppendOpen()|


### MachAppendException

```cs
public sealed class MachAppendException : MachException
```

Same as MachException, except that:

* An error message is received from the server side.
* A data buffer in which an error has occurred can be obtained. (comma-separated) can be used to process and re-append or record data.

The exception is only available within the ErrorDelegateFunc.

#### GetRowBuffer

```cs
string GetRowBuffer()
```

A data buffer in which an error has occurred can be obtained.

## Usage and Examples

### Connection

You can create a MachConnection and use Open () - Close ().
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
MachConnection sConn = new MachConnection(sConnString);
sConn.Open();
//... do something
sConn.Close();
```

If you use the using statement, you do not need to call Close (), which is a connection closing task.
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();
    //... do something
} // you don't need to call sConn.Close();
```

### Executing Queries

Create a MachCommand and perform the query.

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    String sQueryString = "CREATE TABLE tab1 ( col1 INTEGER, col2 VARCHAR(20) )";
    MachCommand sCommand = new MachCommand(sQueryString , sConn)
    try
    {
        sCommand.ExecuteNonQuery();
    }
    catch (MachException me)
    {
        throw me;
    }
}
```

Again, using the using statement, MachCommand release can be done immediately.
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    String sQueryString = "CREATE TABLE tab1 ( col1 INTEGER, col2 VARCHAR(20) )";
    using(MachCommand sCommand = new MachCommand(sQueryString , sConn))
    {
        try
        {
            sCommand.ExecuteNonQuery();
        }
        catch (MachException me)
        {
            throw me;
        }
    }
}
```

### Executing SELECT
You can get a MachDataReader by executing a MachCommand with a SELECT query.

You can fetch the records one by one through the MachDataReader.
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    String sQueryString = "SELECT * FROM tab1;";
    using(MachCommand sCommand = new MachCommand(sQueryString , sConn))
    {
        try
        {
            MachDataReader sDataReader = sCommand.ExecuteReader();
            while (sDataReader.Read())
            {
                for (int i = 0; i < sDataReader.FieldCount; i++)
                {
                    Console.WriteLine(String.Format("{0} : {1}",
                                                    sDataReader.GetName(i),
                                                    sDataReader.GetValue(i)));
                }
            }
        }
        catch (MachException me)
        {
            throw me;
        }
    }
}
```

### Parameter Binding
You can create a MachParameterCollection and then link it to a MachCommand.
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    string sSelectQuery = @"SELECT *
        FROM tab2
        WHERE CreatedDateTime < @CurrentTime
        AND CreatedDateTime >= @PastTime";

    using (MachCommand sCommand = new MachCommand(sSelectQuery, sConn))
    {
        DateTime sCurrtime = DateTime.Now;
        DateTime sPastTime = sCurrtime.AddMinutes(-1);

        try
        {
            sCommand.ParameterCollection.Add(new MachParameter { ParameterName = "@CurrentTime", Value = sCurrtime });
            sCommand.ParameterCollection.Add(new MachParameter { ParameterName = "@PastTime", Value = sPastTime });

            MachDataReader sDataReader = sCommand.ExecuteReader();

            while (sDataReader.Read())
            {
                for (int i = 0; i < sDataReader.FieldCount; i++)
                {
                    Console.WriteLine(String.Format("{0} : {1}",
                                                    sDataReader.GetName(i),
                                                    sDataReader.GetValue(i)));
                }
            }
        }
        catch (MachException me)
        {
            throw me;
        }
    }
}
```

### APPEND
When you run AppendOpen () on a MachCommand, you get a MachAppendWriter object.

Using this object and MachCommand, you can get a list of one input record and perform an AppendData().
AppendFlush() will reflect the input of all records, and AppendClose () will end the entire Append process.
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    using (MachCommand sAppendCommand = new MachCommand(sConn))
    {
        MachAppendWriter sWriter = sAppendCommand.AppendOpen("tab2");
        sWriter.SetErrorDelegator(AppendErrorDelegator);

        var sList = new List<object>();
        for (int i = 1; i <= 100000; i++)
        {
            sList.Add(i);
            sList.Add(String.Format("NAME_{0}", i % 100));

            sAppendCommand.AppendData(sWriter, sList);

            sList.Clear();

            if (i % 1000 == 0)
            {
                sAppendCommand.AppendFlush();
            }
        }

        sAppendCommand.AppendClose(sWriter);
        Console.WriteLine(String.Format("Success Count : {0}", sWriter.SuccessCount));
        Console.WriteLine(String.Format("Failure Count : {0}", sWriter.FailureCount));
    }
}
```
```c#
private static void AppendErrorDelegator(MachAppendException e)
{
    Console.WriteLine("{0}", e.Message);
    Console.WriteLine("{0}", e.GetRowBuffer());
}
```

### Set Error Delegator

In MachAppendWriter, you can specify a function to detect errors occurring on the MACHBASE server side during APPEND.

In .NET, this function type is specified as a Delegator Function.
```c#
public static void ErrorCallbackFunc(MachAppendException e)
{
    Console.WriteLine("====================");
    Console.WriteLine("Error occured");
    Console.WriteLine(e.Message);
    Console.WriteLine(e.StackTrace);
    Console.WriteLine("====================");
}

public static void DoAppend()
{
    MachCommand com = new MachCommand(conn);
    MachAppendWriter writer = com.AppendOpen("tag", errorCheckCount);
    writer.SetErrorDelegator(ErrorCallbackFunc);
    //... do append
}
```

### Set Auto AppendFlush

If you set `Set Connect Append Flush` to true in the connection, flush is automatically performed during append.

```cs
private static string connString = $"SERVER={HOST};PORT_NO={port};USER={USER};PWD={PWD}";

public static void Main(string[] args)
{
    MachConnection conn = new MachConnection(connString);
    conn.Open();
    conn.SetConnectAppendFlush(true);
}
```

If set to false, the function is disabled.

```cs
conn.SetConnectAppendFlush(false);
```

## Full Provider APIs (Protocol 4.0-full)

The `4.0-full` handshake unlocks the full ADO.NET surface. In the 8.0.54 source package,
the 4.0 limited connector is version 3.1.2 and the 4.0-full connector is version 3.2.1.
Installed Linux packages may include only the net50 flavor under `$MACHBASE_HOME/lib/`; build
or restore additional target frameworks when your application needs them.

- `UniMachNetConnector-net50-8.0.54.dll` – universal entry point commonly installed with DBMS Standard Linux packages.
- `machNetConnector-40-net50-3.1.2.dll` – protocol 4.0 limited connector.
- `machNetConnector-40-net50-3.2.1.dll` – protocol 4.0-full connector.

### Key types introduced by 4.0-full
- `MachDbProviderFactory` (`Instance`, `Register()`, and the standard `Create*` methods) so frameworks can resolve the connector by invariant name `Mach.Data`.
- `MachConnectionStringBuilder` for strongly typed connection-string edits without remembering every keyword.
- `MachDataAdapter` plus the `MachRowUpdating`/`MachRowUpdated` events for DataTable/DataSet workflows.
- `MachCommandBuilder` to auto-generate INSERT/DELETE (and UPDATE for tables that support it—never for log/tag tables) commands from a SELECT statement.

### Enable the full provider stack
```csharp
var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
```

Use lookup or volatile tables when you need INSERT/DELETE/UPDATE semantics. Log and tag tables do not accept UPDATE statements, so keep those workloads append-only.

### Build connection strings fluently
```csharp
var builder = new MachConnectionStringBuilder
{
    Server = "127.0.0.1",
    Port = 5656,
    UserID = "SYS",
    Password = "MANAGER"
};

// Protocol stays a string key so older connectors understand the value.
builder["PROTOCOL"] = "4.0-full";

using var connection = new MachConnection(builder.ConnectionString);
connection.Open();
```

### Sample: append rows with MachDataAdapter
This example downloads a lookup table into a `DataTable`, appends a new row, and pushes the change back. The `MachCommandBuilder` auto-generates the INSERT statement. (If the table does not exist yet, create it once: `CREATE LOOKUP TABLE dotnet_lookup_demo(id LONG PRIMARY KEY, name VARCHAR(64));`)

```csharp
using Mach.Data.MachClient;
using System.Data;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
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

> **Tip**: When you need to inspect or veto outgoing commands, subscribe to `MachDataAdapter.MachRowUpdating` / `MachRowUpdated`.

```csharp
adapter.MachRowUpdating += (sender, args) =>
{
    Console.WriteLine($"About to run {args.StatementType} with SQL: {args.Command?.CommandText}");
};
```

### Sample: work through DbProviderFactory
`MachDbProviderFactory.Instance` lets you plug Machbase into provider-agnostic infrastructure such as `DbProviderFactories`, Dapper, or your own DI container.

```csharp
using System.Data.Common;
using Mach.Data.MachClient;

DbProviderFactory factory = MachDbProviderFactory.Instance;

using DbConnection connection = factory.CreateConnection()!;
connection.ConnectionString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
connection.Open();

using DbCommand command = connection.CreateCommand();
command.CommandText = "SELECT COUNT(*) FROM dotnet_lookup_demo";
var count = (long)command.ExecuteScalar();

Console.WriteLine($"Lookup rows: {count}");
```

Need to make the factory visible to configuration-driven apps? Call `MachDbProviderFactory.Register()` once during startup so `DbProviderFactories.GetFactory("Mach.Data")` returns the same instance.

Remember that `4.0-full` is only available when you connect to Machbase 7.x or later servers; fall back to `Protocol=4.0` (limited surface) or the 2.x/3.x protocols for older clusters.

## cli-odbc


CLI is  a software development standard defined in [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)/[IEC](https://en.wikipedia.org/wiki/International_Electrotechnical_Commission) 9075-3: 2003.

The CLI defines functions and specifications for how to pass SQL to the database and how to receive and analyze the results. This CLI was developed in the early 1990s and was developed exclusively for C and COBOL languages, and its specifications have been maintained to date.

The most widely known standard interface to date is ODBC (Open Database Connectivity), which provides a way for a client program to access a database regardless of the type of database. The current ODBC API version is 3.52 and is defined in ISO and X/Open standards.


## Standard CLI Functions

See the following links for usage of the standard functions.
* [Wikipedia](http://en.wikipedia.org/wiki/Call_Level_Interface)
* [Open Group Document](https://www2.opengroup.org/ogsys/catalog/c451)

You can refer to the following function.

| | | | |
|--|--|--|--|
|SQLAllocConnect|SQLDisconnect|SQLGetDescField|SQLPrepare|
|SQLAllocEnv|SQLDriverConnect|SQLGetDescRec|SQLPrimaryKeys|
|SQLAllocHandle|SQLExecDirect|SQLGetDiagRec|SQLStatistics|
|SQLAllocStmt|SQLExecute|SQLGetEnvAttr|SQLRowCount|
|SQLBindCol|SQLFetch|SQLGetFunctions|SQLSetConnectAttr|
|SQLBindParameter+|SQLFreeConnect|SQLGetInfo|SQLSetDescField|
|SQLColAttribute|SQLFreeEnv|SQLGetStmtAttr|SQLSetDescRec|
|SQLColumns|SQLFreeHandle|SQLGetTypeInfo|SQLSetEnvAttr|
|SQLConnect|SQLFreeStmt|SQLNativeSQL|SQLSetStmtAttr|
|SQLCopyDesc|SQLGetConnectAttr|SQLNumParams|SQLStatistics|
|SQLDescribeCol|SQLGetData|SQLNumResultCols|SQLTables|


## Connection String for Connecting

To connect through the CLI, you need to create a connection string. The contents of each are as follows.

|Connection String Item Name|Item Description|
|--|--|
|DSN|Specifies the data source name.<br>ODBC specifies the section name of the file containing the resource, and CLI specifies the server name or IP address.|
|DBNAME|Describes the DB name of Machbase.|
|SERVER|Indicates the host name or IP address of the server where Machbase is located.|
|NLS_USE|Sets the language type to use with each other (currently unused, kept for future expansion).|
|UID|User ID|
|PWD|User password|
|PORT_NO|Port number to connect to|
|PORT_DIR|Specifies the file path to use when connecting to a Unix domain from Unix.<br>(It is specified when modified from the server, and it works even if it is not specified by default.)|
|CONNTYPE|Specifies the connection method between the client and the server.<br><br>1: Connection with TCP / IP INET<br>2: Connect to Unix Domain|
|COMPRESS|Indicates whether to compress the Append protocol.<br><br>If this value is 0, it is transmitted without compression.<br>If this value is any value greater than 0, it is compressed only if the Append record is larger than its value.<br><br>Ex) COMPRESS = 512<br>Only when the record size is larger than 512, it is compressed and operates.<br><br>For remote connection, compression improves transmission performance.|
|SHOW_HIDDEN_COLS|Decides whether to show the hidden column (`_arrival_time`) when executing it with select *.<br><br>If it is 0, it is not shown. If it is 1, information of the corresponding column is output.|
|CONNECTION_TIMEOUT|Sets how long to wait on the first connection.<br><br>The default setting is 30 seconds.<br>This value is set higher if the server response on the first connection is slower than 30 seconds.|
|SOCKET_TIMEOUT|This is a timeout that occurs when Protocol I/O takes time.<br><br>The client checks and waits , then performing Disconnect.<br><br>Same as Read Timeout of ORACLE. (In MYSQL and MSSQL, uses SOCKET_TIMEOUT as same as Machbase.)<br><br>Set SOCKET_TIMEOUT=NN (seconds) in Connection String, and the default value is set to 30 minutes (1800).|
|ALTERNATIVE_SERVERS|When using the cluster version, it is a setting to have the information of several brokers additionally.<br><br>When multiple brokers are registered, even if the connected broker is terminated, the data is continuously input after connecting to another broker.<br><br>Multiple brokers can be registered, and the values of <server address>:<server port> are separated by commas.<br><br>ex) ALTERNATIVE_SERVERS=192.168.0.10:20320,192.168.0.11:20320;|
|AUTH_MODE|Authentication mode. Use `PASSWORD` for password authentication or `CHALLENGE` for private-key challenge authentication. If `AUTH_KEY_FILE` is set and `AUTH_MODE` is omitted, the CLI treats the connection as `CHALLENGE`.|
|AUTH_SIG_SCHEME|Signature scheme for `AUTH_MODE=CHALLENGE`: `ECDSA`, `RSA_PKCS1_V15`, or `RSA_PSS`. If omitted, the client attempts to infer the default scheme from the key file.|
|AUTH_KEY_FILE|Local PEM private key file path for `AUTH_MODE=CHALLENGE`. The key file is required for challenge authentication.|

An example of CLI connection is as follows.

```c
sprintf(connStr,"SERVER=127.0.0.1;COMPRESS=512;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

if (SQL_ERROR == SQLDriverConnect( gCon, NULL, (SQLCHAR *)connStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT )) {
   ...
}
```


## Extension CLI Function (APPEND)

The CLI extension function is a function for implementing the Append protocol provided to input data to the Machbase server at high speed.

This function consists of four functions: channel open, channel data input, channel flush, and channel closing.

### Understanding Append Protocol

The Append protocol provided by Machbase works asynchronously. The term asynchronous means that the response to a specific job requested by the client to the server does not completely synchronize with each other but occurs at the moment when an arbitrary event occurs. That is, even if a client has performed an append, you can not immediately get or verify the results of that execution, and you can check it at any time when the server is ready. For this reason, developers who develop applications using the Append protocol should have an understanding of the following internal behaviors. The following discussion is about how and when a client detects asynchronous errors that occur in the server.

### Append Data Transfer

In a typical call such as SQLExecute or SQLExecDirect (), Machbase uses a synchronous scheme that returns the results back to the client immediately. However, SQLAppendDataV2 () does not send a request immediately after user data is entered. Instead, it waits until all of the client communication buffers are full, and then it sends the data to the client all at once. The reason for this design is that the input data of the client using Append assumes tens to hundreds of thousands of records per second, so it utilizes the buffering method for high-speed data transmission. For this reason, if the user wants to transmit the contents of the buffer at will, the user can input data explicitly by calling SQLAppendFlush () function.

### Append Data Error Check

As mentioned earlier, the Append protocol is buffered and operates asynchronously. In particular, it is very important to understand when and how an error is detected because it takes a method to detect an error only when an error occurs, without receiving any response when an error does not occur in the server. In addition, since the cost of detecting an error is relatively large, it is very inefficient to check each time a record is input, and currently Machbase is designed to detect an error only in the following cases explicitly. When an error is detected, the error callback function set by the user is called every time.
1. Checks after all the transmit buffers are full and the data has been explicitly sent to the server,
2. Checks after explicitly sending data to the server from within SQLAppendFlush ()
3. Checks just before shut down from within SQLAppendClose ()

In other words, it is basically designed to detect errors only in the above three cases, and is designed to minimize the occurrence of I/O.

### Additional Options for Checking Server Errors

In order to achieve the maximum performance, the default error detection technique can be more frequently checked and utilized by the user if desired. This can be done by adjusting the last argument to the SQLAppendOpen () function, aErrorCheckCount. When this value is 0, it does not perform any checking operation and operates basically. However, if this value is greater than 0, SQLAppendData () is explicitly checked for errors every time it is called. In other words, if this value is 10, you pay the cost of checking for errors every 10 appends. Therefore, when this value is small, system resources for error detection are used much, so it should be adjusted to an appropriate number.

### Leaving Trace Log When Server Error Occurs

If you want to leave a trace log for the append data where an error occurs, set the prepared property DUMP_APPEND_ERROR to 1 on the server. With this setting, the specification of the record that generated the error in the mach.trc file is written to the file. However, if the number of errors is excessive, the amount of system resources used will increase drastically, which may degrade the overall performance of Machbase.

### APPEND Function Description

#### SQLAppendOpen

```sql
SQLRETURN SQLAppendOpen(SQLHSTMT   aStatementHandle,
                        SQLCHAR   *aTableName,
                        SQLINTEGER aErrorCheckCount );
```

This function opens a channel for the target table. If this channel is not closed afterwards, it is kept open continuously.
A maximum of 1024 statements can be set for one connection. You can use SQLAppendOpen for each statement.

1. aStatementHandle: Represents the handle of the Statement to be appended.
2. aTableName: Indicates the name of the table to which Append will be performed.
3. aErrorCheckCount: Decides whether to check the server for errors whenever several data are input. If this value is 0, no error is checked arbitrarily.

#### SQLAppendData (deprecated)
`SQLRETURN  SQLAppendData(SQLHSTMT StatementHandle, void *aData[]);
`

This function is a function that inputs data for the channel.

* aData is an array containing pointers to the data to be input. The number of arrays must match the number of columns held by the table specified at Open.
* The return value can be SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, or SQL_ERROR.<br>
  In particular, if SQL_SUCCESS_WITH_INFO is returned, there may be errors such as a lengthy input column being truncated, so check the result again.

**Configuration According to Data Type**

Numeric and character types
* Types such as float, double, short, int, long long, and char * work well with pointers to their values.

Address type

* 0x04, 0x7f, 0x00, 0x00, 0x01 are entered in this order.
* In the case of ipv4, it is passed as an array of 5-byte unsigned char.
* The first byte is set to 4, the next 4 bytes are set to consecutive address values.
* For example, in the case of 127.0.0.1, five byte arrays **0x04, 0x7f, 0x00, 0x00, and 0x01** are entered in order.

```c
// For tables with four column information (short (16), int (32), long (64), varchar)

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

**Configuration According to Data Type**

datetime type

* Since Machbase internally has a nano-unit time resolution value, it must be converted when setting the time on the client, and it is expressed as a 64-bit unsigned integer value.<br>
  Therefore, for proper conversion, you need to add nano values ​​after converting to seconds using the UNIX library mktime.<br>
  ※ Machbase time = (total time (seconds) since January 1, 1970) * 1,000,000,000 + milli-second * 1,000,000 + micro-second * 1000 + nano-second;

```c
// Code if Date String is entered as "Year - Month - Date: Minute: Second Millis: Micro: Nano"

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

### SQLAppendDataByTime(deprecated)

```c
SQLRETURN  SQLAppendDataByTime(SQLHSTMT StatementHandle, SQLBIGINT aTime, void *aData[]);
```

This function is a function to input data for the corresponding channel, and the value of `_arrival_time` stored in the DB can be set to a specific time value instead of the current time.
For example, you want to enter the date in the log file a month ago as the date.

* aTime is a time value set to `_arrival_time`.
* aData is an array containing pointers to the data to be input.
* The number of arrays must match the number of columns held by the table specified at Open.

For the rest, refer to the SQLAppendData () function.

```c
// For tables with four column information (short (16), int (32), long (64), varchar)

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

### SQLAppendDataV2

```c
SQLRETURN  SQLAppendDataV2(SQLHSTMT StatementHandle, SQL_APPEND_PARAM *aData);
```

This function is a newly introduced Append function since Machbase 2.0. It is a convenient function that improves the input method inconvenient in existing functions.
In the case of TEXT and BINARY type introduced in 2.0 especially, input is possible only in SQLAppendDataV2 () function.

* Can input NULL for each type
* Can input string length when inputting VARCHAR
* Can input binary and string data when inputting IPv4 or IPv6
* Can specify data length for TEXT, BINARY type

The function arguments are structured as follows.

* aData is a pointer to an array of arguments called SQL_APPEND_PARAM. The number of this array must match the number of columns held by the table specified at Open.
* The return value can be SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, or SQL_ERROR. In particular, if SQL_SUCCESS_WITH_INFO is returned, there may be errors such as a lengthy input column being truncated, so check the result again.

Below is the definition of SQL_APPEND_PARAM that will actually be used in V2 , which is included in machbase_sqlcli.h.

```c
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

As you can see from the above, there is a structure in which a shared structure machbaseAppendParam which internally contains one argument. The length and value for the data and string can be explicitly entered for each data type. Examples of actual use are as follows.

**Fixed-Length Numeric Type Input**

Fixed-length numeric types are short, ushort, integer, uinteger, long, ulong, float, and double. This type can be entered by directly assigning a value to the structure member of SQL_APPEND_PARAM.

|Database Type|NULL Macro|SQL_APPEND_PARAM Member|
|--|--|--|
|SHORT|SQL_APPEND_SHORT_NULL|mShort|
|USHORT|SQL_APPEND_USHORT_NULL|mUShort|
|INTEGER|SQL_APPEND_INTEGER_NULL|mInteger|
|UINTEGER|SQL_APPEND_UINTEGER_NULL|mUInteger|
|LONG|SQL_APPEND_LONG_NULL|mLong|
|ULONG|SQL_APPEND_ULONG_NULL|mULong|
|FLOAT|SQL_APPEND_FLOAT_NULL|mFloat|
|DOUBLE|SQL_APPEND_DOUBLE_NULL|mDouble|

The following is an example of entering actual values.

```c
// Assume that the Table Schema consists of eight columns, SHORT, USHORT, INTEGER, UINTEGER, LONG, ULONG, FLOAT, and DOUBLE, respectively.

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

**Date Type Input**

Below is an example of inputting data of DATETIME type. Several macros are available for convenience.

Performs operations on the mDateTime member in SQL_APPEND_PARAM. The following macro can specify a date by setting a 64-bit integer value called mTime in the mDateTime structure.

```c
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

|Macro|Description|
|--|--|
|SQL_APPEND_DATETIME_NOW|Enters the current client time.|
|SQL_APPEND_DATETIME_STRUCT_TM|Sets a value to mTM, the struct tm structure of mDateTime, and inputs the value to the database.|
|SQL_APPEND_DATETIME_STRING|Sets a value for the string type of mDateTime and enters it into the database.<br><br>mDateStr: real date string value assigned<br>mFormatStr: format string assignment for date string|
|SQL_APPEND_DATETIME_NULL|Enters the value of the date column as NULL.|
|Any 64-bit Value|This value is entered as the actual datetime.<br><br>This value represents an integer value in nanoseconds since January 1, 1970.<br>For example, if this value is 1 billion (1,000,000,000), it represents 0: 1: 1 on January 1, 1970. (GMT)|

```c

// Assume that the table schema consists of eight columns, SHORT, USHORT, INTEGER, UINTEGER, LONG, ULONG, FLOAT, and DOUBLE, respectively.

void testAppendDateTimeFunc()
{
    SQL_APPEND_PARAM sParam[1];
    /* NULL Insert */
    sParam[0].mDateTime.mTime   = SQL_APPEND_DATETIME_NULL;
    SQLAppendDataV2(Stmt, sParam);

    /* Current Time */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_NOW;
    SQLAppendDataV2(Stmt, sParam);

    /* nano second since 1970/01/01 */
    sParam[0].mDateTime.mTime      = 1234;
    SQLAppendDataV2(Stmt, sParam);

    /* String format time */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRING;
    sParam[0].mDateTime.mDateStr   = "23/May/2014:17:41:28";
    sParam[0].mDateTime.mFormatStr = "DD/MON/YYYY:HH24:MI:SS";
    SQLAppendDataV2(Stmt, sParam);

    /* struct tm based time */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRUCT_TM;
    sParam[0].mDateTime.mTM.tm_year = 2000 - 1900;
    sParam[0].mDateTime.mTM.tm_mon  =  11;
    sParam[0].mDateTime.mTM.tm_mday  = 31;
    SQLAppendDataV2(Stmt, sParam);
}
```

**Internet Address Type Input**

The following is an example of inputting IPv4 and IPv6 type data. There are also several macros available for your convenience. Performs operations on the mLength member in SQL_APPEND_PARAM.

```c
/* for IPv4, IPv6 as bin or string representation */
typedef struct machbaseAppendIPStruct
{
unsigned char   mLength; /* 0:null, 4:ipv4, 6:ipv6, 255:string representation */
unsigned char   mAddr[16];
char           *mAddrString;
} machbaseAppendIPStruct;
```

|Macro (set on mLength)|Description|
|--|--|
|SQL_APPEND_IP_NULL|Enters a NULL value in the corresponding column|
|SQL_APPEND_IP_IPV4|mAddr has IPv4|
|SQL_APPEND_IP_IPV6|mAddr has IPv6|
|SQL_APPEND_IP_STRING|mAddrString has an address string.|

The following is an example of entering actual values for each case.

```c
void testAppendIPFunc()
{
SQL_APPEND_PARAM sParam[1];
/* NULL */
sParam[0].mIP.mLength  = SQL_APPEND_IP_NULL;
SQLAppendDataV2(Stmt, sParam);

    /* Direct array access */
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

**Variable Data Types (Character and Binary Data) Input**

Variable data types include VARCHAR and TEXT, and BLOB and CLOB. In existing functions, only VARCHAR was supported, and there was no way for the user to enter the length of the string. For that reason, we had to get the length through the strlen () function each time, but from function V2, the user can directly specify the length for the variable data type. Thus, if the user knows the length in advance, data can be input more quickly. Internally, the variable data type is a structure. However, for convenience of development, members are created separately for each data type.

```c
typedef struct machbaseAppendVarStruct
{
unsigned int mLength;
void *mData;
} machbaseAppendVarStruct;
```

When inputting a variable data type, set the length of the data to mLength and set the primitive data pointer to mData. If mLength is greater than the defined schema, it is automatically truncated. At this time, SQLAppendDataV2 () returns SQL_SUCCESS_WITH_INFO and also fills the internal structure with a related warning message. To see this warning message, use SQLError () function.

|Database Type|NULL Macro|SQL_APPEND_PARAM Member<br>(mVar is acceptable)|
|--|--|--|
|VARCHAR|SQL_APPEND_VARCHAR_NULL|mVarchar|
|TEXT|SQL_APPEND_TEXT_NULL|mText|
|JSON|SQL_APPEND_JSON_NULL|mJson|
|BINARY|SQL_APPEND_BINARY_NULL|mBinary|
|BLOB|SQL_APPEND_BLOB_NULL|mBlob|
|CLOB|SQL_APPEND_CLOB_NULL|mClob|

The following is an example of entering actual values for each environment. Assumes that there is one VARCHAR column.

```sql
CREATE TABLE ttt (name VARCHAR(10));
```

```c
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

The following is an example of inserting text type data.

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


### SQLAppendDataByTimeV2

```sql
SQLRETURN  SQLAppendDataByTimeV2(SQLHSTMT StatementHandle, SQLBIGINT aTime, SQL_APPEND_PARAM  *aData);
```

This function is a function to input data for the corresponding channel, and the value of `_arrival_time` stored in the DB can be set to a specific time value instead of the current time. For example, you want to enter the date in the log file a month ago as the date.

* aTime is the time value to be set to `_arrival_time`. You must enter the nano second value from January 1, 1970 to the present. Also, input values ​​must be sorted in order from the past to the present.
* aData is an array containing pointers to the data to be input. The number of arrays must match the number of columns held by the table specified at Open.

For the rest, refer to the SQLAppendDataV2 () function.

### SQLAppendDataV3 and SQLAppendDataByTimeV3

```c
SQLRETURN SQLAppendDataV3(SQLHSTMT aStmtHandle,
                          SQL_APPEND_PARAM *aData,
                          SQLINTEGER aColCount);

SQLRETURN SQLAppendDataByTimeV3(SQLHSTMT aStmtHandle,
                                SQLBIGINT aTime,
                                SQL_APPEND_PARAM *aData,
                                SQLINTEGER aColCount);
```

V3 uses the same `SQL_APPEND_PARAM` values as V2 and adds `aColCount`.
Use it when the number of values supplied by the client must be explicit instead of inferred only from the table metadata opened by `SQLAppendOpen`.

### SQLAppendBatch and SQLAppendBatchByTime

```c
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

Batch append sends a rectangular row set in one call. `aTypes` is an array of `SQL_APPEND_TYPE_*` values, and `aData` contains `aRowCount * aColCount` values in row order. `SQL_APPEND_TYPE_JSON` is available for JSON columns; BLOB and CLOB type entries are retained for variable binary/text payloads.

### SQLAppendFlush

```sql
SQLRETURN SQLAppendFlush(SQLHSTMT StatementHandle);
```

This function immediately sends the data accumulated in the current channel buffer to the Machbase server.

### SQLAppendClose
```sql
SQLRETURN SQLAppendClose(SQLHSTMT   aStmtHandle,
                         SQLBIGINT* aSuccessCount,
                         SQLBIGINT* aFailureCount);
```

This function closes the currently open channel. If an unopened channel exists, an error occurs.

* aSuccessCount: The number of successful Append records.
* aFailureCount: The number of failed Append records.

### SQLAppendSetErrorCallback

```sql
SQLRETURN SQLAppendSetErrorCallback(SQLHSTMT aStmtHandle, SQLAppendErrorCallback aFunc);
```

This function sets the callback function that is called when an error occurs during append. If you do not set this function, the client will ignore any errors that occur in the server.

* aStmtHandle: Specifies a Statement to check for errors.
* aFunc: Specifies the function pointer to call on Append failure.

The prototype for SQLAppendErrorCallback is:

```c
typedef void (*SQLAppendErrorCallback)(SQLHSTMT aStmtHandle,
                                     SQLINTEGER aErrorCode,
                                     SQLPOINTER aErrorMessage,
                                         SQLLEN aErrorBufLen,
                                     SQLPOINTER aRowBuf,
                                         SQLLEN aRowBufLen);
```

* aStatementHandle: the statement handle that generated the error
* aErrorCode: 32-bit error code that caused the error
* aErrorMessage: string for the error code
* aErrorBufLen: the length of aErrorMessage
* aRowBuf: a string containing the detailed description of the record that caused the error
* aRowBufLen: length of aRowBuf

**Example of Using Error Callback (dumpError)**

```c
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
    // Setting Callback.
    assert(SQLAppendSetErrorCallback(m_IStmt, dumpError) == SQL_SUCCESS);

    doAppend(sMaxAppend);

    if( SQLAppendClose(m_IStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        fprintf(stdout, "SQLAppendClose error\n");
        exit(-1);
    }
}
```

### SQLSetConnectAppendFlush

```sql
SQLRETURN SQL_API SQLSetConnectAppendFlush(SQLHDBC hdbc, SQLINTEGER option)
```

The data input by Append is written to the communication buffer and is sent to the server when the user calls the SQLAppendFlush function in the waiting state or the communication buffer becomes full. You can use this function if you want the user to send data by append to the server at regular intervals even if the buffer is not full. This function computes the difference between the last transmitted time and the current time every 100ms, and transfers the contents of the communication buffer to the server when the specified time (1 second if not set) has passed.

The parameters are:

* hdbc: DB connection handle.
* If option: 0, auto flush is off; otherwise, auto flush is on.

Executing on an unconnected hdbc will result in an error.

### SQLSetStmtAppendInterval
```sql
SQLRETURN SQL_API SQLSetStmtAppendInterval(SQLHSTMT hstmt, SQLINTEGER fValue)
```

Uses SQLSetConnectAppendFlush to turn off automatic flushing or flushing for a particular statement when you turn on flushing on a time unit.

The parameters are:

* hstmt: This is the statement handle that you want to adjust the flush interval.
* fValue: The value to which you want to adjust the flush interval. **If 0, flush is not performed and the unit is ms**. Set to a multiple of 100 since the thread that determines whether to flush every 100ms is executed. It does not automatically flush at exactly the right time. **1000 is the default value**.

Execution of this function will succeed even if time-based flush is not running.

**Error Check and Description**

This is a description of the code and how to check for errors when using the Append related functions. If the return value in the CLI function is not SQL_SUCCESS, you can check the error message using the following code.

```c
SQLINTEGER errNo;
int msgLength;
char sqlState[6];
char errMsg[1024];

if (SQL_SUCCESS == SQLError ( env, con, stmt, (SQLCHAR *)sqlState, &errNo,
(SQLCHAR *)errMsg, 1024, &msgLength ))
{
//set five length error code
printf("ERROR-%05d: %s\n", errNo, errMsg);
}
```

The error message returned from the Append related function is as follows.

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
      <td>Occurs when SQLAppendOpen is executed in duplicate.</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>Stream protocol termination failed.</td>
    </tr>
    <tr>
      <td>Failed to read protocol.</td>
      <td>A network read error occurred.</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>Invalid column meta information structure</td>
    </tr>
    <tr>
      <td>cannot allocate memory.</td>
      <td>An internal buffer memory allocation error occurred.</td>
    </tr>
    <tr>
      <td>cannot allocate compress memory.</td>
      <td>Compressed buffer memory allocation error occurred.</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>Return value has an error.</td>
    </tr>
    <tr>
      <td rowspan="3">SQLAppendData</td>
      <td>statement is not opened.</td>
      <td>Called AppendData without AppendOpen.</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>Occurs when you enter data that is larger than the size specified in the varchar type column.</td>
    </tr>
    <tr>
      <td>Failed to add binary.</td>
      <td>Write error in communication buffer occurred.</td>
    </tr>
    <tr>
      <td rowspan="5">SQLAppendClose</td>
      <td>statement is not opened.</td>
      <td>Not in AppendOpen state.</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>Stream protocol termination failed.</td>
    </tr>
    <tr>
      <td>Failed to close buffer protocol.</td>
      <td>Buffer protocol termination failed.</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>The column meta information structure is incorrect.</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>Return value has an error.</td>
    </tr>
    <tr>
      <td rowspan="2">SQLAppendFlush</td>
      <td>statement is not opened.</td>
      <td>Not in AppendOpen state</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>A network write error occurred.</td>
    </tr>
    <tr>
      <td rowspan="2">SQLSetErrorCallback</td>
      <td>statement is not opened.</td>
      <td>Not in AppendOpen state.</td>
    </tr>
    <tr>
      <td>Protocol Error (not APPEND_DATA_PROTOCOL)</td>
      <td>Communication buffer read result is not APPEND_DATA_PROTOCOL value.</td>
    </tr>
    <tr>
      <td rowspan="8">SQLAppendDataV2</td>
      <td>Invalid date format or date string.</td>
      <td>Occurs when the datetime type is wrong.</td>
    </tr>
    <tr>
      <td>statement is not opened.</td>
      <td>Not in AppendOpen state</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>This occurs when you enter data that is larger than the size specified in the binary type column.</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>Occurs when you enter data that is larger than the size specified in the varchar and text type column.</td>
    </tr>
    <tr>
      <td>Failed to add stream.</td>
      <td>Write error in communication buffer occurred.</td>
    </tr>
    <tr>
      <td>IP address length is invalid.</td>
      <td>The mLength value of the IPv4, IPv6 type structure is specified incorrectly.</td>
    </tr>
    <tr>
      <td>IP string is invalid.</td>
      <td>Not in IPv4 or IPv6 format.</td>
    </tr>
    <tr>
      <td>Unknown data type has been specified.</td>
      <td>Not the data type used by Machbase.</td>
    </tr>
  </tbody>
</table>

## Column wise parameter binding

The SQLAppend function, which is used to enter a large amount of data into Machbase quickly, can be used only when entering a log / tag table, and the SQLAppend function cannot be used to perform a bulk update on a lookup or volatile table.
For this purpose, Machbase 5.5 and later versions support column wise parameter binding. (Row wise format parameter binding is not yet supported.)
Set SQL_ATTR_PARAM_BIND_TYPE in the argument Attribute of the function SQLSetStmtAttr () and SQL_PARAM_BIND_BY_COLUMN in the parameter param.
For each column to bind, set the parameter to an array and the indicator variable to an array. Then call SQLBindParameter () with this parameter.
The figure below shows how columnar binding works for each parameter array.

<table>
  <thead>
    <tr>
      <th colspan="2">Column A<br>(parameter A)</th>
      <th colspan="2">Column B<br>(parameter B)</th>
      <th colspan="2">Column C<br>(parameter C)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Value_Array</td>
      <td>Indicator/<br><br>length array</td>
      <td>Value_Array</td>
      <td>Indicator/<br><br>length array</td>
      <td>Value_Array</td>
      <td>Indicator/<br><br>length array</td>
    </tr>
  </tbody>
</table>


```c
#define DESC_LEN 51
#define ARRAY_SIZE 10
SQLCHAR * Statement = "INSERT INTO Parts (PartID, Description, Price) VALUES (?, ?, ?)";

/* Array of parameters to bind */
SQLUINTEGER PartIDArray[ARRAY_SIZE];
SQLCHAR DescArray[ARRAY_SIZE][DESC_LEN];
SQLREAL PriceArray[ARRAY_SIZE];
/* Array of predicate variables to bind */
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

## Supported Strings

Machbase stores string data using UTF-8 by default.
In the case of Windows that inputs/outputs strings in methods other than UTF-8, ODBC converts them as follows.

|OS|Unicode/Non-Unicode|String Conversion|Note|
|--|--|--|--|
|Windows|Unicode (UTF-16)|UTF-16 ⟷ UTF-8|N/A|
|Windows|Non-Unicode (MBCS)|MBCS ⟷ UTF-8|Use the default string of Non-Unicode application in Windows settings|
|Linux|UTF-8|N/A|UTF-8 only supported|

## cli-odbc-example


## Application Development

### Check CLI Installation

If the following files are included in include and lib of the directory where Machbase is installed, the environment in which the application can be developed is complete.

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

### Makefile Creation Guide

```bash
mach@localhost:~/machbase_home$ cd sample/
mach@localhost:~/machbase_home/sample$ cd cli/
mach@localhost:~/machbase_home/sample/cli$ ls
Makefile sample1_connect.c
```

If the Machbase package was installed, the sample program will be installed in the following path.

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

### Compile and Link

Executing the following for a given sample creates an executable file.

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

> You can write your application as necessary by modifying the sample Makefile above

## Sample Program

### Connection Example

We will create an example program to connect using the CLI.
The sample file name is sample1_connect.c.
MACHBASE_PORT_NO must be the same as the PORT_NO value in the $MACHBASE_HOME/conf/machbase.conf file.

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

If you register sample1_connect.c in Makefile, compile and run it, it will appear as follows.

```bash
[mach@localhost cli]$ make

[mach@localhost cli]$ ./sample1_connect
connected ...
```

## Data Input and Output Example

In the example source below, we created a table using the CREATE TABLE statement, arbitrarily create simple data values, input data using the INSERT statement, and output the data using the SELECT statement. You will be able to see how to configure each type when entering and checking values ​​directly.
The sample file name is sample2_insert.c.

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


If you register sample2_insert.c in the Makefile, compile and run it, it will appear as follows.

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

### Prepare Execute Example

Let's write an example program that binds and INSERTs data.
You can enter a value by binding data in Machbase. When you use this, you need to specify the types of data values ​​clearly. In case of long string types, you must specify the length value.
The following example shows how to bind data for each type.
The file name is sample3_prepare.c.

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

If you register sample3_prepare.c in the Makefile, compile and run it, it will appear as follows.

```bash
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

### Extension Function Append Example

In Machbase, the append protocol is provided by reading a large amount of data from a file and inputting it at a high speed. Let's write an example program that uses this Append protocol.

First, let's look at an example of how to append to the various types provided by Machbase. The Append method has its own settings for each type. Therefore, if you know how to use every method, you will be able to write programs more efficiently. All the methods are listed in the example code at the bottom.

The file name is sample4_append1.c.

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

If you register sample4_append1.c in the Makefile, compile and run it, it will appear as follows.

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

Now let's use a fast append method using a file. This is an example useful for fast input of large amounts of logs, packets, etc. used in business. The file name is sample4_append2.c.

You have to save the data to be entered in advance in data.txt.

```bash
./make_data
```

Modifying the given make_data.c gives you the opportunity to create a data.txt file for your situation.

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

If you register sample4_append2.c in the Makefile, compile and run it, it will appear as follows.

```
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

### Acquiring Table Column Information Example

There are a number of ways to obtain table column information, but we will look at how to use SQLDescribeCol and SQLColumns.

#### SQLDescribeCol

The sample file name is sample5_describe.c.

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

If you add the above file and run make, you can see the contents of the column as shown below.

```
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

SQLColumns is a function that can find the information of the columns existing in the current table. Machbase also supports the above functions and can be used to find out the information of each column.

The file name is sample6_columns.c.


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

Add the above file and run make. The results are as follows.

```
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


### Multi-Thread Append Example

An example of using multiple threads in one program to append to multiple tables.

The file name is sample8_multi_session_multi_table.c.

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

Add the make code and run the executable file. Because the threads are used, the output order may be different. The results are as follows.

```
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

You can see the result through machsql as below.

```
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
