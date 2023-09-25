---
title : "패키지 개요"
type : docs
weight: 10

---

## 패키지 종류

MACHBASE 는 매뉴얼 설치, 패키지 설치 파일을 제공한다.

|설치 형태|특징|비고|
|--|--|--|
|매뉴얼 설치| 압축파일 형태를 띄고 있으며, 유닉스의 경우에는 확장자가 tgz 이다.<br>사용자는 tar 및 GNU gzip 을 이용하여 압축을 풀어서 설치를 진행해야 한다.| 콘솔 환경에서만 설치 가능|
|패키지 설치|각 운영체제 환경에 맞는 설치 패키지를 제공한다.<br> - Windows: msi <br> -  Linux: tgz| 콘솔 환경에서 설치 가능|

## 패키지 파일명 구조

패키지 파일명은 다음과 같이 구성된다.

```
_machbase-EDITION_VERSION-OS-CPU-BIT-MODE-OPTIONAL.EXT_
```

|항목|설명|
|--|--|
|EDITION| 패키지의 에디션을 나타낸다.<br> - standard: Standard Edition<br> - cluster: Cluster Edition|
|VERSION| 버전을 나태낸다.<br>세부적으로는 _MajorVersion.MinorVersion.FixVersion.AUX_ 로 숫자 및 문자로 구분된다.<br>- Major Version: 제품 메인버전<br>- Minor Version: 같은 메인버전에서 비교적 큰 기능이 추가된 버전. DB 파일/프로토콜 호환을 보장하지 않는다.<br>- Fix Version: 같은 메인 버전에서 버그/사소한 기능이 추가된 버전. DB 파일/프로토콜 호환을 보장한다.<br> - AUX: 패키지의 구분을 나타낸다.<br>-- official: 일반 패키지<br> -- community: 커뮤니티 에디션 용 패키지<br> -- develop: 내부 개발자용 패키지(비공개)|
|OS| 운영채제 명을 나타낸다. (예: LINUX, WINDOWS)|
|CPU| 해당 운영체제에 설치된 CPU 의 타입을 나타낸다. (예: X86, IA64)|
|BIT| 컴파일된 바이너리가 32비트 혹은 64비트 인지 나타낸다. (예: 32, 64)|
|MODE| 컴파일 시 해당 바이너리의 릴리즈 모드를 나타낸다.<br> (예: release, debug, prerelease)|
|OPTIONAL|lightweight: coordinator 에 추가할 경량화 package 를 나타낸다.|
|EXT| 패키지 파일 확장자이다. 패키지에 따라 tgz, rpm, deb, msi 로 제공된다.|
