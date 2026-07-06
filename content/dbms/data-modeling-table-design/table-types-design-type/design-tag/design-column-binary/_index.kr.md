---
type: docs
title: '이진 데이터 컬럼 설계'
weight: 70
---

TAG 테이블에 이미지, 파형, 스펙트럼 등 이진(Binary) 데이터를 함께 저장해야 하는 경우 `BINARY` 타입을 사용합니다.

## BINARY 타입

```sql
CREATE TAG TABLE waveform_data (
    name     VARCHAR(64) PRIMARY KEY,
    time     DATETIME    BASETIME,
    rms      DOUBLE,
    waveform BINARY      -- 파형 데이터 (이진)
);
```

## 삽입

```sql
-- SDK(Go, Python, C 등)에서 바이트 슬라이스로 삽입
-- machsql에서는 hex 문자열 사용
INSERT INTO waveform_data VALUES (
    'sensor-01', NOW,
    0.354,
    X'0102030405060708'
);
```

## 주의사항

- `BINARY` 컬럼의 최대 크기는 64MB입니다.
- `BINARY` 데이터에는 집계 함수(`AVG`, `SUM` 등)를 적용할 수 없습니다.
- 대용량 이진 데이터를 자주 조회하면 성능에 영향이 있을 수 있습니다. 이진 데이터는 별도 파일 스토리지에 저장하고, TAG 테이블에는 파일 경로 또는 참조 키만 저장하는 패턴도 고려합니다.

## 이진 데이터를 외부 참조로 대체하는 패턴

```sql
CREATE TAG TABLE waveform_ref (
    name      VARCHAR(64) PRIMARY KEY,
    time      DATETIME    BASETIME,
    rms       DOUBLE,
    file_path VARCHAR(512)  -- 외부 파일 참조
);
```
