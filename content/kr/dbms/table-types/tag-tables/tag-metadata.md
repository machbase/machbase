---
title: 'Tag 메타데이터 관리'
type: docs
weight: 20
---

## Tag 메타데이터 이해하기

Tag 메타데이터는 Machbase에서 센서 또는 데이터 소스의 식별 정보 및 추가 정보를 나타냅니다. 이것을 모든 센서의 레지스트리로 생각할 수 있습니다. 각 tag는 고유한 이름을 가지며 관련된 설명 정보를 가질 수 있습니다.

## 기본 Tag 메타데이터 작업

### 간단한 Tag 메타데이터 생성

tag 테이블을 생성할 때 구조를 정의합니다. 실제로 사용하려면 tag 이름을 등록해야 합니다:

```sql
-- 먼저 tag 테이블 생성
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);

Mach> desc tag;
[ COLUMN ]
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
NAME                          varchar             20
TIME                          datetime            31
VALUE                         double              17
```

### Tag 이름 삽입

새 센서/tag 등록:

```sql
Mach> insert into tag metadata values ('TAG_0001');
1 row(s) inserted.
```

### Tag 메타데이터 조회

Machbase는 등록된 모든 tag를 조회할 수 있는 특수 테이블 `_tag_meta`를 제공합니다:

```sql
Mach> select * from _tag_meta;
ID                   NAME
----------------------------------------------
1                    TAG_0001
[1] row(s) selected.
```

ID는 시스템에 의해 자동으로 할당됩니다.

### Tag 이름 수정

필요할 때 tag 이름을 수정할 수 있습니다:

```sql
Mach> update tag metadata set name = 'NEW_0001' where NAME = 'TAG_0001';
1 row(s) updated.

Mach> select * from _tag_meta;
ID                   NAME
----------------------------------------------
1                    NEW_0001
[1] row(s) selected.
```

### Tag 메타데이터 삭제

더 이상 필요하지 않을 때 tag 메타데이터를 제거합니다:

```sql
Mach> delete from tag metadata where name = 'NEW_0001';
1 row(s) deleted.

Mach> select * from _tag_meta;
ID                   NAME
----------------------------------------------
[0] row(s) selected.
```

> **중요**: 실제 센서 데이터가 참조하지 않는 경우에만 tag 메타데이터를 삭제할 수 있습니다.

## 추가 메타데이터 작업

### 풍부한 메타데이터 구조 생성

tag 이름 외에도 설명 정보를 추가합니다:

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized)
metadata (type short, create_date datetime, srcip ipv4);

Mach> desc tag;
[ COLUMN ]
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
NAME                          varchar             20
TIME                          datetime            31
VALUE                         double              17
[ META-COLUMN ]
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
TYPE                          short               6
CREATE_DATE                   datetime            31
SRCIP                         ipv4                15
```

### 부분 메타데이터로 삽입

tag 이름만 삽입할 수 있습니다 - 다른 필드는 NULL이 됩니다:

```sql
Mach> insert into tag metadata(name) values ('TAG_0001');
1 row(s) inserted.

Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP
-------------------------------------------------------------------------------------------------------------
1                    TAG_0001              NULL        NULL                            NULL
[1] row(s) selected.
```

### 완전한 메타데이터 삽입

또는 모든 메타데이터 필드를 제공합니다:

```sql
Mach> insert into tag metadata values ('TAG_0002', 99, '2010-01-01', '1.1.1.1');
1 row(s) inserted.

Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP
-------------------------------------------------------------------------------------------------------------
1                    TAG_0001              NULL        NULL                            NULL
2                    TAG_0002              99          2010-01-01 00:00:00 000:000:000 1.1.1.1
[2] row(s) selected.
```

### 메타데이터 값 업데이트

모든 메타데이터 필드를 업데이트합니다:

```sql
Mach> update tag metadata set type = 11 where name = 'TAG_0001';
1 row(s) updated.

Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP
-------------------------------------------------------------------------------------------------------------
2                    TAG_0002              99          2010-01-01 00:00:00 000:000:000 1.1.1.1
1                    TAG_0001              11          NULL                            NULL
[2] row(s) selected.
```

> **참고**: 메타데이터를 업데이트할 때 WHERE 절에 NAME 컬럼을 포함해야 합니다.

## Tag 메타데이터용 RESTful API

### 모든 Tag 가져오기

HTTP를 통해 모든 tag 목록을 조회합니다:

```bash
$ curl -G "http://192.168.0.148:5001/machiot-rest-api/tags/list"
{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"NAME": "TAG_0001"},
          {"NAME": "TAG_0002"}]}
```

### Tag 시간 범위 가져오기

tag의 최소 및 최대 타임스탬프를 찾습니다 (차트 작성에 유용):

```bash
# 모든 tag의 시간 범위
$ curl -G "http://192.168.0.148:5001/machiot-rest-api/tags/range/"
{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"MAX": "2018-02-10 10:00:00 000:000:000", "MIN": "2018-01-01 01:00:00 000:000:000"}]}

# 특정 tag의 시간 범위
$ curl -G "http://192.168.0.148:5001/machiot-rest-api/tags/range/TAG_0001"
{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"MAX": "2018-01-10 10:00:00 000:000:000", "MIN": "2018-01-01 01:00:00 000:000:000"}]}
```

## 실제 사용 예제

다음은 온도 센서 메타데이터를 설정하는 방법을 보여주는 완전한 예제입니다:

```sql
-- 메타데이터가 있는 tag 테이블 생성
CREATE TAG TABLE sensors (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(50),
    sensor_type VARCHAR(20),
    installed_date DATETIME,
    ip_address IPV4
);

-- 전체 메타데이터로 센서 등록
INSERT INTO sensors METADATA VALUES (
    'TEMP_BUILDING_A_FLOOR1', 'Building A - Floor 1', 'Temperature', '2024-01-15', '192.168.1.101'
);

INSERT INTO sensors METADATA VALUES (
    'TEMP_BUILDING_A_FLOOR2', 'Building A - Floor 2', 'Temperature', '2024-01-15', '192.168.1.102'
);

-- 등록된 모든 센서 조회
SELECT * FROM _sensors_meta;
```

## 모범 사례

1. **설명적인 이름 사용**: Tag 이름은 의미 있고 일관된 명명 규칙을 따라야 합니다
2. **메타데이터 활용**: 센서 데이터의 중복을 피하기 위해 메타데이터 컬럼에 정적 정보를 저장합니다
3. **스키마 계획**: tag 테이블을 생성할 때 필요한 모든 메타데이터 컬럼을 정의합니다
4. **정기적인 정리**: 레지스트리를 깨끗하게 유지하기 위해 사용하지 않는 tag 메타데이터를 제거합니다
5. **API 접근**: 외부 애플리케이션과의 통합을 위해 RESTful API를 사용합니다

## 다음 단계

- 센서 판독값 기록을 시작하려면 [Tag 데이터 삽입](../inserting-data)을 알아보세요
- 데이터 조회를 위해 [Tag 데이터 조회](../querying-data)를 살펴보세요
- 성능 최적화를 위해 [Tag 인덱스](../tag-indexes)를 이해하세요
