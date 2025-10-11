---
title: "@jsh/process"
type: docs
weight: 3
---

{{< neo_since ver="8.0.52" />}}

`@jsh/process` 모듈은 JSH 애플리케이션 전용으로 설계되었으며, 다른 JSH 모듈과 달리 TQL의 `SCRIPT()`에서는 사용할 수 없습니다.

## pid()

현재 프로세스의 PID를 반환합니다.

<h6>사용 형식</h6>

```js
pid()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

프로세스 ID를 나타내는 숫자.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const m = require("@jsh/process")
console.log("my pid =", m.pid())
```

## ppid()

부모 프로세스의 PID를 반환합니다.

<h6>사용 형식</h6>

```js
ppid()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

부모 프로세스 ID를 나타내는 숫자.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const m = require("@jsh/process")
console.log("parent pid =", m.ppid())
```

## args()

명령행 인자 목록을 반환합니다.

<h6>사용 형식</h6>

```js
args()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

`String[]` 명령행 인자 배열.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process");
args = p.args();
x = parseInt(args[1]);
console.log(`x = ${x}`);
```

## cwd()

현재 작업 디렉터리를 반환합니다.

<h6>사용 형식</h6>

```js
cwd()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

`String` 작업 디렉터리 경로.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process");
console.log("cwd :", p.cwd());
```

## cd()

현재 작업 디렉터리를 변경합니다.

<h6>사용 형식</h6>

```js
cd(path)
```

<h6>매개변수</h6>

`path` 이동할 디렉터리 경로.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process");
p.cd('/dir/path');
console.log("cwd :", p.cwd());
```

## readDir()

지정한 디렉터리의 파일과 하위 디렉터리를 순회합니다.

<h6>사용 형식</h6>

```js
readDir(path, callback)
```

<h6>매개변수</h6>

- `path` `String` 탐색할 디렉터리 경로입니다.
- `callback` `function(DirEntry): undefined|Boolean` 콜백 함수입니다. `false`를 반환하면 순회를 중단합니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const process = require("@jsh/process");
process.readDir(".", entry => {
    console.log(entry.name, entry.isDir ? "[dir]" : "");
});
```

## DirEntry

| 속성               | 타입       | 설명               |
|:-------------------|:-----------|:-------------------|
| name               | String     | 항목 이름          |
| isDir              | Boolean    | 디렉터리 여부      |
| readOnly           | Boolean    | 읽기 전용 여부     |
| type               | String     | 파일 유형          |
| size               | Number     | 크기(바이트)       |
| virtual            | Boolean    | 가상 항목 여부     |

<!-- ## readLine()

...

<h6>사용 형식</h6>

```js
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
``` -->

## print()

인자를 출력합니다. 로그 파일을 지정하지 않으면 stdout으로 기록됩니다.

<h6>사용 형식</h6>

```js
print(...args)
```

<h6>매개변수</h6>

`args` `...any` 출력할 가변 길이 인자입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.print("Hello", "World!", "\n")
```

## println()

인자를 출력하고 마지막에 줄바꿈을 추가합니다. 로그 파일을 지정하지 않으면 stdout으로 기록됩니다.

<h6>사용 형식</h6>

```js
println(...args)
```

<h6>매개변수</h6>

`args` `...any` 출력할 가변 길이 인자입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.println("Hello", "World!")
```

## exec()

다른 JavaScript 애플리케이션을 실행합니다.

<h6>사용 형식</h6>

```js
exec(cmd, ...args)
```

<h6>매개변수</h6>

`cmd` `String` 실행할 `.js` 파일 경로입니다.  
`args` `...String` 대상 스크립트에 전달할 인자입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.exec("/sbin/hello.js")
```

## daemonize()

현재 스크립트를 부모 PID가 `1`인 데몬 프로세스로 전환합니다.

<h6>사용 형식</h6>

```js
daemonize(opts)
```

<h6>매개변수</h6>

- `opts` `Object` 옵션 객체입니다.

| 속성               | 타입       | 설명               |
|:-------------------|:-----------|:-------------------|
| reload             | Boolean    | 소스 변경을 감지해 자동 재시작을 활성화합니다. |

`reload`가 `true`이면 데몬 프로세스가 소스 변경 감시자를 함께 실행합니다.  
메인 소스 파일이 수정되면 현재 데몬을 종료하고 즉시 재시작하여 변경 사항을 반영합니다.  
개발 및 테스트에는 유용하지만 파일 감시에 추가 리소스가 필요하므로 운영 환경에서는 비활성화하는 편이 좋습니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const p = require("@jsh/process")
if( p.ppid() == 1) {
    doBackgroundJob()
} else {
    p.daemonize()
    p.print("daemonize self, then exit")
}

function doBackgroundJob() {
    for(true){
        p.sleep(1000);
    }
}
```

