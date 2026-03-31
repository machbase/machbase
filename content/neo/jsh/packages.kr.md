---
title: 패키지 관리자
type: docs
weight: 200
---

`pkg` 명령은 `package.json` 생성, JSH 패키지 설치, 패키지 스크립트 실행을 담당합니다.
JSH 애플리케이션이 `/work` 같은 프로젝트 디렉터리 안에서 의존성을 관리할 때 사용합니다.

## 개요

`pkg` 명령은 다음 작업을 지원합니다.

- 새 `package.json` 생성
- `node_modules`에 의존성 설치
- `package-lock.json` 유지
- `package.json`의 `scripts` 실행
- 설치한 패키지의 `bin` 항목으로 실행 wrapper 생성
- 의존성과 생성된 wrapper 제거

## package.json

`pkg`는 `package.json`을 선택된 패키지 루트의 manifest로 취급합니다.
일반 프로젝트 설치에서는 현재 디렉터리 또는 `--dir`로 지정한 디렉터리가 그 루트입니다.
`pkg install -g`, `pkg uninstall -g`에서는 패키지가 `/work/node_modules` 아래에 설치되지만 `/work/package.json`, `/work/package-lock.json`은 만들지 않습니다.

최소한의 프로젝트 manifest 예시는 다음과 같습니다.

```json
{
  "name": "demo-app",
  "version": "1.0.0",
  "scripts": {
    "start": "./main.js"
  },
  "dependencies": {
    "generic-pkg": "^1.2.0",
    "github.com/acme/demo": "#tag=v1.1.0"
  }
}
```

`pkg`가 주로 사용하는 필드는 다음과 같습니다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `name` | `String` | 프로젝트 패키지 이름 |
| `version` | `String` | 프로젝트 버전 |
| `scripts` | `Object` | `pkg run`으로 실행할 이름 있는 명령행 |
| `dependencies` | `Object` | 패키지 이름과 버전 지정자 맵 |

추가 설명:

- `scripts`는 현재 프로젝트 manifest의 항목이며 `pkg run`만 사용합니다.
- `dependencies`는 선택된 패키지 루트 기준으로 `pkg install`, `pkg uninstall`이 갱신합니다.
- 일반 프로젝트 설치에서는 재현 가능한 설치를 위해 `pkg`가 `package.json` 옆에 `package-lock.json`도 기록합니다.
- `bin`은 `node_modules` 아래 각 설치 패키지의 자체 `package.json`에서 읽어 오며, `pkg`는 그것을 바탕으로 `node_modules/.bin` wrapper를 생성합니다.

예를 들어 `pkg install -g github.com/acme/demo`를 실행하면 설치된 패키지 manifest는 `/work/node_modules/github.com/acme/demo/package.json`이고, `pkg`의 전역 metadata는 `/work/node_modules/.pkg/` 아래에 저장됩니다.

## pkg init

현재 프로젝트 디렉터리에 새 `package.json`을 생성합니다.

<h6>사용 형식</h6>

```sh
pkg init [options] <name>
```

<h6>옵션</h6>

- `-C, --dir <dir>` 현재 작업 디렉터리 대신 지정한 프로젝트 디렉터리를 사용합니다.
- `-h, --help` 도움말을 표시합니다.

<h6>사용 예시</h6>

```sh
/work > pkg init demo-app
Created /work/package.json
```

생성되는 파일에는 빈 `scripts`, `dependencies` 객체가 포함됩니다.

```json
{
  "name": "demo-app",
  "version": "1.0.0",
  "scripts": {},
  "dependencies": {}
}
```

## pkg install

`package.json`에 선언된 의존성을 설치하거나, 단일 패키지 요청을 설치하면서
`package.json`, `package-lock.json`을 함께 갱신합니다.

<h6>사용 형식</h6>

```sh
pkg install [options] [name]
```

<h6>옵션</h6>

- `-C, --dir <dir>` 현재 작업 디렉터리 대신 지정한 프로젝트 디렉터리를 사용합니다.
- `-g, --global` `--dir`를 무시하고 `/work/node_modules`에 설치합니다.
- `-h, --help` 도움말을 표시합니다.

`name`을 생략하면 선택된 프로젝트 manifest에 선언된 기존 의존성을 설치합니다. `-g`에서는 `/work/node_modules/.pkg/` 아래의 내부 metadata를 사용합니다.

### 전역 설치

`pkg install -g <name>`은 `/work/node_modules`에 설치합니다.
`-g`가 있으면 `pkg`는 `--dir`을 무시합니다.

이 방식으로 다음 두 가지를 처리할 수 있습니다.

- `bin` wrapper를 셸 `PATH`에서 바로 실행할 수 있는 전역 명령 패키지 설치
- 전역 패키지 디렉터리에 공유 라이브러리 패키지 설치

예시는 다음과 같습니다.

```sh
/work > pkg install -g github.com/acme/demo
Installed github.com/acme/demo#tag=v1.1.0
```

### npm 패키지

패키지 이름이 GitHub 저장소 경로가 아니면 npm registry에서 설치합니다.

