---
title: SQL 파일 실행
type: docs
weight: 20
---

`machbase-neo shell run <file>` 명령은 지정한 파일에 있는 여러 명령을 순차적으로 실행합니다.

## 스크립트 파일 작성

아래와 같은 예제 스크립트 파일을 작성합니다.

- `cat batch.sh`

```sql
#
# comments starts with `#` or `--`
# A statement should be ends with semi-colon `;`
#

-- Count 1
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos';

-- Count 2
SELECT count(*) FROM EXAMPLE 
  WHERE name = 'wave.sin'
;
```

## 스크립트 파일 실행

```sh
machbase-neo shell run batch.sh
```

실행 결과

```
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos'
 ROWNUM  COUNT(*)
──────────────────
      1  2175
a row fetched.

SELECT count(*) FROM EXAMPLE WHERE name = 'wave.sin'
 ROWNUM  COUNT(*)
──────────────────
      1  8175
a row fetched.
```

## 인터랙티브 모드에서 실행

```sh
$ machbase-neo shell

machbase-neo» run ./b.sh;
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos'
╭────────┬──────────╮
│ ROWNUM │ COUNT(*) │
├────────┼──────────┤
│      1 │ 2175     │
╰────────┴──────────╯
a row fetched.

SELECT count(*) FROM EXAMPLE WHERE name = 'wave.sin'
╭────────┬──────────╮
│ ROWNUM │ COUNT(*) │
├────────┼──────────┤
│      1 │ 8175     │
╰────────┴──────────╯
a row fetched.
```

## 실행 가능한 스크립트 만들기

스크립트 파일의 첫 줄에 shebang(`#!`)을 추가합니다.

```sql
#!/usr/bin/env /path/to/machbase-neo shell run

-- Count 1
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos';

-- Count 2
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.sin';
```

이후 `chmod`로 실행 권한을 부여합니다.

```sh
$ chmod +x batch.sh
```

스크립트를 실행합니다.

```sh
$ ./batch.sh

SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos'
 ROWNUM  COUNT(*)
──────────────────
      1  2175
a row fetched.

SELECT count(*) FROM EXAMPLE WHERE name = 'wave.sin'
 ROWNUM  COUNT(*)
──────────────────
      1  8175
a row fetched.
```
