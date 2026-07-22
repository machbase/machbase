---
type: docs
title: '17.10.13 llms-full.txt / chunk index'
weight: 130
toc: true
---

이 페이지는 RAG(Retrieval-Augmented Generation) 시스템이 Machbase 매뉴얼 전체를 청크 단위로 검색할 수 있도록 인덱싱 메타데이터를 제공합니다.

## 목적

- 대형 언어 모델(LLM)이 이 매뉴얼 전체를 청크 단위로 검색할 수 있도록 인덱싱 메타데이터 제공
- RAG 파이프라인에서 관련 청크를 효율적으로 검색하기 위한 범주별 안내
- `llms-full.txt` 파일의 구조와 청크 구성 원칙 설명

## 청크 구성 원칙

- 각 섹션(`_index.kr.md`)이 독립적인 하나의 청크
- 청크 메타데이터 구성 요소:
  - **URL**: 해당 섹션의 정규 URL (`/dbms/...`)
  - **제목**: 섹션 제목 (`title` frontmatter)
  - **키워드**: 섹션 핵심 용어 목록
  - **섹션 깊이**: 문서 계층 깊이 (1~4단계)
  - **weight**: 섹션 순서 (낮을수록 앞)

## 주요 청크 범주

| 범주 | 예상 섹션 수 | 핵심 키워드 예시 | 대표 URL |
|------|:-----------:|----------------|----------|
| 핵심 개념 | ~15 | TAG, LOG, LOOKUP, VOLATILE, TRANSACTION, ROLLUP, STREAM, Append, BASETIME | `/dbms/core-concepts/` |
| 시작하기 | ~10 | 설치, 빠른 시작, 첫 번째 쿼리, machadmin | `/dbms/getting-started/` |
| 애플리케이션 연동 | ~50 | JDBC, Python, Go, .NET, Node.js, REST, Append, machbaseAPI, machcli | `/dbms/application-integration/` |
| 성능 튜닝 | ~20 | 배치 크기, ROLLUP, 캐시, Append 최적화, 인덱스 | `/dbms/performance/` |
| 운영 / 설정 | ~80 | BACKUP, MOUNT, ALTER SYSTEM, 설정 파라미터, machadmin, machclusterctl | `/dbms/operations-configuration-recovery/` |
| 보안 | ~40 | 사용자, 권한, AUTH KEY, GRANT, REVOKE, 원격 접속, 암호화 | `/dbms/security-access-control/` |
| 시나리오 | ~15 | IoT, 파이프라인, 대시보드, Grafana, 센서 데이터 | `/dbms/scenarios/` |
| 문제 해결 | ~35 | 오류, 진단, 복구, Connection refused, 느린 쿼리, ROLLUP 문제 | `/dbms/troubleshooting/` |
| 레퍼런스 | ~100 | SQL, DDL, DML, SELECT, 내장 함수, 데이터 타입, 설정, 에러 코드, 도구 | `/dbms/reference/` |

## 청크 메타데이터 예시

```json
{
  "url": "/dbms/core-concepts/tag-table/",
  "title": "TAG 테이블",
  "keywords": ["TAG", "BASETIME", "SUMMARIZED", "Append", "ROLLUP", "시계열"],
  "depth": 2,
  "weight": 10,
  "section": "core-concepts"
}
```

## llms-full.txt 파일 접근

`llms-full.txt`는 이 문서 사이트의 루트에서 다음 경로로 접근할 수 있습니다:

```
https://<docs-site>/llms-full.txt
```

이 파일은 모든 섹션의 내용을 단일 텍스트 파일로 합친 것으로, RAG 시스템의 초기 인덱싱에 활용할 수 있습니다.

## RAG 시스템 연동 권장 사항

1. **청크 분할 단위**: 섹션(`_index.kr.md`) 단위를 기본으로 사용
2. **임베딩 우선순위**: 핵심 개념, 레퍼런스, 문제 해결 범주를 우선 인덱싱
3. **메타데이터 필터링**: `section` 또는 `keywords` 기반으로 관련 청크를 사전 필터링
4. **URL 정규화**: [canonical-url-map](../canonical-url-map/)에서 정규 URL 확인
5. **버전 관리**: 이 문서는 Machbase 8.6 기준. 버전 태그를 메타데이터에 포함 권장

## 참조

- 문서 구조 목차: [llms.txt](../llms-txt/)
- 정규 URL 맵: [canonical-url-map](../canonical-url-map/)
- AI Agent Reference 전체: [AI Agent Reference](../)
