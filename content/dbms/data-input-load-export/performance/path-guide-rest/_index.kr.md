---
type: docs
title: 'REST 입력 경로 안내'
weight: 20
---

Machbase는 HTTP REST API를 통해 외부 시스템이나 IoT 디바이스에서 직접 데이터를 입력할 수 있습니다.

## REST API 입력 개요

REST API는 HTTP JSON 기반으로 동작합니다. SDK나 별도 드라이버 없이 `curl` 등 표준 HTTP 클라이언트로 연동할 수 있어 범용성이 높습니다.

```bash
# REST API로 데이터 삽입 예시
curl -X POST http://127.0.0.1:5657/machbase \
    -H "Content-Type: application/json" \
    -d '{"name":"sensor_log","date_format":"YYYY-MM-DD HH24:MI:SS","values":[["TEMP-01","2024-01-15 10:00:00",25.3]]}'
```

## 성능 특성

- SQL INSERT 대비 빠르나, SDK Append API보다는 낮은 처리량
- HTTP 오버헤드가 있으므로 초당 수십만 건 이하의 적재에 적합
- 배치(bulk) 전송으로 처리량 향상 가능

## 주요 사용 사례

- IoT 디바이스, 센서 게이트웨이
- 외부 시스템과의 HTTP 기반 연동
- 언어·플랫폼 무관 데이터 수집

## 상세 문서

REST API의 인증, 엔드포인트, 요청/응답 형식, 배치 전송 방법은 다음 문서를 참고하세요.

> **[8장 애플리케이션 연동 → REST API](/dbms/application-integration/)** 에서 상세 내용을 다룹니다.
