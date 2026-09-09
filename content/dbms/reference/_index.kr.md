---
type: docs
title: '16. 레퍼런스'
weight: 160
toc: true
---

문법, 함수, 설정, 시스템 카탈로그의 정확한 정의를 빠르게 찾아보는 종합 레퍼런스입니다.
SDK/API 문서는 11장 개발 및 애플리케이션 연동에서, 개념이나 사용 예시는 각 기능 장에서
확인하십시오.

## 구성

| 섹션 | 설명 |
|------|------|
| [SQL 레퍼런스](./sql/) | SQL 문법 사전, 함수 사전, 데이터 타입, 힌트, 상대 시간 표현 |
| [설정 레퍼런스](./configuration/) | machbase.conf 속성, 동적 변경 가능 속성 목록 |
| [명령줄 도구](./command-line-tools/) | machsql, machadmin, machloader 등 CLI 도구 옵션 |
| [개발 도구 연동](../development-tools-integration/) | Go, Python, Java, C 클라이언트 SDK/API (11장) |
| [시스템 카탈로그](./system-catalog/) | V$, M$SYS 뷰 목록 및 컬럼 설명 |
| [에러 코드](./error-codes/) | 에러 코드 번호, 메시지, 원인 및 조치 방법 |
| [지원 범위 및 제약](./support-scope-constraints/) | 테이블 유형별 기능 지원 여부, 알려진 제약 사항 |
| [AI Agent Reference](./ai-agent-reference/) | AI·RAG용 탐색 가이드, 정본 맵과 LLM 출력 |

## 활용 방법

- **문법 확인** → [SQL 문법 사전](./sql/syntax/)
- **함수 인자와 반환값** → [SQL 함수 사전](./sql/functions/)
- **데이터 타입 범위와 기본값** → [데이터 타입 사전](./sql/types/)
- **설정값 의미와 허용 범위** → [설정 레퍼런스](./configuration/)
- **에러 원인 파악** → [에러 코드](./error-codes/)

> 동작 원리, 선택 기준, 운영 가이드는 해당 기능을 다루는 장을 참고하십시오.
