---
type: docs
title: '네트워크 데이터 타입 연산자'
weight: 40
---

Machbase는 IPv4 및 IPv6 주소를 전용 데이터 타입으로 저장하고 조회하는 기능을 제공합니다. IP 주소는 내부적으로 이진 형식으로 저장되지만, 조회 시에는 점 표기법(dotted notation) 문자열로 표시됩니다.

## IP 주소 데이터 타입

| 타입 | 설명 | 예시 |
|------|------|------|
| `IPV4` | 32비트 IPv4 주소 | `192.168.1.10` |
| `IPV6` | 128비트 IPv6 주소 | `2001:db8::1` |

### 테이블 생성 예시

```sql
CREATE TABLE network_log (
    ts       DATETIME,
    src_ip   IPV4,
    dst_ip   IPV4,
    src_ipv6 IPV6,
    port     INTEGER
);
```

## NULL 검사 연산자

```sql
-- NULL인 행 조회
SELECT * FROM network_log WHERE src_ip ISNULL;

-- NULL이 아닌 행 조회
SELECT * FROM network_log WHERE src_ip IS NOT NULL;
```

> `ISNULL` 키워드와 표준 `IS NOT NULL` 조건을 사용할 수 있습니다.

## 문자열 리터럴과의 비교

IP 주소를 문자열 리터럴과 비교할 때 자동으로 형변환이 수행됩니다.

```sql
-- 단일 IP 비교
SELECT * FROM network_log
WHERE src_ip = '192.168.1.10';

-- 특정 IP가 아닌 행 조회
SELECT * FROM network_log
WHERE src_ip <> '10.0.0.1';
```

## BETWEEN을 이용한 IP 범위 조회

`BETWEEN` 연산자로 IP 주소 범위를 조회할 수 있습니다. IP 주소의 대소 비교는 이진 표현 기준으로 수행됩니다.

```sql
-- 192.168.1.0/24 서브넷 범위 조회
SELECT * FROM network_log
WHERE src_ip BETWEEN '192.168.1.0' AND '192.168.1.255';

-- 10.x.x.x 대역 조회
SELECT * FROM network_log
WHERE src_ip BETWEEN '10.0.0.0' AND '10.255.255.255';
```

## IN을 이용한 복수 IP 조회

```sql
SELECT * FROM network_log
WHERE src_ip IN ('192.168.1.1', '192.168.1.2', '10.0.0.1');
```

## IPv6 조회 예시

```sql
-- IPv6 단일 주소 비교
SELECT * FROM network_log
WHERE src_ipv6 = '2001:db8::1';

-- IPv6 범위 조회
SELECT * FROM network_log
WHERE src_ipv6 BETWEEN '2001:db8::' AND '2001:db8::ffff';
```

## 문자열로 변환하여 조회

IP 컬럼에는 `LIKE` 연산자를 직접 사용할 수 없습니다. 패턴 매칭이 필요한 경우 `TO_CHAR` 등으로 문자열 변환 후 사용하세요.

```sql
-- LIKE 직접 사용 불가 (오류 발생)
-- SELECT * FROM network_log WHERE src_ip LIKE '192.168.%';  -- 사용 불가

-- 문자열로 변환 후 LIKE 적용
SELECT * FROM network_log
WHERE TO_CHAR(src_ip) LIKE '192.168.%';
```

> 문자열 변환 후 LIKE를 사용하면 인덱스를 활용하지 못합니다. 가능하면 `BETWEEN`으로 범위를 지정하는 것이 성능상 유리합니다.

## 집계 예시

```sql
-- 출발지 IP별 접속 횟수 집계
SELECT src_ip, COUNT(*) AS access_count
FROM network_log
WHERE ts >= NOW - 86400000000000
GROUP BY src_ip
ORDER BY access_count DESC
LIMIT 10;
```
