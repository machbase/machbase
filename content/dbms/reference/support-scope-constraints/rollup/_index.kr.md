---
type: docs
title: '17.6.6 ROLLUP 지원 범위'
weight: 60
toc: true
aliases:
  - /dbms/tag-rollup-usage/support-scope-rollup/
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

> **Custom ROLLUP과 ROLLUP_REBUILD는 Cluster Edition에서 지원하지 않습니다.** 지원되지 않는
> 기능을 실행하면 서버가 오류를 반환합니다. 내부 symbolic error 이름을 사용자 계약으로
> 사용하지 마십시오.
>
> 기본 ROLLUP 스레드는 Cluster Edition에서 각 노드에서 독립적으로 동작합니다.

### 테이블 타입별 ROLLUP 지원

| 테이블 타입 | ROLLUP 지원 |
|------------|:---:|
| TAG (시간축) | O |
| TAG (거리축) | X |
| LOG | X |
| TRANSACTION | X |
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
-- 대상 database에서 ROLLUP 객체를 생성·삭제할 권한
GRANT CREATE, DROP ON DATABASE MACHBASEDB TO rollup_user;
```

권한 체계는 [권한 관리](/dbms/security-access-control/privileges/)를 참고하십시오.
