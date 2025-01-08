---
title: Dashboard
type: docs
weight: 14
---

## Overview
The dashboard provides the functionality to view data stored in Machbase in chart format.  
It is offered in the form of a dashboard composed of multiple charts, with adjustable chart panel sizes and positions. Additionally, it supports an auto-refresh feature to periodically update data.

### Starting Dashboard
By clicking the "DASHBOARD" on the Machbase Neo home screen, you can create a new dashboard.

{{< figure src="/images/web-ui/main-dashboard.jpg" width="600" >}}

If you select a pre-created dashboard file (*.dsh) from the "EXPLORER" on the left side, you can view and edit the corresponding dashboard.  
View mode is provided using the link of a saved dashboard. (Please refer to the "Dashboard Control" section).

## Dashboard
### Screen Layout

{{< figure src="/images/web-ui/dashboard-screen.jpg" width="600" >}}

The dashboard consists of charts that display actual data. The size and position of each chart panel can be freely adjusted.

1. Area where the chart(s) are displayed
2. Title of the dashboard
3. Control area for managing the entire dashboard

### Adding Charts
By clicking the [+] button in the dashboard control area, the screen switches to the chart settings.  
After setting the chart as desired and clicking the [Save] button, a chart panel is added to the dashboard.  
※ Please refer to the "Chart Settings" section.

The newly added chart is placed with a default size.  
You can adjust the size by dragging the bottom-right corner of the panel and change its position by dragging the top of the panel.

### Dashboard Control
#### Time Range
Displays the time range applied to the dashboard. You can specify a fixed time range or configure it to sync with the current time. (‘now’ represents the current time, ‘h’ for hours, ‘m’ for minutes, ‘s’ for seconds)  
Example: now-3h = Current time minus 3 hours

#### Dashboard Control Buttons

{{< figure src="/images/web-ui/dashboard-control.jpg" width="400" >}}

1. Adds a new chart.
2. Reloads data and updates the charts.
3. Allows configuration of the time range for data queries.
    - You can use "now" or "last" for time ranges:  
      **now** : Current time  
      **last** : The last time of the data stored in the database
    - Clicking an item in the "Quick Range" sets the From/To time accordingly.
    - < or > buttons shift the specified time range by 50%. If "now" or "last" is used, they are converted to absolute times.
    - If a refresh interval is set, the dashboard will automatically redraw at the specified intervals.
4. Saves the current dashboard.
    - The file extension is ‘.dsh’.
    - For a new dashboard, you can specify a file name and folder.
5. Saves the dashboard with a new name.
6. Copies the link to the dashboard's view mode to the clipboard.
    - This function is only available if the dashboard has been saved.
    - Login is required to access the dashboard in view mode.
    - In view mode, only time range adjustments and the refresh function are available.  

## Chart Panel
### Screen Layout

{{< figure src="/images/web-ui/panel-screen.jpg" width="600" >}}

1. Drag Panel Header:  
    Dragging the top of the panel allows you to change the position of the panel.
2. Resize Panel:  
    Dragging the bottom-right corner of the panel allows you to adjust its size.
3. Toggle Legend:  
    Clicking on a legend item toggles the corresponding series on or off.
4. Panel menu:  
    Clicking the button in the top-right corner of the chart panel reveals a menu with the following options:
    - Setting : Modifies the chart settings. (Please refer to the "Chart Settings" section.)
    - Duplicate : Creates a new chart by copying the existing one.
    - Show Taganalyzer : Views the content of the current chart in the Tag Analyzer.
    - Delete : Removes the chart panel.
    - Save to tql : Saves the content of the chart as a TQL file.  

#### Save to TQL
The charts in the dashboard internally generate TQL to display the data. This function allows you to save the TQL used by the dashboard.

{{< figure src="/images/web-ui/save2tql.jpg" width="400" >}}

- File Name : Specifies the name of the TQL file to be saved.
- Output : Defines the type of TQL to save.  
    **DATA** : TQL used to retrieve the required data.  
    **CHART** : TQL used to render the corresponding chart.
- Block : Used only when the output is set to DATA. Allows you to specify the Tag Name.  

### Chart Settings
Chart settings allow you to configure the detailed parameters of a chart.

{{< figure src="/images/web-ui/chart-setting.jpg" width="600" >}}

1. Chart Type  
    Select the type of chart. The available configuration options depend on the chosen chart type.
    - Chart Types : Line, Bar, Scatter, Gauge, Pie, Liquid Fill, TQL Chart  
      ※ Please refer to the "Options by Chart Type" and "TQL chart" section.
2. Query  
    Configure the data to be used in the chart. The input fields vary depending on the type of input mode, which are "Tag-Based Query Mode" and "Advanced Query Mode".  
