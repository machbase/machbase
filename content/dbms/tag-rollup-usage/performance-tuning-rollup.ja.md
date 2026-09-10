---
type: docs
title: '6.11 ROLLUPのパフォーマンスチューニング'
weight: 110
toc: true
---

<a id="tuning-rollup"></a>

## 同じ結果を確認してからコストを比較

ROLLUPの効果は、読み取る生データの行数を減らすことにあります。
まずタグ、時間区間、NULL処理、集計基準が同じ結果になることを確認し、実行時間・CPU・I/O・メモリを比較します。
小さな例の実行時間は、本番性能を保証しません。

## 比較実習

```sql
CREATE TAG TABLE ch6_perf (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_perf_ru ON ch6_perf(value) INTERVAL 1 MIN;
INSERT INTO ch6_perf VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_perf VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_perf VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_perf VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_perf);
ALTER ROLLUP ch6_perf_ru FORCE;

SELECT DATE_TRUNC('minute', time) AS bucket,
       SUM(value), COUNT(value), AVG(value), MIN(value), MAX(value)
  FROM ch6_perf
 WHERE name = 'TEMP_01'
   AND time >= TO_DATE('2026-01-01 00:00:00')
   AND time < TO_DATE('2026-01-01 00:02:00')
 GROUP BY bucket ORDER BY bucket;

SELECT rollup('min', 1, time) AS bucket,
       SUM(value), COUNT(value), AVG(value), MIN(value), MAX(value)
  FROM ch6_perf
 WHERE name = 'TEMP_01'
   AND time >= TO_DATE('2026-01-01 00:00:00')
   AND time < TO_DATE('2026-01-01 00:02:00')
 GROUP BY bucket ORDER BY bucket;

EXPLAIN SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_perf WHERE name = 'TEMP_01'
 GROUP BY bucket;
```

両方の結果は、00:00が合計30・件数2・平均15・最小値10・最大値20、
00:01が合計30・件数1・平均30・最小値30・最大値30です。
元データを読むDATE_TRUNCクエリの実行計画も、同じ方法で確認します。

## 運用負荷の測定

| 項目 | 併せて記録する条件 |
|---|---|
| 入力スループット | タグ数・入力レート・行幅・同時入力クライアント数 |
| クエリ遅延 | タグ範囲・バケット・同時クエリ数・コールドまたはウォームキャッシュ |
| 集計遅延 | 階層別のgap・ジョブ状態・処理時間 |
| 保存容量 | 元データ・集計・インデックス・圧縮・レプリカ |
| 変更の影響 | WAKEUP周期と階層の変更前後の入力・検索コスト |

WAKEUPを短くすると、同じバケットに部分集計がより頻繁に作成される場合があります。
集計バケットを小さくすると、保存量と再集計量が増えます。両方の間隔を同じチューニング項目として扱わないでください。
単独実行だけでなく、入力と検索が同時に進む状況も測定します。

## 階層サイズの意味

1つのタグが30日間のすべての区間にデータを持つと仮定した場合の、論理バケット数です。

| 検索区間 | バケット数 |
|---|---:|
| 1秒 | 2,592,000 |
| 1分 | 43,200 |
| 1時間 | 720 |
| 1日 | 30 |

これは物理的な保存行数ではありません。
複数の部分集計、空の区間、NULL、条件フィルターを含む実際の保存量は、サンプルのロードで測定します。
最も粗い候補が常に正しい結果を作るわけでもないため、必要な解像度・origin・候補選択の制約を併せて確認してください。

日単位の結果には、適用可能なHOUR/MIN/SEC集計を再集計します。
24 HOUR ROLLUPを`rollup('day', 1, ...)`の代替保存階層として推奨しません。
[クエリ候補の規則](../query-syntax-rollup/)と実際のEXPLAINを基準にしてください。

## 遅延と不一致の区別

gap=0は処理位置に追いついたことを表し、元データの補正が反映済みであることを意味しません。
性能比較の前に、集計の進行状況と過去の訂正状態を区別し、定義とフィルターが一致するか確認してください。
適用可能なROLLUPがない`rollup()`クエリを、元データの性能測定に使用しないでください。

## クリーンアップ

```sql
DROP ROLLUP ch6_perf_ru;
DROP TABLE ch6_perf;
```

[制御と状態](../ingestion-control-rollup/)、[階層設計](../target-tag-table-design/)、
[トラブルシューティング](../../troubleshooting/rollup/)を参照して次の調整を選択してください。
