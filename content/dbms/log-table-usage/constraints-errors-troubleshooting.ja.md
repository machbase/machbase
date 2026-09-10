---
type: docs
title: '7.8 制約、エラー、トラブルシューティング'
weight: 80
toc: true
---

失敗したSQLを繰り返しても原因は解消せず、状態が複雑になることがあります。
まず未サポートの操作か、入力値やオブジェクトの状態の問題かを区別してください。
この節では、症状に応じて確認箇所を絞り込みます。

<a id="limitations-log"></a>
<a id="지원하지-않는-기능"></a>

<a id="모델의-제약인지-먼저-확인합니다"></a>

## 機能のサポート範囲

| 要求 | LOGの対応 | 代替方法 |
|---|---|---|
| 一般的なUPDATE | 未サポート | 訂正イベントを設計するか、更新可能なテーブルを選択 |
| 任意条件のDELETE WHERE | 未サポート | BEFORE・OLDEST・EXCEPTを使用するか、モデルを変更 |
| PRIMARY KEY・UNIQUE制約 | 未サポート | 収集段階で重複を処理するか、別のテーブルを選択 |
| 値・範囲インデックス | LSMをサポート | 型と条件に合わせて選択 |
| 単語検索 | KEYWORDをサポート | VARCHAR・TEXTに作成し、SEARCH・ESEARCHを使用 |
| 分析用BITMAPインデックス | サポート条件内で使用 | 型・エンコーディング・値の分布を確認 |
| TEXT自体のORDER BY・GROUP BY | 未サポート | コード・重要度・時刻を別カラムに格納 |

<a id="증상에서-확인-지점을-찾습니다"></a>

## 症状別の診断

| 症状 | 最初の確認事項 | 対処 |
|---|---|---|
| 指定した到着時刻と保存時刻が異なる | 直前の時刻とTIME_INVERSION_MODE | 補正の有無を確認し、発生時刻は別に保持 |
| SEARCHでインデックス関連エラー | 対象カラムのKEYWORDインデックス | 型・テーブル・インデックス名を確認 |
| 単語があるのに検索されない | SEARCHのトークンとLIKEの部分文字列の違い | 元の1行で両方の結果を比較 |
| インデックス作成後も検索が遅い | 実行計画・構築状態・時間範囲 | 反映状態を確認後、代表的な負荷を測定 |
| カラム長の変更に失敗 | 既存の型と新しい長さ | VARCHARの拡張のみ使用し、最大長を確認 |
| MINMAXの変更に失敗 | 可変長型かどうか | LOGで対応する固定長カラムのみを対象にする |
| NOT NULLへの変更に失敗 | 既存のNULL行 | 既存データの検査とNOCHECKの意味を区別 |
| 同じイベントが複数表示される | 元のID・再試行・ファイル再処理 | 再送ポリシーを確認し、任意行の削除で解決しない |
| DDL実行中にリソース使用中エラー | 入力・検索とDDLの競合 | 実行時刻を調整して再確認 |

サーバー設定とインデックス一覧は次のように確認できます。

```sql
SELECT NAME, VALUE FROM V$PROPERTY
 WHERE NAME IN ('DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE', 'TABLE_SCAN_DIRECTION');
SHOW INDEXES;
```

設定の確認と変更は別の操作です。
原因を特定する前に、本番サーバーのグローバル設定を変更しないでください。

<a id="작은-테이블에서-오류와-정상-경로를-비교합니다"></a>

## エラーの再現と解決

```sql
CREATE LOG TABLE ch7_error (event_id INTEGER, message TEXT);
INSERT INTO ch7_error VALUES (1, 'connection timeout');
SELECT event_id, message FROM ch7_error;
```

1行が返されます。以下のSQLはそれぞれ意図的に失敗します。
通常の実習とまとめて実行せず、確認したい文だけを個別に実行してください。

```sql
-- KEYWORDインデックスがない状態です。
SELECT event_id FROM ch7_error WHERE message SEARCH 'timeout';

-- TEXT自体のソート・グループ化はサポートしていません。
SELECT message FROM ch7_error ORDER BY message;
SELECT message, COUNT(*) FROM ch7_error GROUP BY message;

-- LOGは一般的なUPDATE・条件付きDELETEをサポートしていません。
UPDATE ch7_error SET message = 'fixed' WHERE event_id = 1;
DELETE FROM ch7_error WHERE event_id = 1;

-- TEXTをVARCHARに変換するコマンドではありません。
ALTER TABLE ch7_error MODIFY COLUMN (message VARCHAR(4096));
```

インデックスを作成し、サポートされる検索方法で確認します。

```sql
CREATE INDEX ch7_error_msg ON ch7_error(message) INDEX_TYPE KEYWORD;
EXEC TABLE_FLUSH(ch7_error);
EXEC INDEX_FLUSH(ch7_error);

SELECT event_id, message FROM ch7_error
 WHERE message SEARCH 'timeout'
 ORDER BY event_id;

DROP TABLE ch7_error;
```

行1が返されることを確認してください。インデックスを追加しても、TEXTのソートやLOGのUPDATEは使用できません。

<a id="보존-문제는-삭제-경계부터-확인하세요"></a>

## 保持ポリシーの診断

期限切れの行が残る場合は、適用ポリシー、実行周期、LAST_DELETED_TIME、実際の`_arrival_time`を合わせて確認してください。
`event_time`だけを見て削除失敗と判断しないでください。
関連する実習は[運用とデータライフサイクル](../operations-lifecycle/)にあります。

問題が続く場合は、サーバーバージョンとEdition、テーブルDDL、失敗したSQL、エラー全文、代表的な入力値を用意してください。
パスワードと機密ログを伏せて共有してください。
全データを送るより、同じ症状を再現する小さな例のほうが原因の特定に役立ちます。
