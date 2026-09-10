---
toc: true
title: Go SDK
type: docs
weight: 65
draft: true
---

Machbase-neoはGo開発者向けに、3種類のGoクライアントライブラリを提供します。
性能とクロスプラットフォームでの配布のため、**`machgo`の使用を推奨**します。
`machcli`は後方互換性のために維持していますが、将来のリリースで非推奨となり、その後削除される可能性があります。

- `machgo` <span class="badge-new">NEW!</span>（推奨）は、*ネイティブポート*（既定値`5656`）用の純粋なGo実装で、`machcli`と互換性のあるAPIを提供します。[詳細](/neo/tutorials/cli-go/)
- `machcli`は、*ネイティブポート*（既定値`5656`）を使用するC実装のGoラッパーで、後方互換性のために維持しています。

{{< callout type="warning" >}}
`machcli`は将来のリリースで非推奨となり、その後削除される可能性があります。
新規開発では、できる限り`machgo`を使用してください。
{{< /callout >}}

## 他のプログラミング言語 {#다른-프로그래밍-언어}

Go以外のプログラミング言語を使用する場合は、柔軟性に優れたHTTP APIの利用を検討してください。

## この章の内容 {#이-장에서-다루는-내용}

{{< children_toc />}}
