---
toc: true
title: パッケージマネージャー
type: docs
weight: 200
---

`pkg`コマンドは、`package.json`の作成、JSHパッケージのインストール、パッケージスクリプトの実行を行います。
JSHアプリケーションで、`/work`などのプロジェクトディレクトリ内の依存関係を管理する場合に使用します。

## 概要 {#개요}

`pkg`コマンドは、以下の操作に対応しています。

- 新しい`package.json`の作成
- `node_modules`への依存関係のインストール
- GitHubプロジェクトを任意のディレクトリにコピーし、その場所にプロジェクトの依存関係をインストール
- `package-lock.json`の管理
- `package.json`の`scripts`の実行
- インストールしたパッケージの`bin`項目から実行ラッパーを生成
- 依存関係と生成したラッパーの削除

## package.json {#packagejson}

`pkg`は、`package.json`を選択したパッケージルートのマニフェストとして扱います。
通常のプロジェクトインストールでは、現在のディレクトリ、または`--dir`で指定したディレクトリがルートです。
`pkg install -g`、`pkg uninstall -g`では、パッケージは`/work/node_modules`にインストールされますが、`/work/package.json`と`/work/package-lock.json`は作成しません。

最小構成のプロジェクトマニフェストは以下のとおりです。

```json
{
  "name": "demo-app",
  "version": "1.0.0",
  "scripts": {
    "start": "./main.js"
  },
  "dependencies": {
    "generic-pkg": "^1.2.0",
    "github.com/acme/demo": "#tag=v1.1.0"
  }
}
```

`pkg`が主に使用するフィールドは以下のとおりです。

| フィールド | 型 | 説明 |
| --- | --- | --- |
| `name` | `String` | プロジェクトのパッケージ名 |
| `version` | `String` | プロジェクトのバージョン |
| `scripts` | `Object` | `pkg run`で実行する、名前付きのコマンドライン |
| `dependencies` | `Object` | パッケージ名とバージョン指定子のマップ |

補足：

- `scripts`は、現在のプロジェクトマニフェストの項目で、`pkg run`だけが使用します。
- `dependencies`は、選択したパッケージルートを基準に、`pkg install`と`pkg uninstall`が更新します。
- 通常のプロジェクトインストールでは、再現可能なインストールのため、`pkg`は`package.json`と同じ場所に`package-lock.json`も書き込みます。
- `bin`は、`node_modules`内の各インストール済みパッケージの`package.json`から読み取ります。`pkg`は、これに基づいて`node_modules/.bin`にラッパーを生成します。

たとえば、`pkg install -g github.com/acme/demo`を実行すると、パッケージのマニフェストは`/work/node_modules/github.com/acme/demo/package.json`に置かれ、`pkg`のグローバルメタデータは`/work/node_modules/.pkg/`に保存されます。

## pkg init {#pkg-init}

現在のプロジェクトディレクトリに、新しい`package.json`を作成します。

<h6>構文</h6>

```sh
pkg init [options] <name>
```

<h6>オプション</h6>

- `-C, --dir <dir>` 現在の作業ディレクトリではなく、指定したプロジェクトディレクトリを使用します。
- `-h, --help` ヘルプを表示します。

<h6>使用例</h6>

```sh
/work > pkg init demo-app
Created /work/package.json
```

作成するファイルには、空の`scripts`と`dependencies`オブジェクトが含まれます。

```json
{
  "name": "demo-app",
  "version": "1.0.0",
  "scripts": {},
  "dependencies": {}
}
```

## pkg install {#pkg-install}

`package.json`に宣言した依存関係をインストールします。または、指定した単一のパッケージをインストールし、
`package.json`と`package-lock.json`を更新します。

<h6>構文</h6>

```sh
pkg install [options] [name]
```

<h6>オプション</h6>

- `-C, --dir <dir>` 現在の作業ディレクトリではなく、指定したプロジェクトディレクトリを使用します。
- `-g, --global` `--dir`を無視して、グローバルパッケージディレクトリにインストールします。このディレクトリはグローバルパッケージ専用のため、通常のプロジェクトルートに使用しないでください。
- `-h, --help` ヘルプを表示します。

`name`を省略すると、選択したプロジェクトマニフェストに宣言済みの依存関係をインストールします。`-g`では、`/work/node_modules/.pkg/`内の内部メタデータを使用します。

