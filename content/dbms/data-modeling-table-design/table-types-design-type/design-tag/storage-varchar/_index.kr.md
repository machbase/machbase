---
type: docs
title: 'VARCHAR 스토리지 최적화'
weight: 80
---

TAG 테이블에서 `VARCHAR` 컬럼을 사용할 때는 크기와 성능의 균형을 고려해야 합니다.

## VARCHAR 크기 설정

```sql
-- 태그 이름: 충분히 여유 있게
CREATE TAG TABLE sensor_data (
    name   VARCHAR(128) PRIMARY KEY,  -- 128자 여유
    time   DATETIME     BASETIME,
    status VARCHAR(32),               -- 상태 문자열
    label  VARCHAR(256)               -- 레이블
);
```

## 권장 크기

| 용도 | 권장 크기 |
|------|---------|
| 태그 이름 (`PRIMARY KEY`) | 64~256 |
| 상태 코드 | 16~32 |
| 단위 | 8~16 |
| 설명 | 128~512 |
| 경로/URL | 512~1024 |

## 주의사항

- `PRIMARY KEY`(`VARCHAR`) 컬럼은 태그 이름으로 사용됩니다. 너무 짧게 설정하면 실제 센서 이름이 잘릴 수 있습니다.
- `VARCHAR`는 실제 저장 데이터 크기만큼만 공간을 차지합니다. 넉넉한 크기를 설정해도 공간 낭비가 없습니다.
- 단, 집계 쿼리나 정렬 시 내부 처리 버퍼 크기에 영향을 줄 수 있으므로 과도하게 큰 값은 피합니다.

## 태그 이름 설계 패턴

태그 이름을 구조화하면 범위 조회가 쉬워집니다.

```sql
-- 구조화된 태그 이름: {site}/{building}/{floor}/{sensor_id}
INSERT INTO sensor_data VALUES ('HQ/A-BLDG/3F/TEMP-01', NOW, 23.5, NULL, NULL);
INSERT INTO sensor_data VALUES ('HQ/A-BLDG/3F/TEMP-02', NOW, 24.1, NULL, NULL);

-- 같은 건물의 센서 조회
SELECT name, time, status
FROM sensor_data
WHERE name LIKE 'HQ/A-BLDG/%'
  AND time >= NOW - 3600000000000;
```
