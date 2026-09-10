---
type: docs
title: '9.6 インデックスとパフォーマンス'
weight: 60
toc: true
---

LOOKUPテーブルのインデックス構造とパフォーマンスチューニングを説明します。

<a id="index-tuning-lookup-volatile"></a>
<a id="original-85-lookup-indexes"></a>
<a id="index-strategy-lookup"></a>

## LOOKUPのインデックスチューニング

LOOKUPのPRIMARY KEYには赤黒木インデックスが自動作成されます。
全行とインデックスは、SQL検索中にメモリに常駐します。
必要に応じて、非PK列にも赤黒木のセカンダリインデックスを追加できます。

### LOOKUPテーブルのインデックス

#### PKの自動赤黒木インデックス

LOOKUPテーブルを作成すると、PRIMARY KEY列に赤黒木インデックスが自動作成されます。
インデックス項目は、そのキーの全列値を含むメモリ行を指します。
そのため、永続テーブルでもクエリの実行経路はメモリベースであり、小規模なマスターデータをキーで繰り返し検索するパターンに最適化されています。

```sql
CREATE LOOKUP TABLE ch9_index_device (
    device_id   VARCHAR(64) PRIMARY KEY,  -- 赤黒木を自動作成
    device_name VARCHAR(128),
    location    VARCHAR(256),
    category    VARCHAR(32)
);

INSERT INTO ch9_index_device VALUES ('DEV-01', 'Boiler', 'Seoul', 'temperature');
INSERT INTO ch9_index_device VALUES ('DEV-02', 'Pump',   'Busan', 'pressure');
```

```sql
-- PK検索: 赤黒木インデックスを使用
SELECT device_id, device_name, location FROM ch9_index_device
 WHERE device_id = 'DEV-01';
```

1行が返されます。イベントログと結合する場合も、LOOKUP側はPKで検索します。

```sql
CREATE LOG TABLE ch9_index_event (device_id VARCHAR(64), level SHORT);
INSERT INTO ch9_index_event VALUES ('DEV-01', 3);
INSERT INTO ch9_index_event VALUES ('DEV-02', 1);
EXEC TABLE_FLUSH(ch9_index_event);

SELECT e.device_id, e.level, d.location
  FROM ch9_index_event e, ch9_index_device d
 WHERE e.device_id = d.device_id
 ORDER BY e.device_id;
```

2行が返されます。LOG側に時間範囲も指定すると、読み取る元データをさらに減らせます。

#### 非PK列のセカンダリインデックス

非PK列にも赤黒木セカンダリインデックスを作成できます。
セカンダリインデックスがない列でフィルタリングすると、テーブル全体を順次スキャンします。

```sql
-- 頻繁にフィルタリングする非PK列にセカンダリインデックスを作成
CREATE INDEX ch9_index_device_location ON ch9_index_device(location);

SELECT device_id FROM ch9_index_device WHERE location = 'Seoul';

-- インデックスのない列は全体スキャンになる場合があります
SELECT device_id FROM ch9_index_device WHERE category = 'temperature';
```

両方のクエリがDEV-01を返します。結果が同じでもアクセス経路が異なるため、
実際の比較は本番規模のデータで実行計画と併せて確認します。

セカンダリインデックスは検索を高速化しますが、更新コストとメモリ使用量が増えます。
頻繁に使用する条件列だけに作成してください。

#### LOOKUPテーブルの使用指針

PRIMARY KEYと赤黒木セカンダリインデックスの検索コストは、木のサイズに応じて増加します。
インデックスのない条件は、メモリにロードされた全行をスキャンします。
行数だけで使用限界を決めず、全行の実サイズ、可変長値、インデックス数、検索と更新の比率を同じワークロードで測定してください。
サーバー起動時には永続データをすべて読み取り、メモリ行とインデックスを構築するため、起動時間も確認します。

| 使用パターン | 適合性 |
|----------|-------|
| PKで機器情報を検索 | 適している（PK使用） |
| 非PK列でリスト検索 | セカンダリインデックス作成時に適している |
| 少数の基準コードテーブル | 適している |
| 全行がサーバーメモリに収まらない大規模マスターデータ | TRANSACTIONテーブルを検討 |
| リレーショナルトランザクションが必要なマスターデータ | TRANSACTIONテーブルを検討 |

### VOLATILEとの区別

VOLATILEは、再起動時にデータが消失する別のテーブルタイプです。
インデックス設計は[VOLATILEのインデックスとパフォーマンス](/dbms/volatile-table-usage/index-performance/)を参照してください。

### 大容量のマスターデータが必要な場合

LOOKUPテーブルのサイズとセカンダリインデックスの更新コストを考慮し、次のシナリオでは代替方法を検討します。

**シナリオ**: 機器のマスターデータを複数列でフィルタリングし、変更履歴も保持する場合

```sql
-- 代替方法: LOGテーブル + LSM/BITMAPインデックス
CREATE LOG TABLE ch9_index_device_hist (
    device_id   VARCHAR(64),
    device_name VARCHAR(128),
    location    VARCHAR(256),
    category    VARCHAR(32),
    updated_at  DATETIME
);

-- 非PK列にインデックスを作成可能
CREATE INDEX ch9_index_hist_location ON ch9_index_device_hist (location);
CREATE INDEX ch9_index_hist_category ON ch9_index_device_hist (category) INDEX_TYPE BITMAP;
```

ただし、LOGテーブルは追加専用のため、マスターデータの更新パターンに合わせて設計する必要があります。

実習で使用したオブジェクトは、次のように削除します。

```sql
DROP TABLE ch9_index_device_hist;
DROP INDEX ch9_index_device_location;
DROP TABLE ch9_index_event;
DROP TABLE ch9_index_device;
```

### 要点

- PRIMARY KEYインデックスは自動作成されます。
- 繰り返す非PK条件にだけセカンダリインデックスを作成します。
- 行・可変長値・インデックスのメモリ、起動時間、更新負荷を併せて測定します。
