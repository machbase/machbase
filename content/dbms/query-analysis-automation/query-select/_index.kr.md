---
type: docs
title: 'SELECT 조회'
weight: 20
---

Machbase의 SELECT 문법과 시계열 특화 조회 기능을 정리합니다.

## 이 절에서 다루는 내용

- **[SELECT 기본 조회](./query-select/)**: SELECT 구문, CASE, 서브쿼리, 집합 연산자
- **[WHERE / ORDER BY / LIMIT](./where-order-limit/)**: 조건·정렬·결과 수 제한
- **[시간 조건과 DURATION](./condition-time-duration/)**: 시계열 조회를 위한 시간 조건
- **[상대 시간 표현](./relative-time/)**: DATEADD, NOW 등 상대 시간 함수
- **[거리축 범위 조회](./distance-axis-query-range/)**: 거리 기반 TAG 테이블 조회
- **[VIEW 조회](./query-view/)**: 저장 VIEW 활용
- **[집합 연산: UNION](./set-operators-union-intersect-except/)**: UNION ALL
- **[SELECT 힌트](./hint-select/)**: SAMPLING, INTERPOLATION 등 힌트
- **[EXPLAIN으로 실행 계획 확인](./execution-plan-explain/)**: 쿼리 성능 분석
