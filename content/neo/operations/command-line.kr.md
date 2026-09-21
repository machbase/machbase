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

| flag                    | default     | desc                                                                   |
|:------------------------|:------------|:---------------------------------------------------------------------- |
| `--log-filename`        | `-` (stdout)| 로그 파일 경로<br/> 예) `--log-filename /data/logs/machbase-neo.log`       |
| `--log-level`           | `INFO`      | 로그 레벨: TRACE, DEBUG, INFO, WARN, ERROR<br/> 예) `--log-level INFO`    |
| `--log-append`          | `true`      | 기존 로그 파일에 이어쓰기                                                    |
| `--log-rotate-schedule` | `@midnight` | 로그 롤링 스케줄                                                           |
| `--log-max-size`        | `10`        | 로그 파일 최대 크기(MB)                                                    |
| `--log-max-backups`     | `1`         | 백업 로그 파일 최대 개수                                                    |
| `--log-max-age`         | `7`         | 백업 파일 보관 일수                                                        |
| `--log-compress`        | `false`     | 백업 파일 gzip 압축                                                       |
| `--log-time-utc`        | `false`     | 로그 타임스탬프를 UTC로 기록                                                 |

**리스너 플래그**

| flag             | default   | desc                                      |
|:-----------------|:----------|-------------------------------------------|
| `--shell-port`   | `5652`    | SSH 수신 포트                              |
| `--mqtt-port`    | `5653`    | MQTT 수신 포트                             |
| `--mqtt-sock`    | `/tmp/machbase-neo-mqtt-5653.sock`| MQTT 유닉스 소켓    |
| `--http-port`    | `5654`    | HTTP 수신 포트                             |
| `--http-sock`    | `/tmp/machbase-neo-http-5654.sock` | HTTP 유닉스 소켓   |
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
| `--server`        | `127.0.0.1:5654` | machbase-neo HTTP 주소<br/> 예) `--server 127.0.0.1:5654`<br/>환경 변수: `NEOSHELL_HOST` |
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

두 방법 중 어느 쪽으로도 지정하지 않은 값은 셸이 기본값(`127.0.0.1:5654`, `SYS`, `manager`)과 함께 입력을 요청합니다. Enter 키를 누르면 기본값을 사용합니다.

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
┌────────┬──────────────────────────────────────────────────┐
│ ROWNUM │ BINARY_SIGNATURE                                 │
├────────┼──────────────────────────────────────────────────┤
│      1 │ 8.7.0.official-DARWIN-ARM_M1-64-release-standard │
└────────┴──────────────────────────────────────────────────┘
a row selected.
```

**테이블 생성**

```sh
machbase-neo» create tag table if not exists example (
  name varchar(20) primary key,
  time datetime basetime,
  value double summarized
);
table created.
```

**스키마 확인**

```sh
machbase-neo» desc example;
┌────────┬────────┬──────────┬────────┬────────────┬───────┐
│ ROWNUM │ COLUMN │ TYPE     │ LENGTH │ FLAG       │ INDEX │
├────────┼────────┼──────────┼────────┼────────────┼───────┤
│      1 │ NAME   │ varchar  │     20 │ tag name   │       │
│      2 │ TIME   │ datetime │     31 │ base time  │       │
│      3 │ VALUE  │ double   │     17 │ summarized │       │
└────────┴────────┴──────────┴────────┴────────────┴───────┘
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
│ ROWNUM │ NAME │ TIME                │ VALUE │
├────────┼──────┼─────────────────────┼───────┤
│      1 │ tag0 │ 2021-08-12 00:00:00 │   100 │
└────────┴──────┴─────────────────────┴───────┘
a row selected.
```

**테이블 삭제**

```sh
machbase-neo» drop table example;
table dropped.
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
     * name = 'tag.1'
```

#### export

```
Usage: export [options] <table>

Arguments:
  table - table name to read

Options:
  -h, --help         Show this help message
  -o, --output       output file (default:'-' stdout) (default: -)
      --compress     compression type (none, gzip) (default: none)
  -f, --format       output format (box, csv, tsv, json, ndjson) (default: csv)
  -t, --timeformat   time format [ns|us|ms|s|<timeformat>] (default: ns)
      --tz           time zone for handling datetime (default: time zone) (default: local)
  -p, --precision    set precision of float value to force round (default: -1)
      --[no-]header  print header (default: false)
      --null-value   string to represent null values (default: )
      --[no-]silent  suppress progress output (default: false)
