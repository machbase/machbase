---
title: モジュール
type: docs
weight: 900
toc: true
---

{{< neo_since ver="8.0.75" />}}

JSHモジュールは、Machbase Neoに組み込まれた標準ライブラリです。
TQLの`SCRIPT()`ブロックと独立した`*.js`アプリケーションの両方で使用でき、
追加のパッケージをインストールせずに、`require()`で直接読み込めます。

モジュール名には、`fs`、`os`、`net`のような短い名前と、
`archive/tar`のようなグループパス形式の名前があります。

## モジュールの読み込み {#모듈-불러오기}

必要なモジュール名を`require()`に渡して読み込みます。

```js
const fs = require('fs');
const os = require('os');

console.println('cwd entries:', fs.readDir('.').length);
console.println('platform:', os.platform(), os.arch());
```

JSHモジュールはランタイムに組み込まれているため、ファイル処理、ネットワーク、システム情報、
データの書式設定、データベースアクセスなどの機能を、標準ライブラリとしてすぐに使用できます。

各モジュールのAPIと詳細な例は、以下のドキュメントを参照してください。

{{< children_toc />}}
