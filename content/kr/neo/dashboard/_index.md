---
title: 대시보드
type: docs
weight: 25
---

## 개요
대시보드는 Machbase에 저장된 데이터를 차트 형태로 시각화하여 보여 줍니다.  
여러 개의 차트 패널을 조합해 하나의 화면을 구성할 수 있으며, 각 패널의 크기와 위치를 자유롭게 조정할 수 있습니다. 또한 지정한 주기마다 차트를 자동으로 새로 고치는 기능도 제공합니다.

### 대시보드 시작하기
Machbase Neo 홈 화면에서 “DASHBOARD” 버튼을 클릭하면 새로운 대시보드를 생성할 수 있습니다.

{{< figure src="/images/web-ui/main-dashboard.jpg" width="600" >}}

좌측 “EXPLORER”에서 저장된 대시보드 파일(`*.dsh`)을 선택하면 해당 대시보드를 열어 확인하거나 편집할 수 있습니다.  
저장된 대시보드 링크를 통해 보기 전용 모드로 접근할 수도 있습니다. (자세한 내용은 “대시보드 제어” 섹션 참고)

## 대시보드
### 화면 구성

{{< figure src="/images/web-ui/dashboard-screen.jpg" width="600" >}}

대시보드는 실제 데이터를 보여주는 여러 차트로 이루어져 있으며, 각 패널은 사용자가 원하는 위치와 크기로 배치할 수 있습니다.

1. 차트가 표시되는 영역
2. 대시보드 제목
3. 대시보드를 제어하는 컨트롤 영역

### 차트 추가
컨트롤 영역의 [+] 버튼을 클릭하면 차트 설정 화면으로 전환됩니다.  
설정을 마치고 [Save] 버튼을 누르면 대시보드에 차트 패널이 추가됩니다.  
※ 자세한 내용은 “차트 설정” 섹션을 참고하십시오.

새로 추가된 차트는 기본 크기로 배치되며, 패널 우측 하단을 드래그해 크기를 조정하고 패널 상단을 드래그해 위치를 변경할 수 있습니다.

### 대시보드 제어
#### Time Range
대시보드 전체에 적용되는 시간 범위를 표시합니다. 특정 기간을 고정할 수도 있고 현재 시각과 동기화하도록 설정할 수도 있습니다. (`now`는 현재 시각, `h/m/s`는 시간/분/초)  
예: `now-3h` → 현재 시각에서 3시간 전까지의 데이터

#### 대시보드 제어 버튼

{{< figure src="/images/web-ui/dashboard-control.jpg" width="400" >}}

1. 새 차트를 추가합니다.
2. 데이터를 다시 로드해 차트를 갱신합니다.
3. 데이터 조회에 사용할 시간 범위를 설정합니다.
    - 시간 범위에는 `now`, `last` 등을 사용할 수 있습니다.  
      **now** : 현재 시각  
      **last** : 데이터베이스에 저장된 마지막 시각
    - “Quick Range” 항목을 클릭하면 From/To 시간이 자동으로 설정됩니다.
    - `<`, `>` 버튼은 선택한 시간 범위를 50%씩 이동합니다. `now` 또는 `last`를 사용 중이면 절대 시간으로 변환됩니다.
    - 자동 새로 고침 간격을 설정하면 지정한 주기로 대시보드가 다시 그려집니다.
4. 현재 대시보드를 저장합니다. (파일 확장자 `.dsh`)
    - 새 대시보드는 파일명과 저장 폴더를 지정할 수 있습니다.
5. 다른 이름으로 저장합니다.
6. 대시보드 보기 모드 링크를 클립보드에 복사합니다.
    - 대시보드가 저장된 후에만 사용할 수 있습니다.
    - 보기 모드로 접근하려면 로그인이 필요하며, 시간 범위 조정과 새로 고침만 가능합니다.
