---
title: '10.7 운영과 데이터 생명주기'
weight: 70
toc: true
---

VOLATILE 테이블의 운영과 데이터 생명주기를 다룬다. VOLATILE 테이블의 데이터는 메모리에만 존재하므로, 생성·적재·사용·소멸·재구성 흐름을 운영 절차에 포함해야 한다.

<a id="operations-volatile-lifecycle"></a>

## 데이터 생명주기

VOLATILE 테이블은 서버가 실행 중일 때만 데이터를 유지한다.

```
서버 시작
  └── VOLATILE 테이블 생성
        └── 초기 데이터 적재
              └── INSERT / UPDATE / DELETE / UPSERT
                    └── 서버 종료 또는 재시작 → 데이터 소멸
```

테이블 정의와 초기 적재 SQL은 운영 스크립트로 관리한다.

```bash
machsql -u SYS -p MANAGER -f /etc/machbase/volatile_startup.sql
```

```sql
CREATE VOLATILE TABLE sensor_latest (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);
```

<a id="operations-volatile-session-scope"></a>

## 세션 공유와 접근

VOLATILE 테이블은 세션 전용 임시 테이블이 아니라 서버 수준에서 공유되는 테이블이다. 한 세션에서 입력한 데이터는 다른 세션에서도 조회할 수 있다.

```sql
-- 세션 A
INSERT INTO sensor_latest VALUES ('TEMP-01', 25.3, NOW);

-- 세션 B
SELECT *
FROM sensor_latest
WHERE sensor_id = 'TEMP-01';
```

여러 애플리케이션이 같은 VOLATILE 테이블을 갱신하면 PRIMARY KEY 기준의 UPSERT 패턴을 사용해 중복 입력을 처리한다.

<a id="operations-volatile-flush"></a>

## 영속 테이블로 플러시

보존이 필요한 데이터는 주기적으로 LOG, TAG, RDB 등 영속 테이블에 복사한다.

```sql
INSERT INTO sensor_latest_history
SELECT sensor_id, value, updated_at
FROM sensor_latest;
```

원본 TAG 테이블에서 최신 상태를 다시 만들 수 있다면, VOLATILE 테이블에는 최신 캐시만 보관하고 원본은 TAG 테이블에 유지한다.

<a id="operations-volatile-restart"></a>

## 재시작 대응

서버 재시작 후에는 VOLATILE 테이블과 데이터가 모두 사라진다. 운영 절차에는 다음 작업을 포함한다.

1. VOLATILE 테이블 생성 SQL 실행
2. 영속 테이블에서 초기 데이터 적재
3. 애플리케이션 캐시 갱신 또는 수집 재개
4. 데이터 건수와 최신 시각 확인

```sql
INSERT INTO sensor_latest
SELECT name, value, time
FROM sensor_data
WHERE time >= NOW - 60000000000;
```

초기 적재 쿼리는 원본 데이터의 구조와 최신값 판정 기준에 맞춰 작성한다.

<a id="operations-volatile-checklist"></a>

## 운영 체크리스트

- VOLATILE 테이블에는 재생성 가능한 데이터만 저장한다.
- 서버 시작 시 생성·초기 적재 스크립트를 자동 실행할 수 있게 준비한다.
- 예상 행 수와 메모리 사용량을 주기적으로 확인한다.
- 중요 데이터는 영속 테이블로 플러시한다.
- 재시작 후 데이터가 비어 있는 상태를 애플리케이션이 처리할 수 있어야 한다.
