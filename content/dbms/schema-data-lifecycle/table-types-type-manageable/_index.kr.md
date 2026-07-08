---
type: docs
title: '테이블 타입별 관리 가능 범위'
weight: 40
---

Machbase의 각 테이블 타입은 DDL 및 DML 작업에 대한 지원 범위가 다릅니다. 설계와 운영 단계에서 테이블 타입별 제약을 미리 파악하면 예상치 못한 오류를 방지할 수 있습니다.

## DDL 지원 범위

| DDL 작업 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|---------|-----|-----|-----|---------|--------|
| CREATE TABLE | O | O | O | O | O |
| DROP TABLE | O | O | O | O | O |
| TRUNCATE TABLE | X | O | O | X | X |
| ALTER TABLE (컬럼 추가) | O (METADATA만) | O | O | O | O |
| ALTER TABLE (컬럼 삭제) | O (METADATA만) | O | O | O | O |
| ALTER TABLE (컬럼 이름 변경) | O (일반 컬럼) | X | O | X | X |
| ALTER TABLE (컬럼 속성 변경) | O (일반 컬럼) | O | X | X | X |
| ALTER TABLE (테이블 이름 변경) | X | X | O | X | X |
| ALTER TABLE ADD RETENTION | O | O | X | X | X |
| ALTER TABLE DROP RETENTION | O | O | X | X | X |
| CREATE INDEX | O (메타데이터) | O | O | X | X |
| DROP INDEX | O | O | O | X | X |
| CREATE VIEW | - (참조 가능) | - | - | - | - |

> ALTER TABLE 지원 범위는 소스 코드(`qpvAlterTable.c`) 기준입니다.

## DML 지원 범위

| DML 작업 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|---------|-----|-----|-----|---------|--------|
| INSERT | O | O | O | O | O |
| Append API | O | O | X | X | X |
| UPDATE | O (조건부) | X | O | O (PK equality) | O (PK equality) |
| DELETE | O (BEFORE/조건) | O (BEFORE/OLDEST/EXCEPT) | O | O (PK equality) | O (PK equality) |
| ON DUPLICATE KEY UPDATE | X | X | X | O | X |

## Retention Policy 지원

| 기능 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|------|-----|-----|-----|---------|--------|
| Retention Policy 적용 | O | O | X | X | X |

## 인덱스 지원

| 인덱스 유형 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|-----------|-----|-----|-----|---------|--------|
| LSM | X | O | X | X | X |
| BITMAP | X | O | X | X | X |
| KEYWORD | X | O | X | X | X |
| REDBLACK (PK/인덱스) | O (name) | X | O | O | O |

## Edition별 제약

| 기능 | Standard | Cluster |
|------|---------|---------|
| RDB 테이블 | O | X |
| TAG data UPDATE | O | 확인 필요 |
| Retention Policy | O | O |
| Cluster 전용 기능 | X | O |

## 선택 가이드 요약

- **대량 시계열 수집 + 장기 보존**: TAG 또는 LOG + Retention Policy
- **수정 가능한 설정·상태 값**: VOLATILE (메모리) 또는 LOOKUP (영구)
- **일반 관계형 데이터 (업데이트 필요)**: RDB (Standard Edition 전용)
- **빠른 JOIN 참조 테이블**: VOLATILE 또는 LOOKUP
