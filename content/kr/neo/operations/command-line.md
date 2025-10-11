---
title: 명령줄
type: docs
weight: 10
---

## machbase-neo serve

machbase-neo 서버 프로세스를 시작합니다.

### 플래그

**일반 플래그**
             
| flag             | desc                                                              |
|:-----------------|:----------------------------------------------------------------- |
| `--host`         | 수신 네트워크 주소(기본값 `127.0.0.1`)<br/> 예) `--host 0.0.0.0`                  |
| `-c`, `--config` | 구성 파일 경로<br/> 예) `--config /data/machbase-neo.conf`|
| `--pid`          | PID 저장 파일 경로<br/> 예) `--pid /data/machbase-neo.pid`    |
| `--data`         | 데이터베이스 경로(기본값 `./machbase_home`)<br/> 예) `--data /data/machbase`                 |
| `--file`         | 파일 저장 경로(기본값 `.`)<br/> 예) `--file /data/files`                       |
| `--backup-dir`   | 백업 디렉터리 경로(기본값 `./backups`)<br/> 예) `--backup-dir /data/backups` {{< neo_since ver="8.0.26" />}} |
| `--pref`         | 환경 설정 디렉터리 경로<br/>(기본값 `~/.config/machbase`)                                |
| `--preset`       | 데이터베이스 프리셋 `auto`, `fog`, `edge` (기본값 `auto`)<br/> 예) `--preset edge`    |

**데이터베이스 세션 플래그**

개념적으로 machbase-neo를 TQL을 포함한 API 영역(HTTP, MQTT 등)과 DBMS 영역으로 나누면, 지금까지는 API와 DBMS 사이의 트래픽 제한이 없었습니다.

예를 들어 MQTT 클라이언트 100개와 HTTP 클라이언트 100개, 총 200개가 동시에 DB 쿼리를 실행하면 DBMS에서는 200개의 세션이 실행됩니다.
DBMS로 전달되는 트래픽 흐름을 제어할 수 있다면 상황에 따라 유연하게 구성할 수 있습니다.
이를 위해 `machbase-neo serve`에 사용할 수 있는 새로운 플래그가 추가되었습니다. {{< neo_since ver="8.0.44" />}}

| flag                     | desc                                                              |
|:-------------------------|:----------------------------------------------------------------- |
| `--max-open-conn`        | `< 0`: 무제한(기본값)<br/> `0`: `CPU_코어_수 * factor`<br/> `> 0`: 지정한 최대 연결 수 |
| `--max-open-conn-factor` | `--max-open-conn`이 0일 때 최대 연결 수를 계산하는 계수(기본값 `2`). |
| `--max-open-query`       | `< 0`: 무제한<br/> `0`(기본값): `CPU_코어_수 * factor`<br/> `> 0`: 지정한 최대 쿼리 실행 수 |
| `--max-open-query-factor`| `--max-open-query`가 0일 때 최대 쿼리 실행 수를 계산하는 계수(기본값 `2`) |

- *--mach-open-conn*은 API와 DBMS 사이에서 동시에 열 수 있는 연결(=세션) 수를 제어합니다. 설정값을 초과하면 API 레벨에서 대기합니다.
  - `< 0` 음수(예: -1)를 지정하면 이전 버전과 동일하게 제한 없이 동작합니다.
  - `0` 기본값으로 설정하지 않으면 `CPU 코어 수 * max-open-conn-factor`로 계산합니다. 기본 max-open-conn-factor는 1.5입니다.
  - `> 0` 양수를 지정하면 해당 값에 맞춰 동작합니다.

이 설정은 `machbase-neo shell`에서 `session limit` 명령으로 확인할 수 있으며, `session limit --set=<num>`으로 변경할 수 있습니다.
변경 사항은 프로세스가 실행되는 동안만 유지되므로 영구적으로 적용하려면 시작 스크립트를 수정해야 합니다.

- *--mach-open-conn-factor*는 위의 `--mach-open-conn`이 0(기본값)일 때 `CPU 코어 수 * factor`로 계산하는 계수를 설정합니다.
  값은 0 이상이어야 하며 0 이하로 지정하면 기본값 `2.0`이 적용됩니다.

