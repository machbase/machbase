---
type: docs
title: '연동 방식 선택'
weight: 10
---

Machbase는 C/C++, Java, Python, .NET, Go, Node.js, REST API 등 다양한 연동 방식을 제공합니다. 이 섹션에서는 프로젝트의 요구사항에 맞는 연동 방식을 선택하는 방법을 안내합니다.

## 이 섹션의 구성

| 문서 | 내용 |
|------|------|
| [연동 방식 선택 가이드](selection-guide-integration-method/) | 언어, 성능 요구사항, 환경별 선택 매트릭스와 결정 트리 |
| [SDK/API canonical owner 구분](distinction-sdk-api-canonical-owner/) | 각 SDK의 완전한 API 명세 위치 안내 |

## 선택 시 고려사항

연동 방식을 선택할 때는 다음 세 가지 관점에서 검토합니다.

**개발 언어와 생태계**
프로젝트에서 사용하는 언어와 기존 라이브러리 생태계를 우선 고려합니다. Java 프로젝트라면 JDBC, Python 데이터 파이프라인이라면 Python SDK가 자연스러운 선택입니다.

**데이터 입력 성능**
초당 수만 건 이상의 대용량 시계열 데이터를 입력해야 한다면 Append API를 지원하는 CLI/ODBC, JDBC, Python SDK가 적합합니다. REST API는 편의성이 높지만 고속 대량 입력에는 적합하지 않습니다.

**운영 환경**
방화벽으로 인해 TCP 5656 포트를 사용할 수 없는 환경이라면 HTTP 기반 REST API를 검토합니다. Windows 환경의 산업용 애플리케이션이라면 .NET 드라이버나 ODBC를 우선 고려합니다.
