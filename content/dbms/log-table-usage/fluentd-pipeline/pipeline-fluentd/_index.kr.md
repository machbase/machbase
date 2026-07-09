---
type: docs
title: 'Fluentd 입력 파이프라인 안내'
weight: 40
---

Fluentd는 오픈소스 데이터 수집 에이전트로, 다양한 소스에서 데이터를 수집하여 Machbase로 전달하는 파이프라인을 구성할 수 있습니다.

## Fluentd + Machbase 구성 개요

```
[로그 소스] → [Fluentd Agent] → [Machbase Fluentd Output Plugin]
  - 애플리케이션 로그
  - 시스템 메트릭
  - 네트워크 장비 로그
```

Fluentd는 Machbase Output Plugin을 통해 Machbase 서버에 접속하고 append 세션으로 데이터를 전송합니다.

## 주요 사용 사례

- 서버 로그를 Machbase LOG 테이블로 수집
- Prometheus/StatsD 메트릭을 TAG 테이블로 저장
- Kafka, AWS S3 등 외부 소스에서 Machbase로 ETL

## 기본 설정 예시

```xml
<!-- Fluentd Machbase Output Plugin -->
<match machbase.**>
  type machbase

  host 127.0.0.1
  port 5656
  uid SYS
  pwd MANAGER

  tablename apache_access_log
  hostname webserver
  arrivaltime true
</match>
```

## 성능 고려사항

- Fluentd의 buffer 설정을 통해 배치 전송으로 성능을 높일 수 있습니다
- `flush_interval`을 낮출수록 실시간성이 높아지지만 처리량이 감소할 수 있습니다
- 고처리량이 필요하다면 여러 Fluentd worker를 병렬로 구성하세요

## 상세 문서

Fluentd Output Plugin 설치, 설정, 튜닝 방법은 다음 문서를 참고하세요.

> **[8장 애플리케이션 연동 → Fluentd](/dbms/application-integration/)** 에서 상세 내용을 다룹니다.
