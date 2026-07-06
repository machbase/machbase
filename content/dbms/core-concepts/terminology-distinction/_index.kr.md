---
type: docs
title: '용어 구분'
weight: 50
---

Machbase DBMS를 처음 접하면 이름이 비슷하거나 역할이 겹쳐 보이는 개념들이 혼동을 일으킬 수 있습니다. 이 섹션은 실제 운영에서 자주 혼동되는 개념 쌍들을 비교 표와 함께 명확하게 구분합니다. 각 문서는 "어떤 상황에 무엇을 선택해야 하는가"에 대한 실용적인 답변을 제공합니다.

- **[ROLLUP vs STREAM](rollup-vs-stream/)** — 자동 집계와 SQL 기반 변환 처리의 차이
- **[Retention vs DELETE / TRUNCATE](retention-vs-delete-truncate/)** — 자동 정책과 수동 삭제 명령의 차이
- **[Backup vs Restore vs Mount](backup-vs-restore-mount/)** — 데이터 복사, 복원, 읽기 전용 연결의 차이
- **[machloader vs csvimport / csvexport vs tagmetaimport](machloader-vs-csvimport-csvexport-tagmetaimport/)** — 파일 기반 입출력 도구들의 차이
- **[LOAD DATA INFILE vs fastload](load-data-infile-vs-fastload/)** — SQL 기반 파일 적재와 고속 CSV 적재의 차이
- **[SDK append vs SQL APPEND vs Collector 수집](ingestion-sdk-append-vs-sql-collector/)** — 실시간 데이터 수집 경로별 특성과 선택 기준
