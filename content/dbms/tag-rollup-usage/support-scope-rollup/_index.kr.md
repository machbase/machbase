---
title: '6.18 ROLLUP 제약과 Cluster Edition 지원 범위'
weight: 170
toc: true
---

<a id="support-scope-rollup-rebuild-cluster"></a>

## ROLLUP 지원 범위

### Edition별 지원

| 기능 | Standard Edition | Cluster Edition |
|------|:---:|:---:|
| CREATE/DROP ROLLUP | O | O |
| ALTER ROLLUP (START/STOP/FORCE/WAKEUP) | O | O |
| WITH ROLLUP 자동 생성 | O | O |
| ROLLUP 조회 (`rollup()` 함수) | O | O |
| Custom Rollup (INTO...AS) | O | X |
| 조건 ROLLUP (WHERE) | O | O |
| 확장 ROLLUP (EXTENSION) | O | O |
| Rollup Rebuild (`EXEC ROLLUP_REBUILD`) | O | X |

> **Custom Rollup과 Rollup Rebuild는 Cluster Edition에서 지원하지 않습니다.** 소스 코드(`qpvRollup.c`) 기준으로 Cluster Edition에서 Custom Rollup 생성 시 `ERR_QP_CUSTOM_ROLLUP_NOT_SUPPORTED_IN_CLUSTER` 오류가 반환됩니다.
>
> 기본 ROLLUP 스레드는 Cluster Edition에서 각 노드에서 독립적으로 동작합니다.

### 테이블 타입별 ROLLUP 지원

| 테이블 타입 | ROLLUP 지원 |
|------------|:---:|
| TAG (시간축) | O |
| TAG (거리축) | X |
| LOG | X |
| RDB | X |
| VOLATILE | X |
| LOOKUP | X |

> ROLLUP은 시간축(BASETIME) TAG 테이블 전용 기능입니다.

### 집계 함수 지원 범위

| 함수 | 기본 ROLLUP | 확장 ROLLUP |
|------|:---:|:---:|
| MIN | O | O |
| MAX | O | O |
| SUM | O | O |
| COUNT | O | O |
| AVG | O | O |
| SUMSQ | O | O |
| FIRST | X | O |
| LAST | X | O |

### ROLLUP 관련 권한

```sql
-- ROLLUP 생성/삭제 권한 (예시)
GRANT CREATE ROLLUP ON *.* TO rollup_user;
GRANT DROP ROLLUP ON *.* TO rollup_user;
```

권한 체계는 [사용자 관리](/dbms/data-modeling-table-design/schema-objects-definition/) 섹션을 참조하세요.