```sh
/work > pkg install generic-pkg
Installed generic-pkg@1.2.0
```

이 경우 `package.json`에는 해석된 npm 버전 범위가 저장됩니다.

```json
{
  "dependencies": {
    "generic-pkg": "^1.2.0"
  }
}
```

### GitHub 저장소 패키지

패키지 이름이 `github.com/<org>/<repo>` 형식이면 GitHub 저장소 내용을 직접 내려받아 설치합니다.

지원 형식은 다음과 같습니다.

- `github.com/<org>/<repo>`
- `github.com/<org>/<repo>@<tag>`
- `github.com/<org>/<repo>#tag=<tag>`
- `github.com/<org>/<repo>#branch=<branch>`

동작 방식은 다음과 같습니다.

- `@<tag>` 또는 `#tag=<tag>`를 지정하면 해당 tag를 사용합니다.
- `#branch=<branch>`를 지정하면 tag 존재 여부와 무관하게 해당 branch를 사용합니다.
- tag를 지정하지 않았고 저장소에 tag가 있으면 GitHub tags API가 반환한 최신 tag를 사용합니다.
- tag를 지정하지 않았고 저장소에 tag가 없으면 저장소의 `default_branch`를 사용합니다.

<h6>사용 예시: 최신 tag 설치</h6>

```sh
/work > pkg install github.com/acme/demo
Installed github.com/acme/demo#tag=v1.1.0
```

<h6>사용 예시: 특정 tag 설치</h6>

```sh
/work > pkg install github.com/acme/demo@v1.0.0
Installed github.com/acme/demo#tag=v1.0.0
```

명시적인 ref 구문도 사용할 수 있습니다.

```sh
/work > pkg install github.com/acme/demo#tag=v1.0.0
Installed github.com/acme/demo#tag=v1.0.0
```

<h6>사용 예시: 특정 branch 설치</h6>

```sh
/work > pkg install github.com/acme/demo#branch=develop
Installed github.com/acme/demo#branch=develop
```

<h6>사용 예시: default branch fallback</h6>

저장소에 tag가 하나도 없으면 default branch를 사용합니다.

```sh
/work > pkg install github.com/acme/notags
Installed github.com/acme/notags#branch=main
```

### 설치 위치

설치된 패키지는 선택된 `node_modules` 디렉터리 아래에 복사됩니다.
예를 들면 다음과 같습니다.

- `generic-pkg` -> `node_modules/generic-pkg`
- `github.com/acme/demo` -> `node_modules/github.com/acme/demo`

GitHub 저장소 패키지도 예외 없이 `node_modules` 아래에 설치됩니다.
`pkg install -g`를 사용하면 이 위치는 `/work/node_modules`가 됩니다.

설치한 패키지의 `package.json`에 `bin`이 있으면 `pkg`는 `node_modules/.bin` 아래에 wrapper를 생성합니다.
wrapper 이름은 설치한 패키지 manifest의 `bin` 설정을 그대로 따릅니다.

지원하는 `bin` 형식은 다음 두 가지입니다.

- 문자열 형식: `"bin": "./main.js"`
- 객체 형식: `"bin": { "demo": "./bin/demo.js" }`

`bin`이 문자열이면 `pkg`는 패키지 이름으로부터 wrapper 이름을 결정합니다.
예를 들어 `github.com/acme/demo`는 `demo.js`를 생성합니다.
`bin`이 객체이면 각 key가 wrapper 이름이 됩니다.
wrapper 이름에는 영문자, 숫자, `.`, `_`, `-`만 사용할 수 있습니다.

예를 들어 설치한 패키지 manifest가 다음과 같다면,

```json
{
  "name": "github.com/acme/demo",
  "bin": {
    "demo": "./bin/demo.js"
  }
}
```

`node_modules/.bin/demo.js`가 생성됩니다. 생성된 wrapper는 설치된 패키지 디렉터리로 작업 디렉터리를 옮긴 뒤, `bin`에 지정된 대상을 실행합니다.

따라서 `bin` 대상은 설치된 패키지 루트 기준으로 유효한 경로여야 합니다.
wrapper 뒤에 전달한 추가 인자는 해당 대상에 그대로 전달됩니다.

### 생성된 `.bin` wrapper 실행

`pkg run`은 설치된 패키지의 `.bin` wrapper를 실행하지 않습니다.
`pkg run`은 현재 프로젝트의 `package.json` `scripts`만 실행합니다.

셸 환경에는 `/work/node_modules/.bin` 과 `./node_modules/.bin` 이 `PATH`에 포함되어 있습니다.
따라서 설치된 패키지 실행 파일은 보통 이름만으로 바로 실행할 수 있습니다.

설치된 패키지 실행 파일을 사용하려면 셸에서 생성된 wrapper를 실행하면 됩니다.
예시는 다음과 같습니다.

```sh
/work > demo.js --help
/work > demo.js import sample.csv
```

필요하면 wrapper 경로를 직접 지정해서 실행할 수도 있습니다.

```sh
/work > ./node_modules/.bin/demo.js --help
```

