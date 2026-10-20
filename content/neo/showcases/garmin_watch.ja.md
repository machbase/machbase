---
title: Garmin ウォッチ
type: docs
weight: 485
toc: true
---

あるランナーの Garmin ウォッチの1年分の記録（約140万ポイント）を Machbase Neo に集めた結果を紹介します。

{{< icon "github" >}} https://github.com/machbase/neo-pkg-garmin
<p/>

{{< youtube gCQw0rRHAlA >}}

Garmin ウォッチの1年分の健康データを使い、Machbase Neo で分析するデモを作成しました。

主なポイント

- あるランナーの健康・運動記録を約140万ポイント収集
- App Store からインストールして Garmin アカウントでログインすると、1時間ごとに自動収集し、過去1年分の記録も取得
- 心拍数・ストレス・歩数・運動データを Machbase Neo にまとめて保存
- TQL ベースの12個のダッシュボードで月別の傾向と運動カレンダーを可視化
- 距離とペースが近いランニングを10組比較し、心拍数の低下を確認
- AI チャットで SQL・TQL を生成・実行し、会話内にチャートを表示
- 別のツールを使わず、データ保存からダッシュボード・AI 分析までを連携

※ Garmin とは無関係の非公式ツールです。ご自身のアカウントとデータのみで使用することを目的としています。
