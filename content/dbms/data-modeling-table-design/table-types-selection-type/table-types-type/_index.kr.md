---
type: docs
title: '테이블 타입 개요'
weight: 10
---

## TAG 테이블

센서·IoT 기기에서 수집되는 계측값을 저장하는 타입입니다. 시간축(BASETIME) 또는 거리축(BASE DISTANCE)을 기준으로 다수의 태그(센서 이름)를 하나의 테이블에서 관리합니다.

```sql
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);
```

- `PRIMARY KEY` 컬럼: 태그(센서) 식별자
- `BASETIME` 컬럼: 시간축 (나노초 정밀도 DATETIME)
- 값 컬럼: DOUBLE, INTEGER 등

## LOG 테이블

시스템 이벤트, 애플리케이션 로그, 네트워크 패킷 등 추가 전용(append-only) 데이터에 적합합니다. `CREATE TABLE` 기본 문법을 사용합니다.

```sql
CREATE TABLE sys_log (
    level    SHORT,
    msg      VARCHAR(512),
    src_ip   IPV4
);
```

- `_arrival_time` 컬럼이 자동 추가됩니다 (나노초 DATETIME).
- UPDATE·DELETE 불가, INSERT/APPEND만 가능합니다.

## RDB 테이블

관계형 구조의 업무 데이터를 저장합니다. Machbase 8.6에서 도입된 타입으로, Key-Value 기반 스토리지를 사용합니다.

```sql
CREATE RDB TABLE product (
    id       INTEGER,
    name     VARCHAR(128),
    category VARCHAR(64),
    price    DOUBLE
);
```

- 최소 4개 컬럼 필요
- SELECT, INSERT, DELETE 지원
- UPDATE 미지원
- KV Secondary Index 생성 가능

## VOLATILE 테이블

메모리에만 존재하는 임시 테이블입니다. 서버 재시작 시 데이터가 소멸됩니다.

```sql
CREATE VOLATILE TABLE session_cache (
    id     INTEGER PRIMARY KEY,
    val    VARCHAR(256)
);
```

- `PRIMARY KEY` 필수
- `ON DUPLICATE KEY UPDATE` 지원
- 세션 간 공유 가능 (서버 수준)

## LOOKUP 테이블

소규모 코드 테이블·기준 정보를 저장합니다. 실시간 업데이트가 가능한 참조 데이터에 적합합니다.

```sql
CREATE LOOKUP TABLE code_master (
    code   VARCHAR(16) PRIMARY KEY,
    label  VARCHAR(128)
);
```

- `PRIMARY KEY` 필수
- UPDATE·DELETE by key 지원
- 디스크에 영속 저장
