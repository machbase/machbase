---
title: 설치
type: docs
weight: 10
---

machbase-neo 설치 과정은 다운로드하고 압축을 풀어 실행 파일을 실행하는 간단한 순서입니다.

{{% steps %}}

### 다운로드

아래 스크립트를 사용해 즉시 다운로드하실 수 있습니다.

```sh
sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
```

또는 [releases](/neo/releases) 페이지에서 사용 중인 플랫폼에 맞는 최신 버전을 내려받은 뒤,
원하는 디렉터리에 압축을 풀어 주십시오.

### 압축 해제

다운로드한 파일의 압축을 해제해 주십시오.

```sh
unzip machbase-neo-{{< neo_latestver >}}-${platform}-${arch}.zip
```

### 실행 파일 확인

```sh
machbase-neo version
```

{{< figure src="../img/server-version.gif" width="600" >}}

{{% /steps %}}
