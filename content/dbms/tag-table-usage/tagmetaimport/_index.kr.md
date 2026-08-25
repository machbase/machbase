---
title: '5.13 tagmetaimport와 메타데이터 일괄 등록'
weight: 130
toc: true
---


<a id="metadata-import-tagmetaimport-tag"></a>

## tagmetaimport로 TAG 메타데이터 가져오기

`tagmetaimport`는 TAG 테이블의 메타데이터를 CSV 파일로 일괄 로드하거나 업데이트하는 전용
도구입니다. 사용자는 TAG 테이블 이름을 지정하며 시스템 저장 객체를 직접 다루지 않습니다.

### TAG 메타데이터란

TAG 테이블에서 `METADATA` 블록으로 정의된 컬럼들의 데이터입니다. 각 태그(name)에 대한 속성 정보(위치, 단위, 설명 등)를 저장합니다.

```sql
CREATE TAG TABLE sensors (
    name    VARCHAR(20) PRIMARY KEY,
    time    DATETIME BASETIME,
    value   DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(40),
    status   VARCHAR(20)
);
```

위 예시에서 `location`, `status`가 메타데이터 컬럼입니다.

### CSV 파일 형식

메타데이터 CSV 파일에는 `name` 컬럼과 사용자가 정의한 메타데이터 컬럼만 포함합니다.

```csv
TEMP_001,Building-A/F1,READY
TEMP_002,Building-A/F2,STOP
TEMP_003,Building-B/F3,READY
```

헤더를 포함하는 경우:
```csv
name,location,status
TEMP_001,Building-A/F1,READY
TEMP_002,Building-A/F2,STOP
```

### tagmetaimport 사용법

```bash
# sensors TAG 테이블의 메타데이터 로드
tagmetaimport -t sensors -d metadata.csv

# 헤더 있는 CSV
tagmetaimport -t sensors -d metadata.csv -H

# 서버 접속 정보 지정
tagmetaimport -t sensors -d metadata.csv \
    -s 192.168.1.10 -P 5656 -u SYS -p MANAGER

# 로그 파일 생성
tagmetaimport -t sensors -d metadata.csv \
    -l import.log -b import.bad
```

### 동작 방식

- **신규 태그**: 메타데이터와 함께 태그 항목 생성
- **기존 태그**: 메타데이터 값 업데이트 (`_LAST_UPDATE_TIME` 자동 갱신)
- 실제 메타데이터 값이 변경된 경우에만 `_LAST_UPDATE_TIME` 갱신

### machloader와 비교

일반 행 데이터의 파일 입출력에는 `machloader`를 사용하고, TAG 메타데이터의 일괄 등록에는
`tagmetaimport`를 사용합니다. 시스템 저장 객체를 `machloader` 대상으로 지정하지 마십시오.

### SQL INSERT로 대체

소량의 메타데이터는 SQL로도 직접 삽입할 수 있습니다.

```sql
-- 메타데이터 삽입
INSERT INTO sensors METADATA VALUES ('TEMP_001', 'Building-A/F1', 'READY');

-- 메타데이터 업데이트
UPDATE sensors METADATA SET location = 'Building-B/F1'
WHERE name = 'TEMP_001';
```
