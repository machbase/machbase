---
type: docs
title: '4.1 스키마 객체 정의'
weight: 10
toc: true
---
이 페이지는 테이블, 컬럼, 인덱스와 VIEW를 설계할 때 결정할 항목을 정리합니다. SQL 문법과
옵션을 중복해서 나열하지 않고 [SQL 문법 사전](/dbms/reference/sql/syntax-dictionary-sql/)을
정본으로 사용합니다.

- **[테이블 생성과 삭제](#create-delete)**
- **[테이블 변경](#alter)**
- **[컬럼과 데이터 타입 선택](#selection-type-column-data-types)**
- **[제약 조건과 기본값](#constraints-defaults-condition)**
- **[인덱스 설계](#index-create-delete)**
- **[VIEW 설계](#create-view)**

<a id="create-delete"></a>

## 테이블 생성과 삭제

먼저 데이터의 역할에 맞는 테이블 타입을 선택합니다.

| 데이터 역할 | 시작할 타입 | 필수 설계 요소 |
| --- | --- | --- |
| 센서·계측 시계열 | TAG | 태그명 `PRIMARY KEY`, 시간 또는 거리 축 |
| 이벤트·로그 | LOG | 이벤트 컬럼, 필요하면 실제 발생 시각 컬럼 |
| 관계형 업무 데이터 | TRANSACTION | 업무 키, 제약 조건과 트랜잭션 범위 |
| 기준·메타데이터 | LOOKUP | `PRIMARY KEY`, 메모리 사용량 |
| 재생성 가능한 상태 캐시 | VOLATILE | `PRIMARY KEY`, 재시작 후 복구 경로 |

테이블 이름은 영문자, 숫자와 밑줄을 사용하고 영문자로 시작하도록 정합니다. 예약어 또는
시스템 객체와 혼동할 수 있는 이름은 피하십시오. 삭제 전에는 의존하는 VIEW, 인덱스,
ROLLUP과 보존 정책을 확인합니다.

타입별 생성 예제는 다음 문서를 참고하십시오.

- [TAG 테이블 생성](/dbms/tag-table-usage/create-alter-drop/)
- [LOG 테이블 생성](/dbms/log-table-usage/create-alter-drop/)
- [TRANSACTION 테이블](/dbms/rdb-table-usage/)
- [LOOKUP 테이블](/dbms/lookup-table-usage/)
- [VOLATILE 테이블](/dbms/volatile-table-usage/)

<a id="alter"></a>

## 테이블 변경

테이블 타입과 데이터 유무에 따라 컬럼 추가·삭제·이름 변경·타입 변경의 지원 범위가
다릅니다. 운영 테이블을 변경하기 전에 다음 순서로 판단하십시오.

1. 대상 Edition과 테이블 타입이 해당 `ALTER TABLE` 동작을 지원하는지 확인합니다.
2. 기존 데이터, 인덱스, VIEW와 애플리케이션의 컬럼 순서 의존성을 확인합니다.
3. 운영과 같은 스키마·데이터량의 검증 환경에서 실행 시간과 잠금 영향을 측정합니다.
4. 되돌리기 어렵다면 새 테이블을 만들고 검증 후 전환하는 방식을 사용합니다.

정확한 지원 범위와 구문은 [ALTER TABLE 사전](/dbms/reference/sql/syntax-dictionary-sql/)과
[테이블 타입별 관리 범위](../table-types-type-manageable/)를 참고하십시오.

<a id="selection-type-column-data-types"></a>

## 컬럼과 데이터 타입 선택

값의 실제 범위와 연산을 기준으로 가장 작은 적합 타입을 선택합니다. 표시 형식을 저장 타입과
혼동하지 마십시오.

| 데이터 | 권장 검토 타입 | 주의점 |
| --- | --- | --- |
| 정수 계측값·코드 | `SHORT`·`INTEGER`·`LONG` 계열 | NULL 예약값과 범위 확인 |
| 실수 계측값 | `FLOAT`·`DOUBLE` | 정밀도와 집계 오차 확인 |
| 시각 | `DATETIME` | 시간대는 클라이언트·세션 정책과 함께 설계 |
| 짧은 문자열 | `VARCHAR` | 최대 길이와 인코딩 확인 |
| 긴 본문 | `TEXT` | 검색 방식과 인덱스 비용 확인 |
| 네트워크 주소 | `IPV4`·`IPV6` | 문자열 대신 주소 타입 사용 검토 |
| 구조화 문서 | `JSON` | 지원 함수와 크기 제한 확인 |
| 이진 데이터 | `BINARY` | 테이블 타입별 길이 제한 확인 |

전체 범위와 테이블 타입별 지원 여부는
[데이터 타입 사전](/dbms/reference/sql/type-data-types-dictionary/)을 기준으로 확인하십시오.

<a id="constraints-defaults-condition"></a>

## 제약 조건과 기본값

`PRIMARY KEY`, `NOT NULL`, `DEFAULT` 지원은 테이블 타입마다 다릅니다. 특히 TAG의
`PRIMARY KEY`는 태그 식별자, LOOKUP·VOLATILE·TRANSACTION의 `PRIMARY KEY`는 행 식별과
갱신 경로를 결정합니다.

시스템이 제공하는 `_ARRIVAL_TIME`이나 `_RID` 같은 컬럼을 애플리케이션의 업무 키로 사용하지
마십시오. 공개된 조회 의미가 필요한 경우에만 참조하고, 시스템 컬럼의 저장 구조나 생성
방식에는 의존하지 않습니다.

<a id="index-create-delete"></a>

## 인덱스 설계

인덱스는 조회 비용을 낮추지만 입력과 저장 비용을 추가합니다.

- 시간 범위와 태그 식별자로 충분한 TAG 조회에는 추가 인덱스를 먼저 만들지 않습니다.
- LOG에서 자주 필터링하는 컬럼은 실제 실행 계획과 선택도를 측정한 뒤 인덱스를 검토합니다.
- LOOKUP·VOLATILE·TRANSACTION은 키 조회와 조인 조건을 기준으로 설계합니다.
- 긴 텍스트의 단어 검색은 해당 타입이 지원하는 `KEYWORD` 인덱스를 검토합니다.

생성·삭제 구문과 지원 타입은 [인덱스 SQL 사전](/dbms/reference/sql/syntax-dictionary-sql/)을
참고하십시오.

<a id="create-view"></a>

## VIEW 설계

VIEW는 반복 쿼리의 이름과 권한 경계를 제공하지만 결과를 저장하지 않습니다. VIEW 정의에서
시간 범위가 고정되거나 불필요한 전체 컬럼을 읽지 않도록 하고, 기반 테이블이나 컬럼을
변경하기 전에 의존 VIEW를 확인하십시오.

VIEW 생성·조회·삭제와 제한은 [VIEW SQL 사전](/dbms/reference/sql/syntax-dictionary-sql/)을
참고하십시오.
