---
type: docs
title: '11.5.5 Append API'
weight: 50
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/append-api/
---

Machbase Append API는 LOG와 TAG 테이블에 여러 행을 연속 입력하는 대량 입력 API입니다.
JDBC에서는 `MachStatement` 확장 메서드로 사용합니다.

## API

| 메서드 | 설명 |
|--------|------|
| `executeAppendOpen(tableName, errorCheckCount)` | Append session을 시작하고 컬럼 메타데이터를 반환합니다. |
| `executeAppendData(metadata, data)` | 한 행을 전송합니다. |
| `executeAppendDataByTime(metadata, time, data)` | 나노초 시간을 지정해 한 행을 전송합니다. |
| `executeAppendFlush()` | pending 응답을 동기화합니다. |
| `executeAppendClose()` | Append session을 종료합니다. |
| `executeSetAppendErrorCallback(callback)` | 행 오류 callback을 등록합니다. |
| `getAppendSuccessCount()` | 성공한 행 수를 반환합니다. |
| `getAppendFailureCount()` | 실패한 행 수를 반환합니다. |

공개 `executeAppendData()`는 성공하면 `1`을 반환하고 유효하지 않은 내부 결과에는
`SQLException`을 던집니다. 최종 성공·실패 건수와 callback도 함께 확인합니다.

## 입력 예제

```sql
CREATE LOG TABLE sensor_data (
    time DATETIME,
    name VARCHAR(40),
    value DOUBLE
);
```

```java
import com.machbase.jdbc.MachStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.util.ArrayList;

try (MachStatement statement =
         (MachStatement) connection.createStatement()) {
    ResultSet appendResult =
        statement.executeAppendOpen("sensor_data", 100);
    ResultSetMetaData metadata = appendResult.getMetaData();

    statement.executeSetAppendErrorCallback(
        (errorNumber, errorMessage, rowMessage) ->
            System.err.printf(
                "Append error [%05d]: %s%n%s%n",
                errorNumber, errorMessage, rowMessage));

    long baseTime = System.currentTimeMillis() * 1_000_000L;

    for (int index = 0; index < 10_000; index++) {
        ArrayList<Object> row = new ArrayList<>();
        row.add(baseTime + index);
        row.add("sensor-" + (index % 10));
        row.add(20.0 + index * 0.001);

        int result = statement.executeAppendData(metadata, row);
        if (result != 1 && result != 2) {
            throw new SQLException(
                "Append failed at row " + index);
        }
    }

    statement.executeAppendFlush();
    statement.executeAppendClose();
    appendResult.close();

    System.out.printf("success=%d failure=%d%n",
        statement.getAppendSuccessCount(),
        statement.getAppendFailureCount());
}
```

## DATETIME

Append의 DATETIME 값은 epoch nanosecond 단위의 `long`으로 전달합니다.

```java
long epochNanoseconds =
    System.currentTimeMillis() * 1_000_000L;
```

`executeAppendDataByTime()`은 별도의 시간 값을 받는 테이블 입력 경로에서 사용합니다.
입력 컬럼 순서와 Java 타입은 `executeAppendOpen()`이 반환한 ResultSetMetaData에 맞춥니다.

## flush와 close

1. `executeAppendOpen()`으로 session을 시작합니다.
2. `executeAppendData()`를 반복 호출합니다.
3. 중간 확인이 필요하면 `executeAppendFlush()`를 호출합니다.
4. 모든 입력을 보낸 뒤 `executeAppendClose()`를 호출합니다.
5. 성공·실패 건수와 callback 결과를 확인합니다.

예외가 발생해도 Append session과 Statement가 닫히도록 try-with-resources와 `finally`를
사용합니다. callback에서는 실패 행을 별도 저장하거나 로깅하고, 무조건적인 재시도로
중복 입력을 만들지 않도록 업무 키를 사용합니다.

## 크기와 사용 범위

ordered append는 protocol packet 한도를 공유하므로 한 행의 전체 인코딩 크기를 64KiB
미만으로 유지합니다. BLOB/CLOB처럼 큰 값을 입력할 때는 행 크기와 클라이언트 메모리
사용량을 함께 확인합니다.

Append API는 TRANSACTION 테이블 입력에 사용하지 않습니다. rollback이 필요한 여러 DML은
[JDBC 트랜잭션](../transaction-pooling/)을 사용합니다.
