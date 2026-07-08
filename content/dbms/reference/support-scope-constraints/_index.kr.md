---
type: docs
title: '지원 범위와 제약'
weight: 80
---

이 섹션은 Machbase의 Edition별, 테이블 타입별, SDK별 기능 지원 범위와 알려진 제약 사항을 한눈에 파악할 수 있도록 정리한 빠른 참조 모음입니다.

기능의 동작 원리나 사용 예시는 각 기능 장을 참고하고, 특정 환경에서 기능이 동작하는지 여부를 빠르게 확인할 때 이 섹션을 활용하세요.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [Edition별 기능 지원표](./edition/) | Standard Edition vs Cluster Edition 기능 비교 |
| [테이블 타입별 기능 지원표](./table-types-type/) | TAG / LOG / LOOKUP / VOLATILE / RDB 테이블별 지원 기능 |
| [SDK별 기능 지원표](./sdk/) | JDBC, Python, Go, .NET, Node.js, REST API 지원 범위 |
| [REST API 지원표](./rest-api/) | HTTP 엔드포인트 목록, 인증 방식 |
| [백업/마운트 지원표](./backup-mount/) | BACKUP / MOUNT 기능의 Edition별 지원 여부 |
| [권한별 기능 지원표](./privileges/) | 데이터베이스 권한 및 테이블 권한 목록 |
| [RDB 기능 지원표](./rdb/) | RDB 테이블 지원 SQL 기능 및 제약 |
| [제한사항 사전](./limitations-dictionary/) | 테이블 유형별, Edition별 주요 제한사항 종합 |
| [버전 및 호환성](./compatibility-version/) | 업그레이드 시 주의사항, 지원 OS/플랫폼 |
| [XMA 프로토콜 호환성](./compatibility-xma-protocol/) | 서버-클라이언트 프로토콜 버전 호환 범위 |
| [LOOKUP SQL/JSON 지원표](./lookup-sql-json/) | LOOKUP 테이블 SQL/JSON 기능 지원 현황과 제약 |
| [TAG data UPDATE 지원표](./tag-data-update/) | TAG UPDATE 조건 및 대상 컬럼 지원 현황 |

## 표기 규칙

이 섹션의 지원 여부 표에서 사용하는 기호는 다음과 같습니다.

| 기호 | 의미 |
|:----:|------|
| O | 완전 지원 |
| X | 미지원 |
| △ | 일부 지원 또는 제약 있음 |
