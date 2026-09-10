---
type: docs
title: '16.6.2 テーブルタイプ別機能サポート表'
weight: 20
toc: true
aliases:
  - /dbms/data-modeling-table-design/table-types-type-manageable/
---

Machbaseは用途に応じて5種類のテーブルタイプを提供します。設計目的により、各タイプのサポート範囲は異なります。

## テーブルタイプの概要

| テーブルタイプ | 主な用途 |
|------------|----------|
| **TAG** | 時系列センサーデータの高速収集と集計（ROLLUP） |
| **LOG** | ログ・イベントを定義済み列へ順次保存、テキスト検索 |
| **LOOKUP** | メタデータ、コードテーブル、参照データ（UPDATE/DELETE対応） |
| **VOLATILE** | メモリ上のサーバー状態・キャッシュ。再起動時にデータ消失 |
| **TRANSACTION** | トランザクションが必要な一般的なリレーショナルデータ |

## テーブルタイプ別機能サポート一覧

| 機能 | TAG | LOG | LOOKUP | VOLATILE | TRANSACTION |
|------|:---:|:---:|:------:|:--------:|:---:|
| **書き込み** | | | | | |
| INSERT (SQL) | O | O | O | O | O |
| **更新/削除** | | | | | |
| UPDATE | △ | X | O | O | O |
| DELETE | O | O | O | O | O |
| **トランザクション** | | | | | |
| Transaction (COMMIT/ROLLBACK) | X | X | X | X | O |
| **集計と検索** | | | | | |
| ROLLUP | O | X | X | X | X |
| テキスト検索 (KEYWORD INDEX) | X | O | X | X | X |
| **JSON** | | | | | |
| JSON 列 | O | O | O | X | O |
| JSON path query | O | O | O | X | O |
| **固定小数点** | | | | | |
| DECIMAL / NUMERIC 列 | O | O | O | O | O |
| **固定長ARRAY** | | | | | |
| ARRAY列の作成 | O | O | O | O | O |
| ARRAY ADD/DROP COLUMN | △ | O | O | O | O |
| **インデックス** | | | | | |
| 基本インデックス | O | O | O | O | O |
| LSM インデックス | X | O | X | X | X |
| **参照** | | | | | |
| SELECT | O | O | O | O | O |
| 最新値の参照(`SCAN_BACKWARD`, TAG stat) | O | X | X | X | X |
| JOIN (他のテーブルと) | △ | △ | O | O | O |
| Subquery | O | O | O | O | O |
| VIEW | O | O | O | O | O |

> 記号: O = サポート、X = 非対応、△ = 一部をサポート、または制約あり

AppendがサポートするテーブルタイプはクライアントAPIによって異なります。使用する言語とAPIの
サポート範囲は[SDK Appendサポート表](/dbms/development-tools-integration/sdk-support-scope/#append-table-type-matrix)を
確認してください。

DECIMALは5種類すべてのテーブルタイプで使用できる正確な固定小数点型です。
`NUMERIC`、`DEC`、`FIXED`、`NUMBER`はDECIMALの別名です。精度（precision）は最大65桁、
小数部の桁数（scale）は最大30桁です。詳細は
[DECIMALとNUMERIC固定小数点型](../../sql/types/decimal-numeric-fixed-point/)を参照してください。

ARRAY ADD/DROPはStandard EditionのLOG、VOLATILE、LOOKUP、TRANSACTION、TAG METADATAで
サポートします。表のTAG列の`△`は、ALTERでTAG DATAの通常列は追加できず、TAG METADATAのみ
サポートすることを示します。Cluster EditionではLOG経路のみをサポートします。正確な構文と
既存行へのDEFAULT規則は[DDL構文](../../sql/syntax/ddl-syntax/#add-column)と
[数値ARRAY型](../../sql/types/array/)を参照してください。

## 主な制約の詳細

### TAGテーブルのUPDATE制約 (△, Standard Edition)

TAGテーブルのUPDATEは、次のすべての条件を満たす必要があります。

Cluster EditionではTAGデータUPDATEは使用できません。

- `WHERE`句にタグ選択条件（`name =`、`name IN`、`name LIKE`）を含める
- `WHERE`句にBASETIME列の条件を含める
- SET対象は実際のデータ列
- `time`（BASETIME）列、`name`列、メタデータ列はデータUPDATEで変更不可
- SETの右辺では既存行の列を参照できず、定数・バインド・列を含まない式のみ使用可能

```sql
-- 可能: タグ条件と時刻条件でデータ列を更新
UPDATE sensor_data
   SET value = 101
 WHERE name = 'sensor01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- 不可: BASETIME列を更新
UPDATE sensor_data
   SET time = SYSDATE
 WHERE name = 'sensor01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

詳細は[TAGデータUPDATEサポート表](../tag-data-update/)を参照してください。

### LOOKUPとVOLATILEのトランザクション範囲

LOOKUPとVOLATILEテーブルの各DMLは文単位で反映されます。複数のDMLを`BEGIN`と
`COMMIT`/`ROLLBACK`でまとめるTRANSACTIONテーブルのトランザクションには参加しません。

### JSON列のサポート範囲

JSON列はTAG、LOG、LOOKUP、TRANSACTIONテーブルでサポートします。VOLATILEではJSON型列を作成できません。LOOKUPのJSON列は通常の列として使用できますが、主キーには使用できません。詳細は[JSON型のテーブルタイプ別サポート範囲](../../sql/types/table-types-type-support-scope-json/)を参照してください。

## TAGテーブルの最新値と 時間範囲の参照

TAGテーブルは、逆方向スキャンと時刻条件で最新値と時間範囲を参照します。

```sql
-- 特定タグの最新5件の値を参照
SELECT /*+ SCAN_BACKWARD(sensor_data) */ *
  FROM sensor_data
 WHERE name = 'sensor01'
 LIMIT 5;

-- 時間範囲の参照
SELECT * FROM sensor_data
WHERE name = 'sensor01'
  AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```
