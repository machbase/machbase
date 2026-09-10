---
type: docs
title: '8.2 テーブル構造とスキーマ'
weight: 20
toc: true
---

自動採番があれば重複の問題は解決したと考えがちです。
しかし、同じ外部機器が異なる番号で2回登録されることは依然として可能です。
行の識別キーと業務上の重複を防ぐキーを区別することが、スキーマ設計の出発点です。

<a id="rdb-table-design"></a>
<a id="rdb-table-design-design-schema-type-rdb"></a>

<a id="내부-식별자와-업무-키를-나눕니다"></a>

## 内部識別子と業務キー

次の例では、内部番号と外部機器コードを別々に管理します。

```sql
CREATE TRANSACTION TABLE ch8_schema (
    id            LONG PRIMARY KEY AUTO_INCREMENT,
    external_code VARCHAR(64) NOT NULL,
    device_name   VARCHAR(128) NOT NULL,
    price         DECIMAL(18,2),
    state         JSON,
    updated_at    DATETIME
);
CREATE UNIQUE INDEX ch8_schema_code ON ch8_schema(external_code);

INSERT INTO ch8_schema(external_code, device_name, price, state, updated_at)
VALUES ('ERP-01', 'Pump A', 19900.25, '{"status":"NORMAL"}',
        TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'));

SELECT external_code, device_name, price, state->'$.status' AS status
  FROM ch8_schema;
```

ERP-01の1行、価格19900.25、状態NORMALが返されます。
idはサーバーが付与します。連続番号や欠番のない発行を業務条件にしないでください。
発行番号の取得方法は、使用するSDKと[AUTO_INCREMENT](/dbms/reference/sql/syntax/auto-increment-syntax/)を確認してください。

<a id="primary-key와-unique는-역할이-다릅니다"></a>

## PRIMARY KEYとUNIQUE

TRANSACTIONのPRIMARY KEYはテーブルごとに1つで、単一列です。
列の後にPRIMARY KEYを指定するか、既存テーブルにCREATE PRIMARY KEY INDEXで追加できます。
NULLや重複を含むデータには作成できません。

複数列の組み合わせを一意にするには、複合UNIQUE INDEXを使用します。
他のDBMSのCREATE TABLE内のUNIQUE・FOREIGN KEY・テーブルレベルPRIMARY KEY構文を、そのまま持ち込まないでください。
一意性はテーブル作成後にCREATE UNIQUE INDEXで指定します。

UNIQUE INDEXのキーにNULLが含まれる場合、NULLを含むキー同士は重複とは見なされません。
コードが必須かつ一意である必要がある場合は、例のようにNOT NULLも宣言してください。
空文字列にも注意が必要です。Machbaseの空文字列とNULLの扱いも実際の取り込み方法で確認し、必須コードは収集段階で検証してください。

次のSQLはUNIQUE違反を確認する任意の実習です。通常の入力とは分けて実行してください。

```sql
-- 意図的に失敗: external_codeの重複
INSERT INTO ch8_schema(external_code, device_name)
VALUES ('ERP-01', 'Duplicate Pump');
```

失敗後もERP-01は1行のままである必要があります。
重複時に更新するには、[UPSERT](../insert-on-duplicate-key-update/)の別の規則を使用します。

<a id="타입은-표현-범위와-연산-목적에-맞춥니다"></a>

## データ型の選択

| 値 | 型の選択 | 確認事項 |
|---|---|---|
| 識別子・数量 | SHORT・INTEGER・LONGとサポートされる符号なし型 | 範囲とNULL予約値 |
| 測定値・近似値 | FLOAT・DOUBLE | 浮動小数点の丸め |
| 金額・正確な小数 | DECIMAL(M,D)とNUMERICなどの別名 | 精度・小数桁数・入力変換 |
| コード・名前 | VARCHAR(n) | 文字数ではなくバイト長 |
| 長い文字列・バイナリ | TEXT/CLOB・BINARY/BLOB | 保存の対応とソート・関数・インデックスの対応を区別 |
| 発生・変更時刻 | DATETIME | 元のタイムゾーンと変換書式 |
| ネットワークアドレス | IPV4・IPV6 | アドレス形式と比較の意味 |
| 追加属性 | JSON | 頻繁に検索するパスと型 |
| 固定長の数値群 | 数値ARRAY | 要素型・長さ・列全体のNULLと要素のNULL |

全体の範囲は[データ型リファレンス](/dbms/reference/sql/types/)、
金額は[DECIMAL](/dbms/reference/sql/types/decimal-numeric-fixed-point/)を基準に確認してください。
例のDOUBLEを慣習的にすべての金額列に使用しないでください。

<a id="필요한-제약만-명시하고-입력도-검증합니다"></a>

## 制約と入力検証

TRANSACTIONには少なくとも1つのユーザー列が必要です。
LOGの自動到着時刻や、TAGのMETADATA・BASETIME・BASEDISTANCEは使用できません。
外部キーが自動的に参照整合性を検査すると考えず、必要な関係の検証をアプリケーションとデータ点検手順に含めてください。

例のUNIQUE INDEXがあっても、機器名や価格の業務上の有効性まで検査されるわけではありません。
必須値、許可する状態、数量範囲は別途定義する必要があります。

```sql
SELECT COUNT(*) AS device_count FROM ch8_schema;
DROP TABLE ch8_schema;
```

クリーンアップ前の件数は1です。
スキーマ変更は[作成・変更・削除](../create-alter-drop/)、クエリのアクセス経路は
[インデックス設計](../index-performance/)で引き続き確認してください。
