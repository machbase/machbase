---
title: 차트 설정
type: docs
weight: 30
---

## 개요

{{< media slug="neo-dashboard/chart-setting-preview" width="600" >}}

차트 설정 화면은 세 영역으로 나뉩니다.

- **미리보기** : 현재 설정으로 그린 차트입니다.
- **시리즈 설정** : 조회할 데이터(Series), 계산(Transform), 이 패널만의 범위(Time 또는 Distance)를 탭으로 정합니다.
- **차트 옵션** : 차트 타입과 표시 옵션을 정합니다.

## 미리보기

오른쪽 위의 `Apply`는 미리보기를 갱신하고, `Save`는 설정한 패널을 대시보드에 추가합니다. `Discard`는 변경을 버리고 나갑니다.

- **Discard** : 저장하지 않고 차트 설정 화면을 닫습니다.
- **Apply** : 바뀐 설정으로 미리보기를 다시 그립니다. 바뀐 설정이 없으면 **Refresh**로 표시되며, 누르면 데이터를 다시 조회합니다.
- **Save** : 새 패널이면 대시보드에 추가하고, 기존 패널이면 수정 내용을 반영한 뒤 화면을 닫습니다.

## 시리즈 설정

탭 오른쪽의 `Total n / 12`는 Visible이 켜진 Series와 Transform의 개수입니다. 한 패널에는 최대 12개까지 표시할 수 있습니다.

### 기본 입력

TAG 테이블을 조회할 때 쓰는 기본 입력입니다.

{{< media slug="neo-dashboard/query-tag-based" width="600" >}}

- **Table** : 조회할 테이블. 목록에는 테이블 이름 아래에 `데이터베이스 · 소유자`가 함께 표시됩니다. `{{변수명}}` 형태로 변수를 직접 입력할 수도 있습니다. Gauge, Pie, Liquid fill 타입에서는 TAG 테이블마다 태그별 통계 뷰 `V$<테이블>_STAT`도 목록에 나타나며, 통계 열(`ROW_COUNT`, `MIN_VALUE`, `MAX_VALUE` 등)을 Value field로 골라 태그의 건수·최솟값·최댓값을 표시할 수 있습니다.
- **Tag** : 사용할 태그 이름. 오른쪽 <img src="/images/web-ui/neo-dashboard/icons/dash_tag_search.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘을 누르면 태그 검색 창이 열립니다.
- **Time field / Value field** : x축 기준 열과 y축 값 열. 값 열이 JSON 타입이면 **JSON key** 선택기가 추가로 나타나 JSON 내부 경로를 지정할 수 있습니다.
- **Aggregator** : x축 간격마다 적용할 집계 함수입니다. `value`(집계 없이 원본), `sum`, `avg`, `min`, `max`, `count`와 함께 `diff`, `diff (abs)`, `diff (no-negative)`를 사용할 수 있습니다.
- **Alias** : 범례에 표시할 이름.

### 상세 입력 (Expand)

시리즈 행의 **Expand** <img src="/images/web-ui/neo-dashboard/icons/dash_series_expand.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘을 누르면 값 열과 조건을 직접 지정하는 입력으로 바뀝니다. Table과 Time field는 기본 입력과 같습니다.

- **Value field** : 값 열입니다. 값마다 Aggregator와 Alias를 지정하며, Geomap 타입에서는 <img src="/images/web-ui/neo-dashboard/icons/dash_add_series.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘으로 값을 여러 개 추가할 수 있습니다.
- **Filter** : WHERE 절 조건을 입력합니다. <img src="/images/web-ui/neo-dashboard/icons/dash_add_series.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘으로 조건을 추가하면 `AND`로 결합되며, 조건 행의 **Typing** <img src="/images/web-ui/neo-dashboard/icons/dash_series_typing.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘을 누르면 조건식을 직접 입력할 수 있습니다.
- **Duration From / To** : LOG 테이블에서만 표시됩니다. 조회 범위의 시작과 끝을 기준에서 얼마나 옮길지 `-30s`, `+30s` 같은 형식으로 지정합니다.