예를 들어 CPU 코어가 8개이고 factor를 2.0으로 설정하면 최대 16개의 연결이 열리고,
0.5로 설정하면 4개의 연결이 됩니다. 두 옵션을 모두 지정하지 않으면 기본 factor 2.0이 적용되어 16개의 연결이 허용됩니다.

**HTTP 플래그**

{{< neo_since ver="8.0.43" />}}

| flag                    | default     | desc                                                                      |
|:------------------------|:------------|:------------------------------------------------------------------------- |
| `--http-linger`         | `-1`        | HTTP 소켓 옵션. `-1`은 SO_LINGER 비활성화, `>=0`은 SO_LINGER 설정           |
| `--http-readbuf-size`   | `0`         | HTTP 소켓 읽기 버퍼 크기. `0`은 시스템 기본값 사용                          |
| `--http-writebuf-size`  | `0`         | HTTP 소켓 쓰기 버퍼 크기. `0`은 시스템 기본값 사용                          |
| `--http-debug`          | `false`     | HTTP 디버그 로그 활성화                                                    |
| `--http-debug-latency`  | `"0"`       | 지정한 시간보다 오래 걸린 요청만 로그 (예: "3s"). "0"은 모든 요청 기록      |
| `--http-allow-statz`    |             | `/db/statz` API 접근을 허용할 출발지 IP(쉼표 구분). 기본은 `127.0.0.1`만 허용 |

**로그 플래그**

| flag                    | default     | desc                                                                      |
|:------------------------|:------------|:------------------------------------------------------------------------- |
| `--log-filename`        | `-` (stdout)| 로그 파일 경로<br/> 예) `--log-filename /data/logs/machbase-neo.log`       |
| `--log-level`           | `INFO`      | 로그 레벨: TRACE, DEBUG, INFO, WARN, ERROR<br/> 예) `--log-level INFO`    |
| `--log-append`          | `true`      | 기존 로그 파일에 이어쓰기 {{< neo_since ver="8.0.13" />}}                |
| `--log-rotate-schedule` | `@midnight` | 로그 롤링 스케줄 {{< neo_since ver="8.0.13" />}}                          |
| `--log-max-size`        | `10`        | 로그 파일 최대 크기(MB) {{< neo_since ver="8.0.13" />}}                  |
| `--log-max-backups`     | `1`         | 백업 로그 파일 최대 개수 {{< neo_since ver="8.0.13" />}}                 |
| `--log-max-age`         | `7`         | 백업 파일 보관 일수 {{< neo_since ver="8.0.13" />}}                      |
| `--log-compress`        | `false`     | 백업 파일 gzip 압축 {{< neo_since ver="8.0.13" />}}                      |
| `--log-time-utc`        | `false`     | 로그 타임스탬프를 UTC로 기록 {{< neo_since ver="8.0.13" />}}              |

**리스너 플래그**

| flag             | default   | desc                                      |
|:-----------------|:----------|-------------------------------------------|
| `--shell-port`   | `5652`    | SSH 수신 포트                              |
| `--mqtt-port`    | `5653`    | MQTT 수신 포트                             |
| `--mqtt-sock`    | `/tmp/machbase-neo-mqtt.sock`| MQTT 유닉스 소켓 {{< neo_since ver="8.0.36" />}}|
| `--http-port`    | `5654`    | HTTP 수신 포트                             |
| `--http-sock`    | `/tmp/machbase-neo.sock` | HTTP 유닉스 소켓 {{< neo_since ver="8.0.36" />}}|
| `--grpc-port`    | `5655`    | gRPC 수신 포트                             |
| `--grpc-sock`    | `mach-grpc.sock` | gRPC 유닉스 도메인 소켓                 |
| `--grpc-insecure`| `false`   | 평문 TCP 소켓 사용 시 `true`로 설정, TLS 비활성화 {{< neo_since ver="8.0.18" />}} |
| `--mach-port`    | `5656`    | Machbase 네이티브 수신 포트                |