7. 변수 설정 {{< neo_since ver="8.0.46" />}}  
    **변수 정의**  
{{< figure src="/images/web-ui/variables-1.jpg" width="600" >}}
    대시보드에서 사용하는 변수를 조회·추가·수정·삭제할 수 있습니다.  
    - [+ New variable] : 새 변수를 생성합니다.  
      {{< figure src="/images/web-ui/variables-2.jpg" width="600" >}}  
        * Label : 변수 입력 필드 제목  
        * Variable Name : 차트 설정에서 사용할 변수 이름 (예: `{{variable_name}}`)  
        * Value : 변수 입력 필드에서 선택할 항목을 정의  
    - 기존 변수를 클릭하면 수정할 수 있습니다.  
    - [Export], [Import] : 변수 설정을 내보내거나 가져옵니다.  

    **변수 사용 방법**  
    - 차트 설정에서  
{{< figure src="/images/web-ui/variables-19.jpg" width="600" >}}  
        변수 적용이 필요한 위치에 “Variable Name”을 입력합니다.  
    - 대시보드에서 변수 변경  
        1. 변수를 설정하면 대시보드 제목 옆에 변수 입력 필드가 표시됩니다.  
{{< figure src="/images/web-ui/variables-10.jpg" width="300" >}}        
        2. 변수 입력 아이콘을 클릭해 값을 선택할 수 있습니다.  
{{< figure src="/images/web-ui/variables-11.jpg" width="300" >}}  

## 차트 패널
### 화면 구성

{{< figure src="/images/web-ui/panel-screen.jpg" width="600" >}}

1. 패널 헤더 드래그  
    패널 상단을 드래그해 위치를 이동합니다.
2. 패널 크기 조절  
    패널 우측 하단을 드래그해 크기를 조절합니다.
3. 범례 토글  
    범례 항목을 클릭하면 해당 시리즈를 표시하거나 숨길 수 있습니다.
4. 패널 메뉴  
    차트 패널 우측 상단 버튼을 클릭하면 다음 메뉴가 표시됩니다.
    - Setting : 차트 설정을 수정합니다. (자세한 내용은 “차트 설정” 섹션 참고)
    - Duplicate : 현재 차트를 복제해 새 차트를 생성합니다.
    - Show Taganalyzer : Tag Analyzer에서 제공하는 등고선 지도를 표시합니다. {{< neo_since ver="8.0.49" />}} (Tag 테이블에서만 사용 가능)
    - Show TQL : TQL 차트 타입의 HTML 뷰어를 표시합니다. (TQL 차트 타입에서만 지원)
    - Delete : 차트 패널을 삭제합니다.

## 차트 설정
### 개요

{{< figure src="/images/web-ui/chart-setting.jpg" width="600" >}}

1. 패널 제목
2. 차트 타입 선택
    - Info : 차트 타입 설명을 확인합니다.
    - Preview : 샘플 데이터를 이용해 차트를 미리 봅니다.
3. Link Mode  
    대시보드의 시간 범위 및 자동 새로 고침 설정과 차트를 연동할지 여부를 지정합니다.
    - With : 대시보드 설정과 연동 (기본값)
    - Without : 연동하지 않음
4. Query
    - 하나의 차트에서 여러 개의 Query를 정의할 수 있습니다.
    - Link Mode에서 연결을 해제하지 않는 이상, 모든 Query는 대시보드 시간 범위 및 자동 새로 고침 설정의 영향을 받습니다.
5. Transform  
    - Query 결과를 이용해 새로운 데이터를 생성합니다. {{< neo_since ver="8.0.46" />}}
    - Transform에서 생성한 데이터도 Query와 동일하게 표시 여부를 선택할 수 있으며, Query와 동일한 옵션을 사용합니다.
6. Chart Option  
    - 차트 타입에 따라 사용할 수 있는 옵션이 다릅니다.  
    - 자세한 내용은 “차트 타입별 옵션”을 참고하십시오.

### Query
하나의 차트에서 여러 Query를 동시에 사용할 수 있으며, 각 Query에 대해 설정을 개별적으로 지정합니다.

