---
type: docs
title: '16.8.13 全文とRAGドキュメントインデックス'
weight: 130
toc: true
---

現行のDBMSマニュアルは、全文Markdownとページ単位のJSONインデックスを提供します。

## 全文

| 言語 | URL |
|------|-----|
| 英語 | [llms-full.txt](/llms-full.txt) |
| 韓国語 | [llms-full.txt](/kr/llms-full.txt) |
| 日本語 | [llms-full.txt](/ja/llms-full.txt) |

全文は、公開済みDBMSページをナビゲーションのweight順に連結します。各ページの境界には
タイトル、言語、正規URLを記載し、本文はソースのMarkdownを保持します。

## JSONインデックス

| 言語 | URL |
|------|-----|
| 英語 | [llms-chunks.json](/llms-chunks.json) |
| 韓国語 | [llms-chunks.json](/kr/llms-chunks.json) |
| 日本語 | [llms-chunks.json](/ja/llms-chunks.json) |

スキーマバージョン1の最上位フィールドは次のとおりです。

| フィールド | 説明 |
|------|------|
| `schema_version` | JSONの仕様バージョン。現在は`1` |
| `product` | `Machbase DBMS` |
| `manual_version` | マニュアルの対象製品バージョン |
| `language` | `en`、`kr`、`ja` |
| `document_count` | `documents`配列の要素数 |
| `documents` | ドキュメントのメタデータ配列 |

各ドキュメントは`id`、`title`、`url`、`markdown_url`、`kind`、`parent_url`、`weight`、
`last_modified`を提供します。JSONには本文を重複保存しません。`markdown_url`から
ページ別のMarkdownを取得するか、`llms-full.txt`をコーパスとして使用します。

## チャンクの境界

現在のインデックスは、1つの公開済みページを1つのドキュメントチャンクとして扱います。
SQL構文、SDKの作業、運用手順は可能な限り個別ページに保持されるため、URLとタイトルを
安定したチャンク識別子として使用できます。大きな辞典ページを細分化するときも既存ページの`id`を保持します。

ビルド時刻などの非決定的な値は出力しません。Neo、DBMS 8.5、ドラフト、エイリアスページは
インデックスと全文の両方から除外します。
