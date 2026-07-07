---
type: docs
title: 'SQL 기반 반출: SAVE DATA INTO'
weight: 20
---

`SAVE DATA INTO`는 SELECT 결과를 **서버 측 파일**로 직접 저장하는 SQL 구문입니다. machsql에서 실행하며 서버 프로세스가 파일을 생성합니다.

## 구문

```text
SAVE DATA INTO 'file_path'
[HEADER ON|OFF]
[(FIELDS | COLUMNS) [TERMINATED BY 'char'] [ENCLOSED BY 'char']]
[ENCODED BY coding_name]
AS select_query;
```

## 주요 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `HEADER ON/OFF` | OFF | 컬럼명 헤더 포함 여부 |
| `FIELDS TERMINATED BY` | `,` | 필드 구분자 |
| `ENCLOSED BY` | `"` | 필드 감싸기 문자 |
| `ENCODED BY` | UTF8 | 파일 인코딩 |

## 예시

```sql
-- 기본: SELECT 결과를 CSV로 저장
SAVE DATA INTO '/data/export/sensor_2024.csv'
AS SELECT * FROM sensor_log;

-- 헤더 포함
SAVE DATA INTO '/data/export/sensor_2024.csv'
HEADER ON
AS SELECT sensor_id, ts, value FROM sensor_log;

-- 조건부 반출
SAVE DATA INTO '/data/export/high_temp.csv'
HEADER ON
AS SELECT name, time, value FROM tag
WHERE name = 'TEMP-01'
  AND time BETWEEN '2024-01-01' AND '2024-01-31';

-- 구분자 변경
SAVE DATA INTO '/data/export/data.tsv'
FIELDS TERMINATED BY '\t'
AS SELECT * FROM sensor_log;

-- 인코딩 및 구분자 지정
SAVE DATA INTO '/data/export/result.csv'
HEADER ON
FIELDS TERMINATED BY ';' ENCLOSED BY '\''
ENCODED BY MS949
AS SELECT * FROM sensor_log WHERE value > 100;
```

## machsql에서 실행

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
Mach> SAVE DATA INTO '/data/export/result.csv' HEADER ON
   2> AS SELECT sensor_id, ts, value FROM sensor_log LIMIT 10000;
Saving data into /data/export/result.csv
10000 rows saved.
```

## 주의사항

- 파일 경로는 **서버 파일시스템** 기준입니다. 클라이언트 로컬 경로가 아닙니다.
- 기존 파일이 있으면 덮어씁니다.
- 서버 프로세스 계정에 해당 디렉터리 쓰기 권한이 필요합니다.
- 대용량 반출 시 디스크 여유 공간을 미리 확인하세요.
