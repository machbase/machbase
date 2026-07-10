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
| Python machbaseAPI 파라미터 바인딩 스타일: `%s` 또는 `%(name)s` | Python SDK 가이드 | `?` 플레이스홀더 사용 불가 |
| Python machbaseAPI는 Server Prepared Statement 미지원 | machbaseAPI 구현 방식 (클라이언트 렌더링) | 쿼리 문자열을 클라이언트에서 완성 후 서버에 전송 |

## Go SDK

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| Go `database/sql` 드라이버: `Begin()` / `BeginTx()` 미구현 | Go 드라이버 소스 코드 | Transaction 시작 불가 |
| Go `machcli` (native): Append API 지원, Transaction 미지원 | machcli 드라이버 문서 | [Go 드라이버 가이드](/dbms/application-integration/guide-drivers/#go) |

## Cluster Edition

| 사실 | 근거 (소스) | 비고 |
|------|------------|------|
| Cluster Edition: RDB 테이블 미지원 | Machbase 공식 제한사항 문서 | [지원 범위와 제약](../../../reference/support-scope-constraints/) |
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
| TAG 테이블 DELETE는 BEFORE/WHERE/METADATA/ROLLUP 등 제한된 형태로 지원 | TAG DELETE 구문과 지원 범위 문서 | 일반 RDB DELETE와 동일한 범위로 가정하지 않음 |
