---
type: docs
title: '12.6 여러 파일과 압축 파일'
weight: 60
toc: true
---

파일 목록을 지정하기 전에 reader별 스키마 결합과 압축 지원을 확인합니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL FROM READ(
 '/srv/dfq/part-1.csv','/srv/dfq/part-2.csv','union_by_name=true');
SELECT COUNT(*) AS N,SUM(v) AS TOTAL FROM READ(
 'sources=/srv/dfq/part-1.csv,/srv/dfq/part-2.csv','union_by_name=true');
SELECT COUNT(*) AS N,SUM(v) AS TOTAL FROM READ(
 '/srv/dfq/part-*.csv','union_by_name=true');
```

샘플 두 파일은 각각 5행이므로 집계는 10·300입니다. 명시 목록은 입력 순서, glob은
준비한 정렬 순서를 사용합니다. 반환 표시 순서가 필요하면 바깥 ORDER BY를 지정합니다.
파일별 meta.source·filename의 지원도 포맷별로 확인합니다.

| 포맷 | 여러 입력·스키마 정책 |
|---|---|
| CSV/TSV | union_by_name으로 이름 기준 결합. 명시 타입과 누락 컬럼 정책 확인 |
| JSON/JSONL | 객체 키를 최초 등장 순서로 결합. type·표본 범위 확인 |
| NPY/NPZ/HDF5 | 타입·shape·선택 대상의 호환 조건 확인 |
| Parquet | 동일 선언 스키마 필요. union_by_name=true 미지원 |
| LeRobot | root 하나. 여러 dataset root 결합 미지원 |

일반 다중 파일은 최대 4,096개, strong source 집합은 최대 256개이며 reader의 더 작은
한도가 우선합니다. 스키마가 호환되지 않을 때 임의로 열 이름을 재배열하거나 타입을 승격하지 않습니다.

## 외부 압축과 컨테이너 내부 압축

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL FROM READ('/srv/dfq/sensor.csv.gz',
 'compression=gzip','type.v=LONG','parallel=false');
```

CSV/TSV·JSON/JSONL은 compression=auto/none/gzip/zstd를 사용합니다.
Parquet codec, NPZ member 압축, MCAP chunk 압축과 HDF5 filter는 각 컨테이너의 reader가
처리하며, 공통 compression=gzip을 무조건 붙이지 않습니다. NPY/NPZ의 외부 .gz wrapping은
지원하지 않습니다. 물리 stored raw와 source revision은 압축된 저장 바이트 기준입니다.

손상은 읽거나 해제한 범위에서 드러날 수 있습니다. LIMIT으로 일부를 성공적으로 읽었다고
전체 파일·전체 member의 무결성을 확인한 것은 아닙니다.
