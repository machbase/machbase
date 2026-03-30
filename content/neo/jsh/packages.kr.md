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

## package.json

최소한의 manifest 예시는 다음과 같습니다.

```json
{
  "name": "demo-app",
  "version": "1.0.0",
  "scripts": {
    "start": "./main.js"
  },
  "dependencies": {
    "generic-pkg": "^1.2.0",
    "github.com/acme/demo": "v1.1.0"
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
| `neo.installType` | `String` | GitHub 저장소 패키지의 설치 방식을 지정하는 선택 필드 |

GitHub 저장소 설치에서는 다음과 같은 사용자 정의 metadata를 인식합니다.

```json
{
  "neo": {
    "installType": "application"
  }
}
```

`neo.installType` 값이 `application`이면 `pkg install github.com/<org>/<repo>`는 내려받은 저장소를 라이브러리 의존성이 아니라 애플리케이션 프로젝트로 간주합니다.

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
- `-h, --help` 도움말을 표시합니다.

`name`을 생략하면 `package.json`에 선언된 기존 의존성을 설치합니다.

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

동작 방식은 다음과 같습니다.

- `@<tag>`를 지정하면 해당 tag를 사용합니다.
- tag를 지정하지 않았고 저장소에 tag가 있으면 GitHub tags API가 반환한 최신 tag를 사용합니다.
- tag를 지정하지 않았고 저장소에 tag가 없으면 저장소의 `default_branch`를 사용합니다.

<h6>사용 예시: 최신 tag 설치</h6>

```sh
/work > pkg install github.com/acme/demo
Installed github.com/acme/demo@v1.1.0
```

<h6>사용 예시: 특정 tag 설치</h6>

```sh
/work > pkg install github.com/acme/demo@v1.0.0
Installed github.com/acme/demo@v1.0.0
```

<h6>사용 예시: default branch fallback</h6>

저장소에 tag가 하나도 없으면 default branch를 사용합니다.

```sh
/work > pkg install github.com/acme/notags
Installed github.com/acme/notags@main
```

### 설치 위치

설치된 패키지는 프로젝트의 `node_modules` 디렉터리 아래에 복사됩니다.
예를 들면 다음과 같습니다.

- `generic-pkg` -> `node_modules/generic-pkg`
- `github.com/acme/demo` -> `node_modules/github.com/acme/demo`

다만 GitHub 저장소 패키지는 manifest metadata로 이 동작을 바꿀 수 있습니다.
내려받은 `package.json`에 `neo.installType: "application"`이 있으면 `pkg`는 해당 저장소를 `node_modules` 아래에 두지 않고, 선택한 대상 디렉터리 자체에 애플리케이션으로 설치합니다.

이 경우에는 다음과 같이 동작합니다.

- 저장소 파일이 대상 프로젝트 파일이 됩니다.
- 내려받은 `package.json`이 대상 프로젝트의 `package.json`이 됩니다.
- 애플리케이션의 의존성만 대상 프로젝트의 `node_modules`에 설치됩니다.

이 방식은 설치 후 바로 작업 디렉터리로 사용할 애플리케이션 템플릿이나 starter project에 유용합니다.

### lock file 동작

`pkg`는 재현 가능한 설치를 위해 `package-lock.json`에 해석된 소스를 기록합니다.
GitHub 패키지는 tag 기반인지 branch 기반인지까지 함께 저장합니다.

예시는 다음과 같습니다.

- `github.com/acme/demo#tag=v1.1.0`
- `github.com/acme/notags#branch=main`

lock file이 있으면 `pkg install`은 새 ref를 다시 해석하지 않고 lock에 기록된 GitHub ref를 재사용합니다.

### 에러 보고

GitHub ref를 결정하지 못하면 `pkg`는 두 단계의 실패 원인을 함께 보여줍니다.
예를 들어 tags 조회 실패와 default branch 조회 실패를 한 문장에 묶어서 보고합니다.

## pkg run

`package.json`의 `scripts`에 정의된 이름 있는 항목을 실행합니다.

<h6>사용 형식</h6>

```sh
pkg run [options] <key> [...args]
```

<h6>옵션</h6>

- `-C, --dir <dir>` 현재 작업 디렉터리 대신 지정한 프로젝트 디렉터리를 사용합니다.
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
- GitHub 저장소 설치는 내려받은 저장소 내용 안에 유효한 `package.json`이 있어야 합니다.
