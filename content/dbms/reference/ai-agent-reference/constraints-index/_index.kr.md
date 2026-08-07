---
type: docs
title: '18.10.5 constraints-index'
weight: 50
toc: true
---

이 페이지는 Machbase의 알려진 제약 사항을 카테고리별로 정리한 인덱스입니다. AI 에이전트가 제약 여부를 빠르게 확인할 때 참조합니다.

## TAG 테이블 제약

| 제약 항목 | 내용 | 비고 |
|-----------|------|------|
| UPDATE WHERE 조건 | 태그 선택 조건(`name =`, `name IN`, `name LIKE`)과 BASETIME 조건 필수 | `OR`, 서브쿼리, 집계 조건 불가 |
| UPDATE SET 대상 | 실제 데이터 컬럼 허용. 메타데이터는 `UPDATE ... METADATA` 사용 | |
| PK(name) 컬럼 UPDATE | 불가 | |
| BASETIME 컬럼 UPDATE | 불가 | |
| DELETE | `BEFORE`, `WHERE`, `METADATA`, `ROLLUP` 등 제한된 형태로 지원 | 일반 TRANSACTION DELETE와 동일하게 가정하지 않음 |
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
| TRANSACTION 테이블 | 미지원 |
| MOUNT / UMOUNT | 미지원 |
| STREAM | 미지원 |
| Custom ROLLUP | 미지원 |
| ROLLUP_REBUILD | 미지원 |

## SDK 제약

| SDK | 제약 항목 | 내용 |
|-----|-----------|------|
| Go (machgo / database/sql) | Transaction | native는 SQL 직접 실행, `database/sql`은 기본 isolation level의 `Begin`/`Commit`/`Rollback` 지원 |
| Python (machbaseAPI) | Transaction | `begin()` / `commit()` / `rollback()` 미지원 |
| .NET (MachConnector) | Transaction | `MachTransaction` 미구현 |
| .NET (MachConnector) | AUTH KEY 인증 | 연결 옵션 미지원 |
| Python (machbaseAPI) | Prepared cursor cache | cursor당 server statement 하나. SQL 문자열이 달라지면 기존 statement 해제 |
| .NET (MachConnector) | Server Prepared Statement | 미지원 — 이름 컬렉션은 client-side 렌더링 후 ExecDirect |
| Go (machgo / database/sql) | Named Bind API | native `api.Named()`, SQL 드라이버 `sql.Named()` 지원 |
| REST API | Transaction | 미지원 |
| REST API | Prepared Statement | 미지원 |
| Node.js | AUTH KEY 인증 | 미지원 |
| Go (database/sql) | Append API | 표준 `sql.DB`/`sql.Tx`에는 없음 — `sql.Conn.Raw()`에서 `machbase.Conn.Appender()` 확장 사용 가능. 신규 대량 입력은 `machgo` 권장 |

## 다중 데이터베이스 제약

| 제약 항목 | 내용 |
|-----------|------|
| Edition | Standard Edition 전용. Cluster/XMA 분산 catalog는 지원하지 않음 |
| 물리 격리 | database별 CPU·메모리·디스크 quota 또는 process 격리를 제공하지 않음 |
| 객체 이름 | 다른 database를 지정할 때 `database.owner.table`을 사용하며 `database.table` shortcut은 없음 |
| Mounted database | READ ONLY이며 `USE`할 수 없음. `USAGE`와 table `SELECT`가 필요 |
| Transaction 중 USE | 진행 중인 transaction에서는 current database를 변경할 수 없음 |
| Handle binding | prepared statement, cursor, appender는 prepare/open 당시 database에 고정 |
| Compatibility | CMI 4.0.3 미만 client/server 조합에서는 비기본 database 선택을 보장하지 않음 |

## 일반 제약

| 제약 항목 | 대상 | 내용 |
|-----------|------|------|
| TRANSACTION | TAG 테이블 | Append-only 구조로 TRANSACTION 없음 |
| TRANSACTION | LOG 테이블 | Append-only 구조로 TRANSACTION 없음 |
| ROLLUP_REBUILD | Cluster Edition | 미지원 |
| 텍스트 전문 검색 | TAG/LOOKUP/VOLATILE/TRANSACTION | 미지원 (LOG 테이블만 지원) |
| JSON 컬럼 | VOLATILE | 미지원 |

## 참조

- 지원 여부 전체 매트릭스: [support-matrix](../support-matrix/)
- 공식 제약 문서: [지원 범위와 제약](../../../reference/support-scope-constraints/)
