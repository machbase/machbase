---
type: docs
title: '9.1 概要と選択基準'
weight: 10
toc: true
---

LOOKUPテーブルは、基準コード、機器マスター、しきい値、設定値など、比較的小規模で頻繁に参照されるデータを保存します。
データは永続保存されますが、SQL検索に使用する全行はメモリに常駐します。
そのため、繰り返し行うキーによる検索と更新に適しています。

<a id="overview-lookup-characteristics"></a>

## LOOKUPテーブルの特性

LOOKUPテーブルは`CREATE LOOKUP TABLE`文で作成し、`PRIMARY KEY`が必須です。

```sql
CREATE LOOKUP TABLE ch9_overview (
    sensor_id VARCHAR(64) PRIMARY KEY,
    site      VARCHAR(32),
    unit      VARCHAR(16),
    status    VARCHAR(16)
);
```

LOOKUPテーブルの主な特性は次のとおりです。

| 項目 | 内容 |
|------|------|
| 主な用途 | コードテーブル、機器マスター、しきい値、参照データ |
| 必須条件 | `PRIMARY KEY`が必要 |
| 保存方式 | 永続保存し、サーバー起動時に全行をメモリへロード |
| 検索パターン | PK検索に最適化。一般条件検索と他のテーブルとのJOINをサポート |
| 変更パターン | INSERT、UPDATE、DELETE |
| 追加機能 | SEQUENCE列、Appendの重複キーポリシー |

<a id="overview-lookup-use-criteria"></a>

## 選択基準

次の条件に該当する場合は、LOOKUPテーブルを使用します。

- データ件数が比較的小さく、全体が頻繁に参照される。
- 全行と必要なセカンダリインデックスをサーバーメモリに保持できる。
- コード、名前、場所、単位、状態などのマスターデータを管理する。
- TAGまたはLOGの元データに説明情報をJOINする必要がある。
- しきい値や設定値など、運用中に変更される参照値を保存する。
- `PRIMARY KEY`で行を明確に識別できる。

TAGまたはLOGデータに場所や単位などの説明を付加するJOIN例は、
[クエリと分析](/dbms/lookup-table-usage/query-analysis/)で説明します。

<a id="overview-lookup-not-use"></a>

## 他のテーブルを検討する場合

次の要件には、他のテーブルタイプを検討します。

| 要件 | 推奨テーブル |
|----------|-------------|
| 大量の時系列計測データの保存 | TAG |
| 追加中心の元イベントの保存 | LOG |
| 全行のメモリロードが困難な大規模リレーショナルデータ | TRANSACTION |
| トランザクションとリレーショナルな業務処理が必要なデータ | TRANSACTION |
| サーバーメモリだけで維持する最新状態キャッシュ | VOLATILE |

LOOKUPテーブルは参照データに適していますが、永続保存されることを理由にディスク中心の大容量テーブルとして使用しないでください。
元データはLOGまたはTAGに保存し、LOOKUPにはメモリに常駐させて繰り返し検索するマスターデータを格納します。
リレーショナルデータがメモリ容量を超える場合や、複雑な業務処理が必要な場合はTRANSACTIONテーブルを使用します。

この節の実習テーブルは、次のように削除します。

```sql
DROP TABLE ch9_overview;
```

<a id="overview-lookup-design-flow"></a>

## 設計手順

LOOKUPテーブルの設計では、次の順序で決定します。

1. 行を識別する`PRIMARY KEY`を決めます。
2. 自然キーか、SEQUENCEまたはAUTO_INCREMENTに基づく代理キーかを決めます。
3. 頻繁に検索・JOINする列にインデックスを追加します。
4. 想定行サイズ・行数と、セカンダリインデックスを含むメモリ使用量を検証します。
5. 運用中に更新する列と不変の列を区別します。
6. 大量変更の前に、対象範囲を確認するクエリを用意します。

スキーマとキーの設計は、[テーブル構造とスキーマ](/dbms/lookup-table-usage/table-structure-schema/)と
[PRIMARY KEYポリシー](/dbms/lookup-table-usage/primary-key-policy/)で説明します。
