---
type: docs
title: '4.1.2 타입 선택 결정 가이드'
weight: 20
---

아래 질문에 순서대로 답하여 적합한 테이블 타입을 선택합니다.

## 결정 흐름

```
데이터가 센서/기기 계측값인가?
  ├── YES → 시간축인가?    YES → TAG TABLE (BASETIME)
  │            거리축인가?  YES → TAG TABLE (BASEDISTANCE)
  └── NO  ↓

데이터가 이벤트/로그/패킷인가? (추가 전용)
  ├── YES → LOG TABLE
  └── NO  ↓

데이터가 코드 테이블/기준 정보인가? (소규모, PK 기반 UPDATE)
  ├── YES, 건수 < 수백만 → LOOKUP TABLE
  └── NO  ↓

데이터가 세션 내 임시 집계/캐시인가?
  ├── YES → VOLATILE TABLE
  └── NO  ↓

일반 관계형 업무 데이터 (UPDATE/DELETE/SELECT/INSERT 모두 필요)
  └── RDB TABLE
```

## 주요 판단 기준

| 질문 | 타입 |
|------|------|
| 시간 또는 거리 기반 계측값인가? | TAG |
| 추가만 하고 수정·삭제 불필요? | LOG |
| PRIMARY KEY 기준 UPDATE/DELETE 필요? 소규모? | LOOKUP |
| 서버 재시작 시 데이터가 사라져도 되는가? | VOLATILE |
| 일반 관계형 업무 (INSERT/UPDATE/DELETE/SELECT)? | RDB |

## 주의사항

- TAG 테이블에 이벤트 로그를 저장하면 태그 수 폭발로 성능이 저하됩니다.
- LOG 테이블은 UPDATE와 일반 조건 DELETE가 불가하므로 수정 가능성이 있는 데이터에는 부적합합니다. 보존/정리 목적의 `BEFORE`, `OLDEST`, `EXCEPT` DELETE만 사용합니다.
- RDB 테이블은 Standard Edition 전용입니다. Cluster Edition 환경에서는 LOOKUP(소규모) 또는 외부 RDBMS를 활용합니다.
- VOLATILE 테이블은 서버 재시작 시 데이터가 소멸됩니다.