{{< callout type="info" emoji="📌">}}
**중요**<br/>
`--host` 기본값은 루프백 주소이므로 원격 호스트에서 machbase-neo에 접근할 수 없습니다.<br/>
원격 클라이언트의 네트워크 연결을 허용하려면 `--host <host-address>` 또는 `--host 0.0.0.0`으로 설정하십시오.
{{< /callout >}}

플래그 없이 `machbase-neo serve`를 실행하면,

```sh
$ machbase-neo serve
```

다음 명령과 동일합니다.

```sh
$ machbase-neo serve --host 127.0.0.1 --data ./machbase_home --file . --preset auto
```

## machbase-neo shell

machbase-neo 셸을 실행합니다. 다른 인수가 없으면 대화형 모드로 시작합니다.

**플래그**

| flag (long)       | default                | desc                                                             |
|:------------------|:-----------------------|:-----------------------------------------------------------------|
| `-s`, `--server`  | `tcp://127.0.0.1:5655` | machbase-neo gRPC 주소<br/> 예) `-s unix://./mach-grpc.sock`<br/>예) `--server tcp://127.0.0.1:5655` |
| `--user`          | `sys`                  | 사용자 이름<br/>환경 변수: `NEOSHELL_USER`         {{< neo_since ver="8.0.4" />}} |
| `--password`      | `manager`              | 비밀번호<br/>환경 변수: `NEOSHELL_PASSWORD`      {{< neo_since ver="8.0.4" />}} |

machbase-neo 셸은 시작할 때 OS 환경 변수 `NEOSHELL_USER`, `NEOSHELL_PASSWORD`에서 사용자 이름과 비밀번호를 찾습니다.
`--user`, `--password` 플래그를 지정하면 환경 변수 대신 해당 값을 사용합니다.

### 사용자 이름과 비밀번호의 우선순위

{{% steps %}}

### 명령줄 플래그

`--user`, `--password`를 지정했다면 해당 값을 사용합니다.

### 환경 변수

`$NEOSHELL_USER`(Windows는 `%NEOSHELL_USER%`)가 설정되어 있으면 해당 값을 사용자 이름으로 사용합니다.

`$NEOSHELL_PASSWORD`(Windows는 `%NEOSHELL_PASSWORD%`)가 설정되어 있으면 해당 값을 비밀번호로 사용합니다.

### 기본값

위 항목이 모두 없으면 기본값 `sys`, `manager`를 사용합니다.

{{% /steps %}}

### 실무 예시

보안을 위해 아래처럼 즉석 환경 변수를 사용하는 것을 권장합니다.

```sh
$ NEOSHELL_PASSWORD='my-secret' machbase-neo shell --user sys
```

`--password` 플래그를 사용하면 아래와 같이 단순한 `ps` 명령으로 비밀번호가 노출될 수 있다는 점에 주의하십시오.

```sh
$ machbase-neo shell --user sys --password manager
```

```sh
$ ps -aef |grep machbase-neo
  501 13551  3598   0  9:33AM ttys000    0:00.07 machbase-neo shell --user sys --password manager
```

**쿼리 실행**
  
```sh
machbase-neo» select binary_signature from v$version;
┌────────┬─────────────────────────────────────────────┐
│ ROWNUM │ BINARY_SIGNATURE                            │
├────────┼─────────────────────────────────────────────┤
│      1 │ 8.0.2.develop-LINUX-X86-64-release-standard │
└────────┴─────────────────────────────────────────────┘
a row fetched.
```

**테이블 생성**

```sh
machbase-neo» create tag table if not exists example (name varchar(20) primary key, time datetime basetime, value double summarized);
executed.
```

**스키마 확인**

```sh
machbase-neo» desc example;
┌────────┬───────┬──────────┬────────┐
│ ROWNUM │ NAME  │ TYPE     │ LENGTH │
├────────┼───────┼──────────┼────────┤
│      1 │ NAME  │ varchar  │     20 │
│      2 │ TIME  │ datetime │      8 │
│      3 │ VALUE │ double   │      8 │
└────────┴───────┴──────────┴────────┘
```

