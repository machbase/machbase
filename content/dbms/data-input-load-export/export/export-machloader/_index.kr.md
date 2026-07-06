---
type: docs
title: 'machloader로 내보내기'
weight: 30
---

`machloader -o` 옵션으로 테이블 데이터를 클라이언트 파일시스템의 CSV 파일로 내보냅니다.

## 기본 내보내기

```bash
machloader -o -d export.csv -t sensor_log
```

| 옵션 | 설명 |
|------|------|
| `-o` | 내보내기 (export) 모드 |
| `-d export.csv` | 저장할 파일 이름 |
| `-t sensor_log` | 대상 테이블 이름 |

## 주요 옵션

```bash
# 접속 정보 지정
machloader -o -d export.csv -t sensor_log \
    -s 192.168.1.10 -P 5656 -u SYS -p MANAGER

# 헤더 포함
machloader -o -d export.csv -t sensor_log -H

# _ARRIVAL_TIME 컬럼 포함
machloader -o -d export.csv -t sensor_log -a

# 탭 구분자
machloader -o -d export.tsv -t sensor_log -D '\t'

# 인코딩 지정
machloader -o -d export.csv -t sensor_log -E MS949

# 실행 로그
machloader -o -d export.csv -t sensor_log -l export.log
```

## 스키마 파일과 함께 내보내기

컬럼 순서 변경이나 특정 컬럼만 내보낼 때 스키마 파일을 사용합니다.

```bash
# 스키마 파일 자동 생성
machloader -c -t sensor_log -f sensor_log.fmt

# 스키마 파일로 내보내기
machloader -o -f sensor_log.fmt -d export.csv
```

스키마 파일에서 `IGNORE` 키워드를 사용하여 특정 컬럼 제외:

```text
table sensor_log
{
    sensor_id varchar(40);
    ts        datetime;
    value     double;
    status    varchar(20) IGNORE;  -- 내보내기에서 제외
}
```

## 결과 확인

```
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 8.6.0
Copyright 2014, MACHBASE Corporation or its subsidiaries.
All Rights Reserved.
-----------------------------------------------------------------
Export time : 0 hour 0 min 2.35 sec
Export success count : 1000000
```

## 주의사항

- 파일은 클라이언트 실행 경로 또는 지정한 경로에 생성됩니다.
- 기존 파일이 있으면 덮어씁니다.
- 대용량 테이블을 내보낼 때는 `-I` 옵션(silent)으로 진행 출력을 줄일 수 있습니다.