#### 변환 함수
{{< figure src="/images/web-ui/chart-setting-function.jpg" width="600" >}}
- X: 시간/범주 값에 적용할 변환식
- Y: 값(수치)에 적용할 변환식
- 전체: X, Y 전체에 적용할 변환식  
※ 이 탭에서 설정한 수식은 Option 탭에서 지정한 설정보다 우선 적용됩니다.  
※ Query 결과를 로그 변환 등의 수식으로 가공할 때 사용합니다.

#### Tag-Based Query Mode
**Tag 테이블**에서만 사용할 수 있는 모드입니다.
- Table : 대상 테이블 이름
- Tag : 사용할 태그 이름 입력 또는 선택
- Aggregator : x축 시간 간격에 따라 적용할 집계 함수  
  **옵션** : value, sum, avg, min, max, count  
  (`value` 선택 시 집계 없이 원본 데이터를 사용)
- Alias : 범례에 표시할 이름

#### Advanced Query Mode
쿼리 구성을 직접 지정하는 모드입니다.
{{< figure src="/images/web-ui/chart-setting-advanced-query.jpg" width="600" >}}  
- Table : 테이블 이름
- Time Field : x축 시간 값으로 사용할 컬럼
- Value Field : y축 값으로 사용할 컬럼
- Aggregator : 집계 함수 (Tag-Based 모드와 동일)
- Alias : 범례에 표시할 이름
- Filter : WHERE 절에 사용할 조건 (여러 조건 입력 시 AND로 결합)

#### Transform Data
정의한 **Query** 결과를 이용해 새로운 데이터를 계산할 수 있습니다. {{< neo_since ver="8.0.46" />}}
- 아래 그림과 같이 두 개 이상의 **Query**를 정의한 뒤  
{{< figure src="/images/web-ui/transform-1.jpg" width="600" >}}
- 계산에만 사용할 Query는 “Visible” 아이콘을 끄면 차트에 표시되지 않습니다.  
{{< figure src="/images/web-ui/transform-2.jpg" width="600" >}}  
- Transform 탭에서 계산에 사용할 **Query**를 선택하고 수식을 입력합니다. 수식에서는 선택된 Query 앞에 표시되는 영문자를 사용합니다. (예: `log(B/A)`)  
{{< figure src="/images/web-ui/transform-3.jpg" width="600" >}}  
- [?] 버튼에서 간단한 도움말을 볼 수 있으며, 사용 가능한 수학 함수는 왼쪽 메뉴 “TQL > Utility Functions”의 “Math” 항목에서 확인할 수 있습니다.  
{{< figure src="/images/web-ui/transform_help.jpg" width="400" >}}  
※ Query 결과를 다시 계산해 시각화하는 방식이므로 단일 Query를 사용하는 것보다 느릴 수 있습니다.

#### Control Function
{{< figure src="/images/web-ui/chart-setting-qurey-tool.jpg" width="200" >}}  
- a. 쿼리를 직접 입력합니다. {{< neo_since ver="8.0.46" />}}  
{{< figure src="/images/web-ui/custom_query.jpg" width="600" >}}
    - SELECT 절은 “시간(밀리초)”과 “값” 순으로 구성해야 합니다.  
      예) `SELECT TO_TIMESTAMP(TIME ROLLUP {{period_value}} {{period_unit}}) / 1000000 AS TIME, avg(VALUE) AS 'Usage'`
    - 기본 변수와 사용자 정의 변수를 모두 사용할 수 있습니다. (기본 변수는 “TQL 차트 설정” 참고)
    - [?] 아이콘을 눌러 간단한 도움말을 확인할 수 있습니다.
- b. 데이터베이스에서 추출한 값에 적용할 수식을 입력합니다. (예: `value * 1.5`)
- c. 해당 Query를 차트에 표시할지 여부를 선택합니다. {{< neo_since ver="8.0.46" />}}
- d. 차트 색상을 지정합니다.
- e. “Advanced Query Mode”와 “Tag-Based Query Mode”를 전환합니다.
- f. Query를 삭제합니다.

### TQL 차트
“TQL Chart” 타입은 대시보드에서 사용자 정의 TQL 파일을 활용할 수 있는 기능입니다. SINK 함수가 `CHART`로 설정된 TQL 파일만 사용할 수 있습니다.

