---
title: 'Binary 컬럼'
type: docs
weight: 95
toc: true
---

## 개요

Tag 테이블에서 `BINARY(n)`은 센서 프레임용 고정 길이 바이너리 값을 저장합니다.
다른 테이블 타입이나 프로토콜에서는 허용되지 않습니다. 길이는 1~32K-1
(1~32767)바이트만 유효하며, 인덱스를 생성할 수 없습니다.

Machbase SQL에서는 명시적 binary literal로 `BINARY` 값을 입력할 수 있습니다.

## DDL 규칙

```sql
CREATE TAG TABLE t1(
  name VARCHAR(32) PRIMARY KEY,
  time DATETIME BASETIME,
  frame BINARY(4)
);
```

- 유효 길이: `1 <= n <= 32767` (32K-1).
- 범위를 벗어나면 생성 시 오류가 발생합니다(`BINARY(0)` 등).
- `DESC`와 테이블 메타데이터는 선언된 바이트 길이(헥스 폭 아님)를 표시합니다.
  SQL `LENGTH(binary_col)`는 짧은 입력값에 붙은 뒤쪽 0 패딩을 제외한 표시
  값 길이를 반환합니다.

## 지원 입력 형식

```sql
X'hex_digits'
x'hex_digits'
B'bit_digits'
b'bit_digits'
O'octal_digits'
o'octal_digits'
```

| 형식 | 의미 | 단위 |
| --- | --- | --- |
| `X'...'`, `x'...'` | 16진수 literal | 16진수 2자리 = 1바이트 |
| `B'...'`, `b'...'` | 2진수 literal | bit 8자리 = 1바이트 |
| `O'...'`, `o'...'` | 8진수 literal | 8진수 3자리 = 1바이트 |

prefix는 대문자와 소문자를 모두 사용할 수 있습니다.

```sql
CREATE TAG TABLE t_bin (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_bin VALUES('hex1', '2024-01-01 00:00:00', X'0A');
INSERT INTO t_bin VALUES('hex2', '2024-01-01 00:00:01', x'00010203');
INSERT INTO t_bin VALUES('bit1', '2024-01-01 00:00:02', B'00001010');
INSERT INTO t_bin VALUES('oct1', '2024-01-01 00:00:03', O'012');
```

`X'0A'`, `B'00001010'`, `O'012'`는 모두 1바이트 값 `0x0A`를 의미합니다.

## Binary literal 규칙

### 16진수 literal

`X'...'`와 `x'...'`에는 `0-9`, `A-F`, `a-f`를 사용할 수 있습니다.

```sql
X'00'
X'0AFF'
x'abcdef'
```

16진수 문자는 반드시 짝수 개여야 합니다. 두 자리 16진수 문자가 1바이트가 됩니다.

### 2진수 literal

`B'...'`와 `b'...'`에는 `0`과 `1`만 사용할 수 있습니다.

```sql
B'00000000'  -- 0x00
B'00001010'  -- 0x0A
b'11111111'  -- 0xFF
```

bit 수는 반드시 8의 배수여야 합니다. 8자리 bit가 1바이트가 됩니다.

### 8진수 literal

`O'...'`와 `o'...'`에는 `0-7`만 사용할 수 있습니다.

```sql
O'000'  -- 0x00
O'012'  -- 0x0A
o'377'  -- 0xFF
```

8진수 문자는 반드시 3자리 단위여야 합니다. 각 3자리 값은 `000`부터
`377`까지의 1바이트 범위여야 합니다.

### 빈 값

작은따옴표 안을 비워 길이 0인 binary 값을 표현할 수 있습니다.

```sql
X''
B''
O''
```

## 길이 제한

`BINARY(n)` 컬럼에는 최대 `n`바이트까지만 입력할 수 있습니다.

```sql
CREATE TAG TABLE t_limit (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(2)
);

INSERT INTO t_limit VALUES('ok_hex', '2024-01-01 00:00:00', X'0AFF');
INSERT INTO t_limit VALUES('ok_bit', '2024-01-01 00:00:01', B'0000101011111111');
INSERT INTO t_limit VALUES('ok_oct', '2024-01-01 00:00:02', O'012377');

INSERT INTO t_limit VALUES('bad_hex', '2024-01-01 00:00:03', X'000102'); -- 실패: 3바이트
```

source 종류와 무관하게 최종 binary 값이 대상 `BINARY(n)` 길이를 초과하면
입력은 실패합니다. 이 규칙은 binary literal뿐 아니라 일반 문자열, 기존
`'0x...'` 문자열 입력, 다른 `BINARY` 컬럼 값을 `INSERT ... SELECT`로
복사하는 경우에도 동일하게 적용됩니다.

```sql
CREATE TAG TABLE t_src (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(8)
);

CREATE TAG TABLE t_dst (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_src VALUES('k1', '2024-01-01 00:00:00', X'0102030405060708');
INSERT INTO t_dst SELECT name, time, value FROM t_src; -- 실패: 8바이트 값을 BINARY(4)에 입력
```

`CASE`, `INSERT ... SELECT`, view 등 SQL expression 안에서 사용하더라도
최종 binary 값이 대상 `BINARY(n)` 길이를 초과하면 입력은 실패합니다.

## 올바르지 않은 입력

다음 입력은 유효하지 않습니다.

```sql
X'0'        -- 16진수 문자가 홀수 개
X'0G'       -- G는 16진수 문자가 아님
B'0101'     -- bit 수가 8의 배수가 아님
B'00000002' -- 2는 2진수 문자가 아님
O'12'       -- 8진수 문자가 3자리 단위가 아님
O'400'      -- 1바이트 범위 초과
X'0102      -- 닫는 작은따옴표가 없음
```

잘못된 값이나 길이 초과 입력은 다음 오류로 실패합니다.

```text
[ERR-02233: Error occurred at column (n): (Invalid insert value.)]
```

## 기존 문자열 입력과의 차이

기존 호환성을 위해 문자열 형태의 `'0x...'` 입력은 계속 사용할 수 있습니다.
다만 `'0x...'`는 문자열 literal에서 `BINARY` 컬럼으로 변환되는 방식이고,
`X'...'`, `B'...'`, `O'...'`는 SQL 문장에서 binary 값임을 명확히 표시하는
binary literal입니다.

일반 문자열을 `BINARY(n)` 컬럼에 입력할 수도 있지만, 문자열 byte 길이가 `n`을
초과하면 실패합니다. 새 SQL을 작성할 때는 의미가 명확한 binary literal 형식을
권장합니다.

`'0b...'`, `'0o...'`, 따옴표 없는 `0x...`, `0b...`, `0o...` 형식은
binary literal로 지원하지 않습니다.

## 출력 및 도구 메모

- machsql은 `0x` 없는 대문자 헥스로 출력합니다. 짧은 입력값에 붙은 뒤쪽
  0 패딩은 텍스트 출력에 표시되지 않습니다.
- machloader: 스키마에 `BINARY(n)`을 선언하고, 잘못된 값이나 길이 초과는
  실패합니다.
- REST append: JSON 문자열을 헥스로 디코드하며, 헥스 파싱 실패 시 기존 base64
  경로로 처리합니다.
- CLI/ODBC/Java/C#/Node 드라이버는 고정 길이 버퍼로 송수신하며 메타데이터
  `LENGTH`는 바이트 길이입니다.
