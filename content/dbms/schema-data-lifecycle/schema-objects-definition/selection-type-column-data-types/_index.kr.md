---
type: docs
title: '컬럼과 데이터 타입 선택'
weight: 30
---

Machbase에서 사용 가능한 컬럼 데이터 타입을 설명합니다.

## 데이터 타입 전체 목록

| 타입 이름 | 설명 | 값 범위 | NULL 값 |
|-----------|------|---------|---------|
| `SHORT` | 16비트 부호 있는 정수 | -32767 ~ 32767 | -32768 |
| `USHORT` | 16비트 부호 없는 정수 | 0 ~ 65534 | 65535 |
| `INTEGER` | 32비트 부호 있는 정수 | -2147483647 ~ 2147483647 | -2147483648 |
| `UINTEGER` | 32비트 부호 없는 정수 | 0 ~ 4294967294 | 4294967295 |
| `LONG` | 64비트 부호 있는 정수 | -9223372036854775807 ~ 9223372036854775807 | -9223372036854775808 |
| `ULONG` | 64비트 부호 없는 정수 | 0 ~ 18446744073709551614 | 18446744073709551615 |
| `FLOAT` | 32비트 부동 소수점 | — | 양수 최대값 |
| `DOUBLE` | 64비트 부동 소수점 | — | 양수 최대값 |
| `DATETIME` | 날짜·시간 (나노초) | 1970-01-01 00:00:00.000:000:000 ~ 2262-04-11 23:47:16.854:775:807 | — |
| `VARCHAR(n)` | 가변 길이 문자열 (UTF-8) | 길이 1 ~ 32768 (32K) | — |
| `IPV4` | IPv4 주소 (4바이트) | "0.0.0.0" ~ "255.255.255.255" | — |
| `IPV6` | IPv6 주소 (16바이트) | "0000:...:0000" ~ "FFFF:...:FFFF" | — |
| `TEXT` | 긴 텍스트 (키워드 인덱스 가능) | 길이 0 ~ 64MB | — |
| `BINARY` | 이진 데이터 | LOG: 0 ~ 64MB / TAG: 1 ~ 32767바이트 | — |
| `JSON` | JSON 문서 | 데이터 최대 32K / 경로 최대 512바이트 | — |

## 숫자형

| 타입 | 크기 | 범위 | 용도 |
|------|------|------|------|
| `SHORT` | 2바이트 | -32,767 ~ 32,767 | 상태 코드, 플래그, 포트 번호 |
| `USHORT` | 2바이트 | 0 ~ 65,534 | 부호 없는 16비트 정수 |
| `INTEGER` (`INT`) | 4바이트 | -2,147,483,647 ~ 2,147,483,647 | 일반 정수값 |
| `UINTEGER` | 4바이트 | 0 ~ 4,294,967,294 | 부호 없는 32비트 정수 |
| `LONG` | 8바이트 | -9,223,372,036,854,775,807 ~ 9,223,372,036,854,775,807 | 대용량 카운터, ID |
| `ULONG` | 8바이트 | 0 ~ 18,446,744,073,709,551,614 | 부호 없는 64비트 정수 |
| `FLOAT` | 4바이트 | 7자리 정밀도 | 저정밀도 실수 |
| `DOUBLE` | 8바이트 | 15자리 정밀도 | 계측값, 금액 |

각 부호 있는 정수 타입(`SHORT`, `INTEGER`, `LONG`)은 C 언어의 해당 정수형과 동일하며, 최소 음수 값이 NULL로 인식됩니다. 부동 소수점 타입(`FLOAT`, `DOUBLE`)은 양수 최대값이 NULL로 인식됩니다. `SHORT`는 `int16`, `INTEGER`는 `int32` 또는 `int`, `LONG`은 `int64`로도 표시될 수 있습니다.

## 문자형

| 타입 | 최대 크기 | 용도 |
|------|---------|------|
| `VARCHAR(n)` | 32,767바이트 | 일반 문자열, 태그 이름, 코드 |
| `TEXT` | 64MB | 전문 검색(SEARCH) 대상 긴 텍스트 |

