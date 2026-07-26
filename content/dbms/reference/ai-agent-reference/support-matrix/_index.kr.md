---
type: docs
title: '17.10.4 support-matrix'
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
| STREAM | O | X |
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

> ¹ TAG 테이블 UPDATE: data UPDATE는 태그 선택 조건(`name =`, `name IN`, `name LIKE`)과
> BASETIME 조건이 모두 필요합니다. SET 대상은 실제 데이터 컬럼이며, PK(`name`), BASETIME,
> 메타데이터 컬럼은 data UPDATE로 수정할 수 없습니다. 메타데이터는 `UPDATE ... METADATA`를 사용합니다.

## SDK × 주요 기능 지원표

| SDK | Append | AUTH KEY | Transaction API | Server Prepared | Named Bind API | Nullable Metadata |
|-----|:------:|:--------:|:---------------:|:---------------:|:--------------:|:-----------------:|
| JDBC | O | O | △ | O | O | O |
| Python (machbaseAPI) | O | X | X | O² | O | O |
| Go (machcli / native) | O | X | X³ | O | X | X |
| Go (database/sql) | X | X | X³ | O | X | X |
| .NET (MachConnector) | O | X | X | X | △⁴ | O |
| Node.js | O | X⁵ | X | O | O | O |
| REST API | O | X | X | X | X | X |
| ODBC/CLI | O | O | △ | O | △⁶ | O |
| R (RODBC) | X | X | X | X | X | X |

> ² Python machbaseAPI는 서버 prepare/bind를 지원합니다. `execute()`는 호출마다
> prepare/execute/close하고, `executemany()`는 한 번 prepare한 statement를 호출 내부에서
> 재사용합니다. 공개 `prepare()` 객체는 없습니다. `%s`와 `%(name)s`는 기존 client-side
> 렌더링 방식입니다.
> ³ Go driver (machcli, database/sql 모두): `Begin()` / `BeginTx()` 미구현.
> ⁴ .NET 이름 컬렉션은 client-side typed literal 렌더링 후 ExecDirect를 사용합니다.
> ⁵ Node.js AUTH KEY: 현재 미지원.
> ⁶ SQLCLI는 이름 API를 제공하고 ODBC는 `:name` SQL을 ordinal로 바인딩합니다.
> JDBC와 ODBC/CLI 트랜잭션은 SQL `BEGIN`을 직접 실행해야 합니다. JDBC
> `setAutoCommit(false)`는 시작 문을 보내지 않으며, ODBC autocommit 속성도 서버 트랜잭션을
> 자동으로 시작하지 않습니다.
> Nullable Metadata의 O는 SELECT 결과 컬럼 조회를 의미합니다. Prepared Parameter의
> Nullable 상태는 Native MachCLI, SQLCLI/ODBC와 JDBC에서 조회할 수 있습니다.
