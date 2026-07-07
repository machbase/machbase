---
type: docs
title: '네트워크 데이터 타입 설계'
weight: 50
---

Machbase는 네트워크 데이터를 효율적으로 저장하기 위한 전용 타입을 제공합니다.

## 네트워크 전용 타입

| 타입 | 저장 크기 | 표현 범위 | 입력 형식 |
|------|---------|---------|---------|
| `IPV4` | 4바이트 | IPv4 주소 | `'192.168.1.1'` |
| `IPV6` | 16바이트 | IPv6 주소 | `'2001:db8::1'` |

## IPV4 사용 예시

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

## IPV6 사용 예시

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

## VARCHAR 대비 장점

- **저장 효율**: IPv4는 문자열(최대 15자) 대비 4바이트로 압축
- **비교 연산**: 숫자 비교로 빠른 범위 조회
- **정렬**: IP 주소 순서로 정렬 가능
