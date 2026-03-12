---
title: Go SDK
type: docs
weight: 65
---

Machbase-neo는 Go 개발자를 위해 세 가지 유형의 Go 클라이언트 라이브러리를 제공합니다.
최고의 성능과 크로스 플랫폼 배포를 위해 **`machgo` 사용을 권장**합니다.
`machcli`와 `machrpc`는 하위 호환을 위해 현재 유지되고 있지만, 향후 릴리즈에서 deprecated로 표시되고 이후 제거될 수 있습니다.

- `machgo` <span class="badge-new">NEW!</span>(권장)는 *네이티브 포트*(기본 `5656`)용 순수 Go 구현이며, `machcli`와 호환되는 API를 제공합니다. [자세히 보기](/kr/neo/sdk-go/machgo/)
- `machcli`는 *네이티브 포트*(기본 `5656`)를 사용하는 C 구현 기반 Go 래퍼이며, 하위 호환을 위해 유지됩니다.
- `machrpc`는 gRPC 기반 Go SQL-드라이버 스타일 클라이언트(기본 `5655`)로, 일반적으로 TLS 인증서가 필요하며 하위 호환을 위해 유지됩니다. 

{{< callout type="warning" >}}
`machcli`와 `machrpc`는 향후 릴리즈에서 deprecated로 표시될 수 있으며, 이후 제거될 수 있습니다.
새로운 개발에는 가능한 한 `machgo`를 사용하세요.
{{< /callout >}}

<!-- ## 다른 프로그래밍 언어

Go 이외의 프로그래밍 언어를 사용하는 경우, 최고의 유연성을 위해 HTTP API 사용을 고려하세요. HTTP를 데이터베이스 상호작용에 사용하지 않으려면, proto 파일을 트랜스파일하여 gRPC를 사용할 수 있습니다.

최신 `.proto` 파일은 GitHub에서 호스팅됩니다. [여기서 찾아보세요](https://github.com/machbase/neo-server/tree/main/api/proto/machrpc.proto).

{{< callout type="warning" >}}
gRPC 인터페이스는 저수준 API를 제공하므로 클라이언트 프로그램은 이를 올바르게 사용해야 합니다. 부정확한 사용은 Machbase의 오작동을 초래할 수 있습니다.
{{< /callout >}} -->

## 이 장에서 다루는 내용

{{< children_toc />}}
