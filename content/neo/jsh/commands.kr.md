---
title: 명령어 레퍼런스
type: docs
weight: 10
---

이 페이지는 JSH shell에서 바로 사용할 수 있는 기본 명령을 기능별로 정리합니다.

## 개요

이 문서는 사용 목적에 따라 명령을 분류합니다.

**참고**

- 모든 명령은 기본적으로 호스트 OS가 아니라 JSH 가상 파일 시스템에서 동작합니다.
- 상대 경로는 현재 JSH 작업 디렉터리를 기준으로 해석됩니다.
- 작업 디렉터리나 환경 변수처럼 현재 shell 상태에 영향을 주는 명령도 포함합니다.
- 일부 명령은 Unix 도구보다 작은 기능 집합만 제공합니다.

## Filesystem Commands

### cd

현재 JSH shell 세션의 작업 디렉터리를 변경합니다.

<h6>사용 형식</h6>

```sh
cd [directory]
```

인자를 생략하면 `$HOME`으로 이동합니다.
대상 경로가 없으면 에러를 출력하고 non-zero 상태를 반환합니다.

<h6>사용 예시</h6>

```sh
/work > cd subdir
/work/subdir >
/work/subdir > cd
/work >
```

### cat

파일 내용을 표준 출력으로 이어서 출력합니다.
행 번호, 줄 끝 표시, 탭 표시, 빈 줄 압축, 문법 강조를 지원합니다.

<h6>사용 형식</h6>

```sh
cat [OPTION]... [FILE]...
```

<h6>옵션</h6>

- `-n, --number` 모든 출력 행에 번호를 붙입니다.
- `-E, --showEnds` 각 줄 끝에 `$`를 표시합니다.
- `-T, --showTabs` 탭 문자를 `^I`로 표시합니다.
- `-s, --squeeze` 연속된 빈 줄을 하나로 압축합니다.
- `-c, --color` 문법 강조를 활성화합니다.
- `-h, --help` 도움말을 표시합니다.

`-c`는 `.js`, `.json`, `.ndjson`, `.sql`, `.csv`, `.yaml`, `.yml`, `.toml` 파일을 강조 표시할 수 있습니다.

<h6>사용 예시</h6>

```sh
/work > cat -n notes.txt
/work > cat -c script.js
/work > cat -sE log.txt
```

### ls

디렉터리 내용을 나열합니다.
기본 출력은 컬럼 형태이며, 숨김 파일, 상세 목록, 시간 정렬, 재귀 탐색을 지원합니다.

<h6>사용 형식</h6>

```sh
ls [OPTION]... [PATH]...
```

<h6>옵션</h6>

- `-l, --long` 상세 목록 형식으로 출력합니다.
- `-a, --all` 숨김 파일을 포함합니다.
- `-t, --time` 수정 시간 기준으로 내림차순 정렬합니다.
- `-R, --recursive` 하위 디렉터리를 재귀적으로 나열합니다.

경로 인자에서는 `*`, `?` wildcard도 지원합니다.

<h6>사용 예시</h6>

```sh
/work > ls
/work > ls -la
/work > ls -t /lib
/work > ls -R src
/work > ls *.js
```

### mkdir

하나 이상의 디렉터리를 생성합니다.

<h6>사용 형식</h6>

```sh
mkdir [OPTION]... DIRECTORY...
```

<h6>옵션</h6>

- `-p, --parents` 필요한 상위 디렉터리까지 함께 생성합니다.
- `-v, --verbose` 생성한 디렉터리마다 메시지를 출력합니다.
- `-h, --help` 도움말을 표시합니다.

`-p` 없이 이미 존재하는 디렉터리를 생성하면 에러를 반환합니다.

<h6>사용 예시</h6>

```sh
/work > mkdir data
/work > mkdir -p logs/app/2026
/work > mkdir -pv build/output
```

### pwd

현재 작업 디렉터리를 출력합니다.

<h6>사용 형식</h6>

```sh
pwd
```

<h6>사용 예시</h6>

```sh
/work > pwd
/work
```

### rm

파일이나 디렉터리를 삭제합니다.

<h6>사용 형식</h6>

```sh
rm [OPTION]... FILE...
```

<h6>옵션</h6>

- `-r, -R, --recursive` 디렉터리와 그 하위 내용을 재귀적으로 삭제합니다.
- `-d, --dir, --directory` 빈 디렉터리를 삭제합니다.
- `-f, --force` 존재하지 않는 경로와 missing operand 오류를 무시합니다.
- `-v, --verbose` 삭제한 경로마다 메시지를 출력합니다.
- `-h, --help` 도움말을 표시합니다.

<h6>사용 예시</h6>

```sh
/work > rm old.txt
/work > rm -rf cache
/work > rm -d empty-dir
/work > rm -fv temp.txt missing.txt
```

## Environment Commands

### env

환경 변수를 출력합니다.
인자를 주지 않으면 전체 환경을 정렬해서 출력하고, 변수 이름을 주면 해당 변수만 출력합니다.

<h6>사용 형식</h6>

```sh
env [NAME]...
```

<h6>사용 예시</h6>

```sh
/work > env
/work > env HOME PWD
```

### setenv

현재 shell 세션의 환경 변수를 설정합니다.

<h6>사용 형식</h6>

```sh
setenv NAME VALUE
setenv NAME=VALUE
```

변수 이름은 영문자 또는 `_`로 시작해야 하며, 이후에는 영문자, 숫자, `_`만 사용할 수 있습니다.

<h6>사용 예시</h6>

```sh
/work > setenv GREETING hello
/work > setenv MESSAGE='hello world'
```

### unsetenv

현재 shell 세션에서 환경 변수를 제거합니다.

