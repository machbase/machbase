---
type: docs
title: '6. TAG 테이블 ROLLUP 활용'
weight: 60
toc: true
---

ROLLUP은 시간축 TAG의 데이터를 미리 집계하고, 조회할 때 그 통계를 합쳐 반복 분석 비용을
줄이는 기능입니다. 이 장은 Machbase DBMS 8.7.0의 기본·조건·확장·JSON·Custom
ROLLUP을 구분하고 생성부터 결과 검증과 재구성까지 설명합니다.

## 먼저 구분할 세 가지 간격

| 개념 | 의미 | 예 |
|---|---|---|
| 생성 INTERVAL | 저장할 집계 버킷의 간격 | 1 MIN |
| WAKEUP INTERVAL | 집계 작업을 깨우는 주기 | 10 SEC |
| 조회 버킷 | 보고서가 요청하는 결과 구간 | `rollup('min', 5, time)` |

같은 버킷에 여러 차례의 부분 집계가 저장될 수 있습니다. 기본 ROLLUP은 공개 조회 구문이
필요한 통계를 병합하고, Custom 대상 TAG는 사용자가 최종 재집계 쿼리를 작성합니다.
원본 보존 기간과 ROLLUP 보존·재구성 정책은 별도로 정합니다.

## 이 장의 구성

| 절 | 내용 |
|---|---|
| [개요와 사용 기준](./overview-use-criteria/) | 기본 실습과 원본·집계 비교 |
| [대상 TAG 설계](./target-tag-table-design/) | ON/FROM, 계층 제약과 용량 산정 |
| [생성과 삭제](./create-delete-rollup/) | CREATE, WITH ROLLUP, IF NOT EXISTS와 의존성 |
| [조회 문법](./query-syntax-rollup/) | 후보 선택, 시간 단위와 origin |
| [조건 ROLLUP](./conditional-rollup/) | 원본 필터와 명시적인 후보 선택 |
| [Custom ROLLUP](./custom-rollup/) | 증분 결과 재집계와 OHLCV 계층 |
| [확장 ROLLUP](./extension-rollup/) | FIRST/LAST와 OHLC 검증 |
| [JSON ROLLUP](./json-summarized-rollup/) | 경로·문서 전체 집계와 NULL |
| [제어와 상태](./ingestion-control-rollup/) | STOP/START/WAKEUP/FORCE, V$ROLLUP과 gap |
| [REBUILD](./rollup-rebuild/) | 실제 지원 대상, 버킷 경계와 정정 |
| [성능 튜닝](./performance-tuning-rollup/) | 같은 결과를 기준으로 비용 비교 |
| [활용 시나리오](./patterns-scenarios/) | 다중 태그와 원본·집계의 역할 분담 |

각 페이지는 독립 실습이며 객체 이름을 `ch6_`로 구분합니다. 기존 업무 객체와 이름이
겹치지 않는지 확인하고, 의도적 오류 예제는 성공 스크립트와 분리합니다. 고정 시각 데이터는
표시한 고정 구간으로 조회합니다. 실습 테이블·ROLLUP만 정리합니다.

Custom과 REBUILD는 Standard Edition 전용입니다. ROLLUP이 생성됐거나 입력에 성공했다는
사실만으로 집계가 끝났다고 판단하지 않습니다. 실습에서는 이름을 지정한 FORCE로 처리
범위를 따라잡고 결과를 확인합니다.

[지원 범위](../reference/support-scope-constraints/rollup/)와
[문제 해결](../troubleshooting/rollup/)에서 제약과 진단을 이어 확인합니다.
