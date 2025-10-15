---
type: docs
title : '패키지 개요'
type : docs
weight: 10
---

## 패키지 유형

MACHBASE는 수동 설치 및 패키지 설치 파일을 제공합니다.

|설치 유형|설명|비고|
|--|--|--|
|수동 설치|Unix용 압축 파일 형식이며 확장자는 tgz입니다.<br>사용자가 tar 및 GNU gzip을 사용하여 압축을 해제하여 설치를 진행합니다.|콘솔 환경에서만 설치 가능|
|패키지 설치|각 운영 체제 환경에 대한 설치 패키지를 제공합니다.<br> - Windows: msi <br> -  Linux: tgz|콘솔 환경에서만 설치 가능|

## 패키지 파일 이름 구조

패키지 파일 이름은 다음과 같이 구성됩니다.

```
machbase-EDITION_VERSION-OS-CPU-BIT-MODE-OPTIONAL.EXT
```

|항목|설명|
|--|--|
|EDITION|패키지의 에디션을 나타냅니다.<br> - standard: Standard Edition<br> - cluster: Cluster Edition|
|VERSION|패키지의 버전을 나타냅니다.<br>자세히는 _MajorVersion.MinorVersion.FixVersion.AUX_로 숫자와 문자로 분류됩니다.<br>- Major Version: 제품 주요 버전 - 숫자<br>- Minior Version: 동일한 주요 버전에서 비교적 큰 기능이 추가된 버전. DB 파일 / 프로토콜 호환성이 보장되지 않습니다. -숫자<br>- Fix Version: 동일한 주요 버전에서 버그 / 작은 기능이 추가된 버전. DB 파일 / 프로토콜 호환성이 보장됩니다. - 숫자<br>- AUX: 패키지 분류를 나타냅니다 -숫자<br> -- official: 일반 패키지<br> -- community: 커뮤니티 에디션 패키지|
|OS|운영 체제 이름을 나타냅니다. (예) LINUX, WINDOWS|
|CPU|운영 체제에 설치된 CPU 유형을 나타냅니다. (예) X86, IA64|
|BIT|컴파일된 바이너리가 32비트인지 64비트인지를 나타냅니다. (예) 32, 64|
|MODE|컴파일된 바이너리의 릴리스 모드를 나타냅니다. (예) release, debug, prerelease|
|OPTIONAL|Enterprise Edition에서만 표시됩니다.<br>lightweight: Coordinator에 추가할 경량 패키지를 나타냅니다.|
|EXT|패키지 파일 확장자입니다. 패키지에 따라 tgz, rpm, deb 및 msi로 사용할 수 있습니다.|
