---
title: Tag Analyzer
type: docs
weight: 26
toc: true
---

Tag Analyzer는 태그 테이블의 시계열 데이터를 대화형으로 탐색하는 Machbase Neo 도구입니다.

다음과 같은 작업에 사용할 수 있습니다:

- 여러 태그의 차트 만들기
- 시간 범위 조절 및 동기화
- 차트 겹치기로 데이터 비교
- 원시 값 확인
- FFT로 주파수 분석
- 차트와 설정을 보드로 저장하고 나중에 다시 열기

<span id="1-quickstart"></span>

## 1. 개요 {#overview}

Tag Analyzer 사용 데모 영상입니다. 차트를 만들고, 데이터를 분석하고, 보드를 저장하는 과정을 보여줍니다.

{{< tag-analyzer-overview >}}

### 1.1 Tag Analyzer 탭 열기 {#create-tag-analyzer-tab}

**+**를 클릭한 뒤 **TAG ANALYZER**를 선택해 새 보드를 여세요.

### 1.2 예제 데이터 추가 (선택 사항) {#예제-데이터-준비}

예제 데이터로 Tag Analyzer를 사용해 보세요. 이미 데이터가 있다면 이 섹션을 건너뛰세요.

1. 새 탭 메뉴에서 **SQL**을 선택하고 아래 SQL 예제를 실행해 테이블을 만드세요.
2. 다른 탭에서 **TQL**을 선택하고 아래 TQL 예제를 실행해 예제 데이터를 넣으세요.

{{< figure
  src="/images/tag-analyzer/prepare-example-data-editors-kr.png?v=7751b45119"
  link="/images/tag-analyzer/prepare-example-data-editors-kr.png?v=7751b45119"
  alt="+ 버튼으로 새 탭을 연 뒤 SQL에서 예제 테이블을 만들고 TQL에서 예제 데이터를 추가하는 위치."
  caption="그림 1.2: SQL 및 TQL 편집기"
>}}

**예제 테이블 만들기 (SQL 탭에서 한 번 실행)**

