---
title: Tag Analyzer
type: docs
weight: 26
---

## Overview
Tag Analyzer provides a feature to view and analyze data as charts using the rollup functionality of the Tag Table.  
Tag Analyzer is structured in the form of a dashboard composed of multiple charts, where each column of the dashboard represents a single chart.

### Applicable Tables
The conditions for using Tag Analyzer are as follows:
- Only Tag Tables can be used.
- To improve the query speed of the chart, create a Rollup Table in advance.  
  Since the X-axis interval is automatically determined based on the time range of the chart query, it is recommended to create basic Rollups with intervals of 1 second, 1 minute, and 1 hour.  

Example of Creating Tag Table and Rollup Table
```sql
CREATE TAG TABLE tag (NAME VARCHAR(80) PRIMARY KEY, TIME DATETIME BASETIME, VALUE DOUBLE SUMMARIZED);

CREATE ROLLUP _tag_rollup_sec FROM tag INTERVAL 1 SEC;
CREATE ROLLUP _tag_rollup_min FROM _tag_rollup_sec INTERVAL 1 MIN;
CREATE ROLLUP _tag_rollup_hour FROM _tag_rollup_min INTERVAL 1 HOUR;
```
※ For more details about Tag Tables, refer to the Machbase manual (Feature and Tables > Tag Table).  

## Dashboard
### Screen Layout

{{< figure src="/images/web-ui/taz_dashboard_screen.jpg" width="600" >}}

The dashboard is composed of charts that display actual data. If there are multiple charts, they are displayed in multiple rows, with each row representing a single chart.
1. Control Area for the Entire Dashboard  
   The time range applied to the dashboard is also displayed here.
2. Panel Where Charts Are Displayed  
   When a new chart is added, it is positioned below the existing charts.
3. Button to Add a New Chart  
   This button is always located in the bottommost row.  

### Adding a Chart
To create a new chart, click the [+] button located at the bottom of the dashboard.  

{{< figure src="/images/web-ui/taz_new_chart.jpg" width="300" >}}

1. Select a Table  
   Only tables in Tag format are displayed.
2. Filter Tags  
   The list of tags will be filtered to include only those containing the input value.
3. Available Tags  
   A list of available tags is displayed, with pagination shown at the bottom.
4. Selected Tags  
   Selected tags are displayed, and you can change the **Calc. mode**. Since the same tag can have different Calc. mode, duplicates are not checked. *1)  
   The number of available tags and the number of selected tags are shown below.
5. Select Chart Type  
   Choose the type of chart (area chart, point chart, line chart). The appearance of the chart can be modified in the Display section of the chart settings.  

*1) **Calc. mode** : Aggregation functions used in STAT mode (e.g., avg, min, max, sum, count).  

### Dashboard Controls
You can control the dashboard using the buttons located at the top of the dashboard.  

#### Time Range
The time range applied to the dashboard is displayed.  
You can set a specific time range manually, as shown in the image, or configure it to synchronize with the current time. (e.g., now: current time, h: hours, m: minutes, s: seconds)  
Example: now-3h = Current time – 3 hours  

#### Control Buttons

{{< figure src="/images/web-ui/taz_control_dashboard.jpg" width="400" >}}

1. Reloads the data and updates the charts.  
   The time range and selection of the chart slide remain unchanged.
2. Reloads the data and updates the charts.  
   The time range and selection of the chart slide revert to their original settings.
3. Saves the Tag Analyzer dashboard with the file extension ".taz".
4. Saves the Tag Analyzer dashboard with a new name.
5. Displays an Overlap Chart (Refer to "Overlap Chart").
6. Set the time range for the query. This time range applies to the entire dashboard (except when a time range is set separately in the chart settings).
   {{< figure src="/images/web-ui/taz_time_range.jpg" width="300" >}}
   - The time range can use now or last:  
     **now** : The current time  
     **last** : The last time of the stored data  
   - Clicking an item in the Quick Range will set the From/To fields to the corresponding time period.  

#### Overlap Chart
The Overlap Chart feature allows you to compare multiple charts by overlaying their graphs onto a single chart.  
1. Click on the chart title to select the charts you want to compare. Selected charts will have a highlighted border.  
   {{< figure src="/images/web-ui/taz_overlap_select.jpg" width="600" >}}
   - Only charts with a single series can be used for the Overlap Chart.  
   - The time range of the first chart clicked will be applied to the Overlap Chart, and an icon will appear in front of the chart title to indicate this.  
