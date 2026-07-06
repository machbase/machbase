---
type: docs
title: '대량 입력 오류 처리'
weight: 20
---

대량 입력 중 발생할 수 있는 오류 유형과 처리 방법을 정리합니다.

## 오류 유형

| 오류 유형 | 원인 | 처리 방법 |
|----------|------|---------|
| 타입 불일치 | CSV 값이 컬럼 타입과 맞지 않음 | bad 파일로 분리, 전처리 후 재시도 |
| VARCHAR 초과 | 값이 컬럼 최대 길이 초과 | 자동 잘림 또는 오류 기록 |
| NULL 제약 위반 | NOT NULL 컬럼에 NULL 값 | bad 파일로 분리 |
| 중복 PK | LOOKUP/VOLATILE에서 PK 중복 | UPSERT 또는 사전 정리 |
| 날짜 형식 오류 | DATETIME 파싱 실패 | `-F` 옵션으로 형식 명시 |

## machloader: bad 파일과 로그 파일

```bash
machloader -i -d data.csv -t sensor_log \
    -b sensor_log.bad \
    -l sensor_log.log
```

- **bad 파일 (`-b`)**: 입력 실패한 원본 행을 기록
- **로그 파일 (`-l`)**: 실패 행의 오류 메시지를 기록

```bash
# 실행 후 결과 확인
# sensor_log.log 예시:
# Row 15: Type mismatch on column 'value'
# Row 42: NULL value in NOT NULL column 'sensor_id'

# bad 파일로 실패 데이터 확인 및 수정 후 재시도
vi sensor_log.bad
machloader -i -d sensor_log.bad -t sensor_log
```

## LOAD DATA INFILE: ON ERROR 옵션

```sql
-- 오류 발생 시 중단 (기본: IGNORE)
LOAD DATA INFILE '/data/sensor.csv' INTO TABLE sensor_log
ON ERROR STOP;

-- 오류 발생 시 해당 행 건너뛰고 계속 진행 (기본값)
LOAD DATA INFILE '/data/sensor.csv' INTO TABLE sensor_log
ON ERROR IGNORE;
```

## Append API: 실패 건수 확인

```go
success, fail, err := appender.Close()
if fail > 0 {
    log.Printf("Input failed: %d rows", fail)
    // 실패 행 재처리 로직
}
```

Append API는 실패한 개별 행에 대한 상세 오류 정보를 반환하지 않습니다. 실패 건수가 많을 경우 배치 크기를 줄이거나 SQL INSERT로 전환하여 오류를 추적하세요.

## INSERT SELECT 오류 처리

INSERT SELECT는 중간에 오류가 발생해도 ROLLBACK되지 않습니다.

```sql
-- 오류가 있어도 성공한 행은 유지됨
INSERT INTO archive_log
SELECT * FROM sensor_log WHERE ts < '2024-01-01';

-- 오류 확인
SELECT COUNT(*) FROM archive_log;
```

## 재시도 패턴

```bash
# bad 파일 오류 수정 후 재시도
# 1. bad 파일 검토
head -20 sensor_log.bad

# 2. 문제 있는 행 수정 (sed, awk 등 활용)
sed 's/incorrect_value/correct_value/' sensor_log.bad > sensor_log_fixed.csv

# 3. 수정된 파일 재시도
machloader -i -d sensor_log_fixed.csv -t sensor_log \
    -b sensor_log_fixed.bad -l sensor_log_fixed.log
```

## 입력 검증 권장 사항

- 대량 입력 전에 소량 샘플로 테스트 입력을 수행하세요.
- DATETIME 형식은 `-F` 옵션 또는 스키마 파일로 명시적으로 지정하세요.
- VARCHAR 컬럼 길이를 사전에 확인하고 데이터를 전처리하세요.
- bad 파일을 반드시 지정하여 실패 데이터를 보존하세요.
