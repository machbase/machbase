---
type: docs
title: '17.4.5 tagmetaimport 명령/옵션 사전'
weight: 50
toc: true
---

`tagmetaimport`는 TAG 테이블의 메타데이터를 CSV 파일에서 일괄 가져오는 도구입니다. 대량의 TAG 이름과 메타데이터를 한 번에 등록할 때 사용합니다.

## 옵션 목록

```bash
tagmetaimport -h
```

| 옵션 | 설명 |
|------|------|
| `-s`, `--server=SERVER` | 서버 IP 주소 (기본값: 127.0.0.1) |
| `-P`, `--port=PORT` | 서버 포트 번호 (기본값: 5656) |
| `-u`, `--user=USER` | 사용자 이름 (기본값: SYS) |
| `-p`, `--password=PASSWORD` | 사용자 비밀번호 (기본값: MANAGER) |
| `-t`, `--table=TABLE_NAME` | 대상 TAG 테이블 이름 |
| `-d`, `--data=DATA_FILE` | 메타데이터 CSV 파일 경로 |
| `-l`, `--log=LOG_FILE` | 로그 파일 경로 |
| `-b`, `--bad=BAD_FILE` | 입력 실패 레코드 저장 파일 경로 |
| `-H`, `--header` | CSV 파일의 첫 번째 행을 헤더로 인식 |
| `-D`, `--delimiter=DELIMITER` | 필드 구분자 (기본값: `,`) |
| `-E`, `--encoding=CHARSET` | 파일 인코딩 (기본값: UTF8) |
| `-I`, `--silent` | 배너 및 상태 출력 없이 실행 |
| `-h`, `--help` | 옵션 목록 출력 |

## 입력 파일 형식

메타데이터 CSV 파일은 TAG 테이블의 메타 컬럼 순서에 맞게 작성합니다.

TAG 테이블 정의 예시:

```sql
CREATE TAG TABLE sensor_tag (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE      SUMMARIZED,
    unit   VARCHAR(32),
    location VARCHAR(128)
);
```

이 테이블의 메타데이터 CSV 파일 (`tag_meta.csv`):

```
name,unit,location
sensor_001,celsius,Building-A Floor-1
sensor_002,celsius,Building-A Floor-2
sensor_003,bar,Boiler-Room
sensor_004,rpm,Motor-Section
```

헤더 없이 데이터만 있는 경우:

```
sensor_001,celsius,Building-A Floor-1
sensor_002,celsius,Building-A Floor-2
```

## 사용 예시

### 기본 가져오기

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t sensor_tag -d tag_meta.csv
```

### 헤더가 있는 CSV 파일 가져오기

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t sensor_tag -d tag_meta.csv -H
```

### 원격 서버에 가져오기

```bash
tagmetaimport -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -t sensor_tag -d tag_meta.csv -H
```

### 탭 구분자 파일

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t sensor_tag -d tag_meta.tsv -D '\t' -H
```

### EUC-KR 인코딩 파일

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t sensor_tag -d tag_meta_kr.csv -E MS949 -H
```

## 동작 방식

- `tagmetaimport`는 내부적으로 TAG 테이블의 메타 영역(`_TAG_META`)에 데이터를 삽입합니다.
- 이미 존재하는 TAG 이름(Primary Key)이 있으면 해당 행은 건너뜁니다.
- 데이터가 입력된 이후에 메타데이터를 추가하려는 경우 이 도구를 사용하면 효율적입니다.
- 소량의 메타데이터는 SQL INSERT 또는 `machsql`에서 직접 입력할 수도 있습니다.

```sql
-- machsql에서 직접 메타데이터 삽입
INSERT INTO sensor_tag (name, unit, location)
VALUES ('sensor_005', 'volt', 'Panel-Room');
```

## 주의 사항

- TAG 테이블이 사전에 생성되어 있어야 합니다.
- CSV 파일의 컬럼 순서는 TAG 테이블의 메타 컬럼 순서와 일치해야 합니다.
- `BASETIME` 컬럼(`time`)과 `SUMMARIZED` 컬럼(`value`)은 메타데이터 파일에 포함하지 않습니다.
