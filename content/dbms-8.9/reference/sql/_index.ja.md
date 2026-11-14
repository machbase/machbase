---
type: docs
title: '16.1 SQLリファレンス'
weight: 10
toc: true
---

SQL構文、関数、データ型、クエリヒント、相対時間式の正確な定義を提供します。

## 下位セクション

| セクション | 説明 |
|------|------|
| [SQL構文辞典](./syntax/) | CREATE、DROP、ALTER、SELECT、WITH/CTE、INSERT、DELETE、UPDATE、BACKUP、MOUNTなど全SQL文のBNF構文と例 |
| [関数辞典](./functions/) | 集約、数学、文字列、日付/時刻、型変換、TAG専用関数の一覧と説明 |
| [データ型辞典](./types/) | 対応するデータ型のサイズ、範囲、デフォルト値、テーブルタイプ別の使用可否 |
| [SELECT hint syntax](./syntax/select-hint-syntax/) | SELECTヒントの構文、使用方法、適用対象 |
| [相対時間式辞典](./relative-time/) | `now - 1h`形式の相対時間リテラルと接尾辞 |
| [ROWID](./rowid/) | テーブル別のROWIDの意味、参照条件、INSERT結果 |

## SQLの特徴

ANSI SQLを基に、時系列データ処理に最適化した拡張構文を提供します。

- **TAG時系列機能**: BASETIME, METADATA, `FIRST`/`LAST`, `SERIES BY`, ROLLUP
- **時間範囲の参照**: `DURATION`、`BEFORE`、`AFTER`、`RANGE`句
- **共通テーブル式**: Standard Editionの非再帰`WITH`/CTE
- **大量取り込みの連携**: クライアントSDKのAppend API（SQL文とは別の取り込みAPI）
- **テキスト検索**: `SEARCH`、`ESEARCH`、`REGEXP`演算子
- **集合演算**: `UNION ALL`（UNION、INTERSECT、EXCEPTは非対応）
