---
title: 기본 명령어
type: docs
weight: 10
---

JSH는 디렉터리 이동, 파일 읽기, 텍스트 출력, 경로 생성 및 삭제, 대기 시간 처리에 사용할 수 있는
기본 shell 스타일 명령어 집합을 제공합니다.

## 개요

대부분의 명령은 `/sbin` 아래의 JavaScript 파일로 구현되어 있으며 JSH 명령 경로를 통해 실행됩니다.
`cd`는 예외로, 현재 shell의 작업 디렉터리를 변경해야 하므로 internal command로 구현되어 있습니다.

**참고**

- 이 명령들은 호스트 OS 파일 시스템이 아니라 JSH 가상 파일 시스템 안에서 동작합니다.
- 상대 경로는 현재 JSH 작업 디렉터리를 기준으로 해석됩니다.
- `cd`는 현재 shell 세션에 영향을 주고, `pwd`, `ls`, `rm` 같은 나머지 명령은 일반 명령으로 실행됩니다.
- 일부 명령은 Unix 명령과 비교했을 때 의도적으로 더 작은 기능 집합만 제공합니다.

## cat

파일 내용을 표준 출력으로 이어서 출력합니다.
행 번호, 줄 끝 표시, 탭 표시, 빈 줄 압축, 문법 강조 기능도 지원합니다.

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

`-c` 사용 시 다음 확장자에 대해 문법 강조를 지원합니다.

- `.js`
- `.json`
- `.ndjson`
- `.sql`
- `.csv`
- `.yaml`
- `.yml`
- `.toml`

<h6>사용 예시</h6>

```sh
/work > cat -n notes.txt
/work > cat -c script.js
/work > cat -sE log.txt
```

## cd

현재 JSH shell 세션의 작업 디렉터리를 변경합니다.
다른 명령과 달리 `cd`는 별도의 `/sbin/*.js` 파일이 아니라 internal command입니다.

<h6>사용 형식</h6>

```sh
cd <directory>
```

대상 디렉터리가 존재하지 않으면 에러 메시지를 출력하고 non-zero 상태를 반환합니다.

<h6>사용 예시</h6>

```sh
/work > cd subdir
/work/subdir >
```

## echo

전달받은 인자를 공백으로 구분하여 출력하고 마지막에 줄바꿈을 붙입니다.

<h6>사용 형식</h6>

```sh
echo [ARG]...
```

현재 `echo`는 `-n` 같은 shell 스타일 플래그나 escape 시퀀스 해석을 지원하지 않습니다.
전달된 인자를 그대로 출력합니다.

<h6>사용 예시</h6>

```sh
/work > echo hello world
hello world
```

## ls

디렉터리 내용을 나열합니다.
기본적으로는 색상을 적용한 이름을 컬럼 형태로 출력합니다.

<h6>사용 형식</h6>

```sh
ls [OPTION]... [PATH]...
```

<h6>옵션</h6>

- `-l, --long` 상세 목록 형식으로 출력합니다.
- `-a, --all` 숨김 파일을 포함합니다.
- `-t, --time` 수정 시간 기준으로 내림차순 정렬합니다.
- `-R, --recursive` 하위 디렉터리를 재귀적으로 나열합니다.

경로를 생략하면 현재 작업 디렉터리를 사용합니다.
또한 경로 인자에서 `*`, `?` 같은 단순 wildcard 패턴도 지원합니다.

<h6>사용 예시</h6>

```sh
/work > ls
/work > ls -la
/work > ls -t /lib
/work > ls -R src
/work > ls *.js
```

## mkdir

하나 이상의 디렉터리를 생성합니다.

<h6>사용 형식</h6>

```sh
mkdir [OPTION]... DIRECTORY...
```

<h6>옵션</h6>

- `-p, --parents` 필요한 상위 디렉터리까지 함께 생성합니다.
- `-v, --verbose` 생성한 디렉터리마다 메시지를 출력합니다.
- `-h, --help` 도움말을 표시합니다.

`-p` 없이 이미 존재하는 디렉터리를 만들면 에러를 반환합니다.
`-p`를 사용하면 이미 존재하는 디렉터리는 허용됩니다.

<h6>사용 예시</h6>

```sh
/work > mkdir data
/work > mkdir -p logs/app/2026
/work > mkdir -pv build/output
```

## pwd

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

## rm

파일이나 디렉터리를 삭제합니다.

<h6>사용 형식</h6>

```sh
rm [OPTION]... FILE...
```

<h6>옵션</h6>

- `-r, -R, --recursive` 디렉터리와 그 하위 내용을 재귀적으로 삭제합니다.
- `-d, --dir, --directory` 빈 디렉터리를 삭제합니다.
- `-f, --force` 존재하지 않는 경로를 무시하고 missing operand 오류도 억제합니다.
- `-v, --verbose` 삭제한 경로마다 메시지를 출력합니다.
- `-h, --help` 도움말을 표시합니다.

주요 동작은 다음과 같습니다.

- `-r`, `-d` 없이 디렉터리를 삭제하려 하면 `Is a directory` 오류가 발생합니다.
- `-d`는 빈 디렉터리만 삭제할 수 있습니다.
- `-R`은 `-r`과 동일하게 처리됩니다.
- `--directory`는 `--dir`과 동일하게 처리됩니다.

<h6>사용 예시</h6>

```sh
/work > rm old.txt
/work > rm -rf cache
/work > rm -d empty-dir
/work > rm -fv temp.txt missing.txt
```

## sleep

지정한 초 수만큼 대기한 뒤 종료합니다.

<h6>사용 형식</h6>

```sh
sleep [options] <sec>
```

<h6>옵션</h6>

- `-h, --help` 도움말을 표시합니다.

값은 초 단위로 해석됩니다.

<h6>사용 예시</h6>

```sh
/work > sleep 5
```
