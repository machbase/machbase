---
title: ロボットアームのデジタルツイン
type: docs
weight: 1000
---

ロボットアームの動作とセンサーデータを時系列で保存し、ダッシュボードで分析する Machbase Neo の Physical AI デモです。

{{< icon "github" >}} https://github.com/machbase/neo-pkg-robot-demo
<p/>

{{< youtube JeABxt2JYFI >}}

DROID ロボットデータセットに基づく Physical AI デモです。

**主なポイント**

- 32,212件のロボットフレームを保存
- 元のロボット軌跡を時間軸に沿って保存
- JSON に生の状態データと派生メトリクスをまとめて保持
- 単一の TAG テーブルでスキーマを簡素化
- JSON パスのロールアップで時間範囲を高速分析
- 特定時点のフレームと前後のウィンドウをリアルタイム UI から照会
- Physical AI データの再生、イベント検出、異常の可視化