## isDaemon()

부모 PID(`ppid()`)가 `1`이면 `true`를 반환합니다. 즉, `ppid() == 1` 조건과 같습니다.

<h6>사용 형식</h6>

```js
isDaemon()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

`Boolean`

## isOrphan()

부모 PID가 지정되지 않은 경우 `true`를 반환합니다. 즉, `ppid() == 0xFFFFFFFF` 조건과 같습니다.

<h6>사용 형식</h6>

```js
isOrphan()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

`Boolean`


## schedule()

지정한 스케줄에 따라 콜백 함수를 실행합니다. 반환된 토큰에서 `stop()`을 호출하기 전까지 흐름은 유지됩니다.

<h6>사용 형식</h6>

```js
schedule(spec, callback)
```

<h6>매개변수</h6>

- `spec` `String` 스케줄 정의입니다. [타이머 스케줄 규칙](/neo/timer/#timer-schedule-spec)을 참고하십시오.
- `callback` `(time_epoch, token) => {}` 첫 번째 인자 `time_epoch`는 밀리초 단위의 UNIX 에포크입니다.  
  두 번째 인자 `token`은 `stop()`을 호출해 스케줄을 종료할 때 사용합니다.
    

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const {schedule} = require("@jsh/process");

var count = 0;
schedule("@every 2s", (ts, token)=>{
    count++;
    console.log(count, new Date(ts));
    if(count >= 5) token.stop();
})

// 1 2025-05-02 16:45:48
// 2 2025-05-02 16:45:50
// 3 2025-05-02 16:45:52
// 4 2025-05-02 16:45:54
// 5 2025-05-02 16:45:56
```

## sleep()

현재 흐름을 지정한 시간 동안 일시 중지합니다.

<h6>사용 형식</h6>

```js
sleep(duration)
```

<h6>매개변수</h6>

`duration` `Number` 대기 시간(밀리초)입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.sleep(1000) // 1 sec.
```

## kill()

지정한 PID를 가진 프로세스를 종료합니다.

<h6>사용 형식</h6>

```js
kill(pid)
```

<h6>매개변수</h6>

`pid` `Number` 종료할 대상 프로세스의 PID입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.kill(123)
```

## ps()

현재 실행 중인 프로세스를 나열합니다.

<h6>사용 형식</h6>

```js
ps()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

`Object[]` `[Process](#process)` 객체 배열입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
list = p.ps()
for( const proc of list ) {
    console.log(
        proc.pid,
        proc.ppid === 0xFFFFFFFF ? "-" : proc.ppid,
        proc.user,
        proc.name,
        proc.uptime)
}
```

## Process

`ps()`가 반환하는 프로세스 정보입니다.

| 속성               | 타입       | 설명                              |
|:-------------------|:-----------|:-------------------|
| pid                | Number     | 프로세스 ID                      |
| ppid               | Number     | 부모 프로세스 ID                |
| user               | String     | 실행 사용자(예: `sys`)          |
| name               | String     | 스크립트 파일 이름              |
| uptime             | String     | 시작 이후 경과 시간             |


## addCleanup()
현재 JavaScript VM이 종료될 때 실행할 콜백을 등록합니다.

<h6>사용 형식</h6>

```js
addCleanup(fn)
```

<h6>매개변수</h6>

`fn` `()=>{}` 종료 시 실행할 콜백입니다.

<h6>반환값</h6>

`Number` `removeCleanup()` 호출에 사용할 토큰.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
p = require("@jsh/process")
p.addCleanup(()=>{ console.log("terminated") })
for(i = 0; i < 3; i++) {
    console.log("run -", i)
}

// run - 0
// run - 1
// run - 2
// terminated
```

## removeCleanup()

등록된 정리 콜백을 토큰으로 제거합니다.

<h6>사용 형식</h6>

```js
removeCleanup(token)
```

<h6>매개변수</h6>

`token` `Number` `addCleanup()`에서 반환된 토큰입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,6]}
p = require("@jsh/process")
token = p.addCleanup(()=>{ console.log("terminated") })
for(i = 0; i < 3; i++) {
    console.log("run -", i)
}
p.removeCleanup(token)

// run - 0
// run - 1
// run - 2
```
