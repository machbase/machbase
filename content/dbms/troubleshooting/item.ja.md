---
type: docs
title: '15.3 入力とロードの問題'
weight: 30
toc: true
---

<a id="failure"></a>

## 入力が失敗する場合

クライアントのエラー全文、対象データベース・テーブル、入力方式、最後の成功行を記録します。
コードの意味は[エラーコードリファレンス](/dbms/reference/error-codes/)で確認し、
このページの固定コード表に依存しないでください。

```sql
DESC target_table;
SELECT NAME, TYPE, COLCOUNT
  FROM M$SYS_TABLES
 WHERE NAME = 'TARGET_TABLE';
```

次を確認します。

- 入力列数・順序・型と NULL 許可
- 現在のデータベースとテーブル所有者
- ユーザーの `CONNECT` とテーブルの `INSERT` 権限
- 時刻文字列の形式と接続タイムゾーン
- ファイルシステムの空き容量と `V$STORAGE_USAGE`
- Append API の戻り値、失敗行、flush 結果

時刻が逆順の入力や UPDATE/DELETE 条件はタイプによって異なるため、各利用章の制約を確認します。

<a id="failure-csv-import"></a>

## CSV インポートが失敗する場合

現在の配布版のオプションは `machloader -h` で確認します。

```bash
machloader -h
machloader -s 127.0.0.1 -P 5656 -u app_user \
  -t target_table -i /data/input.csv \
  -b /data/input.bad -l /data/input.log
```

小さいファイルから、次の順に再現します。

1. サーバーではなく loader 実行ホストの絶対パスとファイル権限を確認します。
2. CSV の1行の列数と `DESC target_table` を比較します。
3. エンコーディング名を現行ヘルプと比較します。配布版には `UTF8`、`MS949`、`KSC5601`、`EUCJP` などがあります。
4. 区切り文字と引用符のオプションを実ファイルに合わせます。
5. 日時形式オプションには対象列名と形式を併せて指定します。
6. bad ファイルの最初の失敗行を修正し、別の検証テーブルへロードします。

正確な `-F` 構文とオプションは
[machloader コマンド・オプションリファレンス](/dbms/reference/command-line-tools/machloader/)を使ってください。
部分成功後の再試行では、入力済み範囲を確認して重複を防ぎます。