### グローバルインストール {#전역-설치}

`pkg install -g <name>`は、`/work/node_modules`にインストールします。
`-g`を指定すると、`pkg`は`--dir`を無視します。
グローバルパッケージディレクトリは、グローバルパッケージとメタデータのための予約領域です。通常のプロジェクトは、`/work`自体ではなく、`/work/my-app`などのサブディレクトリに作成してください。

この方式で、次の2つの用途に対応できます。

- `bin`ラッパーをシェルの`PATH`から直接実行できる、グローバルコマンドパッケージのインストール
- グローバルパッケージディレクトリへの共有ライブラリパッケージのインストール

例を示します。

```sh
/work > pkg install -g github.com/acme/demo
Installed github.com/acme/demo#tag=v1.1.0
```

### npmパッケージ {#npm-패키지}

パッケージ名がGitHubリポジトリのパスでなければ、npmレジストリからインストールします。

```sh
/work > pkg install generic-pkg
Installed generic-pkg@1.2.0
```

この場合、`package.json`には解決したnpmバージョン範囲を保存します。

```json
{
  "dependencies": {
    "generic-pkg": "^1.2.0"
  }
}
```

### GitHubリポジトリのパッケージ {#github-저장소-패키지}

パッケージ名が`github.com/<org>/<repo>`形式なら、GitHubリポジトリの内容を直接ダウンロードしてインストールします。

対応する形式は以下のとおりです。

- `github.com/<org>/<repo>`
- `github.com/<org>/<repo>@<tag>`
- `github.com/<org>/<repo>#tag=<tag>`
- `github.com/<org>/<repo>#branch=<branch>`

動作は以下のとおりです。

- `@<tag>`または`#tag=<tag>`を指定すると、そのタグを使用します。
- `#branch=<branch>`を指定すると、タグの有無に関係なく、そのブランチを使用します。
- タグを指定せず、リポジトリにタグがある場合は、GitHub tags APIが返す最新タグを使用します。
- タグを指定せず、リポジトリにタグがない場合は、リポジトリの`default_branch`を使用します。

<h6>使用例: 最新タグのインストール</h6>

```sh
/work > pkg install github.com/acme/demo
Installed github.com/acme/demo#tag=v1.1.0
```

<h6>使用例: 指定タグのインストール</h6>

```sh
/work > pkg install github.com/acme/demo@v1.0.0
Installed github.com/acme/demo#tag=v1.0.0
```

明示的なref構文も使用できます。

```sh
/work > pkg install github.com/acme/demo#tag=v1.0.0
Installed github.com/acme/demo#tag=v1.0.0
```

<h6>使用例: 指定ブランチのインストール</h6>

```sh
/work > pkg install github.com/acme/demo#branch=develop
Installed github.com/acme/demo#branch=develop
```

<h6>使用例: 既定ブランチへのフォールバック</h6>

リポジトリにタグがない場合は、既定のブランチを使用します。

```sh
/work > pkg install github.com/acme/notags
Installed github.com/acme/notags#branch=main
```

### インストール先 {#설치-위치}

インストールしたパッケージは、選択した`node_modules`ディレクトリにコピーされます。
例を示します。

- `generic-pkg` -> `node_modules/generic-pkg`
- `github.com/acme/demo` -> `node_modules/github.com/acme/demo`

GitHubリポジトリのパッケージも、`node_modules`にインストールされます。
`pkg install -g`を使用すると、この場所は`/work/node_modules`になります。

インストールしたパッケージの`package.json`に`bin`がある場合、`pkg`は`node_modules/.bin`にラッパーを生成します。
ラッパー名は、パッケージマニフェストの`bin`設定に従います。

対応する`bin`の形式は、次の2つです。

- 文字列形式：`"bin": "main.js"`
- オブジェクト形式：`"bin": { "demo": "demo.js" }`

`bin`が文字列の場合、`pkg`はパッケージ名からラッパー名を決めます。
たとえば、`github.com/acme/demo`は`demo.js`を生成します。
`bin`がオブジェクトの場合、各キーがラッパー名になります。
ラッパー名には、英字、数字、`.`、`_`、`-`だけを使用できます。

たとえば、インストールしたパッケージのマニフェストが以下の場合、

```json
{
  "name": "github.com/acme/demo",
  "bin": {
    "demo": "demo.js"
  }
}
```

