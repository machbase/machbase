---
title: Tag Analyzer
type: docs
weight: 26
---

## 개요
Tag Analyzer는 태그 테이블의 롤업 기능을 활용해 데이터를 차트 형태로 조회하고 분석할 수 있는 기능을 제공합니다.  
복수의 차트로 구성된 대시보드 구조이며, 대시보드의 각 열이 하나의 차트를 의미합니다.

### 사용 가능한 테이블
Tag Analyzer를 사용하려면 다음 조건을 만족해야 합니다.
- 태그 테이블만 사용할 수 있습니다.
- 차트 조회 속도를 높이려면 롤업 테이블을 미리 생성해 두십시오.  
  차트 조회 시 X축 간격은 조회 시간 범위에 따라 자동으로 결정되므로, 1초·1분·1시간 간격의 기본 롤업을 만들어 두는 것을 권장합니다.

태그 테이블 및 롤업 테이블 생성 예시는 아래와 같습니다.
```sql
CREATE TAG TABLE tag (NAME VARCHAR(80) PRIMARY KEY, TIME DATETIME BASETIME, VALUE DOUBLE SUMMARIZED);

CREATE ROLLUP _tag_rollup_sec FROM tag INTERVAL 1 SEC;
CREATE ROLLUP _tag_rollup_min FROM _tag_rollup_sec INTERVAL 1 MIN;
CREATE ROLLUP _tag_rollup_hour FROM _tag_rollup_min INTERVAL 1 HOUR;
```
※ 태그 테이블에 대한 자세한 내용은 Machbase 매뉴얼(Feature and Tables > Tag Table)을 참고해 주십시오.

## 대시보드
### 화면 구성

{{< figure src="/images/web-ui/taz_dashboard_screen.jpg" width="600" >}}

대시보드는 실제 데이터를 표시하는 차트들로 구성됩니다. 차트가 여러 개이면 행 단위로 나열되며, 각 행이 하나의 차트를 의미합니다.
1. 대시보드 전체 제어 영역입니다. 여기에서 대시보드에 적용된 시간 범위도 확인할 수 있습니다.
2. 차트가 표시되는 패널입니다. 새 차트를 추가하면 기존 차트 아래쪽에 배치됩니다.
3. 새 차트를 추가하는 버튼입니다. 항상 가장 아래쪽 행에 위치합니다.

### 차트 추가
대시보드 하단의 [+] 버튼을 클릭하면 새 차트를 만들 수 있습니다.

{{< figure src="/images/web-ui/taz_new_chart.jpg" width="300" >}}

1. 테이블 선택  
   태그 형식의 테이블만 목록에 표시됩니다.
2. 태그 필터  
   입력한 값이 포함된 태그만 목록에 표시됩니다.
3. 사용 가능한 태그  
   페이지 형태로 태그 목록이 표시되며, 하단에 페이지 이동 버튼이 나타납니다.
4. 선택한 태그  
   선택된 태그가 표시되며 **Calc. mode**를 변경할 수 있습니다. 동일한 태그라도 Calc. mode가 다르면 중복 선택이 가능합니다.*1)  
   하단에는 사용 가능한 태그 수와 선택된 태그 수가 표시됩니다.
5. 차트 유형 선택  
   영역형·포인트형·라인형 차트를 선택할 수 있습니다. 차트 외형은 차트 설정의 Display 항목에서 변경할 수 있습니다.

*1) **Calc. mode** : STAT 모드에서 사용하는 집계 함수(avg, min, max, sum, count 등)를 의미합니다.

### 대시보드 제어
대시보드 상단에 배치된 버튼으로 대시보드를 제어할 수 있습니다.

#### 시간 범위
대시보드에 적용된 시간 범위가 표시됩니다.  
이미지와 같이 From/To 값을 직접 입력하거나, 현재 시각과 연동되도록 설정할 수 있습니다(now: 현재 시각, h: 시, m: 분, s: 초).  
예) `now-3h` = 현재 시각에서 3시간 전

#### 제어 버튼

{{< figure src="/images/web-ui/taz_control_dashboard.jpg" width="400" >}}