**데이터 삽입**

```sh
machbase-neo» insert into example values('tag0', to_date('2021-08-12'), 100);
a row inserted.
```

**데이터 조회**

```sh
machbase-neo» select * from example;
┌────────┬──────┬─────────────────────┬───────┐
│ ROWNUM │ NAME │ TIME(LOCAL)         │ VALUE │
├────────┼──────┼─────────────────────┼───────┤
│      1 │ tag0 │ 2021-08-12 00:00:00 │ 100   │
└────────┴──────┴─────────────────────┴───────┘
a row fetched.
```

**테이블 삭제**

```sh
machbase-neo» drop table example;
executed.
```

### 서브 커맨드

#### explain

구문: `explain [--full] <sql>`

SQL 실행 계획을 보여줍니다.

```sh
machbase-neo» explain select * from example where name = 'tag.1';
 PROJECT
  TAG READ (RAW)
   KEYVALUE INDEX SCAN (_EXAMPLE_DATA_0)
    [KEY RANGE]
     * IN ()
   VOLATILE INDEX SCAN (_EXAMPLE_META)
    [KEY RANGE]
     *
```

#### export

```
  export [options] <table>
  arguments:
    table                    읽어올 테이블 이름
  options:
    -o,--output <file>       출력 파일(기본값: `-` stdout)
    -f,--format <format>     출력 형식
                csv          CSV 형식(기본값)
                json         JSON 형식
       --compress <method>   압축 방식 [gzip] (기본값은 비압축)
       --[no-]heading        헤더 출력 여부(기본값:false)
       --[no-]footer         푸터 출력 여부(기본값:false)
    -d,--delimiter           CSV 구분자(기본값 `,`)
       --tz                  datetime 처리용 타임존 지정
    -t,--timeformat          시간 형식 [ns|ms|s|<timeformat>] (기본값 `ns`)
                             자세한 내용은 "help timeformat" 참조
    -p,--precision <int>     부동소수점 값을 강제로 반올림할 자릿수 지정
```

#### import

```
  import [options] <table>
  arguments:
    table                 데이터를 쓸 테이블 이름
  options:
    -i,--input <file>     입력 파일(기본값: `-` 표준입력)
    -f,--format <fmt>     파일 형식 [csv] (기본값 `csv`)
       --compress <alg>   입력 데이터 압축 방식(지원: gzip)
       --no-header        헤더 없음, 첫 줄 생략하지 않음(기본값)
       --charset          입력이 UTF-8이 아니면 문자 인코딩 지정
       --header           첫 줄이 헤더이면 건너뜀
       --method           쓰기 방식 [insert|append] (기본값 `insert`)
       --create-table     테이블이 없으면 생성(기본값:false)
       --truncate-table   새 데이터 입력 전 테이블 비우기(기본값:false)
    -d,--delimiter        CSV 구분자(기본값 `,`)
       --tz               datetime 처리용 타임존 지정
    -t,--timeformat       시간 형식 [ns|ms|s|<timeformat>] (기본값 `ns`)
                          자세한 내용은 "help timeformat" 참조
       --eof <string>     EOF 라인 지정, [a-zA-Z0-9]+ 에 맞는 문자열 사용(기본값 '.')
```

#### show info

서버 정보를 표시합니다.

```sh
machbase-neo» show info;
┌────────────────────┬─────────────────────────────┐
│ NAME               │ VALUE                       │
├────────────────────┼─────────────────────────────┤
│ build.version      │ v2.0.0                      │
│ build.hash         │ #c953293f                   │
│ build.timestamp    │ 2023-08-29T08:08:00         │
│ build.engine       │ static_standard_linux_amd64 │
│ runtime.os         │ linux                       │
│ runtime.arch       │ amd64                       │
│ runtime.pid        │ 57814                       │
│ runtime.uptime     │ 2h 30m 57s                  │
│ runtime.goroutines │ 45                          │
│ mem.sys            │ 32.6 MB                     │
│ mem.heap.sys       │ 19.0 MB                     │
│ mem.heap.alloc     │ 9.7 MB                      │
│ mem.heap.in-use    │ 13.0 MB                     │
│ mem.stack.sys      │ 1,024.0 KB                  │
│ mem.stack.in-use   │ 1,024.0 KB                  │
└────────────────────┴─────────────────────────────┘
```