같은 wrapper 이름이 이미 있으면 설치는 계속 진행되고 경고 메시지를 출력하며, 충돌한 wrapper만 생성하지 않습니다.
즉 패키지 설치 자체는 성공하지만, 해당 실행 이름만 만들지 않습니다.

충돌한 파일이 다른 설치 패키지가 만든 wrapper면 경고에 owner package 이름이 포함됩니다.
반대로 `pkg`가 관리하지 않는 기존 파일이면 단순히 existing wrapper로 보고합니다.

### lock file 동작

일반 프로젝트 설치에서는 `pkg`가 재현 가능한 설치를 위해 `package-lock.json`에 해석된 소스를 기록합니다.
GitHub 패키지는 tag 기반인지 branch 기반인지까지 함께 저장합니다.

예시는 다음과 같습니다.

- `github.com/acme/demo#tag=v1.1.0`
- `github.com/acme/notags#branch=main`

lock file이 있으면 `pkg install`은 새 ref를 다시 해석하지 않고 lock에 기록된 GitHub ref를 재사용합니다.

### 에러 보고

GitHub ref를 결정하지 못하면 `pkg`는 두 단계의 실패 원인을 함께 보여줍니다.
예를 들어 tags 조회 실패와 default branch 조회 실패를 한 문장에 묶어서 보고합니다.

## pkg run

`package.json`의 `scripts`를 실행합니다.

<h6>사용 형식</h6>

```sh
pkg run [options] <key> [...args]
```

<h6>옵션</h6>

- `-C, --dir <dir>` 현재 작업 디렉터리 대신 지정한 프로젝트 디렉터리를 사용합니다.
- `-g, --global` `--dir`를 무시하고 `/work/node_modules`에서 패키지를 제거합니다.
- `-h, --help` 도움말을 표시합니다.

`pkg run`은 스크립트를 실행하기 전에 현재 작업 디렉터리를 선택한 프로젝트 디렉터리로 변경합니다.
따라서 `./main.js` 같은 상대 경로 명령은 패키지 디렉터리를 기준으로 해석됩니다.

<h6>사용 예시</h6>

다음 manifest가 있다고 가정하면,

```json
{
  "scripts": {
    "start": "./main.js --mode prod"
  }
}
```

다음과 같이 실행할 수 있습니다.

```sh
/work > pkg run start
```

추가 인자는 스크립트 명령행 뒤에 이어 붙습니다.

```sh
/work > pkg run start --verbose
```

최종적으로 실행되는 명령행은 다음과 같습니다.

```sh
./main.js --mode prod --verbose
```

## pkg uninstall

의존성과 생성된 wrapper를 함께 제거합니다.

<h6>사용 형식</h6>

```sh
pkg uninstall [options] <name>
```

<h6>옵션</h6>

- `-C, --dir <dir>` 현재 작업 디렉터리 대신 지정한 프로젝트 디렉터리를 사용합니다.
- `-h, --help` 도움말을 표시합니다.

`pkg uninstall`은 다음 항목을 정리합니다.

- `package.json`의 dependency 항목
- 설치한 패키지에 속한 `node_modules/.bin` wrapper
- 설치된 패키지 디렉터리
- 필요 시 `package-lock.json`

`pkg install -g`로 설치한 패키지를 제거하려면 `pkg uninstall -g`를 사용합니다.

```sh
/work > pkg uninstall -g github.com/acme/demo
Removed github.com/acme/demo
```

설치 시 alias 충돌 때문에 wrapper 생성이 건너뛰어졌다면 삭제할 wrapper가 없을 수 있습니다.
또한 `pkg uninstall`은 `pkg`가 관리하지 않는 사용자가 만든 `node_modules/.bin` 파일은 삭제하지 않습니다.

<h6>사용 예시</h6>

```sh
/work > pkg uninstall github.com/acme/demo
Removed github.com/acme/demo
```

## 일반적인 작업 순서

```sh
/work > pkg init demo-app
/work > pkg install github.com/acme/demo
/work > pkg install generic-pkg
/work > pkg run start
```

## 참고

- `install`을 패키지 이름 없이 실행하거나 `run`을 실행하려면 유효한 `package.json`이 필요합니다.
- `pkg run`은 POSIX shell이 아니라 JSH 명령 해석을 통해 스크립트 라인을 실행합니다.
- 프로젝트 내부 실행 파일은 `./tool.js` 같은 상대 경로로 정의하는 것을 권장합니다.
- 패키지 개발자는 생성된 wrapper가 설치 패키지 디렉터리에서 실행된다는 점을 기준으로 `./bin/demo.js` 같은 상대 `bin` 경로를 사용하는 편이 안전합니다.
- 패키지 개발자는 실행 이름을 명시적으로 정하고 싶다면 객체 형식 `bin`을, 패키지 이름을 그대로 실행 이름으로 쓰고 싶다면 문자열 형식 `bin`을 사용하면 됩니다.
- GitHub 저장소 설치는 내려받은 저장소 내용 안에 유효한 `package.json`이 있어야 합니다.