`node_modules/.bin/demo.js`が生成されます。ラッパーは、インストール済みパッケージのディレクトリに作業ディレクトリを変更してから、`bin`の対象を実行します。

そのため、`bin`の対象は、インストール済みパッケージのルートを基準とする有効なパスである必要があります。
ラッパーの後に指定した追加引数は、そのまま対象に渡されます。

### 生成された`.bin`ラッパーの実行 {#생성된-bin-wrapper-실행}

`pkg run`は、インストール済みパッケージの`.bin`ラッパーを実行しません。
`pkg run`は、現在のプロジェクトの`package.json`にある`scripts`だけを実行します。

シェル環境では、`PATH`に`/work/node_modules/.bin`と`./node_modules/.bin`が含まれています。
そのため、インストール済みパッケージの実行ファイルは、通常は名前だけで実行できます。

パッケージの実行ファイルを使用するには、シェルから生成されたラッパーを実行します。
例を示します。

```sh
/work > demo.js --help
/work > demo.js import sample.csv
```

必要に応じて、ラッパーのパスを直接指定して実行することもできます。

```sh
/work > ./node_modules/.bin/demo.js --help
```

同名のラッパーが存在する場合、インストールは続行し、警告を出力して競合するラッパーだけを生成しません。
パッケージ自体のインストールは成功しますが、その実行名だけを作成しません。

競合ファイルが他のインストール済みパッケージのラッパーの場合、警告に所有元のパッケージ名を含めます。
`pkg`の管理外の既存ファイルの場合は、単に既存のラッパーとして報告します。

### ロックファイルの動作 {#lock-file-동작}

通常のプロジェクトインストールでは、再現可能なインストールのため、`pkg`は解決したソースを`package-lock.json`に記録します。
GitHubパッケージでは、タグに基づくかブランチに基づくかも保存します。

例を示します。

- `github.com/acme/demo#tag=v1.1.0`
- `github.com/acme/notags#branch=main`

ロックファイルがある場合、`pkg install`はrefを再解決せず、記録済みのGitHub refを再利用します。

### エラー報告 {#에러-보고}

GitHub refを決定できない場合、`pkg`は2段階の失敗原因をまとめて表示します。
たとえば、タグの検索失敗と既定ブランチの検索失敗を、1つのメッセージで報告します。

## pkg copy {#pkg-copy}

GitHubリポジトリのパッケージを、`node_modules`ではなく、指定した対象ディレクトリに直接コピーします。
プロジェクトファイルをコピーした後、コピー先のプロジェクトルートと、存在する場合は`cgi-bin`に依存関係をインストールします。

<h6>構文</h6>

```sh
pkg copy [options] <source> <dest>
```

<h6>オプション</h6>

- `-f, --force` 対象ディレクトリが存在し、空でなくても続行します。
- `-h, --help` ヘルプを表示します。

`source`には、`pkg install`と同じGitHubリポジトリの構文を使用する必要があります。
対応する形式は以下のとおりです。

- `github.com/<org>/<repo>`
- `github.com/<org>/<repo>@<tag>`
- `github.com/<org>/<repo>#tag=<tag>`
- `github.com/<org>/<repo>#branch=<branch>`

`dest`は、現在の作業ディレクトリを基準に解釈するファイルシステムパスです。
対象ディレクトリがなければ、`pkg copy`が作成します。
対象ディレクトリが存在し、空でない場合は、`--force`がなければ失敗します。

### コピーの動作 {#복사-동작}

`pkg copy`は、`pkg install`と同じGitHub refの解決規則を使用します。
明示的なタグやブランチがあればそれを使用し、なければ最新タグを解決します。タグがない場合は、リポジトリの`default_branch`を使用します。

リポジトリの内容は、`<dest>`に直接コピーされます。
`pkg install`と異なり、GitHubプロジェクトを`node_modules/github.com/...`には配置しません。
元のディレクトリ構造は、対象ディレクトリ配下で保持されます。

コピー後、`pkg copy`は以下のプロジェクトルートを確認し、`pkg install`と同じインストール処理とロックファイルの動作で依存関係をインストールします。

- `<dest>/package.json`がある場合は`<dest>`
- `<dest>/cgi-bin/package.json`がある場合は`<dest>/cgi-bin`

