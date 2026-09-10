---
title : 'CLI/ODBC'
type : docs
weight: 10
toc: true
---

CLI は、[ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)/[IEC](https://en.wikipedia.org/wiki/International_Electrotechnical_Commission) 9075-3:2003 で定義されたソフトウェア開発標準です。

SQL をデータベースへ渡し、結果を受け取って処理する関数と仕様を定義します。1990 年代初頭に C と COBOL 向けに開発され、仕様が維持されています。

広く使われる標準インターフェースに ODBC（Open Database Connectivity）があり、クライアントが DB の種類に依存せず接続できます。本リファレンスは、ISO と X/Open で定義された ODBC API 3.52 を説明します。


## 標準 CLI 関数 {#standard-cli-functions}

標準関数の使い方は、次を参照してください。
* [Wikipedia](http://en.wikipedia.org/wiki/Call_Level_Interface)
* [Open Group のドキュメント](https://www2.opengroup.org/ogsys/catalog/c451)

次の関数を参照できます。

| | | | |
|--|--|--|--|
|SQLAllocConnect|SQLDisconnect|SQLGetDescField|SQLPrepare|
|SQLAllocEnv|SQLDriverConnect|SQLGetDescRec|SQLPrimaryKeys|
|SQLAllocHandle|SQLExecDirect|SQLGetDiagRec|SQLStatistics|
|SQLAllocStmt|SQLExecute|SQLGetEnvAttr|SQLRowCount|
|SQLBindCol|SQLFetch|SQLGetFunctions|SQLSetConnectAttr|
|SQLBindParameter+|SQLFreeConnect|SQLGetInfo|SQLSetDescField|
|SQLColAttribute|SQLFreeEnv|SQLGetStmtAttr|SQLSetDescRec|
|SQLColumns|SQLFreeHandle|SQLGetTypeInfo|SQLSetEnvAttr|
|SQLConnect|SQLFreeStmt|SQLNativeSQL|SQLSetStmtAttr|
|SQLCopyDesc|SQLGetConnectAttr|SQLNumParams|SQLStatistics|
|SQLDescribeCol|SQLGetData|SQLNumResultCols|SQLTables|


## 接続文字列 {#connection-string-for-connecting}

CLI 接続には、次の項目で接続文字列を作成します。

| 接続文字列の項目 | 説明 |
|--|--|
|DSN|データソース名。ODBC ではリソース設定ファイルのセクション名、CLI ではサーバー名または IP アドレス。|
|DBNAME|Machbase の DB 名。|
|SERVER|サーバーのホスト名または IP アドレス。|
|NLS_USE|使用言語の設定。現在は未使用で、将来の拡張用。|
|UID|ユーザー ID|
|PWD|パスワード|
|PORT_NO|接続ポート|
|PORT_DIR|Unix ドメインソケットのファイルパス。サーバーで既定値を変更した場合に指定。既定では省略可能。|
|CONNTYPE|接続方法。<br>1：TCP/IP INET<br>2：Unix ドメイン|
|COMPRESS|Append プロトコルの圧縮。<br>0 は圧縮なし。正の値を指定すると、レコードサイズがその値を超える場合のみ圧縮。<br>例：COMPRESS=512 は 512 を超えるレコードを圧縮。リモート接続の転送性能を改善。|
|SHOW_HIDDEN_COLS|SELECT * で隠し列 `_arrival_time` を表示するか。0 は非表示、1 は表示。|
|CONNECTION_TIMEOUT|初回接続の待ち時間。既定は 30 秒。初回のサーバー応答に30秒以上かかる場合は増やす。0は無制限で、接続に失敗しても無期限に待機するため、できるだけ使用を避けてください。|
|SOCKET_TIMEOUT|プロトコル I/O のタイムアウト。指定時間待ってから切断する。ORACLE の Read Timeout、MySQL/MSSQL の SOCKET_TIMEOUT に相当。SOCKET_TIMEOUT=NN（秒）で指定し、既定値は 1800（30 分）。|
|ALTERNATIVE_SERVERS|クラスタで代替 Broker を登録。接続中の Broker が終了しても、別の Broker に接続して入力を継続する。複数のアドレス:ポートをカンマで区切る。<br>例：ALTERNATIVE_SERVERS=192.168.0.10:20320,192.168.0.11:20320;|
|`AUTH_MODE`|`PASSWORD` はパスワード認証、`CHALLENGE` は秘密鍵によるチャレンジ認証。`AUTH_KEY_FILE` があり `AUTH_MODE` が省略されると `CHALLENGE` として扱う。|
|AUTH_SIG_SCHEME|`CHALLENGE` の署名方式：`ECDSA`、`RSA_PKCS1_V15`、`RSA_PSS`。省略時は鍵ファイルから既定方式の推論を試みる。|
|`AUTH_KEY_FILE`|`CHALLENGE` に必要な、ローカルの PEM 秘密鍵ファイル。|

CLI 接続の例を示します。

```c
sprintf(connStr,"SERVER=127.0.0.1;COMPRESS=512;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);
 
if (SQL_ERROR == SQLDriverConnect( gCon, NULL, (SQLCHAR *)connStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT )) {
   ...
}
```


## 拡張 CLI 関数（APPEND） {#extension-cli-function-append}

拡張 CLI 関数は、サーバーへデータを高速入力する Append プロトコルを実装します。

チャネルの開始、入力、フラッシュ、終了の 4 操作から構成されます。

### Append プロトコルの動作 {#understanding-append-protocol}

Append は非同期で動作します。クライアントの要求とサーバーの応答は完全に同期せず、所定のイベント時に結果を確認します。APPEND の直後に結果を確認できるとは限らないため、実装時には内部動作を理解する必要があります。以下では、サーバーで発生する非同期エラーを、クライアントがいつ、どのように検出するか説明します。

### データの転送 {#append-data-transfer}

SQLExecute や SQLExecDirect() は同期処理で直ちに結果を返します。一方 SQLAppendDataV2() は、入力ごとに要求を送信せず、クライアントの通信バッファーが満杯になってからまとめてサーバーに送ります。毎秒数万～数十万件の入力を想定した高速転送のためです。任意のタイミングで送信するには SQLAppendFlush() を呼び出します。

### データのエラーチェック {#append-data-error-check}

Append はバッファリングと非同期処理を使用し、エラーがない場合は応答を返しません。エラーチェックにはコストがあるため、レコードごとには行わず、次の場合に確認します。エラー検出時は、設定されたユーザーのコールバックを呼び出します。
1. 送信バッファーが満杯となり、サーバーへ送信した後。
2. SQLAppendFlush() で明示的に送信した後。
3. SQLAppendClose() で終了する直前。

基本の確認タイミングをこの 3 つに限定し、I/O の発生を最小限に抑えます。

### サーバーエラー確認の追加設定 {#additional-options-for-checking-server-errors}

必要なら、`SQLAppendOpen`() の最後の引数 aErrorCheckCount で、より頻繁に確認できます。0 は追加チェックなしで、基本動作のみです。正の値を指定すると、SQLAppendData() の指定回数ごとに確認します。例えば 10 なら 10 回ごとです。小さい値ほど確認用リソースを消費するため、適切に調整してください。

### サーバーエラーのトレースログ {#leaving-trace-log-when-server-error-occurs}

エラーになったデータを記録するには、サーバーの DUMP_APPEND_ERROR を 1 にします。mach.trc に該当レコードの詳細が記録されます。大量のエラーがあるとリソース使用量が急増し、全体性能が低下する場合があります。

### APPEND 関数 {#append-function-description}

#### `SQLAppendOpen` {#sqlappendopen}

```sql
SQLRETURN SQLAppendOpen(SQLHSTMT   aStatementHandle,
                        SQLCHAR   *aTableName,
                        SQLINTEGER aErrorCheckCount );
```

対象テーブルへのチャネルを開きます。明示的に閉じるまで開いたままです。
1 接続に最大 1024 ステートメントを設定でき、それぞれで `SQLAppendOpen` を使用できます。

1. aStatementHandle：APPEND を実行するステートメントハンドル。
2. aTableName：対象テーブル名。
3. aErrorCheckCount：指定件数ごとのエラーチェック。0 は追加のチェックを行いません。

#### SQLAppendData（非推奨） {#sqlappenddata-deprecated}
`SQLRETURN SQLAppendData(SQLHSTMT StatementHandle, void *aData[]);`

チャネルへデータを入力します。

* `aData` は入力データへのポインター配列です。要素数は、開始時に指定したテーブルの列数と一致させます。
* 戻り値は SQL_SUCCESS、SQL_SUCCESS_WITH_INFO、SQL_ERROR です。<br>
  SQL_SUCCESS_WITH_INFO の場合、長い列の切り詰めなどの警告があるため、詳細を確認してください。

**データ型ごとの設定**

数値型と文字列型
* float、double、short、int、long long、char * は、値へのポインターを渡します。

アドレス型

* 0x04、0x7f、0x00、0x00、0x01 の順に入力します。
* IPv4 は、5 バイトの unsigned char 配列で渡します。
* 最初のバイトは 4、続く 4 バイトはアドレスの値です。
* 127.0.0.1 の場合、**0x04、0x7f、0x00、0x00、0x01** を順に格納します。

```c
// 4 列（short 16、int 32、long 64、varchar）の場合
 
testAppendIPFunc()
{
   short val1 = 0;
   int   val2 = 1;
   long long  val3 = 2;  
   char *val4 = "my string";
   void *valueArray[4];
 
   valueArray[0] = (void *)&val1;
   valueArray[1] = (void *)&val2;
   valueArray[2] = (void *)&val3;
   valueArray[3] = (void *)val4;
 
   SQLAppendData(aStmt, valueArray);
}
```

**データ型ごとの設定**

日時型

* Machbase の内部時刻はナノ秒精度のため、クライアントで 64 ビット符号なし整数に変換します。<br>
  UNIX の mktime で秒に変換してから、秒未満の値を加えます。<br>
  ※ Machbase 時刻 =（1970 年 1 月 1 日からの秒数）× 1,000,000,000 + ミリ秒 × 1,000,000 + マイクロ秒 × 1000 + ナノ秒。

```c
// 日時文字列が「年-月-日 時:分:秒 ミリ:マイクロ:ナノ」の場合
 
testAppendDateStrFunc(char *aDateString)
{
    int yy, int mm, int dd, int hh, int mi, int ss;
    unsigned long t1;
    void *valueArray[5];
    sscanf(aDateString, "%d-%d-%d %d:%d:%d %d:%d:%d",
        &yy, &mm, &dd, &hh, &mi, &ss, &mmm, &uuu, &nnn);
    sTm.tm_year = yy - 1900;
    sTm.tm_mon = mm - 1;
    sTm.tm_mday = dd;
    sTm.tm_hour = hh;
    sTm.tm_min = mi;
    sTm.tm_sec = ss;
    t1 = mktime(&sTm);
    t1 = t1 * 1000000000L;
    t1 = t1 + (mmm*1000000L) + (uuu*1000) + nnn;
 
    valueArray[4] = &t1;
    SQLAppendData(aStmt, valueArray);
}
```

### SQLAppendDataByTime（非推奨） {#sqlappenddatabytimedeprecated}

```c
SQLRETURN  SQLAppendDataByTime(SQLHSTMT StatementHandle, SQLBIGINT aTime, void *aData[]);
```

チャネルへデータを入力し、DB の `_arrival_time` に現在時刻以外の値を指定します。
例えば、1 か月前のログの日時をそのまま入力する場合に使用します。

* aTime：`_arrival_time` に設定する時刻。
* `aData`：入力データへのポインター配列。
* 配列の要素数は、開始時に指定したテーブルの列数と一致させます。

その他は SQLAppendData() を参照してください。

```c
// 4 列（short 16、int 32、long 64、varchar）の場合
 
testAppendFuncWithTime()
{
   long long sTime = 1;
   short val1 = 0;
   int   val2 = 1;
   long long  val3 = 2;  
   char *val4 = "my string";
   void *valueArray[4];
 
   valueArray[0] = (void *)&val1;
   valueArray[1] = (void *)&val2;
   valueArray[2] = (void *)&val3;
   valueArray[3] = (void *)val4;
 
   SQLAppendDataByTime(aStmt, sTime, valueArray);
}
```

### SQLAppendDataV2 {#sqlappenddatav2}

```c
SQLRETURN  SQLAppendDataV2(SQLHSTMT StatementHandle, SQL_APPEND_PARAM *aData);
```

Machbase 2.0 で導入された、従来の入力方法を改善した関数です。
特に 2.0 で追加された TEXT と BINARY の入力には、SQLAppendDataV2() が必要です。

* 各型で NULL を入力可能
* VARCHAR の文字列長を指定可能
* IPv4/IPv6 をバイナリーまたは文字列で入力可能
* TEXT/BINARY の長さを指定可能

引数の構成を示します。

* `aData` は `SQL_APPEND_PARAM` 配列へのポインターです。要素数は、開始時に指定したテーブルの列数と一致させます。
* 戻り値は SQL_SUCCESS、SQL_SUCCESS_WITH_INFO、SQL_ERROR です。SQL_SUCCESS_WITH_INFO は長い列の切り詰めなどを示すため、詳細を確認してください。

machbase_sqlcli.h にある `SQL_APPEND_PARAM` の定義を示します。

```c
typedef struct machbaseAppendVarStruct
{
    unsigned int mLength;
    void *mData;
} machbaseAppendVarStruct;
 
/* IPv4/IPv6 をバイナリーまたは文字列で指定 */
typedef struct machbaseAppendIPStruct
{
    unsigned char   mLength; /* 0：NULL、4：IPv4、6：IPv6、255：文字列 */
    unsigned char   mAddr[16];
    char           *mAddrString;
} machbaseAppendIPStruct;
 
/* 日時*/
typedef struct machbaseAppendDateTimeStruct
{
    long long       mTime;
#if defined(SUPPORT_STRUCT_TM)
    struct tm       mTM;
#endif
    char           *mDateStr;
    char           *mFormatStr;
} machbaseAppendDateTimeStruct;
 
typedef union machbaseAppendParam
{
    short                        mShort;
    unsigned short               mUShort;
    int                          mInteger;
    unsigned int                 mUInteger;
    long long                    mLong;
    unsigned long long           mULong;
    float                        mFloat;
    double                       mDouble;
    machbaseAppendIPStruct       mIP;
    machbaseAppendVarStruct      mVar;     /* すべての可変長型用 */
    machbaseAppendVarStruct      mVarchar; /* 別名 */
    machbaseAppendVarStruct      mText;    /* 別名 */
    machbaseAppendVarStruct      mJson;    /* 別名 */
    machbaseAppendVarStruct      mBinary;  /* バイナリー */
    machbaseAppendVarStruct      mBlob;    /* 予約された別名 */
    machbaseAppendVarStruct      mClob;    /* 予約された別名 */
    machbaseAppendDateTimeStruct mDateTime;
} machbaseAppendParam;
 
#define SQL_APPEND_PARAM machbaseAppendParam
```

machbaseAppendParam は、1 引数を格納する共用体です。各型の値や文字列の長さを明示できます。使用例を示します。

**固定長数値型の入力**

short、ushort、integer、uinteger、long、ulong、float、double は、`SQL_APPEND_PARAM` の対応メンバーに値を直接代入します。

| DB 型 | NULL マクロ | `SQL_APPEND_PARAM` メンバー |
|--|--|--|
|SHORT|SQL_APPEND_SHORT_NULL|mShort|
|USHORT|SQL_APPEND_USHORT_NULL|mUShort|
|INTEGER|SQL_APPEND_INTEGER_NULL|mInteger|
|UINTEGER|SQL_APPEND_UINTEGER_NULL|mUInteger|
|LONG|SQL_APPEND_LONG_NULL|mLong|
|ULONG|SQL_APPEND_ULONG_NULL|mULong|
|FLOAT|SQL_APPEND_FLOAT_NULL|mFloat|
|DOUBLE|SQL_APPEND_DOUBLE_NULL|mDouble|

実際の値を入力する例です。

```c
// SHORT、USHORT、INTEGER、UINTEGER、LONG、ULONG、FLOAT、DOUBLE の 8 列を想定
 
void testAppendExampleFunc()
{
    SQL_APPEND_PARAM sParam[8];
 
    /* 固定長列 */
    sParam[0].mShort = SQL_APPEND_SHORT_NULL;
    sParam[1].mUShort = SQL_APPEND_USHORT_NULL;
    sParam[2].mInteger = SQL_APPEND_INTEGER_NULL;
    sParam[3].mUInteger = SQL_APPEND_UINTEGER_NULL;
    sParam[4].mLong = SQL_APPEND_LONG_NULL;
    sParam[5].mULong = SQL_APPEND_ULONG_NULL;
    sParam[6].mFloat = SQL_APPEND_FLOAT_NULL;
    sParam[7].mDouble = SQL_APPEND_DOUBLE_NULL;
 
    SQLAppendDataV2(Stmt, sParam);
 
    /* 固定長列の値 */
    sParam[0].mShort = 2;
    sParam[1].mUShort = 3;
    sParam[2].mInteger = 4;
    sParam[3].mUInteger = 5;
    sParam[4].mLong = 6;
    sParam[5].mULong = 7;
    sParam[6].mFloat = 8.4;
    sParam[7].mDouble = 10.9;
 
    SQLAppendDataV2(Stmt, sParam);
}
```

**日時型の入力**

DATETIME の入力例です。便利なマクロを利用できます。

`SQL_APPEND_PARAM` の mDateTime を使用します。mDateTime 内の 64 ビット整数 mTime に、次のマクロまたは時刻を指定します。

```c
typedef struct machbaseAppendDateTimeStruct
{
long long       mTime;
#if defined(SUPPORT_STRUCT_TM)
struct tm       mTM;
#endif
char           *mDateStr;
char           *mFormatStr;
} machbaseAppendDateTimeStruct;
```

| マクロ | 説明 |
|--|--|
|SQL_APPEND_DATETIME_NOW|クライアントの現在時刻を入力。|
|SQL_APPEND_DATETIME_STRUCT_TM|mDateTime の struct tm 型 mTM に値を設定して入力。|
|SQL_APPEND_DATETIME_STRING|文字列で日時を入力。<br>mDateStr：日時文字列<br>mFormatStr：その書式文字列|
|SQL_APPEND_DATETIME_NULL|日時列に NULL を入力。|
|任意の 64 ビット値|1970 年 1 月 1 日からのナノ秒数として入力。<br>例：1,000,000,000 は 1970-01-01 00:00:01（GMT）。|

```c

// SHORT、USHORT、INTEGER、UINTEGER、LONG、ULONG、FLOAT、DOUBLE の 8 列を想定
 
void testAppendDateTimeFunc()
{
    SQL_APPEND_PARAM sParam[1];
    /* NULL を入力 */
    sParam[0].mDateTime.mTime   = SQL_APPEND_DATETIME_NULL;
    SQLAppendDataV2(Stmt, sParam);
 
    /* 現在時刻 */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_NOW;
    SQLAppendDataV2(Stmt, sParam);
 
    /* 1970/01/01 からのナノ秒 */
    sParam[0].mDateTime.mTime      = 1234;
    SQLAppendDataV2(Stmt, sParam);
 
    /* 文字列の日時 */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRING;
    sParam[0].mDateTime.mDateStr   = "23/May/2014:17:41:28";
    sParam[0].mDateTime.mFormatStr = "DD/MON/YYYY:HH24:MI:SS";
    SQLAppendDataV2(Stmt, sParam);
 
    /* struct tm の日時 */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRUCT_TM;
    sParam[0].mDateTime.mTM.tm_year = 2000 - 1900;
    sParam[0].mDateTime.mTM.tm_mon  =  11;
    sParam[0].mDateTime.mTM.tm_mday  = 31;
    SQLAppendDataV2(Stmt, sParam);
}
```

**インターネットアドレス型の入力**

IPv4/IPv6 の入力例です。`SQL_APPEND_PARAM` の mLength に指定するマクロを利用できます。

```c
/* IPv4/IPv6 をバイナリーまたは文字列で指定 */
typedef struct machbaseAppendIPStruct
{
unsigned char   mLength; /* 0：NULL、4：IPv4、6：IPv6、255：文字列 */
unsigned char   mAddr[16];
char           *mAddrString;
} machbaseAppendIPStruct;
```

| マクロ（mLength に設定） | 説明 |
|--|--|
|SQL_APPEND_IP_NULL|対応列に NULL を入力|
|SQL_APPEND_IP_IPV4|mAddr に IPv4 を格納|
|SQL_APPEND_IP_IPV6|mAddr に IPv6 を格納|
|SQL_APPEND_IP_STRING|mAddrString にアドレス文字列を格納|

各形式の入力例を示します。

```c
void testAppendIPFunc()
{
SQL_APPEND_PARAM sParam[1];
/* NULL */
sParam[0].mIP.mLength  = SQL_APPEND_IP_NULL;
SQLAppendDataV2(Stmt, sParam);

    /* 配列へ直接アクセス */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV4;
    sParam[0].mIP.mAddr[0] = 127;
    sParam[0].mIP.mAddr[1] = 0;
    sParam[0].mIP.mAddr[2] = 0;
    sParam[0].mIP.mAddr[3] = 1;
    SQLAppendDataV2(Stmt, sParam);
 
    /* バイナリーから IPv4 を設定 */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV4;
    *(in_addr_t *)(sParam[0].mIP.mAddr) = inet_addr("192.168.0.1");
    SQLAppendDataV2(Stmt, sParam);
 
    /* IPv4：文字列 */
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "203.212.222.111";
    SQLAppendDataV2(Stmt, sParam);
 
    /* IPv4：不正な文字列 */
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "ip address is not valid";
    SQLAppendDataV2(Stmt, sParam);                           // 不正な IP 値
 
    /* IPv6：バイト列 */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV6;
    sParam[0].mIP.mAddr[0]  = 127;
    sParam[0].mIP.mAddr[1]  = 127;
    sParam[0].mIP.mAddr[2]  = 127;
    sParam[0].mIP.mAddr[3]  = 127;
    sParam[0].mIP.mAddr[4]  = 127;
    sParam[0].mIP.mAddr[5]  = 127;
    sParam[0].mIP.mAddr[6]  = 127;
    sParam[0].mIP.mAddr[7]  = 127;
    sParam[0].mIP.mAddr[8]  = 127;
    sParam[0].mIP.mAddr[9]  = 127;
    sParam[0].mIP.mAddr[10] = 127;
    sParam[0].mIP.mAddr[11] = 127;
    sParam[0].mIP.mAddr[12] = 127;
    sParam[0].mIP.mAddr[13] = 127;
    sParam[0].mIP.mAddr[14] = 127;
    sParam[0].mIP.mAddr[15] = 127;
    SQLAppendDataV2(Stmt, sParam);
 
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "::127.0.0.1";
    SQLAppendDataV2(Stmt, sParam);
 
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "FFFF:FFFF:1111:2222:3333:4444:7733:2123";
    SQLAppendDataV2(Stmt, sParam);
}
```

IP型を文字列で入力すると、`SQLAppendDataV2()`の後に`mLength`が型に応じて4または6へ変わります。ループで使用する場合は、毎回の`SQLAppendDataV2()`の前に`mLength`を`SQL_APPEND_IP_STRING`に設定してください。

**可変長データ（文字列とバイナリー）の入力**

可変長型には VARCHAR、TEXT、BLOB、CLOB があります。従来の関数は VARCHAR のみで、長さを指定できず、毎回 strlen() が必要でした。V2 では長さを直接指定できるため、既知の場合は高速化できます。内部の構造は共通ですが、使いやすさのため型ごとのメンバーも用意されています。

```c
typedef struct machbaseAppendVarStruct
{
unsigned int mLength;
void *mData;
} machbaseAppendVarStruct;
```

mLength に長さ、mData に元データへのポインターを設定します。定義されたサイズを超える場合は切り詰められ、SQLAppendDataV2() は SQL_SUCCESS_WITH_INFO を返して警告を設定します。SQLError() で詳細を確認できます。

| DB 型 | NULL マクロ | `SQL_APPEND_PARAM` メンバー<br>（mVar も使用可能） |
|--|--|--|
|VARCHAR|SQL_APPEND_VARCHAR_NULL|mVarchar|
|TEXT|SQL_APPEND_TEXT_NULL|mText|
|JSON|SQL_APPEND_JSON_NULL|mJson|
|BINARY|SQL_APPEND_BINARY_NULL|mBinary|
|BLOB|SQL_APPEND_BLOB_NULL|mBlob|
|CLOB|SQL_APPEND_CLOB_NULL|mClob|

VARCHAR 列が 1 つある場合の、各形式の入力例です。

```sql
CREATE TABLE ttt (name VARCHAR(10));
```

```c
void testAppendVarcharFunc()
{
    SQL_APPEND_PARAM sParam[1];
 
    /*  VARCHAR：NULL */
    sParam[0].mVarchar.mLength = SQL_APPEND_VARCHAR_NULL;
    SQLAppendDataV2(Stmt, sParam); /* 正常 */
 
    /*  VARCHAR：文字列 */
    strcpy(sVarchar, "MY VARCHAR");
    sParam[0].mVarchar.mLength = strlen(sVarchar);
    sParam[0].mVarchar.mData   = sVarchar;
    SQLAppendDataV2(Stmt, sParam); /* 正常 */
 
    /*  VARCHAR：切り詰め */
    strcpy(sVarchar, "MY VARCHAR9"); /* 切り詰め */
    sParam[0].mVarchar.mLength = strlen(sVarchar);
    sParam[0].mVarchar.mData   = sVarchar;
    SQLAppendDataV2(Stmt, sParam);  /* SQL_SUCCESS_WITH_INFO */
}
```

TEXT データの入力例です。

```sql
CREATE TABLE ttt (doc TEXT);
```

```cpp
void testAppendFunc()
{
    SQL_APPEND_PARAM sParam[1];
 
    /*  TEXT：NULL */
    sParam[0].mText.mLength = SQL_APPEND_TEXT_NULL;
    SQLAppendDataV2(Stmt, sParam); /* 正常 */
 
    /*  TEXT：文字列 */
    strcpy(sText, "This is the sample document for tutorial.");
    sParam[0].mVar.mLength = strlen(sText);
    sParam[0].mVar.mData   = sText;
    SQLAppendDataV2(Stmt, sParam); /* 正常 */
}
```


### SQLAppendDataByTimeV2 {#sqlappenddatabytimev2}

```sql
SQLRETURN  SQLAppendDataByTimeV2(SQLHSTMT StatementHandle, SQLBIGINT aTime, SQL_APPEND_PARAM  *aData);
```

`_arrival_time` に現在時刻以外の時刻を指定して入力します。例えば、1 か月前のログ日時を保持する場合に使用します。

* aTime：`_arrival_time` に設定する、1970 年 1 月 1 日からのナノ秒数。入力は古い時刻から新しい時刻の順に並べる必要があります。
* `aData`：入力データへのポインター配列。要素数は、開始時に指定したテーブルの列数と一致させます。

その他は SQLAppendDataV2() を参照してください。

### SQLAppendDataV3 と SQLAppendDataByTimeV3 {#sqlappenddatav3-and-sqlappenddatabytimev3}

```c
SQLRETURN SQLAppendDataV3(SQLHSTMT aStmtHandle,
                          SQL_APPEND_PARAM *aData,
                          SQLINTEGER aColCount);

SQLRETURN SQLAppendDataByTimeV3(SQLHSTMT aStmtHandle,
                                SQLBIGINT aTime,
                                SQL_APPEND_PARAM *aData,
                                SQLINTEGER aColCount);
```

V3 は V2 と同じ `SQL_APPEND_PARAM` に加えて `aColCount` を指定します。
`SQLAppendOpen` で取得したテーブルメタデータだけに依存せず、クライアントが渡す値の数を明示する場合に使用します。

### SQLAppendBatch と SQLAppendBatchByTime {#sqlappendbatch-and-sqlappendbatchbytime}

```c
SQLRETURN SQLAppendBatch(SQLHSTMT aStmtHandle,
                         SQLCHAR *aTableName,
                         SQLINTEGER aRowCount,
                         SQLINTEGER aColCount,
                         SQL_APPEND_TYPES *aTypes,
                         SQL_APPEND_PARAM *aData);

SQLRETURN SQLAppendBatchByTime(SQLHSTMT aStmtHandle,
                               SQLCHAR *aTableName,
                               SQLBIGINT aTime,
                               SQLINTEGER aRowCount,
                               SQLINTEGER aColCount,
                               SQL_APPEND_TYPES *aTypes,
                               SQL_APPEND_PARAM *aData);
```

行と列からなるデータを、1 回でまとめて送信します。`aTypes` は `SQL_APPEND_TYPE_*` の配列、`aData` は行順に並べた aRowCount × `aColCount` 個の値です。JSON 列には `SQL_APPEND_TYPE_JSON` を使用でき、可変長のバイナリーとテキスト用に BLOB/CLOB の型項目も用意されています。

### SQLAppendFlush {#sqlappendflush}

```sql
SQLRETURN SQLAppendFlush(SQLHSTMT StatementHandle);
```

現在のチャネルバッファーに蓄積したデータを、直ちにサーバーへ送信します。

### SQLAppendClose {#sqlappendclose}
```sql
SQLRETURN SQLAppendClose(SQLHSTMT   aStmtHandle,
                         SQLBIGINT* aSuccessCount,
                         SQLBIGINT* aFailureCount);
```

開いているチャネルを閉じます。開いていない場合はエラーになります。

* aSuccessCount：APPEND 成功件数。
* aFailureCount：APPEND 失敗件数。

### SQLAppendSetErrorCallback {#sqlappendseterrorcallback}

```sql
SQLRETURN SQLAppendSetErrorCallback(SQLHSTMT aStmtHandle, SQLAppendErrorCallback aFunc);
```

`SQLAppendOpen()`が成功した後、APPENDエラー時に呼び出すコールバックを設定します。未設定の場合、クライアントはサーバー側のエラーを無視します。

* aStmtHandle：エラーを確認するステートメント。
* aFunc：失敗時に呼び出す関数ポインター。

SQLAppendErrorCallback のプロトタイプ：

```c
typedef void (*SQLAppendErrorCallback)(SQLHSTMT aStmtHandle,
                                     SQLINTEGER aErrorCode,
                                     SQLPOINTER aErrorMessage,
                                         SQLLEN aErrorBufLen,
                                     SQLPOINTER aRowBuf,
                                         SQLLEN aRowBufLen);
```

* aStatementHandle：エラーが発生したハンドル。
* aErrorCode：32 ビットのエラーコード。
* aErrorMessage：エラーメッセージ文字列。
* aErrorBufLen：aErrorMessage の長さ。
* aRowBuf：エラーレコードの詳細を含む文字列。
* aRowBufLen：aRowBuf の長さ。

**エラーコールバック dumpError の使用例**

```c
void dumpError(SQLHSTMT    aStmtHandle,
SQLINTEGER  aErrorCode,
SQLPOINTER  aErrorMessage,
SQLLEN      aErrorBufLen,
SQLPOINTER  aRowBuf,
SQLLEN      aRowBufLen)
{
char       sErrMsg[1024] = {0, };
char       sRowMsg[32 * 1024] = {0, };

    if (aErrorMessage != NULL)
    {
        strncpy(sErrMsg, (char *)aErrorMessage, aErrorBufLen);
    }
 
    if (aRowBuf != NULL)
    {
        strncpy(sRowMsg, (char *)aRowBuf, aRowBufLen);
    }
 
    fprintf(stdout, "Append Error : [%d][%s]\n[%s]\n\n", aErrorCode, sErrMsg, sRowMsg);
}


......

    if( SQLAppendOpen(m_IStmt, TableName, aErrorCheckCount) != SQL_SUCCESS )
    {
        fprintf(stdout, "SQLAppendOpen error\n");
        exit(-1);
    }
    // コールバックを設定
    assert(SQLAppendSetErrorCallback(m_IStmt, dumpError) == SQL_SUCCESS);
 
    doAppend(sMaxAppend);
 
    if( SQLAppendClose(m_IStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        fprintf(stdout, "SQLAppendClose error\n");
        exit(-1);
    }
}
```

### SQLSetConnectAppendFlush {#sqlsetconnectappendflush}

```sql
SQLRETURN SQL_API SQLSetConnectAppendFlush(SQLHDBC hdbc, SQLINTEGER option)
```

通常、APPEND データは通信バッファーへ格納され、SQLAppendFlush の呼び出し時または満杯になった時に送信されます。この関数で、満杯でなくても一定間隔で送信できます。100 ms ごとに前回送信からの経過時間を確認し、指定時間（未設定時は 1 秒）を過ぎると送信します。

パラメーター：

* hdbc：DB 接続ハンドル。
* option：0 は自動フラッシュ無効、それ以外は有効。

未接続の hdbc で実行するとエラーになります。

### SQLSetStmtAppendInterval {#sqlsetstmtappendinterval}
```sql
SQLRETURN SQL_API SQLSetStmtAppendInterval(SQLHSTMT hstmt, SQLINTEGER fValue)
```

SQLSetConnectAppendFlush で時間ベースの自動フラッシュを有効にした場合、特定のステートメントの間隔を調整、または無効化します。

パラメーター：

* hstmt：間隔を調整するステートメント。
* fValue：間隔。**単位は ms、0 は無効**です。判定スレッドは 100 ms ごとに動くため、100 の倍数で指定します。指定時刻ぴったりの送信は保証されません。**既定値は 1000** です。

時間ベースのフラッシュが動作していなくても、この設定は成功します。

**エラーの確認と説明**

APPEND 関連関数の戻り値が SQL_SUCCESS でない場合、次のコードでエラーメッセージを確認できます。

```c
SQLINTEGER errNo;
int msgLength;
char sqlState[6];
char errMsg[1024];

if (SQL_SUCCESS == SQLError ( env, con, stmt, (SQLCHAR *)sqlState, &errNo,
(SQLCHAR *)errMsg, 1024, &msgLength ))
{
//長さ 5 のエラーコードを設定
printf("ERROR-%05d: %s\n", errNo, errMsg);
}
```

主なエラーメッセージを示します。

<table>
  <thead>
    <tr>
      <th>関数</th>
      <th>メッセージ</th>
      <th>説明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="7">SQLAppendOpen</td>
      <td>statement is already opened.</td>
      <td>SQLAppendOpen を重複して実行。</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>ストリームプロトコルの終了に失敗。</td>
    </tr>
    <tr>
      <td>Failed to read protocol.</td>
      <td>ネットワーク読み取りエラー。</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>列メタデータの構造が不正。</td>
    </tr>
    <tr>
      <td>cannot allocate memory.</td>
      <td>内部バッファーのメモリ確保に失敗。</td>
    </tr>
    <tr>
      <td>cannot allocate compress memory.</td>
      <td>圧縮バッファーのメモリ確保に失敗。</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>戻り値が不正。</td>
    </tr>
    <tr>
      <td rowspan="3">SQLAppendData</td>
      <td>statement is not opened.</td>
      <td>AppendOpen なしで AppendData を呼び出した。</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>VARCHAR 列の定義サイズを超えるデータを入力。</td>
    </tr>
    <tr>
      <td>Failed to add binary.</td>
      <td>通信バッファーへの書き込みエラー。</td>
    </tr>
    <tr>
      <td rowspan="5">SQLAppendClose</td>
      <td>statement is not opened.</td>
      <td>AppendOpen 状態ではない。</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>ストリームプロトコルの終了に失敗。</td>
    </tr>
    <tr>
      <td>Failed to close buffer protocol.</td>
      <td>バッファープロトコルの終了に失敗。</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>列メタデータの構造が不正。</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>戻り値が不正。</td>
    </tr>
    <tr>
      <td rowspan="2">SQLAppendFlush</td>
      <td>statement is not opened.</td>
      <td>AppendOpen 状態ではない。</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>ネットワーク書き込みエラー。</td>
    </tr>
    <tr>
      <td rowspan="2">SQLSetErrorCallback</td>
      <td>statement is not opened.</td>
      <td>AppendOpen 状態ではない。</td>
    </tr>
    <tr>
      <td>Protocol Error (not APPEND_DATA_PROTOCOL)</td>
      <td>通信バッファーから読み取った値が APPEND_DATA_PROTOCOL ではない。</td>
    </tr>
    <tr>
      <td rowspan="8">SQLAppendDataV2</td>
      <td>Invalid date format or date string.</td>
      <td>日時形式が不正。</td>
    </tr>
    <tr>
      <td>statement is not opened.</td>
      <td>AppendOpen 状態ではない。</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>BINARY 列の定義サイズを超えるデータを入力。</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>VARCHAR または TEXT 列の定義サイズを超えるデータを入力。</td>
    </tr>
    <tr>
      <td>Failed to add stream.</td>
      <td>通信バッファーへの書き込みエラー。</td>
    </tr>
    <tr>
      <td>IP address length is invalid.</td>
      <td>IPv4/IPv6 構造体の mLength が不正。</td>
    </tr>
    <tr>
      <td>IP string is invalid.</td>
      <td>IPv4 または IPv6 の形式ではない。</td>
    </tr>
    <tr>
      <td>Unknown data type has been specified.</td>
      <td>Machbase のデータ型ではない。</td>
    </tr>
  </tbody>
</table>

## 列単位のパラメーターバインド {#column-wise-parameter-binding}

大量データを高速入力する SQLAppend は、Lookup/Volatile テーブルの一括更新には使用できません。SQLAppendによる一括入力の対象はLog/Tagテーブルです。
この用途のため、Machbase 5.5 以降は列単位のパラメーターバインドをサポートします。行単位のバインドは未サポートです。
SQLSetStmtAttr() の Attribute に SQL_ATTR_PARAM_BIND_TYPE、param に SQL_PARAM_BIND_BY_COLUMN を指定します。
列ごとにパラメーター配列とインジケーター配列を用意し、SQLBindParameter() に渡します。
配列ごとの列単位バインドの構成を示します。

<table>
  <thead>
    <tr>
      <th colspan="2">列 A<br>（パラメーター A）</th>
      <th colspan="2">列 B<br>（パラメーター B）</th>
      <th colspan="2">列 C<br>（パラメーター C）</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Value_Array</td>
      <td>インジケーター/<br><br>長さの配列</td>
      <td>Value_Array</td>
      <td>インジケーター/<br><br>長さの配列</td>
      <td>Value_Array</td>
      <td>インジケーター/<br><br>長さの配列</td>
    </tr>
  </tbody>
</table>


```c
#define DESC_LEN 51
#define ARRAY_SIZE 10
SQLCHAR * Statement = "INSERT INTO Parts (PartID, Description, Price) VALUES (?, ?, ?)";
 
/* バインドするパラメーターの配列 */
SQLUINTEGER PartIDArray[ARRAY_SIZE];
SQLCHAR DescArray[ARRAY_SIZE][DESC_LEN];
SQLREAL PriceArray[ARRAY_SIZE];
/* バインドするインジケーターの配列 */
SQLINTEGER PartIDIndArray[ARRAY_SIZE], DescLenOrIndArray[ARRAY_SIZE], PriceIndArray[ARRAY_SIZE];
SQLUSMALLINT i, ParamStatusArray[ARRAY_SIZE];
SQLUINTEGER ParamsProcessed;
 
// SQL_ATTR_PARAM_BIND_TYPE を設定して、
// 列単位のバインドを使用する
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_BIND_TYPE, SQL_PARAM_BIND_BY_COLUMN, 0);
// 各パラメーター配列の要素数を指定
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMSET_SIZE, ARRAY_SIZE, 0);
// 各パラメーターセットの状態を返す
// 配列を指定する
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_STATUS_PTR, ParamStatusArray, 0);
// 処理済みのパラメーターセット数を返す
// SQLUINTEGER 値を指定する
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMS_PROCESSED_PTR, &ParamsProcessed, 0);
// 列単位でパラメーターをバインド
SQLBindParameter(hstmt, 1, SQL_PARAM_INPUT, SQL_C_ULONG, SQL_INTEGER, 5, 0,
    PartIDArray, 0, PartIDIndArray);
SQLBindParameter(hstmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, DESC_LEN - 1, 0,
    DescArray, DESC_LEN, DescLenOrIndArray);
SQLBindParameter(hstmt, 3, SQL_PARAM_INPUT, SQL_C_FLOAT, SQL_REAL, 7, 0,
    PriceArray, 0, PriceIndArray);
```

## 文字列の対応 {#supported-strings}

Machbase は、既定で文字列を UTF-8 で保存します。
Windows で UTF-8 以外の文字列を入出力する場合、ODBC が次のように変換します。

| OS | Unicode/非 Unicode | 文字列変換 | 備考 |
|--|--|--|--|
|Windows|Unicode（UTF-16）|UTF-16 ⟷ UTF-8|なし|
|Windows|非 Unicode（MBCS）|MBCS ⟷ UTF-8|Windows の非 Unicode アプリケーションの既定設定を使用|
|Linux|UTF-8|なし|UTF-8 のみ対応|
