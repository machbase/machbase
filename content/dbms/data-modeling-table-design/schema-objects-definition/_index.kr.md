---
type: docs
title: '4.2 스키마 객체 정의'
weight: 20
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

먼저 [테이블 타입 선택](../table-types-selection-type/)을 완료합니다. 이 페이지는 선택한
타입에 맞게 테이블 이름, 컬럼, 키, 제약 조건, 인덱스와 VIEW를 정의합니다.

### 행의 단위와 컬럼의 역할

테이블 하나에서 행의 단위를 일정하게 유지합니다. 설비별 하루 요약과 초 단위 원본을
같은 의미의 행처럼 섞으면 `COUNT`나 `AVG`를 해석하기 어렵습니다. 원본과 집계에는
각각 명확한 행의 단위와 조회 이름을 부여합니다.

| 컬럼 역할 | 예 | 설계 원칙 |
|---|---|---|
| 대상 식별 | `sensor_id`, `equipment_id` | 표시 이름과 분리한 안정적인 값 사용 |
| 발생 기준 | `measured_at`, `event_time` | 실제 발생 시각인지 수신 시각인지 명시 |
| 측정값 | `temperature_c`, `pressure_kpa` | 단위, 유효 범위와 보정 방법 정의 |
| 품질 | `quality_code` | 값 누락, 측정 실패와 정상 0 구분 |
| 기준 속성 | 위치, 설비 종류 | 태그 메타데이터 또는 별도 기준표에서 관리할지 결정 |

외부 장비 코드처럼 업무에서 이미 사용하는 키는 자연키이고, 별도로 발급한 번호는
대리키입니다. 코드가 바뀔 수 있거나 여러 수집원이 같은 코드를 사용하면 식별 범위를
명확히 하거나 대리키를 검토합니다. 자동 증가 번호는 생성 순서를 위한 값이지 발생 시각이나
무중복 수집을 자동 보장하는 값이 아닙니다. TAG의 이름은 측정 행이 아닌 태그를 식별합니다.

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

