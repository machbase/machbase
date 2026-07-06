---
type: docs
title: 'csvimport로 가져오기'
weight: 30
---

`csvimport`는 machloader를 CSV에 특화하여 래핑한 도구로, 옵션을 간소화하여 빠르게 CSV 파일을 적재할 수 있습니다.

## 기본 사용법

```bash
# 기본 형식
csvimport -t table_name -d data.csv

# 테이블명과 파일명을 위치 인자로 지정
csvimport table_name data.csv
csvimport data.csv table_name
```

## 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-t TABLE` | 대상 테이블 이름 |
| `-d FILE` | CSV 데이터 파일 |
| `-H` | 첫 줄을 헤더로 인식하여 입력 제외 |
| `-C` | 테이블 없으면 자동 생성 (컬럼명: c0, c1, ...) |
| `-m MODE` | append(기본)/replace |
| `-b FILE` | 실패 행 기록 파일 |
| `-l FILE` | 실행 로그 파일 |
| `-a` | `_ARRIVAL_TIME` 컬럼 포함 |
| `-P PORT` | 서버 포트 (기본: 5656) |
| `-F DATEFORMAT` | 날짜 형식 |
| `-I` | 상태 출력 최소화 |

## 예시

```bash
# 기본 적재
csvimport -t sensor_log -d sensor_data.csv

# 헤더 행 제외
csvimport -t sensor_log -d sensor_data.csv -H

# 오류 로그 저장
csvimport -t sensor_log -d sensor_data.csv \
    -l import.log -b import.bad

# 테이블 자동 생성 (헤더를 컬럼명으로)
csvimport -t new_table -d data.csv -C -H

# replace 모드 (기존 데이터 삭제 후 삽입)
csvimport -t sensor_log -d data.csv -m replace

# 날짜 형식 지정
csvimport -t sensor_log -d data.csv \
    -F "ts YYYY-MM-DD HH24:MI:SS"
```

## machloader와의 차이

`csvimport`는 `machloader -i`의 간편 래퍼입니다. machloader의 모든 옵션(`-D`, `-e`, `-f`, `-E` 등)을 그대로 사용할 수 있습니다.

```bash
# csvimport에서 machloader 확장 옵션 사용
csvimport -t sensor_log -d data.tsv -D '\t'
csvimport -t sensor_log -d data.csv -E MS949
```