LOG, VIEW 등 TAG 테이블이 아닌 테이블은 처음부터 상세 입력으로 표시되며, 기본 입력으로 전환할 수 없습니다.

### SQL 직접 입력 (Typing)

{{< neo_since ver="8.0.46" />}}

시리즈 행의 **Typing** <img src="/images/web-ui/neo-dashboard/icons/dash_series_typing.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘을 누르면 조회 내용 전체를 SQL로 직접 작성할 수 있습니다. Line과 Bar 타입에서만 사용할 수 있으며, Aggregator가 `diff` 계열이면 전환되지 않습니다.

{{< media slug="neo-dashboard/query-typing-mode" width="600" >}}

- SELECT 절은 “시각(밀리초)” 다음에 “값” 순서로 구성해야 합니다.
- 대시보드가 제공하는 기본 변수(`{{period_value}}`, `{{period_unit}}` 등)와 사용자 정의 변수를 함께 쓸 수 있습니다. 기본 변수 목록은 “TQL 차트”를 참고하십시오.

### 시리즈 행 아이콘

{{< media slug="neo-dashboard/query-control-icons" width="200" >}}

왼쪽부터 차례로 다음 기능입니다.

- <img src="/images/web-ui/neo-dashboard/icons/dash_series_typing.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Typing** : SQL 직접 입력으로 전환합니다. SQL 입력 중에는 **Selecting**으로 바뀌며, 누르면 선택 입력으로 돌아갑니다.
- <img src="/images/web-ui/neo-dashboard/icons/dash_series_formula.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Enter formula** : 조회한 값에 적용할 수식을 입력합니다. (예: `value * 1.5`)
- <img src="/images/web-ui/neo-dashboard/icons/dash_series_visible.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Visible** : 이 시리즈를 차트에 표시할지 정합니다. 계산에만 쓰는 시리즈는 꺼 둡니다.
- <img src="/images/web-ui/neo-dashboard/icons/dash_series_color.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Color** : 시리즈 색상을 지정합니다.
- <img src="/images/web-ui/neo-dashboard/icons/dash_series_expand.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Expand** : 상세 입력으로 전환합니다. 상세 입력 중에는 **Collapse**로 바뀌며, 누르면 기본 입력으로 돌아갑니다.
- <img src="/images/web-ui/neo-dashboard/icons/dash_series_delete.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Delete** : 시리즈를 삭제합니다.

### Transform

{{< neo_since ver="8.0.46" />}}

정의한 시리즈 결과로 새로운 데이터를 계산합니다. Line, Bar, Scatter, Pie, Adv scatter, Liquid fill, Gauge, Text 타입에서 탭이 표시됩니다. 먼저 계산에 사용할 시리즈를 두 개 이상 정의합니다.

{{< media slug="neo-dashboard/query-two-series" width="600" >}}

그다음 **Transform** 탭에서 행을 추가하고 수식을 작성합니다.

{{< media slug="neo-dashboard/transform-filled" width="600" >}}

- **Alias** : 결과 시리즈의 이름.
- **Series** : 계산에 사용할 시리즈를 선택합니다.
- **Formula** : 선택한 시리즈 앞에 표시되는 영문자로 식을 씁니다. (예: `log(B/A)`)
- <img src="/images/web-ui/neo-dashboard/icons/dash_transform_help.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘에서 간단한 도움말을 볼 수 있으며, 사용 가능한 수학 함수는 왼쪽 메뉴 “TQL > Utility Functions”의 Math 항목에 있습니다.

Transform으로 만든 시리즈는 일반 시리즈와 똑같이 다룹니다.

- 행 오른쪽의 **Visible** <img src="/images/web-ui/neo-dashboard/icons/dash_series_visible.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">·**Color** <img src="/images/web-ui/neo-dashboard/icons/dash_series_color.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">로 표시 여부와 색을 정합니다. 계산에만 쓴 원본 시리즈는 Visible을 꺼 두고 결과 시리즈만 보이게 할 수 있습니다.
- 차트 옵션에서 시리즈를 고르는 곳(yAxis의 Series, Text의 Series 등)에 **Alias** 이름으로 나타납니다. Alias를 비워 두면 `TRANSFORM_VALUE(0)`처럼 순번 이름이 붙습니다.
- Visible이 켜진 Transform 결과도 `Total n / 12`에 포함됩니다.

