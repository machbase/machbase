---
title: '7.12 정규식과 네트워크 타입 조회'
weight: 120
toc: true
---
문자열 패턴은 `REGEXP`, 네트워크 주소는 `IPV4`·`IPV6` 타입의 비교 연산으로 조회합니다.
두 기능 모두 먼저 `_arrival_time` 등 선택도가 높은 조건으로 조회 범위를 줄이십시오.

<a id="regex"></a>

## 정규식 검색

<a id="regexp-not"></a>
<a id="regex-regexp-not"></a>

### REGEXP·NOT REGEXP

`REGEXP`는 POSIX 확장 정규 표현식 패턴과 일치하는 행을, `NOT REGEXP`는 일치하지 않는 행을
선택합니다.

```text
string_expression [NOT] REGEXP 'pattern'
```

대표 패턴은 다음과 같습니다.

| 패턴 | 의미 |
| --- | --- |
| `^TEMP` | `TEMP`로 시작 |
| `[0-9]+$` | 하나 이상의 숫자로 끝남 |
| `error\|timeout` | 두 단어 중 하나 포함 |
| `[^0-9]` | 숫자가 아닌 문자 포함 |

<a id="regexp-like"></a>
<a id="regex-regexp-like"></a>

### REGEXP_LIKE

`REGEXP_LIKE(string_expression, pattern)`은 일치하면 `1`, 일치하지 않으면 `0`을 반환하므로
SELECT 목록이나 `CASE` 식에도 사용할 수 있습니다.

```sql
SELECT REGEXP_LIKE('TEMP01', '^TEMP[0-9]+') AS matched;
```

정규식 검색은 넓은 범위를 읽을 수 있습니다. 전문 검색이 목적이라면 KEYWORD 인덱스의
`SEARCH`·`ESEARCH`로 후보를 줄인 뒤 정규식을 적용하는 방식을 검토하십시오.

## 네트워크 데이터 타입

주소를 문자열 정렬로 비교하지 말고 `IPV4` 또는 `IPV6` 컬럼으로 저장합니다. 주소 타입은
동등 비교, `IN`, `BETWEEN`과 NULL 검사를 사용할 수 있습니다.

다음 예제는 정규식과 두 주소 타입의 조회를 한 번에 검증하고 객체를 정리합니다.

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

SELECT sensor_id, message
  FROM network_log
 WHERE message REGEXP 'ERR-[0-9]+|timeout';

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
