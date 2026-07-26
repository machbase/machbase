---
type: docs
title: '17.10.6 evidence-map'
weight: 60
toc: true
---

이 페이지는 Machbase에 관한 기술적 사실의 근거(소스)를 매핑합니다. AI 에이전트가 사실에 근거한 답변을 생성하거나, 답변의 출처를 명시할 때 참조합니다.

## 인증 / 보안

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| `AUTH_SIG_SCHEME` 허용값: `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS` | AUTH KEY 구성 문서 | [AUTH KEY 문서](../../../security-access-control/authentication-auth-key/) |
| `AUTH_MODE` 허용값: `PASSWORD`, `CHALLENGE` | AUTH KEY 구성 문서 | [AUTH KEY 문서](../../../security-access-control/authentication-auth-key/) |
| AUTH KEY는 공개키 기반 인증 — 비밀번호 대신 사용 가능 | Machbase 8.6 매뉴얼 보안 섹션 | [AUTH KEY 문서](../../../security-access-control/authentication-auth-key/) |

## Python SDK

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| Python machbaseAPI의 `paramstyle`은 `named` | dbms-nfx `ux/src/python/machbaseAPI/__init__.py` | `:name` SQL과 mapping 사용 |
| `execute()`와 `executemany()`의 named mapping은 서버 prepare/bind 사용 | dbms-nfx#3935, commit `a60f8414` | 공개 `prepare()` 객체는 없음 |
| `%s`, `%(name)s`는 호환용 client-side 렌더링 | Python SDK 구현 | 새 코드에는 `:name` 권장 |

## Named Bind Parameter

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| 공통 marker 문법은 `:name`이고 값 위치에만 사용 | dbms-nfx#3935, commit `a60f8414` | [SQL 문법](../../sql/syntax-dictionary-sql/named-bind-parameter-syntax/) |
| 파라미터는 고유 이름이 아니라 발생 횟수로 계산하며 최대 256개 | dbms-nfx 3935 회귀 테스트 | 반복 이름도 각 occurrence로 계산 |
| JDBC, Node.js, Python 이름 API는 반복 이름에 한 값을 적용 | dbms-nfx 3935 SDK 회귀 테스트 | 이름은 대소문자 구분 |
| .NET 이름 컬렉션은 client-side 렌더링 후 ExecDirect 사용 | MachConnector40 provider 구현 | 서버 Named Bind 근거로 사용하지 않음 |

## Go SDK

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| Go `database/sql` 드라이버: `Begin()` / `BeginTx()` 미구현 | Go 드라이버 소스 코드 | Transaction 시작 불가 |
| Go `machcli` (native): Append API 지원, Transaction 미지원 | machcli 드라이버 문서 | [Go 드라이버 가이드](/dbms/application-integration/guide-drivers/#go) |

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
| TAG data UPDATE WHERE는 태그 선택 조건과 BASETIME 조건을 요구하며 `name IN`, `name LIKE`, 시간 범위, 데이터 컬럼 predicate를 지원 | TAG data UPDATE 구문과 지원 범위 문서 | [TAG data UPDATE](/dbms/reference/support-scope-constraints/tag-data-update/) |
| TAG data UPDATE SET은 실제 데이터 컬럼을 허용하고 PK(name), BASETIME, 메타데이터 컬럼은 거부 | TAG data UPDATE 구문과 지원 범위 문서 | [TAG data UPDATE 구문](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/tag-data-update-syntax/) |
| TAG 테이블 DELETE는 BEFORE/WHERE/METADATA/ROLLUP 등 제한된 형태로 지원 | TAG DELETE 구문과 지원 범위 문서 | 일반 TRANSACTION DELETE와 동일한 범위로 가정하지 않음 |
