---
type: docs
title: '11.2 공통 연동 개념'
weight: 20
toc: true
aliases:
  - /dbms/application-integration/concepts-common/
---

드라이버나 언어에 관계없이 공통으로 적용되는 연결, 바인딩, 트랜잭션, 대량 입력, 오류 처리
원칙을 설명합니다. SDK별 함수명과 완전한 코드는 이 장의 SDK별 페이지를 정본으로 사용합니다.

<a id="connection-string-authentication"></a>

## 연결 문자열과 인증

연결에는 호스트, native 포트, 사용자, 인증 정보를 사용합니다. 기본 포트는 `5656`이지만
배포 환경의 `machbase.conf` 설정을 확인합니다.

| 항목 | 확인 사항 |
|------|-----------|
| 호스트·포트 | 애플리케이션 실행 위치에서 TCP 연결 가능 여부 |
| 사용자 | 대상 database와 테이블에 필요한 최소 권한 |
| 비밀번호 | 환경 변수나 secret manager로 주입 |
| database | SDK가 초기 database 선택을 지원하는지 확인 |
| timeout | 연결·명령·읽기 제한을 워크로드에 맞게 설정 |
| timezone | SDK와 서버가 지원하는 옵션명과 적용 범위 확인 |

예제의 `SYS`/`MANAGER`는 로컬 검증용입니다. 운영 애플리케이션에는 전용 계정을 만들고
소스, 명령 이력, 로그에 비밀번호를 기록하지 않습니다.

AUTH KEY는 비밀번호 대신 개인키로 challenge에 서명하는 방식입니다. 키 형식, 파일 권한,
SDK별 옵션은 [AUTH KEY 인증](/dbms/security-access-control/authentication-auth-key/)과
해당 드라이버 문서를 함께 확인합니다.

pool을 사용하면 반환된 연결의 current database, session 설정, 열린 statement가 다음
요청에 영향을 주지 않도록 reset 동작을 검증합니다.

<a id="timezone-connection"></a>

## 타임존과 시간값

Machbase `DATETIME`은 nanosecond 정밀도를 지원합니다. 애플리케이션에서는 시간값의 의미와
표현을 분리해 관리합니다.

- 수집 시각의 기준대(UTC 또는 업무 지역)를 명시합니다.
- 문자열을 바인딩할 때 format과 timezone을 함께 고정합니다.
- epoch 값을 전달할 때 SDK가 요구하는 단위가 초, 밀리초, 마이크로초, 나노초 중 무엇인지
  확인합니다.
- 조회 문자열의 timezone은 connection 옵션이나 `TO_CHAR()` 등 실제 사용 경로에서
  왕복 테스트합니다.
- `NOW`와 `SYSDATE`를 업무 규칙에 혼용하지 말고 필요한 의미를 SQL 레퍼런스에서 확인합니다.

문자열 왕복 검증은 동일한 connection에서 입력값, 조회값, timezone 변경 후 조회값을
비교합니다. 상세 함수는 [SQL 함수](/dbms/reference/sql/dictionary/functions-full/)를
참고합니다.

<a id="prepared-statement"></a>

## Prepared statement

Prepared statement는 SQL 구조와 값을 분리하고 같은 SQL을 반복 실행할 때 사용합니다.

```text
INSERT INTO sensor_data VALUES (?, ?, ?)
SELECT value FROM sensor_data WHERE name = ? AND time >= ?
```

statement를 준비한 connection과 current database가 바뀌지 않았는지 확인하고, 사용 후
close합니다. statement cache를 제공하는 SDK는 cache 범위와 eviction, database 전환 시
reset 동작을 확인합니다.

CTE, LIMIT 등 문법 위치에 따라 parameter marker가 허용되지 않을 수 있습니다. 문법 오류가
나면 값을 문자열로 합치기 전에 [Named Bind Parameter](/dbms/reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/)와
해당 SDK의 marker 지원 범위를 확인합니다.

<a id="parameter-binding"></a>

## Parameter binding

