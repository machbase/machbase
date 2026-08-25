---
type: docs
title: '17.6.11 제한사항 색인'
weight: 110
toc: true
---

제한사항을 다른 지원표와 중복해서 정의하지 않고 기능별 정본으로 연결합니다.

| 범주 | 정본 |
|---|---|
| Edition | [Edition별 지원](../edition/) |
| 테이블 타입 | [테이블 타입별 지원](../table-types-type/) |
| TRANSACTION | [TRANSACTION 지원](../rdb/) |
| TAG UPDATE | [TAG UPDATE 지원](../tag-data-update/) |
| LOOKUP SQL·JSON | [LOOKUP 지원](../lookup-sql-json/) |
| ROLLUP | [ROLLUP 지원](../rollup/) |
| SDK | [SDK 기능 지원](/dbms/development-tools-integration/sdk-support-scope/) |
| 권한 | [권한별 지원](../privileges/) |
| 백업·마운트 | [백업·마운트 지원](../backup-mount/) |
| server·SDK 버전 | [호환성](../compatibility-xma-protocol/) |

## 공통 판단 원칙

- 다른 테이블 타입의 DML·index·transaction 규칙을 그대로 적용하지 않습니다.
- Cluster와 Standard의 객체·운영 명령 지원 범위를 실행 전에 확인합니다.
- SDK 기능은 server와 client 버전을 함께 확인합니다.
- 지원표에 없는 내부 object, flag와 protocol 동작에 의존하지 않습니다.
- 정확한 SQL과 option은 해당 레퍼런스의 현재 문법을 사용합니다.

기능별 오류 진단은 [문제 해결](/dbms/troubleshooting/)을 참고하십시오.
