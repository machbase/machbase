---
title: '7.12 정규식과 네트워크 타입 조회'
weight: 120
toc: true
---

<a id="regex"></a>

## 정규식 검색

정규 표현식을 사용한 패턴 검색을 지원합니다.

### 이 절에서 다루는 내용

- **[REGEXP / NOT REGEXP](/dbms/log-table-usage/regex-network-query/#regexp-not)**: 정규식 매칭 연산자
- **[REGEXP_LIKE](/dbms/log-table-usage/regex-network-query/#regexp-like)**: 함수형 정규식 매칭

<a id="regex-regexp-not"></a>

### REGEXP / NOT REGEXP

`REGEXP`는 정규 표현식 패턴으로 컬럼 값을 필터링합니다.

#### 구문

```text
column REGEXP 'pattern'
column NOT REGEXP 'pattern'
```

#### 예시

```sql
-- 'time'을 포함하는 값
SELECT * FROM sensor_log WHERE sensor_id REGEXP 'time';

-- 숫자로 끝나는 sensor_id
SELECT * FROM sensor_log WHERE sensor_id REGEXP 'TEMP[0-9]+';

-- 특정 패턴 NOT REGEXP
SELECT * FROM sensor_log WHERE sensor_id NOT REGEXP 'TEMP[12]';

-- 정확한 패턴 매칭
SELECT 'abcde' REGEXP 'a[bcd]{1,10}e';  -- → 1 (true)

-- 복수 조건 조합
SELECT * FROM event_log
WHERE message REGEXP 'error|timeout'
  AND source REGEXP '^app\\.';
```

#### 성능 주의사항

REGEXP는 인덱스를 사용하지 않으므로 전체 스캔이 발생합니다. 다음 전략으로 범위를 줄이세요.

1. **SEARCH/ESEARCH로 1차 필터링** 후 REGEXP로 정밀 검색:

```sql
-- 1단계: KEYWORD 인덱스로 범위 축소
-- 2단계: 범위가 줄어든 상태에서 REGEXP 적용
SELECT * FROM event_log
WHERE message SEARCH 'error'    -- 인덱스 사용
  AND message REGEXP 'ERR-[0-9]{4}';  -- 정밀 필터
```

2. **시간 범위 먼저 지정**:
```sql
SELECT * FROM event_log
WHERE ts >= NOW - 3600000000000    -- 시간 조건으로 범위 축소
  AND message REGEXP 'CRITICAL.*timeout';
```

#### 지원 정규식 문법

POSIX 확장 정규 표현식(ERE)을 지원합니다.

| 패턴 | 의미 |
|------|------|
| `.` | 임의의 한 문자 |
| `*` | 0회 이상 반복 |
| `+` | 1회 이상 반복 |
| `?` | 0 또는 1회 |
| `[abc]` | a, b, c 중 하나 |
| `[^abc]` | a, b, c가 아닌 문자 |
| `^` | 문자열 시작 |
| `$` | 문자열 끝 |
| `{m,n}` | m~n회 반복 |
| `(abc)` | 그룹 |
| `a\|b` | a 또는 b |

<a id="regex-regexp-like"></a>

### REGEXP_LIKE 함수

`REGEXP_LIKE`는 정규 표현식 매칭 결과를 **숫자값(1/0)**으로 반환합니다. `REGEXP` 연산자는 WHERE 조건에서만 쓸 수 있지만, `REGEXP_LIKE`는 SELECT 목록, CASE 표현식, WHERE 조건 어디서든 사용할 수 있습니다.

#### 구문

```sql
REGEXP_LIKE(string_expr, 'pattern')
```

| 인수 | 설명 |
|------|------|
| `string_expr` | 검사할 문자열 컬럼 또는 표현식 |
| `pattern` | POSIX 확장 정규 표현식(ERE) 패턴 |

- 패턴이 일치하면 `1`, 일치하지 않으면 `0`을 반환합니다.
- `string_expr`이 NULL이면 `NULL`을 반환합니다.

#### REGEXP 연산자와의 비교

| 구분 | `REGEXP` 연산자 | `REGEXP_LIKE` 함수 |
|------|----------------|-------------------|
| 사용 위치 | WHERE 절 전용 | SELECT 목록, CASE, WHERE 등 어디서나 |
| 반환 타입 | 조건 (행 필터) | 정수 (1 또는 0) |
| 사용 목적 | 행 필터링 | 값 계산, 태깅, 분기 |

#### 예시

##### SELECT 목록에서 행 태깅

```sql
-- 각 행에 패턴 일치 여부를 숫자로 부여
SELECT
    sensor_id,
    value,
    REGEXP_LIKE(sensor_id, 'TEMP[0-9]+') AS is_temp_sensor
FROM sensor_log;
```

##### CASE 표현식과 조합

```sql
-- 패턴에 따라 센서 종류를 분류
SELECT
    sensor_id,
    value,
    CASE
        WHEN REGEXP_LIKE(sensor_id, '^TEMP') THEN '온도 센서'
        WHEN REGEXP_LIKE(sensor_id, '^PRESS') THEN '압력 센서'
        WHEN REGEXP_LIKE(sensor_id, '^FLOW') THEN '유량 센서'
        ELSE '기타'
    END AS sensor_type
FROM sensor_log;
```

##### WHERE 절과 함께 사용

```sql
-- WHERE에서도 사용 가능 (REGEXP 연산자와 동일한 효과)
SELECT * FROM sensor_log
WHERE REGEXP_LIKE(sensor_id, 'TEMP[0-9]+');

-- 위 쿼리는 아래와 결과가 같음
SELECT * FROM sensor_log
WHERE sensor_id REGEXP 'TEMP[0-9]+';
```

##### 집계와 조합

```sql
-- 패턴별 행 수 집계
SELECT
    SUM(CASE WHEN REGEXP_LIKE(sensor_id, '^TEMP') THEN 1 ELSE 0 END) AS temp_count,
    SUM(CASE WHEN REGEXP_LIKE(sensor_id, '^PRESS') THEN 1 ELSE 0 END) AS press_count,
    SUM(CASE WHEN REGEXP_LIKE(sensor_id, '^FLOW') THEN 1 ELSE 0 END) AS flow_count
FROM sensor_log
WHERE ts >= NOW - 3600000000000;
```

#### 지원 정규식 문법

`REGEXP` 연산자와 동일한 POSIX ERE 패턴 문법을 사용합니다.

| 패턴 | 의미 |
|------|------|
| `.` | 임의의 한 문자 |
| `*` | 0회 이상 반복 |
| `+` | 1회 이상 반복 |
| `?` | 0 또는 1회 |
| `[abc]` | a, b, c 중 하나 |
| `[^abc]` | a, b, c가 아닌 문자 |
| `^` | 문자열 시작 |
| `$` | 문자열 끝 |
| `{m,n}` | m~n회 반복 |
| `(abc)` | 그룹 |
| `a\|b` | a 또는 b |

#### 성능 주의사항

> `REGEXP_LIKE`는 인덱스를 사용하지 않습니다. 시간 범위나 다른 인덱스 조건을 먼저 적용하여 대상 행 수를 줄인 뒤 사용하세요.

```sql
-- 권장: 시간 조건으로 범위를 먼저 축소
SELECT
    sensor_id,
    REGEXP_LIKE(sensor_id, '^TEMP') AS is_temp
FROM sensor_log
WHERE ts >= NOW - 3600000000000;   -- 인덱스 활용
```

<a id="type-network-data-types-operators"></a>

## 네트워크 데이터 타입 연산자

IPv4 및 IPv6 주소를 전용 데이터 타입으로 저장하고 조회할 수 있습니다. 내부적으로는 이진 형식으로 저장되며, 조회 시에는 점 표기법(dotted notation) 문자열로 표시됩니다.

### IP 주소 데이터 타입

| 타입 | 설명 | 예시 |
|------|------|------|
| `IPV4` | 32비트 IPv4 주소 | `192.168.1.10` |
| `IPV6` | 128비트 IPv6 주소 | `2001:db8::1` |

#### 테이블 생성 예시

```sql
CREATE TABLE network_log (
    ts       DATETIME,
    src_ip   IPV4,
    dst_ip   IPV4,
    src_ipv6 IPV6,
    port     INTEGER
);
```

### NULL 검사 연산자

```sql
-- NULL인 행 조회
SELECT * FROM network_log WHERE src_ip ISNULL;

-- NULL이 아닌 행 조회
SELECT * FROM network_log WHERE src_ip IS NOT NULL;
```

> `ISNULL` 키워드와 표준 `IS NOT NULL` 조건을 사용할 수 있습니다.

### 문자열 리터럴과의 비교

IP 주소와 문자열 리터럴을 비교하면 자동 형변환이 수행됩니다.

```sql
-- 단일 IP 비교
SELECT * FROM network_log
WHERE src_ip = '192.168.1.10';

-- 특정 IP가 아닌 행 조회
SELECT * FROM network_log
WHERE src_ip <> '10.0.0.1';
```

### BETWEEN을 이용한 IP 범위 조회

`BETWEEN`으로 IP 주소 범위를 조회할 수 있습니다. 대소 비교는 이진 표현 기준입니다.

```sql
-- 192.168.1.0/24 서브넷 범위 조회
SELECT * FROM network_log
WHERE src_ip BETWEEN '192.168.1.0' AND '192.168.1.255';

-- 10.x.x.x 대역 조회
SELECT * FROM network_log
WHERE src_ip BETWEEN '10.0.0.0' AND '10.255.255.255';
```

### IN을 이용한 복수 IP 조회

```sql
SELECT * FROM network_log
WHERE src_ip IN ('192.168.1.1', '192.168.1.2', '10.0.0.1');
```

### IPv6 조회 예시

```sql
-- IPv6 단일 주소 비교
SELECT * FROM network_log
WHERE src_ipv6 = '2001:db8::1';

-- IPv6 범위 조회
SELECT * FROM network_log
WHERE src_ipv6 BETWEEN '2001:db8::' AND '2001:db8::ffff';
```

### 문자열로 변환하여 조회

IP 컬럼에 `LIKE` 연산자를 직접 사용할 수는 없습니다. 패턴 매칭이 필요하면 `TO_CHAR`로 문자열 변환 후 적용합니다.

```sql
-- LIKE 직접 사용 불가 (오류 발생)
-- SELECT * FROM network_log WHERE src_ip LIKE '192.168.%';  -- 사용 불가

-- 문자열로 변환 후 LIKE 적용
SELECT * FROM network_log
WHERE TO_CHAR(src_ip) LIKE '192.168.%';
```

> 문자열 변환 후 LIKE를 사용하면 인덱스를 활용하지 못합니다. 가능하면 `BETWEEN`으로 범위를 지정하는 것이 성능상 유리합니다.

### 집계 예시

```sql
-- 출발지 IP별 접속 횟수 집계
SELECT src_ip, COUNT(*) AS access_count
FROM network_log
WHERE ts >= NOW - 86400000000000
GROUP BY src_ip
ORDER BY access_count DESC
LIMIT 10;
```

<a id="original-85-network-type"></a>

## 네트워크 데이터 타입 / 연산자

> **8.5 원문 보강 자료**: 이 문서는 기존 8.5 매뉴얼의 내용을 새 장 구조에 맞춰 보존한 것입니다. Machbase 8.6 기준과 표현이 다른 부분은 같은 절의 최신 리뉴얼 문서를 우선합니다.

네트워크 데이터 타입과 SELECT 문에서 사용 가능한 관련 함수를 지원합니다.

* IPv4 형식: 4바이트 주소 타입
* IPv6 형식: 16바이트 주소 타입
* 네트워크 마스크: IPv4 또는 IPv6에 대한 네트워크 마스크 지정 형식(/ 비트 수)


### IPv4

#### INSERT

```sql
INSERT INTO table_name VALUES (value1,value2,value3,...);
```

```sql
CREATE TABLE addrtable (addr IPV4);
INSERT  INTO addrtable VALUES ('127.0.0.1');
INSERT  INTO addrtable VALUES ('127.0' || '.0.2');
INSERT  INTO addrtable VALUES ('127.0.0.3');
INSERT  INTO addrtable VALUES ('127.0.0.4');
INSERT  INTO addrtable VALUES ('127.0.0.5');
INSERT  INTO addrtable VALUES ('255.255.255.255');
```


#### SELECT

```sql
SELECT  column_name,column_name FROM    table_name;
```

```sql
Mach> SELECT addr FROM addrtable WHERE addr = '127.0.0.3' or addr = '127.0.0.5';
addr
------------------
127.0.0.5
127.0.0.3
[2] row(s) selected.

Mach> SELECT addr FROM addrtable WHERE addr > '127.0.0.3' AND addr < '127.0.0.5';
addr
------------------
127.0.0.4
[1] row(s) selected.

Mach> SELECT addr FROM addrtable WHERE addr <> '127.0.0.3';
addr
------------------
255.255.255.255
127.0.0.5
127.0.0.4
127.0.0.2
127.0.0.1
[5] row(s) selected.

Mach> SELECT addr FROM addrtable WHERE addr = '127.0.0.*';
addr
------------------
127.0.0.5
127.0.0.4
127.0.0.3
127.0.0.2
127.0.0.1
[5] row(s) selected.

Mach> SELECT addr FROM addrtable WHERE addr = '*.0.0.*';
addr
------------------
127.0.0.5
127.0.0.4
127.0.0.3
127.0.0.2
127.0.0.1
[5] row(s) selected.
```

### IPv6

#### INSERT

```sql
INSERT  INTO    table_name  VALUES  (value1,value2,value3,...);
```

```sql
CREATE TABLE addrtable6 (addr ipv6);
INSERT INTO addrtable6 VALUES ('::0.0.0.0');
INSERT INTO addrtable6 VALUES ('::127.0' || '.0.1');
INSERT INTO addrtable6 VALUES ('::127.0.0.3');
INSERT INTO addrtable6 VALUES ('::127.0.0.4');
INSERT INTO addrtable6 VALUES ('21DA:D3:0:2F3B:2AA:FF:FE28:9C5A');
INSERT INTO addrtable6 VALUES ('::FFFF:255.255.255.255');
```

#### SELECT

```sql
SELECT  column_name,column_name FROM    table_name;
```

```sql
Mach> SELECT addr FROM addrtable6 WHERE addr = '::127.0.0.3' or addr = '::127.0.0.5';
addr
---------------------------------------------------------------
::127.0.0.3
[1] row(s) selected.

Mach> SELECT addr FROM addrtable6 WHERE addr > '::127.0.0.3' and addr < '::127.0.0.5';
addr
---------------------------------------------------------------
::127.0.0.4
[1] row(s) selected.

Mach> SELECT addr FROM addrtable6 WHERE addr <> '::127.0.0.3';
addr
---------------------------------------------------------------
::ffff:255.255.255.255
21da:d3::2f3b:2aa:ff:fe28:9c5a
::127.0.0.4
::127.0.0.1
::
[5] row(s) selected.

Mach> SELECT addr FROM addrtable6 WHERE addr >= '21DA::';
addr
---------------------------------------------------------------
21da:d3::2f3b:2aa:ff:fe28:9c5a
[1] row(s) selected.

Mach> SELECT addr FROM addrtable6 order by addr desc;
addr
---------------------------------------------------------------
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.1
::
[6] row(s) selected.
```

### 네트워크 마스크

네트워크 마스크는 특정 주소가 특정 네트워크에 포함되는지 여부를 지정하는 표현 형식입니다. Machbase는 네트워크 마스크 타입 및 관련 연산자를 지원합니다.

#### 마스크 표현 타입

일반적인 네트워크 표현과 같이, 네트워크 주소는 / 기호와 끝에 비트 수로 표현됩니다.

```
'192.128.0.0/16'
'FFFF::192.128.99.0/32'
```

#### 마스크 연산자

**CONTAINS**

이 연산자는 왼쪽에 네트워크 마스크가 있어야 하고 오른쪽에 네트워크 주소 데이터 타입이 있어야 합니다. 즉, 입력 주소가 주어진 네트워크 마스크에 포함되는지 확인합니다. NOT 연산자를 함께 사용할 수 있습니다.

```sql
SELECT addr FROM addrtable  WHERE '192.0.0.0/16'    CONTAINS    addr;
SELECT addr FROM addrtable  WHERE '192.128.99.0/32' NOT CONTAINS    addr;
```

**CONTAINED**

CONTAINS와 반대로, 네트워크 주소가 왼쪽에 있고 네트워크 마스크가 오른쪽에 있습니다. 왼쪽 주소가 오른쪽 마스크의 일부인지 확인합니다.

```sql
SELECT addr FROM addrtable  WHERE addr CONTAINED '192.0.0.0/16';
SELECT addr FROM addrtable  WHERE addr NOT CONTAINED '192.128.99.0/32';
```

#### 마스크 사용 예제

네트워크 마스크 타입을 사용한 검색 예제는 다음과 같습니다.

```sql
CREATE TABLE ip_table (addr4 IPV4, addr6 IPV6);

INSERT INTO ip_table VALUES ('192.0.0.1','FFFF::192.0.0.1');
INSERT INTO ip_table VALUES ('192.0.10.1','FFFF::192.0.10.1');
INSERT INTO ip_table VALUES ('192.128.0.1','FFFF::192.128.0.1');
INSERT INTO ip_table VALUES ('192.128.99.128','FFFF::192.128.99.128');
INSERT INTO ip_table VALUES ('192.128.99.64','FFFF::192.128.99.64');
INSERT INTO ip_table VALUES ('192.128.99.32','FFFF::192.128.99.32');
INSERT INTO ip_table VALUES ('192.128.99.16','FFFF::192.128.99.16');
INSERT INTO ip_table VALUES ('192.128.99.8','FFFF::192.128.99.8');
INSERT INTO ip_table VALUES ('192.128.99.4','FFFF::192.128.99.4');
INSERT INTO ip_table VALUES ('192.128.99.2','FFFF::192.128.99.2');
INSERT INTO ip_table VALUES ('192.128.99.1','FFFF::192.128.99.1');

Mach> SELECT addr4 FROM ip_table WHERE '192.0.0.0/16' CONTAINS addr4;
addr4
-----------
192.0.10.1
192.0.0.1
[2] row(s) selected.

Mach> SELECT addr4 FROM ip_table WHERE '192.128.0.0/16' CONTAINS addr4;
addr4
-----------
192.128.99.1
192.128.99.2
192.128.99.4
192.128.99.8
192.128.99.16
192.128.99.32
192.128.99.64
192.128.99.128
192.128.0.1
[9] row(s) selected.

Mach> SELECT addr4 FROM ip_table WHERE '192.0.10.0/24' CONTAINS addr4;
addr4
--------------------------------------------------------------------
192.0.10.1
[1] row(s) selected.

Mach> SELECT addr4 FROM ip_table WHERE '192.128.99.0/31' CONTAINS addr4;
addr4
-------------------------------------------------------
192.128.99.1
[1] row(s) selected.

Mach> SELECT addr4 FROM ip_table WHERE '192.128.99.0/32' NOT CONTAINS addr4;
addr4
-----------
192.128.99.1
192.128.99.2
192.128.99.4
192.128.99.8
192.128.99.16
192.128.99.32
192.128.99.64
192.128.99.128
192.128.0.1
192.0.10.1
192.0.0.1
[11] row(s) selected.

Mach> SELECT addr4 FROM ip_table WHERE addr4 CONTAINED '192.0.0.0/16';
addr4
-------------------------------------
192.0.10.1
192.0.0.1
[2] row(s) selected.

Mach> SELECT addr4 FROM ip_table WHERE addr4 CONTAINED '192.128.0.0/16';
addr4
-------------------------------------
192.128.99.1
192.128.99.2
192.128.99.4
192.128.99.8
192.128.99.16
192.128.99.32
192.128.99.64
192.128.99.128
192.128.0.1
[9] row(s) selected.

Mach> SELECT addr4 FROM ip_table WHERE addr4 CONTAINED '192.0.10.0/24';
addr4
----------------------------
192.0.10.1
[1] row(s) selected.

Mach> SELECT addr4 FROM ip_table WHERE addr4 not CONTAINED '192.128.99.0/32';
addr4
-------------------------------------------------
192.128.99.1
192.128.99.2
192.128.99.4
192.128.99.8
192.128.99.16
192.128.99.32
192.128.99.64
192.128.99.128
192.128.0.1
192.0.10.1
192.0.0.1
[11] row(s) selected.

Mach> SELECT addr6 FROM ip_table WHERE 'FFFF::192.0.0.0/104' CONTAINS addr6;
addr6
-------------------------------------
ffff::c080:6301
ffff::c080:6302
ffff::c080:6304
ffff::c080:6308
ffff::c080:6310
ffff::c080:6320
ffff::c080:6340
ffff::c080:6380
ffff::c080:1
ffff::c000:a01
ffff::c000:1
[11] row(s) selected.

Mach> SELECT addr6 FROM ip_table WHERE 'FFFF::192.128.0.0/112' CONTAINS addr6;
addr6
------------------------------------
ffff::c080:6301
ffff::c080:6302
ffff::c080:6304
ffff::c080:6308
ffff::c080:6310
ffff::c080:6320
ffff::c080:6340
ffff::c080:6380
ffff::c080:1
[9] row(s) selected.

Mach> SELECT addr6 FROM ip_table WHERE 'FFFF::192.0.10.0/120' CONTAINS addr6;
addr6
------------------------------------------------
ffff::c000:a01
[1] row(s) selected.

Mach> SELECT addr6 FROM ip_table WHERE 'FFFF::192.128.99.0/31' CONTAINS addr6;
addr6
---------------------------------------------
ffff::c080:6301
ffff::c080:6302
ffff::c080:6304
ffff::c080:6308
ffff::c080:6310
ffff::c080:6320
ffff::c080:6340
ffff::c080:6380
ffff::c080:1
ffff::c000:a01
ffff::c000:1
[11] row(s) selected.

Mach> SELECT addr6 FROM ip_table WHERE 'FFFF::192.128.99.0/32' not CONTAINS addr6;
addr6
-------------------------------------
[0] row(s) selected.

Mach> SELECT addr6 FROM ip_table WHERE addr6 CONTAINED 'FFFF::192.0.0.0/104';
addr6
-------------------------------------
ffff::c080:6301
ffff::c080:6302
ffff::c080:6304
ffff::c080:6308
ffff::c080:6310
ffff::c080:6320
ffff::c080:6340
ffff::c080:6380
ffff::c080:1
ffff::c000:a01
ffff::c000:1
[11] row(s) selected.

Mach> SELECT addr6 FROM ip_table WHERE addr6 CONTAINED 'FFFF::192.128.0.0/112';
addr6
-------------------------------------
ffff::c080:6301
ffff::c080:6302
ffff::c080:6304
ffff::c080:6308
ffff::c080:6310
ffff::c080:6320
ffff::c080:6340
ffff::c080:6380
ffff::c080:1
[9] row(s) selected.

Mach> SELECT addr6 FROM ip_table WHERE addr6 CONTAINED 'FFFF::192.0.10.0/120';
addr6
-------------------------------------
ffff::c000:a01
[1] row(s) selected.

Mach> SELECT addr6 FROM ip_table WHERE addr6 not CONTAINED 'FFFF::192.128.99.0/32';
addr6
-------------------------------------
[0] row(s) selected.
```

<a id="design-type-network-data-types"></a>

## 네트워크 데이터 타입 설계

네트워크 데이터를 효율적으로 저장하기 위한 전용 타입을 제공합니다.

### 네트워크 전용 타입

| 타입 | 저장 크기 | 표현 범위 | 입력 형식 |
|------|---------|---------|---------|
| `IPV4` | 4바이트 | IPv4 주소 | `'192.168.1.1'` |
| `IPV6` | 16바이트 | IPv6 주소 | `'2001:db8::1'` |

### IPV4 사용 예시

```sql
CREATE TABLE network_flow (
    src_ip    IPV4,
    dst_ip    IPV4,
    src_port  INTEGER,
    dst_port  INTEGER,
    protocol  SHORT,
    bytes     INTEGER,
    packets   INTEGER
);

-- 삽입
INSERT INTO network_flow VALUES (
    '192.168.1.10', '10.0.0.1',
    54321, 80, 6, 1500, 10
);

-- 특정 서브넷 조회
SELECT * FROM network_flow
WHERE src_ip >= '192.168.1.0' AND src_ip <= '192.168.1.255';

-- IP 범위 조회 (서브넷)
SELECT * FROM network_flow
WHERE src_ip BETWEEN '10.0.0.0' AND '10.255.255.255';
```

### IPV6 사용 예시

```sql
CREATE TABLE ipv6_traffic (
    src_ip  IPV6,
    dst_ip  IPV6,
    bytes   LONG
);

INSERT INTO ipv6_traffic VALUES (
    '2001:db8::1', 'fe80::1', 4096
);
```

### VARCHAR 대비 장점

- **저장 효율**: IPv4는 문자열(최대 15자) 대비 4바이트로 압축
- **비교 연산**: 숫자 비교로 빠른 범위 조회
- **정렬**: IP 주소 순서로 정렬 가능
