---
type: docs
title: '13.2.7 타임존'
weight: 70
---

Machbase는 모든 시각(DATETIME) 값을 내부적으로 **UTC 나노초** 단위로 저장합니다. 클라이언트가 데이터를 읽거나 쓸 때, 세션에 설정된 타임존에 따라 변환이 이루어집니다.

## 타임존 동작 원리

Machbase의 타임존은 세 가지 레이어로 구분됩니다.

| 레이어 | 적용 범위 | 설정 방법 |
|--------|-----------|-----------|
| 서버 타임존 | 서버 기본값. 클라이언트가 타임존을 지정하지 않으면 이 값이 세션에 적용됨 | `machbase.conf`의 `TIMEZONE` 프로퍼티 또는 OS 기본 타임존 |
| 세션 타임존 | 개별 연결(세션)에 적용. 서버 타임존을 재정의 | 연결 문자열의 `TIMEZONE` 파라미터, machsql의 `-z` 옵션 |
| 표시 타임존 | 데이터를 출력할 때 변환하는 기준 타임존 | REST API 헤더 또는 쿼리 파라미터 |

### 동작 규칙

1. 서버는 OS의 기본 타임존을 읽어 초기값으로 사용합니다. `machbase.conf`에서 `TIMEZONE`을 명시하면 OS 설정을 무시합니다.
2. 클라이언트가 타임존을 지정하지 않고 연결하면 서버의 타임존이 세션에 적용됩니다.
3. 클라이언트가 연결 시 타임존을 명시하면 해당 세션은 지정된 타임존으로 동작합니다.

## Machbase 타임존 형식

Machbase는 `+HHMM` 또는 `-HHMM` 형식의 5자리 오프셋을 사용합니다.

```
+0900   # UTC+9 (한국 표준시 KST)
+0000   # UTC
-0500   # UTC-5 (미국 동부 표준시 EST)
+0530   # UTC+5:30 (인도 표준시 IST)
```

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [서버 타임존 설정](./timezone-server-configuration/) | `TIMEZONE` 프로퍼티 설정, OS 타임존과의 관계 |
| [machsql -z](./machsql-z/) | machsql 세션 타임존 설정 옵션 |
| [machloader -z](./machloader-z/) | CSV 데이터 로드 시 타임존 지정 |
| [CLI/JDBC/.NET TIMEZONE 연결 옵션](./connection-cli-jdbc-net-timezone/) | 연결 문자열에서 타임존 지정 |
| [REST API 타임존 응답](./timezone-rest-api/) | HTTP 헤더로 응답 타임존 지정 |
