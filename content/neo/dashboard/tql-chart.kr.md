---
title: TQL 차트
type: docs
weight: 50
---

## 개요

차트 타입에서 **Tql chart**를 선택하면 사용자가 작성한 TQL 파일을 대시보드 패널로 사용할 수 있습니다.

{{< media slug="neo-dashboard/type-tql-chart" width="600" >}}

- **Tql path** : 사용할 TQL 파일을 선택합니다. `Select file`로 고르거나 `Open file`로 편집기에서 엽니다.
- **Params** : TQL 파일에 전달할 파라미터를 등록합니다. 값을 직접 입력하거나 대시보드가 제공하는 기본 변수를 사용할 수 있습니다.
- **Theme** : 테마는 TQL 파일 안의 `CHART( theme("...") )`로 지정합니다. 사용 가능한 테마 이름이 오른쪽 패널에 안내됩니다.

SINK가 `CHART`인 TQL이 가장 일반적이지만, 표(CSV)·Markdown·HTML·NDJSON·텍스트를 출력하는 TQL도 패널에 그대로 표시됩니다. 단, `CHART`가 아닌 출력을 표시하는 패널에는 자동 새로 고침(대시보드·패널 주기 모두)이 적용되지 않으며, 새로 고침 버튼을 누르거나 시간 범위를 바꿀 때 다시 조회합니다.

## 기본 변수

**Time range** — 대시보드의 다른 패널과 시간을 맞출 때 사용합니다.

| 파라미터 | 설명 |
|:-------|:-----|
| {{from_str}} | 날짜 문자열 (YYYY-MM-DD HH:MI:SS) |
| {{from_s}},{{from_ms}},{{from_us}},{{from_ns}} | 유닉스 타임스탬프 (초/밀리초/마이크로초/나노초) |
| {{to_str}} | 날짜 문자열 (YYYY-MM-DD HH:MI:SS) |
| {{to_s}},{{to_ms}},{{to_us}},{{to_ns}} | 유닉스 타임스탬프 (초/밀리초/마이크로초/나노초) |

**period** — 시간 범위와 패널 크기에 따라 계산된 x축 간격입니다.

| 파라미터 | 설명 |
|:-------|:-----|
| {{period}} | 기간 표현 (예: 10s) |
| {{period_value}} | 기간 값 (예: 10) |
| {{period_unit}} | 기간 단위 (예: sec) |

## TQL 파일에서 파라미터 사용하기

TQL 파일에서는 `param()` 함수로 대시보드가 전달한 값을 받습니다.

```sql
SQL(strSprintf(`
SELECT date_trunc('%s', TIME, %1.0f) as TIME, avg(VALUE) as VALUE
FROM EXAMPLE
WHERE TIME between FROM_UNIXTIME(%1.0f) and FROM_UNIXTIME(%1.0f) AND NAME IN ('%s')
GROUP BY TIME ORDER BY TIME`, 
(param('period_unit') ?? 'msec'), 
parseFloat(param('period_value') ?? 10), 
parseFloat(param('from') ?? 1703055573), 
parseFloat(param('to') ?? 1703055583),
(param('tag') ?? 'tag01')
))

CHART_LINE()
```

**SQL()** — `param()`과 `strSprintf()`로 쿼리를 동적으로 만듭니다. 주요 파라미터는 `period_unit`(기본 `msec`), `period_value`(기본 10), `from`·`to`(조회 기간), `tag`(조회할 태그, 기본 `tag01`)입니다.

**CHART_LINE()** — 쿼리 결과를 라인 차트로 그립니다.
