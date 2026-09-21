---
title: Tag Analyzer
type: docs
weight: 26
toc: true
---

Tag Analyzer is Machbase Neo's interactive tool for exploring time-series data in tag tables.

It can be used to:

- Create charts for multiple tags.
- Adjust and synchronize time ranges.
- Compare charts with Overlap Chart.
- Inspect raw values.
- Analyze frequencies with FFT.
- Save charts and settings as a board to reopen later.

<span id="1-quickstart"></span>

## 1. Create a Tag Analyzer Demo {#overview}

{{< figure
  src="/images/tag-analyzer/created-tag-analyzer-chart.png"
  link="/images/tag-analyzer/created-tag-analyzer-chart.png"
  alt="Tag Analyzer board showing a temperature tag chart and time-range navigator"
>}}

### 1.1 Open a Tag Analyzer Tab {#create-tag-analyzer-tab}

Click **+**, then choose **TAG ANALYZER** to open a new board.

{{< tag-analyzer-features
  id="open-tab"
  title="Open a Tag Analyzer Tab"
  caption="Figure 1.1: Open a Tag Analyzer Tab"
>}}

### 1.2 Add Sample Data (Optional) {#prepare-example-data}

Use this sample data to try Tag Analyzer. Skip this section if you already have data.

{{< tag-analyzer-features
  id="example-editors"
  title="SQL and TQL Editors"
  caption="Figure 1.2: SQL and TQL Editors"
>}}

**Create the sample table (run once in a SQL tab)**

