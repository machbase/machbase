---
title: 차트 패널
type: docs
weight: 20
---

## 패널 조작

- **위치 이동** : 패널 상단(헤더)을 드래그합니다.
- **크기 조절** : 패널 우측 하단 모서리를 드래그합니다. 저장된 크기보다 작게 줄일 수는 없습니다.
- **범례 토글** : 범례 항목을 클릭하면 해당 시리즈를 표시하거나 숨깁니다.
- **자동 새로 고침 표시** : 패널이 자체 새로 고침 주기를 가지면 헤더에 남은 시간을 나타내는 링이 표시되며, 이 링에서 주기를 바로 바꾸거나 끌 수 있습니다.

## 패널 메뉴

패널 우측 상단의 <img src="/images/web-ui/neo-dashboard/icons/dash_panel_menu.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘을 클릭하면 메뉴가 열립니다.

{{< media slug="neo-dashboard/panel-menu" width="600" >}}

- **Setting** : 차트 설정을 수정합니다. (자세한 내용은 “차트 설정” 참고)
- **Duplicate** : 현재 차트를 복제합니다. 복제된 패널은 원본 바로 아래에 배치됩니다.
- **Show Taganalyzer** : 현재 차트의 내용을 Tag Analyzer에서 엽니다. {{< neo_since ver="8.0.49" />}} TAG 테이블을 사용하는 패널에서만 표시됩니다.
- **Download data** : 패널이 조회한 데이터를 CSV 파일로 곧바로 내려받습니다.
- **Delete** : 차트 패널을 삭제합니다.
- **Save to tql** : 패널이 내부적으로 사용하는 TQL을 파일로 저장합니다. 저장 창에서 파일명과 Output(`CHART` / `DATA(JSON)` / `DATA(CSV)`)을 지정하며, 특정 시리즈만 골라 저장할 수도 있습니다. Tql chart, Geomap, Text, Video 타입에는 이 항목이 없습니다.

차트 타입에 따라 아래 항목이 추가로 나타납니다.

- **Use zoom control** (Geomap) : 지도 확대·축소 컨트롤을 바로 켜고 끕니다.
- **Synchronization**, **Child board**, **Fullscreen** (Video) : “Video 패널”을 참고하십시오.

## 패널 단위 시간·거리 범위

### Time 탭

차트 설정 화면의 **Time** 탭에서 그 패널만의 조회 범위와 새로 고침 주기를 지정할 수 있습니다.

{{< media slug="neo-dashboard/panel-time-tab" width="600" >}}

- **Refresh** : 이 패널만의 자동 새로 고침 주기입니다. 지정하면 패널 헤더에 카운트다운 링이 표시됩니다.
- **From / To** : 대시보드 전체 범위 대신 사용할 시간 범위입니다.
- **Quick Range** : 자주 쓰는 범위를 한 번에 지정합니다.

값을 지정하지 않으면 패널은 대시보드의 시간 범위와 새로 고침 설정을 그대로 따릅니다.

### Distance 탭

거리 기준으로 조회하는 패널에는 Time 탭 대신 **Distance** 탭이 나타납니다.

{{< media slug="neo-dashboard/panel-distance-tab" width="600" >}}

- **Refresh** : 이 패널만의 자동 새로 고침 주기입니다.
- **범위 표시와 배지** : 이 패널만의 범위를 지정하면 `Panel` 배지와 함께 그 범위가 표시됩니다. 지정하지 않으면 `Board` 배지와 함께 데이터 전체 범위가 흐리게 표시되고, 패널은 대시보드의 거리 범위를 따릅니다.
- **슬라이더 · FROM / TO** : 범위를 정합니다. `first`, `last-1000` 같은 앵커 표현식도 쓸 수 있습니다.
- **Quick windows** : First 10%, First 25%, First 50%, Last 50%, Last 25%, Full 중에서 골라 한 번에 지정합니다.
- **Clear** : 이 패널만의 범위를 지우고 다시 대시보드 범위를 따르게 합니다. 패널 범위가 있을 때만 누를 수 있습니다.

패널 범위를 지정한 패널은 대시보드의 거리 범위를 바꾸거나 `Reset to default`로 초기화해도 자기 범위를 그대로 사용합니다.