2. Click the Overlap Chart button to overlay the selected charts into a single chart.  
   {{< figure src="/images/web-ui/taz_overlap_view.jpg" width="600" >}}
   You can fine-tune the time range for each tag individually when querying.

## Chart
### Screen Layout

{{< figure src="/images/web-ui/taz_chart_screen.jpg" width="600" >}}

At the top of the chart, the time range of the currently displayed graph, the time interval of the x-axis ticks, and function buttons are displayed.  
At the bottom, there is a slider for selecting the time range to zoom in on within the dashboard's time range, along with the legend for the tags used in the chart.  
1. The time range of the chart is displayed. You can select a specific portion of the dashboard's time range for a detailed view using the slider.  
   The interval indicates the time interval of the x-axis ticks.
2. Function buttons for controlling each chart are displayed.  
   {{< figure src="/images/web-ui/taz_chart_functions.jpg" width="300" >}}
   a. Reload the data to update the chart.  
   b. Redraw the chart.  
   　 The time range and selection of the chart slide revert to their original settings.  
   c. Modify the chart settings (refer to "Chart Settings").  
   d. Delete the chart.  
   e. Switch to "**RAW Data Mode**".  
   f. Stat Query : Select the button and drag on the chart to display the stats.  
   　 The FFT Chart functionality can also be used here.  
   - **RAW Data mode**  
     Uses raw data stored in the database without applying the calc mode.  
     If the number of selected data points exceeds the value calculated using the "Pixels between tick marks" setting, the queried time range will be adjusted, and the selected range on the slider will be updated accordingly.  
3. The area where the actual chart is displayed.
4. Displays the time range of the slider used to select the time range for querying.  
   The < > buttons shift the specified time range by 50%.
5. Controls the slider and the selected range.  
   {{< figure src="/images/web-ui/taz_chart_slidebar.jpg" width="300" >}}
   a. The selected range on the slider expands by 12.5% (x2) or 25% (x4) on both sides.  
   　 The time range displayed on the chart expands(making the slider bar larger).  
   b. The selected range on the slider shrinks by 12.5% (x2) or 25% (x4) on both sides.  
   　 The time range displayed on the chart decreases(making the slider bar smaller).  
   c. The chart's time range changes to match the entire time range of the slider, and  
   　 the selected area of the slider is centered with a size of 50% of the slider's length.  
   　 This is used to view the chart's data in greater detail.  
6. Move or resize the slider to set the range currently queried on the chart.  
7. The legend displays the data series shown on the chart.  
   Clicking on a series in the legend toggles it on or off.  

### FFT Chart
The "FFT Chart" feature becomes available when using the stat query function to retrieve stats for a selected range.  

{{< figure src="/images/web-ui/taz_fft_select.jpg" width="600" >}}

When querying stats, the "FFT Chart" button becomes available for use.  

{{< figure src="/images/web-ui/taz_fft_view.jpg" width="600" >}}

You can configure settings to view the FFT Chart.  
1. Select the tag for which you want to view the FFT chart.
2. Enter the range for Hz (set to 0 to disable).
3. Choose between 2D or 3D chart.  
   For the 3D chart, a time axis will be added.
4. Generate the FFT chart based on the entered conditions.  

### Chart Settings
The settings of the currently viewed chart will be changed.  

{{< figure src="/images/web-ui/taz_setting_screen.jpg" width="600" >}}

1. Displays the chart being configured. After changing the settings, you can view the changes by clicking the [Apply] button.
2. The tab to select which field to modify.  
   **General** : Modify general chart settings  
   **Data** : Modify the tags used in the chart  
   **Axes** : Change the settings for the X-axis and Y-axis  
   **Display** : Modify settings related to the appearance of the chart  
   **Time range** : Set the time range specific to the chart  
3. Area to modify values
4. Button display area  
   **Apply** : Apply the changes to the chart. You can cancel by clicking the [Cancel] button.  
   **Ok** : Apply the changes and exit the settings mode (only the changes from pressing [Apply] will be applied).  
   **Cancel** : Cancel the changes and exit the settings mode.  

#### General
Modify the general settings of the chart.  
{{< figure src="/images/web-ui/taz_setting_general.jpg" width="600" >}}  
| Item                    | Desc                                               |
|:------------------------|:---------------------------------------------------|
| Chart title             | Modify the chart title.                            |
| Use Zoom when dragging  | Use zoom when dragging within the chart area.      |
| Keep Navigator Position | Save the selected area information of the slider when saving. |

