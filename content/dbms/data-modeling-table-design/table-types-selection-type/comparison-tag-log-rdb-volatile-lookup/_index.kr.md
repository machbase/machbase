---
type: docs
title: '타입 비교표'
weight: 30
---

다섯 가지 테이블 타입의 주요 기능을 한눈에 비교합니다.

## 기능 비교

| 항목 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| DDL | `CREATE TAG TABLE` | `CREATE TABLE` | `CREATE RDB TABLE` | `CREATE VOLATILE TABLE` | `CREATE LOOKUP TABLE` |
| 주 용도 | 센서·계측값 | 이벤트·로그 | 관계형 업무 | 임시 집계 | 코드·기준 |
| INSERT | O | O | O | O | O |
| APPEND API | O | O | X | X | X |
| UPDATE | X | X | X | O (ON DUPLICATE KEY) | O (by PK) |
| DELETE | X | X | O | O | O |
| PRIMARY KEY | 필수 | X | X | 필수 | 필수 |
| BASETIME | 필수 (시간축) | X | X | X | X |
| _arrival_time | X | 자동 추가 | X | X | X |
| 인덱스 | 태그 인덱스 | 없음 | KV Secondary | Red-Black | B-Tree |
| 영속성 | O | O | O | X (메모리) | O |
| Cluster Edition | O | O | X | O | O |

## 스토리지 특성

| 항목 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| 스토리지 | 컬럼형 | 컬럼형 | Key-Value | 메모리 | 행 기반 |
| 압축 | O | O | 제한적 | N/A | X |
| 시계열 최적화 | O | 일부 | X | X | X |
| 대용량 적합 | O | O | O | X | X |

## RDB 테이블 제약

RDB 테이블(8.6 신규)은 다음 제약이 있습니다.

- **최소 컬럼 수**: 4개 이상 필요
- **UPDATE 미지원**: DELETE 후 INSERT 패턴 사용
- **Cluster Edition 미지원**: Standard Edition 전용
- **APPEND API 미지원**: INSERT 문 또는 Machbase SDK INSERT 사용
