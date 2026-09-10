---
toc: true
title: "vizspec"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`vizspec`モジュールは、ADVNドキュメントの作成、検証、解析、出力形式の変換を行うJSH APIです。
ADVNはAnalysis Data Visualization Notationの略で、分析結果の可視化用の、レンダラーに依存しないドキュメント形式です。

ADVNを使うと、データの意味とレンダラー固有の出力を分離できます。

## ADVNと`vizspec` {#advn과-vizspec}

- ADVNは、意味を表すセマンティックレイヤーです。
- ADVNはドキュメント形式であり、分析結果の意味を表現します。
- `vizspec`モジュールは、ADVNドキュメントを作成・変換するJSH APIです。
- `viz`は、ADVNドキュメントを検証・プレビュー・エクスポートするコマンドです。

## 基本例 {#기본-예제}

```js {linenos=table,linenostart=1}
const vizspec = require('vizspec');

const spec = new vizspec.Builder()
    .setDomain({
        kind: 'time',
        timeformat: vizspec.Timeformat.ns,
    })
    .setXAxis({ id: 'time', type: 'time', label: 'Time' })
    .addYAxis({ id: 'value', type: 'linear', label: 'Value' })
    .addTimeBucketValueSeries({
        id: 'series-1',
        axis: 'value',
        data: [
            ['1712102400000000000', 10],
            ['1712102460000000000', 12],
        ],
    })
    .build();
```

## 定数 {#상수}

このモジュールは、以下の定数グループを提供します。

- `RepresentationKind`
- `AnnotationKind`
- `Timeformat`

アプリケーションのコードでADVNの値を明示的に指定する場合、これらの定数を使うと誤記を減らせます。

### RepresentationKind {#representationkind}

| メンバー | 値 | 説明 |
| --- | --- | --- |
| `RepresentationKind.rawPoint` | `raw-point` | `[x, y]`形式の生のポイントサンプルです。 |
| `RepresentationKind.timeBucketValue` | `time-bucket-value` | 単一の数値を持つ時間バケットの集計表現です。 |
| `RepresentationKind.timeBucketBand` | `time-bucket-band` | `min/max/avg`の帯域値を持つ時間バケットの集計表現です。 |
| `RepresentationKind.distributionHistogram` | `distribution-histogram` | ヒストグラム分布のバケット表現です。 |
| `RepresentationKind.distributionBoxplot` | `distribution-boxplot` | 箱ひげ図の分布グループ表現です。 |
| `RepresentationKind.eventPoint` | `event-point` | 1つの時刻・値の位置で発生した瞬間的なイベントの表現です。 |
| `RepresentationKind.eventRange` | `event-range` | `from/to`の時間範囲を持つ継続イベントの表現です。 |

### AnnotationKind {#annotationkind}

| メンバー | 値 | 説明 |
| --- | --- | --- |
| `AnnotationKind.point` | `point` | 1つの位置を指すポイント注釈です。 |
| `AnnotationKind.line` | `line` | しきい値または参照線の注釈です。 |
| `AnnotationKind.range` | `range` | 範囲を強調する範囲注釈です。 |

### Timeformat {#timeformat}

| メンバー | 値 | 説明 |
| --- | --- | --- |
| `Timeformat.rfc3339` | `rfc3339` | RFC3339文字列による時刻表現です。 |
| `Timeformat.s` | `s` | エポック秒です。 |
| `Timeformat.ms` | `ms` | エポックミリ秒です。 |
| `Timeformat.us` | `us` | エポックマイクロ秒です。 |
| `Timeformat.ns` | `ns` | エポックナノ秒です。 |

## parse() {#parse}

ADVNのJSON文字列を解析し、正規化したspecオブジェクトを返します。

<h6>構文</h6>

```js
parse(text)
```

<h6>パラメーター</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `text` | string | 解析するADVN JSON文字列です。 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const vizspec = require('vizspec');
const spec = vizspec.parse('{"version":1,"series":[]}');
console.println(spec.version);
```

## stringify() {#stringify}

specオブジェクトをADVNのJSON文字列にシリアライズします。

<h6>構文</h6>

```js
stringify(spec)
```

<h6>パラメーター</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `spec` | object | シリアライズするADVN specオブジェクトです。 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const vizspec = require('vizspec');
const text = vizspec.stringify(vizspec.createSpec({ version: 1 }));
console.println(typeof text);
```

## validate() {#validate}

