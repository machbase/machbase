---
type: docs
title: '4.6 테이블 타입별 관리 가능 범위'
weight: 60
toc: true
---

각 테이블 타입은 DDL 및 DML 작업에 대한 지원 범위가 다릅니다. 설계와 운영 단계에서 테이블 타입별 제약을 미리 파악해 두면 예상치 못한 오류를 방지할 수 있습니다.

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
| CREATE INDEX | O (메타데이터/값 컬럼) | O | O | O | O |
| DROP INDEX | O | O | O | O | O |
| CREATE VIEW | - (참조 가능) | - | - | - | - |

세부 문법과 제약은 [테이블 정의와 스키마 객체](../schema-objects-definition/)를 참고하십시오.

## DML 지원 범위

| DML 작업 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|---------|-----|-----|-----|---------|--------|
| INSERT | O | O | O | O | O |
| Append API | O | O | O (SDK) | X | O |
| UPDATE | O (태그/축 조건) | X | O | O (PK equality) | O (일반 조건식) |
| DELETE | O (BEFORE/조건) | O (BEFORE/OLDEST/EXCEPT) | O | O (PK equality) | O (일반 조건식/전체) |
| ON DUPLICATE KEY UPDATE | X | X | O | O | O |

## Retention Policy 지원

| 기능 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|------|-----|-----|-----|---------|--------|
| Retention Policy 적용 | O | O | X | X | X |

KV 테이블도 Retention Policy를 적용할 수 있습니다.

## 인덱스 지원

| 인덱스 유형 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|-----------|-----|-----|-----|---------|--------|
| LSM | X | O | X | X | X |
| BITMAP | X | O | X | X | X |
| KEYWORD | X | O | X | X | X |
| REDBLACK (PK/인덱스) | O (메타데이터) | X | X | O | O |
| BTREE | X | X | O | X | X |

## Edition별 제약

| 기능 | Standard | Cluster |
|------|---------|---------|
| RDB 테이블 | O | X |
| TAG data UPDATE | O | X |
| Retention Policy | O | O |
| Cluster 전용 기능 | X | O |

## 선택 가이드 요약

- **대량 시계열 수집 + 장기 보존**: TAG, KV 또는 LOG + Retention Policy
- **수정 가능한 설정·상태 값**: VOLATILE (메모리) 또는 LOOKUP (영구)
- **일반 관계형 데이터 (업데이트 필요)**: RDB (Standard Edition 전용)
- **빠른 JOIN 참조 테이블**: VOLATILE 또는 LOOKUP
