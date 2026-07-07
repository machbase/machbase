---
type: docs
title: '고급 조회 항목'
weight: 30
---

Machbase는 시계열 데이터 분석에 필요한 다양한 고급 SQL 기능을 제공합니다. 기본 SELECT 조회에서 한 단계 나아가, 데이터를 집계·변환·보간·연산하는 분석 쿼리를 작성할 수 있습니다.

## 이 절에서 다루는 내용

- **[집계 함수와 GROUP BY](./aggregation-group/)**: COUNT, SUM, AVG 등 집계 함수와 GROUP BY, HAVING 절 사용법
- **[GROUP_CONCAT](./aggregation-group-concat/)**: 그룹 내 값을 하나의 문자열로 이어 붙이는 함수
- **[JOIN](./join/)**: 시계열 테이블과 참조 테이블의 결합, 메타데이터 조인 패턴
- **[PIVOT](./pivot/)**: 행을 열로 변환하여 여러 센서 값을 나란히 비교
- **[윈도우 함수와 OVER](./window-functions-over/)**: 이동 평균, 순위 등 윈도우 기반 분석 연산
- **[보간 조회와 SERIES BY](./query-interpolation-series/)**: 누락 구간을 채우는 보간 및 SERIES BY 절
- **[ROLLUP](./rollup/)**: 시간 축 기반 자동 집계와 다단계 시간 해상도 조회
