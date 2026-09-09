---
title: machbase-neo
weight: 10
toc: true
---

✓ 고성능 시계열 데이터베이스를 기반으로 한 Physical AI 시대의 데이터 플랫폼입니다.<br/>
✓ 엣지 디바이스(Raspberry Pi)부터 하이엔드 서버까지 확장할 수 있습니다.<br/>
✓ 물리 세계의 데이터를 수집, 변환, 시각화합니다.<br/>
✓ 대시보드로 현장 데이터를 실시간 모니터링할 수 있습니다.<br/>
✓ 즉시 다운로드하여 실행할 수 있어 설치가 간편합니다.<br/>
✓ 테이블과 컬럼을 사용하는 익숙한 SQL로 쉽게 학습하실 수 있습니다.<br/>
✓ **HTTP**, **MQTT**, SQL을 통해 손쉽게 데이터를 적재하고 조회하실 수 있습니다.<br/>
✓ SQLite, PostgreSQL, MySQL, MSSQL, MQTT 브로커, NATS와 연동할 수 있습니다.<br/>

{{< button color="purple" href="./getting-started/">}} 시작하기 {{< /button >}}
{{< button color="green" href="./releases/">}} 다운로드 {{< /button >}}
{{< label color="green" >}} 최신 버전 <i>{{< neo_latestver >}}</i> {{< /label>}}

`machbase-neo`는 C 언어로 구현된 고성능 Machbase 시계열 데이터베이스 엔진을
기반으로, Physical AI 시대에 필요한 데이터 플랫폼입니다.
로봇, 자율 시스템, 스마트 팩토리, 엣지 디바이스 등 물리 세계에서 발생하는
시계열 데이터를 수집, 저장, 변환, 시각화하고, 애플리케이션과 AI 모델이
학습·추론에 바로 활용할 수 있는 형태로 제공합니다.
MQTT 기반 실시간 수집, HTTP SQL 조회, TQL 변환, 대시보드, 외부 시스템 브리지를
하나로 묶어 현장의 데이터를 AI-ready 데이터셋과 서비스로 연결합니다.
엣지 디바이스부터 고성능 서버까지 폭넓은 환경에 설치하여 사용할 수 있을 만큼 유연합니다.

### 다운로드

{{< tabs >}}
    {{< tab name="Linux/macOS" icon="terminal">}}
    아래 스크립트를 쉘 프롬프트에 붙여 넣으면 최신 버전을 설치하실 수 있습니다.

    ```bash
    sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
    ```
    {{< /tab >}}

    {{< tab name="Windows" icon="desktop-computer">}}
    명령줄보다 GUI를 선호하신다면 Windows 배포판에 포함된 `neow`를 실행해 주십시오.

    [Windows]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip)용 최신 릴리스를 다운로드하십시오.

    ![interfaces](/images/neow-win.png)
    {{< /tab >}}

    {{< tab name="Choose Manually" icon="globe">}}
    [releases](./releases/) 페이지에서 원하는 버전과 플랫폼에 맞는 파일을 찾아 다운로드해 주십시오.
    {{< /tab >}}
{{< /tabs >}}


### 데이터 시각화

데이터 변환과 시각화를 위한 언어인 *TQL*을 기본으로 제공합니다.

{{< figure src="/images/data-visualization.jpg" width="740" >}}

- [TQL](/neo/tql)은 데이터 변환을 위한 DSL입니다.
- [CHART()](/neo/tql/chart/)는 데이터 시각화를 지원합니다.
- [SCRIPT()](/neo/tql/script/)를 사용하여 사용자 정의 로직을 구현하실 수 있습니다.

<span class="badge-new">NEW!</span> 지리 공간 기반 데이터 시각화를 지원합니다.

{{< figure src="/images/map-visualization.jpg" width="600" >}}

- [GEOMAP()](/neo/tql/geomap/)을 이용해 지도를 시각화해 보십시오.

### 대시보드

실시간 데이터를 즉시 모니터링하실 수 있습니다.

{{< figure src="/images/dashboard.png" width="740" >}}

### API 및 인터페이스

- [x] HTTP : 애플리케이션과 엣지 디바이스가 [HTTP](/neo/api-http) REST API로 데이터를 읽고 쓸 수 있습니다.
- [x] MQTT : 로봇·장비·엣지 디바이스가 [MQTT](/neo/api-mqtt) 프로토콜(MQTT v3.1.1 & v5)로 데이터를 전송할 수 있습니다.
- [x] SSH : [ssh](/neo/shell/#remote-access-via-ssh)를 통한 명령줄 사용자 인터페이스를 지원합니다.
- [x] GUI : [Web](/neo/getting-started/webui/) 사용자 인터페이스를 제공합니다.

{{< figure src="/images/interfaces.jpg" width="600" >}}

### 브리지

외부 시스템과 쉽게 연동하실 수 있습니다.

- [x] SQLite
- [x] PostgreSQL
- [x] MySQL
- [x] MS-SQL
- [x] MQTT Broker
- [x] NATS


### 기여

다른 개발자를 위한 문서와 예제를 함께 만들어 주시면 언제든 환영합니다. 오탈자나 끊어진 링크를 발견하시면 편하게 제보해 주십시오.


[^1]: [TPCx-IoT 성능 결과](https://www.tpc.org/tpcx-iot/results/tpcxiot_perf_results5.asp?version=2)