<h6>사용 형식</h6>

```sh
unsetenv NAME
```

잘못된 변수 이름이나 누락된 인자를 전달하면 사용법 메시지를 출력합니다.

<h6>사용 예시</h6>

```sh
/work > unsetenv GREETING
```

## System Commands

### pkg

JSH 패키지와 프로젝트 manifest를 관리합니다.
서브커맨드, 옵션, 작업 흐름은 [패키지 관리자](../packages/) 문서를 참고하세요.

<h6>사용 형식</h6>

```sh
pkg <command> [options] [args...]
```

### servicectl

서비스 컨트롤러를 통해 장시간 실행되는 JSH 서비스를 관리합니다.
서브커맨드, 옵션, 서비스 관리 흐름은 [서비스 관리자](../services/) 문서를 참고하세요.

<h6>사용 형식</h6>

```sh
servicectl [--controller=<addr>] <command> [args...]
```

## Text And Utility Commands

### echo

인자를 공백으로 구분해 출력하고 마지막에 줄바꿈을 붙입니다.

<h6>사용 형식</h6>

```sh
echo [ARG]...
```

현재 구현은 `-n` 같은 shell 스타일 플래그나 escape 시퀀스 해석을 지원하지 않습니다.

<h6>사용 예시</h6>

```sh
/work > echo hello world
hello world
```

### sleep

지정한 초 수만큼 대기한 뒤 종료합니다.

<h6>사용 형식</h6>

```sh
sleep [OPTION] <sec>
```

<h6>옵션</h6>

- `-h, --help` 도움말을 표시합니다.

<h6>사용 예시</h6>

```sh
/work > sleep 5
```

### wc

파일별 줄 수, 단어 수, 바이트 수, 문자 수를 계산합니다.
파일을 생략하거나 `-`를 지정하면 표준 입력을 읽습니다.

<h6>사용 형식</h6>

```sh
wc [OPTION]... [FILE]...
```

<h6>옵션</h6>

- `-l, --lines` 줄 수를 출력합니다.
- `-w, --words` 단어 수를 출력합니다.
- `-c, --bytes` 바이트 수를 출력합니다.
- `-m, --chars` 문자 수를 출력합니다.
- `-h, --help` 도움말을 표시합니다.

옵션을 지정하지 않으면 기본적으로 줄 수, 단어 수, 바이트 수를 출력합니다.

<h6>사용 예시</h6>

```sh
/work > wc notes.txt
/work > wc -l *.log
/work > cat notes.txt | wc -w -
```

### which

지정한 명령이 JSH 명령 경로에서 어디에 있는지 출력합니다.

<h6>사용 형식</h6>

```sh
which <command>
```

명령을 찾지 못하면 에러를 출력하고 non-zero 상태를 반환합니다.

<h6>사용 예시</h6>

```sh
/work > which ls
/sbin/ls.js
```

## Messaging Commands

### mqtt_pub

MQTT broker에 메시지를 publish합니다.

<h6>사용 형식</h6>

```sh
mqtt_pub [OPTION]...
```

<h6>옵션</h6>

- `-t, --topic` publish할 topic입니다.
- `-b, --broker` broker 주소입니다. 기본값은 `tcp://localhost:5653`입니다.
- `-m, --message` 직접 지정한 메시지 payload입니다.
- `-f, --file` payload를 읽을 파일입니다.
- `-q, --qos` MQTT QoS 레벨입니다. `0`, `1`, `2`를 지원합니다.
- `-d, --debug` 디버그 로그를 출력합니다.
- `-h, --help` 도움말을 표시합니다.

`-m`과 `-f`는 함께 사용할 수 없습니다.

<h6>사용 예시</h6>

```sh
/work > mqtt_pub -t sensors/temp -m '{"value":21.5}'
/work > mqtt_pub -b tcp://broker:1883 -t logs/app -f payload.json -q 1
```

### nats_pub

NATS subject에 메시지를 publish합니다.
reply subject를 지정하거나 request 모드로 단일 응답을 기다릴 수 있습니다.

<h6>사용 형식</h6>

```sh
nats_pub [OPTION]...
```

<h6>옵션</h6>

- `-t, --topic` publish 대상 subject입니다.
- `-s, --subject` `--topic`과 동일한 의미의 별칭입니다.
- `-b, --broker` broker 주소입니다. 기본값은 `nats://localhost:4222`입니다.
- `-m, --message` 직접 지정한 메시지 payload입니다.
- `-f, --file` payload를 읽을 파일입니다.
- `-r, --reply` 응답을 기다릴 reply subject입니다.
- `--request` 임시 inbox subject를 생성해 응답 하나를 기다립니다.
- `--timeout` 연결과 응답 대기 타임아웃입니다. 기본값은 `10000`ms입니다.
- `-d, --debug` 디버그 로그를 출력합니다.
- `-h, --help` 도움말을 표시합니다.

`-m`과 `-f`는 함께 사용할 수 없습니다.

<h6>사용 예시</h6>

```sh
/work > nats_pub -t events.demo -m 'hello'
/work > nats_pub -s rpc.echo -m 'ping' --request
/work > nats_pub -s rpc.echo -m 'ping' -r reply.demo --timeout 3000
```

## Interactive Commands

### repl

JSH JavaScript REPL을 시작합니다.
명령형 shell이 아니라 JavaScript 표현식을 직접 실행하는 대화형 환경입니다.

<h6>사용 형식</h6>

```sh
repl
```

### shell

새 JSH shell 세션을 시작합니다.
현재 환경을 기반으로 별도 shell 루프를 실행할 때 사용합니다.

<h6>사용 형식</h6>

```sh
shell
```