1. 데이터를 다시 조회하여 차트를 갱신합니다.  
   시간 범위와 차트 슬라이더의 선택 영역은 유지됩니다.
2. 데이터를 다시 조회하여 차트를 갱신합니다.  
   시간 범위와 차트 슬라이더의 선택 영역이 초기 설정으로 되돌아갑니다.
3. Tag Analyzer 대시보드를 “.taz” 확장자로 저장합니다.
4. 다른 이름으로 대시보드를 저장합니다.
5. Overlap Chart(겹쳐보기) 기능을 실행합니다. 자세한 내용은 "Overlap Chart" 절을 참고해 주십시오.
6. 조회 시간 범위를 설정합니다. 개별 차트에서 별도 범위를 설정하지 않았다면 이 범위가 대시보드 전체에 적용됩니다.  
   {{< figure src="/images/web-ui/taz_time_range.jpg" width="300" >}}  
   - `now` 또는 `last`를 사용할 수 있습니다.  
     **now** : 현재 시각  
     **last** : 저장된 데이터의 마지막 시각  
   - Quick Range를 클릭하면 해당 구간이 자동으로 From/To에 반영됩니다.

#### Overlap Chart
차트 여러 개를 한 화면에 겹쳐 비교할 수 있는 기능입니다.
1. 비교할 차트의 제목을 클릭하여 선택합니다. 선택된 차트는 테두리가 강조 표시됩니다.  
   {{< figure src="/images/web-ui/taz_overlap_select.jpg" width="600" >}}  
   - 단일 시리즈를 가진 차트만 Overlap Chart에 사용할 수 있습니다.  
   - 가장 먼저 선택한 차트의 시간 범위가 Overlap Chart에 적용되며, 제목 앞에 이를 나타내는 아이콘이 표시됩니다.
2. Overlap Chart 버튼을 클릭하면 선택한 차트가 하나의 차트로 합쳐집니다.  
   {{< figure src="/images/web-ui/taz_overlap_view.jpg" width="600" >}}  
   태그별로 조회 시간 범위를 세밀하게 조정하여 비교할 수 있습니다.

## 차트
### 화면 구성

{{< figure src="/images/web-ui/taz_chart_screen.jpg" width="600" >}}

차트 상단에는 현재 그래프의 시간 범위, X축 간격, 기능 버튼이 표시되며, 하단에는 슬라이더와 범례가 배치됩니다.
1. 현재 차트가 표시 중인 시간 범위를 보여 줍니다. 슬라이더를 이용해 대시보드 시간 범위 내에서 특정 구간만 선택해 상세 조회할 수 있습니다. 간격(Interval)은 X축 눈금 간격을 의미합니다.
2. 차트별 기능 버튼이 나타납니다.  
   {{< figure src="/images/web-ui/taz_chart_functions.jpg" width="300" >}}  
   a. 데이터를 다시 조회해 차트를 갱신합니다.  
   b. 차트를 다시 그립니다. 시간 범위와 슬라이더 선택 영역이 초기값으로 돌아갑니다.  
   c. 차트 설정 창을 엽니다(“Chart Settings” 절 참고).  
   d. 차트를 삭제합니다.  
   e. “RAW Data Mode”로 전환합니다.  
   f. Stat Query : 버튼을 선택한 뒤 차트에서 드래그하면 통계를 조회할 수 있습니다. FFT Chart 기능도 이곳에서 사용할 수 있습니다.  
   - **RAW Data Mode** : Calc mode를 적용하지 않고 데이터베이스에 저장된 원본 데이터를 사용합니다.  
     “Pixels between tick marks” 설정값으로 계산된 개수보다 많은 데이터를 선택하면 조회 시간 범위를 조정하고 슬라이더 선택 영역도 함께 변경됩니다.
3. 실제 차트가 표시되는 영역입니다.
4. 슬라이더로 선택한 조회 범위가 표시됩니다. `<` `>` 버튼을 이용해 선택한 시간 범위를 50%씩 이동할 수 있습니다.
5. 슬라이더를 이동하거나 크기를 조정해 차트의 조회 범위를 설정합니다.
6. 슬라이더가 현재 조회 중인 시간 범위를 표시합니다.
7. 범례에는 차트에 표시된 데이터 시리즈가 나타나며, 클릭하면 표시/숨김을 전환할 수 있습니다.

