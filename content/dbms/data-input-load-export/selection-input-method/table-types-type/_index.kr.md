---
type: docs
title: '테이블 타입별 입력 방식'
weight: 10
---

테이블 타입에 따라 사용 가능한 입력 방식이 다릅니다.

## 테이블 타입별 지원 입력 방식

| 입력 방식 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|----------|-----|-----|-----|---------|--------|
| SQL INSERT | O | O | O | O | O |
| INSERT SELECT | O | O | O | O | O |
| INSERT ON DUPLICATE KEY UPDATE | X | X | X | O (PK 필요) | X |
| Append API | O | O | O (트랜잭션 기반) | X | X |
| LOAD DATA INFILE | O | O | O | O | O |
| machloader | O | O | O | O | O |
| csvimport | O | O | O | O | O |
| tagmetaimport | O (메타데이터만) | X | X | X | X |

## 테이블 타입별 권장 입력 방식

### TAG 테이블

- **대량 시계열 수집**: Append API (SDK 경유) 또는 REST API
- **메타데이터 초기 로드**: tagmetaimport 또는 SQL INSERT METADATA
- **소량 데이터**: SQL INSERT

### LOG 테이블

- **대량 로그 수집**: Append API 또는 machloader
- **파일 배치 적재**: machloader, csvimport, LOAD DATA INFILE
- **스트리밍 수집**: REST API 또는 SDK

### RDB 테이블

- **초기 데이터 로드**: machloader 또는 SQL INSERT
- **애플리케이션 연동**: SQL INSERT/UPDATE/DELETE (JDBC, ODBC, SDK)
- **파일 적재**: csvimport

### VOLATILE / LOOKUP 테이블

- **참조 데이터 초기 로드**: SQL INSERT 또는 machloader
- **UPSERT**: INSERT ON DUPLICATE KEY UPDATE (VOLATILE, PK 있는 경우)
- **설정 업데이트**: SQL UPDATE (PK 기준)
