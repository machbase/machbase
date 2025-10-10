---
title: 'Tag 테이블 생성 및 삭제'
type: docs
weight: 10
---

## 학습 내용

Tag 테이블은 Machbase에서 시계열 센서 데이터를 저장하는 기본 구조입니다. 이 가이드는 Tag 테이블을 효과적으로 생성, 설정 및 삭제하는 방법을 다룹니다.

## 기본 Tag 테이블 생성

가장 간단한 Tag 테이블은 세 가지 필수 요소를 필요로 합니다:
- **태그 이름** (PRIMARY KEY): 센서 또는 데이터 소스를 식별
- **입력 시간** (BASETIME): 데이터가 기록된 시간
- **센서 값**: 실제 측정값

### 간단한 생성 예제

```sql
-- 이것은 실패합니다 - 필수 키워드 누락
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME, value DOUBLE);
[ERR-02253: Mandatory column definition (PRIMARY KEY / BASETIME) is missing.]

-- 올바른 방법 - 필수 BASETIME 키워드 포함
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE);
Executed successfully.

-- 통계 정보를 위한 SUMMARIZED 포함
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
Executed successfully.

Mach> desc tag;
[ COLUMN ]
----------------------------------------------------------------
NAME      TYPE        LENGTH
----------------------------------------------------------------
NAME      varchar         20
TIME      datetime       31
VALUE     double          17
```

> **팁**: SUMMARIZED 키워드는 value 컬럼에 대한 자동 통계 추적(최소값, 최대값, 평균)을 활성화하며, 분석에 유용합니다.

## 추가 센서 컬럼 추가

실제 센서 데이터는 종종 이름, 시간, 값 이상을 필요로 합니다. 그룹 ID, IP 주소 등과 같은 메타데이터를 위한 추가 컬럼을 추가할 수 있습니다.

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double, grpid short, myip ipv4);
Executed successfully.

Mach> desc tag;
[ COLUMN ]
----------------------------------------------------------------
NAME             TYPE        LENGTH
----------------------------------------------------------------
NAME             varchar         20
TIME             datetime        31
VALUE            double          17
GRPID            short            6       <=== 추가된 컬럼
MYIP             ipv4            15       <=== 추가된 컬럼
```

> **참고**: 5.6 버전 이전에는 VARCHAR 타입이 추가 컬럼으로 허용되지 않았습니다. 5.6 버전 이상에서는 추가 컬럼에서 VARCHAR를 지원합니다.

## 메타데이터 컬럼 추가

메타데이터 컬럼은 각 센서 읽기마다 중복으로 저장하지 않고 각 태그 이름에 특정한 정보(예: 방 번호 또는 설명)를 저장합니다.

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double)
   2  metadata (room_no integer, tag_description varchar(100));
Executed successfully.
```

### 메타데이터 사용 예제

|name|room_no|tag_description|
|--|--|--|
|temp_001|1|섭씨 온도를 읽습니다|
|humid_001|1|백분율로 습도를 읽습니다|

센서 데이터와 함께 메타데이터를 쿼리:

```sql
Mach> SELECT name, time, value, tag_description FROM tag LIMIT 1;
name                  time                            value
--------------------------------------------------------------------------------------
tag_description
------------------------------------------------------------------------------------
temp_001              2019-03-01 09:52:17 000:000:000 25.3
섭씨 온도를 읽습니다
```

## 테이블 속성 설정

다음 속성으로 메모리 및 CPU 사용을 제어합니다:

|속성|설명|기본값|범위|
|--|--|--|--|
|TAG_PARTITION_COUNT|파티션 개수|4|1-1024|
|TAG_DATA_PART_SIZE|파티션당 데이터 크기|16MB|1MB-1GB|
|TAG_STAT_ENABLE|통계 추적 활성화|1 (활성화)|0-1|

### 속성 예제

```sql
-- 저용량 데이터를 위한 단일 파티션
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE)
      TAG_PARTITION_COUNT=1;

-- 사용자 정의 데이터 파트 크기
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE)
      TAG_DATA_PART_SIZE=1048576;

-- 여러 속성
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)
      TAG_PARTITION_COUNT=2, TAG_STAT_ENABLE=1;
```

## Tag 테이블 삭제

Tag 테이블을 다시 생성하거나 디스크 공간을 확보해야 할 때 DROP 명령을 사용합니다:

```sql
Mach> DROP TABLE tag;
Dropped successfully.

Mach> DESC tag;
tag does not exist.
```

> **경고**: Tag 테이블을 삭제하면 관련된 모든 데이터 및 메타데이터 테이블이 영구적으로 삭제됩니다. 이 작업은 되돌릴 수 없습니다.

## 모범 사례

1. **SUMMARIZED 사용**: 통계 정보가 필요할 때 value 컬럼에 SUMMARIZED 키워드를 추가합니다
2. **파티션 계획**: 파티션 개수가 많을수록 병렬 처리가 향상되지만 더 많은 메모리를 사용합니다
3. **적절한 이름 선택**: Tag 테이블 이름은 유효한 식별자라면 무엇이든 가능합니다 ("TAG"일 필요 없음)
4. **메타데이터 vs 추가 컬럼**:
   - 드물게 변경되는 태그별 정보에는 메타데이터를 사용합니다
   - 각 읽기마다 변경되는 데이터에는 추가 컬럼을 사용합니다

## 다음 단계

- [Tag 메타데이터 관리](../tag-metadata)에서 태그 이름 생성 및 관리에 대해 학습합니다
- [Tag 데이터 삽입](../inserting-data)에서 다양한 데이터 입력 방법을 탐색합니다
- [Tag 데이터 쿼리](../querying-data)에서 효율적인 데이터 검색을 이해합니다
