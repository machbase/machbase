---
type: docs
title: '18.1.1 SQL 문법 사전'
weight: 10
toc: true
---

SQL 문법 사전은 Machbase에서 지원하는 모든 SQL 구문의 BNF 표기와 최소 예시를 제공합니다.

## 지원 SQL 구문 목록

| 구문 | 분류 | 설명 |
|------|------|------|
| [CREATE TABLE](./ddl-syntax/#create-table) | DDL | 로그/TAG/LOOKUP/VOLATILE/TRANSACTION 테이블 생성 |
| [DROP TABLE](./ddl-syntax/#drop-table) | DDL | 테이블 삭제 |
| [ALTER TABLE](./ddl-syntax/#alter-table) | DDL | 테이블 스키마 변경 (컬럼 추가/삭제/수정/이름 변경) |
| [TRUNCATE TABLE](./ddl-syntax/#truncate-table) | DDL | 테이블 데이터 전체 삭제 |
| [CREATE INDEX](./index-syntax/#create-index) | DDL | 테이블 타입별 인덱스 생성 |
| [DROP INDEX](./index-syntax/#drop-index) | DDL | 인덱스 삭제 |
| [CREATE ROLLUP](./rollup-syntax/#create-rollup) | DDL | TAG 테이블 롤업 정의 생성 |
| [DROP ROLLUP / ALTER ROLLUP](./rollup-syntax/#drop-rollup) | DDL | 롤업 삭제 및 제어 |
| [CREATE RETENTION](./retention-syntax/#create-retention) | DDL | 데이터 보존 정책 생성 |
| [CREATE VIEW / DROP VIEW](./view-syntax/) | DDL | 저장 뷰 생성 및 삭제 |
| [CREATE TABLESPACE](./ddl-syntax/#create-tablespace) | DDL | 테이블스페이스 생성 |
| [INSERT INTO](./dml-syntax/#insert-into) | DML | 단건 및 다건 데이터 삽입 |
| [INSERT SELECT](./dml-syntax/#insert-select) | DML | 조회 결과를 다른 테이블에 삽입 |
| [UPDATE](./dml-syntax/#update) | DML | LOOKUP/VOLATILE 테이블 레코드 수정 |
| [DELETE](./dml-syntax/#delete) | DML | 테이블 데이터 삭제 |
| [LOAD DATA INFILE](./load-data-infile-syntax/) | DML | CSV 파일에서 직접 데이터 입력 |
| [SELECT](./select-syntax/) | SELECT | 데이터 조회 (JOIN, GROUP BY, ORDER BY, LIMIT 포함) |
| [WITH / CTE](./cte-syntax/) | SELECT | Standard Edition의 비재귀 공통 테이블 표현식 |
| [Named Bind Parameter](./named-bind-parameter-syntax/) | SQL 공통 | `:name` 형식의 값 파라미터 |
| [CAST](../dictionary/functions-full/#cast) | SQL 표현식 | 값을 지정한 데이터 타입으로 명시적으로 변환 |
| [SAVE DATA INTO](./save-data-into-syntax/) | SELECT | 조회 결과를 CSV 파일로 저장 |
| [BACKUP](./backup-restore-mount-syntax/#backup) | 운영 | 데이터베이스 또는 테이블 백업 |
| [RESTORE (machadmin -r)](./backup-restore-mount-syntax/#restore) | 운영 | 오프라인 복원 |
| [MOUNT / UMOUNT DATABASE](./backup-restore-mount-syntax/#mount-database) | 운영 | 백업 데이터베이스 마운트/언마운트 |
| [CREATE USER / DROP USER / ALTER USER](./user-auth-syntax/#create-drop-alter-user) | 사용자 | 사용자 생성, 삭제, 비밀번호 변경 |
| [GRANT / REVOKE](./user-auth-syntax/#grant-revoke) | 사용자 | 권한 부여 및 회수 |
| [AUTH KEY 관리](./user-auth-syntax/#auth-key) | 사용자 | 공개키 기반 인증 키 등록/관리 |
| [ALTER SYSTEM](./system-session-alter-syntax/#alter-system) | 시스템 | 세션 제어, PVO Cache flush, 라이선스 설치 등 |
| [ALTER SESSION](./system-session-alter-syntax/#alter-session) | 세션 | 세션별 파라미터 설정 |
| [PIVOT](./pivot-syntax/) | 분석 | 행을 열로 변환하는 피벗 쿼리 |
| [WINDOW FUNCTION (OVER)](./window-function-over-syntax/) | 분석 | 윈도우 함수와 OVER 절 |
| [SERIES BY](./series-syntax/) | 분석 | 연속 조건 만족 레코드 그룹화 |
| [SEARCH / ESEARCH / REGEXP](./search-esearch-regexp-syntax/) | 검색 | 키워드 인덱스 기반 텍스트 검색 |
| [ROLLUP REBUILD](./rollup-rebuild-syntax/) | 운영 | 롤업 결과 재계산 |
| [DATABASE](./database-syntax/) | DDL/세션 | 논리 데이터베이스 생성·선택·삭제와 상태 확인 |

## BNF 표기 규칙

이 사전에서 사용하는 BNF(Backus-Naur Form) 표기는 다음 규칙을 따릅니다.

| 표기 | 의미 |
|------|------|
| `'keyword'` | SQL 예약어 (대소문자 무관) |
| `name` | 사용자 정의 이름 |
| `( A \| B )` | A 또는 B 중 하나 |
| `[ ... ]` | 선택적 요소 (생략 가능) |
| `( ... )*` | 0회 이상 반복 |
| `( ... )+` | 1회 이상 반복 |
| `( ... )?` | 0회 또는 1회 |
