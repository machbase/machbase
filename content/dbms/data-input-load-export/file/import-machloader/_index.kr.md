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

## LOAD DATA INFILE (SQL 구문)

machsql이나 JDBC/ODBC에서 직접 SQL로 CSV 파일을 가져올 수 있습니다.

### 문법

```sql
LOAD DATA INFILE 'file_name'
INTO TABLE table_name
[TABLESPACE tbs_name]
[AUTO (BULKLOAD | HEADUSE | HEADUSE_ESCAPE)]
[(FIELDS | COLUMNS) [TERMINATED BY 'char'] [ENCLOSED BY 'char']]
[TRIM (ON | OFF)]
[IGNORE number (LINES | ROWS)]
[MAX_LINE_LENGTH number]
[ENCODED BY coding_name]
[ON ERROR (STOP | IGNORE)];
```

### 옵션 설명

| 옵션 | 설명 |
|------|------|
| `AUTO BULKLOAD` | 한 행을 하나의 컬럼으로 입력. 컬럼 구분이 불필요한 원시 데이터에 사용 |
| `AUTO HEADUSE` | 파일의 첫 번째 줄을 컬럼명으로 사용하여 테이블 자동 생성 |
| `AUTO HEADUSE_ESCAPE` | HEADUSE와 동일하나 예약어 충돌을 피하기 위해 컬럼명 앞뒤에 `_` 추가, 특수문자는 `_`로 치환 |
| `FIELDS TERMINATED BY 'char'` | 필드 구분자 지정 (기본값: `,`) |
| `ENCLOSED BY 'char'` | 필드 감싸기 문자 지정 (기본값: `"`) |
| `TRIM (ON\|OFF)` | 공백 제거 여부. 기본값 ON |
| `IGNORE n LINES\|ROWS` | 처음 n줄 무시 (헤더 건너뛰기에 사용) |
| `MAX_LINE_LENGTH n` | 한 줄의 최대 길이 지정. 기본값 512K |
| `ENCODED BY` | 파일 인코딩 지정: UTF8(기본), MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280 |
| `ON ERROR STOP\|IGNORE` | 오류 발생 시 중단(STOP) 또는 해당 줄 건너뛰기(IGNORE). 기본값 IGNORE |

### 예시

```sql
-- 기본 CSV 입력 (쉼표 구분자, 큰따옴표 감싸기)
LOAD DATA INFILE '/tmp/aaa.csv' INTO TABLE sample_data;

-- 한 줄을 하나의 컬럼으로 입력
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE newtable AUTO BULKLOAD;

-- 첫 번째 줄을 컬럼명으로 사용하여 테이블 자동 생성
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE newtable AUTO HEADUSE;

-- 첫 번째 줄 무시, 세미콜론 구분자, 작은따옴표 감싸기, 오류 무시
LOAD DATA INFILE '/tmp/ccc.csv' INTO TABLE sample_data
FIELDS TERMINATED BY ';' ENCLOSED BY '\''
IGNORE 1 LINES ON ERROR IGNORE;

-- EUC-KR 인코딩 파일 입력
LOAD DATA INFILE '/tmp/data_kr.csv' INTO TABLE sample_data
ENCODED BY MS949;
```

> AUTO 옵션을 사용하지 않는 경우, 대상 테이블의 모든 컬럼은 VARCHAR 또는 TEXT 타입으로 생성되어 있어야 합니다.
