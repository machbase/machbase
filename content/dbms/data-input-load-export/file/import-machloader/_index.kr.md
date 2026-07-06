---
type: docs
title: 'machloader로 가져오기'
weight: 20
---

`machloader`는 CSV 파일을 Machbase 서버로 가져오거나 내보내는 범용 CLI 도구입니다. 스키마 파일을 통해 컬럼 매핑, 날짜 형식, 특정 컬럼 무시 등 유연한 설정이 가능합니다.

## 기본 가져오기

```bash
machloader -i -d data.csv -t sensor_log
```

| 옵션 | 설명 |
|------|------|
| `-i` | 가져오기 (import) 모드 |
| `-d data.csv` | 데이터 파일 지정 |
| `-t sensor_log` | 대상 테이블 이름 |

## 자주 쓰는 옵션

```bash
# 접속 정보 지정
machloader -i -d data.csv -t sensor_log \
    -s 192.168.1.10 -P 5656 -u SYS -p MANAGER

# 헤더 행 건너뛰기
machloader -i -d data.csv -t sensor_log -H

# 로그/bad 파일 생성
machloader -i -d data.csv -t sensor_log \
    -l sensor_log.log -b sensor_log.bad

# 기존 데이터 삭제 후 입력 (replace 모드)
machloader -i -d data.csv -t sensor_log -m replace

# 탭 구분자
machloader -i -d data.tsv -t sensor_log -D '\t'

# 인코딩 지정
machloader -i -d data.csv -t sensor_log -E MS949

# _ARRIVAL_TIME 컬럼 포함
machloader -i -d data.csv -t sensor_log -a
```

## DATETIME 형식 지정

`-F` 옵션으로 날짜 형식을 지정합니다.

```bash
# 컬럼명과 날짜 형식 지정
machloader -i -d data.csv -t sensor_log \
    -F "ts YYYY-MM-DD HH24:MI:SS"

# Unix 타임스탬프
machloader -i -d data.csv -t sensor_log \
    -F "ts unixtimestamp"

# 나노초 타임스탬프
machloader -i -d data.csv -t sensor_log \
    -F "ts nanotimestamp"
```

## 스키마 파일 사용

스키마 파일로 컬럼 타입, 날짜 형식, 특정 컬럼 무시를 세밀하게 제어합니다.

### 스키마 파일 자동 생성

```bash
machloader -c -t sensor_log -f sensor_log.fmt
```

### 스키마 파일 형식

```text
table sensor_log
{
    sensor_id varchar(40);
    ts        datetime;
    value     double;
    status    varchar(20) IGNORE;  -- 이 컬럼은 CSV에 있지만 무시
}
DATEFORMAT ts "YYYY-MM-DD HH24:MI:SS"
```

### 스키마 파일로 가져오기

```bash
machloader -i -f sensor_log.fmt -d data.csv
```

## 자동 테이블 생성

테이블이 없을 때 자동 생성합니다. 컬럼 타입은 `varchar(32767)`로 생성됩니다.

```bash
# 컬럼명 c0, c1, ... 자동 생성
machloader -i -d data.csv -t auto_table -C

# CSV 헤더를 컬럼명으로 사용
machloader -i -d data.csv -t auto_table -C -H
```

## 옵션 전체 목록

```bash
machloader -h
```

| 주요 옵션 | 설명 |
|----------|------|
| `-s SERVER` | 서버 IP (기본: 127.0.0.1) |
| `-u USER` | 사용자 (기본: SYS) |
| `-p PASSWORD` | 비밀번호 (기본: MANAGER) |
| `-P PORT` | 포트 (기본: 5656) |
| `-i` | 가져오기 모드 |
| `-o` | 내보내기 모드 |
| `-d FILE` | 데이터 파일 |
| `-f FILE` | 스키마 파일 |
| `-t TABLE` | 테이블 이름 |
| `-l FILE` | 로그 파일 |
| `-b FILE` | 실패 행 기록 파일 |
| `-m MODE` | append(기본)/replace |
| `-D CHAR` | 필드 구분자 |
| `-e CHAR` | 필드 감싸기 문자 |
| `-H` | 헤더 행 처리 |
| `-C` | 자동 테이블 생성 |
| `-a` | `_ARRIVAL_TIME` 포함 |
| `-E ENCODING` | 파일 인코딩 |
| `-F DATEFORMAT` | 날짜 형식 지정 |
| `-z TIMEZONE` | 타임존 (예: +0900) |
