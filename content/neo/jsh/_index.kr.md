---
title: JSH
type: docs
weight: 75
tags: JavaScript
---

{{< neo_since ver="8.0.52" />}}

{{< callout type="warning" >}}
**베타 안내**<br/>
JSH는 현재 베타 단계입니다. 향후 릴리스에서 API와 명령어가 변경될 수 있습니다.
{{< /callout >}}


JSH를 이용하시면 Machbase Neo를 이용하는 JavaScript 애플리케이션을 작성하실 수 있습니다.
확장자가 `.js`인 파일 또는 `index.js`를 포함하고 있는 디렉터리는 Machbase Neo에서 실행 가능한 애플리케이션으로 인식됩니다.

## 명령어

- `exit` 현재 JSH 세션을 종료합니다.
- `ls` 현재 작업 디렉터리의 파일 목록을 표시합니다.
- `cd` 작업 디렉터리를 변경하거나 `/work` 디렉터리로 이동합니다.
<!-- - `ps` 실행 중인 프로세스와 PID를 보여 드립니다.
- `kill <pid>` 지정한 PID의 프로세스를 종료합니다.
- `servicectl` 서비스 제어 명령입니다. 자세한 내용은 [아래](#service-control-commands)를 참고하십시오. -->

기능은 단순하지만 스크립트를 검증하시기에는 충분합니다.

## Hello World 예제

아래 코드를 복사하여 `hello.js`로 저장하십시오.

```js
console.print("Hello World?\n")
```

"New..." 페이지에서 "JSH"를 선택해 주십시오.

{{< figure src="./img/fish.jpg" width="86">}}

`.js` 파일을 실행하기 위한 단순한 명령줄 인터프리터로 동작합니다.

저장한 스크립트를 실행하려면 다음 명령을 입력해 주십시오.

```
/work > ./hello.js
Hello World? 
```

{{< figure src="./img/fish-hello.jpg" width="486">}}

## 디렉터리 마운트

JSH 런타임 환경은 호스트 OS의 파일 시스템과 분리된 가상의 파일시스템으로 동작합니다.
JSH를 실행해서 내부에서 `ls -l /`을 해보면 아래와 같이 JSH가 동작하는 OS와 완전히 다른 디렉터리 트리 구조를 가진 것을 확인할 수 있다.

{{< figure src="./img/fish-ls.jpg" width="513">}}

이 기본 디렉터리들 중에 `/sbin`, `/lib` 는 JSH에 기본으로 내장된 읽기만 가능한 파일들이 존재하며 
`/work`는 JSH를 실행할 때 별도로 지정하지 않은 경우 OS의 현재 디렉터리 또는 웹 환경에서 파일 익스플로러에서 보이는 디렉터리가 자동으로 마운트 됩니다.

사용자가 임의의 디렉터리를 마운트하려면 `-v mount_point=os_dir`옵션을 사용합니다.
예를 들어 OS의 `/var/tmp`를 JSH의 `/tmp`로 마운트하려면 아래와 같이 실행합니다.

```sh
$ machbase-neo jsh -v /tmp=/var/tmp
```

{{< figure src="./img/fish-ls-mount.jpg" width="513">}}

## 외부 실행

작성한 js 애플리케이션은 machbase-neo 서버 프로세스와 독립적인 환경에서 machbase-neo 실행파일만 있으면 아래와 같이 실행 가능합니다.
`machbase-neo jsh`를 실행하면 JSH 인터프리터가 주어진 스크립트를 실행하게 됩니다.
이 방식으로 활용하면 machbase-neo 실행 파일만으로 추가적인 도구 없이 데이터베이스를 입력/조회하는 애플리케이션을 작성할 수 있습니다.

짧은 JavaScript 코드를 별도의 스크립트 파일로 만들지 않고 명령줄에서 바로 실행하려면
`-C <code>` 옵션을 사용하십시오.

```sh
$ /path/to/the/machbase-neo jsh -C 'console.println("Hello World?")'
Hello World?
```

로컬 디렉터리 마운트 없이 저장된 스크립트를 실행하려면 `-C @script_path` 옵션으로 스크립트의 경로를 지정합니다.

```sh
# hello.js 파일이 ./src/hello.js 에 있다면
$ /path/to/the/machbase-neo jsh -C @./src/hello.js
Hello World?
```

로컬 디렉터리에 저장된 스크립트를 실행하려면 `-v <mount_point>=<src_dir>` 옵션을 사용하십시오.
이 옵션은 호스트 디렉터리를 JSH 런타임에 마운트하므로, 마운트된 경로를 통해 스크립트를 실행할 수 있습니다.
특히 스크립트가 같은 디렉터리에 있는 다른 파일에 의존하는 경우에 유용합니다.

```sh
# hello.js 파일이 ./src/hello.js 에 있다면, src 디렉터리를 /script 로 마운트합니다.
$ /path/to/the/machbase-neo jsh -v /script=./src /script/hello.js
Hello World?
```


## 데이터베이스 예제

마크베이스의 데이터를 조회하거나 입력하는 애플리케이션을 간단하게 작성할 수 있습니다.

```js
'use strict';
// Load machbase client module.
const machcli = require('machcli');
// Create database client instance.
const db = new machcli.Client({
    host: '127.0.0.1',
    port: 5656, // machbase native port
    username:'sys',
    password: 'manager'
})

var conn, rows;
try {
    // Create a database connection.
    conn = db.connect();
    // Execute query.
    rows = conn.query('SELECT NAME, TYPE, COLCOUNT FROM m$sys_tables LIMIT 5');
    // Iterates result set.
    for (const row of rows) {
        console.println(row.NAME, row.TYPE, row.COLCOUNT);
    }
} finally {
    // Release resources
    rows && rows.close();
    conn && conn.close();
}
```

<!-- ## 데몬

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

**`servicectl update`** 구성을 다시 읽고 변경 내용을 적용합니다. -->

## 모듈
JSH는 TQL의 `SCRIPT()`와 `*.js` 애플리케이션에서 사용할 수 있는 다양한 JavaScript 모듈을 제공합니다.
단, TQL의 `$.yield()`와 같은 편리한 메서드를 제공하는 TQL 컨텍스트 객체 `$`는 TQL 전용으로, `*.js` 애플리케이션에서는 접근하실 수 없습니다.

자세한 내용은 각 모듈 문서를 참고해 주십시오.

{{< children_toc />}}
