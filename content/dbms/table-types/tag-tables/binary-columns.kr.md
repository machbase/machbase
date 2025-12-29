---
title: 'Binary 컬럼'
type: docs
weight: 95
toc: true
---

## 개요

Tag 테이블에서 `BINARY(n)`은 센서 프레임용 고정 길이 바이너리를 저장합니다.
다른 테이블 타입이나 프로토콜에서는 허용되지 않습니다. 길이는 1~32K-1
(1~32767)바이트만 유효하며, 인덱스를 생성할 수 없습니다.

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
- `LENGTH`와 `DESC`는 선언된 바이트 길이(헥스 폭 아님)를 표시합니다.

## 입력 규칙 (공통)

- 입력 형식: 헥스 문자열, `0x` 접두는 선택, 대소문자 무관.
- 홀수 자릿수는 상위 니블을 0으로 패딩(`0xF` → `0x0F`).
- 선언 길이보다 짧으면 뒤를 0x00으로 패딩하고, 길이를 넘으면 오류입니다.
- 잘못된 헥스/길이 초과 시
  `[ERR-02233: Error occurred at column (n): (Invalid insert value.)]`.
- NULL 허용.

```sql
-- frame binary(4)
INSERT INTO t1 VALUES('k1', '2024-01-01', '0x01');        -- 저장: 01 00 00 00
INSERT INTO t1 VALUES('k2', '2024-01-01', '0x0FFF');      -- 저장: 0F FF 00 00
INSERT INTO t1 VALUES('k3', '2024-01-01', '0xFFFFFFFF');  -- OK
INSERT INTO t1 VALUES('k4', '2024-01-01', '0xF');         -- 저장: 0F 00 00 00
INSERT INTO t1 VALUES('k5', '2024-01-01', '0xFFFFFFFFF'); -- 오류: 길이 초과
```

## 출력 및 도구 메모

- machsql은 `0x` 없는 대문자 헥스로 출력하며, 패딩을 포함한 선언 길이에 맞춰
  표시합니다.
- machloader: 스키마에 `BINARY(n)`을 선언하고, 홀수 자릿수는 패딩되며
  비-헥스/길이 초과는 실패합니다.
- REST append: JSON 문자열을 헥스로 디코드하며, 헥스 파싱 실패 시 기존 base64
  경로로 처리합니다.
- CLI/ODBC/Java/C#/Node 드라이버는 고정 길이 버퍼로 송수신하며 메타데이터
  `LENGTH`는 바이트 길이입니다.
