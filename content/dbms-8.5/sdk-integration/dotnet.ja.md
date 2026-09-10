---
title: '.NET コネクター'
type: docs
weight: 20
toc: true
---

## 目次 {#index}

* [概要](#overview)
* [インストール](#install)
* [NuGet（統合版 8.0.54）](#nuget-unified-connector)
* [NuGet（旧 5.x）パッケージマネージャー](#install-connector-via-nuget-package-manager)
* [接続文字列](#connection-string-reference)
* [API リファレンス](#api-reference)
* [使用方法と例](#usage-and-examples)
* [完全版プロバイダー API（4.0-full）](#full-provider-apis-protocol-40-full)

## 概要 {#overview}

Machbase は、サポートする全ワイヤープロトコル（`2.1` ～ `4.0`）をまとめた汎用 ADO.NET プロバイダー `UniMachNetConnector` を提供します。DBMS Standard のソースでは、統合パッケージのバージョンは 8.0.54、対象フレームワークは `net452`、`net5.0`、`net6.0`、`net7.0`、`net8.0` です。接続文字列に基づいて、実行時に適切なプロトコルを選択します。

## インストール {#install}

サーバーとクライアントのインストーラーは、汎用 .NET プロバイダーを `$MACHBASE_HOME/lib/` に配置します。
Standard の Linux パッケージには、例えば .NET 5.0 用の
`UniMachNetConnector-net50-8.0.54.dll` と、プロトコル別の
`machNetConnector-40-net50-3.2.1.dll` が含まれます。対応する .NET SDK があれば、
ソースから他の対象フレームワーク用にもビルドできます。

- **`UniMachNetConnector`**：フレームワークに依存しない入口です。ファイル名は
  `UniMachNetConnector-net{452|50|60|70|80}-<version>.dll` なので、
  配布先のフレームワークに合うものを選びます。
- **旧プロトコルコネクター**：汎用ローダーが必要に応じて読み込む任意のアセンブリーです。
  例：`machNetConnector-XX-net{40|50|60|70|80}-<version>.dll`。

アプリケーションに合う DLL を参照し、配布時にはバイナリーの隣にコピーしてください。

## NuGet によるインストール（統合版 8.0.54） {#nuget-unified-connector}

パッケージ ID は `UniMachNetConnector` です。DLL を個別に配布せずにプロジェクトで管理できるため、新規アプリケーションに推奨します。

- 対象フレームワーク：`net452`、`net5.0`、`net6.0`、`net7.0`、`net8.0`。
- `net5.0` 以降のビルドは自己完結しています。`net452` のビルドは、ソースプロジェクトの指定どおり
  `System.ValueTuple` 4.5.0 を復元します。

### クイックスタート（CLI） {#quick-start-cli}

```bash
# プロジェクトのディレクトリで実行
dotnet add package UniMachNetConnector --version 8.0.54
dotnet build
```

CI、オフライン、社内フィードなどで取得元を制御する場合は、参照を追加してから明示的に restore を実行します。

```bash
dotnet add package UniMachNetConnector --version 8.0.54 --no-restore

# nuget.org だけから復元（新しいメタデータを強制取得）
dotnet nuget locals http-cache --clear
dotnet restore --no-cache --source https://api.nuget.org/v3/index.json
```

### Visual Studio {#visual-studio}

- プロジェクトを右クリック →「NuGet パッケージの管理」→「参照」で `UniMachNetConnector` を検索 → 8.0.54 を選択 → インストールします。

### プロジェクトファイルの例 {#project-file-example}

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.54" />
  <!-- 他のMachbaseパッケージは不要 -->
  <!-- 対象：net452|net5.0|net6.0|net7.0|net8.0 -->
  <!-- アプリに合わせてAnyCPU/x64を維持。Machbaseサーバー側への影響はありません -->
</ItemGroup>
```

### ローカルフィードまたはプライベートフィードの使用 {#using-a-local-or-private-feed-optional}

フォルダーフィードや社内レジストリを使う場合は、それを復元元に指定します。フォルダーフィードでは、`UniMachNetConnector.8.0.54.nupkg` をディレクトリに置き、ソースとして追加します。

```bash
# 初回のみ設定
dotnet nuget add source /path/to/local-nuget -n mach-local

# nuget.org とローカルフィードから復元
dotnet restore --no-cache \
  --source /path/to/local-nuget \
  --source https://api.nuget.org/v3/index.json
```

CI や権限を制限したアカウントでは、パッケージの保存ディレクトリを絶対パスで明示してください。

```bash
PKG_DIR="$(pwd)/.nuget-packages"; mkdir -p "$PKG_DIR"
NUGET_PACKAGES="$PKG_DIR" dotnet restore --no-cache --source /path/to/local-nuget
NUGET_PACKAGES="$PKG_DIR" dotnet run --no-restore
```

> ヒント：`NU1102`（指定バージョンが見つからない）が発生する場合や、8.0.54の公開後も `dotnet add package` が古い版を報告する場合は、HTTP キャッシュを削除し、上記の `--no-cache` を使用します。一時的な incompatible with 'all' frameworks は、実際の TFM 不一致ではなく、復元失敗による場合があります。

### 最小限の使用例 {#minimal-usage-sample}

```csharp
using Mach.Data.MachClient;

var cs = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var conn = new MachConnection(cs);
conn.Open();

using var cmd = new MachCommand("SELECT COUNT(*) FROM V$TABLES", conn);
var count = (long)cmd.ExecuteScalar();
Console.WriteLine($"Tables: {count}");
```

## NuGet（旧 5.x）パッケージマネージャー {#install-connector-via-nuget-package-manager}

> **注意**：Machbase .NET Connector 5.0 も NuGet に登録されています。これは統合版 `UniMachNetConnector` より前の、独立した旧パッケージです。

Visual Studio では旧コネクターも取得できます。以下は `machNetConnector5.0` の導入手順です。統合版より前のコードを対象とする必要がある場合にのみ使用してください。

1. Visual Studio で新しい C# .NET プロジェクトを作成します。
2. ソリューションエクスプローラーでプロジェクトを右クリックし、「NuGet パッケージの管理」を選択します。
3. 左上の「参照」タブで machNet を検索します。
4. `machNetConnector5.0` を選択してインストールします。
5. 変更のプレビューが表示されたら「OK」で続行します。
6. 成功したら、ソリューションエクスプローラーの「依存関係 → パッケージ」で確認できます。
7. `Program.cs`に`using Mach.Data.MachClient;`を追加して利用します。

> 使用する NuGet パッケージの選択
> - 新規開発や更新では `UniMachNetConnector` 8.0.54 を推奨します。`net452` と `net5.0` ～ `net8.0` に対応し、完全版プロバイダー（`4.0-full`）を含む全プロトコルをまとめています。
> - 統合版へまだ移行できない旧アプリケーションに限り、`machNetConnector5.0` を使用します。

## 接続文字列 {#connection-string-reference}

各項目をセミコロン（`;`）で区切ります。同じ行のキーワードは別名です。

| キーワード | 説明 | 例 | 既定値 |
|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|-------------------------------------------------|---------|
| `DSN`, `SERVER`, `HOST` | ホスト名または IP アドレス | `SERVER=127.0.0.1` | なし |
| `PORT`, `PORT_NO` | リスナーポート | `PORT=5656` | `5656` |
| `USERID`, `USERNAME`, `USER`, `UID` | ユーザー名 | `UID=SYS` | `SYS` |
| `PASSWORD`, `PWD` | パスワード | `PWD=manager` | なし |
| `CONNECT_TIMEOUT`, `ConnectionTimeout`, `connectTimeout` | 接続タイムアウト（ms） | `CONNECT_TIMEOUT=10000` | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout`, `commandTimeout` | コマンドごとのタイムアウト（ms） | `COMMAND_TIMEOUT=50000` | `60000` |
| `PROTOCOL`, `ProtocolVersion`, `MachProtocol` | 使用するプロトコル。例：`2.1`、`3.0`、`4.0`、`4.0-full`、`auto`、`auto-full`。`UniMachNetConnector` では省略時に `4.0` を使用。 | `PROTOCOL=auto` | `4.0` |

例：

```csharp
var connectionString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;COMMAND_TIMEOUT=50000;PROTOCOL=4.0-full",
    host,
    port);
```

### プロトコルの自動検出（`PROTOCOL=auto`） {#protocol-auto-detection-protocolauto}

複数の Machbase バージョンに接続する場合は、`PROTOCOL=auto` で実行時にハンドシェイクを選択できます。次のように動作します。

- `auto` は、指定されたホスト、ポート、ユーザー、パスワード、データベース、`CONNECT_TIMEOUT` を使い、`4.0`、`3.0`、2.2、`2.1` の順に試します。
- `auto-full` も同様ですが、サーバーが `4.0` を返した場合は、制限版へ切り替える前に完全版（`4.0-full`）を優先します。
- `SERVER=hostA:5700,hostB:6000` のような複数ホストは順に試します。エラーにはホストとプロトコルごとの試行が記録されます。
- 認証情報は旧ネイティブドライバーと同様に大文字へ変換され、既存の `SYS`/MANAGER のテスト環境をそのまま使えます。既定の `data` カタログを使用しない場合は `DATABASE=` を明示してください。
- `CONNECT_TIMEOUT` は各プローブの通信に適用されます。`Protocol probe received an invalid response (missing result)` はハンドシェイク未完了を示します。ポート、TLS/SSL、ファイアウォールを確認してください。

サーバーの版がわかっている場合は、`PROTOCOL=2.1`、`3.0`、`4.0`、`4.0-full` を明示して自動検出を省略できます。

## API リファレンス {#api-reference}

{{<callout type="warning">}}
以下にない機能は、未実装または正常に動作しない場合があります。<br>
未対応のメソッドやフィールドを呼び出すと、NotImplementedException または NotSupportedException が発生します。
{{</callout>}}

### MachConnection {#machconnection}

```cs
public sealed class MachConnection : DbConnection
```

Machbase への接続を管理するクラスです。

DbConnection と同様に IDisposable を実装し、Dispose()、または using 文でリソースを解放できます。

#### コンストラクター {#constructor}
```
MachConnection(string aConnectionString)
```

接続文字列から MachConnection を作成します。


#### Open {#open}

```cs
void Open()
```

接続文字列に従って接続を試みます。

#### Close {#close}

```cs
void Close()
```

開いている接続を閉じます。

#### SetConnectAppendFlush {#setconnectappendflush}

```cs
void SetConnectAppendFlush(bool activeFlush)
```

APPEND 中に自動フラッシュするよう設定します。

#### フィールド {#field}

| 名前 | 説明 |
|--|--|
|State|System.Data.ConnectionState の値。|
|StatusString|接続された MachCommand が開始した操作の状態。<br>内部でエラーメッセージを構成するために使います。現在のクエリー状態を確認する用途には適しません。|


### MachCommand {#machcommand}

```cs
public sealed class MachCommand : DbCommand
```

MachConnection を使って SQL または APPEND を実行するクラスです。

DbCommand と同様に IDisposable を実装し、Dispose()、または using 文でリソースを解放できます。

#### コンストラクター {#constructor-1}

```cs
MachCommand(string aQueryString, MachConnection aConn)
```

接続先の MachConnection と、実行するクエリーを指定して作成します。

```cs
MachCommand(MachConnection aConn)
```

接続先の MachConnection だけを指定して作成します。APPEND など、実行するクエリーがない場合に使用します。


#### CreateParameter {#createparameter}

```cs
MachParameter CreateParameter()
```

新しい MachParameter を作成します。

#### AppendOpen {#appendopen}

```cs
MachAppendWriter AppendOpen(string aTableName, int aErrorCheckCount = 0,
    MachAppendOption option = MachAppendOption.None)
```

APPEND を開始し、MachAppendWriter を返します。

* aTableName：対象テーブル名
* aErrorCheckCount：APPEND-DATA の累積入力件数が指定件数に達するたびに、サーバーへの送信を確認します。<br>
  自動 APPEND-FLUSH のタイミングを指定します。<br>
* MachAppendOption：次のオプションがあります。
  * MachAppendOption.None：オプションなし。
  * MachAppendOption.MicroSecTruncated：DateTime の入力をマイクロ秒までに切り詰めます。
  DateTime の Ticks は 100 ナノ秒単位です。

#### AppendData {#appenddata}

```cs
void AppendData(MachAppendWriter aWriter, List<object> aDataList)
```

MachAppendWriter を使用し、データを含むリストをデータベースへ入力します。
- リスト内の順序と各データ型を、テーブルの列に合わせてください。
- 値の数が不足または超過すると、エラーになります。

> **注意**：`ulong`で`_arrival_time`を指定する場合は、1970-01-01 UTCからのナノ秒数を渡します。`DateTime.Ticks`は100ナノ秒単位のため、UTCのTicksからエポックのTicksを差し引いた後、100を掛けます。


```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, DateTime aArrivalTime)
```

AppendData() の _arrival_time を DateTime で明示的に指定するメソッドです。

```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, ulong aArrivalTimeLong)
```

AppendData() の _arrival_time を ulong で指定するメソッドです。ulong の入力に関する注意は、上記の AppendData() を参照してください。

#### AppendFlush {#appendflush}

```cs
void AppendFlush(MachAppendWriter aWriter)
```

AppendData() のデータを直ちにサーバーへ送信して、入力を反映します。<br>
呼び出し頻度を上げると、システム障害時のデータ損失を減らし、早くエラーを検出できますが、性能は低下します。<br>
頻度を下げると性能は向上しますが、データ損失の可能性が増え、エラー検出が遅れます。

#### AppendClose {#appendclose}

```cs
void AppendClose(MachAppendWriter aWriter)
```

APPEND を終了します。内部で AppendFlush() を実行してから、プロトコルを終了します。

#### ExecuteNonQuery {#executenonquery}

```cs
int ExecuteNonQuery()
```

クエリーを実行し、影響を受けたレコード数を返します。通常、SELECT 以外に使用します。

#### ExecuteScalar {#executescalar}

```cs
object ExecuteScalar()
```

クエリーを実行し、選択リストの最初の値を object として返します。特に結果が 1 つの SELECT で、DbDataReader を使わずに値を取得する場合に使用します。

#### ExecuteDbDataReader {#executedbdatareader}

```cs
DbDataReader ExecuteDbDataReader(CommandBehavior aBehavior)
```

クエリーを実行し、結果を読み取る DbDataReader を作成して返します。

#### フィールド {#field-1}

| 名前 | 説明 |
|--|--|
| Connection / DbConnection | 接続先の MachConnection。 |
| ParameterCollection / DbParameterCollection | バインドに使う MachParameterCollection。 |
| CommandText | クエリー文字列。 |
| `CommandTimeout` | サーバー応答を待つ操作のタイムアウト（ミリ秒）。MachConnection の設定に従い、ここでは参照のみ可能。 |
| FetchSize | 1 回で取得するレコード数。既定値は 3000。 |
| IsAppendOpened | APPEND が開いているか。 |


### MachDataReader {#machdatareader}

```cs
public sealed class MachDataReader : DbDataReader
```

取得した結果を読み取るクラスです。直接作成せず、MachCommand.ExecuteDbDataReader() が返すオブジェクトを使用します。

#### GetName {#getname}

```cs
string GetName(int ordinal)
```

指定した位置の列名を返します。

#### GetDataTypeName {#getdatatypename}

```cs
string GetDataTypeName(int ordinal)
```

指定した位置の列のデータ型名を返します。

#### GetFieldType {#getfieldtype}

```cs
Type GetFieldType(int ordinal)
```

指定した位置の列に対応する.NET側の型を返します。


#### GetOrdinal {#getordinal}

```cs
int GetOrdinal(string name)
```

列名に対応するインデックスを返します。


#### GetValue {#getvalue}

```cs
object GetValue(int ordinal)
```

現在のレコードの指定位置の値を返します。

#### IsDBNull {#isdbnull}

```cs
bool IsDBNull(int ordinal)
```

現在のレコードの指定位置が NULL かを返します。

#### GetValues {#getvalues}

```cs
int GetValues(object[] values)
```

現在のレコードの全値を設定し、個数を返します。

#### Get*xxxx* {#getxxxx}

```cs
bool GetBoolean(int ordinal)
byte GetByte(int ordinal)
char GetChar(int ordinal)
short GetInt16(int ordinal)
int GetInt32(int ordinal)
long GetInt64(int ordinal)
DateTime GetDateTime(int ordinal)
string GetString(int ordinal)
decimal GetDecimal(int ordinal)
double GetDouble(int ordinal)
float GetFloat(int ordinal)
```

指定した位置の列の値を、対応するデータ型で返します。

#### Read {#read}

```cs
bool Read()
```

次のレコードを読み取ります。結果がなければ False を返します。

#### フィールド {#field-2}

| 名前 | 説明 |
|--|--|
| FetchSize | 1 回で取得するレコード数。既定値 3000。ここでは変更不可。 |
| FieldCount | 結果の列数。 |
| this[int ordinal] | object GetValue(int ordinal) と同等。 |
| this[string name] | object GetValue(GetOrdinal(name)) と同等。 |
| HasRows | 結果が存在するか。 |
| RecordsAffected | MachCommand と異なり、取得した件数を表す。 |

### MachParameterCollection {#machparametercollection}

```cs
public sealed class MachParameterCollection : DbParameterCollection, IEnumerable<MachParameter>
```

MachCommand のパラメーターをバインドするクラスです。

バインド後に実行すると、指定した値を使用します。

> 現在の版では、プリペアードステートメントの実行計画キャッシュは実装されていません。同じクエリーを繰り返しても、実行性能は初回と同じです。

#### Add {#add}

```cs
MachParameter Add(string parameterName, DbType dbType)
```

名前と型を指定して MachParameter を追加し、そのオブジェクトを返します。

```cs
int Add(object value)
```

値を追加し、追加位置のインデックスを返します。


```cs
void AddRange(Array values)
```

単純な値の配列を追加します。

```cs
MachParameter AddWithValue(string parameterName, object value)
```

名前と値を指定して追加し、MachParameter を返します。

#### Contains {#contains}

```cs
bool Contains(object value)
```

指定した値が追加済みか確認します。

```cs
bool Contains(string value)
```

指定した名前のパラメーターが追加済みか確認します。

#### Clear {#clear}

```cs
void Clear()
```

すべてのパラメーターを削除します。

#### IndexOf {#indexof}

```cs
int IndexOf(object value)
```

指定した値のインデックスを返します。

```cs
int IndexOf(string parameterName)
```

指定したパラメーター名のインデックスを返します。

#### Insert {#insert}

```cs
void Insert(int index, object value)
```

指定したインデックスに値を挿入します。

#### Remove {#remove}

```cs
void Remove(object value)
```

指定した値を持つパラメーターを削除します。

```cs
void RemoveAt(int index)
```

指定したインデックスのパラメーターを削除します。

```cs
void RemoveAt(string parameterName)
```

指定した名前のパラメーターを削除します。

#### フィールド {#field-3}

| 名前 | 説明 |
| ----------------- | --------------------------------------- |
|Count|パラメーター数。|
|this[int index]|指定位置の MachParameter。|
|this[string name]|名前が一致する MachParameter。|

### MachParameter {#machparameter}

```cs
public sealed class MachParameter : DbParameter
```

各 MachCommand にバインドするパラメーター情報を保持するクラスです。

特別なメソッドはありません。

#### フィールド {#field-4}

| 名前 | 説明 |
| ------------- | --------------------------------------------------------------------------------- |
|ParameterName|パラメーター名|
|Value|値|
|Size|値のサイズ|
|Direction|ParameterDirection（Input / Output / InputOutput / ReturnValue）。既定値は Input。|
|DbType|.NET側のDB型|
|MachDbType|MACHBASE の DB 型。DbType と異なる場合があります。|
|IsNullable|NULL を許可するか|
|HasSetDbType|DB 型が指定済みか|


### MachException {#machexception}

```cs
public class MachException : DbException
```

Machbase のエラーを表すクラスです。

エラーメッセージが設定されます。全メッセージは MachErrorMsg で確認できます。

#### フィールド {#field-5}

| 名前 | 説明 |
|--|--|
|int MachErrorCode|MACHBASE のエラーコード|

### MachAppendWriter {#machappendwriter}

```cs
public sealed class MachAppendWriter
```

MachCommand を使用する別のクラスとして APPEND を提供します。
ADO.NET 標準ではなく、MACHBASE Append プロトコルをサポートするクラスです。

直接コンストラクターで作成せず、MachCommand.AppendOpen() で取得します。

#### SetErrorDelegator {#seterrordelegator}

```cs
void SetErrorDelegator(ErrorDelegateFuncType aFunc)

void ErrorDelegateFuncType(MachAppendException e);
```

エラー時に呼び出す ErrorDelegateFunc を指定します。

#### フィールド {#field-6}

| 名前 | 説明 |
|--|--|
|SuccessCount|成功したレコード数。AppendClose() 後に設定。|
|FailureCount|入力に失敗したレコード数。AppendClose() 後に設定。|
|Option|AppendOpen() に渡した MachAppendOption。|


### MachAppendException {#machappendexception}

```cs
public sealed class MachAppendException : MachException
```

次の点を除き、MachException と同じです。

* サーバーからエラーメッセージを受け取ります。
* エラーになったデータバッファー（カンマ区切り）を取得し、加工して再 APPEND したり、記録したりできます。

この例外は ErrorDelegateFunc の内部でのみ利用できます。

#### GetRowBuffer {#getrowbuffer}

```cs
string GetRowBuffer()
```

エラーが発生したデータバッファーを取得します。

## 使用方法と例 {#usage-and-examples}

### 接続 {#connection}

MachConnection を作成し、Open() と Close() を使用します。
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
MachConnection sConn = new MachConnection(sConnString);
sConn.Open();
//処理を実行
sConn.Close();
```

using 文を使用すると、接続終了用の Close() を明示的に呼ぶ必要はありません。
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();
    //処理を実行
} // sConn.Close() の明示的な呼び出しは不要
```

### クエリーの実行 {#executing-queries}

MachCommand を作成してクエリーを実行します。

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    String sQueryString = "CREATE TABLE tab1 ( col1 INTEGER, col2 VARCHAR(20) )";
    MachCommand sCommand = new MachCommand(sQueryString , sConn)
    try
    {
        sCommand.ExecuteNonQuery();
    }
    catch (MachException me)
    {
        throw me;
    }
}
```

using 文で MachCommand を確実に解放できます。
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    String sQueryString = "CREATE TABLE tab1 ( col1 INTEGER, col2 VARCHAR(20) )";
    using(MachCommand sCommand = new MachCommand(sQueryString , sConn))
    {
        try
        {
            sCommand.ExecuteNonQuery();
        }
        catch (MachException me)
        {
            throw me;
        }
    }
}
```

### SELECT の実行 {#executing-select}
SELECT を MachCommand で実行すると、MachDataReader を取得できます。

MachDataReader でレコードを 1 件ずつ読み取れます。
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    String sQueryString = "SELECT * FROM tab1;";
    using(MachCommand sCommand = new MachCommand(sQueryString , sConn))
    {
        try
        {
            MachDataReader sDataReader = sCommand.ExecuteReader();
            while (sDataReader.Read())
            {
                for (int i = 0; i < sDataReader.FieldCount; i++)
                {
                    Console.WriteLine(String.Format("{0} : {1}",
                                                    sDataReader.GetName(i),
                                                    sDataReader.GetValue(i)));
                }
            }
        }
        catch (MachException me)
        {
            throw me;
        }
    }
}
```

### パラメーターバインド {#parameter-binding}
MachParameterCollection を作成し、MachCommand に関連付けます。
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    string sSelectQuery = @"SELECT *
        FROM tab2
        WHERE CreatedDateTime < @CurrentTime
        AND CreatedDateTime >= @PastTime";

    using (MachCommand sCommand = new MachCommand(sSelectQuery, sConn))
    {
        DateTime sCurrtime = DateTime.Now;
        DateTime sPastTime = sCurrtime.AddMinutes(-1);

        try
        {
            sCommand.ParameterCollection.Add(new MachParameter { ParameterName = "@CurrentTime", Value = sCurrtime });
            sCommand.ParameterCollection.Add(new MachParameter { ParameterName = "@PastTime", Value = sPastTime });

            MachDataReader sDataReader = sCommand.ExecuteReader();

            while (sDataReader.Read())
            {
                for (int i = 0; i < sDataReader.FieldCount; i++)
                {
                    Console.WriteLine(String.Format("{0} : {1}",
                                                    sDataReader.GetName(i),
                                                    sDataReader.GetValue(i)));
                }
            }
        }
        catch (MachException me)
        {
            throw me;
        }
    }
}
```

### APPEND {#append}
MachCommand.AppendOpen() で MachAppendWriter を取得します。

このオブジェクトと MachCommand を使用し、1 レコード分のリストを AppendData() に渡します。
AppendFlush() ですべての入力を反映し、AppendClose() で APPEND を終了します。
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    using (MachCommand sAppendCommand = new MachCommand(sConn))
    {
        MachAppendWriter sWriter = sAppendCommand.AppendOpen("tab2");
        sWriter.SetErrorDelegator(AppendErrorDelegator);

        var sList = new List<object>();
        for (int i = 1; i <= 100000; i++)
        {
            sList.Add(i);
            sList.Add(String.Format("NAME_{0}", i % 100));

            sAppendCommand.AppendData(sWriter, sList);

            sList.Clear();

            if (i % 1000 == 0)
            {
                sAppendCommand.AppendFlush(sWriter);
            }
        }

        sAppendCommand.AppendClose(sWriter);
        Console.WriteLine(String.Format("Success Count : {0}", sWriter.SuccessCount));
        Console.WriteLine(String.Format("Failure Count : {0}", sWriter.FailureCount));
    }
}
```
```c#
private static void AppendErrorDelegator(MachAppendException e)
{
    Console.WriteLine("{0}", e.Message);
    Console.WriteLine("{0}", e.GetRowBuffer());
}
```

### エラーデリゲートの設定 {#set-error-delegator}

MachAppendWriter に、APPEND 中のサーバー側エラーを検出する関数を設定できます。

.NET では、デリゲート関数として指定します。
```c#
public static void ErrorCallbackFunc(MachAppendException e)
{
    Console.WriteLine("====================");
    Console.WriteLine("Error occured");
    Console.WriteLine(e.Message);
    Console.WriteLine(e.StackTrace);
    Console.WriteLine("====================");
}

public static void DoAppend()
{
    MachCommand com = new MachCommand(conn);
    MachAppendWriter writer = com.AppendOpen("tag", errorCheckCount);
    writer.SetErrorDelegator(ErrorCallbackFunc);
    //APPEND を実行
}
```

### 自動 AppendFlush の設定 {#set-auto-appendflush}

`MachConnection.SetConnectAppendFlush(true)`を指定すると、APPEND 中に自動フラッシュします。

```cs
private static string connString = $"SERVER={HOST};PORT_NO={port};USER={USER};PWD={PWD}";

public static void Main(string[] args)
{
    MachConnection conn = new MachConnection(connString);
    conn.Open();
    conn.SetConnectAppendFlush(true);
}
```

false で無効にします。

```cs
conn.SetConnectAppendFlush(false);
```

## 完全版プロバイダー API（`4.0-full`） {#full-provider-apis-protocol-40-full}

`4.0-full` のハンドシェイクで、完全な ADO.NET インターフェースを利用できます。8.0.54 のソースでは、
`4.0` 制限版は 3.1.2、`4.0-full` は 3.2.1 です。
Linux パッケージには、`$MACHBASE_HOME/lib/` に net50 版だけが含まれる場合があります。
他のフレームワークが必要なら、対応版をビルドするか復元してください。

- `UniMachNetConnector-net50-8.0.54.dll`：DBMS Standard の Linux パッケージに一般に含まれる汎用入口。
- `machNetConnector-40-net50-3.1.2.dll`：プロトコル `4.0` の制限版。
- `machNetConnector-40-net50-3.2.1.dll`：プロトコル `4.0-full`。

### `4.0-full` で追加された主な型 {#key-types-introduced-by-40-full}
- `MachDbProviderFactory`：`Instance`、`Register()`、標準の `Create*` メソッドにより、フレームワークが不変名 `Mach.Data` でコネクターを解決できます。
- `MachConnectionStringBuilder`：各キーワードを覚えずに、型付きで接続文字列を編集できます。
- `MachDataAdapter` と `MachRowUpdating`/`MachRowUpdated` イベント：`DataTable`/DataSet の処理に使用します。
- `MachCommandBuilder`：SELECT から INSERT/DELETE と、対応テーブルの UPDATE を自動生成します。Log/Tag の UPDATE は生成できません。

### 完全版プロバイダーの有効化 {#enable-the-full-provider-stack}
```csharp
var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
```

INSERT/DELETE/UPDATE が必要なら、Lookup または Volatile テーブルを使用します。Log と Tag は UPDATE を許可しないため、追記用に使用してください。

### ビルダーによる接続文字列の作成 {#build-connection-strings-fluently}
```csharp
var builder = new MachConnectionStringBuilder
{
    Server = "127.0.0.1",
    Port = 5656,
    UserID = "SYS",
    Password = "MANAGER"
};

// 旧コネクターとの互換性のため Protocol は文字列キーのまま
builder["PROTOCOL"] = "4.0-full";

using var connection = new MachConnection(builder.ConnectionString);
connection.Open();
```

### 例：`MachDataAdapter` で行を追加 {#sample-append-rows-with-machdataadapter}
Lookup テーブルを `DataTable` に読み込み、新しい行を追加して書き戻します。`MachCommandBuilder` が INSERT を自動生成します。テーブルがない場合は、先に `CREATE LOOKUP TABLE dotnet_lookup_demo(id LONG PRIMARY KEY, name VARCHAR(64));` を実行します。

```csharp
using Mach.Data.MachClient;
using System.Data;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

var adapter = new MachDataAdapter(
    "SELECT id, name FROM dotnet_lookup_demo ORDER BY id",
    connection);
var builder = new MachCommandBuilder(adapter);

var table = new DataTable();
adapter.Fill(table);

var newRow = table.NewRow();
newRow["id"] = 2001;
newRow["name"] = "Inserted from MachDataAdapter";
table.Rows.Add(newRow);

adapter.Update(table);
```

> **ヒント**：送信するコマンドを確認、または拒否する必要がある場合は、`MachDataAdapter.MachRowUpdating` / `MachRowUpdated` を購読します。

```csharp
adapter.MachRowUpdating += (sender, args) =>
{
    Console.WriteLine($"About to run {args.StatementType} with SQL: {args.Command?.CommandText}");
};
```

### 例：DbProviderFactory の使用 {#sample-work-through-dbproviderfactory}
`MachDbProviderFactory.Instance` により、`DbProviderFactories`、Dapper、独自の DI コンテナーなど、プロバイダーに依存しない基盤へ組み込めます。

```csharp
using System.Data.Common;
using Mach.Data.MachClient;

DbProviderFactory factory = MachDbProviderFactory.Instance;

using DbConnection connection = factory.CreateConnection()!;
connection.ConnectionString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
connection.Open();

using DbCommand command = connection.CreateCommand();
command.CommandText = "SELECT COUNT(*) FROM dotnet_lookup_demo";
var count = (long)command.ExecuteScalar();

Console.WriteLine($"Lookup rows: {count}");
```

設定から利用するアプリケーションでは、起動時に `MachDbProviderFactory.Register()` を 1 回呼び出します。`DbProviderFactories.GetFactory("Mach.Data")` が同じインスタンスを返すようになります。

`4.0-full` は Machbase 7.x 以降のサーバーでのみ利用できます。古いクラスタには `Protocol=4.0`（制限版）、または 2.x/3.x を使用してください。
