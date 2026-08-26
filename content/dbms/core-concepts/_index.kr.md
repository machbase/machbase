---
type: docs
title: '2. 핵심 개념'
weight: 20
toc: true
---

Machbase의 데이터·시간·저장·Edition 모델을 이해합니다. 이 장은 동작 이유와 용어를
설명하며, 실제 테이블·컬럼·DML 설계는 4장에서 결정합니다.

## 이 장의 구성

| 절 | 내용 |
|---|---|
| [데이터 모델 개념](concepts/) | 시계열 데이터, 테이블 타입 역할, append와 시간 모델 |
| [저장 및 실행 구조](storage-execution-architecture/) | architecture, 컬럼 저장, index와 cache 원리 |
| [주요 기능 개념](features-concepts/) | ROLLUP, Retention, Backup·Restore·Mount의 역할 |
| [Edition 개념](concepts-edition/) | Standard와 Cluster의 구조·선택 기준 |
| [운영 개념 구분](terminology-distinction/) | Retention·삭제, Backup·Restore·Mount 구분 |

개념을 확인한 뒤 [테이블 타입 선택과 스키마 설계](/dbms/data-modeling-table-design/)로
이동하십시오.
