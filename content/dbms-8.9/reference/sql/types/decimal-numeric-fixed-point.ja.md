---
type: docs
title: 'DECIMALとNUMERIC固定小数点型'
weight: 20
toc: true
---

`DECIMAL`は10進数を誤差なく保存する正確な固定小数点型です。`NUMERIC`、`DEC`、`FIXED`、`NUMBER`は
`DECIMAL`の別名であり、`DESC`、`SHOW`、結果メタデータでは正規名の`DECIMAL`と表示されます。
`NUMBER`はMySQLの別名ではなく、Machbaseの互換性拡張の別名です。

## 宣言構文

```sql
DECIMAL
DECIMAL(precision)
DECIMAL(precision, scale)

NUMERIC
NUMERIC(precision)
NUMERIC(precision, scale)
```

| 宣言 | 解釈 |
|------|------|
| `DECIMAL` | `DECIMAL(10,0)` |
| `DECIMAL(M)` | `DECIMAL(M,0)` |
| `DECIMAL(M,D)` | precision `M`, scale `D` |

- precisionは有効数字の総桁数で、`1`から`65`まで指定します。
- scaleは小数部の桁数で、`0`から`30`まで指定します。
- scaleはprecisionを超えることはできません。
- `UNSIGNED`と`ZEROFILL`はサポートしません。

```sql
CREATE TRANSACTION TABLE invoice (
    invoice_id LONG PRIMARY KEY,
    amount     DECIMAL(18,2),
    tax_rate   NUMERIC(7,4)
);
```

## 丸めと範囲超過

入力値の小数桁数がscaleを超えた場合は、中間値を0から遠ざかる方向へ丸める
round-half-away-from-zeroを適用します。

```sql
CREATE TRANSACTION TABLE decimal_rounding (
    id     INTEGER PRIMARY KEY,
    amount DECIMAL(5,2)
);

INSERT INTO decimal_rounding VALUES (1, 1.235);   -- 1.24
INSERT INTO decimal_rounding VALUES (2, -1.235);  -- -1.24
```

precisionを超える値は、切り捨てや浮動小数点への変換を行わずエラーとして扱います。
`DECIMAL`のNULLは特定の数値を番兵値として使用せず、値とは別に管理します。

## テーブルタイプ別サポート

| テーブルタイプ | DECIMAL列 | 主な用途 |
|------------|:------------:|----------------|
| LOG | O | 金額・精算イベント、正確な集計 |
| TAG | O | 正確な計測値と集計対象のデータ列 |
| VOLATILE | O | 状態・キャッシュ値、主キー |
| LOOKUP | O | 基準金額・比率、主キーとセカンダリインデックス |
| TRANSACTION | O | リレーショナルな業務データ、PK/UNIQUE/通常インデックス |

```sql
CREATE LOG TABLE payment_log (
    occurred_at DATETIME,
    amount      DECIMAL(18,2)
);

CREATE TAG TABLE meter_value (
    name   VARCHAR(80) PRIMARY KEY,
    time   DATETIME BASETIME,
    value  DECIMAL(24,6)
);

CREATE VOLATILE TABLE exchange_cache (
    rate_key DECIMAL(12,6) PRIMARY KEY,
    label    VARCHAR(32)
);

CREATE LOOKUP TABLE price_rule (
    rule_id LONG PRIMARY KEY,
    amount  DECIMAL(18,2)
);
```

Cluster EditionではLOG/TAGテーブルのDECIMAL列とDDL伝播をサポートします。TRANSACTIONテーブルは
DECIMAL型とは関係なくStandard Editionで使用します。

## 比較とインデックス

すべてのテーブルエンジンは同じDECIMAL比較規則を使用します。表現するscaleが異なっても、
数値が同じなら等しい値として比較します。

```sql
-- 1、1.0、1.00は等値・PK・UNIQUEの比較で同じ値です。
SELECT * FROM price_rule WHERE amount = 1.00;
```

VOLATILEとLOOKUPの主キーメモリインデックス、TRANSACTIONテーブルの通常・UNIQUE・PRIMARY KEY
インデックスでDECIMALを使用できます。TRANSACTIONインデックスは等値、範囲、並べ替えに同じ数値順序を適用します。

VIEWの派生列もDECIMALのprecisionとscaleを維持します。`DESC`、`SHOW`、`M$SYS_COLUMNS`、
クライアントの結果メタデータでprecisionとscaleをそれぞれ確認できます。

## 式と集約関数

`+`、`-`、`*`、`/`、`ROUND`、`TRUNC`、[CAST](../../functions/functions-full/#cast)と次の集計・ソート操作で
DECIMAL値を使用できます。

- `SUM`, `AVG`, `MIN`, `MAX`
- `GROUP BY`, `ORDER BY`, `DISTINCT`

正確なDECIMAL処理経路がない高度な統計関数、percentile、`TOP_K`などはDECIMAL値をDOUBLEに
変換して計算するため、結果が近似値になる場合があります。

## 入出力とクライアントマッピング

machloaderの`.fmt`、CSVインポート/エクスポート、Append経路は、符号、NULL、precision、scaleを
保持します。浮動小数点型を経由せず、文字列または各言語のdecimal型で渡してください。

| インターフェース | 推奨マッピング |
|-----------|-----------|
| ODBC | `SQL_DECIMAL` / `SQL_NUMERIC`, `SQL_C_NUMERIC` |
| JDBC | `java.math.BigDecimal` |
| Python | `decimal.Decimal` |
| Node.js | decimal互換の文字列、またはコネクターのdecimal表現 |
| .NET | `decimal`, `DbType.Decimal` |

GoでNUMERIC値を扱う場合も、`float64`へ変換せず、コネクターが提供する10進精度を保持する値か
文字列表現を使用してください。

## 型の選択

- 通貨、税率、精算額など10進数の正確性が必要な場合は`DECIMAL`を使用します。
- センサーの実数値など、近似値と広い指数範囲が重要な場合は`FLOAT`または`DOUBLE`を使用します。
- 保存・比較・演算中にDECIMAL値をDOUBLEへ変換すると、正確な固定小数点の性質が失われます。
