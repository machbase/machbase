---
type: docs
title: '테이블 타입'
weight: 60
---

Machbase의 네 가지 테이블 타입에 대한 상세한 참조 문서입니다. 각 섹션은 완전한 구문, 기능 및 고급 사용 패턴을 제공합니다.

## 테이블 타입

- [Tag 테이블](./tag-tables/) - 센서/장치 시계열 데이터
- [Log 테이블](./log-tables/) - 이벤트 스트림 및 로그
- [Volatile 테이블](./volatile-tables/) - 인메모리 실시간 데이터
- [Lookup 테이블](./lookup-tables/) - 참조 및 마스터 데이터

## 빠른 참조

| 타입 | 생성 구문 | 최적 용도 |
|------|--------------|----------|
| Tag | `CREATE TAGDATA TABLE` | 센서 데이터 (ID, 시간, 값) |
| Log | `CREATE TABLE` | 이벤트, 로그, 유연한 스키마 |
| Volatile | `CREATE VOLATILE TABLE` | 실시간 캐시, 세션 |
| Lookup | `CREATE LOOKUP TABLE` | 장치 레지스트리, 설정 |

포괄적인 비교 및 결정 가이드는 [테이블 타입 개요](../core-concepts/table-types-overview/)를 참조하세요.
