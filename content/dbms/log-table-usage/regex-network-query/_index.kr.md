---
title: '7.12 네트워크 타입 조회'
weight: 120
toc: true
---
네트워크 주소를 `IPV4`·`IPV6` type으로 저장하고 비교하는 방법을 설명합니다. 문자열
`REGEXP`는 [텍스트 검색과 KEYWORD 인덱스](../text-search-keyword-index/#regex)로 이동했습니다.

<a id="design-type-network-data-types"></a>

## 네트워크 데이터 타입

주소를 문자열 정렬로 비교하지 말고 `IPV4` 또는 `IPV6` 컬럼으로 저장합니다. 주소 타입은
동등 비교, `IN`, `BETWEEN`과 NULL 검사를 사용할 수 있습니다.

다음 예제는 두 주소 타입의 조회를 검증하고 객체를 정리합니다.

```sql
CREATE LOG TABLE network_log (
    sensor_id VARCHAR(32),
    message   VARCHAR(128),
    src_ip    IPV4,
    dst_ip    IPV6
);

INSERT INTO network_log
VALUES ('TEMP01', 'ERR-1001 timeout', '192.168.0.10', '2001:db8::10');
INSERT INTO network_log
VALUES ('FLOW02', 'normal', '10.0.0.5', '2001:db8::20');

SELECT sensor_id, src_ip
  FROM network_log
 WHERE src_ip BETWEEN '192.168.0.1' AND '192.168.0.255';

SELECT sensor_id, dst_ip
  FROM network_log
 WHERE dst_ip = '2001:db8::10';

DROP TABLE network_log;
```

### 주소 타입 선택

| 요구사항 | 권장 타입 |
| --- | --- |
| IPv4 주소만 저장 | `IPV4` |
| IPv6 또는 혼합 주소 정책 | `IPV6`와 변환 규칙 검토 |
| 원본 문자열도 보존해야 함 | 주소 타입과 원문 컬럼을 분리 |

IPv4와 IPv6 사이의 암시적 변환에 의존하지 말고 입력 단계에서 형식을 검증하십시오. 출력
문자열 형식이 필요하면 지원되는 변환 함수를 명시적으로 사용합니다.

전체 연산자와 함수는 [SQL 함수 사전](/dbms/reference/sql/dictionary/)을,
전문 검색은 [텍스트 검색과 KEYWORD 인덱스](../text-search-keyword-index/)를 참고하십시오.
