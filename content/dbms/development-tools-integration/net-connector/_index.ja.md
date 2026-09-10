---
type: docs
title: '11.8 .NET Connector'
weight: 80
toc: true
aliases:
  - /dbms/reference/sdk-api/net-connector/
---

## 目次 {#index}

* [概要](#overview)
* [インストール](#install)
* [NuGet（統合8.0.55）](#nuget-unified-connector)
* [接続文字列リファレンス](#connection-string-reference)
* [APIリファレンス](#api-reference)
* [使用例](#usage-and-examples)
* [プロトコル4.0-fullの全API](#full-provider-apis-protocol-40-full)

## 概要 {#overview}

Machbaseは通信プロトコル2.1～4.0をサポートする汎用ADO.NETプロバイダー
**UniMachNetConnector**を提供します。現在の統合パッケージは`UniMachNetConnector` 8.0.55で、
`net452`、`net5.0`、`net6.0`、`net7.0`、`net8.0`のターゲットをビルドします。
自動ネゴシエーションは接続文字列に`PROTOCOL=auto`または`auto-full`を指定した場合のみ動作します。

## インストール {#install}

インストール済みMachbaseサーバー・クライアントには、`$MACHBASE_HOME/lib/`に汎用.NETプロバイダーも
配布されます。標準のLinuxインストールには、たとえば`UniMachNetConnector-net50-8.0.55.dll`や
`machNetConnector-40-net50-3.2.2.dll`などのプロトコル別アセンブリが含まれる場合があります。
ソースプロジェクトは必要な.NET SDKがある場合、追加の対象フレームワーク向けビルドも可能です。

- **UniMachNetConnector**: フレームワークに依存しないエントリーポイントです。ソースビルドのファイル名は
  `UniMachNetConnector-net{452|50|60|70|80}-<version>.dll`形式で、デプロイ先フレームワークに
  合うファイルを選択します。
- **レガシープロトコルコネクター**: `machNetConnector-XX-net{40|50|60|70|80}-<version>.dll`のように
  プロトコルごとに分かれたアセンブリです。UniMachNetConnectorが必要に応じてロードします。

アプリケーションでは対象フレームワークに合うDLLを参照するか、デプロイ時に実行ファイルと同じ場所に
配置します。

## マルチデータベース

MachConnector 4.0は接続文字列の`DATABASE`または`DB_NAME`で初期データベースを選択できます。

```text
SERVER=127.0.0.1;PORT_NO=5656;UID=APP_A;PWD=secret;DATABASE=FACTORY_A
```

標準の`Database`プロパティと`ChangeDatabase()`は現在のカタログの切り替えAPIとして保証されないため、
SQLの`USE`と`CURRENT_DATABASE()`を使用します。接続プールへの返却時のカタログ初期化も、自動的に
行われるとは考えません。詳細な制限は
[マルチデータベース運用ガイド](/dbms/operations-configuration-recovery/multi-database/#97-net)を参照してください。

## NuGetでインストール（統合コネクター、8.0.55） {#nuget-unified-connector}

統合コネクターのパッケージIDは`UniMachNetConnector`です。新規プロジェクトでは、DLLのコピーより
NuGetパッケージ参照を推奨します。

- サポートするTFM: net452、net5.0、net6.0、net7.0、net8.0
- net5.0以降のビルドは自己完結型です。net452ビルドはソースプロジェクト基準で
  `System.ValueTuple` 4.5.0を復元します。

### クイックスタート（コマンドライン）

```bash
# プロジェクトフォルダーで実行
dotnet add package UniMachNetConnector --version 8.0.55
dotnet build
```

ソース（フィード）を明示的に制御する場合は、参照だけ追加して別途復元してください。

```bash
dotnet add package UniMachNetConnector --version 8.0.55 --no-restore

# nuget.orgのメタデータを強制更新
dotnet nuget locals http-cache --clear
dotnet restore --no-cache --source https://api.nuget.org/v3/index.json
```

### Visual Studio

- プロジェクトを右クリック → NuGetパッケージの管理 → 参照 → 「UniMachNetConnector」を検索 → 8.0.55を選択 → インストール。

### プロジェクトファイルの例

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.55" />
  <!-- 追加のMachbaseパッケージは不要 -->
  <!-- 対象フレームワーク: net452|net5.0|net6.0|net7.0|net8.0 -->
</ItemGroup>
```

### ローカル・社内フィードの使用（任意）

社内レジストリやフォルダーフィードを使用する場合は、次のようにソースを追加して復元します。
フォルダーフィードは該当ディレクトリに`UniMachNetConnector.8.0.55.nupkg`を配置します。

```bash
# 初回のみ設定
dotnet nuget add source /path/to/local-nuget -n mach-local

# nuget.orgと併用して復元
dotnet restore --no-cache \
  --source /path/to/local-nuget \
  --source https://api.nuget.org/v3/index.json
```

権限制限がある環境では、パッケージキャッシュのパスを絶対パスで指定してください。

```bash
PKG_DIR="$(pwd)/.nuget-packages"; mkdir -p "$PKG_DIR"
NUGET_PACKAGES="$PKG_DIR" dotnet restore --no-cache --source /path/to/local-nuget
NUGET_PACKAGES="$PKG_DIR" dotnet run --no-restore
```

> ヒント: 公開直後にNU1102（指定バージョンが見つからない）や「incompatible with 'all' frameworks」が
> 表示される場合、通常はインデックス・キャッシュの問題です。`dotnet nuget locals http-cache --clear`後に
> `--no-cache`で復元すると解決します。パッケージはnet452とnet5.0～net8.0をサポートします。

### 最小の使用例

```csharp
using System;
using Mach.Data.MachClient;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var cs = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var conn = new MachConnection(cs);
conn.Open();

using var cmd = new MachCommand("SELECT COUNT(*) FROM V$TABLES", conn);
var count = Convert.ToInt64(cmd.ExecuteScalar());
Console.WriteLine($"Tables: {count}");
```

## 接続文字列リファレンス {#connection-string-reference}

接続文字列の各項目はセミコロン（`;`）で区切ります。表の同じ行にあるキーワードは同じ意味です。

| キーワード | 説明 | 例 | デフォルト値 |
|----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------|---------|
| `DSN`, `SERVER`, `HOST` | ホスト名またはIPアドレス | `SERVER=127.0.0.1` | なし |
| `PORT`, `PORT_NO` | リスナーポート | `PORT=5656` | `5656` |
| `USERID`, `USERNAME`, `USER`, `UID` | ユーザー名 | `UID=SYS` | `SYS` |
| `PASSWORD`, `PWD` | パスワード | `PWD=manager` | なし |
| `CONNECT_TIMEOUT`, `ConnectionTimeout`, `connectTimeout` | 接続タイムアウト（ミリ秒） | `CONNECT_TIMEOUT=10000` | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout`, `commandTimeout` | コマンドごとのタイムアウト（ミリ秒） | `COMMAND_TIMEOUT=50000` | `60000` |
| `PROTOCOL`, `ProtocolVersion`, `MachProtocol` | 優先する通信プロトコル（`2.1`、`3.0`、`4.0`、`4.0-full`、`auto`、`auto-full`など）。省略時は`4.0`。 | `PROTOCOL=auto` | `4.0` |

例:

```csharp
var connectionString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;COMMAND_TIMEOUT=50000;PROTOCOL=4.0-full",
    host,
    port);
```

### プロトコルの自動検出（`PROTOCOL=auto`）

サーバーバージョンが混在する環境では、`PROTOCOL=auto`を指定し、UniMachNetConnectorが実行時に適切な
レガシープロトコルをネゴシエートするよう設定できます。動作は次のとおりです。

- `PROTOCOL=auto`は4.0 → 3.0 → 2.2 → 2.1の順でハンドシェイクを試み、接続文字列のホスト・ポート・
  ユーザー・パスワード・データベース・`CONNECT_TIMEOUT`値をそのまま使用します。
- `PROTOCOL=auto-full`はサーバーのメジャーバージョンが4なら登録済みの`4.0-full`ディスクリプターを
  選択します。ディスクリプターがないビルドだけlimited 4.0を選び、full接続失敗後にlimitedへ
  自動再試行しません。
- `SERVER=hostA:5700,hostB:6000`のように複数ホストを指定すると順番に試行します。失敗メッセージには
  各ホスト・プロトコルの組み合わせが記録され、問題箇所を特定できます。
- 認証情報は既存レガシードライバーと同様に大文字へ変換されます。デフォルトのデータベース（`data`）を
  使用しない場合は`DATABASE=`値を明示してください。
- `CONNECT_TIMEOUT`値は各検出の往復に適用されます。例外メッセージに
  `Protocol probe received an invalid response`がある場合は、ポート・ファイアウォール・TLS設定を再確認します。

サーバーバージョンが既知なら、`PROTOCOL=2.1`、`3.0`、`4.0`、`4.0-full`のように明示して
自動検出を省略することもできます。

## APIリファレンス {#api-reference}

{{< callout type="warning" >}}
以下に記載されていない機能は未実装、または正常に動作しない場合があります。<br>
宣言済みのAPIでも、未実装・非サポート機能は`NotImplementedException`または
`NotSupportedException`を返す場合があります。必要なAPIがインストールしたプロバイダーにあるか、
先に確認してください。
{{< /callout >}}

### MachConnection

```cs
public sealed class MachConnection : DbConnection
```

Machbaseとの接続を担当するクラスです。`DbConnection`と同様に`IDisposable`を実装するため、
`Dispose()`または`using`で安全に解放できます。

#### コンストラクター

```
MachConnection(string aConnectionString)
```

接続文字列を受け取り、`MachConnection`インスタンスを作成します。

#### Open

```cs
void Open()
```

接続文字列を使用して実際の接続を確立します。

#### Close

```cs
void Close()
```

開いている接続を終了します。

#### SetConnectAppendFlush

```cs
void SetConnectAppendFlush(bool activeFlush)
```

Append中に自動フラッシュするかを設定します。

#### フィールド

| 名前 | 説明 |
|--|--|
| `State` | `System.Data.ConnectionState`の値を表します。 |
| `StatusString` | 現在の接続が依存する`MachCommand`の状態文字列です。内部ログ用のため、クエリ状態の判定には使用しないことを推奨します。 |

### MachCommand

```cs
public sealed class MachCommand : DbCommand
```

`MachConnection`経由でSQLコマンドやAppendを実行するクラスです。
`DbCommand`と同様に`IDisposable`を実装します。

#### コンストラクター

```cs
MachCommand(string aQueryString, MachConnection aConn)
```

実行するクエリと接続オブジェクトを指定してインスタンスを作成します。

```cs
MachCommand(MachConnection aConn)
```

クエリが不要なAppend専用コマンドを作成します。

#### CreateParameter

```cs
MachParameter CreateParameter()
```

新しい`MachParameter`を作成します。

#### AppendOpen

```cs
MachAppendWriter AppendOpen(
    string aTableName,
    int aErrorCheckCount = 0,
    MachAppendOption option = MachAppendOption.None)
```

Appendセッションを開き、`MachAppendWriter`を返します。

* `aTableName`: 対象テーブル名
* `aErrorCheckCount`: 指定レコード数ごとにサーバーへ送信して失敗の有無を確認します。
  つまり自動`APPEND-FLUSH`のタイミングを設定します。
* `option`: `None`または`MicroSecTruncated`を指定できます。

#### AppendData

```cs
void AppendData(MachAppendWriter writer, List<object> dataList)
```

リスト内の値を順番にAppendバッファへ格納します。各値の型はテーブル列の型と一致する必要があり、
値の数が不足・超過すると例外になります。

> **補足**: `_arrival_time`を`ulong`で直接指定する場合は、Machbaseが要求する1970-01-01 UTC基準の
> ナノ秒値を入力する必要があります。

```cs
void AppendDataWithTime(
    MachAppendWriter writer,
    List<object> dataList,
    DateTime arrivalTime)
```

`_arrival_time`を`DateTime`で明示します。

```cs
void AppendDataWithTime(
    MachAppendWriter writer,
    List<object> dataList,
    ulong arrivalTime)
```

`_arrival_time`をナノ秒単位の`ulong`で指定します。

#### AppendFlush

```cs
void AppendFlush(MachAppendWriter writer)
```

バッファ内のデータをサーバーに送信します。呼び出し間隔を短くするとクライアントバッファに残るデータと
送信遅延を減らせますが、通信コストは増える場合があります。呼び出し成功だけでディスクの耐久性を判断せず、
サーバー処理結果と対象テーブルの耐久性ポリシーも確認します。

#### AppendClose

```cs
void AppendClose(MachAppendWriter writer)
```

Appendセッションを終了します。内部では`AppendFlush()`の後にプロトコルを終了します。

#### ExecuteNonQuery

```cs
int ExecuteNonQuery()
```

クエリを実行し、影響を受けたレコード数を返します。主に`INSERT`、`UPDATE`、`DELETE`、DDLで使用します。

#### RowId

```cs
UInt64? RowId
```

Standard Editionで単一の`INSERT ... VALUES`が成功すると、MachConnector 4.0/4.0-fullと
Universal .NETの`ExecuteNonQuery()`の後に入力行のROWIDを確認できます。

```cs
using (var command = new MachCommand(
    "INSERT INTO orders(item) VALUES('pump')", connection))
{
    command.ExecuteNonQuery();
    ulong? rowId = command.RowId;
}
```

返すROWIDがない場合は`null`です。ROWIDは64ビットの`RowId`で読み取り、従来の32ビットの
`LastInsertedId`は使用しません。バッチやAppendなどの違いは
[ROWIDとINSERT結果ID](/dbms/reference/sql/rowid/)を参照してください。

#### ExecuteScalar

```cs
object ExecuteScalar()
```

クエリを実行し、最初の列の値を返します。

#### ExecuteDbDataReader

```cs
DbDataReader ExecuteDbDataReader(CommandBehavior behavior)
```

クエリを実行し、結果を順次読み取れる`DbDataReader`を返します。

#### フィールド

| 名前 | 説明 |
|--|--|
| `Connection` / `DbConnection` | 現在接続している`MachConnection`です。 |
| `ParameterCollection` / `DbParameterCollection` | バインドするパラメーターのコレクションです。 |
| `CommandText` | 実行するSQL文字列です。 |
| `CommandTimeout` | サーバー応答を待つ最大時間（ミリ秒）です。値は`MachConnection`設定に従い、ここでは読み取り専用です。 |
| `FetchSize` | サーバーから一度に取得するレコード数です。デフォルトは3000です。 |
| `IsAppendOpened` | Appendセッションが開いているかを表します。 |
| `RowId` | 成功した単一INSERTの64ビットROWIDです。値がない場合は`null`です。 |

### MachDataReader

```cs
public sealed class MachDataReader : DbDataReader
```

フェッチした結果を順次読み取るリーダーです。`MachCommand.ExecuteDbDataReader()`で取得した
オブジェクトのみ使用できます。

#### GetName

```cs
string GetName(int ordinal)
```

指定インデックスの列名を返します。

#### GetDataTypeName

```cs
string GetDataTypeName(int ordinal)
```

Machbaseの列の型名を返します。

#### GetFieldType

```cs
Type GetFieldType(int ordinal)
```

.NET側のマッピング型を返します。

#### GetOrdinal

```cs
int GetOrdinal(string name)
```

列名に対応するインデックスを返します。

#### GetValue

```cs
object GetValue(int ordinal)
```

現在のレコードの値を`object`で返します。

#### IsDBNull

```cs
bool IsDBNull(int ordinal)
```

該当列の値が`NULL`か確認します。

#### GetValues

```cs
int GetValues(object[] values)
```

現在のレコードの値を配列に格納し、格納した項目数を返します。

#### GetSchemaTable

```cs
DataTable GetSchemaTable()
```

SELECT結果列のスキーマメタデータを返します。`AllowDBNull`でNULL許容性を確認します。
MachConnector40とMachConnector40-full-APIに同じ動作が適用されます。

```csharp
using var reader = command.ExecuteReader();
DataTable schema = reader.GetSchemaTable();

foreach (DataRow row in schema.Rows)
{
    string columnName = Convert.ToString(row["ColumnName"]);
    object allowDBNull = row["AllowDBNull"];

    if (allowDBNull is bool value && !value)
    {
        Console.WriteLine($"{columnName}: NO_NULLS");
    }
    else
    {
        // trueまたはDBNull.Value: NULL処理が必要
        Console.WriteLine($"{columnName}: NULL処理が必要");
    }
}
```

| `AllowDBNull` | 意味 |
|---------------|------|
| `false` | NULLにならない |
| `true` | NULLになり得る |
| `DBNull.Value` | 判定不能 |

`DBNull.Value`は`NOT NULL`を意味しません。NULLが発生し得るものとして処理します。
SQL結果の判定規則は
[NULL許容性メタデータのサポート範囲](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-nullable-metadata)を
参照してください。

Machbase SQLでは`''`はSQLの`NULL`のため、`GetSchemaTable()`の`AllowDBNull`は`true`で、
該当行の`IsDBNull()`も`true`です。`''''`は単一引用符1文字であり、`AllowDBNull=false`の
NULLではない文字列結果です。

`GetSchemaTable()`は`ColumnName`、`ColumnOrdinal`、`ColumnSize`、`NumericPrecision`、
`NumericScale`、`DataType`、`ProviderType`、`IsLong`、`AllowDBNull`、`IsKey`を提供します。
`IsKey`が`true`ならSELECT結果の直接の列がPRIMARY KEYです。式や集計式は`false`です。

旧バージョンのサーバーまたはSDKでは`IsKey`が`false`として返る場合があります。

NULL許容性メタデータはDECIMALの精度`1~65`、スケール`0~30`や実際の値を変更しません。
.NETでは精度29以下かつスケール28以下のDECIMALを`System.Decimal`で返します。この範囲を超えるDECIMALは、
精度損失を防ぐため`System.String`で返します。このとき`GetSchemaTable().DataType`、`GetFieldType()`、
実際の行の値のCLR型もすべて`System.String`です。

#### Get*XXXX*

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

列の値を指定した型で返します。

#### Read

```cs
bool Read()
```

次のレコードを読み取ります。結果がなくなると`false`を返します。

#### フィールド

| 名前 | 説明 |
|--|--|
| `FetchSize` | サーバーから一度に取得するレコード数です。デフォルトは3000で、ここでは変更できません。 |
| `FieldCount` | 結果列数です。 |
| `this[int ordinal]` | `GetValue(int ordinal)`と同じです。 |
| `this[string name]` | `GetValue(GetOrdinal(name))`と同じです。 |
| `HasRows` | 結果が存在するかを表します。 |
| `RecordsAffected` | フェッチしたレコード数を表します。 |

### MachParameterCollection

```cs
public sealed class MachParameterCollection :
    DbParameterCollection,
    IEnumerable<MachParameter>
```

`MachCommand`にバインドするパラメーター集合を管理するクラスです。

パラメーターを設定して実行すると、その値も送信されます。

> `MachParameter`のバインディングは、プリペアドステートメントとしての実行計画キャッシュを提供しません。
> 繰り返し実行の性能は、実際のクエリとサーバーキャッシュの状態で測定します。
>
> 現在のプロバイダーはパラメーターを型別のSQLリテラルに変換してからExecDirectで実行します。
> そのため`MachParameterCollection`は、サーバーのPrepared Named Bindプロトコルや
> パラメーターメタデータを使用しません。

#### Add

```cs
MachParameter Add(string parameterName, DbType dbType)
```

パラメーター名と型を指定して`MachParameter`を追加し、作成したオブジェクトを返します。

```cs
int Add(object value)
```

値を追加し、追加先のインデックスを返します。

```cs
void AddRange(Array values)
```

単純な値の配列をまとめて追加します。

```cs
MachParameter AddWithValue(string parameterName, object value)
```

パラメーター名と値を同時に追加し、作成した`MachParameter`を返します。

#### Contains

```cs
bool Contains(object value)
```

その値が追加済みか確認します。

```cs
bool Contains(string parameterName)
```

指定パラメーター名が存在するか確認します。

#### Clear

```cs
void Clear()
```

全パラメーターを削除します。

#### IndexOf

```cs
int IndexOf(object value)
```

その値のインデックスを返します。

```cs
int IndexOf(string parameterName)
```

パラメーター名があるインデックスを返します。

#### Insert

```cs
void Insert(int index, object value)
```

指定位置に値を挿入します。

#### Remove

```cs
void Remove(object value)
```

その値を含むパラメーターを削除します。

```cs
void RemoveAt(int index)
```

指定インデックスのパラメーターを削除します。

```cs
void RemoveAt(string parameterName)
```

指定名のパラメーターを削除します。

#### フィールド

| 名前 | 説明 |
|--|--|
| `Count` | パラメーター数です。 |
| `this[int index]` | 指定インデックスの`MachParameter`です。 |
| `this[string name]` | 名前に一致する`MachParameter`です。 |

### MachParameter

```cs
public sealed class MachParameter : DbParameter
```

個々のパラメーターのバインディング情報を保存するクラスです。

#### フィールド

| 名前 | 説明 |
|--|--|
| `ParameterName` | パラメーター名です。 |
| `Value` | 送信する値です。 |
| `Size` | 値の長さです。 |
| `Direction` | `ParameterDirection`値です。デフォルトは`Input`です。 |
| `DbType` | .NET側のDB型です。 |
| `MachDbType` | Machbase固有の型です。 |
| `IsNullable` | `NULL`許容性です。 |
| `HasSetDbType` | `DbType`が設定済みかを表します。 |

### MachException

```cs
public class MachException : DbException
```

Machbaseで発生したエラーを表す例外クラスです。

#### フィールド

| 名前 | 説明 |
|--|--|
| `MachErrorCode` | 利用可能な場合のMachbaseエラーコードです。Universalプロバイダーが既存互換の例外を変換した場合は`0`になることがあります。 |

### MachAppendWriter

```cs
public sealed class MachAppendWriter
```

Appendプロトコル用の補助クラスです。`MachCommand.AppendOpen()`でインスタンスを取得します。

#### SetErrorDelegator

```cs
void SetErrorDelegator(ErrorDelegateFuncType callback)

void ErrorDelegateFuncType(MachAppendException e);
```

Append中のエラー時に呼び出すデリゲートを登録します。

#### フィールド

| 名前 | 説明 |
|--|--|
| `SuccessCount` | 保存に成功したレコード数です。`AppendClose()`後に確認できます。 |
| `FailureCount` | 失敗したレコード数です。`AppendClose()`後に設定されます。 |
| `Option` | `AppendOpen()`で使用した`MachAppendOption`値です。 |

### MachAppendException

```cs
public sealed class MachAppendException : MachException
```

Append中のエラー情報を追加提供する例外です。サーバーのエラーメッセージをそのまま伝え、
失敗したレコードを文字列で確認できます。

#### GetRowBuffer

```cs
string GetRowBuffer()
```

エラーが発生した元のレコードを文字列で返します。

## 使用例 {#usage-and-examples}

### 接続

次の例は環境変数のパスワードで接続し、LOGテーブルを作成・入力・検索してから削除します。

```csharp
using System;
using Mach.Data.MachClient;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
const string tableName = "NET_QUERY_DEMO";

using (var create = new MachCommand(
    $"CREATE LOG TABLE {tableName} (id INTEGER, name VARCHAR(40))", connection))
{
    create.ExecuteNonQuery();
}
try
{
    using (var insert = new MachCommand(
        $"INSERT INTO {tableName} VALUES (1, 'pump')", connection))
    {
        insert.ExecuteNonQuery();
    }
    using var query = new MachCommand($"SELECT id, name FROM {tableName}", connection);
    using var reader = query.ExecuteReader();
    while (reader.Read())
    {
        for (var column = 0; column < reader.FieldCount; column++)
        {
            Console.WriteLine($"{reader.GetName(column)} : {reader.GetValue(column)}");
        }
    }
}
finally
{
    using var drop = new MachCommand($"DROP TABLE {tableName}", connection);
    drop.ExecuteNonQuery();
}
```

### パラメーターバインディング

`MachParameterCollection`は`:name`、`@name`、`?name`プレースホルダーを処理します。
共通SQL構文と同じ`:name`形式を推奨します。名前検索は大文字・小文字を区別せず、同じ名前が繰り返されると
1つの値が全位置に適用されます。

`:name`形式はMachbase 8.7.0サーバーへの接続で使用します。旧サーバーでは`MachException`を返します。
`@name`と`?name`は既存プロバイダーの互換形式です。

```csharp
var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

const string sql = @"
    SELECT NAME
      FROM V$TABLES
     WHERE NAME = :table_name OR NAME = :table_name";

using var command = new MachCommand(sql, connection);

command.Parameters.AddWithValue(":table_name", "V$TABLES");

using var reader = command.ExecuteReader();
while (reader.Read())
{
    Console.WriteLine($"{reader.GetName(0)} : {reader.GetValue(0)}");
}
```

NULLは`DBNull.Value`で渡します。共通の名前構文は
[Named Bind Parameter syntax](../../reference/sql/syntax/named-bind-parameter-syntax/)を参照してください。

### Append

Appendプロトコルを使用すると、大量の時系列データを高速にロードできます。

```csharp
using System;
using System.Collections.Generic;
using Mach.Data.MachClient;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

const string tableName = "NET_APPEND_DEMO";
using (var create = new MachCommand(
    $"CREATE LOG TABLE {tableName} (ID INTEGER, NAME VARCHAR(40))", connection))
{
    create.ExecuteNonQuery();
}

try
{
using var appendCommand = new MachCommand(connection);
var writer = appendCommand.AppendOpen(tableName);
writer.SetErrorDelegator(error =>
    Console.Error.WriteLine($"Append row error: {error.Message}\n{error.GetRowBuffer()}"));

try
{
    for (var i = 1; i <= 100000; i++)
    {
        appendCommand.AppendData(writer, new List<object> { i, $"NAME_{i % 100}" });
        if (i % 1000 == 0) appendCommand.AppendFlush(writer);
    }
}
finally
{
    if (appendCommand.IsAppendOpened) appendCommand.AppendClose(writer);
}

Console.WriteLine($"Success Count : {writer.SuccessCount}");
Console.WriteLine($"Failure Count : {writer.FailureCount}");
if (writer.FailureCount != 0)
    throw new InvalidOperationException($"Append failed rows: {writer.FailureCount}");
}
finally
{
    if (connection.State == System.Data.ConnectionState.Open)
    {
        try
        {
            using var drop = new MachCommand($"DROP TABLE {tableName}", connection);
            drop.ExecuteNonQuery();
        }
        catch (Exception cleanupError)
        {
            Console.Error.WriteLine($"cleanup failed: {cleanupError.Message}");
        }
    }
}
```

### ARRAYと選択列Append

Machbase DBMS 8.7.0のfull/legacyプロバイダーはARRAYを`object[]`で返します。
要素NULLは配列内の`null`、配列全体のNULLは`IsDBNull()`で区別します。

通常の`AppendOpen(table)`でも、`MachSparseArray`をARRAY列の値として入力できます。

```csharp
var writer = append.AppendOpen("ARRAY_APPEND_FULL_EXAMPLE");
```

この場合、入力行はテーブルの列順序に従います。`ID LONG, A INT32[4]`テーブルにスパース値、
空のスパース配列、全体NULLを入力する
[通常Openの例](../data-input-load-export/array-append/#dotnet-full-open)では、
`AppendData()`からClose・結果確認まで説明しています。

`AppendOpen()`の`IList<string>`オーバーロードには、通常の列または`ARRAY_COLUMN[position]`を
渡せます。行ごとに異なる位置を入力する場合は、`MachSparseArray`を配列全体の対象に渡します。
要素位置を指定した対象と`MachSparseArray.Set()`の位置は0始まりです。

```csharp
using var append = new MachCommand(connection);
var writer = append.AppendOpen(
    "ARRAY_APPEND_EXAMPLE",
    new List<string> { "ID", "A" });
var sparse = new MachSparseArray(MachDBType.INT32_ARRAY, 4)
    .Set(1, 200)
    .Set(3, 400);

try
{
    append.AppendData(writer, new List<object> { 2L, sparse });
}
finally
{
    if (append.IsAppendOpened)
        append.AppendClose(writer);
}
```

空の`MachSparseArray`は全要素がNULLのARRAYで、`DBNull.Value`は配列全体のNULLです。
オーバーロードと全検証例は
[Sparse ARRAYと選択列Append API](../data-input-load-export/array-append/)を参照してください。

### Error Delegatorの設定

Append中の行エラーは、上の例のようにwriterを開いた直後にデリゲートで受け取り、close後に
成功・失敗件数を確認します。

### 自動AppendFlushの設定

AppendOpenは自動フラッシュスレッドを開始します。無効化するには、開いたwriterに対して
`connection.SetConnectAppendFlush(false)`を呼び出します。自動スレッドのエラーが直ちに公開例外として
通知されない場合があるため、明示的なflush・closeとコールバック・件数の確認を続けます。

## プロトコル4.0-fullの全API {#full-provider-apis-protocol-40-full}

`PROTOCOL=4.0-full`では拡張されたADO.NET APIを使用できます。8.0.55ソースパッケージの
4.0 limited connectorは3.1.3、4.0-full connectorは3.2.2です。インストール済みLinuxパッケージには
`$MACHBASE_HOME/lib/`にnet50版のみ含まれる場合があるため、別の対象フレームワークが必要なら
ソースビルドまたはNuGetの復元成果物を使用してください。

- `UniMachNetConnector-net50-8.0.55.dll` – DBMS Standard Linuxパッケージで一般的にインストールされる汎用エントリーポイント
- `machNetConnector-40-net50-3.1.3.dll` – プロトコル4.0 limited connector
- `machNetConnector-40-net50-3.2.2.dll` – プロトコル4.0-full connector

### 4.0-fullで追加された主な型

- `MachDbProviderFactory`: 不変名`Mach.Data`でプロバイダーを登録・作成できます。
- `MachConnectionStringBuilder`: キーワードの入力誤りを避けて接続文字列を構成できます。
- `MachDataAdapter`、`MachRowUpdating`、`MachRowUpdated`: `DataTable`/`DataSet`のワークフローをサポートします。
- `MachCommandBuilder`: SELECT文からINSERT/DELETE（条件によりUPDATE）文を自動生成します。
  自動生成SQLが対象テーブルのDML制約に適合するか、実行前に確認します。

### 全APIの有効化

```csharp
var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString =
    $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
```

UPDATE/DELETEが必要な場合は、テーブルタイプ別の条件とドライバーのSQL生成範囲を合わせて確認します。
LOGはUPDATEをサポートしません。Machbase DBMS 8.7.0 Standard EditionのTAG UPDATEにはNAMEと
BASETIME条件が必要なため、汎用CommandBuilderのSQLに依存せず、
[TAG UPDATE構文](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-syntax/)に合うコマンドと
バインディングを使用します。

### 接続文字列ビルダーの使用

```csharp
var builder = new MachConnectionStringBuilder
{
    Server = "127.0.0.1",
    Port = 5656,
    UserID = "SYS",
    Password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
        ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required")
};

builder["PROTOCOL"] = "4.0-full";

using var connection = new MachConnection(builder.ConnectionString);
connection.Open();
```

### 例: MachDataAdapterでSQL INSERT

LOOKUPテーブルを`DataTable`へ取り込んで新しい行を追加すると、CommandBuilderが通常のSQL INSERTを
実行します。この経路はAppendプロトコルではありません。

```csharp
using Mach.Data.MachClient;
using System;
using System.Data;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString =
    $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

using (var create = new MachCommand(
    "CREATE LOOKUP TABLE dotnet_lookup_demo (id INTEGER PRIMARY KEY, name VARCHAR(80))",
    connection))
{
    create.ExecuteNonQuery();
}

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

adapter.MachRowUpdating += (sender, args) =>
{
    Console.WriteLine(
        $"About to run {args.StatementType} with SQL: {args.Command?.CommandText}");
};

adapter.Update(table);

using var drop = new MachCommand("DROP TABLE dotnet_lookup_demo", connection);
drop.ExecuteNonQuery();
```

> **ヒント**: 送信前にSQLを確認するには、上記のように`Update()`前にイベントを購読してください。

### 例: DbProviderFactoryの活用

`MachDbProviderFactory.Instance`を使用すると、`DbProviderFactories`、Dapperなどプロバイダーに
依存しない構成にMachbaseを接続できます。

```csharp
using System;
using System.Data.Common;
using Mach.Data.MachClient;

DbProviderFactory factory = MachDbProviderFactory.Instance;

using DbConnection connection = factory.CreateConnection()!;
var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
connection.ConnectionString =
    $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
connection.Open();

using DbCommand command = connection.CreateCommand();
command.CommandText = "SELECT COUNT(*) FROM V$TABLES";
var count = (long)command.ExecuteScalar();

Console.WriteLine($"Visible tables: {count}");
```

設定ベースのアプリケーションでファクトリーを自動公開するには、起動時に
`MachDbProviderFactory.Register()`を1回呼び、`DbProviderFactories.GetFactory("Mach.Data")`が
同じインスタンスを返すように構成してください。

`4.0-full`プロトコルはMachbase 7.x以降のサーバーでのみ使用できます。それより前のバージョンでは
`PROTOCOL=4.0`（制限された機能）または2.x/3.xプロトコルを使用する必要があります。