### FFT Chart
선택한 구간에 대해 통계 조회 기능을 사용하면 FFT Chart 버튼이 활성화되며, 해당 구간을 주파수 영역으로 변환해 확인할 수 있습니다.

{{< figure src="/images/web-ui/taz_fft_select.jpg" width="600" >}}

통계를 조회했을 때 FFT Chart 버튼을 사용할 수 있습니다.

{{< figure src="/images/web-ui/taz_fft_view.jpg" width="600" >}}

설정 방법은 다음과 같습니다.
1. FFT 차트를 확인할 태그를 선택합니다.
2. 분석할 주파수(Hz) 범위를 입력합니다. 0을 입력하면 제한이 없습니다.
3. 2D 또는 3D 차트를 선택합니다. 3D 차트는 시간 축이 추가됩니다.
4. 입력한 조건에 따라 FFT 차트를 생성합니다.

### 차트 설정
현재 차트에 적용된 설정을 변경할 수 있습니다.

{{< figure src="/images/web-ui/taz_setting_screen.jpg" width="600" >}}

1. 설정 중인 차트가 표시됩니다. [Apply] 버튼을 클릭하면 변경 내용을 즉시 확인할 수 있습니다.
2. 수정할 항목을 선택하는 탭입니다.  
   **General** : 차트 일반 설정  
   **Data** : 차트에 사용되는 태그  
   **Axes** : X축과 Y축 설정  
   **Display** : 차트의 시각적 표현  
   **Time range** : 차트에만 적용되는 시간 범위
3. 선택한 항목의 값을 변경하는 영역입니다.
4. 버튼 영역입니다.  
   **Apply** : 변경 사항을 적용하지만 설정 창은 유지합니다.  
   **Ok** : 변경 사항을 적용하고 설정 창을 닫습니다. (Apply를 통해 반영한 내용만 유지됩니다.)  
   **Cancel** : 변경 사항을 취소하고 설정 창을 닫습니다.

#### General
차트 기본 설정을 변경합니다.  
{{< figure src="/images/web-ui/taz_setting_general.jpg" width="600" >}}
| 항목                     | 설명                                                         |
|:-------------------------|:-------------------------------------------------------------|
| Chart title              | 차트 제목을 수정합니다.                                      |
| Use Zoom when dragging   | 차트 영역을 드래그할 때 확대 기능을 사용할지 여부입니다.       |
| Keep Navigator Position  | 저장할 때 슬라이더 선택 영역 정보를 함께 저장할지 여부입니다. |

#### Data
차트에서 사용 중인 태그를 수정합니다.  
{{< figure src="/images/web-ui/taz_setting_data.jpg" width="600" >}}

**태그 항목 수정**
| 항목      | 설명                                                                 |
|:----------|:---------------------------------------------------------------------|
| Calc Mode | 집계 함수를 변경합니다.                                              |
| Tag Names | 사용 중인 태그를 변경합니다. 괄호에는 테이블 이름이 표시되며, 테이블 자체는 변경할 수 없습니다. |
| Alias     | 범례에 표시될 이름을 수정합니다.<br/> 설정하지 않으면 태그 이름과 Calc Mode가 표시됩니다. |
| Color     | 색상을 변경합니다.                                                   |
| X         | 해당 태그를 삭제합니다.                                              |

**태그 추가**  
하단의 [+] 버튼을 클릭하면 차트 생성 시와 동일한 화면이 열리며 태그를 추가할 수 있습니다.

#### Axes
X축과 Y축 설정을 변경합니다.  
{{< figure src="/images/web-ui/taz_setting_axes.jpg" width="600" >}}  
※ “Set additional Y-axis” 옵션을 먼저 활성화해야 추가 Y축 영역이 활성화됩니다.

