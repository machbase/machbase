---
type: docs
title: '9.8.3 제약 및 주의사항'
weight: 100
---

## 제약 사항

| 항목 | 상태 |
|------|------|
| PRIMARY KEY | 필수 |
| Append API | 지원 |
| 대용량 (수천만 건 이상) | 미권장 |
| BASETIME / BASEDISTANCE | 미지원 |

## 규모 제한

LOOKUP 테이블은 소규모 참조 데이터에 최적화되어 있습니다. 건수가 수백만 건을 넘는 경우 성능이 저하될 수 있으며, 이 경우 RDB 테이블을 고려합니다.

| 규모 | 권장 타입 |
|------|---------|
| 수십만 건 이하 | LOOKUP |
| 수백만~수천만 건 | 경계 — 성능 테스트 필요 |
| 수천만 건 이상 | RDB 테이블 |

## Append API

```bash
# LOOKUP 테이블에는 INSERT 문 또는 SDK Append API 사용
```

## 주의사항

- LOOKUP 테이블에 시계열 데이터를 저장하지 않습니다. 계측값은 TAG 테이블을 사용합니다.
- PRIMARY KEY 중복 삽입 시 오류가 발생합니다.
- 테이블 전체를 교체해야 하는 경우, DELETE 후 INSERT 또는 TRUNCATE + INSERT 패턴을 사용합니다.

---

**다음 읽을 내용**
- [VOLATILE 테이블 설계](/dbms/volatile-table-usage/)
