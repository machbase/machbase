---
type: docs
title: 'constraints-index'
weight: 50
---

이 페이지는 Machbase의 알려진 제약 사항을 카테고리별로 정리한 인덱스입니다. AI 에이전트가 제약 여부를 빠르게 확인할 때 참조합니다.

## TAG 테이블 제약

| 제약 항목 | 내용 | 비고 |
|-----------|------|------|
| UPDATE WHERE 조건 | 태그 선택 조건(`name =`, `name IN`, `name LIKE`)과 BASETIME 조건 필수 | `OR`, 서브쿼리, 집계 조건 불가 |
| UPDATE SET 대상 | 실제 데이터 컬럼 허용. 메타데이터는 `UPDATE ... METADATA` 사용 | |
| PK(name) 컬럼 UPDATE | 불가 | |
| BASETIME 컬럼 UPDATE | 불가 | |
| DELETE | `BEFORE`, `WHERE`, `METADATA`, `ROLLUP` 등 제한된 형태로 지원 | 일반 RDB DELETE와 동일하게 가정하지 않음 |
| TRANSACTION | 없음 (Append-only, COMMIT/ROLLBACK 불가) | |
| INSERT vs Append | SQL INSERT 가능하나 Append API 대비 성능 낮음 | |

## LOOKUP 테이블 제약

| 제약 항목 | 내용 | 비고 |
|-----------|------|------|
| 비-PK predicate UPDATE/DELETE | 지원; 조건에 맞는 모든 row에 적용되므로 대상 범위 확인 필요 | |
| JSON 타입 컬럼 | 일반 컬럼으로 지원 | |
| JSON path query | 지원; JSON path별 전용 인덱스는 미지원 | |
| JSON PK | 미지원 | |

## Cluster Edition 제약

| 제약 항목 | 내용 |
|-----------|------|
| LOOKUP 테이블 | 미지원 |
| VOLATILE 테이블 | 미지원 |
| RDB 테이블 | 미지원 |
| MOUNT / UNMOUNT | 미지원 |
| STREAM | 미지원 |
| Custom ROLLUP | 미지원 |
| ROLLUP_REBUILD | 미지원 |

## SDK 제약

| SDK | 제약 항목 | 내용 |
|-----|-----------|------|
| Go (machcli / database/sql) | Transaction | `Begin()` / `BeginTx()` 미구현 — COMMIT/ROLLBACK 불가 |
| Python (machbaseAPI) | Server Prepared Statement | 미지원 — `%s` 또는 `%(name)s` 플레이스홀더를 클라이언트에서 렌더링 후 전송 |
| REST API | Transaction | 미지원 |
| REST API | Prepared Statement | 미지원 |
| Node.js | AUTH KEY 인증 | 현재 미지원 |
| Go (database/sql) | Append API | 미지원 — Append가 필요하면 `machcli` (native) 사용 |

## 일반 제약

| 제약 항목 | 대상 | 내용 |
|-----------|------|------|
| TRANSACTION | TAG 테이블 | Append-only 구조로 TRANSACTION 없음 |
| TRANSACTION | LOG 테이블 | Append-only 구조로 TRANSACTION 없음 |
| ROLLUP_REBUILD | Cluster Edition | 미지원 |
| 텍스트 전문 검색 | TAG/LOOKUP/VOLATILE/RDB | 미지원 (LOG 테이블만 지원) |
| JSON 컬럼 | VOLATILE | 미지원 |

## 참조

- 지원 여부 전체 매트릭스: [support-matrix](../support-matrix/)
- 공식 제약 문서: [지원 범위와 제약](../../../reference/support-scope-constraints/)
