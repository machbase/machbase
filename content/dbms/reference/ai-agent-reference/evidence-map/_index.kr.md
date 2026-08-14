---
type: docs
title: '18.10.6 evidence-map'
weight: 60
toc: true
---

이 페이지는 Machbase에 관한 기술적 사실의 근거(소스)를 매핑합니다. AI 에이전트가 사실에 근거한 답변을 생성하거나, 답변의 출처를 명시할 때 참조합니다.

## 다중 데이터베이스

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| 하나의 Standard 인스턴스에서 여러 logical database를 사용하며 기본 DB는 `MACHBASEDB` | dbms-nfx #3235 / PR #3977 최종 user manual | Cluster/XMA와 물리 자원 격리는 범위 밖 |
| 객체 이름은 `table`, `owner.table`, `database.owner.table`이며 `db.table`은 owner.table | dbms-nfx #3235 최종 parser·regression·user manual | 3-part 이름으로 다른 DB를 명시 |
| `DATABASE_ID`는 logical catalog ID이고 `TABLESPACE_ID`와 다름 | dbms-nfx PR #3977 system catalog implementation | `V$DATABASES`, `M$SYS_*` 조인 시 함께 사용 |
| mounted database는 READ ONLY이며 `USAGE`와 table `SELECT`가 필요 | dbms-nfx #3235 backup/security regression | `USE`와 쓰기는 불가 |
| Machbase 8.7.0 프로토콜(버전 4.0.3)이 multi-database client/server 경계 | dbms-nfx PR #3977 protocol compatibility tests | 8.5.2/구형 프로토콜(버전 4.0.2)은 MACHBASEDB 호환 동작만 확인 |
| prepared/cursor/appender는 prepare/open 시점 catalog에 고정 | dbms-nfx #3235 session/client regression | `USE` 후 새 handle 생성 권장 |

## 인증 / 보안

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| `AUTH_SIG_SCHEME` 허용값: `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS` | AUTH KEY 구성 문서 | [AUTH KEY 문서](../../../security-access-control/authentication-auth-key/) |
| `AUTH_MODE` 허용값: `PASSWORD`, `CHALLENGE` | AUTH KEY 구성 문서 | [AUTH KEY 문서](../../../security-access-control/authentication-auth-key/) |
| AUTH KEY는 공개키 기반 인증 — 비밀번호 대신 사용 가능 | Machbase 8.7.0 매뉴얼 보안 섹션 | [AUTH KEY 문서](../../../security-access-control/authentication-auth-key/) |

## Python SDK

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| Python machbaseAPI의 `paramstyle`은 `named` | dbms-nfx `ux/src/python/machbaseAPI/__init__.py` | `:name` SQL과 mapping 사용 |
| 일반 cursor의 named `execute()`는 호출마다 서버 prepare/execute/close | dbms-nfx#3935, commit `a60f8414` | prepared cursor와 구분 |
| 일반 cursor의 `executemany()`는 호출 내부에서 statement 재사용 | dbms-nfx#3935, commit `a60f8414` | 호출이 끝나면 statement close |
| `cursor(prepared=True)`는 동일 원본 SQL의 server statement 재사용 | dbms-nfx#3980, commit `f3e153d6` | SQL 변경 또는 cursor close 시 해제 |
| `MachbasePreparedCursor`는 공개 package symbol | dbms-nfx `machbaseAPI/__init__.py`, commit `f3e153d6` | Python API 2.4 |
| prepared cursor는 `%s`, `?`, `%(name)s`, `:name` 지원 | dbms-nfx#3980 회귀 테스트 | quote와 comment 내부 marker는 보존 |
| Machbase 8.7.0 프로토콜(버전 4.0.3)을 지원하지 않는 named 실행은 PREPARE 전 `NotSupportedError(0A000)` | dbms-nfx#3980, commit `95a9be1d` | 기존 cached statement 유지 |
| marker 없는 SQL의 빈 mapping은 parameter 없음으로 정규화 | dbms-nfx#3980, commit `95a9be1d` | `None`, 빈 sequence와 동일 |

## Named Bind Parameter

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| 공통 marker 문법은 `:name`이고 값 위치에만 사용 | dbms-nfx#3935, commit `a60f8414` | [SQL 문법](../../sql/syntax-dictionary-sql/named-bind-parameter-syntax/) |
| 파라미터는 고유 이름이 아니라 발생 횟수로 계산하며 최대 256개 | dbms-nfx 3935 회귀 테스트 | 반복 이름도 각 occurrence로 계산 |
| JDBC, Node.js, Python 이름 API는 반복 이름에 한 값을 적용 | dbms-nfx 3935 SDK 회귀 테스트 | 이름은 대소문자 구분 |
| Go native `api.Named()`와 Go `database/sql` `sql.Named()` 지원 | neo-client PR #3, 최종 커밋 `6b9dae0c` | named와 positional 인자 혼용 금지 |
| .NET 이름 컬렉션은 client-side 렌더링 후 ExecDirect 사용 | MachConnector40 provider 구현 | 서버 Named Bind 근거로 사용하지 않음 |

