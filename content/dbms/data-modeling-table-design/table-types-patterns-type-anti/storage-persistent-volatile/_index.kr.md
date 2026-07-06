---
type: docs
title: 'VOLATILE 영속 저장 오용'
weight: 40
---

## 문제

VOLATILE 테이블에 영구 보존이 필요한 데이터를 저장하는 패턴입니다.

## 안티패턴 예시

```sql
-- 잘못됨: 중요 설정을 VOLATILE에 저장
CREATE VOLATILE TABLE critical_config (
    key_name VARCHAR(64) PRIMARY KEY,
    value    VARCHAR(256)
);

INSERT INTO critical_config VALUES ('license_key', 'XXXX-XXXX-XXXX');
INSERT INTO critical_config VALUES ('max_connections', '1000');
-- 서버 재시작 시 모든 설정 소멸!
```

## 문제점

- 서버 재시작, 장애, OOM 등 어떤 상황에서도 데이터가 소멸됩니다.
- 운영 중 데이터 소멸로 서비스 장애가 발생합니다.

## 올바른 패턴

영구 보존이 필요한 데이터는 LOOKUP 또는 RDB 테이블에 저장합니다.

```sql
-- 올바름: 설정은 LOOKUP 테이블
CREATE LOOKUP TABLE app_config (
    key_name VARCHAR(64) PRIMARY KEY,
    value    VARCHAR(256)
);

INSERT INTO app_config VALUES ('max_connections', '1000');
-- 서버 재시작 후에도 데이터 유지
```

## VOLATILE의 올바른 용도

VOLATILE 테이블은 **재생성 가능한 캐시 데이터**에만 사용합니다.

| 적합 | 부적합 |
|------|--------|
| 센서 최신값 캐시 | 원본 트랜잭션 데이터 |
| 실시간 집계 결과 | 중요 설정 값 |
| 세션 임시 상태 | 감사 로그 |
| 대시보드 캐시 | 사용자 정보 |