3. Time  
   Use this option to specify a time range for the chart independently of the dashboard's global time range.  
   Functions the same as the dashboard's time range settings but applies only to the specific chart, overriding the dashboard time range.

#### Tag-Based Query Mode
This feature can only be used with **Tag Tables**. Please refer to the image above.  
- Table : Specify the table name.
- Tag : Enter or select the Tag Name to use.
- Aggregator : Choose the aggregation function to apply based on the time interval of the x-axis. If ‘value’ is selected, raw data is used without aggregation.  
  **Options** : value, sum, avg, min, max, count  
- Alias : Name to be displayed in the legend.

#### Advanced Query Mode
Allows specifying all query elements manually.  
{{< figure src="/images/web-ui/chart-setting-advanced-query.jpg" width="600" >}}
- Table : Specify the table name.
- Time Field : Select the column to use as the x-axis time value.
- Value Field : Select the column to use as the y-axis value.
- Aggregator : Aggregation function (same as in "Tag-Based Query Mode").
- Alias : Name to be displayed in the legend.
- Filter : Input conditions to be used in the WHERE clause of the query.  
   Multiple conditions can be entered, and they are combined using ’AND’.

#### Control Function
{{< figure src="/images/web-ui/chart-setting-qurey-tool.jpg" width="200" >}}  
- a. Input a formula to process values extracted from the database (value = DB value)  
     Example: value * 1.5
- b. Assign a color to the chart.
- c. Switch between "Advanced Query Mode" and "Tag-Based Query Mode".
- d. Remove the query.

### TQL chart
The "TQL Chart" type allows you to use custom TQL files in the dashboard. Only TQL files where the SINK function is set to "CHART" can be used.

{{< figure src="/images/web-ui/tql-chart-setting.jpg" width="600" >}}

#### TQL Chart Settings
**Tql path :**  
Select the TQL file to be used.  
**Params :**  
Register the parameters to pass to the TQL file.  
You can input values directly or use the predefined variables provided by Machbase Neo Dashboard. By default, the provided variables include Time Range and the x-axis time interval, which are explained in detail in the right panel.
- Time range : It is used to synchronize the time with other chart panels in the dashboard.
  | Params | Desc |
  |:-------|:-----|
  | $from_str | date string (YYYY-MM-DD HH:MI:SS) |
  | $from_s, $from_ms, $from_us, $from_ns | unix timestamp (milli, micro, nano) |
  | $to_str | date string (YYYY-MM-DD HH:MI:SS) |
  | $to_s, $to_ms, $to_us, $to_ns | unix timestamp (milli, micro, nano) |
- period : The time interval for the x-axis ticks, calculated based on the time range and panel size. |
  | Params | Desc |
  |:-------|:-----|
  | $period | duration expression (ex: 10s) |
  | $period_value | period value (ex: 10) |
  | $period_unit | period unit (ex: sec) |

#### Applying Parameters in TQL Files
To use parameters in a TQL file for chart rendering, the param() function is used.  

Example TQL File:
```sql
SQL(strSprintf(`
SELECT date_trunc('%s', TIME, %1.0f) as TIME, avg(VALUE) as VALUE
FROM EXAMPLE
WHERE TIME between FROM_UNIXTIME(%1.0f) and FROM_UNIXTIME(%1.0f) AND NAME IN ('%s')
GROUP BY TIME ORDER BY TIME`, 
(param('period_unit') ?? 'msec'), 
parseFloat(param('period_value') ?? 10), 
parseFloat(param('from') ?? 1703055573), 
parseFloat(param('to') ?? 1703055583),
(param('tag') ?? 'tag01')
))

CHART_LINE()
```
**SQL():**  
- Executes a query where the parameters are dynamically applied using the param() and strSprintf() functions.  
- Parameters:
  - period_unit: Unit for the time interval (default :  msec).
  - period_value: Interval value (default : 10).
  - from and to: Time range for the query.
  - tag: Specifies the tag to query (default : tag01).

**CHART_LINE():**  
- Uses the query result to render the chart as a line chart.  

### Options by Chart Type
#### Common Options
- Panel option
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Title           | The title displayed on the chart panel.                    |
| Theme           | The theme of the chart. (Refer to the TQL - CHART section) |

- Legend
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Show legend     | Checkbox to toggle the display of the legend.              |
| Vertical        | Vertical position (top / center / bottom)                  |
| Horizontal      | Horizontal position (left / center / right)                |
| Alignment type  | Alignment method (horizontal / vertical)                   |

- Panel padding  
Set the size of the margin between the panel border and the chart.  
※ Space for the legend must be reserved by adjusting the padding settings.
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Top             | Top margin                                                 |
| Bottom          | Bottom margin                                              |
| Left            | Left margin                                                |
| Right           | Right margin                                               |

