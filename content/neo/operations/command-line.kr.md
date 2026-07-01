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

{{< neo_since ver="8.5.5" />}}

| flag                     | desc                                                              |
|:-------------------------|:----------------------------------------------------------------- |
| `--max-open-conn`        | 데이터베이스에 대한 최대 오픈 연결 수.<br/>(기본값 `-1` 무제한) |
| `--max-idle-conn`        | 연결 풀의 최대 유휴 연결 수.<br/> `<=0`이면 유휴 연결을 유지하지 않음.<br/> (기본값 2) |
| `--conn-max-lifetime`    | 연결을 재사용할 수 있는 최대 시간.<br/> 만료된 연결은 재사용 전에 지연 종료될 수 있음.<br/> `<= 0`이면 연결 시간로 인한 종료 없음. (기본값 `10m`) |
| `--conn-max-idletime`    | 연결이 유휴 상태일 수 있는 최대 시간.<br/> 만료된 연결은 재사용 전에 지연 종료될 수 있음.<br/> `<= 0`이면 유휴 시간으로 인한 종료 없음. (기본값 `1m`)|

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
| `--mqtt-sock`    | `/tmp/machbase-neo-mqtt-5653.sock`| MQTT 유닉스 소켓 {{< neo_since ver="8.0.36" />}}|
| `--http-port`    | `5654`    | HTTP 수신 포트                             |
| `--http-sock`    | `/tmp/machbase-neo-http-5654.sock` | HTTP 유닉스 소켓 {{< neo_since ver="8.0.36" />}}|
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

| flag (long)       | default          | desc                                                             |
|:------------------|:-----------------|:-----------------------------------------------------------------|
| `-s`, `--server`  | `127.0.0.1:5654` | machbase-neo HTTP 주소<br/> 예) `--server 127.0.0.1:5654`<br/>환경 변수: `NEOSHELL_HOST` |
| `--user`          | `sys`            | 사용자 이름<br/>환경 변수: `NEOSHELL_USER`                            |
| `--password`      | `manager`        | 비밀번호<br/>환경 변수: `NEOSHELL_PASSWORD`                          |

machbase-neo 셸은 시작할 때 OS 환경 변수 `NEOSHELL_HOST`, `NEOSHELL_USER`, `NEOSHELL_PASSWORD`에서 서버 주소, 사용자 이름과 비밀번호를 찾습니다.
`--server`, `--user`, `--password` 플래그를 지정하면 환경 변수 대신 해당 값을 사용합니다.

### 사용자 이름과 비밀번호의 우선순위

{{% steps %}}

### 명령줄 플래그

`--server`, `--user`, `--password`를 지정했다면 해당 값을 사용합니다.

### 환경 변수

`$NEOSHELL_HOST`(Windows는 `%NEOSHELL_HOST%`)가 설정되어 있으면 해당 값을 서버 주소로 사용합니다.

`$NEOSHELL_USER`(Windows는 `%NEOSHELL_USER%`)가 설정되어 있으면 해당 값을 사용자 이름으로 사용합니다.

`$NEOSHELL_PASSWORD`(Windows는 `%NEOSHELL_PASSWORD%`)가 설정되어 있으면 해당 값을 비밀번호로 사용합니다.

### 기본값

위 항목이 모두 없으면 기본값 `127.0.0.1:5654`, `sys`, `manager`를 사용합니다.

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
machbase-neo» create tag table if not exists example (
  name varchar(20) primary key,
  time datetime basetime,
  value double summarized
);
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

![machbase-neo_version](/neo/operations/img/machbase-neo-version.png)

## machbase-neo gen-config

기본 설정 템플릿을 출력합니다.

```
$ machbase-neo gen-config ↵

define DEF {
    LISTEN_HOST       = flag("--host", "127.0.0.1")
    SHELL_PORT        = flag("--shell-port", "5652")
    MQTT_PORT         = flag("--mqtt-port", "5653")
    HTTP_PORT         = flag("--http-port", "5654")
......
```
