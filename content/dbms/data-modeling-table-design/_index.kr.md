---
type: docs
title: '4. 테이블 타입 개념과 선택'
weight: 40
---

다섯 가지 테이블 타입 중 저장할 데이터의 성격과 접근 패턴에 맞는 타입을 선택한다.

| 타입 | DDL | 주요 용도 |
|------|-----|----------|
| TAG | `CREATE TAG TABLE` | 센서·IoT 계측값 (시계열·거리축) |
| LOG | `CREATE TABLE` (기본) | 이벤트·로그 (추가 전용) |
| RDB | `CREATE RDB TABLE` | 관계형 업무 데이터, DELETE·조회 필요 시 |
| VOLATILE | `CREATE VOLATILE TABLE` | 세션 내 임시 집계·조회 |
| LOOKUP | `CREATE LOOKUP TABLE` | 소규모 코드 테이블·기준 정보 |

## 이 장의 구성

- **[테이블 타입 선택](/dbms/data-modeling-table-design/table-types-selection-type/)** — 각 타입의 특성과 선택 기준
- **[안티패턴](/dbms/data-modeling-table-design/table-types-patterns-type-anti/)** — 피해야 할 설계 사례
- **[모델링 패턴](/dbms/data-modeling-table-design/patterns-modeling/)** — 시계열·상태·이벤트·마스터 데이터 설계 패턴
