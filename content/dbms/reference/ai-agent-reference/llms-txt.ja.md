---
type: docs
title: '16.8.12 llms.txt'
weight: 120
toc: true
---

`llms.txt`は、LLMが現行のMachbase DBMSマニュアルの構造と主な正式リファレンスを
すばやく見つけるための、UTF-8プレーンテキスト形式の目次です。

## URL

| 言語 | URL |
|------|-----|
| 英語 | [https://docs.machbase.com/llms.txt](/llms.txt) |
| 韓国語 | [https://docs.machbase.com/kr/llms.txt](/kr/llms.txt) |
| 日本語 | [https://docs.machbase.com/ja/llms.txt](/ja/llms.txt) |

出力には現行の`/dbms/`ドキュメントのみを含みます。Machbase Neo、保存用のDBMS 8.5、
ドラフト、エイリアスページは含みません。

## 内容

- 製品とマニュアルのバージョン
- DBMSの上位章と正規URL
- SQL、SDK、運用、サポート範囲、エラーコードの正式な参照先
- AI Agent Reference
- 全文とJSONインデックスのURL

## 利用方法

1. `llms.txt`で質問のトピックに対応する正規セクションを探します。
2. 個別のMarkdownが必要な場合は、該当ドキュメントURLの`index.md`を読みます。
3. コーパス全体が必要な場合は[llms-full.txt](../llms-full-txt-chunk-index/)を使用します。
4. クローラーでドキュメント単位のメタデータが必要な場合は`llms-chunks.json`を使用します。

`llms.txt`は参照先を探すためのインデックスであり、製品仕様の正式な根拠ではありません。
回答を作成するときはリンク先の現行ドキュメントを確認します。
