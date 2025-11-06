---
title: 웹 UI
type: docs
weight: 15
---

## 로그인

웹 브라우저를 열고 [http://127.0.0.1:5654/](http://127.0.0.1:5654/)로 이동해 주십시오. 기본 계정인 **ID** `sys`, **비밀번호** `manager`로 로그인할 수 있습니다.

> machbase-neo가 원격 머신에서 실행 중이라면 [시작과 종료](../start-stop) 문서를 참고하여 원격 접속을 허용해 주십시오.

{{< figure src="/images/web-login.png" width="600" >}}

## 비밀번호 변경

보안을 위해 원격 접속을 활성화하기 전에 기본 비밀번호를 변경하시기를 권장드립니다.

1. 왼쪽 아래 메뉴에서 "Change password"를 선택해 주십시오. {{< neo_since ver="8.0.20" />}}

{{< figure src="/neo/getting-started/img/change_passwd_ui.jpg" width="203px" >}}

2. 대화 상자에서 새 비밀번호를 입력한 뒤 한 번 더 입력하여 확인해 주십시오.

{{< figure src="/neo/getting-started/img/change_passwd_ui2.jpg" width="342px" >}}

### SQL

{{< figure src="/neo/getting-started/img/change_passwd.jpg" width="800px" >}}

```sql
ALTER USER sys IDENTIFIED BY new_password;
```

### 명령줄

```sh
machbase-neo shell "ALTER USER SYS IDENTIFIED BY new_password"
```

{{< callout type="info" emoji="❗️">}}
**Escape from OS shell**<br/>
명령줄에서 비대화형 모드로 SQL 구문을 실행할 때는 운영체제 셸의 특수 문자를 반드시 이스케이프해야 합니다.
예를 들어 `machbase-neo shell select * from table`과 같이 따옴표 없이 실행하면
`*`가 bash(또는 zsh)에서 "모든 파일"을 의미하도록 해석됩니다.
같은 이유로 `\`, `!`, `$`, 따옴표도 주의해서 사용해야 합니다.
<br/>
또는 neo-shell 대화형 모드를 사용할 수 있습니다.
`machbase-neo shell`을 실행하면 `machbase-neo >>` 프롬프트가 표시되며,
이 대화형 모드에서는 추가로 셸 이스케이프를 할 필요가 없습니다.
{{< /callout >}}
