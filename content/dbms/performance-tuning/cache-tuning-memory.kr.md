---
type: docs
title: '12.6 PVO Cache와 메모리 튜닝'
weight: 60
toc: true
aliases:
  - /dbms/tag-table-usage/tag-cache-operations/
---

<a id="pvo-cache"></a>

## PVO Cache 운영

PVO Cache는 SQL 실행 계획을 재사용합니다. 조회 결과 행을 저장하는 캐시가 아닙니다.

<a id="tuning-memory-configuration"></a>

## 메모리 설정 튜닝

PVO Cache, Min-Max Cache, 프로세스 상한, 쿼리의 일시 메모리를 사용 가능한 물리 메모리
예산 안에서 함께 계획합니다.
