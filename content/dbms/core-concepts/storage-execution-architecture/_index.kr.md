---
type: docs
title: '저장 및 실행 구조'
weight: 20
---

이 섹션은 Machbase DBMS가 내부적으로 어떻게 데이터를 저장하고 SQL을 실행하는지를 설명합니다. 각 주제는 개념 수준의 이해를 목적으로 하며, 성능 튜닝과 시스템 운영 시 올바른 판단을 내리는 데 필요한 배경지식을 제공합니다.

- **[Machbase 아키텍처 개요](architecture-machbase/)** — SQL 엔진, 저장 관리자, 프로세스 관리자의 역할과 Standard/Cluster Edition의 구조적 차이를 설명합니다.
- **[컬럼형 저장과 압축](storage-columnar-compression-column/)** — 행 지향 저장과의 차이, 시계열 데이터에서 컬럼 압축이 특히 효과적인 이유, 파티션 구조를 설명합니다.
- **[인덱싱 기본 원리](indexing-basics/)** — 테이블 유형별 인덱스 특성(TAG의 파티션 인덱스, LOG의 LSM 인덱스, VOLATILE의 Red-Black 트리)을 설명합니다.
- **[Cache와 실행 계획 개념](execution-concepts-plan-cache/)** — SQL 실행 과정과 Plan Cache, Result Cache, PVO Cache의 역할을 설명합니다.
