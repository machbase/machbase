---
type: docs
title: '10.1 概要と選択基準'
weight: 10
toc: true
aliases:
  - /dbms/volatile-table-usage/patterns-scenarios/
  - /dbms/volatile-table-usage/state-cache-temporary-aggregation/
---

VOLATILEテーブルは、データをメモリに保存する一時テーブルです。
サーバーを再起動するとデータが消失するため、再作成可能な最新状態、一時集計、セッション間の共有キャッシュに使用します。

<a id="overview-volatile-characteristics"></a>

## VOLATILEテーブルの特性

VOLATILEテーブルは`CREATE VOLATILE TABLE`文で作成します。

```sql
CREATE VOLATILE TABLE ch10_overview (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);
```

VOLATILEテーブルの主な特性は次のとおりです。

| 項目 | 内容 |
|------|------|
| 主な用途 | 最新状態のキャッシュ、一時集計、中間結果 |
| 保存場所 | メモリ |
| 再起動後のデータ | 消失 |
| 共有範囲 | サーバー全体で共有 |
| キー | PRIMARY KEYは任意 |
| 主な機能 | UPDATE、DELETE、`ON DUPLICATE KEY UPDATE`、赤黒木インデックス |
| バックアップ | 未サポート |

<a id="overview-volatile-use-criteria"></a>
<a id="use-cases-volatile"></a>

## 選択基準

次の条件に該当する場合は、VOLATILEテーブルを使用します。

- サーバー再起動後にデータが失われても問題がない。
- 元データからいつでも再計算または再構築できる。
- 最新状態、直近の集計、一時処理結果を高速に検索する必要がある。
- 複数のセッションで同じ一時状態を共有する必要がある。
- ディスクの永続性より、メモリによる応答時間を重視する。

最新のセンサー状態を維持する例は次のとおりです。

```sql
INSERT INTO ch10_overview VALUES ('TEMP-01', 23.5, NOW)
ON DUPLICATE KEY UPDATE SET value = 23.5, updated_at = NOW;

SELECT *
FROM ch10_overview
WHERE sensor_id = 'TEMP-01';

-- 次の節で同じ名前を使うため、削除します。
DROP TABLE ch10_overview;
```

### 活用パターン

| パターン | key | 再作成元 | 推奨する期限管理方法 |
|------|-----|-------------|----------------|
| 機器の最新状態 | 機器ID | TAGまたはLOG | 同じkeyを更新 |
| 短周期の集計 | 対象と時間bucket | TAGまたはLOG | bucketの置き換えまたは再構築 |
| 処理の進行状態 | ジョブID | ジョブシステム | 完了後にkeyを削除 |
| 一時クエリキャッシュ | リクエストまたはオブジェクトID | 永続テーブル | 全体を再構築 |

最新状態の更新は[データ入力と変更](../data-input-mutation/)、
一時集計は[クエリと分析](../query-analysis/)を参照してください。

<a id="overview-volatile-not-use"></a>

## 他のテーブルを検討する場合

次の要件には、他のテーブルタイプを使用します。

| 要件 | 推奨テーブル |
|----------|-------------|
| 再起動後も必ず保持する元データ | TAGまたはLOG |
| 基準コードや機器マスターなどの永続的な参照データ | LOOKUP |
| トランザクションとリレーショナルな更新が必要な業務データ | TRANSACTION |
| 長期分析対象の時系列データ | TAG |

VOLATILEテーブルだけに保存したデータは、サーバー終了時に復旧できません。
重要なデータはTAG、LOG、LOOKUP、TRANSACTIONから適切な永続テーブルを選んで保存し、
VOLATILEテーブルはキャッシュや中間結果に使用します。

<a id="overview-volatile-design-flow"></a>

## 設計手順

VOLATILEテーブルの設計では、次の順序で決定します。

1. データを再作成できることを確認します。
2. PRIMARY KEYが必要かを決めます。
3. 想定行数とメモリ使用量を見積もります。
4. 再起動後の初期ロード手順を用意します。
5. 保持が必要な結果は、アプリケーションの明示的な書き込みで永続テーブルに保存します。
   VOLATILEを永続化する専用のflushコマンドはありません。

スキーマとPRIMARY KEYの設計は[テーブル構造とスキーマ](/dbms/volatile-table-usage/table-structure-schema/)、
再起動への対応は[再起動とデータ消失](/dbms/volatile-table-usage/operations-lifecycle/)で説明します。