`VARCHAR`는 실제 저장 데이터 크기만큼만 공간을 사용합니다. 길이 기준은 영문 한 문자 기준이므로 UTF-8 환경에서 실제 문자 수와 다를 수 있습니다. `TEXT`는 키워드 인덱스를 통해 검색할 수 있으며 주로 대용량 텍스트를 별도 컬럼으로 저장하고 검색하는 데 사용됩니다.

## 날짜·시간

| 타입 | 크기 | 용도 |
|------|------|------|
| `DATETIME` | 8바이트 | 나노초 정밀도 날짜·시각 |

`DATETIME`은 1970년 1월 1일 자정 이후 경과된 시간을 나노초 단위로 저장합니다.

```sql
-- 문자열로 삽입
INSERT INTO t1 VALUES ('2024-01-01 12:00:00');
INSERT INTO t1 VALUES ('2024-01-01 12:00:00.123456789');  -- 나노초

-- NOW 함수
INSERT INTO t1 VALUES (NOW);
```

## 네트워크 주소

| 타입 | 크기 | 용도 |
|------|------|------|
| `IPV4` | 4바이트 | IPv4 주소 (`'192.168.1.1'`) |
| `IPV6` | 16바이트 | IPv6 주소 (`'2001:db8::1'`) |

문자열 비교 대비 저장 효율이 높고 범위 비교가 빠릅니다. IPv6는 `:` 기호를 사용하는 축약 표기도 지원합니다 (예: `"::FFFF:1232"`, `"::FFFF:192.168.0.3"`).

## 이진·JSON

| 타입 | 최대 크기 | 용도 |
|------|---------|------|
| `BINARY` | LOG: 64MB / TAG: 32767바이트 | 파형, 이미지 등 이진 데이터 |
| `JSON` | 32KB | JSON 문서 |

### BINARY 타입: LOG vs TAG 차이

- **LOG 테이블**: 이미지나 문서 같은 비정형 데이터를 저장하는 일반 타입으로, 최대 64MB까지 저장할 수 있습니다.
- **TAG 테이블**: `BINARY(n)` 형태의 고정 길이 변형으로, 유효 길이는 1 ~ 32767바이트입니다. SQL에서 `X'...'`, `B'...'`, `O'...'` binary literal을 사용할 수 있으며(소문자 prefix도 지원), 기존 호환성을 위해 `'0x...'` 형태의 문자열 입력도 가능합니다. 선언된 길이를 초과하는 입력은 오류가 발생합니다.
- **LOOKUP / VOLATILE 테이블**: `BINARY` 컬럼을 허용하지 않습니다.

자세한 입력 형식은 [Binary 컬럼](../../table-types/tag-tables/binary-columns/)을 참고하십시오.

## SQL DataType 매핑

다음 표는 Machbase 데이터 타입에 해당하는 SQL 데이터 타입과 C 데이터 타입을 보여줍니다.