**X-Axis**
| 항목                          | 설명                                                          |
|:------------------------------|:--------------------------------------------------------------|
| Display the X-Axis tick line  | X축 눈금을 표시합니다.                                        |
| Pixels between tick marks     | X축 데이터 1개가 차지하는 픽셀 수입니다.<br/>※ 표시 가능한 데이터 수 = 가로 해상도 ÷ 설정 값 |
| _(for)_ Raw                   | RAW 모드에서 사용하는 값입니다. (대규모 데이터를 표시할 때 주로 1 미만으로 설정합니다.) |
| _(for)_ Calculation           | STAT 모드에서 사용하는 값입니다.                             |
| use Sampling                  | RAW 모드에서 Machbase의 샘플링 기능을 사용하여 **슬라이드** 데이터를 빠르게 조회합니다. |

**Y-Axis**
| 항목                                | 설명                                                        |
|:------------------------------------|:------------------------------------------------------------|
| The scale of the Y-Axis start at zero | Y축을 0에서 시작할지 여부입니다.                           |
| Display the Y-Axis tick line        | Y축 눈금을 표시합니다.*1)                                   |
| Custom scale                        | Y축 최소·최대 값을 직접 설정합니다.                         |
| Custom scale for raw data chart     | RAW 모드에서 사용할 Y축 최소·최대 값을 설정합니다.          |
| use UCL                             | UCL(Upper Control Limit)을 설정합니다.                      |
| use LCL                             | LCL(Lower Control Limit)을 설정합니다.                      |

*1) 추가 Y축을 사용하는 경우 항상 표시됩니다.

**Additional Y-Axis**
| 항목                                | 설명                                                        |
|:------------------------------------|:------------------------------------------------------------|
| Set additional Y-Axis               | 추가 Y축 사용 여부를 설정합니다.                            |
| The scale of the Y-Axis start at zero | 추가 Y축을 0에서 시작할지 여부입니다.                     |
| Display the Y-Axis tick line        | 추가 Y축 눈금을 표시합니다.*1)                               |
| Custom scale                        | 추가 Y축의 최소·최대 값을 설정합니다.                      |
| Custom scale for raw data chart     | RAW 모드에서 사용할 추가 Y축 최소·최대 값을 설정합니다.     |
| use UCL                             | 추가 Y축의 UCL을 설정합니다.                                |
| use LCL                             | 추가 Y축의 LCL을 설정합니다.                                |
| Select Tag                          | 사용할 태그를 선택합니다.<br/>선택된 태그를 다시 클릭하면 선택이 해제됩니다. |

*1) 추가 Y축을 사용하는 경우 항상 표시됩니다.

#### Display
차트의 시각적 요소를 설정합니다.  
{{< figure src="/images/web-ui/taz_setting_display.jpg" width="600" >}}
| 항목                       | 설명                                                                  |
|:---------------------------|:----------------------------------------------------------------------|
| Chart Type                 | 선택한 차트 유형에 맞게 표시 방식을 조정합니다.                       |
| Display data point in the line chart | 라인 차트에 데이터 포인트를 표시할지 여부입니다.           |
| Display legend             | 범례 표시 여부입니다.                                                 |
| Point Radius               | 포인트 크기를 설정합니다.<br/>0으로 설정하면 표시되지 않습니다.      |
| Opacity of Fill Area       | 영역형 차트의 채우기 투명도를 설정합니다(0~1).<br/>0이면 표시되지 않습니다. |
| Line Thickness             | 선 두께를 설정합니다.                                                 |

#### Time range
차트에만 적용되는 시간 범위를 설정합니다. 값을 지정하지 않으면 대시보드의 시간 범위를 사용합니다.  
{{< figure src="/images/web-ui/taz_setting_timerange.jpg" width="600" >}}
| 항목        | 설명                                                                 |
|:------------|:---------------------------------------------------------------------|
| From        | 시간 범위의 시작 값을 설정합니다.                                    |
| To          | 시간 범위의 종료 값을 설정합니다.                                    |
| Quick range | 항목을 클릭하면 “now” 또는 “last”를 이용해 해당 구간이 자동으로 설정됩니다. |
