---
type: docs
title: '6.7 拡張ROLLUPとFIRST/LAST'
weight: 70
toc: true
aliases:
  - /dbms/tag-rollup-usage/first-last-rollup/
---

<a id="rollup-extension"></a>

## EXTENSIONと元データのFIRST/LASTの違い

EXTENSIONはROLLUPに最初・最後の値と関連する時刻情報を追加します。
通常の元データのGROUP BYでFIRST/LASTを使うことと、保存済みROLLUPからFIRST/LASTを取得することは異なります。
後者には、適用可能な拡張ROLLUPが必要です。

時刻のみのEXTENSIONは最初・最後の値と時刻を保存し、ソート付きEXTENSIONは候補の補助キーも保存します。
MIN、MAX、SUM、COUNT、平方和のSUMSQは通常のROLLUPにも保存されます。
SUMSQから分散と標準偏差を計算する方法は、
[SUMSQと分散・標準偏差](../query-syntax-rollup/#query-sumsq-stddev-rollup)を参照してください。

## 準備と入力

```sql
CREATE TAG TABLE ch6_ext (
    code VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    price DOUBLE
);
CREATE ROLLUP ch6_ext_first
  ON ch6_ext(price) INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP ch6_ext_plain
  ON ch6_ext(price) INTERVAL 1 MIN;
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:10', 'YYYY-MM-DD HH24:MI:SS'), 105);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:20', 'YYYY-MM-DD HH24:MI:SS'), 99);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:30', 'YYYY-MM-DD HH24:MI:SS'), 103);
EXEC TABLE_FLUSH(ch6_ext);
ALTER ROLLUP ch6_ext_first FORCE;
ALTER ROLLUP ch6_ext_plain FORCE;
```

## 元データとOHLCの比較

```sql
SELECT DATE_TRUNC('minute', time) AS bucket,
       FIRST(time, price) AS open_price, MAX(price) AS high_price,
       MIN(price) AS low_price, LAST(time, price) AS close_price
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_ext_first) */
       rollup('min', 1, time) AS bucket,
       FIRST(time, price) AS open_price, MAX(price) AS high_price,
       MIN(price) AS low_price, LAST(time, price) AS close_price
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket ORDER BY bucket;
```

両方のクエリは、09:00バケットにOpen=100、High=105、Low=99、Close=103を返します。
時刻のみのROLLUPのFIRST/LASTでは、第1引数にBASETIME、第2引数に集計対象カラムを使用します。
同じ時刻の行に業務上の順序が必要な場合は、以下の複合キー定義を使用します。

## 通常の候補と拡張候補が共存する場合

通常のROLLUPが拡張ROLLUPより無条件に優先されるわけではありません。
同じ条件・間隔の候補は、登録順序の影響を受けます。
この例では拡張を先に作成していますが、特定候補を使用する必要がある場合は上記のように明示してください。
拡張だけが適用可能な環境では、ヒントなしで選択される場合もあります。

次は通常のROLLUPを強制するため、意図的に失敗するクエリです。

```sql
SELECT /*+ ROLLUP_TABLE(ch6_ext_plain) */
       rollup('min', 1, time) AS bucket, FIRST(time, price)
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket;
```

自動階層に拡張が必要なら、別のテーブルのCREATEで`WITH ROLLUP (SEC) EXTENSION`を使用します。
FROMで階層を作成する場合も、拡張属性を一致させる必要があります。
Custom OHLCVの再集計は[Customの例](../custom-rollup/)を参照してください。

## クリーンアップ

```sql
DROP ROLLUP ch6_ext_plain;
DROP ROLLUP ch6_ext_first;
DROP TABLE ch6_ext;
```

<a id="composite-first-last"></a>

## 複合キーFIRST/LASTとソート付きROLLUP

> 複合キーFIRST/LASTとソート付きEXTENSION ROLLUPはMachbase 8.7.3から対応します。エディション別の制約は以下を確認してください。

8.7.3以降のStandardは明示的なROWID補助キーにも対応します。以下の
[Standard専用ROWID例](#standard-rowid-key)を参照してください。Clusterは非対応です。

### サンプルデータ

raw_tabはROLLUPのない元TAG、rollup_tabはソート付きROLLUPの集約元TAGです。
同名オブジェクトがない別環境を前提とします。第1キーは時刻です。
入力順は業務キー順と異なり、銘柄ごとの各分の開始時刻には同じcode/timeの行が3件あります。

```sql
CREATE TAG TABLE raw_tab (
    code     VARCHAR(20) PRIMARY KEY,
    time     DATETIME BASETIME,
    price    DOUBLE SUMMARIZED,
    seq      INTEGER,
    event_id INTEGER
);

INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 102, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:50'), 105, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 103, 2, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 101, 1, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:50'), 104, 1, 1);

INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 202, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:50'), 205, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 203, 2, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 201, 1, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:50'), 204, 1, 1);

INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 302, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:50'), 305, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 303, 2, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 301, 1, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:50'), 304, 1, 1);

INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 402, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:50'), 405, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 403, 2, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 401, 1, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:50'), 404, 1, 1);

EXEC TABLE_FLUSH(raw_tab);

SELECT COUNT(*) AS row_count FROM raw_tab;
```

### 元データ照会と同順位

timeのみの場合、Aの09:00のFIRST候補は101/102/103、LAST候補は104/105です。
(time, seq)ではFIRSTが101/102に絞られますが、time/seqが等しいため特定行は保証されません。
次の照会はevent_idも比較して候補を決定します。

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST(time, price) AS first_price,
       LAST(time, price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time, seq), price) AS first_price,
       LAST((time, seq), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

| code | bucket | first_price | last_price |
|---|---|---:|---:|
| A | 2026-10-22 09:00:00 | 101 | 105 |
| A | 2026-10-22 09:01:00 | 201 | 205 |
| B | 2026-10-22 09:00:00 | 301 | 305 |
| B | 2026-10-22 09:01:00 | 401 | 405 |

### キー別の方向

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time ASC, seq ASC, event_id DESC), price) AS first_price,
       LAST((time ASC, seq ASC, event_id DESC), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

event_idのみDESCにすると、結果はA=102/104、202/204、B=302/304、402/404になります。

### ソート付きROLLUPの定義と照会

rollup_tabに同じデータを格納し、定義と一致するキーで照会します。
ROLLUP_TABLEヒントは、この例で保存済みROLLUPを明示的に選択します。

```sql
CREATE TAG TABLE rollup_tab (
    code     VARCHAR(20) PRIMARY KEY,
    time     DATETIME BASETIME,
    price    DOUBLE SUMMARIZED,
    seq      INTEGER,
    event_id INTEGER
);

INSERT INTO rollup_tab SELECT * FROM raw_tab;
EXEC TABLE_FLUSH(rollup_tab);

CREATE ROLLUP price_1m_ordered
    ON rollup_tab(price)
    INTERVAL 1 MIN
    EXTENSION ORDER BY time ASC, seq ASC, event_id ASC;

ALTER ROLLUP price_1m_ordered FORCE;
```

```sql
SELECT /*+ ROLLUP_TABLE(price_1m_ordered) */
       code, ROLLUP('min', 1, time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM rollup_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

結果は元データの3キーASC照会と同じです。DESC照会には方向が一致する別の定義が必要です。

```sql
CREATE ROLLUP price_1m_desc
    ON rollup_tab(price)
    INTERVAL 1 MIN
    EXTENSION ORDER BY time ASC, seq ASC, event_id DESC;

ALTER ROLLUP price_1m_desc FORCE;

SELECT /*+ ROLLUP_TABLE(price_1m_desc) */
       code, ROLLUP('min', 1, time) AS bucket,
       FIRST((time, seq, event_id DESC), price) AS first_price,
       LAST((time, seq, event_id DESC), price) AS last_price
  FROM rollup_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

### 上位ROLLUP

```sql
CREATE ROLLUP price_1h_ordered
    FROM price_1m_ordered
    INTERVAL 1 HOUR EXTENSION;

ALTER ROLLUP price_1h_ordered FORCE;

SELECT /*+ ROLLUP_TABLE(price_1h_ordered) */
       code, ROLLUP('hour', 1, time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM rollup_tab
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

上位ROLLUPは下位のソート定義と元の候補キーを継承します。時間単位の結果はA=101/205、B=301/405です。

### 定義の一致と変更制約

- 第1キーは元TAGのBASETIME、補助キーは対応する通常データカラムでなければなりません。
  TAG名、メタデータ、式、テーブル名付きカラム参照は定義に使用できません。
- Standardの明示的な公開ROWID補助キーは、以下の個別制約に従って使用できます。
- 数値対象のソート付きEXTENSIONをサポートします。JSON_PATH/JSON_SUMMARYとの組み合わせは非対応です。
- 照会のキー数・カラム・順序・方向・型は定義と一致する必要があります。
  存在するが定義が一致しないROLLUPを`ROLLUP_TABLE`ヒントで指定すると、
  `ERR-02813: Invalid ROLLUP expression. (Token = ROLLUP ordering mismatch, Unit = 0)`を返します。
  ヒント対象が存在しない場合は`ERR-02025`です。先行するROLLUP検証のエラーが優先される場合もあります。
  定義に非対応キーを指定した場合は、`ERR-02813`の`Token = EXTENSION ORDER BY`で区別します。
- 既存の時刻のみのROLLUPには補助キーがありません。新定義で元データを再集計します。削除済みの元キーは復元できません。
- 保存候補キーによって、通常のWHERE・GROUP BY・出力で元カラムを利用できる範囲が拡大することはありません。
- ソート付きROLLUPは、キーごとに全キー一覧を含む内部集約SQLを生成します。このSQLが内部の長さ上限を超えると、
  作成時に`ERR-02813`（`Token = ordering query exceeds supported size, Unit = 0`）で拒否されます。
  キーが多いほど、また列名が長いほど早く上限に達します。たとえば`time`と`seq`9個による
  10キーの定義は拒否されます。同順位の解消に必要なキーだけを指定してください。
  ソート定義自体がメタデータの長さ制限を超える場合のTokenは`EXTENSION ORDER BY`です。
- Standardでは参照キーのRENAMEをERR-02686で拒否します。停止中ジョブと上位の依存関係にも適用します。
  関連する上位・下位ROLLUPをすべてDROPした後、カラム名を変更して再作成します。
- 元データUPDATE後の自動再集計を追加する機能ではありません。
- Clusterの全broker・warehouseに、機能をサポートする同一ビルドが必要です。

### 既存EXTと自動選択 {#ordered-rollup-selection}

両方を使用できる通常の集約では、まずWHERE条件のない候補を探します。
同じ条件区分で値カラムがNULLを許容する場合、ソート定義のない既存ROLLUPを優先します。
集約する値カラムのNOT NULLが確認できる場合、既存・ソート付き候補を同等に扱います。
`COUNT(*)`は値カラムのNOT NULLを推定せず、既存候補の優先を維持します。
照会周期を割り切れる最大の有効周期を選び、同周期では登録順に従います。
複合キーFIRST/LASTは、キーと方向が一致するソート定義のみ使用できます。

時刻のみのEXTとソート付きROLLUPではNULLバケットの扱いが異なります。
NULL許容のpriceで、ある分にNULL、10、次の分に20が入力された場合、既存EXTは最初の分を
除外してSUM/COUNT(price)が20/1になることがあります。ソート付きROLLUPはバケットを保持し、
30/2になることがあります。集約一覧・照会周期・ヒント・既存オブジェクトの削除で候補が
変わるため、移行時はFIRST/LASTだけでなくSUM/COUNTも照合してください。

従来の`FIRST(time, price)` / `LAST(time, price)`を使う保存ROLLUP照会には、適用可能な
既存の時刻のみのEXTが必要です。ソート付きROLLUPでは代用できません。
従来照会を維持する場合は既存EXTも保持してください。ソート付きROLLUPしかない場合、この照会は
`ERR-02685`（`There are no applicable ROLLUP tables.`）を返します。SUM・COUNTなどの通常の集約は
ソート付きROLLUPを使用できます。条件付き候補は絞り込んだ入力を集約します。

### 定義の確認と再構成

`V$ROLLUP.EXT_TYPE = 1`だけではソート付き・時刻のみのEXTやソートキーを区別できません。
定義を管理できるようにCREATE ROLLUP SQLを保存してください。
`WITH ROLLUP ... EXTENSION`はORDER BYを受け付けず、ソート付きオブジェクトはCREATE ROLLUPで作成します。
FROMの上位階層はORDER BY省略時に下位定義を継承します。
明示する場合は下位と同じキー・方向でなければなりません。

ROLLUP_REBUILDが任意のソート付きオブジェクトも再集計すると仮定しないでください。
対象は別途文書化された自動階層とCustom経路に限定されます。
元データを補正した後は、依存する上位から下位の順に削除し、保存してある元データから
ソート階層を再作成して結果を確認してください。削除済みの元キーは復元できません。

### 旧バイナリとロールバック {#ordered-rollup-compatibility}

ソート付きROLLUPを含むDBを、この機能がない旧バイナリで開く、またはMOUNTする運用は非対応です。
この機能ではメタバージョンを上げないため、同じメタバージョンの旧バイナリが検査を通過し、
ソート付きオブジェクトを既存EXTとして解釈する可能性があります。戻す場合は機能導入前の
バックアップを復元し、対象バージョンの復旧手順に従ってください。ソート付きオブジェクトの
DROPだけでは、すべてのカタログ・ファイルの互換性は保証されません。

8.5.13でソート付きROLLUPを作成したDBを8.7にアップグレードする場合は、8.7.3以降を使用してください。
8.7.0～8.7.2にはこの機能がないため、上記のとおりソート付きオブジェクトを既存EXTとして解釈する可能性があります。

### Standardの公開ROWID補助キー {#standard-rowid-key}

この追加例は、上記の`rollup_tab`を使う8.7.3以降のStandard用です。
Clusterではこの節を実行しません。ROWIDは`(time, seq, ROWID)`のように2番目以降の
明示的な補助キーに使用できます。要約行自体ではなく、選択された元の行のROWIDを保持します。

```sql
CREATE ROLLUP price_1m_rowid
    ON rollup_tab(price)
    INTERVAL 1 MIN EXTENSION ORDER BY time, ROWID;
ALTER ROLLUP price_1m_rowid FORCE;

SELECT code,
       FIRST((time, ROWID), price) AS first_price,
       LAST((time, ROWID), price) AS last_price
  FROM rollup_tab
 GROUP BY code
 ORDER BY code;

SELECT /*+ ROLLUP_TABLE(price_1m_rowid) */
       code, ROLLUP('hour', 1, time) AS bucket,
       FIRST((time, ROWID), price) AS first_price,
       LAST((time, ROWID), price) AS last_price
  FROM rollup_tab
 GROUP BY code, bucket
 ORDER BY code, bucket;

DROP ROLLUP price_1m_rowid;
```

この1時間のデータでは、codeごとの元データ照会とROLLUP照会のFIRST/LASTが一致する必要があります。
前述の業務連番の例と同じ価格になる保証はありません。ROWIDは保存行識別子であり、業務連番や
テーブル全体の入力順序ではありません。バックアップ再ロードやテーブル再作成後に同じ値・順序を
保証せず、暗黙にソートキーへ追加されることもありません。

既存のROWID制限も維持します。ROLLUP照会のGROUP BY・ORDER BYでROWIDを直接使う、
またはBITANDで包んで別キーを作ることはできません。複合FIRST/LASTの明示的な補助キーに使い、
その集約式・別名・SELECT一覧の位置でソートすることは可能です。
Clusterは公開ROWIDキーを拒否します。このSELECT形式は`ERR-02056`、定義は
`Token = EXTENSION ORDER BY`の`ERR-02813`を返します。

### サンプルオブジェクトの削除

```sql
DROP ROLLUP price_1h_ordered;
DROP ROLLUP price_1m_desc;
DROP ROLLUP price_1m_ordered;
DROP TABLE rollup_tab;
DROP TABLE raw_tab;
```
