---
type: docs
title: '입력과 적재 문제'
weight: 30
---

데이터가 Machbase에 정상적으로 들어오지 않을 때, 원인은 크게 세 가지 경로로 나뉩니다. Append API를 통한 직접 입력 실패, machloader를 이용한 CSV 파일 가져오기 실패, 그리고 Machbase Collector를 통한 수집 파이프라인 오류입니다.

각 경우는 오류가 발생하는 위치와 증상이 다르므로 해당하는 섹션에서 진단을 시작하십시오.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [입력이 실패할 때](./failure/) | Append API 오류 원인 분석 및 해결 방법 |
| [CSV import가 실패할 때](./failure-csv-import/) | machloader 오류 진단 및 옵션 설정 |
| [Collector 수집이 실패할 때](./failure-ingestion-collector/) | Collector 트레이스 로그 분석 및 복구 절차 |
