---
type: docs
title: '17.7.2.6 마이그레이션과 문제 해결'
weight: 60
toc: true
---

최신 Machbase JDBC는 Java 8/JDBC 4.2를 기준으로 버전 보고, metadata, 타입 변환,
트랜잭션과 자원 수명주기를 표준 JDBC 계약에 맞춥니다. 이전 동작에 의존하는
애플리케이션은 다음 차이를 확인합니다.

## 이전 드라이버에서 전환

| 영역 | 현재 동작 | 애플리케이션 확인 사항 |
|------|-----------|------------------------|
| Java/JDBC 기준 | Java 8 bytecode, JDBC 4.2 보고 | 실행 JDK를 Java 8 이상으로 사용합니다. |
| 드라이버 버전 | driver와 metadata가 3.0.0 보고 | 버전 판별 로직을 갱신합니다. |
| 자동 검색 | JDBC service provider 제공 | 명시적 `Class.forName()`은 선택 사항입니다. |
| ParameterMetaData | JDBC precision, DB type name과 Java class 반환 | 저장 byte 크기에 의존하지 않습니다. |
| 트랜잭션 | lazy `BEGIN`, 실제 commit/rollback | Standard TRANSACTION 작업을 명시적으로 완료합니다. |
| holdability | `CLOSE_CURSORS_AT_COMMIT` | commit 후 ResultSet을 다시 조회합니다. |
| DatabaseMetaData | 표준 result shape와 capability 반환 | vendor ordinal 대신 column label을 사용합니다. |
| 타입 API | typed `getObject()`, `JDBCType`, Boolean, unsigned, LOB | metadata의 Java class로 조회·바인딩합니다. |
| 오류 | 잘못된 상태에서 표준 `SQLException` 반환 | SQLState로 오류를 분기합니다. |
| timeout | query/network timeout 지원 | network timeout 뒤 연결을 폐기합니다. |
| 커넥션 풀 | logical lease와 상태 reset | close한 handle과 metadata를 재사용하지 않습니다. |

named bind는 호환 서버에서 사용합니다. 이전 서버가 이름 기반 bind를 지원하지 않으면
SQLState `0A000`이 발생하므로 `?` positional parameter로 전환합니다.

## 미지원 기능

다음 JDBC 선택 기능은 지원하지 않습니다.

- savepoint
- generated keys
- XA와 분산 트랜잭션
- stored procedure와 CallableStatement 성공 경로
- scrollable 또는 updateable ResultSet
- Statement pooling
- multiple open results
- Array, Struct, Ref, RowId, SQLXML과 UDT type map
- 별도 NClob storage와 factory
- Machbase 전용 RowSet provider
- JDBC 4.3 sharding과 request boundary API

미지원 기능은 일반적으로 `SQLFeatureNotSupportedException`과 SQLState `0A000`을
반환합니다. 기능을 호출하기 전에 DatabaseMetaData capability를 확인합니다.

## `No suitable driver`

**증상**

`DriverManager.getConnection()`에서 `No suitable driver`가 발생합니다.

**확인 및 해결**

1. 실행 classpath에 `machbase.jar`가 있는지 확인합니다.
2. JAR에 `META-INF/services/java.sql.Driver`가 있는지 확인합니다.
3. URL이 `jdbc:machbase://<host>:<port>/machbasedb` 형식인지 확인합니다.
4. 여러 버전의 Machbase JDBC JAR가 동시에 포함되지 않았는지 확인합니다.

## SQLState `0A000`

선택한 기능이나 서버 protocol이 해당 API를 지원하지 않습니다. savepoint, generated keys,
scrollable cursor와 XA에는 대체 흐름을 사용합니다. named bind에서 발생하면 positional
parameter인 `?`를 사용합니다.

## commit 이후 ResultSet이 닫힘

정상 동작입니다. Machbase의 transaction holdability는
`CLOSE_CURSORS_AT_COMMIT`입니다. commit 전에 결과를 소비하거나 commit 후 query를 다시
실행합니다. Statement와 PreparedStatement는 다시 사용할 수 있습니다.

## LOG DML이 rollback되지 않음

manual transaction에서 TRANSACTION 테이블을 변경하기 전에 실행한 첫 LOG DML은 호환
경로에서 auto-commit으로 재실행될 수 있습니다. 이 입력은 이후 rollback 대상이 아닙니다.
rollback이 필요한 데이터는 TRANSACTION 테이블을 사용합니다.

## 여러 TRANSACTION 테이블을 함께 commit

정상적인 commit과 rollback은 지원하지만 backend commit 중 장애가 발생했을 때 여러
TRANSACTION 테이블의 전역 원자성을 보장하지 않습니다. 중요한 원자 작업은 하나의
TRANSACTION 테이블 범위로 설계합니다.

## network timeout 또는 연결 오류

socket read timeout과 SQLState class `08` 연결 오류가 발생하면 해당 물리 연결을
재사용하지 않습니다. 커넥션 풀에서 새 연결을 대여하고, 활성 트랜잭션은 업무 멱등성
정책에 따라 처음부터 다시 실행합니다. commit 성공 여부를 예외만으로 추정하지 않습니다.

## close한 pool 객체 재사용

logical Connection을 닫은 뒤 그 Connection에서 얻은 Statement, ResultSet과
DatabaseMetaData를 다음 lease에서 재사용하면 SQLState `08003`이 발생합니다. 각 lease의
객체를 try-with-resources 범위 안에서만 사용합니다.
