---
title: 릴리스
type: docs
weight: 10
toc: false
---


### 최신 버전 {{< neo_latestver >}}

사용 중인 플랫폼에 맞는 최신 패키지를 선택해 주십시오.

| OS         | 아키텍처       |  다운로드 |
|:-----------|:---------------|:----------|
| Linux      | arm64          | [machbase-neo-{{< neo_latestver >}}-linux-arm64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm64.zip)   |
| Linux      | x64            | [machbase-neo-{{< neo_latestver >}}-linux-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-amd64.zip)   |
| Linux      | arm32          | [machbase-neo-{{< neo_latestver >}}-linux-arm32.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm32.zip)   |
| macOS      | arm64          | [machbase-neo-{{< neo_latestver >}}-darwin-arm64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-arm64.zip) |
| macOS      | x64            | [machbase-neo-{{< neo_latestver >}}-darwin-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-amd64.zip) |
| Windows    | x64     | [machbase-neo-{{< neo_latestver >}}-windows-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip) |

### 기타 Linux 배포판

미리 제공되는 패키지가 사용 중인 배포판과 호환되지 않는 경우, 소스 코드를 직접 빌드할 수 있습니다.

1. Go 1.24와 gcc가 설치되어 있는지 확인합니다.
2. [GitHub](https://github.com/machbase/neo-server)에서 `neo-server` 저장소를 클론합니다.
3. `go run mage.go install-neo-web`을 실행해 Machbase Neo 웹 UI를 내려받습니다.
4. `go run mage.go machbase-neo`를 실행해 Machbase Neo를 빌드합니다.
5. 빌드된 실행 파일은 `./tmp/machbase-neo` 경로에 생성됩니다.
6. 원하는 설치 경로에 실행 파일을 복사합니다.

### 변경 사항 {{< neo_latestver >}}

자세한 변경 내역은 [Changes](https://github.com/machbase/neo-server/releases/tag/{{< neo_latestver >}})에서 확인할 수 있습니다.

### v8.0.x에서 업그레이드하기

업그레이드는 실행 파일을 교체하는 간단한 절차만으로 완료됩니다.

1. 실행 중인 machbase-neo 프로세스를 종료합니다.
2. `machbase-neo`(또는 Windows의 경우 `machbase-neo.exe`) 실행 파일을 새로운 파일로 교체합니다.
3. machbase-neo 프로세스를 다시 시작합니다.

### 이전 버전

과거 버전은 [GitHub 릴리스 페이지](https://github.com/machbase/neo-server/releases)에서 내려받을 수 있습니다.

{{< callout type="warning" emoji="⚠️">}}
과거 **v1.5.0**까지 제공되었던 **Edge / Fog 에디션**은 v1.5.0 이후 단일 “Standard” 에디션으로 통합되었습니다.<br/>
Raspberry Pi와 같은 소형 기기에서 구버전을 실행해야 한다면 Edge 에디션을 선택하십시오.<br/>
워크스테이션이나 서버처럼 메모리와 CPU 코어가 충분한 환경에서는 Fog 에디션을 사용하면 됩니다.
{{< /callout >}}

### CLASSIC SDK

아래 패키지는 레거시 MACHBASE DBMS와 JDBC, ODBC, C 클라이언트 라이브러리 등 애플리케이션 드라이버를 포함합니다.

| OS         | 아키텍처       |  다운로드 |
|:-----------|:---------------|:----------|
| Linux      | x64            | [machbase-SDK-8.0.39.official-LINUX-X86-64-release.tgz](https://github.com/machbase/packages/releases/download/8.0.39/machbase-SDK-8.0.39.official-LINUX-X86-64-release.tgz) |
| Linux      | arm64          | [machbase-SDK-8.0.31.official-LINUX-ARM_CORTEX_A53-64-release.tgz](https://github.com/machbase/packages/releases/download/8.0.31/machbase-SDK-8.0.31.official-LINUX-ARM_CORTEX_A53-64-release.tgz) |
| Windows    | x64            | [machbase-SDK-8.0.32.official-WINDOWS-X86-64-release.msi](https://github.com/machbase/packages/releases/download/8.0.32/machbase-SDK-8.0.32.official-WINDOWS-X86-64-release.msi)
| Windows    | x86            | [machbase-SDK-8.0.23.official-WINDOWS-X86-32-release.msi](https://github.com/machbase/packages/releases/download/8.0.23/machbase-SDK-8.0.23.official-WINDOWS-X86-32-release.msi) |
| macOS      | arm64          | [machbase-SDK-8.0.2.official-DARWIN-ARM_M1-64-release.tgz](https://github.com/machbase/packages/releases/download/8.0.2/machbase-SDK-8.0.2.official-DARWIN-ARM_M1-64-release.tgz) |
| macOS      | x64            | [machbase-SDK-8.0.2.official-DARWIN-X86-64-release.tgz](https://github.com/machbase/packages/releases/download/8.0.2/machbase-SDK-8.0.2.official-DARWIN-X86-64-release.tgz) |
