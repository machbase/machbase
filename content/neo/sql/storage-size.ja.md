---
title: ストレージの自動管理
type: docs
weight: 51
toc: true
---

## はじめに

多数のデータソースから高頻度で取り込む時系列データベースでは、データが継続的に蓄積します。毎秒数百万件に達する取り込みには大きな保存容量が必要です。ディスク使用量の監視と定期的な DELETE を手動で行うと、運用が複雑になり、誤操作の可能性も高まります。また、多くの用途では一定期間のデータだけを保持し、それより古いデータを削除します。

Machbase は **保持ポリシー（Retention Policy）** により、指定した保持期間を過ぎたデータを自動削除します。ポリシーを宣言すると、長期的なデータライフサイクルとストレージ使用量を管理しやすくなります。

## 基本概念: 保持ポリシー

保持ポリシーは、指定したテーブルのデータを時刻に基づいて自動削除する規則です。次の 2 つのパラメーターで設定します。

* **Duration**: データの保持期間。ポリシーの検査時のシステム時刻からこの期間を引いた時刻より古いデータが削除対象です。単位は `MONTH`、`DAY`、`HOUR`、`MIN`、`SEC` です。
* **Interval**: `DURATION` に基づいて削除対象を検査する実行間隔。単位は `DAY`、`HOUR`、`MIN`、`SEC` です。

テーブルにポリシーを適用すると、バックグラウンド処理が `INTERVAL` ごとに検査します。`BASETIME` 列の時刻が、現在のシステム時刻から `DURATION` を引いた時刻より古い行を自動削除します。

使用手順:
1. `DURATION` と `INTERVAL` を指定して、名前付きの保持ポリシーを作成します。
2. 1 つ以上の対象テーブルにポリシーを適用します。
3. Machbase が指定の周期で削除を実行します。
4. 自動削除が不要になったテーブルからポリシーを解除します。
5. どのテーブルにも適用されていない不要なポリシーを削除します。

## 保持ポリシーの作成

`CREATE RETENTION` で独立したデータベースオブジェクトとして定義します。

**構文:**

```sql
CREATE RETENTION policy_name
    DURATION duration_value { MONTH | DAY | HOUR | MIN | SEC }
    INTERVAL interval_value { DAY | HOUR | MIN | SEC };
```

* `policy_name`: 一意のポリシー名。
* `duration_value`: 保持期間を表す整数。
* `MONTH | DAY | HOUR | MIN | SEC`: 保持期間の単位。
* `interval_value`: 削除対象を検査する間隔を表す整数。
* `DAY | HOUR | MIN | SEC`: 検査間隔の単位。

**例:**

```sql
-- 1 日分のデータを保持し、1 時間ごとに検査
CREATE RETENTION policy_1d_1h
    DURATION 1 DAY
    INTERVAL 1 HOUR;

-- 1 か月相当のデータを保持し、3 日ごとに検査
CREATE RETENTION policy_1m_3d
    DURATION 1 MONTH
    INTERVAL 3 DAY;
```

## テーブルへの保持ポリシーの適用

作成したポリシーを `ALTER TABLE ... ADD RETENTION` で対象テーブルに関連付けます。1 つのテーブルに同時に適用できるポリシーは 1 個だけです。

**構文:**

```sql
ALTER TABLE table_name ADD RETENTION policy_name;
```

* `table_name`: 適用先のテーブル名。
* `policy_name`: 作成済みの保持ポリシー名。

**例:**

```sql
-- policy_1d_1h が作成済みであること。sensor_data を作成する。
CREATE TAG TABLE sensor_data ( name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED );

-- sensor_data に policy_1d_1h を適用
ALTER TABLE sensor_data ADD RETENTION policy_1d_1h;
```

## 保持ポリシーの監視

定義したポリシーと適用状況は、システムカタログビューから確認できます。

* **`M$RETENTION`**: データベースに定義されたすべてのポリシーの名前と、設定した `DURATION`、`INTERVAL`（内部表現は秒単位）を表示します。

    ```sql
    -- 定義したすべての保持ポリシーを表示
    SELECT * FROM M$RETENTION;
    ```