| Machbase 타입 | Machbase CLI 타입 | SQL 타입 | C 타입 | C 기본 타입 |
|--------------|------------------|---------|--------|------------|
| `short` | SQL_SMALLINT | SQL_SMALLINT | SQL_C_SSHORT | int16_t (short) |
| `ushort` | SQL_USMALLINT | SQL_SMALLINT | SQL_C_USHORT | uint16_t (unsigned short) |
| `integer` | SQL_INTEGER | SQL_INTEGER | SQL_C_SLONG | int32_t (int) |
| `uinteger` | SQL_UINTEGER | SQL_INTEGER | SQL_C_ULONG | uint32_t (unsigned int) |
| `long` | SQL_BIGINT | SQL_BIGINT | SQL_C_SBIGINT | int64_t (long long) |
| `ulong` | SQL_UBIGINT | SQL_BIGINT | SQL_C_UBIGINT | uint64_t (unsigned long long) |
| `float` | SQL_FLOAT | SQL_REAL | SQL_C_FLOAT | float |
| `double` | SQL_DOUBLE | SQL_FLOAT, SQL_DOUBLE | SQL_C_DOUBLE | double |
| `datetime` | SQL_TIMESTAMP / SQL_TIME | SQL_TYPE_TIMESTAMP / SQL_BIGINT / SQL_TYPE_TIME | SQL_C_TYPE_TIMESTAMP / SQL_C_UBIGINT / SQL_C_TIME | char * (YYYY-MM-DD HH24:MI:SS) / int64_t (나노초) / struct tm |
| `varchar` | SQL_VARCHAR | SQL_VARCHAR | SQL_C_CHAR | char * |
| `ipv4` | SQL_IPV4 | SQL_VARCHAR | SQL_C_CHAR | char * (IP 문자열) / unsigned char[4] |
| `ipv6` | SQL_IPV6 | SQL_VARCHAR | SQL_C_CHAR | char * (IP 문자열) / unsigned char[16] |
| `text` | SQL_TEXT | SQL_LONGVARCHAR | SQL_C_CHAR | char * |
| `binary` | SQL_BINARY | SQL_BINARY | SQL_C_BINARY | char * |
| `json` | SQL_JSON | SQL_JSON | SQL_C_CHAR | json_t |

## 사전 정의 시스템 컬럼

Machbase는 사용자가 직접 정의하지 않아도 내부적으로 관리되는 시스템 컬럼을 제공합니다.

### _ARRIVAL_TIME

LOG 테이블의 모든 행에 자동으로 부여되는 수신 시각 컬럼입니다.

- 타입: `DATETIME` (나노초 정밀도)
- INSERT 시 명시하지 않으면 INSERT 실행 시점의 서버 시각이 자동 부여됩니다.
- `_ARRIVAL_TIME`을 명시하여 삽입할 경우, 지정값이 테이블에 이미 존재하는 가장 최신 `_ARRIVAL_TIME`보다 이전이면 해당 행은 입력되지 않습니다.
- SELECT 쿼리에서 명시적으로 조회하거나 WHERE 조건에 사용할 수 있습니다.

```sql
-- 명시적 삽입
INSERT INTO sensor_log (_arrival_time, sensor_id, value)
VALUES ('2024-01-01 12:00:00', 'TEMP-01', 25.3);

-- 조회
SELECT _arrival_time, sensor_id, value FROM sensor_log;
```

### _RID

각 행에 고유하게 부여되는 내부 행 식별자(Row ID)입니다.

- 타입: `LONG` (자동 증가)
- SELECT 시 명시적으로 조회할 수 있습니다.
- WHERE 조건에서 특정 행을 지정하는 데 사용할 수 있습니다.

```sql
SELECT _rid, sensor_id, value FROM sensor_log WHERE _rid = 1000;
```

## 타입 선택 지침

| 데이터 | 권장 타입 |
|--------|---------|
| 온도, 전압, 유량 등 센서값 | `DOUBLE` |
| IP 주소 | `IPV4` / `IPV6` |
| 포트 번호 (0~65535) | `SHORT` |
| 상태 코드, 플래그 | `SHORT` 또는 `INTEGER` |
| 태그/센서 이름 | `VARCHAR(64~256)` |
| 긴 설명 텍스트 | `TEXT` |
| 날짜·시각 | `DATETIME` |
| 큰 정수 ID, 누적값 | `LONG` |

## 테이블 타입별 타입 제약

| 컬럼 역할 | 제약 |
|---------|------|
| TAG PRIMARY KEY | `VARCHAR(n)` 필수 |
| TAG BASETIME | `DATETIME` 필수 |
| TAG BASE DISTANCE | `DOUBLE`, `LONG`, `ULONG` 중 하나 |
| LOOKUP/VOLATILE PRIMARY KEY | 모든 타입 가능 |
| LOOKUP SEQUENCE | `LONG` 필수 |
