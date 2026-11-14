---
type: docs
title: '12.4 포맷별 상세 사용법'
weight: 40
toc: true
---

지원 포맷의 옵션·제약·조합 예제를 확인합니다. 같은 옵션 이름이라도 reader마다 기본값과
허용 조합이 다릅니다. 포맷을 선택한 뒤 해당 페이지의 작업별 빠른 찾기를 사용합니다.

| 포맷 | 선택 기준 |
|---|---|
| [CSV](./csv/) | 구분자·헤더·인코딩과 컬럼 타입을 조합해 행을 읽습니다 |
| [TSV](./tsv/) | 탭으로 구분된 입력을 독립적인 TSV 형식으로 읽습니다 |
| [JSON](./json/) | 객체는 한 행, 최상위 배열은 원소별 행으로 읽습니다 |
| [JSONL](./jsonl/) | 각 비어 있지 않은 줄을 부모 레코드로 읽습니다 |
| [PARQUET](./parquet/) | 선언된 컬럼 타입과 중첩 STRUCT/LIST를 보존해 조회합니다 |
| [NPY](./npy/) | NumPy 배열의 dtype과 shape에 따라 SQL 행·컬럼을 만듭니다 |
| [NPZ](./npz/) | ZIP 안의 NPY 배열을 선택해 조회합니다 |
| [MCAP](./mcap/) | 파일 안의 메시지·토픽·스키마·첨부·메타데이터를 선택합니다 |
| [HDF5](./hdf5/) | dataset 하나 또는 같은 group의 직계 dataset들을 컬럼으로 묶어 조회합니다 |
| [LeRobot](./lerobot/) | 서버에 준비한 LeRobot v2 |
