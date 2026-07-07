---
type: docs
title: 'REST API 타임존 응답'
weight: 50
---

Machbase REST API를 사용할 때 HTTP 요청 헤더에 타임존을 지정하면, 응답에 포함된 DATETIME 값이 해당 타임존 기준으로 변환되어 반환됩니다.

## 요청 헤더에서 타임존 지정

`The-Timezone-Machbase` 헤더를 사용하여 응답 타임존을 지정합니다.

```
The-Timezone-Machbase: +0900
```

### curl 예시

```bash
# KST(UTC+9) 기준으로 쿼리 결과 조회
curl -H "Authorization: Basic $(echo -n 'SYS:MANAGER' | base64)" \
     -H "The-Timezone-Machbase: +0900" \
     -G "http://127.0.0.1:5657/machbase" \
     --data-urlencode 'q=SELECT sysdate FROM v$tables LIMIT 1'
```

응답 JSON의 `timezone` 필드에 적용된 타임존 값이 반환됩니다.

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "sysdate",
      "type": 6,
      "length": 31
    }
  ],
  "timezone": "+0900",
  "data": [
    {
      "sysdate": "2026-07-07 10:30:00 000:000:000"
    }
  ]
}
```

## UTC 기준으로 조회

```bash
# UTC 기준으로 조회
curl -H "Authorization: Basic $(echo -n 'SYS:MANAGER' | base64)" \
     -H "The-Timezone-Machbase: +0000" \
     -G "http://127.0.0.1:5657/machbase" \
     --data-urlencode 'q=SELECT sysdate FROM v$tables LIMIT 1'
```

```json
{
  "timezone": "+0000",
  "data": [
    {
      "sysdate": "2026-07-07 01:30:00 000:000:000"
    }
  ]
}
```

## 타임존 미지정 시 동작

`The-Timezone-Machbase` 헤더를 포함하지 않으면 서버의 기본 타임존(`machbase.conf`의 `TIMEZONE` 값 또는 OS 타임존)이 적용됩니다.

## 데이터 입력 시 타임존 적용

REST API로 데이터를 INSERT할 때도 동일한 헤더를 사용하면 DATETIME 값이 지정 타임존으로 해석되어 UTC로 변환 후 저장됩니다.

```bash
curl -X POST \
     -H "Authorization: Basic $(echo -n 'SYS:MANAGER' | base64)" \
     -H "Content-Type: application/json" \
     -H "The-Timezone-Machbase: +0900" \
     -d '{"q":"INSERT INTO sensor VALUES(TO_DATE(\"2026-07-07 10:00:00\"), 25.3)"}' \
     "http://127.0.0.1:5657/machbase"
```

위 예시에서 `2026-07-07 10:00:00`은 KST로 해석되어 UTC 기준 `2026-07-07 01:00:00`으로 저장됩니다.

## 주의 사항

- 헤더 이름은 `The-Timezone-Machbase`이며, 대소문자를 구분하지 않는 HTTP 표준에 따라 처리됩니다.
- 오프셋 형식은 `+HHMM` 또는 `-HHMM`(5자리)이어야 합니다.