specオブジェクトを検証します。構造やフィールドの組み合わせが不正な場合は、例外を発生させます。

<h6>構文</h6>

```js
validate(spec)
```

<h6>パラメーター</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `spec` | object | 検証するADVN specオブジェクトです。 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const vizspec = require('vizspec');
const ok = vizspec.validate(vizspec.createSpec({ version: 1 }));
console.println(ok);
```

## normalize() {#normalize}

部分的に指定したspecオブジェクトを正規化し、基本構造のフィールドを補完します。

<h6>構文</h6>

```js
normalize(spec)
```

<h6>パラメーター</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `spec` | object | 正規化する部分的なADVN specオブジェクトです。 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const vizspec = require('vizspec');
const spec = vizspec.normalize({});
console.println(spec.version);
```

## createSpec() {#createspec}

初期化オブジェクトからspecオブジェクトを作成し、正規化・検証します。

<h6>構文</h6>

```js
createSpec(init)
```

<h6>パラメーター</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `init` | object | ADVN specの初期値オブジェクトです。 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const vizspec = require('vizspec');
const spec = vizspec.createSpec({
    domain: { kind: 'time', timeformat: vizspec.Timeformat.ns },
    series: [],
});
console.println(spec.domain.kind);
```

## listSeries() {#listseries}

`spec.series`の正規化された概要一覧を返します。

<h6>構文</h6>

```js
listSeries(spec)
```

<h6>パラメーター</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `spec` | object | 確認するADVN specオブジェクトです。 |

<h6>返されるフィールド</h6>

| フィールド | 型 | 説明 |
| --- | --- | --- |
| `index` | integer | `spec.series`内の、0から始まる系列インデックスです。 |
| `id` | string | 系列IDです。 |
| `name` | string | 指定されている場合の系列名です。 |
| `title` | string | 表示タイトルです。`name`があれば`name`、なければ`id`を使用します。 |
| `kind` | string | 表現の種類です。 |
| `tuiLinesCompatible` | boolean | `toTUILines()`で描画できる系列かどうかを表します。 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const listed = vizspec.listSeries(spec);
console.println(listed[0].id);
console.println(listed[0].tuiLinesCompatible);
```

## 系列ヘルパー {#series-helper}

系列ヘルパー関数は、正しい表現の種類と既定のフィールド構成を持つ系列オブジェクトを作成します。

使用できるヘルパー：

- `rawPointSeries(init)`
- `timeBucketValueSeries(init)`
- `timeBucketBandSeries(init)`
- `distributionHistogramSeries(init)`
- `distributionBoxplotSeries(init)`
- `eventPointSeries(init)`
- `eventRangeSeries(init)`

<h6>構文</h6>

```js
timeBucketValueSeries(init)
eventRangeSeries(init)
```

<h6>共通の初期化フィールド</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `id` | string | 系列の識別子です。 |
| `name` | string | アダプターで使用する表示名です。 |
| `axis` | string | 数値レンダラーで使用するY軸IDです。 |
| `representation` | object | フィールドまたは表現メタデータの上書きに使用します。 |
| `data` | array | 系列ペイロードの行配列です。 |
| `style` | object | color、opacityなど、レンダラーへのヒントとなるスタイル値です。 |
| `quality` | object | coverage、rowCountなどの品質メタデータです。 |
| `source` | object | 系列の出所を示すメタデータです。 |
| `extra` | object | 箱ひげ図の外れ値など、表現固有の追加データです。 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const vizspec = require('vizspec');
const series = vizspec.timeBucketValueSeries({
    id: 'cpu',
    axis: 'value',
    data: [['1712102400000000000', 10]],
});
console.println(series.representation.kind);
```

## 注釈ヘルパー {#annotation-helper}

注釈ヘルパー関数は、正しい注釈の種類を持つトップレベルの注釈オブジェクトを作成します。

使用できるヘルパー：

- `pointAnnotation(init)`
- `lineAnnotation(init)`
- `rangeAnnotation(init)`

<h6>構文</h6>

```js
lineAnnotation(init)
rangeAnnotation(init)
```

<h6>共通の初期化フィールド</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `axis` | string | 対象の軸IDです。 |
| `label` | string | ユーザーに表示する注釈ラベルです。 |
| `value` | any | 線またはポイントの注釈で使用する値です。 |
| `at` | any | ポイント注釈の位置です。 |
| `from` | any | 範囲の開始値です。 |
| `to` | any | 範囲の終了値です。 |
| `style` | object | 省略可能な、レンダラーへのヒントとなるスタイル値です。 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const vizspec = require('vizspec');
const annotation = vizspec.lineAnnotation({ axis: 'value', value: 80, label: 'warning' });
console.println(annotation.kind);
```