{{< figure src="/images/web-ui/tql-chart-setting.jpg" width="600" >}}

#### TQL 차트 설정
**Tql path :** 사용할 TQL 파일을 선택합니다.  
**Params :** TQL 파일에 전달할 파라미터를 등록합니다.  
값을 직접 입력하거나 대시보드에서 제공하는 기본 변수를 사용할 수 있으며, 기본 변수에는 시간 범위와 x축 간격 등이 포함됩니다.
- Time range : 대시보드의 다른 차트와 시간 동기화를 위해 사용됩니다.
  | Params | Desc |
  |:-------|:-----|
  | {{from_str}} | 날짜 문자열 (YYYY-MM-DD HH:MI:SS) |
  | {{from_s}},{{from_ms}},{{from_us}},{{from_ns}} | 유닉스 타임스탬프 (초/밀리초/마이크로초/나노초) |
  | {{to_str}} | 날짜 문자열 (YYYY-MM-DD HH:MI:SS) |
  | {{to_s}},{{to_ms}},{{to_us}},{{to_ns}} | 유닉스 타임스탬프 (초/밀리초/마이크로초/나노초) |
- period : 시간 범위와 패널 크기에 따라 계산된 x축 간격
  | Params | Desc |
  |:-------|:-----|
  | {{period}} | 기간 표현 (예: 10s) |
  | {{period_value}} | 기간 값 (예: 10) |
  | {{period_unit}} | 기간 단위 (예: sec) |

#### TQL 파일에서 파라미터 사용하기
TQL 파일에서 `param()` 함수를 사용해 대시보드에서 전달된 파라미터를 활용할 수 있습니다.

예시 TQL:
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
- `param()`과 `strSprintf()`를 이용해 동적으로 쿼리를 생성합니다.  
- 주요 파라미터  
  - `period_unit`: 시간 간격 단위 (기본값 `msec`)  
  - `period_value`: 간격 값 (기본값 10)  
  - `from`, `to`: 조회 기간  
  - `tag`: 조회할 태그 (기본값 `tag01`)

**CHART_LINE():**  
- 쿼리 결과를 라인 차트로 렌더링합니다.

### 차트 타입별 옵션
#### 공통 옵션
- 패널 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Title | 차트 패널에 표시될 제목 |
| Theme | 차트 테마 (왼쪽 메뉴 “TQL > CHART” 참고) |

- 범례 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Show legend | 범례 표시 여부 |
| Vertical | 세로 정렬 (top / center / bottom) |
| Horizontal | 가로 정렬 (left / center / right) |
| Alignment type | 정렬 방식 (horizontal / vertical) |

- 패널 여백  
패널 테두리와 차트 사이의 여백을 설정합니다. 범례 공간이 필요하다면 여백을 넉넉히 설정하십시오.
| 옵션 | 설명 |
|:-----|:-----|
| Top | 상단 여백 |
| Bottom | 하단 여백 |
| Left | 좌측 여백 |
| Right | 우측 여백 |

- 툴팁
| 옵션 | 설명 |
|:-----|:-----|
| Show tooltip | 툴팁 사용 여부 |
| Type | 툴팁 타입 (axis / item) |
| Unit | 툴팁에 표시할 단위 |
| Decimals | 소수점 자릿수 |

- xAxis
| 옵션 | 설명 |
|:-----|:-----|
| Interval type | x축 시간 간격 단위 (none / sec / min / hour, none은 자동 계산) |
| Interval value | x축 간격 값 |

- yAxis  
※ [+] 버튼을 눌러 듀얼 Y축을 구성할 수 있습니다. {{< neo_since ver="8.0.46" />}} 추가된 Y축에 사용할 시리즈를 선택하면 하단 옵션은 기본 Y축과 동일합니다.
| 옵션 | 설명 |
|:-----|:-----|
| Position | Y축 위치 (left / right) |
| Offset | 축과 라벨 사이의 간격 |
| Type | Y축 값 타입 |
| - Unit | 단위 |
| - Decimals | 소수점 자릿수 |
| - Name | Y축 이름 (축 상단에 표시) |
| Min | 최소값 |
| Max | 최대값 |
| Start at zero | Y축에 항상 0을 포함할지 여부 |

