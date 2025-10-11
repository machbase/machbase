---
title: JSH - JavaScript
type: docs
weight: 75
---

{{< neo_since ver="8.0.52" />}}

{{< callout type="warning" >}}
**베타 안내**<br/>
JSH는 현재 베타 단계입니다. 향후 릴리스에서 API와 명령어가 변경될 수 있습니다.
{{< /callout >}}


JSH를 이용하시면 Machbase Neo 프로세스 안에서 바로 실행되는 JavaScript 애플리케이션을 작성하실 수 있습니다.
확장자가 `.js`인 파일은 Machbase Neo에서 실행 가능한 스크립트로 인식됩니다.

## Hello World 예제

아래 코드를 복사하여 `hello.js`로 저장하십시오.

```js
p = require("@jsh/process");
p.print("Hello", "World?", "\n")
```

"New..." 페이지에서 "JSH"를 선택해 주십시오.

{{< figure src="./img/fish.jpg" width="86">}}

`.js` 파일을 실행하기 위한 단순한 명령줄 인터프리터로 동작합니다.

저장한 스크립트를 실행하려면 다음 명령을 입력해 주십시오.

```
jsh / > ./hello.js
Hello World? 
```

{{< figure src="./img/fish-hello.jpg" width="486">}}


## 명령어

- `exit` 현재 JSH 세션을 종료합니다.
- `ls` 현재 작업 디렉터리의 파일 목록을 표시합니다.
- `cd` 작업 디렉터리를 변경합니다.
- `ps` 실행 중인 프로세스와 PID를 보여 드립니다.
- `kill <pid>` 지정한 PID의 프로세스를 종료합니다.
- `servicectl` 서비스 제어 명령입니다. 자세한 내용은 [아래](#service-control-commands)를 참고하십시오.

기능은 단순하지만 스크립트를 검증하시기에는 충분합니다.

## 데몬

백그라운드에서 실행되는 애플리케이션이 필요하다면 데몬 프로세스로 구현하시기 바랍니다.

```js {linenos=table,hl_lines=[8,"18-22"],linenostart=1}
const p = require("@jsh/process")
const s = require("@jsh/system")
const log = new s.Log("example-daemon");

if( p.isDaemon()) {
    doService()
} else {
    p.daemonize()
    log.info("svc daemonized")
}
function doService() {
    log.info("svc start - "+p.pid())
    p.addCleanup(()=>{
        // 프로세스가 종료될 때 실행되는 정리 코드입니다.
        log.info("svc stop - "+p.pid())
    })
    sum = 0
    for( i = 0; i < 60; i++) {
        p.sleep(1000)
        sum += i
        log.info("svc pid =", p.pid(), "i =", i)
    }
    log.info("svc sum =", sum)
}
```

- 8행: `daemonize()`는 현재 애플리케이션을 백그라운드 프로세스로 전환합니다.
- 18~22행: 1초 간격으로 1분 동안 반복 실행합니다.

코드를 저장한 뒤 실행하시면 기본 로그 라이터인 stdout에 메시지가 출력됩니다.

```
2025/04/28 15:44:25.295 INFO  example-daemon   svc start - 1035
2025/04/28 15:44:26.296 INFO  example-daemon   svc pid = 1035 i = 0
2025/04/28 15:44:27.296 INFO  example-daemon   svc pid = 1035 i = 1
2025/04/28 15:44:28.298 INFO  example-daemon   svc pid = 1035 i = 2
                ... 생략 ...
2025/04/28 15:45:24.358 INFO  example-daemon   svc pid = 1035 i = 58
2025/04/28 15:45:25.360 INFO  example-daemon   svc pid = 1035 i = 59
2025/04/28 15:45:25.360 INFO  example-daemon   svc sum = 1770
2025/04/28 15:45:25.360 INFO  example-daemon   svc stop - 1035
```

## 서비스

machbase-neo가 시작될 때 백그라운드 프로세스를 자동으로 실행하려면 애플리케이션 기동 방법을 정의한 JSON 파일을 준비하십시오.

`/etc/services` 디렉터리를 만든 뒤 해당 디렉터리에 JSON 파일을 작성합니다.

- `/etc/services/svc.json`

```json
{
    "enable": true,
    "start_cmd": "/sbin/svc.js",
    "start_args": []
}
```

machbase-neo는 시작 시 `/etc/services` 디렉터리에서 JSON 파일을 검색합니다.
각 JSON 파일은 지정한 애플리케이션을 실행하기 위한 서비스 지시문으로 처리됩니다.


### 서비스 제어 명령

**`servicectl status`** 서비스 상태를 표시합니다.

**`servicectl start <service>`** 지정한 서비스를 시작합니다.

**`servicectl stop <service>`** 지정한 서비스를 중지합니다.

**`servicectl reread`** `/etc/services/*.json` 구성을 다시 읽고 변경 사항을 알려 드립니다.

**`servicectl update`** 구성을 다시 읽고 변경 내용을 적용합니다.

## 모듈
JSH는 TQL의 `SCRIPT()`와 `*.js` 애플리케이션에서 사용할 수 있는 다양한 JavaScript 모듈을 제공합니다.
단, `@jsh/process` 모듈은 `*.js` 애플리케이션에서만 사용할 수 있으며 TQL에서는 사용할 수 없습니다.
반대로 `$.yield()`와 같은 편리한 메서드를 제공하는 TQL 컨텍스트 객체 `$`는 TQL 전용으로, `*.js` 애플리케이션에서는 접근하실 수 없습니다.

자세한 내용은 각 모듈 문서를 참고해 주십시오.

{{< children_toc />}}
