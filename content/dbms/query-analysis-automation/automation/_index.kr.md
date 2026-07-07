---
type: docs
title: '자동화'
weight: 40
---

Machbase는 데이터 변환·이동·처리를 자동화하는 STREAM 기능을 제공합니다. STREAM은 원본 테이블에 새로 입력된 데이터를 감지해 사전 정의된 쿼리를 자동으로 실행하며, 그 결과를 대상 테이블에 저장합니다.

## 이 섹션의 구성

| 주제 | 설명 |
|------|------|
| [STREAM 개요](stream/) | STREAM의 개념과 동작 원리 |
| [활용 사례](stream/use-cases-stream/) | STREAM 적용 패턴 |
| [생성과 삭제](stream/create-delete-stream/) | STREAM_CREATE / STREAM_DROP |
| [시작](stream/start-stream/) | STREAM_START / STREAM_STOP |
| [사용자 실행 (BY USER)](stream/stream-execute-user/) | STREAM_EXECUTE 수동 호출 |
| [상태 확인](stream/status-check-state-stream/) | V$STREAMS |
| [활용 예시](stream/examples-stream/) | 실전 쿼리 예시 |
| [지원 범위](stream/support-scope-stream-edition-cluster/) | Edition별 지원 범위 |

> STREAM은 Standard Edition 전용 기능입니다. Cluster Edition에서는 지원되지 않습니다.
