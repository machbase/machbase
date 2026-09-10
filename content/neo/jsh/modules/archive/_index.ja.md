---
toc: true
title: "archive"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

archiveモジュールグループは、JSHアプリケーションでTARおよびZIPアーカイブを扱う機能を提供します。

両サブモジュールは、以下の機能に対応しています。

- メモリ上でのアーカイブの作成・展開
- コールバック形式の非同期ラッパー
- ストリーム形式のwriter / readerオブジェクト
- `.tar`、`.zip`ファイルを扱うファイルベースのクラスAPI

ディレクトリエントリまたはTARリンクのメタデータが必要な場合は、`archive/tar`を使用してください。
一般的なZIPツールとそのまま互換性のある圧縮アーカイブが必要な場合は、`archive/zip`を使用してください。

{{< children_toc />}}
