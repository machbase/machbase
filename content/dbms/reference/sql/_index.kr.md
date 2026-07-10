---
type: docs
title: '17.1 SQL 레퍼런스'
weight: 10
toc: true
---

SQL 문법, 함수, 데이터 타입, 쿼리 힌트, 상대 시간 표현의 정확한 정의를 제공합니다.

## 하위 섹션

| 섹션 | 설명 |
|------|------|
| [SQL 문법 사전](./syntax-dictionary-sql/) | CREATE, DROP, ALTER, SELECT, INSERT, DELETE, UPDATE, BACKUP, MOUNT 등 모든 SQL 구문의 BNF 문법과 예시 |
| [함수 사전](./dictionary/) | 집계 함수, 수학 함수, 문자열 함수, 날짜/시간 함수, 타입 변환 함수, TAG 전용 함수 목록 및 설명 |
| [데이터 타입 사전](./type-data-types-dictionary/) | 지원 데이터 타입의 크기, 범위, 기본값, 테이블 유형별 사용 가능 여부 |
| [힌트 사전](./hint-dictionary-select/) | SELECT 쿼리 힌트 종류, 사용법, 적용 대상 |
| [상대 시간 표현 사전](./relative-time-dictionary/) | DURATION, BEFORE, AFTER, RANGE 등 시간 범위 표현 문법 |
| [8.5 전체 SQL 레퍼런스](./original-8-5-full/) | 8.5 원본 SQL 레퍼런스의 전체 항목 보존본 |

## SQL 특징

표준 ANSI SQL을 기반으로 시계열 데이터 처리에 최적화된 확장 문법을 제공합니다.

- **TAG 테이블 전용 문법**: `TAG TABLE` 키워드, `RECENT`, `FIRST`/`LAST`, `SERIES BY`, `ROLLUP`
- **시간 범위 조회**: `DURATION`, `BEFORE`, `AFTER`, `RANGE` 절
- **빠른 전체 삽입**: `APPEND` 프로토콜 (CLI/SDK)
- **텍스트 검색**: `SEARCH`, `ESEARCH`, `REGEXP` 연산자
- **집합 연산**: `UNION ALL` (UNION, INTERSECT, EXCEPT 미지원)