#### show ports

서버의 인터페이스 포트를 표시합니다.

```sh
machbase-neo» show ports;
┌─────────┬────────────────────────────────────────┐
│ SERVICE │ PORT                                   │
├─────────┼────────────────────────────────────────┤
│ grpc    │ tcp://127.0.0.1:5655                   │
│ grpc    │ unix:///database/mach-grpc.sock        │
│ http    │ tcp://127.0.0.1:5654                   │
│ mach    │ tcp://127.0.0.1:5656                   │
│ mqtt    │ tcp://127.0.0.1:5653                   │
│ shell   │ tcp://127.0.0.1:5652                   │
└─────────┴────────────────────────────────────────┘
```

#### show tables

구문: `show tables [-a]`

테이블 목록을 표시합니다. `-a` 플래그를 지정하면 숨김 테이블이 포함됩니다.

```sh
machbase-neo» show tables;
┌────────┬────────────┬──────┬─────────────┬───────────┐
│ ROWNUM │ DB         │ USER │ NAME        │ TYPE      │
├────────┼────────────┼──────┼─────────────┼───────────┤
│      1 │ MACHBASEDB │ SYS  │ EXAMPLE     │ Tag Table │
│      2 │ MACHBASEDB │ SYS  │ TAG         │ Tag Table │
│      3 │ MACHBASEDB │ SYS  │ TAGDATA     │ Tag Table │
└────────┴────────────┴──────┴─────────────┴───────────┘
```

#### show table

구문: `show table [-a] <table>`

테이블의 컬럼 목록을 표시합니다. `-a` 플래그를 지정하면 숨김 컬럼도 함께 표시됩니다.

```sh
machbase-neo» show table example -a;
┌────────┬───────┬──────────┬────────┬──────────┐
│ ROWNUM │ NAME  │ TYPE     │ LENGTH │ DESC     │
├────────┼───────┼──────────┼────────┼──────────┤
│      1 │ NAME  │ varchar  │    100 │ tag name │
│      2 │ TIME  │ datetime │     31 │ basetime │
│      3 │ VALUE │ double   │     17 │          │
│      4 │ _RID  │ long     │     20 │          │
└────────┴───────┴──────────┴────────┴──────────┘
```

#### show meta-tables

```sh
machbase-neo» show meta-tables;
┌────────┬─────────┬────────────────────────┬─────────────┐
│ ROWNUM │      ID │ NAME                   │ TYPE        │
├────────┼─────────┼────────────────────────┼─────────────┤
│      1 │ 1000020 │ M$SYS_TABLESPACES      │ Fixed Table │
│      2 │ 1000024 │ M$SYS_TABLESPACE_DISKS │ Fixed Table │
│      3 │ 1000049 │ M$SYS_TABLES           │ Fixed Table │
│      4 │ 1000051 │ M$TABLES               │ Fixed Table │
│      5 │ 1000053 │ M$SYS_COLUMNS          │ Fixed Table │
│      6 │ 1000054 │ M$COLUMNS              │ Fixed Table │
......
```

#### show virtual-tables

```sh
machbase-neo» show virtual-tables;
┌────────┬─────────┬─────────────────────────────────────────┬────────────────────┐
│ ROWNUM │      ID │ NAME                                    │ TYPE               │
├────────┼─────────┼─────────────────────────────────────────┼────────────────────┤
│      1 │      65 │ V$HOME_STAT                             │ Fixed Table (stat) │
│      2 │      93 │ V$DEMO_STAT                             │ Fixed Table (stat) │
│      3 │     227 │ V$SAMPLEBENCH_STAT                      │ Fixed Table (stat) │
│      4 │     319 │ V$TAGDATA_STAT                          │ Fixed Table (stat) │
│      5 │     382 │ V$EXAMPLE_STAT                          │ Fixed Table (stat) │
│      6 │     517 │ V$TAG_STAT                              │ Fixed Table (stat) │
......
```

