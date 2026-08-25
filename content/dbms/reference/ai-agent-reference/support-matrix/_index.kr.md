---
type: docs
title: '17.8.4 support-matrix'
weight: 40
toc: true
---

이 페이지는 Machbase의 핵심 기능 지원 여부를 요약한 매트릭스입니다. AI 에이전트가 "X Edition에서 Y 기능이 지원되나요?" 유형의 질문에 답할 때 참조합니다.

범례: O = 지원, △ = 제한적 지원, X = 미지원, - = 해당 없음

## 에디션 × 기능 지원표

| 기능 | Standard Edition | Cluster Edition |
|------|:----------------:|:---------------:|
| TAG 테이블 | O | O |
| LOG 테이블 | O | O |
| LOOKUP 테이블 | O | O |
| VOLATILE 테이블 | O | X |
| TRANSACTION 테이블 | O | X |
| ROLLUP | O | O |
| ROLLUP_REBUILD | O | X |
| ROWID / generated ROWID | O | X |
| 논리 다중 데이터베이스 | O | X |
| MOUNT / UMOUNT | O | X |
| 수평 확장 (Scale-out) | X | O |
| HA (고가용성) | X | O |
| Broker 노드 | X | O |
| Warehouse 노드 | X | O |

## 테이블 타입 × 기능 지원표

| 기능 | TAG | LOG | LOOKUP | VOLATILE | TRANSACTION |
|------|:---:|:---:|:------:|:--------:|:---:|
| INSERT (SQL) | O | O | O | O | O |
| Append API | O | O | O | X | O |
| UPDATE | 조건부¹ | X | O | O | O |
| DELETE | 제한적 | O | O | O | O |
| Transaction (COMMIT/ROLLBACK) | X | X | X | X | O |
| ROLLUP 대상 | O | X | X | X | X |
| 전문 검색 (TEXT INDEX) | X | O | X | X | X |
| JSON 컬럼 저장 | O | O | O | X | O |
| PRIMARY KEY | O (name) | X | O | O | O |
| BASETIME 컬럼 | O | - | - | - | - |
| ROWID 조회 | O | O | 조건부² | 조건부² | 조건부² |
| AUTO_INCREMENT | X | X | O | O | O |

> ¹ TAG 테이블 UPDATE: Standard Edition에서만 지원됩니다. data UPDATE는 태그 선택 조건
> (`name =`, `name IN`, `name LIKE`)과 하나 이상의 BASETIME 조건이 필요합니다. SET 대상은
> 실제 데이터 컬럼이며, PK(`name`), BASETIME, 메타데이터 컬럼은 data UPDATE로 수정할 수
> 없습니다. SET 우변은 기존 행 컬럼을 참조할 수 없습니다. 메타데이터는 `UPDATE ... METADATA`를 사용합니다.

> ² LOOKUP, VOLATILE, TRANSACTION의 ROWID는 0 이상의 단일 `LONG`/`INT64` PRIMARY KEY를
> 사용합니다. `AUTO_INCREMENT`는 선택 사항입니다.

## SDK × 주요 기능 지원표

| SDK | Append | Generated ROWID | AUTH KEY | Transaction API | Server Prepared | Named Bind API | Nullable Metadata |
|-----|:------:|:---------------:|:--------:|:---------------:|:---------------:|:--------------:|:-----------------:|
| JDBC | O | O | O | O | O | O | O |
| Python (machbaseAPI) | O | O | X | X | O³ | O | O |
| Go (machgo / native) | O | X | X | △⁴ | O | O | O |
| Go (database/sql) | △ | O | X | O | O | O | O |
| .NET (MachConnector) | O | O | X | X | X | △⁵ | O |
| Node.js | O | O | X⁶ | X | O | O | O |
| Machbase SQLCLI | O | O | O | △ | O | O | O |
| ODBC | O | X⁸ | O | △ | O | △⁷ | O |
| R (RODBC) | X | X | X | X | X | X | X |

> Go `database/sql`의 Append `△`는 표준 `sql.DB`/`sql.Tx` 기능이 아니라
> `sql.Conn.Raw()`에서 `machbase.Conn.Appender()`를 호출하는 neo-client 확장입니다.

> Generated ROWID는 Standard Edition의 단일 `INSERT ... VALUES`에만 제공됩니다. batch,
> `executemany()`, Append API, loader, `INSERT ... SELECT`, UPSERT에서는 반환하지 않습니다.

> ³ Python machbaseAPI 2.4는 `cursor(prepared=True)`로 동일 SQL의 server statement를
> 여러 `execute()`와 `executemany()` 호출에서 재사용합니다. cursor 하나는 statement
> 하나를 보유합니다. 일반 cursor의 `%s`와 `%(name)s`는 client-side 렌더링 방식이며,
> prepared cursor에서는 각각 `?`와 `:name`으로 변환하여 서버에 바인딩합니다.
> ⁴ Go `database/sql`은 기본 isolation level의 `Begin()` / `BeginTx()`를 지원합니다. Go native는
> 전용 트랜잭션 편의 메서드 대신 같은 연결에서 `BEGIN` / `COMMIT` / `ROLLBACK` SQL을 직접 실행합니다.
> ⁵ .NET 이름 컬렉션은 client-side typed literal 렌더링 후 ExecDirect를 사용합니다.
> ⁶ Node.js AUTH KEY: 현재 미지원.
> ⁷ SQLCLI는 이름 API를 제공하고 ODBC는 `:name` SQL을 ordinal로 바인딩합니다.
> ⁸ Generated ROWID는 Machbase SQLCLI 확장에서 제공됩니다. 표준 ODBC API 집합에는
> generated ROWID 조회 함수가 없습니다.
> JDBC는 Standard Edition TRANSACTION 테이블에서 `setAutoCommit(false)`, `commit()`과
> `rollback()`을 지원하며 첫 Statement에서 lazy `BEGIN`을 실행합니다. SQLCLI와 ODBC는 SQL
> `BEGIN` 또는 해당 transaction 제어 API의 지원 범위를 확인합니다.
> Nullable Metadata의 O는 SELECT 결과 컬럼 조회를 의미합니다. Go native는
> `api.Column.Nullability`, Go `database/sql`은 `Rows.ColumnTypeNullable()`을 사용합니다.

## PRIMARY KEY 메타데이터 지원

위의 테이블 타입별 `PRIMARY KEY` 행은 스키마 정의 지원을 나타냅니다. SELECT 결과 컬럼의
PRIMARY KEY 메타데이터는 SDK별 API가 별도로 제공됩니다.

| SDK | 결과 컬럼 PK 메타데이터 | 테이블 카탈로그 PK |
|-----|:----------------------:|:------------------:|
| JDBC | O | O |
| Python (machbaseAPI) | O | 카탈로그 SQL |
| Go (machgo / native) | O | 카탈로그 SQL |
| Go (database/sql) | 표준 API 없음 | 카탈로그 SQL |
| .NET (MachConnector40) | O | 카탈로그 SQL |
| Node.js | O | 카탈로그 SQL |
| ODBC | 별도 표준 API 없음 | `SQLPrimaryKeys()` |
| SQLCLI | 별도 표준 API 없음 | 카탈로그 SQL |

결과 컬럼 PK 플래그는 직접 참조한 PK 컬럼과 TAG `NAME`에만 적용되며, 표현식·집계식·외부
조인의 NULL 공급 측 컬럼에는 적용되지 않습니다. 이 메타데이터를 사용하려면 Machbase 8.7.0
서버와 해당 버전용 클라이언트 SDK를 함께 사용합니다.
