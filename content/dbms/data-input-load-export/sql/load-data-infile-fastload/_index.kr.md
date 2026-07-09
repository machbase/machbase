---
type: docs
title: 'LOAD DATA INFILE'
weight: 30
---

`LOAD DATA INFILE`은 **서버에 위치한** CSV 파일을 SQL 한 줄로 직접 적재하는 구문입니다. 클라이언트에서 파일을 전송하는 machloader와 달리, 서버 프로세스가 직접 파일을 읽어 처리합니다.

## 기본 구문

```sql
LOAD DATA INFILE 'file_path'
INTO TABLE table_name
[AUTO {BULKLOAD | HEADUSE | HEADUSE_ESCAPE}]
[(FIELDS | COLUMNS) [TERMINATED BY 'char'] [ENCLOSED BY 'char']]
[LINES TERMINATED BY 'char']
[TRIM {ON | OFF}]
[IGNORE number LINES]
[MAX_LINE_LENGTH number]
[ENCODED BY coding_name]
[ON ERROR {STOP | IGNORE}];
```

## 주요 옵션

| 옵션 | 설명 |
|------|------|
| `AUTO BULKLOAD` | 한 행 전체를 하나의 컬럼으로 입력 (컬럼 구분 없는 원시 데이터) |
| `AUTO HEADUSE` | CSV 첫 줄을 컬럼명으로 사용하여 자동 테이블 생성 |
| `AUTO HEADUSE_ESCAPE` | HEADUSE와 동일하나, 예약어·특수문자 컬럼명에 `_` 처리 |
| `FIELDS TERMINATED BY` | 필드 구분자 (기본값: `,`) |
| `ENCLOSED BY` | 필드 감싸는 문자 (기본값: `"`) |
| `LINES TERMINATED BY` | 줄 구분자 |
| `TRIM ON/OFF` | 공백 제거 여부 (기본값: ON) |
| `IGNORE N LINES` | 첫 N줄 무시 (헤더 건너뛰기) |
| `MAX_LINE_LENGTH` | 한 줄 최대 길이 (기본값: 512KB) |
| `ENCODED BY` | 파일 인코딩 (기본값: UTF8) |
| `ON ERROR STOP/IGNORE` | 오류 시 중단 또는 건너뜀 (기본값: STOP) |

## 예시

```sql
-- 기본: 기본 구분자(,)로 sensor_log 테이블에 입력
LOAD DATA INFILE '/data/sensor_2024.csv' INTO TABLE sensor_log;

-- 헤더 1줄 건너뛰기
LOAD DATA INFILE '/data/sensor_2024.csv' INTO TABLE sensor_log
IGNORE 1 LINES;

-- 탭 구분자
LOAD DATA INFILE '/data/sensor_2024.tsv' INTO TABLE sensor_log
FIELDS TERMINATED BY '\t';

-- 오류 발생 시 중단
LOAD DATA INFILE '/data/critical.csv' INTO TABLE orders
ON ERROR STOP;

-- 자동 테이블 생성 (첫 줄을 컬럼명으로)
LOAD DATA INFILE '/data/new_data.csv' INTO TABLE auto_table
AUTO HEADUSE;

-- 인코딩 지정
LOAD DATA INFILE '/data/korean.csv' INTO TABLE sensor_log
ENCODED BY MS949;
```

## machsql에서 실행

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
Mach> LOAD DATA INFILE '/data/sensor_2024.csv' INTO TABLE sensor_log;
Load success count : 1000000
Load fail count    : 0
```

## 클라이언트 적재 도구와 비교

| 항목 | LOAD DATA INFILE | machloader |
|------|-----------------|-----------|
| 파일 위치 | 서버 파일시스템 | 클라이언트 파일시스템 |
| 실행 방법 | SQL 구문 | CLI 명령 |
| 스키마 파일 | 불필요 | 필요 시 사용 |
| 자동 테이블 생성 | O (AUTO 옵션) | O (-C 옵션) |

## 주의사항

- 파일 경로는 **Machbase 서버 프로세스**가 접근 가능한 경로여야 합니다.
- 원격 클라이언트에서 실행할 경우, 서버 로컬 경로를 기준으로 파일을 미리 복사해 두어야 합니다.
- 파일이 매우 클 경우 `MAX_LINE_LENGTH`를 적절히 늘려야 합니다.
