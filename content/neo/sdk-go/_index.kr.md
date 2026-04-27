---
title: Go SDK
type: docs
weight: 65
draft: true
---

Machbase-neo는 Go 개발자를 위해 세 가지 유형의 Go 클라이언트 라이브러리를 제공합니다.
최고의 성능과 크로스 플랫폼 배포를 위해 **`machgo` 사용을 권장**합니다.
`machcli`는 하위 호환을 위해 현재 유지되고 있지만, 향후 릴리즈에서 deprecated로 표시되고 이후 제거될 수 있습니다.

- `machgo` <span class="badge-new">NEW!</span>(권장)는 *네이티브 포트*(기본 `5656`)용 순수 Go 구현이며, `machcli`와 호환되는 API를 제공합니다. [자세히 보기](/kr/neo/sdk-go/machgo/)
- `machcli`는 *네이티브 포트*(기본 `5656`)를 사용하는 C 구현 기반 Go 래퍼이며, 하위 호환을 위해 유지됩니다.

{{< callout type="warning" >}}
`machcli`는 향후 릴리즈에서 deprecated로 표시될 수 있으며, 이후 제거될 수 있습니다.
새로운 개발에는 가능한 한 `machgo`를 사용하세요.
{{< /callout >}}

## 다른 프로그래밍 언어

Go 이외의 프로그래밍 언어를 사용하는 경우, 최고의 유연성을 위해 HTTP API 사용을 고려하세요.

## 이 장에서 다루는 내용

{{< children_toc />}}