#### Data
Edit the tags used in the chart.  
{{< figure src="/images/web-ui/taz_setting_data.jpg" width="600" >}}  
**Edit Tag Items** 
| Item        | Desc                                                           |
|:------------|:---------------------------------------------------------------|
| Calc Mode   | Change the aggregation function.                               |
| Tag Names   | Change the tags being used. The table name is displayed in parentheses. (Tables cannot be modified.) |
| Alias       | Modify the content displayed in the legend.<br/> If not set, the Tag Name and Calc Mode will be displayed. |
| Color Icon  | Change the color.                                              |
| X           | Delete the corresponding tag.                                  |

**Add Tags**  
By clicking the [+] button at the bottom, a screen similar to the one used for chart creation will appear, allowing you to add tags.  

#### Axes
Modify the settings for the X-axis and Y-axis.  
{{< figure src="/images/web-ui/taz_setting_axes.jpg" width="600" >}}  
※ The "Set additional Y-axis" option must be checked for the a. area to be activated.  

**X-Axis**  
| Item                         | Desc                                          |
|:-----------------------------|:----------------------------------------------|
| Display the X-Axis tick line | Draws the tick marks on the X-axis.           |
| Pixels between tick marks    | The number of pixels per data point on the X-axis. <br/>※ Number of data points that can be displayed = Horizontal resolution / Set value |
| _(for)_ Raw                  | Value in RAW mode. (Typically used with values less than 1 to display large amounts of data.) |
| _(for)_ Calculation          | Value in STAT mode.                    |
| use Sampling                 | In RAW mode, Machbase's sampling feature is used to quickly retrieve **slide** data. |

**Y-Axis**  
| Item                                | Desc                                   |
|:------------------------------------|:---------------------------------------|
| The scale of the Y-Axis start at zero | The Y-axis starts from 0.            |
| Display the Y-Axis tick line        | Draw the tick marks on the Y-axis. *1) |
| Custom scale                        | Set the min/max values for the Y-axis. |
| Custom scale for raw data chart     | Set the min/max values for the Y-axis in RAW mode. |
| use UCL                             | Set the UCL (Upper Control Limit).     |
| use LCL                             | Set the LCL (Lower Control Limit).     |

*1) It is always displayed when using the additional Y-axis.

**Additional Y-Axis**  
| Item                                | Desc                                   |
|:------------------------------------|:---------------------------------------|
| Set additional Y-Axis               | Configure whether to use an additional Y-axis. |
| The scale of the Y-Axis start at zero | The Y-axis starts from 0.            |
| Display the Y-Axis tick line        | Draw the tick marks on the Y-axis. *1) |
| Custom scale                        | Set the min/max values for the Y-axis. |
| Custom scale for raw data chart     | Set the min/max values for the Y-axis in RAW mode. |
| use UCL                             | Set the UCL (Upper Control Limit).     |
| use LCL                             | Set the LCL (Lower Control Limit).     |
| Select Tag                          | Select the tag to be used. <br/> Clicking on a selected tag will deselect it. |

*1) It is always displayed when using the additional Y-axis.

#### Display
Modify settings related to the appearance of the chart.  
{{< figure src="/images/web-ui/taz_setting_display.jpg" width="600" >}}  
| Item                 | Desc                                                  |
|:---------------------|:------------------------------------------------------|
| Chart Type           | Adjust the settings according to the selected chart type. |
| Display data point in the line chart | Show points for each data value.      |
| Display legend       | Set whether to display the legend.                    |
| Point Radius         | Adjust the size of the points. <br/>If set to 0, it will not be displayed. |
| Opacity of Fill Area | Set the transparency of the area. (0~1) <br/>If set to 0, it will not be displayed. |
| Line Thickness       | Set the thickness of the line.                        |

#### Time range
Set the time range that applies only to the chart. If this value is not set, the time range from the dashboard will be used.  
{{< figure src="/images/web-ui/taz_setting_timerange.jpg" width="600" >}}  
| Item        | Desc                                                            |
|:------------|:----------------------------------------------------------------|
| From        | The starting value of the time range.                           |
| To          | The ending value of the time range.                             |
| Quick range | Clicking an item will set the time range using "now" or "last". |