## Builder {#builder}

メソッドチェーンでADVNドキュメントを作成するには、ビルダーを使用します。

<h6>構文</h6>

```js
new Builder([init])
```

<h6>主なメソッド</h6>

| メソッド | 説明 |
| --- | --- |
| `setDomain(definition)` | `spec.domain`を設定します。 |
| `setXAxis(definition)` | `spec.axes.x`を設定します。 |
| `addYAxis(definition)` | Y軸定義を1つ追加します。 |
| `addRawPointSeries(definition)` | `raw-point`系列を追加します。 |
| `addTimeBucketValueSeries(definition)` | `time-bucket-value`系列を追加します。 |
| `addTimeBucketBandSeries(definition)` | `time-bucket-band`系列を追加します。 |
| `addDistributionHistogramSeries(definition)` | ヒストグラム系列を追加します。 |
| `addDistributionBoxplotSeries(definition)` | 箱ひげ図系列を追加します。 |
| `addEventPointSeries(definition)` | event-point系列を追加します。 |
| `addEventRangeSeries(definition)` | event-range系列を追加します。 |
| `addAnnotation(definition)` | 注釈オブジェクトを追加します。 |
| `addLineAnnotation(definition)` | 線の注釈を追加します。 |
| `addRangeAnnotation(definition)` | 範囲の注釈を追加します。 |
| `setView(definition)` | `spec.view`を設定します。 |
| `setMeta(definition)` | `spec.meta`を設定します。 |
| `build()` | 正規化したspecを返します。 |
| `stringify()` | ビルド結果を文字列にシリアライズします。 |
| `listSeries()` | 正規化した系列の概要一覧を返します。 |
| `toEChartsOption(options)` | ビルド結果をEChartsのオプションに変換します。 |
| `toTUILines(options)` | ビルド結果を、ターミナル用のTUIグラフの行配列に変換します。 |
| `toTUIBlocks(options)` | ビルド結果をTUIブロックの配列に変換します。 |
| `toSVG(options)` | ビルド結果をSVG文字列に変換します。 |
| `toPNG([svgOptions[, pngOptions]])` | ビルド結果をPNGバイナリデータに変換します。 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const vizspec = require('vizspec');

const spec = new vizspec.Builder()
    .setDomain({ kind: 'time', timeformat: vizspec.Timeformat.ns })
    .setXAxis({ id: 'time', type: 'time', label: 'Time' })
    .addYAxis({ id: 'value', type: 'linear', label: 'Temperature' })
    .addTimeBucketBandSeries({
        id: 'sensor-1',
        axis: 'value',
        data: [
            ['1712102400000000000', 18, 24, 21],
            ['1712102460000000000', 17, 23, 20],
        ],
    })
    .build();
```

## 出力アダプター {#output-adapter}

### toEChartsOption() {#toechartsoption}

specをEChartsのオプションオブジェクトに変換します。

<h6>構文</h6>

```js
toEChartsOption(spec[, options])
```

<h6>パラメーター</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `spec` | object | 描画するADVN specオブジェクトです。 |
| `options` | object | 省略可能な出力側の時刻設定です。 |

<h6>オプションフィールド</h6>

| オプション | 型 | 既定値 | 説明 |
| --- | --- | --- | --- |
| `timeformat` | string | `rfc3339` | ECharts用に時刻値をエンコードする際の、出力時刻の表現です。 |
| `tz` | string | ローカルタイムゾーン | RFC3339の時刻値を出力する際に適用するタイムゾーンです。 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const option = vizspec.toEChartsOption(spec, {
    timeformat: vizspec.Timeformat.rfc3339,
    tz: 'Asia/Seoul',
});
console.println(JSON.stringify(option));
```

### toTUILines() {#totuilines}

スパークライン対応の最初の系列を、ターミナル用のスパークライン行配列に変換します。

<h6>構文</h6>

```js
toTUILines(spec[, options])
```

<h6>パラメーター</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `spec` | object | 描画するADVN specオブジェクトです。 |
| `options` | object | 省略可能なスパークラインの描画設定です。 |

<h6>オプションフィールド</h6>

