---
type: docs
title: 'support-matrix'
weight: 40
---

이 페이지는 Machbase의 핵심 기능 지원 여부를 요약한 매트릭스입니다. AI 에이전트가 "X Edition에서 Y 기능이 지원되나요?" 유형의 질문에 답할 때 참조합니다.

범례: O = 지원, X = 미지원, - = 해당 없음

## 에디션 × 기능 지원표

| 기능 | Standard Edition | Cluster Edition |
|------|:----------------:|:---------------:|
| TAG 테이블 | O | O |
| LOG 테이블 | O | O |
| LOOKUP 테이블 | O | X |
| VOLATILE 테이블 | O | X |
| RDB 테이블 | O | X |
| ROLLUP | O | O |
| ROLLUP_REBUILD | O | X |
| STREAM | O | X |
| MOUNT / UNMOUNT | O | X |
| 수평 확장 (Scale-out) | X | O |
| HA (고가용성) | X | O |
| Broker 노드 | X | O |
| Warehouse 노드 | X | O |

## 테이블 타입 × 기능 지원표

| 기능 | TAG | LOG | LOOKUP | VOLATILE | RDB |
|------|:---:|:---:|:------:|:--------:|:---:|
| INSERT (SQL) | O | O | O | O | O |
| Append API | O | O | X | X | X |
| UPDATE | 제한적¹ | X | O | O | O |
| DELETE | X | X | O | O | O |
| Transaction (COMMIT/ROLLBACK) | X | X | O | O | O |
| ROLLUP 대상 | O | X | X | X | X |
| 전문 검색 (TEXT INDEX) | X | O | X | X | X |
| JSON 컬럼 저장 | X | O | O | X | O |
| PRIMARY KEY | O (name) | X | O | O | O |
| BASETIME 컬럼 | O | - | - | - | - |

> ¹ TAG 테이블 UPDATE: `WHERE name = ?` 조건(PK)만 허용, SET 대상은 SUMMARIZED/METADATA 컬럼만 가능. PK(name) 및 BASETIME 컬럼은 UPDATE 불가.

## SDK × 주요 기능 지원표

| SDK | Append | AUTH KEY 인증 | Transaction | Server Prepared Statement |
|-----|:------:|:-------------:|:-----------:|:-------------------------:|
| JDBC | O | O | O | O |
| Python (machbaseAPI) | O | O | O | X² |
| Go (machcli / native) | O | O | X³ | O |
| Go (database/sql) | X | O | X³ | O |
| .NET (MachConnector) | O | O | O | O |
| Node.js | O | X⁴ | X | X |
| REST API | X | X | X | X |
| ODBC/CLI | O | O | O | O |
| R (RODBC) | X | X | X | X |

> ² Python machbaseAPI는 `%s` 클라이언트 렌더링 방식 사용. 서버 Prepared Statement 미지원.  
> ³ Go driver (machcli, database/sql 모두): `Begin()` / `BeginTx()` 미구현.  
> ⁴ Node.js AUTH KEY: 현재 미지원.
