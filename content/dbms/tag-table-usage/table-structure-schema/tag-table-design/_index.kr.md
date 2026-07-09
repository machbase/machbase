---
type: docs
title: 'TAG 테이블 설계'
weight: 20
---

TAG 테이블은 센서·IoT 기기의 계측값을 저장하는 시계열 전용 테이블입니다. 태그(센서) 이름을 `PRIMARY KEY`로, 시간 또는 거리 기준 컬럼을 축으로 대량의 시계열 데이터를 효율적으로 저장합니다.

- **[시간축 TAG 테이블 설계](/dbms/tag-table-usage/time-distance-axis/time-axis-design-tag/)**
- **[거리축 TAG 테이블 설계](/dbms/tag-table-usage/time-distance-axis/distance-axis-design-tag/)**
- **[활용 사례](/dbms/tag-table-usage/patterns-scenarios/use-cases-tag/)**
- **[METADATA 설계](/dbms/tag-table-usage/tag-metadata/metadata-design-tag/)**
- **[JSON METADATA 설계](/dbms/tag-table-usage/tag-metadata/metadata-design-json/)**
- **[값 컬럼 설계](/dbms/tag-table-usage/table-structure-schema/tag-table-design/design-column/)**
- **[이진 데이터 컬럼 설계](/dbms/tag-table-usage/table-structure-schema/tag-table-design/design-column-binary/)**
- **[VARCHAR 스토리지 최적화](/dbms/tag-table-usage/table-structure-schema/tag-table-design/storage-varchar/)**
- **[스토리지 전략](/dbms/tag-table-usage/table-structure-schema/tag-table-design/strategy/)**
- **[데이터 보정 설계](/dbms/tag-table-usage/tag-data-update-correction/design-correction-tag/)**
- **[LSL·USL 설계](/dbms/tag-table-usage/table-structure-schema/tag-table-design/lsl-usl/)**
- **[제약 및 주의사항](/dbms/tag-table-usage/constraints-errors-troubleshooting/limitations-tag/)**
- **[자동 중복 제거](/dbms/tag-table-usage/table-structure-schema/tag-table-design/duplication-removal/)**
