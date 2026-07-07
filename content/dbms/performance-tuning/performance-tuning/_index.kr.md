---
type: docs
title: '입력 성능 튜닝'
weight: 40
---

데이터 입력 성능은 Machbase 운영에서 가장 중요한 요소 중 하나입니다. 잘못된 입력 방식은 초당 수백만 건을 처리할 수 있는 Machbase의 잠재력을 수십 배 낮출 수 있습니다.

## Append API vs INSERT 비교

| 방식 | 특성 | 처리량 | 적합한 상황 |
|------|------|--------|-----------|
| **Append API** | 비트랜잭션, 버퍼 기반 | 매우 높음 (수십만~수백만 건/초) | 시계열 센서 데이터, 로그 수집 |
| **INSERT (단건)** | 트랜잭션, 즉시 커밋 | 낮음 (수천 건/초) | 관계형 데이터, RDB 테이블 |
| **INSERT (배치)** | 트랜잭션, 다건 | 중간 (수만 건/초) | 소규모 배치 적재 |

> TAG와 LOG 테이블의 대량 수집에는 **반드시 Append API**를 사용하세요.

## 핵심 입력 성능 원칙

1. **Append API 사용**: INSERT 대비 10~100배 빠른 처리량
2. **배치 크기 조정**: 너무 작으면 RTT 오버헤드, 너무 크면 flush 지연
3. **병렬 입력**: 여러 스레드에서 동시에 Append 실행
4. **인덱스 최소화**: 각 인덱스는 Append 성능을 약 5~10% 감소시킴
5. **네트워크 거리 최소화**: 가능하면 Machbase와 같은 호스트 또는 동일 네트워크

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [대량 입력 성능 튜닝](./performance-tuning-bulk/) | 배치 크기, 병렬 Append, machloader, _ARRIVAL_TIME 주의사항 |
| [Collector 수집 성능 튜닝](./ingestion-performance-tuning-collector/) | Collector 컴포넌트 튜닝, 수집 파이프라인 최적화 |
