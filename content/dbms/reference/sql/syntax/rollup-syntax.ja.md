---
type: docs
title: 'ROLLUP'
weight: 180
toc: true
---

ROLLUPは時間軸TAGの繰り返し集計を保存・参照する機能です。通常・条件付き・拡張ROLLUPは
公開の`rollup()`関数で参照し、Customはユーザーの出力先TAGを再集計して参照します。

<a id="create-rollup"></a>

## 作成

次は構文の表記です。角括弧や波括弧をそのまま実行しないでください。

```text
CREATE ROLLUP [IF NOT EXISTS] name
    ON source_tag [(column_name | json_path_expression)]
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }]
    [EXTENSION]
    [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] name
    FROM source_rollup
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }]
    [EXTENSION]
    [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] name
    INTO (destination_tag)
    AS (SELECT ...)
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }];
```

- EXTENSIONはキーワードのみを記述し、extension_nameは付けません。
- CREATEの時間単位はSEC/MIN/HOURです。DAYなどのクエリ単位とは区別します。
- 通常の数値列はSUMMARIZEDなしで明示できます。JSONパス集計とドキュメント全体の集計は異なり、ドキュメント全体とWITH ROLLUPによる自動作成にはSUMMARIZED条件があります。
- FROMの間隔はソースより大きな整数倍であり、拡張属性と集計モードが一致する必要があります。
- WAKEUPは正数で、集計間隔以下であり、その間隔を割り切れる必要があります。
- CustomはStandard専用です。ソースTAGが1つと事前作成済みの出力先TAGが必要です。WHEREはSELECT内に記述し、BASETIMEの直接条件・JOIN・FROMサブクエリは許可しません。
- IF NOT EXISTSは既存名の場合に作成を省略する機能であり、定義の変更、比較、一致処理は行いません。構文とソースの検証をすべて省略するオプションでもありません。

<a id="drop-rollup"></a>

## 削除

```sql
DROP ROLLUP rollup_name;
```

参照元となる上位ROLLUPから削除します。Custom出力先TAGは、関連ジョブが残っているとDROPが拒否されます。
元のTAGのCASCADEは関連ROLLUPの削除範囲を確認してから使用し、ユーザーのCustom出力先テーブルは
別のライフサイクルで管理します。

<a id="alter-rollup"></a>

## 制御

```sql
ALTER ROLLUP rollup_name STOP;
ALTER ROLLUP rollup_name START;
ALTER ROLLUP rollup_name WAKEUP;
ALTER ROLLUP rollup_name FORCE;
ALTER ROLLUP rollup_name SET WAKEUP INTERVAL 10 SEC;
```

これらのコマンドは、既存ジョブと有効な間隔条件を前提とします。作成時に自動開始し、すでに開始・停止済みの
状態を繰り返し指定するとエラーになる場合があります。WAKEUPは完了を待たず、FORCEは対象がソースの
処理範囲に追いつくまで待機します。過去のソースの補正では、[REBUILD固有のサポート範囲](../rollup-rebuild-syntax/)を確認します。

## クエリと候補の選択

```text
rollup(time_unit, period, basetime_column [, origin])
```

戻り値の型はDATETIMEです。periodは正の整数リテラルです。通常のDATE_TRUNC + GROUP BYクエリは、
ROLLUPが存在するだけでは自動的に切り替わりません。ROLLUPの参照には`rollup()`を明示し、適用可能な
候補がなければ別途ソースデータのクエリを使用します。

自動選択では、同じ列・パス・モードで条件なしの候補を先に探し、使用可能な最大の間隔を選びます。
同じ間隔では登録順序が影響します。通常/拡張だけで優先順位を断定しないでください。
特定のデータ集合に固定するにはROLLUP_TABLEヒントを使用します。

SEC/MINの候補間隔はperiod秒/分を基準に確認します。HOUR・DAY・WEEK・MONTH・YEARは候補選択時に
period時間を基準に確認します。これは結果バケットの暦計算とは別の規則です。
月・年のoriginでは、月の1日であるという条件を確認してください。

SELECTでnameを返すタグ別集計は、GROUP BYにもnameを含めます。時間範囲・origin・NULL処理・候補条件を
そろえてから元データの結果と比較します。通常の数値ROLLUPはMIN/MAX/SUM/COUNT/AVG/SUMSQ、
拡張ROLLUPはFIRST/LASTもサポートします。元データに対するFIRST/LASTの使用と保存ROLLUPの拡張要件は
区別してください。JSONドキュメント全体のCOUNTとパス別の件数は別の規則です。

実行可能な作成・参照・エラーの例は、[第6章 ROLLUPの利用](/dbms/tag-rollup-usage/)と
[クエリ構文](/dbms/tag-rollup-usage/query-syntax-rollup/)を参照してください。
