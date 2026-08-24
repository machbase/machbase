---
type: docs
title: '2. 핵심 개념'
weight: 20
toc: true
---

Machbase DBMS를 효과적으로 활용하려면 시스템 설계 원칙을 먼저 이해해야 합니다. 2장은 테이블 설계와 SQL 작성에 앞서 알아야 할 핵심 개념을 다섯 섹션으로 나누어 다룹니다.

**[데이터 모델 개념](concepts/)** -- 시계열 데이터가 일반 업무 데이터와 어떻게 다른지, append-only 구조를 채택한 이유, 테이블 유형별 시간 표현 방식을 다룹니다. **[저장 및 실행 구조](storage-execution-architecture/)** -- 전체 아키텍처와 컬럼형 저장, 인덱싱 원리, 실행 계획 및 캐시 개념을 다룹니다. **[주요 기능 개념](features-concepts/)** -- ROLLUP, Retention Policy, Backup/Restore/Mount의 역할과 동작 방식을 다룹니다. **[Edition 개념](concepts-edition/)** -- 기존 RDBMS와의 차이, Standard Edition과 Cluster Edition의 차이를 다룹니다. **[용어 구분](terminology-distinction/)** -- 운영에서 혼동하기 쉬운 개념 쌍들을 비교 표와 함께 구분합니다.

각 섹션은 독립적으로 읽을 수 있지만, 처음 접하는 경우 데이터 모델 개념부터 순서대로 읽는 것을 권장합니다.
