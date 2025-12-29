---
type: docs
title: 'Tag Tables'
weight: 10
---

센서 및 디바이스 시계열 데이터를 위한 Machbase의 특화된 테이블 타입인 Tag 테이블에 대한 완전한 레퍼런스입니다.

## 개요

Tag 테이블은 (센서 ID, 타임스탬프, 값) 패턴의 센서 데이터 저장에 최적화되어 있습니다. 자동 롤업 통계, 메타데이터 관리 및 초고속 시계열 쿼리를 제공합니다.

## 주요 기능

- **초당 수백만 건의 삽입**
- **자동 롤업 통계** (초당, 분당, 시간당)
- **3단계 파티션 인덱싱**
- **메타데이터 레이어** (센서 정보용)
- **높은 압축률** (10-100배 압축 비율)

## 기본 구문

```sql
CREATE TAGDATA TABLE table_name (
    tag_column VARCHAR(n) PRIMARY KEY,
    time_column DATETIME BASETIME,
    value_column data_type SUMMARIZED
);
```

## 사용 시기

- IoT 센서 데이터
- 산업 장비 텔레메트리
- 스마트 미터
- GPS 추적
- 환경 모니터링
- (센서 ID, 시간, 값) 패턴의 모든 데이터

## 관련 문서

- [튜토리얼: IoT 센서 데이터](../../tutorials/iot-sensor-data/)
- [핵심 개념: 테이블 타입](../../core-concepts/table-types-overview/)
- [Binary 컬럼](./binary-columns/)
- 원본 레퍼런스: [Tag Tables](../../../dbms/feature-table/tag/)
