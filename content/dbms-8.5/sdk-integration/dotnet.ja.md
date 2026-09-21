---
title: '.NET コネクター'
type: docs
weight: 20
toc: true
---

## 目次 {#index}

* [概要](#overview)
* [インストール](#install)
* [NuGet（統合版 8.0.54）](#install-via-nuget-unified-connector-8054)
* [NuGet（旧 5.x）](#install-via-nuget-legacy-5x)
* [接続文字列](#connection-string-reference)
* [API リファレンス](#api-reference)
* [使用方法と例](#usage-and-examples)
* [完全版プロバイダー API（4.0-full）](#full-provider-apis-protocol-40-full)

## 概要 {#overview}

Machbase は、サポートする全ワイヤープロトコル（2.1～4.0）をまとめた汎用 ADO.NET プロバイダー **UniMachNetConnector** を提供します。DBMS Standard のソースでは、統合パッケージは `UniMachNetConnector` 8.0.54 で、対象フレームワーク `net452`、`net5.0`、`net6.0`、`net7.0`、`net8.0` 向けにビルドされます。コネクターは実行時に接続文字列に基づいて適切なプロトコルを自動でネゴシエートするため、時系列データの収集や照会のワークロードでも、追加の設定なしで適切なプロトコルが選択されます。

## インストール {#install}

Machbase のサーバーとクライアントのインストーラーは、汎用 .NET プロバイダーを `$MACHBASE_HOME/lib/` に配置します。
標準の Linux インストールには、例えば .NET 5.0 用のビルドである
`UniMachNetConnector-net50-8.0.54.dll` と、`machNetConnector-40-net50-3.2.1.dll` などの
プロトコル別アセンブリーが含まれる場合があります。対応する .NET SDK があれば、
ソースプロジェクトから他の対象フレームワーク用のビルドも作成できます。

- **UniMachNetConnector**：フレームワークに依存しない入口です。ソースビルドのファイル名は
  `UniMachNetConnector-net{452|50|60|70|80}-<version>.dll` の形式なので、
  配布先の対象フレームワークに合うものを選びます。
- **旧プロトコルコネクター**：汎用ローダーが必要に応じて読み込む、プロトコル別の任意のアセンブリーです。
  例：`machNetConnector-XX-net{40|50|60|70|80}-<version>.dll`。

アプリケーションの対象フレームワークに合う DLL を参照するか、配布時に実行ファイルと同じ場所にコピーしてください。

## NuGet によるインストール（統合版 8.0.54） {#install-via-nuget-unified-connector-8054}

統合版のパッケージ ID は `UniMachNetConnector` です。DLL を個別に配布せずにプロジェクトでパッケージとして管理できるため、新規アプリケーションにはこの方法を推奨します。

- 対象フレームワーク：net452、net5.0、net6.0、net7.0、net8.0。
- net5.0 以降のビルドは自己完結しています。net452 のビルドは、ソースプロジェクトの指定どおり
  `System.ValueTuple` 4.5.0 を復元します。

### クイックスタート（CLI） {#quick-start-cli}

```bash
# プロジェクトのディレクトリで実行
dotnet add package UniMachNetConnector --version 8.0.54
dotnet build
```

CI、オフライン、社内フィードなどでパッケージの取得元を制御する必要がある場合は、先に参照だけを追加してから、明示的に復元します。

```bash
dotnet add package UniMachNetConnector --version 8.0.54 --no-restore

# nuget.org だけから復元（新しいメタデータを強制取得）
dotnet nuget locals http-cache --clear
dotnet restore --no-cache --source https://api.nuget.org/v3/index.json
```

### Visual Studio {#visual-studio}

- プロジェクトを右クリック →「NuGet パッケージの管理」→「参照」タブで “UniMachNetConnector” を検索 → 8.0.54 を選択 →「インストール」。

### プロジェクトファイルの例 {#project-file-example}

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.54" />
  <!-- 他のMachbaseパッケージは不要 -->
  <!-- 対象：net452|net5.0|net6.0|net7.0|net8.0 -->
  <!-- アプリに合わせてAnyCPU/x64を維持。Machbaseサーバー側への影響はありません -->
</ItemGroup>
```

### ローカルフィードまたはプライベートフィードの使用（任意） {#using-a-local-or-private-feed-optional}

ローカルのフォルダーフィードや社内レジストリを使う場合は、それらを復元元に指定します。フォルダーフィードでは、`UniMachNetConnector.8.0.54.nupkg` をディレクトリに置き、ソースとして追加します。

```bash
# 初回のみ設定
dotnet nuget add source /path/to/local-nuget -n mach-local

# nuget.org とローカルフィードから復元
dotnet restore --no-cache \
  --source /path/to/local-nuget \
  --source https://api.nuget.org/v3/index.json
```

CI や権限が制限されたアカウントでは、パッケージキャッシュのディレクトリを絶対パスで指定してください。

```bash
PKG_DIR="$(pwd)/.nuget-packages"; mkdir -p "$PKG_DIR"
NUGET_PACKAGES="$PKG_DIR" dotnet restore --no-cache --source /path/to/local-nuget
NUGET_PACKAGES="$PKG_DIR" dotnet run --no-restore
```

> ヒント：8.0.54 の公開直後に `NU1102`（指定バージョンが見つからない）が発生する場合や、`dotnet add package` が古いバージョンを報告し続ける場合は、通常インデックスやキャッシュの問題です。`dotnet nuget locals http-cache --clear` で HTTP キャッシュを削除し、上記のように `--no-cache` で復元してください。一時的に表示される “incompatible with 'all' frameworks” は、実際の TFM 不一致ではなく、復元失敗の副作用であることがほとんどです。パッケージは net452 と net5.0～net8.0 に対応しています。

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

## NuGet によるインストール（旧 5.x） {#install-via-nuget-legacy-5x}

> **注意**：Machbase .NET Connector 5.0 も NuGet に登録されています。この 5.0 パッケージは、統合版 UniMachNetConnector より前の独立した旧パッケージです。

Visual Studio では、統合前の旧コネクターも NuGet から取得できます。以下は旧 `machNetConnector5.0` パッケージのインストール手順です。統合版より前のコードを対象とする必要がある場合にのみ使用し、新規プロジェクトには `UniMachNetConnector` 8.0.54 を推奨します。

1. Visual Studio で新しい C# .NET プロジェクトを作成します。
2. ソリューションエクスプローラーでプロジェクト名を右クリックし、**NuGet パッケージの管理** を選択します。
3. NuGet パッケージマネージャーが開いたら、左上の **参照** タブを選択し、`machNet` を検索します。
4. 検索結果から **machNetConnector5.0** を選択し、**インストール** をクリックします。
5. **変更のプレビュー** ウィンドウが表示されたら、**OK** をクリックしてインストールを続行します。
6. インストールが完了すると、ソリューションエクスプローラーの **依存関係 → パッケージ** で確認できます。
7. `Program.cs` に `using Mach.Data.MachClient;` を追加すると、machNetConnector の API を使用できます。

> 使用する NuGet パッケージの選択
> - 新規開発や更新では `UniMachNetConnector` 8.0.54 を推奨します。net452 と net5.0～net8.0 に対応し、完全版プロバイダー（4.0-full）を含む全プロトコルをまとめています。
> - 統合版へまだ移行できない旧アプリケーションに限り、`machNetConnector5.0` を使用します。

## 接続文字列 {#connection-string-reference}

接続文字列の各項目はセミコロン（`;`）で区切ります。同じ行のキーワードは別名です。

| キーワード | 説明 | 例 | 既定値 |
|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|-------------------------------------------------|---------|
| `DSN`, `SERVER`, `HOST` | ホスト名または IP アドレス | `SERVER=127.0.0.1` | なし |
| `PORT`, `PORT_NO` | リスナーポート | `PORT=5656` | `5656` |
| `USERID`, `USERNAME`, `USER`, `UID` | ユーザー名 | `UID=SYS` | `SYS` |
| `PASSWORD`, `PWD` | パスワード | `PWD=manager` | なし |
| `CONNECT_TIMEOUT`, `ConnectionTimeout`, `connectTimeout` | 接続タイムアウト（ミリ秒） | `CONNECT_TIMEOUT=10000` | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout`, `commandTimeout` | コマンドごとのタイムアウト（ミリ秒） | `COMMAND_TIMEOUT=50000` | `60000` |
| `PROTOCOL`, `ProtocolVersion`, `MachProtocol` | 使用するワイヤープロトコル（例：`2.1`、`3.0`、`4.0`、`4.0-full`、`auto`、`auto-full`）。省略すると UniMachNetConnector は `4.0` を使用します。 | `PROTOCOL=auto` | `4.0` |

例：

```csharp
var connectionString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;COMMAND_TIMEOUT=50000;PROTOCOL=4.0-full",
    host,
    port);
```

### プロトコルの自動検出（`PROTOCOL=auto`） {#protocol-auto-detection-protocolauto}

複数の Machbase リリースに接続するアプリケーションでは、`PROTOCOL=auto` を指定すると、UniMachNetConnector が実行時に適切な旧プロトコルのハンドシェイクをネゴシエートします。次のように動作します。

- `PROTOCOL=auto` は、接続文字列で指定したホスト、ポート、ユーザー、パスワード、データベース、`CONNECT_TIMEOUT` を使用し、4.0、3.0、2.2、2.1 の順に試します。
- `PROTOCOL=auto-full` も同様ですが、サーバーがプロトコル 4.0 を返した場合は、まず完全版の記述子（`4.0-full`）を試し、必要に応じて制限版（4.0）へ切り替えます。
- `SERVER=hostA:5700,hostB:6000` のように複数のホストを指定すると順に試します。失敗メッセージにはホストとプロトコルごとの試行が記録されるため、問題箇所を特定できます。
- 認証情報は旧ネイティブドライバーと同様に大文字へ変換されるため、既存の SYS/MANAGER のテスト環境をそのまま使用できます。既定の `data` カタログを使用しない場合は `DATABASE=` を明示してください。
- `CONNECT_TIMEOUT` は各プローブの往復に適用されます。例外メッセージに `Protocol probe received an invalid response (missing result)` が含まれる場合は、ハンドシェイクが完了していません。ポート、TLS/SSL の設定、ファイアウォールを確認してください。

サーバーのバージョンがわかっている場合は、`PROTOCOL=2.1`、`3.0`、`4.0`、`4.0-full` を明示して自動検出を省略できます。

## API リファレンス {#api-reference}

{{<callout type="warning">}}
以下に記載されていない機能は、未実装であるか、正常に動作しない場合があります。<br>
存在しないメソッドやフィールドを呼び出すと、`NotImplementedException` または `NotSupportedException` が発生します。
{{</callout>}}

### MachConnection {#machconnection}

```cs
public sealed class MachConnection : DbConnection
```

Machbase との接続を管理するクラスです。

DbConnection と同様に IDisposable を実装しているため、Dispose() の呼び出し、または using 文で解放できます。

#### コンストラクター {#constructor}

```
MachConnection(string aConnectionString)
```

接続文字列を受け取り、MachConnection のインスタンスを作成します。

#### Open {#open}

```cs
void Open()
```

接続文字列を使用して、実際の接続を確立します。

#### Close {#close}

```cs
void Close()
```

開いている接続を閉じます。

#### SetConnectAppendFlush {#setconnectappendflush}

```cs
void SetConnectAppendFlush(bool activeFlush)
```

Append 中に自動でフラッシュするかどうかを設定します。

#### フィールド {#field}

| 名前 | 説明 |
|--|--|
|State|System.Data.ConnectionState の値。|
|StatusString|接続が現在依存している MachCommand の状態文字列。<br>内部でエラーメッセージを構成するために使用し、操作を開始した時点の状態を表すため、クエリーの状態を確認する用途には使用しないでください。|

### MachCommand {#machcommand}

```cs
public sealed class MachCommand : DbCommand
```

MachConnection を使って **SQL コマンドまたは APPEND** を実行するクラスです。

DbCommand と同様に IDisposable を実装しているため、Dispose() の呼び出し、または using 文で解放できます。

#### コンストラクター {#constructor-1}

```cs
MachCommand(string aQueryString, MachConnection aConn)
```

実行するクエリーと、使用する MachConnection オブジェクトを指定してインスタンスを作成します。

```cs
MachCommand(MachConnection aConn)
```

使用する MachConnection オブジェクトだけを指定してインスタンスを作成します。APPEND など、実行するクエリーがない場合に使用します。

#### CreateParameter {#createparameter}

```cs
MachParameter CreateParameter()
```

新しい MachParameter を作成します。

#### AppendOpen {#appendopen}

```cs
MachAppendWriter AppendOpen(
    string aTableName,
    int aErrorCheckCount = 0,
    MachAppendOption option = MachAppendOption.None)
```

APPEND を開始し、MachAppendWriter オブジェクトを返します。

* aTableName：対象テーブル名。
* aErrorCheckCount：AppendData で入力したレコードの累積件数がこの値に達するたびに、サーバーへ送信して失敗の有無を確認します。つまり、自動 APPEND-FLUSH のタイミングを設定します。
* option：次の MachAppendOption のいずれかを指定します。
    * MachAppendOption.None：オプションなし。
    * MachAppendOption.MicroSecTruncated：DateTime の値をマイクロ秒までに切り詰めて入力します（DateTime オブジェクトの Ticks は 100 ナノ秒単位で表されます）。

#### AppendData {#appenddata}

```cs
void AppendData(MachAppendWriter aWriter, List<object> aDataList)
```

MachAppendWriter オブジェクトを使用し、データを含むリストを受け取ってデータベースへ入力します。

- リスト内の値は順に Append バッファーへ格納され、各値の型は対応するテーブル列の型と一致する必要があります。
- 値の数が不足または超過すると、例外が発生します。

> **注意**：`_arrival_time` を `ulong` で指定する場合は、Machbase が想定する 1970-01-01 UTC からのナノ秒数を渡します。DateTime オブジェクトの Tick 値をそのまま渡さないでください。`DateTime.Ticks` は 100 ナノ秒単位のため、UTC の Ticks からエポック（1970-01-01）の Ticks を差し引いた後、100 を掛けます。

```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, DateTime aArrivalTime)
```

AppendData() と同じですが、`_arrival_time` の値を DateTime オブジェクトで明示的に指定します。

```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, ulong aArrivalTimeLong)
```

AppendData() と同じですが、`_arrival_time` の値をナノ秒単位の `ulong` で明示的に指定します。`ulong` の値を `_arrival_time` に指定する際の注意点は、上記の AppendData() を参照してください。

#### AppendFlush {#appendflush}

```cs
void AppendFlush(MachAppendWriter aWriter)
```

AppendData() で入力したデータを直ちにサーバーへ送信し、入力を反映します。<br>
呼び出し頻度を上げると、システム障害時のデータ損失が減り、エラーも早く検出できますが、性能は低下します。<br>
呼び出し頻度を下げると、データ損失の可能性が高まり、エラーの検出も遅れますが、性能は大きく向上します。

#### AppendClose {#appendclose}

```cs
void AppendClose(MachAppendWriter aWriter)
```

APPEND を終了します。内部で AppendFlush() を呼び出した後、プロトコルを終了します。

#### ExecuteNonQuery {#executenonquery}

```cs
int ExecuteNonQuery()
```

クエリーを実行し、影響を受けたレコード数を返します。通常、INSERT、UPDATE、DELETE、DDL など、SELECT 以外のクエリーに使用します。

#### ExecuteScalar {#executescalar}

```cs
object ExecuteScalar()
```

クエリーを実行し、選択リストの最初の値を object として返します。通常、結果が 1 つだけの SELECT クエリー（スカラークエリー）の結果を、DbDataReader を使わずに取得する場合に使用します。

#### ExecuteDbDataReader {#executedbdatareader}

```cs
DbDataReader ExecuteDbDataReader(CommandBehavior aBehavior)
```

クエリーを実行し、結果を順に読み取る DbDataReader を返します。

#### フィールド {#field-1}

| 名前 | 説明 |
|--|--|
| Connection / DbConnection | 接続中の MachConnection。 |
| ParameterCollection / DbParameterCollection | バインドに使用する MachParameterCollection。 |
| CommandText | 実行する SQL 文字列。 |
| CommandTimeout | サーバーの応答を待つ最大時間（ミリ秒）。<br>MachConnection の設定値に従い、ここでは参照のみ可能です。 |
| FetchSize | サーバーから 1 回で取得するレコード数。既定値は 3000。 |
| IsAppendOpened | Append セッションが開いているかどうか。 |

### MachDataReader {#machdatareader}

```cs
public sealed class MachDataReader : DbDataReader
```

取得した結果を順に読み取るクラスです。直接作成することはできず、MachCommand.ExecuteDbDataReader() で取得したオブジェクトのみを使用できます。

#### GetName {#getname}

```cs
string GetName(int ordinal)
```

指定した位置の列名を返します。

#### GetDataTypeName {#getdatatypename}

```cs
string GetDataTypeName(int ordinal)
```

指定した位置の列の Machbase データ型名を返します。

#### GetFieldType {#getfieldtype}

```cs
Type GetFieldType(int ordinal)
```

指定した位置の列に対応する .NET 側の型を返します。

#### GetOrdinal {#getordinal}

```cs
int GetOrdinal(string name)
```

列名に対応するインデックスを返します。

#### GetValue {#getvalue}

```cs
object GetValue(int ordinal)
```

現在のレコードの指定位置の値を object として返します。

#### IsDBNull {#isdbnull}

```cs
bool IsDBNull(int ordinal)
```

現在のレコードの指定位置の値が NULL かどうかを返します。

#### GetValues {#getvalues}

```cs
int GetValues(object[] values)
```

現在のレコードの値を配列に格納し、格納した値の数を返します。

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

次のレコードを読み取ります。結果がなくなると false を返します。

#### フィールド {#field-2}

| 名前 | 説明 |
|--|--|
| FetchSize | サーバーから 1 回で取得するレコード数。既定値は 3000 で、ここでは変更できません。 |
| FieldCount | 結果の列数。 |
| this[int ordinal] | GetValue(int ordinal) と同等。 |
| this[string name] | GetValue(GetOrdinal(name)) と同等。 |
| HasRows | 結果が存在するかどうか。 |
| RecordsAffected | MachCommand とは異なり、ここでは取得したレコード数を表します。 |

### MachParameterCollection {#machparametercollection}

```cs
public sealed class MachParameterCollection : DbParameterCollection, IEnumerable<MachParameter>
```

MachCommand にバインドするパラメーターの集合を管理するクラスです。

パラメーターをバインドしてから実行すると、その値が一緒に送信されます。

> 現在のバージョンでは、プリペアドステートメントの実行計画キャッシュが実装されていません。そのため、バインド後に同じクエリーを繰り返し実行しても、性能は初回の実行と同じです。

#### Add {#add}

```cs
MachParameter Add(string parameterName, DbType dbType)
```

パラメーター名と型を指定して MachParameter を追加し、追加した MachParameter オブジェクトを返します。

```cs
int Add(object value)
```

値を追加し、追加した位置のインデックスを返します。

```cs
void AddRange(Array values)
```

単純な値の配列をまとめて追加します。

```cs
MachParameter AddWithValue(string parameterName, object value)
```

パラメーター名と値を一緒に追加し、追加した MachParameter オブジェクトを返します。

#### Contains {#contains}

```cs
bool Contains(object value)
```

指定した値がすでに追加されているかどうかを確認します。

```cs
bool Contains(string value)
```

指定した名前のパラメーターが存在するかどうかを確認します。

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

指定した値を含むパラメーターを削除します。

```cs
void RemoveAt(int index)
```

指定したインデックスにあるパラメーターを削除します。

```cs
void RemoveAt(string parameterName)
```

指定した名前のパラメーターを削除します。

#### フィールド {#field-3}

| 名前 | 説明 |
| ----------------- | --------------------------------------- |
|Count|パラメーターの数。|
|this[int index]|指定したインデックスの MachParameter。|
|this[string name]|名前が一致する MachParameter。|

### MachParameter {#machparameter}

```cs
public sealed class MachParameter : DbParameter
```

MachCommand にバインドする個々のパラメーターの情報を保持するクラスです。

特別なメソッドはありません。

#### フィールド {#field-4}

| 名前 | 説明 |
| ------------- | --------------------------------------------------------------------------------- |
|ParameterName|パラメーター名|
|Value|送信する値|
|Size|値のサイズ|
|Direction|ParameterDirection（Input / Output / InputOutput / ReturnValue）。<br>既定値は Input です。|
|DbType|.NET 側の DB 型|
|MachDbType|Machbase 固有の DB 型。<br>DbType と異なる場合があります。|
|IsNullable|NULL を許可するかどうか|
|HasSetDbType|DbType が設定済みかどうか|

### MachException {#machexception}

```cs
public class MachException : DbException
```

Machbase で発生したエラーを表す例外クラスです。

エラーメッセージが設定されます。すべてのエラーメッセージは MachErrorMsg で確認できます。

#### フィールド {#field-5}

| 名前 | 説明 |
|--|--|
|int MachErrorCode|Machbase が返したエラーコード|

### MachAppendWriter {#machappendwriter}

```cs
public sealed class MachAppendWriter
```

MachCommand と組み合わせて APPEND を別途サポートする補助クラスです。
ADO.NET 標準ではなく、Machbase の Append プロトコルをサポートするためのクラスです。

専用のコンストラクターはなく、MachCommand.AppendOpen() を呼び出してインスタンスを取得します。

#### SetErrorDelegator {#seterrordelegator}

```cs
void SetErrorDelegator(ErrorDelegateFuncType aFunc)

void ErrorDelegateFuncType(MachAppendException e);
```

Append 中にエラーが発生したときに呼び出す ErrorDelegateFunc を登録します。

#### フィールド {#field-6}

| 名前 | 説明 |
|--|--|
|SuccessCount|正常に保存されたレコード数。AppendClose() の後に設定されます。|
|FailureCount|入力に失敗したレコード数。AppendClose() の後に設定されます。|
|Option|AppendOpen() の呼び出し時に指定した MachAppendOption の値。|

### MachAppendException {#machappendexception}

```cs
public sealed class MachAppendException : MachException
```

次の点を除き、MachException と同じです。

* サーバーが返したエラーメッセージをそのまま受け取ります。
* エラーの原因となったレコードのデータバッファー（カンマ区切り）を取得できるため、加工して再度 APPEND したり、記録したりできます。

この例外は ErrorDelegateFunc の内部でのみ使用できます。

#### GetRowBuffer {#getrowbuffer}

```cs
string GetRowBuffer()
```

エラーの原因となったレコードのデータバッファーを文字列で返します。

## 使用方法と例 {#usage-and-examples}

### 接続 {#connection}

MachConnection を作成し、Open() と Close() で接続を制御できます。

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
MachConnection sConn = new MachConnection(sConnString);
sConn.Open();
//処理を実行
sConn.Close();
```

using 文を使用すると、Close() を明示的に呼び出さなくてもリソースが解放されます。

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();
    //処理を実行
} // sConn.Close() の明示的な呼び出しは不要
```

### クエリーの実行 {#executing-queries}

MachCommand を作成して SQL 文を実行できます。

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    String sQueryString = "CREATE TABLE tab1 ( col1 INTEGER, col2 VARCHAR(20) )";
    MachCommand sCommand = new MachCommand(sQueryString , sConn);
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

using 文を使用すると、MachCommand もすぐに解放できます。

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

SELECT クエリーを指定した MachCommand を ExecuteReader() で実行すると、MachDataReader を取得できます。

MachDataReader でレコードを 1 件ずつ順に読み取れます。

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

MachCommand の MachParameterCollection にパラメーターを設定して関連付けられます。これにより、時系列の照会条件などをパラメーターとして安全に渡せます。

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

Append プロトコルを使用すると、大量の時系列データを高速に格納できます。

MachCommand で AppendOpen() を実行すると、MachAppendWriter オブジェクトを取得できます。

このオブジェクトと MachCommand を使用し、1 レコード分のリストを AppendData() に渡します。
AppendFlush() で入力したすべてのレコードを反映し、AppendClose() で APPEND 全体を終了します。

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

MachAppendWriter には、APPEND 中に Machbase サーバー側で発生したエラーを検出する関数を指定できます。Append 中にサーバーでエラーが発生すると、指定したデリゲートが呼び出されます。

.NET では、この関数をデリゲート関数として指定します。

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

接続で `SetConnectAppendFlush(true)` を呼び出すと、APPEND 中に一定間隔で自動フラッシュが実行されます。

```cs
private static string connString = $"SERVER={HOST};PORT_NO={port};USER={USER};PWD={PWD}";

public static void Main(string[] args)
{
    MachConnection conn = new MachConnection(connString);
    conn.Open();
    conn.SetConnectAppendFlush(true);
}
```

false を指定すると、自動フラッシュは無効になります。

```cs
conn.SetConnectAppendFlush(false);
```

## 完全版プロバイダー API（4.0-full） {#full-provider-apis-protocol-40-full}

`4.0-full` のハンドシェイクで、完全な ADO.NET インターフェースを利用できます。8.0.54 のソースパッケージでは、
4.0 制限版コネクターは 3.1.2、4.0-full コネクターは 3.2.1 です。
インストールされた Linux パッケージには、`$MACHBASE_HOME/lib/` に net50 版だけが含まれる場合があります。
他の対象フレームワークが必要な場合は、ソースからビルドするか、NuGet で復元してください。

- `UniMachNetConnector-net50-8.0.54.dll`：DBMS Standard の Linux パッケージに一般に含まれる汎用の入口。
- `machNetConnector-40-net50-3.1.2.dll`：プロトコル 4.0 の制限版コネクター。
- `machNetConnector-40-net50-3.2.1.dll`：プロトコル 4.0-full のコネクター。

### 4.0-full で追加された主な型 {#key-types-introduced-by-40-full}

- `MachDbProviderFactory`：`Instance`、`Register()`、標準の `Create*` メソッドにより、フレームワークが不変名 `Mach.Data` でコネクターを解決できます。
- `MachConnectionStringBuilder`：すべてのキーワードを覚えなくても、型付きで接続文字列を編集できます。
- `MachDataAdapter` と `MachRowUpdating`/`MachRowUpdated` イベント：`DataTable`/`DataSet` を使う処理に使用します。
- `MachCommandBuilder`：SELECT 文から INSERT/DELETE（対応するテーブルでは UPDATE も）を自動生成します。Log テーブルと Tag テーブルでは UPDATE を生成しません。

### 完全版プロバイダーの有効化 {#enable-the-full-provider-stack}

```csharp
var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
```

INSERT/DELETE/UPDATE が必要な場合は、Lookup テーブルまたは Volatile テーブルを使用します。Log テーブルと Tag テーブルは UPDATE を受け付けないため、追記専用として使用してください。

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

### 例：MachDataAdapter で行を追加 {#sample-append-rows-with-machdataadapter}

Lookup テーブルを `DataTable` に読み込み、新しい行を追加して、`MachDataAdapter` で変更を書き戻す例です。INSERT 文は `MachCommandBuilder` が自動生成します。（テーブルがまだない場合は、先に一度作成してください：`CREATE LOOKUP TABLE dotnet_lookup_demo(id LONG PRIMARY KEY, name VARCHAR(64));`）

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

> **ヒント**：送信前にコマンドを確認したり、実行を拒否したりする必要がある場合は、`MachDataAdapter.MachRowUpdating` / `MachRowUpdated` を購読します。

```csharp
adapter.MachRowUpdating += (sender, args) =>
{
    Console.WriteLine($"About to run {args.StatementType} with SQL: {args.Command?.CommandText}");
};
```

### 例：DbProviderFactory の使用 {#sample-work-through-dbproviderfactory}

`MachDbProviderFactory.Instance` を使用すると、`DbProviderFactories`、Dapper、独自の DI コンテナーなど、プロバイダーに依存しない基盤に Machbase を組み込めます。

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

設定ベースのアプリケーションにファクトリーを公開するには、起動時に `MachDbProviderFactory.Register()` を 1 回呼び出し、`DbProviderFactories.GetFactory("Mach.Data")` が同じインスタンスを返すようにします。

`4.0-full` は、Machbase 7.x 以降のサーバーに接続する場合にのみ使用できます。古いサーバーには `PROTOCOL=4.0`（制限版）、または 2.x/3.x のプロトコルを使用してください。
