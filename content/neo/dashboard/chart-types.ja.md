---
title: チャートタイプ別のオプション
type: docs
weight: 40
toc: true
---

チャートタイプはチャート設定画面の右上で選択します。選択できるタイプは **Line、Bar、Scatter、Adv scatter、Gauge、Pie、Liquid fill、Text、Geomap、Tql chart、Video** の 11 種類で、タイプによって下に表示されるオプションが変わります。複数のタイプで共通の Panel option・Legend・Panel padding・Tooltip・xAxis・yAxis は「チャート設定」のチャートオプションを参照してください。

Tql chart と Video は設定方法が異なるため、別のページ（「TQL チャート」「Video パネル」）で説明します。

## Line

{{< media slug="neo-dashboard/type-line" width="600" >}}

| オプション | 説明 |
|:-----|:-----|
| Fill area | 線の下を塗りつぶします。不透明度（0〜1）を指定します。 |
| Smooth line | 線を曲線で表示します。 |
| Show symbols | データポイントを表示します。 |
| Symbol type | シンボルの形（circle / rect / roundRect / triangle / diamond / pin / arrow） |
| Symbol size | シンボルのサイズ |
| Stack | 複数のシリーズを積み上げて表示します。 |
| Step style | 階段状の線で表示します。 |
| Large data mode | 大量データを表示するときのモードです。 |

## Bar

{{< media slug="neo-dashboard/type-bar" width="600" >}}

| オプション | 説明 |
|:-----|:-----|
| Large data mode | 大量データを表示するときのモードです。 |
| Polar mode | 棒を円形に配置します。 |
| - Max | 最大値 |
| - Start angle | 開始角度 |
| - Radius | 内側の半径（0 は中央を空けません） |
| - Polar size | 外側の半径（100 でパネル全体） |
| - Polar axis | X 軸の種類（time / category） |

棒の幅はシリーズ数とパネルサイズから自動的に計算されます。

## Scatter

{{< media slug="neo-dashboard/type-scatter" width="600" >}}

| オプション | 説明 |
|:-----|:-----|
| Large data mode | 大量データを表示するときのモードです。 |
| Symbol type | シンボルの形 |
| Symbol size | シンボルのサイズ |

## Adv scatter

{{< neo_since ver="8.0.46" />}}

{{< media slug="neo-dashboard/type-adv-scatter" width="600" >}}

X 軸と Y 軸の両方に値を使う散布図です。時間の代わりに**別のシリーズの値を X 軸（基準軸）** として使用します。

- **基準軸の指定**: 右側オプションの `xAxis > Series` で基準軸にするシリーズを 1 つ選びます。同時に選べるのは 1 つだけで、指定しない場合は最初のシリーズが基準軸になります。
- **点の描き方**: 基準軸以外のシリーズの値が、同じ時刻の基準シリーズの値と対応して 1 つの点（x, y）として描かれます。
- **基準シリーズを非表示にする**: 基準シリーズは X 座標にのみ使われるため、そのシリーズ行の **Visible** <img src="/images/web-ui/neo-dashboard/icons/dash_series_visible.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンをオフにして、チャートに単独で描かれないようにします。

下の画面は `demo.cpu` を基準軸に指定して Visible をオフにし、`demo.mem` を Y 軸の値として描いた例です。

| オプション | 説明 |
|:-----|:-----|
| Unit / Decimals | X 軸の値の単位と小数点以下の桁数 |
| Min / Max | X 軸の最小値・最大値 |
| Start at zero | X 軸に常に 0 を含めます。 |
| Series | X 軸に使用するシリーズ。デフォルトは最初のシリーズです。 |
| Symbol type / size | シンボルの形とサイズ |

## Gauge

{{< media slug="neo-dashboard/type-gauge" width="600" >}}

| オプション | 説明 |
|:-----|:-----|
| Min / Max | ゲージの最小値・最大値 |
| Label distance | ラベルと目盛り線の距離（負の値は外側） |
| Show axis tick | 目盛りを表示します。 |
| Setting line colors | 値の範囲ごとの線の色（0〜1 の比率で指定） |
| Show anchor / Size | 中央の円の表示とサイズ |
| Font size | ゲージ内部に表示する値のフォントサイズ |
| Offset from center | 値の表示位置の中心からの距離 |
| Unit | ゲージの値の単位 |
| Decimal | 小数点以下の桁数 |
| Active animation | アニメーションの使用 |

## Pie

{{< media slug="neo-dashboard/type-pie" width="600" >}}

| オプション | 説明 |
|:-----|:-----|
| Doughnut ratio | 中央を空ける比率（0〜100） |
| Nightingale mode | 値に応じて半径が変わるモード |

## Liquid fill

{{< media slug="neo-dashboard/type-liquid-fill" width="600" >}}

| オプション | 説明 |
|:-----|:-----|
| Shape | 形状（container / circle / rect / roundRect / triangle / diamond / pin / arrow） |
| Unit | 表示値の単位 |
| Digit | 小数点以下の桁数 |
| Font size | フォントサイズ |
| Wave min / max | 波形の最小値・最大値 |
| Wave amplitude | 波形の振幅（0 は直線） |
| Background color | 波形領域の背景色 |
| Wave animation | 波形アニメーションの使用 |
| Outline | 輪郭の表示 |

## Text

{{< neo_since ver="8.0.46" />}}

{{< media slug="neo-dashboard/type-text" width="600" >}}

最初のシリーズの値を大きな文字で表示し、2 つ目のシリーズを背景チャートとして描画します。

| オプション | 説明 |
|:-----|:-----|
| Font size | フォントサイズ |
| Unit | 単位 |
| Digit | 小数点以下の桁数 |
| Color | 既定の色。値の範囲を追加すると、範囲ごとに異なる色を指定できます。 |
| Series | テキストと背景チャートに使用するシリーズをそれぞれ指定します。 |
| Type | 背景チャートの種類（line / bar / scatter） |
| Opacity | 塗りつぶしの不透明度（0〜1、line のみ） |
| Symbol size | データポイントのサイズ（0 は非表示） |

## Geomap

{{< neo_since ver="8.0.46" />}}

{{< media slug="neo-dashboard/type-geomap" width="600" >}}

| オプション | 説明 |
|:-----|:-----|
| Time | ツールチップに時刻を表示します。 |
| Latitude, Longitude | ツールチップに緯度・経度を表示します。 |
| Interval type / value | X 軸の時間間隔（none / sec / min / hour。none は自動計算） |
| Use zoom control | 地図のズームコントロールを使用します。パネルメニューからも切り替えられます。 |
| Series | シリーズごとに次の項目を指定します。 |
| - Latitude / Longitude | 緯度・経度の列名 |
| - Marker shape | マーカーの形（marker / circleMarker / circle） |
| - Marker radius | マーカーの半径（circleMarker はピクセル、circle はメートル） |

## Line・Bar のオプションで作る派生形

エリア（Area）、積み上げ（Stacked）、階段（Step）チャートは独立したタイプではなく、Line・Bar のオプションの組み合わせです。

| 作りたい形 | タイプ | 設定 |
|:--|:--|:--|
| エリア | Line | `Fill area` をオン |
| 積み上げエリア | Line | `Fill area` + `Stack` |
| 階段 | Line | `Step style` |
| 縦棒 | Bar | デフォルト |
| 円形の棒 | Bar | `Polar mode` |