## UPDATE/DELETE 영향 행 수

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| `UPDATE`는 실제 값 변경 여부와 무관하게 `WHERE` 조건에 일치한 행 수를 반환 | dbms-nfx#3982, commit `038e7568` | 동일 값 반복 UPDATE도 대상 행을 포함 |
| `DELETE`는 실제 삭제된 행 수를 반환 | dbms-nfx#3982 회귀 테스트 | 같은 DELETE를 반복하면 다음 실행은 `0` |
| Direct execution과 prepared statement는 같은 영향 행 수 기준을 사용 | dbms-nfx#3982 MMP 구현 및 회귀 테스트 | [DML 영향 행 수](../../sql/syntax-dictionary-sql/dml-syntax/#dml-update-delete-affected-rows) |
| 기존 SDK 공개 API가 서버의 영향 행 수를 노출 | dbms-nfx#3982 Standard/Cluster 및 SDK 회귀 테스트 | [SDK별 확인 방법](/dbms/application-integration/concepts-common/#dml-affected-rows) |

## Go SDK

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| Go `database/sql` 드라이버: `Begin()` / `BeginTx()` 구현 | neo-client PR #3, 최종 커밋 `6b9dae0c` | 기본 isolation level의 SQL 트랜잭션 |
| Go native `machgo`: Appender, named bind, DECIMAL, NULL·PRIMARY KEY 메타데이터 지원 | neo-client PR #3, 커밋 `915d846b` | [Go SDK 레퍼런스](/dbms/development-tools-integration/go/) |
| Go `database/sql`: named bind, DECIMAL, NULL 메타데이터 지원. 표준 PK API는 없음 | neo-client PR #3, 커밋 `915d846b` 및 Go 표준 `database/sql` 계약 | [Go SDK 레퍼런스](/dbms/development-tools-integration/go/) |

## PRIMARY KEY 메타데이터

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| Machbase 8.7.0 프로토콜(버전 4.0.3)이 결과 컬럼 type 정보에 PRIMARY KEY 플래그를 전달 | dbms-nfx #4010, 커밋 `7e4a6f411` | 직접 컬럼에만 적용 |
| TRANSACTION·LOOKUP·VOLATILE PK와 TAG `NAME`을 결과 메타데이터로 식별 | dbms-nfx #4010 분석·회귀 테스트 | LOG, 표현식, 집계식, 외부 조인 NULL 측은 PK 아님 |
| Go native `api.Column.PrimaryKey`가 `Rows.Columns()`와 `Row.Columns()`에 전달 | neo-client PR #3, 커밋 `915d846b` | prepared·statement cache 경로 포함 |
| Go `database/sql.ColumnType`에는 PRIMARY KEY API가 없음 | Go 표준 인터페이스 및 neo-client 구현 | native API 또는 카탈로그 조회 사용 |
| ODBC `SQLPrimaryKeys()`와 JDBC `getPrimaryKeys()`가 실제 PK 목록 반환 | dbms-nfx #4010 회귀 테스트 | 비-SYS 소유자와 TAG `NAME` 포함 |
| `machsql DESC`가 `[ PRIMARY KEY ]` 섹션 표시 | dbms-nfx #4010 회귀 테스트 | SQLCLI `DescribeCol` 계약은 변경 없음 |
| 구형 프로토콜(버전 4.0.2 이하)에서는 신규 PRIMARY KEY 플래그를 숨김 | dbms-nfx #4010 protocol 호환성 테스트 | 구형 클라이언트 호환성 유지 |

## Cluster Edition

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| Cluster Edition: TRANSACTION 테이블 미지원 | Machbase 공식 제한사항 문서 | [지원 범위와 제약](../../../reference/support-scope-constraints/) |
| Cluster Edition: VOLATILE 테이블 미지원 | Machbase 공식 제한사항 문서 | |
| Cluster Edition: STREAM, MOUNT, Custom ROLLUP, ROLLUP_REBUILD 미지원 | Machbase 공식 제한사항 문서 | |

## 성능

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| TAG 테이블 Append가 SQL INSERT보다 빠름 | Append 전용 이진 프로토콜 사용 (SQL 파싱 오버헤드 없음) | [Append 개념](/dbms/application-integration/concepts-common/#append-api-batch) |
| ROLLUP은 집계를 사전 계산하여 조회 속도 향상 | ROLLUP 설계 문서 | [ROLLUP](/dbms/tag-rollup-usage/overview-use-criteria/#rollup) |

## TAG 테이블 DML 제약

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| TAG data UPDATE WHERE는 Standard Edition에서 태그 선택 조건과 하나 이상의 BASETIME 조건을 요구하며 `name IN`, `name LIKE`, 한쪽/양쪽 시간 범위, 데이터 컬럼 predicate를 지원 | TAG data UPDATE 구문과 지원 범위 문서 | [TAG data UPDATE](/dbms/reference/support-scope-constraints/tag-data-update/) |
| TAG data UPDATE SET은 실제 데이터 컬럼을 허용하고 PK(name), BASETIME, 메타데이터 컬럼과 기존 행 컬럼을 참조하는 RHS는 거부 | TAG data UPDATE 구문과 지원 범위 문서 | [TAG data UPDATE 구문](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/tag-data-update-syntax/) |
| TAG 테이블 DELETE는 BEFORE/WHERE/METADATA/ROLLUP 등 제한된 형태로 지원 | TAG DELETE 구문과 지원 범위 문서 | 일반 TRANSACTION DELETE와 동일한 범위로 가정하지 않음 |