```sql
CREATE TAG TABLE IF NOT EXISTS TAG_ANALYZER_DEMO (
    NAME VARCHAR(80) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

**예제 테이블에 데이터 추가하기 (TQL 편집기에서 실행)**

```js
FAKE(oscillator(
    freq(1/60, 10, 20),
    range('now-10m', '10m', '1s')
))
PUSHVALUE(0, 'temperature')
APPEND(table('TAG_ANALYZER_DEMO'))
```

### 1.3 첫 차트 만들기 {#tag-analyzer-만들기}

Tag Analyzer 탭에서 **New Chart**를 클릭해 차트 생성 대화상자를 여세요.
자신의 테이블과 태그를 사용하거나 아래 예제 설정을 따라 하세요.

1. **Chart name**에 `Temperature`를 입력하고 **Line**을 선택하세요.
2. 예제 데이터를 만든 **Database**와 **User**를 선택한 뒤, **Table**은 **TAG_ANALYZER_DEMO**,
   **Time**은 **TIME**, **Value**는 **VALUE**를 선택하세요.
3. **Enter** 또는 검색 버튼으로 `temperature`를 검색하고 **Item list**에서 클릭하세요.
   **Selected**에 추가되면 **AVG**를 유지하세요.
4. **Apply**를 클릭해 차트를 만드세요.

{{< figure
  src="/images/tag-analyzer/create-tag-analyzer-chart-kr.png?v=96111f013c"
  link="/images/tag-analyzer/create-tag-analyzer-chart-kr.png?v=96111f013c"
  alt="전체 Machbase Neo 화면과 New Chart 대화상자. 1. 이름을 입력하고 Line을 선택하세요. 2. 테이블, TIME, VALUE를 선택하세요. 3. temperature를 검색하고 선택하세요. 4. Apply를 클릭해 차트를 만드세요."
  caption="그림 1.3: 첫 차트 만들기"
>}}

### 1.4 화면 구성 {#화면-구성}

차트가 준비되었습니다. Tag Analyzer로 데이터를 탐색하고 분석해 보세요.

아래 이미지는 Tag Analyzer의 화면 구성을 보여줍니다.

{{< figure
  src="/images/web-ui/tag-analyzer/controls-overview.png?v=c287c40a80"
  alt="temperature 예제의 보드 컨트롤, 패널 컨트롤, 범위, 도구와 패널 편집기 위치"
  caption="그림 1.4: 화면 구성"
>}}

## 2. 보드 컨트롤

맨 위 도구 모음에서 공통 범위, 새로 고침, 저장, 겹쳐 보기를 조작합니다.

{{< figure
  src="/images/web-ui/tag-analyzer/board-controls.png"
  alt="범위, 새로 고침, 저장, 겹쳐 보기와 도움말을 보라색으로 표시한 보드 도구 모음"
  caption="그림 2: 보드 컨트롤"
>}}

### 2.1 새 차트 추가 {#새-차트-추가}

**New Chart**를 클릭해 현재 보드에 차트를 추가합니다.

{{< tag-analyzer-features
  id="add-chart"
  title="보드에서 새 차트 만들기"
  caption="그림 2.1: 새 차트 추가"
>}}

### 2.2 보드 범위 설정 {#공통-범위-설정}

**TIME**을 클릭해 모든 시간 기반 차트의 공통 내비게이터 범위를 설정하거나,
**DIST**를 클릭해 모든 거리 기반 차트의 공통 내비게이터 범위를 설정합니다.
둘 다 **From/To**를 사용합니다.

*패널에 따로 설정한 범위가 우선합니다.*

| X축 | From → To (예제) | 의미 |
|---|---|---|
| 시간 | `first` → `last` | 생성한 예제 데이터 전체. |
| 시간 | `last-5m` → `last` | 예제 데이터의 마지막 5분. |
| 시간 | `first` → `first+5m` | 예제 데이터의 첫 5분. |

날짜와 시간을 직접 입력하거나 빠른 범위를 선택할 수도 있습니다.
숫자 범위에서는 슬라이더와 빠른 구간 선택을 사용할 수 있습니다.


### 2.3 새로 고침 {#새로-고침과-전체-데이터-보기}

- **Refresh data:** 각 패널의 현재 범위를 유지하며 데이터를 다시 조회합니다.
- **Refresh ranges:** 데이터 범위를 다시 확인하고 설정된 범위를 재적용합니다.
  `last-5m`와 같은 상대 범위도 다시 계산합니다.
- **Expand all panels to full data range:** 모든 패널에서 사용 가능한 전체 데이터를 봅니다.

설정된 범위가 없으면 범위 새로 고침은 중앙 구간을 표시합니다. 전체를 보려면 전체 범위 버튼을 사용합니다.

### 2.4 저장하고 다시 열기 {#변경-사항-저장-또는-사본-만들기}

**Save**는 현재 `.taz` 파일에 저장하고, **Save as**는 다른 이름이나 폴더를 선택합니다.
**Ctrl+S**(macOS는 **Cmd+S**)로도 저장할 수 있습니다. 편집 중인 변경 사항은 먼저 적용합니다.

`.taz` 파일에는 차트 설정, 범위, 하이라이트, 주석이 저장됩니다. 테이블 데이터는 복사하지 않습니다.

<span id="저장하고-다시-열기"></span>

보드 탭을 닫은 뒤 File Explorer에서 저장한 파일을 클릭하면 보드가 다시 열립니다.

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/save-reopen-kr.mp4?v=304f5cf981"
  poster="/images/web-ui/tag-analyzer/save-reopen-kr-poster.webp?v=a7c7cfadc9"
  alt="Tag Analyzer 보드 저장하고 다시 열기"
  caption="데모 2.4: 저장하고 다시 열기"
>}}

### 2.5 차트 겹쳐 보기 {#차트-겹쳐-비교하기}

차트 겹쳐 보기는 여러 차트를 한 화면에 겹쳐 표시하여 데이터 패턴을 비교할 수 있게 합니다.
각 차트를 X축 방향으로 이동해 서로 다른 시점의 봉우리나 이벤트를 맞출 수 있습니다.여러 시리즈가 있는 차트도 사용할 수 있습니다. 

{{< overlap-chart >}}

### 2.6 TAZ 파일 삭제 {#taz-파일-삭제}

**File Explorer**에서 `.taz` 파일을 우클릭하고 **Delete**를 선택한 뒤 확인합니다.
저장된 보드가 삭제되며 테이블 데이터는 유지됩니다.

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/delete-taz-kr.mp4?v=a20e0c59af"
  poster="/images/web-ui/tag-analyzer/delete-taz-kr-poster.webp?v=b33a88b8e2"
  alt="File Explorer에서 TAZ 파일 삭제하기"
  caption="데모 2.6: TAZ 파일 삭제"
>}}

## 3. 패널 컨트롤 {#3-패널-컨트롤}

### 3.1 범위 {#범위와-탐색}

<span id="기본-범위-조절"></span>

차트 위 범위에서 **From/To**를 설정하고 **Apply**를 클릭합니다. 내비게이터를 드래그하거나 확대·축소해 범위를 조절합니다.
위에서 만든 예제 데이터는 `last-10m`부터 `last`까지로 설정합니다.

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/basic-range-control-kr.mp4?v=3c67039c20"
  poster="/images/web-ui/tag-analyzer/basic-range-control-kr-poster.webp?v=81b60c0d09"
  alt="범위 설정, 내비게이터 이동과 확대"
  caption="데모 3.1: 기본 범위 조절"
>}}

{{< range-controls >}}

<details>
<summary>설정된 범위</summary>

[패널 편집기 → Range](#main-range)의 **Main Range (1)**는 표시 범위에 우선 적용됩니다.
별도로 설정한 **Nav Range (2)**는 보드 범위보다 우선합니다.

</details>

### 3.2 도구 {#panel-control-tools}

도구 모음의 왼쪽부터 순서대로 설명합니다.

{{< figure
  src="/images/web-ui/tag-analyzer/panel-controls.png"
  alt="왼쪽부터 RAW, Select range, Refresh range, Panel Editor, Delete, Extra 순서의 패널 도구"
  caption="그림 3.2: 도구"
>}}

#### 3.2.1 RAW {#raw-데이터-보기}

**RAW**를 클릭하면 구간별 집계 데이터와 개별 원본 행 사이를 전환합니다.
집계 모드에서는 시리즈별 **AVG**, **MIN**, **MAX** 등의 집계 방식을 사용합니다.

<details>
<summary>RAW 조회 제한과 샘플링</summary>

메인 차트 샘플링을 사용하지 않으면 RAW 조회는 **시리즈당 최대 20,000행**을 반환합니다.
제한에 도달하면 반환된 데이터에 맞춰 표시 범위가 줄어들 수 있습니다.
범위를 좁히거나 **Data Setting → Use main chart sampling**을 사용합니다.

메인 차트가 RAW 모드여도 내비게이터에는 평균값이나 샘플링된 데이터가 표시될 수 있습니다.

</details>

#### 3.2.2 Select Range와 FFT {#통계-확인}

선택 구간의 통계를 확인하거나 FFT로 주파수를 분석합니다.
FFT는 **RAW 모드의 시간축 차트**에서 사용할 수 있습니다.

<span id="fft로-주파수-분석"></span>

{{< fft-demo >}}

`temperature`의 **Min Hz**를 **0.005**, **Max Hz**를 **0.1**로 설정하고 **Apply values**를 클릭합니다.
예제의 주된 주파수는 약 **0.0167 Hz**입니다.

이 예제의 **3D** 구간은 **1 min**으로 설정합니다. 구간마다 최소 **16개 샘플**이 필요합니다.

#### 3.2.3 Refresh Range {#이-패널-새로-고침}

데이터 범위를 다시 확인하고 설정된 범위를 재적용합니다.

#### 3.2.4 차트 수정 {#panel-editor-tool}

<span id="차트-수정"></span>

톱니바퀴 버튼으로 설정을 수정합니다. **Apply**는 변경 사항을 적용하고, **Close**는 편집기를 닫습니다.

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/edit-chart-kr.mp4?v=d13b47d4c3"
  poster="/images/web-ui/tag-analyzer/edit-chart-kr-poster.webp?v=3293acd718"
  alt="차트 제목과 모양 변경하기"
  caption="데모 3.2.4: 차트 수정"
>}}

설정 탭은 [패널 편집기](#4-패널-설정)를 참고합니다.

#### 3.2.5 차트 삭제 {#delete-panel-tool}

<span id="차트-삭제"></span>

**Delete panel**(휴지통 버튼)을 클릭하고 확인합니다.

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/delete-chart-kr.mp4?v=adf54d76fe"
  poster="/images/web-ui/tag-analyzer/delete-chart-kr-poster.webp?v=5f2933c6ce"
  alt="보드에서 차트 삭제하기"
  caption="데모 3.2.5: 차트 삭제"
>}}

차트는 `.taz` 보드의 항목 하나입니다. 차트를 삭제해도 `.taz` 파일과 테이블 데이터는 유지됩니다.

#### 3.2.6 하이라이트 {#highlight}

<span id="하이라이트와-주석-추가"></span>

**Extra → Highlight**로 차트의 구간을 강조하고 이름을 붙입니다.

{{< markup-guide id="highlight" >}}

#### 3.2.7 주석 {#annotation}

**Extra → Annotation**으로 시리즈의 특정 지점에 메모를 붙입니다.

{{< markup-guide id="annotation" >}}

하이라이트와 주석을 유지하려면 보드를 저장합니다.

#### 3.2.8 Extra {#extra-panel-tools}

{{< figure
  src="/images/web-ui/tag-analyzer/panel-extra-tools.png"
  alt="Extra 메뉴"
  caption="그림 3.2.8: Extra"
>}}

- **Set global range:** 이 패널의 범위를 X축 유형이 같은 다른 패널에 복사합니다.
- **Reload data:** 현재 범위를 유지하며 데이터를 다시 조회합니다.
- **Expand to full data range:** 이 패널의 전체 데이터를 봅니다.

<span id="편리한-도구"></span>

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/handy-tools-kr.mp4?v=a549ea9065"
  poster="/images/web-ui/tag-analyzer/handy-tools-kr-poster.webp?v=8cd2b60ab5"
  alt="temperature 데이터를 새로 고치고 전체 범위를 표시하는 과정"
  caption="데모 3.2.8: 새로 고침과 전체 범위"
>}}

## 4. 패널 편집기 {#4-패널-설정}

차트의 톱니바퀴 버튼을 클릭합니다. **Apply**는 변경 사항을 적용하고, **Close**는 편집기를 닫습니다.

**변경 사항을 적용한 뒤 `.taz` 보드를 저장해야 다음에도 유지됩니다.**

### 4.1 General 탭 {#general}

{{< panel-editor-tab id="general" caption="그림 4.1: General 탭" >}}

### 4.2 Data 탭 {#data}

{{< panel-editor-tab id="data" caption="그림 4.2: Data 탭" >}}

### 4.3 Data Setting 탭 {#data-setting}

{{< panel-editor-tab id="data-setting" caption="그림 4.3: Data Setting 탭" >}}

### 4.4 Axes 탭 {#axes}

{{< panel-editor-tab id="axes" caption="그림 4.4: Axes 탭" >}}

### 4.5 Display 탭 {#display}

{{< panel-editor-tab id="display" caption="그림 4.5: Display 탭" >}}

### 4.6 Range 탭 {#main-range}

{{< panel-editor-tab id="main-range" caption="그림 4.6: Range 탭" >}}