| オプション | 型 | 既定値 | 説明 |
| --- | --- | --- | --- |
| `height` | integer | `3` | raw-pointとtime-bucket-valueの行出力に使用するグラフの高さです。 |
| `width` | integer | `40` | 値をサンプリングし、スパークライン本体を描画する際の幅です。 |
| `seriesId` | string | 最初の対応系列 | `series[].id`で、描画する系列を選択します。 |
| `timeformat` | string | `rfc3339` | スパークラインのX軸ラベルに使用する出力時刻形式です。 |
| `tz` | string | ローカルタイムゾーン | スパークラインのX軸ラベルに適用するタイムゾーンです。 |

注意：

- `seriesId`を省略すると、`toTUILines()`はスパークライン対応の最初の系列を返します。
- `seriesId`を指定すると、`series[].id`が一致する系列を描画します。
- 選択できる系列IDを確認するには、`listSeries()`を使用します。
- 指定した`seriesId`が存在しない場合や、スパークライン非対応の系列を指す場合は、エラーが発生します。
- 戻り値は、複数行のTUIグラフを構成するターミナル用の行配列です。
- `toTUIBlocks()`と異なり、軸ラベルを含む展開された複数行グラフ形式を維持します。
- `height`は、`raw-point`と`time-bucket-value`の出力だけに適用します。`time-bucket-band`は、既存の`max/avg/min`形式を維持します。
- 現在の`toTUILines()`は、`rows`と`compact`オプションを受け取っても使用しません。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const lines = vizspec.toTUILines(spec, { width: 32, height: 5, seriesId: 'series-1' });
console.println(lines.join('\n'));
```

CLI 例:

```sh
viz lines --height 5 --series series-1 sample.json
```


<details>
<summary>ソースコード全体：</summary>

```js {linenos=table,linenostart=1}
const vizspec = require('vizspec');
const { Client } = require('machcli');

const dbConf = {
    host: '127.0.0.1', port: 5656,
    user: 'sys', password: 'manager',
};

var db, conn, rows;
var data = [];
try {
    db = new Client(dbConf);
    conn = db.connect();
    rows = conn.query(`SELECT TIME, VALUE FROM EXAMPLE
        WHERE NAME = ? AND TIME > now - 2h`, 'machbase:ps:cpu_percent');
    for (const row of rows) {
        data.push([row.TIME, row.VALUE]);
    }
} catch( e ) {
    console.println("ERROR", e.message);
} finally {
    rows && rows.close();
    conn && conn.close();
    db && db.close();
}

const spec = new vizspec.Builder()
    .setDomain({ kind: 'time', timeformat: vizspec.Timeformat.rfc3339 })
    .setXAxis({ id: 'time', type: 'time', label: 'Time' })
    .addYAxis({ id: 'value', type: 'linear', label: 'Value' })
    .addTimeBucketValueSeries({ id: 'series-1', axis: 'value', data: data })
    .build();

