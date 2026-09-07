---
title: '7.12 네트워크 타입 조회'
weight: 120
toc: true
---

IP 주소를 문자열로 보관하면 눈으로 읽기는 편하지만, 문자열 정렬과 주소 범위의 순서가
같다고 가정하기 쉽습니다. 주소 비교가 목적이라면 IPV4·IPV6 타입을 사용하고,
원문 표기까지 필요할 때만 별도 문자열을 함께 보관하세요.

<a id="design-type-network-data-types"></a>

## 범위의 양 끝과 NULL을 함께 준비합니다

```sql
CREATE LOG TABLE ch7_network (
    event_id INTEGER,
    src_ip   IPV4,
    dst_ip   IPV6,
    dst_port INTEGER
);
INSERT INTO ch7_network VALUES (1, '192.0.2.1',   '2001:db8::1', 80);
INSERT INTO ch7_network VALUES (2, '192.0.2.255', '2001:db8::2', 65535);
INSERT INTO ch7_network VALUES (3, '198.51.100.1', '2001:db8::3', 443);
INSERT INTO ch7_network VALUES (4, NULL, NULL, NULL);

SELECT event_id, src_ip, dst_ip, dst_port FROM ch7_network ORDER BY event_id;
```

네 행이 조회됩니다. 포트는 INTEGER를 사용합니다.
USHORT의 최댓값 65535는 NULL 예약값이므로 포트 전체 범위를 그대로 표현하기에 맞지 않습니다.

## 동등 비교와 범위 조회를 구분합니다

```sql
SELECT event_id FROM ch7_network
 WHERE src_ip BETWEEN '192.0.2.1' AND '192.0.2.255'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE src_ip IN ('192.0.2.1', '198.51.100.1')
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE dst_ip = '2001:db8::2'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE dst_ip BETWEEN '2001:db8::1' AND '2001:db8::2'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE src_ip IS NULL
 ORDER BY event_id;
```

| 조건 | 선택되는 event_id |
|---|---|
| IPv4 BETWEEN | 1, 2 |
| IPv4 IN | 1, 3 |
| IPv6 동등 비교 | 2 |
| IPv6 BETWEEN | 1, 2 |
| IPv4 IS NULL | 4 |

BETWEEN은 양 끝 주소를 포함합니다. 이 예제의 IPv4 범위는 CIDR 대역의 의미를
자동 적용한 것이 아니라, 직접 지정한 두 주소 사이의 범위입니다.
NULL은 `= NULL`이 아니라 `IS NULL`로 검사하세요.

## 혼합 주소와 원본 표기 정책을 먼저 정하세요

IPv4만 들어오면 IPV4로, IPv6가 들어오면 IPV6로 스키마를 정합니다.
두 종류를 함께 다루는 경우에는 입력 변환·컬럼 분리 정책을 먼저 정하고 실제 표본으로
검증하세요. 암시적 변환이 원본 주소를 항상 의도대로 정규화해 줄 것이라고 가정하지 마세요.

실수하기 쉬운 부분은 출력 문자열입니다. 같은 IPv6 주소라도 원문 압축 표기와 조회 결과의
표기가 다를 수 있습니다. 원문을 증빙으로 남겨야 한다면 주소 타입 컬럼과 원문 컬럼을
분리하는 편이 명확합니다.

대량 데이터에서는 주소 조건과 함께 `_arrival_time` 범위를 제한하고 실행 계획을
확인하세요. 메시지의 정규식 검색은
[텍스트 검색](../text-search-keyword-index/#regex)과
[SQL 함수 사전](/dbms/reference/sql/dictionary/)에서 이어서 살펴볼 수 있습니다.

```sql
DROP TABLE ch7_network;
```

주소 조회가 예상과 다르면 원본 문자열, 입력 타입, 범위의 양 끝부터 나란히 비교해 보세요.
문자열 표현의 차이인지 실제 주소 범위의 차이인지 구분하기 쉬워집니다.
