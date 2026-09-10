---
type: docs
title: '8.1 概要と選択基準'
weight: 10
toc: true
aliases:
  - /dbms/rdb-table-usage/patterns-scenarios/
---

機器の測定値は継続的に蓄積されますが、点検状態や在庫数量は既存値を変更する必要があります。
両方を同じモデルで処理すると、元データの保持と状態変更の要件が混在しがちです。
変更可能な業務データをTRANSACTIONに、元の時系列データをTAG・LOGに格納する構成を先に検討してください。

<a id="overview-rdb-characteristics"></a>

<a id="수정과-관계형-조회가-필요한-데이터에-사용합니다"></a>

## TRANSACTIONテーブルの特性

TRANSACTIONはSELECT・INSERT・UPDATE・DELETE、PRIMARY KEY、UNIQUE INDEX、セカンダリインデックスをサポートします。
Standard Edition専用で、次の3つの構文は同じテーブルを作成します。

| 構文 | 意味 |
|---|---|
| CREATE TABLE | タイプを省略したデフォルトのTRANSACTION作成 |
| CREATE TRANSACTION TABLE | タイプを明示した作成 |
| CREATE TXN TABLE | 短縮形による作成 |

公開文書と運用スクリプトでは、タイプが明確なCREATE TRANSACTION TABLEを推奨します。
CREATE RDB TABLE・CREATE TRX TABLEはサポートしていません。
Clusterでは上の3つの作成構文をすべて使用できません。LOGはCREATE LOG TABLEで明示します。

<a id="overview-rdb-use-criteria"></a>
<a id="use-cases-rdb"></a>

<a id="상태-변경을-작은-예제로-확인합니다"></a>

## 状態変更とロールバック

```sql
CREATE TRANSACTION TABLE ch8_overview (
    item_id LONG PRIMARY KEY,
    qty     INTEGER NOT NULL
);
INSERT INTO ch8_overview VALUES (42, 10);

BEGIN;
UPDATE ch8_overview SET qty = qty - 3 WHERE item_id = 42 AND qty >= 3;
SELECT item_id, qty FROM ch8_overview;
ROLLBACK;

SELECT item_id, qty FROM ch8_overview;
DROP TABLE ch8_overview;
```

同じ接続では、トランザクション内の検索は数量7、ROLLBACK後の検索は10を返します。
`qty >= 3`は、在庫不足の場合に変更しないための業務条件です。

UPDATEがエラーなしで終了すれば業務も成功した、と判断しないよう注意してください。
条件に一致する行がなければ、変更件数は0になり得ます。
アプリケーションでは影響行数が想定した1であることを確認し、次の処理かロールバックかを決める必要があります。
SQL例の数値を置き換えることより、この確認手順が重要です。

<a id="overview-rdb-not-use"></a>

<a id="원본-참조-정보-업무-상태를-구분합니다"></a>

## 他のテーブルとの比較

| 主な要件 | 最初に検討するテーブル |
|---|---|
| センサー名ごとの測定値とROLLUP | TAG |
| 更新しないログ・イベントの元データ | LOG |
| 小規模な現在のマスターデータ | LOOKUP |
| リレーショナルなDMLと明示的トランザクション | TRANSACTION |
| 再起動後に消失してもよいメモリ上の状態 | VOLATILE |

TRANSACTIONには、機器の点検状態、業務履歴、別途作成した要約結果などを格納できます。
大量の元データの収集では、TAG・LOGとスループット・取り込み方法を比較してください。
TRANSACTIONもAppendをサポートしますが、TAG・LOGと同じスループットやバッチ境界を前提にしないでください。
[取り込み方式](../data-input-mutation/)で具体的に区別します。

LOOKUPは、TRANSACTIONの全機能を代替するテーブルではありません。
Clusterでリレーショナルトランザクションが必須の場合は、別のRDBMSを含む構成を検討する必要があります。

<a id="overview-rdb-design-flow"></a>

<a id="키와-실패-처리부터-설계합니다"></a>

## 設計基準

1行を識別するキーと、重複を防ぐ業務キーを区別してください。
内部番号にはPRIMARY KEY、外部システムのコードなど別の一意値にはUNIQUE INDEXが必要な場合があります。
自動採番を使用しても、業務キーの重複は自動的には防げません。

続いて、頻繁に実行するWHERE条件と業務の成功基準を決めます。
トランザクションの終了位置とエラー時の確認事項まで決めておくと、同時要求や接続障害が発生しても対応を一貫させられます。
[スキーマ](../table-structure-schema/)と[トランザクション](../transaction/)を併せて確認してください。
