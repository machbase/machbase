---
type: docs
title: '16.1.6 ROWID'
weight: 60
toc: true
aliases:
  - /dbms/application-integration/rowid-generated-id/
  - /dbms/development-tools-integration/rowid-generated-id/
---

<span class="badge-since">Machbase 8.7.0以降でサポート</span>

`ROWID`はテーブル内の1行を再検索するための64ビット識別子です。このページではSQLでの意味、
テーブル別の参照条件、INSERTの実行結果、有効期間を定義します。SDK別のアクセスAPIとコードは、
[SDK機能のサポート範囲](/dbms/development-tools-integration/sdk-support-scope/)と各言語のページを参照してください。

この機能はStandard Editionでサポートします。サーバーとSDKをROWIDに対応するバージョンへ一緒に
更新してください。Cluster Editionでは使用できません。

## ROWIDと業務キーの区別

ROWIDは現在のテーブルの保存行の位置を示す識別子であり、注文番号や機器IDなどの永続的な業務キーではありません。

- 通常の列ではないため`SELECT *`には含まれません。必要な場合は明示的に選択してください。
- 他のテーブルのROWIDと比較したり、他のテーブルの参照に使用したりしないでください。
- ROWID値を分解したり算術演算に使用したりしないでください。
- 数値の大小はテーブル全体の取り込み順序を意味しません。
- 新規テーブルには`ROWID`という実列を定義できません。
- 旧バージョンで実際の`ROWID`列を作成したテーブルでは、その列を優先します。ROWID疑似列を使用するには既存列の名前を変更してください。

```sql
SELECT ROWID, name, time, value
  FROM sensor_tag
 WHERE name = 'TAG-01';
```

## テーブル別のサポート範囲

| テーブル | ROWIDの意味 | 参照条件 | 単一行INSERTの結果 |
|--------|--------------|-----------|------------------|
| LOG | 保存されたログ行の識別子 | `=`, `<`, `<=`, `>`, `>=`, `BETWEEN`, `ORDER BY` | 生成されたROWIDを返す |
| TAG | 保存された元のTAG行の識別子 | 最上位の`AND`に含む単一の`ROWID = 値` | 生成されたROWIDを返す |
| TRANSACTION | 単一の`LONG`/`INT64` PRIMARY KEY値 | 既存PKがサポートする条件 | PK値をROWIDとして返す |
| LOOKUP | 単一の`LONG`/`INT64` PRIMARY KEY値 | 既存PKがサポートする条件 | PK値をROWIDとして返す |
| VOLATILE | 単一の`LONG`/`INT64` PRIMARY KEY値 | 既存PKがサポートする条件 | PK値をROWIDとして返す |

TRANSACTION、LOOKUP、VOLATILEでは、`AUTO_INCREMENT`の使用に関係なく、値が`0`以上の単一
`LONG`/`INT64` PRIMARY KEYをROWIDとして使用します。アプリケーションがPK値を指定した場合はその値を、
`AUTO_INCREMENT` PKを省略またはNULLにした場合はサーバーが生成した値を返します。負数のPKはROWIDとして使用できません。

LOGとTAGのROWIDは`0..UINT64_MAX-1`、3つのPRIMARY KEYベースのテーブルは`0..INT64_MAX`の範囲です。
`0`は有効な値で、`UINT64_MAX`はROWIDとして使用できません。

### LOGの参照

LOGのROWIDは範囲参照とソートに使用できます。`_ARRIVAL_TIME`は複数行で同じ値になる場合があるため、
特定行の再検索にはROWIDを使用します。

```sql
SELECT ROWID, message
  FROM app_log
 WHERE ROWID >= ?
   AND ROWID < ?
 ORDER BY ROWID;
```

`ROWID IN (...)`はサポートしません。

### TAGの参照

TAGは単一ROWIDの等値参照のみをサポートします。タグ名、時刻、値の条件を`AND`で併用でき、
すべての条件を満たす行だけを返します。

```sql
SELECT ROWID, name, time, value
  FROM sensor_tag
 WHERE ROWID = ?
   AND name = 'TAG-01'
   AND time >= TO_DATE('2026-08-10 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

TAG ROWIDの条件のサポート可否は次のとおりです。

| 使用方法 | サポート |
|--------|:---------:|
| `ROWID = ?` | O |
| `ROWID > ?`、`BETWEEN`などの範囲条件 | X |
| `ROWID IN (...)` | X |
| `ROWID = ? OR ...` | X |
| `ORDER BY ROWID` | X |
| `DELETE ... WHERE ROWID = ?` | X |
| rollup、custom rollup、statの結果との組み合わせ | X |

### TRANSACTION、LOOKUP、VOLATILEの比較

次の3つのテーブルは同じ`AUTO_INCREMENT`宣言を使用できますが、再起動時の動作と取り込み機能は異なります。

```sql
CREATE TRANSACTION TABLE orders (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);

