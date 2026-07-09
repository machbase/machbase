---
type: docs
title: '입력 방식 선택 가이드'
weight: 20
---

상황별로 최적의 입력 방법을 선택하는 기준을 정리합니다.

## 선택 플로우

```
데이터를 어디서 생성하는가?
├── 파일(CSV 등)
│   ├── 서버에서 직접 읽을 수 있다 → LOAD DATA INFILE
│   ├── 빠른 적재가 필요, 유연한 매핑 필요 → machloader
│   └── 단순 CSV → csvimport
│
├── 애플리케이션/SDK
│   ├── 대량 시계열 (수만 건/초 이상) → Append API
│   ├── RDB 대량 batch 입력 → client appendBatch/append stream
│   └── 소량 또는 일반 트랜잭션 처리 → SQL INSERT
│
├── HTTP/REST
│   └── 외부 시스템, IoT → REST API (8장 참고)
│
└── TAG 메타데이터
    └── 초기 로드 또는 일괄 업데이트 → tagmetaimport
```

## 성능 기준 선택

| 처리량 목표 | 권장 방법 |
|-----------|---------|
| 수백만 건/초 (TAG/LOG) | Append API (SDK) |
| 수십만 건/초 | Append API, client appendBatch 또는 machloader 병렬 |
| 수천~수만 건/초 | LOAD DATA INFILE 또는 machloader |
| 수백 건/초 이하 | SQL INSERT |

## 실시간 vs 배치

| 구분 | 권장 방법 |
|------|---------|
| 실시간 스트리밍 | REST API, SDK Append API |
| 정기 배치 | machloader, csvimport, LOAD DATA INFILE |
| 이벤트 기반 | SDK INSERT 또는 REST API |

## 연동 경로 요약

- **REST API 상세**: [8장 애플리케이션 연동](/dbms/application-integration/) 참고
- **SDK (Go/Python/C) 상세**: [8장 애플리케이션 연동](/dbms/application-integration/) 참고
