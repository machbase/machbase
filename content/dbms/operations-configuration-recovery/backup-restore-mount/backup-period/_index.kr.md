---
type: docs
title: '기간 백업'
weight: 50
---

기간 백업은 특정 시간 범위에 해당하는 데이터만 선택하여 백업합니다. 오래된 데이터를 아카이브하거나 특정 기간의 데이터를 별도로 보관할 때 사용합니다.

## 문법

```sql
BACKUP DATABASE
  FROM start_time
  TO end_time
  INTO DISK = 'backup_path';
```

- `start_time`, `end_time`: `TO_DATE()` 함수로 표현한 시간 범위
- FROM 절을 생략하면 `1970-01-01 00:00:00`부터 적용됩니다.
- TO 절을 생략하면 명령 실행 시점의 현재 시간까지 적용됩니다.

## 예제

```sql
-- 특정 월 데이터 백업 (2024년 1월)
BACKUP DATABASE
  FROM TO_DATE('20240101','YYYYMMDD')
  TO   TO_DATE('20240131','YYYYMMDD')
  INTO DISK = '/backup/machbase_202401';

-- 특정 날짜 하루 데이터 백업
BACKUP DATABASE
  FROM TO_DATE('2024-01-15 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  TO   TO_DATE('2024-01-15 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
  INTO DISK = '/backup/machbase_20240115';

-- 테이블 단위 기간 백업
BACKUP TABLE sensor_log
  FROM TO_DATE('20240101','YYYYMMDD')
  TO   TO_DATE('20240131','YYYYMMDD')
  INTO DISK = '/backup/sensor_log_202401';
```

## 동작 방식

- 지정한 시간 범위에 속하는 데이터만 백업 파일에 포함됩니다.
- 시간 조건은 각 레코드의 입력 시각(`_arrival_time` 또는 태그 테이블의 타임스탬프 컬럼)을 기준으로 적용됩니다.
- 기간 백업으로 생성된 백업 파일도 마운트(`MOUNT DATABASE`)할 수 있습니다.

## 주요 활용 시나리오

### 월별 아카이브

디스크 공간을 절약하기 위해 오래된 데이터를 기간 백업으로 아카이브한 뒤 원본 데이터를 삭제하는 방식입니다.

```bash
# 매월 말일에 해당 월 데이터를 아카이브
YEAR_MONTH="202401"
machsql -u sys -p manager -e "
  BACKUP DATABASE
    FROM TO_DATE('${YEAR_MONTH}01','YYYYMMDD')
    TO   TO_DATE('${YEAR_MONTH}31','YYYYMMDD')
    INTO DISK = '/archive/machbase_${YEAR_MONTH}';
"
```

### 장기 보관 데이터 조회

아카이브된 기간 백업 파일을 마운트하여 과거 데이터를 현재 서버에서 직접 조회합니다.

```sql
-- 2024년 1월 아카이브 마운트
MOUNT DATABASE '/archive/machbase_202401' TO archive_202401;

-- 아카이브에서 조회
SELECT * FROM archive_202401.sys.sensor_log
 WHERE _arrival_time BETWEEN TO_DATE('20240110','YYYYMMDD')
                         AND TO_DATE('20240115','YYYYMMDD');

-- 조회 완료 후 언마운트
UNMOUNT DATABASE archive_202401;
```

## 주의 사항

- TAG 테이블의 경우 기간 백업으로 복원(`machadmin -r`)하는 것은 지원되지 않습니다. 기간 백업을 마운트하여 읽기 전용으로 활용하는 방식은 사용 가능합니다.
- FROM과 TO 범위가 정확하게 지정되어야 원하는 데이터가 포함됩니다. 범위 경계값 포함 여부를 확인하세요.
