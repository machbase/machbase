---
type: docs
title: '2.3 주요 기능 개념'
weight: 30
---

이 섹션은 Machbase DBMS의 핵심 기능들이 어떤 역할을 하는지, 언제 사용하는지를 개념 수준에서 설명합니다. 실제 SQL 문법이나 설정 파라미터는 각 기능의 상세 문서에서 다루며, 여기서는 각 기능의 존재 이유와 동작 원리를 이해하는 데 집중합니다.

- **[ROLLUP 통계의 역할](role-statistics-rollup/)** — 원시 데이터를 SEC/MIN/HOUR 단위로 자동 집계해 조회 성능을 높이는 메커니즘을 설명합니다.
- **[STREAM 처리 모델](processing-model-stream/)** — 주기적으로 SELECT 결과를 다른 테이블에 INSERT하는 자동 처리 객체의 개념과 ROLLUP과의 차이를 설명합니다.
- **[Retention Policy의 역할](role-retention-policy/)** — 오래된 데이터를 기간 기반으로 자동 삭제해 저장 공간을 관리하는 정책 개념을 설명합니다.
- **[Backup / Restore / Mount 개념](concepts-backup-restore-mount/)** — 데이터 복사, 복원, 읽기 전용 연결의 세 가지 데이터 보호 수단이 각각 언제 필요한지 설명합니다.
