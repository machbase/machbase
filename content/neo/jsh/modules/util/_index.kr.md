---
title: "util"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`util` 모듈 그룹은 JSH 애플리케이션과 내장 명령에서 자주 쓰는 작은 helper API를 제공합니다.

현재 모듈 그룹은 다음 하위 모듈로 구성됩니다.

- `util/parseArgs`: 명령행 스타일 인자 파서
- `util/splitFields`: 따옴표를 인식하는 shell 스타일 필드 분리기

각 helper는 해당 모듈 경로로 직접 불러와 사용합니다.

```js
const parseArgs = require('util/parseArgs');
const splitFields = require('util/splitFields');
```

옵션, positional, sub-command, help text 생성까지 함께 처리해야 하면 `parseArgs`를 사용하십시오.
공백 기준으로 문자열을 나누되, 따옴표로 감싼 부분은 하나의 필드로 유지해야 하면 `splitFields`를 사용하십시오.

{{< children_toc />}}