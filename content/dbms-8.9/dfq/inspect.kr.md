---
type: docs
title: '12.2 파일 구조와 컬럼 확인하기'
weight: 20
toc: true
---

파일을 처음 받았을 때는 내부 대상과 실제 반환 컬럼을 먼저 확인합니다.

## DESC와 도움말

```sql
DESC '/srv/dfq/sensor.csv';
DESC '/srv/dfq/arrays.npz';
DESC '/srv/dfq/sensor.h5';
DESC '/srv/dfq/lerobot/v30';
HELP READ;
HELP READ CSV;
HELP READ SQL;
```

HELP는 machsql의 정적 도움말입니다. 파일을 열어 검사하지 않으며 서버의 실제 지원 여부를
대신하지 않습니다. DESC는 서버의 파일 접근 권한과 reader를 사용해 실제 구조를 읽습니다.
파일 설명에는 FILE·SOURCE MAP·STRUCTURE·COLUMNS·HELP·NOTES 등의 정보가 표시됩니다.

```text
파일/데이터셋
 ├─ NPZ: main.npy → array=main
 ├─ HDF5: /records → dataset=/records
 │         /table → group=/table
 └─ LeRobot: data → target=steps
              meta → target=episodes / tasks
              미디어 참조 → target=media
```

LeRobot의 `[reference; not opened]`는 미디어 파일을 실제로 읽어 확인했다는 뜻이 아닙니다.
DESC는 dataset의 선언과 이미 연 metadata/data의 연결을 보여 줍니다.

## 목적별 탐색

| 목적 | 호출 옵션 | 확인할 내용 |
|---|---|---|
| 조회 대상 목록 | mode=list | 정확한 target ID와 capability·이유 |
| 논리 구조 | mode=schema | 원본 타입·필드·shape와 SQL 표현 |
| SQL 결과 컬럼 | mode=inspect, view=columns | COLUMN_NAME·SQL_TYPE·크기·NULLABLE |
| 선언 필드 경로 | mode=inspect, view=fields | 원래 경로·지원 여부·재조회 SQL |
| 적용 가능한 옵션 | mode=inspect, view=options | 기본값과 허용값 |
| 유효 설정 | mode=inspect, view=option_values | 현재 호출에 적용한 설정 |
| 읽기 진단 | mode=inspect, view=diagnostics | 미지원·부분 탐색의 이유 |

```sql
SELECT * FROM READ('/srv/dfq/sensor.csv','mode=list');
SELECT COLUMN_NAME,SQL_TYPE FROM READ('/srv/dfq/sensor.csv',
 'mode=inspect','view=columns') ORDER BY COLUMN_ORDINAL;
SELECT * FROM READ('/srv/dfq/arrays.npz','mode=inspect','view=arrays');
SELECT DATASET,KIND,DTYPE,SHAPE FROM READ('/srv/dfq/sensor.h5',
 'mode=inspect','view=datasets');
```

mode=list의 ROW_COUNT가 NULL이면 행 수를 빠르게 확정하지 못했다는 뜻입니다.
READABLE과 작업별 capability를 확인하고 unknown을 지원으로 해석하지 않습니다.
목록의 정확한 target·경로를 사용합니다. 이름·대소문자·슬래시를 임의로 바꾸지 않습니다.

## 선택 옵션을 유지한 컬럼 확인

```sql
SELECT COLUMN_NAME,SQL_TYPE FROM READ('/srv/dfq/sensor.h5',
 'dataset=/records','mode=inspect','view=columns') ORDER BY COLUMN_ORDINAL;
```

기본 target과 선택한 target의 컬럼이 다를 수 있습니다. projection·이름·타입·target을
실제 조회와 같게 지정합니다. 바깥 SELECT의 집계·표현식 결과 컬럼은 JDBC 메타데이터나
SQLDescribeCol 등 클라이언트 API로 확인합니다.

inspect view=describe는 구조화된 파일 설명이며 view=describe_text는 SOURCE MAP을 포함한
화면용 설명입니다. view=structure를 모든 포맷의 일반 구조 조회로 사용하지 않습니다.
HDF5의 내부 구조와 파일 설명의 용도는 [HDF5](../formats/hdf5/)에서 구분합니다.