console.println(vizspec.toTUILines(spec, { width: 80 }).join('\n'));
```
</details>

出力例：

{{< figure src="/neo/jsh/img/vizspec_sparkline.jpg" width="637" >}}

### toTUIBlocks() {#totuiblocks}

specを、ターミナルで確認するためのTUIブロックオブジェクト配列に変換します。

<h6>構文</h6>

```js
toTUIBlocks(spec[, options])
```

<h6>パラメーター</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `spec` | object | 描画するADVN specオブジェクトです。 |
| `options` | object | 省略可能なTUI描画設定です。 |

<h6>オプションフィールド</h6>

| オプション | 型 | 既定値 | 説明 |
| --- | --- | --- | --- |
| `width` | integer | `40` | スパークライン、ヒストグラム、タイムラインの描画幅です。 |
| `rows` | integer | `8` | table、histogram、eventブロックに表示する詳細行の最大数です。 |
| `compact` | boolean | `false` | 系列の概要と生データの表ブロックを非表示にします。 |
| `timeformat` | string | `rfc3339` | 出力時刻の形式です。`rfc3339`、`s`、`ms`、`us`、`ns`を使用できます。 |
| `tz` | string | ローカルタイムゾーン | 出力時刻値に適用するタイムゾーンです。 |

<h6>戻り値</h6>

戻り値はブロックオブジェクトの配列です。各ブロックは、以下の共通フィールドを持つ場合があります。

| フィールド | 型 | 説明 |
| --- | --- | --- |
| `type` | string | ブロックの種類です。例：`summary`、`series-summary`、`sparkline`、`bandline`、`bars`、`box-summary`、`event-list`、`timeline`、`table`、`annotations`。 |
| `title` | string | ブロックのタイトルです。 |
| `stats` | array | 概要系ブロックで使用する`{ label, value }`オブジェクトの配列です。 |
| `lines` | array | sparkline、timeline、histogramなどの行形式のブロックで使用する文字列配列です。現在の`sparkline`ブロックは、コンパクトなスパークラインを1行返します。 |
| `columns` | array | `table`ブロックの列名の配列です。 |
| `rows` | array | `table`ブロックの行配列です。各行は、列順に並ぶ値の配列です。 |
| `meta` | object | ブロック固有の付加情報です。例：`representation`、`axis`、`totalRows`、`truncated`。 |

実際に設定されるフィールドは`type`によって異なります。たとえば、`sparkline`ブロックは主に`lines`を使用し、`table`ブロックは`columns`、`rows`、`meta`を使用します。

注意：

- `toTUIBlocks()`の`sparkline`ブロックは、従来のコンパクトなスパークライン表現を返します。
- 軸ラベルと複数のグラフ行を含む展開形式が必要な場合は、`toTUILines()`を使用します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const blocks = vizspec.toTUIBlocks(spec, {
    width: 80,
    rows: 5,
    timeformat: vizspec.Timeformat.rfc3339,
    tz: 'Asia/Seoul',
});
console.println(blocks[0].type);           // summary
console.println(blocks[0].stats[0].label); // series
console.println(blocks[2].type);           // sparkline
console.println(blocks[2].lines[0]);       // ▁▃▅▇█▆▄▂
```

### toSVG() {#tosvg}

specをSVG文字列に変換します。

<h6>構文</h6>

```js
toSVG(spec[, options])
```

<h6>パラメーター</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `spec` | object | 描画するADVN specオブジェクトです。 |
| `options` | object | 省略可能なSVG描画設定です。 |

<h6>オプションフィールド</h6>

| オプション | 型 | 既定値 | 説明 |
| --- | --- | --- | --- |
| `width` | integer | `960` | SVGキャンバスの幅（ピクセル）です。 |
| `height` | integer | `420` | SVGキャンバスの高さ（ピクセル）です。 |
| `padding` | integer | `48` | グラフの外側の余白（ピクセル）です。 |
| `background` | string | `white` | SVGの背景色です。 |
| `fontFamily` | string | `sans-serif` | 既定のフォントファミリーです。 |
| `fontSize` | integer | `12` | 既定のフォントサイズ（ピクセル）です。 |
| `showLegend` | boolean | `true` | 凡例を描画するかどうかを制御します。 |
| `title` | string | 空 | 省略可能なグラフのタイトルです。 |
| `timeformat` | string | `rfc3339` | 軸ラベルと出力時刻値に使用する時刻形式です。 |
| `tz` | string | ローカルタイムゾーン | RFC3339時刻の出力に適用するタイムゾーンです。 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const svg = vizspec.toSVG(spec, {
    title: 'Sensor Overview',
    width: 960,
    height: 420,
    timeformat: vizspec.Timeformat.rfc3339,
    tz: 'Asia/Seoul',
});
```

### toPNG() {#topng}

specをPNGバイナリデータに変換します。戻り値は`ArrayBuffer`で、必要に応じて`new Uint8Array(png)`で読み取れます。

<h6>構文</h6>

```js
toPNG(spec[, options])
```

<h6>パラメーター</h6>

| 名前 | 型 | 説明 |
| --- | --- | --- |
| `spec` | object | 描画するADVN specオブジェクトです。 |
| `options` | object | 省略可能な、グラフレイアウト・テキスト・出力時刻・ラスタライズの統合設定です。 |

<h6>オプションフィールド</h6>

レイアウトとテキストのフィールド：

| オプション | 型 | 既定値 | 説明 |
| --- | --- | --- | --- |
| `width` | integer | `960` | ラスター拡大前の出力幅（ピクセル）です。 |
| `height` | integer | `420` | ラスター拡大前の出力高さ（ピクセル）です。 |
| `padding` | integer | `48` | グラフの外側の余白（ピクセル）です。 |
| `background` | string | `white` | SVGレイアウトとPNGラスター出力に共通で適用する背景色です。 |
| `fontFamily` | string | `sans-serif` | 既定のフォントファミリーです。 |
| `fontSize` | integer | `12` | 既定のフォントサイズ（ピクセル）です。 |
| `showLegend` | boolean | `true` | 凡例を描画するかどうかを制御します。 |
| `title` | string | 空 | 省略可能なグラフのタイトルです。 |
| `timeformat` | string | `rfc3339` | 軸ラベルと出力時刻値に使用する時刻形式です。 |
| `tz` | string | ローカルタイムゾーン | RFC3339時刻の出力に適用するタイムゾーンです。 |

ラスタライズのフィールド：

| オプション | 型 | 既定値 | 説明 |
| --- | --- | --- | --- |
| `scale` | number | `1` | SVGベースのレイアウトを倍率に従って拡大し、ラスタライズします。 |
| `dpi` | integer | 未設定 | `scale`がない場合に使用する目標DPIです。内部で`dpi / 96`の倍率として適用します。 |
| `theme` | string | `mrtg` | PNGテーマ名です。現在は`mrtg`だけに対応しています。 |

注意：

- `scale`と`dpi`を両方指定すると、`scale`が優先されます。
- 現在のPNGレンダラーは、MRTG形式の出力を生成します。
- JavaScript APIは、単一の`options`オブジェクトを受け取り、内部でレイアウトとラスタライズのフィールドに分割します。
- 後方互換性のため、従来の`toPNG(spec, svgOptions, pngOptions)`の呼び出し形式にも対応しています。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const png = vizspec.toPNG(spec, {
    title: 'Sensor Overview',
    width: 640,
    height: 240,
    scale: 2,
    theme: 'mrtg'
});
const bytes = new Uint8Array(png);
console.println(bytes[0].toString(16));
```

