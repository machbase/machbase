---
title: JSH
type: docs
weight: 75
tags: JavaScript
---

{{< neo_since ver="8.0.75" />}}

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

전체 명령어는 [명령어 레퍼런스](./commands/) 문서를 참고해 주십시오.

## 파이프와 리다이렉션

JSH는 외부 명령에 대해 셸 스타일의 파이프와 리다이렉션 연산자를 지원합니다.

- `cmd1 | cmd2`는 `cmd1`의 표준 출력을 `cmd2`의 표준 입력으로 전달합니다.
- `< file`은 파일을 표준 입력으로 리다이렉션합니다.
- `> file`은 표준 출력을 파일로 기록하며 기존 내용을 덮어씁니다.
- `>> file`은 표준 출력을 파일 끝에 이어서 기록합니다.
- `2> file`은 표준 에러를 파일로 기록하며 기존 내용을 덮어씁니다.
- `2>> file`은 표준 에러를 파일 끝에 이어서 기록합니다.
- `2>&1`은 표준 에러를 표준 출력으로 합칩니다.

예시:

```sh
 cat sample.txt | wc -l
 sort < input.txt > output.txt
 write-stderr boom 1 2> error.log
 write-stderr boom 0 2>&1 | wc -l
```

참고:

- 파이프와 리다이렉션 연산자는 따옴표 바깥에서만 해석됩니다. 예를 들어 `echo "a | b"`의 `|`는 일반 문자로 처리됩니다.
- 파이프라인에서는 입력 리다이렉션은 첫 번째 단계에서만, 출력 리다이렉션은 마지막 단계에서만 지원됩니다.
- `cd`, `ls`, `exit`와 같은 내부 명령은 리다이렉션을 지원하지 않으며 파이프라인에서도 사용할 수 없습니다.

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

## 모듈
JSH는 TQL의 `SCRIPT()`와 `*.js` 애플리케이션에서 사용할 수 있는 다양한 JavaScript 모듈을 제공합니다.
단, TQL의 `$.yield()`와 같은 편리한 메서드를 제공하는 TQL 컨텍스트 객체 `$`는 TQL 전용으로, `*.js` 애플리케이션에서는 접근하실 수 없습니다.

자세한 내용은 각 모듈 문서를 참고해 주십시오.

{{< children_toc />}}
