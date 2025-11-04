---
title: 사용자 정의 셸
type: docs
weight: 10
---

사용자는 명령줄 셸을 직접 등록해 웹 UI에서 실행할 수 있습니다.

웹 UI에서 *SHELL*을 열거나 터미널에서 `machbase-neo shell`을 실행한 뒤 `shell` 명령으로 사용자 정의 셸을 추가·삭제할 수 있습니다.

아래 예시에서는 *nix 환경에서 `/bin/bash`(또는 `/bin/zsh`), Windows 환경에서 `cmd.exe`를 실행하는 사용자 정의 셸을 추가하는 방법을 보여 줍니다. 이 외에도 다른 언어의 REPL, 타 데이터베이스의 CLI, 서버에 접속하는 SSH 명령 등 원하는 도구를 등록할 수 있습니다.

## 사용자 정의 셸 추가

### 셸 등록

1. 왼쪽 메뉴에서 <img src="../img/shell_icon.jpg" width=47 style="display:inline"> 아이콘을 선택합니다.

2. 상단 왼쪽 패널에서 `+` 아이콘 <img src="../img/shell_add_icon.jpg" width=265 style="display:inline"> 을 클릭합니다.

3. "Display name"을 입력하고 "Command" 필드에 실행 파일의 절대 경로와 인자를 지정합니다.
   예를 들어 macOS에서 zsh를 등록하려면 절대 경로를 입력한 뒤 "Save"를 클릭합니다.

{{< figure src="../img/shell_add_form.jpg" width="684px">}}

- Name: 표시 이름(예약어를 제외한 임의의 텍스트 사용 가능)
- Command: 전체 경로와 인자를 포함한 실행 명령
- Theme : 터미널 색상 테마

예를 들어 다음과 같은 명령을 등록할 수 있습니다.
- Windows Cmd.exe: `C:\Windows\System32\cmd.exe`
- Linux bash: `/bin/bash`
- PostgreSQL 클라이언트(macOS): `/opt/homebrew/bin/psql postgres`

### 등록한 셸 사용

- 메인 에디터 영역에서 사용자 정의 셸을 엽니다.

{{< figure src="/images/web-custom-shell.jpeg" width="600px">}}

- 콘솔 영역에서 사용자 정의 셸을 엽니다.

{{< figure src="../img/web-custom-shell-console.jpg" width="700px">}}

## 명령줄에서 제어

사용자 정의 셸은 machbase-neo 셸 CLI로도 관리할 수 있습니다.

### 새 셸 추가

`shell add <name> <command and args>` 명령을 사용합니다. 원하는 이름과 실행 명령을 지정할 수 있지만 기본 셸 이름 `SHELL`은 예약되어 있습니다.

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

### 등록된 셸 목록 확인

```sh
machbase-neo» shell list;
┌────────┬────────────────────────────┬────────────┬──────────────┐
│ ROWNUM │ ID                         │ NAME       │ COMMAND      │
├────────┼────────────────────────────┼────────────┼──────────────┤
│      1 │ 11F4AFFD-2A9B-4FC5-BB20-637│ BASHTERM   │ /bin/bash    │
│      2 │ 11F4AFFD-2A9B-4FC5-BB20-638│ TERMINAL   │ /bin/zsh -il │
└────────┴────────────────────────────┴────────────┴──────────────┘
```


### 사용자 정의 셸 삭제

```sh
machbase-neo» shell del 11F4AFFD-2A9B-4FC5-BB20-637;
deleted
```

