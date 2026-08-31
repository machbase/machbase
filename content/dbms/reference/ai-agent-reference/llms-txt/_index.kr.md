---
type: docs
title: '17.8.12 llms.txt'
weight: 120
toc: true
---

`llms.txt`는 LLM이 현재 Machbase DBMS 매뉴얼의 구조와 주요 정본을 빠르게 찾도록 제공하는
UTF-8 plain-text 목차입니다.

## URL

| 언어 | URL |
|------|-----|
| 영어 | [https://docs.machbase.com/llms.txt](/llms.txt) |
| 한국어 | [https://docs.machbase.com/kr/llms.txt](/kr/llms.txt) |

출력은 현재 `/dbms/` 문서만 포함합니다. Machbase Neo, 보존용 DBMS 8.5, draft와 alias
페이지는 포함하지 않습니다.

## 내용

- 제품과 매뉴얼 버전
- DBMS 상위 장과 canonical URL
- SQL, SDK, 운영, 지원 범위와 오류 코드 정본
- AI Agent Reference
- 전체 본문과 JSON 인덱스 URL

## 사용 방법

1. `llms.txt`에서 질문 주제의 canonical section을 찾습니다.
2. 개별 Markdown이 필요하면 해당 문서 URL의 `index.md`를 읽습니다.
3. 전체 corpus가 필요하면 [llms-full.txt](../llms-full-txt-chunk-index/)를 사용합니다.
4. crawler가 문서 단위 metadata를 필요로 하면 `llms-chunks.json`을 사용합니다.

`llms.txt`는 제품 사실의 정본이 아니라 탐색용 인덱스입니다. 실제 답변은 링크된 현재
문서를 확인해 작성합니다.
