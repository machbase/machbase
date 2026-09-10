---
toc: true
title: SQLファイルの実行
type: docs
weight: 20
---

`machbase-neo shell run <file>`コマンドは、指定したファイル内の複数のコマンドを順に実行します。

## スクリプトファイルの作成 {#스크립트-파일-작성}

以下のようなサンプルのスクリプトファイルを作成します。

- `cat batch.sh`

```sql
#
# コメントは `#` または `--` で始めます。
# 文の末尾にセミコロン `;` を付けます。
#

-- Count 1
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos';

-- Count 2
SELECT count(*) FROM EXAMPLE 
  WHERE name = 'wave.sin'
;
```

## スクリプトファイルの実行 {#스크립트-파일-실행}

```sh
machbase-neo shell run batch.sh
```

実行結果

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

## 対話モードでの実行 {#인터랙티브-모드에서-실행}

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

## 実行可能なスクリプトの作成 {#실행-가능한-스크립트-만들기}

スクリプトファイルの先頭行にshebang（`#!`）を追加します。

```sql
#!/usr/bin/env /path/to/machbase-neo shell run

-- Count 1
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos';

-- Count 2
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.sin';
```

次に、`chmod`で実行権限を付与します。

```sh
$ chmod +x batch.sh
```

スクリプトを実行します。

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
