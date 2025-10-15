---
title: 태그 테이블
type: docs
weight: 01
---

## 개요

Machbase 태그(Tag) 테이블은 센서·장비에서 발생하는 시계열 데이터를 효율적으로 저장하기 위한 전용 구조입니다. 전통적인 넓은(wide) 테이블 대신, **식별자(name)·시간(time)·값(value)** 으로 구성된 세로형(tall) 모델을 사용해 스키마 확장과 분석을 간편하게 합니다.

| TAGID       | timestamp           | value |
|:------------|:--------------------|:------|
| temperature | 2023-04-15 09:34:12 | 23.5  |
| humidity    | 2023-04-15 09:34:12 | 78.9  |
| pressure    | 2023-04-15 09:34:12 | 11    |
| ...         | ...                  | ...   |

- 태그 추가·삭제 시 스키마 변경이 필요 없습니다.
- 태그별 집계, 통계 분석이 쉽습니다.
- Machbase의 압축/인덱스 기술로 고성능을 유지합니다.

## 기본 구조

태그 테이블은 **데이터 영역**과 **메타 영역**으로 나뉩니다.

- 데이터 영역: `name`(PRIMARY KEY), `time`(BASETIME), `value` 컬럼을 기본으로 갖습니다.
- 메타 영역: 태그별 부가 정보를 저장하며 `_테이블명_meta` 테이블로 관리됩니다.

```sql
CREATE TAG TABLE vibration (
    name  VARCHAR(80) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA (
    factory   VARCHAR(32),
    equipment VARCHAR(64)
)
TAG_PARTITION_COUNT = 2,
TAG_STAT_ENABLE     = 1;
```

### 주요 속성

| 속성                      | 설명                                   | 기본값 |
|:--------------------------|:---------------------------------------|:-------|
| `TAG_PARTITION_COUNT`     | 내부 파티션 수(동시성 향상)            | 4      |
| `TAG_STAT_ENABLE`         | 태그별 통계 수집 활성화                | 1      |
| `TAG_DUPLICATE_CHECK_DURATION` | 중복 데이터 검사 기간(분)        | 0      |
| `TAG_DATA_PART_SIZE`      | 데이터 블록 크기(바이트)               | 16MB   |

## 지원 데이터 타입

| 타입      | 설명                        | 범위/주의사항                                |
|:----------|:----------------------------|:--------------------------------------------|
| `BYTE`    | 8비트 정수                  | -128 ~ 127                                   |
| `SHORT`   | 16비트 정수                 | -32,768 ~ 32,767                             |
| `INTEGER` | 32비트 정수                 | 약 ±21억                                     |
| `LONG`    | 64비트 정수                 | ±9.22e18                                     |
| `FLOAT`   | 4바이트 부동소수점          | IEEE-754                                     |
| `DOUBLE`  | 8바이트 부동소수점          | IEEE-754                                     |
| `VARCHAR` | 가변 길이 문자열            | 최대 32KB                                    |
| `DATETIME`| 나노초 정밀도의 타임스탬프  | `TO_DATE` 함수 이용                          |
| `BOOLEAN` | 논리 값                     | `TRUE` / `FALSE`                             |
| `IPv4`    | IPv4 주소                   | `0.0.0.0` ~ `255.255.255.255`                |
| `IPv6`    | IPv6 주소                   | `::` ~ `FFFF:...:FFFF`                       |
| `JSON`    | JSON 데이터                 | 1B~32KB / 경로 512자 이하                    |

`TEXT`, `BINARY` 타입은 태그 테이블에서 지원되지 않습니다.

## 데이터 적재

### import 도구

```bash
machbase-neo import --input data.csv --table vibration --timeformat s
machbase-neo import --format json --timeformat s --table vibration --input data.json
```

### REST API 사용

```
POST /db/write/vibration
[
  ["sensor-A", "2024-03-01 10:00:00", 12.3],
  ["sensor-B", "2024-03-01 10:00:00", 15.7]
]
```

## 메타데이터 관리

태그별 부가 정보는 메타 테이블(`_vibration_meta`)에 저장합니다. 구조 변경 시 `ALTER TABLE`을 사용하며 `DROP COLUMN`은 지원되지 않습니다.

```sql
ALTER TABLE _vibration_meta ADD COLUMN (location VARCHAR(32));
INSERT INTO vibration metadata VALUES ('sensor-A', 'factory-1', 'machine-1');
```

구조 변경 후에는 `REBUILD METADATA`로 변경 사항을 반영합니다.

## Rollup 및 통계

- `WITH ROLLUP`을 지정하면 초·분·시간 단위로 자동 집계 테이블이 생성되어 시간 구간별 분석이 빨라집니다.
- `TAG_STAT_ENABLE=1`이면 `v$<table>_stat` 뷰에서 태그별 건수, 최소/최대 값, 최신 시각 등을 즉시 확인할 수 있습니다.

## 뷰 구성 예시

```sql
CREATE VIEW vibration_view AS
SELECT m.name,
       m.factory,
       m.equipment,
       d.time,
       d.value
FROM vibration d
JOIN _vibration_meta m ON d.name = m.name;
```

## 운영 팁

- **중복 데이터 방지**: `TAG_DUPLICATE_CHECK_DURATION` 값을 설정하면 일정 시간 내 동일 `(name, time)` 데이터는 자동으로 무시됩니다.
- **보관 기간 관리**: Retention Policy를 추가해 일정 기간이 지난 데이터는 자동 삭제되도록 설정하십시오.
- **파티션 수 조절**: 고성능 서버는 높은 `TAG_PARTITION_COUNT`, 엣지 장비는 낮은 값을 사용해 자원 사용량을 조절합니다.

Machbase 태그 테이블은 간단한 스키마로 대량의 시계열 데이터를 적재·분석할 수 있도록 설계되어 있으며, Rollup·통계·보관 정책과 결합해 완성도 높은 시계열 데이터 플랫폼을 구성할 수 있습니다.
