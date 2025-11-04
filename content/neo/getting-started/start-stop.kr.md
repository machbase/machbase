---
title: 시작과 종료
type: docs
weight: 12
---

## Linux & macOS

Linux와 macOS에서는 `serve` 명령으로 machbase-neo를 실행합니다.

```sh
machbase-neo serve
```

{{< figure src="../img/server-serve.gif" width="600" >}}

### 포트 개방

machbase-neo는 기본적으로 보안을 위해 로컬호스트에서만 실행되고 대기합니다. 원격에서 실행되는 클라이언트가 네트워크를 통해 접속하려면 `--host <bind address>` 옵션을 사용해 리슨 주소를 지정해야 합니다.

모든 주소에서의 접속을 허용하려면 `0.0.0.0`을 지정해 주십시오.

```sh
machbase-neo serve --host 0.0.0.0
```

특정 주소만 허용하려면 호스트의 IP 주소를 지정하면 됩니다.

```sh
machbase-neo serve --host 192.168.1.10
```

### 종료

서버를 포그라운드 모드로 실행 중이라면 `Ctrl+C`를 눌러 종료하실 수 있습니다.

또는 `shutdown` 명령을 사용할 수 있습니다. 이 명령은 동일한 호스트에서 실행할 때만 동작합니다.

```sh
machbase-neo shell shutdown
```

## Linux Service

[Operations/Linux service](../../operations/service-linux/) 문서를 참고하시면 machbase-neo를 백그라운드 프로세스로 등록하는 방법을 확인하실 수 있습니다.

## Windows

Windows에서는 `neow.exe`를 두 번 클릭한 다음 창 왼쪽 상단의 "machbase-neo serve" 버튼을 눌러 실행해 주십시오.

{{< figure src="/images/neow-win.png" width="600" >}}

### Windows Service

machbase-neo는 Windows 서비스로 등록할 수 있습니다.<br/>
아래 명령은 관리자 권한으로 실행해야 합니다.

- 설치

서비스를 등록합니다. `machbase-neo service install` 뒤에 오는 인수는 `machbase-neo serve`와 동일하며, 모든 경로는 *절대 경로*여야 합니다.

```
C:\neo-server>.\machbase-neo service install --host 127.0.0.1 --data C:\neo-server\database --file C:\neo-server\files --log-filename C:\neo-server\machbase-neo.log --log-level INFO

```

- 시작 및 중지

Windows에서 제공하는 서비스 관리 기능을 사용해 시작하거나 중지할 수 있으며,
아래 명령을 직접 실행해도 됩니다.

```
C:\neo-server>.\machbase-neo service start
success to start machbase-neo service.

C:\neo-server>.\machbase-neo service stop
success to stop machbase-neo service.
```

- 삭제

Windows 서비스에서 machbase-neo를 제거합니다.

```
C:\neo-server>.\machbase-neo service remove
success to remove machbase-neo service.
```
