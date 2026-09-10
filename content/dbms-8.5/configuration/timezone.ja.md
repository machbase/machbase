---
layout : post
title : 'タイムゾーン'
type : docs
toc: true
weight: 0
---

## 目次 {#index}

* [Machbase のタイムゾーン](#timezone-of-machbase)
* [タイムゾーンの指定形式](#timezone-format-in-machbase)
    * [machsql](#machsql)
    * [machloader](#machloader)
    * [SDK](#sdk)
    * [REST API](#rest-api)

## Machbase のタイムゾーン {#timezone-of-machbase}

クライアントのタイムゾーンは、それぞれのセッション内でのみ有効です。

一般には、日時文字列にタイムゾーンを付けて指定します。

```
"YYYY-MM-DD HH24:MI:SS ZZZ(Timezone String)"

例）
"12:06:56.568+01:00"
"2006.07.10 at 15:08:56 -05:00"
"09  AM, GMT+09:00"
```

この方式では、日時ごとにタイムゾーンを指定する手間がかかり、大量のデータに含めると転送量もデータ件数に比例して増加します。

そのため Machbase は、クライアントとサーバーの接続セッションにタイムゾーンを設定する方式をサポートします。

タイムゾーンは次のように動作します。

* サーバーは、インストール先 OS の既定のタイムゾーンで動作します。<br>
    明示的な設定がなければ、OS のタイムゾーンを読み取って使用します。

* クライアントがタイムゾーンを指定せずに接続すると、サーバーの設定を引き継ぎます。<br>
    サーバーの TIMEZONE が KST なら、クライアントも KST で動作します。

* クライアントが明示的に指定した場合、そのセッションは指定したタイムゾーンで動作します。<br>
    サーバーが KST でも、クライアントが接続時に EDT を指定すれば、そのセッションは EDT で動作します。

## タイムゾーンの指定形式 {#timezone-format-in-machbase}

指定を簡単にするため、Machbase は 5 文字の単一形式を使用します。

先頭は `+` または `-`、続く 2 桁は時（00 ～ 23）、最後の 2 桁は分（00 ～ 59）です。

サポートする TIMEZONE の形式を示します。

```
例）
TIMEZONE=+0900
TIMEZONE=-0900
```

### machsql {#machsql}
---

起動時に次のオプションでタイムゾーンを指定します。

```
-z, --timezone=+-HHMM
```

現在の設定は SHOW TIMEZONE コマンドで確認できます。

```
SHOW TIMEZONE;

Mach> show timezone;
Timezone : +0900
```

### machloader {#machloader}
---

実行時に次のオプションでタイムゾーンを指定します。

```
-z, --timezone=+-HHMM
```

指定したタイムゾーンで接続し、その設定に基づいて時刻を計算します。

### SDK {#sdk}
---

接続文字列の TIMEZONE で、セッションのタイムゾーンを指定できます。

TIMEZONE を省略した場合は、サーバーのタイムゾーンを使用します。

CLI、ODBC、JDBC、DOTNET で共通です。

接続文字列の例

```
SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;NLS_USE=UTF8;PORT_NO=5656;TIMEZONE=+0300
```

### REST API {#rest-api}
---

REST API は、リクエストの HTTP ヘッダーで指定したタイムゾーンを使用します。

ヘッダー名は The-Timezone-Machbase です。次のように指定します。

```
Authorization: Basic XXXXXXXXXXXXXXXXXXX
...................
The-Timezone-Machbase: +0900
...............
```

上記の形式で、使用するタイムゾーン文字列を指定します。

省略した場合は、サーバーのタイムゾーンを使用します。

リクエストの例：UTC を指定

```bash
curl -H "The-Timezone-Machbase: +0000" -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode 'q=select sysdate from v$tables limit 1'
```

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "sysdate",
      "type": 6,
      "length": 31
    }
  ],
  "timezone": "+0000",
  "data": [
    {
      "sysdate": "2026-06-13 07:58:30 328:941:439"
    }
  ]
}
```

結果の JSON の timezone 項目に、適用されたタイムゾーンが返されます。
