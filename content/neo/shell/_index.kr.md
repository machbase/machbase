---
title: 셸
type: docs
weight: 21
---

## 웹을 통한 원격 접속

1. 새 탭 화면에서 <img src="/neo/shell/img/shell_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> `SHELL`을 선택합니다.

{{< figure src="/images/web-shell-pick.png" width="600px" >}}

2. 메인 영역에 셸이 열립니다. `sys machbase-neo` 프롬프트에서 SQL 문과 machbase-neo 셸 명령을 실행할 수 있습니다.

{{< figure src="/images/web-shell-ui.png" width="700px" >}}

<a id="remote-access-via-ssh"></a>
## SSH를 통한 원격 접속

SSH(Secure Shell)는 원격 시스템에 안전하게 접속하기 위한 프로토콜입니다.
비밀번호 인증뿐 아니라 더 안전한 공개키 인증도 지원합니다.

machbase-neo는 원격 운영과 관리를 위해 SSH 인터페이스를 제공합니다.
아래와 같이 SSH 명령을 사용해 SQL 인터프리터에 접속할 수 있습니다.

- 사용자: SYS
- 기본 비밀번호: manager
- 기본 포트: 5652

```sh
$ ssh -p 5652 sys@127.0.0.1
sys@127.0.0.1's password: manager↵
```

`machbase-neo»` 프롬프트가 표시되면 SQL 문을 실행할 수 있습니다.

```
machbase-neo» select * from example;
┌─────────┬──────────┬─────────────────────────┬───────────┐
│ ROWNUM  │ NAME     │ TIME(UTC)               │ VALUE     │
├─────────┼──────────┼─────────────────────────┼───────────┤
│       1 │ wave.sin │ 2023-01-31 03:58:02.751 │ 0.913716  │
│       2 │ wave.cos │ 2023-01-31 03:58:02.751 │ 0.406354  │
                        ...omit...
│      13 │ wave.sin │ 2023-01-31 03:58:05.751 │ 0.668819  │
│      14 │ wave.cos │ 2023-01-31 03:58:05.751 │ -0.743425 │
└─────────┴──────────┴─────────────────────────┴───────────┘
```

### 비밀번호 없이 SSH 접속하기

1. **키 쌍 생성**: 접속할 로컬 머신에서 새 키 쌍을 생성합니다. `ssh-keygen` 명령을 사용합니다.

    > 이미 키 쌍이 있다면 이 단계를 건너뛸 수 있습니다.

    ```bash
    ssh-keygen -t rsa
    ```

    이 명령은 홈 디렉터리의 `.ssh` 폴더에 `id_rsa`(개인키)와 `id_rsa.pub`(공개키) 파일을 만듭니다.

2. **공개키 복사**: 생성한 공개키를 원격 서버로 복사합니다.

    machbase 서버에 공개키를 등록하려면 아래 절차를 수행합니다.

3. **키 쌍으로 로그인**: 이제 키 쌍을 이용해 machbase 서버에 로그인할 수 있습니다.
SSH 클라이언트는 개인키로 서버가 보낸 챌린지를 복호화해 사용자를 인증합니다.

    ```bash
    ssh -p 5652 sys@127.0.0.1
    ```

    모든 설정을 마치면 비밀번호 입력 없이 machbase-neo에 접속할 수 있습니다.

#### 웹 UI에서 SSH 키 등록

1. 왼쪽 메뉴 맨 아래 <img src="/neo/shell/img/settings_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘을 클릭하고 `SSH Keys`를 선택합니다. {{< neo_since ver="8.0.20" />}}

{{< figure src="/neo/shell/img/ssh_keys.jpg" width="200px" >}}

2. `New SSH key`를 클릭한 뒤 `Title`에 키를 구분할 이름을, `Public Key`에 공개키 전문을 붙여 넣고 `Add SSH key`를 클릭합니다.

{{< figure src="/neo/shell/img/ssh_keys2.jpg" width="590px" >}}

3. 등록한 키가 `Authentication Keys` 목록에 표시됩니다. 더 이상 쓰지 않는 키는 `Delete`로 지웁니다.

{{< figure src="/neo/shell/img/ssh_keys3.jpg" width="600px" >}}

#### 셸 명령으로 SSH 키 등록

machbase-neo 서버에 공개키를 등록하면 `machbase-neo shell` 명령을 비밀번호 없이 실행할 수 있습니다.

1. 공개키를 서버에 등록합니다.

```sh
machbase-neo shell ssh-key add `cat ~/.ssh/id_rsa.pub`
```

2. 등록된 공개키 목록을 확인합니다.

```sh
machbase-neo shell ssh-key list
```

or

```
$ machbase-neo shell ↵

machbase-neo» ssh-key list
┌────────┬───────────────────────────────────────────┬─────────────────────┬────────────────────────────────────────────────────┐
│ ROWNUM │ NAME                                      │ KEY TYPE            │ FINGERPRINT                                        │
├────────┼───────────────────────────────────────────┼─────────────────────┼────────────────────────────────────────────────────┤
│      1 │ **DO NOT DELETE** machbase-neo server key │ ecdsa-sha2-nistp521 │ SHA256:osfeJKNiUV+a2bIdZPA92maMDI23xA/40gAFwqAfpyQ │
│      2 │ myid@laptop.local                         │ ecdsa-sha2-nistp256 │ SHA256:0IFv6KPDuNJe2s9PoqUBimreYAYih3sDKcxpCYpZCmE │
└────────┴───────────────────────────────────────────┴─────────────────────┴────────────────────────────────────────────────────┘
```

3. 등록된 공개키를 삭제합니다.

```sh
machbase-neo» ssh-key del <fingerprint>
SSH key deleted successfully.
```

#### 비밀번호 없이 접속 확인

```sh
$ ssh -p 5652 sys@127.0.0.1 ↵

Greetings, SYS
machbase-neo v8.7.1-snapshot (b55f8170 2026-09-10T05:43:13) standard
sys machbase-neo 2026-09-17 17:45:13
> 
```

### SSH로 명령 실행

`ssh`만으로 원격에서 모든 machbase-neo 셸 명령을 실행할 수 있습니다.

```sh
$ ssh -p 5652 sys@127.0.0.1 'select * from example order by time desc limit 5'↵

┌────────┬────────┬─────────────────────────┬───────────┐
│ ROWNUM │ NAME   │ TIME                    │     VALUE │
├────────┼────────┼─────────────────────────┼───────────┤
│      1 │ signal │ 2026-09-17 17:09:26.712 │ -0.033411 │
│      2 │ signal │ 2026-09-17 17:09:26.711 │ -0.185026 │
│      3 │ signal │ 2026-09-17 17:09:26.71  │ -0.344666 │
│      4 │ signal │ 2026-09-17 17:09:26.709 │ -0.508032 │
│      5 │ signal │ 2026-09-17 17:09:26.708 │ -0.670817 │
└────────┴────────┴─────────────────────────┴───────────┘
5 rows selected.
```

### 보안 주의 사항

공개키 인증이 비밀번호 인증보다 안전하더라도 개인키를 안전하게 보관하는 것이 매우 중요합니다.
개인키가 유출되면 해당 공개키가 등록된 모든 시스템에 로그인할 수 있습니다.
