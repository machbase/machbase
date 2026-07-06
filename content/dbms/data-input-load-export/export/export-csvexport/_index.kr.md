---
type: docs
title: 'csvexport로 내보내기'
weight: 40
---

`csvexport`는 machloader의 CSV 반출 전용 래퍼입니다. 옵션을 간소화하여 테이블 데이터를 빠르게 CSV로 내보낼 수 있습니다.

## 기본 사용법

```bash
# 기본 형식
csvexport -t table_name -d output.csv

# 위치 인자로 지정
csvexport table_name output.csv
csvexport output.csv table_name
```

## 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-t TABLE` | 내보낼 테이블 이름 |
| `-d FILE` | 저장할 CSV 파일 이름 |
| `-H` | 컬럼명을 CSV 헤더로 포함 |
| `-a` | `_ARRIVAL_TIME` 컬럼 포함 |
| `-l FILE` | 실행 로그 파일 |
| `-P PORT` | 서버 포트 (기본: 5656) |
| `-F DATEFORMAT` | 날짜 형식 |
| `-I` | 상태 출력 최소화 |

## 예시

```bash
# 기본 반출
csvexport -t sensor_log -d sensor_log.csv

# 헤더 포함
csvexport -t sensor_log -d sensor_log.csv -H

# _ARRIVAL_TIME 포함
csvexport -t sensor_log -d sensor_log.csv -a

# 로그 파일 생성
csvexport -t sensor_log -d sensor_log.csv -l export.log

# 조용히 실행 (배치 스크립트 사용 시)
csvexport -t sensor_log -d sensor_log.csv -I
```

## machloader와의 차이

`csvexport`는 `machloader -o`의 간편 래퍼입니다. machloader의 모든 옵션(`-D`, `-E`, `-f` 등)을 그대로 사용할 수 있습니다.

```bash
# csvexport에서 탭 구분자 사용
csvexport -t sensor_log -d export.tsv -D '\t'

# 특정 인코딩으로 내보내기
csvexport -t sensor_log -d export.csv -E MS949
```
