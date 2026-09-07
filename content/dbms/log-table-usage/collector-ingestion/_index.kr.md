---
type: docs
title: '7.13 Collector 기반 수집'
weight: 130
toc: true
---

Collector가 실행 중인데 테이블 값이 예상과 다르다면 파일 필드와 컬럼 매핑부터 확인하세요.
프로세스가 정상이라는 사실과 원본이 올바르게 해석되었다는 사실은 다릅니다.
여기서는 CSV 두 줄을 기준으로 원본, 규칙 파일, 저장 결과를 연결해 봅니다.

## 소스와 파서를 구분합니다

현재 확인되는 수집 소스는 FILE과 SFTP입니다.
CSV·REGEX·JSON·JSON_PIVOT은 소스가 아니라 파일 내용을 해석하는 파싱 방식입니다.
템플릿에 socket·ODBC 이름의 호환 키가 남아 있어도 해당 소스의 지원을 뜻하지 않습니다.

이 실습은 FILE+CSV를 사용합니다. 검증용 DBMS와 Collector Manager가 준비되어 있고,
Collector 계정이 원본·규칙 파일을 읽고 완료 파일 디렉터리에 쓸 수 있어야 합니다.
Manager의 준비와 복구는
[Collector 운영](/dbms/operations-configuration-recovery/collector/)을 따릅니다.
다른 수집기가 실행 중인 환경에서 Manager 전체를 재시작하지 마세요.

## 대상 테이블을 먼저 만듭니다

```sql
CREATE LOG TABLE ch7_collector_event (
    source_time DATETIME,
    host_name   VARCHAR(64),
    level       VARCHAR(16),
    message     VARCHAR(1024)
);
SELECT COUNT(*) AS initial_rows FROM ch7_collector_event;
```

초기 건수는 0이어야 합니다.
`_arrival_time`은 자동 컬럼이므로 사용자 컬럼 목록에 다시 선언하지 않습니다.
원본의 발생 시각은 `source_time`에 보존합니다.

## 표본 CSV와 매핑 파일을 준비합니다

다음 경로는 검증 환경의 예시입니다. 접근 가능한 작업 디렉터리로 바꾸되 템플릿 안의
경로도 함께 맞추세요. `done` 디렉터리까지 미리 준비하고, 아직 처리한 적 없는
새 표본 파일로 시작합니다.

```text
/opt/machbase/collector/ch7/
  sample.csv
  sample.rgx
  sample.tpl
  done/
```

`sample.csv`는 UTF-8, 헤더 없는 두 줄로 저장합니다.
이 표본은 필드 안에 쉼표나 줄바꿈이 없는 단순 CSV입니다.

```text
2026-01-01 10:00:00,web-01,INFO,service started
2026-01-01 10:01:00,web-02,ERROR,connection timeout
```

`sample.rgx`는 다음과 같습니다. REGEX_NO는 이 CSV 표본의 필드 순서에 맞춘 번호입니다.

```ini
LOG_TYPE=machbase
FIELD_TERM=","
RECORD_TERM="\n"

COL_LIST= (
    (
        REGEX_NO=1
        NAME=source_time
        TYPE=datetime
        SIZE=8
        DATE_FORMAT="%Y-%m-%d %H:%M:%S"
    ),
    (
        REGEX_NO=2
        NAME=host_name
        TYPE=varchar
        SIZE=64
    ),
    (
        REGEX_NO=3
        NAME=level
        TYPE=varchar
        SIZE=16
    ),
    (
        REGEX_NO=4
        NAME=message
        TYPE=varchar
        SIZE=1024
    )
)
```

실수하기 쉬운 부분은 날짜 형식입니다. 여기의 DATE_FORMAT은 SQL TO_DATE의
`YYYY-MM-DD HH24:MI:SS` 형식이 아닙니다.
이 표본은 원본과 수집 환경의 시간대가 같은 조건으로 비교합니다.
시간대가 다르면 변환 정책과 TIMEZONE_OFFSET 설정을
[Collector 템플릿 사전](/dbms/reference/collector/dictionary-collector-template/)에서 확인하고
알려진 시각 한 건으로 먼저 검증하세요.