```sql
CREATE TAG TABLE IF NOT EXISTS TAG_ANALYZER_DEMO (
    NAME VARCHAR(80) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

**Insert data into the sample table (run in the TQL editor)**

```js
FAKE(oscillator(
    freq(1/60, 10, 20),
    range('now-10m', '10m', '1s')
))
PUSHVALUE(0, 'temperature')
APPEND(table('TAG_ANALYZER_DEMO'))
```

### 1.3 Create Your First Chart {#create-tag-analyzer}

In the Tag Analyzer tab, click **New Chart** to open the chart creation dialog.
Use your own table and tag, or follow the sample settings below.

{{< tag-analyzer-features
  id="create-chart"
  title="Create Your First Chart"
  caption="Figure 1.3: Create Your First Chart"
>}}

### 1.4 Screen Overview {#screen-overview}

Your chart is ready. Use Tag Analyzer to explore and analyze your data.

The image below shows the layout of Tag Analyzer.

{{< tag-analyzer-features
  id="overview"
  title="Screen Overview"
  caption="Figure 1.4: Screen Overview"
>}}

## 2. Board Control {#2-board-controls}

Use the board toolbar for shared ranges, refresh, saving, and overlap.

{{< tag-analyzer-features
  id="board-controls"
  title="Board Control"
  caption="Figure 2: Board Control"
>}}

### 2.1 Add a New Chart {#add-a-new-chart}

Click **New Chart** to add a chart to the current board.

{{< tag-analyzer-features
  id="add-chart"
  title="Create a new chart from the board"
  caption="Figure 2.1: Add a New Chart"
>}}

### 2.2 Board Range Settings {#set-shared-ranges}

Click **TIME** to set the shared navigator range for all time-based charts, or **DIST**
for all distance-based charts. Both use **From/To**.

*A panel's own range settings take priority.*

| X-axis | From → To (example) | Meaning |
|---|---|---|
| Time | `first` → `last` | All generated sample data. |
| Time | `last-5m` → `last` | The last five minutes of the sample. |
| Time | `first` → `first+5m` | The first five minutes of the sample. |

You can also enter dates and times or choose a quick range.
Numeric ranges provide a slider and quick windows. The start must be less than the end.


### 2.3 Refresh {#refresh-and-show-all-data}

- **Refresh data:** reload all panels, keeping their current ranges.
- **Refresh ranges:** recheck data extents and reapply configured ranges, including expressions
  such as `last-5m`.
- **Expand all panels to full data range:** show all available data in each panel.

Without configured ranges, range refresh shows a central window. Use the full-range button to see all data.

### 2.4 Save and Reopen {#save-changes-or-create-a-copy}

**Save** writes the board to its current `.taz` file. **Save as** chooses another name or folder.
Use **Ctrl+S** (**Cmd+S** on macOS) to save. Editor changes must be applied before saving.

A `.taz` file stores chart configuration, ranges, highlights, and annotations. It does not copy
the table data.

<span id="save-and-reopen"></span>

Close the board tab, then click the saved file in File Explorer to reopen the board.

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/save-reopen.mp4?v=f5150d7350"
  poster="/images/web-ui/tag-analyzer/save-reopen-poster.webp?v=deb53b81fa"
  alt="Saving and reopening a Tag Analyzer board"
  caption="Demo 2.4: Save and Reopen"
>}}

### 2.5 Overlap Chart {#compare-charts-with-overlap}

Overlap Chart displays multiple charts together for comparison and lets you shift each one
independently along the X-axis.

{{< overlap-chart >}}

### 2.6 Delete a TAZ File {#delete-a-taz-file}

Right-click the `.taz` file in **File Explorer**, choose **Delete**, and confirm.
This removes the saved board; table data stays intact.

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/delete-taz.mp4?v=39e14d44bd"
  poster="/images/web-ui/tag-analyzer/delete-taz-poster.webp?v=bbf4098393"
  alt="Deleting a TAZ file from File Explorer"
  caption="Demo 2.6: Delete a TAZ File"
>}}

## 3. Panel Control {#3-panel-controls}

### 3.1 Range {#range-and-navigation}

<span id="basic-range-control"></span>

Click the chart's range to set **From/To**, then **Apply**. Drag or zoom in the navigator to adjust the range.
For the generated sample, use `last-10m` to `last`.

{{< range-controls >}}

<details>
<summary>Configured ranges</summary>

In [Panel Editor → Range](#main-range), **Main Range (A)** takes priority for the visible range.
A separate **Nav Range (B)** takes priority over the board range.

</details>

### 3.2 Tools {#panel-control-tools}

Follow the toolbar from left to right.

{{< tag-analyzer-features
  id="panel-tools"
  title="Tools"
  caption="Figure 3.2: Tools"
>}}

#### 3.2.1 RAW {#view-raw-data}

Click **RAW** to switch between calculated intervals and individual data rows.
Calculated mode uses each series' calculation mode, such as **AVG**, **MIN**, or **MAX**.

<details>
<summary>RAW limits and sampling</summary>

Without main chart sampling, RAW queries return up to **20,000 rows per series**.
If the limit is reached, the visible range can shrink to the returned data.
Narrow the range or enable **Data Setting → Use main chart sampling**.

The navigator may show averages or sampled data even while the main chart is in RAW mode.

</details>

#### 3.2.2 Select Range and FFT {#inspect-statistics}

Inspect a selected range's statistics or analyze frequencies with FFT.
FFT requires **RAW mode** and a **time-axis chart**.

<span id="analyze-frequencies-with-fft"></span>

{{< fft-demo >}}

For `temperature`, set **Min Hz** to **0.005** and **Max Hz** to **0.1**, then click **Apply values**.
The sample's main frequency is about **0.0167 Hz**.

For **3D**, use a **1 min** interval for this sample. Each interval needs at least **16 samples**.

#### 3.2.3 Refresh Range {#refresh-this-panel}

Recheck the data extent and reapply configured ranges.

#### 3.2.4 Edit a Chart {#panel-editor-tool}

<span id="edit-a-chart"></span>

Click the gear to edit settings. **Apply** applies changes; **Close** closes the editor.

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/edit-chart.mp4?v=b4e33d681f"
  poster="/images/web-ui/tag-analyzer/edit-chart-poster.webp?v=608d4edbdf"
  alt="Changing a chart's title and style"
  caption="Demo 3.2.4: Edit a Chart"
>}}

See [Panel Editor](#4-panel-settings) for the settings tabs.

#### 3.2.5 Delete a Chart {#delete-panel-tool}

<span id="delete-a-chart"></span>

Click **Delete panel** (trash) and confirm.

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/delete-chart.mp4?v=66bf8bb25c"
  poster="/images/web-ui/tag-analyzer/delete-chart-poster.webp?v=cb5b0e6c96"
  alt="Deleting a chart from the board"
  caption="Demo 3.2.5: Delete a Chart"
>}}

A chart is one entry in a `.taz` board. Deleting it keeps the `.taz` file and table data.

#### 3.2.6 Highlight {#highlight}

<span id="add-highlights-and-annotations"></span>

Use **Extra → Highlight** to mark and label a range on the chart.

{{< markup-guide id="highlight" >}}

#### 3.2.7 Annotation {#annotation}

Use **Extra → Annotation** to attach a note to a point in a series.

{{< markup-guide id="annotation" >}}

Save the board to keep highlights and annotations.

#### 3.2.8 Extra {#extra-panel-tools}

{{< tag-analyzer-features
  id="extra-tools"
  title="Extra"
  caption="Figure 3.2.8: Extra"
>}}


<span id="handy-tools"></span>

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/handy-tools.mp4?v=96adddb1ff"
  poster="/images/web-ui/tag-analyzer/handy-tools-poster.webp?v=770a824754"
  alt="Refreshing the temperature data and viewing its full range"
  caption="Demo 3.2.8: Refresh and Full Range"
>}}

## 4. Panel Editor {#4-panel-settings}

Click the chart's gear button. **Apply** applies changes; **Close** closes the editor.

**After applying changes, save the `.taz` board to keep them.**

### 4.1 General Tab {#general}

{{< panel-editor-tab id="general" caption="Figure 4.1: General Tab" >}}

### 4.2 Data Tab {#data}

{{< panel-editor-tab id="data" caption="Figure 4.2: Data Tab" >}}

### 4.3 Data Setting Tab {#data-setting}

{{< panel-editor-tab id="data-setting" caption="Figure 4.3: Data Setting Tab" >}}

### 4.4 Axes Tab {#axes}

{{< panel-editor-tab id="axes" caption="Figure 4.4: Axes Tab" >}}

### 4.5 Display Tab {#display}

{{< panel-editor-tab id="display" caption="Figure 4.5: Display Tab" >}}

### 4.6 Range Tab {#main-range}

{{< panel-editor-tab id="main-range" caption="Figure 4.6: Range Tab" >}}
