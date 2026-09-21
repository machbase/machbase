---
title: 차트 타입별 옵션
type: docs
weight: 40
---

차트 설정 화면 오른쪽 위에서 타입을 고릅니다. 선택할 수 있는 타입은 **Line, Bar, Scatter, Adv scatter, Gauge, Pie, Liquid fill, Text, Geomap, Tql chart, Video** 11종이며, 타입에 따라 아래쪽 옵션 목록이 달라집니다. 여러 타입이 함께 쓰는 Panel option·Legend·Panel padding·Tooltip·xAxis·yAxis는 “차트 설정”의 차트 옵션을 참고하십시오.

Tql chart와 Video는 설정 방식이 다르므로 별도 문서(“TQL 차트”, “Video 패널”)에서 다룹니다.

## Line

{{< media slug="neo-dashboard/type-line" width="600" >}}

| 옵션 | 설명 |
|:-----|:-----|
| Fill area | 선 아래를 채웁니다. 불투명도(0~1)를 함께 지정합니다. |
| Smooth line | 선을 곡선으로 표시합니다. |
| Show symbols | 데이터 포인트를 표시합니다. |
| Symbol type | 심볼 모양 (circle / rect / roundRect / triangle / diamond / pin / arrow) |
| Symbol size | 심볼 크기 |
| Stack | 여러 시리즈를 쌓아서 표시합니다. |
| Step style | 계단형 선으로 표시합니다. |
| Large data mode | 대량 데이터를 표시할 때 사용하는 모드입니다. |

## Bar

{{< media slug="neo-dashboard/type-bar" width="600" >}}

| 옵션 | 설명 |
|:-----|:-----|
| Large data mode | 대량 데이터를 표시할 때 사용하는 모드입니다. |
| Polar mode | 막대를 원형으로 배치합니다. |
| - Max | 최대값 |
| - Start angle | 시작 각도 |
| - Radius | 안쪽 반지름 (0이면 가운데를 비우지 않습니다) |
| - Polar size | 바깥 반지름 (100이면 패널을 가득 채웁니다) |
| - Polar axis | x축 종류 (time / category) |

막대 폭은 시리즈 수와 패널 크기에 따라 자동으로 계산됩니다.

## Scatter

{{< media slug="neo-dashboard/type-scatter" width="600" >}}

| 옵션 | 설명 |
|:-----|:-----|
| Large data mode | 대량 데이터를 표시할 때 사용하는 모드입니다. |
| Symbol type | 심볼 모양 |
| Symbol size | 심볼 크기 |

## Adv scatter

{{< neo_since ver="8.0.46" />}}

{{< media slug="neo-dashboard/type-adv-scatter" width="600" >}}

x축과 y축에 모두 값을 쓰는 산점도입니다. 시간 대신 **다른 시리즈의 값을 x축(기준축)** 으로 사용합니다.

- **기준축 지정** : 오른쪽 옵션의 `xAxis > Series`에서 기준축으로 쓸 시리즈를 하나 고릅니다. 한 번에 하나만 선택할 수 있으며, 지정하지 않으면 첫 번째 시리즈가 기준축이 됩니다.
- **점이 찍히는 방식** : 기준축이 아닌 시리즈의 값이 같은 시각의 기준 시리즈 값에 대응해 한 점(x, y)으로 찍힙니다.
- **기준 시리즈 숨기기** : 기준 시리즈는 x좌표로만 쓰이므로, 해당 시리즈 행의 **Visible** <img src="/images/web-ui/neo-dashboard/icons/dash_series_visible.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘을 꺼서 차트에 따로 그려지지 않게 합니다.

아래 화면은 `demo.cpu`를 기준축으로 지정하고 Visible을 끈 뒤, `demo.mem`을 y축 값으로 그린 예시입니다.

| 옵션 | 설명 |
|:-----|:-----|
| Unit / Decimals | x축 값의 단위와 소수점 자릿수 |
| Min / Max | x축 최소·최대값 |
| Start at zero | x축에 항상 0을 포함합니다. |
| Series | x축으로 사용할 시리즈. 기본값은 첫 번째 시리즈입니다. |
| Symbol type / size | 심볼 모양과 크기 |

