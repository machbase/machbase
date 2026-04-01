---
title: "semver"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`semver` 모듈은 JSH 애플리케이션에서 시맨틱 버전 비교 기능을 제공합니다.

일반적으로 다음과 같이 사용합니다.

```js
const semver = require('semver');
```

## 내보내는 함수

- `satisfies(version, constraint)`
- `maxSatisfying(versions, constraint)`
- `compare(left, right)`

## satisfies()

버전이 시맨틱 버전 제약 조건을 만족하는지 확인합니다.

<h6>구문</h6>

```js
semver.satisfies(version, constraint)
```

<h6>매개변수</h6>

- `version` `String`
- `constraint` `String`

<h6>반환값</h6>

`version`이 `constraint`를 만족하면 `true`, 아니면 `false`를 반환합니다.

빈 제약 조건과 `latest`는 `*`로 처리됩니다.

## maxSatisfying()

제약 조건을 만족하는 버전 중 가장 높은 버전을 반환합니다.

<h6>구문</h6>

```js
semver.maxSatisfying(versions, constraint)
```

<h6>매개변수</h6>

- `versions` `String[]`
- `constraint` `String`

<h6>반환값</h6>

가장 적합한 원본 버전 문자열을 반환합니다.
일치하는 버전이 없으면 빈 문자열을 반환합니다.

형식이 잘못된 후보 버전은 건너뜁니다.

## compare()

두 시맨틱 버전을 비교합니다.

<h6>구문</h6>

```js
semver.compare(left, right)
```

<h6>매개변수</h6>

- `left` `String`
- `right` `String`

<h6>반환값</h6>

- `-1`: `left < right`
- `0`: `left === right`
- `1`: `left > right`

## 사용 예제

```js {linenos=table,linenostart=1}
const semver = require('semver');

console.println(semver.satisfies('1.4.2', '1.2 - 1.4'));
console.println(semver.satisfies('2.0.0', '1.2 - 1.4'));
console.println(semver.maxSatisfying(['1.2.0', '1.4.2', '2.0.0'], '1.2 - 1.4'));
console.println(semver.maxSatisfying(['1.0.0', '1.1.4', '1.2.0'], '~1.1'));
console.println(semver.compare('1.1.0', '1.2.0'));
console.println(semver.compare('1.2.0', '1.1.0'));
console.println(semver.compare('1.2.0', '1.2.0'));
```

## 동작 메모

- 잘못된 `version`, `left`, `right`, `constraint` 값은 오류를 발생시킵니다.
- 버전과 제약 조건은 파싱 전에 앞뒤 공백을 제거합니다.
- 제약 조건 파싱은 `1.2 - 1.4`, `~1.1` 같은 범위 표현을 지원하는 내부 시맨틱 버전 규칙을 따릅니다.