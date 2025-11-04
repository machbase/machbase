---
title: gRPC API
type: docs
weight: 130
---

gRPC는 Machbase의 1급 API로, gRPC를 지원하는 모든 프로그래밍 언어에서 기능을 온전히 활용할 수 있습니다.

{{< callout type="warning" >}}
gRPC 인터페이스는 저수준 API이므로 클라이언트 프로그램이 올바르게 사용해야 합니다. 잘못 사용할 경우 Machbase가 정상적으로 동작하지 않을 수 있습니다.
{{< /callout >}}

### proto file

최신 `.proto` 파일은 GitHub에 호스팅되어 있습니다. [GitHub에서 확인해 주십시오](https://github.com/machbase/neo-server/tree/main/api/proto/machrpc.proto).

## 이 장에서 안내하는 내용

{{< children_toc />}}
