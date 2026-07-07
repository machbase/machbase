---
type: docs
title: 'ROLLUP'
weight: 70
---

ROLLUP은 TAG 테이블의 시계열 데이터를 정해진 시간 단위(초/분/시)로 자동 집계해 저장하는 Machbase 고유의 기능입니다. 수백만 건의 원시 데이터를 스캔하는 대신 사전 계산된 통계를 이용하므로 분석 쿼리의 응답 속도가 크게 향상됩니다.

## ROLLUP의 역할

실시간으로 수집되는 센서 데이터는 초 단위의 원시 값입니다. 분·시간 단위의 추세 분석이나 대시보드를 위해 매번 수억 건을 스캔하면 성능 문제가 생깁니다. ROLLUP은 데이터가 입력되는 즉시 백그라운드에서 집계를 처리해 두고, 조회 시 미리 집계된 값을 반환합니다.

```
원시 데이터 (초 단위) → ROLLUP (1초 집계) → ROLLUP (1분 집계) → ROLLUP (1시간 집계)
```

각 레벨의 집계 테이블에는 시간 구간별로 MIN, MAX, SUM, COUNT, AVG, SUMSQ 값이 저장됩니다. 확장 ROLLUP(EXTENSION)을 사용하면 구간의 첫 번째·마지막 값(FIRST/LAST)도 함께 저장됩니다.

## 이 섹션의 구성

| 주제 | 설명 |
|------|------|
| [ROLLUP 개념](rollup/) | ROLLUP 테이블 구조와 집계 원리 |
| [확장 ROLLUP](rollup-extension/) | EXTENSION 키워드와 FIRST/LAST 함수 |
| [생성과 삭제](create-delete-rollup/) | CREATE/DROP ROLLUP 구문 |
| [시작·중지와 즉시 수집](ingestion-start-stop-immediate-collect-rollup/) | ALTER ROLLUP START/STOP/FORCE/WAKEUP |
| [상태 확인](state-status-rollup-wakeup-interval-vrollup/) | V$ROLLUP, WAKEUP INTERVAL |
| [조회 문법](query-syntax-rollup/) | rollup() 함수와 GROUP BY |
| [주/월/연 조회](query-week-month-year-day-timezone-origin-rollup/) | day/week/month/year 단위 조회 |
| [조건 ROLLUP](condition-conditional-rollup/) | WHERE 조건이 있는 필터 집계 |
| [사용자 정의 ROLLUP](custom-rollup/) | INTO ... AS (SELECT ...) 구문 |
| [FIRST/LAST](first-last-rollup/) | 구간 시작/종료 값 조회 |
| [설계 가이드](design-rollup-on/) | ON vs FROM, 계층 구성 |
| [JSON SUMMARIZED](json-summarized-rollup/) | JSON 컬럼 ROLLUP |
| [삭제·부분 재구성 차이](differences-rollup-delete-partial-rebuild/) | DROP ROLLUP과 Rebuild 비교 |
| [지원 범위](support-scope-rollup-rebuild-cluster/) | Standard/Cluster Edition 지원 |
| [운영 주의사항](operational-notes-rollup/) | 주기 설정, 부하, 주의사항 |
| [활용 사례](use-cases-rollup/) | 실전 패턴 모음 |