## Gauge

{{< media slug="neo-dashboard/type-gauge" width="600" >}}

| 옵션 | 설명 |
|:-----|:-----|
| Min / Max | 게이지의 최소·최대값 |
| Label distance | 라벨과 눈금선 사이 거리 (음수면 바깥쪽) |
| Show axis tick | 눈금 표시 |
| Setting line colors | 값 구간별 선 색상 (0~1 비율로 지정) |
| Show anchor / Size | 가운데 원의 표시 여부와 크기 |
| Font size | 게이지 안에 표시되는 값의 글꼴 크기 |
| Offset from center | 값 표시 위치의 중심으로부터 거리 |
| Unit | 게이지 값의 단위 |
| Decimal | 소수점 자릿수 |
| Active animation | 애니메이션 사용 여부 |

## Pie

{{< media slug="neo-dashboard/type-pie" width="600" >}}

| 옵션 | 설명 |
|:-----|:-----|
| Doughnut ratio | 가운데를 비우는 비율 (0~100) |
| Nightingale mode | 값에 따라 반지름이 달라지는 모드 |

## Liquid fill

{{< media slug="neo-dashboard/type-liquid-fill" width="600" >}}

| 옵션 | 설명 |
|:-----|:-----|
| Shape | 모양 (container / circle / rect / roundRect / triangle / diamond / pin / arrow) |
| Unit | 표시 값의 단위 |
| Digit | 소수점 자릿수 |
| Font size | 글꼴 크기 |
| Wave min / max | 파형의 최소·최대값 |
| Wave amplitude | 파형의 진폭 (0이면 직선) |
| Background color | 파형 영역의 배경색 |
| Wave animation | 파형 애니메이션 사용 여부 |
| Outline | 외곽선 표시 여부 |

## Text

{{< neo_since ver="8.0.46" />}}

{{< media slug="neo-dashboard/type-text" width="600" >}}

첫 번째 시리즈 값을 큰 글자로 표시하고, 두 번째 시리즈를 배경 차트로 그립니다.

| 옵션 | 설명 |
|:-----|:-----|
| Font size | 글꼴 크기 |
| Unit | 단위 |
| Digit | 소수점 자릿수 |
| Color | 기본 색상. 값 구간을 추가해 구간별로 다른 색을 지정할 수 있습니다. |
| Series | 텍스트와 배경 차트에 사용할 시리즈를 각각 지정합니다. |
| Type | 배경 차트 종류 (line / bar / scatter) |
| Opacity | 채우기 불투명도 (0~1, line에서만) |
| Symbol size | 데이터 포인트 크기 (0이면 표시하지 않음) |

## Geomap

{{< neo_since ver="8.0.46" />}}

{{< media slug="neo-dashboard/type-geomap" width="600" >}}

| 옵션 | 설명 |
|:-----|:-----|
| Time | 툴팁에 시각을 표시합니다. |
| Latitude, Longitude | 툴팁에 위도·경도를 표시합니다. |
| Interval type / value | x축 시간 간격 (none / sec / min / hour, none은 자동 계산) |
| Use zoom control | 지도 확대·축소 컨트롤을 사용합니다. 패널 메뉴에서도 바로 켜고 끌 수 있습니다. |
| Series | 시리즈별로 아래 항목을 지정합니다. |
| - Latitude / Longitude | 위도·경도 컬럼 이름 |
| - Marker shape | 마커 모양 (marker / circleMarker / circle) |
| - Marker radius | 마커 반경 (circleMarker는 픽셀, circle은 미터) |

## Line·Bar 옵션으로 만드는 변형

영역형(Area), 누적(Stacked), 계단형(Step) 차트는 별도 타입이 아니라 Line·Bar의 옵션 조합입니다.

| 만들고 싶은 모양 | 타입 | 설정 |
|:--|:--|:--|
| 영역형 | Line | `Fill area` 켜기 |
| 누적 영역형 | Line | `Fill area` + `Stack` |
| 계단형 | Line | `Step style` |
| 세로 막대 | Bar | 기본값 |
| 원형 막대 | Bar | `Polar mode` |
