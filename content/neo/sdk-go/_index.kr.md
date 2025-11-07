---
title: Go SDK
type: docs
weight: 65
---

Machbase-neo는 Go 개발자를 위해 두 가지 유형의 Go 클라이언트 라이브러리를 제공합니다.
첫 번째는 Go 표준 SQL 드라이버 호환 `machrpc`, 두 번째는 네이티브 C 클라이언트 라이브러리를 감싸는 `machcli` 패키지입니다.

- `machcli`는 *네이티브 포트*를 통해 통신하는 C 구현을 감싸는 Go 래퍼이며, 기본 포트는 `5656`입니다.
- `machrpc`는 SQL 드라이버로 순수 Go 구현이므로 CGo가 필요하지 않습니다. 전송을 위해 gRPC 계층에 의존하므로 기본적으로 TLS 인증이 필요합니다. gRPC 포트는 `5655`입니다.

## 다른 프로그래밍 언어

Go 이외의 프로그래밍 언어를 사용하는 경우, 최고의 유연성을 위해 HTTP API 사용을 고려하세요. HTTP를 데이터베이스 상호작용에 사용하지 않으려면, proto 파일을 트랜스파일하여 gRPC를 사용할 수 있습니다.

최신 `.proto` 파일은 GitHub에서 호스팅됩니다. [여기서 찾아보세요](https://github.com/machbase/neo-server/tree/main/api/proto/machrpc.proto).

{{< callout type="warning" >}}
gRPC 인터페이스는 저수준 API를 제공하므로 클라이언트 프로그램은 이를 올바르게 사용해야 합니다. 부정확한 사용은 Machbase의 오작동을 초래할 수 있습니다.
{{< /callout >}}

## 이 장에서 다루는 내용

{{< children_toc />}}
