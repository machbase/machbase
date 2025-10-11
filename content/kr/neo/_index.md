---
title: machbase-neo
weight: 10
toc: true
---

✓ 고성능 시계열 데이터베이스입니다.<br/>
✓ Raspberry Pi부터 하이엔드 서버까지 확장할 수 있습니다.<br/>
✓ 데이터 변환과 시각화를 제공합니다.<br/>
✓ 대시보드로 데이터를 모니터링할 수 있습니다.<br/>
✓ 즉시 다운로드하여 실행할 수 있어 설치가 간편합니다.<br/>
✓ 테이블과 컬럼을 사용하는 익숙한 SQL로 쉽게 학습하실 수 있습니다.<br/>
✓ **HTTP**, **MQTT**, **gRPC**를 통해 손쉽게 데이터를 적재하고 조회하실 수 있습니다.<br/>
✓ SQLite, PostgreSQL, MySQL, MSSQL, MQTT 브로커, NATS와 연동할 수 있습니다.<br/>

{{< button color="purple" href="./getting-started/">}} 바로 시작하기 {{< /button >}}
{{< button color="green" href="./releases/">}} 다운로드 {{< /button >}}
{{< label color="green" >}} 최신 버전 <i>{{< neo_latestver >}}</i> {{< /label>}}

Machbase는 IoT 애플리케이션에 최적화된 고성능 시계열 데이터베이스이며 C 언어로 구현되었습니다.
`machbase-neo`는 Machbase 엔진을 통합한 IoT 데이터베이스 서버로,
IoT 플랫폼 구축에 필요한 필수 기능과 사용하기 쉬운 도구를 함께 제공합니다.
MQTT를 통해 IoT 센서에서 직접 데이터를 수집하고,
애플리케이션이 HTTP 기반 SQL로 데이터를 조회할 수 있도록 여러 프로토콜을 지원합니다.
Raspberry Pi부터 고성능 서버까지 폭넓은 환경에 설치하여 사용할 수 있을 만큼 유연합니다.

### 다운로드

{{< tabs items="Linux/macOS,Windows,Choose Manually">}}
    {{< tab >}}
    아래 스크립트를 쉘 프롬프트에 붙여 넣으면 최신 버전을 설치하실 수 있습니다.

    ```bash
    sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
    ```
    {{< /tab >}}

    {{< tab >}}
    명령줄보다 GUI를 선호하신다면 Windows 배포판에 포함된 `neow`를 실행해 주십시오.

    [Windows]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip)용 최신 릴리스를 다운로드하십시오.

    ![interfaces](/images/neow-win.png)
    {{< /tab >}}

    {{< tab >}}
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

- [x] HTTP : 애플리케이션과 센서가 [HTTP](/neo/api-http) REST API로 데이터를 읽고 쓸 수 있습니다.
- [x] MQTT : 센서가 [MQTT](/neo/api-mqtt) 프로토콜(MQTT v3.1.1 & v5)로 데이터를 전송할 수 있습니다.
- [x] gRPC : 확장을 위한 1급 API를 제공합니다.
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