| 값 종류 | 권장 방식 |
|---------|-----------|
| 정수·실수 | 언어의 고정 폭 타입과 SQL 타입 범위를 맞춤 |
| 문자열 | encoding과 최대 길이를 확인 |
| DATETIME | SDK의 시간 객체 또는 명시된 epoch 단위 사용 |
| NULL | 언어별 NULL 표현과 SQL 타입을 함께 지정 |
| DECIMAL | 문자열 변환보다 SDK의 정확한 고정소수 타입을 우선 |
| binary·IP | SDK가 요구하는 byte 배열 또는 전용 타입 사용 |

positional marker `?`는 등장 순서대로 값을 바인딩합니다. named marker `:name`은 지원하는
서버와 SDK에서만 사용하며, 같은 이름의 반복 처리 규칙을 확인합니다. 식별자나 SQL keyword는
값 parameter로 바인딩할 수 없으므로 허용 목록으로 검증한 뒤 SQL을 구성합니다.

<a id="dml-affected-rows"></a>

## DML 영향 행 수

`INSERT`, `UPDATE`, `DELETE` 뒤에는 SDK가 반환한 영향 행 수를 확인합니다. 성공 응답만으로
업무 대상이 실제 변경됐다고 가정하지 않습니다.

- 단건 변경은 기대값이 1인지 확인합니다.
- 0건이면 조건 불일치, 이미 반영된 상태, 권한·테이블 타입 제약을 구분합니다.
- 일괄 변경은 실행 전 같은 조건의 `COUNT(*)`로 범위를 확인합니다.
- Append는 SQL 영향 행 수 대신 close·ack의 성공 건수와 실패 건수를 확인합니다.

<a id="transaction"></a>

## 트랜잭션

명시적 `BEGIN`, `COMMIT`, `ROLLBACK`은 TRANSACTION 테이블의 관계형 DML에 사용합니다.
LOG·TAG Append를 같은 rollback 단위로 가정하지 않습니다.

1. 실제 SDK가 transaction API를 제공하는지 확인합니다.
2. 제공하지 않으면 지원되는 SQL 제어 구문을 같은 connection에서 실행합니다.
3. 오류 경로에서 rollback하고 connection을 재사용할 수 있는지 확인합니다.
4. pool 반환 전에 미완료 transaction이 남지 않도록 합니다.
5. 여러 테이블 타입을 섞은 작업은 각 statement의 commit 범위를 사전 검증합니다.

완전한 SQL 예제는
[TRANSACTION 테이블의 트랜잭션](/dbms/rdb-table-usage/transaction/)을 참고합니다.

<a id="append-api-batch"></a>

## Append API와 batch

입력 방식 선택과 결과 확인 항목은 [데이터 입력과 반출](../data-input-load-export/)에서,
client·table type별 Append gate는
[SDK Append matrix](../sdk-support-scope/#append-table-type-matrix)에서 다룹니다. 이 페이지에는
공통 원칙만 유지합니다. Append connection은 일반 query connection과 분리하고 flush·close와
실패 row를 확인합니다.

<a id="error-handling-retry"></a>

## 오류 처리와 재시도

오류는 연결, 인증·권한, SQL·스키마, 데이터, 자원 부족으로 분류합니다.

- 연결 단절과 일시적 timeout만 제한된 횟수와 backoff로 재시도합니다.
- 인증 실패, 권한 부족, 문법 오류, 타입 오류는 수정 전 자동 재시도하지 않습니다.
- 재시도 전에 statement·cursor·Append handle과 connection을 정리합니다.
- INSERT 재시도는 업무 키나 중복 처리 정책으로 멱등성을 확보합니다.
- 서버 오류 코드와 message는 기록하되 자격 증명과 원문 민감 데이터는 제거합니다.
- pool에서 오류가 난 connection은 유효성 검사 후 반환하거나 폐기합니다.

운영 오류 분류와 진단 순서는 [문제 해결](/dbms/troubleshooting/)을 참고합니다.