CREATE LOOKUP TABLE lookup_orders (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);

CREATE VOLATILE TABLE volatile_orders (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);
```

| 項目 | TRANSACTION | LOOKUP | VOLATILE |
|------|-------------|--------|----------|
| 再起動後に行と次の自動値を保持 | O | O | X |
| 明示的トランザクション | O | X | X |
| `INSERT ... SELECT`で自動値を生成 | O | X | X |
| AUTO_INCREMENTテーブルのUPSERT | O (ROWID返却はX) | X | X |
| 単一行`INSERT ... VALUES`の結果ROWID | O | O | O |

LOOKUPの`PROPERTY(SEQUENCE)`と`NEXTVAL()`は`AUTO_INCREMENT`とは別の機能です。
同じ列に両方式を指定しないでください。

明示的トランザクション中はTRANSACTIONテーブルのDDLを実行できません。`CREATE TRANSACTION TABLE`が
`ERR-02362`で失敗したら、先に`COMMIT`または`ROLLBACK`してから再実行します。

### JOIN、集約、View

JOIN結果全体を代表するROWIDはありません。必要なソーステーブルの別名ごとにROWIDを参照します。

```sql
SELECT a.ROWID AS order_rowid,
       b.ROWID AS item_rowid,
       a.customer, b.item
  FROM orders a JOIN order_items b ON a.id = b.order_id;
```

| 参照形式 | ROWIDの処理 |
|-----------|------------|
| JOIN | 必要なソーステーブルの別名ごとに`alias.ROWID`を指定 |
| 集約、`GROUP BY`、`DISTINCT`、集合演算 | 結果行に新しいROWIDを生成しない |
| View, CTE, inline view | 内部SELECTでROWIDを明示的に選択した場合のみ伝播 |

## INSERT結果でROWIDを受け取る条件

`INSERT ... RETURNING ROWID`構文は使用しません。対応するSDKは、成功した単一行の
`INSERT ... VALUES`の実行結果にROWIDも含めて返します。

| 取り込み方法 | generated ROWID | 説明 |
|-----------|:---------------:|------|
| 単一行の直接`INSERT ... VALUES` | O | 1行の作成が成功した場合 |
| 単一行のプリペアドINSERT | O | 実行ごとに現在の結果を返す |
| `INSERT ... SELECT` | X | 複数行を作成する可能性があるため単一値を返さない |
| execute-array, batch, `executemany()` | X | 内部の最終行を代表値として公開しない |
| Append API, append batch | X | 高速取り込み経路では返さない |
| loader | X | ファイル取り込み経路では返さない |
| UPSERT | X | INSERTまたはUPDATEの結果を単一ROWIDで代表しない |
| 失敗したINSERT | X | 前回の実行のROWIDも消去 |

生成されたROWIDはステートメントごとの結果です。接続全体の最新値を参照するSQL関数は提供しません。

## 参照結果とエラーの区別

形式が正しいROWIDが現在のテーブルになければ、エラーではなく0行を返します。削除済みの行や追加条件を
満たさない行も同様です。一方、NULL、負数のPK、`UINT64_MAX`、数値へ変換できない値、TAGで非対応の
範囲・IN・OR・ソート条件はエラーです。

## 有効期間と再試行

ROWIDを長期保存する業務キーとして使用しないでください。

| 状況 | 既存のROWID |
|------|------------|
| 正常な再起動 | 保持された行では維持 |
| ROWIDの保持に対応する製品のバックアップ/復元 | 保持された行では維持 |
| 行のDELETE | 無効 |
| transaction ROLLBACK | 該当INSERTのROWIDは無効 |
| スナップショット復旧で破棄された行 | 無効 |
| LOG TRUNCATE | 以前の値が再利用される場合がある |
| テーブルのDROP後の再作成 | 以前の値が別の行を指す場合がある |
| エクスポート/インポートまたは行の再挿入 | 保持しない |

INSERTが成功してもネットワーク応答が失われると、アプリケーションがROWIDを受け取れない場合があります。
同じINSERTを自動再試行すると重複行が生じる可能性があるため、業務キーや別途の冪等性ポリシーで
実際の反映状態を先に確認してください。

## 関連ドキュメント

- [SDK機能のサポート範囲](/dbms/development-tools-integration/sdk-support-scope/)
- [AUTO_INCREMENT](/dbms/reference/sql/syntax/auto-increment-syntax/)
- [LOGデータの取り込み](/dbms/log-table-usage/data-input-mutation/)
- [TAGデータの取り込み](/dbms/tag-table-usage/data-input-mutation/)
