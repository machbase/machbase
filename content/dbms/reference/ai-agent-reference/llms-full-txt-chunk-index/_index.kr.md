---
type: docs
title: '17.8.13 전체 본문과 RAG 문서 인덱스'
weight: 130
toc: true
---

현재 DBMS 매뉴얼은 전체 Markdown 본문과 페이지 단위 JSON 인덱스를 제공합니다.

## 전체 본문

| 언어 | URL |
|------|-----|
| 영어 | [llms-full.txt](/llms-full.txt) |
| 한국어 | [llms-full.txt](/kr/llms-full.txt) |

전체 본문은 navigation weight 순서로 published DBMS 페이지를 연결합니다. 각 페이지 경계에는
제목, 언어와 canonical URL이 있으며 본문은 source Markdown을 유지합니다.

## JSON 인덱스

| 언어 | URL |
|------|-----|
| 영어 | [llms-chunks.json](/llms-chunks.json) |
| 한국어 | [llms-chunks.json](/kr/llms-chunks.json) |

schema version 1의 최상위 필드는 다음과 같습니다.

| 필드 | 설명 |
|------|------|
| `schema_version` | JSON 계약 버전. 현재 `1` |
| `product` | `Machbase DBMS` |
| `manual_version` | 문서 대상 제품 버전 |
| `language` | `en` 또는 `kr` |
| `document_count` | `documents` 배열 크기 |
| `documents` | 문서 metadata 배열 |

각 문서는 `id`, `title`, `url`, `markdown_url`, `kind`, `parent_url`, `weight`,
`last_modified`를 제공합니다. JSON에는 본문을 중복 저장하지 않습니다. `markdown_url`에서
페이지별 Markdown을 가져오거나 `llms-full.txt`를 corpus로 사용합니다.

## Chunk 경계

현재 인덱스는 한 published page를 한 document chunk로 취급합니다. SQL 문법, SDK 작업과
운영 절차가 가능한 한 개별 페이지에 유지되므로 URL과 제목을 안정적인 chunk 식별자로
사용할 수 있습니다. 큰 사전 페이지를 더 나눌 때도 기존 page `id`는 유지합니다.

빌드 시각 같은 비결정적 값은 출력하지 않습니다. Neo, DBMS 8.5, draft와 alias 페이지는
인덱스와 전체 본문에서 제외합니다.
