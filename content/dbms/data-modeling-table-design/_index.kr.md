---
type: docs
title: '4. 테이블 타입 개념과 선택'
weight: 40
toc: true
---

저장할 데이터의 성격, 변경 방식, 조회 패턴을 기준으로 Machbase 테이블 타입을 선택하고
스키마를 설계합니다. 먼저 테이블 타입을 결정한 뒤 제약 조건과 데이터 변경 정책을 정의하고,
검증된 모델링 패턴을 적용합니다.

## 테이블 타입 요약

| 타입 | DDL | 주요 용도 |
|------|-----|----------|
| TAG | `CREATE TAG TABLE` | 이름과 시간축을 가진 센서·계측 데이터 |
| LOG | `CREATE TABLE` | 순차적으로 추가되는 이벤트·로그 데이터 |
| RDB | `CREATE RDB TABLE` | 트랜잭션과 관계형 변경이 필요한 업무 데이터 |
| VOLATILE | `CREATE VOLATILE TABLE` | 재시작 시 폐기 가능한 인메모리 상태·캐시 |
| LOOKUP | `CREATE LOOKUP TABLE` | 코드, 기준 정보, 참조 데이터 |

## 이 장의 구성

| 순서 | 섹션 | 내용 |
|-----:|------|------|
| 4.1 | [스키마 객체 정의](./schema-objects-definition/) | 테이블, 컬럼, 데이터 타입, 제약 조건, 인덱스, 뷰 |
| 4.2 | [테이블 타입 선택](./table-types-selection-type/) | 데이터 특성과 접근 패턴에 따른 선택 기준 |
| 4.3 | [데이터 변경 정책](./alter-data-mutation-policy/) | 테이블 타입별 UPDATE, DELETE, TRUNCATE 정책 |
| 4.4 | [안티패턴](./table-types-patterns-type-anti/) | 피해야 할 테이블 선택과 스키마 설계 |
| 4.5 | [모델링 패턴](./patterns-modeling/) | 시계열, 이벤트, 상태, 참조, 업무 데이터 모델 |
| 4.6 | [테이블 타입별 관리 가능 범위](./table-types-type-manageable/) | DDL, DML, 인덱스, Retention 지원 범위 |

새 스키마를 설계할 때는 4.2에서 테이블 타입을 선택하고, 4.1과 4.3에서 스키마와 변경 정책을
구체화한 뒤 4.4의 안티패턴을 점검합니다.
