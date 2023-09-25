---
title: Java
type: docs
weight: 110
---

# How to use JDBC driver

JDBC driver is provided for Java developers.

## Install

Please refer to the [maven cetral repository](https://central.sonatype.com/artifact/com.machbase/machjdbc/{{ site.jdbc_version }}) for other build tool chains.

### maven

```xml
<dependency>
    <groupId>com.machbase</groupId>
    <artifactId>machjdbc</artifactId>
    <version>{{ site.jdbc_version }}</version>
</dependency>
```

### gradle

```
implementation group: 'com.machbase', name: 'machjdbc', version: '{{ site.jdbc_version }}'
```

### sbt

```
libraryDependencies += "com.machbase" % "machjdbc" % "{{ site.jdbc_version }}"
```

## Connect

```java
Class.forName("com.machbase.jdbc.driver");

Properties sProps = new Properties();
sProps.put("user", "sys");
sProps.put("password", "manager");

String sURL = "jdbc:machbase://localhost:5656/mhdb";
Connection conn = DriverManager.getConnection(sURL, sProps);
```