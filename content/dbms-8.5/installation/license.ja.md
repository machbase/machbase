---
title : 'ライセンスのインストール'
type : docs
weight: 40
toc: true
---

通常、MACHBASE のインストール後にライセンスキーを導入します。ライセンスを導入しない場合でも、制限付きで利用できます。本節では、ライセンスポリシー、ファイル構成、導入方法を説明します。


## ライセンスファイルの構成 {#license-file-structure}

MACHBASE のライセンスは license.dat で管理します。製品用または評価用のライセンス情報がテキスト形式で記載されています。

```bash
mach@localhost:~$ cat license.dat 
 
\#License ID: 00000001
\#Issue DATE: 20991231
\#License Type\(Version 3\): FOGUNLIMITED
\#Company: MACHBASE
\#Project\(Product\): NONE
\#Country Code: KR
 dXlIm7cdJjV1eUibtx0mNQ-GMxH+xLveLI-ewu63w8qMx33l77I+Ot0hY9sBCI...
```


## ライセンスファイルがない場合 {#no-license-file}

ライセンスがなくてもサーバーは動作しますが、制限があります。この場合は評価目的にのみ利用できます。本番で利用する場合は、正規の手続きでライセンスを取得してください。

ライセンスファイルがない場合、次の制限が適用されます。

    1. 1 セッションで Append プロトコルにより 1 億件を超えるレコードを入力すると、警告が表示され、Append 入力が停止します。この制限状態は、サーバーを再起動した場合にのみ解除されます。

    2. テーブルスペースの作成時に、ディスクディレクトリを 2 つ以上作成できません。複数のディスクを使用すると、高速入力のための並列 I/O 機能を利用できないことを示す警告が表示されます。

```bash
CREATE TABLESPACE tbs1 DATADISK disk1 (disk_path="tbs1_disk1"), disk2 (disk_path="tbs1_disk2"), disk3 (disk_path="tbs1_disk3");
[ERR-00867 : Error in adding disk to tablespace. You cannot use multiple disks for tablespace without valid license.]
```


## ライセンスのインストール {#license-installation}

ライセンスは `$MACHBASE_HOME/conf` に配置します。既定のファイル名は license.dat です。

ライセンスファイルを `$MACHBASE_HOME/conf` にコピーします。

発行されたファイルの名前を **license.dat** に変更してコピーしてください。サーバーの起動時にライセンスの有効性を確認して適用します。

**machadmin -t 'licensefile_path'** を実行します。

この方法では、ファイル名や配置場所を変更せずにコマンドで簡単に導入できます。

クエリーによるインストール：サーバーの稼働中にクエリー文でライセンスを導入できます。


## ライセンスの確認 {#verifying-license-installation}

### インストール済みの場合 {#license-installed}

ライセンスが導入されている場合、サーバー起動後の machbase.trc に次の情報が表示されます。

```bash
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [License ID] [00000001]
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [Issue DATE] [20991231]
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [License Type(Version 3)] [FOGUNLIMITED]
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [Company] [MACHBASE]
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [Project(Product)] [NONE]
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [Country Code] [KR]
```

`machadmin -f` コマンドでも確認できます。

### 未インストールの場合 {#license-not-installed}

ライセンスファイルがない場合や無効な場合は、`machadmin -f` または `V$LICENSE_INFO` で状態を確認します。Standard 8.5 でも同じ Version 3 のフィールドを使用し、違反の詳細は `V$LICENSE_INFO` の `VIOLATE_STATUS` 列と `VIOLATE_MSG` 列に表示されます。

```sql
SELECT ID, ISSUE_DATE, TYPE, CUSTOMER, PROJECT, COUNTRY_CODE,
       INSTALL_DATE, VIOLATE_STATUS, VIOLATE_MSG
FROM V$LICENSE_INFO;
```
