---
type: docs
title: '입력 방식 선택'
weight: 10
---

Machbase에 데이터를 입력하는 방법은 사용 목적과 데이터 볼륨에 따라 선택합니다.

## 입력 방법 개요

| 입력 방법 | 특징 | 주요 사용 사례 |
|----------|------|--------------|
| SQL INSERT | 단건·소량. 트랜잭션 지원 | 설정값 등록, 테스트 |
| Append API | 초고속 대량 입력. 비트랜잭션 버퍼 | TAG/LOG 시계열 대량 수집 |
| LOAD DATA INFILE | SQL로 서버 측 파일 직접 로드 | 서버에 위치한 대용량 파일 일괄 적재 |
| machloader | CLI 도구. 유연한 스키마 매핑 | 정기 배치, 마이그레이션 |
| csvimport | machloader 래퍼. 간편 CSV 입력 | 빠른 파일 적재 |
| tagmetaimport | TAG 메타데이터 전용 | TAG 메타데이터 초기 로드·업데이트 |
| REST API | HTTP 기반. 범용 연동 | 외부 시스템, IoT 디바이스 |
| SDK (Go/Python/C) | 내장 Append/INSERT | 애플리케이션 직접 연동 |

상세 선택 가이드는 하위 페이지를 참고하세요.
