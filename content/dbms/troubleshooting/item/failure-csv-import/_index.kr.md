---
type: docs
title: 'CSV import가 실패할 때'
weight: 20
---

machloader를 사용한 CSV 파일 가져오기가 실패하는 경우 대부분 파일 경로, 컬럼 수, 인코딩, 구분자, 날짜 형식 중 하나가 원인입니다. 오류 로그 파일을 먼저 확인한 뒤 해당 옵션을 조정하면 대부분의 문제를 해결할 수 있습니다.

## 오류 로그 확인

machloader 실행 후 현재 디렉토리에 오류 파일이 생성됩니다.

```bash
# machloader 실행 후 오류 파일 확인
cat machloader_error.txt
```

오류 메시지에 행 번호와 오류 원인이 기록되어 있습니다. 이 정보를 단서로 삼아 아래 항목 중 해당하는 원인을 찾으십시오.

## 원인별 진단 및 해결

### 1. 파일 경로 오류

```
ERR: cannot open file '/path/to/data.csv'
```

상대 경로를 사용하면 machloader를 실행하는 디렉토리에 따라 경로가 달라질 수 있습니다. 절대 경로를 사용하십시오.

```bash
# 잘못된 예 (상대 경로)
machloader -i -t sensor_log -d data.csv

# 올바른 예 (절대 경로)
machloader -i -t sensor_log -d /data/import/sensor_log_20240101.csv
```

### 2. 컬럼 수 불일치

```
ERR: column count mismatch at line 5
```

CSV 파일의 컬럼 수가 테이블의 컬럼 수와 맞지 않을 때 발생합니다.

```bash
# CSV 첫 번째 행(헤더) 확인
head -1 /data/import/sensor_log.csv

# 테이블 컬럼 확인
machsql -e "DESC sensor_log"
```

CSV에 헤더 행이 포함되어 있다면 `-H` 옵션을 추가합니다.

```bash
machloader -i -t sensor_log -d data.csv -H
```

### 3. 인코딩 문제

```
ERR: invalid character sequence at line 12
```

한글 등 멀티바이트 문자가 포함된 CSV 파일에서 인코딩이 맞지 않으면 오류가 발생합니다. `-E` 옵션으로 인코딩을 명시합니다.

```bash
# UTF-8 인코딩 명시
machloader -i -t sensor_log -d data.csv -E UTF-8

# EUC-KR 인코딩 명시
machloader -i -t sensor_log -d data.csv -E EUC-KR
```

파일의 실제 인코딩 확인 방법입니다.

```bash
file -i /data/import/sensor_log.csv
```

### 4. 구분자 오류

기본 구분자는 쉼표(`,`)입니다. 세미콜론, 탭, 파이프 등 다른 구분자를 사용하는 파일이라면 `-D` 옵션으로 지정합니다.

```bash
# 파이프(|) 구분자
machloader -i -t sensor_log -d data.csv -D '|'

# 탭 구분자
machloader -i -t sensor_log -d data.csv -D '\t'

# 세미콜론 구분자
machloader -i -t sensor_log -d data.csv -D ';'
```

### 5. 날짜 형식 오류

```
ERR: invalid datetime format at line 3
```

타임스탬프 컬럼의 값 형식이 machloader가 기대하는 형식과 다를 때 발생합니다. `-f` 옵션으로 시간 포맷을 직접 지정합니다.

```bash
# ISO 8601 형식 (예: 2024-01-15 09:30:00)
machloader -i -t sensor_log -d data.csv -f "YYYY-MM-DD HH24:MI:SS"

# 밀리초 포함 형식 (예: 2024-01-15 09:30:00.123)
machloader -i -t sensor_log -d data.csv -f "YYYY-MM-DD HH24:MI:SS.mmm"
```

## 자주 쓰는 옵션 조합

### 헤더 있는 CSV

```bash
machloader -i -t sensor_log -d data.csv -H
```

### 인코딩과 구분자 명시

```bash
machloader -i -t sensor_log -d data.csv -E UTF-8 -D '|'
```

### 날짜 형식과 헤더 함께 지정

```bash
machloader -i -t sensor_log -d data.csv -H -f "YYYY-MM-DD HH24:MI:SS"
```

## 부분 적재 후 재시작

대용량 파일 가져오기 도중 중단된 경우 처음부터 다시 시작하면 중복 데이터가 입력됩니다. `-S` 옵션으로 시작 행을 지정해 이미 입력된 행을 건너뜁니다.

```bash
# 1001번째 행부터 재시작 (헤더 제외 1000행 완료 가정)
machloader -i -t sensor_log -d data.csv -H -S 1001
```

오류 파일(`machloader_error.txt`)에 기록된 마지막 성공 행 번호를 `-S` 값으로 사용하십시오.

## machloader 주요 옵션 요약

| 옵션 | 설명 | 예시 |
|------|------|------|
| `-i` | import 모드 | `-i` |
| `-t` | 대상 테이블명 | `-t sensor_log` |
| `-d` | CSV 파일 경로 | `-d /data/file.csv` |
| `-H` | 첫 번째 행을 헤더로 처리 | `-H` |
| `-E` | 파일 인코딩 | `-E UTF-8` |
| `-D` | 구분자 | `-D '|'` |
| `-f` | 날짜 포맷 | `-f "YYYY-MM-DD HH24:MI:SS"` |
| `-S` | 시작 행 번호 | `-S 1001` |
