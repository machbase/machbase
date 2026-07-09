---
type: docs
title: '11.5 외부 도구 연동'
weight: 50
---

Machbase Neo는 다양한 외부 도구와 연동하여 데이터 수집, 시각화, 분석 워크플로우를 구성할 수 있습니다. 이 섹션에서는 현장에서 자주 사용되는 외부 도구들과 Machbase의 연동 방법을 설명합니다.

## 지원 도구 개요

| 도구 | 용도 | 연동 방식 |
|------|------|-----------|
| [Grafana](grafana-plugin/) | 시계열 데이터 실시간 시각화 및 대시보드 구성 | Machbase 전용 데이터소스 플러그인 |
| [Fluentd](fluentd-plugin/) | 로그 및 이벤트 데이터 수집·전송 파이프라인 구성 | `fluent-plugin-machbase` 출력 플러그인 |
| [Tableau](tableau-connector/) | 비즈니스 인텔리전스 분석 및 리포팅 | JDBC / ODBC 드라이버 연결 |

## 도구 선택 가이드

- **실시간 모니터링 대시보드**가 필요하다면 → [Grafana](grafana-plugin/)
- **다양한 소스의 로그·이벤트를 한 곳에 모아야** 한다면 → [Fluentd](fluentd-plugin/)
- **경영진 보고나 BI 분석**이 필요하다면 → [Tableau](tableau-connector/)