※ 시리즈 결과를 다시 계산해 시각화하므로 계산 없는 시리즈보다 느릴 수 있습니다.

### Time · Distance 탭

이 패널만의 조회 범위와 새로 고침 주기를 정합니다. 거리 기준으로 조회하는 패널에는 Time 탭 대신 Distance 탭이 나타납니다. 자세한 내용은 “차트 패널”의 패널 단위 시간·거리 범위를 참고하십시오.

## 차트 옵션

맨 위에서 차트 타입을 고르고, 그 아래에서 표시 옵션을 정합니다. 타입마다 달라지는 옵션은 “차트 타입별 옵션”을 참고하십시오.

아래 옵션은 여러 차트 타입에 공통으로 나타납니다. 표시되는 타입은 다음과 같습니다.

- **Panel option** : TQL, Video를 제외한 모든 타입
- **Legend · Panel padding · Tooltip** : TQL, Video, Text, Geomap을 제외한 모든 타입
- **xAxis · yAxis** : Line, Bar, Scatter, Adv scatter

### Panel option

| 옵션 | 설명 |
|:-----|:-----|
| Title | 차트 패널에 표시될 제목. Geomap에서는 오른쪽 색상 선택기로 제목 색도 지정합니다. |
| Theme | 차트 테마 (왼쪽 메뉴 “TQL > CHART” 참고) |

### Legend

| 옵션 | 설명 |
|:-----|:-----|
| Show legend | 범례 표시 여부 |
| Vertical | 세로 위치 (top / center / bottom) |
| Horizontal | 가로 위치 (left / center / right) |
| Alignment type | 정렬 방식 (horizontal / vertical) |

### Panel padding

패널 테두리와 차트 사이의 여백입니다. 범례 공간이 필요하면 여백을 넉넉히 설정하십시오.

| 옵션 | 설명 |
|:-----|:-----|
| Top | 상단 여백 |
| Bottom | 하단 여백 |
| Left | 좌측 여백 |
| Right | 우측 여백 |

### Tooltip

| 옵션 | 설명 |
|:-----|:-----|
| Show tooltip | 툴팁 사용 여부 |
| Type | 툴팁 타입 (item / axis) |
| Unit | 툴팁에 표시할 단위 |
| Decimals | 소수점 자릿수 |

### xAxis

| 옵션 | 설명 |
|:-----|:-----|
| Interval type | x축 간격 단위. 시간 축은 none / sec / min / hour, 거리 축은 none / value 중에서 고릅니다. none은 자동 계산입니다. |
| Interval value | x축 간격 값 |

거리 기준 축을 쓰는 패널과 Adv scatter에서는 **Options** 항목에 값 축 옵션(Unit · Decimals · Min · Max · Start at zero)이 추가로 표시됩니다.

### yAxis

{{< neo_since ver="8.0.46" />}}

| 옵션 | 설명 |
|:-----|:-----|
| Name | Y축 이름 |
| Position | Y축 위치 (left / right) |
| Offset | 축을 기본 위치에서 옮기는 거리(픽셀) |
| Tick options | 눈금 값의 Unit(단위), Decimals(소수점 자릿수), Min(최소값), Max(최대값), Start at zero(항상 0 포함) |
| Thresholds | **Add threshold**로 값과 색을 지정한 임계선을 추가합니다. 여러 개 추가할 수 있습니다. (Line / Bar / Scatter) |

<img src="/images/web-ui/neo-dashboard/icons/dash_add_series.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘으로 Y축을 하나 더 추가하고(최대 2개), 추가된 축의 **Series**에서 그 축에 그릴 시리즈를 선택합니다. 추가된 축의 옵션은 기본 Y축과 같습니다.
