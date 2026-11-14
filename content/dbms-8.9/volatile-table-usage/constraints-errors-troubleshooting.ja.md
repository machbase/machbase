---
type: docs
title: '10.8 制約、エラー、トラブルシューティング'
weight: 80
toc: true
---

VOLATILEテーブルの制約、発生し得るエラー、解決方法を説明します。
多くの問題は、メモリ上限、PRIMARY KEY設計、未サポートの列型、再起動後のデータ消失に起因します。

<a id="limitations-volatile"></a>

## 制約

VOLATILEテーブルでは、次の制約を考慮してください。

| 項目 | 制約 |
|------|------|
| 保存場所 | メモリ |
| 再起動後のデータ | 消失 |
| バックアップ・マウント | 未サポート |
| JSON列 | 未サポート |
| PRIMARY KEY | 任意。1つだけ指定 |
| UPDATE/DELETE | `PRIMARY KEY = 値`条件のみサポート |
| メモリ上限 | Volatile/Lookupテーブル全体のメモリ上限の影響を受ける |

```sql
-- 失敗例: VOLATILEテーブルではJSON列を使用できません。
CREATE VOLATILE TABLE ch10_err_json (
    session_id VARCHAR(64) PRIMARY KEY,
    payload    JSON
);
```

可変的な属性が必要なら、頻繁に検索する値を通常の列に分離してください。
永続的なJSON列が必要な場合は、TRANSACTIONまたはTAGテーブルを検討します。

<a id="error-volatile-memory"></a>

## メモリ不足

VOLATILEテーブルのデータとインデックスはメモリを使用します。
行数の増加や多数のインデックスによって、メモリ上限に達する場合があります。

診断は次の順序で行います。次の実習テーブルは、このページの最後で削除します。

```sql
-- 診断例の実習テーブルです。
CREATE VOLATILE TABLE ch10_diag (
    device_id VARCHAR(64) PRIMARY KEY,
    value     DOUBLE
);
INSERT INTO ch10_diag VALUES ('DEV-01', 10.0);

-- 1. 対象テーブルの行数を確認します。
SELECT COUNT(*) FROM ch10_diag;
```

```sql
-- 2. VOLATILEテーブル全体のメモリ使用量を確認します。
SELECT *
FROM V$STORAGE_DC_VOLATILE_TABLE;
```

必要に応じて、設定の`VOLATILE_TABLESPACE_MEMORY_MAX_SIZE`を確認します。

```sql
SELECT NAME, VALUE
FROM V$PROPERTY
WHERE NAME = 'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE';
```

対処方法は次のとおりです。

- 不要な行を削除します。
- キャッシュの保持範囲を縮小します。
- 使用していないインデックスを削除します。
- 重要なデータを永続テーブルに移してから、VOLATILEテーブルを再構築します。
- 運用ポリシーに合わせてメモリ上限の調整を検討します。

<a id="error-volatile-primary-key"></a>

## PRIMARY KEY関連のエラー

`ON DUPLICATE KEY UPDATE`、[PKによるUPDATE](../data-input-mutation/#volatile-primary-key-update)、
PKによるDELETEを使用するにはPRIMARY KEYが必要です。

```sql
CREATE VOLATILE TABLE ch10_err_device (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    updated_at DATETIME
);
```

PRIMARY KEYの値は重複できません。重複入力を更新として処理する場合は、`ON DUPLICATE KEY UPDATE`を使用します。

```sql
INSERT INTO ch10_err_device VALUES ('DEV-01', 'ONLINE', NOW)
ON DUPLICATE KEY UPDATE SET status = 'ONLINE', updated_at = NOW;
```

PRIMARY KEY列自体はUPDATEできません。キーを変更する場合は、既存行を削除して新しいキーで挿入します。

<a id="error-volatile-restart-loss"></a>

## 再起動後のデータ消失

サーバーの正常終了、異常終了、再起動時に、VOLATILEテーブルのデータは消失します。
これはエラーではなく、テーブルタイプの特性です。

問題が発生したら、次の項目を確認してください。

1. サーバーの再起動履歴を確認します。
2. VOLATILEテーブルの作成スクリプトが実行されたか確認します。
3. 初期ロードクエリが正常に実行されたか確認します。
4. 元のTAG/LOG/TRANSACTIONテーブルからキャッシュを再構築します。

```sql
SELECT COUNT(*) FROM ch10_diag;
```

結果が0の場合は、初期ロード手順を再実行します。

このページの実習テーブルは、次のように削除します。

```sql
DROP TABLE ch10_diag;
DROP TABLE ch10_err_device;
```

<a id="troubleshooting-volatile-checklist"></a>

## トラブルシューティングのチェックリスト

- テーブルに保存したデータを再作成できるか確認します。
- PRIMARY KEYが必要な操作か確認します。
- `COUNT(*)`と`V$STORAGE_DC_VOLATILE_TABLE`で規模とメモリ使用量を確認します。
- 再起動後は初期ロードSQLを再実行します。テーブルの再作成は不要です。
- 永続保持が必要なら、VOLATILEではなくTAG、LOG、LOOKUP、TRANSACTIONテーブルを使用します。