#### Line

{{< figure src="/images/web-ui/line-chart-setting.jpg" width="600" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Fill area | 면 채우기 사용 (0~1 사이의 불투명도 설정 필요) |
| Smooth line | 곡선 형태로 선을 표시 |
| Show symbols | 데이터 포인트 표시 여부 |
| Symbol type | 심볼 타입 (circle / rect / roundRect / triangle / diamond / pin / arrow) |
| Symbol size | 심볼 크기 |
| Symbol rotate | 심볼 회전 각도 |
| Symbol offset | 심볼 위치 오프셋 |
| Stack | 시리즈를 스택 모드로 표시 |
| Step style | 계단형 선 스타일 |
| Emphasis | 강조 설정 (hover 시) |
| Animation | 애니메이션 사용 여부 |

#### Area
{{< figure src="/images/web-ui/area-chart-setting.jpg" width="600" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Fill area | 면 채우기 사용 (0~1 사이 불투명도) |
| Emphasis | 강조 설정 |
| Animation | 애니메이션 사용 여부 |

#### Column
{{< figure src="/images/web-ui/column-chart-setting.jpg" width="600" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Bar width | 막대 너비 |
| Emphasis | 강조 설정 |
| Animation | 애니메이션 사용 여부 |

#### Column range
{{< figure src="/images/web-ui/column-range-chart-setting.jpg" width="600" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Bar width | 막대 너비 |
| Emphasis | 강조 설정 |
| Animation | 애니메이션 사용 여부 |

- Query 옵션  
Column range는 각 시리즈에 최대값과 최소값 쿼리가 필요합니다.
| 옵션 | 설명 |
|:-----|:-----|
| Max query | 최대값을 반환하는 Query |
| Min query | 최소값을 반환하는 Query |

#### Column step
{{< figure src="/images/web-ui/column-step-chart-setting.jpg" width="600" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Bar width | 막대 너비 |
| Emphasis | 강조 설정 |
| Animation | 애니메이션 사용 여부 |

#### Stacked column
{{< figure src="/images/web-ui/stacked-column-chart-setting.jpg" width="600" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Bar width | 막대 너비 |
| Emphasis | 강조 설정 |
| Animation | 애니메이션 사용 여부 |

- 스택 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Stacked column | 스택 모드 사용 여부 |
| Stacked type | 스택 방식 (normal / percent) |

#### XY column
{{< figure src="/images/web-ui/xy-column-chart-setting.jpg" width="600" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Bar width | 막대 너비 |
| Emphasis | 강조 설정 |
| Animation | 애니메이션 사용 여부 |

- Query 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Value Field | y축 값으로 사용할 컬럼 |
| Category Field | x축 범주로 사용할 컬럼 |

#### Stacked area
{{< figure src="/images/web-ui/stacked-area-chart-setting.jpg" width="600" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Fill area | 면 채우기 사용 |
| Smooth line | 곡선 처리 |
| Emphasis | 강조 설정 |
| Animation | 애니메이션 사용 여부 |

- 스택 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Stacked area | 스택 모드 사용 여부 |
| Stacked type | 스택 방식 (normal / percent) |

#### Scatter

{{< figure src="/images/web-ui/scatter-chart-setting.jpg" width="600" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Large data mode | 대량 데이터 처리 모드 |

- 심볼 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Type | 심볼 타입 (circle / rect / roundRect / triangle / diamond / pin / arrow) |
| Size | 심볼 크기 |

#### Adv scatter
{{< neo_since ver="8.0.46" />}}
{{< figure src="/images/web-ui/adv-scatter-chart-setting.jpg" width="600" >}}

- xAxis
| 옵션 | 설명 |
|:-----|:-----|
| Type | x축 값 타입 |
| - Unit | 단위 |
| - Decimals | 소수점 자릿수 |
| Min | 최소값 |
| Max | 최대값 |
| Start at zero | x축에 항상 0 포함 |
| Series | x축으로 사용할 시리즈 선택 (기본값 첫 번째 Query) |

- 심볼 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Type | 심볼 타입 (circle / rect / roundRect / triangle / diamond / pin / arrow) |
| Size | 심볼 크기 |

#### Gauge

{{< figure src="/images/web-ui/gauge-chart-setting.jpg" width="250" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Min | 최소값 |
| Max | 최대값 |

- 축 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Label distance | 라벨과 원형 라인 사이 거리 (음수면 외부) |
| Show axis tick | 눈금 표시 여부 |
| Setting line colors | 값 범위에 따라 선 색상 지정 (0~1 비율) |

- Anchor
| 옵션 | 설명 |
|:-----|:-----|
| Show anchor | 중앙 원 표시 여부 |
| Size | 중앙 원 크기 |

- 표시 값
| 옵션 | 설명 |
|:-----|:-----|
| Font size | 게이지 내부 값의 글꼴 크기 |
| Offset from center | 중심으로부터의 거리 |
| Decimal places | 소수점 자릿수 |
| Active animation | 애니메이션 사용 여부 |

#### Pie

{{< figure src="/images/web-ui/pie-chart-setting.jpg" width="250" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Doughnut ratio | 도넛 모드 비율 (0~100) |
| Nightingale mode | 나이팅게일 모드 적용 (값에 따라 반지름 변화) |

#### Liquid fill

{{< figure src="/images/web-ui/liquid_fill-chart-setting.jpg" width="250" >}}

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Shape | 모양 (container / circle / rect / roundRect / triangle / diamond / pin / arrow) |
| Unit | 표시 값의 단위 |
| Digit | 소수점 자릿수 |
| Font size | 글꼴 크기 |
| Wave min | 파형 최소값 |
| Wave max | 파형 최대값 |
| Wave amplitude | 파형 진폭 (0이면 직선) |
| Background color | 파형 영역 배경색 |
| Wave animation | 파형 애니메이션 사용 여부 |
| Outline | 외곽선 표시 여부 |

#### Text
{{< neo_since ver="8.0.46" />}}
{{< figure src="/images/web-ui/text-chart-setting.jpg" width="250" >}}

첫 번째 **Query** 결과가 텍스트로 표시되며, 두 번째 **Query**를 추가하면 배경 차트로 활용됩니다.
- 텍스트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Font size | 글꼴 크기 |
| Unit | 단위 |
| Digit | 소수점 자릿수 |
| Color | 색상 |

- 차트 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Type | 배경 차트 타입 (line / bar / scatter) |
| Opacity | 채우기 불투명도 (0~1, line 타입만 해당) |
| Symbol size | 데이터 포인트 크기 (0이면 표시 없음) |
| Color | 색상 |

#### Geomap
{{< neo_since ver="8.0.46" />}}
{{< figure src="/images/web-ui/geomap-chart-setting.jpg" width="400" >}}

- 툴팁
| 옵션 | 설명 |
|:-----|:-----|
| Time | 툴팁에 시간 표시 |
| Latitude, Longitude | 위도·경도 표시 |

- Interval
| 옵션 | 설명 |
|:-----|:-----|
| Interval type | x축 시간 간격 단위 (none / sec / min / hour, none은 자동 계산) |
| Interval value | x축 간격 값 |

- 지도 옵션
| 옵션 | 설명 |
|:-----|:-----|
| Use zoom control | 지도의 줌 컨트롤 사용 여부 |
| Series | Query 별로 설정 |
| - Latitude | 위도 컬럼 이름 (별칭 또는 집계 컬럼 선택 가능) |
| - Longitude | 경도 컬럼 이름 (별칭 또는 집계 컬럼 선택 가능) |
| - Marker shape | 마커 형태 (marker, circleMarker, circle) |
| - Marker radius | 마커 반경 (circleMarker: 픽셀, circle: 미터) |