```

#### import

```
Usage: import [options] <table>

Arguments:
  table - table name to read

Options:
  -h, --help          Show this help message
  -i, --input         input file (default:'-' stdin) (default: -)
      --compress      compression type (none, gzip) (default: none)
  -f, --format        input format (csv, tsv, ndjson) (default: csv)
  -t, --timeformat    time format [ns|us|ms|s|<timeformat>] (default: ns)
      --tz            time zone for handling datetime (default: time zone) (default: local)
      --header        header option [skip|columns|none] (default: none)
      --null-value    string to represent null values (default: NULL)
      --[no-]dry-run  run in dry mode (default: false)
      --[no-]verbose  verbose mode, it works only with --dry-run (default: false)
```

#### show info

서버 정보를 표시합니다.

```sh
machbase-neo» show info;
┌────────┬────────────────────┬──────────────────────────────┐
│ ROWNUM │ NAME               │ VALUE                        │
├────────┼────────────────────┼──────────────────────────────┤
│      1 │ build.engine       │ static_standard_darwin_arm64 │
│      2 │ build.hash         │ b55f8170                     │
│      3 │ build.timestamp    │ 2026-09-10T05:43:13          │
│      4 │ build.version      │ v8.7.1-snapshot              │
│      5 │ mem.frees          │ 397,853,948                  │
│      6 │ mem.heap_alloc     │ 32.8MB                       │
│      7 │ mem.heap_in_use    │ 40.0MB                       │
│      8 │ mem.heap_sys       │ 547.9MB                      │
│      9 │ mem.lives          │ 253,315                      │
│     10 │ mem.mallocs        │ 398,107,263                  │
│     11 │ mem.stack_in_use   │ 1.5MB                        │
│     12 │ mem.stack_sys      │ 1.5MB                        │
│     13 │ mem.sys            │ 564.2MB                      │
│     14 │ runtime.arch       │ arm64                        │
│     15 │ runtime.goroutines │ 32                           │
│     16 │ runtime.os         │ darwin                       │
│     17 │ runtime.pid        │ 35507                        │
│     18 │ runtime.processes  │ 10                           │
│     19 │ runtime.uptime     │ 6 days 4h 4m 42s             │
└────────┴────────────────────┴──────────────────────────────┘
```

#### show ports

서버의 인터페이스 포트를 표시합니다.

```sh
machbase-neo» show ports;
┌────────┬────────────┬─────────────────────────────────────────┐
│ ROWNUM │ PORT       │ ADDRESS                                 │
├────────┼────────────┼─────────────────────────────────────────┤
│      1 │ http       │ tcp://127.0.0.1:5654                    │
│      2 │ http       │ unix:///tmp/machbase-neo-http-5654.sock │
│      3 │ mach       │ tcp://127.0.0.1:5656                    │
│      4 │ mqtt       │ tcp://127.0.0.1:5653                    │
│      5 │ mqtt       │ unix:///tmp/machbase-neo-mqtt-5653.sock │
│      6 │ servicectl │ tcp://127.0.0.1:62978                   │
│      7 │ shell      │ tcp://127.0.0.1:5652                    │
└────────┴────────────┴─────────────────────────────────────────┘
```

#### show tables

구문: `show tables [FROM <database>[.<user>]] [LIKE <pattern>] [WITH ALL]`

{{< neo_since ver="8.7.0" />}}

`show` 명령은 일부 하위 명령에서 `FROM`과 `LIKE` 절을 지원합니다.
`FROM <database>[.<user>]`는 조회할 데이터베이스와 사용자를 지정하고, `LIKE <pattern>`은 이름 패턴으로 결과를 필터링합니다.
`LIKE` 패턴은 작은따옴표나 큰따옴표로 감싼 SQL `LIKE` 패턴을 사용하며, `%`는 0개 이상의 문자, `_`는 1개의 문자와 일치합니다.
`FROM` 대신 `IN`을 사용할 수 있습니다.
`WITH ALL`은 숨김 항목을 포함합니다.

```sh
machbase-neo» show tables from MACHBASEDB.SYS like 'TAG%' with all;
machbase-neo» show indexes like 'IDX_%';
```

| command | `FROM` | `LIKE` | `WITH ALL` | `LIKE` 적용 대상 |
|:--------|:------:|:------:|:----------:|:-----------------|
| `show tables` | O | O | O | 테이블 이름 |
| `show indexes` | O | O | - | 인덱스 이름 |
| `show table [-a] <table>` | O | - | - | - |
| `show index <index>` | O | - | - | - |
| `show tags <table> [tag...]` | O | O | - | 태그 이름 |
| `show storage` | O | O | - | 테이블 이름 |
| `show table-usage` | O | O | - | 테이블 이름 |
| `show lsm` | O | O | - | 테이블 이름 |
| `show indexgap` | O | O | - | 테이블 이름 |
| `show tagindexgap` | O | O | - | 테이블 이름 |
| `show rollupgap` | O | O | - | 테이블 이름 |
| `show users` | - | O | - | 사용자 이름 |
| `show databases` | - | O | - | 데이터베이스 이름 |
| `show meta-tables` | - | O | - | 테이블 이름 |
| `show virtual-tables` | - | O | - | 테이블 이름 |
| `show sessions` | - | O | - | 사용자 이름 |
| `show statements` | - | O | - | 쿼리 텍스트 |

`show table`, `show index`, `show tags` 처럼 대상 이름을 인자로 받는 명령에서는 `<database>.<user>.<name>` 형식의 한정 이름과 `FROM` 절을 동시에 사용할 수 없습니다.
`show tags`에서 명시적인 태그 이름을 인자로 지정한 경우에는 `LIKE` 절을 함께 사용할 수 없습니다.

테이블 목록을 표시합니다. `WITH ALL`을 지정하면 숨김 테이블이 포함됩니다.

```sh
machbase-neo» show tables;
┌────────┬───────────────┬───────────┬────────────┬──────────┬────────────┬────────────┐
│ ROWNUM │ DATABASE_NAME │ USER_NAME │ TABLE_NAME │ TABLE_ID │ TABLE_TYPE │ TABLE_FLAG │
├────────┼───────────────┼───────────┼────────────┼──────────┼────────────┼────────────┤
│      1 │ MACHBASEDB    │ SYS       │ EXAMPLE    │      770 │ Tag        │            │
└────────┴───────────────┴───────────┴────────────┴──────────┴────────────┴────────────┘
```

#### show table

구문: `show table [-a] <table>`

테이블의 컬럼 목록을 표시합니다. `-a`를 지정하면 숨김 컬럼도 함께 표시됩니다.

```sh
machbase-neo» show table -a example;
┌────────┬────────┬──────────┬────────┬────────────┬───────┐
│ ROWNUM │ COLUMN │ TYPE     │ LENGTH │ FLAG       │ INDEX │
├────────┼────────┼──────────┼────────┼────────────┼───────┤
│      1 │ NAME   │ varchar  │     20 │ tag name   │       │
│      2 │ TIME   │ datetime │     31 │ base time  │       │
│      3 │ VALUE  │ double   │     17 │ summarized │       │
│      4 │ _RID   │ long     │     20 │            │       │
└────────┴────────┴──────────┴────────┴────────────┴───────┘
```

#### show indexes

구문: `show indexes [FROM <database>[.<user>]] [LIKE <pattern>]`

인덱스 목록을 표시합니다. `FROM` 절로 조회 범위를 지정하고 `LIKE` 절로 인덱스 이름을 필터링할 수 있습니다.

```sh
machbase-neo» show indexes from MACHBASEDB.SYS like 'TAG%';
```

#### show meta-tables

```sh
machbase-neo» show meta-tables;
┌────────┬─────────┬────────────────────────┬───────┐
│ ROWNUM │      ID │ NAME                   │ TYPE  │
├────────┼─────────┼────────────────────────┼───────┤
│      1 │ 1000019 │ M$SYS_TABLESPACES      │ Fixed │
│      2 │ 1000023 │ M$SYS_TABLESPACE_DISKS │ Fixed │
│      3 │ 1000049 │ M$SYS_TABLES           │ Fixed │
│      4 │ 1000052 │ M$SYS_VIEWS            │ Fixed │
│      5 │ 1000054 │ M$TABLES               │ Fixed │
│      6 │ 1000056 │ M$SYS_COLUMNS          │ Fixed │
......
```

#### show virtual-tables

```sh
machbase-neo» show virtual-tables;
┌────────┬─────────┬─────────────────────────────────────────┬───────┐
│ ROWNUM │      ID │ NAME                                    │ TYPE  │
├────────┼─────────┼─────────────────────────────────────────┼───────┤
│      1 │     769 │ V$EXAMPLE_STAT                          │ Fixed │
│      2 │ 1000000 │ V$SYSSTAT                               │ Fixed │
│      3 │ 1000001 │ V$SYSTIME                               │ Fixed │
│      4 │ 1000002 │ V$SYSMEM                                │ Fixed │
│      5 │ 1000003 │ V$PROPERTY                              │ Fixed │
│      6 │ 1000004 │ V$MUTEX                                 │ Fixed │
......
```

#### show users

```sh
machbase-neo» show users;
┌────────┬─────────┬──────┐
│ ROWNUM │ USER_ID │ NAME │
├────────┼─────────┼──────┤
│      1 │       1 │ SYS  │
└────────┴─────────┴──────┘
```

#### show license

```sh
machbase-neo» show license;
┌────────┬──────────┬───────────┬──────────┬─────────┬──────────────┬─────────────────────┬────────────┬────────┐
│ ROWNUM │ ID       │ TYPE      │ CUSTOMER │ PROJECT │ COUNTRY_CODE │ INSTALL_DATE        │ ISSUE_DATE │ STATUS │
├────────┼──────────┼───────────┼──────────┼─────────┼──────────────┼─────────────────────┼────────────┼────────┤
│      1 │ 00000000 │ COMMUNITY │ NONE     │ NONE    │ KR           │ 2026-09-10 10:06:19 │ 20991231   │ VALID  │
└────────┴──────────┴───────────┴──────────┴─────────┴──────────────┴─────────────────────┴────────────┴────────┘
```

#### session list

구문: `session list` {{< neo_since ver="8.0.17" />}}

접속 중인 세션 목록은 `show sessions`로 조회합니다.

```sh
machbase-neo» show sessions;
┌────────┬──────┬───────────┬─────────┬─────────────────────────┬──────┬───────────┬─────────────┐
│ ROWNUM │   ID │ USER_NAME │ USER_ID │ LOGIN_TIME              │ TYPE │ USER_IP   │ MAX_QPX_MEM │
├────────┼──────┼───────────┼─────────┼─────────────────────────┼──────┼───────────┼─────────────┤
│      1 │ 2484 │ SYS       │       1 │ 2026-09-17 17:35:01.139 │ CLI  │ 127.0.0.1 │ 1.1GB       │
└────────┴──────┴───────────┴─────────┴─────────────────────────┴──────┴───────────┴─────────────┘
```

#### session kill

구문: `session kill <ID>` {{< neo_since ver="8.0.17" />}}

#### session stat

구문: `session stat` {{< neo_since ver="8.0.17" />}}

```sh
machbase-neo» session stat;
┌────────┬──────────────────────┬───────┐
│ ROWNUM │ METRIC               │ VALUE │
├────────┼──────────────────────┼───────┤
│      1 │ OPEN CONN            │     1 │
│      2 │ IDLE                 │     1 │
│      3 │ IN USE               │     0 │
│      4 │ MAX IDLE CLOSED      │   268 │
│      5 │ MAX IDLE TIME CLOSED │   410 │
│      6 │ MAX LIFETIME CLOSED  │   852 │
│      7 │ WAIT COUNT           │     0 │
│      8 │ WAIT DURATION (AVG)  │    0s │
└────────┴──────────────────────┴───────┘
```

#### desc

구문: `desc [-a] <table>`

테이블 구조를 확인합니다.

```sh
machbase-neo» desc example;
┌────────┬────────┬──────────┬────────┬────────────┬───────┐
│ ROWNUM │ COLUMN │ TYPE     │ LENGTH │ FLAG       │ INDEX │
├────────┼────────┼──────────┼────────┼────────────┼───────┤
│      1 │ NAME   │ varchar  │     20 │ tag name   │       │
│      2 │ TIME   │ datetime │     31 │ base time  │       │
│      3 │ VALUE  │ double   │     17 │ summarized │       │
└────────┴────────┴──────────┴────────┴────────────┴───────┘
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
