---
type: docs
title: '17.8.4 support-matrix'
weight: 40
toc: true
---

이 페이지는 지원표를 복제하지 않고 질문의 차원을 확인한 뒤 현재 정본으로 연결합니다.

## 확인 순서

1. [Edition별 지원표](/dbms/reference/support-scope-constraints/edition/)에서 Standard와
   Cluster 범위를 확인합니다.
2. [테이블 타입별 지원표](/dbms/reference/support-scope-constraints/table-types-type/)에서
   대상 테이블의 SQL·API 범위를 확인합니다.
3. [SDK 지원 범위](/dbms/development-tools-integration/sdk-support-scope/)에서 client API와
   최소 provenance를 확인합니다.
4. 기능별 상세 지원표에서 조건과 예외를 확인합니다.

| 기능군 | 정본 |
|--------|------|
| TAG data UPDATE | [TAG UPDATE 지원표](/dbms/reference/support-scope-constraints/tag-data-update/) |
| ROLLUP | [ROLLUP 지원 범위](/dbms/reference/support-scope-constraints/rollup/) |
| TRANSACTION | [TRANSACTION 지원 범위](/dbms/reference/support-scope-constraints/rdb/) |
| 백업·MOUNT | [백업/MOUNT 지원표](/dbms/reference/support-scope-constraints/backup-mount/) |
| 권한 | [권한 지원표](/dbms/reference/support-scope-constraints/privileges/) |

지원 여부를 답할 때는 `O/△/X`만 인용하지 말고 Edition, 테이블 타입, 서버와 SDK 버전,
필수 조건을 함께 제시합니다.
