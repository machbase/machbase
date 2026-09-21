---
title: 대시보드 조작
type: docs
weight: 10
---

## 화면 구성

{{< media slug="neo-dashboard/statz-board" width="600" >}}

대시보드는 실제 데이터를 보여주는 여러 차트로 이루어져 있으며, 각 패널은 사용자가 원하는 위치와 크기로 배치할 수 있습니다.

- 상단 왼쪽: 대시보드 제목. 클릭해서 바로 수정할 수 있습니다.
- 상단 오른쪽: 대시보드 전체를 제어하는 컨트롤 영역
- 가운데: 차트 패널이 배치되는 영역

## 차트 추가

컨트롤 영역의 <img src="/images/web-ui/neo-dashboard/icons/dash_new_panel.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘을 클릭하면 차트 설정 화면이 열립니다. 설정을 마치고 `Save`를 누르면 대시보드에 패널이 추가됩니다.  
※ 자세한 내용은 “차트 설정”을 참고하십시오.

{{< media slug="neo-dashboard/add-chart" width="600" >}}

패널이 하나도 없는 새 대시보드에서는 화면 가운데의 <img src="/images/web-ui/neo-dashboard/icons/dash_create_panel.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘을 눌러도 같은 화면이 열립니다.  
새로 추가된 차트는 기본 크기로 배치되며, 패널 우측 하단을 드래그해 크기를 조정하고 패널 상단을 드래그해 위치를 변경할 수 있습니다. 저장된 패널보다 작게 줄일 수는 없습니다.

## 제어 버튼

{{< media slug="neo-dashboard/control-buttons" width="600" >}}

※ 저장되지 않은 새 대시보드에는 아래 8개 버튼이 표시됩니다. 대시보드를 저장하면 보기 모드 링크를 공유하는 버튼이 추가로 나타나고, 변수를 정의하면 제목 옆에 변수 값과 변수 아이콘이 나타납니다.

1. <img src="/images/web-ui/neo-dashboard/icons/dash_new_panel.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 새 차트를 추가합니다.
2. <img src="/images/web-ui/neo-dashboard/icons/dash_refresh.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 데이터를 다시 로드해 차트를 갱신합니다.
3. `TIME` 칩: 데이터 조회에 사용할 시간 범위를 설정합니다.
4. `DIST` 칩: 거리 기준으로 조회하는 패널의 거리 범위를 설정합니다.
5. <img src="/images/web-ui/neo-dashboard/icons/dash_auto_refresh.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 자동 새로 고침 간격을 설정합니다.
6. <img src="/images/web-ui/neo-dashboard/icons/dash_save.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 현재 대시보드를 저장합니다. (파일 확장자 `.dsh`) 새 대시보드는 파일명과 저장 폴더를 지정할 수 있습니다.
7. <img src="/images/web-ui/neo-dashboard/icons/dash_save_as.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 다른 이름으로 저장합니다.
8. <img src="/images/web-ui/neo-dashboard/icons/dash_variable_config.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 변수를 설정합니다. {{< neo_since ver="8.0.46" />}}

## 시간 범위 (TIME)

칩을 클릭하면 범위 설정 창이 열립니다.

{{< media slug="neo-dashboard/board-time-range" width="420" >}}

- `now`는 현재 시각, `last`는 데이터베이스에 저장된 마지막 시각을 뜻합니다. `h`/`m`/`s`는 시·분·초이며, 예를 들어 `now-3h`는 현재 시각에서 3시간 전입니다.
- “Quick Range” 항목을 클릭하면 From/To가 자동으로 설정됩니다. 오른쪽 목록(`... of data`)은 데이터의 마지막 시각을 기준으로 합니다.
- 칩 좌우의 `<`, `>` 버튼은 선택한 범위를 50%씩 이동합니다. `now`나 `last`를 사용 중이면 절대 시간으로 변환됩니다.

## 거리 범위 (Distance)

시간 대신 거리(구간)를 기준으로 조회하는 패널에 적용됩니다. 같은 창의 Distance 탭에서 설정합니다.

{{< media slug="neo-dashboard/board-dist-range" width="420" >}}

