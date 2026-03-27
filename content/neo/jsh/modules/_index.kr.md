---
title: 모듈
type: docs
weight: 900
toc: true
---

JSH 모듈은 Machbase Neo에 기본 포함된 표준 라이브러리입니다.
이 모듈들은 TQL의 `SCRIPT()` 블록과 독립적인 `*.js` 애플리케이션에서 모두 사용할 수 있으며,
별도의 패키지 설치 없이 `require()`로 바로 불러올 수 있습니다.

모듈 이름은 `fs`, `os`, `net`처럼 짧은 이름을 쓰기도 하고,
`archive/tar`처럼 그룹 경로 형태를 쓰기도 합니다.

## 모듈 불러오기

필요한 모듈 이름을 `require()`에 전달해 로드합니다.

```js
const fs = require('fs');
const os = require('os');

console.println('cwd entries:', fs.readDir('.').length);
console.println('platform:', os.platform(), os.arch());
```

JSH 모듈은 런타임에 기본 포함되어 있으므로 파일 처리, 네트워크, 시스템 정보,
데이터 포매팅, 데이터베이스 접근과 같은 기능을 표준 라이브러리처럼 바로 사용할 수 있습니다.

각 모듈의 API와 상세 예제는 아래 문서를 참고하십시오.

{{< children_toc />}}
