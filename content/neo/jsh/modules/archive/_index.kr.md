---
title: "archive"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

archive 모듈 그룹은 JSH 애플리케이션에서 TAR 및 ZIP 아카이브를 다루기 위한 기능을 제공합니다.

두 하위 모듈 모두 다음 기능을 지원합니다.

- 메모리 기반 아카이브 생성 및 해제
- 콜백 스타일 비동기 래퍼
- 스트림 스타일 writer / reader 객체
- `.tar`, `.zip` 파일을 다루는 파일 기반 클래스 API

디렉터리 엔트리 또는 TAR 링크 메타데이터가 필요하면 `archive/tar`를 사용하십시오.
일반적인 ZIP 도구와 바로 호환되는 압축 아카이브가 필요하면 `archive/zip`을 사용하십시오.

{{< children_toc />}}
