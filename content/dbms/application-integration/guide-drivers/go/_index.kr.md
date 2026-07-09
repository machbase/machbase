---
type: docs
title: '11.3.6 Go'
weight: 60
---

## 개요

Machbase는 Go 애플리케이션을 위해 두 가지 연결 방식을 제공합니다.

| 방식 | 패키지 | 특징 |
|------|--------|------|
| [Go 클라이언트](./go/) | `github.com/machbase/neo-client/machgo` | Machbase 네이티브 API, Append 고속 삽입 지원 |
| [Go SQL 드라이버](./go-sql/) | `github.com/machbase/neo-client` | Go 표준 `database/sql` 인터페이스 |

## 어느 방식을 선택해야 하나요?

**Go 클라이언트 (`machgo`)를 선택하세요:**
- 최대 성능이 필요한 경우 (Append API로 고속 대량 삽입)
- Machbase 고유 기능(세밀한 연결 튜닝, FetchRows 제어 등)을 활용하고 싶은 경우
- 신규 프로젝트에서 Machbase 전용 코드로 작성하는 경우

**Go SQL 드라이버를 선택하세요:**
- 기존 코드가 `database/sql` 인터페이스를 사용하는 경우
- GORM, sqlx 등 `database/sql` 기반 라이브러리와 함께 사용하는 경우
- 여러 데이터베이스를 추상화된 인터페이스로 다루는 경우

## 공통 사전 요구사항

- Machbase 서버가 네이티브 포트(기본 `5656`)로 접근 가능해야 합니다.
- Go 1.22 이상이 설치되어 있어야 합니다.

## 패키지 설치

두 방식 모두 동일한 패키지를 사용합니다.

```sh
go get github.com/machbase/neo-client@latest
```