## 時刻の処理 {#시간-처리}

エポックタイムスタンプを`s`、`ms`、`us`、`ns`形式で使用すると、値自体がUTCに基づく絶対時刻を表すため、
入力データにタイムゾーンを明示する必要はありません。タイムゾーンは、元のタイムスタンプに付ける情報ではなく、
そのタイムスタンプを読みやすい文字列として出力する際のオプションです。

特に`ns`は桁数が大きく、JavaScriptの`number`で表すと精度が失われる場合があります。
たとえば、`1712102400000000000`などの値は、IEEE 754倍精度浮動小数点数の安全な整数範囲を超えるため、
ナノ秒のエポック時刻は、文字列で渡すことを推奨します。

Machbase Neoのタイムスタンプデータには、次の組み合わせを推奨します。

- `timeformat: vizspec.Timeformat.ns`
- JavaScriptのnumberではなく、文字列のタイムスタンプを使用

例:

```js
const spec = vizspec.createSpec({
    domain: {
        kind: 'time',
        timeformat: vizspec.Timeformat.ns,
    },
    series: [vizspec.eventRangeSeries({
        id: 'maintenance',
        data: [['1712102400000000000', '1712102460000000000', 'maintenance']],
    })],
});
```


## 時刻の表示 {#시간-렌더링}

データソースの時刻エンコーディングと出力時の時刻表現は、別々に扱います。

- `domain.timeformat`は、ADVNドキュメント内のタイムスタンプのエンコーディングを表します。
- アダプターオプションの`timeformat`と`tz`は、そのタイムスタンプを表示する形式とタイムゾーンを表します。

アダプターオプションを省略すると、`vizspec`アダプターは既定で`rfc3339`とローカルタイムゾーンを使用します。

例:

```js
const svg = vizspec.toSVG(spec, {
    title: 'CPU Usage',
    width: 960,
    height: 420,
    timeformat: vizspec.Timeformat.rfc3339,
    tz: 'Asia/Seoul',
});
```

同じ規則は、`toTUIBlocks()`と`toEChartsOption()`にも適用されます。

## `viz`コマンドの使用 {#viz-명령어-사용}

作成した仕様を検証するには、次のように実行します。

```sh
/work > viz validate cpu-usage.json
VALID version=1 series=1 annotations=1
```

ターミナルで確認するには、次のように実行します。

```sh
/work > viz view cpu-usage.json
```

SVGに出力するには、次のように実行します。

```sh
/work > viz export --title "CPU Usage" --output cpu-usage.svg cpu-usage.json
```

出力時刻形式とタイムゾーンを明示するには、次のように実行します。

```sh
/work > viz view --timeformat rfc3339 --tz Asia/Seoul cpu-usage.json
```
