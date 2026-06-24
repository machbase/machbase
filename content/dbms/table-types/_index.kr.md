---
type: docs
title: '테이블 타입'
weight: 60
---

Machbase 테이블 타입에 대한 상세한 참조 문서입니다. 각 섹션은 구문, 기능 및 사용 패턴을 제공합니다.

## 테이블 타입

- [Tag 테이블](./tag-tables/) - 센서/장치 시계열 데이터
- [Log 테이블](./log-tables/) - 이벤트 스트림 및 로그
- [Volatile 테이블](./volatile-tables/) - 비영구 메모리 primary-key 테이블
- [Lookup 테이블](./lookup-tables/) - 메모리 primary-key 인덱스를 사용하는 영구 참조 테이블
- [RDB 테이블](./rdb-tables/) - 범용 디스크 row 테이블

## 빠른 참조

| 타입 | 생성 구문 | 저장소 | 인덱스 모델 | 지속성 | DML 범위 |
|------|--------------|---------|-------------|-------------|-----------|
| Tag | `CREATE TAG TABLE` | 디스크 시계열 | Tag + axis 인덱스 | 예 | `SELECT`, `INSERT`, 시간 기반 `DELETE` |
| Log | `CREATE TABLE` | 디스크 append log | 시간 파티션 + 선택적 log 인덱스 | 예 | `SELECT`, `INSERT`, 시간 기반 `DELETE` |
| Volatile | `CREATE VOLATILE TABLE` | 메모리 | 단일 primary-key 메모리 인덱스 | 아니오 | primary key 기반 전체 DML |
| Lookup | `CREATE LOOKUP TABLE` | 영구 참조 데이터 | 단일 primary-key 메모리 인덱스 | 예 | primary key 기반 전체 DML |
| RDB | `CREATE RDB TABLE` | 디스크 row 테이블 | 선택적 primary key, 일반, unique, JSON path 인덱스 | 예 | 전체 row DML 및 인덱스 predicate |

포괄적인 비교 및 결정 가이드는 [테이블 타입 개요](../core-concepts/table-types-overview/)를 참조하세요.
