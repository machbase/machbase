---
title: '10.14 상태 캐시와 임시 집계 패턴'
weight: 140
toc: true
---

<a id="pattern-volatile-latest-state"></a>

## 최신 상태 캐시

장비나 센서 ID를 `PRIMARY KEY`로 사용하고 같은 키를 중복 키 갱신하면 최신 상태 한 건을
유지할 수 있습니다. 원본 이벤트는 TAG 또는 LOG에 별도로 저장합니다.

<a id="pattern-volatile-temporary-aggregation"></a>

## 임시 집계

대상 ID와 시간 버킷을 결합한 값을 키로 사용하면 짧은 주기 집계를 캐시할 수 있습니다.
집계의 기준 시간대, 닫힌 버킷 판단, 재계산 범위를 함께 정의해야 합니다. 보존할 집계는
영속 테이블로 기록합니다.

<a id="pattern-volatile-work-queue-state"></a>

## 작업 상태

작업 ID를 키로 진행률과 마지막 갱신 시각을 저장할 수 있습니다. VOLATILE은 영속 큐가
아니므로, 재시작 후 이어서 처리해야 하는 작업 정의는 별도 영속 저장소에 둡니다.

<a id="pattern-volatile-rebuild"></a>

## 재구성 기준

재구성 SQL에는 다음 항목을 명시합니다.

- 원본 테이블과 조회 기준 시각
- 동일 키가 여러 건일 때 최신 행을 고르는 기준
- 재구성 중 들어오는 새 데이터의 처리 순서
- 완료 확인용 행 수, 최신 시각, 표본 키

<a id="pattern-volatile-guidelines"></a>

## 관련 예제

테이블 생성과 갱신은 [데이터 입력과 변경](/dbms/volatile-table-usage/data-input-mutation/)을,
조회와 임시 집계는 [조회와 분석](/dbms/volatile-table-usage/query-analysis/)을 참고합니다.
