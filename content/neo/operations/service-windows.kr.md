---
title: Windows 서비스
type: docs
weight: 81
---

`machbase-neo service` 명령은 Windows 서비스 등록을 제어합니다.
서비스 설치가 완료되면 Windows 부팅과 함께 machbase-neo가 자동으로 시작됩니다.

{{< callout emoji="📌">}}
이 작업은 **관리자 권한**이 필요합니다.
{{< /callout >}}


## machbase-neo service install

machbase-neo를 Windows 서비스에 등록합니다.

```cmd
machbase-neo.exe service install --host 0.0.0.0 --data D:\database --file D:\database\files --log-filename D:\database\machbase-neo.log
```

## machbase-neo service remove

Windows 서비스에서 machbase-neo를 제거합니다.

```cmd
machbase-neo.exe service remove
```

## start and stop

서비스를 시작하거나 중지합니다. Windows 서비스 제어판에서 제공하는 동작과 동일합니다.

```cmd
machbase-neo.exe service start
```

```cmd
machbase-neo.exe service stop
```
