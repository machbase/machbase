---
type: docs
title: '4.1 テーブルタイプの選択'
weight: 10
toc: true
---
タイプの選択を誤ると性能低下や機能制限につながるため、設計初期にデータの性質に合うタイプを決めます。

- **[タイプ選択ガイド](/dbms/data-modeling-table-design/table-types-selection-type/#selection-decision)**
- **[タイプ比較表](/dbms/data-modeling-table-design/table-types-selection-type/#comparison-tag-log-rdb-volatile-lookup)**
- **[TRANSACTION と LOOKUP の比較](/dbms/data-modeling-table-design/table-types-selection-type/#comparison-rdb-vs-lookup)**


<a id="table-types-type"></a>

役割と保存の概念は[データモデルの概念](../../core-concepts/concepts/#time-series)を参照してください。
同じデータでも、履歴を蓄積するか現在状態を更新するかで適切なタイプが変わります。
変更・クエリ・永続性の要件を併せて検討します。

### 選択前に記述するデータの説明

テーブル名より先に、1行が表す事実を1文で記述します。同じ設備でも、1回の温度計測、
現在の運転状態、1件の保守作業は異なる単位であり、キーと変更方法も異なります。

| 設計上の問い | 設備監視で決める内容 |
|---|---|
| 1行は何か | センサーの1回の計測か、設備の現在状態か |
| 何で検索するか | センサー名と発生時刻、設備 ID、保守作業番号 |
| 値はどう変わるか | 履歴の追加、誤値の補正、現在行の上書き |
| 同時に確定する変更があるか | 保守作業登録と部品数量変更を1トランザクションにまとめるか |
| どれだけ保持するか | 元データ・集計の期間と、再起動後の再生成可否 |
| 規模はどの程度か | タグ数、毎秒行数、行サイズ、参照データとインデックスのメモリ |

例えば温度履歴は TAG、アラームイベントは LOG、設備コード表は LOOKUP が候補です。
部品在庫変更と作業登録を同時に確定するなら Standard Edition の TRANSACTION を検討します。
現在状態キャッシュは元データから再構築できる場合に VOLATILE へ分離できます。
1テーブルへ統合する前に、行の意味と失敗時の復旧方法を整合させます。

<a id="selection-decision"></a>

## タイプ選択ガイド

次の流れで候補を絞り、比較表で DML、トランザクション、メモリ、Edition の要件を確認します。
参照データでも複数変更を1トランザクションへまとめる場合は、LOOKUP ではなく TRANSACTION を検討します。

### 選択フロー

```
センサー/機器の計測値か?
  ├── YES → 時間軸か? YES → TAG TABLE (BASETIME)
  │         距離軸か? YES → TAG TABLE (BASEDISTANCE)
  └── NO  ↓

イベント/ログ/パケットか?（追記専用）
  ├── YES → LOG TABLE
  └── NO  ↓

コード表/参照データか?（繰り返し検索・更新）
  ├── YES → LOOKUP TABLE
  └── NO  ↓

再起動時に破棄できるインメモリ状態/キャッシュか?
  ├── YES → VOLATILE TABLE
  └── NO  ↓

一般的なリレーショナル業務データ（UPDATE/DELETE/SELECT/INSERT がすべて必要）
  └── TRANSACTION TABLE
```

### 主な判断基準

| 問い | タイプ |
|------|------|
| 時間または距離に基づく計測値か | TAG |
| 元イベントを追記し、古い範囲だけを削除するか | LOG |
| PRIMARY KEY が必要な参照データを繰り返し検索・更新するか | LOOKUP |
| 再起動でデータが消えてもよいか | VOLATILE |
| 一般的なリレーショナル業務（INSERT/UPDATE/DELETE/SELECT）か | TRANSACTION |

### 注意事項

- イベントごとに一意なタグ名を付けると、タグ数とメタデータが増え続けます。
  繰り返し計測する対象がないイベントには LOG を検討します。
- LOG は UPDATE と一般条件 DELETE ができないため、更新が必要なデータには不適切です。
  保持・整理用の `BEFORE`、`OLDEST`、`EXCEPT` DELETE を使用します。
- TRANSACTION は Standard Edition 専用です。Cluster では小規模 LOOKUP または外部 RDBMS を使用します。
- VOLATILE のデータは再起動で消失します。

<a id="comparison-tag-log-rdb-volatile-lookup"></a>

## タイプ比較表

### 機能比較

| 項目 | TAG | LOG | TRANSACTION | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| DDL | `CREATE TAG TABLE` | `CREATE LOG TABLE` | `CREATE TABLE` / `CREATE TRANSACTION TABLE` / `CREATE TXN TABLE` | `CREATE VOLATILE TABLE` | `CREATE LOOKUP TABLE` |
| 主用途 | センサー・計測 | イベント・ログ | リレーショナル業務 | 一時集計 | コード・参照データ |
| INSERT | O | O | O | O | O |
| UPDATE | O（Standard、タグ/BASETIME 条件） | X | O | O | O |
| DELETE | O（BEFORE/条件/全体） | O（BEFORE/OLDEST/EXCEPT/全体） | O | O（PK 一致/全体） | O（一般条件/全体） |
| PRIMARY KEY | 必須 | X | 任意 | 任意 | 必須 |
| BASETIME | 必須（時間軸） | X | X | X | X |
| _arrival_time | X | 自動追加 | X | X | X |
| インデックス | タグ・軸アクセス、対応するセカンダリ | BITMAP/KEYWORD/LSM | BTREE PK + セカンダリ | キー・セカンダリ | キー・セカンダリ |
| 永続性 | O | O | O | X（メモリ） | O |
| Cluster Edition | O | O | X | O | O |

Append API の対応は、テーブルだけでなく SDK と入力経路でも変わります。
[SDK Append 対応表](../../development-tools-integration/sdk-support-scope/#append-table-type-matrix)で
使用するドライバーとテーブルの組み合わせを確認します。

### ストレージ特性

| 項目 | TAG | LOG | TRANSACTION | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| ストレージ | 列指向 | 列指向 | 行指向（リレーショナル） | メモリ | 永続保存 + 全行がメモリに常駐 |
| 容量検討基準 | タグ数・元データ・ROLLUP・保持期間 | 元データ・検索インデックス・保持期間 | 行・インデックス・トランザクション負荷 | 全行とインデックスのメモリ | 全行とインデックスのメモリ、再起動時のロード時間 |

インメモリテーブルが小さいとは、固定の行数を意味しません。行幅、可変長値、セカンダリインデックスを
含めて実メモリ使用量を測定します。ディスク型でも圧縮率やサーバー仕様だけで性能は保証されないため、
代表的な入力とクエリを同時に実行します。

### TRANSACTION の制約

TRANSACTION には次の制約があります。

- **Cluster Edition 非対応**: Standard Edition 専用。
- **最小列数**: 1列以上。

<a id="comparison-rdb-vs-lookup"></a>

## TRANSACTION と LOOKUP の比較

両方ともリレーショナルデータを保存しますが、対象規模と機能が異なります。

### 比較表

| 項目 | TRANSACTION | LOOKUP |
|------|-----------|--------------|
| DDL | `CREATE TRANSACTION TABLE` | `CREATE LOOKUP TABLE` |
| PRIMARY KEY | 任意 | 必須 |
| INSERT | O | O |
| UPDATE（WHERE あり） | O | O |
| UPDATE（WHERE なし） | O（全行） | X |
| DELETE | O | O |
| 明示的トランザクション | 複数文を COMMIT/ROLLBACK で制御 | 参加せず、文ごとに変更 |
| インデックス | BTREE PK + セカンダリ | メモリ上のキー・セカンダリ |
| データ規模 | ディスク容量とトランザクション負荷で検証 | 参照データの検索・更新負荷で検証 |
| JOIN 対象 | O | O |
| Cluster Edition | X | O |

### 選択ガイド

**TRANSACTION を選ぶ場合**

- 明示的トランザクションとリレーショナル DML が必要。
- UPDATE・DELETE・INSERT・SELECT がすべて必要な一般的ワークロード。
- PRIMARY KEY なしで多様な列の組み合わせを検索。
- Standard Edition 環境。

**LOOKUP を選ぶ場合**

- コード表と参照データ。
- PRIMARY KEY 検索と単一行 UPDATE/DELETE が必要。
- Cluster Edition でも使用。
- 参照データをリアルタイムに更新。

### 例

```sql
-- LOOKUP: 国コード表（PK 検索と条件付き UPDATE）
CREATE LOOKUP TABLE country_code (
    code   VARCHAR(4)   PRIMARY KEY,
    name   VARCHAR(64)
);
INSERT INTO country_code VALUES ('KR', 'Republic of Korea');
UPDATE country_code SET name = 'Korea' WHERE code = 'KR';
SELECT code, name FROM country_code WHERE code = 'KR';

-- TRANSACTION: 注文履歴（大規模、一般 UPDATE/DELETE 対応）
CREATE TRANSACTION TABLE order_history (
    order_id  LONG PRIMARY KEY,
    item_id   INTEGER,
    qty       INTEGER,
    amount    DECIMAL(18,2)
);
INSERT INTO order_history VALUES (12345, 501, 1, 12000.00);
UPDATE order_history SET qty = 10 WHERE order_id = 12345;
SELECT order_id, qty, amount FROM order_history WHERE order_id = 12345;
DELETE FROM order_history WHERE order_id = 12345;
SELECT COUNT(*) FROM order_history WHERE order_id = 12345;
```

最初の SELECT は変更後の国名、注文 SELECT は数量 `10`、最後の COUNT は `0` を返します。
この例の `amount` は数量変更と別に維持する金額で、自動再計算されません。実際の注文モデルでは
単価・数量・合計の関係と、一緒に変更する列を明示します。終了後、例で作ったテーブルだけを
`DROP TABLE` で削除します。