새 컬럼을 추가한 뒤에는 기존 행과 이후 입력한 행을 각각 조회해 NULL·DEFAULT 결과를
확인합니다. 모든 테이블에서 기존 행이 DEFAULT로 채워지는 것은 아닙니다. 예를 들어
VOLATILE의 기존 행과 TAG 메타데이터의 자동 등록 행에는 별도 규칙이 있습니다.
[ARRAY의 DEFAULT 규칙](/dbms/reference/sql/type-data-types-dictionary/array/#default와-기존-row)을
포함해 실제 타입의 DDL 계약을 확인하십시오.

애플리케이션 배포와 스키마 변경의 순서도 정합니다. 가능한 입력 경로에서는 컬럼 목록을
명시하고, 위치 순서에 의존하는 Append와 바인딩 코드는 새 스키마와 대조합니다.
새 테이블로 이전하면 행 수뿐 아니라 키별 건수, 시간 범위, NULL 비율과 대표 집계도
비교하고, 전환 중 새로 들어오는 행의 누락·중복을 어떻게 처리할지 정합니다.

정확한 지원 범위와 구문은 [ALTER TABLE 사전](/dbms/reference/sql/syntax-dictionary-sql/)과
[테이블 타입별 지원 범위](/dbms/reference/support-scope-constraints/table-types-type/)를
참고하십시오.

<a id="selection-type-column-data-types"></a>

## 컬럼과 데이터 타입 선택

값의 실제 범위와 연산을 기준으로 가장 작은 적합 타입을 선택합니다. 표시 형식을 저장 타입과
혼동하지 마십시오.

| 데이터 | 권장 검토 타입 | 주의점 |
| --- | --- | --- |
| 정수 계측값·코드 | `SHORT`·`INTEGER`·`LONG` 계열 | NULL 예약값과 범위 확인 |
| 실수 계측값 | `FLOAT`·`DOUBLE` | 정밀도와 집계 오차 확인 |
| 정확한 소수 계산이 필요한 값 | `DECIMAL` | 전체 자릿수, 소수 자릿수와 반올림 규칙 확인 |
| 시각 | `DATETIME` | 시간대는 클라이언트·세션 정책과 함께 설계 |
| 짧은 문자열 | `VARCHAR` | 최대 길이와 인코딩 확인 |
| 긴 본문 | `TEXT` | 검색 방식과 인덱스 비용 확인 |
| 네트워크 주소 | `IPV4`·`IPV6` | 문자열 대신 주소 타입 사용 검토 |
| 구조화 문서 | `JSON` | 지원 함수와 크기 제한 확인 |
| 이진 데이터 | `BINARY` | 테이블 타입별 길이 제한 확인 |
| 고정 개수의 숫자 묶음 | 숫자 `ARRAY` | 요소 타입·길이, 요소별 NULL과 전체 NULL 구분 |

`VARCHAR(n)`의 길이는 바이트 수입니다. 한글이나 이모지를 포함하면 문자 수와 다를 수
있습니다. 정수 타입은 일부 경계값을 NULL 표현으로 예약하므로 일반 프로그래밍 언어의
정수 범위를 그대로 적용하지 않습니다. 금액은 필요한 자릿수의 DECIMAL을, 오차가 허용되는
계측값은 FLOAT/DOUBLE을 검토합니다. “작은 타입”보다 유효 범위와 연산 의미가 우선입니다.

전체 범위와 테이블 타입별 지원 여부는
[데이터 타입 사전](/dbms/reference/sql/type-data-types-dictionary/)을 기준으로 확인하십시오.

<a id="constraints-defaults-condition"></a>

## 제약 조건과 기본값

`PRIMARY KEY`, `NOT NULL`, `DEFAULT` 지원은 테이블 타입마다 다릅니다. 특히 TAG의
`PRIMARY KEY`는 태그 식별자, LOOKUP·VOLATILE·TRANSACTION의 `PRIMARY KEY`는 행 식별과
갱신 경로를 결정합니다.

NULL은 알 수 없거나 없는 값이고 0이나 빈 구간과 다릅니다. 측정 실패를 DEFAULT 0으로
대체하면 평균과 정상값 판정이 왜곡될 수 있습니다. `COUNT(*)`는 행 수, `COUNT(value)`는
그 컬럼이 NULL이 아닌 행 수이므로 표본 수를 보고할 때 구분합니다.

기본값은 생략한 입력에 대한 정책이며 값의 유효성 검사를 대신하지 않습니다. 테이블이
제공하지 않는 제약은 수집·업무 애플리케이션에서 검증합니다. 예를 들어 외래 키처럼
다른 DBMS의 제약을 이름만 보고 지원한다고 가정하지 말고
[TRANSACTION 지원 범위](/dbms/reference/support-scope-constraints/rdb/)를 확인합니다.

시스템이 제공하는 `_ARRIVAL_TIME`이나 `_RID` 같은 컬럼을 애플리케이션의 업무 키로 사용하지
마십시오. 공개된 조회 의미가 필요한 경우에만 참조하고, 시스템 컬럼의 저장 구조나 생성
방식에는 의존하지 않습니다.

<a id="index-create-delete"></a>

## 인덱스 설계

인덱스는 조회 비용을 낮추지만 입력과 저장 비용을 추가합니다.

대표 조회를 먼저 적고 조건에 맞는 행의 비율(선택도)을 확인합니다. 전체 설비의 한 달
평균과 설비 한 대의 특정 주문 조회는 접근 방식이 다릅니다. 필터·조인 컬럼마다 무조건
인덱스를 만들기보다 `EXPLAIN`과 실제 실행 시간을 비교해 도움이 되는 인덱스를 남깁니다.

- 시간 범위와 태그 식별자로 충분한 TAG 조회에는 추가 인덱스를 먼저 만들지 않습니다.
- LOG에서 자주 필터링하는 컬럼은 실제 실행 계획과 선택도를 측정한 뒤 인덱스를 검토합니다.
- LOOKUP·VOLATILE·TRANSACTION은 키 조회와 조인 조건을 기준으로 설계합니다.
- 긴 텍스트의 단어 검색은 해당 타입이 지원하는 `KEYWORD` 인덱스를 검토합니다.

생성·삭제 구문과 지원 타입은 [인덱스 SQL 사전](/dbms/reference/sql/syntax-dictionary-sql/)을
참고하십시오.

<a id="create-view"></a>

## VIEW 설계

VIEW는 반복해서 사용하는 조회에 이름을 부여하지만 결과 자체를 저장하지 않습니다. VIEW 정의에서
시간 범위가 고정되거나 불필요한 전체 컬럼을 읽지 않도록 하고, 기반 테이블이나 컬럼을
변경하기 전에 의존 VIEW를 확인하십시오.

자주 쓰는 컬럼 목록과 단위 변환을 VIEW로 일관되게 제공할 수 있습니다. 그러나 VIEW를
만든 것만으로 데이터가 복사되거나 조회 비용이 줄지는 않습니다. 과거 이벤트를 최신 기준표와
조인한 VIEW는 기준표가 바뀌면 과거 결과도 바뀔 수 있으므로, 발생 당시의 속성이 필요하면
버전별 기준 정보나 원본에 기록한 속성을 사용합니다.

VIEW 생성·조회·삭제와 제한은 [VIEW SQL 사전](/dbms/reference/sql/syntax-dictionary-sql/)을
참고하십시오.