- Tooltip
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Show tooltip    | Checkbox to enable or disable the use of tooltips.         |
| Type            | Tooltip type (axis / item).                                |
| Unit            | Unit displayed in the tooltip.                             |
| Decimals        | Number of decimal places for the tooltip value.            |

- xAxis
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Interval type   | Unit of time intervals for the x-axis (none / sec / min / hour).<br/> ※ none = auto-calculated. |
| Interval value  | Value of the time intervals for the x-axis.                 |

- yAxis
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Position        | Position of the Y-axis (left / right).                     |
| Type            | Type of Y-axis values.                                     |
| - Unit          | Unit of measurement.                                       |
| - Decimals      | Number of decimal places.                                  |
| - Name          | Name of the Y-axis (displayed at the top of the axis).     |
| Min             | Minimum value of the Y-axis.                               |
| Max             | Maximum value of the Y-axis.                               |

#### Line

{{< figure src="/images/web-ui/line-chart-setting.jpg" width="600" >}}

- Chart option
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Fill area       | Enable or disable the use of area fill.<br/> ※ Requires opacity setting (0 ~ 1). |
| Smooth line     | Display lines smoothly.                                    |
| Step line       | Display lines in a step-like format.                       |
| Stack mode      | Display lines in a stacked format.                         |
| Large data mode | Mode used when handling a large amount of data.            |
| Symbol          | Display symbols on values.                                 |
- Symbol
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Type            | Type of symbol <br/> (circle / rect / roundRect / triangle / diamond / pin / arrow). |
| Size            | Size of the symbol.                                        |

#### Bar

{{< figure src="/images/web-ui/bar-chart-setting.jpg" width="600" >}}

- Chart option
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Stack mode      | Enable stack mode.                                         |
| Large data mode | Mode used when handling a large amount of data.            |
| Polar mode      | Enable polar mode.                                         |
- Polar mode
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Max             | Maximum value.                                             |
| Start angle     | Starting angle of the Y-axis.                              |
| Radius          | Inner radius (0: no inner circle).                         |
| Polar size      | Outer radius (100: circle that fills the entire panel).    |
| Polar axis      | X-axis type (time / category).                             |

#### Scatter

{{< figure src="/images/web-ui/scatter-chart-setting.jpg" width="600" >}}

- Chart option
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Large data mode | Mode used when handling a large amount of data.            |
- Symbol
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Type            | Type of symbol <br/> (circle / rect / roundRect / triangle / diamond / pin / arrow). |
| Size            | Size of the symbol.                                        |

#### Gauge

{{< figure src="/images/web-ui/gauge-chart-setting.jpg" width="250" >}}

- Chart option
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Min             | Minimum value.                                             |
| Max             | Maximum value.                                             |
- Axis
| Option               | Desc                                                  |
|:---------------------|:------------------------------------------------------|
| Label distance       | Distance of the label from the line of the circle <br/> (negative values are outside). |
| Show axis tick       | Display axis ticks.                                   |
| Setting line colors  | Set colors based on values <br/> (value range is specified as a ratio from 0 to 1). |
- Anchor
| Option          | Desc                                                       |
|:----------------|:-----------------------------------------------------------|
| Show anchor     | Display the central circle.                                |
| Size            | Size of the central circle.                                |
- Display value
| Option              | Desc                                                   |
|:--------------------|:-------------------------------------------------------|
| Font size           | Font size of the value displayed inside the gauge.     |
| Offset from center  | Distance from the center.                              |
| Decimal places      | Number of decimal places.                              |
| Active animation    | Whether animation is applied.                          |

#### Pie

{{< figure src="/images/web-ui/pie-chart-setting.jpg" width="250" >}}

- Chart option
| Option           | Desc                                                      |
|:-----------------|:----------------------------------------------------------|
| Doughnut ratio   | Proportion of the inner circle (0-100).                   |
| Nightingale mode | Apply Nightingale mode <br/> (radius changes according to the values). |

#### Liquid fill

{{< figure src="/images/web-ui/liquid_fill-chart-setting.jpg" width="250" >}}

- Chart option
| Option           | Desc                                                      |
|:-----------------|:----------------------------------------------------------|
| Shape            | Shape (container / circle / rect / roundRect / triangle / diamond / pin / arrow). |
| Unit             | Unit of the displayed value.                              |
| Digit            | Number of decimal places.                                 |
| Font size        | Font size.                                                |
| Wave min         | Minimum value for the wave display.                       |
| Wave max         | Maximum value for the wave display.                       |
| Wave amplitude   | Amplitude of the wave display (0: straight line).         |
| Background color | Background color of the wave display area.                |
| Wave animation   | Whether wave animation is applied.                        |
| Outline          | Whether to display the outline.                           |
