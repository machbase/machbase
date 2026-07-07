---
type: docs
title: 'machloader 로그'
weight: 40
---

`machloader`는 CSV, TXT 등의 파일을 Machbase에 대량 적재하는 도구입니다. 실행 중에 발생한 오류와 통계 정보를 로그 파일에 기록합니다.

## 로그 파일 종류

machloader는 실행 시 현재 작업 디렉터리에 두 개의 로그 파일을 생성합니다.

| 파일 이름 | 용도 |
|---------|------|
| `machloader.log` | 적재 통계 (처리 건수, 오류 건수, 소요 시간) |
| `machloader.err` | 오류가 발생한 레코드와 오류 메시지 |

로그 파일 이름은 `-l` 옵션으로 변경할 수 있습니다.

```bash
# 기본 로그 파일명 사용
machloader -i -t sensor_log -d data.csv -f csv

# 사용자 지정 로그 파일명
machloader -i -t sensor_log -d data.csv -f csv -l /logs/load_20240115
# /logs/load_20240115.log, /logs/load_20240115.err 생성
```

## machloader.log — 적재 통계

적재 완료 후 처리 현황 요약이 기록됩니다.

```
Mach Load Started...
Total: 1000000 records
Loaded: 998523 records
Error: 1477 records
Elapsed: 45.23 seconds
Load rate: 22082 records/sec
```

| 항목 | 설명 |
|------|------|
| Total | 입력 파일의 전체 레코드 수 |
| Loaded | 성공적으로 적재된 레코드 수 |
| Error | 오류로 처리하지 못한 레코드 수 |
| Elapsed | 총 소요 시간 |
| Load rate | 초당 처리 건수 |

## machloader.err — 오류 레코드

적재에 실패한 레코드의 원본 데이터와 오류 이유가 기록됩니다.

```
[2024-01-15 10:23:45] Line=1024, Error=Column type mismatch: column=temperature, value=N/A
2024-01-15T10:00:00,sensor-001,N/A,60.5

[2024-01-15 10:23:45] Line=2048, Error=Timestamp out of range: column=_arrival_time
2024-01-15T25:00:00,sensor-002,25.3,60.1
```

오류 메시지와 함께 원본 레코드가 기록되므로, 오류 레코드를 수정하여 재처리할 수 있습니다.

## 오류 레코드 재처리

오류 레코드를 수정하여 재적재하는 절차입니다.

```bash
# 1단계: 오류 레코드 추출 (짝수 줄 = 원본 데이터)
grep -v '^\[' machloader.err > error_records.csv

# 2단계: 오류 원인 분석
grep 'Error=' machloader.err | sort | uniq -c | sort -rn

# 3단계: 데이터 수정 후 재적재
machloader -i -t sensor_log -d error_records_fixed.csv -f csv
```

## 오류 허용 설정

적재 중 오류가 발생해도 계속 진행하려면 `-e` 옵션으로 허용할 오류 건수를 지정합니다.

```bash
# 오류 100건까지 허용하고 계속 진행
machloader -i -t sensor_log -d data.csv -f csv -e 100

# 오류 건수 제한 없이 계속 진행 (0 = 무제한)
machloader -i -t sensor_log -d data.csv -f csv -e 0
```

## 주요 적재 오류 유형

| 오류 유형 | 원인 | 조치 |
|---------|------|------|
| Column type mismatch | 데이터 타입 불일치 (문자열 → 숫자 등) | 소스 데이터 형식 확인 및 수정 |
| Timestamp out of range | 유효하지 않은 날짜/시간 값 | 타임스탬프 형식과 범위 확인 |
| String too long | 문자열이 컬럼 최대 길이 초과 | 테이블 컬럼 길이 확인 또는 데이터 트리밍 |
| Duplicate primary key | 기본키 중복 (Fixed/Lookup 테이블) | 중복 레코드 제거 후 재적재 |

## 적재 성능 모니터링

대용량 파일 적재 중 진행 상황을 확인합니다.

```bash
# 적재 중 처리 건수 실시간 확인 (다른 터미널에서)
tail -f machloader.log

# 오류 레코드 실시간 확인
tail -f machloader.err
```

적재 완료 후에는 오류 건수를 반드시 확인하고, 오류 비율이 높으면 소스 데이터 품질을 점검하십시오.
