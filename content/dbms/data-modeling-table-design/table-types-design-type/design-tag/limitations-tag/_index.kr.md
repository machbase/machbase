---
type: docs
title: '제약 및 주의사항'
weight: 120
---

## 지원하지 않는 기능

| 기능 | 상태 |
|------|------|
| UPDATE | 미지원 |
| DELETE | 미지원 |
| 다중 PRIMARY KEY | 미지원 (단일 컬럼만) |
| BASETIME과 BASE DISTANCE 동시 사용 | 미지원 |
| ALTER TABLE (컬럼 삭제/변경) | 미지원 |

## 태그 수 제한

- 단일 TAG 테이블에 생성 가능한 태그 수는 시스템 설정에 따라 제한됩니다.
- 태그 수가 수십만 개를 초과하면 조회 성능이 저하될 수 있습니다.
- 태그 이름이 레코드마다 고유한 값이 되도록 설계하면 안 됩니다 (안티패턴 — [센서별 테이블 생성](/dbms/data-modeling-table-design/table-types-patterns-type-anti/per-sensor-create/) 참고).

## 시간 역삽입 제한

- BASETIME 컬럼에는 임의의 과거 시각을 삽입할 수 있습니다.
- 단, 내부적으로는 BASETIME 기준으로 정렬되어 저장되므로, 과도한 역삽입은 스토리지 단편화를 유발할 수 있습니다.

## Cluster Edition 지원

TAG 테이블은 Cluster Edition에서 지원됩니다.

## 요약

```
TAG 테이블 = 센서 이름 (PK) + 시간/거리 축 + 계측값
- INSERT/APPEND: O
- UPDATE: X
- DELETE: X
- METADATA: O (별도 속성 저장, UPDATE 가능)
```

---

**다음 읽을 내용**
- [RDB 테이블 설계](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/)
