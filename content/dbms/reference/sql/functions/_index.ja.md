---
type: docs
title: '16.1.3 関数辞典'
weight: 30
toc: true
---

組み込み関数をカテゴリー別に示します。

| カテゴリー | 説明 |
|----------|------|
| [集約関数](aggregation/) | COUNT、SUM、AVG、MIN、MAX、STDDEV、FIRST、LASTなどのグループ集約関数 |
| [ウィンドウ/系列関数](series/) | ROWNUM、SERIESNUMなどのウィンドウ・系列分析関数 |
| [日付/時刻関数](datetime/) | TO_DATE、TO_CHAR、DATE_TRUNC、ADD_TIMEなどの日付・時刻処理関数 |
| [JSON関数とJSONドット表記](operators-json/) | JSONデータの抽出・操作関数とメンバーアクセス構文 |
| [正規表現関数](regex/) | REGEXP_LIKE、REGEXP_SUBSTRなどの正規表現による検索・変換関数 |
| [NEXTVAL関数](nextval/) | LookupテーブルのSequence列用の自動増分値生成関数 |
| [ユーザーコンテキスト関数](functions-full/#current-session-user) | CURRENT_USER、SESSION_USER、内部ユーザーIDの参照 |
| [完全な関数リファレンス](functions-full/) | 既存の関数とCASTを含む完全な関数リファレンス |

## 共通規則

- 特に記載がない場合、入力値が`NULL`なら結果も`NULL`です。
- 引数の型が一致しない場合は`ERR-02036`または`ERR-02037`エラーが発生します。