そのため、コピーした各プロジェクトルートは、独自の`node_modules`と`package-lock.json`を個別に保持します。

<h6>使用例</h6>

```sh
/work > pkg copy github.com/acme/helloapp public/hello
Copying github.com/acme/helloapp#branch=main to /work/public/hello
Installing dependencies in /work/public/hello
Installing dependencies in /work/public/hello/cgi-bin
```

このコマンドを実行すると、以下のようになります。

- リポジトリのファイルが`/work/public/hello`にコピーされます。
- `/work/public/hello/package.json`の依存関係が、`/work/public/hello/node_modules`にインストールされます。
- `/work/public/hello/cgi-bin/package.json`がある場合、その依存関係が`/work/public/hello/cgi-bin/node_modules`にインストールされます。

指定パスにプロジェクトツリーをそのまま配置し、GitHub refの解決とコピー先の依存関係のインストールを`pkg`に任せる場合は、`pkg copy`を使用します。

## pkg run {#pkg-run}

`package.json`の`scripts`を実行します。

<h6>構文</h6>

```sh
pkg run [options] <key> [...args]
```

<h6>オプション</h6>

- `-C, --dir <dir>` 現在の作業ディレクトリではなく、指定したプロジェクトディレクトリを使用します。
- `-h, --help` ヘルプを表示します。

`pkg run`は、スクリプトの実行前に、現在の作業ディレクトリを選択したプロジェクトディレクトリに変更します。
そのため、`./main.js`などの相対パスのコマンドは、パッケージディレクトリを基準に解釈します。

<h6>使用例</h6>

以下のマニフェストがある場合、

```json
{
  "scripts": {
    "start": "./main.js --mode prod"
  }
}
```

次のように実行できます。

```sh
/work > pkg run start
```

追加引数は、スクリプトのコマンドラインの末尾に追加されます。

```sh
/work > pkg run start --verbose
```

実際に実行するコマンドラインは以下のとおりです。

```sh
./main.js --mode prod --verbose
```

## pkg uninstall {#pkg-uninstall}

依存関係と、その生成済みラッパーを削除します。

<h6>構文</h6>

```sh
pkg uninstall [options] <name>
```

<h6>オプション</h6>

- `-C, --dir <dir>` 現在の作業ディレクトリではなく、指定したプロジェクトディレクトリを使用します。
- `-g, --global` `--dir`を無視して、`/work/node_modules`からパッケージを削除します。
- `-h, --help` ヘルプを表示します。

`pkg uninstall`は、`pkg`が管理する以下の項目を削除します。

- `package.json`の依存関係の項目
- インストール済みパッケージに属する`node_modules/.bin`ラッパー
- インストール済みパッケージのディレクトリ
- 依存関係が残らない場合の`package-lock.json`

`pkg install -g`でインストールしたパッケージを削除するには、`pkg uninstall -g`を使用します。

```sh
/work > pkg uninstall -g github.com/acme/demo
Removed github.com/acme/demo
```

インストール時にエイリアスの競合でラッパー生成をスキップした場合は、削除するラッパーがないことがあります。
また、`pkg uninstall`は、`pkg`の管理外のユーザー作成の`node_modules/.bin`ファイルを削除しません。

<h6>使用例</h6>

```sh
/work > pkg uninstall github.com/acme/demo
Removed github.com/acme/demo
```

## 一般的な作業手順 {#일반적인-작업-순서}

```sh
/work > pkg init demo-app
/work > pkg install github.com/acme/demo
/work > pkg install generic-pkg
/work > pkg run start
```

## 注意 {#참고}

- パッケージ名なしの`install`、または`run`の実行には、有効な`package.json`が必要です。
- `pkg run`は、POSIXシェルではなくJSHのコマンド解決でスクリプト行を実行します。
- プロジェクト内の実行ファイルは、`./tool.js`などの相対パスで定義することを推奨します。
- パッケージ開発者は、生成したラッパーがインストール先のパッケージディレクトリで実行されることを前提に、`./bin/demo.js`などの相対`bin`パスを使用してください。
- 実行名を明示的に指定する場合はオブジェクト形式の`bin`を、パッケージ名を実行名にする場合は文字列形式の`bin`を使用します。
- GitHubリポジトリからインストールするには、ダウンロードした内容に有効な`package.json`が必要です。
