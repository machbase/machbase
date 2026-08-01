---
type: docs
title: '17.7.2.4 DatabaseMetaData'
weight: 40
toc: true
---

`Connection.getMetaData()`는 드라이버, 서버, 스키마 객체와 JDBC capability 정보를
반환합니다. 결과 컬럼은 JDBC 표준 이름과 순서를 사용하므로 숫자 위치보다 column label로
읽는 것을 권장합니다.

```java
import java.sql.DatabaseMetaData;

DatabaseMetaData metadata = connection.getMetaData();

System.out.println(metadata.getDriverName());
System.out.println(metadata.getDriverVersion());
System.out.println(metadata.getDatabaseProductName());
System.out.println(metadata.getDatabaseProductVersion());
```

## 테이블과 VIEW

```java
try (ResultSet tables = metadata.getTables(
         null, null, "%", new String[] {"TABLE", "VIEW"})) {
    while (tables.next()) {
        System.out.printf("%s %s%n",
            tables.getString("TABLE_NAME"),
            tables.getString("TABLE_TYPE"));
    }
}
```

`getTables()`는 TABLE과 VIEW를 구분합니다. Machbase 세부 테이블 종류는 `REMARKS`에서
확인합니다. 애플리케이션은 특정 ordinal에 의존하지 말고 표준 column label을 사용합니다.

## 컬럼

```java
try (ResultSet columns = metadata.getColumns(
         null, null, "SENSOR_TX", "%")) {
    while (columns.next()) {
        System.out.printf(
            "%s %s size=%d nullable=%s%n",
            columns.getString("COLUMN_NAME"),
            columns.getString("TYPE_NAME"),
            columns.getInt("COLUMN_SIZE"),
            columns.getString("IS_NULLABLE"));
    }
}
```

`NULLABLE`은 숫자 상수, `IS_NULLABLE`은 `YES`, `NO` 또는 빈 문자열로 반환됩니다.
LOOKUP과 VOLATILE 테이블의 PRIMARY KEY는 명시적인 NOT NULL 절이 없어도
`columnNoNulls`와 `NO`로 반환됩니다.

VARCHAR, DATETIME, BINARY, BLOB과 CLOB처럼 수치 속성이 적용되지 않는 컬럼의
`DECIMAL_DIGITS`와 `NUM_PREC_RADIX`는 SQL NULL입니다. `getInt()`의 0만 확인하지 말고
`getObject()` 또는 `wasNull()`로 NULL 여부를 확인합니다.

## PRIMARY KEY와 인덱스

```java
try (ResultSet keys = metadata.getPrimaryKeys(
         null, null, "SENSOR_TX")) {
    while (keys.next()) {
        System.out.printf("%s position=%d%n",
            keys.getString("COLUMN_NAME"),
            keys.getShort("KEY_SEQ"));
    }
}

try (ResultSet indexes = metadata.getIndexInfo(
         null, null, "SENSOR_TX", false, false)) {
    while (indexes.next()) {
        System.out.printf("%s %s%n",
            indexes.getString("INDEX_NAME"),
            indexes.getString("COLUMN_NAME"));
    }
}
```

PRIMARY KEY 여부를 `ResultSetMetaData.isNullable()` 값으로 추정하지 않습니다.
`getPrimaryKeys()`와 `getIndexInfo()`를 사용합니다.

## 스키마와 타입 정보

다음 메서드는 JDBC 표준 형태의 ResultSet을 반환합니다.

- `getSchemas()`, `getCatalogs()`, `getTableTypes()`
- `getTypeInfo()`
- `getTables()`, `getColumns()`
- `getPrimaryKeys()`, `getIndexInfo()`

지원하지 않는 선택적 metadata 조회는 null이나 비표준 ResultSet 대신 표준 컬럼을 가진 빈
ResultSet을 반환할 수 있습니다. 기능을 사용하기 전에 capability 메서드를 확인합니다.

```java
if (metadata.supportsSavepoints()) {
    // 지원되는 환경에서만 savepoint를 사용합니다.
}
```

## catalog

`Connection.getCatalog()`과 `setCatalog()`은 드라이버가 노출하는 현재 catalog 값을
관리합니다. metadata 메서드의 catalog 인자는 이 값과 일치하는 요청을 필터링하는 데
사용합니다.

```java
String initialCatalog = connection.getCatalog();
connection.setCatalog(initialCatalog);
```

커넥션 풀에서 logical Connection을 반환하면 catalog는 URL에서 결정한 초기 값으로
복원됩니다. 이전 lease에서 얻은 DatabaseMetaData 객체는 다음 lease에서 재사용하지
않습니다.

## 지원 범위 확인

Machbase JDBC는 실제 지원 범위를 capability에 반영합니다. 예를 들어 트랜잭션 격리 수준,
ResultSet 종류, savepoint, generated key와 multiple open results 지원 여부를 다음과 같이
확인합니다.

```java
System.out.println(metadata.supportsTransactions());
System.out.println(metadata.supportsTransactionIsolationLevel(
    Connection.TRANSACTION_SERIALIZABLE));
System.out.println(metadata.supportsResultSetType(
    ResultSet.TYPE_FORWARD_ONLY));
System.out.println(metadata.supportsSavepoints());
System.out.println(metadata.supportsGetGeneratedKeys());
System.out.println(metadata.supportsMultipleOpenResults());
```

`Driver.jdbcCompliant()`이 `false`인 것과 개별 JDBC API의 지원 여부는 별개입니다.
애플리케이션은 필요한 capability를 직접 확인합니다.
