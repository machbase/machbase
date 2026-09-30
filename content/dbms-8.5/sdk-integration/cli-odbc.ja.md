---
title : 'CLI/ODBC'
type : docs
weight: 10
toc: true
---

CLI は、[ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)/[IEC](https://en.wikipedia.org/wiki/International_Electrotechnical_Commission) 9075-3:2003 で定義されたソフトウェア開発標準です。

CLI は、SQL をデータベースへ渡し、結果を受け取って解析する方法について、関数と仕様を定義します。CLI は 1990 年代初頭に C と COBOL 専用に開発され、その仕様は現在まで維持されています。

現在最も広く知られている標準インターフェースは ODBC（Open Database Connectivity）で、クライアントプログラムがデータベースの種類に関係なく接続する方法を提供します。現在の ODBC API の最新バージョンは 3.52 で、ISO と X/Open の標準で定義されています。


## 標準 CLI 関数 {#standard-cli-functions}

標準関数の使い方は、次のリンクを参照してください。

* [Wikipedia](https://en.wikipedia.org/wiki/Call_Level_Interface)
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

CLI で接続するには接続文字列を作成します。各項目は次のとおりです。

| 接続文字列の項目 | 説明 |
|--|--|
|DSN|データソース名を指定します。<br>ODBC ではリソースを含むファイルのセクション名、CLI ではサーバー名または IP アドレスを指定します。|
|DBNAME|Machbase の DB 名。|
|SERVER|Machbase が動作するサーバーのホスト名または IP アドレス。|
|NLS_USE|互いに使用する言語の種類を設定します。現在は未使用で、将来の拡張用に残しています。|
|UID|ユーザー ID|
|PWD|パスワード|
|PORT_NO|接続先のポート番号|
|PORT_DIR|Unix で Unix ドメインソケットを使って接続する場合のファイルパス。<br>サーバー側で変更した場合に指定し、既定では指定しなくても動作します。|
|CONNTYPE|クライアントとサーバーの接続方法。<br>1：TCP/IP INET で接続<br>2：Unix ドメインで接続|
|COMPRESS|Append プロトコルを圧縮するかどうか。<br>0 の場合は圧縮せずに送信します。<br>0 より大きい値を指定すると、Append レコードがその値より大きい場合にのみ圧縮します。<br>例：COMPRESS=512<br>レコードサイズが 512 より大きい場合にのみ圧縮します。<br>リモート接続では、圧縮により転送性能が向上します。|
|SHOW_HIDDEN_COLS|`select *` の実行時に隠し列（`_arrival_time`）を表示するかどうか。<br>0 は非表示、1 は該当列を出力します。|
|CONNECTION_TIMEOUT|初回接続時の待機時間。<br>既定値は 30 秒です。<br>初回接続時のサーバー応答が 30 秒より遅くなる可能性がある場合は、この値を大きくします。<br>0 はタイムアウトの制限がないことを意味し、接続に失敗しても無期限に待機するため、できるだけ使用を避けてください。|
|SOCKET_TIMEOUT|プロトコル I/O に時間がかかった場合に発生するタイムアウト。<br>クライアントで確認し、待機した後に切断します。<br>ORACLE の Read Timeout に相当します（MYSQL と MSSQL でも同じ SOCKET_TIMEOUT という名前を使用します）。<br>接続文字列で SOCKET_TIMEOUT=NN（秒）と指定し、既定値は 30 分（1800）です。|
|ALTERNATIVE_SERVERS|クラスター版で、複数の Broker の情報を追加で保持する設定。<br>複数の Broker を登録しておくと、接続中の Broker が停止しても別の Broker に接続し、入力中のデータを引き続き入力します。<br>複数の Broker を登録でき、<サーバーアドレス>:<サーバーポート> の値をカンマで区切って記述します。<br>例：ALTERNATIVE_SERVERS=192.168.0.10:20320,192.168.0.11:20320;|
|AUTH_MODE|認証方式。パスワード認証は `PASSWORD`、秘密鍵によるチャレンジ認証は `CHALLENGE` を使用します。`AUTH_KEY_FILE` だけを指定して `AUTH_MODE` を省略すると、CLI は `CHALLENGE` として扱います。|
|AUTH_SIG_SCHEME|`AUTH_MODE=CHALLENGE` で使用する署名方式。`ECDSA`、`RSA_PKCS1_V15`、`RSA_PSS` を指定できます。省略すると、鍵ファイルから既定の方式を推定します。|
|AUTH_KEY_FILE|`AUTH_MODE=CHALLENGE` で使用する、ローカルの PEM 秘密鍵ファイルのパス。チャレンジ認証では必須です。|

CLI 接続の例を示します。

```c
sprintf(connStr,"SERVER=127.0.0.1;COMPRESS=512;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);
 
if (SQL_ERROR == SQLDriverConnect( gCon, NULL, (SQLCHAR *)connStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT )) {
   ...
}
```


## 拡張 CLI 関数（APPEND） {#extension-cli-function-append}

拡張 CLI 関数は、Machbase サーバーへデータを高速に入力するために提供される Append プロトコルを実装する関数です。

チャネルのオープン、チャネルへのデータ入力、チャネルのフラッシュ、チャネルのクローズの 4 種類の関数で構成されます。

### Append プロトコルの動作 {#understanding-append-protocol}

Machbase の Append プロトコルは非同期で動作します。非同期とは、クライアントがサーバーに要求した処理の応答が要求と完全には同期せず、任意のイベントが発生した時点で届くことを意味します。つまり、クライアントが Append を実行しても、その結果をすぐに取得したり確認したりできず、サーバーの準備が整った任意の時点で確認できます。そのため、Append プロトコルを使ってアプリケーションを開発する場合は、次の内部動作を理解する必要があります。以下では、サーバーで発生した非同期エラーを、クライアントがいつ、どのように検出してユーザーに返すかを説明します。

### データの転送 {#append-data-transfer}

SQLExecute() や SQLExecDirect() などの通常の呼び出しでは、Machbase は結果を直ちにクライアントへ返す同期方式を使用します。一方、SQLAppendDataV2() は、ユーザーデータが入力された直後には要求を送信しません。クライアントの通信バッファーが満杯になるまで待ち、満杯になるとデータをまとめてサーバーへ送信します。これは、Append を使うクライアントが毎秒数万～数十万件のレコードを入力することを想定し、高速に転送するためにバッファリングを利用する設計です。そのため、任意のタイミングでバッファーの内容を送信したい場合は、SQLAppendFlush() を呼び出して明示的にデータを入力できます。

### データのエラーチェック {#append-data-error-check}

前述のとおり、Append プロトコルはバッファリングされ、非同期で動作します。特に、サーバーでエラーが発生しなければ応答を受け取らず、エラーが発生した場合にのみ検出する方式のため、エラーがいつ、どのように検出されるかを理解することが非常に重要です。また、エラーの検出には比較的大きなコストがかかり、レコードを入力するたびに確認するのは非効率なため、現在の Machbase は次の場合にのみ明示的にエラーを検出します。エラーを検出すると、ユーザーが設定したエラーコールバック関数を毎回呼び出します。

1. 送信バッファーが満杯になり、サーバーへ明示的にデータを送信した後に確認
2. SQLAppendFlush() の内部でサーバーへ明示的にデータを送信した後に確認
3. SQLAppendClose() の内部で終了する直前に確認

つまり、基本的には上記の 3 つの場合にのみエラーを検出し、I/O の発生を最小限に抑える設計です。

### サーバーエラー確認の追加設定 {#additional-options-for-checking-server-errors}

性能を最大限に確保するための既定のエラー検出方式は、必要に応じてより頻繁に確認するよう変更できます。SQLAppendOpen() の最後の引数 aErrorCheckCount を調整します。この値が 0 の場合は追加の確認を行わず、既定の方式で動作します。0 より大きい場合は、SQLAppendData() をその回数だけ呼び出すたびに明示的にエラーを確認します。例えば 10 の場合は、Append を 10 回実行するたびにエラー確認のコストが発生します。値が小さいほどエラー検出にシステムリソースを多く使用するため、適切な値に調整してください。

### サーバーエラーのトレースログ {#leaving-trace-log-when-server-error-occurs}

エラーになった Append データについてトレースログを残すには、サーバーのプロパティ DUMP_APPEND_ERROR を 1 に設定します。この設定により、エラーの原因となったレコードの詳細が mach.trc ファイルに記録されます。ただし、エラーが過度に発生するとシステムリソースの使用量が急増し、Machbase 全体の性能が低下する可能性があるため、注意して使用してください。

### APPEND 関数 {#append-function-description}

#### SQLAppendOpen {#sqlappendopen}

```c
SQLRETURN SQLAppendOpen(SQLHSTMT   aStatementHandle,
                        SQLCHAR   *aTableName,
                        SQLINTEGER aErrorCheckCount );
```

対象テーブルへのチャネルを開きます。チャネルを閉じるまで、開いた状態が続きます。

1 つの接続に最大 1024 個のステートメントを設定できます。ステートメントごとに SQLAppendOpen を使用します。

1. aStatementHandle：Append を実行するステートメントのハンドル。
2. aTableName：Append を実行する対象テーブルの名前。
3. aErrorCheckCount：何件のデータを入力するごとにサーバーのエラーを確認するかを指定します。0 の場合は追加のエラー確認を行いません。

#### SQLAppendData（非推奨） {#sqlappenddata-deprecated}

```c
SQLRETURN  SQLAppendData(SQLHSTMT StatementHandle, void *aData[]);
```

チャネルへデータを入力する関数です。

* aData は、入力データへのポインターを格納した配列です。要素数は、オープン時に指定したテーブルの列数と一致させる必要があります。
* 戻り値は SQL_SUCCESS、SQL_SUCCESS_WITH_INFO、SQL_ERROR のいずれかです。特に SQL_SUCCESS_WITH_INFO が返された場合は、入力した列が長すぎて切り詰められたなどの問題がある可能性があるため、結果を再確認してください。

**データ型ごとの設定**

数値型と文字列型

* float、double、short、int、long long、char * などの型は、値へのポインターを設定するだけで動作します。

アドレス型

* IPv4 は、5 バイトの unsigned char 配列で渡します。
* 最初のバイトは 4、続く 4 バイトは連続するアドレス値に設定します。
* 例えば 127.0.0.1 の場合は、5 バイトの配列 **0x04、0x7f、0x00、0x00、0x01** の順に格納します。

```c
// For tables with four column information (short (16), int (32), long (64), varchar)
 
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

* Machbase は内部でナノ秒単位の時刻分解能を持つため、クライアントで時刻を設定する際は変換が必要で、値は 64 ビット符号なし整数で表します。適切に変換するには、UNIX のライブラリー関数 mktime で秒に変換してから、秒未満の値を加えます。
* ※ Machbase の時刻 =（1970 年 1 月 1 日からの総秒数）× 1,000,000,000 + ミリ秒 × 1,000,000 + マイクロ秒 × 1000 + ナノ秒

```c
// Code for a date string in the form "Year-Month-Day Hour:Minute:Second Milli:Micro:Nano"
 
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

#### SQLAppendDataByTime（非推奨） {#sqlappenddatabytimedeprecated}

```c
SQLRETURN  SQLAppendDataByTime(SQLHSTMT StatementHandle, SQLBIGINT aTime, void *aData[]);
```

チャネルへデータを入力する関数で、DB に保存される `_arrival_time` の値を、現在時刻ではなく特定の時刻に設定できます。

例えば、1 か月前のログファイルにある日時を、その当時の日時のまま入力する場合に使用します。

* aTime は、`_arrival_time` に設定する時刻の値です。
* aData は、入力データへのポインターを格納した配列です。
* 配列の要素数は、オープン時に指定したテーブルの列数と一致させる必要があります。

その他は SQLAppendData() を参照してください。

```c
// For tables with four column information (short (16), int (32), long (64), varchar)
 
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

#### SQLAppendDataV2 {#sqlappenddatav2}

```c
SQLRETURN  SQLAppendDataV2(SQLHSTMT StatementHandle, SQL_APPEND_PARAM *aData);
```

Machbase 2.0 で導入された Append 関数で、従来の関数で不便だった入力方法を大きく改善しています。

特に、2.0 で追加された TEXT 型と BINARY 型は、SQLAppendDataV2() でのみ入力できます。

* 型ごとに NULL を入力可能
* VARCHAR の入力時に文字列長を指定可能
* IPv4/IPv6 をバイナリーまたは文字列で入力可能
* TEXT 型と BINARY 型のデータ長を指定可能

引数は次のとおりです。

* aData は、SQL_APPEND_PARAM 配列へのポインターです。要素数は、オープン時に指定したテーブルの列数と一致させる必要があります。
* 戻り値は SQL_SUCCESS、SQL_SUCCESS_WITH_INFO、SQL_ERROR のいずれかです。特に SQL_SUCCESS_WITH_INFO が返された場合は、入力した列が長すぎて切り詰められたなどの問題がある可能性があるため、結果を再確認してください。

V2 で使用する SQL_APPEND_PARAM の定義を示します。この定義は machbase_sqlcli.h に含まれています。

```c
typedef struct machbaseAppendVarStruct
{
    unsigned int mLength;
    void *mData;
} machbaseAppendVarStruct;
 
/* for IPv4, IPv6 as bin or string representation */
typedef struct machbaseAppendIPStruct
{
    unsigned char   mLength; /* 0:null, 4:ipv4, 6:ipv6, 255:string representation */
    unsigned char   mAddr[16];
    char           *mAddrString;
} machbaseAppendIPStruct;
 
/* Date time*/
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
    machbaseAppendVarStruct      mVar;     /* for all varying type */
    machbaseAppendVarStruct      mVarchar; /* alias */
    machbaseAppendVarStruct      mText;    /* alias */
    machbaseAppendVarStruct      mJson;    /* alias */
    machbaseAppendVarStruct      mBinary;  /* binary */
    machbaseAppendVarStruct      mBlob;    /* reserved alias */
    machbaseAppendVarStruct      mClob;    /* reserved alias */
    machbaseAppendDateTimeStruct mDateTime;
} machbaseAppendParam;
 
#define SQL_APPEND_PARAM machbaseAppendParam
```

上記のとおり、内部では共用体 machbaseAppendParam が 1 つの引数を保持します。データ型ごとに、データや文字列の長さと値を明示的に指定できます。使用例を示します。

**固定長数値型の入力**

固定長数値型とは、short、ushort、integer、uinteger、long、ulong、float、double です。これらの型は、SQL_APPEND_PARAM の対応するメンバーに値を直接代入して入力します。

| DB 型 | NULL マクロ | SQL_APPEND_PARAM メンバー |
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
// Assume that the Table Schema consists of eight columns, SHORT, USHORT, INTEGER, UINTEGER, LONG, ULONG, FLOAT, and DOUBLE, respectively.
 
void testAppendExampleFunc()
{
    SQL_APPEND_PARAM sParam[8];
 
    /* fixed column */
    sParam[0].mShort = SQL_APPEND_SHORT_NULL;
    sParam[1].mUShort = SQL_APPEND_USHORT_NULL;
    sParam[2].mInteger = SQL_APPEND_INTEGER_NULL;
    sParam[3].mUInteger = SQL_APPEND_UINTEGER_NULL;
    sParam[4].mLong = SQL_APPEND_LONG_NULL;
    sParam[5].mULong = SQL_APPEND_ULONG_NULL;
    sParam[6].mFloat = SQL_APPEND_FLOAT_NULL;
    sParam[7].mDouble = SQL_APPEND_DOUBLE_NULL;
 
    SQLAppendDataV2(Stmt, sParam);
 
    /* FIXED COLUMN Value */
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

DATETIME 型のデータを入力する例です。便利なマクロがいくつか用意されています。

SQL_APPEND_PARAM の mDateTime メンバーを操作します。次のマクロは、mDateTime 構造体の 64 ビット整数 mTime を設定して日時を指定します。

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
|SQL_APPEND_DATETIME_NOW|クライアントの現在時刻を入力します。|
|SQL_APPEND_DATETIME_STRUCT_TM|mDateTime の struct tm 構造体 mTM に値を設定し、その値をデータベースへ入力します。|
|SQL_APPEND_DATETIME_STRING|mDateTime に文字列の値を設定し、データベースへ入力します。<br>mDateStr：実際の日時文字列<br>mFormatStr：日時文字列の書式文字列|
|SQL_APPEND_DATETIME_NULL|日時列に NULL を入力します。|
|任意の 64 ビット値|この値が実際の datetime として入力されます。<br>1970 年 1 月 1 日からの経過時間をナノ秒単位で表す整数です。<br>例えば、この値が 10 億（1,000,000,000）の場合は 1970 年 1 月 1 日 0 時 0 分 1 秒（GMT）を表します。|

DATETIME 列が 1 つあると想定し、各形式で実際の値を入力する例です。

```c
void testAppendDateTimeFunc()
{
    SQL_APPEND_PARAM sParam[1];
    /* NULL Insert */
    sParam[0].mDateTime.mTime   = SQL_APPEND_DATETIME_NULL;
    SQLAppendDataV2(Stmt, sParam);
 
    /* Current Time */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_NOW;
    SQLAppendDataV2(Stmt, sParam);
 
    /* nano second since 1970/01/01 */
    sParam[0].mDateTime.mTime      = 1234;
    SQLAppendDataV2(Stmt, sParam);
 
    /* String format time */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRING;
    sParam[0].mDateTime.mDateStr   = "23/May/2014:17:41:28";
    sParam[0].mDateTime.mFormatStr = "DD/MON/YYYY:HH24:MI:SS";
    SQLAppendDataV2(Stmt, sParam);
 
    /* struct tm based time */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRUCT_TM;
    sParam[0].mDateTime.mTM.tm_year = 2000 - 1900;
    sParam[0].mDateTime.mTM.tm_mon  =  11;
    sParam[0].mDateTime.mTM.tm_mday  = 31;
    SQLAppendDataV2(Stmt, sParam);
}
```

**インターネットアドレス型の入力**

IPv4 型と IPv6 型のデータを入力する例です。こちらも便利なマクロがいくつか用意されています。SQL_APPEND_PARAM の mLength メンバーを操作します。

```c
/* for IPv4, IPv6 as bin or string representation */
typedef struct machbaseAppendIPStruct
{
    unsigned char   mLength; /* 0:null, 4:ipv4, 6:ipv6, 255:string representation */
    unsigned char   mAddr[16];
    char           *mAddrString;
} machbaseAppendIPStruct;
```

| マクロ（mLength に設定） | 説明 |
|--|--|
|SQL_APPEND_IP_NULL|対応する列に NULL を入力|
|SQL_APPEND_IP_IPV4|mAddr に IPv4 を格納|
|SQL_APPEND_IP_IPV6|mAddr に IPv6 を格納|
|SQL_APPEND_IP_STRING|mAddrString にアドレス文字列を格納|

各形式で実際の値を入力する例です。

```c
void testAppendIPFunc()
{
    SQL_APPEND_PARAM sParam[1];
    /* NULL */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_NULL;
    SQLAppendDataV2(Stmt, sParam);
 
    /* Direct array access */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV4;
    sParam[0].mIP.mAddr[0] = 127;
    sParam[0].mIP.mAddr[1] = 0;
    sParam[0].mIP.mAddr[2] = 0;
    sParam[0].mIP.mAddr[3] = 1;
    SQLAppendDataV2(Stmt, sParam);
 
    /* IPv4 from binary */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV4;
    *(in_addr_t *)(sParam[0].mIP.mAddr) = inet_addr("192.168.0.1");
    SQLAppendDataV2(Stmt, sParam);
 
    /* IPv4 : ipv4 from string */
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "203.212.222.111";
    SQLAppendDataV2(Stmt, sParam);
 
    /* IPv4 : ipv4 from invalid string */
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "ip address is not valid";
    SQLAppendDataV2(Stmt, sParam);                           // invalid IP value
 
    /* IPv6 : ipv6 from binary bytes */
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

IP 型を文字列で入力すると、SQLAppendDataV2() の呼び出し後に mLength がアドレスの型に応じて 4 または 6 に変わります。そのため、ループで入力する場合は、SQLAppendDataV2() を呼び出す前に毎回 mLength を SQL_APPEND_IP_STRING に設定してください。

**可変長データ（文字列とバイナリー）の入力**

可変長データ型には VARCHAR、TEXT、BLOB、CLOB があります。従来の関数は VARCHAR のみに対応し、ユーザーが文字列の長さを指定する方法もなかったため、毎回 strlen() で長さを取得する必要がありました。V2 からは可変長データの長さを直接指定できるため、長さが事前にわかっていれば、より高速にデータを入力できます。内部では可変長データ型は 1 つの構造体ですが、開発の便宜のため、データ型ごとにメンバーが用意されています。

```c
typedef struct machbaseAppendVarStruct
{
    unsigned int mLength;
    void *mData;
} machbaseAppendVarStruct;
```

可変長データを入力する場合は、mLength にデータの長さ、mData に元データへのポインターを設定します。mLength がスキーマで定義された長さより大きい場合は、自動的に切り詰めて入力されます。このとき SQLAppendDataV2() は SQL_SUCCESS_WITH_INFO を返し、関連する警告メッセージを内部構造体に設定します。警告メッセージは SQLError() で確認できます。

| DB 型 | NULL マクロ | SQL_APPEND_PARAM メンバー<br>（mVar も使用可能） |
|--|--|--|
|VARCHAR|SQL_APPEND_VARCHAR_NULL|mVarchar|
|TEXT|SQL_APPEND_TEXT_NULL|mText|
|JSON|SQL_APPEND_JSON_NULL|mJson|
|BINARY|SQL_APPEND_BINARY_NULL|mBinary|
|BLOB|SQL_APPEND_BLOB_NULL|mBlob|
|CLOB|SQL_APPEND_CLOB_NULL|mClob|

各形式で実際の値を入力する例です。VARCHAR 列が 1 つあると想定します。

```sql
CREATE TABLE ttt (name VARCHAR(10));
```

```c
void testAppendVarcharFunc()
{
    SQL_APPEND_PARAM sParam[1];
 
    /*  VARCHAR : NULL */
    sParam[0].mVarchar.mLength = SQL_APPEND_VARCHAR_NULL;
    SQLAppendDataV2(Stmt, sParam); /* OK */
 
    /*  VARCHAR : string */
    strcpy(sVarchar, "MY VARCHAR");
    sParam[0].mVarchar.mLength = strlen(sVarchar);
    sParam[0].mVarchar.mData   = sVarchar;
    SQLAppendDataV2(Stmt, sParam); /* OK */
 
    /*  VARCHAR : Truncation! */
    strcpy(sVarchar, "MY VARCHAR9"); /* Truncation! */
    sParam[0].mVarchar.mLength = strlen(sVarchar);
    sParam[0].mVarchar.mData   = sVarchar;
    SQLAppendDataV2(Stmt, sParam);  /* SQL_SUCCESS_WITH_INFO */
}
```

TEXT 型のデータを入力する例です。

```sql
CREATE TABLE ttt (doc TEXT);
```

```c
void testAppendFunc()
{
    SQL_APPEND_PARAM sParam[1];
 
    /*  TEXT : NULL */
    sParam[0].mText.mLength = SQL_APPEND_TEXT_NULL;
    SQLAppendDataV2(Stmt, sParam); /* OK */
 
    /*  TEXT : string */
    strcpy(sText, "This is the sample document for tutorial.");
    sParam[0].mVar.mLength = strlen(sText);
    sParam[0].mVar.mData   = sText;
    SQLAppendDataV2(Stmt, sParam); /* OK */
}
```

#### SQLAppendDataByTimeV2 {#sqlappenddatabytimev2}

```c
SQLRETURN  SQLAppendDataByTimeV2(SQLHSTMT StatementHandle, SQLBIGINT aTime, SQL_APPEND_PARAM  *aData);
```

チャネルへデータを入力する関数で、DB に保存される `_arrival_time` の値を、現在時刻ではなく特定の時刻に設定できます。例えば、1 か月前のログファイルにある日時を、その当時の日時のまま入力する場合に使用します。

* aTime は、`_arrival_time` に設定する時刻の値です。1970 年 1 月 1 日からのナノ秒数を指定します。また、入力値は過去から現在の順に並べる必要があります。
* aData は、入力データへのポインターを格納した配列です。要素数は、オープン時に指定したテーブルの列数と一致させる必要があります。

その他は SQLAppendDataV2() を参照してください。

#### SQLAppendDataV3 と SQLAppendDataByTimeV3 {#sqlappenddatav3-and-sqlappenddatabytimev3}

```c
SQLRETURN SQLAppendDataV3(SQLHSTMT aStmtHandle,
                          SQL_APPEND_PARAM *aData,
                          SQLINTEGER aColCount);

SQLRETURN SQLAppendDataByTimeV3(SQLHSTMT aStmtHandle,
                                SQLBIGINT aTime,
                                SQL_APPEND_PARAM *aData,
                                SQLINTEGER aColCount);
```

V3 は V2 と同じ `SQL_APPEND_PARAM` の値を使用し、`aColCount` を追加で受け取ります。
`SQLAppendOpen` で開いたテーブルのメタデータだけに依存せず、クライアントが渡す値の数を明示する必要がある場合に使用します。

#### SQLAppendBatch と SQLAppendBatchByTime {#sqlappendbatch-and-sqlappendbatchbytime}

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

バッチ Append は、行と列がそろった行セットを 1 回の呼び出しで送信します。`aTypes` は `SQL_APPEND_TYPE_*` の値の配列、`aData` は行の順に並べた `aRowCount * aColCount` 個の値です。JSON 列には `SQL_APPEND_TYPE_JSON` を使用でき、可変長のバイナリーとテキスト用に BLOB/CLOB の型項目も残されています。

#### SQLAppendFlush {#sqlappendflush}

```c
SQLRETURN SQLAppendFlush(SQLHSTMT StatementHandle);
```

現在のチャネルバッファーに蓄積されたデータを、直ちに Machbase サーバーへ送信します。

#### SQLAppendClose {#sqlappendclose}

```c
SQLRETURN SQLAppendClose(SQLHSTMT   aStmtHandle,
                         SQLBIGINT* aSuccessCount,
                         SQLBIGINT* aFailureCount);
```

現在開いているチャネルを閉じます。チャネルが開いていない場合はエラーになります。

* aSuccessCount：Append に成功したレコード数。
* aFailureCount：Append に失敗したレコード数。

#### SQLAppendSetErrorCallback {#sqlappendseterrorcallback}

```c
SQLRETURN SQLAppendSetErrorCallback(SQLHSTMT aStmtHandle, SQLAppendErrorCallback aFunc);
```

SQLAppendOpen() が成功した後、Append でエラーが発生したときに呼び出すコールバック関数を設定します。設定しない場合、サーバーでエラーが発生してもクライアントは無視します。

* aStmtHandle：エラーを確認するステートメントを指定します。
* aFunc：Append の失敗時に呼び出す関数ポインターを指定します。

SQLAppendErrorCallback のプロトタイプは次のとおりです。

```c
typedef void (*SQLAppendErrorCallback)(SQLHSTMT aStmtHandle,
                                     SQLINTEGER aErrorCode,
                                     SQLPOINTER aErrorMessage,
                                         SQLLEN aErrorBufLen,
                                     SQLPOINTER aRowBuf,
                                         SQLLEN aRowBufLen);
```

* aStatementHandle：エラーが発生したステートメントハンドル
* aErrorCode：エラーの原因となった 32 ビットのエラーコード
* aErrorMessage：エラーコードに対応する文字列
* aErrorBufLen：aErrorMessage の長さ
* aRowBuf：エラーの原因となったレコードの詳細を含む文字列
* aRowBufLen：aRowBuf の長さ

**エラーコールバック（dumpError）の使用例**

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
    // Setting Callback.
    assert(SQLAppendSetErrorCallback(m_IStmt, dumpError) == SQL_SUCCESS);
 
    doAppend(sMaxAppend);
 
    if( SQLAppendClose(m_IStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        fprintf(stdout, "SQLAppendClose error\n");
        exit(-1);
    }
}
```

#### SQLSetConnectAppendFlush {#sqlsetconnectappendflush}

```c
SQLRETURN SQL_API SQLSetConnectAppendFlush(SQLHDBC hdbc, SQLINTEGER option)
```

Append で入力したデータは通信バッファーに書き込まれて送信待ちとなり、ユーザーが SQLAppendFlush を呼び出すか、通信バッファーが満杯になるとサーバーへ送信されます。バッファーが満杯でなくても一定間隔で Append データをサーバーへ送信するには、この関数を使用します。この関数は 100 ms ごとに前回の送信時刻と現在時刻の差を計算し、指定時間（未設定の場合は 1 秒）が経過すると通信バッファーの内容をサーバーへ送信します。

パラメーターは次のとおりです。

* hdbc：DB の接続ハンドル。
* option：0 の場合は自動フラッシュを無効にし、0 以外の値の場合は有効にします。

接続されていない hdbc に対して実行するとエラーになります。

#### SQLSetStmtAppendInterval {#sqlsetstmtappendinterval}

```c
SQLRETURN SQL_API SQLSetStmtAppendInterval(SQLHSTMT hstmt, SQLINTEGER fValue)
```

SQLSetConnectAppendFlush で時間ベースのフラッシュを有効にしている場合に、特定のステートメントについて自動フラッシュを無効にしたり、フラッシュ間隔を調整したりするときに使用します。

パラメーターは次のとおりです。

* hstmt：フラッシュ間隔を調整するステートメントハンドル。
* fValue：設定するフラッシュ間隔。**0 の場合はフラッシュせず、単位は ms です**。フラッシュするかどうかを判定するスレッドが 100 ms ごとに実行されるため、100 の倍数で指定します。指定したとおりの時刻に自動フラッシュが実行されるとは限りません。**既定値は 1000 です**。

時間ベースのフラッシュが動作していなくても、この関数の実行は成功します。

**エラーの確認と説明**

Append 関連関数を使用する際のエラーの確認方法と、エラーコードについて説明します。CLI 関数の戻り値が SQL_SUCCESS でない場合は、次のコードでエラーメッセージを確認できます。

```c
SQLINTEGER errNo;
int msgLength;
char sqlState[6];
char errMsg[1024];
 
if (SQL_SUCCESS == SQLError ( env, con, stmt, (SQLCHAR *)sqlState, &errNo,
                              (SQLCHAR *)errMsg, 1024, &msgLength ))
{
    //set five length error code
    printf("ERROR-%05d: %s\n", errNo, errMsg);
}
```

Append 関連関数が返すエラーメッセージは次のとおりです。

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
      <td>SQLAppendOpen を重複して実行した場合に発生します。</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>ストリームプロトコルの終了に失敗しました。</td>
    </tr>
    <tr>
      <td>Failed to read protocol.</td>
      <td>ネットワークの読み取りエラーが発生しました。</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>列メタデータの構造が不正です。</td>
    </tr>
    <tr>
      <td>cannot allocate memory.</td>
      <td>内部バッファーのメモリ確保でエラーが発生しました。</td>
    </tr>
    <tr>
      <td>cannot allocate compress memory.</td>
      <td>圧縮バッファーのメモリ確保でエラーが発生しました。</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>戻り値にエラーがあります。</td>
    </tr>
    <tr>
      <td rowspan="3">SQLAppendData</td>
      <td>statement is not opened.</td>
      <td>AppendOpen を実行せずに AppendData を呼び出しました。</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>VARCHAR 型の列に、指定サイズより大きいデータを入力した場合に発生します。</td>
    </tr>
    <tr>
      <td>Failed to add binary.</td>
      <td>通信バッファーへの書き込みエラーが発生しました。</td>
    </tr>
    <tr>
      <td rowspan="5">SQLAppendClose</td>
      <td>statement is not opened.</td>
      <td>AppendOpen の状態ではありません。</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>ストリームプロトコルの終了に失敗しました。</td>
    </tr>
    <tr>
      <td>Failed to close buffer protocol.</td>
      <td>バッファープロトコルの終了に失敗しました。</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>列メタデータの構造が不正です。</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>戻り値にエラーがあります。</td>
    </tr>
    <tr>
      <td rowspan="2">SQLAppendFlush</td>
      <td>statement is not opened.</td>
      <td>AppendOpen の状態ではありません。</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>ネットワークの書き込みエラーが発生しました。</td>
    </tr>
    <tr>
      <td rowspan="2">SQLSetErrorCallback</td>
      <td>statement is not opened.</td>
      <td>AppendOpen の状態ではありません。</td>
    </tr>
    <tr>
      <td>Protocol Error (not APPEND_DATA_PROTOCOL)</td>
      <td>通信バッファーから読み取った値が APPEND_DATA_PROTOCOL ではありません。</td>
    </tr>
    <tr>
      <td rowspan="8">SQLAppendDataV2</td>
      <td>Invalid date format or date string.</td>
      <td>日時の形式が不正な場合に発生します。</td>
    </tr>
    <tr>
      <td>statement is not opened.</td>
      <td>AppendOpen の状態ではありません。</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>BINARY 型の列に、指定サイズより大きいデータを入力した場合に発生します。</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>VARCHAR 型または TEXT 型の列に、指定サイズより大きいデータを入力した場合に発生します。</td>
    </tr>
    <tr>
      <td>Failed to add stream.</td>
      <td>通信バッファーへの書き込みエラーが発生しました。</td>
    </tr>
    <tr>
      <td>IP address length is invalid.</td>
      <td>IPv4/IPv6 型の構造体に指定した mLength の値が不正です。</td>
    </tr>
    <tr>
      <td>IP string is invalid.</td>
      <td>IPv4 または IPv6 の形式ではありません。</td>
    </tr>
    <tr>
      <td>Unknown data type has been specified.</td>
      <td>Machbase で使用するデータ型ではありません。</td>
    </tr>
  </tbody>
</table>

## 列単位のパラメーターバインド {#column-wise-parameter-binding}

大量のデータを Machbase へ高速に入力する SQLAppend 関数は、Log テーブルと Tag テーブルへの入力にのみ使用でき、Lookup テーブルや Volatile テーブルの一括更新には使用できません。

この用途のため、Machbase 5.5 以降では列単位のパラメーターバインドをサポートします（行単位のパラメーターバインドは未サポートです）。

SQLSetStmtAttr() の引数 Attribute に SQL_ATTR_PARAM_BIND_TYPE を、引数 param に SQL_PARAM_BIND_BY_COLUMN を設定します。バインドする列ごとにパラメーターを配列で用意し、インジケーター変数も配列で用意します。その後、これらのパラメーターを渡して SQLBindParameter() を呼び出します。

パラメーター配列ごとに列単位のバインドがどのように動作するかを、次の図に示します。

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
      <td>インジケーター/<br>長さの配列</td>
      <td>Value_Array</td>
      <td>インジケーター/<br>長さの配列</td>
      <td>Value_Array</td>
      <td>インジケーター/<br>長さの配列</td>
    </tr>
  </tbody>
</table>

列単位のパラメーターバインドを使用して、大量のデータを挿入する例です。

```c
#define DESC_LEN 51
#define ARRAY_SIZE 10
SQLCHAR * Statement = "INSERT INTO Parts (PartID, Description, Price) VALUES (?, ?, ?)";
 
/* Array of parameters to bind */
SQLUINTEGER PartIDArray[ARRAY_SIZE];
SQLCHAR DescArray[ARRAY_SIZE][DESC_LEN];
SQLREAL PriceArray[ARRAY_SIZE];
/* Array of indicator variables to bind */
SQLINTEGER PartIDIndArray[ARRAY_SIZE], DescLenOrIndArray[ARRAY_SIZE], PriceIndArray[ARRAY_SIZE];
SQLUSMALLINT i, ParamStatusArray[ARRAY_SIZE];
SQLUINTEGER ParamsProcessed;
 
// Set the SQL_ATTR_PARAM_BIND_TYPE statement attribute to use
// column-wise binding.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_BIND_TYPE, SQL_PARAM_BIND_BY_COLUMN, 0);
// Specify the number of elements in each parameter array.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMSET_SIZE, ARRAY_SIZE, 0);
// Specify an array in which to return the status of each set of
// parameters.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_STATUS_PTR, ParamStatusArray, 0);
// Specify an SQLUINTEGER value in which to return the number of sets of
// parameters processed.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMS_PROCESSED_PTR, &ParamsProcessed, 0);
// Bind the parameters in column-wise fashion.
SQLBindParameter(hstmt, 1, SQL_PARAM_INPUT, SQL_C_ULONG, SQL_INTEGER, 5, 0,
    PartIDArray, 0, PartIDIndArray);
SQLBindParameter(hstmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, DESC_LEN - 1, 0,
    DescArray, DESC_LEN, DescLenOrIndArray);
SQLBindParameter(hstmt, 3, SQL_PARAM_INPUT, SQL_C_FLOAT, SQL_REAL, 7, 0,
    PriceArray, 0, PriceIndArray);
```

## 文字列の対応 {#supported-strings}

Machbase は、既定で文字列データを UTF-8 で保存します。

UTF-8 以外の方式で文字列を入出力する Windows では、ODBC が次のように変換します。

| OS | Unicode/非 Unicode | 文字列変換 | 備考 |
|--|--|--|--|
|Windows|Unicode（UTF-16）|UTF-16 ⟷ UTF-8|なし|
|Windows|非 Unicode（MBCS）|MBCS ⟷ UTF-8|Windows の設定にある、非 Unicode アプリケーションの既定の文字コードを使用|
|Linux|UTF-8|なし|UTF-8 のみ対応|
