---
type: docs
title: '13.1 시계열 JOIN'
weight: 10
toc: true
---

[시계열 JOIN·TIMESTAMP·TIE 전체 BNF](../../reference/sql/syntax/time-series-join-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

시계열 JOIN은 키와 지정 시각으로 관측의 관계를 계산합니다. 한 행 선택·보간·시간창 집계·사건 축 결합을 구분해 선택합니다.

| 주제 |
|---|
| [13.1.1 ASOF JOIN: 이벤트 시점의 직전 상태](./asof/) |
| [13.1.2 LT JOIN: 같은 시각을 제외한 직전 상태](./lt/) |
| [13.1.3 NEAREST JOIN: 가장 가까운 관측값](./nearest/) |
| [13.1.4 INTERPOLATE JOIN: 실측 사이의 선형 보간](./interpolate/) |
| [13.1.5 WINDOW JOIN: 이벤트 시간창의 집계](./window/) |
| [13.1.6 HORIZON JOIN: 여러 오프셋 시각의 조회](./horizon/) |
| [13.1.7 일반 JOIN과 시계열 JOIN 비교](./ordinary/) |
| [13.1.8 SPLICE JOIN: 양쪽 관측의 변화 시점](./splice/) |

## 공통 실습 데이터

[공통 실습 준비](../#실습-준비)의 setup.sql을 먼저 실행합니다.
TS13_EVENT와 TS13_MOTOR의 NAME은 모두 edu27_main입니다. EVENT의 VALUE는 발생 순서 1~6,
MOTOR의 VALUE는 기준에서 지난 초의 제곱입니다.

| EVENT_S | VALUE |
| --- | --- |
| 10 | 1 |
| 21 | 2 |
| 30 | 3 |
| 41 | 4 |
| 46 | 5 |
| 60 | 6 |

| MOTOR_S | VALUE |
| --- | --- |
| 0 | 0 |
| 4 | 16 |
| 8 | 64 |
| 10 | 100 |
| 12 | 144 |
| 16 | 256 |
| 18 | 324 |
| 22 | 484 |
| 24 | 576 |
| 28 | 784 |
| 30 | 900 |
| 32 | 1024 |
| 36 | 1296 |
| 38 | 1444 |
| 42 | 1764 |
| 44 | 1936 |
| 48 | 2304 |
| 50 | 2500 |


## 입력 시간축

TAG는 BASETIME을 기본으로 사용합니다. LOG·파생 SELECT는 alias 뒤에 TIMESTAMP(DATETIME컬럼)을
선언합니다. 이름이 TIME인 문자열이나 정수 컬럼을 자동으로 시간축으로 취급하지 않습니다.
원본 관측 ID와 시간 보정 정보를 명시하려면 [SOURCE와 PROVENANCE](../provenance/)를 사용합니다.

## 방식 선택

| 목적 | 방식 | 기준 이벤트당 결과 |
|---|---|---|
| 현재까지 알려진 상태 | ASOF | 오른쪽 한 행 또는 NULL |
| 정확히 같은 시각 제외 | LT | 오른쪽 한 행 또는 NULL |
| 전후 가장 가까운 실측 | NEAREST | 오른쪽 한 행 또는 NULL |
| 실측 사이 추정값 | INTERPOLATE | 보간값 또는 NULL |
| 전후 구간 통계 | WINDOW | 창의 집계 |
| 여러 오프셋의 상태 | HORIZON | 오프셋마다 한 행 |
| 모든 적격 조합 | 일반 JOIN | 조건에 맞는 조합 |
| 어느 쪽이든 변화할 때 상태 | SPLICE | 양쪽 사건 축의 행 |

## 키와 허용 시간

ASOF·LT·NEAREST·INTERPOLATE·WINDOW·HORIZON·SPLICE의 ON은 양쪽 키의 동등 비교를
AND로 연결합니다. 입력의 값 조건은 source 서브쿼리에서 거르고 최종 WHERE는 결과 필터로
사용합니다. NULL 키는 동등 매칭되지 않습니다. SPLICE는 NULL 키·시각의 원본 사건을
반대쪽 NULL과 함께 보존합니다.

ASOF·LT·NEAREST의 TOLERANCE는 두 관측의 허용 시간차이며 경계를 포함합니다.
`5s`, `200ms`, `1ns` 같은 고정 기간을 사용합니다. 괄호 안의 정수식은 나노초입니다.
시간축의 기본 단위는 나노초이므로 단위 없는 정수를 초로 추측하지 않습니다.

## READ 입력과 저장 테이블 결합

READ의 DATETIME 컬럼을 `TIMESTAMP(컬럼)`으로 지정하고 장치·세션 키를 ON에 넣습니다.
동일 시각의 후보에는 논리 순서 키로 TIE 정책을 지정합니다.
[파일 관측과 저장 테이블 JOIN 실습](../../dfq/analysis-load/#read-storage-join)을 참고합니다.
