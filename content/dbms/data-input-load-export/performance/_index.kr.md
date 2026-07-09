---
type: docs
title: '입력 성능과 연동 경로'
weight: 70
---

데이터 입력 경로별 성능 특성과 선택 기준을 정리합니다.

## 입력 경로별 성능 비교

| 입력 경로 | 최대 처리량 | 지연 | 주요 특징 |
|----------|-----------|------|---------|
| SDK Append API | TAG/LOG에서 수백만 건/초 | 최소 | 내부 Append 버퍼. RDB는 client appendBatch/stream 경로 |
| REST API (JSON) | 수만~수십만 건/초 | 낮음 | HTTP 오버헤드, 범용성 |
| machloader | 수십만~수백만 건/초 | 파일 기반 | 배치 적재, 병렬 실행 가능 |
| LOAD DATA INFILE | 수십만~수백만 건/초 | 파일 기반 | 서버 직접 읽기, 네트워크 무관 |
| SQL INSERT | 수천~수만 건/초 | 트랜잭션 포함 | 단건/소량, 모든 테이블 타입 |

## 이 절에서 다루는 내용

- **[입력 성능 기본 원칙](./performance-principles/)**: 처리량을 높이는 핵심 원칙
- **[REST 입력 경로 안내](./path-guide-rest/)**: REST API 연동 개요 (상세는 8장)
- **[SDK 입력 경로 안내](./path-guide-sdk/)**: SDK Append/INSERT 개요 (상세는 8장)
- **[Fluentd 파이프라인](./pipeline-fluentd/)**: Fluentd 기반 파이프라인 개요 (상세는 8장)