## 템플릿에는 기존 테이블을 보존하는 모드를 사용합니다

`sample.tpl`의 주소·포트·계정·비밀번호·경로를 실제 검증 환경 값으로 바꾸세요.
아래 비밀번호는 반드시 교체할 자리 표시자입니다. 완성된 파일에는 접속 정보가 들어가므로
읽기 권한을 제한하고 저장소에 커밋하거나 그대로 공유하지 마세요.

```ini
COLLECT_TYPE=FILE
PARSE_TYPE=CSV
LOG_SOURCE=/opt/machbase/collector/ch7/sample.csv
REGEX_PATH=/opt/machbase/collector/ch7/sample.rgx
DB_TABLE_NAME="ch7_collector_event"
DB_ADDR="127.0.0.1"
DB_PORT=5656
DB_USER="SYS"
DB_PASS="REPLACE_WITH_DB_PASSWORD"
CREATE_TABLE_MODE=0
FILE_BACKUP_PATH="/opt/machbase/collector/ch7/done/sample.csv"
```

CREATE_TABLE_MODE=0은 테이블을 새로 만들거나 비우지 않고 입력합니다.
대상 테이블을 앞에서 만든 이유입니다. 1은 truncate, 3은 drop 후 생성이므로
오류 해결을 위해 운영 테이블에 무심코 적용하면 안 됩니다.

## 등록 후에는 처리 상태와 실제 값을 함께 확인합니다

Manager가 준비된 환경에서 다음 명령을 실행합니다.

```bash
machcollectoradmin --create-collector=ch7_file --template=/opt/machbase/collector/ch7/sample.tpl
machcollectoradmin --start-collector=ch7_file
machcollectoradmin --status-collector=ch7_file
```

처리가 끝나면 SQL로 확인합니다. 아래 형식화 결과는 원본과 조회 환경의 시간대를 맞춘
경우를 기준으로 합니다.

```sql
SELECT COUNT(*) AS row_count,
       MIN(source_time) AS first_event,
       MAX(source_time) AS last_event
  FROM ch7_collector_event;

SELECT TO_CHAR(source_time, 'YYYY-MM-DD HH24:MI:SS') AS source_time_text,
       host_name, level, message
  FROM ch7_collector_event
 ORDER BY source_time, host_name;
```

건수는 2, 시각은 10:00과 10:01이며 원본의 host·level·message와 일치해야 합니다.
`_arrival_time`은 실제 이번 적재에서 정해지므로 원본의 2026-01-01 시각과
같아야 하는 값이 아닙니다. 건수만 맞고 컬럼 값이 밀려 있다면 매핑부터 다시 확인하세요.

빈 필드·NULL 표기·따옴표 안의 쉼표·긴 한글 메시지는 이 표본에 포함하지 않았습니다.
운영에 투입하기 전에 실제 파일 형식으로 해당 사례를 추가 검증하세요.

## 재처리 전에 원본과 완료 위치를 확인합니다

```bash
machcollectoradmin --stop-collector=ch7_file
machcollectoradmin --status-collector=ch7_file
```

중지 상태와 처리 완료를 확인한 뒤에만 실습 Collector를 삭제합니다.

```bash
machcollectoradmin --drop-collector=ch7_file
```

```sql
DROP TABLE ch7_collector_event;
```

이 정리는 실습 Collector와 테이블만 대상으로 합니다.
표본·완료 파일은 자동으로 모두 삭제된다고 가정하지 마세요.
재실행하려면 이전 처리 위치와 파일 상태를 확인한 뒤 별도 표본을 준비하세요.
이미 처리한 파일을 입력 위치에 다시 놓으면 같은 이벤트가 다시 들어갈 수 있습니다.

수집이 막히면 실패한 원본 한 줄, 매핑 규칙, Collector 로그를 함께 확인해 보세요.
접속 정보를 가린 작은 표본이 있으면 동료와 원인을 공유하기도 수월합니다.
