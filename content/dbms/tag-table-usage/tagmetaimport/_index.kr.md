---
title: '5.13 tagmetaimport와 메타데이터 일괄 등록'
weight: 130
toc: true
---


<a id="metadata-import-tagmetaimport-tag"></a>

## tagmetaimport로 TAG 메타데이터 가져오기

`tagmetaimport`는 TAG 테이블의 메타데이터를 CSV 파일로 일괄 로드하거나 업데이트하는 전용 도구입니다. 내부적으로 `_TAG_META` 테이블을 대상으로 `machloader`를 실행합니다.

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

메타데이터 CSV 파일은 `name` 컬럼과 사용자 메타데이터 컬럼만 포함합니다. 내부 컬럼(`_ID`, `_LAST_UPDATE_TIME`)은 포함하지 않습니다.

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

machloader를 사용할 경우 TAG 메타데이터 물리 테이블을 직접 지정해야 합니다.

```bash
# machloader로 TAG 메타데이터 적재 시
machloader -i -d metadata.csv -t _tag_meta -I
# 또는 tagmetaimport 사용 권장
```

`tagmetaimport`는 지정한 TAG 테이블의 메타데이터를 `_tag_meta` 경로로 적재하도록 처리합니다.

### SQL INSERT로 대체

소량의 메타데이터는 SQL로도 직접 삽입할 수 있습니다.

```sql
-- 메타데이터 삽입
INSERT INTO sensors METADATA VALUES ('TEMP_001', 'Building-A/F1', 'READY');

-- 메타데이터 업데이트
UPDATE sensors METADATA SET location = 'Building-B/F1'
WHERE name = 'TEMP_001';
```
