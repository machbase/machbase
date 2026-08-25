---
type: docs
title: '18.1.5 SELECT 힌트 사전'
weight: 50
toc: true
---

SELECT 힌트의 문법, 지원 대상과 예제는
[SELECT hint syntax](/dbms/reference/sql/syntax-dictionary-sql/select-hint-syntax/)를
정본으로 사용합니다.

| 목적 | 힌트 |
|------|------|
| 병렬 실행 제어 | `PARALLEL`, `NOPARALLEL` |
| 스캔·인덱스 제어 | `FULL`, `NO_INDEX`, `RID_RANGE`, `SCAN_FORWARD`, `SCAN_BACKWARD` |
| ROLLUP 선택 | `ROLLUP_TABLE` |
| TAG 시간 구간 처리 | `SAMPLING`, `INTERPOLATION` |

힌트는 `SELECT` 바로 뒤의 `/*+ ... */` 블록에 작성합니다. 실행 계획을 먼저 확인하고,
필요한 경우에만 적용한 뒤 변경 전후를 같은 조건에서 측정하십시오.
