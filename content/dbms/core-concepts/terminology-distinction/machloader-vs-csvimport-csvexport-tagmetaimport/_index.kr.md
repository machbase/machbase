---
type: docs
title: 'machloader vs csvimport / csvexport vs tagmetaimport'
weight: 40
---

Machbase는 파일로 데이터를 적재하거나 내보내는 여러 도구를 제공합니다. 이름이 비슷해 혼동하기 쉽지만, 각 도구가 다루는 대상과 용도가 다릅니다.

## 비교 표

| 항목 | machloader | csvimport | csvexport | tagmetaimport |
| --- | --- | --- | --- | --- |
| 방향 | 입력 또는 반출 | 입력 전용 | 반출 전용 | 입력 전용 |
| 대상 테이블 | LOG, LOOKUP | LOG | 모든 테이블 | TAG (메타데이터) |
| 파일 형식 | CSV, 바이너리 등 | CSV | CSV | CSV |
| 적재 내용 | 행 데이터 | 행 데이터 | 행 데이터 | 태그 이름 및 속성 |
| 실행 위치 | 클라이언트 | 클라이언트 | 클라이언트 | 클라이언트 |
| 주요 특징 | 범용, 설정 파일 기반, 다양한 포맷 지원 | 단순 CSV 입력 | 단순 CSV 반출 | TAG 테이블 태그 목록 일괄 등록 |

## machloader

machloader는 LOG 테이블과 LOOKUP 테이블을 대상으로 파일에서 데이터를 적재하거나 반출하는 범용 도구입니다. CSV뿐 아니라 다양한 파일 형식을 지원하며, 설정 파일(`.mach`)로 컬럼 매핑, 구분자, 날짜 포맷 등을 세밀하게 제어할 수 있습니다.

```bash
# 적재 예시
machloader -i -t device_log -d /data/device_events.csv -f /conf/device_log.mach

# 반출 예시
machloader -o -t device_log -d /data/export.csv -f /conf/device_log.mach
```

데이터 양이 많거나 파일 포맷이 복잡할 때, 또는 컬럼 매핑이 필요한 경우 machloader를 사용합니다.

## csvimport / csvexport

csvimport와 csvexport는 단순한 CSV 파일 입출력 도구입니다. machloader보다 옵션이 적고 사용법이 간단합니다.

```bash
# CSV 파일 적재
csvimport -t device_log -d /data/device_events.csv

# CSV 파일 반출
csvexport -t device_log -d /data/export.csv
```

빠르게 소량의 CSV를 적재하거나 데이터를 확인 목적으로 내보낼 때 적합합니다. 복잡한 컬럼 매핑이나 변환이 필요하면 machloader를 사용합니다.

## tagmetaimport

tagmetaimport는 TAG 테이블의 태그 메타데이터(태그 이름과 사용자 정의 속성 컬럼 값)를 CSV 파일로 일괄 등록하는 도구입니다. 계측값 데이터(타임스탬프와 측정값)를 적재하는 것이 아니라, 태그 목록과 그 속성을 등록합니다.

```bash
# TAG 테이블에 태그 메타데이터 일괄 등록
tagmetaimport -t sensor_values -d /data/tag_list.csv
```

수천 개의 센서를 처음 등록하거나, 공정 라인 추가로 새 태그를 대량으로 등록할 때 사용합니다. 개별 태그 등록은 `INSERT INTO sensor_values (name) VALUES ('tag_name')` 으로도 가능하지만, 대량 등록에는 tagmetaimport가 효율적입니다.

## 선택 기준 요약

| 상황 | 권장 도구 |
| --- | --- |
| LOG 테이블에 CSV 대량 적재, 컬럼 매핑 필요 | machloader |
| LOG 테이블에 단순 CSV 소량 적재 | csvimport |
| 테이블 데이터 CSV 반출 | csvexport |
| TAG 테이블에 태그 이름/속성 일괄 등록 | tagmetaimport |
| 바이너리나 비CSV 포맷 파일 적재 | machloader |

## 다음 읽을 내용

- [LOAD DATA INFILE vs fastload](../load-data-infile-vs-fastload/) — SQL 기반 파일 적재 방법 비교
- [SDK append vs SQL APPEND vs Collector 수집](../ingestion-sdk-append-vs-sql-collector/) — 실시간 수집 경로 비교
