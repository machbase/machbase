---
toc: true
title: カスタムシェル
type: docs
weight: 10
---

コマンドラインシェルを登録し、Web UIで実行できます。

Web UIで*SHELL*を開くか、ターミナルで`machbase-neo shell`を実行し、`shell`コマンドでカスタムシェルを追加・削除できます。

以下の例では、*nix環境で`/bin/bash`（または`/bin/zsh`）、Windows環境で`cmd.exe`を実行するカスタムシェルの追加方法を示します。他の言語のREPL、他のデータベースのCLI、サーバーに接続するSSHコマンドなど、任意のツールも登録できます。

## カスタムシェルの追加 {#사용자-정의-셸-추가}

### シェルの登録 {#셸-등록}

1. 左側のメニューで<img src="/neo/shell/img/shell_icon.jpg" width=47 style="display:inline">アイコンを選択します。

2. 左上のパネルで`+`アイコン<img src="/neo/shell/img/shell_add_icon.jpg" width=265 style="display:inline">をクリックします。

3. 「Display name」を入力し、「Command」フィールドに実行ファイルの絶対パスと引数を指定します。
   たとえば、macOSでzshを登録するには、絶対パスを入力して「Save」をクリックします。

{{< figure src="/neo/shell/img/shell_add_form.jpg" width="684px">}}

- Name: 表示名（予約語以外の任意のテキストを使用可能）
- Command: 絶対パスと引数を含む実行コマンド
- Theme : ターミナルの配色テーマ

たとえば、次のコマンドを登録できます。
- Windows Cmd.exe: `C:\Windows\System32\cmd.exe`
- Linux bash: `/bin/bash`
- PostgreSQL クライアント(macOS): `/opt/homebrew/bin/psql postgres`

### 登録したシェルの使用 {#등록한-셸-사용}

- メインエディター領域でカスタムシェルを開きます。

{{< figure src="/images/web-custom-shell.jpeg" width="600px">}}

- コンソール領域でカスタムシェルを開きます。

{{< figure src="/neo/shell/img/web-custom-shell-console.jpg" width="700px">}}

## コマンドラインでの操作 {#명령줄에서-제어}

カスタムシェルは、machbase-neoシェルのCLIでも管理できます。

### 新しいシェルの追加 {#새-셸-추가}

`shell add <name> <command and args>`コマンドを使用します。任意の名前と実行コマンドを指定できますが、既定のシェル名`SHELL`は予約されています。

```sh
machbase-neo» shell add bashterm /bin/bash;
added
```

```sh
machbase-neo» shell add terminal /bin/zsh -il;
added
```

```sh
machbase-neo» shell add console C:\Windows\System32\cmd.exe;
added
```

### 登録済みシェルの一覧確認 {#등록된-셸-목록-확인}

```sh
machbase-neo» shell list;
┌────────┬────────────────────────────┬────────────┬──────────────┐
│ ROWNUM │ ID                         │ NAME       │ COMMAND      │
├────────┼────────────────────────────┼────────────┼──────────────┤
│      1 │ 11F4AFFD-2A9B-4FC5-BB20-637│ BASHTERM   │ /bin/bash    │
│      2 │ 11F4AFFD-2A9B-4FC5-BB20-638│ TERMINAL   │ /bin/zsh -il │
└────────┴────────────────────────────┴────────────┴──────────────┘
```


### カスタムシェルの削除 {#사용자-정의-셸-삭제}

```sh
machbase-neo» shell del 11F4AFFD-2A9B-4FC5-BB20-637;
deleted
```