* **`V$RETENTION_JOB`**: 各テーブルに適用されたポリシー、ジョブの状態（例: `WAITING`）、最後の削除処理で使用した基準時刻（`LAST_DELETED_TIME`）を表示します。

    ```sql
    -- 現在テーブルに適用されているポリシーを表示
    SELECT * FROM V$RETENTION_JOB;
    ```

## ポリシーの解除と削除

テーブルからポリシーを解除すると、そのテーブルの自動削除が停止します。ポリシー自体が不要になり、他のテーブルにも適用されていない場合は、ポリシーオブジェクトを削除できます。

### テーブルからの解除

`ALTER TABLE ... DROP RETENTION` でテーブルとの関連付けを解除します。

**構文:**

```sql
ALTER TABLE table_name DROP RETENTION;
```

* `table_name`: 現在のポリシーを解除するテーブル名。

### ポリシーオブジェクトの削除

`DROP RETENTION` でポリシー定義を削除します。まだテーブルに適用されている場合は失敗します。

**構文:**

```sql
DROP RETENTION policy_name;
```

* `policy_name`: 削除する保持ポリシー名。

**依存関係の例:**

```sql
-- sensor_data に policy_1d_1h が適用されているものとする

-- 使用中のポリシーの削除は失敗する
DROP RETENTION policy_1d_1h;
-- 想定エラー: [ERR-02702: Policy (POLICY_1D_1H) is in use.]

-- 先にテーブルからポリシーを解除
ALTER TABLE sensor_data DROP RETENTION;

-- 解除後はポリシーを削除できる
DROP RETENTION policy_1d_1h;
```

## 使用例

保持ポリシーを使用する手順を示します。

**1. スキーマの準備:**

```sql
-- 既存テーブルと依存する Rollup テーブルを削除
DROP TABLE IF EXISTS ret_tag CASCADE;

-- サンプル TAG テーブルを作成（例として Rollup を指定するが、保持ポリシーに必須ではない）
CREATE TAG TABLE ret_tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP(MIN) TAG_PARTITION_COUNT=1;
```

**2. 保持ポリシーの作成:**

```sql
-- 1 日保持、1 時間ごとの検査を定義
CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;

-- ポリシーの作成を確認
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'POLICY_1D_1H';
```

**3. テーブルへの適用:**

```sql
-- ret_tag に作成したポリシーを適用
ALTER TABLE ret_tag ADD RETENTION policy_1d_1h;

-- ポリシーの適用を確認
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'RET_TAG';
-- 想定: RET_TAG、POLICY_1D_1H、状態（通常 WAITING）、初期の last_deleted_time（NULL）の行を表示。
```

**4. 古いデータを含むデータの取り込み:**

```tql
// 1 秒間隔の 150,000 件を生成する（現在までの約 41.7 時間）。
// 1 日より古いデータも含まれる。
FAKE(arrange(1, 150000, 1))
MAPVALUE(1, sin((2*PI*value(0)/100)))
MAPVALUE(0, timeAdd("now", strSprintf("-%.fs", 150000-value(0))))
PUSHVALUE(0, "sensor-a")
APPEND(table("ret_tag"))
```

**5. 初期データ件数の確認:**

```sql
-- 挿入した合計件数を確認
SELECT COUNT(*) FROM ret_tag;
-- 想定: 保持処理がまだ実行されていなければ 150000 件
```

**6. 保持処理の実行を待つ:**

ポリシーの `INTERVAL`（この例では 1 時間）を超える時間を待ちます。バックグラウンドの保持処理が自動実行されます。

**7. データ削除の確認:**

```sql
-- 保持処理の状態を再確認。LAST_DELETED_TIME が更新されている場合がある
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'RET_TAG';

-- 件数を再確認。初期件数より少なくなる。
-- ジョブ実行時点で 1 日より古いデータが削除されるため。
SELECT COUNT(*) FROM ret_tag;
-- 想定: 150000 未満。
```

**8. ポリシーの解除と削除:**

```sql
-- ret_tag の自動削除を停止
ALTER TABLE ret_tag DROP RETENTION;

-- 解除を確認（ret_tag の行がなくなる）
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'RET_TAG';

-- ポリシー定義を削除
DROP RETENTION policy_1d_1h;

-- 削除を確認
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'POLICY_1D_1H';
-- 想定: 行が返されない。
```
