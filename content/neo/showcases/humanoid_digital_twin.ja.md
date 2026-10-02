---
title: ヒューマノイドのデジタルツイン
type: docs
weight: 998
---

ヒューマノイドの関節・姿勢・状態データをリアルタイムに収集し、Neo ダッシュボードで動作の異常を確認します。

{{< icon "github" >}} https://github.com/machbase/neo-humanoid-demo
<p/>

{{< youtube OEYVL7ysXo4 >}}

Machbase Neo を使ってヒューマノイドロボットのデータを可視化するデモです。

**主なポイント**

- Humanoid Everyday / OpenHE Motion データの保存
- センサータイムラインと連動したリアルタイムのロボット動作再生
- 高速な時系列データの照会と分析

**デモの機能**

- Unitree G1 の3D動作再生
- 関節、IMU、オドメトリー、手の圧力センサーを可視化
- RGB・Depth・LiDAR の状態表示
- Episode / Task 単位での探索
- Live Query によるフレーム照会
- 複数のカメラ視点に対応
- 選択した Episode のセンサーデータをダウンロードし、クエリ URL をコピー

ロボットの動作とセンサーデータを1つのタイムラインで分析し、Machbase Neo を活用した Physical AI データの利用方法を確認できます。