- **적용 대상** : 기준 컬럼이 DATETIME이 아닌 숫자(거리·주행거리 등)인 태그 테이블을 쓰는 패널입니다. 이런 테이블은 기준 컬럼을 `BASE DISTANCE`로 선언해 만듭니다. (예: `CREATE TAG TABLE dist_data (NAME VARCHAR(80) PRIMARY KEY, DIST DOUBLE BASE DISTANCE, VALUE DOUBLE SUMMARIZED)`) 대시보드에 그런 패널이 없으면 데이터 범위를 알 수 없어 `0 – 0`으로 표시됩니다.
- **데이터 범위(min/max)** : 창을 열면 패널 데이터의 최솟값·최댓값을 불러와 슬라이더의 양 끝으로 사용합니다. 슬라이더를 끌거나 FROM/TO 입력칸에 값을 넣어 범위를 정하면, 창 위쪽에 선택한 범위(예: `0 – 1,237.5`)와 그 길이가 표시됩니다.
- **앵커 표현식** : 숫자 대신 `first`, `last`, `first+1000`, `last-1000`처럼 데이터 끝을 기준으로 입력할 수 있습니다. 시간 축의 `last-1h ~ last`처럼 데이터가 늘어나도 범위가 데이터 끝을 따라갑니다. 적용하면 칩에도 `last-1000 ~ last`처럼 표현식이 그대로 표시됩니다.
- **Quick windows** : First 10%, First 25%, First 50%, Last 50%, Last 25%, Full 중에서 골라 데이터 범위의 비율로 한 번에 지정합니다. 누르면 FROM/TO가 앵커 표현식으로 채워집니다. (예: 데이터 범위가 0~4,950일 때 First 25%는 `first` ~ `first+1237.5`)
- **`Reset to default`** : 누르는 즉시(Apply 없이) 대시보드의 거리 범위를 지우고 창을 닫습니다. 칩은 점선으로 표시된 빈 칩으로 돌아가고, 패널은 데이터 전체 범위를 표시합니다. 차트 설정의 Distance 탭에서 자체 범위를 지정한 패널은 그 범위를 계속 사용합니다.

## 자동 새로 고침

{{< media slug="neo-dashboard/board-autorefresh" width="600" >}}

Off, 3초, 5초, 10초, 30초, 1분, 5분, 10분, 1시간 중에서 선택합니다. 설정하면 지정한 주기마다 대시보드 전체가 다시 조회됩니다. 패널 단위로 다른 주기를 쓰려면 “차트 패널”의 패널별 자동 새로 고침을 참고하십시오.

## 공유

{{< media slug="neo-dashboard/share" width="600" >}}

공유 버튼은 저장된 대시보드에서만 나타납니다. 버튼을 누르면 Share 창이 열립니다.

{{< media slug="neo-dashboard/share-modal" width="600" >}}

- **SNS 버튼** : Facebook, X, 이메일, WhatsApp으로 링크를 보냅니다.
- **링크** : 보기 전용 모드 주소입니다. 형식은 `http://<서버 주소>/web/ui/board/<폴더 경로>/<파일 이름(확장자 제외)>`이며, 오른쪽 버튼으로 복사합니다.
- **iframe / embed** : 다른 웹 페이지에 끼워 넣는 코드입니다. 탭을 고른 뒤 오른쪽 버튼으로 복사합니다.

보기 전용 모드로 접근하려면 로그인이 필요합니다. 패널은 편집할 수 없고, 시간 범위(TIME)·거리 범위(Distance)와 자동 새로 고침 변경, 새로 고침만 가능합니다.

## 변수

{{< neo_since ver="8.0.46" />}}

{{< media slug="neo-dashboard/board-variable-config" width="600" >}}

대시보드에서 사용하는 변수를 조회·추가·수정·삭제할 수 있습니다. `Export`, `Import`로 변수 설정을 내보내거나 가져올 수 있으며, 형식은 `LABEL,VARIABLE NAME,VALUES` 입니다.

[+ New variable]를 누르면 변수를 정의합니다.

{{< media slug="neo-dashboard/variable-new" width="600" >}}

- **Label** : 변수 입력 필드에 표시할 제목
- **Variable Name** : 차트 설정에서 사용할 변수 이름. 중괄호 없이 `tag`처럼 입력해도 `{{tag}}` 형식으로 저장되며, 차트 설정에서는 `{{tag}}`로 사용합니다.
- **Value** : 변수 입력 필드에서 고를 수 있는 항목. 오른쪽 <img src="/images/web-ui/neo-dashboard/icons/dash_variable_add_value.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 아이콘으로 항목을 추가합니다.

변수를 정의하면 대시보드 제목 옆에 변수의 현재 값이 표시됩니다. 값을 클릭하면 왼쪽에 변수 창이 열리고, 다른 값을 고른 뒤 `Apply`를 눌러야 차트에 반영됩니다. 제목 옆 아이콘을 누르면 모든 변수를 한 번에 볼 수 있습니다.

{{< media slug="neo-dashboard/variables" width="600" >}}
