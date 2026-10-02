---
title: 設備階層とタグの探索
type: docs
weight: 965
---

収集したタグを Plant、Production Line、Equipment の階層に整理し、Data Viewer で確認する方法を紹介します。

{{< youtube wdiUfiA5_10 >}}

このガイドでは、OPC UA で収集したタグを設備階層に整理し、確認したい設備のデータをすばやく探す方法を紹介します。

産業設備では、温度、振動、モーター電流、運転速度など、1台の設備から数十から数百のタグが生成されることがあります。タグを単純な一覧で管理すると、必要なデータを見つけにくくなります。

Machbase Neo では、Plant（工場）→ Production Line（生産ライン）→ Equipment（設備）の Asset Hierarchy にタグを整理し、設備とデータを体系的に管理できます。

たとえば Smart Plant 1 の下に Assembly Line A を作成し、その生産ラインに Press Machine 01、Conveyor 01、Robot Arm 01 などの設備を配置します。各設備には、温度、振動、モーター電流、運転速度などのタグを関連付けます。

Data Viewer ではタグ一覧だけでなく、Asset Hierarchy から設備とタグを選んでデータを照会できます。複雑なタグ名を覚えていなくても、必要なデータを直感的に見つけられます。

この動画では、OPC UA で収集したタグを Asset Hierarchy に整理し、Data Viewer で設備データを効率よく確認する方法を紹介します。