#### show users

```sh
machbase-neo» show users;
┌────────┬───────────┐
│ ROWNUM │ USER_NAME │
├────────┼───────────┤
│      1 │ SYS       │
└────────┴───────────┘
a row fetched.
```

#### show license

```sh
 machbase-neo» show license;
┌────────┬──────────┬──────────────┬──────────┬────────────┬──────────────┬─────────────────────┐
│ ROWNUM │ ID       │ TYPE         │ CUSTOMER │ PROJECT    │ COUNTRY_CODE │ INSTALL_DATE        │
├────────┼──────────┼──────────────┼──────────┼────────────┼──────────────┼─────────────────────┤
│      1 │ 00000023 │ FOGUNLIMITED │ VUTECH   │ FORESTFIRE │ KR           │ 2024-04-22 15:56:14 │
└────────┴──────────┴──────────────┴──────────┴────────────┴──────────────┴─────────────────────┘
a row fetched.
```

#### session list

구문: `session list` {{< neo_since ver="8.0.17" />}}

```sh
 machbase-neo» session list;
┌────┬───────────┬─────────┬────────────┬─────────┬─────────┬──────────┐
│ ID │ USER_NAME │ USER_ID │ STMT_COUNT │ CREATED │ LAST    │ LAST SQL │
├────┼───────────┼─────────┼────────────┼─────────┼─────────┼──────────┤
│ 25 │ SYS       │ 1       │          1 │ 1.667ms │ 1.657ms │ CONNECT  │
└────┴───────────┴─────────┴────────────┴─────────┴─────────┴──────────┘
```

#### session kill

구문: `session kill <ID>` {{< neo_since ver="8.0.17" />}}

#### session stat

구문: `session stat` {{< neo_since ver="8.0.17" />}}

```sh
machbase-neo» session stat;
┌────────────────┬───────┐
│ NAME           │ VALUE │
├────────────────┼───────┤
│ CONNS          │ 1     │
│ CONNS_USED     │ 17    │
│ STMTS          │ 0     │
│ STMTS_USED     │ 20    │
│ APPENDERS      │ 0     │
│ APPENDERS_USED │ 0     │
│ RAW_CONNS      │ 1     │
└────────────────┴───────┘
```

#### desc

Syntax `desc [-a] <table>`

테이블 구조를 확인합니다.

```sh
machbase-neo» desc example;
┌────────┬───────┬──────────┬────────┬──────────┐
│ ROWNUM │ NAME  │ TYPE     │ LENGTH │ DESC     │
├────────┼───────┼──────────┼────────┼──────────┤
│      1 │ NAME  │ varchar  │    100 │ tag name │
│      2 │ TIME  │ datetime │     31 │ basetime │
│      3 │ VALUE │ double   │     17 │          │
└────────┴───────┴──────────┴────────┴──────────┘
```

## machbase-neo restore

구문: `machbase-neo restore --data <machbase_home_dir> <backup_dir>` {{< neo_since ver="8.0.17" />}}

백업에서 데이터베이스를 복구합니다.

```sh
$ machbase-neo restore --data <machbase home dir>  <backup dir>
```

## machbase-neo version

버전 및 엔진 정보를 보여 줍니다.

![machbase-neo_version](../img/machbase-neo-version.png)

## machbase-neo gen-config

기본 설정 템플릿을 출력합니다.

```
$ machbase-neo gen-config ↵

define DEF {
    LISTEN_HOST       = flag("--host", "127.0.0.1")
    SHELL_PORT        = flag("--shell-port", "5652")
    MQTT_PORT         = flag("--mqtt-port", "5653")
    HTTP_PORT         = flag("--http-port", "5654")
    GRPC_PORT         = flag("--grpc-port", "5655")
......
```
