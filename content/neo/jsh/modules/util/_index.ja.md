---
toc: true
title: "util"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`util`モジュールグループは、JSHアプリケーションや組み込みコマンドでよく使用する小さなヘルパーAPIを提供します。

現在のモジュールグループは、次のサブモジュールで構成されます。

- `util/parseArgs`: コマンドライン形式の引数パーサー
- `util/splitFields`: 引用符を認識するシェル形式のフィールド分割機能

各ヘルパーは、対応するモジュールパスから直接読み込んで使用します。

```js
const parseArgs = require('util/parseArgs');
const splitFields = require('util/splitFields');
```

オプション、位置引数、サブコマンド、ヘルプテキストの生成を扱う場合は、`parseArgs`を使用してください。
文字列を空白で分割し、引用符で囲まれた部分を1つのフィールドとして保持する場合は、`splitFields`を使用してください。

{{< children_toc />}}
